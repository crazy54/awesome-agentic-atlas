"""Fetch metadata + README for every repo across all source lists.

Reuses 02_fetch.py's batching wholesale -- the only new job is collapsing 2,209
listed rows down to the distinct repos behind them, so a project listed by six
lists is still fetched once.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"
READMES.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

BATCH = 20


def main() -> None:
    rows = json.loads((CACHE / "entries_all.json").read_text(encoding="utf-8"))
    meta_path = CACHE / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    # distinct repos, in first-listed order, that we do not already have
    want: list[dict] = []
    seen: set[str] = set()
    for r in rows:
        nwo = r.get("nwo") or ""
        if not nwo or nwo.lower() in seen:
            continue
        seen.add(nwo.lower())
        if nwo in meta:
            continue
        want.append({"nwo": nwo, "owner": r["owner"], "repo": r["repo"]})

    # the source lists themselves get credited on the Sources sheet
    for nwo in sorted({r["source_nwo"] for r in rows}):
        if nwo not in meta and nwo.lower() not in {w["nwo"].lower() for w in want}:
            owner, repo = nwo.split("/", 1)
            want.append({"nwo": nwo, "owner": owner, "repo": repo})

    print(f"{len(seen)} distinct repos referenced, {len(meta)} cached, {len(want)} to fetch",
          flush=True)

    for start in range(0, len(want), BATCH):
        batch = want[start:start + BATCH]
        try:
            data = f2.graphql_batch(batch)
        except RuntimeError as exc:
            print(f"  batch {start}: graphql failed, per-repo fallback ({str(exc)[:90]})", flush=True)
            data = {}
        for i, e in enumerate(batch):
            node = data.get(f"r{i}") if data else None
            readme_text = ""
            if node:
                readme_text = ((node.get("readme") or {}).get("text")) or ""
                record = {k: v for k, v in node.items() if k != "readme"}
                if not readme_text:
                    readme_text = f2.rest_fallback(e["nwo"]).get("readme") or ""
            else:
                fb = f2.rest_fallback(e["nwo"])
                if "error" in fb:
                    meta[e["nwo"]] = {"error": fb["error"], "readme_bytes": 0}
                    continue
                record = fb["meta"]
                readme_text = fb.get("readme") or ""

            record["readme_bytes"] = len(readme_text)
            meta[e["nwo"]] = record
            if readme_text:
                (READMES / f"{e['nwo'].replace('/', '__')}.md").write_text(
                    readme_text[:f2.MAX_README], encoding="utf-8")

        done = min(start + BATCH, len(want))
        if start % (BATCH * 5) == 0 or done == len(want):
            meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"  {done}/{len(want)}", flush=True)

    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    ok = [v for v in meta.values() if "error" not in v]
    print(f"\ndone: {len(meta)} records, {len(ok)} ok, {len(meta) - len(ok)} errors", flush=True)


if __name__ == "__main__":
    main()
