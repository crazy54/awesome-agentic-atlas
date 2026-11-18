"""Unit tests for the local-AI page: `scripts/32_local.py`, the vendored fit method `scripts/localfit.mjs`, and
`config/local-ai/`.

What this file holds, and why each is here rather than in the browser check:

  the data      -- `validate()` passes the committed catalogue and picks, and refuses each kind of entry that
                   would make the page give a wrong answer confidently: a device naming a GPU that is not
                   there, a quant with no size, no size for the quant Ollama's tag ships, a missing runner
                   name, missing model geometry, a duplicate id. The refusals are the point; a validator that
                   only ever said yes is not tested by the committed data passing it.
  the maths     -- not its correctness, which is ds-models' and has its own 46 checks and calibration gate in
                   `team/local-ai/fit/test.mjs`, but the two things this repository does to it: the inlining
                   (every export of the module reaches `LOCALFIT`, and the wrapped script answers exactly what
                   the module answers, over every pick on every cheat-sheet machine), and the build-time run
                   that writes the cheat sheet. Plus the properties the page's copy leans on: more memory never
                   gives a worse verdict, a 70B model does not fit an 8 GB laptop and does fit a 128 GB Mac,
                   and an 8B model runs on a 16 GB Mac.
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
node = shutil.which("node")


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


def dev(c, **kw):
    c["devices"][0] = dict(c["devices"][0], **kw)


def mod(p, **kw):
    p["models"][0] = dict(p["models"][0], **kw)


b32.validate(CAT, PICKS)
true("the committed catalogue and picks validate", True)
refuses("a device naming a GPU the catalogue lacks", lambda c, p: dev(c, gpu="rtx-9999", igpu=None), "rtx-9999")
refuses("a device with a graphics card and no VRAM",
        lambda c, p: dev(c, gpu=c["gpus"][0]["id"], vram_gb=0, igpu=None), "no memory")
refuses("a device with both a graphics card and a shared-memory GPU",
        lambda c, p: dev(c, gpu=c["gpus"][0]["id"], vram_gb=8, igpu={"vendor": "apple"}), "both")
refuses("a shared-memory GPU on a machine that is not unified",
        lambda c, p: dev(c, unified=False, igpu={"vendor": "amd"}), "not unified")
refuses("a duplicate device id", lambda c, p: c["devices"].append(dict(c["devices"][0])), "twice")
refuses("a duplicate GPU id", lambda c, p: c["gpus"].append(dict(c["gpus"][0])), "twice")
refuses("a GPU from an unknown vendor", lambda c, p: c["gpus"].__setitem__(0, dict(c["gpus"][0], vendor="3dfx")), "3dfx")
refuses("a device of an unknown kind", lambda c, p: dev(c, kind="toaster"), "toaster")
refuses("a device with an unknown OS", lambda c, p: dev(c, os=["beos"]), "beos")
refuses("a device missing a contract field", lambda c, p: c["devices"][0].pop("ram_bandwidth_gbs"), "ram_bandwidth_gbs")
refuses("a device with no RAM sizes", lambda c, p: dev(c, ram_gb_options=[]), "no RAM")
refuses("an OS with no find-out steps", lambda c, p: c["find_out"].pop("steamos"), "steamos")
refuses("a model with no size for the quant its Ollama tag ships",
        lambda c, p: mod(p, run=dict(p["models"][0]["run"], ollama_q="Q9_X")), "Q9_X")
refuses("a quant with no size", lambda c, p: p["models"][0]["quants"][0].__setitem__("bytes", 0), "without a size")
refuses("a quant with no repo", lambda c, p: p["models"][0]["quants"][0].pop("repo"), "without a size, a repo")
refuses("a model with no quants", lambda c, p: mod(p, quants=[]), "no quant")
refuses("a model missing the geometry the fit needs",
        lambda c, p: p["models"][0]["config"].pop("num_key_value_heads"), "num_key_value_heads")
refuses("a model with more active parameters than parameters",
        lambda c, p: p["models"][0]["config"].__setitem__("params_active", 1e15), "params_active")
refuses("a model with no Ollama tag", lambda c, p: p["models"][0]["run"].pop("ollama"), "Ollama")
refuses("a model with an unknown task", lambda c, p: mod(p, tasks=["juggle"]), "juggle")
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
true("every device names an OS the how-to has steps for", all(d["os"][0] in b32.OSES for d in CAT["devices"]))


# ---------------------------------------------------------------- the maths: the vendored module and its wrapper
src = b32.FIT_MJS.read_text(encoding="utf-8")
exports = re.findall(r"^export (?:const|function|let) (\w+)", src, re.M)
true("localfit.mjs exports the API fit.md names",
     {"assess", "bestQuant", "fit", "speed", "normalizeModel", "normalizeHardware", "budgets", "speedWords"} <= set(exports),
     str(exports))
check("...and has no import, default export or export list the inliner would miss",
      re.findall(r"^\s*(?:import\b|export\s+(?:default|\{|\*|async|class))", src, re.M), [])
wrapped = b32.fit_js()
check("the wrapper drops every export keyword", re.findall(r"^export ", wrapped, re.M), [])
true("...and returns every exported name on LOCALFIT",
     all(re.search(rf"return \{{[^}}]*\b{n}\b", wrapped) for n in exports))

answers = b32.cheat_answers(PICKS, {}) if node else None
true("node is on PATH, which the cheat sheet needs", node)
if node and answers:
    check("the cheat sheet has an answer for every pick on every machine",
          [len(r) for r in answers], [len(PICKS["models"])] * len(b32.CHEAT))
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "in.json").write_text(json.dumps({"machines": [m for _, m in b32.CHEAT], "models": PICKS["models"],
                                               "ctx": PICKS.get("default_ctx", 8192)}), encoding="utf-8")
        # The wrapped classic script, run as the browser runs it, against the module the build imported.
        (t / "wrapped.js").write_text(wrapped + r"""
const I = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
const out = I.machines.map((hw) => I.models.map((p) => {
  const b = LOCALFIT.bestQuant(Object.assign({id: p.id}, p.config, {quants: p.quants}), hw, {context: I.ctx});
  return b ? {id: p.id, verdict: b.verdict, quant: b.quant, tps: b.speed.decodeTps} : {id: p.id, verdict: "too-big"};
}));
process.stdout.write(JSON.stringify(out));
""", encoding="utf-8")
        res = subprocess.run([node, str(t / "wrapped.js"), str(t / "in.json")], capture_output=True, text=True)
    true("the inlined LOCALFIT runs as a classic script", res.returncode == 0, res.stderr[:400])
    if res.returncode == 0:
        check("...and answers exactly what the module answers, on every pick and cheat-sheet machine",
              json.loads(res.stdout), answers)

    V = {"great": 3, "slow": 2, "tight": 1, "too-big": 0}
    by = {label: {a["id"]: a for a in row} for (label, _), row in zip(b32.CHEAT, answers)}
    L = [label for label, _ in b32.CHEAT]
    check("a 70B model is too big for an 8 GB laptop", by[L[0]]["llama-3.3-70b"]["verdict"], "too-big")
    true("...and runs on a 128 GB Mac", by[L[-1]]["llama-3.3-70b"]["verdict"] in ("great", "slow"))
    true("an 8B model runs on a 16 GB Mac", by[L[3]]["llama-3.1-8b"]["verdict"] == "great")
    true("something runs great on an 8 GB laptop with no graphics card",
         any(a["verdict"] == "great" for a in by[L[0]].values()))
    worse = [(m, a, b) for a, b in ((L[0], L[1]), (L[3], L[4]), (L[4], L[-1]), (L[5], L[6]), (L[6], L[7]), (L[7], L[8]))
             for m in by[a] if V[by[b][m]["verdict"]] < V[by[a][m]["verdict"]]]
    check("more memory never gives a worse verdict, across the cheat sheet's ladders", worse, [])
    rows = b32.cheat_rows(PICKS, answers)
    true("every cheat-sheet row names at least one model that runs great", all(g for _, g, _ in rows))


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
    check("...and no Hugging Face slice when there is no index", data["hf"], None)
    check("...and the runners' own default context, below which no context step is shown", data["runner_ctx"], 4096)
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
true("...and does no memory or speed arithmetic of its own: every number comes from LOCALFIT",
     not re.search(r"bandwidth_gbs\s*\*|\* *0\.6\b|kv_heads \*", js))

hf_rows = {"cols": ["id", "name"], "variant_cols": ["repo", "fmt"], "file_cols": ["q", "bytes"], "snapshot": "2026-11-18",
           "models": [["Qwen/Qwen3-8B", "Qwen3-8B"], ["nobody/else", "else"]]}
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "models.json"
    check("with no Hugging Face index the join is empty, not an error", b32.hf_join(PICKS, p), {})
    p.write_text(json.dumps(hf_rows), encoding="utf-8")
    check("with one, only the rows the picks name are carried, in the index's own column shape",
          b32.hf_join(PICKS, p), {"cols": ["id", "name"], "variant_cols": ["repo", "fmt"], "file_cols": ["q", "bytes"],
                                  "snapshot": "2026-11-18", "rows": [["Qwen/Qwen3-8B", "Qwen3-8B"]]})
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
