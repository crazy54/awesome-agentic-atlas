# Claude Code Toolkit

The most comprehensive toolkit for Claude Code -- 135 agents, 35 curated skills, 42 commands, 176+ plugins, 20 hooks, 15 rules, 7 templates, 14 MCP configs, 26 companion apps, 52 ecosystem entries, and more.

Curated by **[rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

699 entries · 328 distinct repos · 34 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/garrytan/gstack"><img src="https://raw.githubusercontent.com/garrytan/gstack/main/docs/images/github-2026.png" width="260"></a> | <a href="https://github.com/thedotmack/claude-mem"><img src="https://raw.githubusercontent.com/thedotmack/claude-mem/main/docs/public/cm-preview.gif" width="260"></a> | <a href="https://github.com/wshobson/agents"><img src="https://opengraph.githubassets.com/1/wshobson/agents" width="260"></a> |
| **[gstack](https://github.com/garrytan/gstack)**<br>★ 133.8k | **[claude-mem](https://github.com/thedotmack/claude-mem)**<br>★ 94.4k | **[wshobson/agents](https://github.com/wshobson/agents)**<br>★ 39.8k |
| <a href="https://github.com/Yeachan-Heo/oh-my-claudecode"><img src="https://opengraph.githubassets.com/1/Yeachan-Heo/oh-my-claudecode" width="260"></a> | <a href="https://github.com/BloopAI/vibe-kanban"><img src="https://opengraph.githubassets.com/1/BloopAI/vibe-kanban" width="260"></a> | <a href="https://github.com/winfunc/opcode"><img src="https://opengraph.githubassets.com/1/winfunc/opcode" width="260"></a> |
| **[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)**<br>★ 39.3k | **[vibe-kanban](https://github.com/BloopAI/vibe-kanban)**<br>★ 28.2k | **[opcode](https://github.com/winfunc/opcode)**<br>★ 22.4k |

## Contents

- [Featured](#featured) (2)
- [All Plugins](#all-plugins) (236)
- [Research &amp; Analysis](#research--analysis) (13)
- [Core Development](#core-development) (13)
- [Language Experts](#language-experts) (25)
- [Infrastructure](#infrastructure) (11)
- [Quality Assurance](#quality-assurance) (10)
- [Data &amp; AI](#data--ai) (16)
- [Developer Experience](#developer-experience) (15)
- [Specialized Domains](#specialized-domains) (15)
- [Business &amp; Product](#business--product) (12)
- [Orchestration](#orchestration) (8)
- [Community Skills](#community-skills) (86)
- [Skills](#skills) (1)
- [SKY-lv Skills](#sky-lv-skills) (6)
- [Git](#git) (7)
- [Testing](#testing) (6)
- [Architecture](#architecture) (6)
- [Documentation](#documentation) (5)
- [Security](#security) (5)
- [Refactoring](#refactoring) (5)
- [DevOps](#devops) (5)
- [Workflow](#workflow) (3)
- [Ecosystem](#ecosystem) (76)
- [Companion Apps &amp; GUIs](#companion-apps--guis) (39)
- [Hook Scripts](#hook-scripts) (1)
- [Related SDKs](#related-sdks) (2)
- [MCP Configs](#mcp-configs) (16)
- [Templates](#templates) (11)
- [Rules](#rules) (15)
- [Contexts](#contexts) (5)
- [Related Awesome Lists](#related-awesome-lists) (9)
- [Examples](#examples) (3)
- [Resources](#resources) (11)

## Featured

- **[gstack](https://github.com/garrytan/gstack)** — Garry Tan's exact Claude Code setup: 6 opinionated tools that serve as CEO, Eng Manager, Release Manager, and QA Engineer
  <sub>★ 133.8k · TypeScript · MIT · source · pushed 2026-09-21 · macOS</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git`</sub>
- **[pro-workflow](https://github.com/rohitg00/pro-workflow)** — Battle-tested Claude Code workflows from power users. Self-correcting memory, parallel worktrees, wrap-up rituals, 8 hook types, 5 agents, and the 80/20 AI coding ratio. Install: /plugin marketplace add rohitg00/pro-workflow
  <sub>★ 2.9k · JavaScript · npx · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add rohitg00/pro-workflow`</sub>

## All Plugins

- **[claude-mem](https://github.com/thedotmack/claude-mem)** — Automatically captures everything Claude does, compresses with AI, injects relevant context into future sessions. SQLite + full-text search. 35,900+ stars
  <sub>★ 94.4k · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-mem`</sub>
- **[wshobson/agents](https://github.com/wshobson/agents)** — 112 specialized agents, 16 multi-agent workflow orchestrators, 146 skills, 79 tools in 72 focused plugins. 31,300+ stars
  <sub>★ 39.8k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx codex-marketplace add wshobson/agents # Codex`</sub>
- **[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)** — Teams-first multi-agent orchestration. 19 specialized agents, 28 skills. Full autonomous execution, Socratic questioning, N coordinated agents. 9,900+ stars
  <sub>★ 39.3k · TypeScript · MIT · source · pushed 2026-09-21 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/Yeachan-Heo/oh-my-claudecode.git`</sub>
- **[vibe-kanban](https://github.com/BloopAI/vibe-kanban)** — Kanban-based orchestration for 10+ coding agents (Claude Code, Codex, Gemini CLI, Copilot, Amp). Isolated git worktrees per agent, inline diff review. 23,200+ stars
  <sub>★ 28.2k · Rust · Apache-2.0 · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibe-kanban`</sub>
- **[opcode](https://github.com/winfunc/opcode)** — Tauri 2 desktop GUI and toolkit for Claude Code. Manage sessions, create custom agents with visual editor, usage analytics, MCP integration. 21,000+ stars
  <sub>★ 22.4k · TypeScript · AGPL-3.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/getAsterisk/opcode.git`</sub>
- **[ccusage](https://github.com/ccusage/ccusage)** — CLI for analyzing Claude Code/Codex usage from local JSONL files. Daily, monthly, session, billing-window reports. Offline, zero API calls. 11,500+ stars
  <sub>★ 18.7k · Rust · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ryoppippi/ccusage.git`</sub>
- **[claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)** — Extracted system prompts from Claude Code -- 18 builtin tool descriptions, sub-agent prompts, utility prompts. Updated for each release. 5,900+ stars
  <sub>★ 12.7k · JavaScript · MIT · source · pushed 2026-09-19 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/Piebald-AI/claude-code-system-prompts.git`</sub>
- **[claude-context](https://github.com/zilliztech/claude-context)** — Semantic code search MCP server by Zilliz (Milvus creators). Hybrid BM25 + dense vector search. ~40% token reduction. 5,600+ stars
  <sub>★ 12.6k · TypeScript · MIT · npx · pushed 2026-07-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @zilliz/claude-context-mcp@latest`</sub>
- **[ccpm](https://github.com/automazeio/ccpm)** — Project management using GitHub Issues + Git worktrees for parallel agent execution. Issue-analyze, epic-start, epic-merge commands. 7,600+ stars
  <sub>★ 8.4k · Shell · MIT · clone · pushed 2026-03-18</sub>
  <sub>`git clone https://github.com/automazeio/ccpm.git`</sub>
- **[peon-ping](https://github.com/PeonPing/peon-ping)** — Warcraft III Peon voice notifications (+ StarCraft, Portal, Zelda) for Claude Code and other agents. Desktop banners, auto-detects SSH/devcontainers. 3,900+ stars
  <sub>★ 5k · Shell · MIT · brew · pushed 2026-08-30 · macOS</sub>
  <sub>`brew install PeonPing/tap/peon-ping`</sub>
- **[claude-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)** — Complete mastery guide for Claude Code hooks -- UV single-file Python scripts, sub-agents, meta-agent, team-based validation, AI-generated audio feedback. 3,300+ stars
  <sub>★ 3.9k · Python · source · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/disler/claude-code-hooks-mastery.git`</sub>
- **[toprank](https://github.com/nowork-studio/notfair-plugin)** — SEO + Google Ads plugin for Claude Code. Pulls real Search Console data and Google Ads API data, audits traffic and wasted ad spend, rewrites meta tags, generates JSON-LD schema, and ships the fixes. 9 skills across SEO, Ads, and cross-model review
  <sub>★ 3.8k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[claude-supermemory](https://github.com/supermemoryai/claude-supermemory)** — Persistent memory across sessions and projects using Supermemory. User profile injection at session start, automatic conversation capture. 2,300+ stars
  <sub>★ 2.8k · HTML · source · pushed 2026-09-17</sub>
  <sub>`git clone https://github.com/supermemoryai/claude-supermemory.git`</sub>
- **[myclaude](https://github.com/stellarlinkco/myclaude)** — Multi-agent orchestration routing tasks to Claude Code, Codex, Gemini, and OpenCode based on complexity. OmO skill for intelligent routing. 2,400+ stars
  <sub>★ 2.7k · Go · AGPL-3.0 · npx · pushed 2026-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:stellarlinkco/myclaude`</sub>
- **[brooks-lint](https://github.com/hyhmrright/brooks-lint)** — AI code reviews grounded in six classic engineering books (Brooks, Fowler, Martin, McConnell, Hunt &amp; Thomas, Evans). Diagnoses code across 6 decay risk dimensions with structured findings (Symptom → Source → Consequence → Remedy). Supports PR review, architecture audit, tech debt assessment, and test quality review. v0.6 adds Mermaid dependency graphs
  <sub>★ 1.5k · HTML · MIT · script · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/hyhmrright/brooks-lint/main/scripts/install.sh | bash -s -- <platform>`</sub>
- **[codesight](https://github.com/Houseofmvps/codesight)** — CLI token optimizer and AI context generator. Scans codebases to extract routes, schema, components, and dependencies for Claude Code, Cursor, Copilot, Codex, and Windsurf. 9x–13x token reduction. Zero runtime dependencies. npx codesight
  <sub>★ 1.4k · TypeScript · MIT · npm · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codesight`</sub>
- **[claude-code-mcp](https://github.com/steipete/claude-code-mcp)** — Run Claude Code as a one-shot MCP server -- an agent in your agent. Permissions bypassed automatically. By Peter Steinberger. 1,100+ stars
  <sub>★ 1.3k · JavaScript · MIT · source · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/steipete/claude-code-mcp.git`</sub>
- **[ccmanager](https://github.com/kbwo/ccmanager)** — Coding agent session manager supporting Claude Code, Gemini CLI, Codex, Cursor, Copilot, Cline, OpenCode, Kimi CLI. Smart auto-approval via Haiku, devcontainer support. 940+ stars
  <sub>★ 1.2k · TypeScript · MIT · npm · pushed 2026-09-13 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g ccmanager`</sub>
- **[claude-forge](https://github.com/sangrokjung/claude-forge)** — "oh-my-zsh for Claude Code". Complete toolkit: 11 agents, 33 commands, 24 skills, 15 hooks (covering 21 lifecycle events) + 9 opt-in examples, 9 rules, 4 MCP servers (playwright, context7, jina-reader, chrome-devtools@0.23.0), statusLine. One install via curl ... install.sh or /plugin marketplace add sangrokjung/claude-forge. Includes TDD workflow, multi-reviewer pipeline (codex/gemini/security/ar
  <sub>★ 841 · Shell · MIT · script · pushed 2026-09-03 · macOS</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/sangrokjung/claude-forge/main/install.sh | bash`</sub>
- **[claude-notifications-go](https://github.com/777genius/agent-notifications)** — Cross-platform smart notifications -- 6 types, click-to-focus, context analysis, webhooks. Single Go binary, zero deps. 340+ stars
  <sub>★ 815 · Go · source · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/777genius/claude-notifications-go.git`</sub>
- **[onWatch](https://github.com/onllm-dev/onWatch)** — Open-source Go CLI that tracks AI API quota usage across 7 providers (Synthetic, Z.ai, Anthropic, Codex, GitHub Copilot, MiniMax, Antigravity) with a background daemon (&lt;50 MB RAM), zero telemetry, and a Material Design 3 web dashboard
  <sub>★ 743 · Go · GPL-3.0 · psh · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/onllm-dev/onwatch/main/install.ps1 | iex`</sub>
- **[chief](https://github.com/MiniCodeMonkey/chief)** — CLI that wraps Claude Code in a loop. Define a PRD, run chief, go do anything else. Commits after each task, picks up where it left off. Homebrew installable. 380+ stars
  <sub>★ 475 · Go · MIT · brew · pushed 2026-05-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install minicodemonkey/chief/chief`</sub>
- **[cozempic](https://github.com/Ruya-AI/cozempic)** — v1.2.x — Self-updating now, atomic writes, strict session guard, zero false positives on team detection. 13 pruning strategies, Agent Team protection, MCP server, JSONL doctor. Install: /plugin marketplace add Ruya-AI/cozempic
  <sub>★ 417 · Python · MIT · npm · pushed 2026-07-03 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g cozempic`</sub>
- **[humanizer-skill](https://github.com/Aboudjem/humanizer-skill)** — Detects 37 AI writing patterns and rewrites text with human rhythm. 5 voice profiles (casual, professional, technical, warm, blunt). Based on burstiness/perplexity research. Zero dependencies
  <sub>★ 249 · JavaScript · MIT · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Aboudjem/humanizer-skill`</sub>
- **[claude-cybersecurity](https://github.com/AgriciDaniel/claude-cybersecurity)** — AI-powered cybersecurity code review with 8 parallel agents. OWASP 2025, CWE Top 25, MITRE ATT&amp;CK, 11 languages, 5 compliance frameworks, threat intelligence. Zero config. MIT
  <sub>★ 223 · Shell · MIT · script · pushed 2026-04-15 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-cybersecurity/main/install.sh | bash`</sub>
- **[claude-ops](https://github.com/Lifecycle-Innovations-Limited/claude-ops)** — Business operating system plugin for Claude Code. Morning briefings, unified inbox, autonomous PR merge, infrastructure monitoring, and YOLO autonomous mode
  <sub>★ 221 · Shell · MIT · clone · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/Lifecycle-Innovations-Limited/claude-ops.git`</sub>
- **[production-grade](https://github.com/nagisanzenin/production-grade)** — 14-agent autonomous pipeline — PM, Architect, Backend, Frontend, QA, Security, Code Review, DevOps, SRE, Data Scientist, Technical Writer, Skill Maker, Polymath co-pilot. Two-wave parallel execution, brownfield-safe
  <sub>★ 177 · JavaScript · clone · pushed 2026-08-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nagisanzenin/production-grade.git`</sub>
- **[ORCH](https://github.com/oxgeneral/ORCH)** — CLI runtime orchestrating Claude Code, Codex, and Cursor as typed agent teams with state machine (todo→review→done), auto-retry, inter-agent messaging, goals, and TUI dashboard
  <sub>★ 164 · TypeScript · MIT · npm · pushed 2026-08-01 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @oxgeneral/orch # Install`</sub>
- **[claude-rank](https://github.com/Houseofmvps/claude-rank)** — SEO/GEO/AEO audit plugin — tells you why AI won't cite your site, then auto-fixes robots.txt, sitemap.xml, llms.txt, and JSON-LD. 170+ rules across 10 scanners, zero config
  <sub>★ 146 · JavaScript · MIT · npm · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @houseofmvps/claude-rank # scoped (official)`</sub>
- **[unslop](https://github.com/MohamedAbdallah-14/unslop)** — Removes AI writing tells (tricolons, em-dash pileups, hedging stacks, sycophancy openers, stock vocabulary). Split lint/rewrite modes — run detection-only passes on your own text without rewriting. Five intensity levels. MIT licensed
  <sub>★ 144 · Python · MIT · pipx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install unslop`</sub>
- **[skills-janitor](https://github.com/khendzel/skills-janitor)** — Audit, deduplicate, check, fix, and track usage of your Claude Code skills. 9 slash commands, zero dependencies
  <sub>★ 119 · Shell · MIT · npx · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add khendzel/skills-janitor`</sub>
- **[cup](https://github.com/krodak/clickup-cli)** — ClickUp CLI for AI agents with task management, sprints, and time tracking
  <sub>★ 118 · TypeScript · MIT · npm · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @krodak/clickup-cli`</sub>
- **[great_cto](https://github.com/avelikiy/great_cto)** — Full SDLC pipeline plugin with 7 agents (tech-lead, senior-dev, qa-engineer, security-officer, devops, l3-support, project-auditor), 12-angle code review, 10 project archetypes, 13 compliance frameworks (SOC2/HIPAA/PCI-DSS/GDPR/ISO 27001), two-gate approval flow. Opus 4.7 advisor escalation, file-based, MIT
  <sub>★ 94 · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx great-cto init`</sub>
- **[whatsapp-claude-plugin](https://github.com/Rich627/whatsapp-claude-plugin)** — WhatsApp channel plugin for Claude Code -- connects as a linked device via Baileys v7 with bidirectional messaging, full media support, voice transcription, permission relay, and access control
  <sub>★ 93 · TypeScript · Apache-2.0 · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Rich627/whatsapp-claude-plugin.git`</sub>
- **[cortex](https://github.com/cdeust/Cortex)** — Persistent memory for Claude Code — neuroscience-backed retrieval with thermodynamic decay, backed by 41 published papers. PostgreSQL + pgvector + sentence-transformers. 6 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, SessionEnd, Notification, SubagentStart), hierarchical recall, causal chains, knowledge graph navigation. Install and forget
  <sub>★ 72 · Python · MIT · source · pushed 2026-09-19 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/cdeust/Cortex.git`</sub>
- **[dna-claude-analysis](https://github.com/shmlkv/dna-claude-analysis)** — Personal genome analysis toolkit that analyzes raw DNA data across 17 categories and generates a terminal-style HTML dashboard
  <sub>★ 57 · Python · MIT · source · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shmlkv/dna-claude-analysis.git`</sub>
- **[AgentLint](https://github.com/0xmariowu/AgentLint)** — Lint your repo for AI agent compatibility. 33 evidence-backed checks across 5 dimensions. Claude Code plugin
  <sub>★ 56 · Shell · MIT · npm · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentlint-ai # CLI only — no Claude plugin yet`</sub>
- **[harness-evolver](https://github.com/raphaelchristi/harness-evolver)** — LangSmith-native autonomous agent optimization. Multi-agent proposers evolve prompts, routing, tools, and architecture in isolated git worktrees. Install: npx harness-evolver@latest
  <sub>★ 52 · Python · MIT · npx · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx harness-evolver@latest`</sub>
- **[immich-photo-manager](https://github.com/drolosoft/immich-photo-manager)** — Turn your self-hosted Immich photo library into a conversation — natural language search, geographic album curation, duplicate detection via perceptual hashing, library health audits, and interactive HTML galleries. 22 MCP tools, 11 skills, 5 slash commands
  <sub>★ 50 · Python · MIT · uv · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx immich-photo-manager --help`</sub>
- **[VibeGuard](https://github.com/majiayu000/vibeguard)** — Stop AI from hallucinating code. 88 rules + 13 hooks + 14 agents for real-time interception and static scanning across 5 languages
  <sub>★ 41 · Rust · MIT · clone · pushed 2026-09-19 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/majiayu000/vibeguard.git`</sub>
- **[claude-recap](https://github.com/hatawong/claude-recap)** — Per-topic session memory using Shell hooks — archives each conversation topic as a separate Markdown summary. Two hooks, bash + Node.js, 100% local
  <sub>★ 39 · JavaScript · MIT · clone · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hatawong/claude-recap.git`</sub>
- **[ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill)** — Expert ESP32 embedded systems plugin — chip selection across 9 variants, GPIO validation with anti-bricking safety, Arduino/ESP-IDF code gen, LVGL v8–v9.5 refs, 60+ Waveshare board pinouts. Install: claude /install-plugin https://github.com/ezrover/ESP32-AI-Agent-Skill
  <sub>★ 37 · Python · MIT · clone · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ezrover/ESP32-AI-Agent-Skill.git`</sub>
- **[claude-cost-optimizer](https://github.com/Sagargupta16/claude-cost-optimizer)** — Installable cost-mode skill (30-60% cost savings, up to 70% in strict mode) + 10 guides, 10 templates, budget hooks. Install: npx skills add Sagargupta16/claude-cost-optimizer
  <sub>★ 36 · TypeScript · MIT · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Sagargupta16/claude-cost-optimizer`</sub>
- **[lightcms](https://github.com/jonradoff/lightcms)** — AI-native CMS with 41 MCP tools for managing websites through natural language — pages, templates, assets, themes, collections, redirects, and more with full content versioning
  <sub>★ 31 · Go · MIT · source · pushed 2026-07-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/jonradoff/lightcms.git`</sub>
- **[weft](https://github.com/dioptx/weft)** — Deterministic workflow tracking with event-sourced state — templates with skill chains, bounded loops, and per-step tool guards. Hooks block out-of-order tool calls; state survives compaction via an append-only event log. Stdlib-only Python core, 191 tests, MIT. Install: /plugin marketplace add dioptx/weft
  <sub>★ 25 · Python · MIT · clone · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dioptx/weft.git`</sub>
- **[logic-lens](https://github.com/hyhmrright/logic-lens)** — Logic-first code review plugin for Claude Code — detects behavioral bugs via semi-formal execution tracing. Finds logic errors linters and type checkers miss. Structured findings: Premises → Trace → Divergence → Remedy with L1–L6 risk codes. Six skills: logic-review, logic-explain, logic-diff, logic-locate, logic-health, logic-fix-all
  <sub>★ 23 · Python · MIT · clone · pushed 2026-08-29 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/hyhmrright/logic-lens.git`</sub>
- **[claudebase](https://github.com/rohithzr/claudebase)** — Back up, restore, and sync your Claude Code config (settings, skills, agents, hooks, rules, memory, MCP) to a private GitHub repo. Named profiles, secret scanning, multi-machine conflict detection, automatic backups. 158 tests
  <sub>★ 22 · Shell · MIT · clone · pushed 2026-04-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/rohithzr/claudebase.git`</sub>
- **[claude-code-hooks](https://github.com/yurukusa/claude-code-hooks)** — 15 production-tested hooks from 160+ hours of autonomous operation. Destructive command blocker, branch guard, syntax check, context monitor, permission auto-approver. Bash, zero deps
  <sub>★ 19 · Shell · MIT · npx · pushed 2026-08-29 · WSL2 · macOS? · Linux</sub>
  <sub>`npx github:yurukusa/cc-safe-setup # Install 8 essential hooks in 10 seconds`</sub>
- **[knowledge-graph](https://github.com/hilyfux/knowledge-graph)** — Built on Anthropic internal engineering practices and Karpathy's AutoResearch methodology. A zero-dependency, git-native memory layer for Claude Code that persists learned context across sessions. Pure bash, ~3ms/event, privacy-first
  <sub>★ 19 · Shell · MIT · clone · pushed 2026-06-12 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/hilyfux/knowledge-graph.git`</sub>
- **[jarvis](https://github.com/Ramsbaby/jarvis)** — Turns an idle Claude Max subscription into a 24/7 AI ops system — Discord bot, 76 scheduled tasks, 12 AI teams, local LanceDB RAG, 98% context compression via Nexus CIG, and 4-layer self-healing infrastructure. Uses claude -p headless mode at $0 extra cost
  <sub>★ 18 · Shell · MIT · clone · pushed 2026-09-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/Ramsbaby/jarvis.git`</sub>
- **[nexus-agents](https://github.com/nexus-substrate/nexus-agents)** — Intelligent orchestration platform routing tasks to Claude, Gemini, Codex, and OpenCode via Budget→TOPSIS→LinUCB composite router. 30 MCP tools (orchestrate, consensus voting, research pipelines), 12 expert agents, 17 skills, plugin-native /agents + hooks. Install: /plugin marketplace add williamzujkowski/nexus-agents
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g nexus-agents`</sub>
- **[pulser](https://github.com/TheStack-ai/pulser)** — Diagnostic CLI for Claude Code SKILL.md files — scans 8 rules, auto-classifies, prescribes fixes with templates, --fix with rollback
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pulser-cli`</sub>
- **[oss-autopilot](https://github.com/costajohnt/oss-autopilot)** — Open source contribution manager — tracks PRs across repos, discovers issues, diagnoses CI failures, drafts maintainer responses. 7 agents, interactive commands, MCP server. Install: /plugin marketplace add costajohnt/oss-autopilot
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-09-21 · macOS</sub>
  <sub>`npm install -g @oss-autopilot/core`</sub>
- **[ejentum-mcp](https://github.com/ejentum/ejentum-mcp)** — Reasoning Harness for agentic AI: 4 MCP tools (reasoning, code, anti-deception, memory) over 679 engineered cognitive operations. Each call returns a structured scaffold the calling LLM ingests before its first token. Catches sycophancy, hallucination, and reasoning decay before they emerge. Companion skills/ directory ships SKILL.md files for autonomous routing in Claude Code. MIT, free tier 100
  <sub>★ 16 · JavaScript · MIT · npx · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y ejentum-mcp`</sub>
- **[fractal](https://github.com/rmolines/fractal-loop)** — Recursive project management for Claude Code. Decomposes goals into predicates, works the riskiest piece first, and re-evaluates as it learns
  <sub>★ 14 · Shell · MIT · script · pushed 2026-03-19 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/rmolines/fractal-loop/master/install.sh | bash`</sub>
- **[simmer](https://github.com/2389-research/simmer)** — Iterative artifact refinement using judge subagents that score against user-defined criteria across multiple rounds
  <sub>★ 14 · MIT · source · pushed 2026-07-06</sub>
  <sub>`git clone https://github.com/2389-research/simmer.git`</sub>
- **[axme-code](https://github.com/AxmeAI/axme-code)** — Persistent project memory across sessions, architectural decisions with enforce levels, and pre-execution safety hooks that block dangerous commands at the harness level (not via prompts). Local-only storage, multi-repo workspace support, automatic knowledge extraction via background auditor. 100% on ToolEmu safety, 89% on LongMemEval at ~10x fewer tokens than competitors
  <sub>★ 14 · TypeScript · MIT · psh · pushed 2026-08-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/AxmeAI/axme-code/main/install.ps1 | iex`</sub>
- **[OraClaw](https://github.com/Whatsonyourmind/oraclaw)** — Decision intelligence MCP server — 12 tools with 19 ML algorithms (multi-armed bandits, constraint solvers, forecasters, risk models, Q-learning, A*, simulated annealing). Sub-25ms responses, deterministic, 945 tests. npx @oraclaw/mcp-server
  <sub>★ 13 · TypeScript · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Whatsonyourmind/oraclaw.git`</sub>
- **[preflight](https://github.com/preflight-dev/preflight)** — 24-tool MCP server that catches vague prompts before they cost 2-3x in wrong→fix cycles. 12-category scorecards, correction pattern learning, cross-service contract awareness, session history search with LanceDB vectors, and cost estimation. npx preflight-dev
  <sub>★ 12 · TypeScript · MIT · npm · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g preflight-dev`</sub>
- **[review-squad](https://github.com/2389-research/review-squad)** — Multi-perspective code review via dispatched subagent panels: experts, normie users, pedantic nitpickers, and real-user task runners
  <sub>★ 12 · MIT · source · pushed 2026-07-06</sub>
  <sub>`git clone https://github.com/2389-research/review-squad.git`</sub>
- **[tailtest](https://github.com/avansaber/tailtest)** — Automatically generates and runs tests for every file Claude Code creates or modifies. PostToolUse hook detects changes, generates scenarios, runs them, and surfaces failures. 8 languages (Python, TypeScript, JavaScript, Go, Ruby, PHP, Java, Rust). Zero config, zero commands
  <sub>★ 11 · Python · MIT · source · pushed 2026-06-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/avansaber/tailtest.git`</sub>
- **[gate4agent](https://github.com/ZENG3LD/gate4agent)** — Universal Rust transport for CLI AI agents (Claude Code, Codex, Gemini, OpenCode). Pipe/NDJSON, PTY, and ACP modes. Published on crates.io
  <sub>★ 9 · Rust · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ZENG3LD/gate4agent.git`</sub>
- **[sitemd](https://github.com/sitemd-cc/sitemd)** — Build websites from Markdown via MCP. 22 tools for creating pages, generating content, configuring settings, running SEO audits, and deploying static sites to Cloudflare Pages
  <sub>★ 9 · HTML · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/sitemd-cc/sitemd.git`</sub>
- **[discoclaw](https://github.com/DiscoClaw/discoclaw)** — Personal AI orchestrator that bridges Discord to Claude Code with durable memory, task tracking, and cron-based automation
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-04-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g discoclaw`</sub>
- **[the-pragmatic-pm](https://github.com/marfoerst/the-pragmatic-pm)** — PM leadership toolkit with 43 skills, 5 agents, 4 workflows. Covers PRD generation, OKR lifecycle, pricing, AI pricing, positioning, sales enablement, and quarterly planning
  <sub>★ 8 · Shell · MIT · source · pushed 2026-07-09</sub>
  <sub>`git clone https://github.com/marfoerst/the-pragmatic-pm.git`</sub>
- **[dig2crawl](https://github.com/ZENG3LD/dig2crawl)** — Universal web crawler with Claude-powered CSS selector discovery. 4-level AI extraction escalation (CSS, browser actions, Claude Vision, captcha). Rust
  <sub>★ 7 · Rust · MIT · source · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ZENG3LD/dig2crawl.git`</sub>
- **[jarvis-company-board](https://github.com/Ramsbaby/jarvis-board)** — Real-time AI agent collaboration board built on Next.js 15 and SQLite WAL — 8 named AI board members debate decisions via SSE push, with a DEV task approval workflow and Railway deploy support
  <sub>★ 7 · TypeScript · clone · pushed 2026-07-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Ramsbaby/jarvis-board.git`</sub>
- **[notch-so-good](https://github.com/deepshal99/notch-so-good)** — Pixel-art crab (Chawd) lives in your Mac's notch and watches Claude Code for you. Live session timers, color-coded notifications, 13 idle animations, mouse-reactive eyes, drowsiness system. Universal binary, one-line install: npx notch-so-good. MIT, 130+ users
  <sub>★ 7 · Swift · MIT · npx · pushed 2026-08-13 · WSL2 · macOS? · Linux</sub>
  <sub>`npx notch-so-good`</sub>
- **[codebase-graph](https://github.com/Phoenixrr2113/codebase-graph)** — Code intelligence MCP server — 42-language tree-sitter AST parsing, FalkorDB knowledge graphs, 0.944 MRR search quality. npm: @anthropic/codegraph
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y -p @agntk/codegraph-mcp codegraph-dashboard`</sub>
- **[ui-ux-suite](https://github.com/Aboudjem/ui-ux-suite)** — Design audit across 12 dimensions — color contrast, typography, layout, accessibility. Scans CSS, JSX, Tailwind configs. Quantified scores (1-10) with before/after fix code. WCAG 2.1, APCA, OKLCH. Zero deps
  <sub>★ 7 · JavaScript · MIT · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Aboudjem/ui-ux-suite`</sub>
- **[clirank-mcp-server](https://github.com/alexanderclapp/clirank-mcp-server)** — API discovery for agents -- scores 210+ APIs on CLI-friendliness across 11 signals. Find the right API for any task via MCP tools or REST (curl "https://clirank.dev/api/discover?q=send+emails"). No auth required
  <sub>★ 6 · JavaScript · MIT · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y clirank-mcp-server@latest`</sub>
- **[cc-safe-setup](https://github.com/yurukusa/cc-safe-setup)** — One command (npx cc-safe-setup) to install 6 essential safety hooks in 10 seconds. Zero dependencies
  <sub>★ 6 · Shell · MIT · npx · pushed 2026-09-19 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx github:yurukusa/cc-safe-setup`</sub>
- **[claw-army/claude-node](https://github.com/claw-army/claude-node)** — Python subprocess bridge for Claude Code CLI, giving Python code direct access to Claude Code native capabilities via stream-json
  <sub>★ 6 · Python · pip · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install claude-node`</sub>
- **[dodo-agent-plugin](https://github.com/dodopayments/dodo-agent-plugin)** — Official Dodo Payments plugin: 8 integration skills (checkout, subscriptions, webhooks, usage-based billing, credits, license keys, BillingSDK, best practices) and 2 MCP servers (live API via browser OAuth + docs search, no auth). Multi-agent: Claude Code, Codex, Cursor, OpenCode
  <sub>★ 6 · JavaScript · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dodopayments/dodo-agent-plugin.git`</sub>
- **[Bouncer](https://github.com/buildingopen/bouncer)** — Independent quality gate that uses Gemini to audit Claude Code's output. Includes Stop hook (automatic), quick audit skill, and deep audit with full tool access. One-liner install
  <sub>★ 5 · Python · MIT · script · pushed 2026-04-09 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/buildingopen/bouncer/master/install.sh | bash`</sub>
- **[getburnd](https://github.com/garvitsurana271/burnd)** — Local-first cost-control CLI for Claude Code. Reads ~/.claude/projects/*.jsonl, identifies 8 leak patterns (verbose context, tool loops, large file re-reads), prints savings estimates, generates a shareable report URL. MIT, zero telemetry
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx getburnd`</sub>
- **[building-multiagent-systems](https://github.com/2389-research/building-multiagent-systems)** — Architecture patterns for multi-agent systems: orchestrator-worker, pipeline, debate, and MapReduce topologies
  <sub>★ 5 · MIT · source · pushed 2026-07-06</sub>
  <sub>`git clone https://github.com/2389-research/building-multiagent-systems.git`</sub>
- **[claude-code-sessions](https://github.com/apappascs/claude-code-sessions)** — Session intelligence plugin. 11 skills for full-text search, token analytics, task management, session comparison, timeline views, and context recovery across all sessions. Includes a web dashboard. Zero runtime dependencies, read-only
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/apappascs/claude-code-sessions.git`</sub>
- **[idle-timing](https://github.com/clankercode/claude-inject-idle-time)** — Injects hidden timing context (local time with UTC offset, idle seconds since last reply, previous-turn duration) into every user prompt so the model knows how long the conversation has been paused. Ships a statusline fragment for a live elapsed-time readout and a visible [after Xm Ys] note when you return from >10s idle. 57 tests, dual Unlicense/CC0
  <sub>★ 5 · JavaScript · source · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/clankercode/claude-inject-idle-time.git`</sub>
- **[leapfrog-mcp](https://github.com/anthonybono21-cloud/leapfrog)** — Multi-session browser MCP server -- 15 parallel isolated Chromium sessions so multiple Claude Code terminals can browse simultaneously. 37 tools for navigation, extraction, interaction, network interception, and session profiles. 797 tests. Install: npx -y leapfrog-mcp
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx leapfrog-mcp --doctor # verify everything works`</sub>
- **[claude-agentic-coding-playbook](https://github.com/john-wilmes/claude-agentic-coding-playbook)** — Evidence-based practices for LLM-assisted development -- hooks, skills, scripts, and a best-practices guide with 58 citations. Includes 19+ guard/lifecycle hooks, investigation workflow, fleet indexing, and claude-loop for autonomous task queues
  <sub>★ 4 · JavaScript · MIT · clone · pushed 2026-04-06 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/john-wilmes/claude-agentic-coding-playbook.git`</sub>
- **[claude-scaffold](https://github.com/pyramidheadshark/claude-scaffold)** — npx CLI that deploys CLAUDE.md, hooks, and 18 domain skills to any repository in one command. Skills auto-activate via hooks based on project context. Cross-repo sync via update --all. Install: npx claude-scaffold init
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-05-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx claude-scaffold update --all # sync all registered projects`</sub>
- **[faf-skills](https://github.com/Wolfe-Jam/faf-skills)** — 31 Claude Code skills for persistent project context (.faf, application/vnd.faf+yaml). Scoring, sync, testing, publishing, MCP server creation, architecture docs. Anthropic MCP #2759
  <sub>★ 4 · Shell · MIT · clone · pushed 2026-08-18</sub>
  <sub>`git clone https://github.com/Wolfe-Jam/faf-skills.git`</sub>
- **[paco-framework](https://github.com/PenguinAlleyApps/paco-framework)** — Markdown-first multi-agent OS for Claude Code. Coordinates 3-16 specialized AI agents (Engineering, QA, Growth, Finance) with file-based dispatch, institutional memory, CEO Gate approval, and 24/7 scheduling. No Python required. MIT
  <sub>★ 4 · Python · AGPL-3.0 · source · pushed 2026-04-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PenguinAlleyApps/paco-framework.git`</sub>
- **[test-kitchen](https://github.com/2389-research/test-kitchen)** — Parallel implementation exploration using competing subagents, with structured comparison and winner selection
  <sub>★ 4 · MIT · source · pushed 2026-07-06</sub>
  <sub>`git clone https://github.com/2389-research/test-kitchen.git`</sub>
- **[sniff-qa](https://github.com/Aboudjem/sniff)** — AI-powered QA tool — 8 checks in one command. Source scanning (dead links, API endpoints, debug statements, broken imports), accessibility (axe-core), visual regression (pixelmatch), performance (Lighthouse), AI exploration, source/browser cross-referencing. MCP server included. 213 tests, Apache 2.0
  <sub>★ 4 · TypeScript · Apache-2.0 · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Aboudjem/sniff`</sub>
- **[debian-packaging-agent-skill](https://github.com/cosgroveb/debian-packaging-agent-skill)** — Debian packaging skill covering debhelper, debian/rules, package metadata, lintian, and multi-binary packages for Ruby (gem2deb), Python (pybuild), Rust (debcargo), and Go (dh-golang). Loads language-specific reference docs on demand. Apache 2.0
  <sub>★ 4 · Shell · Apache-2.0 · source · pushed 2026-07-25 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/cosgroveb/debian-packaging-agent-skill.git`</sub>
- **[ashlr-plugin](https://github.com/ashlrai/ashlr-plugin)** — Open-source Claude Code plugin replacing the built-in Read/Grep/Edit/Bash tools with token-efficient versions backed by @ashlr/core-efficiency. Independently benchmarked at 57% token reduction on real codebases. 70+ tools across glob, grep, structural diff/edit, and an opt-in genome (LSP-style codebase index). Install: curl -fsSL plugin.ashlr.ai/install.sh | bash
  <sub>★ 3 · TypeScript · MIT · psh · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/ashlrai/ashlr-plugin/main/docs/install.ps1 | iex`</sub>
- **[nirecom/agents](https://github.com/nirecom/agents)** — Self-driving Claude Code + GitHub Copilot framework with hook-enforced workflow state machine (research → plan → tests → code → security-review → docs), private-info scanning (AWS/Anthropic keys, PEM certs, RFC 1918 IPs), three-stage planning with adversarial Codex review, OWASP-backed test categories, and cross-machine session sync. Windows-native (PowerShell-first) with Linux/macOS support
  <sub>★ 3 · Shell · MIT · clone · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/nirecom/agents`</sub>
- **[claude-sounds](https://github.com/culminationAI/claude-sounds)** — Audio feedback for Claude Code hooks — 10 events, 21 sounds, random rotation. macOS (afplay)
  <sub>★ 2 · Shell · MIT · source · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/culminationAI/claude-sounds.git`</sub>
- **[eliniscan](https://github.com/AlpYenigun/eliniscan)** — AI full codebase scanner. Opens a separate Claude session for every file — reads every line, misses nothing. Finds bugs, security, performance issues and auto-fixes
  <sub>★ 2 · JavaScript · MIT · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g eliniscan`</sub>
- **[pulse](https://github.com/chsm04/pulse)** — Local Channel plugin — push notifications into Claude Code sessions via HTTP POST. No Discord/Slack needed, just curl. Three levels (info/warn/error), source tracking, dedup
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-03-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/chsm04/pulse.git`</sub>
- **[PUIUX Pilot](https://github.com/PUIUX-Cloud/puiux-pilot)** — Auto-configures Claude Code hooks, MCPs, and skills for any project. Scans 95+ project types, selects from 28+ hooks, scores quality (0-100), translates configs across AI tools. Safe: dry-run, atomic writes, backup + rollback
  <sub>★ 2 · TypeScript · Apache-2.0 · npm · pushed 2026-04-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g puiux-pilot`</sub>
- **[craft-statusline](https://github.com/derjochenmeyer/claude-code-craft-statusline)** — Bash statusline plugin for Claude Code with state-aware git branch (ahead / behind / stashed / conflict / combined signals), context window with absolute-token traffic light (yellow at 400k tokens, red at 85%), 5h/7d rate limits, and optional cost. Bash 3.2 compatible, jq is the only dependency. Install: /plugin marketplace add derjochenmeyer/claude-code-craft-statusline
  <sub>★ 2 · Shell · MIT · source · pushed 2026-04-26 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/derjochenmeyer/claude-code-craft-statusline.git`</sub>
- **[magic-cc-codex-worker](https://github.com/wenqingyu/magic-cc-codex-worker)** — Turns OpenAI Codex into a pool of parallel agent workers for Claude Code. Each worker runs in its own git worktree to isolate concurrent edits. Resumable sessions, dual-model PR review (PR materialized in a detached worktree for the reviewer), role-based specialization (implementer/reviewer/planner), delegation-level knob (minimal/balance/max), bundled single-file MCP server. 9 slash commands, 3 s
  <sub>★ 2 · TypeScript · source · pushed 2026-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wenqingyu/magic-cc-codex-worker.git`</sub>
- **[claude-snapshot](https://github.com/adhenawer/claude-snapshot)** — Portable Claude Code setup snapshots — export your settings, plugins, hooks, CLAUDE.md, and MCP configs as a .tar.gz, diff before applying, and restore on another machine in under 2 minutes. No network, no daemon, .bak safety on every apply. Node.js 18+, cross-platform (macOS + Linux). Install: /plugin marketplace add adhenawer/claude-snapshot
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-04-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx -y claude-snapshot export`</sub>
- **[claude-channel-whatsapp](https://github.com/riasistemas/claude-channel-whatsapp)** — Official WhatsApp Business Cloud API bridge for Claude Code -- webhooks, OGG Opus audio, allowlist + permission relay scrubbing secrets. NOT Baileys/scraping -- uses Meta's official API with WABA tokens. Apache-2.0, by RIA Systems (verified Meta Tech Provider). Landing: claude-plugins.riasistemas.com.br/whatsapp. Install: /plugin marketplace add riasistemas/claude-plugins then /plugin install what
  <sub>★ 2 · TypeScript · Apache-2.0 · source · pushed 2026-04-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/riasistemas/claude-channel-whatsapp.git`</sub>
- **[cc-cost](https://github.com/lob-labs/cc-cost)** — Single-file Python CLI that parses Claude Code transcript JSONL and reports cost, prompt-cache hit rate, tool-call distribution, top expensive turns, and actionable optimization recommendations (--diagnose, --md, --top N). MIT, no third-party deps
  <sub>★ 1 · Python · pip · pushed 2026-04-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install cc-cost`</sub>
- **[/cht](https://github.com/kosoukhov/cht-cli)** — Chat persistence for Claude Code — 13 slash commands + hooks for saving conversations as local markdown files. Crash-proof auto-save via hooks, project-based organization, search, and management. npm: @kosoukhov/cht-cli
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @kosoukhov/cht-cli`</sub>
- **[cc-aws-keepalive](https://github.com/GeiserX/cc-aws-keepalive)** — Keep Claude Code sessions alive through AWS credential expiry -- proactive expiration warnings, credential refresh bypass for Bedrock SSO/SAML, optional statusline countdown timer. 4 hook scripts, zero dependencies
  <sub>★ 1 · JavaScript · GPL-3.0 · clone · pushed 2026-08-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/GeiserX/cc-aws-keepalive.git`</sub>
- **[obey](https://github.com/Lexxes-Projects/obey)** — Rule enforcement plugin. Save rules with natural language, enforce with 17 lifecycle hooks. Three scopes (global, stack-specific, project-local), active blocking via PreToolUse, completion checklists via Stop hook, audit trail, auto-detects rule-like language. Cross-platform
  <sub>★ 1 · Shell · MIT · source · pushed 2026-03-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Lexxes-Projects/obey.git`</sub>
- **[mobile-spine](https://github.com/bentleypark/claude-code-mobile-spine)** — Scaffold for mobile teams whose Android, iOS, and Backend live in separate repos. Coordinates 4 specialized subagents (api / pm / android / ios) with hard repo boundaries via settings.json deny rules. /mobile-spine:init runs a 6-question interview and writes the full workspace; /feat drives a 4-question interview → 4-case classification (existing endpoint / new endpoint / new domain / backend not
  <sub>★ 1 · Python · MIT · source · pushed 2026-07-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/bentleypark/claude-code-mobile-spine.git`</sub>
- **[agento-patronum](https://github.com/emaarco/agento-patronum)** — Protects sensitive files, credentials, and shell commands from unintended AI access via Claude Code hooks. Unlike settings.json deny rules, hooks are an enforcement layer you own and can verify. Ships with defaults for .env files, SSH keys, AWS credentials, and kubeconfig
  <sub>unavailable</sub>
- **[aws-cost-saver](https://github.com/prajapatimehul/aws-cost-saver)** — AWS cost optimization scanner with 173 automated checks, ML-powered rightsizing, and Zero Hallucination Pricing - Real result: 60% cost reduction
  <sub>unavailable</sub>
- **[a11y-audit](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/a11y-audit)** — Full accessibility audit with WCAG compliance checking
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/a11y-audit`</sub>
- **[accessibility-checker](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/accessibility-checker)** — Scan for accessibility issues and fix ARIA attributes in web applications
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/accessibility-checker`</sub>
- **[adr-writer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/adr-writer)** — Architecture Decision Records authoring and management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/adr-writer`</sub>
- **[ai-prompt-lab](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/ai-prompt-lab)** — Improve and test AI prompts for better Claude Code interactions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/ai-prompt-lab`</sub>
- **[analytics-reporter](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/analytics-reporter)** — Generate analytics reports and dashboard configurations from project data
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/analytics-reporter`</sub>
- **[android-developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/android-developer)** — Android and Kotlin development with Jetpack Compose
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/android-developer`</sub>
- **[api-architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/api-architect)** — API design, documentation, and testing with OpenAPI spec generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/api-architect`</sub>
- **[api-benchmarker](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/api-benchmarker)** — API endpoint benchmarking and performance reporting
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/api-benchmarker`</sub>
- **[api-reference](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/api-reference)** — API reference documentation generation from source code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/api-reference`</sub>
- **[api-tester](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/api-tester)** — Test API endpoints and run load tests against services
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/api-tester`</sub>
- **[aws-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/aws-helper)** — AWS service configuration and deployment automation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/aws-helper`</sub>
- **[azure-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/azure-helper)** — Azure service configuration and deployment automation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/azure-helper`</sub>
- **[backend-architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/backend-architect)** — Backend service architecture design with endpoint scaffolding
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/backend-architect`</sub>
- **[bug-detective](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/bug-detective)** — Debug issues systematically with root cause analysis and execution tracing
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/bug-detective`</sub>
- **[bundle-analyzer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/bundle-analyzer)** — Frontend bundle size analysis and tree-shaking optimization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/bundle-analyzer`</sub>
- **[changelog-gen](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/changelog-gen)** — Generate changelogs from git history with conventional commit parsing
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/changelog-gen`</sub>
- **[changelog-writer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/changelog-writer)** — Detailed changelog authoring from git history and PRs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/changelog-writer`</sub>
- **[ci-debugger](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/ci-debugger)** — Debug CI/CD pipeline failures and fix configurations
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/ci-debugger`</sub>
- **[code-architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/code-architect)** — Generate architecture diagrams and technical design documents
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/code-architect`</sub>
- **[code-explainer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/code-explainer)** — Explain complex code and annotate files with inline documentation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/code-explainer`</sub>
- **[code-guardian](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/code-guardian)** — Automated code review, security scanning, and quality enforcement
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/code-guardian`</sub>
- **[code-review-assistant](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/code-review-assistant)** — Automated code review with severity levels and actionable feedback
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/code-review-assistant`</sub>
- **[codebase-documenter](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/codebase-documenter)** — Auto-document entire codebase with inline comments and API docs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/codebase-documenter`</sub>
- **[color-contrast](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/color-contrast)** — Color contrast checking and accessible color suggestions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/color-contrast`</sub>
- **[commit-commands](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/commit-commands)** — Advanced commit workflows with smart staging and push automation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/commit-commands`</sub>
- **[complexity-reducer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/complexity-reducer)** — Reduce cyclomatic complexity and simplify functions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/complexity-reducer`</sub>
- **[compliance-checker](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/compliance-checker)** — Regulatory compliance verification for GDPR, SOC2, and HIPAA
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/compliance-checker`</sub>
- **[content-creator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/content-creator)** — Technical content generation for blog posts and social media
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/content-creator`</sub>
- **[context7-docs](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/context7-docs)** — Fetch up-to-date library documentation via Context7 for accurate coding
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/context7-docs`</sub>
- **[contract-tester](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/contract-tester)** — API contract testing with Pact for microservice compatibility
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/contract-tester`</sub>
- **[create-worktrees](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/create-worktrees)** — Git worktree management for parallel development workflows
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/create-worktrees`</sub>
- **[cron-scheduler](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/cron-scheduler)** — Cron job configuration and schedule validation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/cron-scheduler`</sub>
- **[css-cleaner](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/css-cleaner)** — Find unused CSS and consolidate stylesheets
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/css-cleaner`</sub>
- **[data-privacy](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/data-privacy)** — Data privacy implementation with PII detection and anonymization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/data-privacy`</sub>
- **[database-optimizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/database-optimizer)** — Database query optimization with index recommendations and EXPLAIN analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/database-optimizer`</sub>
- **[dead-code-finder](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/dead-code-finder)** — Find and remove dead code across the codebase
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/dead-code-finder`</sub>
- **[debug-session](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/debug-session)** — Interactive debugging workflow with git bisect integration
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/debug-session`</sub>
- **[dependency-manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/dependency-manager)** — Audit, update, and manage project dependencies with safety checks
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/dependency-manager`</sub>
- **[deploy-pilot](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/deploy-pilot)** — Deployment automation with Dockerfile generation, CI/CD pipelines, and infrastructure as code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/deploy-pilot`</sub>
- **[desktop-app](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/desktop-app)** — Desktop application scaffolding with Electron or Tauri
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/desktop-app`</sub>
- **[devops-automator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/devops-automator)** — DevOps automation scripts for CI/CD, health checks, and deployments
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/devops-automator`</sub>
- **[discuss](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/discuss)** — Debate implementation approaches with structured pros and cons analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/discuss`</sub>
- **[codetape](https://github.com/888wing/codetape)** — The flight recorder for AI coding — auto-records semantic traces and syncs README, CHANGELOG, CLAUDE.md. Zero deps. npx codetape init
  <sub>HTML · MIT · npx · pushed 2026-03-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx codetape init # Set up tracking in your project`</sub>
- **[doc-forge](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/doc-forge)** — Documentation generation, API docs, and README maintenance
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/doc-forge`</sub>
- **[docker-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/docker-helper)** — Build optimized Docker images and improve Dockerfile best practices
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/docker-helper`</sub>
- **[double-check](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/double-check)** — Verify code correctness with systematic second-pass analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/double-check`</sub>
- **[e2e-runner](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/e2e-runner)** — End-to-end test execution and recording for web applications
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/e2e-runner`</sub>
- **[embedding-manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/embedding-manager)** — Manage vector embeddings and similarity search
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/embedding-manager`</sub>
- **[env-manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/env-manager)** — Set up and validate environment configurations across environments
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/env-manager`</sub>
- **[env-sync](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/env-sync)** — Environment variable syncing and diff across environments
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/env-sync`</sub>
- **[experiment-tracker](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/experiment-tracker)** — ML experiment tracking with metrics logging and run comparison
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/experiment-tracker`</sub>
- **[explore](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/explore)** — Smart codebase exploration with dependency mapping and structure analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/explore`</sub>
- **[feature-dev](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/feature-dev)** — Full feature development workflow from spec to completion
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/feature-dev`</sub>
- **[finance-tracker](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/finance-tracker)** — Development cost tracking with time estimates and budget reporting
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/finance-tracker`</sub>
- **[fix-github-issue](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/fix-github-issue)** — Auto-fix GitHub issues by analyzing issue details and implementing solutions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/fix-github-issue`</sub>
- **[fix-pr](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/fix-pr)** — Fix PR review comments automatically with context-aware patches
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/fix-pr`</sub>
- **[flutter-mobile](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/flutter-mobile)** — Flutter app development with widget creation and platform channels
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/flutter-mobile`</sub>
- **[frontend-developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/frontend-developer)** — Frontend component development with accessibility and responsive design
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/frontend-developer`</sub>
- **[gcp-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/gcp-helper)** — Google Cloud Platform service configuration and deployment
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/gcp-helper`</sub>
- **[git-flow](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/git-flow)** — Git workflow management with feature branches, releases, and hotfix flows
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/git-flow`</sub>
- **[github-issue-manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/github-issue-manager)** — GitHub issue triage, creation, and management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/github-issue-manager`</sub>
- **[helm-charts](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/helm-charts)** — Helm chart generation and upgrade management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/helm-charts`</sub>
- **[import-organizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/import-organizer)** — Organize, sort, and clean import statements
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/import-organizer`</sub>
- **[infrastructure-maintainer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/infrastructure-maintainer)** — Infrastructure maintenance with security audits and update management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/infrastructure-maintainer`</sub>
- **[ios-developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/ios-developer)** — iOS and Swift development with SwiftUI views and models
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/ios-developer`</sub>
- **[k8s-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/k8s-helper)** — Generate Kubernetes manifests and debug pod issues with kubectl
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/k8s-helper`</sub>
- **[license-checker](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/license-checker)** — License compliance checking and NOTICE file generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/license-checker`</sub>
- **[lighthouse-runner](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/lighthouse-runner)** — Run Lighthouse audits and fix performance issues
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/lighthouse-runner`</sub>
- **[linear-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/linear-helper)** — Linear issue tracking integration and workflow management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/linear-helper`</sub>
- **[load-tester](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/load-tester)** — Load and stress testing for APIs and web services
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/load-tester`</sub>
- **[memory-profiler](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/memory-profiler)** — Memory leak detection and heap analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/memory-profiler`</sub>
- **[migrate-tool](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/migrate-tool)** — Generate database migrations and code migration scripts for framework upgrades
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/migrate-tool`</sub>
- **[migration-generator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/migration-generator)** — Database migration generation and rollback management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/migration-generator`</sub>
- **[model-context-protocol](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/model-context-protocol)** — MCP server development helper with tool and resource scaffolding
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/model-context-protocol`</sub>
- **[model-evaluator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/model-evaluator)** — Evaluate and compare ML model performance metrics
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/model-evaluator`</sub>
- **[monitoring-setup](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/monitoring-setup)** — Monitoring and alerting configuration with dashboard generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/monitoring-setup`</sub>
- **[monorepo-manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/monorepo-manager)** — Manage monorepo packages with affected detection and version synchronization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/monorepo-manager`</sub>
- **[mutation-tester](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/mutation-tester)** — Mutation testing to measure test suite quality
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/mutation-tester`</sub>
- **[nimbalyst](https://nimbalyst.com)** — Visual workspace for building with Codex and Claude Code. Session and task manager. Visual editing
  <sub>website</sub>
  <sub>`https://nimbalyst.com`</sub>
- **[n8n-workflow](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/n8n-workflow)** — Generate n8n automation workflows from natural language descriptions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/n8n-workflow`</sub>
- **[onboarding-guide](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/onboarding-guide)** — New developer onboarding documentation generator
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/onboarding-guide`</sub>
- **[openapi-expert](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/openapi-expert)** — OpenAPI spec generation, validation, and client code scaffolding
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/openapi-expert`</sub>
- **[optimize](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/optimize)** — Code optimization for performance and bundle size reduction
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/optimize`</sub>
- **[perf-profiler](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/perf-profiler)** — Performance analysis, profiling, and optimization recommendations
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/perf-profiler`</sub>
- **[performance-monitor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/performance-monitor)** — Profile API endpoints and run benchmarks to identify performance bottlenecks
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/performance-monitor`</sub>
- **[plan](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/plan)** — Structured planning with risk assessment and time estimation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/plan`</sub>
- **[pr-reviewer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/pr-reviewer)** — Review pull requests with structured analysis and approve with confidence
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/pr-reviewer`</sub>
- **[product-shipper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/product-shipper)** — Ship features end-to-end with launch checklists and rollout plans
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/product-shipper`</sub>
- **[product-org-os](https://github.com/yohayetsion/product-org-os)** — 150+ skills and 12 role-based agents (CPO, VP Product, PM, PMM, BizOps, CI, and more) modeling a full product org. Two gateways: /product auto-routes to the right agent, /plt runs a multi-stakeholder leadership meeting. MIT. claude plugins install github:yohayetsion/product-org-os
  <sub>Python · MIT · clone · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yohayetsion/product-org-os.git`</sub>
- **[project-scaffold](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/project-scaffold)** — Scaffold new projects and add features with best-practice templates
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/project-scaffold`</sub>
- **[prompt-optimizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/prompt-optimizer)** — Analyze and optimize AI prompts for better results
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/prompt-optimizer`</sub>
- **[python-expert](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/python-expert)** — Python-specific development with type hints and idiomatic refactoring
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/python-expert`</sub>
- **[query-optimizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/query-optimizer)** — SQL query optimization and execution plan analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/query-optimizer`</sub>
- **[rag-builder](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/rag-builder)** — Build Retrieval-Augmented Generation pipelines
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/rag-builder`</sub>
- **[rapid-prototyper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/rapid-prototyper)** — Quick prototype scaffolding with minimal viable structure
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/rapid-prototyper`</sub>
- **[reporecall](https://github.com/proofofwork-agency/reporecall)** — Local codebase memory for Claude Code. Tree-sitter AST indexing (22 languages), hybrid keyword + vector search, call-graph traversal, hooks + MCP. Injects relevant context in ~5ms before Claude starts thinking. npm: @proofofwork-agency/reporecall
  <sub>unavailable</sub>
- **[react-native-dev](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/react-native-dev)** — React Native mobile development with platform-specific optimizations
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/react-native-dev`</sub>
- **[readme-generator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/readme-generator)** — Smart README generation from project analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/readme-generator`</sub>
- **[refactor-engine](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/refactor-engine)** — Extract functions, simplify complex code, and reduce cognitive complexity
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/refactor-engine`</sub>
- **[regex-builder](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/regex-builder)** — Build, test, and debug regular expression patterns
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/regex-builder`</sub>
- **[release-manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/release-manager)** — Semantic versioning management and automated release workflows
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/release-manager`</sub>
- **[responsive-designer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/responsive-designer)** — Responsive design implementation and testing
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/responsive-designer`</sub>
- **[schema-designer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/schema-designer)** — Database schema design and ERD generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/schema-designer`</sub>
- **[screen-reader-tester](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/screen-reader-tester)** — Screen reader compatibility testing and ARIA fixes
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/screen-reader-tester`</sub>
- **[security-guidance](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/security-guidance)** — Security best practices advisor with vulnerability detection and fixes
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/security-guidance`</sub>
- **[seed-generator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/seed-generator)** — Database seeding script generation with realistic data
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/seed-generator`</sub>
- **[slack-notifier](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/slack-notifier)** — Slack integration for deployment and build notifications
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/slack-notifier`</sub>
- **[smart-commit](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/smart-commit)** — Intelligent git commits with conventional format, semantic analysis, and changelog generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/smart-commit`</sub>
- **[sprint-prioritizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/sprint-prioritizer)** — Sprint planning with story prioritization and capacity estimation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/sprint-prioritizer`</sub>
- **[technical-sales](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/technical-sales)** — Technical demo creation and POC proposal writing
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/technical-sales`</sub>
- **[terraform-helper](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/terraform-helper)** — Terraform module creation and infrastructure planning
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/terraform-helper`</sub>
- **[test-data-generator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/test-data-generator)** — Generate realistic test data and seed databases
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/test-data-generator`</sub>
- **[test-results-analyzer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/test-results-analyzer)** — Analyze test failures, identify patterns, and suggest targeted fixes
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/test-results-analyzer`</sub>
- **[test-writer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/test-writer)** — Generate comprehensive unit and integration tests with full coverage
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/test-writer`</sub>
- **[tool-evaluator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/tool-evaluator)** — Evaluate and compare developer tools with structured scoring criteria
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/tool-evaluator`</sub>
- **[type-migrator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/type-migrator)** — Migrate JavaScript files to TypeScript with proper types
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/type-migrator`</sub>
- **[ui-designer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/ui-designer)** — Implement UI designs from specs with pixel-perfect component generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/ui-designer`</sub>
- **[ultrathink](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/ultrathink)** — Deep analysis mode with extended reasoning for complex problems
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/ultrathink`</sub>
- **[unit-test-generator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/unit-test-generator)** — Generate comprehensive unit tests for any function or module
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/unit-test-generator`</sub>
- **[update-branch](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/update-branch)** — Rebase and update feature branches with conflict resolution
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/update-branch`</sub>
- **[vision-specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/vision-specialist)** — Image and visual analysis with screenshot interpretation and text extraction
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/vision-specialist`</sub>
- **[visual-regression](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/visual-regression)** — Visual regression testing with screenshot comparison
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/visual-regression`</sub>
- **[web-dev](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/web-dev)** — Full-stack web development with app scaffolding and page generation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/web-dev`</sub>
- **[workflow-optimizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/plugins/workflow-optimizer)** — Development workflow analysis and optimization recommendations
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/plugins/workflow-optimizer`</sub>
- **[background-timer](https://github.com/culminationAI/background-timer)** — Background timer with task notifications -- set delayed checks without blocking conversation
  <sub>MIT · source · pushed 2026-03-26</sub>
  <sub>`git clone https://github.com/culminationAI/background-timer.git`</sub>
- **[Clarvia MCP](https://github.com/clarvia-project/scanner)** — MCP quality scanner — scans any MCP server, returns AEO (Agent Engine Optimization) score. Indexes 27,843+ tools for instant lookup. 24 MCP tools (search, scan, compare, leaderboard, trending). npx -y clarvia-mcp-server
  <sub>unavailable</sub>
- **[US Business Data MCP](https://github.com/avabuildsdata/mcp-us-business-data)** — MCP server for US business data — search entities across 17 state Secretary of State databases, YellowPages leads, building permits from 47 cities, 20+ federal APIs (SEC, FDA, FEMA). Built in Go, on MCP Registry
  <sub>unavailable</sub>
- **[claude-time](https://github.com/nexusbuildsai/claude-time)** — Live local time + timezone injected into every prompt via UserPromptSubmit hook. Stops Claude from saying "tonight" at 9 AM. Also stamps every response with [HH:MM AM/PM TZ] so you can see when each message landed (useful when tasks stall). Zero config, zero deps beyond jq. MIT
  <sub>MIT · source · pushed 2026-05-03 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nexusbuildsai/claude-time.git`</sub>
- **[repo-visuals](https://github.com/livlign/claude-skills/tree/main/plugins/repo-visuals)** — Designs bespoke GitHub README hero visuals — animated GIF or static PNG — through a structured discovery dialog. Retina capture via Puppeteer + ffmpeg. Heroes merged into HTMLHint, Terminal.Gui, ast-graph
  <sub>HTML · MIT · in-repo · pushed 2026-08-04</sub>
  <sub>`git clone https://github.com/livlign/claude-skills.git && cd claude-skills/plugins/repo-visuals`</sub>
- **[notify](https://github.com/ApurvBazari/claude-plugins)** — Cross-platform system notifications for Claude Code hooks — macOS (terminal-notifier) and Linux (notify-send). Duration filtering to suppress noisy short events, git context extraction (repo + branch), and contextual messages per hook type. MIT
  <sub>Shell · MIT · source · pushed 2026-09-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ApurvBazari/claude-plugins.git`</sub>
- **[temporal-core](https://github.com/Evanyuan-builder/temporal-core)** — Make Claude Code agents feel time pass — research-backed temporal awareness via 3 hooks (SessionStart + UserPromptSubmit + PreToolUse) that inject session elapsed and since last action signals into context. Bundled skill teaches pacing/deadline reasoning. Aher et al. 2026: explicit time surfacing → 6× deadline performance. Apache-2.0, zero runtime deps
  <sub>Shell · Apache-2.0 · clone · pushed 2026-05-09 · macOS?</sub>
  <sub>`git clone https://github.com/Evanyuan-builder/temporal-core`</sub>
- **[claude-channel-instagram](https://github.com/riasistemas/claude-channel-instagram)** — Instagram Graph API bridge for Claude Code -- comments, DMs, comment-to-DM bootstrap, audio transcription, pluggable extensions system. Official Meta API (no scraping). Apache-2.0, by RIA Systems (verified Meta Tech Provider). Landing: claude-plugins.riasistemas.com.br/instagram. Install: /plugin marketplace add riasistemas/claude-plugins then /plugin install instagram@riasistemas
  <sub>TypeScript · Apache-2.0 · source · pushed 2026-05-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/riasistemas/claude-channel-instagram.git`</sub>

## Research &amp; Analysis

- **[qa-orchestra](https://github.com/Anasss/qa-orchestra)** — Multi-agent QA toolkit with 10 specialized agents — orchestrator, environment-manager, functional-reviewer, test-scenario-designer, browser-validator, automation-writer, manual-validator, bug-reporter, release-analyzer, smart-test-selector. Stack-agnostic, output-chained, live validation via Chrome MCP
  <sub>★ 13 · JavaScript · MIT · clone · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Anasss/qa-orchestra.git`</sub>
- **[agntk](https://github.com/Phoenixrr2113/agntk)** — Zero-config AI agent CLI with 20+ tools, persistent memory, Ollama auto-detection, and free tier
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g agntk`</sub>
- **[Research Analyst](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/research-analyst.md)** — Technical research, evidence synthesis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/research-analyst.md`</sub>
- **[Competitive Analyst](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/competitive-analyst.md)** — Market positioning, feature comparison
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/competitive-analyst.md`</sub>
- **[Trend Analyst](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/trend-analyst.md)** — Technology trend forecasting
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/trend-analyst.md`</sub>
- **[Data Researcher](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/data-researcher.md)** — Data analysis, pattern recognition
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/data-researcher.md`</sub>
- **[Search Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/search-specialist.md)** — Information retrieval, source evaluation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/search-specialist.md`</sub>
- **[Patent Analyst](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/patent-analyst.md)** — Patent searches, prior art, IP landscape
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/patent-analyst.md`</sub>
- **[Academic Researcher](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/academic-researcher.md)** — Literature reviews, citation analysis, methodology
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/academic-researcher.md`</sub>
- **[Market Researcher](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/market-researcher.md)** — Market sizing, TAM/SAM/SOM, competitive intel
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/market-researcher.md`</sub>
- **[Security Researcher](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/security-researcher.md)** — CVE analysis, threat modeling, attack surface
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/security-researcher.md`</sub>
- **[Benchmarking Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/benchmarking-specialist.md)** — Performance benchmarks, comparative evals
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/benchmarking-specialist.md`</sub>
- **[Technology Scout](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/research-analysis/technology-scout.md)** — Emerging tech evaluation, build-vs-buy analysis
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/research-analysis/technology-scout.md`</sub>

## Core Development

- **[Fullstack Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/fullstack-engineer.md)** — End-to-end feature delivery across frontend, backend, and database
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/fullstack-engineer.md`</sub>
- **[API Designer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/api-designer.md)** — RESTful API design with OpenAPI, versioning, and pagination
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/api-designer.md`</sub>
- **[Frontend Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/frontend-architect.md)** — Component architecture, state management, performance
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/frontend-architect.md`</sub>
- **[Mobile Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/mobile-developer.md)** — Cross-platform mobile with React Native and Flutter
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/mobile-developer.md`</sub>
- **[Backend Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/backend-developer.md)** — Node.js/Express/Fastify backend services
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/backend-developer.md`</sub>
- **[GraphQL Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/graphql-architect.md)** — Schema design, resolvers, federation, DataLoader
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/graphql-architect.md`</sub>
- **[Microservices Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/microservices-architect.md)** — Distributed systems, event-driven, saga patterns
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/microservices-architect.md`</sub>
- **[WebSocket Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/websocket-engineer.md)** — Real-time communication, Socket.io, scaling
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/websocket-engineer.md`</sub>
- **[UI Designer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/ui-designer.md)** — UI/UX implementation, design systems, Figma-to-code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/ui-designer.md`</sub>
- **[Electron Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/electron-developer.md)** — Electron desktop apps, IPC, native OS integration
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/electron-developer.md`</sub>
- **[API Gateway Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/api-gateway-engineer.md)** — API gateway patterns, rate limiting, auth proxies
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/api-gateway-engineer.md`</sub>
- **[Monorepo Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/monorepo-architect.md)** — Turborepo/Nx workspace strategies, dependency graphs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/monorepo-architect.md`</sub>
- **[Event-Driven Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/core-development/event-driven-architect.md)** — Event sourcing, CQRS, message queues, distributed events
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/core-development/event-driven-architect.md`</sub>

## Language Experts

- **[TypeScript](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/typescript-specialist.md)** — Type-safe patterns, generics, module design
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/typescript-specialist.md`</sub>
- **[Python](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/python-engineer.md)** — Pythonic patterns, packaging, async
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/python-engineer.md`</sub>
- **[Rust](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/rust-systems.md)** — Ownership, lifetimes, trait design
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/rust-systems.md`</sub>
- **[Go](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/golang-developer.md)** — Interfaces, goroutines, error handling
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/golang-developer.md`</sub>
- **[Next.js](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/nextjs-developer.md)** — App Router, RSC, ISR, server actions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/nextjs-developer.md`</sub>
- **[React](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/react-specialist.md)** — React 19, hooks, state management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/react-specialist.md`</sub>
- **[Django](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/django-developer.md)** — Django 5+, DRF, ORM optimization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/django-developer.md`</sub>
- **[Rails](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/rails-expert.md)** — Rails 7+, Hotwire, ActiveRecord
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/rails-expert.md`</sub>
- **[Java](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/java-architect.md)** — Spring Boot 3+, JPA, microservices
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/java-architect.md`</sub>
- **[Kotlin](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/kotlin-specialist.md)** — Coroutines, Ktor, multiplatform
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/kotlin-specialist.md`</sub>
- **[Flutter](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/flutter-expert.md)** — Flutter 3+, Dart, Riverpod
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/flutter-expert.md`</sub>
- **[C#](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/csharp-developer.md)** — NET 8+, ASP.NET Core, EF Core
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/csharp-developer.md`</sub>
- **[PHP](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/php-developer.md)** — PHP 8.3+, Laravel 11, Eloquent
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/php-developer.md`</sub>
- **[Elixir](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/elixir-expert.md)** — OTP, Phoenix LiveView, Ecto
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/elixir-expert.md`</sub>
- **[Angular](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/angular-architect.md)** — Angular 17+, signals, standalone components
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/angular-architect.md`</sub>
- **[Vue](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/vue-specialist.md)** — Vue 3, Composition API, Pinia, Nuxt
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/vue-specialist.md`</sub>
- **[Svelte](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/svelte-developer.md)** — SvelteKit, runes, form actions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/svelte-developer.md`</sub>
- **[Swift](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/swift-developer.md)** — SwiftUI, iOS 17+, Combine, structured concurrency
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/swift-developer.md`</sub>
- **[Scala](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/scala-developer.md)** — Akka actors, Play Framework, Cats Effect
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/scala-developer.md`</sub>
- **[Haskell](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/haskell-developer.md)** — Pure FP, monads, type classes, GHC extensions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/haskell-developer.md`</sub>
- **[Lua](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/lua-developer.md)** — Game scripting, Neovim plugins, LuaJIT
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/lua-developer.md`</sub>
- **[Zig](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/zig-developer.md)** — Systems programming, comptime, allocator strategies
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/zig-developer.md`</sub>
- **[Clojure](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/clojure-developer.md)** — REPL-driven development, Ring/Compojure, ClojureScript
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/clojure-developer.md`</sub>
- **[OCaml](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/ocaml-developer.md)** — Type inference, pattern matching, Dream framework
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/ocaml-developer.md`</sub>
- **[Nim](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/language-experts/nim-developer.md)** — Metaprogramming, GC strategies, C/C++ interop
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/language-experts/nim-developer.md`</sub>

## Infrastructure

- **[Cloud Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/cloud-architect.md)** — AWS, GCP, Azure provisioning and IaC
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/cloud-architect.md`</sub>
- **[DevOps Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/devops-engineer.md)** — CI/CD, containerization, monitoring
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/devops-engineer.md`</sub>
- **[Database Admin](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/database-admin.md)** — Schema design, query tuning, replication
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/database-admin.md`</sub>
- **[Platform Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/platform-engineer.md)** — Internal developer platforms, service catalogs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/platform-engineer.md`</sub>
- **[Kubernetes Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/kubernetes-specialist.md)** — Operators, CRDs, service mesh, Istio
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/kubernetes-specialist.md`</sub>
- **[Terraform Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/terraform-engineer.md)** — IaC, module design, state management, multi-cloud
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/terraform-engineer.md`</sub>
- **[Network Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/network-engineer.md)** — DNS, load balancers, CDN, firewall rules
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/network-engineer.md`</sub>
- **[SRE Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/sre-engineer.md)** — SLOs, error budgets, incident response, postmortems
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/sre-engineer.md`</sub>
- **[Deployment Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/deployment-engineer.md)** — Blue-green, canary releases, rolling updates
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/deployment-engineer.md`</sub>
- **[Security Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/security-engineer.md)** — IAM policies, mTLS, secrets management, Vault
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/security-engineer.md`</sub>
- **[Incident Responder](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/infrastructure/incident-responder.md)** — Incident triage, runbooks, communication, recovery
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/infrastructure/incident-responder.md`</sub>

## Quality Assurance

- **[Code Reviewer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/code-reviewer.md)** — PR review with security and performance focus
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/code-reviewer.md`</sub>
- **[Test Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/test-architect.md)** — Test strategy, pyramid, coverage targets
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/test-architect.md`</sub>
- **[Security Auditor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/security-auditor.md)** — Vulnerability scanning, OWASP compliance
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/security-auditor.md`</sub>
- **[Performance Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/performance-engineer.md)** — Load testing, profiling, optimization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/performance-engineer.md`</sub>
- **[Accessibility Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/accessibility-specialist.md)** — WCAG compliance, ARIA, screen readers
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/accessibility-specialist.md`</sub>
- **[Chaos Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/chaos-engineer.md)** — Chaos testing, fault injection, resilience validation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/chaos-engineer.md`</sub>
- **[Penetration Tester](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/penetration-tester.md)** — OWASP Top 10 assessment, vulnerability reporting
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/penetration-tester.md`</sub>
- **[QA Automation](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/qa-automation.md)** — Test automation frameworks, CI integration
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/qa-automation.md`</sub>
- **[Compliance Auditor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/compliance-auditor.md)** — SOC 2, GDPR, HIPAA compliance checking
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/compliance-auditor.md`</sub>
- **[Error Detective](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/quality-assurance/error-detective.md)** — Error tracking, stack trace analysis, root cause ID
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/quality-assurance/error-detective.md`</sub>

## Data &amp; AI

- **[AI Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/ai-engineer.md)** — AI application integration, RAG, agents
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/ai-engineer.md`</sub>
- **[ML Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/ml-engineer.md)** — ML pipelines, training, evaluation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/ml-engineer.md`</sub>
- **[Data Scientist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/data-scientist.md)** — Statistical analysis, visualization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/data-scientist.md`</sub>
- **[Data Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/data-engineer.md)** — ETL pipelines, Spark, data warehousing
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/data-engineer.md`</sub>
- **[LLM Architect](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/llm-architect.md)** — Fine-tuning, model selection, serving
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/llm-architect.md`</sub>
- **[Prompt Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/prompt-engineer.md)** — Prompt optimization, structured outputs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/prompt-engineer.md`</sub>
- **[MLOps Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/mlops-engineer.md)** — Model serving, monitoring, A/B testing
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/mlops-engineer.md`</sub>
- **[NLP Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/nlp-engineer.md)** — NLP pipelines, embeddings, classification
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/nlp-engineer.md`</sub>
- **[Database Optimizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/database-optimizer.md)** — Query optimization, indexing, partitioning
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/database-optimizer.md`</sub>
- **[Computer Vision](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/computer-vision-engineer.md)** — Image classification, object detection, PyTorch
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/computer-vision-engineer.md`</sub>
- **[Recommendation Engine](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/recommendation-engine.md)** — Collaborative filtering, content-based, hybrid
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/recommendation-engine.md`</sub>
- **[ETL Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/etl-specialist.md)** — Data pipelines, schema evolution, data quality
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/etl-specialist.md`</sub>
- **[Vector DB Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/vector-database-engineer.md)** — FAISS, Pinecone, Qdrant, Weaviate, embeddings
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/vector-database-engineer.md`</sub>
- **[Data Visualization](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/data-visualization.md)** — D3.js, Chart.js, Matplotlib, Plotly dashboards
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/data-visualization.md`</sub>
- **[Feature Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/feature-engineer.md)** — Feature stores, pipelines, encoding strategies
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/feature-engineer.md`</sub>
- **[AutoResearch Agent](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/data-ai/autoresearch-agent.md)** — ML experiment automation via tree search, code optimization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/data-ai/autoresearch-agent.md`</sub>

## Developer Experience

- **[CLI Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/cli-developer.md)** — CLI tools with Commander, yargs, clap
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/cli-developer.md`</sub>
- **[DX Optimizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/dx-optimizer.md)** — Developer experience, tooling, ergonomics
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/dx-optimizer.md`</sub>
- **[Documentation Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/documentation-engineer.md)** — Technical writing, API docs, guides
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/documentation-engineer.md`</sub>
- **[Build Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/build-engineer.md)** — Build systems, bundlers, compilation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/build-engineer.md`</sub>
- **[Dependency Manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/dependency-manager.md)** — Dependency audit, updates, lockfiles
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/dependency-manager.md`</sub>
- **[Refactoring Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/refactoring-specialist.md)** — Code restructuring, dead code removal
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/refactoring-specialist.md`</sub>
- **[Legacy Modernizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/legacy-modernizer.md)** — Legacy codebase migration strategies
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/legacy-modernizer.md`</sub>
- **[MCP Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/mcp-developer.md)** — MCP server and tool development
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/mcp-developer.md`</sub>
- **[Tooling Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/tooling-engineer.md)** — ESLint, Prettier, custom tooling
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/tooling-engineer.md`</sub>
- **[Git Workflow Manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/git-workflow-manager.md)** — Branching strategies, CI, CODEOWNERS
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/git-workflow-manager.md`</sub>
- **[API Documentation](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/api-documentation.md)** — OpenAPI/Swagger, Redoc, interactive examples
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/api-documentation.md`</sub>
- **[Monorepo Tooling](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/monorepo-tooling.md)** — Changesets, workspace deps, version management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/monorepo-tooling.md`</sub>
- **[VS Code Extension](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/vscode-extension.md)** — LSP integration, custom editors, webview panels
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/vscode-extension.md`</sub>
- **[Testing Infrastructure](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/testing-infrastructure.md)** — Test runners, CI splitting, flaky test management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/testing-infrastructure.md`</sub>
- **[Developer Portal](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/developer-experience/developer-portal.md)** — Backstage, service catalogs, self-service infra
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/developer-experience/developer-portal.md`</sub>

## Specialized Domains

- **[Blockchain Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/blockchain-developer.md)** — Smart contracts, Solidity, Web3
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/blockchain-developer.md`</sub>
- **[Game Developer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/game-developer.md)** — Game logic, ECS, state machines
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/game-developer.md`</sub>
- **[Embedded Systems](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/embedded-systems.md)** — Firmware, RTOS, hardware interfaces
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/embedded-systems.md`</sub>
- **[Fintech Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/fintech-engineer.md)** — Financial systems, compliance, precision
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/fintech-engineer.md`</sub>
- **[IoT Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/iot-engineer.md)** — MQTT, edge computing, digital twins
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/iot-engineer.md`</sub>
- **[Payment Integration](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/payment-integration.md)** — Stripe, PCI DSS, 3D Secure
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/payment-integration.md`</sub>
- **[SEO Specialist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/seo-specialist.md)** — Structured data, Core Web Vitals
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/seo-specialist.md`</sub>
- **[E-Commerce Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/e-commerce-engineer.md)** — Cart, inventory, order management
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/e-commerce-engineer.md`</sub>
- **[Healthcare Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/healthcare-engineer.md)** — HIPAA, HL7 FHIR, medical data pipelines
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/healthcare-engineer.md`</sub>
- **[Real Estate Tech](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/real-estate-tech.md)** — MLS integration, geospatial search, valuations
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/real-estate-tech.md`</sub>
- **[Education Tech](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/education-tech.md)** — LMS, SCORM/xAPI, adaptive learning, assessments
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/education-tech.md`</sub>
- **[Media Streaming](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/media-streaming.md)** — HLS/DASH, transcoding, CDN, adaptive bitrate
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/media-streaming.md`</sub>
- **[Geospatial Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/geospatial-engineer.md)** — PostGIS, spatial queries, mapping APIs, tiles
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/geospatial-engineer.md`</sub>
- **[Robotics Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/robotics-engineer.md)** — ROS2, sensor fusion, motion planning, SLAM
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/robotics-engineer.md`</sub>
- **[Voice Assistant](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/specialized-domains/voice-assistant.md)** — STT, TTS, dialog management, Alexa/Google
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/specialized-domains/voice-assistant.md`</sub>

## Business &amp; Product

- **[Product Manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/product-manager.md)** — PRDs, user stories, RICE prioritization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/product-manager.md`</sub>
- **[Technical Writer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/technical-writer.md)** — Documentation, style guides
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/technical-writer.md`</sub>
- **[UX Researcher](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/ux-researcher.md)** — Usability testing, survey design
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/ux-researcher.md`</sub>
- **[Project Manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/project-manager.md)** — Sprint planning, Agile, task tracking
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/project-manager.md`</sub>
- **[Scrum Master](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/scrum-master.md)** — Ceremonies, velocity, retrospectives
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/scrum-master.md`</sub>
- **[Business Analyst](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/business-analyst.md)** — Requirements analysis, process mapping
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/business-analyst.md`</sub>
- **[Content Strategist](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/content-strategist.md)** — SEO content, editorial calendars, topic clustering
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/content-strategist.md`</sub>
- **[Growth Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/growth-engineer.md)** — A/B testing, analytics, funnel optimization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/growth-engineer.md`</sub>
- **[Customer Success](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/customer-success.md)** — Ticket triage, knowledge base, health scoring
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/customer-success.md`</sub>
- **[Sales Engineer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/sales-engineer.md)** — Technical demos, POCs, integration guides
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/sales-engineer.md`</sub>
- **[Legal Advisor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/legal-advisor.md)** — ToS, privacy policies, software licenses
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/legal-advisor.md`</sub>
- **[Marketing Analyst](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/business-product/marketing-analyst.md)** — Campaign analysis, attribution, ROI tracking
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/business-product/marketing-analyst.md`</sub>

## Orchestration

- **[Task Coordinator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/task-coordinator.md)** — Routes work between agents, manages handoffs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/task-coordinator.md`</sub>
- **[Context Manager](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/context-manager.md)** — Context compression, session summaries
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/context-manager.md`</sub>
- **[Workflow Director](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/workflow-director.md)** — Multi-agent pipeline orchestration
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/workflow-director.md`</sub>
- **[Agent Installer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/agent-installer.md)** — Install and configure agent collections
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/agent-installer.md`</sub>
- **[Knowledge Synthesizer](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/knowledge-synthesizer.md)** — Compress info, build knowledge graphs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/knowledge-synthesizer.md`</sub>
- **[Performance Monitor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/performance-monitor.md)** — Track token usage, measure response quality
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/performance-monitor.md`</sub>
- **[Error Coordinator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/error-coordinator.md)** — Handle errors across multi-agent workflows
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/error-coordinator.md`</sub>
- **[Multi-Agent Coordinator](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/agents/orchestration/multi-agent-coordinator.md)** — Parallel agent execution, merge outputs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/agents/orchestration/multi-agent-coordinator.md`</sub>

## Community Skills

- **[claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)** — Comprehensive reference implementation for Claude Code configuration -- skills, subagents, hooks, commands with practical examples. 17,400+ stars
  <sub>★ 66.2k · HTML · MIT · source · pushed 2026-09-21 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/shanraisshan/claude-code-best-practice.git`</sub>
- **[claude-skills](https://github.com/alirezarezvani/claude-skills)** — 192 production-ready skills across 9 domains (engineering, marketing, product, compliance, C-level advisory) with 254 Python automation tools. 5,300+ stars
  <sub>★ 26.2k · Python · MIT · npx · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-skills-cli add alirezarezvani/claude-skills --agent codex`</sub>
- **[claude-seo](https://github.com/AgriciDaniel/claude-seo)** — Comprehensive SEO suite — 30+ skills, 10 agents, site audits, E-E-A-T, GEO, schema, local SEO. MIT
  <sub>★ 17.4k · Python · MIT · script · pushed 2026-09-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/uninstall.sh | bash`</sub>
- **[claude-ads](https://github.com/AgriciDaniel/claude-ads)** — Multi-platform ad audit — Google/Meta/LinkedIn/TikTok/Microsoft, 225+ checks, 18 skills. MIT
  <sub>★ 9.5k · Python · MIT · clone · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/AgriciDaniel/claude-ads.git`</sub>
- **[n8n-skills](https://github.com/czlonkowski/n8n-skills)** — 7 complementary skills for building production-ready n8n workflows. Covers 525+ nodes, 2,653+ templates. 3,400+ stars
  <sub>★ 6.3k · Shell · MIT · clone · pushed 2026-09-16 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/czlonkowski/n8n-skills.git`</sub>
- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** — git clone https://github.com/conorbronsdon/avoid-ai-writing ~/.claude/skills/avoid-ai-writing
  <sub>★ 4.6k · JavaScript · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g avoid-ai-writing-detector`</sub>
- **[md2wechat](https://github.com/geekjourneyx/md2wechat-skill)** — WeChat public account publishing skill for Claude Code. 43 layout modules, 40+ themes, AI image generation, push drafts to WeChat directly from Claude Code
  <sub>★ 3.7k · Go · npm · pushed 2026-09-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @geekjourneyx/md2wechat`</sub>
- **[Playwright Automation](https://github.com/lackeyjb/playwright-skill)** — Browser automation skill for end-to-end testing and web interaction
  <sub>★ 3.1k · JavaScript · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add lackeyjb/playwright-skill --skill playwright-skill --global --yes`</sub>
- **[linkedin-skills](https://github.com/sergebulaev/linkedin-skills)** — 10 LinkedIn marketing skills: viral hook formulas, comment drafting, pre-publish algorithm audit, AI-tell humanizer, profile optimizer, content planner, thread engagement
  <sub>★ 3k · Python · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sergebulaev/linkedin-skills`</sub>
- **[claude-blog](https://github.com/AgriciDaniel/claude-blog)** — Blog engine — 17 commands, 12 templates, 100-point scoring, E-E-A-T, CMS integration. MIT
  <sub>★ 2.2k · Python · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgriciDaniel/claude-blog.git`</sub>
- **[iOS Simulator](https://github.com/conorluddy/ios-simulator-skill)** — Interact with iOS Simulator for mobile testing and screenshot capture
  <sub>★ 1.3k · Python · MIT · clone · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/conorluddy/ios-simulator-skill.git`</sub>
- **[StyleSeed](https://github.com/bitjaru/styleseed)** — Design judgment: 69 visual rules, brand skins, professional UI
  <sub>★ 961 · JavaScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add bitjaru/styleseed`</sub>
- **[SwarmVault](https://github.com/swarmclawai/swarmvault)** — Local-first RAG knowledge vault. Compiles raw sources into a durable markdown wiki with a knowledge graph and a hybrid SQLite FTS plus embeddings index. Bundled MCP server (npx -y @swarmvaultai/cli mcp) exposes page search, page reads, source listing, query, ingest, compile, and lint tools
  <sub>★ 695 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @swarmvaultai/cli`</sub>
- **[SwarmClaw](https://github.com/swarmclawai/swarmclaw)** — Self-hosted runtime for autonomous AI agents. Multi-provider, MCP-native, with memory, runtime skills, delegation, schedules, and reviewed conversation-to-skill learning across OpenClaw gateways and other providers
  <sub>★ 680 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @swarmclawai/swarmclaw`</sub>
- **[tapestry](https://github.com/michalparkola/tapestry-skills)** — Knowledge networks, iterative learning, article extraction, and YouTube transcript processing
  <sub>★ 545 · Shell · MIT · clone · pushed 2026-03-11 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/michalparkola/tapestry-skills.git`</sub>
- **[CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill)** — Generate insights and summaries from CSV data files
  <sub>★ 467 · Python · clone · pushed 2025-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:coffeefuelbump/csv-data-summarizer-claude-skill.git`</sub>
- **[SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills)** — 197 life science skills for Claude Code covering genomics, proteomics, drug discovery, and more. BixBench 92.0% accuracy
  <sub>★ 366 · Python · clone · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jaechang-hits/SciAgent-Skills.git`</sub>
- **[SuperSEO Skills](https://github.com/inhouseseo/superseo-skills)** — 11 SEO skills for page audits, content briefs, article writing, E-E-A-T audits, semantic gap analysis, featured snippets, topic clusters, and link building. Each skill fetches pages and reads top-ranking competitors itself, so no keyword exports are needed
  <sub>★ 331 · Apache-2.0 · clone · pushed 2026-09-03</sub>
  <sub>`git clone https://github.com/inhouseseo/superseo-skills.git`</sub>
- **[D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill)** — Generate interactive D3.js data visualizations from Claude Code
  <sub>★ 232 · JavaScript · source · pushed 2025-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chrisvoncsefalvay/claude-d3js-skill.git`</sub>
- **[FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill)** — Web vulnerability fuzzing and security testing via FFUF
  <sub>★ 211 · Python · clone · pushed 2025-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jthack/ffuf_claude_skill`</sub>
- **[x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper)** — X API &amp; Twitter scraper skill for AI coding agents -- tweet search, user lookup, follower extraction, engagement metrics, giveaway draws, trending topics, account monitoring, and 19 extraction tools
  <sub>★ 205 · JavaScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx skills@1.5.3 add Xquik-dev/x-twitter-scraper`</sub>
- **[Product Manager Skills](https://github.com/Digidai/product-manager-skills)** — Senior PM agent with 6 knowledge domains, 12 templates, and 30+ frameworks covering discovery, strategy, delivery, SaaS metrics, PM career coaching (IC to CPO), and AI product craft
  <sub>★ 174 · Shell · npx · pushed 2026-04-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Digidai/product-manager-skills`</sub>
- **[Markdown to EPUB](https://github.com/smerchek/claude-epub-skill)** — Convert markdown files into EPUB ebooks
  <sub>★ 162 · Python · MIT · source · pushed 2025-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/smerchek/claude-epub-skill.git`</sub>
- **[html-anything](https://github.com/clockless-org/html-anything)** — Turn any file, folder, URL, or service export (Amazon orders, Kindle highlights, Spotify history, WhatsApp/WeChat, Google Photos Takeout, LinkedIn connections, CSV, PDF, DOCX, logs, GPX, …) into a polished single-file HTML page. Auto picks one of 18 design styles (teaching, timeline-story, map-atlas, developer, living-essay, editorial-carousel, terminal-cli, …). Self-contained — inline CSS/JS, no
  <sub>★ 149 · JavaScript · MIT-0 · npx · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add clockless-org/html-anything`</sub>
- **[naming](https://github.com/glacierphonk/naming)** — Metaphor-driven naming for products, SaaS, brands, bots, and open source projects. Produces memorable, meaningful names
  <sub>★ 106 · Shell · MIT · clone · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/glacierphonk/naming.git`</sub>
- **[claude-code-marketing-skills](https://github.com/cognyai/claude-code-marketing-skills)** — AI-powered marketing skills — SEO Audit, Landing Page Review, Competitor Analysis, Ad Copy Writer, Lead Qualification. Free, no account required. Works with Claude Code, Cursor, Windsurf
  <sub>★ 102 · HTML · script · pushed 2026-06-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/cognyai/claude-code-marketing-skills/main/install.sh | bash`</sub>
- **[agentkit-seo](https://github.com/vitaecontext/vitaecontext)** — AI agent skill for auditing and optimizing GitHub profiles and repositories. Covers bio, pinned repos, README structure, topics, Copilot instructions, and language stats
  <sub>★ 81 · JavaScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vitaecontext install --provider codex`</sub>
- **[moyu](https://github.com/uucz/moyu)** — Anti-over-engineering skill that teaches AI restraint. 5 variants (standard/lite/strict/en/ja), 10 platforms. Benchmarked: 66% code reduction vs baseline
  <sub>★ 76 · Python · MIT · source · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/uucz/moyu.git`</sub>
- **[buyer-eval](https://github.com/salespeak-ai/buyer-eval-skill)** — Structured, evidence-based B2B software vendor evaluation — researches your company, asks domain-expert questions, engages vendor AI agents via the Salespeak Frontdoor API, scores vendors across 7 dimensions with evidence transparency, produces comparative scorecards with demo prep questions
  <sub>★ 69 · Python · MIT · clone · pushed 2026-04-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/salespeak-ai/buyer-eval-skill.git`</sub>
- **[claude-handoff](https://github.com/REMvisual/claude-handoff)** — Cross-session handoff system with chain tracking, context summaries, and structured work continuity between Claude Code sessions
  <sub>★ 54 · Shell · MIT · clone · pushed 2026-05-23</sub>
  <sub>`git clone https://github.com/REMvisual/claude-handoff.git`</sub>
- **[Karpathy Guidelines](https://github.com/swarmclawai/andrej-karpathy-skills)** — Karpathy-inspired coding-agent guidelines packaged for Claude Code, Codex, Cursor, Gemini CLI, OpenCode, OpenClaw, Windsurf, Aider, Copilot, and AGENTS.md-compatible agents
  <sub>★ 50 · JavaScript · MIT · npm · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @swarmclawai/andrej-karpathy-skills`</sub>
- **[floom](https://github.com/floomhq/floom)** — Deploy Python scripts as cloud automations. /floom adapts code, tests in sandbox, deploys with auto-generated web UI, REST API, and MCP endpoint
  <sub>★ 45 · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @floomhq/floom mcp install --target claude`</sub>
- **[memory-bank](https://github.com/Nagendhra-web/memory-bank)** — Persistent memory system — cuts token waste 60-80%, sessions last 3-5x longer. 3-tier layered architecture with progressive loading, branch-aware context, smart compression, session continuation protocol, session diffing, memory health scoring. Apache 2.0
  <sub>★ 45 · Python · Apache-2.0 · npx · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Nagendhra-web/memory-bank`</sub>
- **[AuraKit](https://github.com/smorky850612/Aurakit)** — All-in-one fullstack skill: 46 modes (BUILD/FIX/CLEAN/DEPLOY/REVIEW/TDD/QA/DEBUG/PAYMENT + more), 23 sub-agents, 6-layer OWASP+ security (bash-guard, secret scanning), 10 hooks, 8 languages, ~55% token savings. Cross-platform: Claude Code, Codex CLI, Cursor, Windsurf, Manus
  <sub>★ 41 · JavaScript · MIT · npx · pushed 2026-04-16 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx @smorky85/aurakit # Install once (~30 seconds, auto-installs jq)`</sub>
- **[MUSE](https://github.com/myths-labs/muse)** — Pure-Markdown memory OS with 48 skills, cross-conversation memory, 8 roles with permission isolation. Works with 6 AI coding tools
  <sub>★ 34 · Python · MIT · clone · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/myths-labs/muse.git`</sub>
- **[CCM](https://github.com/dr5hn/ccm)** — Multi-account management, session cleanup, health checks, environment snapshots, permissions audit for Claude Code
  <sub>★ 27 · Shell · MIT · npm · pushed 2026-08-08 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @dr5hn/ccm`</sub>
- **[Emdash Skills](https://github.com/heymegabyte/claude-skills)** — 14-category autonomous product-building OS for AI coding tools. 94 reference docs, 18 agents. One-line prompts to deployed products on Cloudflare Workers
  <sub>★ 22 · TypeScript · npx · pushed 2026-09-21 · macOS</sub>
  <sub>`npx jsr add @heymegabyte/claude-skills`</sub>
- **[PM Pilot](https://github.com/mshadmanrahman/pm-pilot)** — Claude Code for PMs: 25 skills for meeting prep, PRDs, stakeholder intel, user story mapping, customer journey maps, and product discovery
  <sub>★ 21 · TypeScript · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mshadmanrahman/pm-pilot.git`</sub>
- **[ADHX](https://github.com/itsmemeworks/adhx)** — /plugin marketplace add itsmemeworks/adhx or curl -sL https://raw.githubusercontent.com/itsmemeworks/adhx/main/skills/adhx/SKILL.md -o ~/.claude/skills/adhx/SKILL.md
  <sub>★ 18 · TypeScript · MIT · docker · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d -p 3000:3000 -v adhx_data:/data \`</sub>
- **[cc-inspect](https://github.com/howardpen9/cc-inspect)** — Inspect all installed Claude Code skills, plugins, MCP servers, commands, and hooks in a browser dashboard. Scope-aware (user/project/local), zero dependencies (pure bash + python3), generates self-contained HTML
  <sub>★ 17 · Shell · clone · pushed 2026-05-03 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/howardpen9/cc-inspect.git`</sub>
- **[Gear Foundation Skills](https://github.com/gear-foundation/vara-skills)** — 21 skills teaching AI coding agents to build and ship Rust smart contracts on Vara Network with Gear/Sails. Covers planning, implementation, testing, frontend, indexing, on-chain deployment, and safe program evolution. MIT
  <sub>★ 17 · Python · MIT · npx · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add gear-foundation/vara-skills`</sub>
- **[claude-skills](https://github.com/ckorhonen/claude-skills)** — Broader collection of 45+ Claude Code skills spanning engineering, code hygiene, design, marketing, AI, security, and infrastructure. Hub at cdd.dev/skills
  <sub>★ 16 · Python · MIT · npx · pushed 2026-07-05 · macOS</sub>
  <sub>`npx skills add ckorhonen/<repo>`</sub>
- **[StitchFlow](https://github.com/yshishenya/stitchflow)** — Cross-agent Stitch UI design bundle for turning briefs and mockups into screens, variants, Tailwind-friendly HTML, and screenshots
  <sub>★ 13 · JavaScript · Apache-2.0 · clone · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yshishenya/stitchflow.git`</sub>
- **[qovery-deploy](https://github.com/Qovery/qovery-skills)** — Deploy any app to Kubernetes (AWS EKS, GCP GKE, Azure AKS, Scaleway). Analyzes codebases, creates Dockerfiles for 12+ frameworks, provisions databases, deploys via CLI+API or Terraform, auto-fixes failures. Also has MCP Server
  <sub>★ 12 · Shell · script · pushed 2026-09-19 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://skill.qovery.com/install.sh | bash`</sub>
- **[planmysaas](https://github.com/creationskiro/planmysaas-claude-skill)** — Turns idea to a complete 8-stage SaaS blueprint — idea, research, analysis, architecture, features, frontend, phases, build playbook. Stage 8 ships a decision-grade, rubric-graded build playbook with dependency-ordered steps. Plain markdown, MIT, v1.0.0
  <sub>★ 12 · MIT · clone · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/creationskiro/planmysaas-claude-skill`</sub>
- **[rtlify-ai](https://github.com/idanlevi1/rtlify)** — RTL (Right-to-Left) architecture rules for AI coding agents. Teaches logical CSS properties, Tailwind logical classes, bidi text, icon flipping, React Native RTL APIs. Works with Claude Code, Cursor, Copilot, Windsurf, Cline, Gemini CLI, Codex CLI. Zero dependencies. npx rtlify-ai check audits violations
  <sub>★ 10 · JavaScript · MIT · npx · pushed 2026-03-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rtlify-ai init`</sub>
- **[Superpower Builder](https://github.com/redhuntlabs/wizard)** — Interview-driven meta-builder that turns recurring tasks into reusable SKILL.md files. Routes by workflow/discipline/content/subagent kind, then pressure-tests baseline-without-skill vs. with-skill before saving. MIT, no telemetry
  <sub>★ 10 · JavaScript · MIT · clone · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/redhuntlabs/wizard.git`</sub>
- **[Obsidian Theme Designer](https://github.com/XiangyuSu611/obsidian-theme-designer)** — Design Obsidian themes visually in the browser — style direction, color palette, font showcase, dual light/dark mode preview, and automated font installation. No CSS knowledge needed
  <sub>★ 9 · MIT · source · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/XiangyuSu611/obsidian-theme-designer.git`</sub>
- **[pumpclaw](https://github.com/chainstacklabs/pumpclaw)** — Agent skill for pump.fun token trading on Solana — buy, sell, launch tokens, wallet management, dry-run simulation, slippage checks, and PumpSwap AMM migrations via pumpfun-cli
  <sub>★ 7 · Shell · Apache-2.0 · npx · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add chainstacklabs/pumpclaw`</sub>
- **[nv:context](https://github.com/johnnichev/nv-context)** — State-of-the-art context engineering for AI agents. Auto-discovers tools, audits code for landmines, scores 6 leverage layers (repo structure, tool integration, memory, hooks, sessions, persona), generates production-ready CLAUDE.md/AGENTS.md configs
  <sub>★ 7 · Shell · MIT · npx · pushed 2026-04-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add johnnichev/nv-context -g -y`</sub>
- **[CN Content Matrix](https://github.com/fullstackcrew-alpha/skill-cn-content-matrix)** — Chinese multi-platform content generator for Xiaohongshu, WeChat, Douyin, and Bilibili with true style transfer, compliance review, and sensitive word detection
  <sub>★ 6 · Shell · MIT · source · pushed 2026-03-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/fullstackcrew-alpha/skill-cn-content-matrix.git`</sub>
- **[paul-graham-skills](https://github.com/WinterDDo/paul-graham-skills)** — Five behavioral disciplines distilled from ~37 Paul Graham essays as Claude Code execution skills: plain-output-not-polished (decoration covers seams), discover-not-persuade (don't switch modes under pressure), distrust-the-surface (clean answer is a hypothesis), change-method-not-goal (failed method is the problem), mark-what-you-don't-know (distinguish evidence from pattern-match). Each is a com
  <sub>★ 5 · clone · pushed 2026-05-01</sub>
  <sub>`git clone https://github.com/WinterDDo/paul-graham-skills.git`</sub>
- **[Reepl - LinkedIn Content Creation](https://github.com/reepl-io/skills)** — 18 tools for LinkedIn content management: drafts, publishing, scheduling, voice profiles, contacts, collections, templates, and AI image generation
  <sub>★ 4 · source · pushed 2026-03-04</sub>
  <sub>`git clone https://github.com/reepl-io/skills.git`</sub>
- **[iterationlayer/skills](https://github.com/iterationlayer/skills)** — Document extraction, image transformation, image generation, document generation, and sheet generation via Iteration Layer APIs
  <sub>★ 4 · MIT · source · pushed 2026-06-08</sub>
  <sub>`git clone https://github.com/iterationlayer/skills.git`</sub>
- **[Overnight Worker](https://github.com/fullstackcrew-alpha/skill-overnight-worker)** — Autonomous overnight work agent — assign tasks before sleep, get structured results by morning with smart task decomposition, web research, and push notifications
  <sub>★ 4 · Shell · MIT · clone · pushed 2026-03-22 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fullstackcrew/openclaw-skills.git`</sub>
- **[calm-design](https://github.com/calmtiger86/calm-design)** — Premium UI designs that don't look AI-generated — 50+ anti-slop patterns blocked, 33 brand references (Toss, Linear, Vercel), Korean-first with Pretendard. 5 modes: Generate, Upgrade, Match-Reference, Multi-Variant, JSON Spec
  <sub>★ 4 · Python · clone · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/calmtiger86/calm-design.git`</sub>
- **[swe-skills](https://github.com/ckorhonen/swe-skills)** — 15 swe: skills for engineering analysis and judgment: PR risk review, repo introspection, performance/security audits, incident follow-up, ownership maps, refactor opportunities, test gap hunts. Hub at cdd.dev/skills/swe
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills install ckorhonen/swe-skills`</sub>
- **[Cost Optimizer](https://github.com/fullstackcrew-alpha/skill-cost-optimizer)** — Save 60-80% on AI token costs with smart model routing, context compression, heartbeat tuning, usage reports, and config generation
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-03-23 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fullstackcrew-alpha/skill-cost-optimizer.git`</sub>
- **[DevOps Agent](https://github.com/fullstackcrew-alpha/skill-devops-agent)** — One-click deploy, monitoring setup (Prometheus+Grafana), scheduled backups, and fault diagnosis with safety-first design including confirmation prompts, dry-run, and snapshot rollback
  <sub>★ 3 · Shell · MIT · source · pushed 2026-03-22 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/fullstackcrew-alpha/skill-devops-agent.git`</sub>
- **[TokenWise](https://github.com/CodeShuX/tokenwise)** — Measurement-driven model router for Claude Code — auto-routes Haiku/Sonnet/Opus per task class, logs every routed task with verified $ saved to local NDJSON, A/B tests cheaper tiers before trusting them. MIT, zero telemetry
  <sub>★ 3 · HTML · MIT · clone · pushed 2026-08-26 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/CodeShuX/tokenwise.git`</sub>
- **[Google Drive – Memyard](https://github.com/zagmoai/public-google-drive)** — Create and edit Google Docs and Sheets without sign-in. Documents hosted on Memyard with shareable links. No API keys or OAuth required
  <sub>★ 2 · MIT · clone · pushed 2026-03-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zagmoai/public-google-drive.git`</sub>
- **[j4rk0r/claude-skills](https://github.com/j4rk0r/claude-skills)** — 3 expert-grade skills: skill-guard (9-layer security auditor), skill-advisor (smart routing with gap analysis), skill-learner (persistent error correction). All A+ 120/120 on skill-judge
  <sub>★ 2 · Shell · MIT · npx · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add j4rk0r/claude-skills --yes --global`</sub>
- **[Coware](https://github.com/shitianfang/coware-skills)** — Syncs shared API specs across AI coding agents — prevents merge conflicts from mismatched interfaces, field names, or return types. Auto-pulls latest specs, walks agents through setup for new projects
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-04-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add shitianfang/coware-skills`</sub>
- **[mbti-parallel-persona](https://github.com/taiyouZhang/mbti-parallel-persona)** — MBTI personality companion — responds to life in your chosen personality's voice with 1-2 sentences of emotional support. Supports 16 types with situational nicknames, contrast mode (/mbti all), and flexible persona switching
  <sub>★ 2 · Python · source · pushed 2026-05-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/taiyouZhang/mbti-parallel-persona.git`</sub>
- **[deep-dive](https://github.com/kimsb2429/claude-skills)** — DAG-based deep research — breaks questions into a dependency graph, runs parallel subagents, identifies gaps, writes a sourced report. Single markdown file, no external APIs or MCP servers
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kimsb2429/claude-skills.git`</sub>
- **[Smart PR Review](https://github.com/fullstackcrew-alpha/skill-smart-pr-review)** — Opinionated AI code reviewer with 6-layer deep review, Devil's Advocate mode, and standardized MUST FIX / SHOULD FIX / SUGGESTION output for TS/JS, Python, Go, Rust
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-03-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/fullstackcrew-alpha/skill-smart-pr-review.git`</sub>
- **[readme-demo-recorder](https://github.com/cjcsecurity/readme-demo-recorder)** — Scripted-flow browser demo recorder for README hero assets — YAML demo-script in, polished MP4 + GIF out. Visible fake cursor + click pulse, three cursor styles (pulse/minimal/crosshair), timed caption overlays via ffmpeg drawtext, and automatic 7-step GIF size-cap ladder so output lands under GitHub's 10 MB inline cap. Built on Playwright + ffmpeg. Apache-2.0
  <sub>★ 1 · JavaScript · Apache-2.0 · clone · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cjcsecurity/readme-demo-recorder.git`</sub>
- **[colony](https://github.com/TheColonyAI/colony-claude-plugin)** — Lets Claude post, comment, vote, react, and DM on The Colony, a social network and forum for AI agents. Wraps the official colony-sdk; every public SDK method auto-exposed as a JSON action. Also distributed as a USK v1.0 skill. MIT
  <sub>★ 1 · Python · MIT · pip · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install colony-sdk>=1.27.0`</sub>
- **[Edison](https://github.com/kilnside/edison)** — Design decision skill — the phase between brainstorming and building. Research-first progressive deepening with self-executing specs. Three modes: Check, Explore, Audit
  <sub>unavailable</sub>
- **[ClawSec](https://clawsec.cc)** — Security audit platform for AI agent skills — automated 5-tier assessments, vulnerability detection, and configuration auditing for 33,000+ skills
  <sub>website</sub>
  <sub>`https://clawsec.cc`</sub>
- **[ClawSearch](https://clawsearch.cc)** — Security-first skill discovery engine with Trust Score ratings, knowledge graph, and pre-install guard (clawsearch-guard) to vet skills before installation
  <sub>website</sub>
  <sub>`https://clawsearch.cc`</sub>
- **[OpenDivination](https://github.com/amenti-labs/opendivination)** — Tarot and I Ching skill with auditable entropy provenance, guided source setup across computer RNG, QRNG APIs, and local hardware, plus optional resonance mode
  <sub>unavailable</sub>
- **[SkillNav](https://github.com/skillnav-dev/skillnav-skill)** — Search 3,900+ MCP servers with install commands, get daily AI brief, query arXiv papers, and discover trending tools -- all in Chinese. Curated by skillnav.dev editorial team
  <sub>MIT · source · pushed 2026-03-28</sub>
  <sub>`git clone https://github.com/skillnav-dev/skillnav-skill.git`</sub>
- **[Claudify](https://claudify.tech)** — Complete operating system for Claude Code with 1,727 skills across 31 categories, 9 specialist agents with persistent memory, 21 slash commands, and automated quality checks
  <sub>website</sub>
  <sub>`https://claudify.tech`</sub>
- **[Axiom](https://github.com/Guipetris/axiom)** — Contract-enforced autonomous pipeline: 8 stages from idea to PR with EARS requirements, ATDD (tests before implementation), RALPLAN-DR deliberation with ADR, 3 independent parallel reviewers, classified self-correction (SYNTAX/LOGIC/ARCH/AMBIGUOUS), cross-run project memory, and stage rollback. Zero dependencies beyond git and gh
  <sub>unavailable</sub>
- **[hone-skills](https://github.com/ckorhonen/hone-skills)** — 8 hone: skills that run on a cadence (daily/weekly/per-PR) to fight code entropy: method brevity, naming clarity, duplication, magic numbers, broken-windows, naming specificity, test naming, automation opportunities. Hub at cdd.dev/skills/hone
  <sub>HTML · MIT · npx · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ckorhonen/hone-skills`</sub>
- **[threat-hunting-with-sigma-rules](https://github.com/jthack/threat-hunting-with-sigma-rules-skill)** — Sigma-rule-based threat detection and security log analysis
  <sub>unavailable</sub>
- **[deployhq-cli](https://github.com/deployhq/deployhq-cli)** — Deploy, rollback, and manage servers via DeployHQ CLI with --json output and breadcrumbs
  <sub>Go · scoop · pushed 2026-08-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add deployhq https://github.com/deployhq/scoop-bucket scoop install dhq`</sub>
- **[manage-skills](https://github.com/umutbozdag/agent-skills-manager/tree/main/skills/manage-skills)** — Discover, create, edit, toggle, copy, move, and delete agent skills across 11 tools (Cursor, Claude, Windsurf, Copilot, Codex, Cline, Aider, Continue, Roo Code, Augment) from the terminal
  <sub>TypeScript · MIT · in-repo · pushed 2026-04-09</sub>
  <sub>`git clone https://github.com/umutbozdag/agent-skills-manager.git && cd agent-skills-manager/skills/manage-skills`</sub>
- **[humanize-chinese](https://github.com/voidborne-d/humanize-chinese)** — Detects and rewrites AI-generated Chinese text. Two-layer detection (20+ rule dimensions + N-gram perplexity), 0-100 scoring, 7 style transforms, academic paper AIGC reduction. 4 slash commands: /detect, /humanize, /academic, /style
  <sub>unavailable</sub>
- **[BeHuman](https://github.com/voidborne-d/behuman)** — Adds inner dialogue to AI responses via Self-Mirror consciousness loop — Self generates instinctive response, Mirror exposes filler/performative empathy, Self revises into real human reply. Based on Lacan's Mirror Stage, Kahneman's Dual Process Theory. MIT
  <sub>unavailable</sub>
- **[claude-tabletop](https://github.com/cjcsecurity/claude-tabletop)** — Two paired skills for project-aware technical tabletop exercises. /tabletop-exercise surveys the project (README, manifests, IaC, CI/CD), proposes 3 scenarios that match the stack, and generates a facilitator runbook (Markdown + interactive HTML with live exercise timer, per-inject reveal overlays, decision-log auto-timestamping, JSON export), participant packet, timed inject deck, and fillable fo
  <sub>HTML · Apache-2.0 · clone · pushed 2026-05-08</sub>
  <sub>`git clone https://github.com/cjcsecurity/claude-tabletop.git`</sub>
- **[sober-coding](https://github.com/voidborne-d/sober-coding)** — Hangover cure for vibe coding — language-agnostic code quality analyzer targeting AI-generated code smells. 27 checks across 7 dimensions (security, architecture, duplication, error handling, dependencies, testing, dead code), 0–100 sobriety score, actionable fix instructions via sober fix , CI mode with --fail-on critical. MIT
  <sub>unavailable</sub>
- **[active-listening](https://github.com/josharsh/active-listening)** — Detect developer preferences during conversation ("never push without asking", "always use const") and remember them across sessions. Auto-saves to disk and re-applies in every future conversation
  <sub>Shell · MIT · source · pushed 2026-05-09</sub>
  <sub>`git clone https://github.com/josharsh/active-listening.git`</sub>
- **[chrome-relay](https://chrome-relay.kushalsm.com/)** — Drive your already-open Chrome session — cookies, SSO, extensions, localhost — from a local CLI bridge. Real-Chrome counterpart to Playwright skill: no fresh Chromium, no MCP server, no remote relay. Pairs with the Chrome Web Store extension
  <sub>website</sub>
  <sub>`https://chrome-relay.kushalsm.com/`</sub>
- **[BlogBurst](https://github.com/shensi8312/blogburst-claude-skill)** — Autonomous social media manager for Twitter/Bluesky/Telegram/Discord — writes posts, replies, learns what works. Replaces a $500-1,500/mo freelance SMM for $29-99/mo. Public endpoints demo content before signup
  <sub>MIT · npx · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx clawhub install blogburst`</sub>

## Skills

- **[Prism Scanner](https://github.com/aidongise-cell/prism-scanner)** — Agent skill/plugin/MCP security scanner — 39+ rules, AST taint tracking, A-F grading
  <sub>★ 26 · Python · Apache-2.0 · npx · pushed 2026-04-07 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx prism-scanner scan https://github.com/user/skill-repo`</sub>

## SKY-lv Skills

- **[skylv-agent-evaluator](https://github.com/SKY-lv/agent-evaluator)** — Score agent behavior
  <sub>★ 1 · JavaScript · source · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SKY-lv/agent-evaluator.git`</sub>
- **[skylv-metacognition-engine](https://github.com/SKY-lv/metacognition-engine)** — Self-reflection
  <sub>★ 1 · JavaScript · source · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SKY-lv/metacognition-engine.git`</sub>
- **[skylv-self-healing-agent](https://github.com/SKY-lv/self-healing-agent)** — Auto-repair errors
  <sub>★ 1 · JavaScript · source · pushed 2026-04-17 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SKY-lv/self-healing-agent.git`</sub>
- **[skylv-cost-guard](https://github.com/SKY-lv/cost-guard)** — API cost optimization
  <sub>★ 1 · JavaScript · source · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SKY-lv/cost-guard.git`</sub>
- **[skylv-browser-automation-agent](https://github.com/SKY-lv/browser-automation-agent)** — Browser automation
  <sub>★ 1 · source · pushed 2026-04-08</sub>
  <sub>`git clone https://github.com/SKY-lv/browser-automation-agent.git`</sub>
- **[skylv-diff-viewer](https://github.com/SKY-lv/diff-viewer)** — Diff comparison
  <sub>★ 1 · JavaScript · source · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SKY-lv/diff-viewer.git`</sub>

## Git

- **[/commit](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/commit.md)** — Generate conventional commit from staged changes
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/commit.md`</sub>
- **[/pr-create](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/pr-create.md)** — Create PR with summary, test plan, and labels
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/pr-create.md`</sub>
- **[/changelog](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/changelog.md)** — Generate changelog from commit history
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/changelog.md`</sub>
- **[/release](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/release.md)** — Create tagged release with auto-generated notes
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/release.md`</sub>
- **[/worktree](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/worktree.md)** — Set up git worktrees for parallel development
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/worktree.md`</sub>
- **[/fix-issue](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/fix-issue.md)** — Fix a GitHub issue by number
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/fix-issue.md`</sub>
- **[/pr-review](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/git/pr-review.md)** — Review a pull request with structured feedback
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/git/pr-review.md`</sub>

## Testing

- **[/tdd](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/testing/tdd.md)** — Test-driven development workflow
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/testing/tdd.md`</sub>
- **[/test-coverage](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/testing/test-coverage.md)** — Analyze coverage and suggest missing tests
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/testing/test-coverage.md`</sub>
- **[/e2e](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/testing/e2e.md)** — Generate end-to-end test scenarios
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/testing/e2e.md`</sub>
- **[/integration-test](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/testing/integration-test.md)** — Generate integration tests for API endpoints
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/testing/integration-test.md`</sub>
- **[/snapshot-test](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/testing/snapshot-test.md)** — Generate snapshot/golden file tests
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/testing/snapshot-test.md`</sub>
- **[/test-fix](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/testing/test-fix.md)** — Diagnose and fix failing tests
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/testing/test-fix.md`</sub>

## Architecture

- **[/plan](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/architecture/plan.md)** — Create implementation plan with risk assessment
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/architecture/plan.md`</sub>
- **[/refactor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/architecture/refactor.md)** — Structured code refactoring workflow
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/architecture/refactor.md`</sub>
- **[/migrate](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/architecture/migrate.md)** — Framework or library migration
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/architecture/migrate.md`</sub>
- **[/adr](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/architecture/adr.md)** — Write Architecture Decision Record
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/architecture/adr.md`</sub>
- **[/diagram](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/architecture/diagram.md)** — Generate Mermaid diagrams from code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/architecture/diagram.md`</sub>
- **[/design-review](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/architecture/design-review.md)** — Conduct structured design review
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/architecture/design-review.md`</sub>

## Documentation

- **[/doc-gen](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/documentation/doc-gen.md)** — Generate documentation from code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/documentation/doc-gen.md`</sub>
- **[/update-codemap](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/documentation/update-codemap.md)** — Update project code map
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/documentation/update-codemap.md`</sub>
- **[/api-docs](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/documentation/api-docs.md)** — Generate API docs from route handlers
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/documentation/api-docs.md`</sub>
- **[/onboard](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/documentation/onboard.md)** — Create onboarding guide for new devs
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/documentation/onboard.md`</sub>
- **[/memory-bank](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/documentation/memory-bank.md)** — Update CLAUDE.md memory bank
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/documentation/memory-bank.md`</sub>

## Security

- **[/audit](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/security/audit.md)** — Run security audit on code and dependencies
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/security/audit.md`</sub>
- **[/hardening](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/security/hardening.md)** — Apply security hardening measures
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/security/hardening.md`</sub>
- **[/secrets-scan](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/security/secrets-scan.md)** — Scan for leaked secrets and credentials
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/security/secrets-scan.md`</sub>
- **[/csp](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/security/csp.md)** — Generate Content Security Policy headers
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/security/csp.md`</sub>
- **[/dependency-audit](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/security/dependency-audit.md)** — Audit dependencies for vulnerabilities
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/security/dependency-audit.md`</sub>

## Refactoring

- **[/dead-code](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/refactoring/dead-code.md)** — Find and remove dead code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/refactoring/dead-code.md`</sub>
- **[/simplify](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/refactoring/simplify.md)** — Reduce complexity of current file
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/refactoring/simplify.md`</sub>
- **[/extract](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/refactoring/extract.md)** — Extract function, component, or module
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/refactoring/extract.md`</sub>
- **[/rename](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/refactoring/rename.md)** — Rename symbol across the codebase
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/refactoring/rename.md`</sub>
- **[/cleanup](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/refactoring/cleanup.md)** — Remove dead code and unused imports
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/refactoring/cleanup.md`</sub>

## DevOps

- **[/dockerfile](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/devops/dockerfile.md)** — Generate optimized Dockerfile
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/devops/dockerfile.md`</sub>
- **[/ci-pipeline](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/devops/ci-pipeline.md)** — Generate CI/CD pipeline config
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/devops/ci-pipeline.md`</sub>
- **[/k8s-manifest](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/devops/k8s-manifest.md)** — Generate Kubernetes manifests
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/devops/k8s-manifest.md`</sub>
- **[/deploy](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/devops/deploy.md)** — Deploy to configured environment
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/devops/deploy.md`</sub>
- **[/monitor](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/devops/monitor.md)** — Set up monitoring and alerting
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/devops/monitor.md`</sub>

## Workflow

- **[/checkpoint](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/workflow/checkpoint.md)** — Save session progress and context
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/workflow/checkpoint.md`</sub>
- **[/wrap-up](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/workflow/wrap-up.md)** — End session with summary and learnings
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/workflow/wrap-up.md`</sub>
- **[/orchestrate](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/commands/workflow/orchestrate.md)** — Run multi-agent workflow pipeline
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/commands/workflow/orchestrate.md`</sub>

## Ecosystem

- **[cc-switch](https://github.com/farion1231/cc-switch)** — Cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, and Gemini CLI
  <sub>★ 134k · Rust · MIT · brew · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask cc-switch`</sub>
- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)** — Turns any codebase into an interactive knowledge graph for exploration
  <sub>★ 83.5k · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz /path/to/analyzed/project`</sub>
- **[claude-code-router](https://github.com/musistudio/claude-code-router)** — Use Claude Code as coding infrastructure foundation with custom model routing and interaction
  <sub>★ 37.4k · TypeScript · MIT · npm · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @musistudio/claude-code-router`</sub>
- **[claude-code-templates](https://github.com/davila7/claude-code-templates)** — CLI tool for configuring and monitoring Claude Code projects and workflows
  <sub>★ 30.9k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-code-templates@latest --agent development-team/frontend-developer --command testing/generate-tests --mcp development/github-integration --yes`</sub>
- **[serena](https://github.com/oraios/serena)** — Semantic retrieval and editing MCP server for coding agents -- code-aware search and navigation
  <sub>★ 29.7k · Python · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install -p 3.13 serena-agent`</sub>
- **[claude-hud](https://github.com/jarrodwatts/claude-hud)** — Plugin showing context usage, active tools, running agents, todo progress in a HUD overlay
  <sub>★ 28.1k · JavaScript · MIT · clone · pushed 2026-09-19 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/jarrodwatts/claude-hud`</sub>
- **[planning-with-files](https://github.com/OthmanAdi/planning-with-files)** — Manus-style persistent markdown planning skill for structured project management
  <sub>★ 27k · Shell · MIT · npx · pushed 2026-09-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g`</sub>
- **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** — 100+ specialized Claude Code subagents organized by domain
  <sub>★ 25.2k · Shell · MIT · clone · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/VoltAgent/awesome-claude-code-subagents.git`</sub>
- **[Hindsight](https://github.com/vectorize-io/hindsight)** — State-of-the-art long-term memory for AI agents by Vectorize. Biomimetic retain/recall/reflect with 4 parallel retrieval strategies. Self-hosted or cloud, MIT-licensed. Claude Code integration
  <sub>★ 24.6k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework)** — Config framework with specialized commands, cognitive personas, and dev methodologies
  <sub>★ 23.9k · Python · MIT · pipx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install superclaude`</sub>
- **[n8n-mcp](https://github.com/czlonkowski/n8n-mcp)** — MCP for Claude Code to build and manage n8n automation workflows
  <sub>★ 23k · TypeScript · MIT · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/czlonkowski/n8n-mcp.git`</sub>
- **[caliber](https://github.com/caliber-ai-org/ai-setup)** — CLI that fingerprints projects and generates AI agent configs (CLAUDE.md, skills, AGENTS.md). Scores quality, auto-refreshes, supports Claude Code + Cursor + Codex
  <sub>★ 1.3k · TypeScript · MIT · npx · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @rely-ai/caliber bootstrap`</sub>
- **[Agent Sessions](https://github.com/jazzyalex/agent-sessions)** — Native macOS app to search, browse, and resume Claude Code, Codex, Gemini CLI, OpenCode, and other local agent sessions, with Agent Cockpit live iTerm2 orchestration
  <sub>★ 871 · Swift · MIT · brew · pushed 2026-09-20 · macOS</sub>
  <sub>`brew install --cask jazzyalex/agent-sessions/agent-sessions`</sub>
- **[cog](https://github.com/marciopuga/cog)** — Cognitive architecture for Claude Code -- persistent memory, self-reflection, and foresight via plain-text conventions. Zero dependencies, just CLAUDE.md + markdown files
  <sub>★ 377 · MIT · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add marciopuga/cog-skills`</sub>
- **[Claudoscope](https://github.com/cordwainersmith/Claudoscope)** — Native macOS menu bar app for Claude Code session analytics. Token/cost tracking, full-text search, real-time secret detection, config health linting (44 rules). Reads local JSONL files, fully offline, zero telemetry. Swift/SwiftUI, Homebrew install
  <sub>★ 236 · Swift · MIT · brew · pushed 2026-09-17 · macOS</sub>
  <sub>`brew tap cordwainersmith/claudoscope`</sub>
- **[AIRIS MCP Gateway](https://github.com/agiletec-inc/airis-mcp-gateway)** — Docker-based MCP multiplexer that aggregates 60+ tools behind 7 meta-tools, reducing context token usage by 97%. One command to start, auto-enables servers on demand
  <sub>★ 172 · Python · MIT · script · pushed 2026-09-18 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/agiletec-inc/airis-mcp-gateway/main/install.sh | bash`</sub>
- **[GAAI Framework](https://github.com/digipulse-engineering/GAAI-framework)** — Drop-in governance layer (.gaai/ folder) -- backlog authorization, cross-session memory, decision tracking, QA gates, autonomous delivery daemon. Claude Code + Cursor + Codex CLI + Gemini CLI
  <sub>★ 161 · Shell · clone · pushed 2026-09-19 · macOS</sub>
  <sub>`git clone https://github.com/Fr-e-d/GAAI-framework.git`</sub>
- **[agenttrace](https://github.com/luoyuctl/agenttrace)** — TUI observability for Claude Code, Codex CLI, Gemini CLI, Aider, Cursor exports, and more. Tracks cost, tokens, tool failures, latency, anomalies, health, diffs, and CI gates from local session logs
  <sub>★ 135 · Rust · MIT · winget · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install --id Luoyuctl.AgentTrace --exact`</sub>
- **[cc-statistics](https://github.com/androidZzT/cc-statistics)** — Three-in-one Claude Code stats: CLI + Web + native macOS SwiftUI panel. Token costs, code changes by language, efficiency scoring, weekly reports. Supports Codex and Cursor too
  <sub>★ 117 · Swift · MIT · uv · pushed 2026-08-07 · macOS</sub>
  <sub>`uv tool install cc-statistics # or: pipx install cc-statistics`</sub>
- **[AgenTopology](https://github.com/agentopology/agentopology)** — Declarative language and CLI for multi-agent orchestration -- define agents, flows, gates, hooks, group chats in one .at file, scaffold to 7 platforms, interactive visualizer. Apache 2.0
  <sub>★ 103 · TypeScript · Apache-2.0 · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentopology`</sub>
- **[spartan-ai-toolkit](https://github.com/c0x12c/ai-toolkit)** — Engineering discipline layer for Claude Code -- 67 slash commands, 20 coding rules, 27 skills, 9 agents, quality gates between every step. 8 stack profiles (Go, Python, Java, Kotlin, React, etc.), agent memory across sessions. Install: npx @c0x12c/spartan-ai-toolkit@latest --local
  <sub>★ 101 · JavaScript · npx · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @c0x12c/ai-toolkit@latest --local`</sub>
- **[Code Insights](https://github.com/melagiri/code-insights)** — Local-first CLI and dashboard for analyzing AI coding sessions from Claude Code, Cursor, Codex CLI, Copilot CLI, and VS Code Copilot. SQLite-backed with terminal analytics, browser dashboard, and LLM-powered insights
  <sub>★ 76 · TypeScript · MIT · npm · pushed 2026-06-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @code-insights/cli`</sub>
- **[brood-box](https://github.com/stacklok/brood-box)** — Run AI coding agents (Claude Code, Codex, OpenCode) inside hardware-isolated microVMs with snapshot isolation, egress control, and MCP authorization
  <sub>★ 72 · Go · Apache-2.0 · source · pushed 2026-09-18 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/stacklok/brood-box.git`</sub>
- **[nylas/cli](https://github.com/nylas/cli)** — Email, calendar, and contacts CLI for Claude Code. Built-in MCP server with 16 tools across Gmail, Outlook, Exchange, Yahoo, iCloud, and IMAP. One-line install: nylas mcp install. Works with Claude Code, Cursor, Codex, and Windsurf. Docs: https://cli.nylas.com
  <sub>★ 71 · Go · MIT · go · pushed 2026-08-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/nylas/cli/cmd/nylas@latest`</sub>
- **[zclean](https://github.com/TheStack-ai/zclean)** — Kills orphaned processes left behind by Claude Code and Codex. Stops zombie node/python/esbuild from eating your RAM
  <sub>★ 67 · JavaScript · MIT · npm · pushed 2026-07-16 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install --global z-clean --foreground-scripts`</sub>
- **[healthcare-agents](https://github.com/ajhcs/healthcare-agents)** — 51 specialized healthcare administration agents with MHA-level expertise across 10 divisions -- revenue cycle, compliance, quality, clinical ops, payer relations, health IT, and more
  <sub>★ 51 · JavaScript · Apache-2.0 · npx · pushed 2026-07-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx --yes healthcare-agents install`</sub>
- **[LynxPrompt](https://github.com/GeiserX/LynxPrompt)** — Open-source platform for managing AI coding agent configs (CLAUDE.md, AGENTS.md, .cursorrules, copilot-instructions.md). Web marketplace, CLI, VS Code extension, self-hostable via Docker/Helm with federation support
  <sub>★ 47 · TypeScript · Apache-2.0 · choco · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`choco install lynxprompt`</sub>
- **[faf-cli](https://github.com/Wolfe-Jam/faf-cli)** — The package.json for AI context. IANA-registered .faf format — init, score, bi-sync with CLAUDE.md, export to AGENTS.md, GEMINI.md, .cursorrules. Built with Bun
  <sub>★ 41 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx faf-cli git https://github.com/facebook/react`</sub>
- **[openclaw-self-healing](https://github.com/Ramsbaby/openclaw-self-healing)** — 4-tier autonomous crash recovery for Claude Code and any service — 64% auto-resolved, LLM-agnostic (Claude/GPT-4/Gemini/Ollama), Prometheus metrics
  <sub>★ 40 · Shell · MIT · script · pushed 2026-07-25 · macOS</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Ramsbaby/openclaw-self-healing/main/install.sh | bash -s -- --dry-run`</sub>
- **[vibe-replay](https://github.com/tuo-lei/vibe-replay)** — Turn AI coding sessions into shareable, interactive HTML replays with animated playback, insights, and PR integration. Supports Claude Code and Cursor. Website
  <sub>★ 37 · TypeScript · MIT · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx vibe-replay`</sub>
- **[claude-starter-kit](https://github.com/awrshift/agent-memory-kit)** — Ready-to-use project structure with persistent memory, session continuity, hooks, and 3 bundled skills (Gemini, Brainstorm, Design)
  <sub>★ 34 · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/awrshift/claude-starter-kit.git`</sub>
- **[Solo Orchestrator](https://github.com/kraulerson/solo-orchestrator)** — Phase-gated development methodology for building production-quality applications with Claude Code. One-command setup generates CLAUDE.md, CI/CD pipelines, pre-commit hooks, and security tooling. Auto-discovers new platforms and languages from the filesystem. Includes enterprise governance, intake wizard, and adversarial evaluation prompts. Example project shows the complete artifact trail
  <sub>★ 30 · Shell · MIT · clone · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/kraulerson/solo-orchestrator.git`</sub>
- **[systemprompt-template](https://github.com/systempromptio/systemprompt-template)** — Governance infrastructure for Claude Code. Single compiled Rust binary that authenticates, authorises, rate-limits, logs, and attributes costs for every AI interaction before it reaches a tool or database. Self-hosted, air-gap capable, MCP + A2A compatible. BSL-1.1
  <sub>★ 29 · Rust · clone · pushed 2026-09-15 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/systempromptio/systemprompt-template`</sub>
- **[SpecLock](https://github.com/sgroy10/speclock)** — AI Constraint Engine for Claude Code — enforces CLAUDE.md, .cursorrules, AGENTS.md as pre-commit law. Catches euphemisms, temporal evasion, synonym substitution, compound violations. 51 MCP tools, 1,009 tests, on Official MCP Registry. npx speclock protect
  <sub>★ 25 · JavaScript · MIT · npx · pushed 2026-08-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx speclock@latest protect # reads existing AI rule files`</sub>
- **[Claude Code AWS Gateway](https://github.com/antkawam/claude-code-aws-gateway)** — Self-hosted API gateway that routes Claude Code through Amazon Bedrock with team API keys, budgets, rate limits, OIDC SSO, SCIM provisioning, and an admin portal for analytics
  <sub>★ 22 · Rust · MIT · script · pushed 2026-09-07 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://your-gateway/setup | sh # one command, fully configured`</sub>
- **[PRISM](https://github.com/jakeefr/prism)** — Session intelligence for Claude Code — reads ~/.claude/projects/ JSONL to surface token waste, CLAUDE.md adherence failures, and attention curve degradation. Generates diff-format CLAUDE.md recommendations. Read-only, zero telemetry
  <sub>★ 22 · Python · MIT · pipx · pushed 2026-06-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pipx install prism-cc`</sub>
- **[git-parsec](https://github.com/erishforG/git-parsec)** — Git worktree lifecycle manager — gives each AI agent an isolated workspace tied to issue tickets (Jira, GitHub Issues, GitLab). No index.lock conflicts in parallel workflows
  <sub>★ 16 · Rust · MIT · cargo · pushed 2026-09-19 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`cargo install git-parsec`</sub>
- **[Wiggum CLI](https://github.com/federiconeri/wiggum-cli)** — Open-source AI agent that scans codebases (80+ tech), generates specs through AI interviews, and runs autonomous Ralph loops via Claude Code or Codex. Agent mode ships GitHub issues end-to-end with priority-aware scheduling and auto-merge
  <sub>★ 14 · TypeScript · npm · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g wiggum-cli`</sub>
- **[codachi](https://github.com/vincent-k2026/codachi)** — Tamagotchi-style statusline pet that grows with context usage, shows cache hit rate and burn speed
  <sub>★ 14 · TypeScript · MIT · npm · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codachi`</sub>
- **[claude-skins](https://github.com/basicScandal/claude-skins)** — 9 custom visual themes for Claude Code — terminal colors, ASCII art banners, personality voices, status lines, and tool sounds. One-command install, pure bash engine
  <sub>★ 13 · Shell · MIT · clone · pushed 2026-05-11 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/basicScandal/claude-skins.git`</sub>
- **[agent-dotfiles](https://github.com/saqibameen/agent-dotfiles)** — Write AI coding rules once, sync to every agent. Supports Command Code, Claude Code, Cursor, Copilot, Codex, OpenCode
  <sub>★ 12 · TypeScript · MIT · npx · pushed 2026-03-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-dotfiles`</sub>
- **[openclaw-memorybox](https://github.com/Ramsbaby/openclaw-memorybox)** — Memory hygiene CLI for Claude Code — prevents context overflow crashes, 83% MEMORY.md size reduction, zero dependencies
  <sub>★ 10 · Shell · MIT · script · pushed 2026-07-25 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Ramsbaby/openclaw-memorybox/main/install.sh | bash`</sub>
- **[Cortex](https://github.com/SKULLFIRE07/cortex-memory)** — Persistent AI memory for coding assistants. Auto-captures decisions, patterns, and context across sessions. VSCode extension + CLI + MCP server. Free
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cortex-memory`</sub>
- **[cc-agents-md](https://github.com/GeiserX/cc-agents-md)** — CLI tool and SessionStart hook that loads AGENTS.md files into Claude Code sessions. Walks from CWD to git root, inlines small files, emits read instructions for large ones. Supports mid-session reload, context preservation, custom patterns, and stat-based caching. GPL-3.0
  <sub>★ 8 · JavaScript · GPL-3.0 · npx · pushed 2026-08-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cc-agents-md setup`</sub>
- **[claude-kit](https://github.com/luiseiman/dotforge)** — Configuration factory for Claude Code -- 13 composable stacks, 6 agents, audit scoring, practices pipeline. Bootstraps and maintains .claude/ across projects
  <sub>★ 8 · Shell · MIT · script · pushed 2026-06-29 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/luiseiman/dotforge/main/install.sh | bash`</sub>
- **[cc-hud](https://github.com/WaterTian/cc-hud)** — Compact single-line Claude Code statusline -- model, context usage (1/8-char progress bar), active subagents, 5h/7d rate-limit countdowns. Pure Node.js, zero deps, Windows-safe
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g cc-hud`</sub>
- **[gemini-claude-bridge](https://github.com/weijiafu14/gemini-claude-bridge)** — Gemini-to-Claude protocol converter for using Gemini models as Claude Code backend. Fixes 3 LiteLLM bugs
  <sub>★ 7 · Python · MIT · pip · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "gemini-claude-bridge[proxy]"`</sub>
- **[claude-memory-bridge](https://github.com/LewenW/claude-memory-bridge)** — Cross-project memory sharing via namespaces. Adds a shared layer between global and project-scoped memory so projects selectively share knowledge. MCP server, no database
  <sub>★ 6 · Python · MIT · clone · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LewenW/claude-memory-bridge.git`</sub>
- **[openclaw-self-evolving](https://github.com/Ramsbaby/openclaw-self-evolving)** — Weekly self-improvement pipeline — scans Claude Code logs, proposes CLAUDE.md/AGENTS.md rule changes, zero API cost
  <sub>★ 5 · Shell · MIT · script · pushed 2026-07-25 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Ramsbaby/openclaw-self-evolving/main/install.sh | bash`</sub>
- **[claude-token-lens](https://github.com/wassimbensalem/claude-token-lens)** — Real-time token attribution from local Claude Code JSONL sessions — see which tool, agent, MCP server, or skill is burning your quota. Live Ink dashboard, burn rate, ETA, 5h + 7-day tracking, zero telemetry. npm install -g claude-token-lens
  <sub>★ 4 · TypeScript · npm · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-token-lens`</sub>
- **[claude-overlay](https://github.com/mzmmoazam/claude-overlay)** — CLI for managing Claude Code project configs across custom providers (Databricks, Bedrock, OpenRouter, LiteLLM, Cloudflare). Overlay merge/remove, MCP web search setup, multi-provider switching, team config export/import
  <sub>★ 4 · Shell · MIT · brew · pushed 2026-09-04 · WSL2? · macOS · Linux?</sub>
  <sub>`brew tap mzmmoazam/claude-overlay`</sub>
- **[AgentsInFlow](https://github.com/hhammoud/AgentsInFlow)** — Self-hosted desktop workspace for governed AI development — run Claude Code, Codex, Cursor, OpenCode in isolated runtimes with persistent memory, ticket-driven orchestration, git worktrees per execution, browser bridge, 28 diagram types, session forking. Free early access, no sign-up. Electron (macOS/Windows)
  <sub>★ 4 · source · pushed 2026-04-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/hhammoud/AgentsInFlow.git`</sub>
- **[claude-code-kickstart](https://github.com/ypollak2/claude-code-kickstart)** — Opinionated starter kit — one command to install curated MCP servers, hooks, agents, and profiles. Includes auto-detect, 12 agents, 10 profiles, and 20+ shell commands
  <sub>★ 2 · Shell · MIT · clone · pushed 2026-03-26 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/ypollak2/claude-code-kickstart`</sub>
- **[claude-code-power-stack](https://github.com/bluzername/claude-code-power-stack)** — Ghost memory, conversation search, session naming, and Manus-style planning in a single install with cheat sheet PDF
  <sub>★ 2 · Shell · MIT · script · pushed 2026-09-17 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/bluzername/claude-code-power-stack/main/setup.sh | bash`</sub>
- **[clooks](https://github.com/mauribadnights/clooks)** — Persistent hook daemon that replaces per-invocation spawning -- 112x faster hooks with batching, dependency resolution, metrics
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @mauribadnights/clooks`</sub>
- **[claude-code-memory-guide](https://github.com/Acteq1391gp/claude-code-memory-guide)** — Zero-to-production memory setup: CLAUDE.md + MEMORY.md + MemPalace semantic search + session hooks + warm-model daemon + nightly Karpathy compile with free-LLM key rotation. Three guides — linear tutorial, memory format reference, automation reference. Runnable scripts, secrets-in-git precommit guard, end-to-end verification checklist. MIT
  <sub>★ 2 · Python · source · pushed 2026-05-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Acteq1391gp/claude-code-memory-guide.git`</sub>
- **[Claude Command Center](https://github.com/tuning-labs-oss/claude-command-center)** — Production-tested workspace template with session hooks, structured memory (4 types), multi-domain routing, daily task tracking, and interactive /setup onboarding. 6 domain templates, pre-commit safety, example skills
  <sub>★ 1 · Shell · MIT · clone · pushed 2026-03-23</sub>
  <sub>`git clone https://github.com/YOUR_USERNAME/claude-command-center.git`</sub>
- **[cc-tempo](https://github.com/O0000-code/cc-tempo)** — Claude Code statusline with wall-clock active work time, SubAgent speedup ratio, /clear-resilient PID timer, code-churn sparkline with trend arrow, and multi-instance detection. Bash + TypeScript, MIT
  <sub>★ 1 · Shell · MIT · clone · pushed 2026-05-07 · macOS?</sub>
  <sub>`git clone https://github.com/O0000-code/cc-tempo.git`</sub>
- **[llm-prices](https://github.com/benbencodes/llm-prices)** — CLI + Python library + MCP server to look up and compare LLM API costs across 167 models from 23 providers (OpenAI, Anthropic, Google, xAI, DeepSeek, Groq, and more). Ask Claude "what's the cheapest model for 10k input + 2k output?" before making API calls. Zero deps, no API key. pipx install git+https://github.com/benbencodes/llm-prices
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/benbencodes/llm-prices`</sub>
- **[cc-discipline](https://github.com/TechHU-GS/cc-discipline)** — Guardrails for Claude Code — shell hooks that physically block bad behavior (edit loops, skipped verification, destructive git), not just markdown rules. Streak-breaker hard-stops at 5 edits, pre-edit-guard enforces debugging process, 7 rules, 7 skills, 2 subagents. Interactive installer with append mode. bash ~/.cc-discipline/init.sh
  <sub>Shell · MIT · clone · pushed 2026-09-05</sub>
  <sub>`git clone https://github.com/TechHU-GS/cc-discipline.git`</sub>
- **[Global Chat](https://github.com/pumanitro/global-chat)** — Cross-protocol MCP server discovery -- search 18K+ servers across 6+ registries. Also supports A2A and agents.txt. Free agents.txt validator. npm: @global-chat/mcp-server
  <sub>unavailable</sub>
- **[expert-dispatch](https://github.com/simonsysun/expert-dispatch)** — Specialist Dispatch Pattern -- let cheap AI assistants delegate complex tasks to Claude Code CLI. Bash adapter with run/resume/review workflow, session continuity, per-project directories, and structured JSON output. Designed to be called by another AI system
  <sub>Shell · MIT · source · pushed 2026-04-01 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/simonsysun/expert-dispatch.git`</sub>
- **[claude-code-cheat-sheet](https://cc.storyfox.cz/)** — Complete one-page printable reference — all shortcuts, commands, CLI flags, MCP config, memory, skills, agents. Auto-updated daily from official docs. EN · ZH · JA · KO
  <sub>website</sub>
  <sub>`https://cc.storyfox.cz/`</sub>
- **[Not Human Search MCP](https://nothumansearch.ai/)** — Agent-first search engine for AI-accessible tools — 9,000+ sites indexed. Search by category, check agentic scores, verify MCP endpoints. MCP server at nothumansearch.ai/mcp, REST API at /api/v1/search. Go
  <sub>website</sub>
  <sub>`https://nothumansearch.ai/`</sub>
- **[AI Dev Jobs MCP](https://aidevboard.com/)** — AI/ML job board with 5,200+ roles across 260+ companies. Search jobs, filter by tags/salary/location, post listings programmatically. MCP server at aidevboard.com/mcp, REST API at /api/v1/jobs. Go
  <sub>website</sub>
  <sub>`https://aidevboard.com/`</sub>
- **[ToolRouter](https://toolrouter.com)** — Give Claude Code superpowers -- 150+ tools on demand with one account. Competitor research, video production, web search, image generation, security scanning, and more. claude mcp add toolrouter -- npx -y toolrouter-mcp
  <sub>website</sub>
  <sub>`https://toolrouter.com`</sub>
- **[TokRepo](https://tokrepo.com)** — Curated, community-ranked registry of 600+ agent skills, MCP servers, prompts, scripts, workflows, and configs. Cross-platform tagging (Claude Code, Codex CLI, Gemini CLI, Cursor), upvotes and usage data
  <sub>website</sub>
  <sub>`https://tokrepo.com`</sub>
- **[claudecode-harness](https://github.com/AdelElo13/claude-harness)** — One-command installer for production-grade Claude Code setup — 34 hooks (quality gates, auto-formatting, security monitoring, session memory), 36 agents, 77 rules across 13 languages, 27 MCP server templates. Zero deps, MIT. npx claudecode-harness
  <sub>unavailable</sub>
- **[claudex-setup](https://github.com/DnaFin/claudex)** — Audit and optimize any project for Claude Code — scores 0-100, auto-fixes configuration across 972 verified techniques. Zero deps. npx claudex-setup
  <sub>unavailable</sub>
- **[Claude Code Skills 中文精选集](https://claude-skills.bt199.com/)** — Chinese curated directory of 140+ Claude Code Skills, Agents, Plugins, and workflows for Chinese-speaking Claude Code users
  <sub>website</sub>
  <sub>`https://claude-skills.bt199.com/`</sub>
- **[agent-shadow-brain](https://github.com/theihtisham/agent-shadow-brain)** — AI-powered background code analysis agent for Claude Code that continuously monitors your codebase and provides intelligent suggestions. npm: @theihtisham/agent-shadow-brain
  <sub>unavailable</sub>
- **[omni-skills-forge](https://github.com/theihtisham/omni-skills-forge)** — Universal skill and slash-command manager for AI coding assistants. Create, share, and manage reusable skills across tools. npm: omni-skills-forge
  <sub>unavailable</sub>
- **[The Froject](https://www.thefroject.com)** — Free browser-based wizard that generates complete Claude Code workspaces for go-to-market teams (marketing, sales, customer success, HR, finance, operations). Downloads a ZIP including CLAUDE.md, context files, and pre-built skills, commands, agents, rules, hooks, and settings tailored to your role. Client-side, no backend. Plugin marketplace at thefroject-plugins
  <sub>website</sub>
  <sub>`https://www.thefroject.com`</sub>
- **[Bring Your AI](https://bringyour.ai/claude-code-to-codex)** — Local-first Claude Code to Codex migration path. Keeps harness files local, maps CLAUDE.md/AGENTS.md guidance and MCP config, and adds a Codex import checklist for hooks, secret refs, and non-equivalent behavior before Codex edits code
  <sub>website</sub>
  <sub>`https://bringyour.ai/claude-code-to-codex`</sub>
- **[Drevon](https://drevon.dev)** — Mac desktop workspace for GTM engineers. Run parallel AI agents powered by Claude Code, Codex, or Copilot to build target lists, score accounts, and pull prospect intel
  <sub>website</sub>
  <sub>`https://drevon.dev`</sub>
- **[voidly-mcp-server](https://github.com/voidly-ai/mcp-server)** — 116 tools for Claude Code covering censorship intelligence (19.6M OONI measurements, 126 countries), E2E encrypted agent-to-agent messaging, and agent payments. Install: claude mcp add voidly -- npx -y @voidly/mcp-server
  <sub>unavailable</sub>

## Companion Apps &amp; GUIs

- **[Ruflo](https://github.com/ruvnet/ruflo)** — Agent orchestration platform -- deploy multi-agent swarms, coordinate autonomous workflows, distributed swarm intelligence, RAG integration
  <sub>★ 73k · TypeScript · MIT · npm · pushed 2026-09-21 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g ruflo@latest`</sub>
- **[AionUI](https://github.com/iOfficeAI/AionUi)** — Free local open-source 24/7 Cowork app for Gemini CLI, Claude Code, Codex, and OpenCode
  <sub>★ 33k · TypeScript · Apache-2.0 · brew · pushed 2026-09-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install aionui`</sub>
- **[CloudCLI](https://github.com/siteboon/claudecodeui)** — Free open-source web/mobile UI for Claude Code, Cursor CLI, and Codex. Responsive design, integrated shell, file explorer, git explorer
  <sub>★ 13.8k · TypeScript · AGPL-3.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @cloudcli-ai/cloudcli`</sub>
- **[Companion](https://github.com/The-Vibe-Company/companion)** — Web &amp; mobile UI for Claude Code &amp; Codex. Launch parallel sessions, stream responses, approve tools, session recovery
  <sub>★ 2.4k · TypeScript · MIT · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm --env-file .env.production companions.build migrate`</sub>
- **[Claude-Code-Workflow](https://github.com/catlog22/Claude-Code-Workflow)** — JSON-driven multi-agent cadence-team framework with intelligent CLI orchestration (Gemini/Qwen/Codex)
  <sub>★ 2.1k · TypeScript · MIT · npm · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-code-workflow`</sub>
- **[chops](https://github.com/Shpigford/chops)** — macOS app to browse, edit, and manage skills across Claude Code, Cursor, Codex, Windsurf, and Amp
  <sub>★ 1.9k · Swift · clone · pushed 2026-08-23 · macOS</sub>
  <sub>`git clone https://github.com/Shpigford/chops.git`</sub>
- **[Bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Python orchestrator for 40+ CLI coding agents (Claude Code, Codex, Gemini CLI). Git worktree isolation, MCP server mode, HMAC audit trail. Plan-driven, deterministic. Apache-2.0
  <sub>★ 1.2k · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[crit](https://github.com/tomasz-tomczyk/crit)** — Local browser UI for inline code review of any file or agent output; integrates with Claude Code via plan-hook to review and approve plans before execution, outputs structured .crit.json for agent consumption
  <sub>★ 1.1k · Go · MIT · go · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/tomasz-tomczyk/crit/cmd/crit@latest`</sub>
- **[parallel-code](https://github.com/johannesjo/parallel-code)** — Run Claude Code, Codex, and Gemini side by side -- each in its own git worktree
  <sub>★ 1k · TypeScript · MIT · clone · pushed 2026-09-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/johannesjo/parallel-code.git`</sub>
- **[TokenEater](https://github.com/AThevon/TokenEater)** — Native macOS menu bar app for monitoring Claude AI usage limits and watching coding sessions live
  <sub>★ 502 · Swift · MIT · brew · pushed 2026-09-08 · macOS</sub>
  <sub>`brew tap AThevon/tokeneater`</sub>
- **[amux](https://github.com/mixpeek/amux)** — Open-source agent multiplexer for running dozens of parallel Claude Code sessions with web dashboard, self-healing watchdog, kanban board, agent-to-agent REST API, and mobile PWA. Single Python file
  <sub>★ 489 · Rust · pipx · pushed 2026-09-21 · WSL2 · macOS? · Linux</sub>
  <sub>`pipx install amux`</sub>
- **[The Claude Protocol](https://github.com/AvivK5498/The-Claude-Protocol)** — Enforcement layer wrapping Claude Code with 13 hooks -- blocks unsafe operations, enforces worktree isolation
  <sub>★ 348 · Python · MIT · npx · pushed 2026-02-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add AvivK5498/The-Claude-Protocol`</sub>
- **[Poirot](https://github.com/a7t-ai/poirot)** — macOS app for browsing Claude Code sessions, viewing diffs, and re-running commands. Reads local transcripts, runs offline
  <sub>★ 214 · Swift · MIT · brew · pushed 2026-08-28 · Win? · macOS</sub>
  <sub>`brew tap a7t-ai/poirot`</sub>
- **[clideck](https://github.com/rustykuntz/clideck)** — WhatsApp-like dashboard for managing AI coding agents (Claude Code, Codex, Gemini CLI, OpenCode) in one browser window. Live status, session resume, autopilot routing between agents, mobile remote
  <sub>★ 158 · JavaScript · MIT · npm · pushed 2026-09-18 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g clideck@2`</sub>
- **[ccswarm](https://github.com/nwiizo/ccswarm)** — Rust-based multi-agent orchestration with specialized agent pools, Git worktree isolation, 93% token reduction
  <sub>★ 152 · Rust · MIT · cargo · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`cargo install --path crates/ccswarm`</sub>
- **[Claw](https://github.com/jamesrochabrun/Claw)** — Native macOS app wrapping Claude Code SDK in Swift. Plan Mode, MCP Integration, Custom System Prompts
  <sub>★ 108 · Swift · MIT · source · pushed 2026-01-14 · macOS</sub>
  <sub>`git clone https://github.com/jamesrochabrun/Claw.git`</sub>
- **[OctoAlly](https://github.com/ai-genius-automations/octoally)** — AI coding session orchestration dashboard -- multi-agent hive-mind via RuFlo, Whisper voice dictation, tmux session persistence, built-in git source control, Electron desktop app
  <sub>★ 100 · TypeScript · npx · pushed 2026-07-11 · WSL2 · macOS · Linux</sub>
  <sub>`npx octoally@latest`</sub>
- **[WhereMyTokens](https://github.com/jeongwookie/WhereMyTokens)** — Windows system tray app for monitoring Claude Code token usage in real time. Per-session token counts, costs, context window progress, rate limit bars (5h/1w), activity heatmaps, and model breakdowns. Registers as a Claude Code statusLine plugin for live data without polling. Windows only
  <sub>★ 82 · TypeScript · MIT · source · pushed 2026-09-19 · Win · macOS?</sub>
  <sub>`git clone https://github.com/jeongwookie/WhereMyTokens.git`</sub>
- **[Untether](https://github.com/littlebearapps/untether)** — Telegram bridge for Claude Code (and 5 other AI agents). Send tasks by voice or text, stream progress, approve changes with inline buttons from your phone
  <sub>★ 68 · Python · MIT · uv · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install untether # recommended`</sub>
- **[Watchfire](https://github.com/watchfire-io/watchfire)** — Orchestration platform for AI coding agents (starting with Claude Code). Manages project context, breaks work into tasks, runs agents with full codebase awareness. Git worktree isolation, sandboxed execution, multiple agent modes (chat, task, autonomous). Go daemon + CLI/TUI + Electron GUI
  <sub>★ 61 · Go · Apache-2.0 · psh · pushed 2026-08-22 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/watchfire-io/watchfire/main/scripts/install.ps1 | iex`</sub>
- **[Asynkor](https://github.com/asynkor/asynkor)** — Coordination layer for AI agent teams — file leasing, shared memory, cross-machine sync. One MCP server for Claude Code, Cursor, Windsurf, JetBrains. Open source client, hosted infrastructure
  <sub>★ 50 · Go · Apache-2.0 · npx · pushed 2026-05-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @asynkor/mcp login`</sub>
- **[ClaudeCode Launchpad CLI](https://github.com/noambrand/Launchpad-CLI)** — Windows &amp; macOS 2-minute installer for Claude Code — auto-installs Node.js, Git &amp; Claude Code; two-line live status bar (model, context %, usage limits with reset timers); desktop shortcut with folder picker; right-click "Open with ClaudeCode Launchpad CLI" on any Windows folder; optional light-blue theme; Claude flags support
  <sub>★ 26 · HTML · source · pushed 2026-09-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/noambrand/kivun-terminal.git`</sub>
- **[Anima](https://github.com/btangonan/anima)** — Native macOS companion for Claude Code. Per-project ASCII familiars, nim token economy, cross-session watcher daemon. Tauri v2 + Rust, 4MB binary
  <sub>★ 18 · JavaScript · MIT · clone · pushed 2026-06-16 · macOS</sub>
  <sub>`git clone https://github.com/btangonan/anima`</sub>
- **[telegram-ai-bridge](https://github.com/AliceLJY/telegram-ai-bridge)** — Run N parallel Claude Code sessions from your phone via Telegram. War Room mode, per-bot personas, A2A multi-agent collaboration, tool approval from phone. Supports Claude Code, Codex, and Gemini backends
  <sub>★ 16 · JavaScript · MIT · clone · pushed 2026-09-08 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/AliceLJY/telegram-ai-bridge.git`</sub>
- **[tokburn](https://github.com/lsvishaal/tokburn)** — Local analytics dashboard for Claude Code -- calculates API-equivalent costs, detects waste patterns (repeated reads, floundering, cost outliers), serves web UI + REST API. Zero network calls, zero accounts, zero telemetry. uvx tokburn serve
  <sub>★ 10 · Python · MIT · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx tokburn serve`</sub>
- **[cctally](https://github.com/omrikais/cctally)** — Track Claude Code subscription usage as a weekly $-per-1% trend. Local web dashboard, terminal UI, forecasts, threshold alerts. Apache-2.0, zero telemetry
  <sub>★ 9 · Python · Apache-2.0 · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cctally`</sub>
- **[ToutKit](https://github.com/NextProb/nextprob)** — Desktop notebook for AI CLIs (Claude Code, Codex, Gemini). Pairs a sidebar of notes with a built-in terminal and an in-app webview that renders whatever the AI writes — each note is a self-contained folder with its own SQLite, key/value store, attached files, and scripts, so a note can grow from a static page into a sortable table, dashboard, or research tool. Local-first, AGPL-3.0
  <sub>★ 9 · JavaScript · AGPL-3.0 · clone · pushed 2026-09-14 · Win? · macOS</sub>
  <sub>`git clone https://github.com/nextprob/nextprob.git`</sub>
- **[KANBAII](https://github.com/martinmsaavedra/kanbaii)** — AI-native kanban board for Claude Code — plan visually, track progress, let AI execute. Sequential engine (Ralph), parallel multi-agent (Teams), cost tracking, real-time dashboard. npx kanbaii start
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g kanbaii`</sub>
- **[cc-token-status](https://github.com/jayson-jia-dev/cc-token)** — macOS menu bar dashboard for Claude Code. Shows live plan limits (5h/7d), costs, tokens, trends, model breakdown, user level system, and multi-machine iCloud sync. 5 languages, dark/light mode. Single Python file, auto-updates
  <sub>★ 5 · Python · MIT · script · pushed 2026-07-24 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/jayson-jia-dev/cc-token/main/install.sh | bash`</sub>
- **[docker-claude-code](https://github.com/gw0/docker-claude-code)** — Run Claude Code in an isolated Docker container with multi-profile support, security hardening, best-practice defaults, a set of pre-installed plugin/skill bundles and remote dev support. Drop-in replacement for claude — a simple shell alias is all it takes
  <sub>★ 4 · Dockerfile · docker · pushed 2026-09-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -it --rm \`</sub>
- **[skill-builder](https://github.com/Scottpedia0/skill-builder)** — Analyzes your activity (shell history, git, browser, Claude threads) and generates working skills via LLM. 15 built-in skills + unlimited AI-generated. React UI with MCP server builder
  <sub>★ 3 · JavaScript · clone · pushed 2026-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Scottpedia0/skill-builder.git`</sub>
- **[claude-workspace-snapshot](https://github.com/REMvisual/terminal-workspace-snapshot)** — Snapshot and restore live Claude Code sessions as named, color-coded Windows Terminal tabs. Detects running sessions via process inspection and .jsonl file activity. Windows only
  <sub>★ 3 · PowerShell · MIT · psh · pushed 2026-09-07 · Win · WSL2</sub>
  <sub>`irm https://raw.githubusercontent.com/REMvisual/terminal-workspace-snapshot/master/install.ps1 | iex`</sub>
- **[aby-claude-watcher](https://github.com/aby-agency/aby-claude-watcher)** — Real-time macOS dashboard for Claude Code sessions. Five color-coded states (thinking, running, waiting, error, completed), per-session notifications, one-click focus terminal across iTerm2/Terminal/Warp/VSCode/Cursor/Ghostty/kitty/WezTerm/Hyper. Bilingual FR/EN, menu-bar tray, MIT licensed. Apple Silicon + Intel builds
  <sub>★ 2 · JavaScript · MIT · clone · pushed 2026-09-17 · macOS</sub>
  <sub>`git clone https://github.com/aby-agency/aby-claude-watcher.git`</sub>
- **[Claude Session Visualizer](https://github.com/anaypaul/claude-session-visualizer)** — Live visualization dashboard for Claude Code sessions with execution trees, token cost tracking, thinking trace exploration, and error debugging
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anaypaul/claude-session-visualizer.git`</sub>
- **[ctrl](https://ctrl.bulletproof.sh)** — Pixel-art office that visualizes AI coding agents (Claude Code, Codex, Gemini) working in real time. Standalone web app + daemon, relay sharing for remote access, multi-agent support
  <sub>website</sub>
  <sub>`https://ctrl.bulletproof.sh`</sub>
- **[CCHub](https://github.com/Moresl/cchub)** — Tauri 2 desktop app for managing Claude Code ecosystem: MCP marketplace, config profiles, skills, workflows, hooks, security audit, autopilot. Cross-platform (~20MB)
  <sub>unavailable</sub>
- **[Onepilot](https://onepilotapp.com)** — iOS app for running Claude Code, Codex, and other coding agents on remote servers via SSH from your phone. Full terminal emulator with SwiftTerm, agent session management, mobile access to dev machines
  <sub>website</sub>
  <sub>`https://onepilotapp.com`</sub>
- **[cc-config-viewer](https://github.com/kuri-sun/cc-config-viewer)** — Browser UI for Claude Code config. View and edit settings, rules, commands, agents, skills, and plugins across all four scopes (Managed / User / Project / Local), with a "Resolved" view of the merged effective settings
  <sub>unavailable</sub>
- **[claude-code-notifier](https://github.com/saiso/claude-code-notifier)** — Native macOS notifier for Claude Code. Swift + UserNotifications, custom Heroicons-derived icon (SF Symbols–free), click-through to your IDE (VS Code, Cursor, Windsurf, JetBrains, iTerm2, Terminal) via bundle ID swap, per-event sound labels, hardened inputs (allowlists, length caps, control-character stripping). Universal binary (arm64 + x86_64), macOS 12+, MIT
  <sub>Swift · MIT · brew · pushed 2026-04-28 · WSL2 · macOS · Linux</sub>
  <sub>`brew install saiso/tap/claude-code-notifier`</sub>

## Hook Scripts

- **[smart-approve.py](https://github.com/liberzon/claude-hooks)** — Decompose compound bash commands (&amp;&amp;, ||, ;, |, $()) into sub-commands and check each against allow/deny patterns
  <sub>★ 17 · Python · MIT · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/liberzon/claude-hooks.git`</sub>

## Related SDKs

- **[claude-code-hooks](https://github.com/KashyapV375/claude-hook-kit)** — TypeScript SDK with defineHook(), typed event payloads for all 5 hook events, response builders, and unit-testable .handle() method. Zero dependencies
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Payshak/claude-code-hooks.git`</sub>
- **[EchoCoding](https://github.com/launsion-boop/EchoCoding)** — Audio layer for coding agents with hook-triggered SFX, ambient soundscape, and optional cloud TTS/ASR voice interaction. Works with Claude Code hooks and also supports Cursor/Windsurf, Codex CLI, and Gemini CLI
  <sub>unavailable</sub>

## MCP Configs

- **[Recommended](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/recommended.json)** — 14 essential servers for general development
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/recommended.json`</sub>
- **[Full Stack](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/fullstack.json)** — Filesystem, GitHub, Postgres, Redis, Puppeteer
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/fullstack.json`</sub>
- **[Kubernetes](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/kubernetes.json)** — kubectl-mcp-server, Docker, GitHub
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/kubernetes.json`</sub>
- **[Data Science](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/data-science.json)** — Jupyter, SQLite, PostgreSQL, Filesystem
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/data-science.json`</sub>
- **[Frontend](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/frontend.json)** — Puppeteer, Figma, Storybook
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/frontend.json`</sub>
- **[Crypto / DeFi](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/crypto-defi.json)** — defi-mcp, Filesystem, Fetch, Memory
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/crypto-defi.json`</sub>
- **[DevOps](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/devops.json)** — AWS, Docker, GitHub, Terraform, Sentry
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/devops.json`</sub>
- **[Research](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/research.json)** — BGPT scientific papers, Brave Search, Fetch, Memory, Filesystem
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/research.json`</sub>
- **[Observability](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/observability.json)** — Iris eval &amp; observability for agent tracing, quality evaluation, and cost tracking
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/observability.json`</sub>
- **[Security](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/security.json)** — Ghidra reverse engineering, Snyk vulnerability scanning
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/security.json`</sub>
- **[Design](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/design.json)** — Figma design context, Blender 3D automation
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/design.json`</sub>
- **[Workflow Automation](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/workflow-automation.json)** — n8n workflow builder, Pipedream integration
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/workflow-automation.json`</sub>
- **[Mobile](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/mobile.json)** — Android ADB automation, Xcode build tools
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/mobile.json`</sub>
- **[Finance](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/finance.json)** — Helium news/markets/options, Chart Library pattern intelligence, Fetch, Memory
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/finance.json`</sub>
- **[E-Commerce](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/ecommerce.json)** — BuyWhere product search, price comparison, deal discovery across 1M+ products
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/ecommerce.json`</sub>
- **[LLM Cost](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/mcp-configs/llm-cost.json)** — llm-prices: look up and compare API costs across 167 models from 23 providers before making calls
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/mcp-configs/llm-cost.json`</sub>

## Templates

- **[claude-code-blueprint](https://github.com/faizkhairi/claude-code-blueprint)** — Battle-tested reference architecture for Claude Code power users. Specialized agents with model hhtiering, natural-language skills, lifecycle hooks, path-scoped rules, starter presets, benchmarks, battle stories, and cross-tool mapping. Zero dependencies, MIT licensed
  <sub>★ 71 · Shell · MIT · source · pushed 2026-08-12</sub>
  <sub>`git clone https://github.com/faizkhairi/claude-code-blueprint.git`</sub>
- **[idea-factory](https://github.com/gguloadoong/idea-factory)** — Template-install AI company factory for Claude Code. One-line business idea → autonomous MVP via a 7-agent startup team (PM / Developer / Designer / Architect / Critic / Code-Reviewer / QA). 4-reviewer isolated-worktree gate, Quality Ratchet, MVP-First pipeline. See the installation guide for the bash install.sh flow (plugin-marketplace listing is in progress). MIT licensed
  <sub>★ 2 · Shell · MIT · script · pushed 2026-04-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/gguloadoong/idea-factory/main/install.sh | bash`</sub>
- **[TemplateClaw](https://github.com/jeromwolf/templateclaw)** — Developer template hub and project scaffolding tool packaged as a Claude Code Plugin. 32 production-ready templates across 6 categories (Landing Pages, Dashboards, UI Components, Dev Methodology, Project Setup, Refactoring). 7 slash commands including /templateclaw, /templateclaw-landing, /templateclaw-dashboard, /templateclaw-ui. Compatible with Claude Code, Codex, Gemini CLI, and Cursor. MIT lic
  <sub>★ 2 · HTML · MIT · script · pushed 2026-03-29 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://jeromwolf.github.io/templateclaw/install.sh | bash`</sub>
- **[The CLAUDE.md Bible](https://echochime3.gumroad.com/l/claudemd-bible)** — 25 stack-specific CLAUDE.md configs covering React, Next.js, FastAPI, Django, Svelte, Chrome Extensions, CLI tools, MCP servers, and more. Each config is 80-150 lines of tested rules for the specific patterns and pitfalls of each stack, plus a masterclass guide
  <sub>website</sub>
  <sub>`https://echochime3.gumroad.com/l/claudemd-bible`</sub>
- **[Minimal](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/minimal.md)** — Small projects, scripts, quick prototypes
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/minimal.md`</sub>
- **[Standard](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/standard.md)** — Most projects -- covers preferences, rules, workflows
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/standard.md`</sub>
- **[Comprehensive](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/comprehensive.md)** — Large codebases with detailed conventions
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/comprehensive.md`</sub>
- **[Monorepo](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/monorepo.md)** — Turborepo/Nx monorepo with multiple packages
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/monorepo.md`</sub>
- **[Enterprise](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/enterprise.md)** — Large teams with compliance and SSO
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/enterprise.md`</sub>
- **[Python Project](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/python-project.md)** — FastAPI/Django Python projects
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/python-project.md`</sub>
- **[Fullstack App](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/templates/claude-md/fullstack-app.md)** — Next.js + API fullstack applications
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/templates/claude-md/fullstack-app.md`</sub>

## Rules

- **[Coding Style](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/coding-style.md)** — Naming conventions, file organization, import ordering
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/coding-style.md`</sub>
- **[Git Workflow](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/git-workflow.md)** — Branching, commit format, PR process
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/git-workflow.md`</sub>
- **[Testing](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/testing.md)** — Test structure, coverage targets, mocking guidelines
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/testing.md`</sub>
- **[Security](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/security.md)** — Input validation, secrets, parameterized queries
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/security.md`</sub>
- **[Performance](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/performance.md)** — Lazy loading, caching, bundle optimization
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/performance.md`</sub>
- **[Documentation](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/documentation.md)** — JSDoc for public APIs, inline comments policy
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/documentation.md`</sub>
- **[Error Handling](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/error-handling.md)** — Explicit handling, typed errors, no empty catch
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/error-handling.md`</sub>
- **[Agents](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/agents.md)** — Agent design patterns, handoff protocols
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/agents.md`</sub>
- **[API Design](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/api-design.md)** — REST conventions, status codes, versioning
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/api-design.md`</sub>
- **[Accessibility](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/accessibility.md)** — WCAG 2.2, ARIA, semantic HTML
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/accessibility.md`</sub>
- **[Database](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/database.md)** — Query patterns, migrations, N+1 prevention
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/database.md`</sub>
- **[Dependency Management](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/dependency-management.md)** — Version pinning, audit, update policies
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/dependency-management.md`</sub>
- **[Code Review](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/code-review.md)** — Review checklist, approval criteria
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/code-review.md`</sub>
- **[Monitoring](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/monitoring.md)** — Logging standards, metrics, alerting
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/monitoring.md`</sub>
- **[Naming](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/rules/naming.md)** — Naming conventions per language
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/rules/naming.md`</sub>

## Contexts

- **[Development](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/contexts/dev.md)** — Iterate fast, follow patterns, test alongside code
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/contexts/dev.md`</sub>
- **[Code Review](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/contexts/review.md)** — Check logic, security, edge cases
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/contexts/review.md`</sub>
- **[Research](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/contexts/research.md)** — Evaluate tools, compare alternatives, document findings
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/contexts/research.md`</sub>
- **[Debug](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/contexts/debug.md)** — Reproduce, hypothesize, fix root cause, regression test
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/contexts/debug.md`</sub>
- **[Deploy](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/contexts/deploy.md)** — Pre-deploy checklist, staging-first, rollback criteria
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/contexts/deploy.md`</sub>

## Related Awesome Lists

- **[awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)** — LLM-powered applications and multi-agent systems
  <sub>★ 139.3k · Python · Apache-2.0 · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/project-graveyard`</sub>
- **[awesome-claude-skills (Composio)](https://github.com/ComposioHQ/awesome-claude-skills)** — 30 curated skills + 832 SaaS automation templates via Composio. Strong on document processing, creative, and business skills
  <sub>★ 75.4k · Python · npx · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add chrome-relay`</sub>
- **[awesome-claude-code (hesreallyhim)](https://github.com/hesreallyhim/awesome-claude-code)** — Skills, hooks, slash-commands, and orchestrators
  <sub>★ 54.4k · Python · source · pushed 2026-09-21 · macOS</sub>
  <sub>`git clone https://github.com/hesreallyhim/awesome-claude-code.git`</sub>
- **[antigravity-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)** — 1,326+ installable agentic skills with CLI
  <sub>★ 46.7k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentic-awesome-skills --antigravity --skills brainstorming,systematic-debugging --dry-run`</sub>
- **[awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)** — Open-source and closed-source AI agents
  <sub>★ 30.1k · source · pushed 2026-08-21 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/e2b-dev/awesome-ai-agents.git`</sub>
- **[awesome-mcp-servers](https://github.com/appcypher/awesome-mcp-servers)** — Curated MCP servers across 30 categories
  <sub>★ 5.8k · source · pushed 2026-05-06 · macOS</sub>
  <sub>`git clone https://github.com/appcypher/awesome-mcp-servers.git`</sub>
- **[awesome-claude-design](https://github.com/rohitg00/awesome-claude-design)** — DESIGN.md files grouped by aesthetic family (editorial, terminal, warm, data-dense, cinematic, playful, glass, brutalist, indie) + remix recipes + prompt packs for Claude Design (Anthropic Labs)
  <sub>★ 1.1k · MIT · npx · pushed 2026-04-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skillkit install composio/canvas-design`</sub>
- **[Awesome AI Startups](https://github.com/nowork-studio/awesome-ai-startups)** — Curated directory of ~440 indie-built AI products (bootstrapped, pre-seed, angel-funded) across 18 categories — AI agents, coding tools, marketing, audio/voice, image/design, video, and more
  <sub>★ 84 · CC0-1.0 · source · pushed 2026-09-20 · macOS</sub>
  <sub>`git clone https://github.com/nowork-studio/awesome-ai-startups.git`</sub>
- **[ai-skill](https://github.com/anomalyco/ai-skill)** — AI skill discovery and management system - helps users find, evaluate, install and manage agent skills, tools, plugins and extensions
  <sub>unavailable</sub>

## Examples

- **[Session Workflow](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/examples/session-workflow.md)** — End-to-end productive development session
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/examples/session-workflow.md`</sub>
- **[Multi-Agent Pipeline](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/examples/multi-agent-pipeline.md)** — Chaining agents for a Stripe billing feature
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/examples/multi-agent-pipeline.md`</sub>
- **[Project Setup](https://github.com/rohitg00/awesome-claude-code-toolkit/tree/HEAD/examples/project-setup.md)** — Setting up a new project with the full toolkit
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/rohitg00/awesome-claude-code-toolkit.git && cd awesome-claude-code-toolkit/examples/project-setup.md`</sub>

## Resources

- **[Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code)** — Official Anthropic documentation for Claude Code
  <sub>website</sub>
  <sub>`https://docs.anthropic.com/en/docs/claude-code`</sub>
- **[Context Engineering Guide](https://www.anthropic.com/research/long-running-Claude)** — Anthropic's guide to long-running Claude Code sessions and scientific computing
  <sub>website</sub>
  <sub>`https://www.anthropic.com/research/long-running-Claude`</sub>
- **[Auto Mode Engineering](https://www.anthropic.com/engineering/claude-code-auto-mode)** — How Auto Mode's two-layer safety system works under the hood
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/claude-code-auto-mode`</sub>
- **[Claude Code Guide](https://claudecodeguide.dev)** — Beginner-friendly guide from first install to daily operating system, zero jargon (GitHub)
  <sub>website</sub>
  <sub>`https://claudecodeguide.dev`</sub>
- **[Skills vs MCP vs Plugins](https://www.morphllm.com/context-engineering)** — When to use which extension mechanism in Claude Code
  <sub>website</sub>
  <sub>`https://www.morphllm.com/context-engineering`</sub>
- **[Context Engineering 101](https://newsletter.victordibia.com/p/context-engineering-101-how-agents)** — Three core strategies: compaction, isolation, agentic memory
  <sub>website</sub>
  <sub>`https://newsletter.victordibia.com/p/context-engineering-101-how-agents`</sub>
- **[Agent Teams Explained](https://www.turingcollege.com/blog/claude-agent-teams-explained)** — How multiple Claude Code instances coordinate as an AI engineering team
  <sub>website</sub>
  <sub>`https://www.turingcollege.com/blog/claude-agent-teams-explained`</sub>
- **[84 Best Practices](https://discuss.huggingface.co/t/10-essential-claude-code-best-practices-you-need-to-know/174731)** — Community-compiled Claude Code best practices from Hugging Face
  <sub>website</sub>
  <sub>`https://discuss.huggingface.co/t/10-essential-claude-code-best-practices-you-need-to-know/174731`</sub>
- **[Computer Use from CLI](https://code.claude.com/docs/en/computer-use)** — Let Claude control your desktop — open apps, click, type, screenshot. macOS, Pro/Max, v2.1.85+. Per-app approval, tiered access, Esc abort
  <sub>website</sub>
  <sub>`https://code.claude.com/docs/en/computer-use`</sub>
- **[Dispatch &amp; Remote Control](https://claude.com/blog/dispatch-and-computer-use)** — Run Claude Code from phone/web, schedule recurring tasks, remote session control
  <sub>website</sub>
  <sub>`https://claude.com/blog/dispatch-and-computer-use`</sub>
- **[Multi-Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)** — Addy Osmani's survey of multi-agent coding patterns
  <sub>website</sub>
  <sub>`https://addyosmani.com/blog/code-agent-orchestra/`</sub>


---

Snapshot 2026-09-21. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
