"""Fetch release asset filenames -- the strongest available signal for which
platforms a project actually ships prebuilt binaries for."""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import signals as sig  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 15

# See 13_signals_all.py: 02_fetch.py owns the single answer to what a non-zero exit from
# `gh api graphql` means, and a batched query that does not go through it will sooner or later throw
# away fourteen good repos because the fifteenth was deleted.
spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

FIELDS = """
    releases(last: 4) {
      nodes {
        tagName
        releaseAssets(first: 40) { nodes { name } }
      }
    }
"""


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    entries = [e for e in entries if "error" not in meta.get(e["nwo"], {})]

    out_path = CACHE / "releases.json"
    force = "--force" in sys.argv
    # Loaded even under --force, and the force applied to the queue predicate instead of by
    # emptying the dict. This stage only owns the primary list's ~194 repos, while
    # 13_signals_all.py fills the same file for all 7,870 the source lists resolve to -- so
    # discarding it here would throw away the other ~7,700 entries and hand 13_signals_all a
    # full re-crawl it did not ask for.
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

    failed = 0
    for start in range(0, len(todo), BATCH):
        batch = todo[start : start + BATCH]
        try:
            data = f2.graphql_batch(batch, FIELDS)
        except RuntimeError as exc:
            # Same rule as 13_signals_all.py, which walks the whole atlas the way this walks the
            # curated list: an empty release record is indistinguishable from a project that has never
            # tagged anything, so a batch that failed writes nothing at all -- its repos keep whatever
            # releases.json already held for them, stamp included. That is what brings them back round:
            # `todo` is scripts/signals.py's staleness test, and an entry whose stamp still predates the
            # push we can see is stale again next run, exactly as an absent one is. Either way they are
            # re-queried instead of being written off as binary-less for good.
            failed += 1
            print(f"  batch {start} failed, left for the next run: {str(exc)[:120]}")
            continue
        for i, e in enumerate(batch):
            node = data.get(f"r{i}")
            # A batch that errored never reaches here -- f2.graphql_batch raises and the handler above
            # catches it -- so a null node now means one thing: GitHub answered, and its answer about
            # this one repo is a NOT_FOUND that graphql_batch deliberately rides past. The repo was
            # deleted, renamed or made private since 02_fetch ran, and next run's meta.json carries its
            # error record and filters it out here. Either way we learned nothing about its releases, so
            # leave whatever is cached alone and stay queued: writing an empty entry and stamping it
            # would record "we looked at this push and found no assets", which is the frozen false
            # negative this stage is being fixed to stop producing.
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
    if failed:
        # 04_classify reads this file to decide which platforms a project ships binaries for, so a run
        # that lost part of it must not let the build continue and publish the shortfall as fact.
        print(f"\n{failed} batch(es) of {BATCH} failed and wrote nothing; up to {failed * BATCH} "
              f"repos still need release data and will be retried on the next run.")
        sys.exit(1)


if __name__ == "__main__":
    main()
