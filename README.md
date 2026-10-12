<div align="center">

<a href="https://aaa.jeremyfhall.com/">
  <img src="docs/favicon.svg" width="64" height="64" alt="Awesome Agentic Atlas logo: a gold globe in pixel sunglasses">
</a>
<a href="https://aaa.jeremyfhall.com/">
  <img src="docs/assets/atlas-byte.png" width="132" alt="Archie 'Atlas' Algorithm, the Awesome Agentic Atlas robot mascot, wearing pixel sunglasses and holding a globe">
</a>

# Awesome Agentic Atlas

**Thirty-nine of the best agentic awesome-lists, merged into one searchable atlas.**

14,914 entries · 8,858 repos · 24.1M combined stars · one spreadsheet · zero tab-hopping

[![entries](https://shieldcn.dev/badge/entries-14%2C914-6557C8.svg?logo=ri%3ALuDatabase&size=sm&font=geist&split=true)](mega-list/README.md)
[![repos](https://shieldcn.dev/badge/repos-8%2C858-1D5E9E.svg?logo=ri%3ALuGithub&size=sm&font=geist&split=true)](mega-list/leaderboard.md)
[![stars](https://shieldcn.dev/badge/combined_stars-24.1M-875A19.svg?logo=ri%3AGoStarFill&size=sm&font=geist&split=true)](mega-list/leaderboard.md)
[![lists merged](https://shieldcn.dev/badge/lists_merged-39-187557.svg?logo=ri%3ALuListChecks&size=sm&font=geist&split=true)](#the-source-lists)
[![license](https://shieldcn.dev/badge/license-MIT-596574.svg?logo=ri%3ALuScale&size=sm&font=geist&split=true)](LICENSE)

### [🔎 Browse it in your browser][site] · [⬇ Download the workbook — dark][dark] · [⬇ light][light]

[![Atlas Leaderboard](https://shieldcn.dev/badge/Atlas-Leaderboard-875A19.svg?logo=ri%3ALuTrophy&size=sm&font=geist&split=true)](mega-list/leaderboard.md)

</div>

---

## The problem this solves

There are dozens of excellent awesome-lists for AI agents. Between them they name the same projects
under different headings, in different orders, with different opinions, and none of them tells you
whether the thing runs on Windows or how to install it. Finding "the best Claude Code observability
tool that runs on Windows" means opening dozens of tabs and reading all of them.

So all thirty-nine are in here once, deduplicated, with the columns those lists don't have: **star
count, language, licence, last push, install command, and a per-OS verdict for Windows, macOS, Linux
and Docker.** Plus a screenshot of every project, so you can see it before you click it. That question
up there is now [one link, ranked][q1].

Figures on this page are from the **2026-09-22 snapshot** (`snapshot` in [`data.json`][data]) and drift
with every rebuild. Working on the project itself? Start with the [handbook](handbook/README.md).

[q1]: https://aaa.jeremyfhall.com/catalog/#topic=observability-evals&target=claude-code&os=windows&confirmed=1

## Pick your surface

| | Best for | Where |
|---|---|---|
| 🔎 **The Atlas site** | Live search and filtering with no download. Pick a topic, pick a harness, pick an OS, cross all three. Every view is a link. | [aaa.jeremyfhall.com][site] |
| 🎲 **Discover** | Not knowing what you are looking for. Fifty projects a day, dated, drawn from every category so a small one gets the same billing as a crowded one, rotated so what appeared this week goes to the back of the queue. Nothing here is ranked by stars. A new fifty at midnight Central, seven days picked each Sunday. | [discover][discover] |
| 📊 **Excel workbook** | Filtering, sorting, "show me every Rust tool with >1k stars that runs native on Windows". 21 sheets, a screenshot embedded on every row, autofilter on every column. Two themes. | [dark][dark] · [light][light] |
| 📄 **Markdown edition** | Reading in the browser, linking to, quoting. Same data, same ordering, split so no page hits GitHub's rendering limit. | [mega-list/](mega-list/README.md) |
| 🏆 **Leaderboard** | The most-starred projects across every list at once, with how many lists name each one — a rough consensus score. | [leaderboard](mega-list/leaderboard.md) |
| 🧰 **Curated collections** | Five recommended sets rather than a ranking — a first setup, a Windows-native one, a Claude Code kit, a local-only one. Each pick says what job it does and why it, and carries its own evidence. | [collections](mega-list/collections/README.md) |
| 🧩 **The JSON dataset** | Building something on top of it. Every repo, verdict, topic and install command in one file, documented and versioned. | [`data.json`][data] · [schema](#the-data-as-an-api) |

### Running the site locally

The site is static files in `docs/`, so a clone serves it with nothing installed but Python:

```bash
python -m http.server -d docs 8000
```

Then open <http://localhost:8000> for the homepage, or <http://localhost:8000/catalog/> for the
searchable catalogue. It does have to be *served*: a `file://` page is not allowed to `fetch` a
sibling file, so double-clicking `docs/catalog/index.html` gives you the layout and none of the rows.

Almost everything in `docs/` is **generated** by the scripts in `scripts/`, so edit the generator,
not the page. The [handbook](handbook/README.md) says which script owns which file, and which ones
can be re-run without the CI-only cache.

## Top of the leaderboard

| ★ | Project | Named by |
|---:|---|---:|
| 390,260 | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 6 lists |
| 290,183 | [obra/superpowers](https://github.com/obra/superpowers) | 6 lists |
| 267,783 | [mattpocock/skills](https://github.com/mattpocock/skills) | 3 lists |
| 265,361 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 6 lists |
| 248,091 | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 3 lists |
| 233,380 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 1 list |
| 214,654 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 3 lists |
| 209,402 | [anomalyco/opencode](https://github.com/anomalyco/opencode) | 4 lists |
| 205,712 | [n8n-io/n8n](https://github.com/n8n-io/n8n) | 2 lists |
| 200,254 | [tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) | 1 list |

[**Full leaderboard — 250 projects →**](mega-list/leaderboard.md)

## Browse by topic

One leaderboard tells you the most-starred agentic project overall. It does not tell you the best
*skill*, or the best *observability tool*. So every project is also filed under exactly one of **14
topics**, ranked inside it — the thirty-nine source lists published hundreds of section names between
them and agreed on almost none, so this is one shared vocabulary laid over all of them.

| Topic | Projects | Top of the topic |
|---|---:|---|
| [MCP Servers](mega-list/topics/mcp-servers.md) | 4,537 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| [Agent Skills](mega-list/topics/agent-skills.md) | 823 | [Superpowers](https://github.com/obra/superpowers) |
| [Harnesses & Runtime Infra](mega-list/topics/harnesses-runtime-infra.md) | 670 | [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) |
| [Plugins, Themes & Clients](mega-list/topics/plugins-themes-clients.md) | 611 | [cc-switch](https://github.com/farion1231/cc-switch) |
| [Frameworks & SDKs](mega-list/topics/frameworks-sdks.md) | 464 | [openclaw](https://github.com/openclaw/openclaw) |
| [Observability & Evals](mega-list/topics/observability-evals.md) | 421 | [LLMApp](https://github.com/pathwaycom/llm-app) |
| [Orchestrators & Multi-Agent](mega-list/topics/orchestrators-multi-agent.md) | 339 | [n8n](https://github.com/n8n-io/n8n) |
| [Coding Agents](mega-list/topics/coding-agents.md) | 281 | [OpenCode](https://github.com/anomalyco/opencode) |
| [Assistants & Domain Agents](mega-list/topics/assistants-domain-agents.md) | 252 | [hermes-agent](https://github.com/NousResearch/hermes-agent) |
| [Sandbox, Security & Governance](mega-list/topics/sandbox-security-governance.md) | 150 | [Daytona](https://github.com/daytonaio/daytona) |
| [Docs, Learning & Lists](mega-list/topics/docs-learning-lists.md) | 142 | [f/awesome-chatgpt-prompts](https://github.com/f/prompts.chat) |
| [Context, Memory & RAG](mega-list/topics/context-memory-rag.md) | 98 | [RAGFlow](https://github.com/infiniflow/ragflow) |
| [Research & Data Agents](mega-list/topics/research-data-agents.md) | 41 | [Pathway](https://github.com/pathwaycom/pathway) |
| [Creative, Voice & Media](mega-list/topics/creative-voice-media.md) | 29 | [whisper](https://github.com/openai/whisper) |

[**All 14 topics, with what each one covers →**](mega-list/topics/README.md)

## Browse by what it plugs into

The other axis: not what a project *is* but what it *runs with*. A project can appear on several of
these, because plenty of them serve Claude Code and opencode and Codex at once.

[MCP](mega-list/targets/mcp.md) 5,104 ·
[Claude / Anthropic](mega-list/targets/claude-anthropic.md) 3,944 ·
[Claude Code](mega-list/targets/claude-code.md) 2,396 ·
[Codex / OpenAI](mega-list/targets/codex-openai.md) 1,579 ·
[Cursor](mega-list/targets/cursor.md) 1,122 ·
[Gemini / Google](mega-list/targets/gemini-google.md) 653 ·
[opencode](mega-list/targets/opencode.md) 406 ·
[GitHub Copilot](mega-list/targets/github-copilot.md) 240 ·
[LangChain / LangGraph](mega-list/targets/langchain-langgraph.md) 175 ·
[Local / Ollama](mega-list/targets/local-ollama.md) 146 ·
[Cline / Roo](mega-list/targets/cline-roo.md) 89 ·
[Aider](mega-list/targets/aider.md) 39

**The two axes cross.** That's what the site and the workbook's *By Category* sheet are for — pick a
topic and a harness at once and you get the answer the individual lists can't give you:

- [the best Claude Code observability tools](https://aaa.jeremyfhall.com/catalog/#topic=observability-evals&target=claude-code), ranked
- [memory and retrieval over MCP](https://aaa.jeremyfhall.com/catalog/#topic=context-memory-rag&target=mcp)
- [skills that run native on Windows](https://aaa.jeremyfhall.com/catalog/#topic=agent-skills&os=windows&confirmed=1)

## Browse by what you actually run

Every list assumes you're on a Mac. This one doesn't. Each project was checked against its own
README, install instructions and CI config for what it actually supports:

| Platform | Projects | Page |
|---|---:|---|
| 🪟 Windows | 2,066 | [windows.md](mega-list/platforms/windows.md) · [inferred](mega-list/platforms/windows-inferred.md) |
| 🍎 macOS | 1,486 | [macos.md](mega-list/platforms/macos.md) · [inferred](mega-list/platforms/macos-inferred.md) |
| 🐧 Linux | 1,985 | [linux.md](mega-list/platforms/linux.md) · [inferred](mega-list/platforms/linux-inferred.md) |
| 🐳 Docker | 1,548 | [docker.md](mega-list/platforms/docker.md) |

Each platform is split into two pages on purpose. The main page is projects with **direct evidence** —
an install command for that OS, a matching CI job, a released binary. The `-inferred` page is projects
whose language and packaging make them near-certain to work but where nobody said so out loud. A pure
Python package with no OS-specific dependency runs on Windows; that is an inference, not a promise, and
it is filed as one. The Docker page has no inferred half: either there's a Dockerfile or there isn't.

## The source lists

Every entry here came from someone else's curation work. All thirty-nine are credited on the workbook's
**Sources** sheet with their own star count and a screenshot, and each has its own page in the
[Markdown edition](mega-list/README.md). The eleven that also get a workbook sheet of their own:

| List | Curator | Entries | Page |
|---|---|---:|---|
| [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | ai-boost | 443 | [→](mega-list/lists/harness-engineering.md) |
| [agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | sickn33 | 278 | [→](mega-list/lists/aas-skill-sources.md) |
| [awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026) | caramaschiHG | 264 | [→](mega-list/lists/ai-agents-2026.md) |
| [awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) | andyrewlee | 227 | [→](mega-list/lists/orchestrators.md) |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | awesome-opencode | 219 | [→](mega-list/lists/opencode.md) |
| [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | e2b-dev | 215 | [→](mega-list/lists/agents-e2b.md) |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | hesreallyhim | 202 | [→](mega-list/lists/claude-code.md) |
| [awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | heilcheng | 194 | [→](mega-list/lists/agent-skills.md) |
| [awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns) | nibzard | 193 | [→](mega-list/lists/agentic-patterns.md) |
| [awesome-agents](https://github.com/kyrolabs/awesome-agents) | kyrolabs | 170 | [→](mega-list/lists/agents-kyrolabs.md) |
| [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | Shubhamsaboo | 120 | [→](mega-list/lists/llm-app-templates.md) |

If you maintain one of these: thank you, and please tell me if anything here misrepresents your list.

## What's in the workbook that isn't in the lists

Twenty-one sheets. Eleven of the source lists get one each, keeping the section headings their curator
published, so you can still read it the way they wrote it; every row of the other twenty-eight is on
the cross-list sheets. Then:

- **Sources** — all thirty-nine lists side by side: entries, distinct repos, total and median stars, how
  many entries are Windows-capable, screenshot coverage.
- **Leaderboard** — one row per repo across all thirty-nine, ranked, with a consensus count.
- **By Category** — the same repos grouped into the 14 topics and ranked *inside* each one, as a
  real Excel table. Filter Category to one topic and the filter *is* that topic's leaderboard; add
  Plugs Into and you're asking both questions at once.
- **Windows / macOS / Linux / Docker** — the platform pools, ordered by evidence strength.
- **Category Stats** and **List Stats** — where the mass actually is, with charts.
- **Start Here** — a cover that explains every column and links to every sheet.

Every row carries a screenshot: the project's README banner where it has one, GitHub's social card
where it doesn't. The images are anchored two-cell, which means they **hide and reappear with their row
when you filter** — the thing embedded pictures in Excel normally refuse to do.

## Honest notes on the data

Aggregating other people's lists introduces failure modes worth naming:

- **Stars and dates drift.** They come from the GitHub API on the build date printed on every page.
  Treat them as a snapshot, not a live feed.
- **The same repo arrives under several names.** GitHub redirects renamed repos for ever, so lists
  written at different times link to the same project under different owners and every link
  works. `OpenDevin/OpenDevin`, `All-Hands-AI/OpenHands` and `OpenHands/OpenHands` are one project.
  Every name is resolved to the one the API reports, so a renamed project, or one spelled in two
  cases, is one row and its stars are counted once.
- **Some entries are folders, not repos.** A skill that lives in a directory of someone else's
  monorepo has no star count of its own. Those rows show a dash rather than borrowing the parent's
  number, and they're excluded from the leaderboard.
- **Descriptions are the curators' words**, lightly normalised for length. The verdicts, platform
  columns, install commands and rankings are this project's.
- **Not every project is good.** This is a merged index, not an endorsement. Sort by last-push before
  you install anything.

## Staying current

Two GitHub Actions workflows keep the three surfaces from going stale, and neither needs a hand on it.

**Daily** ([`daily.yml`](.github/workflows/daily.yml), 11:12 UTC) asks each of the thirty-nine source lists
for its newest commit. If none of them has moved, the job stops there — a rebuild would produce byte-identical
files. If any has, it refetches every repo's metadata, rebuilds the site and the Markdown edition, and
commits them, which is what republishes the site. It also stops, successfully, when the last weekly
run did not finish its screenshots, so a green daily is not proof that anything was published; the
`snapshot` in `data.json` is ([details](handbook/ci-cd.md#the-daily-build)).

**Weekly** ([`weekly.yml`](.github/workflows/weekly.yml), Sundays) does all of that and then the expensive
part the daily run skips: capturing a screenshot for each new project, rebuilding both workbooks, and
publishing them as a dated release. That's why the [download links][dark] never rot — they point at
`releases/latest`, and each Sunday's release becomes the latest.

The split is about cost, not caution. Metadata for the whole atlas is a few hundred GraphQL queries,
twenty repos to a query. Screenshots are a headless-browser render per project. So a project added on
Tuesday shows GitHub's own repo card until Sunday, then gets its real image.

### The pull cache

[`scripts/pull_sources.py`](scripts/pull_sources.py) is what actually downloads the lists, and it keeps a
commit id per list in `cache/sources/index.json` so it can decline to. Ask a list for its head commit, and
if it matches the one already cached — and the cached bytes are still on disk — there is nothing to read
and the pull is skipped. On a day when one list moved, one list is re-read, not thirty-nine.

When a list has moved, the new copy and the cached one are both run through the same parser the build uses
and the resulting entries are compared. That is the difference between a diff over lines and a diff over
meaning: a reworded heading or a new badge changes the file without changing a single row, and is correctly
silent, while an entry whose name, category or description moved is reported and queued.

The queue matters because of an asymmetry in the screenshot stage. A brand-new entry has no image on file,
so it gets one on the next weekly run without being told to. An entry that is still listed under the same
URL but has been *rewritten* looks identical to a cached one, and before this it kept its old image for
ever. `cache/collect-queue.json` carries those across from the daily job, which finds them, to the weekly
job, which captures them and drains the queue.

Two smaller things it fixes. Lists are pulled from `raw.githubusercontent.com`, because above roughly a
megabyte `gh api repos/{nwo}/readme` returns a payload whose content field is *empty* rather than an error
— the 1.4 MB list that reads as zero entries. And a pull that comes back at a fraction of the size of the
copy it replaces is refused rather than written, because a truncated transfer and an author deleting most
of their list look the same from here, and only one of them should silently remove rows from the atlas.

### The New filter

A project's arrival date is the one thing the API can't tell you — a repo created in 2023 can be new *to
this atlas* today. So the pipeline keeps its own ledger,
[`state/first-seen.json`](state/first-seen.json): the date each repo was first seen in any source list.
Everything already present when the ledger was created is stamped as founding stock, so day one marked
nothing.

What is marked is **the most recent import that brought anything** — one cohort, not a rolling window. The
next run that adds a repo takes the mark off the last lot by finding this lot, so `New` always answers "this
is what just landed" rather than "this arrived within some number of days". A run that adds nothing changes
nothing: the builds are daily and a quiet Tuesday should not silently expire Monday's arrivals.

That matters here because almost nothing on this site is new *in the world*. Repos arrive when a curator adds
them to somebody's list, and the median one has existed for a year or more; the only newness this pipeline can
honestly observe is newness to the atlas. Three ways to see it:

- A **New** chip beside the sort control, with a count on it, and clicking it narrows the table to exactly
  those projects. Their titles read `✨ ProjectName - Added 09/21/26`. The filter lives in the URL, so it's a
  link: [`#new=1`][new].
- Each new row wears a `--warn` outline that pulses for a few seconds and then holds as a static edge, in
  both the table and the cards view. If your system asks for reduced motion you get the edge without the
  pulse; if an import brings more rows than fit on a screen *and* most of what you are looking at is new, the
  pulse stops on its own — a nudge pointing at everything is not a nudge.
- A **Since your last visit** chip, which is your device's own answer rather than the atlas's. It counts
  across however many imports have landed since this browser was last here, so being away for a month shows
  you a month. It is the one filter deliberately kept out of the URL: it describes your machine, so sharing
  it would show somebody else a set neither of you chose.

In the Markdown edition, each topic and target page opens with a line saying how many the latest import
brought, and every marked row carries a ✨ and its date.

One bound on all of this: a cohort with nothing newer to supersede it stops being `New` after **fourteen
days**. That is not the definition, it is the failure mode — the pipeline does stop sometimes, and an import
from three weeks ago should not go on presenting itself as the latest news. The bound is re-applied in your
browser against your own clock as well as at build time, so a tab left open overnight expires it on time, and
a `#new=1` link that has outlived its cohort shows the whole atlas rather than an empty page.

## The data as an API

The site is one static page over one JSON file, and that file is public at a stable URL:

**<https://aaa.jeremyfhall.com/data.json>**

About 4 MB on the 2026-09-22 snapshot (it grows with the corpus), `application/json`,
`Access-Control-Allow-Origin: *`, no key and nothing to sign up for, rewritten by the same job that
republishes the site. It exists because the page needs it, but it is the whole atlas in one request —
every repo, every topic and target, five OS verdicts each — so it is
documented here rather than left to be reverse-engineered from view-source. It changes at most once a
day; cache it accordingly.

**Rows are arrays, not objects.** Eighteen keys repeated on every one of thousands of rows would be
megabytes of the word `"listed_by"` and its neighbours, on a file that is rewritten on every rebuild and that the table cannot
draw until it has arrived. So the keys are hoisted into a `cols` array once and each row carries values
in that order. The page maps them back into objects in a single pass on load, and any consumer should do
the same — after one line the array shape stops mattering:

```python
ix = {c: i for i, c in enumerate(d["cols"])}
```

### The columns

In `cols` order. There is no `null` anywhere in the file: an absent string is `""`, an absent number is
`0`, an absent list is `[]`. The one exception is `d7`/`d30`, where `0` is a real answer (no stars gained)
and so an absent one is `""`.

| Column | Type | Meaning |
|---|---|---|
| `name` | string | The project's display name, as all three surfaces print it. Not unique — two different projects are called *OpenCode*. `nwo` is the key. |
| `nwo` | string | `owner/repo`, as the GitHub API reports it today, after renames are resolved. Unique across rows. |
| `cat` | int | **An index into the top-level `cats` array**, not a name. Exactly one topic per repo. |
| `targets` | int[] | **Indices into the top-level `targets` array**, ascending, no duplicates. Empty for repos that plug into nothing in particular. |
| `stars` | int | Stargazer count on `snapshot`. `0` covers both "genuinely none" and "has no count of its own" — `os` tells you which. |
| `lists` | int | How many of the source lists name this repo. At least 1; the ceiling moves as lists are added. |
| `listed_by` | string | Those lists' short names, `", "`-joined. The count always matches `lists`. |
| `os` | string | Five characters, one per entry of the top-level `os` array, in that order. Encoding below. |
| `blurb` | string | The curator's description, whitespace-collapsed and cut to 400 characters with a trailing `…`. Empty for the handful nobody described. |
| `install` | string | One line you can paste — `git clone`, `npx`, `pip install`, `irm`. Empty where there was nothing to say. |
| `lang` | string | GitHub's primary language. Empty for repos it reports none for. |
| `license` | string | SPDX identifier. Empty for no licence *and* for `NOASSERTION`, which are the same thing to someone deciding whether they may use it. |
| `pushed` | string | Last push, `YYYY-MM-DD`. Empty when the repo could not be read. |
| `url` | string | The link the atlas prints. Effectively always `https://github.com/<nwo>`, but it is not derived from it — use the column. |
| `img` | string | Screenshot or README banner. **Empty means "derive it"**, not "no image" — see below. |
| `first_seen` | string | Arrival date, `YYYY-MM-DD`. Empty for founding stock, and that is not "unknown" — see below. |
| `d7` | int or `""` | Stars gained over the last seven days — the live `stars` minus a sample about a week old. Can be negative. **`""` means "no answer"**, never `0`: no sample of the right age yet, the repo postdates it, or either end is not a count. |
| `d30` | int or `""` | The same over thirty days. `velocity` says which sample each window was measured from. |

#### `os` — five characters, five verdicts

A fixed-width string, one character per operating system, in the order the top-level `os` array gives
them: **Windows, WSL2, macOS, Linux, Docker**. The first row in the file is `"YYYYN"` — native Windows,
WSL2, macOS and Linux all confirmed, no Dockerfile.

| Char | Verdict | Means |
|---|---|---|
| `Y` | Yes | Stated evidence: an install command for that OS, a matching CI job, a released binary. |
| `L` | Likely | Inferred from language and packaging. A pure Python package with no OS-specific dependency runs on Windows, but nobody said so out loud. |
| `N` | No | Looked at, and there is no support. |
| `a` | n/a | The question does not apply. Pure GitHub Actions, which run on a hosted runner and are never installed on your machine. |
| `-` | unknown | **Not "no".** Nothing was classifiable — the entry is a folder inside someone else's repo, the repo 404s, or it is a hosted product with no README to read. Every such row also has `stars` `0`, for want of a count rather than want of stars — though not every `0` is one of them. |

A "does this run on Windows" filter usually wants `Y` or `L` in position 0, or `Y` in position 1, which
is what the site's Windows chip does. `"L"` is an inference, not a promise; drop it if you need only
stated support. The Windows figure in the platform table above is that stricter count: `Y` in position 0
or 1.

#### `img` — empty means derive

Every repo has a GitHub social card, so `img` is left empty whenever that card is what the surfaces
would show anyway — about two rows in three on the 2026-09-22 snapshot. Writing it out would be 55 bytes
on each of them, of a string that is a pure function of `nwo`. Treat empty as "this project has no image"
and you drop the picture on most of the atlas:

```python
img = row[ix["img"]] or f"https://opengraph.githubassets.com/1/{row[ix['nwo']]}"
```

#### `first_seen` — empty means "was already here"

`baseline` is the day the arrival ledger was created, and everything present on that day is founding
stock. `first_seen` carries a date only for repos that arrived *after* the baseline; on every other row
it is `""`, which means "here since before anyone was counting" — not "unknown", and certainly not
"new". The file carries the raw date and no flag. What the site marks `New` is the rows whose
`first_seen` equals the top-level `cohort` — [one import, not a rolling window](#the-new-filter) — and a
consumer that wants the same answer should compare against `cohort` rather than against a clock.

### The top-level keys

| Key | Type | Meaning |
|---|---|---|
| `schema_version` | int | `2` — `d7` and `d30` joined `cols`. Bumped only for a change to something this section calls stable. Absent from snapshots published before it was introduced, so read a missing key as `1`. |
| `snapshot` | string | Build date, `YYYY-MM-DD`. Every star count, language, licence and push date in the file is as of this day. |
| `repo` | string | `crazy54/awesome-agentic-atlas` — the atlas's own repo, so a consumer can link back without hardcoding it. |
| `generated` | string | When this file was written, UTC, `YYYY-MM-DDTHH:MM:SSZ` to the minute. Later than `snapshot` on a rebuild that reused the day's data. |
| `cols` | string[] | The column names, in row order. This is the thing to read. |
| `window_days` | int | `14`. Not a recency window: the age at which a cohort nothing has superseded stops being `New`. Carried here so the page and this file cannot disagree about it. |
| `baseline` | string | `YYYY-MM-DD`. The day the arrival ledger started; see `first_seen`. |
| `cohort` | string | `YYYY-MM-DD`. The import whose arrivals are `New`: a row is new when its `first_seen` equals this. `""` when there is none to show, including once `window_days` has lapsed. |
| `cats` | object[] | The 14 topics, `{name, slug, blurb}`. The index space for `cat`. |
| `targets` | object[] | The 12 harnesses, `{name, slug, blurb}`. The index space for `targets`. |
| `os` | string[] | The five OS labels, in the order the `os` column encodes them. |
| `rows` | array[] | One array per repo, one value per `cols` entry, sorted by stars descending, then name case-insensitively. |
| `velocity` | object | Where `d7` and `d30` came from. `to` is the date the gains run up to. `d7` and `d30` are each `{days, from, span, n}`: the nominal window, the date of the sample it was measured from (`""` if none was the right age), the days that sample really spans, and how many rows got an answer. `rise` is `{col, min_abs, min_pct}`: the window the site's Rising filter uses (`""` switches it off) and its threshold — a row rises when its gain is at least `max(min_abs, min_pct% of stars)`. |

A topic's or target's `slug` is the same string that names its Markdown page and its URL hash:
`cats[2].slug` is `agent-skills`, its page is `mega-list/topics/agent-skills.md`, and the filtered view
is `#topic=agent-skills`. One vocabulary across all three surfaces, which is what lets a link into one
of them mean something in the others.

JSON objects are unordered, and this one genuinely is — `velocity` sits after `rows` because a later
stage appends it to a dataset that predated it. Read by key.

### What will and will not change

The daily job rebuilds whenever any source list moves, which is most days. Volatile, and changing
without notice:

- every value in every row — stars, language, licence, `pushed`, blurbs, install commands, verdicts
- `snapshot`
- which repos are present, and therefore the row count
- **row ordering.** Stars descending today. A different tie-break, or a different default sort, is not
  a schema change.
- **the indices in `cats` and `targets`.** A fifteenth topic changes what `cat: 4` means. Resolve
  through the arrays on every read — the `slug` is the stable identifier, the position is not.

Not without a `schema_version` bump:

- the set, the meaning and the order of `cols`
- the `Y`/`L`/`N`/`a`/`-` verdict encoding, and the five-OS order the `os` column uses
- `img` empty meaning "derive from `nwo`"
- the slug rules — `#topic=agent-skills` is a link people have already sent each other
- ISO `YYYY-MM-DD` for `snapshot`, `pushed`, `first_seen`, `baseline` and `cohort`
- no `null`s: `""`, `0`, `[]` — and `""`, never `0`, for a `d7`/`d30` with no answer

**Read `cols`; do not hardcode positions.** `ix["stars"]` costs one line and survives a column being
inserted. `row[4]` is correct until the day one is added in front of it, and then it does not raise — it
reads `lists`, a single-digit number, as a star count and ranks the atlas by nothing. That is the
whole difference: a name lookup either finds its column or fails loudly on the rebuild that moved it,
while a magic index quietly starts answering a different question.

### A worked example

"Every Rust project that runs native on Windows, ranked by stars." Standard library, no dependencies:

```python
import json, urllib.request

URL = "https://aaa.jeremyfhall.com/data.json"
with urllib.request.urlopen(URL) as r:
    d = json.load(r)

ix = {c: i for i, c in enumerate(d["cols"])}   # never hardcode 4
WIN = d["os"].index("Windows")                 # position in the five-character os string

hits = [r for r in d["rows"]
        if r[ix["lang"]] == "Rust" and r[ix["os"]][WIN] == "Y"]   # "Y" is stated, "L" is inferred
hits.sort(key=lambda r: -r[ix["stars"]])

print(f"{len(hits)} Rust projects with stated Windows support, snapshot {d['snapshot']}")
for r in hits[:5]:
    print(f"{r[ix['stars']]:>7,}  {r[ix['nwo']]:<34}  {d['cats'][r[ix['cat']]]['name']}")
```

```
159 Rust projects with stated Windows support, snapshot 2026-09-22
134,191  farion1231/cc-switch                Plugins, Themes & Clients
125,960  openai/codex                        Coding Agents
 90,728  zed-industries/zed                  Coding Agents
 68,404  openinterpreter/openinterpreter     Coding Agents
 54,567  aaif-goose/goose                    Coding Agents
```

Two lookups and no magic numbers, and the same dozen lines keep working across a rebuild that adds a
column, a topic or four hundred repos.

## How it's built

A Python pipeline of numbered stages in [`scripts/`](scripts/): pull each source list that has moved, parse its Markdown, resolve and fetch every repo
through the GitHub API, pull release and Actions metadata, classify OS support from README and CI
evidence, capture a screenshot per project, then render the workbooks with `openpyxl`, the Markdown
edition, and the site's dataset from the same in-memory records — so the three surfaces cannot
disagree. The topic and target assignments come from one taxonomy module all three read, which is why
`topics/agent-skills.md`, `#topic=agent-skills` and `Category = Agent Skills` are the same rows.

The [handbook](handbook/README.md) documents every stage (what it reads, what it writes, and which
ones need the CI-only cache), the two build workflows, the test suite and the front end.

The build cache (a fetched README and a screenshot per project) is deliberately **not** committed. It
is other people's content, it grows with every list added, and it is reproducible from the fetch scripts.

That is also why the pull cache's commit ids live in `cache/sources/index.json` rather than alongside the
ledger in `state/`. An id recorded in a committed file would still be there on a clone that has none of the
content it describes, and the puller would compare it, find it equal, skip every download and then have
nothing to parse. Keeping the id next to the bytes makes "unchanged" mean "we still have it".

`state/first-seen.json` is the opposite case and is committed for the same reason: it is the only thing
here that a rebuild cannot recreate. Delete it and every project looks as old as every other one. The SHA
it also stores per list is a different fact from the puller's — that one means "this commit has been
*built*", and it is recorded only after a build succeeds, so a build that dies halfway is retried instead
of being written off as done.

A clone with an empty `cache/` starts with `python scripts/pull_sources.py`; the stages that read the
lists now say so by name instead of failing on a missing file.

## Contributing

Corrections are the most valuable thing you can send. Especially:

- a platform verdict that's wrong for your project
- an install command that doesn't work
- a project that's dead, renamed, or filed under the wrong heading
- a list that should be merged in

Open an issue with the repo name and what's wrong. New source lists are welcome — the parser needs one
per list, so say which list and I'll add it.

Changing the code? Read the [contributor guide](handbook/contributing.md) first. Pull requests go
against `latest_branch`, which is also the branch the site is published from, and
`node tests/run.mjs` runs the full suite ([testing](handbook/testing.md)).

## Licence and credit

This repository is **MIT** — see [LICENSE](LICENSE). MIT rather than Apache-2.0 deliberately: this is a
directory and a build pipeline, not a library with patent surface, and MIT's five clauses are the least
friction for anyone who wants to fork the data or reuse the scripts.

That covers **this project's own work**: the pipeline, the platform classifications, the merge, the
compilation. It does not relicense the thirty-nine source lists — the descriptive text is the work of the
curators named above, each of whom retains their own licence, and every entry links back to both the
project and the list that found it. Star counts, languages and licences are facts from the GitHub API.

If you think something here should be attributed differently, open an issue and I'll fix it.

---

<div align="center">

**[Filter it live][site]** · **[Browse the mega list](mega-list/README.md)** ·
**[By topic](mega-list/topics/README.md)** · **[Leaderboard](mega-list/leaderboard.md)** ·
**[Download: dark][dark] / [light][light]**

</div>

[site]: https://aaa.jeremyfhall.com/
[new]: https://aaa.jeremyfhall.com/catalog/#new=1
[discover]: https://aaa.jeremyfhall.com/discover/
[data]: https://aaa.jeremyfhall.com/data.json
[dark]: https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx
[light]: https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx
