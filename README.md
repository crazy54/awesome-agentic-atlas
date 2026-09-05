<div align="center">

# Awesome Agentic Atlas

**Eleven of the best agentic awesome-lists, merged into one searchable atlas.**

2,394 tools · 1,294 repos · 12.5M combined stars · one spreadsheet · zero tab-hopping

[![tools](https://img.shields.io/badge/tools-2%2C394-6f42c1?style=for-the-badge)](mega-list/README.md)
[![repos](https://img.shields.io/badge/repos-1%2C294-0969da?style=for-the-badge)](mega-list/leaderboard.md)
[![stars](https://img.shields.io/badge/combined%20stars-12.5M-f9c513?style=for-the-badge)](mega-list/leaderboard.md)
[![lists merged](https://img.shields.io/badge/lists%20merged-11-1a7f37?style=for-the-badge)](#the-eleven-lists)
[![license](https://img.shields.io/badge/license-MIT-24292f?style=for-the-badge)](LICENSE)

### [🔎 Browse it in your browser][site] · [⬇ Download the workbook — dark][dark] · [⬇ light][light]

</div>

---

## The problem this solves

There are a dozen excellent awesome-lists for AI agents. Between them they name the same projects
under different headings, in different orders, with different opinions, and none of them tells you
whether the thing runs on Windows or how to install it. Finding "the best Claude Code observability
tool that runs on Windows" means opening eleven tabs and reading all of them.

So all eleven are in here once, deduplicated, with the columns those lists don't have: **star count,
language, licence, last push, install command, and a per-OS verdict for Windows, macOS, Linux and
Docker.** Plus a screenshot of every project, so you can see it before you click it. That question up
there is now [one link — twenty tools, ranked][q1].

[q1]: https://crazy54.github.io/awesome-agentic-atlas/#topic=observability-evals&target=claude-code&os=windows&confirmed=1

## Pick your surface

| | Best for | Where |
|---|---|---|
| 🔎 **The Atlas site** | Live search and filtering with no download. Pick a topic, pick a harness, pick an OS, cross all three. Every view is a link. | [crazy54.github.io/awesome-agentic-atlas][site] |
| 📊 **Excel workbook** | Filtering, sorting, "show me every Rust tool with >1k stars that runs native on Windows". 21 sheets, a screenshot embedded on every row, autofilter on every column. Two themes. | [dark][dark] · [light][light] |
| 📄 **Markdown edition** | Reading in the browser, linking to, quoting. Same data, same ordering, split so no page hits GitHub's rendering limit. | [mega-list/](mega-list/README.md) |
| 🏆 **Leaderboard** | The most-starred projects across every list at once, with how many lists name each one — a rough consensus score. | [leaderboard](mega-list/leaderboard.md) |

### Running the site locally

The site is one static page plus one JSON file, so a clone serves it with nothing installed but Python:

```bash
python -m http.server -d docs 8000
```

Then open <http://localhost:8000>. It does have to be *served* — a `file://` page is not allowed to
`fetch` a sibling file, so double-clicking `docs/index.html` gives you the layout and none of the 1,294
rows. Nothing here is built or bundled: edit `docs/index.html` and reload.

## Top of the leaderboard

| ★ | Project | Named by |
|---:|---|---:|
| 388,645 | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 3 lists |
| 281,176 | [obra/superpowers](https://github.com/obra/superpowers) | 3 lists |
| 246,813 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 2 lists |
| 246,557 | [mattpocock/skills](https://github.com/mattpocock/skills) | 1 list |
| 239,998 | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 2 lists |
| 209,837 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 2 lists |
| 203,467 | [anomalyco/opencode](https://github.com/anomalyco/opencode) | 3 lists |
| 203,229 | [n8n-io/n8n](https://github.com/n8n-io/n8n) | 1 list |
| 187,101 | [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 1 list |
| 180,046 | [ollama/ollama](https://github.com/ollama/ollama) | 1 list |

[**Full leaderboard — 250 projects →**](mega-list/leaderboard.md)

## Browse by topic

One leaderboard tells you the most-starred agentic project overall. It does not tell you the best
*skill*, or the best *observability tool*. So every project is also filed under exactly one of **14
topics**, ranked inside it — the eleven source lists published 140 section names between them and
agreed on almost none, so this is one shared vocabulary laid over all of them.

| Topic | Projects | Top of the topic |
|---|---:|---|
| [Agent Skills](mega-list/topics/agent-skills.md) | 278 | [Superpowers](https://github.com/obra/superpowers) |
| [Plugins, Themes & Clients](mega-list/topics/plugins-themes-clients.md) | 208 | [Oh My Opencode](https://github.com/code-yeongyu/oh-my-openagent) |
| [Coding Agents](mega-list/topics/coding-agents.md) | 165 | [OpenCode](https://github.com/anomalyco/opencode) |
| [Orchestrators & Multi-Agent](mega-list/topics/orchestrators-multi-agent.md) | 123 | [n8n](https://github.com/n8n-io/n8n) |
| [Frameworks & SDKs](mega-list/topics/frameworks-sdks.md) | 95 | [openclaw](https://github.com/openclaw/openclaw) |
| [Assistants & Domain Agents](mega-list/topics/assistants-domain-agents.md) | 84 | [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) |
| [Harnesses & Runtime Infra](mega-list/topics/harnesses-runtime-infra.md) | 68 | [everything-claude-code](https://github.com/affaan-m/ECC) |
| [Observability & Evals](mega-list/topics/observability-evals.md) | 66 | [Langfuse](https://github.com/langfuse/langfuse) |
| [Context, Memory & RAG](mega-list/topics/context-memory-rag.md) | 51 | [headroom](https://github.com/headroomlabs-ai/headroom) |
| [Sandbox, Security & Governance](mega-list/topics/sandbox-security-governance.md) | 50 | [Daytona](https://github.com/daytonaio/daytona) |
| [Docs, Learning & Lists](mega-list/topics/docs-learning-lists.md) | 50 | [Learn Claude Code](https://github.com/shareAI-lab/learn-claude-code) |
| [Research & Data Agents](mega-list/topics/research-data-agents.md) | 24 | [RAGFlow](https://github.com/infiniflow/ragflow) |
| [Creative, Voice & Media](mega-list/topics/creative-voice-media.md) | 21 | [Meta AudioCraft](https://github.com/facebookresearch/audiocraft) |
| [MCP Servers](mega-list/topics/mcp-servers.md) | 11 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |

[**All 14 topics, with what each one covers →**](mega-list/topics/README.md)

## Browse by what it plugs into

The other axis: not what a project *is* but what it *runs with*. A project can appear on several of
these, because plenty of them serve Claude Code and opencode and Codex at once.

[Claude / Anthropic](mega-list/targets/claude-anthropic.md) 669 ·
[Claude Code](mega-list/targets/claude-code.md) 479 ·
[Codex / OpenAI](mega-list/targets/codex-openai.md) 374 ·
[opencode](mega-list/targets/opencode.md) 284 ·
[MCP](mega-list/targets/mcp.md) 217 ·
[Cursor](mega-list/targets/cursor.md) 133 ·
[Gemini / Google](mega-list/targets/gemini-google.md) 132 ·
[GitHub Copilot](mega-list/targets/github-copilot.md) 49 ·
[LangChain / LangGraph](mega-list/targets/langchain-langgraph.md) 41 ·
[Local / Ollama](mega-list/targets/local-ollama.md) 23 ·
[Cline / Roo](mega-list/targets/cline-roo.md) 13 ·
[Aider](mega-list/targets/aider.md) 12

**The two axes cross.** That's what the site and the workbook's *By Category* sheet are for — pick a
topic and a harness at once and you get the answer the individual lists can't give you:

- [the best Claude Code observability tools](https://crazy54.github.io/awesome-agentic-atlas/#topic=observability-evals&target=claude-code) — 38 of them, ranked
- [memory and retrieval over MCP](https://crazy54.github.io/awesome-agentic-atlas/#topic=context-memory-rag&target=mcp) — 29
- [skills that run native on Windows](https://crazy54.github.io/awesome-agentic-atlas/#topic=agent-skills&os=windows&confirmed=1)

## Browse by what you actually run

Every list assumes you're on a Mac. This one doesn't. Each project was checked against its own
README, install instructions and CI config for what it actually supports:

| Platform | Projects | Page |
|---|---:|---|
| 🪟 Windows | 1,105 | [windows.md](mega-list/platforms/windows.md) · [inferred](mega-list/platforms/windows-inferred.md) |
| 🍎 macOS | 1,092 | [macos.md](mega-list/platforms/macos.md) · [inferred](mega-list/platforms/macos-inferred.md) |
| 🐧 Linux | 1,120 | [linux.md](mega-list/platforms/linux.md) · [inferred](mega-list/platforms/linux-inferred.md) |
| 🐳 Docker | 210 | [docker.md](mega-list/platforms/docker.md) |

Each platform is split into two pages on purpose. The main page is projects with **direct evidence** —
an install command for that OS, a matching CI job, a released binary. The `-inferred` page is projects
whose language and packaging make them near-certain to work but where nobody said so out loud. A pure
Python package with no OS-specific dependency runs on Windows; that is an inference, not a promise, and
it is filed as one. The Docker page has no inferred half: either there's a Dockerfile or there isn't.

## The eleven lists

Every entry here came from someone else's curation work. All eleven are credited on the workbook's
**Sources** sheet with their own star count and a screenshot, and each has its own page below:

| List | Curator | Entries | Page |
|---|---|---:|---|
| [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | ai-boost | 426 | [→](mega-list/lists/harness-engineering.md) |
| [awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026) | caramaschiHG | 264 | [→](mega-list/lists/ai-agents-2026.md) |
| [agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | sickn33 | 255 | [→](mega-list/lists/aas-skill-sources.md) |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | awesome-opencode | 219 | [→](mega-list/lists/opencode.md) |
| [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | e2b-dev | 215 | [→](mega-list/lists/agents-e2b.md) |
| [awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) | andyrewlee | 194 | [→](mega-list/lists/orchestrators.md) |
| [awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | heilcheng | 194 | [→](mega-list/lists/agent-skills.md) |
| [awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns) | nibzard | 193 | [→](mega-list/lists/agentic-patterns.md) |
| [awesome-agents](https://github.com/kyrolabs/awesome-agents) | kyrolabs | 165 | [→](mega-list/lists/agents-kyrolabs.md) |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | hesreallyhim | 153 | [→](mega-list/lists/claude-code.md) |
| [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | Shubhamsaboo | 116 | [→](mega-list/lists/llm-app-templates.md) |

If you maintain one of these: thank you, and please tell me if anything here misrepresents your list.

## What's in the workbook that isn't in the lists

Twenty-one sheets. The eleven source lists each get one, keeping the section headings their curator
published, so you can still read it the way they wrote it. Then:

- **Sources** — all eleven lists side by side: entries, distinct repos, total and median stars, how
  many entries are Windows-capable, screenshot coverage.
- **Leaderboard** — one row per repo across all eleven, ranked, with a consensus count.
- **By Category** — the same 1,294 repos grouped into the 14 topics and ranked *inside* each one, as a
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
- **The same repo arrives under several names.** GitHub redirects renamed repos for ever, so eleven
  lists written at different times link to the same project under different owners and every link
  works. `OpenDevin/OpenDevin`, `All-Hands-AI/OpenHands` and `OpenHands/OpenHands` are one project.
  Twenty-four repos were in here more than once that way. Every name is now resolved to the one the
  API reports, which took **1,102,114 double-counted stars off the total** — 258,781 from three repos
  spelled in two cases, and 843,333 from twenty that had simply been renamed.
- **Some entries are folders, not repos.** A skill that lives in a directory of someone else's
  monorepo has no star count of its own. Those rows show a dash rather than borrowing the parent's
  number, and they're excluded from the leaderboard.
- **Descriptions are the curators' words**, lightly normalised for length. The verdicts, platform
  columns, install commands and rankings are this project's.
- **Not every project is good.** This is a merged index, not an endorsement. Sort by last-push before
  you install anything.

## Staying current

Two GitHub Actions workflows keep the three surfaces from going stale, and neither needs a hand on it.

**Daily** ([`daily.yml`](.github/workflows/daily.yml), 11:12 UTC) asks each of the eleven source lists for
its newest commit. If none of them has moved, the job stops there — a rebuild would produce byte-identical
files. If any has, it refetches every repo's metadata, rebuilds the site and the Markdown edition, and
commits them, which is what republishes the site.

**Weekly** ([`weekly.yml`](.github/workflows/weekly.yml), Sundays) does all of that and then the expensive
part the daily run skips: capturing a screenshot for each new project, rebuilding both workbooks, and
publishing them as a dated release. That's why the [download links][dark] never rot — they point at
`releases/latest`, and each Sunday's release becomes the latest.

The split is about cost, not caution. Metadata for 1,294 repos is about seventy GraphQL queries.
Screenshots are 3,462 headless-browser renders. So a project added on Tuesday shows GitHub's own repo card
until Sunday, then gets its real image.

### The New filter

A project's arrival date is the one thing the API can't tell you — a repo created in 2023 can be new *to
this atlas* today. So the pipeline keeps its own ledger,
[`state/first-seen.json`](state/first-seen.json): the date each repo was first seen in any source list.
Everything already present when the ledger was created is stamped as founding stock, so day one marked
nothing.

Anything that arrives after that is marked for **fourteen days**:

- On the site, a **New** chip appears beside the sort control with a count on it, and clicking it narrows
  the table to exactly those projects. Their titles read `✨ ProjectName - New on 09/14/26`. The filter
  lives in the URL, so it's a link: [`#new=1`][new].
- In the Markdown edition, each topic and target page opens with a line saying how many arrived, and every
  marked row carries a ✨ and its date.

The fourteen days are counted in your browser against your own clock rather than fixed at build time, so a
mark expires on time whether or not anything was rebuilt that day. A `#new=1` link that has outlived its
window shows the whole atlas rather than an empty page.

## How it's built

A nineteen-stage Python pipeline: parse each source list's Markdown, resolve and fetch every repo
through the GitHub API, pull release and Actions metadata, classify OS support from README and CI
evidence, capture a screenshot per project, then render the workbooks with `openpyxl`, the Markdown
edition, and the site's dataset from the same in-memory records — so the three surfaces cannot
disagree. The topic and target assignments come from one taxonomy module all three read, which is why
`topics/agent-skills.md`, `#topic=agent-skills` and `Category = Agent Skills` are the same 278 rows.

The build cache (~4,800 files: fetched READMEs and screenshots) is deliberately **not** committed. It
is other people's content, it is 64 MB, and it is reproducible from the fetch scripts.

`state/first-seen.json` is the opposite case and is committed for the same reason: it is the only thing
here that a rebuild cannot recreate. Delete it and every project looks as old as every other one.

## Contributing

Corrections are the most valuable thing you can send. Especially:

- a platform verdict that's wrong for your project
- an install command that doesn't work
- a project that's dead, renamed, or filed under the wrong heading
- a list that should be merged in

Open an issue with the repo name and what's wrong. New source lists are welcome — the parser needs one
per list, so say which list and I'll add it.

## Licence and credit

This repository is **MIT** — see [LICENSE](LICENSE). MIT rather than Apache-2.0 deliberately: this is a
directory and a build pipeline, not a library with patent surface, and MIT's five clauses are the least
friction for anyone who wants to fork the data or reuse the scripts.

That covers **this project's own work**: the pipeline, the platform classifications, the merge, the
compilation. It does not relicense the eleven source lists — the descriptive text is the work of the
curators named above, each of whom retains their own licence, and every entry links back to both the
project and the list that found it. Star counts, languages and licences are facts from the GitHub API.

If you think something here should be attributed differently, open an issue and I'll fix it.

---

<div align="center">

**[Filter it live][site]** · **[Browse the mega list](mega-list/README.md)** ·
**[By topic](mega-list/topics/README.md)** · **[Leaderboard](mega-list/leaderboard.md)** ·
**[Download: dark][dark] / [light][light]**

</div>

[site]: https://crazy54.github.io/awesome-agentic-atlas/
[new]: https://crazy54.github.io/awesome-agentic-atlas/#new=1
[dark]: https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx
[light]: https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx
