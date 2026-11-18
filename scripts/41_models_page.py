"""Render the models catalogue, `docs/models/index.html`, from the committed `docs/models.json`.

`40_models.py` builds the index; this draws it. The page is for browsing: by family, by size, by what a
model is for, and by the format a reader's tools want. Each model shows the facts that decide whether it
is worth a download -- parameters (and active parameters for a MoE), context, licence, the size of its
common 4-bit GGUF -- and opens into every quantisation of every trusted variant with its exact size and
the command that runs it. The question "will it fit on *my* machine" is the local-AI page's, which reads
the same file; this page does not guess at hardware.

    python scripts/41_models_page.py
    python scripts/24_pwa.py           # re-version the worker afterwards, as for any page

THE LICENCE IS SHOWN, NOT IMPLIED. Every card prints the licence by name with its kind: *permissive*
(Apache, MIT and friends), *copyleft*, *non-commercial*, or *custom* -- Llama's and Gemma's terms, the
OpenRAILs, and anything the card calls `other` -- which means "read it before you ship", not "closed".
A gated original says so too: its weights need an accepted licence on Hugging Face, even when a quant
repo of it does not ask.

HOW IT RENDERS. The first FIRST_PAINT models, by popularity, are written into the page as HTML, so the
page reads without script and paints before the data arrives. The script then fetches `models.json` and
redraws the list from it with the filters in the URL hash:
`#use=code&size=m&fmt=gguf&lic=permissive&fam=qwen3&q=coder`. The service worker does not route that file
(`24_pwa.DATA_FILES` lists the atlas's own data files), so offline the page keeps its first paint; routing
it there would be a change to `24_pwa.py`, not to this page. The card markup is written twice, here in `card()` and in the page script's `card()`, and
`tests/models_test.py` runs the script's marked CARD CORE block under Node over real rows and requires
byte-identical output, so the two cannot drift.

Theme tokens only, the thirteen every theme declares (see `tests/theme_test.py`), and the shared
`pages.css`; nothing here changes the shared layout. Reads `docs/models.json` and nothing else, so it runs
on any checkout.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "docs" / "models" / "index.html"
DATA = ROOT / "docs" / "models.json"
FIRST_PAINT = 60


def _load(name: str, alias: str):
    # The same reuse-if-loaded dynamic import as `25_collections.py`, for the same reason.
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, HERE / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


b25 = _load("25_collections.py", "b25")
b19, b20 = b25.b19, b25.b20
sys.path.insert(0, str(HERE))
import mark  # noqa: E402
import sitewide  # noqa: E402

SITE, REPO = b25.SITE, b25.REPO
esc, clip = b20.esc, b20.clip
THEME_JS = b20.THEME_JS

# Size buckets by total parameters: the ranges people talk about hardware in.
SIZES = [("xs", "up to 4B", 0, 4.5e9), ("s", "4–10B", 4.5e9, 10.5e9), ("m", "10–20B", 10.5e9, 20.5e9),
         ("l", "20–40B", 20.5e9, 40.5e9), ("xl", "40–80B", 40.5e9, 80.5e9), ("xxl", "80B+", 80.5e9, 1e15)]
USE_LABEL = {"chat": "Chat", "reasoning": "Reasoning", "code": "Code", "tools": "Tool calling",
             "vision": "Vision", "embed": "Embeddings", "rerank": "Reranker", "asr": "Speech to text",
             "tts": "Text to speech", "base": "Base model"}
FMT_LABEL = {"gguf": "GGUF", "mlx": "MLX", "awq": "AWQ", "gptq": "GPTQ", "bnb": "bitsandbytes", "fp8": "FP8",
             "safetensors": "Safetensors"}
KIND_LABEL = {"permissive": "Permissive", "copyleft": "Copyleft", "custom": "Custom terms",
              "non-commercial": "Non-commercial"}


def rows(doc: dict) -> list[dict]:
    """The model rows as objects, variants and files too."""
    out = []
    for r in doc["models"]:
        m = dict(zip(doc["cols"], r))
        m["variants"] = [dict(zip(doc["variant_cols"], v)) for v in m["variants"]]
        for v in m["variants"]:
            v["files"] = [dict(zip(doc["file_cols"], f)) for f in v["files"]]
        out.append(m)
    return out


def num(n: int | None) -> str:
    """8190735360 -> 8.2B; 600000000 -> 600M. Parameters and context alike, in the units people use."""
    if not n:
        return "?"
    for div, unit in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if n >= div:
            v = n / div
            s = f"{v:.1f}" if v < 10 else f"{v:.0f}"
            return s.rstrip("0").rstrip(".") + unit if "." in s else s + unit
    return str(n)


def ctxs(n: int | None) -> str:
    """Context in K tokens, binary as the configs write it: 32768 -> 32K, 131072 -> 128K."""
    if not n:
        return "?"
    return f"{n // 1024}K" if n >= 1024 and n % 1024 == 0 else num(n)


def gb(n: int) -> str:
    """Decimal gigabytes, the unit drives and downloads are sold in, to one place."""
    return f"{n / 1e9:.1f} GB" if n >= 1e9 else f"{n / 1e6:.0f} MB"


def pick(m: dict) -> tuple[dict, dict] | None:
    """(variant, file) a reader most likely wants: a Q4_K_M GGUF from the most downloaded GGUF variant
    that has one, else that variant's file nearest 4.8 bits, else the smallest MLX 4-bit, else None."""
    for v in m["variants"]:
        if v["fmt"] == "gguf":
            f = next((f for f in v["files"] if f["q"] == "Q4_K_M"), None)
            if f:
                return v, f
    for v in m["variants"]:
        if v["fmt"] == "gguf" and v["files"]:
            return v, min(v["files"], key=lambda f: abs((f["bpw"] or 4.8) - 4.8))
    for v in m["variants"]:
        if v["fmt"] == "mlx" and v["files"] and v["files"][0]["q"].startswith("4bit"):
            return v, v["files"][0]
    return None


def size_bucket(p: int | None) -> str:
    if not p:
        return ""
    return next(k for k, _, lo, hi in SIZES if lo <= p < hi)


def card(m: dict, lic_kind: dict) -> str:
    """One card. Mirrored by `card()` in the page script below: change both, the test compares them."""
    facts = [f"<b>{num(m['params'])}</b> params"] if m["params"] else []
    if m["active"]:
        facts.append(f"<b>{num(m['active'])}</b> active")
    if m["ctx"]:
        facts.append(f"<b>{ctxs(m['ctx'])}</b> context")
    if m["arch"]:
        facts.append(esc(m["arch"]))
    kind = lic_kind.get(m["license"] or "", {}).get("kind", "custom")
    lname = lic_kind.get(m["license"] or "", {}).get("name") or "No licence stated"
    if m["license"] == "other" and m["license_name"]:
        lname = m["license_name"]
    lic = (f'<a class="lic lic-{kind}" href="{esc(m["license_url"])}" rel="noopener">{esc(lname)}</a>'
           if m["license_url"] else f'<span class="lic lic-{kind}">{esc(lname)}</span>')
    lic += f' <span class="lick">{KIND_LABEL[kind]}</span>'
    if m["gated"]:
        lic += ' <span class="gate" title="The original repository asks you to accept its licence before downloading">gated</span>'
    tags = "".join(f'<span class="tag">{USE_LABEL[u]}</span>' for u in m["uses"])
    if "uncensored" in m["flags"]:
        tags += '<span class="tag flag">uncensored</span>'
    if "community" in m["flags"]:
        tags += '<span class="tag flag">community</span>'
    nq = sum(len(v["files"]) for v in m["variants"])
    run = []
    p = pick(m)
    if p:
        v, f = p
        run.append(f'{FMT_LABEL[v["fmt"]]} {esc(f["q"])} <b>{gb(f["bytes"])}</b>')
    run.append(f"{len(m['variants'])} variant{'s' if len(m['variants']) != 1 else ''} · {nq} file{'s' if nq != 1 else ''}")
    if m["ollama"]:
        run.append(f'<code class="cmd">ollama run {esc(m["ollama"]["name"])}:{esc(m["ollama"]["tag"])}</code>')
    return (f'<li class="mcard" data-id="{esc(m["id"])}"><div class="mhd"><h2><a href="https://huggingface.co/{esc(m["id"])}" '
            f'rel="noopener">{esc(m["name"])}</a></h2><span class="mby">{esc(m["author"])} · {esc(m["family"])}</span></div>'
            f'<p class="mfacts">{" · ".join(facts)}</p><p class="mlic">{lic}</p><p class="mtags">{tags}</p>'
            f'<p class="mrun">{" · ".join(run)}</p>'
            f'<details class="mq"><summary>Every quantisation and how to run it</summary><div class="mqb"></div></details></li>')


CSS = """<style>
/* The models page. Tokens only -- the thirteen every theme declares -- so every theme repaints it. */
.mtools{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:flex-end;margin:18px 0 6px}
.mtools label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 4px}
.mtools input,.mtools select{font:14px var(--ui);color:var(--ink);background:var(--plane);border:1px solid var(--grid);
  border-radius:7px;padding:7px 10px;min-height:36px}
.mtools input{min-width:min(340px,80vw)}
.mtools input:focus-visible,.mtools select:focus-visible,.mgrp button:focus-visible,.mcard a:focus-visible,
.mq summary:focus-visible,#mmore:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.mgrp{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0}
.mgrp .gl{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);align-self:center;min-width:64px}
.mgrp button{font:13px var(--ui);color:var(--ink2);background:var(--band);border:1px solid var(--grid);border-radius:999px;
  padding:5px 11px;min-height:32px;cursor:pointer}
.mgrp button[aria-pressed=true]{background:var(--bar);color:var(--onbar);border-color:var(--bar)}
#mcount{color:var(--muted);font-size:13px;margin:14px 0 8px}
.mlist{list-style:none;margin:0;padding:0;display:grid;align-items:start;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:12px}
.mcard{background:var(--panel);border:1px solid var(--grid);border-radius:10px;padding:14px 16px;min-width:0}
.mhd{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px}
.mcard h2{font-size:16px;margin:0;overflow-wrap:anywhere}
.mcard h2 a{color:var(--ink)}
.mby{color:var(--muted);font-size:12.5px}
.mfacts{margin:6px 0 0;font-size:13.5px;color:var(--ink2)}
.mfacts b{color:var(--ink)}
.mlic,.mtags,.mrun{margin:7px 0 0;font-size:13px;color:var(--ink2)}
.mrun b{color:var(--ink)}
.mrun code.cmd{white-space:nowrap;display:inline-block;max-width:100%;overflow:hidden;text-overflow:ellipsis;vertical-align:bottom}
.lic{font-weight:600}
.lic-permissive{color:var(--good)}
.lic-copyleft{color:var(--link)}
.lic-custom{color:var(--bar)}
.lic-non-commercial{color:var(--warn)}
.lick{color:var(--muted);font-size:12px}
.gate{font:600 11px var(--mono);color:var(--warn);border:1px solid var(--warn);border-radius:5px;padding:1px 6px}
.tag.flag{color:var(--muted)}
.mq{margin-top:9px}
.mq summary{cursor:pointer;color:var(--link);font-size:13px}
.mqb{overflow-x:auto}
.mqb table{font-size:12.5px;margin-top:8px}
.mqb td,.mqb th{padding:4px 8px 4px 0;text-align:left;vertical-align:top;border-bottom:1px solid var(--grid)}
.mqb .qs{display:flex;flex-wrap:wrap;gap:4px}
.mqb .q{font:12px var(--mono);background:var(--band);border:1px solid var(--grid);border-radius:5px;padding:1px 6px;white-space:nowrap}
.mqb code.cmd{font-size:12px;white-space:normal;overflow-wrap:anywhere}
#mmore{margin:16px 0}
.mfam{display:flex;flex-wrap:wrap;gap:6px}
@media (max-width:640px){.mgrp .gl{min-width:100%}}
</style>
"""


def page(doc: dict) -> str:
    ms = rows(doc)
    lk = doc["licenses"]
    c = doc["counts"]
    url = SITE + "models/"
    depth = 1
    fams: dict[str, list] = {}
    for m in ms:
        fams.setdefault(m["family"], []).append(m)
    top_fams = sorted(fams.items(), key=lambda kv: -sum(m["downloads_all"] for m in kv[1]))[:48]
    fam_chips = "".join(
        f'<a class="chip" href="#fam={esc(f.lower())}">{esc(f)} <span class="ct">{len(v)}</span></a>' for f, v in top_fams)
    nq = sum(1 for m in ms if any(v["fmt"] in ("gguf", "mlx", "awq", "gptq") for v in m["variants"]))
    desc = clip(f"{c['models']} open models for agents -- chat, reasoning, code, tool calling, vision, embeddings and "
                f"speech -- with {c['files']:,} quantisations and their exact sizes, licences, and how to run each locally.", 158)

    def grp(key, label, opts):
        return (f'<div class="mgrp" role="group" aria-label="{esc(label)}"><span class="gl">{esc(label)}</span>'
                + "".join(f'<button type="button" data-f="{key}" data-v="{esc(v)}" aria-pressed="false">{esc(t)}</button>'
                          for v, t in opts) + "</div>")

    uses_present = [u for u in doc["uses"] if any(u in m["uses"] for m in ms)]
    tools = (f"""<div class="mtools">
  <div><label for="mq">Search</label><input id="mq" type="search" placeholder="Model, family, author or quantiser" autocomplete="off"></div>
  <div><label for="msort">Sort</label><select id="msort">
    <option value="pop">Most used (all variants)</option><option value="trend">Trending</option>
    <option value="new">Newest</option><option value="small">Smallest first</option><option value="big">Largest first</option>
    <option value="ctx">Longest context</option></select></div>
</div>
{grp("use", "Use", [(u, USE_LABEL[u]) for u in uses_present])}
{grp("size", "Size", [(k, t) for k, t, _, _ in SIZES])}
{grp("fmt", "Format", [("gguf", "GGUF"), ("mlx", "MLX"), ("awq", "AWQ / GPTQ"), ("fp8", "FP8")])}
{grp("lic", "Licence", [(k, KIND_LABEL[k]) for k in ("permissive", "copyleft", "custom", "non-commercial")])}""")

    first = "\n".join(card(m, lk) for m in ms[:FIRST_PAINT])
    return b25.head(f"Models: open weights for agents, with every quantisation — Awesome Agentic Atlas", desc, url, depth) + CSS + f"""<body>
<header><div class="wrap">
  <nav class="brandbar">{mark.brand(b25.rel(depth))}</nav><div class="top">
  <div>
    <p class="kick">The weights</p>
    <h1>Models</h1>
    <p class="sub"><b>{c['models']:,}</b> models · <b>{c['families']:,}</b> families · <b>{c['variants']:,}</b> runnable
      copies · <b>{c['files']:,}</b> quantisations · snapshot {esc(doc['snapshot'])}</p>
    <p class="intro">The open models people build agents on, from Hugging Face: chat and reasoning models, coders,
      tool callers, vision-language models, embeddings, rerankers and speech. Each one is gathered with every
      re-packaging a trusted quantiser publishes &mdash; GGUF for llama.cpp, Ollama and LM Studio, MLX for Apple
      silicon, AWQ, GPTQ and FP8 for vLLM &mdash; and every quantisation's exact download size. {nq:,} of them run
      locally from one of those.</p>
  </div>
{b25.nav(depth)}
</div></div></header>

<main><div class="wrap">
{tools}
<p id="mcount" aria-live="polite">The {min(FIRST_PAINT, len(ms))} most used of {len(ms):,}. Filters load with the data.</p>
<ol class="mlist" id="mlist">
{first}
</ol>
<button class="chip" id="mmore" type="button" hidden>Show more</button>

<section class="allin">
  <h2>Families</h2>
  <p>The {len(top_fams)} most used. A family is read off the model's name, so it groups releases rather than
    vouching for lineage.</p>
  <div class="mfam">{fam_chips}</div>
</section>

<section class="allin">
  <h2>How this is made</h2>
  <p>A weekly read of the Hugging Face Hub's public API. A model is kept when it is popular in its own right or
    can be run locally from a trusted re-packaging, and every re-packaging of it &mdash; from its own lab, or from
    bartowski, unsloth, lmstudio-community, ggml-org, mlx-community, RedHatAI or hugging-quants &mdash; is one
    entry under it rather than a model of its own. Sizes are the files' own byte counts, split parts summed, in
    decimal gigabytes. NSFW-tagged repos, adapters, empty cards, small merges and long-abandoned forks are left
    out. The whole index is <a href="{b25.rel(depth, 'models.json')}">one JSON file</a>, documented in the
    <a href="https://github.com/{esc(REPO)}/blob/HEAD/handbook/pipeline.md#the-models-index">handbook</a>.</p>
  <p>Licences are as each model's card states them. <span class="lic lic-custom">Custom terms</span> means the
    model has its own licence (Llama, Gemma, OpenRAIL and others) that you should read before shipping it;
    <span class="gate">gated</span> means the original repository asks you to accept that licence first.</p>
</section>
</div></main>

<footer><div class="wrap">
  {sitewide.buildtags(REPO)}
  Part of the <a href="{b25.rel(depth)}">Awesome Agentic Atlas</a>. Model data from the
  <a href="https://huggingface.co/models">Hugging Face Hub</a> on {esc(doc['snapshot'])}; downloads are the Hub's
  thirty-day counts and drift daily. Ollama tags are matched by name and checked against the GGUF sizes where
  possible; <code>ollama run hf.co/&lt;repo&gt;:&lt;quant&gt;</code> works for every GGUF here regardless.
</div></footer>
{SCRIPT}
{sitewide.site_script(b25.rel(depth))}{THEME_JS}{b19.follow()}{b19.beacon()}{b19.telemetry(b25.rel(depth))}</body>
</html>
"""


SCRIPT = r"""<script>
(function () {
  "use strict";
  /* CARD CORE: no DOM below this line until END CARD CORE. tests/models_test.py runs exactly this block
     under Node and requires its card() to print what card() in scripts/41_models_page.py prints. */
  var USE = {chat:"Chat",reasoning:"Reasoning",code:"Code",tools:"Tool calling",vision:"Vision",embed:"Embeddings",
             rerank:"Reranker",asr:"Speech to text",tts:"Text to speech",base:"Base model"};
  var FMT = {gguf:"GGUF",mlx:"MLX",awq:"AWQ",gptq:"GPTQ",bnb:"bitsandbytes",fp8:"FP8",safetensors:"Safetensors"};
  var KIND = {permissive:"Permissive",copyleft:"Copyleft",custom:"Custom terms","non-commercial":"Non-commercial"};
  var SIZES = [["xs",0,4.5e9],["s",4.5e9,10.5e9],["m",10.5e9,20.5e9],["l",20.5e9,40.5e9],["xl",40.5e9,80.5e9],["xxl",80.5e9,1e15]];
  var lic = {};

  function h(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;"}[c]; }); }  // html.escape's spelling, so both copies agree
  function num(n) {
    if (!n) return "?";
    var u = [[1e12,"T"],[1e9,"B"],[1e6,"M"],[1e3,"K"]];
    for (var i = 0; i < u.length; i++) if (n >= u[i][0]) {
      var v = n / u[i][0], s = v < 10 ? v.toFixed(1) : v.toFixed(0);
      if (s.indexOf(".") >= 0) s = s.replace(/0+$/, "").replace(/\.$/, "");
      return s + u[i][1];
    }
    return String(n);
  }
  function ctxs(n) { return !n ? "?" : (n >= 1024 && n % 1024 === 0 ? (n / 1024 | 0) + "K" : num(n)); }
  function gb(n) { return n >= 1e9 ? (n / 1e9).toFixed(1) + " GB" : Math.round(n / 1e6) + " MB"; }
  function obj(cols, r) { var o = {}; for (var i = 0; i < cols.length; i++) o[cols[i]] = r[i]; return o; }
  function pick(m) {
    var i, v, f;
    for (i = 0; i < m.variants.length; i++) { v = m.variants[i];
      if (v.fmt === "gguf") for (var j = 0; j < v.files.length; j++) if (v.files[j].q === "Q4_K_M") return [v, v.files[j]]; }
    for (i = 0; i < m.variants.length; i++) { v = m.variants[i];
      if (v.fmt === "gguf" && v.files.length) {
        f = v.files.slice().sort(function (a, b) { return Math.abs((a.bpw || 4.8) - 4.8) - Math.abs((b.bpw || 4.8) - 4.8); })[0];
        return [v, f]; } }
    for (i = 0; i < m.variants.length; i++) { v = m.variants[i];
      if (v.fmt === "mlx" && v.files.length && v.files[0].q.indexOf("4bit") === 0) return [v, v.files[0]]; }
    return null;
  }
  // The same card as card() in scripts/41_models_page.py. tests/models_test.py compares the two.
  function card(m) {
    var facts = m.params ? ["<b>" + num(m.params) + "</b> params"] : [];
    if (m.active) facts.push("<b>" + num(m.active) + "</b> active");
    if (m.ctx) facts.push("<b>" + ctxs(m.ctx) + "</b> context");
    if (m.arch) facts.push(h(m.arch));
    var L = lic[m.license || ""] || {}, kind = L.kind || "custom", lname = L.name || "No licence stated";
    if (m.license === "other" && m.license_name) lname = m.license_name;
    var l = m.license_url ? '<a class="lic lic-' + kind + '" href="' + h(m.license_url) + '" rel="noopener">' + h(lname) + "</a>"
                          : '<span class="lic lic-' + kind + '">' + h(lname) + "</span>";
    l += ' <span class="lick">' + KIND[kind] + "</span>";
    if (m.gated) l += ' <span class="gate" title="The original repository asks you to accept its licence before downloading">gated</span>';
    var tags = m.uses.map(function (u) { return '<span class="tag">' + USE[u] + "</span>"; }).join("");
    if (m.flags.indexOf("uncensored") >= 0) tags += '<span class="tag flag">uncensored</span>';
    if (m.flags.indexOf("community") >= 0) tags += '<span class="tag flag">community</span>';
    var nq = 0; m.variants.forEach(function (v) { nq += v.files.length; });
    var run = [], p = pick(m);
    if (p) run.push(FMT[p[0].fmt] + " " + h(p[1].q) + " <b>" + gb(p[1].bytes) + "</b>");
    run.push(m.variants.length + " variant" + (m.variants.length !== 1 ? "s" : "") + " · " + nq + " file" + (nq !== 1 ? "s" : ""));
    if (m.ollama) run.push('<code class="cmd">ollama run ' + h(m.ollama.name) + ":" + h(m.ollama.tag) + "</code>");
    return '<li class="mcard" data-id="' + h(m.id) + '"><div class="mhd"><h2><a href="https://huggingface.co/' + h(m.id) +
      '" rel="noopener">' + h(m.name) + '</a></h2><span class="mby">' + h(m.author) + " · " + h(m.family) + "</span></div>" +
      '<p class="mfacts">' + facts.join(" · ") + '</p><p class="mlic">' + l + '</p><p class="mtags">' + tags + "</p>" +
      '<p class="mrun">' + run.join(" · ") + "</p>" +
      '<details class="mq"><summary>Every quantisation and how to run it</summary><div class="mqb"></div></details></li>';
  }
  /* END CARD CORE */
  var PAGE = 60;
  var list = document.getElementById("mlist"), count = document.getElementById("mcount"),
      more = document.getElementById("mmore"), q = document.getElementById("mq"), sort = document.getElementById("msort");
  var all = [], shown = PAGE, state = {use: [], size: [], fmt: [], lic: [], fam: "", q: "", sort: "pop"};
  function runs(v, f) {
    if (v.fmt === "gguf") return "llama-server -hf " + v.repo + ":" + f.q + "\nollama run hf.co/" + v.repo + ":" + f.q;
    if (v.fmt === "mlx") return "mlx_lm.generate --model " + v.repo + ' --prompt "hello"';
    if (v.fmt === "awq" || v.fmt === "gptq" || v.fmt === "fp8" || v.fmt === "safetensors") return "vllm serve " + v.repo;
    return "";
  }
  function quants(m) {
    var rows = m.variants.map(function (v) {
      var fs = v.files.map(function (f) {
        return '<span class="q" title="' + f.parts + " file" + (f.parts > 1 ? "s" : "") + (f.bpw ? ", " + f.bpw + " bits per weight" : "") +
          '">' + h(f.q) + " " + gb(f.bytes) + "</span>"; }).join("");
      // The command names Q4_K_M where there is one -- the quant most guides start from -- else the middle.
      var mid = v.files.filter(function (f) { return f.q === "Q4_K_M"; })[0] || v.files[Math.floor((v.files.length - 1) / 2)] || {};
      var mm = v.mmproj ? " + " + gb(v.mmproj) + " vision projector" : "";
      return "<tr><td><a href=\"https://huggingface.co/" + h(v.repo) + '" rel="noopener">' + h(v.repo) + "</a><br>" + FMT[v.fmt] +
        " · " + h(v.by) + " · " + num(v.downloads) + " downloads" + h(mm) + '</td><td><div class="qs">' + fs + "</div>" +
        (runs(v, mid) ? '<code class="cmd">' + h(runs(v, mid)).replace(/\n/g, "<br>") + "</code>" : "") + "</td></tr>";
    }).join("");
    return "<table><thead><tr><th>Repository</th><th>Quantisations (exact sizes) and a command</th></tr></thead><tbody>" + rows + "</tbody></table>";
  }
  function bucket(p) { for (var i = 0; i < SIZES.length; i++) if (p >= SIZES[i][1] && p < SIZES[i][2]) return SIZES[i][0]; return ""; }
  function passes(m) {
    if (state.use.length && !state.use.some(function (u) { return m.uses.indexOf(u) >= 0; })) return false;
    if (state.size.length && state.size.indexOf(bucket(m.params || 0)) < 0) return false;
    if (state.fmt.length && !m.variants.some(function (v) {
      return state.fmt.indexOf(v.fmt) >= 0 || (state.fmt.indexOf("awq") >= 0 && v.fmt === "gptq"); })) return false;
    if (state.lic.length && state.lic.indexOf((lic[m.license || ""] || {}).kind || "custom") < 0) return false;
    if (state.fam && m.family.toLowerCase() !== state.fam) return false;
    if (state.q) {
      var hay = (m.id + " " + m.family + " " + m.arch + " " + m.variants.map(function (v) { return v.repo; }).join(" ")).toLowerCase();
      if (!state.q.split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; })) return false;
    }
    return true;
  }
  var SORTS = {
    pop: function (a, b) { return b.downloads_all - a.downloads_all; },
    trend: function (a, b) { return (b.trending || 0) - (a.trending || 0); },
    "new": function (a, b) { return (b.created || "").localeCompare(a.created || ""); },
    small: function (a, b) { return (a.params || 1e18) - (b.params || 1e18); },
    big: function (a, b) { return (b.params || 0) - (a.params || 0); },
    ctx: function (a, b) { return (b.ctx || 0) - (a.ctx || 0); }
  };
  function readHash() {
    var p = new URLSearchParams(location.hash.slice(1));
    ["use", "size", "fmt", "lic"].forEach(function (k) { state[k] = (p.get(k) || "").split(",").filter(Boolean); });
    state.fam = (p.get("fam") || "").toLowerCase(); state.q = (p.get("q") || "").toLowerCase().trim();
    state.sort = SORTS[p.get("sort")] ? p.get("sort") : "pop";
  }
  function writeHash() {
    var p = new URLSearchParams();
    ["use", "size", "fmt", "lic"].forEach(function (k) { if (state[k].length) p.set(k, state[k].join(",")); });
    if (state.fam) p.set("fam", state.fam); if (state.q) p.set("q", state.q); if (state.sort !== "pop") p.set("sort", state.sort);
    var s = p.toString(); history.replaceState(null, "", s ? "#" + s : location.pathname + location.search);
  }
  function sync() {
    document.querySelectorAll(".mgrp button").forEach(function (b) {
      b.setAttribute("aria-pressed", state[b.dataset.f].indexOf(b.dataset.v) >= 0 ? "true" : "false"); });
    q.value = state.q; sort.value = state.sort;
  }
  function draw() {
    var hit = all.filter(passes).sort(SORTS[state.sort]);
    list.innerHTML = hit.slice(0, shown).map(card).join("");
    more.hidden = hit.length <= shown;
    count.textContent = hit.length === all.length ? "All " + all.length.toLocaleString() + " models" + (hit.length > shown ? ", the first " + shown + " shown." : ".")
      : hit.length.toLocaleString() + " of " + all.length.toLocaleString() + " models" + (state.fam ? " in " + state.fam : "") + (hit.length > shown ? ", the first " + shown + " shown." : ".");
  }
  list.addEventListener("toggle", function (e) {
    var d = e.target; if (!d.open || !all.length) return;
    var li = d.closest(".mcard"), box = d.querySelector(".mqb");
    if (box.childNodes.length) return;
    var m = all.filter(function (x) { return x.id === li.dataset.id; })[0];
    if (m) box.innerHTML = quants(m);
  }, true);
  document.querySelectorAll(".mgrp button").forEach(function (b) {
    b.addEventListener("click", function () {
      var a = state[b.dataset.f], i = a.indexOf(b.dataset.v);
      if (i >= 0) a.splice(i, 1); else a.push(b.dataset.v);
      shown = PAGE; writeHash(); sync(); if (all.length) draw();
    });
  });
  var t; q.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () {
    state.q = q.value.toLowerCase().trim(); shown = PAGE; writeHash(); if (all.length) draw(); }, 150); });
  sort.addEventListener("change", function () { state.sort = sort.value; writeHash(); if (all.length) draw(); });
  more.addEventListener("click", function () { shown += PAGE * 2; draw(); });
  window.addEventListener("hashchange", function () { readHash(); sync(); shown = PAGE; if (all.length) draw(); });
  readHash(); sync();
  fetch("../models.json").then(function (r) { return r.json(); }).then(function (d) {
    lic = d.licenses;
    all = d.models.map(function (r) {
      var m = obj(d.cols, r);
      m.variants = m.variants.map(function (v) { v = obj(d.variant_cols, v);
        v.files = v.files.map(function (f) { return obj(d.file_cols, f); }); return v; });
      return m;
    });
    draw();
  }).catch(function () { count.textContent = "The full index could not be loaded; the most used models are shown."; });
})();
</script>"""


def urls() -> list[str]:
    """The one URL this stage publishes, for `20_landing.py`'s sitemap -- the same arrangement Discover has,
    and for the same reason: `tests/indexnow_test.py` requires every `docs/**/index.html` in a sitemap."""
    return [SITE + "models/"]


def main() -> None:
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    html = page(doc)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"docs/models/index.html · {doc['counts']['models']} models, first {FIRST_PAINT} in the page · {b20.kb(len(html.encode()))}")


if __name__ == "__main__":
    main()
