"""Fetch release asset filenames -- the strongest available signal for which
platforms a project actually ships prebuilt binaries for."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import signals as sig  # noqa: E402

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
    # Loaded even under --force, and the force applied to the queue predicate instead of by
    # emptying the dict. This stage only owns the primary list's ~194 repos, while
    # 13_signals_all.py fills the same file for all 1,294 -- so discarding it here would throw
    # away the other 1,100 entries and hand 13_signals_all a full re-crawl it did not ask for.
    rel = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}

    # See scripts/signals.py: presence alone froze these entries for ever, so the queue also
    # asks whether the repo has been pushed since the entry was written, whether we looked so
    # soon after that push that the release CI cannot have finished uploading yet, and how long
    # ago we looked at all. One clock for the whole run, so every entry it writes agrees.
    now = sig.utcnow()
    pushed = {e["nwo"]: sig.meta_push(meta, e["nwo"]) for e in entries}
    why = {e["nwo"]: sig.reason(rel, e["nwo"], pushed[e["nwo"]], now) for e in entries}
    todo = [e for e in entries if force or why[e["nwo"]] != sig.FRESH]
    print(f"{len(todo)} of {len(entries)} repos to check for release assets"
          f"{sig.breakdown([why[e['nwo']] for e in todo])}")

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
            node = (data or {}).get(f"r{i}")
            # A null node means the batch errored or GitHub had nothing to say about this repo,
            # so we learned nothing -- leave whatever is cached alone and stay queued for the
            # next run. Writing an empty entry and stamping it would record "we looked at this
            # push and found no assets", which is the frozen false negative this stage is being
            # fixed to stop producing: one transient network error would freeze fifteen repos
            # until their next push.
            if not node:
                continue
            assets, tags = [], []
            for r in ((node.get("releases") or {}).get("nodes") or []):
                tags.append(r.get("tagName") or "")
                assets += [a["name"] for a in ((r.get("releaseAssets") or {}).get("nodes") or [])]
            rel[e["nwo"]] = {"tags": tags, "assets": sorted(set(assets)),
                             **sig.observed(pushed[e["nwo"]], now)}
        print(f"  {min(start + BATCH, len(todo))}/{len(todo)}")
        out_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")

    out_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
    with_assets = sum(1 for v in rel.values() if v.get("assets"))
    print(f"\ndone: {len(rel)} repos, {with_assets} publish release assets")


if __name__ == "__main__":
    main()
