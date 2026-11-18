"""Run the daily's (or the weekly's) stages on a laptop, in the workflow's order, from any stage to any stage.

WHY

When a build goes red on a runner, the question is almost always "which stage, on what input", and the only
way to answer it used to be pushing a branch and asking for a dispatch of `daily.yml` -- which shares the
`atlas-build` queue with the real daily, takes an hour and a half, and has to go through the lead. Most
failures do not need a runner at all: drift reproduces with `pull_sources.py` and `10_parse_sources.py`, a
broken page with the generators over the committed data, a crash in a signal stage with that stage alone.
This runs exactly those, here.

WHERE THE STAGES COME FROM

From the workflow file itself, not from a list kept here. Every `python scripts/...` line in a `run:` block
of `daily.yml` (or `weekly.yml` with `--workflow weekly`) is a stage, in the order the file runs them, named
for its script and its arguments: `01_parse`, `02_fetch--force`, `12_scout`, `12_scout--follow-renames`.
A list kept here would be a second copy of the pipeline order, and the first time a stream added a stage to
the workflow and not to the copy, a local run would quietly stop reproducing CI. So adding a stage to the
daily is adding a line to `daily.yml` -- see `handbook/ci-cd.md` -- and this picks it up with no change.

What it leaves out, and why:

  - the workflow's own shell: the cache restore, the gate, "Every tracked page was rewritten", staging,
    photographing, committing and pushing. They are about the runner and the branch, not about the stages.
  - anything that publishes or records: `26_indexnow.py` (it tells Bing and others to fetch live URLs) and
    `watch_sources.py --update` (it records the source SHAs as built). A laptop must not do either.
  - the verification suite (`node tests/run.mjs`), unless `--with-suite`, and then under `AAA_SKIP` as the
    workflow sets it. The team rule is not to run the whole browser suite on a shared machine; with
    `AAA_ONLY=a.mjs,b.py` set in your environment it runs just those.
  - weekly's screenshots (`05_shots`, `06_web_shots`, `15_shots_all`, `15b_shots_sources`) need Playwright and
    hours. They are listed and run if you name them, but `--skip-shots` is the default for `--workflow weekly`.

THE CACHE

The stages read and write `cache/` at the repository root (gitignored), as on the runner. A cold one makes the
fetch stages do a full crawl -- about 1,200 GraphQL points and 800 REST requests at today's size, through your
own `gh` login -- and makes the shot-dependent pages fall back to Open Graph cards. `--cache DIR` points
`cache/` at a directory you keep between worktrees (a symlink, or a junction on Windows), so a second worktree
does not crawl again. Nothing here downloads the runner's cache: GitHub offers no API for that.

WHAT IT CHANGES

The stages write `docs/`, `mega-list/` and `state/` in this working tree, exactly as on the runner, and this
says so at the end with a count. `git restore docs mega-list state` (and `git clean -fd docs mega-list`) puts
them back. Run it in your own worktree, not someone else's.

  python tools/local_daily.py --list                       the stages, in order, with the step each is in
  python tools/local_daily.py                              all of them
  python tools/local_daily.py --from 10_parse_sources      that stage and everything after it
  python tools/local_daily.py --only 10_parse_sources      just that one (repeatable, comma-separated)
  python tools/local_daily.py --from 17_markdown --to 22_detail
  python tools/local_daily.py --workflow weekly --only 23_og
  python tools/local_daily.py --dry-run --from 19_pages    print the commands, run nothing

A stage can be named by its full name or by its script alone (`12_scout` is its first run). On a failure it
stops and prints the `--from` that resumes at the stage that failed.
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
# Stages that talk to the outside world on the site's behalf, or record a build as done. Never run locally.
NEVER = [re.compile(p) for p in (r"^python scripts/26_indexnow\.py", r"^python scripts/watch_sources\.py --update")]
SHOTS = {"05_shots", "06_web_shots", "15_shots_all", "15b_shots_sources"}


@dataclass
class Stage:
    name: str      # 02_fetch--force
    script: str    # 02_fetch
    command: str   # python scripts/02_fetch.py --force
    step: str      # the workflow step it is in
    line: int      # its line in the workflow file


# `node tests/run.mjs || status=$?` is how both workflows run the suite: the status is read, not propagated.
# `within ` is weekly's deadline wrapper for the screenshot stages; locally there is no deadline.
COMMAND = re.compile(r"^(?:within )?(python scripts/(\S+?)\.py(?:\s+([^|]*?))?|node tests/run\.mjs)\s*(\|\| status=\$\?)?$")


def stages(workflow: Path) -> list[Stage]:
    """Every stage command in `workflow`'s `run:` blocks, in file order.

    Not a YAML parser, and it does not need to be one: what it reads is the shape these workflows are written
    in -- `- name:` opens a step, `run: |` opens a block, the block is everything indented deeper, and
    `run: <command>` is a block of one line. Comment
    lines and anything that is not a bare `python scripts/...` or `node tests/run.mjs` line are ignored, so a
    command inside an `if` or a heredoc is not a stage. `tests/ci_tools_test.py` asserts that the daily's
    stages come out as the list the handbook describes, so a reshaped workflow fails there, not here.
    """
    out: list[Stage] = []
    step, block_indent = "", None
    lines = workflow.read_text(encoding="utf-8").splitlines()
    for n, raw in enumerate(lines, 1):
        indent = len(raw) - len(raw.lstrip(" "))
        text = raw.strip()
        m = re.match(r"^- name:\s*(.+)$", text)
        if m:
            step, block_indent = m.group(1).strip().strip('"'), None
            continue
        if re.match(r"^-\s", text) and block_indent is not None and indent <= block_indent:
            step, block_indent = "", None  # an unnamed step (`- uses:`, `- run:`)
        if re.match(r"^(- )?run:\s*\|", text):
            block_indent = indent
            continue
        inline = re.match(r"^(- )?run:\s*(\S.*)$", text)
        if inline:
            block_indent = None
            text = inline.group(2)  # a one-line step: `run: python scripts/12_scout.py`
        elif block_indent is not None and text and indent <= block_indent:
            block_indent = None
            continue
        elif block_indent is None or text.startswith("#"):
            continue
        c = COMMAND.match(text)
        if not c:
            continue
        if c.group(1).startswith("node"):
            out.append(Stage("suite", "suite", c.group(1), step, n))
            continue
        script, args = c.group(2), (c.group(3) or "").strip()
        # Named for the script and its flags, not their values: `02_fetch--force`, `12_scout--follow-renames`.
        name = script + "".join(a if a.startswith("--") else "" for a in shlex.split(args))
        out.append(Stage(name, script, c.group(1), step, n))
    return out


def pick(all_: list[Stage], key: str) -> int:
    """The index of the stage `key` names: its full name, else the first stage running that script."""
    for i, s in enumerate(all_):
        if s.name == key:
            return i
    for i, s in enumerate(all_):
        if s.script == key or s.script == key.removesuffix(".py"):
            return i
    raise SystemExit(f"no stage called {key!r}. The stages are: " + ", ".join(s.name for s in all_))


def plan(all_: list[Stage], start: str | None, stop: str | None, only: list[str], suite: bool,
         shots: bool) -> list[Stage]:
    """Which stages run, in order. `--only` wins over `--from`/`--to`; the denylist wins over everything."""
    if only:
        chosen = [all_[pick(all_, k)] for k in only]
    else:
        lo = pick(all_, start) if start else 0
        hi = pick(all_, stop) if stop else len(all_) - 1
        chosen = all_[lo:hi + 1]
        if not suite:
            chosen = [s for s in chosen if s.name != "suite"]
        if not shots:
            chosen = [s for s in chosen if s.script not in SHOTS]
    return [s for s in chosen if not any(p.match(s.command) for p in NEVER)]


def link_cache(target: str) -> None:
    """Point `cache/` at `target`, once. Refuses to replace a real cache directory -- one with any file in it.

    An empty one is replaced: running the tests in a fresh worktree leaves a `cache/` holding nothing but empty
    directories (a harness that imports a stage creates `cache/readmes/`), and refusing that would make
    `--cache` fail in exactly the fresh worktree it is for."""
    cache, dest = ROOT / "cache", Path(target).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    if cache.is_symlink() or cache.is_junction() or (cache.exists() and cache.resolve() == dest):
        return
    if cache.is_dir() and not any(p.is_file() for p in cache.rglob("*")):
        shutil.rmtree(cache)
    if cache.exists():
        raise SystemExit(f"cache/ already exists here and is not a link to {dest}; move it aside first")
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(cache), str(dest)], check=True, capture_output=True)
    else:
        cache.symlink_to(dest, target_is_directory=True)
    print(f"cache/ -> {dest}")


def run(stage: Stage, env: dict) -> int:
    argv = shlex.split(stage.command)
    argv[0] = sys.executable if argv[0] == "python" else argv[0]
    return subprocess.run(argv, cwd=ROOT, env=env).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workflow", default="daily", help="daily (default) or weekly, or a workflow file name")
    ap.add_argument("--from", dest="start", help="start at this stage")
    ap.add_argument("--to", dest="stop", help="stop after this stage")
    ap.add_argument("--only", action="append", default=[], help="run only these (repeatable, comma-separated)")
    ap.add_argument("--list", action="store_true", help="print the stages and exit")
    ap.add_argument("--dry-run", action="store_true", help="print the commands, run nothing")
    ap.add_argument("--with-suite", action="store_true", help="also run node tests/run.mjs where the workflow does")
    ap.add_argument("--with-shots", action="store_true", help="weekly: also run the screenshot stages")
    ap.add_argument("--cache", help="keep cache/ in this directory (linked into the worktree)")
    a = ap.parse_args()

    name = a.workflow if a.workflow.endswith(".yml") else a.workflow + ".yml"
    wf = WORKFLOWS / name
    if not wf.exists():
        raise SystemExit(f"no workflow {wf}")
    all_ = stages(wf)
    if a.list:
        step = None
        for s in all_:
            if s.step != step:
                print(f"\n{s.step or '(unnamed step)'}")
                step = s.step
            skipped = " (never run locally)" if any(p.match(s.command) for p in NEVER) else ""
            print(f"  {s.name:<34} {s.command}{skipped}")
        return 0

    only = [k for o in a.only for k in o.split(",") if k]
    todo = plan(all_, a.start, a.stop, only, a.with_suite, a.with_shots or name != "weekly.yml")
    if a.dry_run:
        for s in todo:
            print(s.command)
        return 0
    if a.cache:
        link_cache(a.cache)

    env = dict(os.environ)
    if any(s.name == "suite" for s in todo) and not env.get("AAA_ONLY"):
        env.setdefault("AAA_SKIP", "bits-check.mjs")  # as the workflow sets it
    t0 = time.monotonic()
    for i, s in enumerate(todo, 1):
        print(f"\n=== [{i}/{len(todo)}] {s.name}   ({s.step}, {name}:{s.line})", flush=True)
        t = time.monotonic()
        code = run(s, env)
        print(f"=== {s.name}: exit {code} in {time.monotonic() - t:.0f}s", flush=True)
        if code:
            print(f"\nstopped at {s.name}. Resume with: python tools/local_daily.py --workflow "
                  f"{a.workflow} --from {s.name}")
            return code
    changed = subprocess.run(["git", "status", "--porcelain", "--", "docs", "mega-list", "state"], cwd=ROOT,
                             capture_output=True, text=True).stdout.count("\n")
    print(f"\n{len(todo)} stage(s) green in {time.monotonic() - t0:.0f}s. {changed} path(s) under docs/, "
          "mega-list/ and state/ differ from HEAD; `git restore docs mega-list state` undoes them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
