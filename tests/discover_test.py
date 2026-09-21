"""Unit tests for the daily-fifty rule in `scripts/discover.py`.

Discover publishes a dated list: fifty projects a day, seven days at a time, the same fifty for every
reader, rolled over at 00:00 in one named zone. The rule that chooses them is the whole feature -- a
carousel of fifty rows is easy, and a carousel that is *fair* is not -- and every property worth having is
a property of a sequence of weeks rather than of one call:

  * every category in every day, or a reader can never stumble into a small one;
  * no row twice in a week, so a day is fifty things and not forty-one;
  * a row featured this week goes to the back of the queue, which is what makes the corpus rotate instead
    of resampling its popular end;
  * and `stars` is not an input, because the front page is already sorted by stars and a Discover that
    consulted them would be the front page with a different heading.

So this file runs the rule over eight consecutive weeks against synthetic corpora whose shape is chosen to
break it -- a category with fewer rows than its week's allocation, more categories than there are slots, a
corpus smaller than a single day -- with the date supplied rather than read from the clock. It imports
`discover` alone: no stage, no `docs/`, no network, and the ledger is repointed into a temp directory
before the first call, so a broken rule cannot reach the committed `state/discover.json`.

Nine groups:

  the day       -- the one piece of clock arithmetic in the feature. `TZ` is a named zone rather than an
                   offset, so the rollover is asserted on both sides of both 2026 DST switches and at the
                   instant UTC has already turned over and Chicago has not. The expected dates are written
                   out by hand here: taking them from the module would only prove it agrees with itself.
  the shape     -- seven consecutive dated cohorts starting on the day asked for, fifty each, and the
                   fields the page needs (`tz`, `per_day`, `probe`) present and honest.
  the split     -- `allocate()`: sums to the day's slots exactly, never drops a live category, never hands
                   the largest one half the day, and orders slots the way it orders sizes. Also the
                   degenerate inputs, which are handled rather than asserted away.
  fairness      -- every category in every day, no row twice in a week, and no overlap between consecutive
                   weeks while the corpus can afford one.
  rotation      -- the ledger's whole purpose: this week's picks are at the back of next week's queue, and
                   a corpus that keeps getting picked over eventually gets covered. Asserted as a
                   trajectory over eight weeks, not as one comparison.
  blindness     -- that popularity, recency and row order change nothing. Three shuffles and a
                   star-permutation, each asserted to produce a byte-identical plan.
  the fallback  -- `covers()` and `for_day()`. A plan that has run out cycles rather than freezing, which
                   is the difference between Discover looking stale and Discover looking broken. Plus the
                   ledger on disk: sorted, one row per line, one trailing newline.
  the copies    -- the four clock functions that exist twice, once in `19d_discover.py`'s `DISCOVER CORE`
                   block and once in the homepage strip in `19_pages.py`, asserted character for character
                   off the two files as text. Plus the five accents by index, the flag, the deep link's two
                   halves, and that the stage is in both workflows. Source, not built output: `19_pages.py`
                   needs CI's crawl cache to run, so the committed `docs/index.html` in any checkout
                   predates whatever was last changed about the strip.
  the payload   -- the real `docs/discover.json`, which is the one thing here that is about the ingest
                   rather than the rule: its columns against `CARD_COLS`, every pick backed by a row, no row
                   carried that no day names, and the ledger's week matching the plan's.

What this cannot see: whether the page renders what it computes, or whether the fifty are any good. The
carousel, the deep link into it and the rollover in the browser are `tests/probe.mjs`'s and
`tests/cards-check.mjs`'s half -- including the one assertion that needs a real JavaScript engine, which is
that the page's `dayIn()` and `forDay()` reproduce the `probe` and `cycle` fixtures this file checks the
Python side of.

Run: python tests/discover_test.py
"""
from __future__ import annotations

import ast
import collections
import importlib.util
import json
import os
import random
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec = importlib.util.spec_from_file_location("discover_for_test", SCRIPTS / "discover.py")
d = importlib.util.module_from_spec(spec)
sys.modules["discover_for_test"] = d
spec.loader.exec_module(d)

# Under `run.mjs` this lands inside the run's own scratch root, swept on the way out however the run ended.
TMP = Path(tempfile.mkdtemp(prefix="discover_test_", dir=os.environ.get("AAA_TMP") or None))
d.LEDGER = TMP / "discover.json"

ok = bad = 0


def eq(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, cond, detail="") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail!r}" if detail else ""))


def corpus(shape: dict) -> list[tuple[str, int]]:
    """`{category: how many rows}` as the `(nwo, cat)` pairs the rule takes.

    Names are `c<cat>/r<n>`, which makes a failure legible: every assertion below that prints a pick
    prints which category it came from.
    """
    return [(f"c{c}/r{i}", c) for c, n in shape.items() for i in range(n)]


def cats_of(rows, picks) -> list:
    at = dict(rows)
    return [at[p] for p in picks]


def utc(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)


# The real corpus's shape, to two significant figures, as of the 8,856-row import: one category with half
# the rows, one with 29. Copied rather than loaded, because the point of a fixture is to stay still while
# the atlas moves -- and because a harness that reads `docs/data.json` measures the ingest, not the rule.
LIVE_SHAPE = {0: 338, 1: 281, 2: 823, 3: 4537, 4: 463, 5: 669, 6: 99, 7: 150,
              8: 421, 9: 611, 10: 41, 11: 29, 12: 252, 13: 142}
LIVE = corpus(LIVE_SHAPE)

print("\n-- the day: one named zone, and both DST switches")

# Written out by hand. America/Chicago is CST (-6) until 02:00 local on the second Sunday in March and CDT
# (-5) until the first Sunday in November, and the only thing that matters here is which *date* an instant
# falls in -- so each pair below straddles a boundary that a fixed offset gets wrong.
for instant, want in [
    ("2026-03-08T07:30:00Z", "2026-03-08"),  # 01:30 CST, before the spring forward
    ("2026-03-08T08:30:00Z", "2026-03-08"),  # 03:30 CDT, after it: same date, an hour of it missing
    ("2026-11-01T05:30:00Z", "2026-11-01"),  # 00:30 CDT, before the fall back
    ("2026-11-01T07:30:00Z", "2026-11-01"),  # 01:30 CST, after it: the hour that happens twice
    ("2026-09-21T04:30:00Z", "2026-09-20"),  # 23:30 the day before, in Chicago
    ("2026-09-21T05:30:00Z", "2026-09-21"),  # 00:30: the rollover itself
    ("2026-12-31T23:59:59Z", "2026-12-31"),  # UTC's new year is Chicago's afternoon
    ("2027-01-01T05:59:59Z", "2026-12-31"),  # ...and its last minute
    ("2027-01-01T06:00:00Z", "2027-01-01"),  # ...to the second
]:
    eq(f"{instant} is {want} in {d.TZ}", d.today(utc(instant)), want)

def raised(fn, *a):
    """The exception `fn(*a)` raised, or None. A refusal is a behaviour, so it is asserted like one."""
    try:
        fn(*a)
        return None
    except Exception as exc:  # noqa: BLE001 - the type of it is the assertion
        return exc


true("a naive datetime is refused rather than quietly read as UTC",
     isinstance(raised(d.today, datetime(2026, 9, 21)), ValueError),
     raised(d.today, datetime(2026, 9, 21)))

eq("week_start on a Sunday is that Sunday", d.week_start("2026-09-20"), "2026-09-20")
eq("...on the Saturday after, still that Sunday", d.week_start("2026-09-26"), "2026-09-20")
eq("...on the next Sunday, the next one", d.week_start("2026-09-27"), "2026-09-27")
eq("...and on a Monday, the day before it", d.week_start("2026-09-21"), "2026-09-20")
eq("dates() runs forward from the day it is given",
   d.dates("2026-09-20"), ["2026-09-20", "2026-09-21", "2026-09-22", "2026-09-23",
                           "2026-09-24", "2026-09-25", "2026-09-26"])
eq("...seven of them, one per day of the week", len(d.dates("2026-09-20")), d.DAYS)

print("\n-- the shape: what the page is handed")

plan, state = d.plan(LIVE, d.blank(), "2026-09-20", snapshot="2026-09-20")
eq("a plan carries one cohort per day", len(plan["days"]), d.DAYS)
eq("...dated consecutively from the day it was built",
   [c["date"] for c in plan["days"]], d.dates("2026-09-20"))
eq("...with the day's full count in each", sorted({len(c["picks"]) for c in plan["days"]}), [d.PER_DAY])
eq("...the zone written down rather than assumed", plan["tz"], "America/Chicago")
eq("...the count written down, so the page never has to guess it", plan["per_day"], d.PER_DAY)
eq("...and the week it belongs to", (plan["week"], plan["generated"]), ("2026-09-20", "2026-09-20"))
eq("the probe covers every instant the page's own clock is checked against",
   sorted(plan["probe"]), sorted(d.PROBE_INSTANTS))
eq("...and each one carries the date this module resolved it to",
   plan["probe"]["2026-09-21T04:30:00Z"], "2026-09-20")
# `cycle` is the same device for `for_day()` that `probe` is for `today()`: this module's own answer, shipped
# so the page's copy can be held to it. Three weeks, because the two dates the copies disagree on are both
# outside the plan -- one before it, one after -- and a fixture that only covered the seven days it does
# cover would assert nothing about either.
eq("the cycle fixture spans the week before the plan, the plan, and the week after",
   sorted(plan["cycle"]), d.dates("2026-09-13", 3 * d.DAYS))
eq("...with every date the plan does cover mapping to its own cohort",
   [plan["cycle"][c["date"]] for c in plan["days"]], d.dates("2026-09-20"))
eq("...a date past the end mapping to the cohort the rotation lands on",
   plan["cycle"]["2026-09-28"], "2026-09-21")
eq("...and one before it begins mapping six days along, which is where a negative remainder goes",
   plan["cycle"]["2026-09-19"], "2026-09-26")
eq("...and every entry in it is what for_day() actually returns, so it cannot drift from the function",
   plan["cycle"], {day: d.for_day(plan, day)[0] for day in plan["cycle"]})
true("a plan is JSON, with nothing in it that json cannot write",
     json.loads(json.dumps(plan)) == plan)
eq("a plan built twice from the same ledger is byte-identical",
   json.dumps(d.plan(LIVE, d.blank(), "2026-09-20", snapshot="2026-09-20")[0], sort_keys=True),
   json.dumps(plan, sort_keys=True))
true("a plan for the next week is not the same fifty",
     set(d.plan(LIVE, state, "2026-09-27")[0]["days"][0]["picks"]) != set(plan["days"][0]["picks"]))
eq("a plan dispatched mid-week still runs from that day",
   [c["date"] for c in d.plan(LIVE, d.blank(), "2026-09-23")[0]["days"]][:2],
   ["2026-09-23", "2026-09-24"])
eq("...and is still filed under the Sunday that week began on",
   d.plan(LIVE, d.blank(), "2026-09-23")[0]["week"], "2026-09-20")

print("\n-- the split: fifty slots across fourteen categories")

alloc = d.allocate(LIVE_SHAPE)
eq("the allocation sums to the day exactly", sum(alloc.values()), d.PER_DAY)
eq("...and no live category is left out of it", sorted(alloc), sorted(LIVE_SHAPE))
true("every category gets at least one slot, which is what makes it discoverable",
     min(alloc.values()) >= 1, alloc)
true("the largest category does not get half the day, which is what proportional would do",
     alloc[3] < d.PER_DAY // 2, (alloc[3], d.PER_DAY))
true("...it gets more than an equal share, because it has 51% of the rows",
     alloc[3] > d.PER_DAY / len(LIVE_SHAPE), (alloc[3], d.PER_DAY / len(LIVE_SHAPE)))
true("a bigger category never gets fewer slots than a smaller one",
     all(alloc[a] >= alloc[b]
         for a in LIVE_SHAPE for b in LIVE_SHAPE if LIVE_SHAPE[a] >= LIVE_SHAPE[b]), alloc)
eq("the measured split is the one the docstring claims", (alloc[3], alloc[11]), (9, 2))
eq("an empty corpus allocates nothing rather than dividing by zero", d.allocate({}), {})
eq("...and so does a day with no slots", d.allocate({1: 10}, 0), {})
eq("a category with no rows in it is not given a slot", d.allocate({1: 10, 2: 0}), {1: 50})
eq("one category takes the whole day", d.allocate({7: 900}), {7: 50})
many = d.allocate({i: 100 + i for i in range(80)})
eq("more categories than slots still sums to the day", sum(many.values()), d.PER_DAY)
eq("...by keeping the largest fifty of them", (len(many), min(many), max(many)), (50, 30, 79))
eq("...one slot each, because there is nothing left to weight", sorted(set(many.values())), [1])

print("\n-- fairness: every category, every day, once each")

state = d.blank()
weeks = []
for w, day in enumerate(["2026-09-20", "2026-09-27", "2026-10-04", "2026-10-11",
                         "2026-10-18", "2026-10-25", "2026-11-01", "2026-11-08"]):
    plan, state = d.plan(LIVE, state, day)
    weeks.append([c["picks"] for c in plan["days"]])

for w, days in enumerate(weeks[:3], 1):
    flat = [p for day in days for p in day]
    eq(f"week {w} deals seven full days", [len(day) for day in days], [d.PER_DAY] * d.DAYS)
    eq(f"...with no row in it twice", len(set(flat)), len(flat))
    eq(f"...and every category in every day",
       sorted({len(set(cats_of(LIVE, day))) for day in days}), [len(LIVE_SHAPE)])

eq("consecutive weeks do not overlap at all while the corpus can afford it",
   [len(set(p for day in weeks[i] for p in day) & set(p for day in weeks[i + 1] for p in day))
    for i in range(len(weeks) - 1)], [0] * (len(weeks) - 1))
first = weeks[0][0]
true("a day does not open with a run of its largest category",
     len(set(cats_of(LIVE, first[:6]))) >= 5, cats_of(LIVE, first[:6]))
true("...and adjacent cards are mostly from different categories",
     sum(1 for a, b in zip(cats_of(LIVE, first), cats_of(LIVE, first)[1:]) if a == b) < d.PER_DAY // 5,
     cats_of(LIVE, first))
true("the seven days of a week do not all open with the same category",
     len({cats_of(LIVE, day)[0] for day in weeks[0]}) > 1,
     [cats_of(LIVE, day)[0] for day in weeks[0]])

print("\n-- rotation: the ledger is what stops it resampling the same end of the corpus")

shown = state["shown"]
dealt = [p for w in weeks for day in w for p in day]
eq("eight weeks deal eight weeks of full days", len(dealt), 8 * d.DAYS * d.PER_DAY)
eq("...and the ledger holds exactly the distinct rows among them", len(shown), len(set(dealt)))
true("...which is a growing share of the corpus rather than a fixed sample",
     len(shown) / len(LIVE) > 0.25, len(shown) / len(LIVE))
true("a row featured this week is not featured next week",
     not (set(p for day in weeks[6] for p in day) & set(p for day in weeks[7] for p in day)))
true("...and the rows that have waited longest are the ones picked",
     all(shown[p] == "2026-11-08" for p in weeks[7][0]), weeks[7][0][:3])

# The one shape that cannot honour "no row twice in a week": a category with fewer rows than its week's
# allocation. The day must still be full, so the overflow has to come from somewhere, and it comes from the
# largest queue rather than from a short day.
small = corpus({1: 3, 2: 4000})
plan, _ = d.plan(small, d.blank(), "2026-09-20")
eq("a category with three rows still leaves every day full",
   [len(c["picks"]) for c in plan["days"]], [d.PER_DAY] * d.DAYS)
week_flat = [p for c in plan["days"] for p in c["picks"]]
eq("...with no row repeated even so", len(set(week_flat)), len(week_flat))
true("...and its three rows are all featured", {"c1/r0", "c1/r1", "c1/r2"} <= set(week_flat))
true("...while the overflow is dealt from the biggest category",
     collections.Counter(cats_of(small, week_flat))[2] > d.PER_DAY * d.DAYS * 0.8,
     collections.Counter(cats_of(small, week_flat)))

tiny = corpus({1: 9, 2: 11})
plan, _ = d.plan(tiny, d.blank(), "2026-09-20")
eq("a corpus smaller than one day fills every day with all of itself, and no more",
   [len(c["picks"]) for c in plan["days"]], [len(tiny)] * d.DAYS)
eq("...with no row twice in a day, which is the invariant that holds at every corpus size",
   [len(set(c["picks"])) for c in plan["days"]], [len(tiny)] * d.DAYS)
eq("...and every row of it in every day", sorted(plan["days"][0]["picks"]), sorted(n for n, _ in tiny))
eq("...including the last day, rather than six empty ones after the queues ran out",
   sorted(plan["days"][-1]["picks"]), sorted(n for n, _ in tiny))
eq("an empty corpus produces seven empty days rather than a crash",
   [c["picks"] for c in d.plan([], d.blank(), "2026-09-20")[0]["days"]], [[]] * d.DAYS)

print("\n-- blindness: popularity, recency and row order change nothing")

base = d.plan(LIVE, d.blank(), "2026-09-20")[0]["days"]
shuffled = list(LIVE)
random.Random(11).shuffle(shuffled)
eq("the order the rows arrive in does not change the plan",
   d.plan(shuffled, d.blank(), "2026-09-20")[0]["days"], base)
eq("...nor does reversing them", d.plan(list(reversed(LIVE)), d.blank(), "2026-09-20")[0]["days"], base)
true("nothing in the module reads a star count, a push date or a list count",
     not any(w in (SCRIPTS / "discover.py").read_text(encoding="utf-8").split('"""')[2]
             for w in ("stars", "pushed", "lists[", '"lists"')),
     "a ranking signal is being consulted by the rule")
eq("the rule takes (nwo, cat) and nothing else, so there is nothing else it could read",
   d.plan([(n, c) for n, c in LIVE], d.blank(), "2026-09-20")[0]["days"], base)

print("\n-- the fallback, and the ledger on disk")

plan, state = d.plan(LIVE, d.blank(), "2026-09-20")
eq("covers() sees a date the plan has", d.covers(plan, "2026-09-23"), True)
eq("...and does not see one it does not", d.covers(plan, "2026-09-28"), False)
eq("for_day() on a date in the plan is that date's cohort",
   d.for_day(plan, "2026-09-23")[1], plan["days"][3]["picks"])
eq("...and says which date it is showing", d.for_day(plan, "2026-09-23")[0], "2026-09-23")
eq("a day past the end cycles to the start rather than freezing on the last cohort",
   d.for_day(plan, "2026-09-27")[0], "2026-09-20")
# The plan spans 09-20..09-26, so a cycled date can only ever be one of those seven. 10-04 is fourteen
# days out and lands back on the first cohort, which is the arithmetic that makes this a rotation rather
# than a slow drift into one cohort: the offset is taken modulo seven, not clamped.
eq("...and keeps cycling, so a stalled build still rotates",
   [d.for_day(plan, day)[0] for day in ["2026-09-28", "2026-09-29", "2026-10-04"]],
   ["2026-09-21", "2026-09-22", "2026-09-20"])
eq("...through all seven cohorts and no eighth, however long the build stays stalled",
   sorted({d.for_day(plan, day)[0] for day in d.dates("2026-09-27", 40)}), d.dates("2026-09-20"))
eq("a day before the plan begins cycles as well",
   d.for_day(plan, "2026-09-19")[0], plan["days"][6]["date"])
eq("an empty plan is empty rather than an exception", d.for_day({"days": []}, "2026-09-20"), ("", []))
eq("...and so is one with no days key at all", d.for_day({}, "2026-09-20"), ("", []))

d.save(state)
raw = d.LEDGER.read_text(encoding="utf-8")
eq("the ledger ends in exactly one newline", (raw.endswith("\n"), raw.endswith("\n\n")), (True, False))
lines = [ln for ln in raw.replace("\r\n", "\n").split("\n") if ln.startswith('  "')]
eq("the ledger is one row per line, so its weekly diff is legible", len(lines), len(state["shown"]))
eq("...and sorted, so the diff has no reordering in it",
   [ln.split('"')[1] for ln in lines], sorted(ln.split('"')[1] for ln in lines))
eq("a saved ledger loads back as itself", d.load(d.LEDGER), state)
eq("a ledger that is not there loads as an empty one", d.load(TMP / "nothing.json"), d.blank())
(TMP / "old.json").write_text('{"shown": {"a/b": "2026-09-13"}}', encoding="utf-8")
eq("...and one written before the week key existed still loads",
   d.load(TMP / "old.json"), {"week": "", "shown": {"a/b": "2026-09-13"}})

print("\n-- the copies: the strip on the index, and the stage that owns the original")

# Source text, not built output. The strip lives in `scripts/19_pages.py`, and that stage cannot run on this
# machine -- it needs the crawl cache CI holds -- so `docs/index.html` in any checkout predates whatever was
# last changed about the strip. An assertion here that read the built page would fail for the whole gap
# between a change and the next successful build, which is why `tests/probe.mjs` gets the half of this that
# needs a real evaluated function and this file gets the half that is a question about two files on disk.
PAGES = (SCRIPTS / "19_pages.py").read_text(encoding="utf-8")
STAGE = (SCRIPTS / "19d_discover.py").read_text(encoding="utf-8")


def jsfn(src: str, name: str) -> str:
    """One `const <name> = ...` out of a JS block, as text, including its closing brace.

    Two shapes, because both are in the block: an arrow function over several lines, closed by `  };` at the
    IIFE's own indent, and a one-liner that ends on the line it started. Indentation is the delimiter rather
    than a brace count, which is what lets this be four lines instead of a parser.
    """
    at = src.index(f"  const {name} = ")
    end = src.index("\n", at)
    return src[at:end] if src[end - 1] == ";" else src[at:src.index("\n  };\n", at) + len("\n  };")]


# THE FOUR FUNCTIONS THAT EXIST TWICE. `19_pages.py`'s `DSTRIP` is a copy of four members of the stage's
# `DISCOVER CORE` block, taken rather than shared because the alternative is the index loading a second
# script to answer one question. A copy is only safe if something notices when it stops being one, and this
# is that something: the text, character for character, with the comments left where each copy has them.
for name in ["dayIn", "asUTC", "daysBetween", "forDay"]:
    eq(f"the index's {name}() is the stage's {name}(), character for character",
       jsfn(PAGES, name), jsfn(STAGE, name))
true("...and there are four of them, so the loop above is not iterating over nothing",
     all(len(jsfn(PAGES, n)) > 40 for n in ["dayIn", "asUTC", "forDay"]))

# The accents by index, not as sets. A card wears its category's colour on the strip and the same colour on
# the page it links to, so two lists with the same five names in a different order would pass a set
# comparison and repaint every card on the click-through.
DACCENTS = ast.literal_eval(PAGES.split("const DACCENTS = ")[1].split(";")[0])
stage_accents = ast.literal_eval(STAGE.split("\nACCENTS = ")[1].split("\n")[0])
eq("the strip's accents are the stage's accents, in the stage's order", DACCENTS, stage_accents)
eq("...and there are five of them", len(DACCENTS), 5)

# The four ids the strip's JavaScript reaches for, against the markup the same file writes. A renamed id is
# a `null.innerHTML` in production and nothing at all here: `paintDiscover()` returns early on a missing
# `#dstrip`, so the strip would simply never appear.
for ident in ["dstrip", "dsrail", "dstripwhat", "dstripall"]:
    true(f'the markup carries id="{ident}", which the strip\'s script looks up',
         f'id="{ident}"' in PAGES and f'getElementById("{ident}")' in PAGES)
true("the strip is behind its flag, so index.discover_strip can turn it off",
     'FLAGS["index.discover_strip"]' in PAGES)
FLAGS = json.loads((ROOT / "config" / "app-flags.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "config" / "app-flags.schema.json").read_text(encoding="utf-8"))
true("...and that flag is declared, so the page is not reading a key nothing defines",
     any(f.get("key") == "index.discover_strip" for f in SCHEMA["flags"]))
true("...and carries a value, which is what the page is handed",
     FLAGS.get("index.discover_strip") in (0, 1))
# The teaser links to the page rather than to the project, which is the one thing about the strip that was
# asked for by name. Both halves of the deep link are asserted: the shape the index writes and the shape the
# page parses, in the two files that would have to agree for a click to land anywhere.
true("a card on the strip links into Discover, not off to the project",
     'href="discover/#repo=' in PAGES)
true("...and the page reads that fragment back", "repo=([^&]+)" in STAGE and "decodeURIComponent" in STAGE)

# BOTH WORKFLOWS. The same guard `19c_live.py` has, for the same reason: dropping this stage from the daily
# fails nothing loudly. The page would go on showing the week's picks with last Sunday's star counts on them,
# and the rollover would still work, so there is no symptom to notice.
for wf in ["daily.yml", "weekly.yml"]:
    text = (ROOT / ".github" / "workflows" / wf).read_text(encoding="utf-8")
    runs = [ln.strip() for ln in text.splitlines() if ln.strip() == "python scripts/19d_discover.py"]
    eq(f"{wf} runs the Discover stage exactly once", len(runs), 1)

print("\n-- the published plan, as the page will read it")

# The generator's real output, which every assertion above this group has deliberately avoided: the rule is
# tested on synthetic corpora so it stays still while the atlas moves. This is the other question -- whether
# what is on disk is the shape the page unpacks -- and only the real file can answer it.
pub = json.loads((ROOT / "docs" / "discover.json").read_text(encoding="utf-8"))
cols = ast.literal_eval(STAGE.split("\nCARD_COLS = ")[1].split("\n")[0])
eq("the payload names its columns, in the order the stage writes them", pub["cols"], cols)
eq("...and every row carries one value per column",
   sorted({len(r) for r in pub["rows"].values()}), [len(cols)])
eq("...the zone, so the page never hardcodes an offset", pub["tz"], d.TZ)
eq("...the day's count, the fortnight bound, and the fourteen category labels",
   (pub["per_day"], pub["window_days"], len(pub["cats"])), (d.PER_DAY, 14, 14))
true("...both fixtures the page's own copies are held to", bool(pub["probe"]) and bool(pub["cycle"]))
missing = sorted({n for c in pub["days"] for n in c["picks"]} - set(pub["rows"]))
eq("every pick in the plan has a row in the payload, so no card is drawn from nothing", missing, [])
extra = sorted(set(pub["rows"]) - {n for c in pub["days"] for n in c["picks"]})
eq("...and no row is carried that no day names, which is 90 KB nobody reads", extra, [])
eq("seven days of the day's count, which is what the page promises on its own heading",
   sorted({len(c["picks"]) for c in pub["days"]}), [d.PER_DAY])
true("the ledger on disk records the week the payload was picked for",
     d.load(ROOT / "state" / "discover.json")["week"] == pub["week"],
     d.load(ROOT / "state" / "discover.json")["week"] + " vs " + pub["week"])

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
