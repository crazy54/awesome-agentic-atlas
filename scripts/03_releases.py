"""Fetch release asset filenames -- the strongest available signal for which
platforms a project actually ships prebuilt binaries for."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 15

FIELDS = """
    releases(last: 4) {
      nodes {
        tagName
        releaseAssets(first: 40) { nodes { name } }
      }
    }
"""


def gh(args: list[str]) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"gh failed: {p.stderr[:400]}")
    return p.stdout


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    entries = [e for e in entries if "error" not in meta.get(e["nwo"], {})]

    out_path = CACHE / "releases.json"
    force = "--force" in sys.argv
    rel = {} if force else json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    todo = [e for e in entries if e["nwo"] not in rel]
    print(f"{len(todo)} repos to check for release assets")

    for start in range(0, len(todo), BATCH):
        batch = todo[start : start + BATCH]
        parts = [
            f'  r{i}: repository(owner: "{e["owner"]}", name: "{e["repo"]}") {{{FIELDS}}}'
            for i, e in enumerate(batch)
        ]
        query = "query {\n" + "\n".join(parts) + "\n}"
        try:
            data = json.loads(gh(["api", "graphql", "-f", f"query={query}"])).get("data") or {}
        except RuntimeError as exc:
            print(f"  batch {start} failed: {exc}")
            data = {}
        for i, e in enumerate(batch):
            node = (data or {}).get(f"r{i}") or {}
            assets, tags = [], []
            for r in ((node.get("releases") or {}).get("nodes") or []):
                tags.append(r.get("tagName") or "")
                assets += [a["name"] for a in ((r.get("releaseAssets") or {}).get("nodes") or [])]
            rel[e["nwo"]] = {"tags": tags, "assets": sorted(set(assets))}
        print(f"  {min(start + BATCH, len(todo))}/{len(todo)}")
        out_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")

    out_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
    with_assets = sum(1 for v in rel.values() if v["assets"])
    print(f"\ndone: {len(rel)} repos, {with_assets} publish release assets")


if __name__ == "__main__":
    main()
