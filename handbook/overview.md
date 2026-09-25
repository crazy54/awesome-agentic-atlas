# Overview and architecture

## What the project is

Awesome Agentic Atlas merges thirty-nine curated "awesome" lists about agentic AI into one deduplicated
catalogue. Each project gets its GitHub metadata (stars, language, licence, last push), an install
command, a screenshot, a topic, the harnesses it plugs into, and a per-OS verdict for Windows, WSL2,
macOS, Linux and Docker.

The number of lists is `len(SOURCES)` in `scripts/10_parse_sources.py`. It was 39 on 2026-09-25. To measure it:

```bash
python -c "import importlib.util as u; s=u.spec_from_file_location('m','scripts/10_parse_sources.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(len(m.SOURCES))"
```

## The published surfaces

| Surface | Where it lives | Built by | Rebuilt |
|---|---|---|---|
| The website | `docs/`, served at <https://aaa.jeremyfhall.com> | stages 19 to 31 | daily and weekly |
| The JSON dataset | `docs/data.json` (documented in the root [README](../README.md#the-data-as-an-api)) | `19_pages.py`, patched by `25_velocity.py` | daily and weekly |
| The Markdown edition | `mega-list/` | `17_markdown.py` (plus `25_collections.py` for `mega-list/collections/`) | daily and weekly |
| The Excel workbooks, dark and light | GitHub release assets, never committed | `16_build_all.py` | weekly only |

All of these come from the same in-memory records, and every topic and target assignment comes from
the single vocabulary in `scripts/taxonomy.py`. That is why the three surfaces cannot disagree about
which topic a project is filed under.

## How data flows

```
source lists on GitHub
   │  pull_sources.py        pulls only lists whose head commit moved          → cache/sources/
   │  10_parse_sources.py    parses every list into rows (01_parse.py for the original list)
   │  11_fetch_all.py        GitHub GraphQL: stars, language, licence, README  → cache/meta.json, cache/readmes/
   │  13_signals_all.py      release assets and action.yml                      → cache/releases.json, actions.json
   │  14_classify_all.py     OS verdicts, install line, kind                    → cache/records_all.json
   │  15_shots_all.py        screenshots (weekly only)                          → cache/shots/
   ▼
cache/  (untracked; restored from the GitHub Actions cache on CI)
   │  16_build_all.py        workbooks (weekly only)                            → *.xlsx, released
   │  17_markdown.py         Markdown edition                                   → mega-list/
   │  19_pages.py            catalogue page + dataset                           → docs/catalog/, docs/data.json
   ▼
docs/data.json  (committed)
   │  25_velocity, 19c_live, 19d_discover, 20_landing, 21_feeds, 22_detail,
   │  25_collections, 23_og, 31_home, 24_pwa, 27_semantic
   ▼
docs/  (committed; GitHub Pages serves it as-is)
```

This produces a hard split that shapes everything else:

- **Stages up to and including 19_pages need `cache/`**, which is not committed. It holds other people's
  READMEs and screenshots, it is large, and it can be rebuilt. On a fresh clone those stages stop with a
  message naming the stage to run first. Only CI has a warm cache. The exception is
  `scripts/devfixture.py`, which rebuilds the three cache files `19_pages.py` needs by inverting the
  committed `docs/data.json` (see [pipeline.md](pipeline.md#working-without-the-cache)).
- **Stages after 19 read the committed `docs/data.json`**, so most of them can run on any checkout.

The full per-script table is in [pipeline.md](pipeline.md).

## Committed state

Three kinds of file are committed and change on every build:

- `docs/`: the site. Almost all of it is generated.
- `mega-list/`: the Markdown edition. All generated.
- `state/`: ledgers that a rebuild **cannot** recreate, so they must be committed.
  - `state/first-seen.json` holds the date each repo first appeared in any list. That date is what "New" is computed from.
  - `state/star-history.json` holds star samples for the 7- and 30-day velocity columns.
  - `state/discover.json` holds the Discover rotation.

  All three are append-style ledgers. When one conflicts in a merge, keep both sides; never pick one.

Hand-written inputs that are not generated:

- `config/app-flags.json` and its schema: the feature flags. See [frontend.md](frontend.md#feature-flags) and [`config/README.md`](../config/README.md).
- `config/collections.json`: the curated collections.
- `docs/CNAME`: the Pages custom domain. `17_markdown.py` reads it to build absolute URLs.
- `docs/favicon.svg` and `docs/assets/atlas-byte.png`: hand-maintained art. `daily.yml` lists them as static.
- `docs/assets/archie*.js` and `docs/assets/rig-show.js`: Archie's code, written by hand. See [archie.md](archie.md).
- `art/`: Blender and Python sources for Archie and the stage rig.

## Directory layout

| Path | What it is |
|---|---|
| `scripts/` | The pipeline: numbered stages plus helper modules. See [pipeline.md](pipeline.md) |
| `docs/` | The published website. GitHub Pages serves it from `latest_branch` |
| `mega-list/` | The generated Markdown edition |
| `state/` | Committed ledgers (first-seen, star history, Discover rotation) |
| `config/` | Feature flags and curated collections |
| `tests/` | The verification suite. See [testing.md](testing.md) |
| `art/` | Blender and Python sources for `archie.glb`, `rig.glb` and the video-wall clips |
| `.github/workflows/` | `daily.yml`, `weekly.yml`, `tests.yml`, `lighthouse.yml`, `og-preview.yml`. See [ci-cd.md](ci-cd.md) |
| `docs-notes/` | Design notes that must not be published |
| `handbook/` | This documentation |
| `cache/`, `build-tmp/`, `preview/` | Untracked: the build cache, test scratch, and Excel PDF previews |

## Technology

- **Python 3** for the whole pipeline. CI uses 3.12. Most stages are standard library only.
  - `openpyxl` and `pillow` are needed by the workbook stages and two harnesses.
  - `numpy` is needed by `27_semantic.py`.
  - `playwright` is installed on the weekly run for screenshot capture.
- **The GitHub CLI (`gh`)** for every GitHub API call. The fetch stages shell out to `gh api graphql`.
- **No front-end build step.** The site is static HTML with inline CSS and JS written by Python generators.
  - The one bundled file is `docs/assets/three-archie.js`, a three.js subset built once with esbuild (see [archie.md](archie.md#the-threejs-bundle)).
  - There is no `package.json` anywhere in the repository.
- **Node 22 and a Chromium** for the test suite only. Nothing from npm is served to readers.
