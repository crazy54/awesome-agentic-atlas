"""Release assets and action.yml presence for every repo, in one pass.

03_releases.py and 03b_actions.py each walk the whole repo set; at the 7,870
repos the source lists now resolve to that is two full sets of round trips for
data that fits in one query, and the saving grew with every list ingested --
it was 1,153 repos when this stage was written to replace them. Same output
files, so 04_classify.py reads them unchanged.

Which repos get queried is scripts/signals.py's rule, shared with those two
stages: anything unseen, anything written before the push stamp existed, and
anything pushed since its entry was written.
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import signals as sig  # noqa: E402

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
    # Loaded even under --force -- the force is applied to the predicate below instead. Emptying
    # the dicts would also silently prune every repo the lists have dropped, which is a different
    # decision wearing the same flag, and it is the reason a --force here used to cost a full
    # re-crawl of both signals for every repo rather than only the ones being refreshed.
    rel = json.loads(rel_path.read_text(encoding="utf-8")) if rel_path.exists() else {}
    act = json.loads(act_path.read_text(encoding="utf-8")) if act_path.exists() else {}

    # `pushedAt` is refetched in full every run (02_fetch.py --force, then 11_fetch_all.py), so
    # this is the current value for every repo and the comparison below is against what we saw
    # when the entry was written. Both signals are fetched by one query, so either one being
    # stale queues the repo and both get rewritten.
    pushed = {r["nwo"]: sig.meta_push(meta, r["nwo"]) for r in repos}
    todo = [r for r in repos
            if force
            or sig.stale(rel, r["nwo"], pushed[r["nwo"]])
            or sig.stale(act, r["nwo"], pushed[r["nwo"]])]
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
            # nothing anywhere would ever say otherwise. Writing nothing instead is what puts those
            # repos back in `todo` on the next run: scripts/signals.py calls an entry stale when it is
            # absent *or* when its recorded push predates the one meta.json can already see, and a
            # batch that wrote nothing leaves every repo in it in one of those two states. So the retry
            # costs one batch and not a rebuild. Note that absent and empty are the same to 04_classify,
            # which reads these with `.get(nwo, {})` -- the difference this makes is entirely in what
            # gets re-queried and in the exit code below, not in how a record already on disk is
            # interpreted.
            failed += 1
            print(f"  batch {start} failed, left for the next run: {str(exc)[:120]}", flush=True)
            continue
        for i, e in enumerate(batch):
            n = data.get(f"r{i}")
            # GitHub answered, and its answer about this one repo is that it no longer exists -- a
            # failed batch cannot land here, because f2.graphql_batch raises and the handler above
            # catches it. The meta.json error filter normally keeps dead repos out entirely, so an
            # alias coming back null means the repo died in the minutes between 11_fetch_all.py and
            # here. Nothing was learned either way, so leave the cache as it is and stay queued:
            # stamping an empty answer would freeze a false negative until that repo's next push.
            # Skipping costs one slot in the next run's batches, by which time meta.json carries its
            # error record and it drops out of `repos` for good.
            if not n:
                continue
            assets, tags = [], []
            for node in ((n.get("releases") or {}).get("nodes") or []):
                tags.append(node.get("tagName") or "")
                assets += [a.get("name") or "" for a in
                           ((node.get("releaseAssets") or {}).get("nodes") or [])]
            rel[e["nwo"]] = {"tags": tags, "assets": assets, sig.STAMP: pushed[e["nwo"]]}
            act[e["nwo"]] = sig.action_entry(bool(n.get("yml") or n.get("yaml")),
                                             pushed[e["nwo"]])

        done = min(start + BATCH, len(todo))
        if start % (BATCH * 8) == 0 or done == len(todo):
            rel_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
            act_path.write_text(json.dumps(act, indent=1), encoding="utf-8")
            print(f"  {done}/{len(todo)}", flush=True)

    rel_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
    act_path.write_text(json.dumps(act, indent=1), encoding="utf-8")
    with_assets = sum(1 for v in rel.values() if v.get("assets"))
    print(f"\ndone: {len(rel)} repos, {with_assets} publish release assets, "
          f"{sum(1 for v in act.values() if sig.is_action(v))} are GitHub Actions", flush=True)

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
