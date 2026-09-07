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

Two further terms sit under that rule, and both exist because the stamp above
is the *push* time rather than the time we looked. An entry records what it
saw and never when it saw it, so nothing in it can tell "queried a second
after the push" from "queried a week after", and those two are worth very
different amounts. `fetched_at` records the second fact.

The first term is the CI upload race, which is the blind spot above reached
through the ordinary release flow instead of by hand. Tagging v1.0 moves
`pushedAt` at once; the release workflow then spends minutes building and
attaching the binaries. A run that lands in that gap sees the new push time
and an empty asset list, the assets arrive afterwards with no push behind
them, and `recorded_push == meta_push` holds from then on -- so the project is
published as shipping no binaries until its next release, which for a finished
or archived project is never. An entry fetched within `CI_GRACE_HOURS` of the
push it recorded is therefore re-queried once. That is the term that closes
the hole rather than merely bounding it.

The second is a ceiling: an entry whose `fetched_at` is older than
`MAX_AGE_DAYS` is re-queried whatever else holds.

What all this costs, recorded here because this is where the batch sizes are.
GitHub scores a GraphQL call by counting the requests needed to fulfil each
*connection* in it -- not the nodes it returns -- then dividing by 100, with a
minimum of one point. These queries ask for two connections per repo:
`releases(last: 4)`, which is one, and a `releaseAssets(first: 40)` under each
of those four releases, which is four. So a repo costs 5, a 12-repo batch costs
60, and 60/100 with a floor of 1 means every batch any of these three stages
issues costs exactly one point. A full 1,294-repo crawl is 108 requests and
108 points; the ~319 repos pushed on an average day are 27 requests; the two
terms above add about 99 repos a day, which is 8 requests more. Against the
1,000 points an hour a `GITHUB_TOKEN` gets, none of that is near a constraint,
which is why these figures are written down rather than optimised.

Untested, and cheap to settle: no run has yet read a `rateLimit { cost }` back
out of GitHub. Adding that field to any one of the three queries and printing
it would turn the paragraph above into an observation.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

# The key each cache entry records its observed push time under. Deliberately
# not `pushedAt`: that is GraphQL's spelling for the live value in meta.json,
# and these two are different facts -- one is now, one is when we last looked.
STAMP = "pushed_at"

# ...and the key it records when we looked under. Two fields rather than one
# because they answer different questions: `pushed_at` says what state the
# answer describes, `fetched_at` says how much to trust it. A single field
# cannot do both, which is why the two terms below were unreachable before it
# existed. Adding a key keeps the migration free -- `cache/` is gitignored and
# rebuilt from the Actions cache, every reader below tolerates the key being
# absent, and an entry that lacks it reads as stale, so the atlas backfills
# itself over one crawl instead of needing a conversion step.
FETCHED = "fetched_at"

# A ceiling on how long a wrong answer can persist -- not a refresh interval.
# Every other term keys off a signal that tells us something changed; this one
# fires when those signals are wrong, and its whole job is to turn "wrong for
# ever" into "wrong for a bounded while". Nothing should be tuned by it:
# lowering it does not make the data fresher, because the push term already
# refreshes everything that moved. At the atlas's current size the 564 repos
# with no push in the last month amortise to about 19 repos a day, which is
# under two extra requests.
MAX_AGE_DAYS = 30

# How long after a push a release answer is not yet trusted. A tag push moves
# `pushedAt` immediately and the job that attaches the binaries finishes later,
# so an entry written inside that window can have seen the push and none of its
# assets. Six hours is measured against release CI rather than against our own
# schedule: cross-compiling matrix builds that upload artifacts land in single
# digit hours, and a daily pipeline gets exactly one attempt at the gap, so the
# window has to cover the slow end rather than the median. It re-queries one
# repo for every repo pushed in the six hours before a run -- roughly 319 *
# 6/24, about 80 a day here, or seven extra requests -- and each of those is
# one-shot: the re-query's own `fetched_at` lands outside the window, so the
# entry is fresh from then on and the term cannot queue the same repo twice.
CI_GRACE_HOURS = 6

# `reason`'s vocabulary. Codes rather than bare booleans so a stage can print
# which term queued each repo; a term that has silently stopped firing, or one
# that fires for the whole atlas, shows up in the run log as a count.
ABSENT = "absent"
UNSTAMPED = "unstamped"
PUSHED = "pushed"
UNFETCHED = "unfetched"
CI_RACE = "ci-race"
BACKSTOP = "backstop"
FRESH = "fresh"


def utcnow() -> datetime:
    """The clock, as an aware UTC datetime.

    Read once per stage and passed down, so that every entry a run writes
    carries the same timestamp and every staleness test in that run is decided
    against the same instant. A crawl that takes twenty minutes should not have
    its first and last repos judged by different clocks.
    """
    return datetime.now(timezone.utc)


def stamp(when: datetime) -> str:
    """`when` in the spelling GitHub uses, so both stamps in an entry match."""
    return when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_stamp(value: object) -> datetime | None:
    """`value` as an aware UTC datetime, or None if it is not a timestamp.

    Accepts every spelling that reaches these caches: GraphQL's trailing `Z`,
    an explicit offset, fractional seconds, and a naive value, which is read as
    UTC because that is what every producer here means. None for anything else
    -- absent, null, a number, a hand-edited mess.

    None is a verdict, not an error. A single malformed entry re-queries one
    repo; an exception here would stop a crawl of 1,294.
    """
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text[-1] in "Zz":
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


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


def recorded_fetch(entry: object) -> str | None:
    """When `entry` was written, or None if it does not say.

    None for the two shapes `recorded_push` handles and for the one shipped
    between them: an entry carrying a push stamp but no fetch stamp. All three
    mean the same thing here -- we cannot tell how soon after that push we
    looked -- and all three route to a re-query.
    """
    if isinstance(entry, dict) and FETCHED in entry:
        seen = entry[FETCHED]
        return seen if isinstance(seen, str) else None
    return None


def _raced_ci(entry: object, seen: str, fetched: datetime) -> bool:
    """Was `entry` written too soon after the push it recorded to be believed?

    Release entries only, detected by the presence of `assets` rather than by
    which stage is calling, because two stages write that file and the caller is
    not the fact that matters. An `action.yml` cannot appear or disappear
    without a push, so an actions entry is complete the instant it is written
    and a grace window on it would be pure cost.

    A gap of zero counts: a run can land in the same second as the push. A
    negative gap does not -- an entry stamped as fetched before the push it
    records is a clock or a hand edit, not a race, and the backstop covers it.
    """
    if not isinstance(entry, dict) or "assets" not in entry:
        return False
    pushed_at = parse_stamp(seen)
    if pushed_at is None:
        return False  # nothing to measure from; the push term owns this entry
    return timedelta(0) <= fetched - pushed_at < timedelta(hours=CI_GRACE_HOURS)


def reason(cache: dict, nwo: str, pushed: str, now: datetime | None = None) -> str:
    """Why `nwo` needs re-querying this run, or `FRESH` if it does not.

    Order matters twice over. The push term is asked before either time term so
    that the common answer costs no date parsing and so a moved push is always
    reported as a moved push rather than as whatever else also happened to
    hold. The fetch-stamp check sits after it, so an entry from the shipped
    push-only schema is refreshed once by whichever term fires first and is
    fully stamped afterwards.
    """
    if nwo not in cache:
        return ABSENT
    entry = cache[nwo]
    seen = recorded_push(entry)
    if seen is None:
        return UNSTAMPED  # written under the old schema; refresh once, then stamped
    if seen != pushed:
        return PUSHED
    fetched = parse_stamp(recorded_fetch(entry))
    if fetched is None:
        return UNFETCHED
    if _raced_ci(entry, seen, fetched):
        return CI_RACE
    if (now or utcnow()) - fetched > timedelta(days=MAX_AGE_DAYS):
        return BACKSTOP
    return FRESH


def stale(cache: dict, nwo: str, pushed: str, now: datetime | None = None) -> bool:
    """Should `nwo` be re-queried this run? `pushed` is `meta_push`'s answer.

    Inequality rather than "newer than", because a force-push that rewrote
    history moves `pushedAt` backwards and the signals can have changed just
    as much.
    """
    return reason(cache, nwo, pushed, now) != FRESH


def breakdown(reasons: list[str]) -> str:
    """The queue's reasons as a log fragment, in a fixed order.

    Fixed order and shared by all three stages so two runs' log lines can be
    read against each other. It is the only way a term is falsifiable in
    production: `ci-race 0` every day for a week says the window is doing
    nothing, and `backstop 1200` says something upstream stopped stamping.
    """
    tally: dict[str, int] = {}
    for code in reasons:
        if code != FRESH:
            tally[code] = tally.get(code, 0) + 1
    order = [ABSENT, UNSTAMPED, PUSHED, UNFETCHED, CI_RACE, BACKSTOP]
    parts = [f"{code} {tally[code]}" for code in order if code in tally]
    parts += [f"{code} {n}" for code, n in sorted(tally.items()) if code not in order]
    return f" ({', '.join(parts)})" if parts else ""


def observed(pushed: str, now: datetime | None = None) -> dict:
    """The stamps every cache entry carries, ready to splat into the value.

    One helper for both so a write site cannot record one and forget the other:
    an entry with a push stamp and no fetch stamp reads as stale on every run
    for ever, which is a cheap mistake to make and an expensive one to keep.
    """
    return {STAMP: pushed, FETCHED: stamp(now or utcnow())}


def action_entry(has_action_yml: bool, pushed: str, now: datetime | None = None) -> dict:
    """An `actions.json` value under the current schema."""
    return {"is_action": bool(has_action_yml), **observed(pushed, now)}


def is_action(entry: object) -> bool:
    """Read an `actions.json` value under either schema.

    Needed because the plain `bool(entry)` the readers used to do is wrong the
    moment entries are dicts: every dict is truthy, so an unmigrated atlas
    would have reported every repo as a GitHub Action.
    """
    if isinstance(entry, dict):
        return bool(entry.get("is_action"))
    return bool(entry)
