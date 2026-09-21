"""Unit tests for the cohort model in `scripts/newness.py`.

`New` on this site means one thing and it is not the obvious thing: not "arrived recently", but "arrived in
the most recent import that brought anything". One cohort wears the mark, the next import that adds a repo
takes it off them, and an import that adds nothing leaves it exactly where it was. That rule is four lines of
`resolve()` and it decides what four surfaces publish -- the homepage chip and outline, the Markdown mega
list's header, the refreshed page, and the count in both feeds -- so it is worth a harness of its own.

Nothing else in this suite can see it. The browser harnesses read the *committed* `docs/`, which was built by
whatever the generator said at the time; `refresh_test.py` feeds `19b_refresh` a hand-written ledger and never
exercises the transitions. And the transitions are the whole feature: a cohort is only correct in relation to
the one before it, so every interesting assertion needs at least two imports in sequence. This file runs them
against a ledger in a scratch directory, several builds deep, with the date supplied rather than read from the
clock -- the stale bound is a fortnight, and a test that waited for it would take a fortnight.

Six groups:

  bootstrap   -- a clone with no ledger. Every repo is founding stock, dated to the baseline, and *nothing*
                 is New; the alternative is a first run that marks the entire atlas. Also that an explicit
                 earlier `day` bootstraps a baseline on that day rather than on today, which is a bug this
                 file found: `load()` dates an absent ledger from the clock, and a baseline in the build's
                 own future makes `cohort()` suppress every cohort that build goes on to create.
  transitions -- the rule itself. The first import that adds becomes the cohort; the next one that adds
                 supersedes it and the previous arrivals lose the mark while keeping their dates; an import
                 that adds nothing changes neither.
  the dodge   -- that a source list read for the first time is a real cohort. An earlier version stamped
                 those repos at the baseline to keep a bulk ingest from marking 85% of the atlas, and that
                 dodge silently swallowed genuine arrivals on any build that did both at once. Its absence
                 is the single most consequential behaviour here, so it is asserted directly.
  stale bound -- `WINDOW` is no longer a definition of New; it is the bound on how long an un-superseded
                 cohort may go on claiming to be the latest news. Asserted on both sides of the boundary,
                 which is inclusive.
  the map     -- `SEEN` is deliberately wider than the marked set: every post-baseline arrival, because the
                 page prints a date on each of them and counts "since your last visit" across cohorts.
  the ledger  -- what lands on disk. Committed on every run that adds a repo, so the diff has to be the
                 repos that arrived: sorted keys, one per line, trailing newline, and re-running a build
                 that adds nothing writes nothing at all.

Standard library only, and it imports `newness` alone -- no stage, no `openpyxl`, no crawl cache. It writes
nowhere but its own temp directory: `newness.PATH` is repointed before the first call, so a broken rule cannot
reach the committed `state/first-seen.json`.

Run: python tests/newness_test.py
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# The mark is U+2728, and a Windows console is cp1252, which cannot encode it. Every other harness gets away
# without this because none of them has a non-Latin-1 character in a fixture; here the character *is* the
# subject, and without this line a genuine failure is reported as a UnicodeEncodeError in the reporter rather
# than as the assertion that failed -- which is the one moment this file has to be legible.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec = importlib.util.spec_from_file_location("newness_for_test", SCRIPTS / "newness.py")
n = importlib.util.module_from_spec(spec)
sys.modules["newness_for_test"] = n
spec.loader.exec_module(n)

# Under `run.mjs` this lands inside the run's own scratch root, swept on the way out however the run ended.
TMP = Path(tempfile.mkdtemp(prefix="newness_test_", dir=os.environ.get("AAA_TMP") or None))
n.PATH = TMP / "first-seen.json"

ok = bad = 0


def eq(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def resolve(nwos, day, sources=None) -> dict[str, str]:
    """`resolve` with its log swallowed. The log is prose for a build, and one group below asserts on it."""
    with redirect_stdout(io.StringIO()):
        return dict(n.resolve(nwos, day=day, sources=sources))


def log(nwos, day, sources=None) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        n.resolve(nwos, day=day, sources=sources)
    return buf.getvalue()


def marked() -> list[str]:
    """The set wearing the mark, read the way the Markdown surface reads it rather than from the ledger."""
    return sorted(k for k in n.SEEN if n.mark(k))


def reset() -> None:
    """Back to a clone with no ledger. Every group below starts from one."""
    if n.PATH.exists():
        n.PATH.unlink()
    n.SEEN.clear()
    n.COHORT = ""


# ---- bootstrap: a clone that has never had a ledger marks nothing
reset()
resolve(["a/1", "a/2", "a/3"], day="2026-09-01")
state = json.loads(n.PATH.read_text(encoding="utf-8"))
eq("a bootstrap marks nothing New", n.COHORT, "")
eq("...and leaves SEEN empty", dict(n.SEEN), {})
eq("...and dates every repo to the baseline", sorted(set(state["repos"].values())), ["2026-09-01"])
eq("...at the day the build passed, not the day the clock says",
   state["baseline"], "2026-09-01")
eq("...with the cohort initialised to the baseline, which is what means 'nothing yet'",
   state["cohort"], state["baseline"])
eq("...and the stale bound written down for the page to re-apply", state["window_days"], n.WINDOW)
eq("a cohort sitting on the baseline is no cohort", n.cohort(state, day="2026-09-01"), "")
eq("mark() says nothing about founding stock", n.mark("a/1"), "")
eq("mark() says nothing about a repo it has never heard of", n.mark("nobody/nothing"), "")

# ---- transitions: the rule the whole feature rests on
first = resolve(["a/1", "a/2", "a/3", "b/1", "b/2"], day="2026-09-05")
eq("the first import that adds becomes the cohort", n.COHORT, "2026-09-05")
eq("...and only its arrivals are marked", marked(), ["b/1", "b/2"])
eq("...with the date in the mark", n.mark("b/1"), " ✨ <sub>Added 09/05/26</sub>")
eq("...and founding stock still unmarked", n.mark("a/3"), "")
eq("SEEN is the arrivals, keyed to their dates", first, {"b/1": "2026-09-05", "b/2": "2026-09-05"})

second = resolve(["a/1", "b/1", "b/2", "c/1"], day="2026-09-09")
eq("the next import that adds supersedes the cohort", n.COHORT, "2026-09-09")
eq("...so last time's arrivals lose the mark", n.mark("b/1"), "")
eq("...and this time's have it", marked(), ["c/1"])
eq("...while the superseded dates are kept, not rewritten", second["b/1"], "2026-09-05")
true("...which is what lets the page still print when they arrived",
     n.pretty(second["b/1"]) == "09/05/26", n.pretty(second["b/1"]))

# A repo that drops off a source list and comes back is not new -- it returned. Same ledger date, no mark.
third = resolve(["a/1", "b/1", "b/2", "c/1"], day="2026-09-11")
eq("an import that adds nothing leaves the cohort alone", n.COHORT, "2026-09-09")
eq("...and leaves the marks alone with it", marked(), ["c/1"])
eq("...and re-stamps nobody", third, second)
eq("a repo that left a list and came back keeps its first date", third["b/1"], "2026-09-05")

# ---- the dodge that is gone: a first-time source list is a real cohort, not founding stock
fourth = resolve(["a/1", "b/1", "c/1", "d/1", "d/2", "d/3"], day="2026-09-14",
                 sources=["owner/a-list-we-have-never-read"])
eq("a source list read for the first time is a real cohort", n.COHORT, "2026-09-14")
eq("...and the repos it brought are the marked set", marked(), ["d/1", "d/2", "d/3"])
eq("...dated to the import, not back-dated to the baseline", fourth["d/1"], "2026-09-14")
eq("...and the cohort it replaced is unmarked", n.mark("c/1"), "")
text = log(["a/1", "b/1", "c/1", "d/1", "e/1"], day="2026-09-15",
           sources=["owner/a-list-we-have-never-read", "owner/another-new-one"])
true("the log distinguishes a newly-read list from a steady-state arrival",
     "read for the first time" in text, text)
true("...and says the mark is temporary", "supersedes" in text, text)
true("...and says what kind of new it is", "not new in the world" in text, text)
steady = log(["a/1", "b/1", "c/1", "d/1", "e/1", "f/1"], day="2026-09-16")
true("a steady-state import says the previous cohort stops being marked",
     "stops being marked" in steady, steady)

# ---- the stale bound: WINDOW bounds a cohort's claim, it does not define New
state = n.load()
eq("the cohort survives the last day of the window", n.cohort(state, day="2026-09-30"), "2026-09-16")
eq("...and is stale the day after", n.cohort(state, day="2026-10-01"), "")
eq("...which is exactly WINDOW days", (30 - 16) + (n.WINDOW - 14), n.WINDOW)
eq("a cohort dated in the future is not live either", n.cohort(state, day="2026-09-15"), "")
eq("within() is inclusive at both ends",
   [n.within("2026-09-16", "2026-09-16"), n.within("2026-09-16", "2026-09-30"),
    n.within("2026-09-16", "2026-10-01")], [True, True, False])
eq("a junk date is old rather than a traceback", n.within("not-a-date", "2026-09-16"), False)
eq("an empty date is not inside anything", n.within("", "2026-09-16"), False)
# The stale case has to leave the *dates* alone: the page still prints them and the feeds still publish them.
# Only the mark expires.
n.COHORT = n.cohort(state, day="2026-10-01")
eq("nothing is marked once the cohort is stale", marked(), [])
true("...but every arrival still has its date", all(n.SEEN.values()), dict(n.SEEN))

# ---- the map: SEEN is wider than the marked set, on purpose
n.COHORT = n.cohort(state, day="2026-09-16")
eq("SEEN spans every cohort since the baseline",
   sorted(n.SEEN), ["b/1", "b/2", "c/1", "d/1", "d/2", "d/3", "e/1", "f/1"])
eq("...where the marked set is one of them", marked(), ["f/1"])
true("...so 'since your last visit' can count across cohorts",
     len([d for d in n.SEEN.values() if d > "2026-09-10"]) == 5,
     sorted(n.SEEN.items()))
eq("SEEN excludes the baseline itself", [k for k, d in n.SEEN.items() if d <= state["baseline"]], [])

# ---- the ledger on disk: this file is committed, so its diff has to be legible
raw = n.PATH.read_text(encoding="utf-8")
eq("the ledger ends in exactly one newline", (raw.endswith("\n"), raw.endswith("\n\n")), (True, False))
true("the ledger is one repo per line, so a diff is the arrivals",
     raw.count('"a/1"') == 1 and '"repos": {\n  "a/1"' in raw.replace("\r\n", "\n"), raw[:120])
keys = [ln.split('"')[1] for ln in raw.replace("\r\n", "\n").split("\n") if ln.startswith('  "')]
eq("...and sorted, so the diff has no reordering in it", keys, sorted(keys))
before = n.PATH.stat().st_mtime_ns, raw
resolve(["a/1", "b/1", "c/1", "d/1", "e/1", "f/1"], day="2026-09-17")
eq("a build that adds nothing does not rewrite the ledger",
   (n.PATH.stat().st_mtime_ns, n.PATH.read_text(encoding="utf-8")), before)

# A missing key is filled rather than crashed on: `load()` has to read a ledger written before cohorts
# existed, and the answer for that file is "nothing is New" -- there is no previous cohort to recover, and
# inventing one would mark a set nobody imported.
reset()
n.PATH.write_text(json.dumps({"baseline": "2026-09-03",
                              "repos": {"x/1": "2026-09-03", "x/2": "2026-09-14"}}), encoding="utf-8")
old = n.load()
eq("a ledger with no cohort key loads with one at the baseline", old["cohort"], "2026-09-03")
eq("...so it marks nothing", n.cohort(old, day="2026-09-15"), "")
eq("...and its other missing keys are filled", (old["window_days"], old["sources"]), (n.WINDOW, {}))
resolve(["x/1", "x/2", "x/3"], day="2026-09-15")
eq("...and the next import that adds gives it a real one", n.COHORT, "2026-09-15")
eq("...marking only what that import brought", marked(), ["x/3"])
eq("...while the pre-existing arrival keeps its date and loses nothing but the mark",
   (dict(n.SEEN)["x/2"], n.mark("x/2")), ("2026-09-14", ""))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
