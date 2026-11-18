"""One issue that says the build is red, what failed, and what to do -- and closes itself when it is green.

WHY THIS EXISTS

Between 2026-10-04 and 2026-11-18 the daily published on six days out of forty-five, and nothing that went
red was noticed in less than two days. Every class of failure in that window -- upstream drift, a generator
change that landed without its output, a flaky harness -- sat red until somebody happened to open the
Actions tab, because the only notification GitHub sends is an email per failed run, to one address, worded
identically for "a list renamed a heading" and "the runner image lost Chromium". The detail-churn failure of
2026-11-03 was red on a push run for two weeks and the fix was one command printed in its own log. (The audit
is `team/ci/failure-audit.md` in the team folder; it is not part of this repository.)

So this turns the state of the three jobs that matter, and of the canary that warns about the first of them,
into one GitHub issue the owner can see, read and act on: which workflow, which step, the first lines of the
error, a link, and the suggested fix where the failure is one we know how to name. It is opened on the first
red run, edited as the state moves, commented on only when a *new* failure arrives (that comment is what
notifies; the same failure on the next run is not new, see `signature()`), and closed with a comment when every
one of them is green again.

WHAT "THE STATE" IS

For each of `daily.yml`, `weekly.yml`, `tests.yml` and `canary.yml`, the newest completed run on `latest_branch` that
says something about the branch: pushes, schedules and dispatches, not pull requests (a PR's run is about the
PR and is reported on the PR). A cancelled run says nothing -- it was superseded by a newer push or stopped by
hand -- unless a job in it was cancelled for exceeding its `timeout-minutes`, which is a failure with the
quietest possible log and exactly the one worth an alert. The daily's "no list moved, stopping" run concludes
`success` and is green, correctly: the site is current.

The newest *relevant* run, not the newest run, so a superseded cancellation does not hide the red run under
it; and newest rather than "any red in the last day", so the issue closes the moment a re-run goes green.

WHY A SWEEP AND NOT AN EVENT HANDLER

The workflow that calls this (`.github/workflows/alert.yml`) fires on `workflow_run` and on a schedule, and
both do the same thing: read all four states from the API and reconcile the issue against them. Nothing is
carried between invocations except what is in the issue itself (a JSON block in an HTML comment at the end of
its body, recording which failures have already been announced). So a missed event costs at most one sweep
interval, two invocations at once converge on the same issue, and running it again is always safe.

The schedule is there because `workflow_run` is not guaranteed to fire for a run that a `GITHUB_TOKEN` push or
dispatch started -- the dead-repo scan dispatches the daily that way -- and an alert that is silent on exactly
the runs nobody watched being started is the failure this file exists to end.

THE SUGGESTED FIX

`suggest()` knows the shapes of failure the audit found, by the text they print: upstream drift (the parser's
"sections no category is named for"), a harness whose FAIL line names the command that fixes it ("-- run:
python scripts/22_detail.py"), a rebase conflict, a timeout, the suite refusing to start. For drift it also
reads the parse proposal, if the failing run uploaded one (artifact `parse-proposal`, written by
`10_parse_sources.py --proposal`): the proposal's own Markdown is the fix, and the canary may already have
opened a PR with it. Anything it does not recognise gets the error lines and the link and no guess.

  python tools/ci_alert.py --dry-run          read the real state, print what it would do, change nothing
  python tools/ci_alert.py                    reconcile the issue (what alert.yml runs)
  python tools/ci_alert.py --dry-run --run 44162625100   classify one run and print its section

`--dry-run` makes only GET requests. Nothing here writes outside the issue it owns, which it finds by label.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "crazy54/awesome-agentic-atlas")
BRANCH = os.environ.get("AAA_ALERT_BRANCH", "latest_branch")
LABEL = "build-red"
TITLE = "Build red on latest_branch"
# The three jobs whose colour is the site's colour, and the canary, whose red is the early warning for the
# first of them: drift seen hours before the daily trips on it, with the mapping already proposed. Lighthouse
# and the monitoring check are left out on purpose: they measure the live site and report through their own
# channels, and a red Lighthouse budget is not a build that stopped.
WORKFLOWS = [
    ("daily.yml", "Daily build"),
    ("weekly.yml", "Weekly build"),
    ("tests.yml", "Tests"),
    ("canary.yml", "Canary"),
]
# The canary's proposals (`tools/bot_branch.py`), by the kind of failure they answer.
PROPOSALS = {"drift": "bot/taxonomy", "regenerate": "bot/regenerate"}
# Events that say something about the branch itself. `pull_request` runs report on their PR.
EVENTS = {"push", "schedule", "workflow_dispatch"}
STATE_MARK = "<!-- ci-alert:state "
LINES = 12  # error lines quoted per failing job; the link has the rest


# ------------------------------------------------------------------------------------------------ the API
def gh(*args: str, text: bool = True) -> str:
    """`gh` with up to three tries: an API that answers 502 once is not a reason to stay silent for two hours."""
    last = ""
    for attempt in range(3):
        p = subprocess.run(["gh", *args], capture_output=True, text=text, encoding="utf-8" if text else None,
                           errors="replace" if text else None)
        if p.returncode == 0:
            return p.stdout
        last = p.stderr.strip()
        if not re.search(r"HTTP 5\d\d|timeout|connection|EOF", last, re.I):
            break
        import time
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"gh {' '.join(args[:3])} failed: {last}")


def api(path: str) -> dict | list:
    return json.loads(gh("api", path))


# ---------------------------------------------------------------------------------------------- the runs
@dataclass
class Failure:
    """One red workflow: what ran, what failed, and what we know to do about it."""
    workflow: str
    title: str
    run_id: int
    url: str
    event: str
    sha: str
    created: str
    steps: list[str] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)
    fix: str = ""
    kind: str = "unknown"


def timed_out(job: dict) -> bool:
    """A job cancelled by its own `timeout-minutes`. Only the annotation says so; the conclusion is `cancelled`."""
    try:
        notes = api(f"repos/{REPO}/check-runs/{job['id']}/annotations")
    except RuntimeError:
        return False
    return any("exceeded the maximum execution time" in (n.get("message") or "") for n in notes)


def latest(workflow: str) -> tuple[dict | None, list[dict]]:
    """The newest completed run of `workflow` on BRANCH that says something about it, and its jobs."""
    try:
        runs = api(f"repos/{REPO}/actions/workflows/{workflow}/runs?branch={BRANCH}&status=completed&per_page=30")
    except RuntimeError as e:
        if "404" not in str(e):
            raise
        return None, []  # a workflow not merged yet (the canary, before its PR lands) has no runs to read
    for run in runs.get("workflow_runs", []):
        if run["event"] not in EVENTS:
            continue
        jobs = api(f"repos/{REPO}/actions/runs/{run['id']}/jobs").get("jobs", [])
        run = effective(run, jobs)
        if run["conclusion"] == "cancelled":
            continue  # superseded or stopped by hand: says nothing about the branch
        return run, jobs
    return None, []


def effective(run: dict, jobs: list[dict]) -> dict:
    """The run, with a cancellation that was really its own timeout called `timed_out`."""
    if run["conclusion"] == "cancelled" and any(j["conclusion"] == "cancelled" and timed_out(j) for j in jobs):
        return {**run, "conclusion": "timed_out"}
    return run


# A log line as GitHub serves it: an ISO timestamp, a space, the text. Older logs carry a BOM on line one.
STAMP = re.compile(r"^﻿?\d{4}-\d\d-\d\dT[\d:.]+Z ")
# Noise that precedes every error and explains nothing: group markers, the env block, the runner's shell
# banner, and deprecation chatter.
NOISE = re.compile(r"^(##\[(group|endgroup)\]|shell: |env:|  [A-Z_]+: |\(node:\d+\)|\(Use `node)")
# GitHub echoes a step's script back before running it, every line in cyan: the step's comments and code,
# hundreds of lines in daily.yml, and none of them output.
ECHO = "\x1b[36;1m"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def job_log(job_id: int) -> str:
    """A job's whole log. Newer `gh` refuses to print one with colour codes in it unless told it may, and older
    `gh` does not know the flag, so it is passed only when the first answer asks for it."""
    path = f"repos/{REPO}/actions/jobs/{job_id}/logs"
    try:
        return gh("api", path)
    except RuntimeError as e:
        if "allow-escape-sequences" not in str(e):
            raise
        return gh("api", "--allow-escape-sequences", path)


def clean(log: str) -> list[str]:
    """The log as text: timestamps off, the echoed script dropped, and then the colour codes off."""
    bare = (STAMP.sub("", l) for l in log.splitlines())
    return [ANSI.sub("", l) for l in bare if not l.startswith(ECHO)]


def short(line: str, room: int = 320) -> str:
    """A long line cut in the middle, not at the end: a harness puts the command that fixes it last."""
    return line if len(line) <= room else line[:room - 120] + " [...] " + line[-114:]


def excerpt(lines: list[str]) -> list[str]:
    """The lines a reader needs first: every FAIL, the parser's drift block, else what led up to the error."""
    keep: list[str] = []
    fails = [l for l in lines if l.startswith("FAIL ")]
    keep += [short(l) for l in fails[:8]]
    keep += [l.strip() for l in lines
             if re.search(r"no tally printed|went quiet --", l) and not l.startswith("##[error]") and "::error" not in l][:4]
    for i, l in enumerate(lines):
        if "no category is named for" in l:
            keep.append(l.strip())
            keep += [x.strip() for x in lines[i + 1:i + 30] if re.match(r"\s+\(", x)]
            break
    conflicts = [l for l in lines if l.startswith("CONFLICT")]
    if conflicts:
        keep += conflicts[:3] + ([f"... and {len(conflicts) - 3} more conflicts"] if len(conflicts) > 3 else [])
    if not keep:
        first = next((i for i, l in enumerate(lines) if l.startswith("##[error]")), None)
        if first is not None:
            before = [l for l in lines[max(0, first - 40):first] if l.strip() and not NOISE.match(l)]
            keep += [l[:300] for l in before[-LINES:]]
    errors = [l[len("##[error]"):] for l in lines
              if l.startswith("##[error]") and not l.startswith("##[error]Process completed with exit code")]
    keep += [short(e) for e in errors[:2]]
    return list(dict.fromkeys(keep))[:LINES + 8]


def suggest(lines: list[str], proposal: str = "") -> tuple[str, str]:
    """(kind, suggested fix) for the shapes of failure we know, by the words they print. ("unknown", "") else."""
    text = "\n".join(lines)
    if "no category is named for" in text:
        fix = ("**Upstream drift.** A source list added or renamed a section, and `scripts/10_parse_sources.py` "
               "refuses rows it cannot file. Add each section above to `taxonomy.SECTIONS` (and `buckets.py` "
               "if it needs a bucket), or merge the canary's proposal.")
        if proposal:
            fix += "\n\nThe parse proposal from this run:\n\n" + proposal.strip()
        return "drift", fix
    m = re.search(r"-- run: (python [^\s,]+(?: [^\s,]+)*)", text)
    if m:
        return "regenerate", (f"**Committed output is stale.** The harness names the fix: run `{m.group(1)}` and "
                              "commit what it writes, or merge the canary's proposal."
                              " A generator changed without its pages being regenerated.")
    if "CONFLICT" in text:
        return "conflict", ("**The push could not rebase.** This run built on a commit that moved while it ran. "
                            "Re-run it: it checks out the branch head, so the retry starts from the new commit.")
    if "exceeded the maximum execution time" in text:
        return "timeout", ("**A job hit its `timeout-minutes`.** It committed and recorded nothing. Read the last "
                           "step that printed anything in the log; the job durations are in the run summary.")
    if "no tally printed" in text:
        return "quiet", ("**A harness died before it printed its tally.** That is a crash, not an assertion: the "
                         "stack trace is in the log just above the harness's line in the total block. A browser "
                         "harness that loses its page mid-call (\"Inspected target navigated or closed\") on a slow "
                         "runner is the usual cause; re-run once, and if it repeats, the harness needs hardening.")
    if "refused to run" in text or "could not run" in text:
        return "refused", ("**The suite could not start.** `run.mjs` exits 2 for a missing browser, a missing "
                           "Python, or a missing entry page in `docs/`; its own output says which.")
    if "FAIL " in text:
        return "assertion", ("**An assertion failed.** The FAIL lines above name the harness and the assertion. "
                             "If it is a browser harness that passed on the previous run, it may be runner "
                             "timing: re-run once, and see `handbook/testing.md` on flaky waits.")
    return "unknown", ""


def proposal_for(run_id: int) -> str:
    """The parse proposal's Markdown, if the run uploaded one. Empty when it did not, or cannot be read."""
    with tempfile.TemporaryDirectory() as d:
        try:
            gh("run", "download", str(run_id), "-R", REPO, "-n", "parse-proposal", "-D", d)
        except RuntimeError:
            return ""
        md = Path(d) / "proposal.md"
        return md.read_text(encoding="utf-8")[:6000] if md.exists() else ""


def failure(workflow: str, title: str, run: dict, jobs: list[dict]) -> Failure:
    f = Failure(workflow, title, run["id"], run["html_url"], run["event"], run["head_sha"][:9],
                run["created_at"][:16].replace("T", " "))
    for j in jobs:
        if j["conclusion"] not in ("failure", "cancelled", "timed_out"):
            continue
        steps = [s["name"] for s in j.get("steps", []) if s.get("conclusion") in ("failure", "cancelled")]
        f.steps.append(f"{j['name']}: {', '.join(steps) or '(no step: the job itself)'}")
        if run["conclusion"] == "timed_out":
            f.lines.append(f"{j['name']}: the job has exceeded the maximum execution time")
            # and then whatever it printed, which says where it was when the limit came
        try:
            log = job_log(j["id"])
        except RuntimeError as e:
            f.lines.append(f"(could not read the log: {e})")
            continue
        f.lines += excerpt(clean(log))
    kind, fix = suggest(f.lines)
    if kind == "drift":
        kind, fix = suggest(f.lines, proposal_for(f.run_id))
    if kind in PROPOSALS:
        fix += proposal_link(PROPOSALS[kind])
    f.kind, f.fix = kind, fix
    return f


def proposal_link(branch: str) -> str:
    """Where the canary's proposal for this is: its open PR, else its branch's compare page, else nothing."""
    try:
        prs = json.loads(gh("pr", "list", "-R", REPO, "--head", branch, "--state", "open", "--json", "url"))
        if prs:
            return f"\n\nThe canary's proposal is open: {prs[0]['url']}"
        api(f"repos/{REPO}/branches/{branch.replace('/', '%2F')}")
    except RuntimeError:
        return ""
    return (f"\n\nThe canary pushed a proposal to `{branch}` but could not open a PR for it; open one in one "
            f"click: https://github.com/{REPO}/compare/{BRANCH}...{branch}?expand=1")


def signature(f: Failure) -> str:
    """What makes two red runs the same failure: the job, the kind, and the quoted lines with every number
    taken out (durations, counts, run ids). The issue is commented on when this changes, not on every run --
    the canary is red every four hours until its proposal is merged, and that is one alert, not six a day."""
    text = "\n".join([f.workflow, f.kind, *(re.sub(r"\d+", "#", l) for l in f.lines)])
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def survey() -> tuple[list[Failure], list[str]]:
    """(the red workflows, one line per green or unknown one)."""
    red, green = [], []
    for wf, title in WORKFLOWS:
        run, jobs = latest(wf)
        if run is None:
            green.append(f"{title}: no completed run on `{BRANCH}`")
        elif run["conclusion"] in ("success", "skipped", "neutral"):
            green.append(f"{title}: green, [run {run['id']}]({run['html_url']}) "
                         f"({run['event']}, {run['created_at'][:10]})")
        else:
            red.append(failure(wf, title, run, jobs))
    return red, green


# --------------------------------------------------------------------------------------------- the issue
def section(f: Failure) -> str:
    out = [f"### {f.title} -- [run {f.run_id}]({f.url})",
           f"`{f.workflow}`, {f.event} at {f.created} UTC on `{f.sha}`.", "",
           "Failing step" + ("s" if len(f.steps) > 1 else "") + ": " + "; ".join(f.steps), ""]
    if f.lines:
        out += ["```", *[l.replace("```", "'''") for l in f.lines], "```", ""]
    out.append(f.fix or "No suggested fix: this is not a failure shape `tools/ci_alert.py` knows. Read the run.")
    return "\n".join(out)


def body(red: list[Failure], green: list[str], announced: dict) -> str:
    parts = ["This issue is opened, edited and closed by `.github/workflows/alert.yml` (`tools/ci_alert.py`). "
             "It reflects the newest relevant run of each build and of the canary on `latest_branch`, and closes itself when "
             "all of them are green. Edits to this body are overwritten; comment instead."]
    parts += [section(f) for f in red]
    if green:
        parts.append("### Green\n\n" + "\n".join(f"- {g}" for g in green))
    parts += [STATE_MARK + json.dumps(announced, sort_keys=True) + " -->"]
    return "\n\n".join(p for p in parts if p)


def state_of(issue_body: str) -> dict:
    i = issue_body.rfind(STATE_MARK)
    if i < 0:
        return {}
    try:
        return json.loads(issue_body[i + len(STATE_MARK):].split(" -->", 1)[0])
    except ValueError:
        return {}


def plan(red: list[Failure], green: list[str], issue: dict | None) -> list[tuple[str, str]]:
    """What to do, as (action, text). Pure, so the decision is testable without the API.

    open      no issue is open and something is red
    edit      the issue is open: its body is rewritten to the current state (always, it is cheap and idempotent)
    comment   a red failure this issue has not announced yet, by `signature()` -- the only thing that notifies
    close     the issue is open and nothing is red
    """
    if not red:
        if issue is None:
            return []
        return [("comment", "Green again. " + "; ".join(green)), ("close", "")]
    old = state_of(issue["body"]) if issue else {}
    announced = {f.workflow: signature(f) for f in red}
    new = [f for f in red if old.get(f.workflow) != announced[f.workflow]]
    text = body(red, green, announced)
    if issue is None:
        return [("open", text)]
    acts = [("edit", text)]
    if new:
        acts.append(("comment", "Red: " + "; ".join(
            f"{f.title} [run {f.run_id}]({f.url}), {f.kind}" for f in new)))
    return acts


def find_issue() -> dict | None:
    found = json.loads(gh("issue", "list", "-R", REPO, "--label", LABEL, "--state", "open",
                          "--json", "number,body,title", "--limit", "5"))
    return found[0] if found else None


def apply(acts: list[tuple[str, str]], issue: dict | None) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        path = tmp.name
    for act, text in acts:
        Path(path).write_text(text, encoding="utf-8")
        if act == "open":
            try:
                gh("label", "create", LABEL, "-R", REPO, "--color", "d73a4a",
                   "--description", "A build on latest_branch is red (opened and closed by alert.yml)")
            except RuntimeError:
                pass  # already exists
            out = gh("issue", "create", "-R", REPO, "--title", TITLE, "--label", LABEL, "--body-file", path)
            print(f"opened {out.strip()}")
        elif act == "edit":
            gh("issue", "edit", str(issue["number"]), "-R", REPO, "--body-file", path)
            print(f"edited #{issue['number']}")
        elif act == "comment":
            gh("issue", "comment", str(issue["number"]), "-R", REPO, "--body-file", path)
            print(f"commented on #{issue['number']}")
        elif act == "close":
            gh("issue", "close", str(issue["number"]), "-R", REPO)
            print(f"closed #{issue['number']}")
    os.unlink(path)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--dry-run", action="store_true", help="print what would be done; make no change")
    ap.add_argument("--run", type=int, help="classify this one run id and print its section (implies --dry-run)")
    a = ap.parse_args()

    if a.run:
        run = api(f"repos/{REPO}/actions/runs/{a.run}")
        jobs = api(f"repos/{REPO}/actions/runs/{a.run}/jobs").get("jobs", [])
        run = effective(run, jobs)
        wf = Path(run["path"]).name
        print(section(failure(wf, dict(WORKFLOWS).get(wf, run["name"]), run, jobs)))
        return 0

    red, green = survey()
    issue = find_issue()
    acts = plan(red, green, issue)
    where = f"#{issue['number']}" if issue else "no open issue"
    print(f"{len(red)} red, {len(green)} green; {where}; {len(acts)} action(s)")
    if a.dry_run:
        for act, text in acts:
            print(f"\n===== would {act}" + (f" #{issue['number']}" if issue else "") + " =====")
            print(text)
        return 0
    apply(acts, issue)
    return 0


if __name__ == "__main__":
    sys.exit(main())
