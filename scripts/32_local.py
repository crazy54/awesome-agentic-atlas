"""Publish the local-AI page: tell someone what their own computer can run, and how to run it.

  docs/local/index.html        the page, with the catalogue, the picks and the fit maths inlined

  python scripts/32_local.py                  write it
  python scripts/32_local.py --out build-tmp  a dry run, off to one side

WHO IT IS FOR, WHICH IS WHAT EVERY DECISION BELOW FOLLOWS FROM
---------------------------------------------------------------
Someone who has heard that "you can run ChatGPT on your own computer", owns a laptop or a Steam Deck, and
has never opened a terminal. They do not know how much memory they have, and "Q4_K_M" is noise. The page
asks them two things -- what they have, and (optionally) what they want to do -- and answers with the models
that will run great, run with a catch, or not fit, each with a reason in their own units ("needs 5.6 GB,
you have 10.7 GB for AI") and a speed in words ("about as fast as you read"), then copy-paste steps for
their OS. The numbers an expert wants are one toggle away. The UX rationale is `team/local-ai/ux.md` in the
team's notes; the short version is in `handbook/frontend.md`.

THE NAME IS ONE CONSTANT
------------------------
The page's name has not been chosen -- the owner is picking from a shortlist -- so the title, the slug and
the one-line pitch live in `sitewide.LOCAL_PAGE` and nowhere else. This stage and the nav links the other
stages carry all read it, so renaming is one edit there and a rebuild. The slug is the directory under `docs/`
and the URL; changing it moves the page, and the old URL then 404s, so do it before launch or not at all.

THREE INPUTS, ALL JOINED HERE AND NOWHERE ELSE
----------------------------------------------
  config/local-ai/catalogue.json   the hardware: device kinds, devices, GPUs, the usable-memory rules, and
                                   the "how to find out what you have" steps. ds-hardware's, to
                                   `team/contracts/hardware.md`.
  config/local-ai/picks.json       the models the page recommends, with file sizes per quant, the shape
                                   numbers the context cache needs, and the exact name each runner knows
                                   them by. ds-models', to `team/contracts/fit.md`.
  docs/models.json (optional)      eng-hf's Hugging Face index (`team/contracts/models.md`). Joined on
                                   `hf_id` for freshness only: likes, downloads, last-modified. A build
                                   without it is a page without those three facts and nothing else.

Both config files are checked by `validate()` before anything is written, and a bad one stops the build
with the reason. That is deliberate: the page's whole claim is "this will run on your machine", and a
catalogue entry pointing at a GPU that is not there, or a model with no size for its default quant, is a
wrong answer delivered confidently -- worse than no page.

WHY EVERYTHING IS INLINED RATHER THAN FETCHED
---------------------------------------------
The catalogue, the picks and `scripts/localfit.js` are written into the page itself, as one JSON block
and one script. About 60 KB on disk and a fraction of that over the wire, because Pages gzips and the JSON
is repetitive. Three things follow:

  * Offline for free. `scripts/24_pwa.py`'s worker caches every page a reader visits and serves it when the
    network fails. A page whose data is in the page needs nothing more from that worker -- no new route, no
    second cache to fall out of step with the first -- so this stage changes nothing there. Someone who
    opens the page once on the café wifi can use it on the train.
  * No waterfall. Every answer the page gives is computed from bytes it already has; the first paint is the
    picker, and the first answer is one click after that.
  * One version. The page and its data were built by one run and cannot be a mismatched pair.

WHY THERE IS A PYTHON COPY OF THE MATHS
---------------------------------------
`scripts/localfit.py` is the same arithmetic as `scripts/localfit.js`, and this stage uses it for one thing:
the cheat sheet, a server-rendered table of what runs on common machines. That is the page for a reader with
no script and for a crawler, and it is a useful summary for everyone else. `tests/local_test.py` runs both
copies over a grid and fails on the first number where they disagree.

WHERE IT GOES IN A BUILD
------------------------
Anywhere before `20_landing.py`, which imports `urls()` below into `docs/sitemap.xml` -- run after it, the
first build would publish a sitemap naming a directory that is not there yet, which `tests/indexnow_test.py`
fails on purpose. It reads nothing another stage writes except the optional `docs/models.json`, so in
practice it sits beside `19d_discover.py`. In both workflows: the page is cheap, and a daily run is what
picks up a picks or catalogue edit without waiting for Sunday.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"
CONFIG = ROOT / "config" / "local-ai"

# The name, in one place: `sitewide.LOCAL_PAGE`. See "THE NAME IS ONE CONSTANT" above.
sys.path.insert(0, str(HERE))
import sitewide  # noqa: E402

PAGE = sitewide.LOCAL_PAGE


def _load(name: str, alias: str):
    """The dynamic load `19d_discover.py` and `25_collections.py` document: the numbered stages are not
    identifiers, and an already-loaded copy is reused so `20_landing.py` importing this module for its
    sitemap does not execute the big stages twice."""
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, HERE / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, str(HERE))
import localfit  # noqa: E402

FIT_JS = HERE / "localfit.js"
HF_MODELS = OUT / "models.json"


def urls(site: str | None = None) -> list[str]:
    """Every URL this stage publishes. Imported by `20_landing.py` for the sitemap.

    Takes the site root rather than importing `19_pages.py` for it, so that `20_landing.py` -- which already
    has it -- can ask for this page's URL without this module dragging the whole page stack in a second time.
    """
    if site is None:
        site = _load("19_pages.py", "b19").b17.SITE
    return [site + PAGE["slug"] + "/"]


# ------------------------------------------------------------------ the inputs
class Bad(ValueError):
    """A config file that would make the page give a wrong answer. Raised, never printed and skipped."""


def load(config: Path = CONFIG) -> tuple[dict, dict]:
    cat = json.loads((config / "catalogue.json").read_text(encoding="utf-8"))
    picks = json.loads((config / "picks.json").read_text(encoding="utf-8"))
    validate(cat, picks)
    return cat, picks


# The fields each record must carry, by the contract. Checked by name so a renamed field upstream is a
# build that says which field, rather than a page that silently shows "undefined GB".
DEVICE_FIELDS = ("id", "kind", "name", "os", "ram_gb_options", "unified", "gpu", "vram_gb", "bw_gbs",
                 "backend")
GPU_FIELDS = ("id", "name", "vendor", "vram_gb_options", "bw_gbs", "backend")
MODEL_FIELDS = ("id", "name", "tasks", "params_b", "active_b", "layers", "kv_heads", "head_dim",
                "default_q", "quants", "run", "blurb", "score", "license")
RULE_FIELDS = ("apple_small_frac", "apple_big_frac", "apple_big_from_gb", "unified_reserve_gb",
               "unified_max_frac", "system_reserve_gb", "system_min_frac", "vram_reserve_gb")
OSES = ("windows", "macos", "linux", "steamos")


def validate(cat: dict, picks: dict) -> None:
    """Every reference resolves, every number is a positive number, every id is unique. Raises `Bad`."""
    def need(rec, fields, what):
        missing = [f for f in fields if f not in rec]
        if missing:
            raise Bad(f"{what} {rec.get('id', '?')!r} is missing {', '.join(missing)}")

    kinds = {k["id"] for k in cat["kinds"]}
    gpus = {}
    for g in cat["gpus"]:
        need(g, GPU_FIELDS, "gpu")
        if g["id"] in gpus:
            raise Bad(f"gpu {g['id']!r} appears twice")
        if not g["vram_gb_options"] or g["bw_gbs"] <= 0:
            raise Bad(f"gpu {g['id']!r} has no memory size or no bandwidth")
        gpus[g["id"]] = g
    seen = set()
    for d in cat["devices"]:
        need(d, DEVICE_FIELDS, "device")
        if d["id"] in seen:
            raise Bad(f"device {d['id']!r} appears twice")
        seen.add(d["id"])
        if d["kind"] not in kinds:
            raise Bad(f"device {d['id']!r} has kind {d['kind']!r}, which is not one of {sorted(kinds)}")
        if d["gpu"] is not None and d["gpu"] not in gpus:
            raise Bad(f"device {d['id']!r} names gpu {d['gpu']!r}, which the catalogue does not have")
        if d["gpu"] is not None and d["vram_gb"] <= 0:
            raise Bad(f"device {d['id']!r} has a graphics card with no memory")
        if not d["ram_gb_options"] or min(d["ram_gb_options"]) <= 0 or d["bw_gbs"] <= 0:
            raise Bad(f"device {d['id']!r} has no RAM size or no bandwidth")
        if not set(d["os"]) <= set(OSES):
            raise Bad(f"device {d['id']!r} lists an OS outside {OSES}: {d['os']}")
    need(cat["usable"], RULE_FIELDS, "usable rules")
    for os_ in OSES:
        if not cat["find_out"].get(os_):
            raise Bad(f"find_out has no steps for {os_}")

    tasks = {t["id"] for t in picks["tasks"]}
    seen = set()
    for m in picks["models"]:
        need(m, MODEL_FIELDS, "model")
        if m["id"] in seen:
            raise Bad(f"model {m['id']!r} appears twice")
        seen.add(m["id"])
        if not set(m["tasks"]) <= tasks:
            raise Bad(f"model {m['id']!r} has tasks outside {sorted(tasks)}: {m['tasks']}")
        if not any(q["q"] == m["default_q"] for q in m["quants"]):
            raise Bad(f"model {m['id']!r} has no size for its default quant {m['default_q']}")
        if any(q["gb"] <= 0 or q["bits"] <= 0 for q in m["quants"]):
            raise Bad(f"model {m['id']!r} has a quant with no size")
        if not 0 < m["active_b"] <= m["params_b"]:
            raise Bad(f"model {m['id']!r} has active_b {m['active_b']} outside (0, params_b]")
        # Ollama and LM Studio are the two routes a beginner is offered, so both are required. The
        # llama.cpp and MLX routes are for the curious and are shown only where the pick has them.
        if not m["run"].get("ollama") or not m["run"].get("lmstudio"):
            raise Bad(f"model {m['id']!r} has no Ollama tag or no LM Studio name")


def hf_join(picks: dict, path: Path = HF_MODELS) -> dict[str, dict]:
    """`hf_id` -> the three freshness facts from eng-hf's index, or {} when there is no index yet.

    Tolerant of the file's absence and of rows it does not recognise, and of nothing else: a file that is
    there but is not JSON is a broken build upstream, and swallowing it would hide that.
    """
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("models", data) if isinstance(data, dict) else data
    want = {m.get("hf_id") for m in picks["models"] if m.get("hf_id")}
    out = {}
    for r in rows if isinstance(rows, list) else []:
        if isinstance(r, dict) and r.get("id") in want:
            out[r["id"]] = {k: r[k] for k in ("likes", "downloads", "last_modified") if k in r}
    return out


# ------------------------------------------------------------------ how to run it
# The steps, per route and per OS, as data the page fills in. `{ollama}`, `{hf_gguf}`, `{quant}`, `{mlx}`
# and `{lmstudio}` are a pick's own `run` fields and its chosen quant; nothing here invents a model name.
# A step is either plain words or `["cmd", "<command>"]`, which the page draws with a copy button.
#
# The Steam Deck is its own OS here because the advice differs: SteamOS's system partition is read-only, so
# Ollama's install script (which writes to /usr/local) fails there, and LM Studio's AppImage -- one file in
# the home directory -- is the route that works without unlocking anything.
HOWTO = {
    "lmstudio": {
        "label": "LM Studio", "pitch": "An app. No typing.",
        "steps": {
            "windows": ["Download LM Studio from <a href=\"https://lmstudio.ai/download\">lmstudio.ai</a> and run the installer.",
                        "Open it and click the magnifying glass (Discover) on the left.",
                        "Search for <b>{lmstudio}</b> and click Download. Pick <b>{quant}</b> if it asks.",
                        "When it finishes, click Chat, choose the model at the top, and start typing."],
            "macos": ["Download LM Studio from <a href=\"https://lmstudio.ai/download\">lmstudio.ai</a> and drag it to Applications.",
                      "Open it and click the magnifying glass (Discover) on the left.",
                      "Search for <b>{lmstudio}</b> and click Download. On a Mac it may offer an MLX version: that one is faster.",
                      "When it finishes, click Chat, choose the model at the top, and start typing."],
            "linux": ["Download the LM Studio AppImage from <a href=\"https://lmstudio.ai/download\">lmstudio.ai</a>.",
                      "Make it runnable, then open it:", ["cmd", "chmod +x ~/Downloads/LM-Studio-*.AppImage && ~/Downloads/LM-Studio-*.AppImage"],
                      "Click the magnifying glass (Discover), search for <b>{lmstudio}</b>, and download <b>{quant}</b>.",
                      "Click Chat, choose the model at the top, and start typing."],
            "steamos": ["Hold the power button and choose <b>Switch to Desktop</b>.",
                        "Open the browser, go to <a href=\"https://lmstudio.ai/download\">lmstudio.ai</a>, and download the Linux AppImage.",
                        "In the Dolphin file manager, right-click the file, choose Properties, then Permissions, and tick <b>Is executable</b>. Double-click it to open.",
                        "Click the magnifying glass (Discover), search for <b>{lmstudio}</b>, and download <b>{quant}</b>. Then click Chat."],
        },
    },
    "ollama": {
        "label": "Ollama", "pitch": "One command.",
        "steps": {
            "windows": ["Download Ollama from <a href=\"https://ollama.com/download/windows\">ollama.com</a> and run the installer.",
                        "Open Terminal: press the Windows key, type <b>Terminal</b>, press Enter.",
                        "Paste this and press Enter. The first time, it downloads the model.", ["cmd", "ollama run {ollama_tag}"],
                        "Type a question when you see <b>&gt;&gt;&gt;</b>. Type <b>/bye</b> to leave."],
            "macos": ["Download Ollama from <a href=\"https://ollama.com/download/mac\">ollama.com</a>, open it, and drag it to Applications.",
                      "Open Terminal: press Cmd + Space, type <b>Terminal</b>, press Enter.",
                      "Paste this and press Enter. The first time, it downloads the model.", ["cmd", "ollama run {ollama_tag}"],
                      "Type a question when you see <b>&gt;&gt;&gt;</b>. Type <b>/bye</b> to leave."],
            "linux": ["Install Ollama. This downloads and runs its official install script, which asks for your password:",
                      ["cmd", "curl -fsSL https://ollama.com/install.sh | sh"],
                      "Then run the model. The first time, it downloads it.", ["cmd", "ollama run {ollama_tag}"],
                      "Type a question when you see <b>&gt;&gt;&gt;</b>. Type <b>/bye</b> to leave."],
            "steamos": ["Ollama's installer can't write to SteamOS's locked system folders, so <b>LM Studio is the easier route on a Deck</b>. If you'd still like Ollama: switch to Desktop Mode and open Konsole.",
                        "Download Ollama into your home folder and start it:",
                        ["cmd", "mkdir -p ~/ollama && curl -fsSL https://ollama.com/download/ollama-linux-amd64.tgz | tar -xz -C ~/ollama && ~/ollama/bin/ollama serve &"],
                        "Then run the model:", ["cmd", "~/ollama/bin/ollama run {ollama_tag}"]],
        },
    },
    "llamacpp": {
        "label": "llama.cpp", "pitch": "For the curious: the engine under most of the others.",
        "steps": {
            "windows": ["Install it with winget, in Terminal:", ["cmd", "winget install llama.cpp"],
                        "Start a chat server. It downloads the model the first time:", ["cmd", "llama-server -hf {hf_gguf}:{quant}"],
                        "Open <b>http://localhost:8080</b> in your browser."],
            "macos": ["Install it with Homebrew:", ["cmd", "brew install llama.cpp"],
                      "Start a chat server. It downloads the model the first time:", ["cmd", "llama-server -hf {hf_gguf}:{quant}"],
                      "Open <b>http://localhost:8080</b> in your browser."],
            "linux": ["Install it with Homebrew, or download a build from <a href=\"https://github.com/ggml-org/llama.cpp/releases\">the releases page</a>:",
                      ["cmd", "brew install llama.cpp"],
                      "Start a chat server. It downloads the model the first time:", ["cmd", "llama-server -hf {hf_gguf}:{quant}"],
                      "Open <b>http://localhost:8080</b> in your browser."],
            "steamos": ["In Desktop Mode, download the Vulkan build for Linux from <a href=\"https://github.com/ggml-org/llama.cpp/releases\">the releases page</a> and unpack it in your home folder.",
                        "In Konsole, from the unpacked folder:", ["cmd", "./llama-server -hf {hf_gguf}:{quant}"],
                        "Open <b>http://localhost:8080</b> in the browser."],
        },
    },
    "mlx": {
        "label": "MLX", "pitch": "For the curious, Apple Silicon only: Apple's own engine, often the fastest on a Mac.",
        "steps": {
            "macos": ["Install it with Python's package manager (Python 3.10 or newer):", ["cmd", "pip install mlx-lm"],
                      "Chat with the model. It downloads it the first time:", ["cmd", "mlx_lm.chat --model {mlx}"]],
        },
    },
}


# ------------------------------------------------------------------ the cheat sheet
# Machines most readers will recognise themselves in, for the table a reader without script gets. Each is
# a machine dict exactly as the page builds one from a catalogue entry, so the Python fit sees what the JS
# fit would.
CHEAT = [
    ("A laptop with 8 GB and no graphics card", {"ram_gb": 8, "vram_gb": 0, "unified": False, "backend": "cpu", "gpu_bw_gbs": 0, "cpu_bw_gbs": 70}),
    ("A laptop with 16 GB and no graphics card", {"ram_gb": 16, "vram_gb": 0, "unified": False, "backend": "cpu", "gpu_bw_gbs": 0, "cpu_bw_gbs": 70}),
    ("A Steam Deck or ROG Ally (16 GB shared)", {"ram_gb": 16, "vram_gb": 0, "unified": True, "backend": "vulkan", "gpu_bw_gbs": 100, "cpu_bw_gbs": 100}),
    ("A Mac with 16 GB", {"ram_gb": 16, "vram_gb": 0, "unified": True, "backend": "metal", "gpu_bw_gbs": 100, "cpu_bw_gbs": 100}),
    ("A Mac with 32 GB (M-series Pro)", {"ram_gb": 32, "vram_gb": 0, "unified": True, "backend": "metal", "gpu_bw_gbs": 200, "cpu_bw_gbs": 200}),
    ("A PC with an 8 GB graphics card and 32 GB RAM", {"ram_gb": 32, "vram_gb": 8, "unified": False, "backend": "cuda", "gpu_bw_gbs": 272, "cpu_bw_gbs": 70}),
    ("A PC with a 12 GB graphics card and 32 GB RAM", {"ram_gb": 32, "vram_gb": 12, "unified": False, "backend": "cuda", "gpu_bw_gbs": 504, "cpu_bw_gbs": 70}),
    ("A PC with a 16 GB graphics card and 32 GB RAM", {"ram_gb": 32, "vram_gb": 16, "unified": False, "backend": "cuda", "gpu_bw_gbs": 717, "cpu_bw_gbs": 70}),
    ("A PC with a 24 GB graphics card and 64 GB RAM", {"ram_gb": 64, "vram_gb": 24, "unified": False, "backend": "cuda", "gpu_bw_gbs": 1008, "cpu_bw_gbs": 80}),
    ("A Mac or mini PC with 128 GB unified memory", {"ram_gb": 128, "vram_gb": 0, "unified": True, "backend": "metal", "gpu_bw_gbs": 546, "cpu_bw_gbs": 546}),
]


def cheat_rows(cat: dict, picks: dict) -> list[tuple[str, list[dict], list[dict]]]:
    """For each cheat-sheet machine: the three best picks that run great, and the best that only run."""
    out = []
    ctx = picks.get("default_ctx", 8192)
    for label, m in CHEAT:
        great, ok = [], []
        for model in picks["models"]:
            r = localfit.fit(m, model, {"ctx": ctx}, cat["usable"])
            if r["verdict"] == "great":
                great.append((model, r))
            elif r["verdict"] == "ok":
                ok.append((model, r))
        great.sort(key=lambda x: -x[0]["score"])
        ok.sort(key=lambda x: -x[0]["score"])
        out.append((label, great[:3], ok[:2]))
    return out


# ------------------------------------------------------------------ the page
b19 = _load("19_pages.py", "b19")
b20 = _load("20_landing.py", "b20")
import mark  # noqa: E402

SITE = b19.b17.SITE
REPO = b19.REPO
esc = b20.esc
ICON, HEAD_THEME, THEME_JS = b20.ICON, b20.HEAD_THEME, b20.THEME_JS


def rel(tail: str = "") -> str:
    """A link out of `docs/<slug>/`. One level down, so everything site-wide is `../`."""
    return "../" + tail


def payload(cat: dict, picks: dict, hf: dict) -> dict:
    """Everything the page script reads, in one object. Compact keys are not worth it: gzip already
    collapses the repetition, and readable keys are what lets a reader of the page source check a number."""
    models = []
    for m in picks["models"]:
        row = {k: m[k] for k in MODEL_FIELDS + ("family", "ctx_max", "gated", "hf_id") if k in m}
        if m.get("hf_id") in hf:
            row["hf"] = hf[m["hf_id"]]
        models.append(row)
    return {
        "page": PAGE,
        "kinds": cat["kinds"], "devices": cat["devices"], "gpus": cat["gpus"], "custom": cat["custom"],
        "find_out": cat["find_out"], "usable": cat["usable"],
        "tasks": picks["tasks"], "models": models, "default_ctx": picks.get("default_ctx", 8192),
        "howto": HOWTO,
        "fixture": bool(cat.get("fixture") or picks.get("fixture")),
    }


def json_script(obj: dict) -> str:
    """JSON safe inside a `<script>` element: `</` cannot close it early and the two line separators that
    JSON allows and JavaScript once did not are escaped."""
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return (text.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def head(title: str, desc: str, url: str) -> str:
    """The `<head>`, the shape `19d_discover.py` and `25_collections.py` write."""
    card = f"https://opengraph.githubassets.com/1/{esc(REPO)}"
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{card}">
<meta property="og:image:alt" content="The Awesome Agentic Atlas repository on GitHub.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{card}">
<link rel="icon" href="{esc(rel(ICON))}" type="image/svg+xml">
{sitewide.font_preload(rel())}{HEAD_THEME}<link rel="stylesheet" href="{esc(rel('pages.css'))}">
<style>{CSS}</style>
<script>document.documentElement.classList.add("lxjs");</script>
{sitewide.SITE_KIT}
</head>
"""


def nav() -> str:
    """The header navigation, matching `19d_discover.py`'s so the page families feel like one site."""
    return f"""  <nav>
    <a href="{esc(rel('discover/'))}">Discover</a> &middot;
    <a href="{esc(rel('collections/'))}">Collections</a> &middot;
    <a href="{esc(rel('catalog/'))}">Catalogue</a> &middot;
    <a href="{esc(rel('repo/'))}">All projects</a><br>
    <a href="https://github.com/{esc(REPO)}">Repository</a> &middot;
    <a href="https://github.com/{esc(REPO)}/tree/HEAD/mega-list">Markdown</a><br>
    <button class="chip" id="theme" aria-pressed="false">Light theme</button>
  </nav>"""


# Line icons for the six tiles, drawn in `currentColor` so every theme paints them and forced-colors mode
# turns them into system text. 24-unit grid, 1.6 stroke; decorative, so `aria-hidden` -- the tile's word
# is the label.
TILE_ICONS = {
    "laptop": '<path d="M4 6h16v10H4zM2 19h20"/>',
    "mac": '<path d="M3 5h18v11H3zM9 20h6M12 16v4"/>',
    "gaming": '<path d="M7 3h10v18H7zM10 7h4M10 11h4M12 16v1"/>',
    "desktop": '<path d="M3 4h18v12H3zM8 20h8M12 16v4"/>',
    "handheld": '<path d="M2 8a3 3 0 0 1 3-3h14a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3zM8 9v6M5 12h6M8 5v0M9 9h6v6H9z" fill="none"/><circle cx="18" cy="11" r="1"/><circle cx="18" cy="14" r="1"/>',
    "minipc": '<path d="M5 8h14v8H5zM8 12h3"/>',
}


def tile(k: dict) -> str:
    icon = TILE_ICONS.get(k["id"], TILE_ICONS["desktop"])
    return (f'<label class="lxtile"><input type="radio" name="kind" value="{esc(k["id"])}">'
            f'<svg class="lxti" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{icon}</svg>'
            f'<b>{esc(k["label"])}</b><small>{esc(k["hint"])}</small></label>')


def cheat_html(rows) -> str:
    """The cheat sheet: a real table, so a screen reader can move by column and a crawler sees text."""
    def names(items):
        return ", ".join(f'{esc(m["name"])}' for m, _ in items) or "&mdash;"
    body = "".join(
        f'<tr><th scope="row">{esc(label)}</th><td>{names(great)}</td><td>{names(ok)}</td></tr>'
        for label, great, ok in rows)
    return ('<table class="lxcheat"><caption class="sr">What runs on common machines</caption>'
            '<thead><tr><th scope="col">If you have</th><th scope="col">Runs great</th>'
            '<th scope="col">Also runs, more slowly or snugly</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')


def render(cat: dict, picks: dict, hf: dict) -> str:
    title = f"{PAGE['title']}: what AI can your computer run? | Awesome Agentic Atlas"
    n = len(picks["models"])
    desc = (f"Pick your laptop, Mac, gaming PC or handheld and see which of {n} open AI models will run on it, "
            "how fast, and the exact steps to run them with LM Studio or Ollama. Free, private, works offline.")
    url = SITE + PAGE["slug"] + "/"
    tasks = "".join(f'<label class="chip lxchip"><input type="checkbox" name="task" value="{esc(t["id"])}">'
                    f'<span>{esc(t["label"])}</span></label>' for t in picks["tasks"])
    fixture = ('<p class="lxfix" role="note">Preview data: these hardware and model numbers are placeholders '
               'while the catalogue is finished. Treat every answer as a rough guide.</p>'
               if cat.get("fixture") or picks.get("fixture") else "")
    return f"""{head(title, desc, url)}<body>
<header><div class="wrap">
  <nav class="brandbar">{mark.brand(rel())}</nav><div class="top">
  <div>
    <p class="kick">{esc(PAGE['title'])}</p>
    <h1>What AI can your computer run?</h1>
    <p class="sub">Tell us what you have. We&rsquo;ll show you which models run great, which run with a catch,
      and exactly how to start one. Nothing you pick leaves this page.</p>
  </div>
{nav()}
  </div>
</div></header>
<main class="lx"><div class="wrap">
{fixture}
<noscript><p class="lxnojs">The picker needs JavaScript. The <a href="#cheat">quick answer by machine</a> and
  the <a href="#learn">explanations</a> below work without it.</p></noscript>

<section class="lxs" id="s1" aria-labelledby="s1h">
  <div class="lxsh"><h2 id="s1h"><span class="lxn" aria-hidden="true">1</span> What do you have?</h2>
    <p class="lxsum" id="s1sum" hidden></p></div>
  <div class="lxbody" id="s1b">
    <fieldset class="lxtiles"><legend class="sr">What kind of computer</legend>
      {"".join(tile(k) for k in cat["kinds"])}
    </fieldset>
    <div class="lxpick" id="pick" hidden>
      <div class="lxfield" id="devf">
        <label for="q" id="qlab">Which one? Start typing its name</label>
        <div class="lxcombo">
          <input id="q" type="text" role="combobox" aria-autocomplete="list" aria-expanded="false"
                 aria-controls="qlist" autocomplete="off" spellcheck="false" placeholder="e.g. MacBook Air M2">
          <ul id="qlist" role="listbox" aria-labelledby="qlab" hidden></ul>
        </div>
        <p class="lxpop" id="pop"></p>
      </div>
      <p class="lxalt"><button class="lxlink" id="custom" type="button" aria-expanded="false"
        aria-controls="customb">I&rsquo;ll enter my graphics card and memory myself</button></p>
      <div class="lxcustom" id="customb" hidden>
        <div class="lxfield">
          <label for="gq" id="gqlab">Graphics card</label>
          <div class="lxcombo">
            <input id="gq" type="text" role="combobox" aria-autocomplete="list" aria-expanded="false"
                   aria-controls="gqlist" autocomplete="off" spellcheck="false" placeholder="e.g. RTX 4060, RX 7800 XT">
            <ul id="gqlist" role="listbox" aria-labelledby="gqlab" hidden></ul>
          </div>
          <p class="lxpop"><button class="chip" type="button" id="nogpu">{esc(cat["custom"]["no_gpu_label"])}</button></p>
        </div>
        <fieldset class="lxramf" id="vramf" hidden><legend>Its memory (VRAM)</legend><div id="vramo"></div></fieldset>
      </div>
      <fieldset class="lxramf" id="ramf" hidden><legend>How much memory (RAM)?
        <a class="lxwhat" href="#findout" data-open="findout">Not sure?</a></legend><div id="ramo"></div></fieldset>
      <p class="lxgores" id="gores" hidden><button class="cta" type="button" id="gobtn">See what you can run &darr;</button></p>
    </div>
    <details class="lxfind" id="findout">
      <summary>Help me find out what I have</summary>
      <div class="lxfindb">
        <p><button class="chip lxgo" type="button" id="guess">Guess from this browser</button>
          <span class="lxquiet">Reads the graphics name your browser reports. Nothing is sent anywhere.</span></p>
        <p id="guessout" role="status"></p>
        <div class="lxos" role="group" aria-label="Your operating system" id="fos"></div>
        <ol id="fsteps"></ol>
        <p class="lxquiet">Still not sure? Pick the smaller option. Too cautious beats too hopeful: a model
          that fits with room to spare is a model that works.</p>
      </div>
    </details>
  </div>
</section>

<section class="lxs" id="s2" aria-labelledby="s2h">
  <div class="lxsh"><h2 id="s2h"><span class="lxn" aria-hidden="true">2</span> What do you want to do? <small>Optional</small></h2></div>
  <fieldset class="lxtasks"><legend class="sr">Pick any that apply</legend>{tasks}</fieldset>
  <p class="lxquiet">&ldquo;Understand pictures&rdquo; means a model that can look at a photo or screenshot and
    talk about it. Making pictures is a different kind of model, not covered here yet.</p>
</section>

<section class="lxs lxres" id="s3" aria-labelledby="s3h">
  <div class="lxsh"><h2 id="s3h" tabindex="-1"><span class="lxn" aria-hidden="true">3</span> What you can run</h2>
    <button class="chip" type="button" id="nums" aria-pressed="false">Show the numbers</button></div>
  <div id="expert" class="lxexpert" hidden>
    <label for="ctx">Context length <a class="lxwhat" href="#q-ctx" data-open="q-ctx">What&rsquo;s that?</a></label>
    <select id="ctx"><option value="4096">4k tokens (~6 pages)</option><option value="8192">8k tokens (~12 pages)</option>
      <option value="32768">32k tokens (~50 pages)</option><option value="131072">128k tokens (a book)</option></select>
  </div>
  <p class="lxmach" id="mach">Pick your computer above and the answers appear here.</p>
  <div id="results"></div>
  <p class="sr" id="live" aria-live="polite"></p>
</section>

<section class="lxs" id="cheat" aria-labelledby="cheath">
  <h2 id="cheath">Quick answer by machine</h2>
  <p class="lxquiet">The same maths as the picker, for some common machines, at an {picks.get("default_ctx", 8192) // 1024}k context.</p>
  {cheat_html(cheat_rows(cat, picks))}
</section>

<section class="lxs" id="learn" aria-labelledby="learnh">
  <h2 id="learnh">The three ideas that explain everything</h2>
  <details id="q-quant"><summary>What&rsquo;s a quantisation (Q4, Q8)?</summary>
    <p>A model is billions of numbers. Quantising stores each one with fewer digits, the way a JPEG shrinks a
      photo. <b>Q4</b> keeps about 4 bits a number: roughly a quarter of the original size, and still very
      good. <b>Q8</b> is closer to the original and twice as big. Below about 3 bits, answers get
      noticeably worse. We pick Q4 unless your machine needs smaller, and we say when it does.</p></details>
  <details id="q-ctx"><summary>Why does context length cost memory?</summary>
    <p>Context is how much the model can keep in mind at once: your conversation so far, or a document you
      paste in. It sets aside memory for that up front, a little for every word it might hold. We assume
      about 8,000 tokens (around 12 pages), which is plenty for a chat. Pasting in a whole book needs much
      more, and on a small machine that can be the difference between fitting and not.</p></details>
  <details id="q-offload"><summary>What does &ldquo;offload&rdquo; mean?</summary>
    <p>A graphics card has its own fast memory. If a model doesn&rsquo;t fit in it, part can live in your
      ordinary RAM instead and run on the main processor. It still works, but every word waits for the slow
      part, so it&rsquo;s much slower than a model that fits on the card.</p></details>
  <details id="q-unified"><summary>Why does my Mac or handheld say less than its memory?</summary>
    <p>Macs, Steam Decks and similar machines share one pool of memory between the processor and the
      graphics. That&rsquo;s great for AI, because the graphics can use most of it, but the system keeps
      some for itself. On a Mac, macOS lets the graphics use about two-thirds of the memory by default (three
      quarters on bigger Macs).</p></details>
  <details id="q-tokens"><summary>What&rsquo;s a token?</summary>
    <p>The piece of text a model reads and writes at a time: usually part of a word. One English word is
      about 1.3 tokens, so 10 tokens a second is about 7 or 8 words a second, faster than most people
      read.</p></details>
  <details id="q-how"><summary>How we worked these numbers out</summary>
    <p>A model needs its download size, plus memory for its context, plus about {localfit.OVERHEAD_GB} GB to work
      in. Your machine offers a share of its memory, by a rule for each kind of machine. Speed comes from how
      fast your memory can be read, because every word means reading the whole active model once. We
      assume about {int(localfit.EFF_GPU * 100)}% of the datasheet speed on a graphics card, and show a range of
      &minus;{round((1 - localfit.SPREAD[0]) * 100)}% to +{round((localfit.SPREAD[1] - 1) * 100)}%. Real speed
      depends on the app, drivers and settings, so treat it as a guide. The code is
      <a href="https://github.com/{esc(REPO)}/blob/HEAD/scripts/localfit.js">open</a>.</p></details>
</section>
</div></main>
<footer><div class="wrap">
  {sitewide.buildtags(REPO)}
  {esc(PAGE['title'])} is part of the <a href="{esc(rel())}">Awesome Agentic Atlas</a>. Model names and
  download sizes come from each model&rsquo;s own release; speeds are estimates. Everything runs in your
  browser. Nothing you pick is sent anywhere.
</div></footer>
<script type="application/json" id="lxdata">{json_script(payload(cat, picks, hf))}</script>
<script>
{FIT_JS.read_text(encoding="utf-8")}</script>
{PAGE_JS}{sitewide.site_script(rel())}{THEME_JS}{b19.follow()}{b19.beacon()}{b19.telemetry(rel())}</body>
</html>
"""


# The page's own rules. Colour comes only from the site's custom properties -- `design-theme` is replacing
# the palette, and a page that wrote one hex value would be the page that did not change. Everything is
# prefixed `lx` so nothing here can reach a rule in `pages.css`.
CSS = """
.lx .wrap{max-width:980px}
/* Several rules below set `display`, which outranks the UA's `[hidden]{display:none}`; this puts it back. */
.lx [hidden]{display:none!important}
.kick{margin:0 0 4px;color:var(--muted);font:600 12px/1.4 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.lxs{margin:26px 0 0;padding:20px;border:1px solid var(--grid);border-radius:14px;background:var(--plane)}
.lxs h2{margin:0;font-size:19px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.lxs h2 small{font-weight:400;font-size:13px;color:var(--muted)}
.lxsh{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.lxn{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--bar);
  color:var(--onbar);font:700 14px/1 var(--mono)}
.lxsum{margin:0;color:var(--ink2);font-weight:600;flex:1 1 260px}
.lxlink{background:none;border:0;padding:4px 0;color:var(--link);text-decoration:underline;font-size:14px}
.lxquiet{color:var(--muted);font-size:13px;margin:8px 0 0}
fieldset{border:0;margin:0;padding:0;min-width:0}
legend{padding:0;font-weight:600;margin:0 0 8px}
.lxtiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin:16px 0 0}
.lxtile{position:relative;display:flex;flex-direction:column;gap:3px;padding:14px 12px;border:1px solid var(--grid);
  border-radius:12px;background:var(--band);cursor:pointer;min-height:44px}
.lxtile input{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}
.lxtile b{font-size:15px;color:var(--ink)}
.lxtile small{font-size:12px;color:var(--muted)}
.lxti{width:28px;height:28px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;color:var(--ink2)}
.lxtile:hover{border-color:var(--link)}
.lxtile:has(input:checked){border-color:var(--bar);box-shadow:inset 0 0 0 2px var(--bar)}
.lxtile:has(input:checked) .lxti{color:var(--bar)}
.lxtile:has(input:focus-visible){outline:2px solid var(--link);outline-offset:2px}
.lxpick{margin:18px 0 0}
.lxfield label{display:block;font-weight:600;margin:0 0 6px}
.lxcombo{position:relative;max-width:520px}
.lxcombo input,.lxexpert select{width:100%;font:inherit;font-size:16px;color:var(--ink);background:var(--surface);
  border:1px solid var(--grid);border-radius:10px;padding:11px 12px;min-height:44px}
.lxexpert select{width:auto;font-size:14px;padding:6px 8px;min-height:36px}
.lxcombo input:focus-visible,.lxexpert select:focus-visible{outline:2px solid var(--link);outline-offset:1px;border-color:var(--link)}
.lxcombo ul{position:absolute;z-index:5;left:0;right:0;top:calc(100% + 4px);margin:0;padding:4px;list-style:none;
  background:var(--plane);border:1px solid var(--grid);border-radius:10px;max-height:320px;overflow:auto;
  box-shadow:0 10px 30px rgba(0,0,0,.25)}
.lxcombo li{padding:9px 10px;border-radius:7px;cursor:pointer;display:flex;justify-content:space-between;gap:10px}
.lxcombo li small{color:var(--muted)}
.lxcombo li[aria-selected=true]{background:var(--band);outline:2px solid var(--link);outline-offset:-2px}
.lxpop{margin:10px 0 0;display:flex;flex-wrap:wrap;gap:0;align-items:center}
.lxpop .lxpl{color:var(--muted);font-size:13px;margin:0 8px 5px 0}
.chip{min-height:32px}
.chip[aria-pressed=true],.lxchip:has(input:checked){background:var(--bar);color:var(--onbar);border-color:var(--bar)}
.lxchip{position:relative;cursor:pointer;display:inline-flex;align-items:center;min-height:40px;font-size:14px;padding:8px 14px}
.lxchip input{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}
.lxchip:has(input:focus-visible),.chip:focus-visible,.lxlink:focus-visible,.lxs summary:focus-visible,
.lxhow:focus-visible,.lxcopy:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.lxtasks{margin:14px 0 0;display:flex;flex-wrap:wrap}
.lxalt{margin:12px 0 0}
.lxgores{margin:16px 0 0}
.lxgores .cta{border:0;font:inherit;font-weight:600;min-height:44px}
.lxgores .cta:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.lxcustom{margin:8px 0 0;padding:14px;border:1px dashed var(--grid);border-radius:12px}
.lxramf{margin:16px 0 0}
.lxramf div{display:flex;flex-wrap:wrap}
.lxfind{margin:18px 0 0;border-top:1px solid var(--grid);padding-top:12px}
.lxs summary{cursor:pointer;color:var(--link);font-weight:600;min-height:32px;padding:4px 0}
.lxfindb{padding:6px 0 0}
.lxfindb ol{margin:10px 0 0;padding-left:22px;color:var(--ink2)}
.lxfindb li{margin:4px 0}
.lxos{display:flex;flex-wrap:wrap;margin:10px 0 0}
.lxwhat{font-weight:400;font-size:13px;margin-left:6px}
.lxmach{margin:14px 0 0;font-size:16px;color:var(--ink);max-width:70ch}
.lxexpert{margin:12px 0 0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.lxexpert label{font-weight:600;font-size:14px}
.lxbest{margin:16px 0 0;padding:16px;border:2px solid var(--bar);border-radius:14px;background:var(--band)}
.lxbest>p:first-child{margin:0 0 6px;font:600 12px/1.4 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.lxbest .lxcard{border:0;padding:0;background:none}
.lxgroup{margin:24px 0 0}
.lxgroup h3{margin:0 0 10px;font-size:16px;display:flex;align-items:center;gap:8px}
.lxgroup h3 .ct{font-weight:400;color:var(--muted);font-size:14px;opacity:1}
.lxcards{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.lxcard{padding:14px 16px;border:1px solid var(--grid);border-radius:12px;background:var(--surface)}
.lxch{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.lxch h4{margin:0;font-size:16px}
.lxv{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--ink);
  border:1px solid var(--grid);border-radius:999px;padding:2px 10px}
.lxv i{font-style:normal;font-size:12px}
.lxv[data-v=great]{border-color:var(--good)}.lxv[data-v=great] i{color:var(--good)}
.lxv[data-v=ok]{border-color:var(--accent-gold)}.lxv[data-v=ok] i{color:var(--accent-gold)}
.lxv[data-v=no] i{color:var(--muted)}
.lxblurb{margin:6px 0 0;color:var(--ink2);font-size:14px}
.lxwhy{margin:8px 0 0;font-size:14px;color:var(--ink)}
.lxwhy span{display:block}
.lxcatch{margin:6px 0 0;padding:0;list-style:none;font-size:13.5px;color:var(--ink2)}
.lxcatch li::before{content:"\\2192  ";color:var(--muted)}
.lxmeta{margin:8px 0 0;font-size:12.5px;color:var(--muted)}
.lxnums{margin:10px 0 0;display:grid;grid-template-columns:max-content 1fr;gap:2px 14px;font:12.5px/1.6 var(--mono);color:var(--ink2)}
.lxnums dt{color:var(--muted)}.lxnums dd{margin:0}
.lxnums select{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--grid);border-radius:6px}
.lxhow{margin:10px 0 0;font:600 14px/1 var(--ui);color:var(--onbar);background:var(--bar);border:0;border-radius:9px;
  padding:10px 14px;min-height:40px}
.lxhow[aria-expanded=true]{background:var(--band);color:var(--ink);border:1px solid var(--grid)}
.lxhowb{margin:12px 0 0;padding:14px;border:1px solid var(--grid);border-radius:12px;background:var(--plane)}
.lxroutes{display:flex;flex-wrap:wrap;align-items:center}
.lxroutes .lxpl{color:var(--muted);font-size:13px;margin:0 8px 5px 0}
.lxpitch{margin:6px 0 0;color:var(--muted);font-size:13px}
.lxhowb ol{margin:10px 0 0;padding-left:22px}
.lxhowb li{margin:6px 0;color:var(--ink2)}
.lxhowb li b{color:var(--ink)}
.lxcmd{display:flex;align-items:stretch;gap:0;margin:6px 0;border:1px solid var(--grid);border-radius:9px;
  background:var(--band);overflow:hidden}
.lxcmd code{flex:1;font:13px/1.5 var(--mono);color:var(--ink);padding:9px 11px;overflow-x:auto;white-space:pre}
.lxcopy{flex:none;font:600 12px/1 var(--ui);background:var(--surface);color:var(--ink);border:0;
  border-left:1px solid var(--grid);padding:0 14px;min-width:64px}
.lxdl{margin:8px 0 0;font-size:13px;color:var(--muted)}
.lxmore{margin:10px 0 0}
.lxnofit summary{color:var(--ink2)}
.lxnote{margin:14px 0 0;color:var(--ink2);font-size:14px}
.lxcheat{margin:12px 0 0;font-size:14px}
.lxcheat th[scope=row]{font-size:14px;text-transform:none;letter-spacing:0;color:var(--ink);font-weight:600;
  background:none;vertical-align:top;border-bottom:1px solid var(--grid);width:34%}
.lxcheat td{padding:10px;color:var(--ink2)}
#learn details{border-top:1px solid var(--grid);padding:6px 0}
#learn details p{margin:6px 0 10px;color:var(--ink2);max-width:72ch}
#learn details:target summary,#learn details[open] summary{color:var(--ink)}
.lxfix{margin:18px 0 0;padding:10px 14px;border:1px dashed var(--accent-gold);border-radius:10px;color:var(--ink2);font-size:13.5px}
.lxnojs{margin:18px 0 0;padding:10px 14px;border:1px solid var(--grid);border-radius:10px}
html:not(.lxjs) #s1,html:not(.lxjs) #s2,html:not(.lxjs) #s3{display:none}
@media (max-width:640px){
  .lxs{padding:16px 14px;border-radius:12px}
  .lxtiles{grid-template-columns:repeat(2,1fr)}
  .lxcheat thead{display:none}
  .lxcheat tr,.lxcheat th[scope=row],.lxcheat td{display:block;width:auto}
  .lxcheat td{padding:4px 0 10px}
  .lxcheat td::before{display:block;color:var(--muted);font-size:12px}
  .lxcheat td:nth-of-type(1)::before{content:"Runs great"}
  .lxcheat td:nth-of-type(2)::before{content:"Also runs"}
}
@media (prefers-reduced-motion:no-preference){
  .lxres #results{animation:lxin .15s ease-out}
  @keyframes lxin{from{opacity:.4}}
}
@media (forced-colors:active){
  .lxtile:has(input:checked),.lxchip:has(input:checked),.chip[aria-pressed=true]{outline:3px solid Highlight}
  .lxv,.lxcard,.lxs,.lxcmd{border:1px solid CanvasText}
  .lxn{border:1px solid CanvasText}
  .lxcombo li[aria-selected=true]{outline:2px solid Highlight}
}
@media print{.lxtiles,.lxpick,.lxfind,#s2,#nums,.lxhow,.lxcopy{display:none}}
"""


# The page's behaviour, in a file of its own so it can be read, linted and diffed as JavaScript. Pure
# functions are on `LOCALUI` and are asserted by `tests/local-check.mjs`; the rest wires them to the DOM.
PAGE_JS = "<script>\n" + (HERE / "local_page.js").read_text(encoding="utf-8") + "</script>\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", help="write under this directory instead of docs/ (a dry run)")
    args = ap.parse_args()
    cat, picks = load()
    hf = hf_join(picks)
    out = Path(args.out) if args.out else OUT
    page = out / PAGE["slug"] / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(render(cat, picks, hf), encoding="utf-8")
    print(f"{PAGE['slug']}/index.html · {b20.kb(page.stat().st_size)} · {len(cat['devices'])} devices, "
          f"{len(cat['gpus'])} graphics cards, {len(picks['models'])} models"
          + (f", {len(hf)} joined to the Hugging Face index" if hf else ", no Hugging Face index yet")
          + (" · FIXTURE data" if cat.get("fixture") or picks.get("fixture") else ""))
    print("sitemap.xml carries this URL via scripts/20_landing.py")


if __name__ == "__main__":
    main()
