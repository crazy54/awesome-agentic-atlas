"""Unit tests for `scripts/signals.py` -- the whole of JFH-211 that can be checked offline.

The three stages this module serves all shell out to `gh api graphql`, so the fetch path cannot be
exercised without a token and a network. That is the reason the decision is a pure function: a cache,
an nwo, a `pushedAt`, a `now`, and no I/O, which is testable on fabricated inputs from a cold
checkout. What is asserted here is the whole of the policy. What is not asserted anywhere is that
GitHub answers the queries or that CI's cache volume contains what we think it does, and no test in
this repository can say otherwise.

Five groups:

  the readers        -- `meta_push`, `recorded_push`, `recorded_fetch`, `parse_stamp` on every shape
                        that has ever been in these files, including the ones that are not timestamps.
  the decision       -- each term of `reason()` at its boundaries: the push inequality, the CI-upload
                        race, the age ceiling, and the three ways an entry can fail to say enough.
  the file shapes    -- that a `cache/*.json` written under any earlier schema loads, reads as stale,
                        and does not read as a bare truthy dict. This is the migration, and it happens
                        on files nobody can inspect in CI because `cache/` is gitignored.
  what gets written  -- that both stamps are written together and that the classifiers can still read
                        the entry afterwards.
  the call sites     -- that the three stages consult it, stamp what they write, and no longer queue on
                        presence. Textual, deliberately: the failure this ticket is about is a queue
                        that quietly stops asking, and that failure exits 0 everywhere else.

Run: python tests/signals_test.py
"""
from __future__ import annotations

import io
import json
import sys
import tokenize
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
import signals as sig  # noqa: E402


def code_only(path: Path) -> str:
    """A stage's source with every comment and string literal blanked out.

    The last group asserts on the *absence* of the old presence-only rule, and the first draft of that
    failed on three files which no longer contain the rule -- they contain a comment saying they used
    to. A tripwire that cannot tell code from prose about code has to be either wrong or silent, and it
    would make the honest thing, documenting the fix beside it, the thing that breaks the build.
    `tokenize` is stdlib and knows the difference.
    """
    src = path.read_text(encoding="utf-8")
    # Blanked in place rather than dropped, so line and column positions survive and a substring
    # search still sees `sig.reason(` written the way the file writes it.
    grid = [list(line) for line in src.splitlines(keepends=True)]
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type not in (tokenize.COMMENT, tokenize.STRING):
            continue
        (srow, scol), (erow, ecol) = tok.start, tok.end
        for row in range(srow, erow + 1):
            chars = grid[row - 1]
            lo = scol if row == srow else 0
            hi = ecol if row == erow else len(chars)
            for i in range(lo, min(hi, len(chars))):
                if chars[i] != "\n":
                    chars[i] = " "
    return "".join("".join(chars) for chars in grid)


ok = bad = 0


def check(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, got) -> None:
    check(name, bool(got), True)


def false(name: str, got) -> None:
    check(name, bool(got), False)


def safe(fn, *args):
    """`fn(*args)`, or a description of what it raised.

    Every reader in `signals.py` documents that a shape it cannot understand is a verdict and not an
    error: a malformed entry re-queries one repo, where an exception would stop a crawl of 1,294. So
    "does not raise" is one of the claims under test, and a claim under test should be reported as a
    failure rather than take the rest of the file down with it -- an exception here would swallow
    every assertion after it and print no tally at all.
    """
    try:
        return fn(*args)
    except Exception as exc:  # noqa: BLE001 -- the breadth is the point
        return f"raised {type(exc).__name__}: {exc}"


NOW = datetime(2026, 9, 6, 12, 0, 0, tzinfo=timezone.utc)
HOUR = timedelta(hours=1)


def at(**delta) -> str:
    """A stamp that many days/hours/seconds before NOW."""
    return sig.stamp(NOW - timedelta(**delta))


def rel(pushed: str, fetched: str, **kw) -> dict:
    """A releases.json entry as the stages now write it."""
    return {"tags": ["v1.0.0"], "assets": ["app-windows-x64.zip"],
            sig.STAMP: pushed, sig.FETCHED: fetched, **kw}


def why(entry, pushed: str, now: datetime = NOW) -> str:
    """`reason` for a single fabricated entry, and a check that `stale` agrees with it.

    Every case below goes through here, so the two functions cannot drift apart: `stale` is the
    boolean the module documents and `reason` is what the stages call, and a term added to one and not
    the other would be invisible to a test that only asked one of them.
    """
    code = safe(sig.reason, {"a/b": entry}, "a/b", pushed, now)
    check(f"stale agrees with reason ({code})", safe(sig.stale, {"a/b": entry}, "a/b", pushed, now),
          code != sig.FRESH)
    return code


# ------------------------------------------------------------------ 1. the readers
check("meta_push reads the live value", sig.meta_push({"a/b": {"pushedAt": "2026-09-05T01:02:03Z"}},
                                                     "a/b"), "2026-09-05T01:02:03Z")
check("meta_push of an unknown repo is empty", sig.meta_push({}, "a/b"), "")
check("meta_push of a null metadata entry is empty", sig.meta_push({"a/b": None}, "a/b"), "")
check("meta_push of metadata with no pushedAt is empty", sig.meta_push({"a/b": {}}, "a/b"), "")
check("meta_push of a null pushedAt is empty", sig.meta_push({"a/b": {"pushedAt": None}}, "a/b"), "")

check("recorded_push reads the stamp", safe(sig.recorded_push, {sig.STAMP: "x"}), "x")
check("recorded_push of a dict without it", safe(sig.recorded_push, {"tags": []}), None)
check("recorded_push of a non-string stamp", safe(sig.recorded_push, {sig.STAMP: 1757160000}), None)
check("recorded_push of a legacy True", safe(sig.recorded_push, True), None)
check("recorded_push of a legacy False", safe(sig.recorded_push, False), None)
check("recorded_push of nothing at all", safe(sig.recorded_push, None), None)
check("recorded_fetch reads the stamp", safe(sig.recorded_fetch, {sig.FETCHED: "y"}), "y")
check("recorded_fetch of the shipped push-only shape", safe(sig.recorded_fetch, {sig.STAMP: "x"}), None)
check("recorded_fetch of a non-string stamp", safe(sig.recorded_fetch, {sig.FETCHED: 0}), None)
check("recorded_fetch of a legacy bool", safe(sig.recorded_fetch, True), None)
check("the two stamps are different keys", sig.STAMP == sig.FETCHED, False)

# Every spelling that reaches these caches. GraphQL sends `Z`; a naive value, an explicit offset and
# fractional seconds all arrive from hand edits and from other producers in this pipeline.
base = datetime(2026, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
for label, text in (("Z", "2026-09-01T12:00:00Z"), ("lowercase z", "2026-09-01t12:00:00z"),
                    ("+00:00", "2026-09-01T12:00:00+00:00"), ("naive", "2026-09-01T12:00:00"),
                    ("microseconds", "2026-09-01T12:00:00.123456Z")):
    got = sig.parse_stamp(text)
    true(f"parse_stamp({label}) is aware UTC", got is not None and got.tzinfo is not None)
    check(f"parse_stamp({label}) is the same instant", got and got.replace(microsecond=0), base)
check("parse_stamp compares across offsets", sig.parse_stamp("2026-09-01T14:00:00+02:00"), base)
for label, value in (("None", None), ("empty", ""), ("blank", "   "), ("prose", "last tuesday"),
                     ("a number", 20260901), ("a dict", {"pushedAt": "2026-09-05"}),
                     ("a list", []), ("a bool", True)):
    check(f"parse_stamp rejects {label}", sig.parse_stamp(value), None)
check("stamp() is second-resolution UTC with a Z",
      sig.stamp(datetime(2026, 1, 2, 3, 4, 5, 678901, tzinfo=timezone.utc)), "2026-01-02T03:04:05Z")
check("stamp() normalises an offset to UTC",
      sig.stamp(datetime(2026, 1, 2, 5, 4, 5, tzinfo=timezone(timedelta(hours=2)))),
      "2026-01-02T03:04:05Z")
check("stamp() round-trips through parse_stamp", sig.parse_stamp(sig.stamp(NOW)), NOW)
true("utcnow() is aware UTC", sig.utcnow().tzinfo is not None)

# ------------------------------------------------------------------ 2. absent, and the legacy shapes
check("an empty cache queues everything", sig.reason({}, "a/b", at(days=1), NOW), sig.ABSENT)
check("a cache holding other repos still queues this one",
      sig.reason({"c/d": rel(at(days=1), at(days=1))}, "a/b", at(days=1), NOW), sig.ABSENT)
# A null value *present* in the cache is not absent -- it is an entry that says nothing.
check("a null entry is unstamped, not absent", why(None, at(days=1)), sig.UNSTAMPED)
for label, entry in (("releases entry", {"tags": ["v1"], "assets": ["a.zip"]}),
                     ("releases entry, empty", {"tags": [], "assets": []}),
                     ("actions entry, true", True),
                     ("actions entry, false", False),
                     ("a stamp that is not a string", {"assets": [], sig.STAMP: 1757160000})):
    check(f"pre-stamp {label} -> unstamped", why(entry, at(days=1)), sig.UNSTAMPED)

# The shape their commit ships: a push stamp and no fetch stamp. The push has not moved, so the push
# term says nothing, and the entry must still read as stale rather than as fresh -- otherwise the two
# new terms below could never be reached by any entry written before this change.
pushed_only = {"tags": [], "assets": [], sig.STAMP: at(days=3)}
check("a push-stamped entry with no fetch stamp -> unfetched", why(pushed_only, at(days=3)),
      sig.UNFETCHED)
check("...and an actions entry likewise", why({"is_action": True, sig.STAMP: at(days=3)}, at(days=3)),
      sig.UNFETCHED)
check("...and a fetch stamp that is not a string likewise",
      why({"assets": [], sig.STAMP: at(days=3), sig.FETCHED: 0}, at(days=3)), sig.UNFETCHED)
check("...and a fetch stamp that is not a timestamp likewise",
      why({"assets": [], sig.STAMP: at(days=3), sig.FETCHED: "soon"}, at(days=3)), sig.UNFETCHED)

# ------------------------------------------------------------------ 3. the push term, untouched
# Inequality, not "newer than": a force-push that rewrote history moves `pushedAt` backwards and the
# signals can have changed just as much. So both directions queue, and only equality does not.
was = at(days=3)
check("the recorded push still matching -> not the push term",
      why(rel(was, at(days=2)), was) == sig.PUSHED, False)
check("pushed one second later -> pushed",
      why(rel(was, at(days=2)), sig.stamp(NOW - timedelta(days=3) + timedelta(seconds=1))),
      sig.PUSHED)
check("pushed one second earlier -> pushed too, because history was rewritten",
      why(rel(was, at(days=2)), at(days=3, seconds=1)), sig.PUSHED)
check("pushed today over an entry from last week -> pushed",
      why(rel(at(days=7), at(days=7)), at(hours=1)), sig.PUSHED)
# Two repos that never carried a `pushedAt` at all compare equal and so do not churn.
check("no push time either side -> not the push term", why(rel("", at(days=2)), "") == sig.PUSHED,
      False)
check("no push time now, one recorded before -> pushed", why(rel(was, at(days=2)), ""), sig.PUSHED)
check("a push time now, none recorded before -> pushed", why(rel("", at(days=2)), was), sig.PUSHED)
# An unreadable live value must not raise and must not be able to make an entry fresh by accident.
for label, live in (("a number", 20260901), ("a dict", {"pushedAt": was}), ("None", None)):
    check(f"an unreadable live pushedAt ({label}) falls through, it does not raise",
          why(rel(was, at(days=2)), live), sig.PUSHED)

# ------------------------------------------------------------------ 4. the CI upload race
# The gap the push term cannot see. A tag push moves `pushedAt` at once and the release job attaches
# the binaries minutes later; an entry written between the two saw the new push and no assets, and
# from then on `recorded_push == meta_push` for ever.
check("the grace window is 6 hours", sig.CI_GRACE_HOURS, 6)
tag = at(days=2)
tagged = NOW - timedelta(days=2)
for label, fetched, expected in (
    ("in the same second as the push", tag, sig.CI_RACE),
    ("a minute after the push", sig.stamp(tagged + timedelta(minutes=1)), sig.CI_RACE),
    ("an hour after the push", sig.stamp(tagged + HOUR), sig.CI_RACE),
    ("one second inside the window", sig.stamp(tagged + 6 * HOUR - timedelta(seconds=1)), sig.CI_RACE),
    ("exactly on the window", sig.stamp(tagged + 6 * HOUR), sig.FRESH),
    ("one second past the window", sig.stamp(tagged + 6 * HOUR + timedelta(seconds=1)), sig.FRESH),
    ("a day after the push", sig.stamp(tagged + 24 * HOUR), sig.FRESH),
    ("a second before the push", sig.stamp(tagged - timedelta(seconds=1)), sig.FRESH),
):
    check(f"release entry fetched {label} -> {expected}", why(rel(tag, fetched), tag), expected)

# One-shot, which is the whole cost argument: re-querying a raced entry writes a `fetched_at` outside
# the window, so the term cannot queue the same repo twice.
raced = rel(tag, sig.stamp(tagged + timedelta(minutes=1)))
check("a raced entry is queued", why(raced, tag), sig.CI_RACE)
requeried = {**raced, **sig.observed(tag, NOW)}
check("...and its re-query settles it", why(requeried, tag), sig.FRESH)

# Restricted to release entries. An `action.yml` cannot appear or disappear without a push, so an
# actions entry is complete the instant it is written and a window on it would be pure cost.
check("an actions entry fetched a minute after the push is fresh",
      why(sig.action_entry(True, tag, tagged + timedelta(minutes=1)), tag), sig.FRESH)
check("an actions entry fetched in the same second as the push is fresh",
      why(sig.action_entry(False, tag, tagged), tag), sig.FRESH)
# Detected by the shape of the entry, not by which stage wrote it: two stages write releases.json.
check("an entry with assets and nothing else is still treated as a release entry",
      why({"assets": [], sig.STAMP: tag, sig.FETCHED: tag}, tag), sig.CI_RACE)
check("an entry with tags but no assets is not", why({"tags": [], sig.STAMP: tag, sig.FETCHED: tag},
                                                     tag), sig.FRESH)
# Nothing to measure the window from. A repo with no push time cannot have a push to race, and the
# term must decline rather than divide by an absent date.
check("a release entry with no push time is not raced", why(rel("", at(hours=1)), ""), sig.FRESH)
check("a release entry with an unreadable push time is not raced",
      why(rel("whenever", at(hours=1)), "whenever"), sig.FRESH)

# ------------------------------------------------------------------ 5. the age ceiling
check("the backstop is 30 days", sig.MAX_AGE_DAYS, 30)
# Pushed long before any of the fetch times below, so the race window cannot also be in play: an
# entry fetched in the same second as its push is a raced entry whatever its age, and the first draft
# of this table accidentally built one.
old_push = at(days=500)
for days, expected in ((29.5, sig.FRESH), (30.0, sig.FRESH), (31.0, sig.BACKSTOP),
                       (400.0, sig.BACKSTOP)):
    check(f"an entry fetched {days}d ago, unpushed since -> {expected}",
          why(rel(old_push, at(days=days)), old_push), expected)
# One second past the boundary, which is where an off-by-one in the comparison hides.
check("an entry fetched 30d and 1s ago -> backstop",
      why(rel(old_push, at(days=30, seconds=1)), old_push), sig.BACKSTOP)
check("an entry fetched 30d less 1s ago -> fresh",
      why(rel(old_push, sig.stamp(NOW - timedelta(days=30) + timedelta(seconds=1))), old_push),
      sig.FRESH)
# An entry with no readable push time at all still ages out -- that is the case the ceiling exists
# for, since no other term can ever fire on it.
check("an unstampable-push entry still ages out", why(rel("", at(days=90)), ""), sig.BACKSTOP)
check("a legacy actions entry aged out is reported as unstamped, not as the backstop",
      why(True, old_push), sig.UNSTAMPED)
# Both terms can hold at once. The earlier one is what gets reported, because a run log that says
# `backstop` when the entry was raced would send a reader to the wrong term.
check("raced and also older than the ceiling -> reported as the race",
      why(rel(at(days=90), sig.stamp(NOW - timedelta(days=90) + HOUR)), at(days=90)), sig.CI_RACE)

# ------------------------------------------------------------------ 6. genuinely fresh
check("pushed last week, fetched yesterday, well clear of both windows",
      why(rel(at(days=7), at(days=1)), at(days=7)), sig.FRESH)
check("an entry stamped by observed() right now is fresh", why({"assets": [], **sig.observed(was, NOW)},
                                                               was), sig.FRESH)
# A stamp from the future is a clock that disagreed, not an entry to churn on. `now - fetched` goes
# negative, which must not read as "older than 30 days" or as a race.
check("a fetch stamp two days in the future does not churn",
      why(rel(at(days=5), sig.stamp(NOW + timedelta(days=2))), at(days=5)), sig.FRESH)
check("a fetch stamp a year in the future does not churn",
      why(rel(at(days=5), sig.stamp(NOW + timedelta(days=365))), at(days=5)), sig.FRESH)
# `now` defaults to the wall clock, which is what keeps their three-argument call sites valid.
fresh_now = {"a/b": {"assets": [], **sig.observed("2026-09-05T00:00:00Z")}}
false("stale() with no clock argument reads a just-written entry as fresh",
      sig.stale(fresh_now, "a/b", "2026-09-05T00:00:00Z"))
true("stale() with no clock argument still sees a moved push",
     sig.stale(fresh_now, "a/b", "2026-09-06T00:00:00Z"))
check("reason() with no clock argument agrees", sig.reason(fresh_now, "a/b", "2026-09-05T00:00:00Z"),
      sig.FRESH)

# ------------------------------------------------------------------ 7. what gets written
w = sig.observed("2026-09-05T09:00:00Z", NOW)
check("observed() records the push it saw", w.get(sig.STAMP), "2026-09-05T09:00:00Z")
check("observed() records when it looked", w.get(sig.FETCHED), "2026-09-06T12:00:00Z")
check("observed() writes exactly the two stamps", sorted(w), sorted([sig.STAMP, sig.FETCHED]))
entry = {"tags": ["v2"], "assets": ["x.msi"], **sig.observed("2026-09-05T09:00:00Z", NOW)}
check("splatting observed() keeps tags", entry["tags"], ["v2"])
# The key `04_classify.classify()` reads. It does `rel.get("assets")`, so the added stamps are inert
# -- but only as long as they are added keys and not a new top level.
check("a stamped releases entry still answers .get('assets')", entry.get("assets"), ["x.msi"])
check("a stamped releases entry still answers .get('tags')", entry.get("tags"), ["v2"])

a_yes, a_no = sig.action_entry(True, "2026-09-05T09:00:00Z", NOW), sig.action_entry(False, "", NOW)
check("action_entry(True) records the verdict", a_yes["is_action"], True)
check("action_entry(False) records the verdict", a_no["is_action"], False)
check("action_entry records the push it saw", a_yes.get(sig.STAMP), "2026-09-05T09:00:00Z")
check("action_entry records when it looked", a_yes.get(sig.FETCHED), "2026-09-06T12:00:00Z")
check("action_entry coerces a truthy non-bool", sig.action_entry(["action.yml"], "", NOW)["is_action"],
      True)
check("is_action reads the current shape, true", sig.is_action(a_yes), True)
check("is_action reads the current shape, false", sig.is_action(a_no), False)
check("is_action reads the legacy shape, true", sig.is_action(True), True)
check("is_action reads the legacy shape, false", sig.is_action(False), False)
check("is_action reads a missing entry as false", sig.is_action(None), False)
# The assertion the dict schema turns on. `bool(a_no)` is True, because a non-empty dict is; a reader
# that kept doing `acts.get(nwo, False)` would classify all 1,294 repos as GitHub Actions, and nothing
# would raise. The two new keys make that dict bigger, not less truthy.
check("the raw current-shape entry is truthy even when the verdict is no", bool(a_no), True)
check("is_action disagrees with bool() on exactly that entry", sig.is_action(a_no) != bool(a_no), True)

# The log breakdown, which is how a term is falsifiable in production rather than only here.
check("breakdown of an empty queue says nothing", sig.breakdown([]), "")
check("breakdown ignores fresh repos", sig.breakdown([sig.FRESH, sig.FRESH]), "")
check("breakdown counts and orders the terms",
      sig.breakdown([sig.BACKSTOP, sig.PUSHED, sig.CI_RACE, sig.PUSHED, sig.ABSENT]),
      " (absent 1, pushed 2, ci-race 1, backstop 1)")
check("breakdown reports a code it does not know about", sig.breakdown(["something-new"]),
      " (something-new 1)")
check("the codes are all distinct",
      len({sig.ABSENT, sig.UNSTAMPED, sig.PUSHED, sig.UNFETCHED, sig.CI_RACE, sig.BACKSTOP,
           sig.FRESH}), 7)

# ------------------------------------------------------------------ 8. the files on disk load
# `cache/` is gitignored -- 64 MB of other people's READMEs -- so every schema change here is one extra
# crawl and not a data conversion. What must hold is that the files already on the Actions cache volume
# load and that every entry in them reads as stale. Fabricated at the exact shape those files have,
# round-tripped through JSON so nothing but JSON types can reach the readers.
legacy_rel = json.loads(json.dumps({
    "openai/codex": {"tags": ["rust-v0.5.0"], "assets": ["codex-x86_64-pc-windows-msvc.zip"]},
    "some/repo": {"tags": [], "assets": []},
}))
legacy_act = json.loads(json.dumps({"actions/checkout": True, "some/repo": False}))
shipped_rel = json.loads(json.dumps({
    "openai/codex": {"tags": ["rust-v0.5.0"], "assets": ["codex.zip"], sig.STAMP: at(days=1)},
    "some/repo": {"tags": [], "assets": [], sig.STAMP: at(days=1)},
}))

live = {k: at(days=1) for k in list(legacy_rel) + list(legacy_act) + list(shipped_rel)}
check("every entry of a pre-stamp releases file is stale",
      [safe(sig.reason, legacy_rel, k, live[k], NOW) for k in legacy_rel], [sig.UNSTAMPED] * 2)
check("every entry of a pre-stamp actions file is stale",
      [safe(sig.reason, legacy_act, k, live[k], NOW) for k in legacy_act], [sig.UNSTAMPED] * 2)
check("every entry of the shipped push-only releases file is stale",
      [safe(sig.reason, shipped_rel, k, live[k], NOW) for k in shipped_rel], [sig.UNFETCHED] * 2)
check("a pre-stamp actions file still reads its verdicts",
      {k: sig.is_action(v) for k, v in legacy_act.items()},
      {"actions/checkout": True, "some/repo": False})
check("a pre-stamp releases file still reads its assets", legacy_rel["openai/codex"].get("assets"),
      ["codex-x86_64-pc-windows-msvc.zip"])
# And a half-migrated file, which is what exists between one fixed run and its successor: a stage that
# dies partway through has written some entries and not others, and one that was interrupted mid-crawl
# is the normal state of a six-hour GitHub Actions job.
mixed = {"old/one": True,
         "new/one": sig.action_entry(True, at(days=9), NOW - timedelta(days=1)),
         "old/two": {"tags": [], "assets": []},
         "shipped/one": {"tags": [], "assets": [], sig.STAMP: at(days=9)},
         "new/two": {"tags": [], "assets": [], **sig.observed(at(days=9), NOW - timedelta(days=1))}}
check("a half-migrated file splits stale from fresh correctly",
      {k: safe(sig.stale, mixed, k, at(days=9), NOW) for k in mixed},
      {"old/one": True, "old/two": True, "shipped/one": True, "new/one": False, "new/two": False})
# Nothing above raised, and that is itself the backward-compatibility claim.
true("no earlier shape raises", True)

# ------------------------------------------------------------------ 9. the call sites still consult it
# Textual, and that is the point: this goes red if somebody reinstates a presence-only queue or writes
# an entry without a fetch stamp. Three separate implementations of the same loop, so all three are
# checked rather than one being taken as evidence about the others.
STAGES = ("03_releases.py", "03b_actions.py", "13_signals_all.py")
for name in STAGES:
    src = code_only(SCRIPTS / name)
    true(f"{name} imports signals", "import signals" in src)
    true(f"{name} asks signals why", "sig.reason(" in src)
    true(f"{name} reads one clock for the run", "sig.utcnow()" in src)
    true(f"{name} passes that clock to the decision", "], now)" in src or ", now)" in src)
    true(f"{name} stamps what it writes", "sig.observed(" in src or "sig.action_entry(" in src)
    true(f"{name} prints which term queued each repo", "sig.breakdown(" in src)
    # Both stamps or neither. A write site that spells out the push stamp by hand is one that has
    # dropped the fetch stamp, and an entry with a push stamp and no fetch stamp is stale for ever.
    false(f"{name} never writes the push stamp on its own", "sig.STAMP:" in src)
    # The old rule, in the three spellings these files used. Its absence is the fix.
    false(f"{name} no longer queues on presence alone",
          "not in rel" in src or "not in act" in src or "not in out" in src)

for name in ("04_classify.py", "14_classify_all.py"):
    src = code_only(SCRIPTS / name)
    true(f"{name} reads the action verdict through is_action", "sig.is_action(" in src)
    # Every read of the actions cache, not merely one of them. Counted rather than pattern-matched
    # because the failure this guards against is a *second* reader added later beside the right one.
    check(f"{name} routes every acts.get through is_action",
          src.count("sig.is_action(acts.get("), src.count("acts.get("))
    true(f"{name} reads the actions cache at all", src.count("acts.get(") > 0)

# Standard library only, everywhere this ticket touched. The repository has no dependencies and no
# build step, and this is the file that would notice first.
THIRD_PARTY = ("requests", "httpx", "dateutil", "pydantic", "arrow", "pendulum", "yaml", "numpy")
for name in STAGES + ("signals.py", "04_classify.py", "14_classify_all.py"):
    src = code_only(SCRIPTS / name)
    hits = [m for m in THIRD_PARTY if f"import {m}" in src or f"from {m}" in src]
    check(f"{name} imports nothing third-party", hits, [])

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
