"""Unit tests for the local-AI page: `scripts/32_local.py`, `scripts/localfit.py` / `localfit.js`, and
`config/local-ai/`.

What this file holds, and why each is here rather than in the browser check:

  the data      -- `validate()` passes the committed catalogue and picks, and refuses each kind of entry that
                   would make the page give a wrong answer confidently: a device naming a GPU that is not
                   there, a model with no size for its default quant, a missing runner name, a duplicate id.
                   The refusals are the point; a validator that only ever said yes is not tested by the
                   committed data passing it.
  the maths     -- the two copies of the fit method agree. `localfit.js` is run under Node over a grid of
                   machines x models x contexts and compared number for number with `localfit.py`, because
                   the page answers with one and the no-script cheat sheet with the other, and a reader who
                   sees both must not see two answers. Plus the properties any correct method has, whatever
                   ds-models' final constants are: more memory never makes a model fit worse, a longer
                   context never needs less, a mixture-of-experts model is faster than a dense one of the
                   same file size, and every verdict comes with the fields its card prints.
  the page      -- the generated HTML carries the name from its one constant, inlines the data and both
                   scripts, writes colour only as custom properties, and has the no-script cheat sheet.
  the wiring    -- the stage is in both workflows before `20_landing.py`, and its URL is in the sitemap.

Run: python tests/local_test.py
"""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import localfit  # noqa: E402
import sitewide  # noqa: E402

spec = importlib.util.spec_from_file_location("b32", SCRIPTS / "32_local.py")
b32 = importlib.util.module_from_spec(spec)
sys.modules["b32"] = b32
spec.loader.exec_module(b32)

ok = bad = 0


def check(name, got, want):
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name, got, detail=""):
    check(name + (f" [{detail}]" if detail and not got else ""), bool(got), True)


CAT, PICKS = b32.load()
RULES = CAT["usable"]
MODELS = {m["id"]: m for m in PICKS["models"]}


# ---------------------------------------------------------------- the data
def refuses(name, mutate, needle):
    cat, picks = copy.deepcopy(CAT), copy.deepcopy(PICKS)
    mutate(cat, picks)
    try:
        b32.validate(cat, picks)
    except b32.Bad as e:
        true(f"refuses {name}", needle in str(e), str(e))
        return
    true(f"refuses {name}", False, "it was accepted")


b32.validate(CAT, PICKS)
true("the committed catalogue and picks validate", True)
refuses("a device naming a GPU the catalogue lacks",
        lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], gpu="rtx-9999")), "rtx-9999")
refuses("a device with a graphics card and no VRAM",
        lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], gpu=c["gpus"][0]["id"], vram_gb=0)), "no memory")
refuses("a duplicate device id", lambda c, p: c["devices"].append(dict(c["devices"][0])), "twice")
refuses("a duplicate GPU id", lambda c, p: c["gpus"].append(dict(c["gpus"][0])), "twice")
refuses("a device of an unknown kind",
        lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], kind="toaster")), "toaster")
refuses("a device with an unknown OS",
        lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], os=["beos"])), "beos")
refuses("a device missing a contract field",
        lambda c, p: c["devices"][0].pop("bw_gbs"), "bw_gbs")
refuses("a device with no RAM sizes",
        lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], ram_gb_options=[])), "no RAM")
refuses("a missing usable-memory rule", lambda c, p: c["usable"].pop("vram_reserve_gb"), "vram_reserve_gb")
refuses("an OS with no find-out steps", lambda c, p: c["find_out"].pop("steamos"), "steamos")
refuses("a model with no size for its default quant",
        lambda c, p: p["models"].__setitem__(0, dict(p["models"][0], default_q="Q9_X")), "Q9_X")
refuses("a model with a zero-size quant",
        lambda c, p: p["models"][0]["quants"][0].__setitem__("gb", 0), "no size")
refuses("a model with more active parameters than parameters",
        lambda c, p: p["models"].__setitem__(0, dict(p["models"][0], active_b=999)), "active_b")
refuses("a model with no Ollama tag",
        lambda c, p: p["models"][0]["run"].pop("ollama"), "Ollama")
refuses("a model with an unknown task",
        lambda c, p: p["models"].__setitem__(0, dict(p["models"][0], tasks=["juggle"])), "juggle")
refuses("a duplicate model id", lambda c, p: p["models"].append(dict(p["models"][0])), "twice")

kinds = {k["id"] for k in CAT["kinds"]}
check("the six tiles the UX plan names", kinds, {"laptop", "mac", "gaming", "desktop", "handheld", "minipc"})
for k in kinds - {"gaming"}:
    true(f"the {k} tile has at least one device to pick", any(d["kind"] == k for d in CAT["devices"]))
true("every kind with devices has a popular one to offer as a chip",
     all(any(d.get("popular") and d["kind"] == k for d in CAT["devices"])
         for k in kinds if any(d["kind"] == k for d in CAT["devices"])))
for t in PICKS["tasks"]:
    true(f"the task {t['id']!r} has at least one model", any(t["id"] in m["tasks"] for m in PICKS["models"]))
true("there is a model small enough for an 8 GB laptop with no graphics card",
     any(localfit.fit(b32.CHEAT[0][1], m, None, RULES)["verdict"] != "no" for m in PICKS["models"]))


# ---------------------------------------------------------------- the maths, Python against JavaScript
MACHINES = [m for _, m in b32.CHEAT] + [
    {"ram_gb": 4, "vram_gb": 0, "unified": False, "backend": "cpu", "gpu_bw_gbs": 0, "cpu_bw_gbs": 17},
    {"ram_gb": 8, "vram_gb": 6, "unified": False, "backend": "cuda", "gpu_bw_gbs": 192, "cpu_bw_gbs": 80},
    {"ram_gb": 64, "vram_gb": 0, "unified": True, "backend": "metal", "gpu_bw_gbs": 400, "cpu_bw_gbs": 400},
    {"ram_gb": 24, "vram_gb": 0, "unified": True, "backend": "vulkan", "gpu_bw_gbs": 128, "cpu_bw_gbs": 128},
]
CTXS = [4096, 8192, 32768, 131072]
cases = [{"m": m, "model": model, "opts": {"ctx": c}} for m in MACHINES for model in PICKS["models"] for c in CTXS]
cases += [{"m": MACHINES[6], "model": model, "opts": {"ctx": 8192, "quant": q["q"]}}
          for model in PICKS["models"] for q in model["quants"]]

node = shutil.which("node")
if not node:
    true("node is on PATH, for the JavaScript half of the parity check", False)
else:
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "cases.json").write_text(json.dumps({"cases": cases, "rules": RULES}), encoding="utf-8")
        runner = Path(tmp) / "run.js"
        runner.write_text(
            (SCRIPTS / "localfit.js").read_text(encoding="utf-8") +
            "\nconst I = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));\n"
            "const out = I.cases.map((c) => LOCALFIT.fit(c.m, c.model, c.opts, I.rules));\n"
            "const words = [0.5, 1.99, 2, 5.9, 6, 14.9, 15, 39, 40, 500].map(LOCALFIT.speedWords);\n"
            "process.stdout.write(JSON.stringify({out, words}));\n", encoding="utf-8")
        res = subprocess.run([node, str(runner), str(Path(tmp) / "cases.json")], capture_output=True, text=True)
    true("localfit.js runs under Node", res.returncode == 0, res.stderr[:400])
    if res.returncode == 0:
        js = json.loads(res.stdout)

        def same(a, b, path=""):
            """Equal to 1e-9, by key, recursively: the shape is part of the contract too."""
            if isinstance(a, dict) and isinstance(b, dict):
                if set(a) != set(b):
                    return f"{path}: keys {sorted(set(a) ^ set(b))} differ"
                for k in a:
                    r = same(a[k], b[k], f"{path}.{k}")
                    if r:
                        return r
                return ""
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                if len(a) != len(b):
                    return f"{path}: lengths {len(a)} vs {len(b)}"
                for i, (x, y) in enumerate(zip(a, b)):
                    r = same(x, y, f"{path}[{i}]")
                    if r:
                        return r
                return ""
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
                return "" if abs(a - b) <= 1e-9 * max(1, abs(a)) else f"{path}: {a} vs {b}"
            return "" if a == b else f"{path}: {a!r} vs {b!r}"

        first = ""
        for c, j in zip(cases, js["out"]):
            py = localfit.fit(c["m"], c["model"], c["opts"], RULES)
            first = same(py, j)
            if first:
                first = f"{c['model']['id']} on {c['m']} at {c['opts']}: {first}"
                break
        true(f"Python and JavaScript agree on all {len(cases)} fits, key for key and to 1e-9", not first, first)
        check("...and on the speed words at every band edge",
              js["words"], [localfit.speed_words(x) for x in [0.5, 1.99, 2, 5.9, 6, 14.9, 15, 39, 40, 500]])


# ---------------------------------------------------------------- the maths, properties
def fit(m, mid, **o):
    return localfit.fit(m, MODELS[mid], o or None, RULES)


RANK = {"no": 0, "ok": 1, "great": 2}
mono = []
for model in PICKS["models"]:
    for base in MACHINES:
        prev = None
        for ram in (8, 16, 24, 32, 48, 64, 96, 128):
            r = localfit.fit(dict(base, ram_gb=ram), model, {"ctx": 8192}, RULES)
            if prev is not None and r["verdict"] == "no" and prev != "no":
                mono.append(f"{model['id']} on {base['backend']} {ram} GB")
            prev = r["verdict"]
check("more RAM never turns a model that fits into one that does not", mono, [])
grow = [m["id"] for m in PICKS["models"]
        if not localfit.need(m, m["quants"][0], 4096)["total"] < localfit.need(m, m["quants"][0], 32768)["total"]]
check("a longer context always needs more memory", grow, [])
q30 = MODELS["qwen3-30b-a3b"]
dense = dict(q30, active_b=q30["params_b"])
big = MACHINES[-2]
moe_t = localfit.fit(big, q30, None, RULES)["tps"][1]
dense_t = localfit.fit(big, dense, None, RULES)["tps"][1]
true("a mixture-of-experts model is faster than a dense one of the same size", moe_t > 3 * dense_t,
     f"{moe_t:.1f} vs {dense_t:.1f}")
r = fit(b32.CHEAT[7][1], "qwen3-32b")
check("a model bigger than the graphics card but within card + RAM is split (offload)", r["place"], "split")
true("...and says so as a catch", "split" in r["catches"])
true("...with the share on the card between 0 and 1", 0 < r["gpu_frac"] < 1, str(r["gpu_frac"]))
r = fit(b32.CHEAT[0][1], "llama-3.3-70b")
check("a 70B model does not fit an 8 GB laptop", r["verdict"], "no")
true("...and a no carries the need and the budget a card prints", r["need"]["total"] > r["have"] > 0)
check("...and no speed", r["tps"], None)
r = fit(b32.CHEAT[3][1], "qwen3-8b")
check("an 8B model runs great on a 16 GB Mac", r["verdict"], "great")
check("...all in shared memory", r["place"], "gpu")
check("...at the default quant", (r["quant"], r["smaller"]), ("Q4_K_M", False))
true("...with a speed range that brackets its middle", r["tps"][0] < r["tps"][1] < r["tps"][2])
apple16 = localfit.budget(b32.CHEAT[3][1], RULES)["gpu"]
true("a 16 GB Mac offers about two-thirds of its memory, not all of it", 10 < apple16 < 11.5, str(apple16))
r = fit(b32.CHEAT[0][1], "qwen3-8b")
true("on an 8 GB laptop with no card an 8B model is squeezed or refused, never offered at full size",
     r["verdict"] == "no" or r["smaller"], str(r["verdict"]))
r = fit(b32.CHEAT[3][1], "qwen3-8b", ctx=8192, quant="Q8_0")
check("a forced quant is the one fitted", r["quant"], "Q8_0")
for v in ("great", "ok", "no"):
    true(f"some machine in the grid gets a {v!r} for some model",
         any(localfit.fit(m, model, None, RULES)["verdict"] == v for m in MACHINES for model in PICKS["models"]))


# ---------------------------------------------------------------- the page
HF = {}
html = b32.render(CAT, PICKS, HF)
true("the page names itself from sitewide.LOCAL_PAGE", f"<p class=\"kick\">{sitewide.LOCAL_PAGE['title']}</p>" in html)
check("the stage's PAGE is that constant, not a copy", b32.PAGE is sitewide.LOCAL_PAGE, True)
check("its URL is the slug", b32.urls("https://x/"), ["https://x/" + sitewide.LOCAL_PAGE["slug"] + "/"])
m = re.search(r'<script type="application/json" id="lxdata">(.*?)</script>', html, re.S)
true("the data is inlined as one JSON block", m)
if m:
    data = json.loads(m.group(1))
    check("...carrying every device, card and model", (len(data["devices"]), len(data["gpus"]), len(data["models"])),
          (len(CAT["devices"]), len(CAT["gpus"]), len(PICKS["models"])))
    check("...and the usable-memory rules the maths reads", data["usable"], RULES)
    check("...and how-to steps for both beginner routes on all four OSes",
          [sorted(data["howto"][k]["steps"]) for k in ("lmstudio", "ollama")],
          [sorted(b32.OSES)] * 2)
true("the fit maths is inlined", "const LOCALFIT = (() => {" in html)
true("the page script is inlined", "const LOCALUI = ((D, FIT) => {" in html)
true("no `</script>` inside the JSON can close it early", "</" not in (m.group(1) if m else "x"))
style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
check("the page's own CSS writes no colour literal: every colour is a site token",
      re.findall(r"#[0-9a-fA-F]{3,8}\b|\brgb\((?!0,0,0,)", style), [])
true("...and has a forced-colors block for high-contrast mode", "@media (forced-colors:active)" in style)
true("...and keeps motion behind prefers-reduced-motion", "prefers-reduced-motion:no-preference" in style)
true("the no-script reader gets the cheat sheet as a real table", '<table class="lxcheat">' in html and
     html.count('<th scope="row">') == len(b32.CHEAT))
true("...and a note saying the picker needs script", "<noscript>" in html)
true("every explainer the cards link to exists",
     all(f'id="{x}"' in html for x in ("q-quant", "q-ctx", "q-offload", "q-unified", "q-tokens")))
true("the picker is an ARIA combobox with a listbox", 'role="combobox"' in html and 'role="listbox"' in html)
true("results are announced politely", 'aria-live="polite"' in html)
true("the fixture banner shows while the data is a fixture",
     ("lxfix" in html) == bool(CAT.get("fixture") or PICKS.get("fixture")))
true("the page links the site stylesheet and the shared tail", "../pages.css" in html and "btags" in html)

js = (SCRIPTS / "local_page.js").read_text(encoding="utf-8")
if node:
    res = subprocess.run([node, "--check", str(SCRIPTS / "local_page.js")], capture_output=True, text=True)
    true("local_page.js parses", res.returncode == 0, res.stderr[:300])
true("the page script writes no colour either", not re.search(r"#[0-9a-fA-F]{6}\b", js))

hf_rows = {"models": [{"id": "Qwen/Qwen3-8B", "likes": 10, "downloads": 99, "last_modified": "2026-11-01", "x": 1},
                      {"id": "nobody/else", "likes": 1}]}
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "models.json"
    check("with no Hugging Face index the join is empty, not an error", b32.hf_join(PICKS, p), {})
    p.write_text(json.dumps(hf_rows), encoding="utf-8")
    check("with one, picks join on hf_id and take only the freshness facts",
          b32.hf_join(PICKS, p), {"Qwen/Qwen3-8B": {"likes": 10, "downloads": 99, "last_modified": "2026-11-01"}})
    p.write_text("not json", encoding="utf-8")
    try:
        b32.hf_join(PICKS, p)
        true("an index that is there but broken stops the build", False)
    except ValueError:
        true("an index that is there but broken stops the build", True)


# ---------------------------------------------------------------- the wiring
STAGE = "python scripts/32_local.py"
for wf in ("daily.yml", "weekly.yml"):
    lines = [ln.strip() for ln in (ROOT / ".github" / "workflows" / wf).read_text(encoding="utf-8").splitlines()]
    true(f"{wf} runs the stage", STAGE in lines)
    if STAGE in lines and "python scripts/20_landing.py" in lines:
        true(f"...before 20_landing in {wf}, which puts its URL in the sitemap",
             lines.index(STAGE) < lines.index("python scripts/20_landing.py"))
landing = (SCRIPTS / "20_landing.py").read_text(encoding="utf-8")
true("20_landing.py asks this stage for its URLs", "def local_urls()" in landing and "+ local)" in landing)
sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
url = b32.urls(b32.SITE)[0]
true("the committed sitemap names the page", f"<loc>{url}</loc>" in sitemap)
true("the committed page exists", (ROOT / "docs" / sitewide.LOCAL_PAGE["slug"] / "index.html").exists())
for f in ("31_home.py", "20_landing.py", "19_pages.py", "19d_discover.py", "25_collections.py"):
    true(f"{f}'s nav links the page by the shared constant", "LOCAL_PAGE" in (SCRIPTS / f).read_text(encoding="utf-8"))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
