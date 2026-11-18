"""The models index: the Hugging Face models people run agents on, with every runnable copy and its exact size.

The rest of the atlas is GitHub repositories. This stage is the other half of an agentic stack -- the
weights -- and it is built for one question above all: *what can I run on this machine, and how?* The
local-AI page answers that from `docs/models.json`, so the file carries what fit maths needs (parameter
counts, MoE routing, context length, layers and KV heads) and what a download needs (every GGUF, MLX,
AWQ, GPTQ and FP8 re-packaging from a trusted quantiser, one row per quantisation, exact bytes). The
models catalogue page (`41_models_page.py`) is drawn from the same file.

    python scripts/40_models.py              # fetch what moved, rebuild docs/models.json, print a report
    python scripts/40_models.py --dry-run    # ...and write nothing
    python scripts/40_models.py --offline    # build from cache/hf/ alone: no network, stale is fine
    python scripts/40_models.py --status     # report on the committed file: no network

HOW IT ASKS. In four rounds, cheapest first, so that a weekly run is mostly cache hits:

  1. Listings (`/api/models?...`, about 35 pages of 1,000). Every repo of every trusted quantiser, the top
     of each relevant pipeline by downloads, likes and trending, and the top GGUF/MLX/AWQ/GPTQ repos
     Hub-wide (which is where official quants like `Qwen/Qwen3-8B-GGUF` turn up). Lean: no `config` and
     no `gguf` expansion, because those carry every chat template and make a page 10.8 MB instead of
     1.5 MB (measured 2026-11-18). Cached for 20 hours.
  2. The base models the quant repos name that no listing returned, by `/api/models/{id}`. Then
     `models.select()` decides which models are kept and which variants attach to each.
  3. For each kept model: its full info (config and chat-template signals), keyed on the repo `sha`
     the listing reported, and its `config.json` from the resolver -- or, when the repo is gated and no
     token can read it, the same file from an ungated mirror or variant, or the header of a GGUF.
  4. For each kept model and variant: the file tree, keyed on `sha`. This is the expensive round on a
     cold cache (7,593 trees of a 9,800-call cold build, about 100 minutes at the anonymous rate,
     measured 2026-11-18) and nearly free on a warm one, because a quant repo's sha almost never moves
     after upload.

Then Ollama: its library page for the names and size tags, and for each matched tag the registry
manifest, whose model layer size is checked against the GGUFs this index already has. See
`models.match_ollama()` and `verify_ollama()`.

THE GUARD. A run that would publish fewer than 70% of the models the committed file has refuses to
write, because that is an API change or an outage, not a week in which a third of open models vanished.
`--force` overrides it, for a deliberate change to the rules.

The rules themselves -- what is a variant, what is kept, the schema -- are in `scripts/models.py`; the
consumer contract is `team/contracts/models.md`; the handbook's summary is
`handbook/pipeline.md#the-models-index`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import hf_hub  # noqa: E402
import models as M  # noqa: E402

OUT = ROOT / "docs" / "models.json"
CACHE = ROOT / "cache" / "hf"
CONF = ROOT / "config" / "models.json"
GUARD = 0.70
MISSING_DL = 2_000                 # see find_bases()
HEADER_BYTES = 512 * 1024          # enough for every architecture key; the vocabulary that follows is not needed
DAY = 24 * 3600

LEAN = ["author", "cardData", "createdAt", "downloads", "gated", "lastModified", "library_name", "likes",
        "pipeline_tag", "safetensors", "sha", "tags", "trendingScore"]
FULL = LEAN + ["config", "gguf"]


def expand(fields: list[str]) -> list[tuple[str, str]]:
    return [("expand[]", f) for f in fields]


def plan(conf: dict) -> list[tuple[str, list[tuple[str, str]], int]]:
    """(cache name, query, pages) for every listing. The page counts are the budget: two pages of
    bartowski is his 2,000 most downloaded repos, which reaches well past anything still in use."""
    out = []
    pages = {"bartowski": 2, "unsloth": 2, "mlx-community": 3}
    for q in conf["quantisers"]:
        out.append((f"by-{q}", [("author", q), ("sort", "downloads"), ("limit", "1000")], pages.get(q, 1)))
        out.append((f"by-{q}-trending", [("author", q), ("sort", "trendingScore"), ("limit", "300")], 1))
    for f in ("gguf", "mlx", "awq", "gptq"):
        out.append((f"fmt-{f}", [("filter", f), ("sort", "downloads"), ("limit", "1000")], 2 if f == "gguf" else 1))
    out.append(("fmt-gguf-trending", [("filter", "gguf"), ("sort", "trendingScore"), ("limit", "500")], 1))
    for pipe, n in (("text-generation", 3), ("image-text-to-text", 1), ("feature-extraction", 1),
                    ("sentence-similarity", 1), ("text-ranking", 1), ("automatic-speech-recognition", 1),
                    ("text-to-speech", 1), ("any-to-any", 1), ("audio-text-to-text", 1)):
        out.append((f"pipe-{pipe}", [("pipeline_tag", pipe), ("sort", "downloads"), ("limit", "1000")], n))
        out.append((f"pipe-{pipe}-trending", [("pipeline_tag", pipe), ("sort", "trendingScore"), ("limit", "300")], 1))
        out.append((f"pipe-{pipe}-likes", [("pipeline_tag", pipe), ("sort", "likes"), ("limit", "500")], 1))
    return out


def gather(hub: hf_hub.Hub, conf: dict, log=print) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for name, query, pages in plan(conf):
        got = hub.list_models(name, query + expand(LEAN), pages=pages, reduce=M.reduce_entry)
        for e in got:
            entries.setdefault(e["id"], e)
        log(f"  listing {name}: {len(got)} repos ({len(entries)} distinct so far)")
    return entries


def info(hub: hf_hub.Hub, rid: str, key: str | None) -> dict | None:
    """A repo's full info, reduced. Keyed on its sha when the listing gave one, else a week old at most."""
    url = f"{hf_hub.HUB}/api/models/{rid}?" + "&".join(f"expand[]={f}" for f in FULL)
    status, body = hub.get("info", rid, url, key=key, max_age=None if key else 6 * DAY)
    return M.reduce_entry(body) if status == 200 and isinstance(body, dict) and body.get("id") else None


def find_bases(hub, entries, conf, snapshot, log=print) -> dict:
    """Rounds of `select()` and fetching the base models it says are missing, until none are."""
    tried: set[str] = set()
    labs = set(conf.get("labs", []))
    for rnd in range(5):
        sel = M.select(entries, conf, snapshot)
        # A base whose trusted quants together see fewer than MISSING_DL downloads a month is not worth
        # a call unless a lab made it: it would fail `keep()` on its variants' evidence anyway.
        todo = sorted(b for b, dl in sel["missing"].items()
                      if b not in tried and (dl >= MISSING_DL or b.split("/")[0] in labs))
        if not todo:
            return sel
        log(f"  round {rnd + 1}: fetching {len(todo)} base model(s) no listing returned "
            f"(skipping {len(sel['missing']) - len(todo)} nobody downloads a quant of)")
        for rid in todo:
            tried.add(rid)
            e = info(hub, rid, None)
            if e:
                entries[e["id"]] = e
                if e["id"] != rid:   # the card spelled it differently; let the walk find either
                    entries.setdefault(rid, e)
    return M.select(entries, conf, snapshot)


def config_for(hub, mid: str, e: dict, trees: dict, sel: dict, entries: dict) -> tuple[dict | None, dict | None]:
    """(config.json, GGUF header) for a model. The header is read only when no config could be."""
    def cfg(rid, sha):
        t = trees.get(rid) or []
        if not any(p == "config.json" for p, _ in t):
            return None
        status, body = hub.get("config", rid, f"{hf_hub.HUB}/{rid}/resolve/main/config.json", key=sha,
                               bucket="resolvers")
        return body if status == 200 and isinstance(body, dict) else None

    if not e["gated"] or hub.token:
        c = cfg(mid, e["sha"])
        if c:
            return c, None
    # A gated original: the same config from a mirror or a re-packaging that ships it.
    alts = [m for m in sel["mirrors"] if mid in entries[m]["card"]["base_model"]]
    alts += [v for v in sel["models"][mid] if sel["variants"][v] != "gguf"]
    for rid in alts:
        if rid not in trees:
            trees[rid] = hub.tree(rid, entries[rid]["sha"])
        c = cfg(rid, entries[rid]["sha"])
        if c:
            return c, None
    for v in sel["models"][mid]:
        if sel["variants"][v] != "gguf" or not trees.get(v):
            continue
        ggufs = sorted((s, p) for p, s in trees[v] if p.lower().endswith(".gguf") and "mmproj" not in p.lower())
        if ggufs:
            raw = hub.head_bytes(v, ggufs[0][1], HEADER_BYTES, entries[v]["sha"])
            if raw:
                try:
                    return None, hf_hub.parse_gguf_header(raw)
                except ValueError:
                    pass
    return None, None


def ollama_rows(hub, rows: list[list], conf: dict, log=print) -> dict[str, dict]:
    """{model id: ollama object} for the rows that have an Ollama library tag. An unreadable library page
    is a warning and no Ollama data, never a failed build: Ollama is a convenience column."""
    try:
        status, html = hub.get("ollama", "library", "https://ollama.com/library", max_age=6 * DAY,
                               bucket="other", parse="text")
    except (hf_hub.HubError, hf_hub.Offline) as e:
        log(f"  ollama: library unreachable ({e}); no Ollama column this run")
        return {}
    lib = M.parse_ollama_library(html or "") if status == 200 else {}
    if len(lib) < 50:
        log(f"  ollama: the library page parsed to {len(lib)} models; treating that as a changed page, not data")
        return {}
    ci = {c: i for i, c in enumerate(M.COLS)}
    shallow = [{"id": r[0], "name": r[1], "uses": r[ci["uses"]], "downloads_all": r[ci["downloads_all"]]} for r in rows]
    matched = M.match_ollama(shallow, lib, conf.get("ollama", {}))
    by_id = {r[0]: r for r in rows}
    out = {}
    for mid, (name, tag, how) in sorted(matched.items()):
        url = f"https://registry.ollama.ai/v2/library/{name}/manifests/{tag}"
        try:
            status, man = hub.get("ollama", f"manifest-{name}-{tag}", url, max_age=6 * DAY, bucket="other",
                                  headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})
        except (hf_hub.HubError, hf_hub.Offline):
            continue
        if status != 200 or not isinstance(man, dict):
            continue
        layer = next((l for l in man.get("layers", []) if l.get("mediaType") == "application/vnd.ollama.image.model"), None)
        if not layer:
            continue
        q = None
        cdig = (man.get("config") or {}).get("digest")
        if cdig:
            try:
                s2, cfg = hub.get("ollama", f"blob-{cdig}", f"https://registry.ollama.ai/v2/library/{name}/blobs/{cdig}",
                                  key=cdig, bucket="other")
                q = (cfg or {}).get("file_type") if s2 == 200 and isinstance(cfg, dict) else None
            except (hf_hub.HubError, hf_hub.Offline):
                pass
        files = [f for v in by_id[mid][-1] if v[1] == "gguf" for f in v[5]]
        ok = M.verify_ollama(files, q, int(layer["size"]))
        out[mid] = {"name": name, "tag": tag, "bytes": int(layer["size"]), "q": q,
                    "match": "verified" if ok else how}
    log(f"  ollama: {len(lib)} library models; {len(out)} matched "
        f"({sum(1 for o in out.values() if o['match'] == 'verified')} size-verified)")
    return out


def build(hub, conf: dict, snapshot: str, generated: str, log=print) -> tuple[dict, dict]:
    entries = gather(hub, conf, log)
    sel = find_bases(hub, entries, conf, snapshot, log)
    log(f"  selected {len(sel['models'])} models from {len(entries)} repos; dropped {sum(sel['dropped'].values())}: "
        + ", ".join(f"{k} {v}" for k, v in sorted(sel["dropped"].items(), key=lambda kv: -kv[1])))

    # Round 3: full info for each kept model, replacing its lean listing entry.
    for i, mid in enumerate(sorted(sel["models"])):
        try:
            full = info(hub, mid, entries[mid]["sha"])
        except hf_hub.Offline:
            full = None
        if full and full["id"] == mid:   # a repo renamed since its listing keeps the listing's entry this run
            entries[mid] = full
        if (i + 1) % 200 == 0:
            log(f"  info {i + 1}/{len(sel['models'])}  {hub.calls}")

    # Round 4: trees.
    trees: dict[str, list | None] = {}
    want = sorted(set(sel["models"]) | {v for vs in sel["models"].values() for v in vs})
    for i, rid in enumerate(want):
        try:
            trees[rid] = hub.tree(rid, entries[rid]["sha"])
        except hf_hub.Offline:   # --offline and never fetched: no sizes for it this run, said in the count
            trees[rid] = None
        if (i + 1) % 250 == 0:
            log(f"  trees {i + 1}/{len(want)}  {hub.calls}")

    rows, fell = [], 0
    for i, mid in enumerate(sorted(sel["models"])):
        e = entries[mid]
        try:
            config, header = config_for(hub, mid, e, trees, sel, entries)
        except hf_hub.Offline:   # --offline and a fallback nobody has fetched: no dims, not no row
            config, header = None, None
        variants = [(entries[v], sel["variants"][v]) for v in sel["models"][mid]]
        r = M.model_row(e, variants, trees, config, header, None, sel["labs"], snapshot)
        if r is None:
            fell += 1
            continue
        rows.append(r)
        if (i + 1) % 250 == 0:
            log(f"  rows {i + 1}/{len(sel['models'])}  {hub.calls}")
    log(f"  {len(rows)} rows; {fell} fell to the keep rule once their config or files were known")

    ol = ollama_rows(hub, rows, conf, log)
    oi = M.COLS.index("ollama")
    for r in rows:
        r[oi] = ol.get(r[0])
    doc = M.document(rows, snapshot, generated)
    return doc, sel


def compact(doc: dict) -> str:
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":"))


def report(doc: dict) -> str:
    c = doc["counts"]
    ci = {k: i for i, k in enumerate(doc["cols"])}
    rows = doc["models"]
    with_q = sum(1 for r in rows if any(v[1] in ("gguf", "mlx", "awq", "gptq") for v in r[ci["variants"]]))
    with_dims = sum(1 for r in rows if r[ci["dims"]] and r[ci["dims"]].get("layers"))
    with_ctx = sum(1 for r in rows if r[ci["ctx"]])
    with_ol = sum(1 for r in rows if r[ci["ollama"]])
    uses: dict[str, int] = {}
    for r in rows:
        for u in r[ci["uses"]]:
            uses[u] = uses.get(u, 0) + 1
    fmts = ", ".join(f"{k} {v}" for k, v in sorted(c["formats"].items(), key=lambda kv: -kv[1]))
    return "\n".join([
        f"models.json snapshot {doc['snapshot']}: {c['models']} models in {c['families']} families, "
        f"{c['variants']} variants, {c['files']} quantisation files",
        f"  variants by format: {fmts}",
        f"  {with_q} models have a GGUF/MLX/AWQ/GPTQ variant; {with_dims} have layer dims; {with_ctx} a context "
        f"length; {with_ol} an Ollama tag",
        "  uses: " + ", ".join(f"{k} {v}" for k, v in sorted(uses.items(), key=lambda kv: -kv[1])),
    ])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--offline", action="store_true", help="build from cache/hf/ only")
    ap.add_argument("--dry-run", action="store_true", help="build and report, write nothing")
    ap.add_argument("--status", action="store_true", help="report on the committed file and stop")
    ap.add_argument("--force", action="store_true", help="write even if the guard refuses")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)

    if a.status:
        doc = json.loads(OUT.read_text(encoding="utf-8"))
        M.validate(doc)
        print(report(doc) + f"\n  {OUT.stat().st_size:,} bytes")
        return 0

    conf = json.loads(CONF.read_text(encoding="utf-8"))
    now = hf_hub.utcnow()
    hub = hf_hub.Hub(CACHE, offline=a.offline)
    print(f"models index: {'offline, ' if a.offline else ''}{'token' if hub.token else 'anonymous'} reads, cache {CACHE}")
    doc, sel = build(hub, conf, now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    text = compact(doc)
    print(report(doc))
    print(f"  {len(text.encode('utf-8')):,} bytes; hub calls {hub.calls}")

    if a.out.exists():
        try:
            old = json.loads(a.out.read_text(encoding="utf-8")).get("counts", {}).get("models", 0)
        except ValueError:
            old = 0
        if old and doc["counts"]["models"] < GUARD * old and not a.force:
            print(f"REFUSED: {doc['counts']['models']} models against {old} committed -- under {GUARD:.0%}. "
                  "An API change or an outage, not a real week; nothing written. --force overrides.")
            return 1
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("### Models index\n\n```\n" + report(doc) + "\n```\n")
    if a.dry_run:
        print("dry run: nothing written")
        return 0
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(text, encoding="utf-8")
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
