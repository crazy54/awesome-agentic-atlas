"""The CI tooling's rules: what a local run may do, what the canary may push, and what every workflow must say.

Three files in `tools/` and four in `.github/workflows/` carry promises that nothing else in the suite can
see, because each one is about a runner, a branch or a schedule rather than about a page. They were written
after the 45-day audit of 2026-11-18, and each group below is a failure that audit found or a rule written so
that a fix for one cannot quietly undo another.

  the local run    -- `tools/local_daily.py` reads its stages out of `daily.yml` itself, in the workflow's
                      order; never runs IndexNow or records the SHAs; and --from/--to/--only pick what they say.
  the bot branch   -- `tools/bot_branch.py` pushes and deletes `bot/...` branches and nothing else, whatever
                      it is passed.
  the workflows    -- every job has a `timeout-minutes`; only the builds share `atlas-build` (a group holds one
                      pending run, so anything else queued there can knock a waiting build out); the canary
                      saves no cache and pushes only through bot_branch; the alert watches workflows by names
                      that exist; the builds' network steps retry.

Run: python tests/ci_tools_test.py
"""
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / ".github" / "workflows"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # a dataclass looks its own module up by name
    spec.loader.exec_module(mod)
    return mod


ld, bb, ca = load("local_daily"), load("bot_branch"), load("ci_alert")
ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


print("the local run")
daily = ld.stages(WF / "daily.yml")
names = [s.name for s in daily]
# The pipeline order the handbook describes. A stage added to the daily lands in this list by itself; this
# asserts the ones whose order is load-bearing (see the notes in daily.yml) are where they must be.
order = ["12_scout", "watch_sources", "pull_sources", "01_parse", "02_fetch--force", "10_parse_sources",
         "11_fetch_all", "12_scout--follow-renames", "14_classify_all", "17_markdown", "check_markdown",
         "19_pages", "25_velocity", "19c_live", "19d_discover", "20_landing", "22_detail", "31_home",
         "24_pwa", "27_semantic", "suite"]
true("every stage the daily runs is found, in the daily's order",
     all(n in names for n in order) and [n for n in names if n in order] == order, str(names))
true("each stage knows the step it is in",
     next(s for s in daily if s.name == "22_detail").step == "Build the Markdown edition and the site")
plan = ld.plan(daily, None, None, [], True, False)
true("IndexNow is never run locally", not any("26_indexnow" in s.command for s in plan))
true("the build is never recorded locally", not any("--update" in s.command for s in plan))
true("...not even when named", ld.plan(daily, None, None, ["watch_sources--update", "26_indexnow--changed"], True, True) == [])
true("the suite is left out unless asked for", "suite" not in [s.name for s in ld.plan(daily, None, None, [], False, False)])
p = [s.name for s in ld.plan(daily, "10_parse_sources", "14_classify_all", [], False, False)]
true("--from and --to are inclusive", p[0] == "10_parse_sources" and p[-1] == "14_classify_all" and "02_fetch--force" not in p, str(p))
true("a script alone names its first run", [s.name for s in ld.plan(daily, None, None, ["12_scout"], False, False)] == ["12_scout"])
true("--only keeps the order it was given",
     [s.name for s in ld.plan(daily, None, None, ["22_detail", "19_pages"], False, False)] == ["22_detail", "19_pages"])
try:
    ld.pick(daily, "no_such_stage")
    true("an unknown stage is refused, with the list", False)
except SystemExit as e:
    true("an unknown stage is refused, with the list", "22_detail" in str(e))
weekly = ld.stages(WF / "weekly.yml")
true("weekly's screenshots are found, and left out unless asked for",
     "15_shots_all" in [s.name for s in weekly] and
     "15_shots_all" not in [s.name for s in ld.plan(weekly, None, None, [], False, False)] and
     "15_shots_all" in [s.name for s in ld.plan(weekly, None, None, [], False, True)])
with tempfile.TemporaryDirectory() as d:
    f = Path(d) / "x.yml"
    f.write_text("""jobs:
  b:
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/aa.py
      - name: Block
        run: |
          set -e
          # python scripts/commented.py
          python scripts/bb.py --flag "$X"
          if true; then python scripts/inside_if.py; fi
          python - <<'PY'
          print("x")
          PY
      - name: Inline
        run: python scripts/cc.py
        env:
          python scripts/not_a_run.py: 1
""", encoding="utf-8")
    got = [(s.name, s.step) for s in ld.stages(f)]
    true("block, inline and unnamed steps are read; comments, ifs and env are not",
         got == [("aa", ""), ("bb--flag", "Block"), ("cc", "Inline")], str(got))

print("the bot branch")
for b in ["bot/taxonomy", "bot/regenerate", "refs/heads/bot/x"]:
    true(f"{b} may be pushed", bb.guard(b).startswith("bot/"))
for b in ["latest_branch", "main", "bot/", "bot/../latest_branch", "refs/heads/latest_branch", "jfh-eng-ci", "bots/x"]:
    try:
        bb.guard(b)
        true(f"{b} is refused", False)
    except SystemExit:
        true(f"{b} is refused", True)

print("the workflows")
files = sorted(WF.glob("*.yml"))
for f in files:
    text = f.read_text(encoding="utf-8")
    jobs = re.split(r"\n(?=  [A-Za-z_-]+:\n)", text.split("\njobs:\n", 1)[1])
    for j in jobs:
        jn = j.strip().split(":", 1)[0]
        true(f"{f.name}: job {jn} has a timeout-minutes", "timeout-minutes:" in j)
    groups = re.findall(r"^concurrency:\n  group: (\S+)", text, re.M)
    if f.name in ("daily.yml", "weekly.yml"):
        true(f"{f.name} is in atlas-build", groups == ["atlas-build"], str(groups))
    else:
        true(f"{f.name} stays out of atlas-build", "atlas-build" not in groups, str(groups))
canary = (WF / "canary.yml").read_text(encoding="utf-8")
true("the canary saves no cache and restores none", "actions/cache" not in canary)
true("the canary pushes only through bot_branch",
     not re.search(r"^\s+git push", canary, re.M) and "tools/bot_branch.py propose --branch bot/" in canary)
true("the canary's bot branches are the ones the alert links", all(v in canary for v in ca.PROPOSALS.values()))
alert = (WF / "alert.yml").read_text(encoding="utf-8")
watched = re.findall(r'^      - "(.+)"$', alert.split("workflow_run:", 1)[1].split("types:", 1)[0], re.M)
named = {re.search(r"^name: (.+)$", f.read_text(encoding="utf-8"), re.M).group(1): f.name for f in files}
true("the alert watches workflows by names that exist", watched and all(w in named for w in watched),
     f"{watched} vs {sorted(named)}")
true("...and the same ones the alert script reads", sorted(named[w] for w in watched) == sorted(w for w, _ in ca.WORKFLOWS),
     str(sorted(named.get(w, w) for w in watched)))
for name in ("daily.yml", "weekly.yml", "tests.yml"):
    text = (WF / name).read_text(encoding="utf-8")
    limit = re.search(r"^    timeout-minutes: (.+)$", text, re.M).group(1).strip()
    budget = re.search(r"run: bash tools/budget\.sh (.+)$", text, re.M)
    true(f"{name}: the time report is against the job's own limit",
         budget and budget.group(1).strip() == limit and "JOB_START=" in text,
         f"{limit} vs {budget and budget.group(1)}")
    true(f"{name}: pip retries", all("tools/retry.sh" in l for l in text.splitlines() if "pip install" in l and "run:" in l),
         str([l for l in text.splitlines() if "pip install" in l]))
for name in ("daily.yml", "weekly.yml", "dead-repos.yml"):
    text = (WF / name).read_text(encoding="utf-8")
    true(f"{name}: the push retries", "git push" not in "".join(l for l in text.splitlines() if not l.strip().startswith("#")
                                                              and "tools/retry.sh" not in l and "git push" in l),
         str([l.strip() for l in text.splitlines() if "git push" in l and not l.strip().startswith("#")]))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
