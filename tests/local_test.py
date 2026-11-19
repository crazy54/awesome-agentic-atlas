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


def mod(p, **kw):
    p["models"][0] = dict(p["models"][0], **kw)


b32.validate(CAT, PICKS)
true("the committed catalogue and picks validate", True)
refuses("a preset naming a device the catalogue lacks",
        lambda c, p: c["presets"].__setitem__(0, dict(c["presets"][0], device="nokia-3310")), "nokia-3310")
refuses("a tile the page has no icon for",
        lambda c, p: c["tiles"].append({"id": "fridge", "label": "Smart fridge", "hint": ""}), "icon")
refuses("a duplicate device id", lambda c, p: c["devices"].append(dict(c["devices"][0])), "twice")
refuses("a device on an unknown tile", lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], tiles=["fridge"])), "fridge")
refuses("a device missing a contract field", lambda c, p: c["devices"][0].pop("confidence"), "confidence")
refuses("a device with no memory size",
        lambda c, p: c["devices"].__setitem__(0, dict(c["devices"][0], memory={"options_gb": []})), "no memory size")
refuses("a catalogue without the processor-only entry the 'No graphics card' button picks",
        lambda c, p: c.__setitem__("devices", [d for d in c["devices"] if d["id"] != b32.NO_GPU]), b32.NO_GPU)
refuses("a tile with no preset", lambda c, p: c.__setitem__("presets", [x for x in c["presets"] if x["tile"] != "handheld"]), "handheld")
refuses("an OS with no help steps", lambda c, p: c["help"].pop("chromeos"), "chromeos")
refuses("a cheat-sheet preset the catalogue dropped",
        lambda c, p: c.__setitem__("presets", [x for x in c["presets"] if x["id"] != b32.CHEAT[0]]), b32.CHEAT[0])
CHAT0 = next(i for i, m in enumerate(PICKS["picks"]) if not b32.embed_only(m))


def pick(p, **kw):
    p["picks"][CHAT0] = dict(p["picks"][CHAT0], **kw)


def model(p):
    return p["picks"][CHAT0]["model"]


refuses("a pick with no file for its default quant", lambda c, p: pick(p, default_quant="Q9_X"), "Q9_X")
refuses("a quant with no size", lambda c, p: model(p)["quants"][0].__setitem__("bytes", 0), "without a size")
refuses("a quant with no repo", lambda c, p: model(p)["quants"][0].pop("repo"), "without a size, a repo")
refuses("a GGUF file with no label", lambda c, p: next(q for q in model(p)["quants"] if q.get("format", "gguf") == "gguf").pop("label"), "label")
refuses("a pick with no GGUF files", lambda c, p: model(p).__setitem__("quants", [q for q in model(p)["quants"] if q.get("format") == "mlx"]), "no GGUF")
refuses("a chat model missing the geometry the context cache needs",
        lambda c, p: model(p).pop("num_key_value_heads"), "num_key_value_heads")
refuses("a model with more active parameters than parameters",
        lambda c, p: model(p).__setitem__("params_active", 1e15), "params_active")
refuses("a pick with no Ollama command", lambda c, p: pick(p, run=dict(p["picks"][CHAT0]["run"], ollama={})), "Ollama")
refuses("a pick with no way into LM Studio",
        lambda c, p: pick(p, run=dict(p["picks"][CHAT0]["run"], lmstudio={"catalog": None, "search": None})), "LM Studio")
refuses("a pick with an unknown use", lambda c, p: pick(p, uses=["juggle"]), "juggle")
refuses("a pick of an unknown tier", lambda c, p: pick(p, tier="huge"), "huge")
refuses("a duplicate pick id", lambda c, p: p["picks"].append(dict(p["picks"][0])), "twice")
refuses("a picks file with nothing to chat with",
        lambda c, p: p.__setitem__("picks", [m for m in p["picks"] if b32.embed_only(m)]), "nothing" if False else "no model to chat")

tiles = {t["id"] for t in CAT["tiles"]}
check("the six tiles the UX plan names, in ds-hardware's ids", tiles,
      {"laptop", "mac", "gaming-pc", "desktop", "handheld", "mini-pc"})
check("...each with an icon", tiles, set(b32.TILE_ICONS))
for t, _ in b32.TASKS:
    true(f"the task {t!r} has at least one pick", any(t in m["uses"] for m in PICKS["picks"]))
check("the task buttons are ds-models' uses, so a pick's `uses` is the filter with no mapping",
      [t for t, _ in b32.TASKS], PICKS["uses"])
true("every device's first OS has how-to steps (ChromeOS through its Linux steps)",
     all(d["os"][0] in b32.HELP_OSES for d in CAT["devices"]), str({d["os"][0] for d in CAT["devices"]} - set(b32.HELP_OSES)))
FULL = json.loads((b32.CONFIG / "hardware.json").read_text(encoding="utf-8"))
check("the page reads ds-hardware's slim catalogue", (b32.CATALOGUE, CAT.get("slim")), ("hardware.slim.json", True))
check("...which has every device and preset the full one has",
      ([d["id"] for d in CAT["devices"]], [p["id"] for p in CAT["presets"]]),
      ([d["id"] for d in FULL["devices"]], [p["id"] for p in FULL["presets"]]))
check("...from the same build", CAT["updated"], FULL["updated"])


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
hsrc = b32.HW_MJS.read_text(encoding="utf-8")
hexports = re.findall(r"^export (?:const|function|let|async function) (\w+)", hsrc, re.M)
true("localhw.mjs exports the API hardware.md names",
     {"search", "popular", "memoryChoices", "toMachine", "detectHints", "osFromUA"} <= set(hexports), str(hexports))
check("...and has no import or export form the inliner would miss",
      re.findall(r"^\s*(?:import\b|export\s+(?:default|\{|\*|class))", hsrc, re.M), [])
hwrapped = b32.hw_js()
check("its wrapper drops every export keyword", re.findall(r"^export ", hwrapped, re.M), [])
true("...and returns every exported name on LOCALHW",
     all(re.search(rf"return \{{[^}}]*\b{n}\b", hwrapped) for n in hexports))

answers = b32.cheat_answers(PICKS, {}) if node else None
true("node is on PATH, which the cheat sheet needs", node)
if node and answers:
    check("the cheat sheet has an answer for every pick on every machine",
          [len(r) for r in answers], [len(PICKS["picks"])] * len(b32.CHEAT))
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "in.json").write_text(json.dumps({"presets": b32.CHEAT, "models": PICKS["picks"], "cat": CAT,
                                               "ctx": b32.DEFAULT_CTX}), encoding="utf-8")
        # Both wrapped classic scripts, run as the browser runs them -- over the slimmed catalogue the page
        # carries -- against the modules and the full catalogue the build imported.
        (t / "wrapped.js").write_text(wrapped + hwrapped + r"""
const I = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
const machines = I.presets.map((id) => {
  const p = I.cat.presets.find((x) => x.id === id);
  return LOCALHW.toMachine(I.cat, {device: p.device, memory_gb: p.memory_gb ?? undefined, ram_gb: p.ram_gb ?? undefined,
                                   ram_kind: p.ram_kind ?? undefined, os: p.os ?? undefined});
});
const out = machines.map((hw) => I.models.map((p) => {
  const b = LOCALFIT.bestQuant(p.model, hw, {context: I.ctx});
  return b ? {id: p.id, verdict: b.verdict, quant: b.quant, tps: b.speed.decodeTps, snag: !!(b.offload || b.nearlyFull || b.squeezed)}
    : {id: p.id, verdict: "too-big"};
}));
process.stdout.write(JSON.stringify(out));
""", encoding="utf-8")
        res = subprocess.run([node, str(t / "wrapped.js"), str(t / "in.json")], capture_output=True, text=True)
    true("the inlined LOCALFIT and LOCALHW run as classic scripts", res.returncode == 0, res.stderr[:400])
    if res.returncode == 0:
        check("...and answer exactly what the modules answer, on every pick and cheat-sheet machine",
              json.loads(res.stdout), answers)

    V = {"great": 3, "slow": 2, "tight": 1, "too-big": 0}
    by = {pid: {a["id"]: a for a in row} for pid, row in zip(b32.CHEAT, answers)}
    big = "openai/gpt-oss-120b"
    check("a 120B model is too big for an 8 GB MacBook Air", by["mba-m1-8"][big]["verdict"], "too-big")
    check("...and runs great on a 128 GB Mac Studio", by["mac-studio-m4max-128"][big]["verdict"], "great")
    small = [m["id"] for m in PICKS["picks"] if m["tier"] == "small" and not b32.embed_only(m)]
    true("a small-tier pick runs great on a 16 GB MacBook Air", any(by["mba-m3-16"][i]["verdict"] == "great" for i in small))
    tiny = [m["id"] for m in PICKS["picks"] if m["tier"] == "tiny" and not b32.embed_only(m)]
    true("a tiny-tier pick runs on an everyday laptop",
         any(by["laptop-office-intel"][i]["verdict"] in ("great", "slow") for i in tiny))
    worse = [(m, a, b) for a, b in (("mba-m1-8", "mba-m3-16"), ("mba-m3-16", "mbp-m4-pro-24"),
                                    ("mbp-m4-pro-24", "mac-studio-m4max-128"), ("pc-3060", "pc-4090"))
             for m in by[a] if V[by[b][m]["verdict"]] < V[by[a][m]["verdict"]]]
    check("a bigger machine of the same kind never gives a worse verdict", worse, [])
    rows = b32.cheat_rows(CAT, PICKS, answers)
    true("every cheat-sheet row names a model that runs at all", all(g or o for _, g, o in rows))
    true("...and no row names an embedding model, which nobody chats with",
         not any(b32.embed_only(m) for _, g, o in rows for m, _ in g + o))


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
    check("...carrying every device, preset and pick",
          (len(data["cat"]["devices"]), len(data["cat"]["presets"]), len(data["models"])),
          (len(CAT["devices"]), len(CAT["presets"]), len(PICKS["picks"])))
    check("...and no Hugging Face slice when there is no index", data["hf"], None)
    check("...and ds-models' runtime notes", data["runtimes"], PICKS["runtimes"])
    check("...and the runners' own default context, below which no context step is shown", data["runner_ctx"], 4096)
    check("...and how-to steps for both beginner routes on all four OSes",
          [sorted(data["howto"][k]["steps"]) for k in ("lmstudio", "ollama")],
          [sorted(b32.OSES)] * 2)
true("the fit maths is inlined", "const LOCALFIT = (() => {" in html)
true("the page script is inlined", "const LOCALUI = ((D, FIT, HW) => {" in html)
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
check("the Hugging Face join is on, through ds-models' merge rule", b32.HF_JOIN, True)
true("...which the page and the cheat sheet both call, and nothing calls the whole-row reader for a pick",
     "FIT.mergePickModel(" in (SCRIPTS / "local_page.js").read_text(encoding="utf-8")
     and "F.mergePickModel(" in b32.CHEAT_JS
     and "normalizeModel(row" not in (SCRIPTS / "local_page.js").read_text(encoding="utf-8") + b32.CHEAT_JS)
# The merge's whole promise is that the index refreshes facts and never changes an answer, so wherever the
# real index is on disk -- eng-hf's worktree, or docs/ once #112 has merged -- the cheat sheet is computed both
# ways and must agree. CI has neither until #112 lands; ds-models' check-picks.mjs guards it weekly after.
for index in (b32.HF_MODELS, ROOT.parent / "aaa-huggingface" / "docs" / "models.json"):
    if node and index.exists():
        joined = b32.hf_join(PICKS, index)
        true(f"the index at {index.parent.parent.name}/docs joins every pick", joined and len(joined["rows"]) == len(PICKS["picks"]),
             str(len(joined["rows"]) if joined else 0))
        strip = lambda rows: [[(a["id"], a["verdict"], a.get("quant")) for a in r] for r in rows]
        check("...and changes none of the cheat sheet's answers", strip(b32.cheat_answers(PICKS, joined)),
              strip(b32.cheat_answers(PICKS, {})))
        break
true("the preview banner shows exactly while PREVIEW is on", ('class="lxfix"' in html) == b32.PREVIEW)
true("the inlined hardware module is there", "const LOCALHW = (() => {" in html)
true("the page states the hardware list's own date", f"Hardware list updated {b32.long_date(CAT['updated'])}" in html)
check("...written out in words", b32.long_date("2026-11-08"), "8 November 2026")
true("the raised-limit toggle ships hidden, inside the numbers panel",
     re.search(r'id="expert"[^>]*hidden>.*?id="raisef" hidden', html, re.S) is not None)
TEAM = ROOT.parent / "Archie and Pals" / "team" / "local-ai"
if (TEAM / "picks.json").exists():
    # Only on a machine with the team's working folder beside the repository; CI has neither, by design.
    true("config/local-ai/picks.json is ds-models' file, verbatim (re-copy it if this fails)",
         json.loads((TEAM / "picks.json").read_text(encoding="utf-8")) == PICKS)
    true("config/local-ai/hardware.slim.json is ds-hardware's file, verbatim (re-copy it if this fails)",
         (TEAM / "hardware" / "hardware.slim.json").read_bytes().replace(b"\r\n", b"\n")
         == (b32.CONFIG / "hardware.slim.json").read_bytes().replace(b"\r\n", b"\n"))
    true("config/local-ai/hardware.json is ds-hardware's file, verbatim (re-copy it if this fails)",
         (TEAM / "hardware" / "hardware.json").read_bytes().replace(b"\r\n", b"\n")
         == (b32.CONFIG / "hardware.json").read_bytes().replace(b"\r\n", b"\n"))
    true("scripts/localhw.mjs is ds-hardware's hardware.mjs, verbatim (re-copy it if this fails)",
         (TEAM / "hardware" / "hardware.mjs").read_bytes().replace(b"\r\n", b"\n") == hsrc.encode("utf-8").replace(b"\r\n", b"\n"))
    true("scripts/localfit.mjs is ds-models' fit.mjs, verbatim (re-copy it if this fails)",
         (TEAM / "fit" / "fit.mjs").read_bytes().replace(b"\r\n", b"\n") == src.encode("utf-8").replace(b"\r\n", b"\n"))
true("the page links the site stylesheet and the shared tail", "../pages.css" in html and "btags" in html)

js = (SCRIPTS / "local_page.js").read_text(encoding="utf-8")
if node:
    res = subprocess.run([node, "--check", str(SCRIPTS / "local_page.js")], capture_output=True, text=True)
    true("local_page.js parses", res.returncode == 0, res.stderr[:300])
true("the page script writes no colour either", not re.search(r"#[0-9a-fA-F]{6}\b", js))
true("...and does no memory or speed arithmetic of its own: every number comes from LOCALFIT",
     not re.search(r"bandwidth_gbs\s*\*|\* *0\.6\b|kv_heads \*", js))

hf_rows = {"cols": ["id", "name"], "variant_cols": ["repo", "fmt"], "file_cols": ["q", "bytes"], "snapshot": "2026-11-18",
           "models": [["Qwen/Qwen3.5-4B", "Qwen3.5-4B"], ["nobody/else", "else"]]}
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "models.json"
    check("with no Hugging Face index the join is empty, not an error", b32.hf_join(PICKS, p), {})
    # #107 merges before #112, so the first builds have no docs/models.json at all. The page must build from the
    # picks as they are, carry no index slice, and give the cheat sheet the answers it gives with the join off.
    bare = b32.render(CAT, PICKS, b32.hf_join(PICKS, p))
    m0 = re.search(r'<script type="application/json" id="lxdata">(.*?)</script>', bare, re.S)
    check("...and the page still builds, falling back to the picks' own sizes", json.loads(m0.group(1))["hf"], None)
    if node:
        check("...with the cheat sheet the picks alone give", b32.cheat_answers(PICKS, b32.hf_join(PICKS, p)),
              b32.cheat_answers(PICKS, {}))
    p.write_text(json.dumps(hf_rows), encoding="utf-8")
    check("with one, only the rows the picks name are carried, in the index's own column shape",
          b32.hf_join(PICKS, p), {"cols": ["id", "name"], "variant_cols": ["repo", "fmt"], "file_cols": ["q", "bytes"],
                                  "snapshot": "2026-11-18", "rows": [["Qwen/Qwen3.5-4B", "Qwen3.5-4B"]]})
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
true("20_landing.py asks this stage for its URLs", "def local_urls()" in landing and "+ local" in landing)
sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
url = b32.urls(b32.SITE)[0]
true("the committed sitemap names the page", f"<loc>{url}</loc>" in sitemap)
true("the committed page exists", (ROOT / "docs" / sitewide.LOCAL_PAGE["slug"] / "index.html").exists())
for f in ("31_home.py", "20_landing.py", "19_pages.py", "19d_discover.py", "25_collections.py"):
    true(f"{f}'s nav links the page by the shared constant", "LOCAL_PAGE" in (SCRIPTS / f).read_text(encoding="utf-8"))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
