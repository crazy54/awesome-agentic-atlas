"""Detect GitHub Actions definitively: an action.yml/action.yaml at the repo root."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 25


def gh(args: list[str]) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(p.stderr[:300])
    return p.stdout


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    entries = [e for e in entries if "error" not in meta.get(e["nwo"], {})]

    out = {}
    for start in range(0, len(entries), BATCH):
        batch = entries[start : start + BATCH]
        parts = [
            f'  r{i}: repository(owner: "{e["owner"]}", name: "{e["repo"]}") {{'
            f' yml: object(expression: "HEAD:action.yml") {{ __typename }}'
            f' yaml: object(expression: "HEAD:action.yaml") {{ __typename }} }}'
            for i, e in enumerate(batch)
        ]
        try:
            data = json.loads(gh(["api", "graphql", "-f", "query=query {\n" + "\n".join(parts) + "\n}"])).get("data") or {}
        except RuntimeError as exc:
            print(f"  batch {start} failed: {exc}")
            data = {}
        for i, e in enumerate(batch):
            n = (data or {}).get(f"r{i}") or {}
            out[e["nwo"]] = bool(n.get("yml") or n.get("yaml"))
        print(f"  {min(start + BATCH, len(entries))}/{len(entries)}")

    (CACHE / "actions.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    hits = sorted(k for k, v in out.items() if v)
    print(f"\n{len(hits)} repos ship an action.yml:")
    for h in hits:
        print(f"  {h}")


if __name__ == "__main__":
    main()
