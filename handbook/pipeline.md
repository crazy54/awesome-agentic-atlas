# The data pipeline

The pipeline is a set of Python scripts in `scripts/`:

- **Numbered stages**, run in order by the workflows.
- **Helper modules**, imported by the stages.

Numbers are not contiguous:

- There is no 12, and nothing between 27 and 30.
- Some stages carry letter suffixes: `03b`, `15b`, `19b`, `19c`, `19d`.
- Two unrelated stages share the number 25.

To count the numbered files:

```bash
ls scripts/*.py | xargs -n1 basename | grep -cE '^[0-9]'
```

That gave 34 on 2026-09-25, plus 19 helper modules.

Stages load each other with `importlib.util.spec_from_file_location`, because a module name that
starts with a digit cannot be imported normally. Helpers are imported the ordinary way.

**Fresh clone?** in the tables below means whether the script can run with no `cache/` directory, which is
the state of every checkout except a CI runner with a restored cache. "Yes" means it reads only committed
files. "No" means it opens something under `cache/` and stops without it.

The module docstrings are the detailed documentation. Read the one at the top of a stage before changing it.

## Fetch and classify (CI only)

| Script | What it does | Reads | Writes | Fresh clone? |
|---|---|---|---|---|
| `pull_sources.py` | Downloads each source list from `raw.githubusercontent.com`, but only if its head commit moved. Diffs old and new copies *by parsed entry*, not by line. Refuses a pull that shrank drastically | GitHub; `cache/sources/index.json` | `cache/README.md`, `cache/sources/*.md`, `cache/sources/index.json`, `cache/pull-report.json`, `cache/collect-queue.json`; sets `pulled`/`changed`/`failed` outputs | Yes; this is how a cache is started. `--status` makes no network calls |
| `watch_sources.py` | Asks each list for its newest commit and compares it with the ledger in `state/first-seen.json` | `gh api repos/{nwo}/commits` | `GITHUB_OUTPUT` `changed`, `moved`. With `--update` it also writes `state/first-seen.json` | Yes |
| `01_parse.py` | Parses the original list (andyrewlee/awesome-agent-orchestrators) | `cache/README.md` | `cache/entries.json` | No |
| `02_fetch.py` | Batched GraphQL for stars, language, licence and README, with a REST fallback | `cache/entries.json`; `gh api` | `cache/meta.json`, `cache/readmes/` | No |
| `03_releases.py`, `03b_actions.py` | Release asset names; whether the repo is a GitHub Action | `cache/entries.json`, `cache/meta.json`; `gh api` | `cache/releases.json`, `cache/actions.json` | No |
| `04_classify.py` | OS verdicts, install command and screenshot candidates for the original list | the four files above plus `cache/readmes/` | `cache/records.json` | No |
| `10_parse_sources.py` | **Defines `SOURCES`**, the list of source lists. Parses every list except `orchestrators` (which goes through `01`/`04`). Fails on a section heading it cannot map to a topic | `cache/sources/*.md` | `cache/entries_all.json` | No; it says to run `pull_sources.py` first |
| `11_fetch_all.py` | Runs 02's batching over every distinct repo | `cache/entries_all.json`, `cache/meta.json` | `cache/meta.json`, `cache/readmes/` | No |
| `13_signals_all.py` | Releases and actions for every repo in one pass. The staleness rule is in `signals.py` | as above | `cache/releases.json`, `cache/actions.json` | No |
| `14_classify_all.py` | The final record per listed item, of kind `repo`, `subpath` or `site` | everything above | `cache/records_all.json` | No |

## Screenshots and workbooks (weekly only)

| Script | What it does | Reads | Writes | Fresh clone? |
|---|---|---|---|---|
| `05_shots.py`, `06_web_shots.py` | Screenshots for the original list: first the README image, then a live capture in headless Chromium | `cache/records.json` | `cache/shots/`, `cache/shots.json` | No |
| `15_shots_all.py` | Four-tier images for every record: README image, then `og:image`, then a live capture, then a generated card. Drains `cache/collect-queue.json` | `cache/records_all.json` | `cache/shots/`, `cache/shots_all.json`, and **`cache/shots_all.done.json`**, the completion marker that the daily gate checks | No |
| `15b_shots_sources.py` | A repo card for each source list | `SOURCES` | `cache/shots_all.json` | No |
| `16_build_all.py` | The combined workbook in two themes, with 21 sheets each (see its "Sheet plan" docstring and `main()`) | the whole cache; `docs/icon-192.png`, `docs/assets/atlas-byte.png` | `Awesome-Agentic-Atlas-{DARK,LIGHT}.xlsx` at the repo root (gitignored; published as release assets) | No. `--brand-existing` re-brands existing workbooks without the cache |
| `18_slicers.py` | Injects Excel slicers into "By Category" | both workbooks | the workbooks in place; `--probe` writes `slicer-probe.xlsx`, which is **not** gitignored | Needs workbooks. **No workflow runs it** |
| `07_build.py`, `08_verify.py`, `09_pdf.py` | The legacy orchestrators-only workbook, a check that opens it in real Excel, and a PDF preview | `cache/records.json` | `Awesome-Agent-Orchestrators-*.xlsx`, `preview/*.pdf` | No. 08 and 09 need Windows with Excel. No workflow runs them |

## Site and Markdown

| Script | What it does | Reads | Writes | Fresh clone? |
|---|---|---|---|---|
| `17_markdown.py` | The Markdown edition. Stamps new arrivals into the first-seen ledger | `cache/records_all.json`, `meta.json`, `records.json`; `docs/CNAME` | `mega-list/**` (except `collections/`); `state/first-seen.json` | No |
| `check_markdown.py` | Lints `mega-list/` for five silent failures, including pages over GitHub's 512 KB rendering limit | `mega-list/**/*.md` | nothing | Yes |
| `19_pages.py` | **The catalogue page and the dataset** | the three cache files above | `docs/catalog/index.html`, `docs/data.json`, `docs/.nojekyll`; `state/first-seen.json` | No; see `devfixture.py` below |
| `25_velocity.py` | Star-velocity ledger. Appends a sample on a 7-day grid and patches `d7`, `d30` and `velocity` into `data.json` | `state/star-history.json`, `docs/data.json` | both, in place | Yes (`--status`, `--dry-run`) |
| `19c_live.py` | `live.json`, the small star/push sidecar that detail pages fetch instead of the full dataset | `docs/data.json` | `docs/live.json` | Yes |
| `19d_discover.py` | Discover: fifty projects a day for seven days, chosen from every category and blind to stars. Selection rules are in `discover.py` | `docs/data.json`, `state/discover.json` | `docs/discover.json`, `docs/discover/index.html`, `state/discover.json` | Yes (`--out`, `--day`) |
| `20_landing.py` | The topic, target and topic×target facet pages. Also writes the shared stylesheet and the sitemap. Prunes pages that no longer exist | `docs/data.json`, `docs/og/*.png` | `docs/topic/**`, `docs/target/**`, `docs/pages.css`, `docs/sitemap.xml`, `docs/robots.txt`, the IndexNow key file | Yes |
| `21_feeds.py` | Atom and JSON feeds of arrivals | `docs/data.json`, `state/first-seen.json` | `docs/feed.xml`, `docs/feed.json` | Yes |
| `22_detail.py` | One page per repo, plus the directory page. Slugs names so that Windows can check them out | `docs/data.json` | `docs/repo/**`, `docs/sitemap-repos.xml` | Yes (`--out`, `--data`) |
| `25_collections.py` | The curated collections. **Fails the build** if a pick's claim no longer holds | `config/collections.json`, `docs/data.json` | `docs/collections/**`, `mega-list/collections/*.md` | Yes. Runs in the weekly build only |
| `23_og.py` | Open Graph preview PNGs, rendered in Chromium | `docs/data.json` | `docs/og/*.png`, `docs/og/cards.json` | Needs Chromium. Outside GitHub Actions it requires `--out DIR` or `--local` |
| `31_home.py` | **The homepage** (`/`): shelves, the spotlight, the Discover strip, and Archie. Adds `?v=` cache-busters to Archie's scripts | `docs/data.json`, `docs/discover.json`, `docs/pages.css`, `docs/assets/*`; imports `30_v2.py` | `docs/index.html`, `docs/build.json`, `docs/discover/cards/*.json` | Yes (`--out`) |
| `24_pwa.py` | Manifest, icons and the service worker. The worker's `VERSION` is a hash of the precached files | `docs/index.html`, `docs/pages.css`, `docs/manifest.webmanifest` | `docs/sw.js`, `docs/manifest.webmanifest`, icons | Yes. **Run it after anything that rewrites `docs/index.html` or `docs/pages.css`** |
| `27_semantic.py` | The offline semantic search index for the catalogue | `docs/data.json`; `cache/readmes/` if present; downloads a model into `cache/m2v` | `docs/search/*` | Partly: needs numpy and network access. READMEs are optional |
| `26_indexnow.py` | Submits changed URLs to IndexNow | a `--changed` file (git name-status) | nothing (it makes a network POST) | Yes (`--dry-run`) |
| `30_v2.py` | The redesign prototype. Its card system is also imported by `31_home.py` | `docs/data.json` | `docs/v2/**` only | Yes. **Runs on demand only**; no workflow runs it |

### Helper modules

| Module | Role |
|---|---|
| `taxonomy.py` | The 14 topics and 12 targets, and the rules that assign them. `python scripts/taxonomy.py --why OWNER/REPO` explains an assignment (needs the cache) |
| `buckets.py` | Folds a list's sections into at most eight colour groups for the workbook |
| `signals.py` | Decides when a cached release or action answer must be re-queried |
| `newness.py` | The first-seen ledger and the "New" cohort rule. Running it with no arguments prints a read-only report |
| `discover.py` | Discover's selection rule and rotation ledger. `python scripts/discover.py [DAY]` prints a plan and writes nothing |
| `app_flags.py`, `apply_flags.py`, `flags_app.py` | Feature flags: the validator, a re-render after an edit, and a local web editor. See [frontend.md](frontend.md#feature-flags) |
| `chrome.py` | Finds a headless Chromium: `CHROME_PATH`, `CHROMIUM_PATH`, `PLAYWRIGHT_CHROMIUM`, then Playwright caches, then `PATH` |
| `media.py` | Deduplicates workbook images so one picture is stored once |
| `pagemin.py` | Strips comments from generated pages |
| `mark.py`, `osicons.py` | Shared SVG marks: the Archie globe and the five platform icons |
| `masthead_art.py` | Draws `docs/assets/masthead-{dark,light}.webp`. Run by hand only |
| `try_source.py` | Works out a parse strategy for a candidate new source list. Writes to `cache/candidates/` |
| `devfixture.py` | Rebuilds the cache files `19_pages.py` needs, from the committed `docs/data.json` (see below) |

## Working without the cache

A normal checkout has no `cache/`, so `19_pages.py` and everything before it cannot run. There are
three ways round that.

- **Regenerate only what reads `docs/data.json`.** Stages `19c`, `19d`, `20`, `21`, `22`, `25_collections`,
  `25_velocity`, `31` and `24` all run on a checkout. Most take `--out DIR`, so you can render into
  scratch and diff the result without touching `docs/`.
- **`scripts/devfixture.py`** reconstructs `cache/records_all.json`, `meta.json` and `records.json` by
  inverting `docs/data.json`. It then hands them to the real `19_pages.main()`. It writes under
  `build-tmp/devfixture` and refuses any output path inside `cache/`, `docs/`, `state/`, `mega-list/`,
  `scripts/` or `tests/`.

  ```bash
  python scripts/devfixture.py                   # report what it would do, touch nothing
  python scripts/devfixture.py --build           # write the fixture and render the catalogue
  python scripts/devfixture.py --build --verify  # ...and compare the result with docs/data.json
  ```

- **`scripts/19b_refresh.py`** re-renders the page shell over the committed rows, and refuses when those
  rows disagree with the checkout's `SOURCES`. It writes the catalogue at `docs/catalog/index.html`
  (`19_pages.CATALOG`), not `docs/index.html`, which is the homepage.

## Order matters

The workflows run the site stages in this order. Some stages read the output of earlier ones, so keep the order:

```
17_markdown → check_markdown → 19_pages → 25_velocity → 19c_live → 19d_discover → 20_landing
  → 21_feeds → 22_detail → [25_collections → 23_og, weekly only] → 31_home → 24_pwa → 27_semantic
```

The dependencies behind that order:

- `25_velocity` patches `data.json` after `19_pages` writes it.
- `31_home` reads `discover.json` and `pages.css`, so it runs after `19d_discover` and `20_landing`.
- `24_pwa` hashes `index.html` and `pages.css`, so it runs **after** everything that writes them.

## Adding a source list

1. Try the list with `scripts/try_source.py --nwo OWNER/REPO`, which reports how it would parse. Flags
   for awkward layouts are listed in its `--help`.
2. Add an entry to `SOURCES` in `scripts/10_parse_sources.py`, and map any new section headings to a topic.
   `10_parse_sources.py` fails loudly on a heading it cannot map.
3. The next CI run pulls the list, fetches its repos and publishes it. The count of lists shown on every
   surface is derived, so there is nothing else to edit. The root README's hand-written figures are the
   exception; see [keeping-docs-current.md](keeping-docs-current.md).
