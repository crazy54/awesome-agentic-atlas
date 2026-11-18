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
  config/local-ai/picks.json       the models the page recommends: ds-models' `team/local-ai/picks.json`,
                                   copied verbatim (`team/contracts/fit.md` section 11). Each pick carries
                                   its tier, uses, one-line why, licence, every quant file's exact size, the
                                   exact command each runner takes, and a fit-ready `model`.
  docs/models.json (optional)      eng-hf's Hugging Face index (`team/contracts/models.md`). A pick whose
                                   id the index has is sized from that row (`normalizeModel()`), so file
                                   sizes follow re-uploads; without it, the pick's own `model` is used.

Both config files are checked by `validate()` before anything is written, and a bad one stops the build
with the reason. That is deliberate: the page's whole claim is "this will run on your machine", and a
catalogue entry pointing at a GPU that is not there, or a model with no size for its default quant, is a
wrong answer delivered confidently -- worse than no page.

WHY EVERYTHING IS INLINED RATHER THAN FETCHED
---------------------------------------------
The catalogue, the picks and `scripts/localfit.mjs` are written into the page itself, as one JSON block
and one script: about 155 KB on disk and 39 KB over the wire with ds-models' picks, because Pages
gzips and the JSON is repetitive. Three things follow:

  * Offline for free. `scripts/24_pwa.py`'s worker caches every page a reader visits and serves it when the
    network fails. A page whose data is in the page needs nothing more from that worker -- no new route, no
    second cache to fall out of step with the first -- so this stage changes nothing there. Someone who
    opens the page once on the café wifi can use it on the train.
  * No waterfall. Every answer the page gives is computed from bytes it already has; the first paint is the
    picker, and the first answer is one click after that.
  * One version. The page and its data were built by one run and cannot be a mismatched pair.

ONE COPY OF THE MATHS, RUN IN TWO PLACES
---------------------------------------
`scripts/localfit.mjs` is ds-models' fit method (`team/contracts/fit.md`): memory need against memory
available, offload, and a decode speed calibrated against 144 published llama.cpp measurements. It is
vendored verbatim, so a refresh is a copy and the diff is theirs. The page runs it in the browser. This stage
also runs it, under Node, for one thing: the cheat sheet, a server-rendered table of what runs on common
machines. That table is the page for a reader with no script and for a crawler.

There used to be a Python port for the cheat sheet. It went the moment the real method landed: a calibrated
model with sliding-window caches, MoE expert offload and per-backend constants is exactly the code that two
copies would let drift, and Node is already on every machine that runs this repository's tests. A build with
no `node` on PATH stops here and says so, rather than publishing a page whose two halves disagree.

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
import re
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


FIT_MJS = HERE / "localfit.mjs"
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
# build that says which field, rather than a page that silently shows "undefined GB". The hardware names are
# the ones `normalizeHardware()` in `localfit.mjs` reads, so the page passes a catalogue entry straight in.
DEVICE_FIELDS = ("id", "kind", "name", "os", "ram_gb_options", "unified", "gpu", "vram_gb", "ram_bandwidth_gbs",
                 "igpu")
GPU_FIELDS = ("id", "name", "vendor", "vram_gb_options", "vram_bandwidth_gbs", "backends")
PICK_FIELDS = ("id", "name", "tier", "uses", "why", "license", "gated", "default_quant", "run", "model")
# The geometry the fit method cannot work without. The rest of `model` (sliding windows, experts, MLA) is
# optional and only sharpens the answer.
CONFIG_FIELDS = ("params_total", "num_hidden_layers", "hidden_size", "num_attention_heads",
                 "num_key_value_heads", "head_dim", "vocab_size")
TIERS = ("tiny", "small", "medium", "large")

# The task buttons: ds-models' `uses`, in the reader's words. The ids are theirs, so a pick's `uses` is the
# filter with no mapping; the labels are the page's copy and live here. "Search my own documents" is the
# embeddings use: those models are not chatted with, so they are shown only when that button is pressed.
TASKS = [
    ("chat", "Chat, write and ask questions"),
    ("coding", "Write code"),
    ("reasoning", "Think hard (maths, logic)"),
    ("vision", "Understand pictures"),
    ("agents", "Build agents (tools)"),
    ("embeddings", "Search my own documents"),
]


def rank(p: dict, tasks: list[str] = ()) -> float:
    """How strongly the page recommends a pick that runs, higher first: the bigger tier (bigger runs better
    when it runs at all), then being ds-models' primary choice for one of the reader's tasks (or for anything,
    with no task chosen), then size. `LOCALUI.rank` is the same rule; the browser check holds the picker's
    first three to the cheat sheet's for one machine, which is where the two would disagree."""
    prim = any(not tasks or c["use"] in tasks for c in p.get("primary_for", []))
    return TIERS.index(p["tier"]) * 10 + (5 if prim else 0) + p["model"]["params_total"] / 1e12


def embed_only(p: dict) -> bool:
    return p["uses"] == ["embeddings"]


OSES = ("windows", "macos", "linux", "steamos")
VENDORS = ("nvidia", "amd", "intel", "apple")


def validate(cat: dict, picks: dict) -> None:
    """Every reference resolves, every number is a positive number, every id is unique. Raises `Bad`."""
    def need(rec, fields, what, rid=None):
        missing = [f for f in fields if f not in rec]
        if missing:
            raise Bad(f"{what} {rid or rec.get('id', '?')!r} is missing {', '.join(missing)}")

    kinds = {k["id"] for k in cat["kinds"]}
    gpus = {}
    for g in cat["gpus"]:
        need(g, GPU_FIELDS, "gpu")
        if g["id"] in gpus:
            raise Bad(f"gpu {g['id']!r} appears twice")
        if not g["vram_gb_options"] or g["vram_bandwidth_gbs"] <= 0:
            raise Bad(f"gpu {g['id']!r} has no memory size or no bandwidth")
        if g["vendor"] not in VENDORS:
            raise Bad(f"gpu {g['id']!r} has vendor {g['vendor']!r}, not one of {VENDORS}")
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
        if d["gpu"] is not None and d["igpu"]:
            raise Bad(f"device {d['id']!r} has both a graphics card and a shared-memory GPU; pick the one AI uses")
        if d["igpu"] and (not d["unified"] or d["igpu"].get("vendor") not in VENDORS):
            raise Bad(f"device {d['id']!r} has a shared-memory GPU but is not unified, or names no vendor")
        if not d["ram_gb_options"] or min(d["ram_gb_options"]) <= 0 or d["ram_bandwidth_gbs"] <= 0:
            raise Bad(f"device {d['id']!r} has no RAM size or no bandwidth")
        if not set(d["os"]) <= set(OSES) or not d["os"]:
            raise Bad(f"device {d['id']!r} lists an OS outside {OSES}: {d['os']}")
    for os_ in OSES:
        if not cat["find_out"].get(os_):
            raise Bad(f"find_out has no steps for {os_}")

    uses = {t for t, _ in TASKS}
    seen = set()
    for m in picks["picks"]:
        need(m, PICK_FIELDS, "pick")
        if m["id"] in seen:
            raise Bad(f"pick {m['id']!r} appears twice")
        seen.add(m["id"])
        if m["tier"] not in TIERS:
            raise Bad(f"pick {m['id']!r} has tier {m['tier']!r}, not one of {TIERS}")
        if not m["uses"] or not set(m["uses"]) <= uses:
            raise Bad(f"pick {m['id']!r} has uses outside {sorted(uses)}: {m['uses']}")
        mod = m["model"]
        # An embedding model is small and context-light, and fit.mjs sizes it from its file alone, so only a
        # model people chat with must carry the geometry the context cache is computed from.
        need(mod, (("params_total",) if embed_only(m) else CONFIG_FIELDS) + ("quants",), "pick model", m["id"])
        gg = [q for q in mod["quants"] if q.get("format", "gguf") == "gguf"]
        if not gg:
            raise Bad(f"pick {m['id']!r} lists no GGUF quant files")
        # A GGUF file needs its label too: it is the `:<quant>` in the download command. MLX entries are a
        # repo each, downloaded whole, so a size and a repo are all they need.
        for q in mod["quants"]:
            gguf = q.get("format", "gguf") == "gguf"
            if not (isinstance(q.get("bytes"), int) and q["bytes"] > 0) or not q.get("repo") or (gguf and not q.get("label")):
                raise Bad(f"pick {m['id']!r} has a quant without a size, a repo or a label: {q}")
        if not any(q["quant"] == m["default_quant"] for q in gg):
            raise Bad(f"pick {m['id']!r} has no file for its default quant {m['default_quant']}")
        if mod.get("params_active") is not None and not 0 < mod["params_active"] <= mod["params_total"]:
            raise Bad(f"pick {m['id']!r} has params_active outside (0, params_total]")
        # Ollama and LM Studio are the two routes a beginner is offered, so both are required: an Ollama
        # command, and either an LM Studio catalogue id or a search string. llama.cpp and MLX are for the
        # curious and are shown only where the pick has them.
        run = m["run"]
        if not (run.get("ollama") or {}).get("pull"):
            raise Bad(f"pick {m['id']!r} has no Ollama command")
        lms = run.get("lmstudio") or {}
        if not (lms.get("catalog") or lms.get("search")):
            raise Bad(f"pick {m['id']!r} has neither an LM Studio catalogue id nor a search string")
        if not m["license"].get("name"):
            raise Bad(f"pick {m['id']!r} has no licence name")
    if not any(not embed_only(m) for m in picks["picks"]):
        raise Bad("picks.json has no model to chat with")


def hf_join(picks: dict, path: Path = HF_MODELS) -> dict:
    """The rows of eng-hf's index (`team/contracts/models.md`) that the picks name, or {} with no index yet.

    Returned with the file's own column lists, untouched: the page turns a row into what the fit method reads
    with `normalizeModel()` from `localfit.mjs`, which is ds-models' mapping and the only one. Rows are
    joined on the pick's `id`, which is the Hugging Face repo id; a pick the index does not have keeps its own
    `model`.

    Tolerant of the file's absence and of rows it does not name, and of nothing else: a file that is there
    but is not JSON is a broken build upstream, and swallowing it would hide that.
    """
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    cols = data["cols"]
    want = {m["id"] for m in picks["picks"]}
    rows = [r for r in data.get("models", []) if dict(zip(cols, r)).get("id") in want]
    if not rows:
        return {}
    return {"cols": cols, "variant_cols": data.get("variant_cols"), "file_cols": data.get("file_cols"),
            "snapshot": data.get("snapshot"), "rows": rows}


# ------------------------------------------------------------------ how to run it
# The steps, per route and per OS, as data the page fills in. The placeholders are filled from the pick's own
# `run` commands at the quant the fit chose for this machine (`LOCALUI.commands`): `{ollama_cmd}`,
# `{llama_cmd}`, `{mlx_cmd}`, `{lmstudio}` (its catalogue id, or the search string where it has none),
# `{qlabel}`, and `{ctx}`, the context the estimate assumed. Nothing here invents a model name or a command. A step is plain words, or
# `["cmd", "<command>"]`, which the page draws with a copy button, or `["ctx", ...]` / `["ctxcmd", ...]`, a
# step and a command shown only when the estimate assumed more context than the runner's own default --
# fit.md's warning that Ollama and LM Studio pick a smaller one, so the answer on the card is only true if the
# reader sets it.
#
# The Steam Deck is its own OS here because the advice differs: SteamOS's system partition is read-only, so
# Ollama's install script (which writes to /usr/local) fails there, and LM Studio's AppImage -- one file in
# the home directory -- is the route that works without unlocking anything.
LMS_CTX = ["ctx", "Before you load it, open the settings beside the model name and set <b>Context Length</b> "
                  "to <b>{ctx}</b>, the amount we sized it for."]
OLLAMA_CTX = ["ctx", "Ollama starts with a shorter memory than we sized this for. Once it&rsquo;s running, "
                     "type this to give it <b>{ctx}</b> tokens:"]
OLLAMA_CTX_CMD = ["ctxcmd", "/set parameter num_ctx {ctx}"]
LMS_GET = "<a href=\"https://lmstudio.ai/download\">lmstudio.ai</a>"
HOWTO = {
    "lmstudio": {
        "label": "LM Studio", "pitch": "An app. No typing.",
        "steps": {
            "windows": [f"Download LM Studio from {LMS_GET} and run the installer.",
                        "Open it and click the magnifying glass (Discover) on the left.",
                        "Search for <b>{lmstudio}</b> and click Download. Pick <b>{qlabel}</b> if it asks.", LMS_CTX,
                        "When it finishes, click Chat, choose the model at the top, and start typing."],
            "macos": [f"Download LM Studio from {LMS_GET} and drag it to Applications.",
                      "Open it and click the magnifying glass (Discover) on the left.",
                      "Search for <b>{lmstudio}</b> and click Download. On a Mac it may offer an MLX version: "
                      "that one is often faster.", LMS_CTX,
                      "When it finishes, click Chat, choose the model at the top, and start typing."],
            "linux": [f"Download the LM Studio AppImage from {LMS_GET}.",
                      "Make it runnable, then open it:",
                      ["cmd", "chmod +x ~/Downloads/LM-Studio-*.AppImage && ~/Downloads/LM-Studio-*.AppImage"],
                      "Click the magnifying glass (Discover), search for <b>{lmstudio}</b>, and download "
                      "<b>{qlabel}</b>.", LMS_CTX,
                      "Click Chat, choose the model at the top, and start typing."],
            "steamos": ["Hold the power button and choose <b>Switch to Desktop</b>.",
                        f"Open the browser, go to {LMS_GET}, and download the Linux AppImage.",
                        "In the Dolphin file manager, right-click the file, choose Properties, then Permissions, "
                        "and tick <b>Is executable</b>. Double-click it to open.",
                        "Click the magnifying glass (Discover), search for <b>{lmstudio}</b>, and download "
                        "<b>{qlabel}</b>.", LMS_CTX,
                        "Click Chat, choose the model at the top, and start typing."],
        },
    },
    "ollama": {
        "label": "Ollama", "pitch": "One command.",
        "steps": {
            "windows": ["Download Ollama from <a href=\"https://ollama.com/download/windows\">ollama.com</a> and "
                        "run the installer.",
                        "Open Terminal: press the Windows key, type <b>Terminal</b>, press Enter.",
                        "Paste this and press Enter. The first time, it downloads the model.",
                        ["cmd", "{ollama_cmd}"], OLLAMA_CTX, OLLAMA_CTX_CMD,
                        "Type a question when you see <b>&gt;&gt;&gt;</b>. Type <b>/bye</b> to leave."],
            "macos": ["Download Ollama from <a href=\"https://ollama.com/download/mac\">ollama.com</a>, open it, "
                      "and drag it to Applications.",
                      "Open Terminal: press Cmd + Space, type <b>Terminal</b>, press Enter.",
                      "Paste this and press Enter. The first time, it downloads the model.",
                      ["cmd", "{ollama_cmd}"], OLLAMA_CTX, OLLAMA_CTX_CMD,
                      "Type a question when you see <b>&gt;&gt;&gt;</b>. Type <b>/bye</b> to leave."],
            "linux": ["Install Ollama. This downloads and runs its official install script, which asks for your "
                      "password:",
                      ["cmd", "curl -fsSL https://ollama.com/install.sh | sh"],
                      "Then run the model. The first time, it downloads it.",
                      ["cmd", "{ollama_cmd}"], OLLAMA_CTX, OLLAMA_CTX_CMD,
                      "Type a question when you see <b>&gt;&gt;&gt;</b>. Type <b>/bye</b> to leave."],
            "steamos": ["Ollama&rsquo;s installer can&rsquo;t write to SteamOS&rsquo;s locked system folders, so "
                        "<b>LM Studio is the easier route on a Deck</b>. If you&rsquo;d still like Ollama: switch "
                        "to Desktop Mode and open Konsole.",
                        "Download Ollama into your home folder and start it:",
                        ["cmd", "mkdir -p ~/ollama && curl -fsSL https://ollama.com/download/ollama-linux-amd64.tgz"
                                " | tar -xz -C ~/ollama && ~/ollama/bin/ollama serve &"],
                        "Then run the model:", ["cmd", "{ollama_cmd_home}"],
                        OLLAMA_CTX, OLLAMA_CTX_CMD],
        },
    },
    "llamacpp": {
        "label": "llama.cpp", "pitch": "For the curious: the engine under most of the others.",
        "steps": {
            "windows": ["Install it with winget, in Terminal:", ["cmd", "winget install llama.cpp"],
                        "Start a chat server. It downloads the model the first time:",
                        ["cmd", "{llama_cmd}"],
                        "Open <b>http://localhost:8080</b> in your browser."],
            "macos": ["Install it with Homebrew:", ["cmd", "brew install llama.cpp"],
                      "Start a chat server. It downloads the model the first time:",
                      ["cmd", "{llama_cmd}"],
                      "Open <b>http://localhost:8080</b> in your browser."],
            "linux": ["Install it with Homebrew, or download a build from "
                      "<a href=\"https://github.com/ggml-org/llama.cpp/releases\">the releases page</a>:",
                      ["cmd", "brew install llama.cpp"],
                      "Start a chat server. It downloads the model the first time:",
                      ["cmd", "{llama_cmd}"],
                      "Open <b>http://localhost:8080</b> in your browser."],
            "steamos": ["In Desktop Mode, download the Vulkan build for Linux from "
                        "<a href=\"https://github.com/ggml-org/llama.cpp/releases\">the releases page</a> and unpack "
                        "it in your home folder.",
                        "In Konsole, from the unpacked folder:", ["cmd", "{llama_cmd_here}"],
                        "Open <b>http://localhost:8080</b> in the browser."],
        },
    },
    "mlx": {
        "label": "MLX", "pitch": "For the curious, Apple Silicon only: Apple's own engine, often faster on a Mac "
                                 "than our estimate.",
        "steps": {
            "macos": ["Install it with Python's package manager (Python 3.10 or newer):", ["cmd", "pip install mlx-lm"],
                      "Chat with the model. It downloads it the first time:", ["cmd", "{mlx_cmd}"]],
        },
    },
}
# Ollama's and LM Studio's own default context, at or below which the `ctx` steps above are left out.
# Ollama's is 4,096 tokens as of its 0.6 releases; LM Studio's is set per model and is commonly 4,096 too.
RUNNER_CTX = 4096
# The context every estimate assumes unless the reader changes it: fit.md section 2.2's default.
DEFAULT_CTX = 8192


# ------------------------------------------------------------------ the cheat sheet
# Machines most readers will recognise themselves in, for the table a reader without script gets. Each is a
# hardware object in the catalogue's field names, which `normalizeHardware()` reads exactly as it reads the
# page's machines.
def _apple(ram, bw):
    return {"ram_gb": ram, "ram_bandwidth_gbs": bw, "unified": True, "os": "macos",
            "gpu": {"vendor": "apple", "integrated": True, "vram_bandwidth_gbs": bw, "backends": ["metal", "mlx"]}}


def _card(vram, bw, ram, ram_bw=80):
    return {"ram_gb": ram, "ram_bandwidth_gbs": ram_bw, "os": "windows",
            "gpu": {"vendor": "nvidia", "vram_gb": vram, "vram_bandwidth_gbs": bw, "backends": ["cuda", "vulkan"]}}


CHEAT = [
    ("A laptop with 8 GB and no graphics card", {"ram_gb": 8, "ram_bandwidth_gbs": 51.2, "os": "windows", "gpu": None}),
    ("A laptop with 16 GB and no graphics card", {"ram_gb": 16, "ram_bandwidth_gbs": 68, "os": "windows", "gpu": None}),
    ("A Steam Deck (16 GB shared)", {"ram_gb": 16, "ram_bandwidth_gbs": 102.4, "unified": True, "os": "steamos",
                                     "gpu": {"vendor": "amd", "integrated": True, "vram_bandwidth_gbs": 102.4,
                                             "backends": ["vulkan"]}}),
    ("A Mac with 16 GB (M-series)", _apple(16, 100)),
    ("A Mac with 36 GB (M-series Pro or Max)", _apple(36, 273)),
    ("A PC with an 8 GB graphics card and 32 GB RAM", _card(8, 272, 32)),
    ("A PC with a 12 GB graphics card and 32 GB RAM", _card(12, 504, 32)),
    ("A PC with a 16 GB graphics card and 32 GB RAM", _card(16, 717, 32)),
    ("A PC with a 24 GB graphics card and 64 GB RAM", _card(24, 1008, 64, 96)),
    ("A Mac with 128 GB (M-series Max)", _apple(128, 546)),
]

# The cheat sheet's runner: the same `localfit.mjs` the page inlines, imported as the module it is, and the
# same model assembly the page does (`modelOf` is `LOCALUI.modelOf`'s rule restated in a few lines; the
# browser check holds the page's answer for a cheat-sheet machine to this table's).
CHEAT_JS = r"""
import * as F from %(fit)s;
import {readFileSync} from "node:fs";
const I = JSON.parse(readFileSync(process.argv[2], "utf8"));
const hf = I.hf && I.hf.rows ? Object.fromEntries(I.hf.rows.map((r) => {
  const o = Object.fromEntries(I.hf.cols.map((c, i) => [c, r[i]])); return [o.id, o]; })) : {};
const modelOf = (p) => {
  const row = hf[p.id];
  const base = row ? F.normalizeModel(row, I.hf.variant_cols, I.hf.file_cols) : null;
  return base && base.quants.length ? Object.assign(base, {id: p.id}) : p.model;
};
const out = I.machines.map((hw) => I.models.map((p) => {
  const b = F.bestQuant(modelOf(p), hw, {context: I.ctx});
  return b ? {id: p.id, verdict: b.verdict, quant: b.quant, tps: b.speed.decodeTps, snag: !!(b.offload || b.nearlyFull)}
    : {id: p.id, verdict: "too-big"};
}));
process.stdout.write(JSON.stringify(out));
"""


def node_bin() -> str:
    import shutil
    n = shutil.which("node")
    if not n:
        raise SystemExit("32_local.py needs Node on PATH: the cheat sheet runs scripts/localfit.mjs, the same "
                         "fit method the page runs, so the two cannot disagree. Install Node 18+ and re-run.")
    return n


def cheat_answers(picks: dict, hf: dict) -> list[list[dict]]:
    """`bestQuant()` for every pick on every cheat-sheet machine, from `localfit.mjs` under Node."""
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "in.json").write_text(json.dumps({"machines": [m for _, m in CHEAT], "models": picks["picks"],
                                               "hf": hf, "ctx": DEFAULT_CTX}), encoding="utf-8")
        (t / "cheat.mjs").write_text(CHEAT_JS % {"fit": json.dumps(FIT_MJS.as_uri())}, encoding="utf-8")
        res = subprocess.run([node_bin(), str(t / "cheat.mjs"), str(t / "in.json")],
                             capture_output=True, text=True, encoding="utf-8")
    if res.returncode:
        raise SystemExit(f"the cheat sheet's run of localfit.mjs failed:\n{res.stderr}")
    return json.loads(res.stdout)


def cheat_rows(picks: dict, answers: list[list[dict]]) -> list[tuple[str, list, list]]:
    """For each cheat-sheet machine: the three best picks that run great, and the two best that only run."""
    by = {m["id"]: m for m in picks["picks"]}
    out = []
    for (label, _), row in zip(CHEAT, answers):
        row = [a for a in row if not embed_only(by[a["id"]])]
        # Clean fits first, as the picker orders them (see `groups` in local_page.js).
        great = sorted((a for a in row if a["verdict"] == "great"), key=lambda a: (a["snag"], -rank(by[a["id"]])))
        ok = sorted((a for a in row if a["verdict"] in ("slow", "tight")), key=lambda a: -rank(by[a["id"]]))
        out.append((label, [(by[a["id"]], a) for a in great[:3]], [(by[a["id"]], a) for a in ok[:2]]))
    return out


def fit_js() -> str:
    """`localfit.mjs` as a classic script defining `LOCALFIT`, for inlining.

    The module is vendored verbatim from ds-models, so it is adapted here rather than edited: every top-level
    `export ` is dropped and the names it exported are returned from a wrapper. The list is read off the
    source, so an export added upstream arrives on `LOCALFIT` with no edit here; `tests/local_test.py` asserts
    the wrapped script exposes every one of them and that the file has no import or other export form this
    rewrite would miss.
    """
    src = FIT_MJS.read_text(encoding="utf-8")
    names = re.findall(r"^export (?:const|function|let) (\w+)", src, re.M)
    body = re.sub(r"^export (?=const|function|let)", "", src, flags=re.M)
    return ("/* LOCAL FIT. scripts/localfit.mjs, ds-models' fit method (team/contracts/fit.md), wrapped by\n"
            "   scripts/32_local.py. Edit the module, not this. */\n"
            f"const LOCALFIT = (() => {{\n{body}\nreturn {{{', '.join(names)}}};\n}})();\n")


# ------------------------------------------------------------------ the page
b19 = _load("19_pages.py", "b19")
b20 = _load("20_landing.py", "b20")
import mark  # noqa: E402
import pagemin  # noqa: E402

SITE = b19.b17.SITE
REPO = b19.REPO
esc = b20.esc
ICON, HEAD_THEME, THEME_JS = b20.ICON, b20.HEAD_THEME, b20.THEME_JS


def rel(tail: str = "") -> str:
    """A link out of `docs/<slug>/`. One level down, so everything site-wide is `../`."""
    return "../" + tail


# The quants `bestQuant()` can choose: fit.mjs's GGUF and MLX ladders. Read off the module rather than
# restated, so a quant ds-models adds to a ladder reaches the page without an edit here.
def ladder() -> set[str]:
    src = FIT_MJS.read_text(encoding="utf-8")
    return {q for name in ("GGUF_LADDER", "MLX_LADDER")
            for q in re.findall(r"'([^']+)'", re.search(rf"{name} = \[([^\]]*)\]", src).group(1))}


def slim(p: dict) -> dict:
    """A pick as the page needs it. Files no ladder reaches (BF16, Q4_1 and the like) are dropped, about 20 KB of
    the page: `bestQuant()` never chooses them, so no answer changes -- the browser check
    holds the picker to the cheat sheet, which is computed from the full file -- and the expert view's quant
    menu offers what the method can rate. `quant_by_budget_gb` is ds-models' static guide for pages without
    the method; this one has the method."""
    keep = ladder() | {p["default_quant"]}
    model = dict(p["model"], quants=[q for q in p["model"]["quants"] if q["quant"] in keep])
    return {k: v for k, v in dict(p, model=model).items() if k != "quant_by_budget_gb"}


def payload(cat: dict, picks: dict, hf: dict) -> dict:
    """Everything the page script reads, in one object. Compact keys are not worth it: gzip already
    collapses the repetition, and readable keys are what lets a reader of the page source check a number.
    `hf` is the joined slice of eng-hf's index (see `hf_join`), carried in its own column-list shape."""
    return {
        "page": PAGE,
        "kinds": cat["kinds"], "devices": cat["devices"], "gpus": cat["gpus"], "custom": cat["custom"],
        "find_out": cat["find_out"],
        "tasks": [{"id": t, "label": l} for t, l in TASKS], "models": [slim(p) for p in picks["picks"]], "hf": hf or None,
        "runtimes": picks.get("runtimes"),
        "default_ctx": DEFAULT_CTX, "runner_ctx": RUNNER_CTX,
        "howto": HOWTO,
        "fixture": bool(cat.get("fixture")),
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
            '<th scope="col">Also runs, more slowly or squeezed</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')


def render(cat: dict, picks: dict, hf: dict) -> str:
    title = f"{PAGE['title']}: what AI can your computer run? | Awesome Agentic Atlas"
    n = sum(1 for p in picks["picks"] if not embed_only(p))
    desc = (f"Pick your laptop, Mac, gaming PC or handheld and see which of {n} open AI models will run on it, "
            "how fast, and the exact steps to run them with LM Studio or Ollama. Free, private, works offline.")
    url = SITE + PAGE["slug"] + "/"
    tasks = "".join(f'<label class="chip lxchip"><input type="checkbox" name="task" value="{esc(t)}">'
                    f'<span>{esc(label)}</span></label>' for t, label in TASKS)
    fixture = ('<p class="lxfix" role="note">Preview data: the hardware list is a placeholder while the '
               'catalogue is finished, so a machine&rsquo;s numbers may be off. Treat every answer as a rough guide.</p>'
               if cat.get("fixture") else "")
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
  <p class="lxquiet">The same maths as the picker, for some common machines, at an {DEFAULT_CTX // 1024}k context.</p>
  {cheat_html(cheat_rows(picks, cheat_answers(picks, hf)))}
</section>

<section class="lxs" id="learn" aria-labelledby="learnh">
  <h2 id="learnh">The three ideas that explain everything</h2>
  <details id="q-quant"><summary>What&rsquo;s a quantisation (Q4, Q8)?</summary>
    <p>A model is billions of numbers. Quantising stores each one with fewer digits, the way a JPEG shrinks a
      photo. <b>Q8</b> keeps 8 bits a number, about half the original size, and most people can&rsquo;t tell
      it from the original. <b>Q4</b> is under a third of the size and slightly worse. Below about 3 bits,
      answers get noticeably worse. We pick the best version that runs well on your machine, and we say when
      we had to squeeze one.</p></details>
  <details id="q-ctx"><summary>Why does context length cost memory?</summary>
    <p>Context is how much the model can keep in mind at once: your conversation so far, or a document you
      paste in. It sets aside memory for that up front, a little for every word it might hold, and how much
      varies a lot between models: Llama 3.1 8B needs about 130 MB per 1,000 tokens, while Qwen3.5 9B needs
      about 33 MB, because most of its layers keep no such memory. We assume about 8,000 tokens (around 12
      pages), which is plenty for a chat. Pasting in a whole book needs much more, and on a small machine
      that can be the difference between fitting and not. &ldquo;Show the numbers&rdquo; gives each
      model&rsquo;s own figure.</p></details>
  <details id="q-offload"><summary>What does &ldquo;offload&rdquo; mean?</summary>
    <p>A graphics card has its own fast memory. If a model doesn&rsquo;t fit in it, part can live in your
      ordinary RAM instead and run on the main processor. For most models that is much slower, because every
      word waits for the slow part: a big 70B model split this way writes about 2 words a second. Models
      called &ldquo;mixture of experts&rdquo; (names with A3B or A4B in them) are the exception. They only
      use a small part of themselves for each word, so the part kept in RAM is touched lightly, and they
      often still run well.</p></details>
  <details id="q-unified"><summary>Why does my Mac or handheld say less than its memory?</summary>
    <p>Macs, Steam Decks and similar machines share one pool of memory between the processor and the
      graphics. That&rsquo;s great for AI, because the graphics can use most of it, but the system keeps
      some for itself. On a Mac, macOS lets the graphics use two-thirds of the memory by default on Macs up to
      32 GB, and three-quarters on bigger ones.</p></details>
  <details id="q-tokens"><summary>What&rsquo;s a token?</summary>
    <p>The piece of text a model reads and writes at a time: usually part of a word. One English word is
      about 1.3 tokens, so 10 tokens a second is about 7 or 8 words a second, faster than most people
      read.</p></details>
  <details id="q-how"><summary>How we worked these numbers out</summary>
    <p>A model needs its download size, plus memory for its context, plus a little working space. Your
      machine offers a share of its memory, by one rule for each kind of machine: what a graphics card keeps
      for its driver and the screen, what macOS lets the graphics use, what Windows keeps for itself. Speed
      comes from how fast that memory can be read, because writing each word means reading the active part of
      the model once. The method is fitted to 144 published speed measurements across Macs, NVIDIA, AMD and
      Intel graphics, handhelds and processors, and lands within about 5% of them typically and 17% at worst
      for nine in ten. Real speed also depends on the app, drivers and settings, so every speed is shown as a
      range. The method is written up
      <a href="https://github.com/{esc(REPO)}/blob/HEAD/scripts/localfit.mjs">with its sources</a>.</p></details>
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
{fit_js()}</script>
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
    # Comments stripped on the way out, the way `19_pages.py` and `31_home.py` ship theirs: they are for
    # whoever edits this stage, `local_page.js` and ds-models' module, and every one stays in the source.
    page.write_text(pagemin.strip_page(render(cat, picks, hf)), encoding="utf-8")
    print(f"{PAGE['slug']}/index.html · {b20.kb(page.stat().st_size)} · {len(cat['devices'])} devices, "
          f"{len(cat['gpus'])} graphics cards, {len(picks['picks'])} picks"
          + (f", {len(hf)} joined to the Hugging Face index" if hf else ", no Hugging Face index yet")
          + (" · FIXTURE hardware" if cat.get("fixture") else ""))
    print("sitemap.xml carries this URL via scripts/20_landing.py")


if __name__ == "__main__":
    main()
