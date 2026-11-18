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
| `12_scout.py` | The one source nobody curates. GitHub search for rising agentic repos (created in the last 180 days with 300+ stars, or 2,000+ stars since 2023 on core topics), filtered for forks, mirrors, spam and off-topic SEO, filed by topic into atlas categories. Sticky: a scouted repo leaves only when search returns it failing a quality rule. Also lists awesome-lists not yet in `SOURCES`. A failed search changes nothing | GitHub search; `state/scout-repos.json`, `state/scout-lists.json` | `state/scout-repos.json`, `state/scout-lists.json`, `cache/sources/scout.md`; `$GITHUB_STEP_SUMMARY` | Yes; `--offline` renders the document from the committed ledger with no network |
| `watch_sources.py` | Asks each list for its newest commit and compares it with the ledger in `state/first-seen.json`. For the scout, which has no commit, it compares the document's SHA-256 instead | `gh api repos/{nwo}/commits`; `cache/sources/scout.md` | `GITHUB_OUTPUT` `changed`, `moved`. With `--update` it also writes `state/first-seen.json` | Yes |
| `01_parse.py` | Parses the original list (andyrewlee/awesome-agent-orchestrators) | `cache/README.md` | `cache/entries.json` | No |
| `02_fetch.py` | Batched GraphQL for stars, language, licence and README, with a REST fallback | `cache/entries.json`; `gh api` | `cache/meta.json`, `cache/readmes/` | No |
| `03_releases.py`, `03b_actions.py` | Release asset names; whether the repo is a GitHub Action | `cache/entries.json`, `cache/meta.json`; `gh api` | `cache/releases.json`, `cache/actions.json` | No |
| `04_classify.py` | OS verdicts, install command and screenshot candidates for the original list | the four files above plus `cache/readmes/` | `cache/records.json` | No |
| `10_parse_sources.py` | **Defines `SOURCES`**, the list of source lists. Parses every list except `orchestrators` (which goes through `01`/`04`). Fails on a section heading it cannot map to a topic | `cache/sources/*.md` | `cache/entries_all.json` | No; it says to run `pull_sources.py` first |
| `11_fetch_all.py` | Runs 02's batching over every distinct repo | `cache/entries_all.json`, `cache/meta.json` | `cache/meta.json`, `cache/readmes/` | No |
| `13_signals_all.py` | Releases and actions for every repo in one pass. The staleness rule is in `signals.py` | as above | `cache/releases.json`, `cache/actions.json` | No |
| `14_classify_all.py` | The final record per listed item, of kind `repo`, `subpath` or `site`. Leaves out every row whose repo is in the dead-repo ledger, so a repo GitHub no longer serves is on no surface | everything above; `state/dead-repos.json` | `cache/records_all.json` | No |
| `dead_repos.py` | **Not a build stage**: run weekly by `dead-repos.yml`. Asks GitHub about every repo in `docs/data.json` and every repo already in the ledger, and records the ones that are gone: GraphQL `NOT_FOUND` and then REST 404, 451 or a 403 `block`, or `isDisabled`. Renamed and archived repos are alive. A repo that answers again leaves the ledger. Writes nothing if any request fails for a reason that is not about the repo, or if the scan would newly mark more than 10% of the atlas (at least 25) dead | `docs/data.json`, `state/dead-repos.json`; `gh api` | `state/dead-repos.json`; `$GITHUB_STEP_SUMMARY` | Yes; `--status` reads the ledger with no network, `--dry-run` scans and writes nothing |

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

## The models index

The atlas's second dataset: open-weight models from the Hugging Face Hub, for the models catalogue
(`docs/models/`) and the local-AI page. It is independent of the GitHub stages above. It reads no part of
`cache/` except its own `cache/hf/`, and nothing else reads its output except those two pages.

| Script | What it does | Reads | Writes | Fresh clone? |
|---|---|---|---|---|
| `40_models.py` | Lists the Hub (every trusted quantiser's repos, the top of each relevant pipeline by downloads, likes and trending, and the top GGUF/MLX/AWQ/GPTQ repos), fetches the base models the quant repos name, keeps the models worth listing, then reads each kept model's info, `config.json` and file tree, and every variant's tree. Matches Ollama library tags. Refuses to write a file with under 70% of the committed model count | Hub API; ollama.com; `config/models.json`; `cache/hf/` | `docs/models.json`; `cache/hf/**`; `$GITHUB_STEP_SUMMARY` | Yes, with network. `--offline` builds from `cache/hf/` only; `--status` validates and reports on the committed file; `--dry-run` writes nothing |
| `41_models_page.py` | The models catalogue: the most used models as HTML for first paint, then the whole index with filters (use, size, format, licence kind, family, search) from `models.json`. Each card opens into every variant's quantisations, exact sizes and a run command. Its URL reaches `docs/sitemap.xml` through `20_landing.models_urls()`, as Discover's does | `docs/models.json` | `docs/models/index.html` | Yes |

| Helper | Role |
|---|---|
| `hf_hub.py` | The Hub client: a cache under `cache/hf/` keyed on each repo's `sha`, a throttle that reads the `RateLimit` header and waits before the window runs out, retries on 429 and 5xx, and a GGUF header parser for gated models whose `config.json` cannot be read anonymously |
| `models.py` | Every rule: what a repo is (`variant_format`), which model it belongs to (`resolve`), what is kept (`keep`), quant labels and summed split sizes (`gguf_files`), fit inputs (`dims_from_config`, `dims_from_gguf`, `active_from_config`), Ollama matching, and the schema with its validator (`validate`) |

### What a row is

One row per **model** (an official repo id), carrying its **variants** (repos that ship those weights in a
runnable format), each carrying one **file** row per quantisation with its exact bytes. Ten quant repos of
one model are one row with ten variants: every GGUF/MLX/AWQ/GPTQ/bitsandbytes/FP8 repo is attached through
its card's `base_model`, walking through quantisers' plain re-uploads (`unsloth/Qwen3-8B`). Only the model's
own author and the quantisers listed in `config/models.json` are attached.

Cards are not always right, and the first real build found each of these (`tests/models_test.py` holds
a fixture for every one):

- **A fine-tune's quant whose card names the root model** (`bartowski/bagel-8b-v1.0-GGUF` says
  `Meta-Llama-3-8B`). A variant attaches only if its own name, less format suffixes, is the model's name
  (`models.same_weights`). If it is not, it is re-homed to the one model that does have its name, or left out.
- **Renamed repos.** A card naming `Meta-Llama-3.1-8B-Instruct` is answered under `Llama-3.1-8B-Instruct`.
  The row is filed under the new name only.
- **Files that share a quant label with the model and are not it.** Speculative-decoding drafts
  (`MTP/`, `mtp-`, `eagle3-`, `dflash-`, `dspark-`, and the pattern `{prefix}-{Model}-{quant}.gguf`),
  projectors, imatrix data, and one quant shipped both whole and split. Of two file sets with one label,
  the largest is kept, and the whole-file copy over the split one. A file row under 1 bit per weight is
  dropped, whatever the cause.

The schema is in `models.COLS`, `VARIANT_COLS` and `FILE_COLS`, and its full description for consumers is
the team contract `team/contracts/models.md`. **Changing a column is a schema change.** Bump
`SCHEMA_VERSION`, update the contract and this page, tell the local-AI page's authors, and update the
frozen copy in `tests/models_test.py`, which fails until all of them agree. The stage validates before it
writes, and the test validates the committed file, so a broken shape fails the build instead of the page.

### The keep rule

In order (`models.keep`): NSFW-tagged repos, adapters and off-topic pipelines are out; so are empty cards,
merges with under 300 likes, text models under 50M parameters or with under a 4,096-token context, and
repos idle for two years with under 20,000 downloads a month. What remains is kept if it is popular
(100,000 monthly downloads across its variants, or 300 likes), from a lab (configured, or any author with a
200,000-download root model) with some use, or a community model with a trusted quant and 10,000 downloads
or 50 likes. Uncensored fine-tunes that pass are kept with the `uncensored` flag.

### Cost, freshness and a token

Anonymous reads allow 500 API calls and 3,000 file resolves per five minutes per IP. A cold cache costs
about 9,800 API calls and 2,300 resolves, about 100 minutes (measured 2026-11-18: 7,593 trees, 2,230 model
infos, 936 base-model fetches, 46 listing pages). That is the weekly step's whole cap (`timeout-minutes: 100`), so the
build is **resumable**: every answer is written to `cache/hf/` as it arrives, keyed on the repo's `sha`,
and `cache/` is banked even when the step fails. `--deadline-minutes 92` makes the stage stop asking
before the cap and exit 3 without writing anything. The next run replays the cache at disk speed and
fetches only what the last one did not reach (checked 2026-11-18: 20 deleted trees, a stopped run, then
a full run that made 24 API calls). In weekly.yml the step sits after "Fetch and classify" and before
"Capture screenshots", whose deadline is computed from the time left, so the models step's time
comes out of the screenshots' budget and never the workbooks'. A warm one re-reads a tree or config only when
the repo's `sha` moved, so a weekly run is the ~45 listing pages, the base-model infos (kept for six days),
and whatever changed. An `HF_TOKEN` secret would raise the API quota, and would let configs be read from
gated repos whose licence that account has accepted. Without one, those models' `dims` come from an
ungated mirror or variant, or from a GGUF header (a 512 KB range read).

### Ollama

Ollama publishes no mapping from its library to Hugging Face, so `ollama` on a row is a match with a
confidence. Library names and size tags come from `ollama.com/library` (HTML, the least stable input; a
parse with under 50 models is treated as a broken page and the column is left empty for the run), and each
matched tag's model layer size comes from the `registry.ollama.ai` manifest. `match` is `verified` when that
size is within 3% of one of the row's GGUFs at the quant Ollama reports, `curated` for an override in
`config/models.json`, and `likely` for a name-and-size match nothing confirmed. Every GGUF variant can be
run with `ollama run hf.co/{repo}:{quant}` regardless.
