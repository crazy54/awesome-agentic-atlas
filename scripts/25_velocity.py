"""Star velocity: a ledger of what the counts used to be, and the two deltas a reader can act on.

Ranking by absolute stars ranks by age as much as by quality. A project that gained four thousand stars
last month sits below a dormant one with more total, and nothing on the page tells the reader which is
which -- `pushed_at` says a commit landed, not that anyone is arriving. The fix needs a number this
repository does not have: what the count *was*. There is exactly one snapshot here, today's, so the
first half of this stage is the only half that can do anything useful on the day it lands.

  state/star-history.json   the ledger. one line per sample, appended, committed
  docs/data.json            patched in place: two columns, `d7` and `d30`, and a `velocity` block

  python scripts/25_velocity.py                    record, derive, patch docs/data.json
  python scripts/25_velocity.py --dry-run          derive and report, write nothing
  python scripts/25_velocity.py --status           what the ledger holds and what it can answer
  python scripts/25_velocity.py --ledger P --data P    somewhere else, for measuring drift

After `19_pages.py`, always, and before anything that reads `docs/data.json`. It cannot run before,
because the present-day star count it needs is the one `19_pages.py` has just written -- and reading it
from there rather than from `cache/` is the same decision `22_detail.py` took for the same reason: this
project derives a star count in exactly one place, and a second derivation is a second chance for two
surfaces to disagree about how many stars something has. It also means this stage makes no API calls at
all, which is the acceptance criterion the ticket leads with.

  -- WHY THE LEDGER IS SAMPLED WEEKLY AND NOT DAILY --

The size question is not academic. Pages here is a `build_type: legacy` deployment and `state/` is
committed alongside `docs/`, so every version of this file is a version git keeps for ever, against a
repository whose entire packed history is ~110 MB today. A ledger is the one artefact in this pipeline
that is *supposed* to grow without bound, so the growth rate is the design.

Measured, not estimated, on today's 1,294 rows:

  one sample, `{"owner/name": 388645, ...}`      ~39,000 bytes
  one sample, JSON array of ints                   5,293 bytes
  one sample, the varint below                     2,889 bytes

The three differ only in what they spend per repo: 30 bytes of key text, 4 bytes of decimal digits, or
2.2 bytes of packed integer. So the roster of names is stored **once**, as an append-only array whose
index is the repo's slot for ever, and a sample is one string of 1,294 varints positionally aligned to
it. That is the whole encoding, and it is what makes the per-sample cost 2.2 bytes rather than 30.

Be warned that the second of those two decisions matters much less than it looks -- see the measurement
below, where the varint turns out to buy 11% of the history and the roster buys the rest.

The precision question has a blunter answer than expected, and the measurement is why this stage does
not quantise. Rounding every count to seven significant bits -- ~1% relative precision, which sounds
generous -- produces a payload of **2,889 bytes**, byte-for-byte the same size as the exact one, because
a varint of a 400,000-star count is four characters and a varint of its rounded form is also four. The
saving is zero and the cost is not: the maximum absolute error is 3,621 stars, and it lands on exactly
the rows this feature exists to rank. A 400,000-star project quantised to a 3,600-wide grid reports
"+0 this week" for five weeks and then "+3,600", which is not a coarse answer to "is this rising" but a
wrong one. Magnitude precision is free here. Nothing is bought by spending it.

What *is* expensive is temporal resolution, and that is where the reduction belongs. The two figures
this stage publishes are a 7-day delta and a 30-day delta. A 7-day delta needs a sample seven days old,
not seven samples; a 30-day delta needs one thirty days old. Daily sampling buys 365 samples a year to
answer two questions that need 52, so the ledger is on a seven-day grid and `record()` refuses a sample
that would land closer than `PERIOD_DAYS` to the last one. That is a 7x reduction with no loss at all in
either published figure -- the only thing given up is a daily-resolution sparkline, which nothing here
draws and which the ticket's own "30- and 90-day deltas" does not need.

Seven days is also the only cadence this repository can actually keep. `daily.yml` is gated on a source
list having moved and skips the whole build on days when none did, so a "daily" stage does not run
daily; `weekly.yml` is ungated and runs every Sunday. The grid and the guaranteed cadence are the same
number by luck, and `record()` does not depend on that -- see IDEMPOTENCE below.

  -- WHAT THAT COSTS, MEASURED, AND WHICH DECISION ACTUALLY PAID --

A three-year simulation of this exact file shape, 1,294 repos growing at ~1.5% a month, committed once
per sample into a scratch repository and then `git gc --aggressive --prune=now`:

  A  daily,  JSON array of ints   1,096 commits   working file 5,863 KB   pack 3.98 MiB
  B  daily,  this varint          1,096 commits   working file 3,254 KB   pack 3.55 MiB
  C  weekly, this varint            157 commits   working file   498 KB   pack  334 KiB

The honest reading of that table is not the one the encoding section above implies. A to B halves the
working file and buys **11%** of the history -- 3.98 MiB to 3.55 MiB -- because an append-only text file
is git's best case and its delta compressor plus zlib were already removing most of the redundancy that
decimal digits carry. The varint earns its place by keeping the file small enough to read and diff, not by
saving history. B to C is the whole win: **10.6x**, from one decision, the sampling grid.

So the shipped design costs ~111 KiB of packed history a year, and 2.18 KiB of it per sample -- less than
the 2,889 bytes a sample adds, because git compresses even the appended bytes. Growth is linear, not
quadratic, because the marginal cost is the new line and not the file. Against the ~32 MB a year
`weekly.yml`'s prerendered facet pages cost, and the ~224 MB a year the comment in `daily.yml` refuses to
spend on running them daily, that is small enough that nothing here throws history away. A rolling window
holding only the samples the two windows need would cap the file at ~9 KB and save perhaps 100 KiB a year,
in exchange for making the 90-day figure the ticket also asks for permanently unbuildable. Bad trade. Every
sample taken is kept.

  -- IDEMPOTENCE --

A sample is keyed by `docs/data.json`'s own `snapshot` date, not by `date.today()`. That is what makes
running this stage twice a no-op rather than a double-count: the second run reads the same snapshot,
finds that date already in `samples`, and records nothing. It holds for a re-run an hour later, a re-run
the next day from a `data.json` that was not rebuilt, and a re-run on a machine whose clock is wrong.
The grid check is the second guard and covers the other case -- a genuinely new snapshot that arrived
too soon after the last sample, which is what a `daily.yml` run in the middle of a week looks like.

Deriving and patching are unconditionally re-run either way, because both are pure functions of the
ledger and of `data.json` and are therefore free to repeat.

  -- WHY A REPO WITH NO HISTORY SHOWS NOTHING RATHER THAN ZERO --

`0` means "gained nothing", `""` means "we were not watching yet". Conflating them would put a fabricated
figure on 1,294 rows on the day this lands and on every row that joins the atlas afterwards, which is
worse than the feature not existing -- and the ticket says so: *rows lacking history degrade quietly
rather than showing zero*. So a window's column is `""` unless the ledger holds a sample of the right age
that also has a slot for that repo, and the page draws nothing at all for `""`.

The same rule covers the 55 rows whose star count is 0. The site already prints those as an em dash,
because a zero there means "this row is a folder inside somebody else's repo, or a dead link" rather than
an unstarred project, and a velocity computed from it would be arithmetic on a number that is not a
count. Absent, both ends.

Repos that leave the atlas keep their roster slot for ever and are stored as the sentinel 0, which is why
the stored value is `stars + 1`: it leaves a value free to mean "in the roster, not in this snapshot",
which is a different fact from "in this snapshot with no stars". A repo that leaves and comes back gets
its original slot and its history back. A repo that is *renamed* does not, because `16_build_all`'s
`canonicalise_nwo` resolves renames upstream and this stage sees a new name it has never recorded -- so
its velocity is absent until seven days of history accrue under the new name. That is the honest answer:
the ledger genuinely does not know that those two names are one project.

  -- THE ROSTER IS POSITIONAL, SO IT IS CHECKED RATHER THAN TRUSTED --

Every sample is a list of numbers whose meaning is "the Nth entry of `repos`". Sort that array, or delete
an entry from the middle of it, and every historical sample silently starts describing the wrong
projects -- no error, no missing key, just 1,294 wrong numbers. The file is committed and therefore
editable by hand, so each sample carries the slot count and a 4-byte digest of the roster prefix it was
written against:

  "<slots>:<digest>:<payload>"

`derive()` recomputes the digest and discards any sample that disagrees, loudly. That turns the failure
mode from wrong numbers into missing numbers, which the row rendering already knows how to survive.

  -- WHAT "RISING" MEANS, AND WHY THE THRESHOLD IS IN THE DATA --

The ticket's third acceptance criterion is the hard one: *Rising surfaces genuine momentum, not
small-number noise from tiny repos*. The two obvious rules both fail it. Ranking by percentage growth
makes a 4-star repo that gained one star (+25%) beat a 200,000-star project that gained three thousand
(+1.5%), which is the noise the criterion names. Requiring only an absolute gain is a star sort wearing a
different label, because gain scales with audience.

So the sort is by absolute gain -- which is the figure the ticket's own complaint is about, and which no
tiny repo can win -- and the *filter* requires both an absolute floor and a relative one:

  gain >= max(RISE_MIN_ABS, RISE_MIN_PCT% of the repo's own count)

Against today's distribution (p25 = 30 stars, p50 = 411, p75 = 4,357, p90 = 26,840, max = 388,645) that
means a 4-star repo can never qualify, because 25 > 4; a median 411-star project needs +25, or 6% in a
month; a p75 project needs +44, or 1%; and the largest needs +3,886. The absolute floor is what silences
the long tail and the percentage is what stops the head qualifying merely for being large.

Both constants travel in `data.json` rather than being hardcoded in the page, for the reason
`window_days` does: the rule is then one edit here and not two files that disagree. And it is worth being
blunt that they are guesses. There is no history in this repository to tune them against, and there will
be none for a month; the first honest look at them is the first build that has a real `d30` column.

`rise.col` names which window the filter uses and is what switches the whole feature on. It is `d30` when
the ledger can answer thirty days, `d7` when it can only answer seven, and `""` when it can answer
neither -- which is the state on the day this lands, and the state in which the page hides the chip and
the sort option entirely rather than offering a control that selects nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "state" / "star-history.json"
SITE_DATA = ROOT / "docs" / "data.json"

SCHEMA = 1

# The sampling grid, in days. See the docstring: seven is what the two published windows need, and it is
# also the only cadence `weekly.yml` guarantees. Raising it costs resolution in both windows; lowering it
# costs history size and buys nothing either window can spend.
PERIOD_DAYS = 7

# The windows, as (column name, nominal days). The column names land in `data.json`'s `cols` and in the
# page's row objects, so they are short for the same reason `nwo` and `img` are.
WINDOWS = [("d7", 7), ("d30", 30)]

# What counts as "a sample of the right age". A build can be missed -- a runner outage, a week where
# `weekly.yml` failed -- and the next sample is then fourteen days old rather than seven. Refusing to
# answer at all would throw the feature away over one bad Sunday; pretending a 14-day gain is a 7-day one
# would overstate it by 100%. So a sample within one sampling period of the target age is accepted and the
# span it actually covers travels with the figure, capped at half the window so a 30-day answer can never
# be built from a 14-day gap.
def tolerance(days: int) -> int:
    return min(PERIOD_DAYS, days // 2)


# The Rising threshold, expressed **per 30 days**. See the docstring for the distribution these were read
# off, and for why they are guesses until the ledger has a month in it. `derive()` scales them to the span
# the filter actually runs on, which matters because the filter falls back to the 7-day window for the
# three weeks before a 30-day one exists: 25 stars is a demanding month and an impossible week, so an
# unscaled threshold would leave the chip hidden for the entire period it exists to cover.
RISE_MIN_ABS = 25
RISE_MIN_PCT = 1.0

# Little-endian base-32 varint with a continuation flag in the sixth bit, so every value is 1-4 characters
# for anything under a million stars and the string is self-delimiting -- no separators to pay for at
# 1,294 values a sample. Every character is JSON-safe and needs no escaping, which a raw base-256 packing
# would not be. Values 0-31 take one character, 0-1023 two, 0-32767 three, 0-1048575 four; today's
# distribution lands at 330 / 436 / 425 / 103 of the 1,294.
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
INDEX = {c: i for i, c in enumerate(ALPHA)}


def encode(values) -> str:
    out = []
    for v in values:
        if v < 0:
            raise ValueError(f"negative value in a star sample: {v}")
        while True:
            low, v = v & 31, v >> 5
            out.append(ALPHA[low | (32 if v else 0)])
            if not v:
                break
    return "".join(out)


def decode(payload: str) -> list[int]:
    out, acc, shift = [], 0, 0
    for c in payload:
        i = INDEX[c]
        acc |= (i & 31) << shift
        if i & 32:
            shift += 5
        else:
            out.append(acc)
            acc, shift = 0, 0
    if shift:
        raise ValueError("truncated star sample: the last value has no terminating character")
    return out


def digest(roster: list[str], slots: int) -> str:
    """A fingerprint of the roster prefix a sample was written against.

    Four bytes, because this is a tripwire and not a signature: it exists to catch a hand-edit that sorted
    or spliced the roster, and any such edit changes the prefix wholesale rather than looking for a
    collision. Newline-joined so that two adjacent names cannot be run together into a third reading --
    `["a/b", "c"]` and `["a/bc"]` hash differently.
    """
    body = "\n".join(roster[:slots]).encode("utf-8")
    return hashlib.blake2b(body, digest_size=4).hexdigest()


# ------------------------------------------------------------------ the ledger file
def blank(day: str) -> dict:
    return {"schema": SCHEMA, "created": day, "period_days": PERIOD_DAYS, "repos": [], "samples": {}}


def load(path: Path) -> dict:
    """The ledger, or an empty one dated today. Missing keys are filled so an older file still loads."""
    if not path.exists():
        return blank(date.today().isoformat())
    state = json.loads(path.read_text(encoding="utf-8"))
    state.setdefault("schema", SCHEMA)
    state.setdefault("created", date.today().isoformat())
    state.setdefault("period_days", PERIOD_DAYS)
    state.setdefault("repos", [])
    state.setdefault("samples", {})
    return state


def save(state: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # `indent=1, sort_keys=True`, the same as `newness.py` and for the same reason: this file is committed
    # on every run that records, so the diff should be the one sample that was added and nothing else. One
    # roster entry per line and one sample per line is also what makes the file git's best case for delta
    # compression -- see the measurement in the docstring.
    path.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def days_between(a: str, b: str) -> int:
    """Whole days from ISO date `a` to ISO date `b`. Both are dates, so this cannot come out fractional."""
    return (datetime.fromisoformat(b[:10]).date() - datetime.fromisoformat(a[:10]).date()).days


# ------------------------------------------------------------------ recording
def snapshot_stars(data: dict) -> tuple[str, dict[str, int]]:
    """Today's counts out of `docs/data.json`, as (snapshot date, {nwo: stars}).

    The date is the snapshot's own, not the clock's. It is what the star counts in that file are a fact
    about, and keying the sample by it is what makes this stage idempotent -- see the docstring.
    """
    cols = data["cols"]
    nwo_at, star_at = cols.index("nwo"), cols.index("stars")
    return data["snapshot"], {r[nwo_at]: (r[star_at] or 0) for r in data["rows"] if r[nwo_at]}


def record(state: dict, day: str, stars: dict[str, int]) -> tuple[bool, str]:
    """Append one sample if the ledger wants one. Returns (recorded, why).

    The roster grows here and only here, and only by appending -- an index once handed out is that repo's
    for the life of the file, because every historical sample is positional against it.
    """
    roster: list[str] = state["repos"]
    known = {n: i for i, n in enumerate(roster)}
    added = [n for n in stars if n not in known]
    for n in added:
        known[n] = len(roster)
        roster.append(n)

    samples: dict[str, str] = state["samples"]
    if day in samples:
        return False, f"{day} is already in the ledger; nothing to record"
    last = max(samples) if samples else None
    if last:
        gap = days_between(last, day)
        if gap < 0:
            return False, f"{day} is older than the last sample {last}; refusing to record out of order"
        if gap < state["period_days"]:
            return False, (f"{day} is {gap} day(s) after {last}, inside the "
                           f"{state['period_days']}-day grid; nothing to record")

    # `stars + 1`, so that 0 is free to mean "in the roster, absent from this snapshot" -- a repo that has
    # dropped off every source list, which is a different fact from a repo with no stars.
    slots = len(roster)
    payload = encode([stars[n] + 1 if n in stars else 0 for n in roster])
    samples[day] = f"{slots}:{digest(roster, slots)}:{payload}"
    return True, (f"recorded {day}: {len(stars):,} of {slots:,} slots, "
                  f"{len(payload):,} bytes" + (f", {len(added):,} new slot(s)" if added else ""))


# ------------------------------------------------------------------ deriving
def read_samples(state: dict) -> tuple[dict[str, list[int]], list[str]]:
    """Every sample the roster still vouches for, decoded. Returns ({date: values}, [complaints]).

    A sample whose digest no longer matches the roster is dropped rather than used. It is the only failure
    mode of a positional file that produces plausible-looking wrong answers instead of an error, so it is
    checked on every read; the cost of being wrong here is 1,294 fabricated numbers.
    """
    roster = state["repos"]
    good, bad = {}, []
    for day, raw in state["samples"].items():
        try:
            slots_s, want, payload = raw.split(":", 2)
            slots = int(slots_s)
            values = decode(payload)
        except (ValueError, KeyError) as exc:
            bad.append(f"{day}: unreadable ({exc})")
            continue
        if len(values) != slots:
            bad.append(f"{day}: says {slots} slots, decodes to {len(values)}")
            continue
        if slots > len(roster):
            bad.append(f"{day}: {slots} slots against a roster of {len(roster)}")
            continue
        if digest(roster, slots) != want:
            bad.append(f"{day}: roster digest {want} does not match the first {slots} entries "
                       f"(the roster was reordered or spliced)")
            continue
        good[day] = values
        # `hits` is not recorded per sample on purpose: a sample is a fact about a day and stays readable
        # even when the roster has grown past it. Trailing slots simply are not in it.
    return good, bad


def pick(days: int, present: str, have: list[str]) -> tuple[str, int]:
    """The sample closest to `days` before `present`, within tolerance. ("", 0) if there is none.

    Nearest rather than oldest-within-range, so a ledger that does hold a sample of exactly the right age
    always uses it; ties break to the older one, so the span is never quietly understated.
    """
    tol = tolerance(days)
    scored = []
    for d in have:
        age = days_between(d, present)
        if days - tol <= age <= days + tol:
            scored.append((abs(age - days), -age, d, age))
    if not scored:
        return "", 0
    _, _, day, age = min(scored)
    return day, age


def derive(state: dict, data: dict) -> tuple[dict[str, dict[str, int]], dict, list[str]]:
    """Per-repo deltas and the metadata block. Returns ({nwo: {col: gain}}, velocity, [complaints]).

    The *present* end of every delta is `data.json`'s live count rather than the newest sample. Both are
    usually the same number, but on a run where the grid refused a sample they are not, and the live count
    is the one the rest of the page is showing -- so a reader can subtract the figures on their own screen
    and get the answer this stage gave them.
    """
    present, now = snapshot_stars(data)
    samples, complaints = read_samples(state)
    roster = state["repos"]
    slot = {n: i for i, n in enumerate(roster)}

    gains: dict[str, dict[str, int]] = {}
    velocity = {"to": present, "rise": {"col": "", "min_abs": 0, "min_pct": 0.0}}
    for col, days in WINDOWS:
        day, age = pick(days, present, list(samples))
        meta = {"days": days, "from": day, "span": age, "n": 0}
        velocity[col] = meta
        if not day:
            continue
        values = samples[day]
        for nwo, stars in now.items():
            i = slot.get(nwo)
            # Four separate ways to have no answer, all of which mean the same thing to the reader and
            # none of which may be reported as a zero: the repo has no slot at all, its slot postdates
            # this sample, or either end of the subtraction is not a count. `values[i] <= 1` is both of
            # the past-end cases at once -- 0 is "in the roster, absent from that snapshot" and 1 is the
            # stored form of zero stars, which the site itself prints as an em dash because it means
            # "this row is a folder inside somebody else's repo, or a dead link" rather than "unstarred".
            # Subtracting from it would turn a row that stopped being a dead link into a growth story.
            if i is None or i >= len(values) or values[i] <= 1 or not stars:
                continue
            gains.setdefault(nwo, {})[col] = stars - (values[i] - 1)
            meta["n"] += 1

    # The window the filter is allowed to use: the longer one when it exists, the shorter one while the
    # ledger is still filling, and nothing at all on the day this stage first runs. One field, so the page
    # has one thing to test and cannot end up offering a chip backed by a column that is empty.
    for col, _days in reversed(WINDOWS):
        if velocity[col]["n"]:
            span = velocity[col]["span"]
            velocity["rise"] = {
                "col": col,
                # Scaled from the per-30-day constants to the span this window really covers, and rounded
                # to whole stars and two decimal places so the number in the file is the number the page
                # applies -- a threshold the reader could not reproduce from the tooltip would be worse
                # than no tooltip.
                "min_abs": max(1, round(RISE_MIN_ABS * span / 30)),
                "min_pct": round(RISE_MIN_PCT * span / 30, 2),
            }
            break
    return gains, velocity, complaints


# ------------------------------------------------------------------ patching data.json
def patch(data: dict, gains: dict[str, dict[str, int]], velocity: dict) -> dict:
    """Add the two columns and the `velocity` block. Safe to run on a file that already has them.

    Appended to `cols` rather than inserted, and rows are padded to the new width, which is the shape
    `19b_refresh.py` already established for `first_seen`: a consumer that reads by `cols.index(name)`
    -- which is every consumer in this pipeline -- is unaffected by a column arriving at the end, and one
    that reads by position keeps reading the same positions.
    """
    cols = list(data["cols"])
    for col, _days in WINDOWS:
        if col not in cols:
            cols.append(col)
    nwo_at = cols.index("nwo")
    width = len(cols)
    for row in data["rows"]:
        while len(row) < width:
            row.append("")
        got = gains.get(row[nwo_at], {})
        for col, _days in WINDOWS:
            # `""` and never `0`. `data.json` has a stated no-nulls rule, and the whole point of this
            # column is that an absent figure is absent rather than a gain of nothing.
            row[cols.index(col)] = got.get(col, "")
    data["cols"] = cols
    data["velocity"] = velocity
    # The column set changed, which is exactly what `19_pages.py` documents `schema_version` as tracking.
    # `max`, not assignment: a future version 3 written upstream must not be walked back by this stage.
    data["schema_version"] = max(int(data.get("schema_version") or 1), 2)
    return data


# ------------------------------------------------------------------ reporting
def report(state: dict, data: dict, gains: dict, velocity: dict, complaints: list[str]) -> None:
    samples = state["samples"]
    print(f"ledger      {len(samples):,} sample(s) · {len(state['repos']):,} slots · "
          f"{state['period_days']}-day grid · created {state['created']}")
    if samples:
        first, last = min(samples), max(samples)
        print(f"            {first} .. {last} ({days_between(first, last)} days of history)")
    for c in complaints:
        print(f"  !! {c}")
    for col, days in WINDOWS:
        m = velocity[col]
        if m["from"]:
            print(f"{col:11s} {m['n']:,} of {len(data['rows']):,} rows · "
                  f"{m['from']} .. {velocity['to']} ({m['span']} days, nominal {days})")
        else:
            print(f"{col:11s} no sample {days - tolerance(days)}-{days + tolerance(days)} days old; "
                  f"absent on every row")
    rise = velocity["rise"]
    col = rise["col"]
    if not col:
        print("rise        no window has history yet; the chip and the sort option stay hidden")
        return
    star_at = data["cols"].index("stars")
    nwo_at = data["cols"].index("nwo")
    stars = {r[nwo_at]: r[star_at] or 0 for r in data["rows"]}
    vals = {n: g[col] for n, g in gains.items() if col in g}
    # The same arithmetic the page will do, on the same numbers the page will be given -- so this line is a
    # check that the emitted thresholds select a useful number of rows, not a second implementation of the
    # rule that could disagree with the first.
    hot = [n for n, v in vals.items()
           if v >= max(rise["min_abs"], rise["min_pct"] / 100 * stars.get(n, 0))]
    down = [n for n, v in vals.items() if v < 0]
    print(f"rise        on {col} · {len(hot):,} of {len(vals):,} row(s) clear "
          f"max({rise['min_abs']}, {rise['min_pct']}%)")
    for n in sorted(hot, key=lambda n: -vals[n])[:10]:
        print(f"  +{vals[n]:<7,} {n}  ({vals[n] / max(1, stars.get(n, 1)) * 100:.1f}%)")
    if down:
        # Stars really do go down, so this is printed rather than suppressed -- but a *lot* of them going
        # down at once is the signature of a bad fetch or a mass rename upstream, not of readers leaving.
        worst = min(down, key=lambda n: vals[n])
        print(f"            {len(down):,} row(s) went down over this window, worst "
              f"{vals[worst]:,} on {worst}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=LEDGER, help="the star-history file")
    ap.add_argument("--data", type=Path, default=SITE_DATA, help="the data.json to read and patch")
    ap.add_argument("--dry-run", action="store_true", help="derive and report; write nothing")
    ap.add_argument("--status", action="store_true", help="report the ledger only; record nothing")
    args = ap.parse_args()

    if not args.data.exists():
        raise SystemExit(f"{args.data} is not there. This stage runs after 19_pages.py, which writes it.")
    data = json.loads(args.data.read_text(encoding="utf-8"))
    state = load(args.ledger)

    if not args.status:
        day, stars = snapshot_stars(data)
        ok, why = record(state, day, stars)
        print(f"{'++' if ok else '=='} {why}")
        if ok and not args.dry_run:
            save(state, args.ledger)

    gains, velocity, complaints = derive(state, data)
    report(state, data, gains, velocity, complaints)

    if args.status or args.dry_run:
        print("(nothing written)")
        return

    patch(data, gains, velocity)
    args.data.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"{args.ledger.name:11s} {args.ledger.stat().st_size / 1024:8.1f} KB")
    print(f"{args.data.name:11s} {args.data.stat().st_size / 1024:8.1f} KB · "
          f"schema_version {data['schema_version']}")


if __name__ == "__main__":
    main()
