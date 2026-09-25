# The Atlas handbook

This is the maintainers' documentation for Awesome Agentic Atlas: how the catalogue is built, tested,
published and changed. The root [README](../README.md) is for readers of the atlas. This directory is for
the people who work on it.

A note on where things live, because it is the first thing that trips people up: **`docs/` is the
published website, not documentation.** GitHub Pages serves it verbatim from `latest_branch`, and most
of it is written by generators. Project documentation lives here, in `handbook/`, which nothing
publishes and no generator touches.

## Contents

| Page | What it covers |
|---|---|
| [Overview and architecture](overview.md) | What the project is, the three published surfaces, how data flows from source lists to the site, and the directory layout |
| [The data pipeline](pipeline.md) | Every script in `scripts/`, stage by stage: what it reads, what it writes, and whether it can run on a fresh clone or needs CI's cache |
| [CI/CD and deployment](ci-cd.md) | Which branch deploys, the daily and weekly builds, the test, Lighthouse and OG-preview workflows, caches, releases and secrets |
| [The test suite](testing.md) | `node tests/run.mjs`, each harness and what it guards, how to run one alone, and the checks known to be flaky or environment-sensitive |
| [The website front end](frontend.md) | The page families, which generator owns each, themes and skins, feature flags, and the PWA and its service-worker versioning rule |
| [Archie, the mascot](archie.md) | The 3D model and its Blender source, animation clips, "Dance with me", the stage rig and effects, the admin panel, `?archie=` flags, and what to regenerate after an edit |
| [Contributor guide](contributing.md) | Branching, pull requests against `latest_branch`, generated vs hand-written files, and the Windows and Git Bash pitfalls |
| [Troubleshooting](troubleshooting.md) | Symptoms and their usual causes: red suites, skipped dailies, stale service workers, broken checkouts |
| [Keeping these docs current](keeping-docs-current.md) | Which page to update when which code changes, and the rules for numbers in prose |

Other documentation in the repository, each of which stays next to the thing it describes:

- [`tests/README.md`](../tests/README.md): the suite's design notes, which are longer than the summary in [testing.md](testing.md).
- [`config/README.md`](../config/README.md): the application flags and the curated collections file.
- [`docs-notes/`](../docs-notes/): a design note on analytics events. Kept outside `docs/` so Pages does not publish it.
- [`WORK-IN-PROGRESS.md`](../WORK-IN-PROGRESS.md): a handoff log from the September 2026 redesign. It is history, and says so at the top.
- Long module docstrings at the top of most files in `scripts/` and `tests/`. They are the most detailed
  documentation in the repository. This handbook summarises them and points at them; it does not replace them.

## How to read the numbers here

Counts in this handbook carry the date they were measured and, where it is not obvious, the command
that measures them. Counts in prose are how this repository has been misled before: a figure copied
forward from older prose becomes a baseline that a later check is compared against. If you need a
number, re-measure it. Don't trust the one written here. [keeping-docs-current.md](keeping-docs-current.md)
has the rules.

Unless a page says otherwise, figures were measured on 2026-09-25 against `latest_branch` at `a77b46eb`,
whose committed `docs/data.json` has snapshot `2026-09-22`.
