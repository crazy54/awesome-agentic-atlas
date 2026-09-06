"""When a repo's release-asset and `action.yml` signals need re-querying.

`cache/releases.json` and `cache/actions.json` were the only two caches in the
pipeline whose entries were written once and then never revisited. All three
stages that fill them queued on presence alone -- `nwo not in rel` -- so an
entry became permanent the moment it was first written, and the two verdicts
derived from it (which platforms a project ships binaries for, and whether it
is a GitHub Action) were frozen at whenever that happened, on a page whose
snapshot date advanced every morning. `02_fetch.py` is called with `--force`
precisely so stars and last-push cannot go stale that way; the same reasoning
was never applied to the signals.

The refresh term lives here rather than in each stage so that all three share
one rule, because three copies of a staleness test is how one of them ends up
without it.

The rule is the one signal that already arrives free. `02_fetch.py --force`
empties `cache/meta.json` and both it and `11_fetch_all.py` refill it on every
run, so every stage below already knows each repo's current `pushedAt`. A repo
that has not been pushed since we last looked cannot have grown an
`action.yml` -- that file arrives only by a push -- and cannot have cut a
release through CI, because the tag push comes first. So a repo whose last
push has not moved is not worth a query, and a repo whose push has moved is
exactly the one that is. That makes the daily cost proportional to the day's
activity rather than to the size of the atlas: about 300 of 1,294 repos are
pushed on a given day.

The push time we saw is recorded inside each cache entry, which means entries
written before this module existed carry no stamp. Those are treated as stale
on first encounter, so the whole atlas migrates once, lazily, and is stamped
from then on -- no rebuild step, and nothing to remember to run. `actions.json`
entries used to be bare booleans, which is the second legacy shape
`recorded_push` has to recognise and `is_action` has to keep reading.

The blind spot, and the reason `--force` is still worth keeping on all three
stages: a maintainer who attaches a binary to an *existing* release without
pushing anything moves no `pushedAt`, so that asset goes unnoticed. It heals
on that project's next release -- both queries ask for `releases(last: 4)`, so
the re-query a later push triggers sees the assets that were missed -- and
persists only for a project whose final release gained its assets after we
last looked and which never pushed again.
"""
from __future__ import annotations

# The key each cache entry records its observed push time under. Deliberately
# not `pushedAt`: that is GraphQL's spelling for the live value in meta.json,
# and these two are different facts -- one is now, one is when we last looked.
STAMP = "pushed_at"


def meta_push(meta: dict, nwo: str) -> str:
    """`nwo`'s current last-push time, as this run's `meta.json` reports it.

    Full ISO timestamp rather than the `[:10]` date the classifiers publish: a
    project that pushes twice in a day should be re-queried twice if the
    pipeline happens to run twice. Empty for a repo whose metadata never
    carried one, which compares equal to an entry stamped the same way and so
    does not churn.
    """
    return (meta.get(nwo) or {}).get("pushedAt") or ""


def recorded_push(entry: object) -> str | None:
    """The push time recorded when `entry` was written, or None if it predates
    the stamp -- a `releases.json` dict without the key, or the bare boolean an
    `actions.json` entry used to be. None means "we do not know what this was
    a snapshot of", which is a reason to look again, not a reason to skip.
    """
    if isinstance(entry, dict) and STAMP in entry:
        seen = entry[STAMP]
        return seen if isinstance(seen, str) else None
    return None


def stale(cache: dict, nwo: str, pushed: str) -> bool:
    """Should `nwo` be re-queried this run? `pushed` is `meta_push`'s answer.

    Inequality rather than "newer than", because a force-push that rewrote
    history moves `pushedAt` backwards and the signals can have changed just
    as much.
    """
    if nwo not in cache:
        return True
    seen = recorded_push(cache[nwo])
    if seen is None:
        return True  # written under the old schema; refresh once, then stamped
    return seen != pushed


def action_entry(has_action_yml: bool, pushed: str) -> dict:
    """An `actions.json` value under the current schema."""
    return {"is_action": bool(has_action_yml), STAMP: pushed}


def is_action(entry: object) -> bool:
    """Read an `actions.json` value under either schema.

    Needed because the plain `bool(entry)` the readers used to do is wrong the
    moment entries are dicts: every dict is truthy, so an unmigrated atlas
    would have reported every repo as a GitHub Action.
    """
    if isinstance(entry, dict):
        return bool(entry.get("is_action"))
    return bool(entry)
