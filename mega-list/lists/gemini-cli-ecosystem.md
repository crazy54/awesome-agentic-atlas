# Gemini CLI Ecosystem

A curated list of awesome tools, extensions, and resources for Gemini CLI.

Curated by **[Piebald-AI/awesome-gemini-cli](https://github.com/Piebald-AI/awesome-gemini-cli)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

177 entries · 162 distinct repos · 17 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/google-gemini/gemini-cli"><img src="https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/assets/gemini-screenshot.png" width="260"></a> | <a href="https://github.com/QwenLM/qwen-code/"><img src="https://img.alicdn.com/imgextra/i3/O1CN01l5GyhGuOPGC3XHtt_!!6000000005884-2-tps-1742-903.png" width="260"></a> | <a href="https://github.com/google-gemini/cookbook"><img src="https://opengraph.githubassets.com/1/google-gemini/cookbook" width="260"></a> |
| **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**<br>★ 107.2k | **[Qwen Code](https://github.com/QwenLM/qwen-code/)**<br>★ 28.1k | **[Gemini CLI cookbook](https://github.com/google-gemini/cookbook)**<br>★ 17.8k |
| <a href="https://github.com/iflow-ai/iflow-cli"><img src="https://raw.githubusercontent.com/iflow-ai/iflow-cli/main/assets/iflow-cli.jpg" width="260"></a> | <a href="https://github.com/google-github-actions/run-gemini-cli"><img src="https://opengraph.githubassets.com/1/google-github-actions/run-gemini-cli" width="260"></a> | <a href="https://github.com/vybestack/llxprt-code"><img src="https://opengraph.githubassets.com/1/vybestack/llxprt-code" width="260"></a> |
| **[iFlow CLI](https://github.com/iflow-ai/iflow-cli)**<br>★ 5.1k | **[Run Gemini CLI](https://github.com/google-github-actions/run-gemini-cli)**<br>★ 2.1k | **[LLxprt Code](https://github.com/vybestack/llxprt-code)**<br>★ 702 |

## Contents

- [Official](#official) (3)
- [Forks](#forks) (3)
- [Commands &amp; Extensions](#commands--extensions) (37)
- [Prompts](#prompts) (1)
- [MCP Servers](#mcp-servers) (33)
- [Agent Orchestration &amp; CLI Tools](#agent-orchestration--cli-tools) (22)
- [Frameworks](#frameworks) (5)
- [Development Tools &amp; Utilities](#development-tools--utilities) (40)
- [Interfaces](#interfaces) (6)
- [Fun](#fun) (1)
- [Browser Extensions](#browser-extensions) (1)
- [Neovim Plugins](#neovim-plugins) (3)
- [API Bridges &amp; Proxies](#api-bridges--proxies) (9)
- [SDKs](#sdks) (2)
- [Non-Gemini CLI](#non-gemini-cli) (3)
- [Documentation &amp; Examples](#documentation--examples) (7)
- [Education &amp; Study Tools](#education--study-tools) (1)

## Official

- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — The official open-source AI agent that brings the power of Gemini directly into your terminal. Features context-aware coding assistance, file manipulation, and command execution capabilities
  <sub>★ 107.2k · TypeScript · Apache-2.0 · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @google/gemini-cli`</sub>
- **[Gemini CLI cookbook](https://github.com/google-gemini/cookbook)** — Official collection of examples and guides demonstrating best practices for using the Gemini API. Essential resource for developers getting started
  <sub>★ 17.8k · Jupyter Notebook · Apache-2.0 · source · pushed 2026-09-25</sub>
  <sub>`git clone https://github.com/google-gemini/cookbook.git`</sub>
- **[Run Gemini CLI](https://github.com/google-github-actions/run-gemini-cli)** — Official GitHub Action that seamlessly integrates Gemini into your CI/CD pipeline, enabling automated code reviews, testing, and documentation generation
  <sub>★ 2.1k · TypeScript · Apache-2.0 · gh-action · pushed 2026-08-21</sub>
  <sub>`uses: google-github-actions/run-gemini-cli@main # in .github/workflows/*.yml`</sub>

## Forks

- **[Qwen Code](https://github.com/QwenLM/qwen-code/)** — Fork by the team behind Qwen LLM. Uses Qwen instead of Gemini
  <sub>★ 28.1k · TypeScript · Apache-2.0 · psh · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.ps1 | iex`</sub>
- **[iFlow CLI](https://github.com/iflow-ai/iflow-cli)** — Powerful fork that extends Gemini CLI with repository analysis, context interpretation, and complex workflow automation. Perfect for teams needing advanced orchestration capabilities
  <sub>★ 5.1k · Shell · npm · pushed 2026-03-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm i -g @iflow-ai/iflow-cli`</sub>
- **[LLxprt Code](https://github.com/vybestack/llxprt-code)** — An open-source multi-provider (including local) fork of Gemini CLI. Use whatever LLM you want to code in your terminal
  <sub>★ 702 · TypeScript · Apache-2.0 · npm · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @vybestack/llxprt-code`</sub>

## Commands &amp; Extensions

- **[AIHawk](https://github.com/feder-cr/invisible_playwright_mcp)** — Gives Gemini CLI a real Firefox to drive from plain-English instructions: opens pages, clicks, types, reads and screenshots through the real pointer and keyboard. Open source, MIT. Install via gemini extensions install https://github.com/feder-cr/AIHawk
  <sub>★ 31.7k · Python · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/feder-cr/AIHawk.git`</sub>
- **[Conductor](https://github.com/gemini-cli-extensions/conductor)** — Conductor is a Gemini CLI extension that allows you to specify, plan, and implement software features
  <sub>★ 3.7k · Python · Apache-2.0 · clone · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gemini-cli-extensions/conductor.git`</sub>
- **[brooks-lint](https://github.com/hyhmrright/brooks-lint)** — AI code reviews grounded in six classic engineering books. Diagnoses decay risks with structured findings (Symptom → Source → Consequence → Remedy)
  <sub>★ 1.5k · HTML · MIT · script · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/hyhmrright/brooks-lint/main/scripts/install.sh | bash -s -- <platform>`</sub>
- **[Pickle Rick](https://github.com/galdawave/pickle-rick-extension)** — This extension transforms the Gemini CLI into "Pickle Rick," a hyper-intelligent, arrogant, yet extremely competent engineering persona. It enforces a rigid, iterative software development lifecycle through continuous AI agent loops
  <sub>★ 454 · TypeScript · Apache-2.0 · source · pushed 2026-05-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/galdawave/pickle-rick-extension.git`</sub>
- **[OpenAccountants](https://github.com/openaccountants/openaccountants)** — 371 tax classification skills across 134 countries. Classify bank statement transactions into VAT/GST, income tax, and social contribution categories with conservative defaults
  <sub>★ 407 · Python · AGPL-3.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openaccountants-mcp`</sub>
- **[gemini-flow](https://github.com/clduab11/gemini-flow)** — Transforms Gemini CLI into an autonomous AI development team using proven Claude-Flow patterns, enabling complex multi-agent workflows
  <sub>★ 387 · TypeScript · MIT · npm · pushed 2026-01-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @clduab11/gemini-flow`</sub>
- **[ru-text](https://github.com/talkstream/ru-text)** — Russian text quality — ~1,040 rules for typography, info-style, editorial, UX writing, business correspondence
  <sub>★ 239 · Shell · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add talkstream/ru-text`</sub>
- **[gemini-cli-custom-slash-commands](https://github.com/amitkmaraj/gemini-cli-custom-slash-commands)** — Curated collection of productivity-boosting custom slash commands that extend Gemini CLI with specialized workflows and shortcuts
  <sub>★ 168 · source · pushed 2025-07-31</sub>
  <sub>`git clone https://github.com/amitkmaraj/gemini-cli-custom-slash-commands.git`</sub>
- **[wiki](https://github.com/plasma-ai/wiki)** — Indexed Markdown knowledge bases with a CLI and installable Agent Skill. wiki install writes the skill to ~/.agents/skills, which Gemini CLI discovers
  <sub>★ 102 · Python · Apache-2.0 · pip · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install plasma-wiki`</sub>
- **[LintLang](https://github.com/hermes-labs-ai/lintlang)** — Static linter and Gemini CLI extension for agent instructions, tool descriptions, and prompt configuration
  <sub>★ 90 · Python · Apache-2.0 · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx lintlang scan AGENTS.md`</sub>
- **[ATXP](https://github.com/atxp-dev/atxp)** — Give your Gemini CLI agent a wallet, email address, phone number, and 100+ paid MCP tools (web search, image gen, SMS, voice, LLM gateway). Self-register with gemini extensions install https://github.com/atxp-dev/atxp — no human login required, $5 free credits included
  <sub>★ 40 · TypeScript · MIT · npx · pushed 2026-03-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx atxp@latest`</sub>
- **[iOS Agent Skill](https://github.com/Nagarjuna2997/ios-agent-skill)** — Gemini CLI extension with Swift development guidance, read-only code review tools, and local Apple source/reference retrieval
  <sub>★ 35 · HTML · MIT · source · pushed 2026-09-22 · macOS?</sub>
  <sub>`git clone https://github.com/Nagarjuna2997/ios-agent-skill.git`</sub>
- **[gemini-beads](https://github.com/thoreinstein/gemini-beads)** — Git-backed persistent memory and task management for Gemini CLI
  <sub>★ 26 · MIT · source · pushed 2026-02-25</sub>
  <sub>`git clone https://github.com/thoreinstein/gemini-beads.git`</sub>
- **[xberg-io plugins](https://github.com/xberg-io/plugins)** — A suite of Gemini CLI extensions from Kreuzberg, Inc.: document extraction (xberg — 97+ formats with OCR), web crawling (crawlberg), HTML→Markdown, a universal LLM client for 143 providers (liter-llm), and code intelligence for 300+ languages (tree-sitter-language-pack). Install via gemini extensions install
  <sub>★ 26 · JavaScript · MIT · pip · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install xberg-hermes-plugin`</sub>
- **[gemini-notifier](https://github.com/thoreinstein/gemini-notifier)** — A Gemini extension to send native system-level notifications when Gemini requests permissions
  <sub>★ 25 · JavaScript · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/thoreinstein/gemini-notifier.git`</sub>
- **[dRPC Agent Skills](https://github.com/drpcorg/drpc-agent-skills)** — Query blockchain RPCs from Gemini CLI. Fetch balances, read contracts, and check gas prices via dRPC
  <sub>★ 23 · TypeScript · MIT · clone · pushed 2026-06-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/drpcorg/drpc-agent-skills.git`</sub>
- **[Screenshare](https://github.com/automateyournetwork/GeminiCLI_ScreenShare_Extension)** — Screen sharing via MCP and custom slash commands
  <sub>★ 21 · Python · Apache-2.0 · source · pushed 2025-10-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/GeminiCLI_ScreenShare_Extension.git`</sub>
- **[GeminiCLI_Slash_Listen](https://github.com/automateyournetwork/GeminiCLI_Slash_Listen)** — Innovative /listen command enabling remote Gemini CLI access through Slack, perfect for collaborative coding and remote assistance scenarios
  <sub>★ 21 · JavaScript · Apache-2.0 · clone · pushed 2025-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/GeminiCLI_Slash_Listen`</sub>
- **[Packet Buddy](https://github.com/automateyournetwork/GeminiCLI_Packet_Buddy_Extension)** — A Gemini CLI extension that uses RAG and MCP and Custom Slash Commands to analyze packet captures
  <sub>★ 20 · Python · Apache-2.0 · source · pushed 2025-11-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/GeminiCLI_Packet_Buddy_Extension.git`</sub>
- **[llm-box](https://github.com/alib8b8/aflare)** — Terminal-first workflow automation engine. Generate and execute YAML workflows from plain English. 20+ built-in nodes (fetch_url, execute, file I/O, HTTP, JSON parsing, template rendering, LLM calls), 15+ LLM providers, and MCP server mode. Install via gemini extensions install https://github.com/alib8b8/llm-box
  <sub>★ 16 · Go · psh · pushed 2026-09-08 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/alib8b8/aflare/main/install.ps1 | iex`</sub>
- **[gemini-cli-on-vscode](https://github.com/d3j/gemini-cli-on-vscode)** — MAGUS Council: World's first? 4-AI consultation system (Gemini+Claude+GPT-5+Qwen) in VS Code - Revolutionary multi-agent development environment
  <sub>★ 16 · TypeScript · MIT · source · pushed 2025-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/d3j/gemini-cli-on-vscode.git`</sub>
- **[Listen](https://github.com/automateyournetwork/GeminiCLI_Listen_Extension)** — Run Gemini CLI as a server with /listen commands
  <sub>★ 14 · Python · Apache-2.0 · source · pushed 2025-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/GeminiCLI_Listen_Extension.git`</sub>
- **[pyATS](https://github.com/automateyournetwork/pyATS_GeminiCLI_Extension)** — pyATS integration for network testing
  <sub>★ 10 · Python · Apache-2.0 · source · pushed 2025-12-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/pyATS_GeminiCLI_Extension.git`</sub>
- **[Clera](https://github.com/getclera/mcp)** — Gemini CLI extension for hiring: search 210,000+ vetted startup candidates, review Clera's picks for your open roles and request intros through Clera's hosted OAuth MCP server
  <sub>★ 9 · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-remote https://mcp.getclera.com`</sub>
- **[Task Monitor](https://github.com/davidwiet/task-monitor)** — Prevents agent loops via message tracking and plays auditory notifications for long tasks or out-of-focus prompts
  <sub>★ 8 · Python · source · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/davidwiet/task-monitor.git`</sub>
- **[Subnet calculator](https://github.com/automateyournetwork/GeminiCLI_SubnetCalculator_Extension)** — An extension for GeminiCLI that performs subnet calculation
  <sub>★ 5 · Python · Apache-2.0 · source · pushed 2025-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/GeminiCLI_SubnetCalculator_Extension.git`</sub>
- **[TokRepo Search Skill](https://github.com/henu-wang/tokrepo-search-skill)** — Cross-platform TokRepo skill with Gemini extension files for finding and installing AI assets such as prompts, MCP configs, workflows, and reusable skills
  <sub>★ 5 · MIT · npx · pushed 2026-04-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx tokrepo search "mcp database"`</sub>
- **[gemini-discord](https://github.com/Yamato-main/gemini-discord)** — Turn your local Gemini CLI agent into an always-on Discord presence that also doubles as your personal server admin
  <sub>★ 5 · TypeScript · MIT · clone · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Yamato-main/gemini-discord`</sub>
- **[16-eyes](https://github.com/kigiela/16-eyes)** — AI-driven security audits via custom Gemini CLI commands and subagents (also supports Claude Code, Cursor, GitHub Copilot) — profiles the repo, verifies every finding, adversarially disproves high-impact ones before they reach the report. Install via npx 16-eyes install --target gemini
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx 16-eyes install`</sub>
- **[ArmorGemini](https://github.com/armoriq/armorGemini)** — Intent-based security enforcement for the Gemini CLI. Every tool call is checked against your ArmorIQ policy via BeforeTool / AfterTool hooks before it runs. Blocks intent drift, unauthorized tool use, and PII/PCI leaks. Install: curl -fsSL https://armoriq.ai/install_armorgemini.sh | bash
  <sub>★ 4 · JavaScript · MIT · script · pushed 2026-09-15 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://armoriq.ai/install_armorgemini.sh | bash`</sub>
- **[Knowledge Delta Skills](https://github.com/sergeyizmailov/knowledge-delta-skills)** — Portable SKILL.md skills for media buying, frontend, security, research, and skill authoring, each kept to what a frontier model does not already reliably know. Copy any skill directory into ~/.gemini/skills/ and Gemini CLI discovers it
  <sub>★ 3 · Python · MIT · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sergeyizmailov/knowledge-delta-skills.git`</sub>
- **[SuperSearch](https://github.com/hermes-labs-ai/supersearch)** — Local Python CLI/library that fans out bounded searches across web, code, community, and research sources and returns source-explicit JSON receipts
  <sub>★ 2 · Python · Apache-2.0 · npx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add hermes-labs-ai/supersearch --skill supersearch`</sub>
- **[Punchcard](https://github.com/Maksim-Burtsev/punchcard)** — Architecture-level code review grounded in thirty engineering books distilled into 78 principles. Three independent passes over a working tree, branch or PR, merged into one verdict; every blocker demonstrated by running the code. Install with npx skills add Maksim-Burtsev/punchcard -a gemini-cli
  <sub>★ 1 · Python · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Maksim-Burtsev/punchcard`</sub>
- **[kgai](https://github.com/kgaidev/kgai-gemini)** — Shared decision memory for AI dev teams: your agent records why the code changed (and the dead ends it ruled out), recalls it before the next edit, and syncs it across the team without merge conflicts. Local-first, immutable, engine installs itself on first run
  <sub>★ 1 · Shell · MIT · source · pushed 2026-09-18 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kgaidev/kgai-gemini.git`</sub>
- **[isitdone](https://github.com/raimondasl/isitdone-gemini)** — Gemini CLI extension that refuses to let the agent end its turn claiming "done" until the repository's real test, typecheck and lint commands pass. An AfterAgent hook runs them on the exact working tree and feeds the failing output back; an AfterTool hook warns when an edit weakened a test. No LLM calls, no network. Install via gemini extensions install https://github.com/raimondasl/isitdone-gemin
  <sub>★ 1 · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx isitdone doctor`</sub>
- **[GTD Brain](https://github.com/minosin/gtdbrain-gemini-extension)** — Getting Things Done (GTD) task board for Gemini CLI: capture to your Inbox, next actions by context, projects, Waiting For and a guided weekly review over a hosted MCP server, plus a GEMINI.md context file and /gtd:* commands. Sign in with an email code, no API key; same board as the GTD Brain web, iOS and Android apps. Install: gemini extensions install https://github.com/minosin/gtdbrain-gemini-
  <sub>★ 1 · MIT · source · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/minosin/gtdbrain-gemini-extension.git`</sub>
- **[Cohesivity](https://github.com/cohesivity-org/cohesivity-plugin/tree/main/packages/gemini)** — cohesivity.ai offers free agent native backend services. Anonymous account (no-signup) to get started through MCP or API. Hosting, postgres, email, storage, containers, LLMs, voice and third-party APIs. Includes free tiers and 5 USD/mo in AI and Search credits. Top-ups through x402
  <sub>JavaScript · MIT · in-repo · pushed 2026-09-25</sub>
  <sub>`git clone https://github.com/cohesivity-org/cohesivity-plugin.git && cd cohesivity-plugin/packages/gemini`</sub>

## Prompts

- **[gemini-cli-prompt-library](https://github.com/harish-garg/gemini-cli-prompt-library)** — 30+ professional prompts for Gemini CLI
  <sub>★ 412 · clone · pushed 2025-10-10</sub>
  <sub>`git clone https://github.com/yourusername/prompt-library-extension.git`</sub>

## MCP Servers

- **[Unity-MCP](https://github.com/IvanMurzak/Unity-MCP)** — Open-source MCP server connecting AI agents (including Gemini CLI) to the Unity Editor and runtime, with 100+ built-in tools
  <sub>★ 4.3k · C# · Apache-2.0 · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g unity-mcp-cli`</sub>
- **[gemini-mcp-tool](https://github.com/jamubc/gemini-mcp-tool)** — Leverages Gemini's industry-leading 2M token context window through MCP, enabling analysis of entire codebases and large documents that other tools can't handle
  <sub>★ 2.3k · TypeScript · source · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jamubc/gemini-mcp-tool.git`</sub>
- **[deja-vu](https://github.com/vshulcz/deja-vu)** — Local memory over the session files Gemini CLI and 19 other agents already write to disk, so a new session can search what you did before — including the months before you installed it. MCP tools plus auto-recall on every prompt; one Go binary, no network calls, MIT. Install: deja install gemini-auto
  <sub>★ 1k · Go · MIT · scoop · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop install deja-vu`</sub>
- **[Agent QA](https://github.com/vostride/agent-qa)** — Source-available (FSL-1.1-ALv2) QA agent for natural-language web and mobile tests. Run agent-qa mcp for authoring, execution, artifacts, and failure triage; dashboard-backed tools need a running dashboard and dashboardUrl. Model and infrastructure costs are separate
  <sub>★ 889 · TypeScript · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-qa init`</sub>
- **[Vestige](https://github.com/samvallad33/vestige)** — Memory system for coding agents: backfill ranks earlier records as candidate causes of a fresh failure even when they share no vocabulary with it, the composed graph records which memories were used together and surfaces never-tried combinations, retrieval decays on an FSRS-6 schedule, and receipts fail closed after compaction. Single Rust binary, local only. Install: gemini extensions install htt
  <sub>★ 635 · Rust · AGPL-3.0 · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g vestige-mcp-server@latest`</sub>
- **[squirrelscan](https://github.com/squirrelscan/squirrelscan)** — Website audit MCP server for coding agents: run audits, read reports, and fix findings from Gemini CLI or any MCP client. 260+ rules across SEO, performance, security, accessibility, and agent experience, with fixes mapped to source. MIT CLI with a local stdio server (squirrel mcp) or hosted Remote MCP with OAuth: gemini mcp add --transport http squirrelscan https://mcp.squirrelscan.com/mcp
  <sub>★ 267 · TypeScript · MIT · npm · pushed 2026-09-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g squirrelscan`</sub>
- **[Godot-MCP](https://github.com/IvanMurzak/Godot-MCP)** — Open-source MCP server connecting AI agents to the Godot Editor and runtime (Godot 4.x, C#)
  <sub>★ 254 · C# · Apache-2.0 · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g godot-cli`</sub>
- **[Xquik MCP](https://github.com/Xquik-dev/x-twitter-scraper)** — X/Twitter data MCP server with 76 REST API endpoints, 20 extraction tools, account monitoring, and giveaway draws. Works with any MCP client including Gemini CLI
  <sub>★ 206 · JavaScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx skills@1.5.3 add Xquik-dev/x-twitter-scraper`</sub>
- **[KubeStellar Console kc-agent](https://github.com/kubestellar/console)** — Multi-cluster Kubernetes MCP server bridging Gemini CLI to kubeconfig and Kubernetes APIs. Manage clusters, policies, and 20+ CNCF project integrations across edge and cloud. Install via brew tap kubestellar/tap &amp;&amp; brew install kc-agent
  <sub>★ 139 · TypeScript · Apache-2.0 · brew · pushed 2026-09-26 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew tap kubestellar/tap`</sub>
- **[ToolsForMCPServer](https://github.com/tanaikech/ToolsForMCPServer)** — Bridges Gemini CLI with Google Workspace through Apps Script integration, automating document processing, spreadsheet manipulation, and workflow automation
  <sub>★ 106 · JavaScript · MIT · source · pushed 2026-01-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tanaikech/ToolsForMCPServer.git`</sub>
- **[mcp-gemini-cli](https://github.com/choplin/mcp-gemini-cli)** — A simple MCP (Model Context Protocol) server wrapper for Google's Gemini CLI
  <sub>★ 101 · TypeScript · clone · pushed 2025-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/choplin/mcp-gemini-cli`</sub>
- **[nika](https://github.com/supernovae-st/nika)** — Read-only oracle for Nika AI workflows: validate .nika.yaml DAGs, explain findings, browse schema/examples, honest cost estimate — before a single token is spent (single Rust binary, config: command nika, args [mcp])
  <sub>★ 89 · Rust · AGPL-3.0 · brew · pushed 2026-09-26 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew install supernovae-st/tap/nika`</sub>
- **[emem](https://github.com/Vortx-AI/emem)** — Shared, signed and content-addressed memory of the physical world that AI agents can read, cite, transfer and independently verify. 108 tools, no API key, no signup. Remote Streamable HTTP. Install: gemini extensions install https://emem.dev/gemini-extension.json
  <sub>★ 60 · Rust · Apache-2.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install ememdev`</sub>
- **[LWC](https://github.com/JanYork/llm-wiki-cli)** — Local-first, source-grounded project memory for Gemini CLI and other coding agents. Provides bounded recall, citations, atomic changesets, an installable Agent Skill, and a read-only stdio MCP server (lwc serve --mcp). Apache-2.0
  <sub>★ 56 · Rust · Apache-2.0 · source · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/JanYork/llm-wiki-cli.git`</sub>
- **[RunAPI MCP](https://github.com/runapi-ai/mcp)** — Remote MCP server for browsing model catalogs, checking pricing, and creating image, video, music, audio, and other model API tasks through RunAPI. Works with Gemini CLI: gemini mcp add --transport http runapi https://mcp.runapi.ai/mcp
  <sub>★ 55 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @runapi.ai/mcp init claude`</sub>
- **[Unreal-MCP](https://github.com/IvanMurzak/Unreal-MCP)** — Open-source MCP server connecting AI agents to Unreal Engine 5.7, editor and runtime (C++ plugin + .NET sidecar)
  <sub>★ 40 · C++ · Apache-2.0 · npm · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g unreal-mcp-cli`</sub>
- **[gemini-cli-mcp](https://github.com/InfolabAI/gemini-cli-mcp)** — Tool that enables using Gemini AI as an MCP server within Claude Code with large file analysis and token savings
  <sub>★ 30 · Python · MIT · clone · pushed 2025-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/InfolabAI/gemini-cli-mcp.git`</sub>
- **[prompt-to-asset](https://github.com/MohamedAbdallah-14/prompt-to-asset)** — MCP server that generates production-ready visual assets (app icons, favicons, OG images, logos, wordmarks) by routing requests across 30+ image generation models. Zero API key required for first run via Pollinations and Stable Horde free tiers. Works with any MCP client including Gemini CLI
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm i -g prompt-to-asset`</sub>
- **[GoodMemory](https://github.com/hjqcan/GoodMemory)** — Local-first durable memory for Gemini CLI through standalone MCP, with scoped recall, provenance and trace inspection, and explicit forgetting. Read-only by default with opt-in governed writes; install with npm install -g goodmemory@0.7.5 and follow the Gemini CLI setup guide
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g goodmemory@0.8.0`</sub>
- **[GameDev-MCP-Server](https://github.com/IvanMurzak/GameDev-MCP-Server)** — Open-source, engine-agnostic MCP server shared by Unity-MCP, Godot-MCP, and Unreal-MCP
  <sub>★ 13 · C# · Apache-2.0 · docker · pushed 2026-09-24 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -i --rm -p 8080:8080 aigamedeveloper/mcp-server`</sub>
- **[Lians](https://github.com/Lians-ai/Lians)** — Open-source, local-first memory for Gemini CLI and other AI agents. Durable cross-session recall through a two-tool MCP extension, with no account or API key. Install: gemini extensions install https://github.com/Lians-ai/Lians
  <sub>★ 12 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install "lians-sdk[local]"`</sub>
- **[gemini-mcp](https://github.com/neriousy/gemini-mcp)** — A simple MCP server for using the Gemini CLI
  <sub>★ 7 · TypeScript · MIT · clone · pushed 2025-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/gemini-mcp.git`</sub>
- **[dsh-skills-anywhere](https://github.com/noteflowai/dsh-skills-anywhere)** — MCP server that exposes every Agent Skill installed for Gemini CLI, Claude Code, Codex, Cursor and 60+ other agents, plus Claude Code plugin marketplaces and any GitHub skills repo, as find_skills/open_skill tools and skill:// resources, read in place with zero copies or symlinks
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx dsh-skills-anywhere@0.15.0 check path/to/SKILL.md --resources --json`</sub>
- **[Find MCP](https://github.com/agentage/find-mcp)** — Search 17,000+ MCP servers synced from the official MCP registry (registry.modelcontextprotocol.io). Remote Streamable HTTP (https://catalog.agentage.io/mcp, no auth for search) or stdio (npx -y @agentage/find-mcp). Works with Gemini CLI: gemini mcp add --transport http find-mcp https://catalog.agentage.io/mcp
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentage/find-mcp.git`</sub>
- **[Lusha](https://github.com/lusha-oss/lusha-mcp-plugin)** — B2B prospecting and data enrichment: find and enrich contacts and companies with verified emails, direct dials, mobile numbers, and real-time buying signals. Remote MCP server bundled with 4 prospecting skills and OAuth sign-in. Works with Gemini CLI (gemini extensions install) and Antigravity (agy plugin install)
  <sub>★ 4 · MIT · source · pushed 2026-08-06</sub>
  <sub>`git clone https://github.com/lusha-oss/lusha-mcp-plugin.git`</sub>
- **[Minds](https://github.com/minds-ai-co/minds-mcp)** — Synthetic market research: create AI audiences, interview them and run studies such as MaxDiff, conjoint and NPS. Remote MCP server with OAuth; installable as a Gemini CLI extension
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/minds-ai-co/minds-mcp.git`</sub>
- **[Mnemoverse Memory](https://github.com/mnemoverse/gemini-extension)** — Hosted memory shared across MCP clients: write a memory in Gemini CLI, recall it in Claude Code, Cursor, VS Code, or any other MCP client. Remote Streamable HTTP with OAuth sign-in, no API key to paste. Install: gemini extensions install https://github.com/mnemoverse/gemini-extension
  <sub>★ 2 · MIT · source · pushed 2026-09-26</sub>
  <sub>`git clone https://github.com/mnemoverse/gemini-extension.git`</sub>
- **[Glasser](https://github.com/glasser-ai/plugins)** — One key to 1,000+ paid third-party data APIs, pay per call: person and company enrichment, SEO and SERP, web scraping, places, news, scholar and social data. The agent searches the catalog, inspects the exact price, runs the endpoint and reports the charge; failed calls and empty results cost $0.00. Remote Streamable HTTP with OAuth sign-in. Works with Gemini CLI: gemini mcp add --transport http g
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @glasser-ai/cli`</sub>
- **[TokRepo MCP Server](https://github.com/henu-wang/tokrepo-mcp-server)** — Search and install AI skills, prompts, MCP configs, and workflows from TokRepo from Gemini CLI and other MCP clients
  <sub>JavaScript · MIT · npx · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx tokrepo init-agent --target all`</sub>
- **[TWZRD Agent Intel](https://intel.twzrd.xyz/mcp)** — Trust scoring and identity verification for AI agent wallets on Solana. Verify agent identity before x402 micropayments or agent-initiated operations. Free: score_agent, preflight_check. Paid (x402): get_trust_receipt. Works with any MCP client including Gemini CLI
  <sub>website</sub>
  <sub>`https://intel.twzrd.xyz/mcp`</sub>
- **[AISO Tools MCP](https://aisotools.com/mcp)** — Query a catalog of 1,636 AI tools from the CLI: keyword/category/pricing search, side-by-side comparison, and alternatives lookup, with a canonical citation URL on every result. Remote Streamable HTTP, no API key. Works with any MCP client including Gemini CLI: gemini mcp add --transport http aisotools https://aisotools.com/api/mcp
  <sub>website</sub>
  <sub>`https://aisotools.com/mcp`</sub>
- **[ContextStream](https://contextstream.io)** — Shared project context for Cursor, Claude Code, Codex, Grok. Intelligence isn’t the bottleneck. Context is. Remote MCP for Gemini CLI and other coding agents: https://mcp.contextstream.io/mcp
  <sub>website</sub>
  <sub>`https://contextstream.io`</sub>
- **[SkillAgent](https://skillagent.dev)** — Remote MCP server (Streamable HTTP, no auth) for searching ~3,500 agent skills, rules files (including Gemini rules) and MCP servers indexed hourly from GitHub, with project-based recommendations and per-agent install instructions for Gemini CLI. Install: gemini mcp add --transport http skillagent https://skillagent.dev/mcp
  <sub>website</sub>
  <sub>`https://skillagent.dev`</sub>

## Agent Orchestration &amp; CLI Tools

- **[Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS)** — Local-first Agent Operation Environment (AOE) that installs into Gemini CLI and other supported hosts to build, route, and run specialist agent teams with portable packages, permissions, and verification gates
  <sub>★ 1.5k · Python · Apache-2.0 · psh · pushed 2026-09-25 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://agentlas.cloud/install.ps1 | iex`</sub>
- **[Bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Multi-agent orchestrator that coordinates Gemini CLI alongside Claude Code and Codex CLI. Spawns parallel coding agents from a single goal, verifies with tests, auto-commits. Deterministic Python coordination, zero LLM tokens on orchestration
  <sub>★ 1.3k · Python · Apache-2.0 · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[Parallel Code](https://github.com/johannesjo/parallel-code)** — Desktop app for orchestrating multiple AI coding agents (Claude Code, Codex CLI, Gemini CLI) simultaneously in isolated git worktrees
  <sub>★ 1k · TypeScript · MIT · clone · pushed 2026-09-26 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/johannesjo/parallel-code.git`</sub>
- **[hcom](https://github.com/aannoo/hcom)** — Let AI agents message, watch, and spawn each other across terminals. First-class Gemini CLI support with hooks integration and PTY wrapper. Also works with Claude Code, Codex, and OpenCode
  <sub>★ 520 · Rust · MIT · psh · pushed 2026-09-26 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://github.com/aannoo/hcom/releases/latest/download/hcom-installer.ps1 | iex`</sub>
- **[AgentBox](https://github.com/madarco/agentbox)** — Run multiple coding agents (Gemini CLI, Claude Code, Codex, OpenCode) in parallel, each teleported into its own sandboxed VM — local Docker, self-hosted, or cloud (Hetzner, Daytona, Vercel, E2B, DigitalOcean). Sub-1s checkpoint startup; git credentials stay on the host. MIT
  <sub>★ 491 · TypeScript · MIT · clone · pushed 2026-09-24 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/madarco/agentbox`</sub>
- **[Ivy Tendril](https://github.com/Ivy-Interactive/Ivy-Tendril)** — Open-source desktop app that orchestrates Gemini CLI alongside Claude Code, Codex, and Copilot through a plan-based lifecycle with verification gates, self-improving memory, and git worktree isolation. Local-first, agent-agnostic, FSL licensed
  <sub>★ 198 · C# · psh · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://cdn.ivy.app/install-tendril.ps1 | iex`</sub>
- **[SandBase CLI](https://github.com/sandbaseai/cli)** — Open-source CLI and MCP bridge that configures Gemini CLI and other AI coding agents to access 2,000+ AI models and APIs through one account
  <sub>★ 188 · TypeScript · Apache-2.0 · npx · pushed 2026-08-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y https://github.com/sandbaseai/cli/releases/download/v0.1.17/sandbaseai-cli-0.1.17.tgz connect`</sub>
- **[clideck](https://github.com/rustykuntz/clideck)** — WhatsApp-like dashboard for managing multiple AI coding agents (including Gemini CLI) in one browser window. Live status, session resume, autopilot that routes work between agents while afk, mobile remote to check in from a phone
  <sub>★ 159 · JavaScript · MIT · npm · pushed 2026-09-22 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g clideck@2`</sub>
- **[Untether](https://github.com/littlebearapps/untether)** — Telegram bridge for Gemini CLI (and 5 other agents). Send tasks by voice, stream progress, configure approval mode (read-only/edit files/full access) via inline buttons. Self-hosted, MIT licensed
  <sub>★ 70 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install untether # recommended`</sub>
- **[YYLO](https://github.com/yylo-dev/yylo)** — Kanban-driven CLI orchestrator that runs Gemini CLI alongside Claude Code and Codex in parallel across isolated git worktrees, with a merge queue that reviews and merges verified task work. Git-native task state, per-agent worktree isolation, installable via npm. MIT
  <sub>★ 61 · Python · MIT · npm · pushed 2026-09-25 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install --global '@yylo/cli@latest'`</sub>
- **[squads-cli](https://github.com/agents-squads/squads-cli)** — Open source CLI for AI agent coordination that organizes agents into domain-aligned squads with persistent memory, goal tracking, and Git-native state. Works with Gemini CLI
  <sub>★ 53 · TypeScript · MIT · npm · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g squads-cli`</sub>
- **[intentic](https://github.com/intentic/intentic)** — Self-hosted workspace that runs Gemini CLI over ACP (gemini --experimental-acp) alongside Claude Code, Codex, and OpenCode. Each agent gets its own Docker container and git worktree on hardware you own; terminals survive disconnects, any browser or phone reopens the same fleet, and changes land through per-file, per-hunk diff review. Scheduled and webhook-triggered runs. MIT
  <sub>★ 46 · TypeScript · MIT · source · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/intentic/intentic.git`</sub>
- **[wolfpack](https://github.com/almogdepaz/wolfpack)** — Mobile &amp; desktop command center for controlling AI coding agents (Claude, Codex, Gemini) across machines from your phone. Secured by Tailscale. Self-hosted
  <sub>★ 40 · TypeScript · MIT · npx · pushed 2026-09-24 · WSL2 · macOS · Linux</sub>
  <sub>`bunx --bun wolfpack-bridge@latest`</sub>
- **[godmode](https://github.com/arbazkhan971/godmode)** — Discipline layer for AI coding agents: 135 skills and 7 subagents that wrap Gemini CLI (and Claude Code, Codex, Cursor, OpenCode, Amp, and pi) in a measure → modify → verify → keep/revert loop with automatic rollback of failed changes. MIT
  <sub>★ 26 · Shell · MIT · source · pushed 2026-08-28 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/arbazkhan971/godmode.git`</sub>
- **[Ralph Harness](https://github.com/rxdt/loopgate_harness)** — Tiny Python scaffold for running Gemini CLI, Claude Code, Codex CLI, and similar coding agents in guarded local loops. It uses repo-local specs, fresh-context iterations, hard caps, git-hook gates, CI verification, and coverage gates
  <sub>★ 23 · Python · MIT · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rxdt/py_ralph_frame.git`</sub>
- **[ToutKit](https://github.com/NextProb/nextprob)** — Desktop notebook with a built-in terminal that runs Gemini CLI alongside Claude Code and Codex; an in-app webview renders whatever the agent writes inline, and each note is a self-contained folder with its own SQLite, files, and scripts. Local-first, Electron, AGPL-3.0
  <sub>★ 9 · JavaScript · AGPL-3.0 · clone · pushed 2026-09-22 · Win? · macOS</sub>
  <sub>`git clone https://github.com/nextprob/nextprob.git`</sub>
- **[PickySteve](https://github.com/KernelLord/pickysteve)** — Skill router and context picker for coding agents: a local model (via Ollama, offline by default) routes each prompt to the right skill via hybrid BM25 + embedding retrieval, cross-encoder rerank, and an LLM judge, then assembles a minimal context bundle for the execution model. Built-in prompt-injection gate scans every retrieved document, fail-closed. Ships an MCP stdio server and an OpenAI-comp
  <sub>★ 9 · Python · MIT · uv · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx pickysteve`</sub>
- **[loopguard](https://github.com/ruslanlap/loopguard)** — Watchdog that tails Gemini CLI session transcripts and alerts when the agent loops, oscillates, or stalls — Telegram notifications, zero dependencies
  <sub>★ 3 · Python · MIT · source · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ruslanlap/loopguard.git`</sub>
- **[DevIntern](https://github.com/getdevintern/devintern)** — Tool that picks up tickets from Jira, Linear, Trello, Asana, Azure DevOps, GitHub Issues, or markdown files and turns them into self-reviewed pull requests by driving Gemini CLI non-interactively (also supports Claude Code, Codex, and others). A feasibility gate flags vague tickets back to the tracker with questions; optional unattended mode schedules ticket pickup and turns PR review comments int
  <sub>★ 3 · TypeScript · bun · pushed 2026-09-26 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`bun install -g @getdevintern/code`</sub>
- **[postmortemthis](https://github.com/Softeria/postmortemthis)** — Runs Gemini CLI alongside your other coding agents (Claude Code, Codex, Qwen, Vibe) in parallel and read-only over your diff, then synthesizes their reviews into one ship / no-ship verdict. A cross-model review panel
  <sub>★ 1 · Rust · MIT · source · pushed 2026-08-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Softeria/postmortemthis.git`</sub>
- **[Tars](https://tars.saccolabs.com)** — A local-first autonomous supervisor and sidekick powered by Google Gemini. Features background persistence (heartbeat), tiered local memory, multi-channel notifications (Discord/WhatsApp), and self-healing background services. Designed for reliable, long-running agentic orchestration in the terminal
  <sub>website</sub>
  <sub>`https://tars.saccolabs.com`</sub>
- **[VibeFuse](https://fuseintelligence.org/products/vibefuse)** — Free Windows desktop harness that runs Gemini CLI alongside Claude Code, Codex, Cursor, and Qwen as live draggable widgets on one canvas, with named sessions, local Whisper/Piper voice, an MCP tool panel, and a marketplace where skill and widget sellers keep 80% (Stripe Connect)
  <sub>website</sub>
  <sub>`https://fuseintelligence.org/products/vibefuse`</sub>

## Frameworks

- **[Maestro](https://github.com/josstei/maestro-orchestrate)** — Turn Gemini CLI into a multi-agent platform — 12 specialized subagents, parallel dispatch, 4-phase orchestration, and standalone dev tools for code review, debugging, security, and performance
  <sub>★ 462 · JavaScript · Apache-2.0 · clone · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/josstei/maestro-orchestrate`</sub>
- **[gemini-code-flow](https://github.com/Theopsguide/gemini-code-flow)** — Enterprise-grade orchestration framework that coordinates multiple Gemini CLI instances for complex development tasks, based on battle-tested Claude Code Flow patterns
  <sub>★ 159 · TypeScript · npm · pushed 2025-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g gemini-code-flow`</sub>
- **[GACUA](https://github.com/openmule/gacua)** — The world's first out-of-the-box computer use agent powered by Gemini CLI @openmule
  <sub>★ 139 · TypeScript · Apache-2.0 · npm · pushed 2025-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @gacua/backend`</sub>
- **[gemini-cli-commands-demo](https://github.com/pauldatta/gemini-cli-commands-demo)** — A proof-of-concept demonstrating a sub-agent orchestration system built within the Gemini CLI
  <sub>★ 91 · Shell · source · pushed 2025-07-31</sub>
  <sub>`git clone https://github.com/pauldatta/gemini-cli-commands-demo.git`</sub>
- **[Emdash Skills](https://github.com/heymegabyte/claude-skills)** — 14-category autonomous product-building OS with 18 specialized agents. Turns one-line prompts into deployed products. Includes GEMINI.md compatibility for cross-tool portability. Skills cover architecture, planning, quality, brand, media, observability, and deployment on Cloudflare Workers
  <sub>★ 22 · TypeScript · npx · pushed 2026-09-25 · macOS</sub>
  <sub>`npx jsr add @heymegabyte/claude-skills`</sub>

## Development Tools &amp; Utilities

- **[Nix AI Tools](https://github.com/numtide/llm-agents.nix)** — Seamless Nix integration for reproducible Gemini CLI installations. Ensures consistent environments across teams and simplifies deployment with declarative configuration
  <sub>★ 2k · Nix · MIT · source · pushed 2026-09-26 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/numtide/nix-ai-tools.git`</sub>
- **[Rulesync](https://github.com/dyoshikawa/rulesync)** — The Node.js CLI tool that automatically generates configs (rules, ignore files, MCP servers, commands, and subagents) for various AI coding agents. Rulesync can convert configs between Gemini CLI and other AI agents in both directions
  <sub>★ 1.5k · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g rulesync`</sub>
- **[ccmanager](https://github.com/kbwo/ccmanager)** — Essential session management tool that saves, restores, and organizes multiple Gemini CLI sessions, perfect for juggling multiple projects or experiments
  <sub>★ 1.2k · TypeScript · MIT · npm · pushed 2026-09-26 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g ccmanager`</sub>
- **[Agent Sessions](https://github.com/jazzyalex/agent-sessions)** — Local-first macOS app to search, browse, and resume Gemini CLI sessions alongside Codex CLI, Claude Code, OpenCode, and other agents, with live iTerm2 monitoring via Agent Cockpit
  <sub>★ 878 · Swift · MIT · brew · pushed 2026-09-23 · Win? · macOS</sub>
  <sub>`brew install --cask jazzyalex/agent-sessions/agent-sessions`</sub>
- **[agnix](https://github.com/agent-sh/agnix)** — Linter for AI agent configurations. Validates GEMINI.md, SKILL.md, hooks, MCP, and more with 156 rules, auto-fix, and LSP server for real-time editor diagnostics
  <sub>★ 426 · Rust · Apache-2.0 · npm · pushed 2026-09-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agnix`</sub>
- **[ClawMetry](https://github.com/vivekchand/clawmetry)** — Self-hosted, local-first observability and kill switch for coding agents, reading Gemini CLI sessions alongside Claude Code, Codex, Cursor, OpenClaw, Aider, Goose, and others. Reads the session logs the runtimes already write on disk, so there is no SDK and nothing in the request path. Shows sessions, transcripts, tool calls, tokens, and cache-aware cost per session and model; an opt-in emergency
  <sub>★ 420 · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vivekchand/clawmetry --skill agent-kill-switch`</sub>
- **[Splitrail](https://github.com/Piebald-AI/splitrail)** — Comprehensive usage analytics platform that tracks and optimizes your Gemini CLI workflows, helping teams understand and improve their AI-assisted development patterns
  <sub>★ 222 · Rust · MIT · source · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Piebald-AI/splitrail.git`</sub>
- **[Lockpaw](https://github.com/sorkila/lockpaw)** — macOS menu bar screen guard for unattended Gemini CLI runs. One hotkey covers the screen and blocks input while the agent keeps running (no sleep), and the locked screen glows plus fires a notification when Gemini CLI needs input or finishes, via a lockpaw ping hook. Touch ID unlock. Also works with Claude Code and Codex. Native Swift, free, open source
  <sub>★ 153 · Swift · MIT · brew · pushed 2026-09-15 · macOS</sub>
  <sub>`brew tap sorkila/lockpaw`</sub>
- **[unslop](https://github.com/MohamedAbdallah-14/unslop)** — CLI and MCP server that removes AI writing patterns from text: tricolons, em-dash overuse, hedging stacks, sycophancy openers, and overused vocabulary. Works with any MCP client including Gemini CLI. Five intensity levels and a lint-only audit mode. Useful for cleaning commit messages, PR descriptions, and documentation
  <sub>★ 147 · Python · MIT · pipx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install unslop`</sub>
- **[agenttrace](https://github.com/luoyuctl/agenttrace)** — Local-first TUI for Gemini CLI and AI coding agent session observability. Parses local logs for cost, tokens, tool failures, latency, anomalies, health gates, and diffs across Gemini CLI, Claude Code, Codex CLI, Aider, Cursor exports, OpenCode, and more
  <sub>★ 136 · Rust · MIT · winget · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install --id Luoyuctl.AgentTrace --exact`</sub>
- **[Terminal Jarvis](https://github.com/BA-CalderonMorales/terminal-jarvis)** — Ultimate command center unifying multiple AI coding assistants in one elegant interface. Switch between tools seamlessly and manage sessions efficiently
  <sub>★ 135 · Rust · MIT · npm · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`npm install -g terminal-jarvis`</sub>
- **[authsome](https://github.com/agentrhq/authsome)** — Local credential broker for AI agents. OAuth2 and API key vault stored locally, a loopback HTTPS proxy injects credentials into outbound provider requests so the Gemini CLI agent never sees raw secrets. 45 providers bundled (GitHub, Google, OpenAI, Linear, Slack, Notion, Resend, Stripe, ...). Python 3.13+, MIT
  <sub>★ 92 · Python · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add agentrhq/authsome`</sub>
- **[Hexis](https://github.com/Bevel-Software/Hexis)** — Git-backed platform for skills, tools, and context for AI agents, available to Gemini CLI through a remote OAuth MCP server
  <sub>★ 90 · TypeScript · Apache-2.0 · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @bevel-software/hexis-mcp`</sub>
- **[Archcore](https://github.com/archcore-ai/archcore)** — Git-native context engineering CLI and MCP server for AI coding agents; archcore init --agent gemini-cli wires Gemini CLI hooks and MCP
  <sub>★ 64 · Shell · Apache-2.0 · psh · pushed 2026-09-26 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://archcore.ai/install.ps1 | iex # Windows, PowerShell 5.1+`</sub>
- **[vsync](https://github.com/nicepkg/vsync)** — Sync Skills, MCP servers, Agents &amp; Commands across Claude Code, Cursor, OpenCode, Codex, and Gemini CLI with automatic format conversion (JSON ↔ TOML ↔ JSONC)
  <sub>★ 61 · TypeScript · MIT · npm · pushed 2026-01-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @nicepkg/vsync`</sub>
- **[EGC](https://github.com/Fmarzochi/EGC)** — Persistent cross-session memory for Gemini CLI and 12 other AI coding tools. SQLite-backed state survives context resets, install with npm install -g @egchq/egc
  <sub>★ 56 · JavaScript · Apache-2.0 · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @egchq/egc`</sub>
- **[andrej-karpathy-skills](https://github.com/swarmclawai/andrej-karpathy-skills)** — Npm installer for Karpathy-inspired GEMINI.md guidelines, plus adapters for Codex, Claude Code, Cursor, OpenCode, OpenClaw, Windsurf, and Aider
  <sub>★ 50 · JavaScript · MIT · npm · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @swarmclawai/andrej-karpathy-skills`</sub>
- **[codebase-recon](https://github.com/yujiachen-y/codebase-recon-skill)** — AI agent skill that analyzes git history to reveal codebase hotspots, bug magnets, bus factor risks, and development momentum before reading any code. Works with Gemini CLI, Claude Code, Cursor, and 20+ other coding agents
  <sub>★ 41 · MIT · npx · pushed 2026-04-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add yujiachen-y/codebase-recon-skill`</sub>
- **[Self Command](https://github.com/stevenAthompson/self-command)** — Allows the Gemini CLI to send commands to itself, run very long commands in the background and be woken, sleep for a specified amount of time, watch logs and receive notifications, etc by leveraging tmux. Reduces usage and improves reliability by avoiding loop detection. After installing the extension you must lauch gemini-cli into a tmux session named "gemini-cli"
  <sub>★ 30 · TypeScript · MIT · source · pushed 2026-03-12 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/stevenAthompson/self-command.git`</sub>
- **[anotifier](https://github.com/DevinoSolutions/anotifier-for-claude-codex-cursor)** — Desktop toasts, ntfy phone push and webhooks when Gemini CLI finishes a task or needs input, wired through its hooks by a one-command setup. Zero-dependency Node CLI whose single config also covers Claude Code, Codex CLI and Cursor
  <sub>★ 28 · JavaScript · AGPL-3.0 · psh · pushed 2026-09-26 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/DevinoSolutions/anotifier-for-claude-codex-cursor/main/setup/install.ps1 | iex`</sub>
- **[DOS](https://github.com/anthony-chaudhary/dos-kernel)** — Deterministic trust kernel for coding agents: hooks that verify "done" claims against git evidence and refuse file collisions between concurrent agents. Wires into Gemini CLI with dos init --hooks gemini; also ships an MCP server. Python, MIT
  <sub>★ 20 · Python · MIT · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from dos-kernel dos quickstart`</sub>
- **[Docker Gemini CLI](https://github.com/tgagor/docker-gemini-cli)** — Gemini CLI wrapped as a Docker image, so you don't need to trash your OS with Node and its dependencies
  <sub>★ 19 · Dockerfile · GPL-2.0 · docker · pushed 2026-09-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -i ${tty_args} --rm \`</sub>
- **[Signum](https://github.com/heurema/signum)** — Evidence-driven development pipeline that uses Gemini CLI as one of three independent reviewers in a multi-model code audit panel (alongside Claude and Codex)
  <sub>★ 18 · Shell · MIT · source · pushed 2026-07-20</sub>
  <sub>`git clone https://github.com/heurema/signum.git`</sub>
- **[Wasla](https://github.com/The-Untitled-Org/wasla)** — TypeScript CLI that syncs agents, MCP configs, skills, commands, and workflow assets across Gemini CLI, Claude Code, Codex, OpenCode/OpenClaw, and GitHub Copilot workflows
  <sub>★ 17 · TypeScript · MIT · npm · pushed 2026-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @untitled-devs/wasla`</sub>
- **[agentwatch](https://github.com/mishanefedov/agentwatch)** — Local-only TUI + web dashboard that tails Gemini CLI sessions alongside Claude Code, Codex, Cursor, Hermes, and OpenClaw on one unified timeline. Parses tokens, tools, and per-turn cost from each Gemini CLI session (gemini-2.5-pro / flash rates), plus context compaction visualizer, MAD z-score anomaly detection, MCP server mode, and OpenTelemetry exporter. No cloud, no telemetry. macOS + Linux. MI
  <sub>★ 15 · TypeScript · MIT · npm · pushed 2026-07-09 · WSL2 · macOS? · Linux</sub>
  <sub>`npm i -g @misha_misha/agentwatch`</sub>
- **[Tintpad](https://github.com/sorkila/tintpad)** — macOS menu bar launcher for the agentic-coding loop. One hotkey opens your terminal at the right repo with Gemini CLI (or Claude Code, Codex) already running. Frecency repo search, Safe/Default/YOLO run modes, git worktrees, headless background dispatch. Native Swift, local-only, free, open source
  <sub>★ 15 · Swift · MIT · brew · pushed 2026-09-23 · macOS</sub>
  <sub>`brew install --cask sorkila/tap/tintpad`</sub>
- **[Devie AI Quota Tracker](https://github.com/mathdevie/devie-ai-quota-tracker)** — Dashboard and macOS menu bar for tracking AI subscription quotas in one place (Claude Code, Codex, Gemini CLI, GitHub Copilot, and Cursor). Supports multi-accounts, notifications, and session-timer start optimization
  <sub>★ 15 · Rust · MIT · clone · pushed 2026-09-25 · macOS</sub>
  <sub>`git clone https://github.com/mathdevie/devie-ai-quota-tracker.git`</sub>
- **[Pluribus](https://github.com/caioribeiroclw-pixel/pluribus)** — Sync one canonical project context into native AI coding-agent rule files, including Gemini CLI GEMINI.md, Claude Code CLAUDE.md/AGENTS.md, Cursor, Cline, Roo Code, Amazon Q, Junie, Warp, Copilot, Windsurf, Continue, Zed, OpenCode, and OpenClaw
  <sub>★ 14 · JavaScript · MIT · npm · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pluribus-context@latest`</sub>
- **[tldr](https://github.com/SurefireStudios/tldr)** — Leads every response with a three-line TL;DR and folds the full detail underneath, so the answer is not buried. Never folds destructive commands, security findings, verbatim errors or diffs. Returns a parseable block for agent-to-agent reports. Ships a Gemini CLI extension
  <sub>★ 10 · Python · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SurefireStudios/tldr.git`</sub>
- **[rule-gen](https://github.com/nedcodes-ok/rule-gen)** — Generate AI coding rules from your actual codebase using Google Gemini. Feeds source files into Gemini's 1M token context window and produces project-specific rules. Supports Cursor (.mdc), Claude Code (CLAUDE.md), Copilot, and Windsurf output formats. Zero dependencies
  <sub>★ 9 · JavaScript · MIT · npx · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rulegen-ai`</sub>
- **[skillet](https://github.com/Brattlof/skillet)** — Zero-dependency Go CLI / package manager that installs Agent Skills and MCP servers into Gemini CLI (and other tools), plus Claude Code slash commands and hooks
  <sub>★ 8 · Go · MIT · go · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/Brattlof/skillet/cmd/skillet@latest`</sub>
- **[Hermes Jailbench](https://github.com/hermes-labs-ai/hermes-jailbench)** — Repeatable jailbreak test harness for Anthropic/OpenAI-compatible endpoints. It emits deterministic refusal/partial/compliance classifications and includes a no-key dry-run and Gemini CLI extension
  <sub>★ 6 · Python · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/hermes-labs-ai/hermes-jailbench --skill hermes-jailbench`</sub>
- **[Gemini Dockerized CLI](https://github.com/nordluf/gemini-dockerized-cli)** — Gemini Dockerized CLI with small improvements
  <sub>★ 4 · Shell · Apache-2.0 · source · pushed 2026-07-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nordluf/gemini-dockerized-cli.git`</sub>
- **[claude-skills-pro](https://github.com/Hahaknight/claude-skills-pro)** — 15 engineering-workflow skills (7-dimension code review, root-cause debugging, bug-catching test generation, behavior-preserving refactor, zero-downtime DB migration; 7 free/MIT) with CN/EN handbooks. Installs into Gemini CLI via the open skills installer: npx skills add Hahaknight/claude-skills-pro --agent gemini-cli (install path verified end-to-end in Gemini CLI)
  <sub>★ 4 · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Hahaknight/claude-skills-pro`</sub>
- **[OpenFiles](https://github.com/devgiordane/openfiles)** — VS Code extension (also on Open VSX for Cursor, Windsurf and VSCodium) that opens every file Gemini CLI edits so ESLint, TypeScript and other language servers check it, then returns the problems to Gemini CLI through an AfterTool hook in the same turn. Also works with Claude Code, Codex, Copilot and Cursor. MIT
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/devgiordane/openfiles.git`</sub>
- **[IssueDB](https://issue-queue.readthedocs.io/en/latest/llm_agents.html)** — LLM frendly command-line issue tracking system for software development projects, with built-in interface, context support and prompt providers for Gemini CLI and others
  <sub>website</sub>
  <sub>`https://issue-queue.readthedocs.io/en/latest/llm_agents.html`</sub>
- **[Gemini CLI Logs Prettifier](https://github.com/Manamama/Puzzles_for_AIs/tree/main/code/Gemini%20CLI%20logs%20prettifier)** — Renders the logs human readable (prettifies them) and browsable as interlinked HTML, with thoughtful explanations and clickable links
  <sub>Python · MIT · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/Manamama/Puzzles_for_AIs.git && cd Puzzles_for_AIs/code/Gemini%20CLI%20logs%20prettifier`</sub>
- **[MCP Config Doctor](https://mcpconfigdoctor.online/)** — Browser-local diagnostic that validates Gemini CLI ~/.gemini/settings.json MCP server entries (shape, env/secret references, transport fields). Also covers Claude Code, Codex CLI, and VS Code MCP configs. No account, no telemetry, no remote calls — runs entirely in the browser
  <sub>website</sub>
  <sub>`https://mcpconfigdoctor.online/`</sub>
- **[Usage HUD](https://hud.thaliabloom.com/)** — Native macOS menu-bar meter that shows your Gemini CLI usage window next to Claude, Codex, Grok and Ollama, with a confidence label on every number. Paid, $9
  <sub>website</sub>
  <sub>`https://hud.thaliabloom.com/`</sub>
- **[Agent Cat](https://agentcat.app)** — Free macOS/Windows menu-bar app that shows Gemini CLI and Antigravity usage and limits next to Claude Code and Codex, read from local files
  <sub>website</sub>
  <sub>`https://agentcat.app`</sub>

## Interfaces

- **[AionUi](https://github.com/iOfficeAI/AionUi)** — Free, local, open-source GUI app for Gemini CLI — Better Chat UI, File Management, AI image editing, multi-agent support, multi-LLMs &amp; apikey polling, code diff view &amp; more
  <sub>★ 33.1k · TypeScript · Apache-2.0 · brew · pushed 2026-09-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install aionui`</sub>
- **[Gemini CLI Desktop](https://github.com/Piebald-AI/gemini-cli-desktop)** — Beautiful desktop and web UI that makes Gemini CLI accessible to non-terminal/mobile users while preserving all its powerful features
  <sub>★ 504 · TypeScript · MIT · clone · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Piebald-AI/gemini-cli-desktop`</sub>
- **[Agent Workbench](https://github.com/cvelasquez/agent-workbench)** — Local web UI for Antigravity CLI (agy), the official successor to Gemini CLI: tabs, browsable history, conversations as cards, and its status and context meter through the status line. Runs Claude Code, Codex and OpenCode side by side and hands a conversation over from one CLI to another. It doesn't drive Gemini CLI itself; the repository includes a one-off importer for old Gemini CLI chats
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-workbench`</sub>
- **[Yaw](https://yaw.sh)** — Cross-platform terminal that auto-detects Gemini CLI and opens a split-pane workflow with a companion terminal
  <sub>website</sub>
  <sub>`https://yaw.sh`</sub>
- **[Termly](https://termly.dev/)** — Free native iOS and Android app to monitor and control Gemini CLI (and other CLI AI assistants) remotely. Zero-knowledge E2E encryption, pairs in under 60 seconds via QR code. No subscriptions, no usage limits
  <sub>website</sub>
  <sub>`https://termly.dev/`</sub>
- **[AnywhereDesign](https://anywheredesign.site)** — Local-first voice cockpit and remote mobile interface for Claude Code &amp; Antigravity/Gemini CLI. Control terminal agent sessions from your phone via local QR code, real-time voice dictation, live terminal output streaming, and zero-token mobile Git sync
  <sub>website</sub>
  <sub>`https://anywheredesign.site`</sub>

## Fun

- **[Oh My Logo](https://github.com/shinshin86/oh-my-logo)** — Adds personality to your terminal with giant ASCII-art logos featuring beautiful color gradients, perfect for customizing your Gemini CLI startup experience
  <sub>★ 1.6k · TypeScript · npm · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g oh-my-logo`</sub>

## Browser Extensions

- **[SRT Subtitle Translator Validator](https://github.com/VjayC/SRT-Subtitle-Translator-Validator)** — Browser-based tool to translate SRT subtitles using your Gemini subscription via CLI Proxy API with automatic validation/error correction - no API keys needed
  <sub>★ 110 · TypeScript · MIT · source · pushed 2026-05-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/VjayC/SRT-Subtitle-Translator-Validator.git`</sub>

## Neovim Plugins

- **[nvim Gemini Companion](https://github.com/gutsavgupta/nvim-gemini-companion)** — A Neovim plugin to integrate Gemini CLI well (+ Qwen Code now)
  <sub>★ 83 · Lua · source · pushed 2026-06-30 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/gutsavgupta/nvim-gemini-companion.git`</sub>
- **[gemini-cli.nvim](https://github.com/JonRoosevelt/gemini-cli.nvim)** — Native Neovim integration bringing Gemini's AI capabilities directly into your editor with keybindings, commands, and buffer manipulation support
  <sub>★ 57 · Lua · source · pushed 2025-08-25</sub>
  <sub>`git clone https://github.com/JonRoosevelt/gemini-cli.nvim.git`</sub>
- **[gemini-nvim](https://github.com/JunYang-tes/agents-parter.nvim)** — Gemini CLI in neovim - An unofficial Neovim plugin for interacting with Google Gemini CLI
  <sub>★ 6 · Lua · source · pushed 2026-02-09</sub>
  <sub>`git clone https://github.com/JunYang-tes/gemini-nvim.git`</sub>

## API Bridges &amp; Proxies

- **[CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)** — Wrap Gemini CLI as an OpenAI/Gemini/Claude compatible API service, allowing you to enjoy the free Gemini 2.5 Pro model through API
  <sub>★ 53.2k · Go · MIT · source · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/router-for-me/CLIProxyAPI.git`</sub>
- **[Bifrost](https://github.com/maximhq/bifrost)** — Self-hosted gateway for Gemini CLI that unifies cloud and local model providers with routing, fallbacks, load balancing, and MCP support
  <sub>★ 8.4k · Go · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @maximhq/bifrost`</sub>
- **[gemini-cli-openai](https://github.com/GewoonJaap/gemini-cli-openai)** — Transform Google's Gemini models into OpenAI-compatible endpoints using Cloudflare Workers, powered the same infrastructure that drives the official Gemini CLI
  <sub>★ 897 · TypeScript · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GewoonJaap/gemini-cli-openai.git`</sub>
- **[geminicli2api](https://github.com/gzzhongqi/geminicli2api)** — Powerful FastAPI proxy that transforms Gemini CLI into standard API endpoints, enabling integration with any OpenAI-compatible tool or service
  <sub>★ 591 · Python · MIT · source · pushed 2025-12-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gzzhongqi/geminicli2api.git`</sub>
- **[Gemini CLI Termux](https://github.com/print-yuhuan/Gemini-CLI-Termux)** — Provides a one-click deployment solution for Gemini CLI reverse proxy service for Android Termux users
  <sub>★ 174 · Python · MIT · source · pushed 2026-03-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/print-yuhuan/Gemini-CLI-Termux.git`</sub>
- **[gemini-cli-proxy](https://github.com/nettee/gemini-cli-proxy)** — OpenAI-compatible API wrapper for Gemini CLI as an OpenAI-compatible API service, allowing you to enjoy the free Gemini 2.5 Pro model through API!
  <sub>★ 153 · Python · MIT · uv · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx gemini-cli-proxy`</sub>
- **[gemini-cli-mcp-openai-bridge](https://github.com/Intelligent-Internet/gemini-cli-mcp-openai-bridge)** — Server application that extends the Google Gemini CLI with MCP toolkit and OpenAI-compatible API bridge
  <sub>★ 138 · TypeScript · Apache-2.0 · npm · pushed 2025-07-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @intelligentinternet/gemini-cli-mcp-openai-bridge`</sub>
- **[gemini-openai-proxy](https://github.com/Brioch/gemini-openai-proxy)** — Universal compatibility layer serving Gemini 2.5 Pro/Flash through OpenAI protocol. Works instantly with existing tools like LangChain, llama.cpp, and VS Code extensions
  <sub>★ 59 · TypeScript · MIT · docker · pushed 2025-08-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 11434:80 -e GEMINI_API_KEY gemini-openai-proxy`</sub>
- **[TeamoRouter](https://teamorouter.cn)** — Hosted LLM gateway — managed alternative to self-hosted bridges. OpenAI-compatible and native Anthropic endpoints behind one API key; works with Gemini CLI, Claude Code, and Codex directly. Free permanent DeepSeek tiers (V4 Pro 200 req/day, V4 Flash 50 req/day, 1M ctx)
  <sub>website</sub>
  <sub>`https://teamorouter.cn`</sub>

## SDKs

- **[Gemini CLI Vercel AI SDK Provider](https://github.com/ben-vargas/ai-sdk-provider-gemini-cli)** — Seamless Vercel AI SDK integration that unlocks Gemini's capabilities in Next.js and React applications with minimal configuration
  <sub>★ 72 · TypeScript · MIT · source · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ben-vargas/ai-sdk-provider-gemini-cli.git`</sub>
- **[Python Gemini CLI SDK](https://github.com/oneryalcin/gemini-cli-sdk)** — Python SDK for Gemini CLI; API-compatible with Claude Code SDK
  <sub>★ 18 · Python · MIT · pip · pushed 2025-09-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install gemini-cli-sdk`</sub>

## Non-Gemini CLI

- **[toprank](https://github.com/nowork-studio/notfair-plugin)** — Claude Code plugin for SEO and Google Ads that includes a Gemini cross-model review skill. Uses Gemini for second-opinion reviews on Google Ads campaigns, SEO metadata, and schema markup — leveraging Gemini's native Google ecosystem knowledge for higher-quality decisions than Claude alone. MIT, 107 stars
  <sub>★ 3.9k · TypeScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[NotFair](https://github.com/nowork-studio/notfair-plugin)** — Open-source Claude Code skills for SEO, GEO, Google Ads, and Meta Ads. Connects to live data via Google Ads MCP, Meta Ads MCP, Google Search Console MCP, and Google Analytics (GA4) MCP. Includes a /notfair:gemini cross-model review skill that runs Gemini as a second-opinion gate on ad campaigns, SEO metadata, and schema markup. MIT, ~2.9k stars
  <sub>★ 3.9k · TypeScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[Git-Alchemist](https://github.com/abduznik/Git-Alchemist)** — A unified AI-powered CLI tool for automating GitHub repository management (issues, PRs, topics, profiles) powered by Gemini 3 and Gemma 3
  <sub>★ 22 · Python · MIT · source · pushed 2026-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/abduznik/Git-Alchemist.git`</sub>

## Documentation &amp; Examples

- **[Gemini CLI Tips by Addy Osmani](https://github.com/addyosmani/gemini-cli-tips)** — ~30 pro-tips for effectively using Gemini CLI for agentic coding
  <sub>★ 2.4k · source · pushed 2025-10-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/addyosmani/gemini-cli-tips.git`</sub>
- **[gemini-cli-extension](https://github.com/philschmid/gemini-cli-extension)** — Essential collection of extensions and commands that enhance Gemini CLI with additional capabilities and workflow improvements
  <sub>★ 148 · Apache-2.0 · source · pushed 2025-07-27</sub>
  <sub>`git clone https://github.com/philschmid/gemini-cli-extension.git`</sub>
- **[gemini-docs-ext](https://github.com/markmcd/gemini-docs-ext)** — Gemini CLI extension that adds Gemini API docs and MCP
  <sub>★ 54 · Apache-2.0 · clone · pushed 2026-01-22</sub>
  <sub>`git clone https://github.com/markmcd/gemini-docs-ext.git`</sub>
- **[gemini-cli-media-generation](https://github.com/vladkol/gemini-cli-media-generation)** — An example of using Gemini CLI with MCP Servers for Genmedia and Gemini 2.5 Flash Image model (Nano-banana)
  <sub>★ 19 · Python · Apache-2.0 · clone · pushed 2025-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vladkol/gemini-cli-media-generation`</sub>
- **[gemini-cli-demos](https://github.com/palladius/gemini-cli-demos)** — Ready-to-run demonstration scenarios showcasing Gemini CLI's capabilities, perfect for learning, presenting, or evaluating the tool
  <sub>★ 14 · Just · source · pushed 2026-07-28</sub>
  <sub>`git clone https://github.com/palladius/gemini-cli-demos.git`</sub>
- **[cli-demo-cookbook](https://github.com/ptone/cli-demo-cookbook)** — Collection of demo scenario and casts for Gemini CLI
  <sub>★ 11 · Python · Apache-2.0 · source · pushed 2025-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ptone/cli-demo-cookbook.git`</sub>
- **[Antigravity CLI Tips](https://github.com/ykdojo/antigravity-cli-tips)** — Practical tips for Antigravity CLI (agy), the official successor to Gemini CLI
  <sub>★ 7 · HTML · source · pushed 2026-07-17 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/ykdojo/antigravity-cli-tips.git`</sub>

## Education &amp; Study Tools

- **[Shiori](https://github.com/kaorii-ako/Shiori-v1)** — Open-source AI study companion powered by Gemini AI. Assignments tracker, SRS flashcards, GPA predictor, AI quiz generator, Pomodoro focus timer, and Claude Code MCP server. Live demo
  <sub>★ 43 · JavaScript · MIT · clone · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kaorii-ako/Shiori-v1.git`</sub>


---

Snapshot 2026-09-26. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
