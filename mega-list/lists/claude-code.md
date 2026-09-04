# Claude Code

Commands, hooks, status lines and tooling for Claude Code.

Curated by **[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

153 entries · 140 distinct repos · 18 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/multica-ai/andrej-karpathy-skills"><img src="https://opengraph.githubassets.com/1/multica-ai/andrej-karpathy-skills" width="260"></a> | <a href="https://github.com/anthropics/skills"><img src="https://opengraph.githubassets.com/1/anthropics/skills" width="260"></a> | <a href="https://github.com/shareAI-lab/learn-claude-code"><img src="https://opengraph.githubassets.com/1/shareAI-lab/learn-claude-code" width="260"></a> |
| **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)**<br>★ 209.8k | **[Agent Skills](https://github.com/anthropics/skills)**<br>★ 173.5k | **[Learn Claude Code](https://github.com/shareAI-lab/learn-claude-code)**<br>★ 76k |
| <a href="https://github.com/luongnv89/claude-howto"><img src="https://opengraph.githubassets.com/1/luongnv89/claude-howto" width="260"></a> | <a href="https://github.com/anthropics/claude-plugins-official"><img src="https://opengraph.githubassets.com/1/anthropics/claude-plugins-official" width="260"></a> | <a href="https://github.com/anthropics/claude-code-action"><img src="https://opengraph.githubassets.com/1/anthropics/claude-code-action" width="260"></a> |
| **[claude-howto](https://github.com/luongnv89/claude-howto)**<br>★ 41.3k | **[Official Plugin Directory](https://github.com/anthropics/claude-plugins-official)**<br>★ 35.9k | **[Claude Code GitHub Action](https://github.com/anthropics/claude-code-action)**<br>★ 8.8k |

## Contents

- [Start Here](#start-here) (10)
- [From Anthropic](#from-anthropic) (11)
- [Observability &amp; Monitoring](#observability--monitoring) (24)
- [Documentation, Knowledge &amp; Learning](#documentation-knowledge--learning) (20)
- [Research &amp; Scientific Inquiry](#research--scientific-inquiry) (2)
- [Security](#security) (15)
- [Agent Orchestration](#agent-orchestration) (11)
- [Memory &amp; Context Persistence](#memory--context-persistence) (11)
- [Alternative Clients](#alternative-clients) (7)
- [Infrastructure &amp; DevOps](#infrastructure--devops) (2)
- [Providers, Runtime &amp; Integration Infrastructure](#providers-runtime--integration-infrastructure) (6)
- [Skills](#skills) (5)
- [Design &amp; UI/UX](#design--uiux) (6)
- [Writing &amp; Prose Quality](#writing--prose-quality) (2)
- [Creative Media](#creative-media) (4)
- [Linting](#linting) (6)
- [Status Lines](#status-lines) (5)
- [Remote Control, Notifications &amp; Voice I/O](#remote-control-notifications--voice-io) (6)

## Start Here

- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** — by multica-ai - A drop-in CLAUDE.md distilling four behavioral guidelines for LLM-assisted coding into Claude Code — a low-friction quick win. Karpathy-inspired, derived from Andrej Karpathy's public notes on LLM coding pitfalls and authored by multica-ai
  <sub>★ 209.8k · source · pushed 2026-04-20</sub>
  <sub>`git clone https://github.com/multica-ai/andrej-karpathy-skills.git`</sub>
- **[Learn Claude Code](https://github.com/shareAI-lab/learn-claude-code)** — by shareAI-lab - A really interesting analysis of how coding agents like Claude Code are designed. It attempts to break an agent down into its fundamental parts and reconstruct it with minimal code. Great learning resource. Final product is a rudimentary agent with skills, sub-agents, and a todo-list in roughly a few hundred lines of Python
  <sub>★ 76k · Python · MIT · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @shareai-lab/kode`</sub>
- **[claude-howto](https://github.com/luongnv89/claude-howto)** — by luongnv89 - A structured, chapter-based getting-started guide for Claude Code with a self-assessment quiz and a ten-module progressive learning path — slash commands, memory, skills, subagents, MCP, hooks, plugins, and checkpoints — with visual diagrams and copy-paste templates
  <sub>★ 41.3k · Python · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/luongnv89/claude-howto.git`</sub>
- **[Claude Code Guide](https://github.com/zebbern/claude-code-guide)** — by zebbern - A current single-page reference for Claude Code: install, environment variables, slash commands, MCP, hooks, and subagents, kept in sync with the official changelog
  <sub>★ 4.6k · Python · MIT · source · pushed 2026-09-03 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/zebbern/claude-code-guide.git`</sub>
- **[Claude Code: Everything You Need to Know](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)** — by wesammustafa - A conceptual, mental-models-first primer that explains what Claude Code is and how its agentic loop works, then layers setup, prompt-engineering workflows, skills, hooks, MCP, subagents, and agent teams, with an experience-tiered path for newcomers
  <sub>★ 2.9k · Python · MIT · source · pushed 2026-07-28 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know.git`</sub>
- **[explore-claude-code](https://github.com/LukeRenton/explore-claude-code)** — by Luke Renton - An interactive click-through of an annotated Claude Code project where every file and folder — CLAUDE.md, settings.json, rules, commands, skills, agents, hooks, plugins, and .mcp.json — is a real, explained concept, teaching the tool's surface area by orientation rather than prose
  <sub>★ 309 · JavaScript · MIT · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LukeRenton/explore-claude-code.git`</sub>
- **[A Field Guide to Claude Fable 5](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)** — by Thariq Shihipar, Anthropic - Really solid, insightful guidance on working/thinking with Claude Fable, and with AI in general. Very well written. Hints of Rumsfeld epistemology, but otherwise it's a great piece
  <sub>website</sub>
  <sub>`https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns`</sub>
- **[Beyond the Prompt: Claude Code](https://arps18.github.io/posts/claude-code-mastery)** — by Arpan Patel - This has what you need. Remarkably clear, information-dense, it's Claude Code: the good parts, for beginners, advanced users, pets, anybody
  <sub>website</sub>
  <sub>`https://arps18.github.io/posts/claude-code-mastery`</sub>
- **[Claude Code Hooks: Complete Guide](https://hidekazu-konishi.com/entry/claude_code_hooks_complete_guide.html)** — by Hidekazu Konishi - A thorough walkthrough of every hook event, when each fires, the two return channels, common anti-patterns, and copy-ready settings.json examples
  <sub>website</sub>
  <sub>`https://hidekazu-konishi.com/entry/claude_code_hooks_complete_guide.html`</sub>
- **[Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)** — by HumanLayer - An essay on CLAUDE.md craft: instruction-budget reasoning, progressive disclosure, and the test of whether Claude would err without a given line
  <sub>website</sub>
  <sub>`https://www.humanlayer.dev/blog/writing-a-good-claude-md`</sub>

## From Anthropic

- **[Agent Skills](https://github.com/anthropics/skills)** — by Anthropic - Anthropic's official repository for Agent Skills — the SKILL.md format, a skill template, and example skills, the same format Claude Code loads natively
  <sub>★ 173.5k · Python · source · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/skills.git`</sub>
- **[Official Plugin Directory](https://github.com/anthropics/claude-plugins-official)** — by Anthropic - Anthropic's official, curated directory of high-quality Claude Code plugins, installable from within Claude Code
  <sub>★ 35.9k · Python · Apache-2.0 · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/claude-plugins-official.git`</sub>
- **[Claude Code GitHub Action](https://github.com/anthropics/claude-code-action)** — by Anthropic - The official GitHub Action for running Claude Code in CI: mention @claude in issues and pull requests to delegate code changes, reviews, and fixes
  <sub>★ 8.8k · TypeScript · MIT · gh-action · pushed 2026-09-01</sub>
  <sub>`uses: anthropics/claude-code-action@main # in .github/workflows/*.yml`</sub>
- **[Claude Code Security Review](https://github.com/anthropics/claude-code-security-review)** — by Anthropic - An official AI-powered security-review GitHub Action that uses Claude to analyze pull-request diffs for vulnerabilities
  <sub>★ 6.2k · Python · MIT · gh-action · pushed 2026-02-11</sub>
  <sub>`uses: anthropics/claude-code-security-review@main # in .github/workflows/*.yml`</sub>
- **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)** — by Anthropic - Anthropic's foundational taxonomy of agent patterns — prompt chaining, routing, orchestrator-workers, and evaluator-optimizer — and when to use each
  <sub>website</sub>
  <sub>`https://www.anthropic.com/research/building-effective-agents`</sub>
- **[Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)** — by Anthropic - Anthropic's canonical guide to working effectively with Claude Code: the agentic-loop mental model, CLAUDE.md guidance, and workflow patterns
  <sub>website</sub>
  <sub>`https://code.claude.com/docs/en/best-practices`</sub>
- **[Claude Code Cheatsheet](https://support.claude.com/en/articles/14553413-claude-code-cheatsheet)** — by Anthropic - Anthropic's official Claude Code cheatsheet — a quick reference for the core vocabulary (session, context window, CLAUDE.md), built-in slash commands, and keyboard shortcuts
  <sub>website</sub>
  <sub>`https://support.claude.com/en/articles/14553413-claude-code-cheatsheet`</sub>
- **[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — by Anthropic - Anthropic's guide to curating the context window — compaction, just-in-time retrieval, and note-taking — the discipline underlying effective long-horizon agent use
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents`</sub>
- **[How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)** — by Anthropic - The official conceptual explainer of Claude Code's agentic loop, tools, and context window, and how skills, hooks, and subagents layer on top
  <sub>website</sub>
  <sub>`https://code.claude.com/docs/en/how-claude-code-works`</sub>
- **[How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)** — by Anthropic - A practical account of orchestrator and subagent coordination, prompt design, and evaluation that maps directly to Claude Code's subagents and agent teams
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/multi-agent-research-system`</sub>
- **[Steering Claude Code: Skills, Hooks, Rules, Subagents and More](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)** — by Anthropic - A framework for choosing which extension mechanism to reach for, organized around deterministic-versus-probabilistic control and context isolation
  <sub>website</sub>
  <sub>`https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more`</sub>

## Observability &amp; Monitoring

- **[ccusage](https://github.com/ccusage/ccusage)** — by ryoppippi - A zero-install CLI (npx ccusage) that analyzes Claude Code token usage and cost from local JSONL logs — daily, monthly, per-session, and 5-hour-block breakdowns, a live monitoring mode, and per-model cost estimates. Runs entirely locally, with JSON output for scripting
  <sub>★ 18.3k · Rust · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ccusage/ccusage.git`</sub>
- **[Multi-Agent Observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)** — by disler - A real-time dashboard that captures Claude Code hook events across concurrent agents — tracing every tool call, task handoff, and lifecycle event through a Bun/SQLite/WebSocket/Vue stack, with session tracking and live filtering
  <sub>★ 1.5k · Python · source · pushed 2026-02-08 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/disler/claude-code-hooks-multi-agent-observability.git`</sub>
- **[ClaudeBar](https://github.com/tddworks/ClaudeBar)** — by tddworks - A macOS menu-bar app that surfaces remaining usage quota for Claude, Codex, Gemini, Copilot, and other AI coding providers at a glance, with burn-rate, dollar-balance, and reset-countdown indicators plus a lightweight live-session indicator. Swift 6 with a layered Domain/Infrastructure architecture
  <sub>★ 1.5k · Swift · brew · pushed 2026-09-03 · Win? · macOS</sub>
  <sub>`brew install --cask claudebar`</sub>
- **[Claude Code Agent Monitor](https://github.com/hoangsonww/Claude-Code-Agent-Monitor)** — by hoangsonww - A self-hosted real-time dashboard that monitors Claude Code agent activity via its native hooks — live sessions, subagent orchestration trees, tool-call timelines, and per-session status — keeping data local (loopback-only). Built on Node/Express + React + SQLite, with a companion MCP server, VS Code extension, and desktop app
  <sub>★ 968 · TypeScript · MIT · npx · pushed 2026-09-03 · macOS</sub>
  <sub>`npx skills add hoangsonww/Claude-Code-Agent-Monitor --list`</sub>
- **[claude-status-bar](https://github.com/m1ckc3s/claude-status-bar)** — by mick - A tiny, hook-driven macOS menu-bar indicator of Claude Code's live turn status — an animated icon while thinking or running a tool, a dot when awaiting permission, and an elapsed-turn timer — aggregated across concurrent CLI, Claude Desktop, and Cursor sessions. Stateless AppKit/Swift app that self-launches on session start and quits when idle
  <sub>★ 678 · Swift · MIT · brew · pushed 2026-08-09 · macOS</sub>
  <sub>`brew install --cask claude-status-bar`</sub>
- **[agents-observe](https://github.com/simple10/agents-observe)** — by Joe Johnston - A real-time Claude Code observability dashboard installed as a plugin: it registers hooks across the full session lifecycle (tool calls, subagent start/stop, task and permission events) and streams them to a local React UI backed by a Dockerized SQLite server, with filtering, parent/subagent hierarchy, full session replay, and per-model token stats
  <sub>★ 666 · TypeScript · MIT · clone · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/simple10/agents-observe.git`</sub>
- **[Claude Code Observability Stack](https://github.com/ColeMurray/claude-code-otel)** — by Cole Murray - A Dockerized OpenTelemetry-to-Grafana observability stack for Claude Code that implements Anthropic's observability guidance, surfacing session activity, performance, token usage, and cost in prebuilt dashboards
  <sub>★ 494 · Makefile · MIT · source · pushed 2025-06-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ColeMurray/claude-code-otel.git`</sub>
- **[toktrack](https://github.com/mag123c/toktrack)** — by mag123c - Ultra-fast token &amp;amp; cost tracker for LLM Token Usage (e.g. Claude Code)
  <sub>★ 187 · Rust · MIT · npx · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx toktrack`</sub>
- **[cctop](https://github.com/stefanprodan/cctop)** — by Stefan Prodan - A live top-style terminal TUI that lists every running Claude Code session with process stats, busy/idle state, context size, model, and git branch, plus a live sub-agent and sub-process tree with open and orphaned ports — reading only the local process table and ~/.claude session and transcript files. Zero-dependency Bun; can signal a runaway session or free orphaned dev-server
  <sub>★ 137 · TypeScript · Apache-2.0 · bun · pushed 2026-09-01 · WSL2 · macOS · Linux</sub>
  <sub>`bun install -g github:stefanprodan/cctop#v0.8.0`</sub>
- **[claude-control](https://github.com/sverrirsig/claude-control)** — by Sverrir Sigurdsson - A native macOS Electron dashboard that auto-discovers running Claude Code CLI sessions and shows live per-session status, git changes, PR checks, and conversation previews across repos and worktrees — and can focus, send input to, approve or reject, kill, or spawn sessions from one place. Electron + Next.js + TypeScript, local-only, via an auto-installed status hook with pr
  <sub>★ 132 · TypeScript · MIT · clone · pushed 2026-08-19 · macOS</sub>
  <sub>`git clone https://github.com/sverrirsig/claude-control.git`</sub>
- **[c9watch](https://github.com/minchenlee/c9watch)** — by minchenlee - A macOS menu-bar app (and companion JSON CLI, built from one Rust/Tauri binary) that auto-discovers running Claude Code sessions by scanning OS processes and shows live working / needs-attention / idle status, plus session-history search, cost tracking, and PM-style worker orchestration. Rust + Tauri 2 + Svelte 5, with a token-gated mobile web client
  <sub>★ 127 · Rust · MIT · script · pushed 2026-09-03 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/minchenlee/c9watch/main/install.sh | bash`</sub>
- **[CCDash](https://github.com/zihenghe04/CCDash)** — by zihenghe04 - Open-source unified usage dashboard for Claude — track tokens, quota, costs across Claude Code, claude.ai &amp;amp; API in one panel. 开源 Claude 全平台用量监控面板，聚合 Claude Code / claude.ai / API 数据，适用于 Pro/Max 订阅用户与开发者。https://dyp23yngrtumg.ok.kimi.link
  <sub>★ 71 · Python · MIT · clone · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zihenghe04/CCDash.git`</sub>
- **[Claude Status](https://github.com/gmr/claude-status)** — by Gavin M. Roy - A native macOS menu-bar app with desktop widgets showing the live state of every running Claude Code session — active, waiting-for-input, compacting, or idle — across many terminals and IDEs, with one-click focus to any session's exact window, tab, or pane. SwiftUI + AppKit + WidgetKit, driven by a bundled hook plugin with process-tree and JSONL-tail fallbacks
  <sub>★ 59 · Swift · BSD-3-Clause · clone · pushed 2026-07-29 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/gmr/claude-status.git`</sub>
- **[CC Harness](https://github.com/lookfree/cc-harness)** — by lookfree - Desktop workbench that reads Claude Code session files locally and renders the subagent and workflow topology as a live graph, with per-node latency, token cost, and nesting depth. Token spend is broken down by source (base session, skills, subagents, MCP) and can be traced from a cost bucket to the exact message that produced it
  <sub>★ 47 · TypeScript · MIT · clone · pushed 2026-08-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/lookfree/cc-harness.git`</sub>
- **[seedeep](https://github.com/duqaXxX/seedeep)** — by duqaXxX - Reads the JSONL session logs Claude Code already writes and shows, live during a turn, what the session is doing: each model call and tool, the context window filling, every subagent on its own window and its own model, and the commits and files the session produced. Bun + TypeScript server serving a local browser GUI, with an optional Tauri menu-bar tray; single-file binaries per pla
  <sub>★ 42 · TypeScript · MIT · npm · pushed 2026-08-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g seedeep`</sub>
- **[goccc](https://github.com/backstabslash/goccc)** — by backstabslash - Fast, zero-dependency cost calculator and customizable statusline for Claude Code. Breakdowns by model, day, project, and branch. Lightweight, single binary, no runtime needed
  <sub>★ 34 · Go · MIT · go · pushed 2026-09-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/backstabslash/goccc@latest`</sub>
- **[cc-costline](https://github.com/Ventuss-OvO/cc-costline)** — by Ventuss-OvO - Enhanced statusline for Claude Code — see your 7d/30d spend at a glance
  <sub>★ 28 · TypeScript · npm · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g cc-costline`</sub>
- **[so-agentbar](https://github.com/sotthang/so-agentbar)** — by sotthang - A native macOS menu-bar app that watches Claude Code and OpenAI Codex CLI session logs in real time and shows each running session's live status, tokens, and cost, with subagent grouping and an optional animated pixel-art view. Swift/SwiftUI + SpriteKit, using FSEvents with incremental JSONL parsing plus multi-provider quota tracking
  <sub>★ 17 · Swift · MIT · clone · pushed 2026-08-21 · Win? · macOS</sub>
  <sub>`git clone https://github.com/sotthang/so-agentbar.git`</sub>
- **[claude-code-status-bar](https://github.com/briansmith80/claude-code-status-bar)** — by briansmith80 - Configurable status bar for Claude Code: usage limits with pacing markers, context window, git state, live activity, session cost, and 8 colour themes. Pure bash, zero dependencies
  <sub>★ 17 · Shell · MIT · psh · pushed 2026-07-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/briansmith80/claude-code-status-bar/main/install.ps1 | iex`</sub>
- **[Claumon](https://github.com/fabioconcina/claumon)** — by fabioconcina - Claude Code dashboard for Pro/Max users: live rate-limit gauges, calibrated usage forecasts, session costs, memory browser. Single binary, zero config
  <sub>★ 16 · Go · MIT · go · pushed 2026-07-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/fabioconcina/claumon@latest`</sub>
- **[AgentWatch](https://github.com/mishanefedov/agentwatch)** — by mishanefedov - Local-only observability for AI agents on your machine. One timeline across coding and non-coding agents
  <sub>★ 14 · TypeScript · MIT · npm · pushed 2026-07-09 · WSL2 · macOS? · Linux</sub>
  <sub>`npm i -g @misha_misha/agentwatch`</sub>
- **[cc-probeline](https://github.com/labzink/cc-probeline)** — by labzink - See where it leaks, stop paying for it — a live Claude Code status line that prices every turn, your subagents, cache rebuilds, plus limits, context and git
  <sub>★ 11 · Go · MIT · scoop · pushed 2026-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add labzink https://github.com/labzink/scoop-bucket scoop install cc-probeline`</sub>
- **[ccvitals](https://github.com/educlopez/ccvitals)** — by educlopez - The prettiest statusline for Claude Code — pure bash, never blocks your prompt. Usage quota, context window, git status &amp;amp; more
  <sub>★ 9 · Shell · MIT · brew · pushed 2026-06-10 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install educlopez/tap/ccvitals`</sub>
- **[Pacer](https://github.com/EricAndrechek/Pacer)** — by EricAndrechek - Native macOS app for tracking Claude Code usage — tokens, cost, rate-limit pacing, per-project breakdowns. SwiftUI + SwiftData
  <sub>★ 8 · Swift · MIT · source · pushed 2026-08-11 · macOS</sub>
  <sub>`git clone https://github.com/EricAndrechek/Pacer.git`</sub>

## Documentation, Knowledge &amp; Learning

- **[claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)** — by Agrici Daniel - Self-organizing AI second brain for Obsidian + Claude Code. Claude reads any source, links it, and files it into one connected knowledge graph of plain Markdown. Based on Karpathy's LLM Wiki pattern
  <sub>★ 14.6k · Python · MIT · clone · pushed 2026-08-26 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgriciDaniel/claude-obsidian.git`</sub>
- **[Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts)** — by Piebald AI - All parts of Claude Code's system prompt, including builtin tool descriptions, sub agent prompts (Plan/Explore/Task), utility prompts (CLAUDE.md, compact, Bash cmd, security review, agent creation, etc.). Updated for each Claude Code version
  <sub>★ 12.6k · JavaScript · MIT · source · pushed 2026-09-02 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/Piebald-AI/claude-code-system-prompts.git`</sub>
- **[Dive into Claude Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)** — by VILA-Lab - A research-lab systematic analysis of the Claude Code codebase whose headline finding — overwhelmingly infrastructure rather than model — reframes Claude Code as a harness
  <sub>★ 2.1k · source · pushed 2026-08-19 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/VILA-Lab/Dive-into-Claude-Code.git`</sub>
- **[cc-thinking-skills](https://github.com/tjboudreaux/cc-thinking-skills)** — by tjboudreaux - A collection of installable thinking-framework skills with a meta-router, notable for publishing a replication-gated evaluation instead of unsupported quality claims
  <sub>★ 1.3k · JavaScript · MIT · npx · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add tjboudreaux/cc-thinking-skills`</sub>
- **[Claude Code Repos Index](https://github.com/danielrosehill/Claude-Code-Projects-Index)** — by Daniel Rosehill - This is either the work of a prolific genius, or a very clever bot (or both), although it hardly matters because the quality is so good - an index of 75+ Claude Code repositories published by the author - and I'm not talking about slop. CMS, system design, deep research, IoT, agentic workflows, server management, personal health... If you spot the lie, let me know, otherwise p
  <sub>★ 537 · Astro · source · pushed 2026-08-19 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/danielrosehill/Claude-Code-Repos-Index.git`</sub>
- **[learn-faster-kit](https://github.com/hluaguo/learn-faster-kit)** — by Hugo Lau - A creative educational framework for Claude Code, inspired by the "FASTER" approach to self-teaching. Ships with a variety of agents, slash commands, and tools that enable Claude Code to help you progress at your own pace, employing well-established pedagogical techniques like active learning and spaced repetition
  <sub>★ 371 · Python · MIT · uv · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install learn-faster --from git+https://github.com/cheukyin175/learn-faster-kit.git`</sub>
- **[Agentic Workflow Patterns](https://github.com/ThibautMelen/agentic-ai-systems)** — by ThibautMelen - A comprehensive and well-documented collection of agentic patterns from Anthropic docs, with colorful Mermaid diagrams and code examples for each pattern. Covers Subagent Orchestration, Progressive Skills, Parallel Tool Calling, Master-Clone Architecture, Wizard Workflows, and more. Also compatible with other providers
  <sub>★ 303 · MIT · source · pushed 2026-07-11</sub>
  <sub>`git clone https://github.com/ThibautMelen/agentic-workflow-patterns.git`</sub>
- **[Bloom](https://github.com/Li-Evan/Bloom)** — by Li-Evan - A self-contained Claude Code skill that turns Benjamin Bloom's "2-sigma" tutoring research into a personal AI tutor: it generates a structured syllabus, teaches one lesson at a time, and adapts each next lesson to the learner's annotations and feedback. The skill is dependency-free and makes no network calls beyond the configured LLM endpoint (an optional web app is also included)
  <sub>★ 249 · Python · MIT · clone · pushed 2026-06-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Li-Evan/Bloom.git`</sub>
- **[claude-code-android](https://github.com/ferrumclaudepilgrim/claude-code-android)** — by ferrumclaudepilgrim - A thorough, device-tested guide and toolkit for running Claude Code natively on Android via three paths (Termux, proot-Ubuntu, and the Android Virtualization Framework), with a verification harness and per-device results. Unusually security-aware for a setup guide — it ships a threat model, an SSRF-guard WebFetch hook, a biometric approval gate, and a permission matrix
  <sub>★ 222 · Shell · MIT · source · pushed 2026-07-27 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/ferrumclaudepilgrim/claude-code-android.git`</sub>
- **[NotebookLM MCP](https://github.com/roomi-fields/notebooklm-mcp)** — by Romain Peyrichou - A mature MCP server (plus a 33-endpoint REST API) that drives Google NotebookLM for citation-backed Q&amp;amp;A and full Studio generation (audio, video, infographics, reports), with multi-account TOTP re-auth. Notably well-maintained and security-attentive — batch-tested on overnight 1,000-question runs, with a documented changelog that includes patching a transitive XSS advisor
  <sub>★ 173 · TypeScript · MIT · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @roomi-fields/notebooklm-mcp@<pinned-version>`</sub>
- **[Bedrock](https://github.com/iurykrieger/claude-bedrock)** — by Iury Krieger - A Claude Code plugin that turns an Obsidian vault into a structured second brain via 8 skills, building an entity-typed (actors/people/teams/topics…) Zettelkasten graph with bidirectional wikilinks and ingesting Confluence, Google Docs, GitHub, and docling-supported files. Operates only on local markdown, with conscientious, opt-out error reporting that explicitly never transmits
  <sub>★ 96 · HTML · MIT · source · pushed 2026-05-05</sub>
  <sub>`git clone https://github.com/iurykrieger/claude-bedrock.git`</sub>
- **[claude-code-docs](https://github.com/costiash/claude-code-docs)** — by Constantin Shafranski - A mirror of the Anthropic&amp;amp;copy; PBC documentation site for Claude/Code, but with bonus features like full-text search and query-time updates - up-to-the-minute, fully-indexed information so that Claude Code can read about itself
  <sub>★ 49 · Python · script · pushed 2026-09-03 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash`</sub>
- **[agentcairn](https://github.com/ccf/agentcairn)** — by ccf - Long-term, cross-project memory for AI coding agents. Your own Obsidian vault as the source of truth. Daemonless and without opaque databases, your memory belongs to you
  <sub>★ 49 · Python · Apache-2.0 · npx · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ccf/agentcairn --skill agentcairn-setup -g`</sub>
- **[Librarian](https://github.com/ngmeyer/librarian-mcp)** — by ngmeyer - A standalone MCP server that gives Claude a markdown second-brain over any Obsidian vault or folder of .md files, with trigram search, auto-wikilinks on write, and real graph analytics (Louvain communities, PageRank, shortest-path, D3 visualization). Runs entirely locally with no network calls or telemetry, productionizing the "LLM wiki" pattern
  <sub>★ 29 · Rust · MIT · cargo · pushed 2026-06-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --git https://github.com/ngmeyer/librarian-mcp`</sub>
- **[cxpak](https://github.com/Barnett-Studios/cxpak)** — by Barnett Studios - A code-intelligence Claude Code plugin and MCP server (Rust, single binary, 43 languages) that builds a typed dependency graph and packs token-budgeted, annotated context bundles for any task. Exceptionally engineered and security-forward — 2,400+ tests, recorded ADRs, a sandboxed WASM plugin SDK, and cosign-signed, SBOM-attested release images
  <sub>★ 27 · Rust · Apache-2.0 · cargo · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install cxpak # any platform, incl. Windows`</sub>
- **[RAG Learning Academy](https://github.com/TakaGoto/rag-learning-academy)** — by Taka Goto - A multi-agent Claude Code learning environment for mastering Retrieval-Augmented Generation, with 20 specialist agents, 22 slash commands, and a 9-module hands-on curriculum that runs zero-config inside Claude Code. Quality is evident — 616 tests, CI, and weekly/monthly content-freshness automation that opens issues for stale material
  <sub>★ 18 · Python · MIT · clone · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TakaGoto/rag-learning-academy.git`</sub>
- **[MDXG Redline](https://github.com/oubakiou/mdxg-redline)** — by oubakiou - A Claude Code skill plus single-file HTML tool that closes the human-review loop on AI-written docs: a person leaves inline comments in the browser, which export as structured JSON keyed by heading path and line, and the skill polls for that file and applies each comment to the exact lines. Strongly privacy-respecting — the local/CLI build enforces a strict CSP (connect-src 'none'),
  <sub>★ 12 · TypeScript · MIT · npx · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mdxg-redline <input.md> ./reviews # writes into ./reviews`</sub>
- **[showreel](https://github.com/HeyRenan/showreel)** — by HeyRenan - A Claude Code plugin that turns CSS selectors + text into finished visual documentation — annotated screenshots, flow GIFs/MP4s, terminal recordings, and before/after composites — placing every annotation deterministically and pixel-verifying each artifact (PASS/FAIL) before it is saved. Self-contained (bundles its own headless Chromium, no browser MCP, no telemetry); every image in
  <sub>★ 9 · JavaScript · MIT · source · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HeyRenan/showreel.git`</sub>
- **[Claude Code Handbook](https://nikiforovall.blog/claude-code-rules/)** — by nikiforovall - Collection of best practices, tips, and techniques for Claude Code development workflows, enhanced with distributable plugins
  <sub>website</sub>
  <sub>`https://nikiforovall.blog/claude-code-rules/`</sub>
- **[Encyclopedia of Agentic Coding Patterns](https://aipatternbook.com)** — by Wolf McNally - A freely available reference covering 190+ patterns for AI-assisted software development (and actually a whole bunch of related technical topics) from foundational concepts through agentic construction patterns, governance, testing, and socio-technical systems. Each entry follows a consistent pattern-language format with Context, Problem, Forces, Solution, Consequences, and Relat
  <sub>website</sub>
  <sub>`https://aipatternbook.com`</sub>

## Research &amp; Scientific Inquiry

- **[My Claude Code Setup](https://github.com/pedrohcgs/claude-code-my-workflow)** — by Pedro H. C. Sant'Anna - A ready-to-fork Claude Code template for academics using LaTeX/Beamer + R. Multi-agent review, quality gates, adversarial QA, and replication protocols. Great use of orchestration patterns and great documentation
  <sub>★ 1.6k · HTML · MIT · clone · pushed 2026-08-24 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/YOUR_USERNAME/claude-code-my-workflow.git`</sub>
- **[AI Research Skills](https://github.com/WenyuChiou/ai-research-skills)** — by Wenyu Chiou - A catalog of 15 Claude Code skills mapped to 8 research-workflow stages (literature → gap analysis → design → drafting → reviewer response), where each stage emits an explicit YAML/Markdown deliverable the next stage consumes. Thoughtfully designed around anti-hallucination — schemas force "gap" status on unsupported claims, and downstream skills refuse malformed, overconfident ha
  <sub>★ 237 · Python · MIT · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install research-hub-pipeline`</sub>

## Security

- **[SkillSpector](https://github.com/NVIDIA/SkillSpector)** — by NVIDIA - Security scanner for AI agent skills. Detect vulnerabilities, malicious patterns, and security risks
  <sub>★ 15.8k · Python · Apache-2.0 · uv · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install git+https://github.com/NVIDIA/skillspector.git`</sub>
- **[Claude Code Safety Net](https://github.com/kenryu42/cc-safety-net)** — by kenryu42 - A coding agent CLI hook that acts as a safety net, catching destructive git and filesystem commands before they execute. Supports Codex, Claude Code, OpenCode, Gemini CLI, Copilot CLI, Kimi Code and Pi
  <sub>★ 1.5k · TypeScript · MIT · npm · pushed 2026-09-03 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g cc-safety-net`</sub>
- **[Code on Incus](https://github.com/mensfeld/code-on-incus)** — by mensfeld - Give each AI agent its own isolated machine with root, Docker, and systemd. Active defense detects and stops threats automatically
  <sub>★ 687 · Go · MIT · script · pushed 2026-09-03 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/mensfeld/code-on-incus/master/install.sh | bash`</sub>
- **[Node9](https://github.com/node9-ai/node9-proxy)** — by node9-ai - The Execution Security Layer for the Agentic Era. Providing deterministic "Sudo" governance and audit logs for autonomous AI agents
  <sub>★ 210 · TypeScript · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g node9-ai`</sub>
- **[authsome](https://github.com/agentrhq/authsome)** — by agentrhq - Credential gateway for AI agents. Log in once via Oauth2 or API Key. Every agent stays authenticated — headless, no SaaS, agents never see your credentials
  <sub>★ 87 · Python · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add agentrhq/authsome`</sub>
- **[Airut](https://github.com/airutorg/airut)** — by airutorg - Airut is a system for running Claude Code tasks from email and Slack. It handles workspace provisioning, container isolation, network sandboxing, session persistence, and cleanup — a secure foundation for autonomous agentic development
  <sub>★ 82 · Python · MIT · uv · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install airut # Install from PyPI`</sub>
- **[Brood Box](https://github.com/stacklok/brood-box)** — by stacklok - CLI tool for running coding agents inside hardware-isolated microVMs
  <sub>★ 64 · Go · Apache-2.0 · source · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/stacklok/brood-box.git`</sub>
- **[Agent Guard](https://github.com/JeongJaeSoon/agent-guard)** — by JeongJaeSoon - Real-time secret-leak guardrails for AI coding agents (Claude Code, Codex), Git hooks, and CI
  <sub>★ 25 · Shell · MIT · script · pushed 2026-09-03 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/JeongJaeSoon/agent-guard/releases/latest/download/bootstrap.sh | sh`</sub>
- **[GouvernAI](https://github.com/Myr-Aya/GouvernAI-claude-code-plugin)** — by Myr-Aya - Runtime guardrails for Claude Code. Auto-approve what's safe, gate what's risky, block what's dangerous. Dual enforcement, full audit trail. MIT
  <sub>★ 22 · Python · MIT · source · pushed 2026-07-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Myr-Aya/GouvernAI-claude-code-plugin.git`</sub>
- **[aicontainer](https://github.com/stefanoginella/aicontainer)** — by stefanoginella - Sandboxed devcontainer for running Claude Code, Codex, and OpenCode in bypass / auto-approve mode
  <sub>★ 20 · Shell · MIT · npm · pushed 2026-09-01 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npm install -g aicontainer`</sub>
- **[compass](https://github.com/dshakes/compass)** — by dshakes - Developer-grade Claude Code + Codex configuration: cost-tiered subagents, workflow commands, guardrail hooks, MCP parity, and an installable plugin/marketplace
  <sub>★ 19 · Shell · MIT · brew · pushed 2026-08-31 · macOS</sub>
  <sub>`brew install dshakes/tap/compass # latest release · --HEAD to track main`</sub>
- **[machine](https://github.com/katspaugh/machine)** — by katspaugh - One isolated Lima VM per GitHub project — sandboxed Claude Code/Codex, Docker, Node, signed git
  <sub>★ 15 · Python · MIT · brew · pushed 2026-07-20 · WSL2 · macOS · Linux</sub>
  <sub>`brew install katspaugh/machine/machine`</sub>
- **[Cleat](https://github.com/cleatdev/cleat)** — by cleatdev - Give the agent a cage, not your keys. One-command Docker sandbox for AI coding agents: full autonomous permissions, per-project isolation, your host stays untouched
  <sub>★ 12 · Shell · MIT · brew · pushed 2026-08-22 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install cleatdev/tap/cleat`</sub>
- **[Claude Code Safety Guard](https://github.com/inoX-Network/claude-code-safety-guard)** — by inoX-Network - 3-level override system for Claude Code - prevents destructive system operations. Born from a real incident
  <sub>★ 6 · Python · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/inoX-Network/claude-code-safety-guard`</sub>
- **[SkilLock](https://github.com/skills-lock/skil-lock)** — by skills-lock - Pin AI Skill behavior. Block unapproved drift in CI. See exactly what changed in every PR
  <sub>★ 3 · Go · Apache-2.0 · go · pushed 2026-09-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/skills-lock/skil-lock/cmd/skil-lock@v0.2.5`</sub>

## Agent Orchestration

- **[gstack](https://github.com/garrytan/gstack)** — by Garry Tan - Garry Tan's (Y Combinator) Claude Code setup and "open source software factory" for managing the development lifecycle end-to-end. Includes a set of agents and in-depth skills/tools along with workflows for advancing a product from ideation to production
  <sub>★ 131.1k · TypeScript · MIT · source · pushed 2026-09-01 · macOS</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git`</sub>
- **[Ralph for Claude Code](https://github.com/frankbria/ralph-claude-code)** — by Frank Bria - An autonomous AI development framework that enables Claude Code to work iteratively on projects until completion. Features intelligent exit detection, rate limiting, circuit breaker patterns, and comprehensive safety guardrails to prevent infinite loops and API overuse. Built with Bash, integrated with tmux for live monitoring, and includes 75+ comprehensive tests
  <sub>★ 9.6k · Shell · MIT · script · pushed 2026-07-18 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -sL https://raw.githubusercontent.com/frankbria/ralph-claude-code/main/uninstall.sh | bash`</sub>
- **[Harness](https://github.com/revfactory/harness)** — by revfactory - A meta-skill that designs domain-specific agent teams, defines specialized agents, and generates the skills they use. Resources are in Korean but can produce high-quality English-language output
  <sub>★ 8.9k · HTML · Apache-2.0 · source · pushed 2026-07-24</sub>
  <sub>`git clone https://github.com/revfactory/harness.git`</sub>
- **[ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator)** — by mikeyobrien - Ralph Orchestrator implements the simple but effective "Ralph Wiggum" technique for autonomous task completion, continuously running an AI agent against a prompt file until the task is marked as complete or limits are reached. This implementation provides a robust, well-tested, and feature-complete orchestration system for AI-driven development. Also cited in the Anthropic Ralph p
  <sub>★ 3.1k · Rust · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ralph-orchestrator/ralph-cli`</sub>
- **[Claude Code Harness](https://github.com/Chachamaru127/claude-code-harness)** — by Chachamaru - A Claude Code development harness that enables reliable high-quality development through an autonomous Plan -&amp;gt; Work -&amp;gt; Review cycle. Well documented and includes an Output Style
  <sub>★ 3.1k · Shell · MIT · source · pushed 2026-08-31</sub>
  <sub>`git clone https://github.com/Chachamaru127/claude-code-harness.git`</sub>
- **[AB Method](https://github.com/ayoubben18/ab-method)** — by Ayoub Bensalah - A principled, spec-driven workflow that transforms large problems into focused, incremental missions using Claude Code's specialized sub agents. Includes slash-commands, sub agents, and specialized workflows designed for specific parts of the SDLC
  <sub>★ 189 · JavaScript · MIT · npx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ab-method`</sub>
- **[RIPER Workflow](https://github.com/tony/claude-code-riper-5)** — by Tony Narlock - Structured development workflow enforcing separation between Research, Innovate, Plan, Execute, and Review phases. Features consolidated subagents for context-efficiency, branch-aware memory bank, and strict mode enforcement for guided development
  <sub>★ 93 · MIT · source · pushed 2026-08-16</sub>
  <sub>`git clone https://github.com/tony/claude-code-riper-5.git`</sub>
- **[Agent Collab Skills](https://github.com/WenyuChiou/agent-collab-skills)** — by Wenyu Chiou - Claude Code marketplace for multi-agent collaboration — task splitter, output reconciler, adversarial debate, shared memory, acceptance gate. Composes with codex-delegate / gemini-delegate
  <sub>★ 25 · Python · MIT · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/WenyuChiou/agent-collab-skills.git`</sub>
- **[Dynamic Workflow Design Patterns](https://github.com/zircote/workflows-plugin)** — by Robert Allen - A Skill based on this extremely well authored article about dynamic workflows. Detailed explanations regarding the Workflow tool and sensible advice covering a range of patterns and anti-patterns
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-07-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zircote/workflows-plugin.git`</sub>
- **[Project Workflow System](https://github.com/harperreed/dotfiles/tree/master/.claude/commands)** — by harperreed - A set of commands that provide a comprehensive workflow system for managing projects, including task management, code review, and deployment processes
  <sub>Vim Script · in-repo · pushed 2026-08-30</sub>
  <sub>`git clone https://github.com/harperreed/dotfiles.git && cd dotfiles/.claude/commands`</sub>
- **[Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)** — by Anthropic PBC - The official Anthropic implementation of the Ralph Wiggum technique for iterative, self-referential AI development loops in Claude Code
  <sub>Python · in-repo · pushed 2026-09-02</sub>
  <sub>`git clone https://github.com/anthropics/claude-code.git && cd claude-code/plugins/ralph-wiggum`</sub>

## Memory &amp; Context Persistence

- **[Hivemind](https://github.com/activeloopai/hivemind)** — by activeloopai - Hivemind turns your traces into reusable skills across agents
  <sub>★ 1.6k · TypeScript · Apache-2.0 · psh · pushed 2026-09-03 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://deeplake.ai/hivemind.ps1 | iex`</sub>
- **[claude-context-optimizer](https://github.com/egorfedorov/claude-context-optimizer)** — by Egor Fedorov - Claude Code plugin that tracks token usage, identifies wasted context, and saves money on unnecessary API costs, by tracking which information is actually being reused later. Visuals include heatmaps, ROI reports, budget alerts, efficiency scores, git-aware suggestions - all local, zero config. The design is still somewhat exploratory, but it shows promise
  <sub>★ 104 · JavaScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/egorfedorov/claude-context-optimizer`</sub>
- **[roampal-core](https://github.com/roampal-ai/roampal-core)** — by roampal-ai - Outcome-based persistent memory MCP server for Claude Code and OpenCode. Good advice promoted, bad advice demoted. pip install roampal
  <sub>★ 50 · Python · Apache-2.0 · pip · pushed 2026-08-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install roampal`</sub>
- **[Callimachus](https://github.com/BetaBots-LLC/callimachus)** — by BetaBots-LLC - One local, searchable index of your AI coding-agent history Claude Code, Codex, Cursor, Gemini &amp;amp; more. Keyword + semantic search, MCP server, CLI &amp;amp; VS Code extension
  <sub>★ 37 · Rust · AGPL-3.0 · cargo · pushed 2026-07-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --path apps/desktop/src-tauri --bin callimachus-mcp`</sub>
- **[faf-cli](https://github.com/Wolfe-Jam/faf-cli)** — by Wolfe-Jam - Authors and versions CLAUDE.md and AGENTS.md from a repository's actual detected stack, so Claude Code's project context stays in sync with the code instead of drifting. One typed source file (project.faf, an IANA-registered media type) is the single origin for every assistant's context file; a deterministic score reports how complete that context is. The file lives in the repo and
  <sub>★ 37 · TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`bunx faf-cli git https://github.com/facebook/react`</sub>
- **[Selvedge](https://github.com/masondelan/selvedge)** — by masondelan - Long-term memory for AI-coded codebases. A git blame for AI agents — but for the why. MCP server that captures the agent's reasoning live, in context, as each change is made. Local SQLite, zero deps
  <sub>★ 22 · Python · MIT · pip · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install selvedge`</sub>
- **[Claude Mnemonic](https://github.com/lukaszraczylo/claude-mnemonic)** — by lukaszraczylo - Memory management and retrieval for Claude Code
  <sub>★ 19 · Go · MIT · psh · pushed 2026-07-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/lukaszraczylo/claude-mnemonic/main/scripts/install.ps1 | iex`</sub>
- **[MAMA](https://github.com/jungjaehoon-lifegamez/MAMA)** — by jungjaehoon-lifegamez - Always-on companion for Claude that remembers your decisions and their evolution. Local-first memory using SQLite + transformers.js embeddings
  <sub>★ 12 · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @jungjaehoon/mama-os`</sub>
- **[capy](https://github.com/serpro69/capy)** — by serpro69 - 🦫 Privacy-first virtualization layer for LLM context with MCP protocol for tool access
  <sub>★ 10 · Go · brew · pushed 2026-09-02 · WSL2? · macOS · Linux</sub>
  <sub>`brew install serpro69/tap/capy`</sub>
- **[fable](https://github.com/grooverLab/fable)** — by grooverLab - High-fidelity transcript memory for Claude Code — index every session, recall byte-identical, search, prune, compose. Local-first, stdlib-only, MCP
  <sub>★ 10 · Python · MIT · pipx · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/grooverLab/fable`</sub>
- **[presence](https://github.com/sara-star-quant/presence)** — by sara-star-quant - Per-repo memory, outcome telemetry, and a calibrated-confidence gate for Claude Code, with MCP and AGENTS.md projections so other AI coding tools can read its context. Notes survive sessions; success claims need test evidence; your reverts are remembered. Local-only, stdlib runtime
  <sub>★ 6 · Python · Apache-2.0 · script · pushed 2026-08-30 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/sara-star-quant/presence/main/install.sh | bash`</sub>

## Alternative Clients

- **[CloudCLI (Claude Code UI)](https://github.com/siteboon/claudecodeui)** — by siteboon - A web and mobile PWA for driving Claude Code (and Cursor/Codex/Gemini) from any device — file explorer, git, integrated shell, and full session management that reads and writes your real ~/.claude config rather than duplicating it. By far the most-adopted Claude Code UI, with a self-hostable open-source core, an optional Docker microVM sandbox mode, a plugin ecosystem, and tools disa
  <sub>★ 13.6k · TypeScript · AGPL-3.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @cloudcli-ai/cloudcli`</sub>
- **[Cate](https://github.com/0-AI-UG/cate)** — by 0-AI UG - A cross-platform desktop IDE built on an infinite zoomable canvas, where editors, terminals, browsers, and docs float in freeform space instead of tabs — and ships skills that let Claude Code spawn agent terminals on the canvas, coordinate through canvas notes, and drive browser panels. A genuinely novel UX, well-engineered (CI, e2e tests, context-isolated IPC, scoped filesystem acces
  <sub>★ 2.1k · TypeScript · MIT · brew · pushed 2026-09-03 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask cate`</sub>
- **[Nimbalyst](https://github.com/nimbalyst/nimbalyst)** — by Greg Hinkle - A visual workspace for building with Claude Code (and Codex) where you and the agent co-edit *visually* — markdown, mockups, mermaid, Excalidraw, CSV, and data models — approving the agent's changes as red/green WYSIWYG diffs, with session/task kanban, worktrees, an extension SDK, and a native iOS companion app. A distinctive higher-bandwidth take on agent collaboration, open sour
  <sub>★ 1.6k · TypeScript · MIT · source · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/nimbalyst/nimbalyst.git`</sub>
- **[Vibeyard](https://github.com/elirantutia/vibeyard)** — by Eliran Tutia - A cross-platform desktop IDE that wraps Claude Code sessions with a swarm mode (parallel agents in a grid), a real-time session inspector (cost, tokens, tool-usage, context), multiple isolated Claude profiles, a kanban board, and encrypted P2P session sharing over WebRTC. Signed/notarized, broadly adopted, and built squarely for the multi-agent, multi-session workflow
  <sub>★ 1.4k · TypeScript · MIT · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g vibeyard`</sub>
- **[Claude Overlay](https://github.com/shengyanlin/claude-overlay)** — by shengyanlin - A frameless, always-on-top floating chat window for Claude Code on Windows. It captures every monitor and lets Claude read the screen to answer questions in context, and drives the user's existing claude CLI login through the Agent SDK, with image paste, model switching, live streaming, and a context-usage statusline
  <sub>★ 89 · Python · MIT · clone · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/shengyanlin/claude-overlay.git`</sub>
- **[Sidekick for Max](https://github.com/cesarandreslopez/sidekick-agent-hub)** — by César Andrés López - A VS Code extension and standalone terminal dashboard that adds visibility and AI conveniences on top of your Claude Max subscription — inline completions, code transforms, AI commit messages, plus deep session observability (token-burn, a 13-week quota heatmap, multi-account management, cross-session search, and asset extraction). Mature and well-maintained (CI, published
  <sub>★ 81 · TypeScript · MIT · npm · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g sidekick-agent-hub # requires Node.js 20+`</sub>
- **[FlyCrys](https://github.com/SergKam/FlyCrys)** — by Sergii Kamenskyi - A native Linux GUI for Claude Code agents built in Rust + GTK4 — single binary, no Electron, starts in under a second — with a file tree, syntax-highlighted viewer, markdown preview, embedded VTE4 terminal, streaming agent chat, workspace tabs, and tool-restricted agent profiles. Fills a real gap as essentially the only native (non-webview) Linux desktop client, using your ow
  <sub>★ 31 · Rust · MIT · clone · pushed 2026-06-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/SergKam/FlyCrys.git`</sub>

## Infrastructure &amp; DevOps

- **[terraform-skill](https://github.com/antonbabenko/terraform-skill)** — by Anton Babenko - A best-practices skill that teaches the agent to write safer Terraform and OpenTofu through a diagnose-first workflow, failure-mode routing, LLM-mistake checklists, and a feature-version guard table mapping features to their version floor and common errors — covering testing, modules, remote state, CI/CD, and security scanning across AWS/Azure/GCP. From an AWS Hero behind the te
  <sub>★ 2.3k · npx · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/antonbabenko/terraform-skill`</sub>
- **[otelcol-doctor](https://github.com/s3onghyun/otelcol-doctor)** — by s3onghyun - A focused, vendor-neutral skill that writes, fixes, and *validates* OpenTelemetry Collector configs — encoding the Collector's real footguns (memory_limiter/batch ordering, core-vs-contrib components, pull-vs-push exporters, deprecated exporters, pipelines that validate but were never wired) as an authoring workflow and diagnosis checklist. Its standout is honesty plus a verificatio
  <sub>★ 8 · Shell · Apache-2.0 · clone · pushed 2026-08-05</sub>
  <sub>`git clone https://github.com/s3onghyun/otelcol-doctor`</sub>

## Providers, Runtime &amp; Integration Infrastructure

- **[Flue](https://github.com/SFKislev/Flue)** — by S.F. Kislev - A tiny bridge that lets Claude Code drive desktop software — Photoshop, Premiere, Blender, Unity, InDesign, Office, 13 apps total — by writing one-time scripts against each app's own automation runtime (COM / AppleScript / CEP), instead of MCP servers or fragile screenshot-based computer use. A genuinely novel approach that unlocks the apps' full scripting surfaces (InDesign alone
  <sub>★ 78 · Python · MIT · pip · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install flue`</sub>
- **[llm-router](https://github.com/ypollak2/llm-router)** — by Yali Pollak - A local-first router that sits under Claude Code (and Codex/Gemini CLI) and sends each prompt to the cheapest capable model, with three-layer token compression and automatic provider fallback — protecting your premium quota and cutting cost with zero config on a Claude subscription. Credibly engineered: 1,900+ tests, an independent RouterArena benchmark placement, and an honest lo
  <sub>★ 77 · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llm-routing # installs the `llm-router` command`</sub>
- **[OpenWeb](https://github.com/imoonkey/openweb)** — by openweb-org - An agent-native skill that accesses 90+ websites by calling their underlying APIs directly (typed JSON in, JSON out) instead of screenshotting and parsing the DOM, with auth auto-resolved locally from your existing browser session. Security is first-class — every operation is tagged read/write/delete/transact behind permission tiers, SSRF protection runs on each request, and there
  <sub>★ 60 · TypeScript · MIT · npm · pushed 2026-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @openweb-org/openweb`</sub>
- **[claude-code-wsl2-setup](https://github.com/congmnguyen/claude-code-wsl2-setup)** — by congmnguyen - A focused collection of documented scripts that fix the most painful Claude Code papercuts on WSL2 + Windows Terminal — clipboard screenshot paste via a Go daemon, Windows notifications on Stop/PermissionRequest hooks, LSP wiring, a usage-aware status line, and voice-mode audio routing. Each fix is written up with root cause and exact config (including non-obvious traps like Sessi
  <sub>★ 48 · Shell · MIT · clone · pushed 2026-08-31 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/congmnguyen/claude-code-wsl2-setup.git`</sub>
- **[chrome-cdp-ex](https://github.com/EndeavorYen/chrome-cdp-ex)** — by Endeavor Yen - A zero-dependency Claude Code skill (68 commands) that connects to your *real* Chrome — logged-in tabs, cookies, live page state — to give the agent a perception layer: layout, visible styles, per-action "what changed" evidence, CSS-cascade-to-source tracing, and session replay/Playwright export. Notably rigorous about its own claims, with a dogfood benchmark gate that blocks per
  <sub>★ 20 · JavaScript · MIT · clone · pushed 2026-09-02 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/EndeavorYen/chrome-cdp-ex.git`</sub>
- **[SPARDA](https://github.com/zakariagharzouli/sparda)** — by Zakaria Gharzouli (Residual Labs) - Converts a running Express or FastAPI app into an MCP server by AST-parsing its routes and injecting a marked, byte-for-byte-removable /mcp router, so the agent can operate your live application (real auth, real data) rather than just read files. Exceptionally safety-minded: writes are disabled by default behind two-phase confirmation, docstrings are sanitize
  <sub>★ 8 · JavaScript · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sparda-mcp apocalypse # prove the tree is safe to deploy — exit 1 on any real risk, or on an unverified premise`</sub>

## Skills

- **[Superpowers](https://github.com/obra/superpowers)** — by Jesse Vincent - A strong bundle of core competencies for software engineering, with good coverage of a large portion of the SDLC - from planning, reviewing, testing, debugging... Well written, well organized, and adaptable. The author refers to them as "superpowers", but many of them are just consolidating engineering best practices - which sometimes does feel like a superpower when working wit
  <sub>★ 281.2k · Shell · MIT · source · pushed 2026-08-31</sub>
  <sub>`git clone https://github.com/obra/superpowers.git`</sub>
- **[Caveman](https://github.com/JuliusBrussee/caveman)** — by Julius Brussee - A plugin that conserves message tokens by communicating in fragmented "caveman speak" - sort of a clever form of compression. Now accompanied by a whole caveman ecosystem including a memory system, caveman spec kit, and a caveman agent
  <sub>★ 102.9k · Go · psh · pushed 2026-09-02 · Win</sub>
  <sub>`irm https://raw.githubusercontent.com/JuliusBrussee/caveman/v2.5.0/install.ps1 | iex`</sub>
- **[Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** — by diet103 - A remarkably innovative approach to working with Skills, the centerpiece of which being a technique that leverages hooks to ensure that Claude intelligently selects and activates the appropriate Skill given the current context. Well-documented and adaptable to different projects and workflows
  <sub>★ 10k · TypeScript · MIT · clone · pushed 2026-07-13 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/diet103/claude-code-infrastructure-showcase.git`</sub>
- **[fable-mode](https://github.com/mrtooher/fable-mode)** — by mrtooher - A Claude skill that activates Fable-style agentic behavior: explicit multi-stage planning, sub-agent delegation, and self-verification
  <sub>★ 849 · Python · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mrtooher/fable-mode.git`</sub>
- **[SuperSEO Skills](https://github.com/inhouseseo/superseo-skills)** — by sanderbz - A nice package of Claude Skills focused on SEO workflows: page audits, content briefs, article writing, E-E-A-T audits, semantic gap analysis, and more. Each skill fetches the target page and reads the top-ranking competitors itself, so users don't paste in keyword exports or crawl reports
  <sub>★ 294 · Apache-2.0 · clone · pushed 2026-05-12</sub>
  <sub>`git clone https://github.com/inhouseseo/superseo-skills.git`</sub>

## Design &amp; UI/UX

- **[Diagram Design](https://github.com/cathrynlavery/diagram-design)** — by Cathryn Lavery - Another welcome contribution to the domain of making Claude Code output look stylish, this collection of skills produces a variety of editorial diagrams in the form of self-contained HTML + SVG. Although I never thought I'd hear these words together, according to the author: "no Mermaid-slop."
  <sub>★ 30.2k · HTML · MIT · clone · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone git@github.com:cathrynlavery/diagram-design.git`</sub>
- **[visual-explainer](https://github.com/nicobailon/visual-explainer)** — by nicobailon - Agent skill and plugin that turns complex terminal output into styled HTML pages or slide decks for diagrams, diff reviews, plan audits, data tables, and project recaps. Generates self-contained browser-readable artifacts with Mermaid diagrams, responsive layouts, themes, and sharing commands
  <sub>★ 9.6k · HTML · MIT · script · pushed 2026-08-28 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/nicobailon/visual-explainer/main/install-pi.sh | bash`</sub>
- **[Dev Browser](https://github.com/SawyerHood/dev-browser)** — by Sawyer Hood - A browser-automation plugin/skill that lets Claude Code drive a browser to test and verify its own work — full Playwright API plus pixel- and DOM-level computer-use toolsets, connecting to your running Chrome or a fresh Chromium. Notably secure and fast: scripts execute inside a QuickJS WASM sandbox with no host filesystem or network access, and a published benchmark shows it beat
  <sub>★ 6.6k · TypeScript · MIT · npm · pushed 2026-07-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g dev-browser`</sub>
- **[StyleSeed](https://github.com/bitjaru/styleseed)** — by kiwiman - A design engine that takes a different tack from "feed the model more tokens": it teaches design *judgment* — ~74 rules pros carry but never write down ("the refined black isn't #000, it's #2A2A2A"; "one accent color, everything else grayscale") — as plain markdown the agent reads automatically, plus a brand-agnostic skin system, a named motion vocabulary, and /ss-* review skills. Wid
  <sub>★ 939 · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add bitjaru/styleseed`</sub>
- **[Snip](https://github.com/rixinhahaha/snip)** — by rixinhahaha - A visual whiteboard between you and your agent: Claude renders diagrams, HTML, or UI components through Snip instead of describing them in text, you approve or annotate directly on the output (circle, arrow, note), and the agent gets structured feedback and iterates. Works via CLI or MCP, doubles as a full local screenshot/annotation app with on-device AI organization (Ollama), an
  <sub>★ 322 · JavaScript · MIT · brew · pushed 2026-05-07 · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask rixinhahaha/snip/snip`</sub>
- **[UI Craft](https://github.com/educlopez/ui-craft)** — by Eduardo Calvo - A deep design-engineering skill that makes agents "design like they have taste" by default, layered so you can just install it, drive it with 22 single-lens commands, or wire its deterministic MCP gates and CLI into CI. Its signature is a *scoreable, defensible* critique — Nielsen's heuristics × classic design laws × persona walkthroughs, every finding tagged by business impact
  <sub>★ 309 · JavaScript · MIT · scoop · pushed 2026-09-03 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`scoop bucket add educlopez https://github.com/educlopez/scoop-bucket scoop install educlopez/ui-craft`</sub>

## Writing &amp; Prose Quality

- **[Avoid AI Writing](https://github.com/conorbronsdon/avoid-ai-writing)** — by Conor Bronsdon - A portable writing skill that audits and rewrites prose to remove "AI-isms" — 49+ pattern categories and a tiered word-replacement vocabulary, with detect / rewrite / edit-in-place modes, content-type and voice profiles, and a two-pass re-check. Stands well above the crowded de-slop field: it ships a deterministic, zero-dependency detector engine (the single source of its 0–100
  <sub>★ 4k · JavaScript · MIT · npx · pushed 2026-08-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills@1.5.23 add conorbronsdon/avoid-ai-writing`</sub>
- **[naming](https://github.com/glacierphonk/naming)** — by GlacierPhonk - A Claude Code skill for naming products, SaaS tools, brands, and projects via a structured metaphor-driven process — naming brief, metaphor exploration, candidate generation, anti-slop filtering, a weighted evaluation rubric, and availability checks for domains/handles/package names. A genuinely different (and creative) take that produces names grounded in meaning instead of the
  <sub>★ 93 · Shell · MIT · clone · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/glacierphonk/naming.git`</sub>

## Creative Media

- **[Vox director skill](https://github.com/Alisa0808/vox-director)** — by Alisa Qian - Vox Director is an open-source skill that turns a one-line topic into a finished Vox-style paper-collage explainer or ad video. It automates the full pipeline — script, collage keyframes, motion, voice-over, music, and captions — on the Atlas Cloud API plus local ffmpeg, with two human approval gates for the beat map and visual style
  <sub>★ 1.7k · Python · MIT · clone · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Alisa0808/vox-director.git`</sub>
- **[claude-replay](https://github.com/es617/claude-replay)** — by es617 - An outstanding, creative library that converts Claude Code session transcripts into self-contained, embeddable HTML replays - interactive playback with speed control, a local editor, collapsible tool-call and thinking blocks, redaction for private information - the output is fantastic. Also supports other providers
  <sub>★ 822 · JavaScript · MIT · npm · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g claude-replay`</sub>
- **[motion-skills](https://github.com/iart-ai/motion-skills)** — by iart.ai - An open-source collection of ~50 motion-graphics, animation, and video skills across 14 installable packs — kinetic typography, data-driven charts, explainers, TikTok/Reels, web/WebGL animation, and Manim math animation — that teach an agent how a professional would build each piece. Every visual skill ships a deliver-and-verify loop (render a frame → screenshot → check) plus a small
  <sub>★ 407 · HTML · MIT · npx · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add iart-ai/tiktok-video-skills`</sub>
- **[capcut-cli](https://github.com/renezander030/capcut-cli)** — by René Zander - A zero-dependency Node CLI (and Claude Code plugin/skill) that lets the agent edit CapCut / JianYing video projects programmatically — inspect timelines, build drafts, add text/audio, word-level captions and Whisper transcription, templates, and cut long-form into shorts — JSON in, JSON out, no server. Deeply mature for a media tool: 205 tests across macOS/Windows/Linux CI, a huge
  <sub>★ 406 · JavaScript · MIT · npm · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g capcut-cli`</sub>

## Linting

- **[agnix](https://github.com/agent-sh/agnix)** — by agent-sh - The linter and LSP for AI coding assistants — validates CLAUDE.md, AGENTS.md, SKILL.md, hooks, and MCP config, with autofixes and IDE plugins
  <sub>★ 403 · Rust · Apache-2.0 · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agnix`</sub>
- **[BlockWatch](https://github.com/mennanov/blockwatch)** — by mennanov - A language-agnostic linter (Rust) that keeps co-dependent code, docs, and config in sync, with a Claude Code plugin skill
  <sub>★ 29 · Rust · MIT · cargo · pushed 2026-09-01 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install blockwatch # from source`</sub>
- **[Schliff](https://github.com/Zandereins/schliff)** — by Zandereins - Deterministic quality scorer for AI agent instruction files — 8-dimension scoring with security, multi-format (SKILL.md, CLAUDE.md, .cursorrules, AGENTS.md), anti-gaming detection, zero dependencies
  <sub>★ 15 · Python · MIT · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx schliff score AGENTS.md # or any SKILL.md / CLAUDE.md / .cursorrules`</sub>
- **[agents-md-cookbook](https://github.com/Taiizor/agents-md-cookbook)** — by Taiizor - The tested, tool-agnostic AGENTS.md kit — verified templates, a CI linter, and migrators from .cursorrules/CLAUDE.md/Copilot/Windsurf/Cline/Aider
  <sub>★ 14 · TypeScript · MIT · npx · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx agents-md-migrate # or: npx agents-md-migrate`</sub>
- **[Upkeep](https://github.com/wei18/Upkeep)** — by wei18 - Upkeep — an AI audit crew for your repo. Catches docs/spec/asset drift with evidence; output-only. Claude Code plugin/skill + reusable CI workflow
  <sub>★ 14 · TypeScript · MIT · npx · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add wei18/upkeep --skill upkeep-audit`</sub>
- **[Ctxlint](https://github.com/ctxlint/Ctxlint)** — by ctxlint - A CLI linter for AI agent context files that catches stale references, dead commands, and hardcoded secrets, with a modular tested rule set
  <sub>★ 11 · JavaScript · MIT · npm · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ctxlint/ctxlint`</sub>

## Status Lines

- **[claude-statusbar](https://github.com/leeguooooo/claude-code-usage-bar)** — by leeguooooo - The most complete Claude Code status line: 5-hour and 7-day rate-limit usage with reset countdowns and *learned* end-of-window projections, context window, prompt-cache-expiry countdown, per-session cost, plus live todo/tool/git activity — across 3 styles and 9 themes, configurable by CLI or natural-language skill. Genuinely well-engineered (PyPI, 320+ tests, a sub-1%-CPU daemon, d
  <sub>★ 359 · Python · MIT · pip · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install claude-statusbar # or: uv tool install / pipx install`</sub>
- **[claude-code-personalities](https://github.com/kumamaki/Claude-Code-Personalities)** — by kumamaki - A delightfully different status line: 30+ kaomoji text-faces that react in real time to what Claude is doing — context-aware personas by file type, and a frustration-escalation system where mounting errors progress from ( ദ്ദി ˙ᗜ˙ ) toward a table-flip (╯°□°)╯︵ ┻━┻. Pure Rust with sub-2ms rendering, a single binary, hook-based activity tracking, and an interactive config TUI — the st
  <sub>★ 31 · Rust · WTFPL · script · pushed 2026-06-30 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/kumamaki/claude-code-personalities/main/install.sh | bash`</sub>
- **[claudinho](https://github.com/arturogarrido/claudinho)** — by Arturo Garrido - 2026 World Cup live scores in your terminal, Claude Code statusline &amp;amp; MCP. No API keys
  <sub>★ 28 · TypeScript · MIT · npm · pushed 2026-08-30 · WSL2 · macOS? · Linux</sub>
  <sub>`npm i -g @claudinho/cli`</sub>
- **[TermaGITchi](https://github.com/TevvvB/termagitchi)** — by TevvvB - A Go CLI that gives each Claude Code session its own creature in the status line, derived by hashing the session id, with one den per git worktree. Where other status-line faces react to what the agent is doing, this one is a stable identity for telling parallel sessions apart, and its expression tracks repository hygiene: uncommitted files, unpushed commits, distance behind trunk and
  <sub>★ 14 · Go · MIT · scoop · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add tevvvb https://github.com/TevvvB/scoop-bucket scoop install termagitchi`</sub>
- **[tmux-claude-status-tabs](https://github.com/LiveNL/tmux-claude-status-tabs)** — by LiveNL - Shows each Claude Code session's state in the tmux tab bar, per window: an animated spinner while it works, amber when it waits on input, red on a permission request, green when done. Event-driven via hooks with no polling; catches unreported transitions (Esc, permission grants, stop-hook continuations) with transcript watchers. 260+ test assertions run in CI
  <sub>★ 3 · Shell · MIT · clone · pushed 2026-09-02 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/LiveNL/tmux-claude-status-tabs`</sub>

## Remote Control, Notifications &amp; Voice I/O

- **[Lockpaw](https://github.com/sorkila/lockpaw)** — by Erik Nielsen - A native-Swift macOS menu-bar app (10 MB, no Electron) that covers and input-locks your screen with one hotkey while your agents keep running, then makes the locked screen glow when Claude Code pauses for permission or finishes. Polished and well-engineered — CI with 50 tests, signed/notarized builds, an honest "visual privacy tool, not a security boundary" disclosure, no analyti
  <sub>★ 147 · Swift · MIT · brew · pushed 2026-08-24 · macOS</sub>
  <sub>`brew tap sorkila/lockpaw`</sub>
- **[WhatsApp Channel Plugin](https://github.com/Rich627/whatsapp-claude-plugin)** — by Richie Liu - Connects WhatsApp as a native Claude Code channel via Baileys linked-device (no bot token or API keys), with bidirectional messaging, full media, voice transcription, remote tool approval, access control, and per-group personalities. Runs entirely locally and was the first community plugin officially reviewed and published on Anthropic's plugin marketplace
  <sub>★ 79 · TypeScript · Apache-2.0 · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Rich627/whatsapp-claude-plugin.git`</sub>
- **[Claude Threads](https://github.com/anneschuth/claude-threads)** — by Anne Schuth - Streams a locally-running Claude Code session live into a Slack or Mattermost thread so a whole team can watch, type, and approve actions together — "screen-sharing for AI pair programming, but everyone can type." Mature and well-maintained (npm-published with CI and coverage), with reaction-based tool approvals, git-worktree isolation, multi-account rotation, and per-thread sessi
  <sub>★ 39 · TypeScript · Apache-2.0 · npm · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g claude-threads # with npm`</sub>
- **[Telegram-Claude (tg-claude)](https://github.com/Imolatte/claude-cli-telegram)** — by Imolatte - A feature-rich Telegram bot that turns your machine into a remote Claude Code terminal driven from your phone: streaming tool progress, voice input, a git panel, Mac remote control, and 30+ commands. Its standout is the approval flow — dangerous-op Approve/Deny taps are injected straight into the real terminal prompt via tmux send-keys, so you authorize from your phone without killin
  <sub>★ 32 · JavaScript · MIT · clone · pushed 2026-04-27 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Imolatte/claude-cli-telegram.git`</sub>
- **[ai-agent-notifier](https://github.com/DevinoSolutions/anotifier-for-claude-codex-cursor)** — by Amin Dhouib (Devino Solutions) - A zero-dependency, cross-platform notifier that fires a desktop toast and a free phone push (via ntfy) the moment Claude Code (or Codex/Cursor/Gemini) finishes a task or needs input, wired up by a one-command setup. The standout among notifiers is its testing rigor — CI drives the *real* agent CLIs end to end and asserts real ntfy round-trips and real OS toast d
  <sub>★ 27 · JavaScript · AGPL-3.0 · psh · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/DevinoSolutions/anotifier-for-claude-codex-cursor/main/setup/install.ps1 | iex`</sub>
- **[dictate](https://github.com/vimalk78/dictate)** — by Vimal Kumar - Local, offline voice-to-text for Claude Code on Linux built on faster-whisper, with a warm daemon for instant transcription, system-wide push-to-talk, a voice-enabled editor, and per-project vocabulary hints that fix technical terms ("Claude" not "cloud"). Fully private — no cloud, no API keys, with thoughtful touches like mic-health monitoring and the ability to offload transcrip
  <sub>★ 20 · Python · MIT · clone · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vimalk78/dictate.git`</sub>


---

Snapshot 2026-09-03. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
