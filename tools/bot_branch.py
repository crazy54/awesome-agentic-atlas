"""Propose a change to latest_branch as one rolling `bot/...` branch and pull request, or withdraw it.

The canary (`.github/workflows/canary.yml`) finds two kinds of thing a human should merge rather than wake up
to: an upstream list that drifted, with the drift proposal's `taxonomy.py`/`buckets.py` lines applied
(`scripts/apply_drift_proposal.py`); and committed pages a generator would now write differently, regenerated. This is the one place either is pushed, and it
exists as a script rather than inline shell so that the one rule that matters -- **it pushes nothing but a
`bot/` branch** -- is enforced in code and asserted in `tests/ci_tools_test.py`, not left to every caller.

One branch per thing to merge, not one per day. Stale pages are one rolling branch, `bot/regenerate`. Drift is
one branch per drift, `bot/drift-<fingerprint[:8]>`, named for `drift.py`'s fingerprint of the placements,
which is the same for the same drift on every run. So the same drift seen six times a day is one branch and one
PR, and a *different* drift -- a second list moving before the first PR is merged -- is a new branch that
supersedes the old one (`--superseding bot/drift-` withdraws every other branch under that prefix). Every run
rebuilds the proposal from `latest_branch` as it stands, so:

  propose    the working tree has changes under the given paths: commit them on top of the checked-out
             `latest_branch` and force-push them to the bot branch -- but only if the tree differs from what
             the branch already holds, so an unchanged proposal is not re-pushed every four hours and its PR
             is not re-notified. Then open the PR if none is open for that branch, else edit its body.
  withdraw   there is nothing to propose any more (the daily regenerated the pages, the owner merged a mapping
             by hand): delete the bot branch, which closes its PR. Only ever a `bot/` branch. With
             `--superseding PREFIX` and no `--branch`, every branch under PREFIX.

Opening the PR needs the repository setting "Allow GitHub Actions to create and approve pull requests". When it
is off, `gh pr create` is refused, and the branch is still pushed: the job summary and the build-red issue carry
the one-click compare link instead (`tools/ci_alert.py` lists open bot branches). A PR opened with the Actions
token does not start the tests on itself -- GitHub does not run workflows for its own token's events -- so the
body says so and says how to start them by hand: `gh workflow run tests.yml --ref <branch>` (tests.yml has
`workflow_dispatch`; the run shows on the branch, not as a check on the PR), or close and reopen the PR as a
person, which fires `pull_request` under their name and does attach the checks. Either way the merge runs them
on latest_branch.

  python tools/bot_branch.py propose --branch bot/regenerate --title "..." --body-file body.md --paths docs/repo
  python tools/bot_branch.py withdraw --branch bot/regenerate
  python tools/bot_branch.py propose --branch bot/drift-1a2b3c4d --superseding bot/drift- ...
  python tools/bot_branch.py withdraw --superseding bot/drift-
  add --dry-run to either to print the git and gh commands and run none
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

REPO = os.environ.get("GITHUB_REPOSITORY", "crazy54/awesome-agentic-atlas")
BASE = os.environ.get("AAA_BOT_BASE", "latest_branch")
NOTE = ("\n\n---\nOpened by `.github/workflows/canary.yml` from `latest_branch` at {sha}. It is rebuilt every run: "
        "pushes here are overwritten, and it is withdrawn by itself once there is nothing left to propose. CI does "
        "not start by itself on a pull request the Actions token opened: run `gh workflow run tests.yml --ref "
        "{branch}`, or close and reopen this PR, to see it before merging. Merging runs it on `latest_branch`.")


def guard(branch: str) -> str:
    """The one rule: nothing but a `bot/` branch, and never the base, whatever the caller passed."""
    b = branch.removeprefix("refs/heads/")
    if not b.startswith("bot/") or b in (BASE, "bot/") or ".." in b or b.endswith("/"):
        raise SystemExit(f"refusing to touch {branch!r}: this script pushes and deletes bot/... branches only")
    return b


class Git:
    def __init__(self, dry: bool):
        self.dry = dry

    def __call__(self, *args: str, check: bool = True, capture: bool = False, mutate: bool = True) -> str:
        if self.dry and mutate:
            print("would run:", " ".join(args))
            return ""
        p = subprocess.run(args, capture_output=True, text=True)
        if check and p.returncode:
            raise SystemExit(f"{' '.join(args[:3])} failed ({p.returncode}): {p.stderr.strip()}")
        return p.stdout if capture else (p.stdout + p.stderr if p.returncode else "")

    def ok(self, *args: str) -> bool:
        return subprocess.run(args, capture_output=True).returncode == 0


def remote_has(git: Git, branch: str) -> bool:
    return git.ok("git", "ls-remote", "--exit-code", "--heads", "origin", branch)


def heads(git: Git, prefix: str) -> list[str]:
    """Every remote branch under `prefix` (itself a `bot/` prefix), by name."""
    out = git("git", "ls-remote", "--heads", "origin", f"refs/heads/{prefix}*", capture=True, mutate=False)
    return [l.split("refs/heads/", 1)[1] for l in out.splitlines() if "refs/heads/" in l]


def propose(git: Git, branch: str, title: str, body: str, paths: list[str], superseding: str = "") -> int:
    sha = git("git", "rev-parse", "--short=9", "HEAD", capture=True, mutate=False).strip()
    new = git("git", "ls-files", "--others", "--exclude-standard", "--", *paths, capture=True, mutate=False)
    if git.ok("git", "diff", "--quiet", "HEAD", "--", *paths) and not new.strip():
        print(f"nothing changed under {' '.join(paths)}: nothing to propose")
        return withdraw(git, branch)
    for old in heads(git, superseding) if superseding else []:
        if old != branch:
            withdraw(git, guard(old))  # an older drift this one replaces
    git("git", "config", "user.name", "github-actions[bot]")
    git("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("git", "checkout", "-B", branch)
    git("git", "add", "--", *paths)
    git("git", "commit", "-m", title, "-m", f"Proposed by the canary from {BASE} at {sha}.")
    if remote_has(git, branch):
        git("git", "fetch", "--depth=1", "origin", branch, mutate=False)
        # The proposed files only: latest_branch moves under the branch every day, and that is not a change
        # to the proposal. (The PR's diff is against the merge base, so it stays just the proposal.)
        if git.ok("git", "diff", "--quiet", "HEAD", "FETCH_HEAD", "--", *paths):
            print(f"{branch} already holds exactly this; not re-pushed")
            return 0
    git("git", "push", "--force", "origin", f"HEAD:refs/heads/{branch}")
    full = body + NOTE.format(sha=sha, branch=branch)
    compare = f"https://github.com/{REPO}/compare/{BASE}...{branch}?expand=1"
    found = git("gh", "pr", "list", "-R", REPO, "--head", branch, "--state", "open", "--json", "number",
                "--jq", ".[0].number", capture=True, mutate=False).strip()
    if found:
        git("gh", "pr", "edit", found, "-R", REPO, "--title", title, "--body", full)
        print(f"updated PR #{found}")
        return 0
    if git.dry:
        print(f"would open a PR from {branch}: {title}")
        return 0
    p = subprocess.run(["gh", "pr", "create", "-R", REPO, "--base", BASE, "--head", branch, "--title", title,
                        "--body", full], capture_output=True, text=True)
    if p.returncode == 0:
        print(f"opened {p.stdout.strip()}")
        return 0
    # Most likely the repository does not let the Actions token open PRs. The branch is pushed; say where it is.
    msg = (f"Pushed `{branch}` but could not open a pull request ({p.stderr.strip()[:200]}). "
           f"Open it in one click: {compare}")
    print(f"::warning title=Proposal pushed, no PR::{msg}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"\n**{title}**\n\n{msg}\n")
    return 0


def withdraw(git: Git, branch: str) -> int:
    if not remote_has(git, branch):
        return 0
    git("git", "push", "origin", "--delete", branch)
    print(f"withdrew {branch} (its PR, if any, closes with it)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("action", choices=["propose", "withdraw"])
    ap.add_argument("--branch")
    ap.add_argument("--superseding", default="", help="a bot/ prefix: withdraw every other branch under it")
    ap.add_argument("--title", default="")
    ap.add_argument("--body-file")
    ap.add_argument("--paths", nargs="+", default=[])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    git = Git(a.dry_run)
    prefix = guard(a.superseding + "x")[:-1] if a.superseding else ""  # the prefix obeys the same rule
    if a.action == "withdraw" and not a.branch:
        if not prefix:
            raise SystemExit("withdraw needs --branch or --superseding")
        for old in heads(git, prefix):
            withdraw(git, guard(old))
        return 0
    if not a.branch:
        raise SystemExit("propose needs --branch")
    branch = guard(a.branch)
    if a.action == "withdraw":
        return withdraw(git, branch)
    if not a.paths or not a.title:
        raise SystemExit("propose needs --paths and --title")
    body = open(a.body_file, encoding="utf-8").read() if a.body_file else ""
    return propose(git, branch, a.title, body, a.paths, prefix)


if __name__ == "__main__":
    sys.exit(main())
