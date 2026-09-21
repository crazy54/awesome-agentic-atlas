"""Which fifty projects the atlas puts in front of a reader today, and why those fifty.

The homepage answers "what is the best thing here": sorted by stars, filtered by facet, and a reader
who never scrolls past the first screen sees the same two hundred repositories forever. 8,856 rows, and
the tail of that distribution -- the median row has 21 stars -- is invisible in practice. Discover is the
other question: *show me something I would not have found*. Fifty projects a day, dated, the same fifty
for everybody, rolled over at midnight.

  state/discover.json     committed. When each repo was last featured, and which week is planned.
  docs/discover.json      published. Seven dated cohorts of fifty, read by the page.

WHY A PUBLISHED PLAN RATHER THAN A SHUFFLE IN THE BROWSER
---------------------------------------------------------
The obvious implementation is `rows.sort(() => Math.random() - 0.5).slice(0, 50)` in the page, and it is
wrong in four ways that all have the same cause: a plan nobody can see is a plan nobody can check.

  * A reader who opens Discover twice in an afternoon gets fifty different projects the second time, so
    the one they meant to come back to is gone. Fifty a day is browsable; fifty a refresh is a slot
    machine.
  * Two readers cannot talk about it. "Have you seen what's on Discover today" only means something if
    there is a today.
  * Nothing rotates. A uniform shuffle revisits the popular end as often as the tail, because it has no
    memory; the ledger here is what makes the whole corpus get a turn instead of a random sample of it.
  * It is untestable. A dated list in a file is a fact a harness can assert on -- `discover_test.py`
    asserts the fairness properties below on a synthetic corpus, several weeks deep, with the date
    supplied rather than read from the clock.

THE DAY BOUNDARY IS A NAMED ZONE, NOT THE READER'S CLOCK
--------------------------------------------------------
`TZ` below, and the page is told which zone rather than assuming one. A published cohort is a fact about
a date, so the date has to mean the same thing everywhere: if the rollover were the reader's own
midnight, two people comparing notes at 23:00 UTC would be on different days and both would be right.
The zone is written into `docs/discover.json` and the page resolves it with `Intl.DateTimeFormat`, which
carries a real tz database and therefore handles CST/CDT without this file hardcoding an offset. The
offset is never written down anywhere, because a hardcoded -5 is correct for eight months of the year.

Two copies of "what day is it in Chicago" is one copy too many, so the plan carries a `probe`: a handful
of UTC instants -- including both sides of the two 2026 DST switches -- with the date `zoneinfo` resolved
them to. `tests/probe.mjs` asserts the page's own function reproduces every one. Same trick as the
tokeniser fixtures in `docs/search/meta.json`, for the same reason: the algorithm exists twice, in two
languages, and there is nothing to import.

`cycle` is the same device for the other duplicated function. `for_day()` here and `forDay()` in the page
both answer "which cohort does this date get", and they disagree in two places a reader would notice and no
unit test would: a date before the plan begins, where a plain `%` is negative in both languages and
`days[-1]` is the last element in Python and `undefined` in JavaScript, and a date past the end, where the
question is whether the plan cycles or freezes. So the plan ships this module's own answer for three weeks
of dates straddling it, and `tests/probe.mjs` asserts the page reproduces every one.

FAIR MEANS EVERY CATEGORY EVERY DAY, AND POPULARITY IS NOT AN INPUT
-------------------------------------------------------------------
`stars` is not read by anything in this module, and that is the point rather than an omission. The
front page already ranks by stars; a Discover that also consulted them would be the front page with a
different heading. The only inputs are the category a row is in and when it was last featured.

Every one of the 14 categories appears in every day's fifty, and the number of slots each gets is
weighted by the square root of its size. The two obvious rules are both worse:

  * Proportional to size gives the largest category 26 of the 50 slots, because it holds 51% of the rows
    (4,537 of 8,856). Half of Discover would be MCP servers, which is the front page's shape again.
  * Equal shares -- 3 or 4 each -- sound fairest and are the least fair over time. The 29-row category
    would be exhausted in its first week and start repeating itself, while the 4,537-row one would take
    181 weeks to come round: a 156x spread in how often a project gets its turn.

Square root splits the difference. Measured on the 8,856-row corpus: 9 slots a day for the largest
category and 2 for the smallest, full rotation in 72 weeks against 2.1, and every one of the fourteen
present in all seven days of a week with no row repeated inside it. A 34x spread rather than 156x, and
the half-page of one category avoided. `allocate()` is the rule; `discover_test.py` asserts these
properties rather than trusting this paragraph.

Within a category the queue is ordered by when each row was last featured, oldest first, never-featured
first of all, ties broken by a hash of the week and the name. So the week's picks are the 350 rows that
have waited longest, and no row can be picked twice in a week: each is dealt out of a queue that only
moves forwards. A category with fewer rows than its week's allocation is the one case that cannot honour
that -- 7 slots and 3 rows -- and it hands its overflow to the largest queue rather than shipping a day
of 47.

Each day's fifty are dealt round-robin across the categories, so the carousel alternates rather than
opening with twelve rows from the largest category, and the rotation starts at a different category each
day so the first card is not always from the same one.

WHAT THIS CANNOT SEE
--------------------
That a small category does not feel repetitive. Fourteen categories in fifty slots means the 29-row one
gets two slots a day, so its whole membership comes round every fortnight while the largest category
takes 72 weeks. That is a property of a 29-row category rather than of this rule -- the only ways out are
to drop it from some days, which makes it undiscoverable, or to shrink it to one slot, which buys four
weeks of rotation and costs half its daily visibility. It is a genuine trade and the resolution is
written down here so the next person can change it on purpose.

Whether the fifty are any *good*. It has no idea what a project does: `cat` is a curated label and the
rest of the row is not read. It cannot tell an abandoned repository from a live one -- `pushed` is in the
dataset and deliberately not consulted here, because "show me something I would not have found" and
"show me something maintained" are different products and mixing them quietly turns this back into a
ranking. What it can promise is coverage, a stable day, and that no row jumps the queue.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "state" / "discover.json"

# The zone the day rolls over in: 00:00:00 in Chicago, CDT or CST as the calendar decides. Named rather
# than offset on purpose -- see the docstring.
TZ = "America/Chicago"

PER_DAY = 50
DAYS = 7

# Sunday. `weekly.yml` runs on Sundays and a plan is computed for the seven days starting with the day
# it ran, so the week's first date is the run's own date; `week_start` exists for the daily builds, which
# need to know which week the current plan belongs to without re-picking it.
WEEK_STARTS_ON = 6  # date.weekday(): Monday is 0, so Sunday is 6.

# UTC instants with something to say about the zone, paired with the Chicago date each falls in. Both
# 2026 DST switches, both sides, plus a plain instant that is "yesterday" in Chicago and "today" in UTC
# -- which is the case a naive `new Date().toISOString().slice(0,10)` gets wrong for five hours a day.
PROBE_INSTANTS = [
    "2026-03-08T07:30:00Z",  # 01:30 CST, half an hour before the spring switch
    "2026-03-08T08:30:00Z",  # 03:30 CDT, half an hour after it
    "2026-11-01T05:30:00Z",  # 00:30 CDT, before the autumn switch
    "2026-11-01T07:30:00Z",  # 01:30 CST, after it
    "2026-09-21T04:30:00Z",  # 23:30 the previous day in Chicago
    "2026-09-21T05:30:00Z",  # 00:30, the same instant an hour later: the rollover itself
    "2026-12-31T23:59:59Z",  # a year boundary UTC is already past and Chicago is not
]


def zone() -> ZoneInfo:
    """The tz database entry for `TZ`, or a hard stop.

    A missing tz database is the one failure here that could publish a plan quietly dated the wrong day,
    so it is a refusal rather than a fallback. On Windows this needs the `tzdata` package; on the CI
    runner the system database is there. An offset computed by hand was the alternative and is a worse
    trade: it would be a second implementation of the DST rule, correct until the next time the United
    States changes its mind about when the clocks move.
    """
    try:
        return ZoneInfo(TZ)
    except ZoneInfoNotFoundError as exc:  # pragma: no cover - environment, not logic
        sys.exit(f"discover: no tz database entry for {TZ} ({exc}). "
                 f"Install `tzdata` (pip install tzdata) so the rollover day can be resolved.")


def today(now: datetime | None = None) -> str:
    """The current date in `TZ`, as ISO. `now` is an aware datetime, for tests."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("discover.today() needs an aware datetime; a naive one has no zone to convert")
    return now.astimezone(zone()).date().isoformat()


def week_start(day: str) -> str:
    """The Sunday on or before `day`. The week a date's plan belongs to."""
    d = date.fromisoformat(day)
    return (d - timedelta(days=(d.weekday() - WEEK_STARTS_ON) % 7)).isoformat()


def dates(start: str, days: int = DAYS) -> list[str]:
    d = date.fromisoformat(start)
    return [(d + timedelta(days=i)).isoformat() for i in range(days)]


def blank() -> dict:
    return {"week": "", "shown": {}}


def load(path: Path | None = None) -> dict:
    """The ledger, or an empty one. Missing keys are filled, so an older file still loads."""
    path = path or LEDGER
    if not path.exists():
        return blank()
    state = json.loads(path.read_text(encoding="utf-8"))
    state.setdefault("week", "")
    state.setdefault("shown", {})
    return state


def save(state: dict, path: Path | None = None) -> None:
    path = path or LEDGER
    path.parent.mkdir(parents=True, exist_ok=True)
    # Sorted, one key per line: this file is committed every week, so its diff should be the rows that
    # were featured and nothing else.
    path.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def allocate(sizes: dict, per_day: int = PER_DAY) -> dict:
    """How many of the day's slots each category gets: square-root weighted, largest remainder.

    Every category with a row in it gets at least one slot, which is the property the whole feature
    rests on -- a category that can be absent from a day is a category a reader can never stumble into.
    That floor is why this cannot be a plain proportional split, and the remainder pass is why it cannot
    be a plain `round()`: fourteen independent roundings do not add up to fifty.

    Degenerate input is handled rather than asserted away: more categories than slots (which this corpus
    is nowhere near, 14 against 50) keeps the largest `per_day` of them, because one slot each and some
    categories silently missing is the one outcome worse than a weighted split.
    """
    live = {k: n for k, n in sizes.items() if n > 0}
    if not live or per_day <= 0:
        return {}
    if len(live) > per_day:
        live = dict(sorted(live.items(), key=lambda kv: (-kv[1], str(kv[0])))[:per_day])

    weight = {k: math.sqrt(n) for k, n in live.items()}
    total = sum(weight.values())
    exact = {k: (per_day - len(live)) * w / total for k, w in weight.items()}
    out = {k: 1 + int(v) for k, v in exact.items()}
    # Largest fractional part first, then the bigger category, then the name: every tie is broken by
    # something in the data, so two runs of this cannot disagree.
    short = per_day - sum(out.values())
    order = sorted(live, key=lambda k: (-(exact[k] % 1), -live[k], str(k)))
    for k in order[:short]:
        out[k] += 1
    assert sum(out.values()) == per_day, (out, per_day)
    return out


def queue(nwos: list[str], shown: dict, week: str) -> list[str]:
    """One category's rows, longest-waiting first.

    `shown.get(nwo, "")` is the week it was last featured, and "" sorts before every date -- so a row
    that has never been featured is always ahead of one that has. The hash breaks ties without
    introducing an alphabet: sorting equal-waiting rows by name would put `a*` on Discover every week
    and `z*` never, which is exactly the systematic unfairness the ledger exists to remove.
    """
    return sorted(nwos, key=lambda n: (shown.get(n, ""), _key(n, week)))


def _key(nwo: str, week: str) -> str:
    return hashlib.sha256(f"{week}|{nwo}".encode("utf-8")).hexdigest()


def deal(rows, shown: dict, week: str, days: list[str]) -> list[dict]:
    """The week's cohorts: one dated list of `PER_DAY` names per day in `days`.

    `rows` is an iterable of `(nwo, cat)`. Nothing else about a row is read, deliberately: see the
    docstring on why popularity is not an input.
    """
    by_cat: dict = {}
    for nwo, cat in rows:
        by_cat.setdefault(cat, []).append(nwo)
    if not by_cat:
        return [{"date": d, "picks": []} for d in days]

    alloc = allocate({c: len(v) for c, v in by_cat.items()})
    queues = {c: queue(v, shown, week) for c, v in by_cat.items() if c in alloc}
    heads = {c: 0 for c in queues}
    # The biggest queue absorbs the overflow when a small category runs out mid-week. Chosen by size and
    # then by name so it is the same queue on every machine.
    biggest = sorted(queues, key=lambda c: (-len(queues[c]), str(c)))[0]
    order = sorted(queues, key=lambda c: (-alloc[c], str(c)))

    def take(cat, used: set) -> str | None:
        """The next unused row for `cat`: its own queue, then the biggest, then a lap around.

        The lap is the smallest-corpus case and it is the one place a row can be featured twice in a
        week. Nine rows cannot fill seven days of fifty, and of the two ways to be wrong about that --
        six empty days, or the same nine rows every day -- only one of them is a Discover page. So the
        invariant this enforces is per *day*: no row appears twice in one day, ever. Per week it is
        best-effort, and on any corpus that can afford it -- 8,856 rows against 350 picks -- the lap is
        never reached and the week is distinct too, which `discover_test.py` asserts both ways.
        """
        for c in (cat, biggest):
            q, i = queues[c], heads[c]
            while i < len(q):
                n = q[i]
                i += 1
                if n not in used:
                    heads[c] = i
                    return n
            heads[c] = i
        for c in (cat, biggest):
            for n in queues[c]:
                if n not in used:
                    return n
        return None

    out = []
    for n, day in enumerate(days):
        # A day's slots as a flat list of categories, then dealt round-robin so the carousel alternates.
        # The rotation starts one category further along each day: without it every day opens with the
        # largest category, which is the one thing a reader would notice as a pattern.
        rota = order[n % len(order):] + order[:n % len(order)]
        want = {c: alloc[c] for c in rota}
        picks: list[str] = []
        used: set = set()
        while len(picks) < sum(alloc.values()):
            moved = False
            for c in rota:
                if want[c] <= 0:
                    continue
                got = take(c, used)
                want[c] -= 1
                if got is not None:
                    picks.append(got)
                    used.add(got)
                    moved = True
            if not moved:
                break  # Nothing unused left anywhere: a corpus smaller than a day. Short is honest.
        out.append({"date": day, "picks": picks})
    return out


def plan(rows, state: dict | None = None, day: str | None = None, snapshot: str = "") -> tuple[dict, dict]:
    """A week's plan and the ledger that records it. Pure: nothing is read or written here.

    Returns `(plan, state)`. `state["shown"]` is stamped with the week for every row the plan features,
    which is what moves those rows to the back of their category's queue next time.
    """
    state = dict(state or blank())
    state["shown"] = dict(state.get("shown", {}))
    day = day or today()
    # The plan runs from the day it was computed, and is *labelled* with the Sunday that week began on.
    # For the weekly, which runs on Sundays, those are the same date. For a dispatch on a Wednesday they
    # are not, and the label is still the right one: it is the ledger's name for "when did this row last
    # have its turn", and two plans computed in one week must agree about that or the second undoes the
    # first's rotation.
    week = week_start(day)
    span = dates(day)
    cohorts = deal(rows, state["shown"], week, span)
    # Three weeks of dates straddling the plan -- the week before it begins, the seven it covers, the week
    # after it ends -- each paired with the cohort date this module gives it. The page's `forDay()` has to
    # reproduce all 21 of them; the docstring says why those two boundaries are where two languages drift.
    # Dates only, not picks: the picks are already in the file and a second copy would triple its size.
    around = dates((date.fromisoformat(day) - timedelta(days=DAYS)).isoformat(), 3 * DAYS)
    for c in cohorts:
        for nwo in c["picks"]:
            state["shown"][nwo] = week
    state["week"] = week
    return {
        "generated": day,
        "week": week,
        "tz": TZ,
        "per_day": PER_DAY,
        "snapshot": snapshot,
        "probe": {i: today(datetime.fromisoformat(i.replace("Z", "+00:00"))) for i in PROBE_INSTANTS},
        "cycle": {d: for_day({"days": cohorts}, d)[0] for d in around},
        "days": cohorts,
    }, state


def covers(published: dict, day: str) -> bool:
    """Does this plan have a cohort dated `day`? The question the stages ask before re-picking."""
    return any(c.get("date") == day for c in published.get("days", []))


def for_day(published: dict, day: str) -> tuple[str, list[str]]:
    """The cohort to show on `day`: `(the cohort's own date, names)`.

    A plan that has run out is cycled rather than frozen. If the weekly stops -- and it has, for five
    consecutive builds in September 2026 -- the alternative is Discover showing one Saturday's fifty
    every day until somebody notices, which is the failure mode with no symptom. Cycling keeps the
    rotation moving through the seven cohorts that do exist, and the returned date is the cohort's own,
    so a caller can say which day's picks these really are instead of implying they are today's.
    """
    days = published.get("days") or []
    if not days:
        return "", []
    for c in days:
        if c.get("date") == day:
            return c["date"], list(c.get("picks") or [])
    first = date.fromisoformat(days[0]["date"])
    c = days[(date.fromisoformat(day) - first).days % len(days)]
    return c["date"], list(c.get("picks") or [])


def main() -> None:
    """Print what a plan for today would contain, without writing anything. The stage is 19d_discover."""
    data = json.loads((ROOT / "docs" / "data.json").read_text(encoding="utf-8"))
    ix = {c: i for i, c in enumerate(data["cols"])}
    rows = [(r[ix["nwo"]], r[ix["cat"]]) for r in data["rows"]]
    day = sys.argv[1] if len(sys.argv) > 1 else today()
    published, state = plan(rows, load(), day, data.get("snapshot", ""))
    cats = [c["name"] for c in data.get("cats", [])]
    print(f"{len(rows):,} rows, week of {published['week']}, {TZ}")
    for c in published["days"]:
        print(f"  {c['date']}  {len(c['picks'])} picks, first three: {', '.join(c['picks'][:3])}")
    counts: dict = {}
    for nwo in published["days"][0]["picks"]:
        cat = dict(rows)[nwo]
        counts[cat] = counts.get(cat, 0) + 1
    print("  day one by category:")
    for cat, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        label = cats[cat] if isinstance(cat, int) and cat < len(cats) else cat
        print(f"    {n:3}  {label}")
    print(f"  ledger would hold {len(state['shown']):,} rows")


if __name__ == "__main__":
    main()
