"""Release assets and action.yml presence for every repo, in one pass.

03_releases.py and 03b_actions.py each walk the whole repo set; at the 7,870
repos the source lists now resolve to that is two full sets of round trips for
data that fits in one query, and the saving grew with every list ingested --
it was 1,153 repos when this stage was written to replace them. Same output
files, so 04_classify.py reads them unchanged.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 12

# Borrowed the way 11_fetch_all.py borrows it, and for the same reason: 02_fetch.py holds the only
# copy of what a non-zero exit from `gh api graphql` actually means. It is the one place that knows a
# NOT_FOUND for a single alias still leaves eleven good repos on stdout, and equally the one place
# that knows Bad credentials must not be mistaken for that. A second opinion kept here would drift.
spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

FIELDS = """
    releases(last: 4) { nodes { tagName releaseAssets(first: 40) { nodes { name } } } }
    yml: object(expression: "HEAD:action.yml") { __typename }
    yaml: object(expression: "HEAD:action.yaml") { __typename }
"""


def main() -> None:
    rows = json.loads((CACHE / "entries_all.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))

    repos: list[dict] = []
    seen: set[str] = set()
    for r in rows:
        nwo = r.get("nwo") or ""
        if not nwo or nwo.lower() in seen or "error" in meta.get(nwo, {"error": 1}):
            continue
        seen.add(nwo.lower())
        repos.append({"nwo": nwo, "owner": r["owner"], "repo": r["repo"]})

    rel_path, act_path = CACHE / "releases.json", CACHE / "actions.json"
    force = "--force" in sys.argv
    rel = {} if force else json.loads(rel_path.read_text(encoding="utf-8")) if rel_path.exists() else {}
    act = {} if force else json.loads(act_path.read_text(encoding="utf-8")) if act_path.exists() else {}

    todo = [r for r in repos if r["nwo"] not in rel or r["nwo"] not in act]
    print(f"{len(repos)} repos with metadata, {len(todo)} needing signals", flush=True)

    failed = 0
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        try:
            data = f2.graphql_batch(batch, FIELDS)
        except RuntimeError as exc:
            # Nothing is written for a batch that failed, and that is the whole repair. This stage used
            # to answer a failed query with `{"tags": [], "assets": []}` and `False` for all twelve
            # repos, which is byte-for-byte what a project that has genuinely never cut a release looks
            # like -- so 04_classify would read twelve projects as shipping no prebuilt binaries and
            # nothing anywhere would ever say otherwise. Leaving the keys absent instead is what puts
            # those repos back in `todo` on the next run, so the retry costs one batch and not a
            # rebuild. Note that absent and empty are the same to 04_classify, which reads these with
            # `.get(nwo, {})` -- the difference this makes is entirely in what gets re-queried and in
            # the exit code below, not in how a record already on disk is interpreted.
            failed += 1
            print(f"  batch {start} failed, left for the next run: {str(exc)[:120]}", flush=True)
            continue
        for i, e in enumerate(batch):
            n = data.get(f"r{i}")
            if n is None:
                # GitHub answered, and its answer is that this repo no longer exists. The meta.json
                # error filter above normally keeps those out entirely, so an alias coming back null
                # means the repo died in the minutes between 11_fetch_all.py and here. Skipping costs
                # one slot in the next run's batches, by which time meta.json carries its error record
                # and it drops out of `repos` for good.
                continue
            assets, tags = [], []
            for node in ((n.get("releases") or {}).get("nodes") or []):
                tags.append(node.get("tagName") or "")
                assets += [a.get("name") or "" for a in
                           ((node.get("releaseAssets") or {}).get("nodes") or [])]
            rel[e["nwo"]] = {"tags": tags, "assets": assets}
            act[e["nwo"]] = bool(n.get("yml") or n.get("yaml"))

        done = min(start + BATCH, len(todo))
        if start % (BATCH * 8) == 0 or done == len(todo):
            rel_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
            act_path.write_text(json.dumps(act, indent=1), encoding="utf-8")
            print(f"  {done}/{len(todo)}", flush=True)

    rel_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
    act_path.write_text(json.dumps(act, indent=1), encoding="utf-8")
    with_assets = sum(1 for v in rel.values() if v.get("assets"))
    print(f"\ndone: {len(rel)} repos, {with_assets} publish release assets, "
          f"{sum(1 for v in act.values() if v)} are GitHub Actions", flush=True)

    # Every batch that did come back is already on disk above, so the next run picks up precisely the
    # repos this one missed and nothing else. The non-zero exit is not about this stage, it is about the
    # four after it: 04_classify turns these two files into the per-platform verdicts the site and both
    # workbooks publish, and a run that quietly lost the signals for part of the atlas would demote
    # those projects on a page that looks freshly built. Better the build stops and the lists get
    # re-read tomorrow -- nothing is committed and nothing is recorded as built until every stage
    # passes, which is what makes stopping here safe rather than lossy.
    if failed:
        print(f"\n{failed} batch(es) of {BATCH} failed and wrote nothing; up to {failed * BATCH} "
              f"repos still need signals and will be retried on the next run.", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
