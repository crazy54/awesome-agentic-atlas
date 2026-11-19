# The data pipeline

The pipeline is a set of Python scripts in `scripts/`:

- **Numbered stages**, run in order by the workflows.
- **Helper modules**, imported by the stages.

Numbers are not contiguous:

- There is no 12, and nothing between 27 and 30.
- Some stages carry letter suffixes: `03b`, `19b`, `19c`, `19d`.
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
| `pull_sources.py` | Downloads each source list from `raw.githubusercontent.com`, but only if its head commit moved. Diffs old and new copies *by parsed entry*, not by line. Keeps the previous copy, and records nothing, when a pull fails, shrank to under a quarter of its bytes, or parses to under a quarter of its entries (`--force` accepts). Records which old section each new one came from, for drift placement. Reports a renamed list repo | GitHub; `cache/sources/index.json` | `cache/README.md`, `cache/sources/*.md`, `cache/sources/index.json`, `cache/pull-report.json`, `cache/collect-queue.json`, `cache/section-moves.json`; sets `pulled`/`changed`/`failed` outputs | Yes; this is how a cache is started. `--status` makes no network calls |
| `12_scout.py` | The one source nobody curates. GitHub search for rising agentic repos (created in the last 180 days with 300+ stars, or 2,000+ stars since 2023 on core topics), filtered for forks, mirrors, spam and off-topic SEO, filed by topic into atlas categories. Sticky: a scouted repo leaves only when search returns it failing a quality rule. Also lists awesome-lists not yet in `SOURCES`. A failed search changes nothing | GitHub search; `state/scout-repos.json`, `state/scout-lists.json` | `state/scout-repos.json`, `state/scout-lists.json`, `cache/sources/scout.md`; `$GITHUB_STEP_SUMMARY` | Yes; `--offline` renders the document from the committed ledger with no network |
| `12b_gitlab.py` | The GitLab scout: gitlab.com's public API asked for agentic projects by topic and by word, judged by rules modelled on the scout's (5+ stars and activity in the last year, or 25+ stars since 2023; forks, archives, spam, off-topic and above all **mirrors** of GitHub repos left out), filed by the scout's own `section_of`. Sticky like the scout. Without `GITLAB_TOKEN` it runs one rotation slice a day, because anonymous gitlab.com allows about 60 requests an hour per IP; a refused query adds nothing. Behind the `intake.gitlab` flag: off, it makes no request and writes an empty document. See [gitlab.md](gitlab.md) | gitlab.com REST and GraphQL; `state/gitlab-repos.json`, `docs/data.json` (for the mirror rule) | `state/gitlab-repos.json`, `cache/sources/gitlab.md`; `$GITHUB_STEP_SUMMARY` | Yes; `--offline` renders from the committed ledger, `--status` reads it |
| `watch_sources.py` | Asks each list for its newest commit and compares it with the ledger in `state/first-seen.json`. For the scout, which has no commit, it compares the document's SHA-256 instead | `gh api repos/{nwo}/commits`; `cache/sources/scout.md` | `GITHUB_OUTPUT` `changed`, `moved`. With `--update` it also writes `state/first-seen.json` | Yes |
| `01_parse.py` | Parses the original list (andyrewlee/awesome-agent-orchestrators) | `cache/README.md` | `cache/entries.json` | No |
| `02_fetch.py` | Batched GraphQL for stars, language, licence and README, with a REST fallback | `cache/entries.json`; `gh api` | `cache/meta.json`, `cache/readmes/` | No |
| `03_releases.py`, `03b_actions.py` | Release asset names; whether the repo is a GitHub Action | `cache/entries.json`, `cache/meta.json`; `gh api` | `cache/releases.json`, `cache/actions.json` | No |
| `04_classify.py` | OS verdicts, install command and screenshot candidates for the original list | the four files above plus `cache/readmes/` | `cache/records.json` | No |
| `10_parse_sources.py` | **Defines `SOURCES`**, the list of source lists. Parses every list except `orchestrators` (which goes through `01`/`04`). On a section heading it cannot map to a topic, or a list wanting a ninth colour: strict (the default) exits 1; provisional (`AAA_PROVISIONAL=1`, set by both workflows) files it for the run and warns. See [Upstream drift](#upstream-drift) | `cache/sources/*.md`, `cache/section-moves.json`, `cache/pull-report.json` | `cache/entries_all.json`, `cache/drift-proposal.json` and `.md`; `cache/provisional.json` on a provisional run with drift; annotations and `$GITHUB_STEP_SUMMARY` | No; it says to run `pull_sources.py` first |
| `11_fetch_all.py` | Runs 02's batching over every distinct repo. If more than max(50, 10%) of the repos it asked about failed for a reason other than the repo being gone, it retries the rate-limited and transient ones (after 1, 4 and 15 minutes, or at GitHub's reported reset, capped at 15) and stops only if they still fail. An auth failure (401, bad credentials) stops at once, because no wait fixes a token | `cache/entries_all.json`, `cache/meta.json` | `cache/meta.json`, `cache/readmes/` | No |
| `11b_fetch_gitlab.py` | The GitLab rows `11` skips: one anonymous GraphQL request per 25 projects, written into `meta.json` under GitHub's field names (`stargazerCount`, `pushedAt` = `lastActivityAt`, `licenseInfo` recognised from the LICENSE text) so every later stage reads them unchanged. Keeps the last good answer per project in `cache/gitlab/meta.json` and uses it for a project this run could not read; one never read is left out of the build by `14` | `cache/entries_all.json`; gitlab.com GraphQL | `cache/meta.json`, `cache/readmes/`, `cache/gitlab/meta.json` | No |
| `13_signals_all.py` | Releases and actions for every repo in one pass. The staleness rule is in `signals.py` | as above | `cache/releases.json`, `cache/actions.json` | No |
| `14_classify_all.py` | The final record per listed item, of kind `repo`, `subpath` or `site`. Leaves out every row whose repo is in the dead-repo ledger, so a repo GitHub no longer serves is on no surface | everything above; `state/dead-repos.json` | `cache/records_all.json` | No |
| `dead_repos.py` | **Not a build stage**: run weekly by `dead-repos.yml`. Asks GitHub about every repo in `docs/data.json` and every repo already in the ledger, and records the ones that are gone: GraphQL `NOT_FOUND` and then REST 404, 451 or a 403 `block`, or `isDisabled`. Renamed and archived repos are alive. A repo that answers again leaves the ledger. Writes nothing if any request fails for a reason that is not about the repo, or if the scan would newly mark more than 10% of the atlas (at least 25) dead | `docs/data.json`, `state/dead-repos.json`; `gh api` | `state/dead-repos.json`; `$GITHUB_STEP_SUMMARY` | Yes; `--status` reads the ledger with no network, `--dry-run` scans and writes nothing |

## Screenshots (weekly only)

| Script | What it does | Reads | Writes | Fresh clone? |
|---|---|---|---|---|
| `05_shots.py`, `06_web_shots.py` | Screenshots for the original list: first the README image, then a live capture in headless Chromium | `cache/records.json` | `cache/shots/`, `cache/shots.json` | No |
| `15_shots_all.py` | Four-tier images for every record: README image, then `og:image`, then a live capture, then a generated card. Drains `cache/collect-queue.json` | `cache/records_all.json` | `cache/shots/`, `cache/shots_all.json`, and **`cache/shots_all.done.json`**, the completion marker that the daily gate checks | No |

The site and the Markdown edition read only each shot's `tier` and `shot_url` (`17_markdown.image`), never
the image files under `cache/shots/`. The files, the letterboxing and `15_shots_all`'s live-capture and
generated-card tiers were for the Excel workbooks.

**The spreadsheet edition is retired.** Spreadsheet edition: retired. The last copy, built 2026-10-22, stays available but is no longer updated. The website is the maintained edition. The last pair is release `v2026.10.22`. Everything
that only built it was removed in November 2026: the writer half of `16_build_all.py`, `15b_shots_sources.py`
(repo cards for its Sources sheet), `18_slicers.py`, the legacy orchestrators workbook (`07_build.py`,
`08_verify.py`, `09_pdf.py`), `media.py`, and their tests. `16_build_all.py` is still here as a library; see
below.

## Site and Markdown

| Script | What it does | Reads | Writes | Fresh clone? |
|---|---|---|---|---|
| `17_markdown.py` | The Markdown edition. Stamps new arrivals into the first-seen ledger | `cache/records_all.json`, `meta.json`, `records.json`; `docs/CNAME` | `mega-list/**` (except `collections/`); `state/first-seen.json` | No |
| `check_markdown.py` | Lints `mega-list/` for five silent failures, including pages over GitHub's 512 KB rendering limit | `mega-list/**/*.md` | nothing | Yes |
| `19_pages.py` | **The catalogue page and the dataset** | the three cache files above | `docs/catalog/index.html`, `docs/data.json`, `docs/.nojekyll`; `state/first-seen.json` | No; see `devfixture.py` below |
| `25_velocity.py` | Star-velocity ledger. Appends a sample on a 7-day grid and patches `d7`, `d30` and `velocity` into `data.json` | `state/star-history.json`, `docs/data.json` | both, in place | Yes (`--status`, `--dry-run`) |
| `19c_live.py` | `live.json`, the small star/push sidecar that detail pages fetch instead of the full dataset | `docs/data.json` | `docs/live.json` | Yes |
| `19d_discover.py` | Discover: fifty projects a day for seven days, chosen from every category and blind to stars. Selection rules are in `discover.py` | `docs/data.json`, `state/discover.json` | `docs/discover.json`, `docs/discover/index.html`, `state/discover.json` | Yes (`--out`, `--day`) |
| `32_local.py` | The local-AI page. **Fails the build** if `config/local-ai/` has a dangling reference or a model with no size for its default quant. Joins `docs/models.json` (eng-hf's Hugging Face index) when present | `config/local-ai/hardware.json`, `config/local-ai/picks.json`, `scripts/localfit.mjs`, `scripts/localhw.mjs`, `scripts/local_page.js`, optional `docs/models.json`; needs `node` for the cheat sheet | `docs/local/index.html` | Yes (`--out`) |
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
| `hosts.py` | **Which forge a row lives on.** A GitHub `nwo` is `owner/repo`; any other is host-qualified, `gitlab.com/group/sub/project`, which no GitHub nwo can equal (GitHub owners cannot contain a dot). Every URL a stage builds for a row -- page, clone, raw file, social card -- comes from here, and `enabled()` is the `intake.gitlab` flag |
| `gitlab_api.py` | The paced, retried client every GitLab read goes through. Fails fast on the hourly anonymous cap rather than sleeping an hour; caches responses under `cache/gitlab/http/` only when given a `ttl` (local tuning) |
| `taxonomy.py` | The 14 topics and 12 targets, and the rules that assign them. `python scripts/taxonomy.py --why OWNER/REPO` explains an assignment (needs the cache) |
| `16_build_all.py` | **Not a stage.** The rows every surface shares: `prepare`, `canonicalise_nwo`, `repo_pool`, `platform_pool`/`platform_rows`, `star_map`, `order_rows`, `SHEETS` and `LIST_TITLE`. `17_markdown`, `19_pages`, `taxonomy.load` and `devfixture` import it. It wrote the retired workbooks until November 2026 |
| `buckets.py` | Folds a list's sections into at most eight groups. It was sized for the retired workbook's eight colours; `order_rows` still orders each list's rows by these groups |
| `drift.py` | Upstream drift: where a provisional build files an unmapped section, and the warnings, summary and proposal that say so. See below |
| `apply_drift_proposal.py` | Writes a provisional build's placements into `taxonomy.py` and `buckets.py`, each in its own list's block, then re-imports both to check. `--check` writes nothing |
| `signals.py` | Decides when a cached release or action answer must be re-queried |
| `newness.py` | The first-seen ledger and the "New" cohort rule. Running it with no arguments prints a read-only report |
| `discover.py` | Discover's selection rule and rotation ledger. `python scripts/discover.py [DAY]` prints a plan and writes nothing |
| `app_flags.py`, `apply_flags.py`, `flags_app.py` | Feature flags: the validator, a re-render after an edit, and a local web editor. See [frontend.md](frontend.md#feature-flags) |
| `chrome.py` | Finds a headless Chromium: `CHROME_PATH`, `CHROMIUM_PATH`, `PLAYWRIGHT_CHROMIUM`, then Playwright caches, then `PATH` |
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

## Upstream drift

The 39 lists change without notice. A curator renames a heading, translates the README, adds a shelf or
restructures the list. `taxonomy.py` refuses to guess at a section it does not name, and `buckets.py`
will not give a ninth colour to an eight-colour palette. Both refusals are deliberate. Until 2026-11,
`10_parse_sources.py` turned them into a red build, and the site stalled until someone wrote one line.

There are now two modes. `AAA_PROVISIONAL` chooses between them.

- **Strict**, with the variable unset. Every local run and every test is strict. An unmapped section or a
  ninth colour exits 1 and prints what to add, as before.
- **Provisional**, with `AAA_PROVISIONAL=1`, which `daily.yml` and `weekly.yml` set for the whole build
  job. The parse files each unmapped section for this run only and the build publishes. Every later
  stage honours the placements through `taxonomy.category_of` and `buckets.bucket_map`, but only under
  the variable. A `cache/provisional.json` left on disk is ignored by strict runs, and a strict parse
  deletes it.

Where a provisional section goes. The strongest evidence wins:

| Basis | Evidence |
|---|---|
| `membership` | At least half its entries were under one mapped section in the list's previous copy. `pull_sources.py` records this in `cache/section-moves.json`, because it is the one stage that holds both copies. Renames and translations keep their entries, so this evidence covers both. If the ledger missed the change (because the cache already held the new copy), the same evidence is read from the list's committed `mega-list/lists/*.md` pages. |
| `position` | The list kept the same number of sections, and this one took a mapped section's slot. |
| `similar` | Its name is more than 75% similar (difflib) to a mapped section of the same list. Sections the list no longer has are checked first. |
| `leftover` | Every other new section in the list was traced. Exactly one new section and one vanished mapped section remain, so they are paired. |
| `modal` | No evidence. The section goes to the category most of the list's rows already use. This placement most needs a reviewer's eye. |

A section that takes over an old section's mapping also takes its bucket. If a list goes over eight
colours, newcomers fold into the list's last bucket. Slots are counted the way the retired workbook writer
(`16_build_all.group_styles`) handed them out; the eight-colour cap outlived it, see `buckets.py`.

Nothing becomes permanent until a person makes it so. Each provisional run produces:

- a `::warning` annotation per placement, saying where the section went, the evidence, and the line to paste;
- a block in the step summary with every `taxonomy.py` and `buckets.py` line;
- `cache/drift-proposal.json`. Its fields are `placements`, `degraded` (lists held at their previous copy)
  and a `fingerprint`, which stays the same when the same drift recurs on later days;
- `cache/drift-proposal.md`, which is the same summary as Markdown.

To make a run's placements permanent, take the proposal from the run's cache or step summary, run
`python scripts/apply_drift_proposal.py PROPOSAL.json`, review the diff (a `modal` placement especially),
and commit it.

Upstream failures that stay hard stops, each for a reason written beside it in the code:

- **A cold cache plus a list that cannot be pulled** (`10_parse_sources.main`). There is no previous copy,
  and publishing without the list would remove its rows from the site.
- **The fetch's mass-failure guard** (`11_fetch_all.mass_failure`).
- **`13_signals_all.py`'s failed batches.**
- **`17_markdown.py`'s page ceiling and `check_markdown.py`'s lint.** No list edit should be able to trip
  these. `prose()` now unescapes an upstream `\|` so that a GitHub description cannot trip them either.

## Order matters

The workflows run the intake and fetch stages in this order (the two scouts first, because the watch step digests their documents; each GitLab stage straight after its GitHub counterpart):

```
12_scout → 12b_gitlab → [watch] → pull_sources → … → 10_parse_sources → 11_fetch_all → 11b_fetch_gitlab
  → 12_scout --follow-renames → 13_signals_all → 14_classify_all
```

and then the site stages:

```
17_markdown → check_markdown → 19_pages → 25_velocity → 19c_live → 19d_discover → 32_local → 20_landing
  → 21_feeds → 22_detail → [25_collections → 23_og, weekly only] → 31_home → 24_pwa → 27_semantic
```

The dependencies behind that order:

- `25_velocity` patches `data.json` after `19_pages` writes it.
- `32_local` runs before `20_landing`, which imports its `urls()` into the sitemap.
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
comes out of the screenshots' budget and never the rebuild's. A warm one re-reads a tree or config only when
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
