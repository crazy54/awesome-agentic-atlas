"""The build-red alert in `tools/ci_alert.py`: what it quotes, what it suggests, and when it opens, comments and closes.

The alert is the one thing in this repository that writes to the issue tracker, and it acts only after a
merge, on the real repository, on the days something is already wrong. So its decisions are tested here
against logs shaped exactly like the ones the 45-day audit read -- the drift block, detail-churn's FAIL line
with its "-- run:" tail, a rebase conflict, a harness that crashed before its tally, a job killed at its
timeout -- and against the issue states it can meet. Nothing here calls `gh`.

Four groups:

  the excerpt   -- timestamps and the echoed script are dropped; FAIL lines and the drift block are kept
                   whole enough to act on; a long FAIL line is cut in the middle, never through its fix.
  the guess     -- each known failure shape gets its kind and fix, and an unknown one gets none.
  the plan      -- open once, comment only on a failure it has not announced (not on every run of the same
                   failure: the canary is red every four hours until merged), edit always, close on green.
  the state     -- the announced ids survive a round trip through the issue body, and a mangled one is empty.

Run: python tests/ci_alert_test.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
spec = importlib.util.spec_from_file_location("ci_alert", TOOLS / "ci_alert.py")
ca = importlib.util.module_from_spec(spec)
sys.modules["ci_alert"] = ca  # a dataclass looks its own module up by name
spec.loader.exec_module(ca)

ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def log(*lines: str) -> str:
    """A job log as GitHub serves it: a timestamp on every line, a BOM on the first."""
    return "\n".join(("﻿" if i == 0 else "") + f"2026-11-17T19:48:59.{i:07d}Z {l}" for i, l in enumerate(lines))


ECHO = "\x1b[36;1m"
DRIFT = log(
    "##[group]Run set -euo pipefail",
    ECHO + "set -euo pipefail\x1b[0m",
    ECHO + "# a comment that mentions CONFLICT and timed out and FAIL in passing\x1b[0m",
    "shell: /usr/bin/bash -e {0}",
    "19170 rows -> cache/entries_all.json",
    "8 sections no category is named for -- add each to taxonomy.SECTIONS:",
    "  ('skills_libukai', 'Content Creation'): ...",
    "  ('skills_libukai', 'Written Tutorials'): ...",
    "##[error]Process completed with exit code 1.",
)
CHURN_FAIL = ("FAIL the committed docs/repo is byte-identical to a fresh regeneration  -- 8638 file(s): "
              + ", ".join(f"differs: repo/o{i}/r{i}/index.html" for i in range(40))
              + ", +8598 more -- run: python scripts/22_detail.py")
CHURN = log(
    "── detail-churn.mjs  ·  every detail page, regenerated and hashed ──",
    CHURN_FAIL,
    "12 passed, 1 failed",
    "RED",
    "##[error]The suite is red. Either an assertion failed or a harness went quiet -- printed no tally.",
    "##[error]Process completed with exit code 1.",
)
CONFLICT = log(*[f"CONFLICT (content): Merge conflict in docs/f{i}.html" for i in range(6)],
               "##[error]Process completed with exit code 1.")
QUIET = log(
    "Error: Inspected target navigated or closed",
    "  friends-check.mjs          no tally printed -- exited 1  131.8s  (printed no tally at all, and exited 1)",
    "##[error]An assertion failed, or a harness went quiet -- printed no tally, asserted nothing.",
)
PLAIN = log("some output", "Traceback (most recent call last):", "KeyError: 'x'",
            "##[error]Process completed with exit code 1.")

print("the excerpt")
d = ca.excerpt(ca.clean(DRIFT))
true("the timestamps and the BOM are gone", all(not l.startswith(("2026-", "﻿")) for l in ca.clean(DRIFT)))
true("the echoed script is gone, with its comments", not any("a comment that mentions" in l for l in ca.clean(DRIFT)))
true("the drift block is quoted, header and every section",
     d[:3] == ["8 sections no category is named for -- add each to taxonomy.SECTIONS:",
               "('skills_libukai', 'Content Creation'): ...", "('skills_libukai', 'Written Tutorials'): ..."], str(d))
true("GitHub's 'exit code 1' line is not quoted", not any("exit code" in l for l in d), str(d))
c = ca.excerpt(ca.clean(CHURN))
true("a long FAIL line is cut in the middle and keeps its fix",
     c[0].startswith("FAIL the committed docs/repo") and c[0].endswith("-- run: python scripts/22_detail.py")
     and " [...] " in c[0] and len(c[0]) <= 330, c[0])
true("the suite's red line is quoted once", sum("The suite is red" in l for l in c) == 1, str(c))
k = ca.excerpt(ca.clean(CONFLICT))
true("conflicts are quoted three and counted", len(k) == 4 and k[3] == "... and 3 more conflicts", str(k))
p = ca.excerpt(ca.clean(PLAIN))
true("with nothing recognised, the lines before the error are quoted",
     "Traceback (most recent call last):" in p and "KeyError: 'x'" in p, str(p))

print("the guess")
true("drift", ca.suggest(d)[0] == "drift")
true("drift carries the proposal when there is one",
     "file `Content Creation` under" in ca.suggest(d, "file `Content Creation` under Skills")[1])
kind, fix = ca.suggest(c)
true("stale output, and the command is the harness's own", kind == "regenerate" and "`python scripts/22_detail.py`" in fix, fix)
true("conflict", ca.suggest(k)[0] == "conflict")
true("a crash before the tally is not called an assertion", ca.suggest(ca.excerpt(ca.clean(QUIET)))[0] == "quiet")
true("a timeout", ca.suggest(["suite: the job has exceeded the maximum execution time"])[0] == "timeout")
true("an assertion", ca.suggest(["FAIL nib: ...nothing saved -- [\"jfhkit:v\"]"])[0] == "assertion")
true("'timed out' inside a FAIL line is still an assertion, not a job timeout",
     ca.suggest(["FAIL the bubble timed out after 8 s"])[0] == "assertion")
true("an unknown failure gets no guess", ca.suggest(p) == ("unknown", ""))
CANARY = log(
    "drift: placed ('skills_libukai', 'Content Creation'), 12 rows, under Skills / Writing by position",
    "drift: degraded mcp_punkpeye (punkpeye/awesome-mcp-servers): shrink -- 412 rows, was 980",
    "drift: 1 placement(s), 1 degraded list(s), fingerprint 1a2b3c4d",
    "##[error]1 section(s) filed provisionally, 1 list(s) degraded. The drift: lines above say which.",
)
cx = ca.excerpt(ca.clean(CANARY))
true("the canary's drift: lines are quoted", sum(l.startswith("drift: ") for l in cx) == 3, str(cx))
kind, fix = ca.suggest(cx)
true("a provisional placement is drift, and the degraded list is mentioned", kind == "drift" and "degraded" in fix, fix)
true("a degraded list alone is its own kind, with no mapping offered",
     ca.suggest([l for l in cx if "placed" not in l])[0] == "degraded")


def F(wf: str, rid: int, lines: list[str] | None = None) -> "ca.Failure":
    return ca.Failure(wf, wf, rid, f"https://x/{rid}", "schedule", "abc", "2026-11-17 19:48", ["build: Fetch"],
                      lines or ["('skills_libukai', 'Content Creation'): ..."], "fix", "drift")


print("the plan")
acts = ca.plan([F("daily.yml", 1)], ["Tests: green"], None)
true("red and no issue: open one, and only that", [a for a, _ in acts] == ["open"], str(acts))
opened = {"number": 7, "body": acts[0][1]}
acts = ca.plan([F("daily.yml", 1)], [], opened)
true("the same red run again: edit, and no comment", [a for a, _ in acts] == ["edit"], str(acts))
acts = ca.plan([F("daily.yml", 2)], [], opened)
true("a new run of the same failure: edit, and no comment", [a for a, _ in acts] == ["edit"], str(acts))
true("...and the body links the newest run", "[run 2](https://x/2)" in acts[0][1])
acts = ca.plan([F("daily.yml", 3, ["FAIL took 131.8s"])], [], opened)
true("a different failure of the same job: edit and comment", [a for a, _ in acts] == ["edit", "comment"], str(acts))
true("...and the comment names the new run", "run 3" in acts[1][1], acts[1][1])
true("numbers alone do not make a failure new",
     ca.signature(F("x", 1, ["FAIL took 131.8s"])) == ca.signature(F("x", 2, ["FAIL took 204.1s"])))
acts = ca.plan([F("daily.yml", 1), F("tests.yml", 9)], [], opened)
true("a second job going red: one comment, naming only the new one",
     [a for a, _ in acts] == ["edit", "comment"] and "run 9" in acts[1][1] and "run 1]" not in acts[1][1], str(acts))
acts = ca.plan([], ["Daily build: green"], opened)
true("all green with the issue open: comment and close", [a for a, _ in acts] == ["comment", "close"], str(acts))
true("all green and no issue: nothing", ca.plan([], ["x"], None) == [])

print("the state")
b = ca.body([F("daily.yml", 41), F("weekly.yml", 42)], [], {"daily.yml": 41, "weekly.yml": 42})
true("announced ids round-trip through the body", ca.state_of(b) == {"daily.yml": 41, "weekly.yml": 42}, ca.state_of(b))
true("a body without the block is an empty state", ca.state_of("someone rewrote this") == {})
true("a mangled block is an empty state, not a crash", ca.state_of(ca.STATE_MARK + "{nope -->") == {})
true("each red job has its own section with its link",
     b.count("### ") == 2 and "[run 41](https://x/41)" in b and "[run 42](https://x/42)" in b)
true("a fence inside a quoted line cannot break out of the code block",
     "```" not in ca.section(ca.Failure("a", "a", 1, "u", "e", "s", "c", [], ["oops ``` here"])).split("```\n", 1)[1]
     .rsplit("\n```", 1)[0])

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
