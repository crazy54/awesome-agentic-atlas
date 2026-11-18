"""Propose a change to latest_branch as one rolling `bot/...` branch and pull request, or withdraw it.

The canary (`.github/workflows/canary.yml`) finds two kinds of thing a human should merge rather than wake up
to: an upstream list that drifted, with the parse proposal's `taxonomy.py`/`buckets.py` lines; and committed
pages a generator would now write differently, regenerated. This is the one place either is pushed, and it
exists as a script rather than inline shell so that the one rule that matters -- **it pushes nothing but a
`bot/` branch** -- is enforced in code and asserted in `tests/ci_tools_test.py`, not left to every caller.

One branch per kind, rolling, not one per day: `bot/taxonomy` and `bot/regenerate`. The owner has one pull
request to look at for each, whose diff is always against the branch's current head, rather than a pile of
dated ones each stale by the next. Every run rebuilds the proposal from `latest_branch` as it stands, so:

  propose    the working tree has changes under the given paths: commit them on top of the checked-out
             `latest_branch` and force-push them to the bot branch -- but only if the tree differs from what
             the branch already holds, so an unchanged proposal is not re-pushed every four hours and its PR
             is not re-notified. Then open the PR if none is open for that branch, else edit its body.
  withdraw   there is nothing to propose any more (the daily regenerated the pages, the owner merged a mapping
             by hand): delete the bot branch, which closes its PR. Only ever a `bot/` branch.

Opening the PR needs the repository setting "Allow GitHub Actions to create and approve pull requests". When it
is off, `gh pr create` is refused, and the branch is still pushed: the job summary and the build-red issue carry
the one-click compare link instead (`tools/ci_alert.py` lists open bot branches). A PR opened with the Actions
token does not start the tests on itself -- GitHub does not run workflows for its own token's events -- so the
body says so; the merge runs them on latest_branch.

  python tools/bot_branch.py propose --branch bot/regenerate --title "..." --body-file body.md --paths docs/repo
  python tools/bot_branch.py withdraw --branch bot/regenerate
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
        "not run on a pull request the Actions token opened; merging runs the tests on `latest_branch`.")


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


def propose(git: Git, branch: str, title: str, body: str, paths: list[str]) -> int:
    sha = git("git", "rev-parse", "--short=9", "HEAD", capture=True, mutate=False).strip()
    new = git("git", "ls-files", "--others", "--exclude-standard", "--", *paths, capture=True, mutate=False)
    if git.ok("git", "diff", "--quiet", "HEAD", "--", *paths) and not new.strip():
        print(f"nothing changed under {' '.join(paths)}: nothing to propose")
        return withdraw(git, branch)
    git("git", "config", "user.name", "github-actions[bot]")
    git("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("git", "checkout", "-B", branch)
    git("git", "add", "--", *paths)
    git("git", "commit", "-m", title, "-m", f"Proposed by the canary from {BASE} at {sha}.")
    if remote_has(git, branch):
        git("git", "fetch", "--depth=1", "origin", branch, mutate=False)
        if git.ok("git", "diff", "--quiet", "HEAD", "FETCH_HEAD"):
            print(f"{branch} already holds exactly this; not re-pushed")
            return 0
    git("git", "push", "--force", "origin", f"HEAD:refs/heads/{branch}")
    full = body + NOTE.format(sha=sha)
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
    ap.add_argument("--branch", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--body-file")
    ap.add_argument("--paths", nargs="+", default=[])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    branch, git = guard(a.branch), Git(a.dry_run)
    if a.action == "withdraw":
        return withdraw(git, branch)
    if not a.paths or not a.title:
        raise SystemExit("propose needs --paths and --title")
    body = open(a.body_file, encoding="utf-8").read() if a.body_file else ""
    return propose(git, branch, a.title, body, a.paths)


if __name__ == "__main__":
    sys.exit(main())
