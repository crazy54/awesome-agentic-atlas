"""Detect GitHub Actions definitively: an action.yml/action.yaml at the repo root.

Incremental, on the rule in scripts/signals.py: an `action.yml` can only appear or
disappear through a push, so a repo whose `pushedAt` has not moved since its cached
entry was written cannot have changed its answer. That makes push-gating this stage
exactly right rather than merely cheap -- unlike release assets, there is no way to
gain one without a push, so this file has no blind spot.

It also stops the write being destructive. This stage used to rebuild `actions.json`
from scratch over the primary list's ~194 repos, which deleted the ~7,700 entries
13_signals_all.py had written for the other thirty-eight of the 39 source lists -- so
every daily run threw away most of the file and 13_signals_all re-crawled it, which
was the bulk of the pipeline's daily GraphQL spend.
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import signals as sig  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 25

# See 13_signals_all.py: 02_fetch.py owns the single answer to what a non-zero exit from
# `gh api graphql` means, and a batched query that does not go through it will sooner or later throw
# away twenty-four good repos because the twenty-fifth was deleted.
spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

FIELDS = """
    yml: object(expression: "HEAD:action.yml") { __typename }
    yaml: object(expression: "HEAD:action.yaml") { __typename }
"""


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    entries = [e for e in entries if "error" not in meta.get(e["nwo"], {})]

    out_path = CACHE / "actions.json"
    force = "--force" in sys.argv
    out = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}

    now = sig.utcnow()
    pushed = {e["nwo"]: sig.meta_push(meta, e["nwo"]) for e in entries}
    # The CI-race term in signals.py deliberately does not apply to this file -- see `_raced_ci`
    # and the docstring above -- so the only terms that can queue a repo here are a moved push, a
    # legacy entry, and the age ceiling.
    why = {e["nwo"]: sig.reason(out, e["nwo"], pushed[e["nwo"]], now) for e in entries}
    todo = [e for e in entries if force or why[e["nwo"]] != sig.FRESH]
    print(f"{len(todo)} of {len(entries)} repos to check for an action.yml"
          f"{sig.breakdown([why[e['nwo']] for e in todo])}")

    failed = 0
    for start in range(0, len(todo), BATCH):
        batch = todo[start : start + BATCH]
        try:
            data = f2.graphql_batch(batch, FIELDS)
        except RuntimeError as exc:
            # `False` for a repo we never got an answer about reads exactly like a repo that has no
            # action.yml, so a failed batch records nothing and the run is written off below. Since
            # this stage merges into the file it reads rather than rebuilding it, "records nothing"
            # now leaves the previous answer and its old stamp in place, which scripts/signals.py
            # reads as stale against the push we can already see -- so these repos come back in
            # `todo` next run, exactly as 03_releases.py's and 13_signals_all.py's do.
            failed += 1
            print(f"  batch {start} failed, left for the next run: {str(exc)[:120]}")
            continue
        for i, e in enumerate(batch):
            n = data.get(f"r{i}")
            # See 03_releases.py: a null node is GitHub answering NOT_FOUND for this one alias --
            # deleted, renamed or gone private since 02_fetch ran -- which taught us nothing about
            # its action.yml. Keep whatever is cached and stay queued rather than stamping a guess
            # as though it were an observation; next run's meta.json filters the repo out for good.
            if not n:
                continue
            out[e["nwo"]] = sig.action_entry(bool(n.get("yml") or n.get("yaml")),
                                             pushed[e["nwo"]], now)
        print(f"  {min(start + BATCH, len(todo))}/{len(todo)}")
        out_path.write_text(json.dumps(out, indent=1), encoding="utf-8")

    out_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    # Counted over the whole file, which now spans every list rather than just this stage's, and
    # named only for the repos this run actually looked at -- listing all of them would be a
    # hundred lines of log saying nothing changed.
    hits = sorted(e["nwo"] for e in todo if sig.is_action(out.get(e["nwo"])))
    print(f"\n{sum(1 for v in out.values() if sig.is_action(v))} of {len(out)} cached repos "
          f"ship an action.yml; {len(hits)} of them among the {len(todo)} checked here:")
    for h in hits:
        print(f"  {h}")

    if failed:
        # The write above is no longer all-or-nothing, so this is not about actions.json being short:
        # every batch that came back is on disk and the ones that did not are queued for next run.
        # It is about 04_classify, which reads this file to decide whether a project is a GitHub
        # Action, and must not publish a gap as a verdict on a page that looks freshly built.
        print(f"\n{failed} batch(es) of {BATCH} failed and wrote nothing; up to {failed * BATCH} "
              f"repos still need an action.yml answer and will be retried on the next run.")
        sys.exit(1)


if __name__ == "__main__":
    main()
