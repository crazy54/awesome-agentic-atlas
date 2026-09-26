# MCP Servers (punkpeye)

A collection of MCP servers.

Curated by **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

4,295 entries · 4,269 distinct repos · 60 sections

[← back to the mega list](../README.md)

Page **7** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · **7**.

## Contents

- [Spirituality &amp; Esoterica](#spirituality--esoterica) (11)
- [Agreements &amp; Coordination](#agreements--coordination) (13)
- [Product Management](#product-management) (17)
- [Environment &amp; Nature](#environment--nature) (9)
- [Health &amp; Wellness](#health--wellness) (4)
- [Aerospace &amp; Astrodynamics](#aerospace--astrodynamics) (3)
- [Accessibility](#accessibility) (2)

## Spirituality &amp; Esoterica

<sub>Entries 8–11 of 11. The rest are on this page's other parts, linked above and below.</sub>

- **[alexsu1212/freebazi-mcp](https://github.com/alexsu1212/freebazi-mcp)** — Offline Bazi / Four Pillars (八字) MCP server: computes a full chart with True Solar Time and historical daylight-saving correction — Day Master, Ten Gods, hidden stems, Na Yin, Twelve Growth Stages, Shen Sha, branch relations (合冲刑害), and Da Yun luck pillars with the current period flagged. Engine cross-validated character-for-character against established libraries, no API key. Install: npx -y free
  <sub>TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx freebazi-mcp`</sub>
- **[asterwise/asterwise-mcp](https://github.com/asterwise/asterwise-mcp)** — Hosted Vedic and Western astrology MCP server (103 read-only tools): natal and divisional charts, five-level Vimshottari dasha, Ashtakavarga, Shadbala, yogas, panchanga and muhurta, Ashtakoota and Tamil porutham matching with Rajju/Vedha vetoes, KP, Lal Kitab, Western charts, numerology, tarot. Swiss Ephemeris precision, OAuth 2.1, free tier. Remote: https://mcp.asterwise.com/mcp
  <sub>Python · MIT · source · pushed 2026-09-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/asterwise/asterwise-mcp.git`</sub>
- **[davidmosiah/astral-mcp](https://github.com/davidmosiah/astral-mcp)** — Zero-setup astrology MCP server for natal charts, current transits, synastry, Moon phases and birthplace lookup, with privacy modes for compact agent payloads
  <sub>TypeScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y astral-mcp # stdio (default)`</sub>
- **[mihnin/stellara-mcp](https://github.com/mihnin/stellara-mcp)** — Stellara: deterministic Swiss Ephemeris tools for Western astrology — natal chart (14 points, houses, angles, aspects with exact orbs and applying/separating), transits to a natal chart, synastry, and a birth-place resolver that turns "Warsaw, 17 May 1990 14:30" into coordinates plus the historically correct UTC offset. No AI inside, nothing stored. Install: npx -y stellara-mcp (free key at https:
  <sub>TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y stellara-mcp`</sub>

## Agreements &amp; Coordination

- **[Vladimir-Human/humanizer-ru](https://github.com/Vladimir-Human/humanizer-ru)** — MCP server (stdio, JSON-RPC 2.0, standard library only) for detecting and normalizing machine-generation traces in Russian text: four tools (scan, markers, polish, detect), schemas generated from the contract, no authorship verdicts
  <sub>★ 126 · Python · MIT · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install humanizer-ru`</sub>
- **[BrightbeamAI/chap](https://github.com/BrightbeamAI/chap)** — Official CHAP Coordinator MCP server for auditable human-agent collaboration: approvals, overrides, handoffs, escalations, and hash-linked evidence. Run locally with npx -y @brightbeamai/chap-coordinator-mcp
  <sub>★ 104 · HTML · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install chap-coordinator`</sub>
- **[tribeunal/mcp-server](https://github.com/tribeunal/mcp-server)** — Community jury platform where humans and AI agents open cases, weigh evidence and vote together; 39 tools plus eight Agent Skills, long-poll verdict awaiting, arbitration mode and HMAC-signed webhooks. Remote Streamable HTTP at https://mcp.tribeunal.com/mcp (OAuth) or local stdio via npx -y @tribeunal/mcp-server
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add tribeunal/mcp-server # the entry skill alone`</sub>
- **[CNSLabs/agreements-api-sdk](https://github.com/CNSLabs/agreements-api-sdk)** — Remote Streamable HTTP and local stdio MCP server for defining, validating, deploying, and operating machine-readable agreements with EIP-712 permit preparation, signed participant inputs, state reads, and input history
  <sub>★ 2 · TypeScript · Apache-2.0 · source · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CNSLabs/agreements-api-sdk.git`</sub>
- **[elicitly/elicitly](https://github.com/elicitly/elicitly)** — Human-in-the-loop over MCP elicitation: elicit_confirm (OK/Cancel) and elicit_form (typed fields from your JSON schema) raise native dialogs in the connected host, and elicit_doctor reports which elicitation features the host actually supports. Local stdio via npx -y elicitly
  <sub>★ 1 · TypeScript · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y elicitly`</sub>
- **[humanforai/humanforai-mcp](https://github.com/humanforai/humanforai-mcp)** — Hire a real human operator for tasks that need physical presence, perception, or judgment: real-world verification, product testing, AI output review, data collection, and local errands. Remote streamable HTTP at https://humanforai.dev/mcp or local stdio via npx -y humanforai
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/humanforai/humanforai-mcp.git`</sub>
- **[lanekingsbery/open-task-relay-public](https://github.com/lanekingsbery/open-task-relay-public)** — Open Task Relay provides free, bounded public-good tasks that autonomous AI agents can discover, complete, submit, and independently verify
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lanekingsbery/open-task-relay-public.git`</sub>
- **[cogdepot/mcp-server](https://github.com/cogdepot/mcp-server)** — Official server for cogDepot, an anonymous broker where agents publish capability listings, negotiate terms, and form direct peer-to-peer deals backed by escrow and two-sided reputation. Five tools need no account at all - what the broker does and what it costs, how to get a key, a preview of the live board, any agent's public reputation record, and the marketplace's aggregate stats; with a key, r
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @cogdepot/mcp-server`</sub>
- **[decision-anchor/mcp-server](https://github.com/decision-anchor/mcp-server)** — External anchoring layer that records AI agent accountability boundaries on both sides — content-blind, non-judgmental. Remote streamable HTTP at https://mcp.decision-anchor.com/mcp; free trial, then pay-per-call USDC (x402) on Base
  <sub>JavaScript · Apache-2.0 · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/decision-anchor/mcp-server.git`</sub>
- **[ianewsfr-a11y/ergonia](https://github.com/ianewsfr-a11y/ergonia)** — A marketplace of verifiable tasks for AI agents: agents register, publish tasks whose completion a stranger can independently check, submit work, and build public reputation. Every action is recorded in a hash-chained register anyone can re-verify. Read access needs no key at https://ergonia.works/mcp/read; writes use a Bearer token obtained once from POST /api/register
  <sub>TypeScript · AGPL-3.0 · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ianewsfr-a11y/ergonia.git`</sub>
- **[gofrantic/frantic-mcp](https://github.com/gofrantic/frantic-mcp)** — A public bounty board where AI agents do paid work. Claim funded bounties, deliver artifacts in the open, and get paid in USDC on Base only when a delivery is accepted, with every claim, judgment, and payout sealed to a public receipt ledger anyone can verify. Vendors hire the Town from the other side: post a task with its acceptance criteria and fund it in the same call. 14 tools across onboardin
  <sub>TypeScript · MIT · npx · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y frantic-mcp`</sub>
- **[TheRealDalaiLama/glyphdna-mcp](https://github.com/TheRealDalaiLama/glyphdna-mcp)** — Machine-native identity, verifiable multi-party meeting rooms (co-signed transcript receipts), and script provenance chains. Agents hold their own Ed25519 keys; join is one MCP call. Python, dependency-free
  <sub>Python · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TheRealDalaiLama/glyphdna-mcp.git`</sub>
- **[sttruji/mundane-mcp](https://github.com/sttruji/mundane-mcp)** — Hire ID-verified people for work that needs hands, eyes, or physical presence: errands, photos of a real place, queue-sitting, and in-person bookings. Agents post a task with location, budget, deadline, and required capabilities, search nearby workers by skill and rating, and make an escrow-backed offer — funds are held until proof of completion is reviewed. Covers the full lifecycle: wallet top-u
  <sub>Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mundane-mcp # from PyPI — no checkout needed`</sub>

## Product Management

- **[spranab/saga-mcp](https://github.com/spranab/saga-mcp)** — A Jira-like project tracker for AI agents with full hierarchy (Projects > Epics > Tasks > Subtasks), task dependencies with auto-block/unblock, threaded comments, reusable templates, activity logging, and a natural language dashboard. SQLite-backed, 31 tools
  <sub>★ 37 · JavaScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g saga-mcp`</sub>
- **[dkships/pm-copilot](https://github.com/dkships/pm-copilot)** — Triangulates HelpScout support tickets and ProductLift feature requests to generate prioritized product plans. Scores themes by convergence (same signal in both sources = 2x boost), scrubs PII, and accepts business metrics from other MCP servers via kpi_context for composable prioritization
  <sub>★ 30 · TypeScript · MIT · clone · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dkships/pm-copilot.git`</sub>
- **[devemberx/mcp-server-polarion](https://github.com/devemberx/mcp-server-polarion)** — Polarion ALM integration with 24 read/write tools for documents, work items, traceability links, and comments. Renders documents as Markdown, searches with Lucene or SQL, walks incoming/outgoing links, and creates/updates/reorganizes work items. Every write tool supports dry_run with pre-write field, enum, and link-target validation. Requires Polarion 2506+. uvx mcp-server-polarion
  <sub>★ 15 · Python · MIT · uv · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-server-polarion`</sub>
- **[TylerIlunga/procore-mcp-server](https://github.com/TylerIlunga/procore-mcp-server)** — MCP server exposing the full Procore REST API (2,636 endpoints) for construction project management. Includes 7 discovery and execution tools covering projects, RFIs, submittals, daily logs, budgets, and more. Single-user OAuth with auto-refresh
  <sub>★ 9 · TypeScript · MIT · clone · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TylerIlunga/procore-mcp-server.git`</sub>
- **[KyaniteLabs/Epoch](https://github.com/KyaniteLabs/Epoch)** — Software estimation server for AI agents: PERT, COCOMO II, Monte Carlo, sprint forecasting, token-to-time and cost mapping, and schedule-risk tools
  <sub>★ 8 · TypeScript · Apache-2.0 · clone · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KyaniteLabs/Epoch.git`</sub>
- **[agrath/Trello-Desktop-MCP](https://github.com/agrath/Trello-Desktop-MCP)** — Comprehensive Trello integration: 46 tools covering boards, cards, lists, labels, checklists, attachments, members, custom fields, and search. Read-only mode, image attachment
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx atlassian-trello-mcp`</sub>
- **[illodev/workfile](https://github.com/illodev/workfile)** — Work, Docs, History and durable Memory as Markdown inside the repository, so the backlog reviews, branches and merges with the code that answers it. Cards carry a lifecycle and a claim, so parallel agents refuse to edit a card another actor holds. 30 tools, plus a CLI, a Claude Code plugin and a local UI. npx -y @illodev/workfile mcp
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pnpm add -g @illodev/workfile # or globally: `workfile` lands on your PATH`</sub>
- **[negoro26/mcp-taiga](https://github.com/negoro26/mcp-taiga)** — Taiga project management MCP server: issues, user stories, tasks, epics, sprints, comments, attachments, and wiki via six op-dispatching tools (about 2.8k-token tool schema). Resolves project slugs, #references, and status names server-side. Runs via npx or Docker over stdio, or streamable HTTP for remote clients
  <sub>★ 2 · TypeScript · MIT · docker · pushed 2026-09-25 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i --env-file .env mcp-taiga`</sub>
- **[xfloukiex-lab/road-poneglyph](https://github.com/xfloukiex-lab/road-poneglyph)** — Reviews a plan for what's missing — unstated assumptions, omitted technical risks, and execution blind spots (a structured pre-mortem). pip install road-poneglyph-mcp
  <sub>★ 2 · Python · Apache-2.0 · pip · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install road-poneglyph-mcp`</sub>
- **[daiji-sshr/redmine-mcp-stateless](https://github.com/daiji-sshr/redmine-mcp-stateless)** — Stateless Redmine MCP server. Credentials are passed per-request via HTTP headers and never stored on the server. Supports listing/creating/updating issues, full-text search across subjects, descriptions and comments, and editing journals (Redmine 5.0+). Deployable on RHEL (systemd) or Docker
  <sub>★ 1 · Python · MIT · source · pushed 2026-07-02 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/daiji-sshr/redmine-mcp-stateless.git`</sub>
- **[Lukaris/framedeck-mcp](https://github.com/Lukaris/framedeck-mcp)** — Framedeck is a Kanban content production manager for YouTube, Instagram, TikTok and Podcast creators. 32 tools for managing productions, stages, frames (cards), checklists, comments, and labels. Ideas land in an Idea Pool and graduate into full productions with stages (Idea → Scripting → Filming → Editing → Published). All tools ship with MCP safety annotations. npx framedeck-mcp
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-04-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx framedeck-mcp`</sub>
- **[mohamed-ashraf-elsaed/loupe](https://github.com/mohamed-ashraf-elsaed/loupe)** — Turns pinned visual product feedback into an actionable backlog: list comments, read one with its target element's HTML, computed styles and screenshot, and update its status. Powers the Loupe SDK, browser extension, and loupekit/laravel package. Install @loupekit/mcp (binary loupe-mcp)
  <sub>★ 1 · TypeScript · source · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mohamed-ashraf-elsaed/loupe.git`</sub>
- **[gonnagetapower/kelvia-mcp](https://github.com/gonnagetapower/kelvia-mcp)** — Kelvia task manager an agent can fully operate: boards, tasks, sprints, member roles, worklogs and a time-blocking day planner. 58 tools with MCP safety annotations and selectable toolsets. Hosted endpoint with OAuth 2.1 — one command, no token to paste. npx kelvia-mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx kelvia-mcp`</sub>
- **[andrelaptenok/redmine-mcp-stdio](https://github.com/andrelaptenok/redmine-mcp-stdio)** — Search, read, create and update Redmine issues, projects and time entries from any MCP client. 12 tools with MCP safety annotations: full-text search, issue journals with attachments, comments and time tracking. npx -y redmine-mcp-stdio
  <sub>TypeScript · MIT · source · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/andrelaptenok/redmine-mcp-stdio.git`</sub>
- **[AIOProductOS/claude-plugin](https://github.com/AIOProductOS/claude-plugin)** — Product management over a shared product spine: link customer feedback and insights to features, tasks, sprints, releases and objectives; weekly signal memo; roadmap-drift detection; customer 360, funnel, path, retention, NPS and NRR analytics; artifact versioning and identity resolution. 38 tools, hosted remote server with OAuth 2.1 (DCR + PKCE)
  <sub>JavaScript · MIT · npx · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @aioproductoscom/mcp`</sub>
- **[igorolv/redmine-mcp-server](https://github.com/igorolv/redmine-mcp-server)** — Redmine for AI agents: issues, projects, wiki, attachments (PDF/DOCX/ZIP text extraction), time entries, release and blocker analytics; read-only by default with optional write tools
  <sub>Java · MIT · docker · pushed 2026-09-15 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -i --rm -e REDMINE_URL=https://redmine.example.com -e REDMINE_API_KEY=your_key ghcr.io/igorolv/redmine-mcp-server:latest`</sub>
- **[kenzotp/mcp-server-zuuna](https://github.com/kenzotp/mcp-server-zuuna)** — MCP server for Zuuna developer project management: 8 tools for boards, cards, moves, and comments over the Zuuna v1 API; the agent reads the board, codes in the repo, and when the PR merges, git activity moves the card. npx -y mcp-server-zuuna
  <sub>TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-server-zuuna`</sub>

## Environment &amp; Nature

- **[Zhonghao1995/agentic-swmm-workflow](https://github.com/Zhonghao1995/agentic-swmm-workflow)** — Eleven MCP servers exposing a reproducible EPA SWMM stormwater-modelling workflow: model building, simulation runs with manifests and continuity checks, calibration, GIS/QGIS integration, design storms and climate scenarios, uncertainty analysis, plotting, and modelling memory. Config generators included for Codex, Claude Code, OpenClaw, and Hermes
  <sub>★ 29 · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add Zhonghao1995/agentic-swmm-workflow`</sub>
- **[Zhonghao1995/Agentic-MIKE-Plus](https://github.com/Zhonghao1995/Agentic-MIKE-Plus)** — MCP server (10 tools) for a headless, natural-language DHI MIKE+ urban-water modelling workflow: model inspection, parameter read/edit, headless simulation runs with parsed QA status, .res1d results reading, and plotting (hydrographs, time series, network maps). Read/plot is license-free; run/edit need Windows + a MIKE+ 2026 license. Works with Claude Code, Codex, OpenClaw, and Hermes
  <sub>★ 8 · Python · MIT · npx · pushed 2026-08-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add Zhonghao1995/Agentic-MIKE-Plus # all 10`</sub>
- **[zax0rz/birdnet-go-mcp](https://github.com/zax0rz/birdnet-go-mcp)** — Fast, read-only MCP server &amp; CLI for BirdNET-Go bioacoustic observatories. Query recent detections, stream outdoor mic telemetry, resolve LAN audio recordings, and inspect sightings with LLMs
  <sub>★ 4 · Go · MIT · npx · pushed 2026-09-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y birdnet-go-mcp status`</sub>
- **[aliafsahnoudeh/wildfire-mcp-server](https://github.com/aliafsahnoudeh/wildfire-mcp-server)** — MCP server for detecting, monitoring, and analyzing potential wildfires globally using multiple data sources including NASA FIRMS, OpenWeatherMap, and Google Earth Engine
  <sub>★ 2 · Python · npx · pushed 2025-12-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector python wildfire_mcp_server.py`</sub>
- **[nalediym/touch-grass](https://github.com/nalediym/touch-grass)** — Claude Code plugin and MCP server that nudges you to take outdoor breaks based on local weather, sunset timing, and session streaks. Tools: check_grass_conditions, suggest_activity, log_touch_grass, get_stats. Fully local, no API keys, no cloud storage
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-04-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nalediym/touch-grass`</sub>
- **[atmospore/atmospore-mcp](https://github.com/atmospore/atmospore-mcp)** — Per-species pollen forecasts at any point on Earth, seven days ahead, via the Atmospore API. Tools: get_pollen, get_top_species, get_area_average, list_supported_species. Free tier (100 calls/day, no credit card). Hosted variant at mcp.atmospore.com
  <sub>★ 1 · Python · MIT · pip · pushed 2026-05-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install atmospore-mcp`</sub>
- **[ambeelabs/ambee-mcp](https://github.com/ambeelabs/ambee-mcp)** — The official Model Context Protocol server for Ambee. It gives any MCP-compatible AI assistant — Claude, ChatGPT, Cursor, VS Code, Ollama, and more — direct access to live air quality, pollen, and weather data
  <sub>JavaScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/getambee/ambee-mcp-server.git`</sub>
- **[gridcarbon/clients](https://github.com/gridcarbon/clients)** — Grid carbon intensity (gCO2eq/kWh) for 45 electricity zones: 33 European bidding zones (ENTSO-E), 11 US balancing authorities (EIA-930), and Great Britain (NESO). Tools: get_carbon_intensity, get_intensity_history, list_zones, compare_zones. Every response carries the interval timestamp and how stale the reading is, so an agent can tell a current value from an hours-old one. Pre-alpha; history cur
  <sub>TypeScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx gridcarbon-mcp`</sub>
- **[malonestar/gov-data-mcp](https://github.com/malonestar/gov-data-mcp)** — 120 US government open-data sources (EPA contamination and drinking water, FEMA flood and risk index, USGS, NOAA, FAA airspace, USACE levees and dams, FDIC, HUD, NRCS soils, county assessor rolls, state licensing boards) as agent-callable tools. Runs locally over stdio with npx gov-data-mcp; 12 dedicated tools plus search-gov-data-tools / describe-gov-data-tool / run-gov-data-tool to reach the res
  <sub>JavaScript · MIT · npx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx gov-data-mcp`</sub>

## Health &amp; Wellness

- **[io.github.PhilipAD/health-export-mcp](https://github.com/PhilipAD/health-export-mcp)** — Query 190 Apple Health metrics from any MCP agent — zero-dependency, read-only, local-first
  <sub>★ 5 · JavaScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx health-export-mcp`</sub>
- **[Thecimal/quantified-self-mcp](https://github.com/Thecimal/quantified-self-mcp)** — Query your personal health and finance data from Claude Desktop. Two local SQLite files, read directly off disk by a Python process you control — no cloud database, no dashboard, no third-party service
  <sub>★ 5 · Python · MIT · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install quantified-self-mcp`</sub>
- **[findsaunaplunge/mcp](https://github.com/findsaunaplunge/mcp)** — Cold plunge, sauna and contrast-therapy venues across 23 US metros, with published temperatures and prices quoted from each venue's own pages and dated. Hosted at https://findsaunaplunge.com/mcp (Streamable HTTP, no auth); tools: search_venues, get_venue, list_cities, get_city_stats, get_data_freshness
  <sub>TypeScript · MIT · source · pushed 2026-09-05 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/findsaunaplunge/mcp.git`</sub>
- **[proscar87/oura-mcp](https://github.com/proscar87/oura-mcp)** — All 19 Oura Ring v2 collections in three tools, with no analysis done in the server. Paginates to exhaustion and reports the page count: one local day of heart rate is 1,231 samples across 2 pages, and a client that stops at the first returns 81% of them with nothing saying so. One-click .mcpb for Claude Desktop, and it runs on Oura's official sample data with no account
  <sub>Python · MIT · uv · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from mcp-oura oura-mcp`</sub>

## Aerospace &amp; Astrodynamics

- **[gregario/astronomy-oracle](https://github.com/gregario/astronomy-oracle)** — Accurate astronomical catalog data and observing session planner. 13,000+ deep-sky objects from OpenNGC with deterministic visibility, rise/transit/set, and alt/az calculations. npx astronomy-oracle
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g astronomy-oracle`</sub>
- **[viventine-space/orbit-sentinel-mcp](https://github.com/Viventine-Space/orbit-sentinel-mcp)** — Search 419,000+ space regulatory filings from FCC, ITU, UNOOSA, and FAA — semantic search, entity dossiers, spectrum holdings, launch licenses, and filing alerts, powered by Orbit Sentinel. brew install --cask viventine-space/tap/orbit-sentinel-mcp
  <sub>★ 1 · Go · MIT · npx · pushed 2026-09-06 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx mcp-remote https://orbit-sentinel.viventine.com/mcp`</sub>
- **[IO-Aerospace-software-community/mcp-server](https://github.com/IO-Aerospace-software-engineering/mcp-server)** — #️⃣ ☁️/🏠 🐧 - IO Aerospace MCP Server: a .NET-based MCP server for aerospace &amp; astrodynamics — ephemeris, orbital conversions, DSS tools, time conversions, and unit/math utilities. Supports STDIO and SSE transports; Docker and native .NET deployment documented
  <sub>unavailable</sub>

## Accessibility

- **[kinti/a11y-toolkit](https://github.com/kinti/a11y-toolkit)** — MCP server + CLI for WCAG 2.2 accessibility: color contrast (pairs plus pixel-level text-over-image sampling), EU accessibility declaration generation (RD 1112/2018, Ley 11/2023 / European Accessibility Act, EN 301 549), and an aria-live announcement monitor. Multilanguage es/en, zero dependencies
  <sub>★ 1 · Python · MIT · clone · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kinti/a11y-toolkit`</sub>
- **[vince-gonzalez/opticquiz-mcp](https://github.com/vince-gonzalez/opticquiz-mcp)** — Color-vision accessibility. Check whether a palette or an image is colorblind-safe and name the conflicting pairs, generate colorblind-safe palettes (Okabe-Ito seeded), recolor an image as protanopia/deuteranopia/tritanopia renders it, and generate Ishihara-style test plates. Built on Machado, Oliveira &amp; Fernandes (2009) + CIEDE2000, published open access at doi.org/10.5281/zenodo.21310578. Runs l
  <sub>JavaScript · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vince-gonzalez/opticquiz-mcp.git`</sub>

Page **7** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · **7**.

---

Snapshot 2026-09-26. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
