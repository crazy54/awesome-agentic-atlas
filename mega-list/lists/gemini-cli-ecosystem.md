# Gemini CLI Ecosystem

A curated list of awesome tools, extensions, and resources for Gemini CLI.

Curated by **[Piebald-AI/awesome-gemini-cli](https://github.com/Piebald-AI/awesome-gemini-cli)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

264 entries · 227 distinct repos · 17 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/google-gemini/gemini-cli"><img src="https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/assets/gemini-screenshot.png" width="260"></a> | <a href="https://github.com/QwenLM/qwen-code/"><img src="https://img.alicdn.com/imgextra/i3/O1CN01l5GyhGuOPGC3XHtt_!!6000000005884-2-tps-1742-903.png" width="260"></a> | <a href="https://github.com/google-gemini/cookbook"><img src="https://opengraph.githubassets.com/1/google-gemini/cookbook" width="260"></a> |
| **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**<br>★ 107.5k | **[Qwen Code](https://github.com/QwenLM/qwen-code/)**<br>★ 28.6k | **[Gemini CLI cookbook](https://github.com/google-gemini/cookbook)**<br>★ 17.9k |
| <a href="https://github.com/iflow-ai/iflow-cli"><img src="https://raw.githubusercontent.com/iflow-ai/iflow-cli/main/assets/iflow-cli.jpg" width="260"></a> | <a href="https://github.com/google-github-actions/run-gemini-cli"><img src="https://opengraph.githubassets.com/1/google-github-actions/run-gemini-cli" width="260"></a> | <a href="https://github.com/vybestack/llxprt-code"><img src="https://opengraph.githubassets.com/1/vybestack/llxprt-code" width="260"></a> |
| **[iFlow CLI](https://github.com/iflow-ai/iflow-cli)**<br>★ 5.1k | **[Run Gemini CLI](https://github.com/google-github-actions/run-gemini-cli)**<br>★ 2.1k | **[LLxprt Code](https://github.com/vybestack/llxprt-code)**<br>★ 702 |

## Contents

- [Official](#official) (3)
- [Forks](#forks) (3)
- [Commands &amp; Extensions](#commands--extensions) (54)
- [Prompts](#prompts) (2)
- [MCP Servers](#mcp-servers) (65)
- [Agent Orchestration &amp; CLI Tools](#agent-orchestration--cli-tools) (32)
- [Frameworks](#frameworks) (5)
- [Development Tools &amp; Utilities](#development-tools--utilities) (60)
- [Interfaces](#interfaces) (9)
- [Fun](#fun) (1)
- [Browser Extensions](#browser-extensions) (1)
- [Neovim Plugins](#neovim-plugins) (3)
- [API Bridges &amp; Proxies](#api-bridges--proxies) (10)
- [SDKs](#sdks) (2)
- [Non-Gemini CLI](#non-gemini-cli) (3)
- [Documentation &amp; Examples](#documentation--examples) (9)
- [Education &amp; Study Tools](#education--study-tools) (2)

## Official

- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — The official open-source AI agent that brings the power of Gemini directly into your terminal. Features context-aware coding assistance, file manipulation, and command execution capabilities
  <sub>★ 107.5k · TypeScript · Apache-2.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @google/gemini-cli`</sub>
- **[Gemini CLI cookbook](https://github.com/google-gemini/cookbook)** — Official collection of examples and guides demonstrating best practices for using the Gemini API. Essential resource for developers getting started
  <sub>★ 17.9k · Jupyter Notebook · Apache-2.0 · source · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/google-gemini/cookbook.git`</sub>
- **[Run Gemini CLI](https://github.com/google-github-actions/run-gemini-cli)** — Official GitHub Action that seamlessly integrates Gemini into your CI/CD pipeline, enabling automated code reviews, testing, and documentation generation
  <sub>★ 2.1k · TypeScript · Apache-2.0 · gh-action · pushed 2026-08-21</sub>
  <sub>`uses: google-github-actions/run-gemini-cli@main # in .github/workflows/*.yml`</sub>

## Forks

- **[Qwen Code](https://github.com/QwenLM/qwen-code/)** — Fork by the team behind Qwen LLM. Uses Qwen instead of Gemini
  <sub>★ 28.6k · TypeScript · Apache-2.0 · psh · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.ps1 | iex`</sub>
- **[iFlow CLI](https://github.com/iflow-ai/iflow-cli)** — Powerful fork that extends Gemini CLI with repository analysis, context interpretation, and complex workflow automation. Perfect for teams needing advanced orchestration capabilities
  <sub>★ 5.1k · Shell · npm · pushed 2026-03-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm i -g @iflow-ai/iflow-cli`</sub>
- **[LLxprt Code](https://github.com/vybestack/llxprt-code)** — An open-source multi-provider (including local) fork of Gemini CLI. Use whatever LLM you want to code in your terminal
  <sub>★ 702 · TypeScript · Apache-2.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @vybestack/llxprt-code`</sub>

## Commands &amp; Extensions

- **[AIHawk](https://github.com/feder-cr/invisible_dots)** — Gives Gemini CLI a real Firefox to drive from plain-English instructions: opens pages, clicks, types, reads and screenshots through the real pointer and keyboard. Open source, MIT. Install via gemini extensions install https://github.com/feder-cr/AIHawk
  <sub>★ 32.2k · TypeScript · MIT · clone · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/feder-cr/invisible_dots;`</sub>
- **[Conductor](https://github.com/gemini-cli-extensions/conductor)** — Conductor is a Gemini CLI extension that allows you to specify, plan, and implement software features
  <sub>★ 3.8k · Python · Apache-2.0 · clone · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gemini-cli-extensions/conductor.git`</sub>
- **[brooks-lint](https://github.com/hyhmrright/brooks-lint)** — AI code reviews grounded in six classic engineering books. Diagnoses decay risks with structured findings (Symptom → Source → Consequence → Remedy)
  <sub>★ 1.5k · HTML · MIT · script · pushed 2026-10-22 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/hyhmrright/brooks-lint/main/scripts/install.sh | bash -s -- <platform>`</sub>
- **[OpenAccountants](https://github.com/openaccountants/openaccountants)** — 371 tax classification skills across 134 countries. Classify bank statement transactions into VAT/GST, income tax, and social contribution categories with conservative defaults
  <sub>★ 457 · Python · AGPL-3.0 · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openaccountants-mcp`</sub>
- **[Pickle Rick](https://github.com/galdawave/pickle-rick-extension)** — This extension transforms the Gemini CLI into "Pickle Rick," a hyper-intelligent, arrogant, yet extremely competent engineering persona. It enforces a rigid, iterative software development lifecycle through continuous AI agent loops
  <sub>★ 453 · TypeScript · Apache-2.0 · source · pushed 2026-05-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/galdawave/pickle-rick-extension.git`</sub>
- **[gemini-flow](https://github.com/clduab11/gemini-flow)** — Transforms Gemini CLI into an autonomous AI development team using proven Claude-Flow patterns, enabling complex multi-agent workflows
  <sub>★ 386 · TypeScript · MIT · npm · pushed 2026-01-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @clduab11/gemini-flow`</sub>
- **[ru-text](https://github.com/talkstream/ru-text)** — Russian text quality — ~1,040 rules for typography, info-style, editorial, UX writing, business correspondence
  <sub>★ 276 · Shell · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add talkstream/ru-text`</sub>
- **[gemini-cli-custom-slash-commands](https://github.com/amitkmaraj/gemini-cli-custom-slash-commands)** — Curated collection of productivity-boosting custom slash commands that extend Gemini CLI with specialized workflows and shortcuts
  <sub>★ 167 · source · pushed 2025-07-31</sub>
  <sub>`git clone https://github.com/amitkmaraj/gemini-cli-custom-slash-commands.git`</sub>
- **[Supercov](https://github.com/supercorp-ai/supercov)** — Coverage, security and code quality for coding agents. Gemini CLI extension that runs the project's existing tests, measures line, branch and MC/DC coverage, and hands Gemini the untested code to test next. Install with gemini extensions install https://github.com/supercorp-ai/supercov
  <sub>★ 157 · Rust · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx supercov quality`</sub>
- **[LintLang](https://github.com/hermes-labs-ai/lintlang)** — Static linter and Gemini CLI extension for agent instructions, tool descriptions, and prompt configuration
  <sub>★ 143 · Python · Apache-2.0 · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx lintlang scan AGENTS.md`</sub>
- **[assay](https://github.com/awss1i/assay)** — Deterministic QA for web pages, with a Gemini CLI skill. assay opens the page in Chromium with Playwright, drives every control, and reports where the page contradicts itself, with no LLM and the same result on every run. The skill tells Gemini CLI to run assay after it changes a page and report what it found. Install with pip install assay-ui, then add the skill file. MIT
  <sub>★ 107 · Python · MIT · uv · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install assay-ui # no Python 3.10+? uv downloads one`</sub>
- **[wiki](https://github.com/plasma-ai/wiki)** — Indexed Markdown knowledge bases with a CLI and installable Agent Skill. wiki install writes the skill to ~/.agents/skills, which Gemini CLI discovers
  <sub>★ 106 · Python · Apache-2.0 · pip · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install plasma-wiki`</sub>
- **[PlaceCall](https://github.com/voygr-tech/placecall)** — Gemini CLI extension (skill + remote MCP server) that places real outbound phone calls to US businesses for bookings, inquiries and quotes, and returns the outcome and transcript. Paid API. Install: gemini extensions install https://github.com/voygr-tech/placecall
  <sub>★ 103 · Shell · MIT · clone · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/voygr-tech/placecall`</sub>
- **[Kin](https://github.com/kinlab-ai/kin)** — Gemini CLI extension for Kin, a graph-native code repository for people and AI agents. Its MCP server lets Gemini look up callers, references and history from the same record you inspect with the kin CLI
  <sub>★ 68 · Rust · Apache-2.0 · psh · pushed 2026-10-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://get.kinlab.dev/install.ps1 | iex`</sub>
- **[ATXP](https://github.com/atxp-dev/atxp)** — Give your Gemini CLI agent a wallet, email address, phone number, and 100+ paid MCP tools (web search, image gen, SMS, voice, LLM gateway). Self-register with gemini extensions install https://github.com/atxp-dev/atxp — no human login required, $5 free credits included
  <sub>★ 45 · TypeScript · MIT · npx · pushed 2026-03-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx atxp@latest`</sub>
- **[iOS Agent Skill](https://github.com/Nagarjuna2997/ios-agent-skill)** — Gemini CLI extension with Swift development guidance, read-only code review tools, and local Apple source/reference retrieval
  <sub>★ 39 · HTML · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
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
- **[Thinking Methods](https://github.com/ysskrishna/ai-agent-skills)** — Curated Agent Skills (SKILL.md) for structured thinking on real decisions: five whys, pre-mortem, trade-offs, prioritization, six thinking hats, and twelve more methods plus a selector skill. Install as a Gemini extension (gemini extensions install https://github.com/ysskrishna/ai-agent-skills) or skills only (gemini skills install https://github.com/ysskrishna/ai-agent-skills.git --path skills).
  <sub>★ 17 · Python · MIT · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ysskrishna/ai-agent-skills`</sub>
- **[gemini-cli-on-vscode](https://github.com/d3j/gemini-cli-on-vscode)** — MAGUS Council: World's first? 4-AI consultation system (Gemini+Claude+GPT-5+Qwen) in VS Code - Revolutionary multi-agent development environment
  <sub>★ 16 · TypeScript · MIT · source · pushed 2025-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/d3j/gemini-cli-on-vscode.git`</sub>
- **[llm-box](https://github.com/alib8b8/aflare)** — Terminal-first workflow automation engine. Generate and execute YAML workflows from plain English. 20+ built-in nodes (fetch_url, execute, file I/O, HTTP, JSON parsing, template rendering, LLM calls), 15+ LLM providers, and MCP server mode. Install via gemini extensions install https://github.com/alib8b8/llm-box
  <sub>★ 15 · Go · psh · pushed 2026-10-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/alib8b8/aflare/main/install.ps1 | iex`</sub>
- **[Listen](https://github.com/automateyournetwork/GeminiCLI_Listen_Extension)** — Run Gemini CLI as a server with /listen commands
  <sub>★ 14 · Python · Apache-2.0 · source · pushed 2025-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/GeminiCLI_Listen_Extension.git`</sub>
- **[dejavu](https://github.com/WhiteBite/dejavu-gates)** — Cross-session error gates: recurring tool-call failures become enforced remind-first, block-on-repeat gates via BeforeTool/AfterTool hooks. One store shared with Claude Code, Codex, OpenCode, Cursor and more. Install: gemini extensions install https://github.com/WhiteBite/dejavu-gates. MIT
  <sub>★ 13 · TypeScript · MIT · npm · pushed 2026-10-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm i -g dejavu-gates`</sub>
- **[figma-maxxing](https://github.com/thiagoxikota/figma-maxxing)** — Gemini CLI extension with 8 skills for agents editing real Figma files: Plugin API gotchas, checks before and after every write, comments to verified fixes, and a handoff gate. Built on figma-console-mcp; 3 of the checks also ran once on Figma's official MCP server. MIT. Install via gemini extensions install https://github.com/thiagoxikota/figma-maxxing
  <sub>★ 11 · Markdown · MIT · npx · pushed 2026-10-22 · macOS</sub>
  <sub>`npx skills add thiagoxikota/figma-maxxing`</sub>
- **[pyATS](https://github.com/automateyournetwork/pyATS_GeminiCLI_Extension)** — pyATS integration for network testing
  <sub>★ 10 · Python · Apache-2.0 · source · pushed 2025-12-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automateyournetwork/pyATS_GeminiCLI_Extension.git`</sub>
- **[Clera](https://github.com/getclera/mcp)** — Gemini CLI extension for hiring: search 210,000+ vetted startup candidates, review Clera's picks for your open roles and request intros through Clera's hosted OAuth MCP server
  <sub>★ 10 · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-remote https://mcp.getclera.com`</sub>
- **[since-cutoff](https://github.com/MohammadHijjawi97/since-cutoff)** — Gemini CLI extension (MCP server + skill) that tells the agent what changed in your Python dependencies since the model's training cutoff: a static diff of each library's public API between the release at the cutoff and the version your lockfile pins, with no model calls or API key. Install via gemini extensions install https://github.com/MohammadHijjawi97/since-cutoff
  <sub>★ 10 · Python · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add MohammadHijjawi97/since-cutoff`</sub>
- **[Hermeneutic](https://github.com/hermes-labs-ai/hermeneutic)** — Gemini CLI extension that reviews final-response wording for completion and certainty claims, then requests at most one evidence-focused revision through an AfterAgent hook. Runs the deterministic check locally
  <sub>★ 9 · Python · Apache-2.0 · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hermes-labs-ai/hermeneutic.git`</sub>
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
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx 16-eyes install`</sub>
- **[ArmorGemini](https://github.com/armoriq/armorGemini)** — Intent-based security enforcement for the Gemini CLI. Every tool call is checked against your ArmorIQ policy via BeforeTool / AfterTool hooks before it runs. Blocks intent drift, unauthorized tool use, and PII/PCI leaks. Install: curl -fsSL https://armoriq.ai/install_armorgemini.sh | bash
  <sub>★ 4 · JavaScript · MIT · script · pushed 2026-09-15 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://armoriq.ai/install_armorgemini.sh | bash`</sub>
- **[SuperSearch](https://github.com/hermes-labs-ai/supersearch)** — Local Python CLI/library that fans out bounded searches across web, code, community, and research sources and returns source-explicit JSON receipts
  <sub>★ 3 · Python · Apache-2.0 · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add hermes-labs-ai/supersearch --skill supersearch`</sub>
- **[Gemini Safety Net](https://github.com/kenryu42/gemini-safety-net)** — Gemini CLI extension that runs cc-safety-net as a BeforeTool hook. It blocks destructive Git and filesystem commands, and reads of secrets such as SSH keys and .env files, before Gemini runs the tool call. It parses the command, so wrapped forms such as bash -c are also checked. It is not a sandbox. MIT. Install with gemini extensions install https://github.com/kenryu42/gemini-safety-net
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y cc-safety-net hook install --kimi-cli`</sub>
- **[8B AI Website Builder](https://github.com/8bsite/8b-agent-plugin)** — Gemini CLI extension that builds an animated one-page website: the agent picks an 8B generated design, writes the copy and returns a preview link, plain-word edits and one HTML file. Remote MCP https://mcp.8b.com/mcp, no account or API key. Install: gemini extensions install https://github.com/8bsite/8b-agent-plugin
  <sub>★ 2 · MIT · source · pushed 2026-10-02</sub>
  <sub>`git clone https://github.com/8bsite/8b-agent-plugin.git`</sub>
- **[NotWorking](https://github.com/RyanNSJ/notworking)** — Downdetector for AI agents: a skill and remote MCP server that checks whether other agents report the same site, skill or MCP server failure, and takes failure reports. Install: gemini extensions install https://github.com/RyanNSJ/notworking
  <sub>★ 2 · Python · MIT · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add RyanNSJ/notworking`</sub>
- **[Kuudo Skills](https://github.com/KuudoAI/skills)** — Gemini CLI extension with 22 Agent Skills for Amazon sellers and advertisers: Sponsored Products and Brands audits, search-term mining, budget pacing, DSP and Amazon Marketing Cloud, listings, product images, repricing, FBA inbound, and profitability, built for Kuudo's hosted Amazon Ads and SP-API MCP servers. Price, budget, listing, and shipment writes are previewed and wait for your approval. In
  <sub>★ 2 · Python · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add /absolute/path/to/skills --skill amazon-profitability-calculator`</sub>
- **[US Watchlist Alerts](https://github.com/eli-alvarado/us-watchlist-alerts)** — Agent Skills (SKILL.md) for a US stock watchlist: NYSE-aware, de-duplicated price alerts (levels, % moves, gaps, 52-week highs/lows, MA crosses, RSI, earnings) and morning/close briefs. Stdlib Python, no API key, never places trades. MIT. Install with npx skills add eli-alvarado/us-watchlist-alerts -y -a gemini-cli
  <sub>★ 2 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add eli-alvarado/us-watchlist-alerts -y -a claude-code`</sub>
- **[Punchcard](https://github.com/Maksim-Burtsev/punchcard)** — Architecture-level code review grounded in thirty engineering books distilled into 78 principles. Three independent passes over a working tree, branch or PR, merged into one verdict; every blocker demonstrated by running the code. Install with npx skills add Maksim-Burtsev/punchcard -a gemini-cli
  <sub>★ 1 · HTML · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Maksim-Burtsev/punchcard`</sub>
- **[kgai](https://github.com/kgaidev/kgai-gemini)** — Shared decision memory for AI dev teams: your agent records why the code changed (and the dead ends it ruled out), recalls it before the next edit, and syncs it across the team without merge conflicts. Local-first, immutable, engine installs itself on first run
  <sub>★ 1 · Shell · MIT · source · pushed 2026-10-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kgaidev/kgai-gemini.git`</sub>
- **[isitdone](https://github.com/raimondasl/isitdone-gemini)** — Gemini CLI extension that refuses to let the agent end its turn claiming "done" until the repository's real test, typecheck and lint commands pass. An AfterAgent hook runs them on the exact working tree and feeds the failing output back; an AfterTool hook warns when an edit weakened a test. No LLM calls, no network. Install via gemini extensions install https://github.com/raimondasl/isitdone-gemin
  <sub>★ 1 · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx isitdone doctor`</sub>
- **[GTD Brain](https://github.com/minosin/gtdbrain-gemini-extension)** — Getting Things Done (GTD) task board for Gemini CLI: capture to your Inbox, next actions by context, projects, Waiting For and a guided weekly review over a hosted MCP server, plus a GEMINI.md context file and /gtd:* commands. Sign in with an email code, no API key; same board as the GTD Brain web, iOS and Android apps. Install: gemini extensions install https://github.com/minosin/gtdbrain-gemini-
  <sub>★ 1 · MIT · source · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/minosin/gtdbrain-gemini-extension.git`</sub>
- **[Better Design](https://github.com/better-designs/better-design-plugin)** — Gemini CLI extension that connects the Better Design MCP server: design systems, UI and UX principles, icons and UI review for the interfaces the agent builds. Install with gemini extensions install https://github.com/better-designs/better-design-plugin; sign in with a free account on first connect
  <sub>★ 1 · MIT · npx · pushed 2026-10-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add better-designs/better-design-plugin`</sub>
- **[brethof-brain](https://github.com/BrethofAI/brethof-brain-client)** — Gemini CLI extension for the hosted brethof-brain memory: with every prompt, the records that bear on it arrive before Gemini answers; a brief at session start; every turn archived; the same memory is shared with Claude Code, Codex and other agents. Needs a brethof-brain account (free plan). Install: gemini extensions install https://github.com/BrethofAI/brethof-brain-client
  <sub>★ 1 · Python · pip · pushed 2026-10-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/BrethofAI/brethof-brain-client.git`</sub>
- **[MoltNode by Chord](https://github.com/tuantqse90/moltnode-mcp)** — Gemini CLI extension that connects two hosted MCP servers and a GEMINI.md context file: MoltNode for JSON-RPC reads on 31 blockchains, and Chord for DEX swap quotes and unsigned swap transactions on Base, Monad, BNB Chain, Avalanche, Arbitrum, Robinhood Chain and Arc, plus token boards, candles and wallet PnL. No API key; the agent's own wallet signs every transaction. MIT. Install via gemini exte
  <sub>★ 1 · Python · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:tuantqse90/moltnode-mcp`</sub>
- **[Cohesivity](https://github.com/cohesivity-org/cohesivity-plugin/tree/main/packages/gemini)** — cohesivity.ai offers free agent native backend services. Anonymous account (no-signup) to get started through MCP or API. Hosting, postgres, email, storage, containers, LLMs, voice and third-party APIs. Includes free tiers and 5 USD/mo in AI and Search credits. Top-ups through x402
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/cohesivity-org/cohesivity-plugin.git && cd cohesivity-plugin/packages/gemini`</sub>
- **[PostEverywhere](https://github.com/posteverywhere/gemini-cli-extension)** — Social media scheduler for Gemini CLI. Write, schedule and publish posts to Instagram, TikTok, YouTube, LinkedIn, X, Threads, Pinterest and Bluesky, and plan a content calendar. Install with gemini extensions install https://github.com/posteverywhere/gemini-cli-extension (posteverywhere.ai)
  <sub>MIT · source · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/posteverywhere/gemini-cli-extension.git`</sub>

## Prompts

- **[gemini-cli-prompt-library](https://github.com/harish-garg/gemini-cli-prompt-library)** — 30+ professional prompts for Gemini CLI
  <sub>★ 411 · clone · pushed 2025-10-10</sub>
  <sub>`git clone https://github.com/yourusername/prompt-library-extension.git`</sub>
- **[OrcaPromptVault](https://github.com/Continuum-AI-Corp/OrcaPromptVault)** — Dated archive of the system prompts and tool schemas shipped AI agents send, including the one Gemini CLI itself puts on the wire
  <sub>★ 77 · AGPL-3.0 · clone · pushed 2026-10-01</sub>
  <sub>`git clone https://github.com/Continuum-AI-Corp/OrcaReplay`</sub>

## MCP Servers

- **[Unity-MCP](https://github.com/IvanMurzak/Unity-MCP)** — Open-source MCP server connecting AI agents (including Gemini CLI) to the Unity Editor and runtime, with 100+ built-in tools
  <sub>★ 4.5k · C# · Apache-2.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g unity-mcp-cli`</sub>
- **[gemini-mcp-tool](https://github.com/jamubc/gemini-mcp-tool)** — Leverages Gemini's industry-leading 2M token context window through MCP, enabling analysis of entire codebases and large documents that other tools can't handle
  <sub>★ 2.3k · TypeScript · source · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jamubc/gemini-mcp-tool.git`</sub>
- **[deja-vu](https://github.com/vshulcz/deja-vu)** — Local memory over the session files Gemini CLI and 19 other agents already write to disk, so a new session can search what you did before — including the months before you installed it. MCP tools plus auto-recall on every prompt; one Go binary, no network calls, MIT. Install: deja install gemini-auto
  <sub>★ 1.3k · Go · MIT · winget · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install vshulcz.deja-vu`</sub>
- **[Agent QA](https://github.com/vostride/agent-qa)** — Source-available (FSL-1.1-ALv2) QA agent for natural-language web and mobile tests. Run agent-qa mcp for authoring, execution, artifacts, and failure triage; dashboard-backed tools need a running dashboard and dashboardUrl. Model and infrastructure costs are separate
  <sub>★ 897 · TypeScript · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-qa init`</sub>
- **[Vestige](https://github.com/samvallad33/vestige)** — Memory system for coding agents: backfill ranks earlier records as candidate causes of a fresh failure even when they share no vocabulary with it, the composed graph records which memories were used together and surfaces never-tried combinations, retrieval decays on an FSRS-6 schedule, and receipts fail closed after compaction. Single Rust binary, local only. Install: gemini extensions install htt
  <sub>★ 655 · Rust · AGPL-3.0 · npx · pushed 2026-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @vestige/init`</sub>
- **[Godot-MCP](https://github.com/IvanMurzak/Godot-MCP)** — Open-source MCP server connecting AI agents to the Godot Editor and runtime (Godot 4.x, C#)
  <sub>★ 302 · C# · Apache-2.0 · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g godot-cli`</sub>
- **[squirrelscan](https://github.com/squirrelscan/squirrelscan)** — Website audit MCP server for coding agents: run audits, read reports, and fix findings from Gemini CLI or any MCP client. 260+ rules across SEO, performance, security, accessibility, and agent experience, with fixes mapped to source. MIT CLI with a local stdio server (squirrel mcp) or hosted Remote MCP with OAuth: gemini mcp add --transport http squirrelscan https://mcp.squirrelscan.com/mcp
  <sub>★ 292 · TypeScript · MIT · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g squirrelscan`</sub>
- **[Xquik MCP](https://github.com/Xquik-dev/x-twitter-scraper)** — X/Twitter data MCP server with 76 REST API endpoints, 20 extraction tools, account monitoring, and giveaway draws. Works with any MCP client including Gemini CLI
  <sub>★ 218 · JavaScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx skills@1.5.3 add Xquik-dev/x-twitter-scraper`</sub>
- **[KubeStellar Console kc-agent](https://github.com/kubestellar/console)** — Multi-cluster Kubernetes MCP server bridging Gemini CLI to kubeconfig and Kubernetes APIs. Manage clusters, policies, and 20+ CNCF project integrations across edge and cloud. Install via brew tap kubestellar/tap &amp;&amp; brew install kc-agent
  <sub>★ 148 · TypeScript · Apache-2.0 · brew · pushed 2026-10-22 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew tap kubestellar/tap`</sub>
- **[Tapetide MCP](https://github.com/Tapetide-hq/nse-bse-indian-stock-market-data-mcp)** — Indian stock market data for Gemini CLI: quotes, quarterly financials, shareholding, a 326-ratio screener, FII/DII flows, option chains and company filings for about 8,200 NSE and BSE stocks. Remote Streamable HTTP with OAuth or a free personal token, or local stdio via npx -y tapetide-mcp; free plan available. MIT. Install: gemini extensions install https://github.com/Tapetide-hq/nse-bse-indian-s
  <sub>★ 141 · TypeScript · MIT · source · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Tapetide-hq/nse-bse-indian-stock-market-data-mcp.git`</sub>
- **[ToolsForMCPServer](https://github.com/tanaikech/ToolsForMCPServer)** — Bridges Gemini CLI with Google Workspace through Apps Script integration, automating document processing, spreadsheet manipulation, and workflow automation
  <sub>★ 108 · JavaScript · MIT · source · pushed 2026-01-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tanaikech/ToolsForMCPServer.git`</sub>
- **[mcp-gemini-cli](https://github.com/choplin/mcp-gemini-cli)** — A simple MCP (Model Context Protocol) server wrapper for Google's Gemini CLI
  <sub>★ 101 · TypeScript · clone · pushed 2025-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/choplin/mcp-gemini-cli`</sub>
- **[nika](https://github.com/supernovae-st/nika)** — Read-only oracle for Nika AI workflows: validate .nika.yaml DAGs, explain findings, browse schema/examples, honest cost estimate — before a single token is spent (single Rust binary, config: command nika, args [mcp])
  <sub>★ 95 · Rust · AGPL-3.0 · brew · pushed 2026-10-21 · Win? · WSL2 · macOS</sub>
  <sub>`brew install supernovae-st/tap/nika`</sub>
- **[emem](https://github.com/Vortx-AI/emem)** — Shared, signed and content-addressed memory of the physical world that AI agents can read, cite, transfer and independently verify. 108 tools, no API key, no signup. Remote Streamable HTTP. Install: gemini extensions install https://emem.dev/gemini-extension.json
  <sub>★ 72 · Rust · Apache-2.0 · docker · pushed 2026-10-20 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 127.0.0.1:5051:5051 ghcr.io/vortx-ai/emem:latest`</sub>
- **[Oh My Android](https://github.com/ateymoori/oh-my-android)** — MCP server that lets Gemini CLI see and drive the Android Emulator on macOS: screenshots, UI tree in dp, tap/type, dark mode, RTL, font scale, logcat. Free, MIT, native macOS app (macOS 26+, Apple silicon) with a built-in stdio server. Install: gemini mcp add --scope user oh-my-android ohmyandroid-mcp
  <sub>★ 69 · Swift · MIT · brew · pushed 2026-10-22 · macOS</sub>
  <sub>`brew install --cask ateymoori/tap/oh-my-android`</sub>
- **[LWC](https://github.com/JanYork/llm-wiki-cli)** — Local-first, source-grounded project memory for Gemini CLI and other coding agents. Provides bounded recall, citations, atomic changesets, an installable Agent Skill, and a read-only stdio MCP server (lwc serve --mcp). Apache-2.0
  <sub>★ 68 · Rust · Apache-2.0 · source · pushed 2026-10-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/JanYork/llm-wiki-cli.git`</sub>
- **[RunAPI MCP](https://github.com/runapi-ai/mcp)** — Remote MCP server for browsing model catalogs, checking pricing, and creating image, video, music, audio, and other model API tasks through RunAPI. Works with Gemini CLI: gemini mcp add --transport http runapi https://mcp.runapi.ai/mcp
  <sub>★ 56 · TypeScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @runapi.ai/mcp init claude`</sub>
- **[Unreal-MCP](https://github.com/IvanMurzak/Unreal-MCP)** — Open-source MCP server connecting AI agents to Unreal Engine 5.7, editor and runtime (C++ plugin + .NET sidecar)
  <sub>★ 51 · C++ · Apache-2.0 · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g unreal-mcp-cli`</sub>
- **[gemini-cli-mcp](https://github.com/InfolabAI/gemini-cli-mcp)** — Tool that enables using Gemini AI as an MCP server within Claude Code with large file analysis and token savings
  <sub>★ 30 · Python · MIT · clone · pushed 2025-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/InfolabAI/gemini-cli-mcp.git`</sub>
- **[SolidPing](https://github.com/fclairamb/solidping)** — Uptime and synthetic monitoring with a remote MCP server (OAuth) to create, run and diagnose checks. Works with Gemini CLI: gemini mcp add --transport http solidping https://solidping.io/api/v1/mcp
  <sub>★ 26 · Go · AGPL-3.0 · scoop · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop bucket add fclairamb https://github.com/fclairamb/scoop-bucket scoop install solidping`</sub>
- **[Selvedge](https://github.com/masondelan/selvedge)** — Local SQLite decision memory for Gemini CLI via stdio MCP, storing explicit decisions, reasons, and rejected approaches for retrieval across sessions. Setup: selvedge setup --agent gemini
  <sub>★ 25 · Python · MIT · uv · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install --upgrade selvedge`</sub>
- **[prompt-to-asset](https://github.com/MohamedAbdallah-14/prompt-to-asset)** — MCP server that generates production-ready visual assets (app icons, favicons, OG images, logos, wordmarks) by routing requests across 30+ image generation models. Zero API key required for first run via Pollinations and Stable Horde free tiers. Works with any MCP client including Gemini CLI
  <sub>★ 24 · TypeScript · MIT · npm · pushed 2026-10-18 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm i -g prompt-to-asset`</sub>
- **[GoodMemory](https://github.com/hjqcan/GoodMemory)** — Local-first durable memory for Gemini CLI through standalone MCP, with scoped recall, provenance and trace inspection, and explicit forgetting. Read-only by default with opt-in governed writes; install with npm install -g goodmemory@0.7.5 and follow the Gemini CLI setup guide
  <sub>★ 20 · TypeScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g goodmemory@0.8.3`</sub>
- **[GameDev-MCP-Server](https://github.com/IvanMurzak/GameDev-MCP-Server)** — Open-source, engine-agnostic MCP server shared by Unity-MCP, Godot-MCP, and Unreal-MCP
  <sub>★ 16 · C# · Apache-2.0 · docker · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -i --rm -p 8080:8080 aigamedeveloper/mcp-server`</sub>
- **[Lians](https://github.com/Lians-ai/Lians)** — Open-source, local-first memory for Gemini CLI and other AI agents. Durable cross-session recall through a two-tool MCP extension, with no account or API key. Install: gemini extensions install https://github.com/Lians-ai/Lians
  <sub>★ 16 · Python · Apache-2.0 · pip · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install "lians-sdk[local]"`</sub>
- **[Hyperconsciousness](https://github.com/louis030195/hyperconsciousness)** — Developer-alpha encrypted, append-only knowledge store with a Rust CLI and stdio MCP server. Gives agents scoped, expiring access to notes and supports device sync. MIT licensed
  <sub>★ 8 · Rust · MIT · script · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/louis030195/hyperconsciousness/main/install.sh | sh`</sub>
- **[gemini-mcp](https://github.com/neriousy/gemini-mcp)** — A simple MCP server for using the Gemini CLI
  <sub>★ 7 · TypeScript · MIT · clone · pushed 2025-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/gemini-mcp.git`</sub>
- **[Find MCP](https://github.com/agentage/find-mcp)** — Search 17,000+ MCP servers synced from the official MCP registry (registry.modelcontextprotocol.io). Remote Streamable HTTP (https://catalog.agentage.io/mcp, no auth for search) or stdio (npx -y @agentage/find-mcp). Works with Gemini CLI: gemini mcp add --transport http find-mcp https://catalog.agentage.io/mcp
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentage/find-mcp.git`</sub>
- **[dsh-skills-anywhere](https://github.com/noteflowai/dsh-skills-anywhere)** — MCP server that exposes every Agent Skill installed for Gemini CLI, Claude Code, Codex, Cursor and 60+ other agents, plus Claude Code plugin marketplaces and any GitHub skills repo, as find_skills/open_skill tools and skill:// resources, read in place with zero copies or symlinks
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx dsh-skills-anywhere@0.19.0 check path/to/SKILL.md --resources --json`</sub>
- **[Lusha](https://github.com/lusha-oss/lusha-mcp-plugin)** — B2B prospecting and data enrichment: find and enrich contacts and companies with verified emails, direct dials, mobile numbers, and real-time buying signals. Remote MCP server bundled with 4 prospecting skills and OAuth sign-in. Works with Gemini CLI (gemini extensions install) and Antigravity (agy plugin install)
  <sub>★ 4 · MIT · source · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/lusha-oss/lusha-mcp-plugin.git`</sub>
- **[Minds](https://github.com/minds-ai-co/minds-mcp)** — Synthetic market research: create AI audiences, interview them and run studies such as MaxDiff, conjoint and NPS. Remote MCP server with OAuth; installable as a Gemini CLI extension
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/minds-ai-co/minds-mcp.git`</sub>
- **[Court Rules](https://github.com/foklepoint/court-rules-mcp)** — U.S. federal court rules, local rules, judge standing orders and court holidays with filing deadline checks, over a hosted MCP server. Install: gemini extensions install https://github.com/foklepoint/court-rules-mcp
  <sub>★ 4 · MIT · source · pushed 2026-09-30</sub>
  <sub>`git clone https://github.com/foklepoint/court-rules-mcp.git`</sub>
- **[Unsora](https://github.com/Shipped-Studio/unsora)** — AI content generation and social media scheduling from Gemini CLI: generate images, video, music and voiceovers, clip long videos into short clips, and schedule or publish posts to YouTube, TikTok, Instagram, Facebook, LinkedIn, Bluesky, Threads and Pinterest. Official open-source MCP server (AGPL-3.0, in apps/mcp), hosted as remote Streamable HTTP with OAuth sign-in or an API key. Paid plans from
  <sub>★ 3 · TypeScript · AGPL-3.0 · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Shipped-Studio/unsora.git`</sub>
- **[looot](https://github.com/loootai/looot-mcp)** — Remote MCP server (OAuth sign-in) that searches, prices and runs 2,500+ data API endpoints from 90+ providers (emails, phones, company and people search, Google results, web pages) on one prepaid balance. Ships a Gemini CLI extension manifest
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx looot-mcp`</sub>
- **[QRX](https://github.com/qrxcodes/qrx-mcp)** — Turn a text prompt and a link into an artistic, branded QR code from Gemini CLI. Each code is checked to scan before it is returned and uses a hosted qrx.to short link. Remote Streamable HTTP with OAuth sign-in or an API key, or local stdio via npx -y @qrxcodes/mcp. MIT. Add with: gemini mcp add --transport http qrx https://qrx.codes/mcp
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add qrxcodes/qrx-mcp`</sub>
- **[Blawgy](https://github.com/adamgusky/blawgy-mcp)** — Run your SEO blog from Gemini CLI. Research keywords, manage the content plan, write and update SEO blog posts with images and internal links, publish them to WordPress, Shopify, Webflow, Wix, Framer, Ghost and Duda, and read Search Console traffic, rankings and indexing status. Remote Streamable HTTP with OAuth sign-in or an API key; the server is closed source, included on every paid plan with a
  <sub>★ 3 · MIT · npx · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-remote https://app.blawgy.com/mcp`</sub>
- **[DropTheHassle](https://github.com/bosmdavid-gif/dropthehassle-mcp)** — Lets Gemini CLI publish the site it built on a real HTTPS link instead of localhost: a free link, no account needed. For your own .com it hands the human a €19/$19-a-year payment link; after payment the site goes live on it with no DNS. No tool spends money. For claimed sites, ask it for visitors, leads or site status. Remote Streamable HTTP, no sign-in for the first publish, or local stdio via np
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add bosmdavid-gif/dropthehassle-skill`</sub>
- **[DC Hub](https://github.com/azmartone67/dchub-mcp-server)** — Live data for data-center site selection: a daily Data Center Power Index (DCPI) of where data centers can get grid power across 300+ markets, live grid feeds from the seven US ISOs, plus fiber, gas and electricity prices. Answers carry an as-of timestamp and a citation line. 94 tools, remote Streamable HTTP, free tier needs no key. Install: gemini extensions install https://github.com/azmartone67
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @azmartone67/dchub --client claude`</sub>
- **[Mnemoverse Memory](https://github.com/mnemoverse/gemini-extension)** — Hosted memory shared across MCP clients: write a memory in Gemini CLI, recall it in Claude Code, Cursor, VS Code, or any other MCP client. Remote Streamable HTTP with OAuth sign-in, no API key to paste. Install: gemini extensions install https://github.com/mnemoverse/gemini-extension
  <sub>★ 2 · MIT · source · pushed 2026-10-10</sub>
  <sub>`git clone https://github.com/mnemoverse/gemini-extension.git`</sub>
- **[MAQAMI Travel](https://github.com/negm17111995/mcp-server)** — Hotel and flight search and booking from Gemini CLI: search hotels (3M+) and flights, read hotel details and reviews, then send the customer a secure checkout link on book.maqami.co for the offer they choose. Remote Streamable HTTP (https://mcp.maqami.co/), no sign-in or API key. Install: gemini extensions install https://github.com/negm17111995/mcp-server
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y maqami-travel`</sub>
- **[Hoot Lens](https://github.com/Parallel-Platforms/hootlens-mcp)** — Session replays and click heatmaps from real website visits. Find clicks that broke, jump to the JavaScript error and source line, and check whether a fix helped. Remote with OAuth (httpUrl: https://mcp.hootlens.com/mcp) or local with npx -y @hootlens/mcp. Demo with sample data, no sign-in: https://mcp.hootlens.com/demo
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @hootlens/mcp@1.1.0 login --scopes read,replay`</sub>
- **[npmscan](https://github.com/salemalem/npmscan-mcp-plugin)** — npm supply-chain security: checks packages for malware, known vulnerabilities, typosquats, maintainer takeovers and risky install scripts before install, and audits package.json, lockfiles, SBOMs and PR dependency changes. 23 read-only tools, no API key, no signup. Remote Streamable HTTP, bundled with 5 skills as a Gemini CLI extension. Install: gemini extensions install https://github.com/salemal
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/salemalem/npmscan-mcp-plugin.git`</sub>
- **[Glasser](https://github.com/glasser-ai/plugins)** — One key to 1,000+ paid third-party data APIs, pay per call: person and company enrichment, SEO and SERP, web scraping, places, news, scholar and social data. The agent searches the catalog, inspects the exact price, runs the endpoint and reports the charge; failed calls and empty results cost $0.00. Remote Streamable HTTP with OAuth sign-in. Works with Gemini CLI: gemini mcp add --transport http g
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @glasser-ai/cli`</sub>
- **[Connections](https://github.com/Lunarwerx/connections-gemini-extension)** — Work a free Connections contact book, follow-ups, ticketed event pages, notes and email from Gemini CLI; no card needed for the account. Remote Streamable HTTP MCP server with OAuth sign-in at https://studio.connections.icu/v1/mcp. Install: gemini extensions install https://github.com/Lunarwerx/connections-gemini-extension
  <sub>★ 1 · MIT · source · pushed 2026-09-27</sub>
  <sub>`git clone https://github.com/Lunarwerx/connections-gemini-extension.git`</sub>
- **[TokRepo MCP Server](https://github.com/henu-wang/tokrepo-mcp-server)** — Search and install AI skills, prompts, MCP configs, and workflows from TokRepo from Gemini CLI and other MCP clients
  <sub>JavaScript · MIT · npx · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx tokrepo init-agent --target all`</sub>
- **[TWZRD Agent Intel](https://intel.twzrd.xyz/mcp?utm_source=awesome-gemini-cli&utm_medium=referral)** — Trust scoring and identity verification for AI agent wallets on Solana. Verify agent identity before x402 micropayments or agent-initiated operations. Free: score_agent, preflight_check. Paid (x402): get_trust_receipt. Works with any MCP client including Gemini CLI
  <sub>website</sub>
  <sub>`https://intel.twzrd.xyz/mcp?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[AISO Tools MCP](https://aisotools.com/mcp?utm_source=awesome-gemini-cli&utm_medium=referral)** — Query a catalog of 1,636 AI tools from the CLI: keyword/category/pricing search, side-by-side comparison, and alternatives lookup, with a canonical citation URL on every result. Remote Streamable HTTP, no API key. Works with any MCP client including Gemini CLI: gemini mcp add --transport http aisotools https://aisotools.com/api/mcp
  <sub>website</sub>
  <sub>`https://aisotools.com/mcp?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[ContextStream](https://contextstream.io?utm_source=awesome-gemini-cli&utm_medium=referral)** — Shared project context for Cursor, Claude Code, Codex, Grok. Intelligence isn’t the bottleneck. Context is. Remote MCP for Gemini CLI and other coding agents: https://mcp.contextstream.io/mcp
  <sub>website</sub>
  <sub>`https://contextstream.io?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[SkillAgent](https://skillagent.dev?utm_source=awesome-gemini-cli&utm_medium=referral)** — Remote MCP server (Streamable HTTP, no auth) for searching ~3,500 agent skills, rules files (including Gemini rules) and MCP servers indexed hourly from GitHub, with project-based recommendations and per-agent install instructions for Gemini CLI. Install: gemini mcp add --transport http skillagent https://skillagent.dev/mcp
  <sub>website</sub>
  <sub>`https://skillagent.dev?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Bestax](https://github.com/allxsmith/bestax/tree/main/bestax-mcp)** — MCP server that gives coding agents the props, examples, CSS variables and Agent Skills for the Bestax React component library (Bulma v1). Runs offline
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/allxsmith/bestax.git && cd bestax/bestax-mcp`</sub>
- **[LogNorm](https://lognorm.com?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosted remote MCP server that hands a website's SEO and AI-visibility (GEO) backlog (site audits, fixes, content drafts, AI-answer tracking) to coding agents. Remote Streamable HTTP with OAuth sign-in, no API key; free plan available. Source: lognorm/lognorm-mcp. Add with: gemini mcp add --transport http lognorm https://lognorm.com/api/mcp
  <sub>website</sub>
  <sub>`https://lognorm.com?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[LinkMCP](https://app.linkmcp.io?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosted LinkedIn MCP server for your own LinkedIn account: profile and company lookups, people and Sales Navigator search, inbox, posts and comments, connection requests, and work email finding. Remote Streamable HTTP with OAuth sign-in; the server is closed source. Paid plans from $19/month, 7-day free trial without a card. Install: gemini extensions install https://github.com/linkmcp-io/linkmcp
  <sub>website</sub>
  <sub>`https://app.linkmcp.io?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[FXMacroData](https://fxmacrodata.com?utm_source=awesome-gemini-cli&utm_medium=referral)** — Official macroeconomic releases, central bank decisions, release calendars, FX rates and COT positioning for 22 currencies, with release timestamps and source links. Remote Streamable HTTP server; USD releases (last 90 days, 15-minute delay), the USD calendar and the USD catalogue work with no sign-in or API key, other currencies and FX rates need a key. Add with: gemini mcp add --transport http f
  <sub>website</sub>
  <sub>`https://fxmacrodata.com?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[BulkPublish](https://github.com/azeemkafridi/bulkpublish-api/tree/main/mcp-server)** — Draft, schedule, cross-post and analyze social media posts on 15 platforms (Instagram, TikTok, YouTube, X, LinkedIn, Bluesky and more) from Gemini CLI. Hosted Streamable HTTP with OAuth sign-in, or local stdio via npx -y @bulkpublish/mcp-server with an API key; free plan available. MIT. Add with: gemini mcp add --transport http bulkpublish https://mcp.bulkpublish.com/mcp
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/azeemkafridi/bulkpublish-api.git && cd bulkpublish-api/mcp-server`</sub>
- **[LinkedNav](https://www.linkednav.com/mcp?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosted MCP server for LinkedIn outreach in your own LinkedNav account: find leads, launch campaigns, send, and reply. LinkedNav detects LinkedIn buying signals and sends personalized outreach you approve. Remote Streamable HTTP with OAuth sign-in or an API key; the server is closed source. Free 7-day trial. An independent service, not affiliated with LinkedIn. Add with: gemini mcp add --transport
  <sub>website</sub>
  <sub>`https://www.linkednav.com/mcp?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[HeyReagent](https://heyreagent.com/linkedin-mcp?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosted LinkedIn MCP server for your own LinkedIn account: read your inbox, send messages and invitations, search people, and work with posts. Remote Streamable HTTP with OAuth sign-in, no key to paste; the server is closed source. Free plan available. An independent service, not affiliated with LinkedIn. Add with: gemini mcp add --transport http heyreagent https://api.heyreagent.com/mcp
  <sub>website</sub>
  <sub>`https://heyreagent.com/linkedin-mcp?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Latchkey](https://latchkey.dev/documentation/connect-your-ai-agent?utm_source=awesome-gemini-cli&utm_medium=referral)** — Self-healing GitHub Actions runners with a hosted MCP server for coding agents: read the CI failures self-heal could not fix (root cause, failing file, logs), check run status, dispatch workflows, and run commands on fresh ephemeral runners. Remote Streamable HTTP with a Latchkey API key; the server is closed source. Add with: gemini mcp add --transport http latchkey https://latchkey.dev/mcp --hea
  <sub>website</sub>
  <sub>`https://latchkey.dev/documentation/connect-your-ai-agent?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Aident Loadout](https://aident.ai?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosted MCP server that gives Gemini CLI and other MCP clients one reusable setup for apps like GitHub, Slack, Gmail, Linear and Notion, plus 400+ expert-built Skills and built-in services (search, scraping, media generation) billed from one balance. Accounts are connected once in the browser and kept in Aident Vault, and every action is logged in Audit. Remote Streamable HTTP with OAuth sign-in; f
  <sub>website</sub>
  <sub>`https://aident.ai?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[CurlShot](https://curlshot.com/docs/guides/ai-agents?utm_source=awesome-gemini-cli&utm_medium=referral)** — Screenshot API with a hosted MCP server: take_screenshot renders any web page in a real browser and returns the image (PNG, JPEG, WebP or PDF; full page, device presets, ad and cookie-banner blocking), so Gemini CLI can see a page, and list_devices lists the presets. Remote Streamable HTTP with a CurlShot API key; the server is closed source. Free plan of 100 screenshots a month, no card. Add with
  <sub>website</sub>
  <sub>`https://curlshot.com/docs/guides/ai-agents?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Pethost](https://pethost.dev?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosting for Docker Compose projects with a remote MCP server (OAuth): Gemini CLI deploys a project, reads its logs and HTTP traffic, and rolls it back. Add it with gemini mcp add --transport http pethost https://mcp.pethost.dev/mcp
  <sub>website</sub>
  <sub>`https://pethost.dev?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Google Hotels MCP](https://github.com/huynhtanan/google-hotels-mcp?utm_source=awesome-gemini-cli&utm_medium=referral)** — Search Google Hotels and Google Vacation Rentals from Gemini CLI: per-OTA nightly rates (Booking.com, Expedia, Agoda, Vrbo, Airbnb, Hotels.com and 10+ other providers), 3-month daily price calendars, amenities, nearby places and review topics. Local stdio server (3 tools) wrapping Apify Google Hotels actors; uvx --from "git+https://github.com/huynhtanan/google-hotels-mcp.git@v0.1.2" google-hotels-
  <sub>Python · MIT · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/huynhtanan/google-hotels-mcp.git && cd google-hotels-mcp/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[AltoRank](https://altorank.co/docs/mcp/?utm_source=awesome-gemini-cli&utm_medium=referral)** — Open-source SEO content software with a hosted MCP server: check whether search engines and AI crawlers can read a site, research keywords, read Google Search Console, and write sourced drafts into a person's review queue. No approve or publish tool. AGPL-3.0 and self-hostable (source). Remote Streamable HTTP with OAuth sign-in. Add with gemini mcp add --transport http altorank https://app.altoran
  <sub>website</sub>
  <sub>`https://altorank.co/docs/mcp/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Firecrawl](https://docs.firecrawl.dev/quickstarts/gemini-cli?utm_source=awesome-gemini-cli&utm_medium=integration)** — Official Firecrawl MCP server for web search, page scraping to markdown or JSON, and site crawling. The hosted server works keyless (rate limited) with search, scrape and parse; add an API key for crawl, map and the rest. The open-source server is MIT (source). Add with: gemini mcp add --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp
  <sub>website</sub>
  <sub>`https://docs.firecrawl.dev/quickstarts/gemini-cli?utm_source=awesome-gemini-cli&utm_medium=integration`</sub>
- **[deed.page](https://deed.page/docs?ref=skill-awesome-gemini-cli)** — Static hosting for agents with a remote MCP server that lets Gemini CLI publish an HTML file or static folder to a permanent public https://.deed.page URL and update it with the token it gets back. No account or API key for publishing; the companion Agent Skill is MIT (source). Remote Streamable HTTP. Add with gemini mcp add --transport http deed-page https://deed.page/mcp
  <sub>website</sub>
  <sub>`https://deed.page/docs?ref=skill-awesome-gemini-cli`</sub>
- **[ppl](https://withppl.com/agents?utm_source=awesome-gemini-cli&utm_medium=referral)** — Personal CRM for humans with AI agents, with a hosted remote MCP server (OAuth) at https://withppl.com/mcp: Gemini CLI can look up contacts, log interactions, keep notes and set reminders about the people in your life. Free beta up to 1,000 contacts at https://withppl.com/register
  <sub>website</sub>
  <sub>`https://withppl.com/agents?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>

## Agent Orchestration &amp; CLI Tools

- **[Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS)** — Local-first Agent Operation Environment (AOE) that installs into Gemini CLI and other supported hosts to build, route, and run specialist agent teams with portable packages, permissions, and verification gates
  <sub>★ 1.6k · Python · Apache-2.0 · psh · pushed 2026-10-20 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://agentlas.cloud/install.ps1 | iex # Windows PowerShell`</sub>
- **[Bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Multi-agent orchestrator that coordinates Gemini CLI alongside Claude Code and Codex CLI. Spawns parallel coding agents from a single goal, verifies with tests, auto-commits. Deterministic Python coordination, zero LLM tokens on orchestration
  <sub>★ 1.4k · Python · Apache-2.0 · uv · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[Parallel Code](https://github.com/johannesjo/parallel-code)** — Desktop app for orchestrating multiple AI coding agents (Claude Code, Codex CLI, Gemini CLI) simultaneously in isolated git worktrees
  <sub>★ 1.1k · TypeScript · MIT · clone · pushed 2026-10-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/johannesjo/parallel-code.git`</sub>
- **[agent-manager](https://github.com/YoanWai/agent-manager)** — Terminal UI that runs Gemini CLI alongside Claude Code, Codex, OpenCode and other coding-agent CLIs, each in its own persistent tmux session. One list shows every session's live status, prompts go into a pane without attaching, a session can spawn into its own Git worktree, and a full-file diff review sends line comments back to the agent. Launches your installed Gemini CLI unmodified, so login, c
  <sub>★ 613 · Go · Apache-2.0 · psh · pushed 2026-10-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/YoanWai/agent-manager/main/install.ps1 | iex`</sub>
- **[Concord MCP](https://github.com/Get-Concord-AI/concord-mcp)** — Local-first shared work-state MCP server (npx -y @concord-ai/concord-mcp) that lets coding agents coordinate on one repo through presence, file claims, messaging, handoffs and review packets. Works with Gemini CLI alongside Claude Code, Codex, Cursor and other agents. TypeScript, stdio, MIT
  <sub>★ 591 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @concord-ai/concord-mcp`</sub>
- **[hcom](https://github.com/aannoo/hcom)** — Let AI agents message, watch, and spawn each other across terminals. First-class Gemini CLI support with hooks integration and PTY wrapper. Also works with Claude Code, Codex, and OpenCode
  <sub>★ 590 · Rust · MIT · psh · pushed 2026-10-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://github.com/aannoo/hcom/releases/latest/download/hcom-installer.ps1 | iex`</sub>
- **[AgentBox](https://github.com/madarco/agentbox)** — Run multiple coding agents (Gemini CLI, Claude Code, Codex, OpenCode) in parallel, each teleported into its own sandboxed VM — local Docker, self-hosted, or cloud (Hetzner, Daytona, Vercel, E2B, DigitalOcean). Sub-1s checkpoint startup; git credentials stay on the host. MIT
  <sub>★ 543 · TypeScript · MIT · clone · pushed 2026-10-07 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/madarco/agentbox`</sub>
- **[Ivy Tendril](https://github.com/Ivy-Interactive/Ivy-Tendril)** — Open-source desktop app that orchestrates Gemini CLI alongside Claude Code, Codex, and Copilot through a plan-based lifecycle with verification gates, self-improving memory, and git worktree isolation. Local-first, agent-agnostic, FSL licensed
  <sub>★ 203 · C# · psh · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://cdn.ivy.app/install-tendril.ps1 | iex`</sub>
- **[SandBase CLI](https://github.com/sandbaseai/cli)** — Open-source CLI and MCP bridge that configures Gemini CLI and other AI coding agents to access 2,000+ AI models and APIs through one account
  <sub>★ 184 · TypeScript · Apache-2.0 · npx · pushed 2026-10-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @sandbaseai/cli@latest connect`</sub>
- **[clideck](https://github.com/rustykuntz/clideck)** — WhatsApp-like dashboard for managing multiple AI coding agents (including Gemini CLI) in one browser window. Live status, session resume, autopilot that routes work between agents while afk, mobile remote to check in from a phone
  <sub>★ 160 · JavaScript · MIT · npm · pushed 2026-10-22 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g clideck@2`</sub>
- **[Crewly](https://github.com/stevehuang0115/crewly)** — MIT-licensed, local platform that runs a team of role-based agents (developer, QA, PM, orchestrator) on Gemini CLI, Claude Code, and Codex, with task delegation through agent skills, shared persistent memory, and a web dashboard of live agent terminals. Requires one of these agent CLIs installed and logged in
  <sub>★ 89 · TypeScript · MIT · npm · pushed 2026-10-22 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npm install -g crewly`</sub>
- **[intentic](https://github.com/intentic/intentic)** — Self-hosted workspace that runs Gemini CLI over ACP (gemini --experimental-acp) alongside Claude Code, Codex, and OpenCode. Each agent gets its own Docker container and git worktree on hardware you own; terminals survive disconnects, any browser or phone reopens the same fleet, and changes land through per-file, per-hunk diff review. Scheduled and webhook-triggered runs. MIT
  <sub>★ 85 · TypeScript · MIT · script · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://intentic.dev/connect | sh -s -- <SETUP_CODE>`</sub>
- **[Untether](https://github.com/littlebearapps/untether)** — Telegram bridge for Gemini CLI (and 5 other agents). Send tasks by voice, stream progress, configure approval mode (read-only/edit files/full access) via inline buttons. Self-hosted, MIT licensed
  <sub>★ 72 · Python · MIT · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install untether # recommended`</sub>
- **[YYLO](https://github.com/yylo-dev/yylo)** — Kanban-driven CLI orchestrator that runs Gemini CLI alongside Claude Code and Codex in parallel across isolated git worktrees, with a merge queue that reviews and merges verified task work. Git-native task state, per-agent worktree isolation, installable via npm. MIT
  <sub>★ 66 · Python · MIT · npm · pushed 2026-10-17 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install --global '@yylo/cli@latest'`</sub>
- **[squads-cli](https://github.com/agents-squads/squads-cli)** — Open source CLI for AI agent coordination that organizes agents into domain-aligned squads with persistent memory, goal tracking, and Git-native state. Works with Gemini CLI
  <sub>★ 55 · TypeScript · MIT · npm · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g squads-cli`</sub>
- **[wolfpack](https://github.com/almogdepaz/wolfpack)** — Mobile &amp; desktop command center for controlling AI coding agents (Claude, Codex, Gemini) across machines from your phone. Secured by Tailscale. Self-hosted
  <sub>★ 49 · TypeScript · MIT · npx · pushed 2026-10-22 · WSL2 · macOS · Linux</sub>
  <sub>`bunx --bun wolfpack-bridge@latest`</sub>
- **[godmode](https://github.com/arbazkhan971/godmode)** — Discipline layer for AI coding agents: 135 skills and 7 subagents that wrap Gemini CLI (and Claude Code, Codex, Cursor, OpenCode, Amp, and pi) in a measure → modify → verify → keep/revert loop with automatic rollback of failed changes. MIT
  <sub>★ 26 · Shell · MIT · source · pushed 2026-08-28 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/arbazkhan971/godmode.git`</sub>
- **[Ralph Harness](https://github.com/rxdt/loopgate_harness)** — Tiny Python scaffold for running Gemini CLI, Claude Code, Codex CLI, and similar coding agents in guarded local loops. It uses repo-local specs, fresh-context iterations, hard caps, git-hook gates, CI verification, and coverage gates
  <sub>★ 24 · Python · MIT · source · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rxdt/py_ralph_frame.git`</sub>
- **[magents](https://github.com/abnegate/magents)** — Gemini CLI extension, MCP server and CLI over the session transcripts Gemini CLI, Claude Code, Codex, Copilot CLI, Cursor, Grok and OpenCode already write. List and read other live sessions, hand off compact state, send into a specific chat, or spawn a headless session that replies through a shared inbox. Install: gemini extensions install https://github.com/abnegate/magents. Rust, MIT
  <sub>★ 15 · Rust · MIT · cargo · pushed 2026-10-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`cargo install magents --locked`</sub>
- **[SpaceApp](https://github.com/oll4com/spaceapp)** — Self-hosted web workspace that runs Gemini CLI alongside OpenCode, Codex, Claude Code and other coding CLIs as side-by-side panes in persistent rooms, with MCP servers and managed browser panes. Install: npx --yes run-spaceapp@latest install. Source-available (BSL 1.1)
  <sub>★ 14 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g run-spaceapp`</sub>
- **[Mudroom](https://github.com/Kernel-Hunter/mudroom)** — Runs Gemini CLI, Claude Code, Codex, Aider and opencode inside a Linux micro-VM on a copy-on-write clone of your project, with a network allowlist and a pull-request-style diff review before changes are applied
  <sub>★ 11 · Swift · MIT · scoop · pushed 2026-10-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`scoop bucket add kernel-hunter https://github.com/Kernel-Hunter/scoop-bucket scoop install mudroom`</sub>
- **[ToutKit](https://github.com/NextProb/nextprob)** — Desktop notebook with a built-in terminal that runs Gemini CLI alongside Claude Code and Codex; an in-app webview renders whatever the agent writes inline, and each note is a self-contained folder with its own SQLite, files, and scripts. Local-first, Electron, AGPL-3.0
  <sub>★ 10 · JavaScript · AGPL-3.0 · clone · pushed 2026-10-16 · Win? · macOS</sub>
  <sub>`git clone https://github.com/nextprob/nextprob.git`</sub>
- **[PickySteve](https://github.com/KernelLord/pickysteve)** — Skill router and context picker for coding agents: a local model (via Ollama, offline by default) routes each prompt to the right skill via hybrid BM25 + embedding retrieval, cross-encoder rerank, and an LLM judge, then assembles a minimal context bundle for the execution model. Built-in prompt-injection gate scans every retrieved document, fail-closed. Ships an MCP stdio server and an OpenAI-comp
  <sub>★ 9 · Python · MIT · uv · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx pickysteve`</sub>
- **[AutoHarness](https://github.com/D-Shey/autoharness)** — Makes Gemini CLI (and Claude Code, Codex, Qwen Code) prepare before it builds: splits the task into areas of know-how, finds or writes a skill for each, checks the result against the original, and lets a fresh critic judge it. MIT
  <sub>★ 4 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install git+https://github.com/D-Shey/autoharness # the CLI (needs uv`</sub>
- **[loopguard](https://github.com/ruslanlap/loopguard)** — Watchdog that tails Gemini CLI session transcripts and alerts when the agent loops, oscillates, or stalls — Telegram notifications, zero dependencies
  <sub>★ 3 · Python · MIT · source · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ruslanlap/loopguard.git`</sub>
- **[DevIntern](https://github.com/getdevintern/devintern)** — Tool that picks up tickets from Jira, Linear, Trello, Asana, Azure DevOps, GitHub Issues, or markdown files and turns them into self-reviewed pull requests by driving Gemini CLI non-interactively (also supports Claude Code, Codex, and others). A feasibility gate flags vague tickets back to the tracker with questions; optional unattended mode schedules ticket pickup and turns PR review comments int
  <sub>★ 3 · TypeScript · npx · pushed 2026-10-22 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`bunx skills add getdevintern/devintern \`</sub>
- **[postmortemthis](https://github.com/Softeria/postmortemthis)** — Runs Gemini CLI alongside your other coding agents (Claude Code, Codex, Qwen, Vibe) in parallel and read-only over your diff, then synthesizes their reviews into one ship / no-ship verdict. A cross-model review panel
  <sub>★ 1 · Rust · MIT · source · pushed 2026-08-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Softeria/postmortemthis.git`</sub>
- **[puenteo](https://github.com/mano7onam/puenteo)** — Gemini CLI extension + MCP server that lets Gemini CLI, Claude Code, Codex and Cursor sessions on one machine search each other's history and message each other live (send/wait/reply, channels, file claims). Local SQLite, no daemon
  <sub>★ 1 · Python · MIT · uv · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install puenteo # or: pipx install puenteo / pip install puenteo`</sub>
- **[DHI Orbit](https://github.com/Dv04/dhi-orbit)** — Local web dashboard that lists Gemini CLI and Antigravity chats alongside Claude Code, Codex and Cursor on one board, with what needs an answer and a reply box (gemini --resume -p). Python standard library only, MIT
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-10-22 · macOS</sub>
  <sub>`pipx install dhi-orbit # or: brew install Dv04/dhi-orbit/dhi-orbit`</sub>
- **[Tars](https://tars.saccolabs.com?utm_source=awesome-gemini-cli&utm_medium=referral)** — A local-first autonomous supervisor and sidekick powered by Google Gemini. Features background persistence (heartbeat), tiered local memory, multi-channel notifications (Discord/WhatsApp), and self-healing background services. Designed for reliable, long-running agentic orchestration in the terminal
  <sub>website</sub>
  <sub>`https://tars.saccolabs.com?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[VibeFuse](https://fuseintelligence.org/products/vibefuse?utm_source=awesome-gemini-cli&utm_medium=referral)** — Free Windows desktop harness that runs Gemini CLI alongside Claude Code, Codex, Cursor, and Qwen as live draggable widgets on one canvas, with named sessions, local Whisper/Piper voice, an MCP tool panel, and a marketplace where skill and widget sellers keep 80% (Stripe Connect)
  <sub>website</sub>
  <sub>`https://fuseintelligence.org/products/vibefuse?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Drevon](https://www.drevon.dev?utm_source=awesome-gemini-cli&utm_medium=referral)** — Mac app that connects to your Claude Code or Codex and turns it into an end-to-end GTM operator: research, grunt work, analysis and actions across your stack from a single prompt, in your own browser with your own logins
  <sub>website</sub>
  <sub>`https://www.drevon.dev?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>

## Frameworks

- **[Maestro](https://github.com/josstei/maestro-orchestrate)** — Turn Gemini CLI into a multi-agent platform — 12 specialized subagents, parallel dispatch, 4-phase orchestration, and standalone dev tools for code review, debugging, security, and performance
  <sub>★ 487 · JavaScript · Apache-2.0 · clone · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/josstei/maestro-orchestrate`</sub>
- **[gemini-code-flow](https://github.com/Theopsguide/gemini-code-flow)** — Enterprise-grade orchestration framework that coordinates multiple Gemini CLI instances for complex development tasks, based on battle-tested Claude Code Flow patterns
  <sub>★ 158 · TypeScript · npm · pushed 2025-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g gemini-code-flow`</sub>
- **[GACUA](https://github.com/openmule/gacua)** — The world's first out-of-the-box computer use agent powered by Gemini CLI @openmule
  <sub>★ 139 · TypeScript · Apache-2.0 · npm · pushed 2025-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @gacua/backend`</sub>
- **[gemini-cli-commands-demo](https://github.com/pauldatta/gemini-cli-commands-demo)** — A proof-of-concept demonstrating a sub-agent orchestration system built within the Gemini CLI
  <sub>★ 91 · Shell · source · pushed 2025-07-31</sub>
  <sub>`git clone https://github.com/pauldatta/gemini-cli-commands-demo.git`</sub>
- **[Emdash Skills](https://github.com/heymegabyte/agent-skills)** — 14-category autonomous product-building OS with 18 specialized agents. Turns one-line prompts into deployed products. Includes GEMINI.md compatibility for cross-tool portability. Skills cover architecture, planning, quality, brand, media, observability, and deployment on Cloudflare Workers
  <sub>★ 24 · TypeScript · npx · pushed 2026-10-11 · macOS</sub>
  <sub>`npx jsr add @heymegabyte/agent-skills`</sub>

## Development Tools &amp; Utilities

- **[Nix AI Tools](https://github.com/numtide/llm-agents.nix)** — Seamless Nix integration for reproducible Gemini CLI installations. Ensures consistent environments across teams and simplifies deployment with declarative configuration
  <sub>★ 2.2k · Nix · MIT · source · pushed 2026-10-22 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/numtide/nix-ai-tools.git`</sub>
- **[Rulesync](https://github.com/dyoshikawa/rulesync)** — The Node.js CLI tool that automatically generates configs (rules, ignore files, MCP servers, commands, and subagents) for various AI coding agents. Rulesync can convert configs between Gemini CLI and other AI agents in both directions
  <sub>★ 1.5k · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g rulesync`</sub>
- **[ccmanager](https://github.com/kbwo/ccmanager)** — Essential session management tool that saves, restores, and organizes multiple Gemini CLI sessions, perfect for juggling multiple projects or experiments
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-10-18 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g ccmanager`</sub>
- **[Agent Sessions](https://github.com/jazzyalex/agent-sessions)** — Local-first macOS app to search, browse, and resume Gemini CLI sessions alongside Codex CLI, Claude Code, OpenCode, and other agents, with live iTerm2 monitoring via Agent Cockpit
  <sub>★ 909 · Swift · MIT · brew · pushed 2026-10-22 · Win? · macOS</sub>
  <sub>`brew install --cask jazzyalex/agent-sessions/agent-sessions`</sub>
- **[agnix](https://github.com/agent-sh/agnix)** — Linter for AI agent configurations. Validates GEMINI.md, SKILL.md, hooks, MCP, and more with 156 rules, auto-fix, and LSP server for real-time editor diagnostics
  <sub>★ 457 · Rust · Apache-2.0 · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agnix`</sub>
- **[ClawMetry](https://github.com/vivekchand/clawmetry)** — Self-hosted, local-first observability and kill switch for coding agents, reading Gemini CLI sessions alongside Claude Code, Codex, Cursor, OpenClaw, Aider, Goose, and others. Reads the session logs the runtimes already write on disk, so there is no SDK and nothing in the request path. Shows sessions, transcripts, tool calls, tokens, and cache-aware cost per session and model; an opt-in emergency
  <sub>★ 436 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vivekchand/clawmetry --skill agent-kill-switch`</sub>
- **[Splitrail](https://github.com/Piebald-AI/splitrail)** — Comprehensive usage analytics platform that tracks and optimizes your Gemini CLI workflows, helping teams understand and improve their AI-assisted development patterns
  <sub>★ 225 · Rust · MIT · source · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Piebald-AI/splitrail.git`</sub>
- **[Lockpaw](https://github.com/sorkila/lockpaw)** — macOS menu bar screen guard for unattended Gemini CLI runs. One hotkey covers the screen and blocks input while the agent keeps running (no sleep), and the locked screen glows plus fires a notification when Gemini CLI needs input or finishes, via a lockpaw ping hook. Touch ID unlock. Also works with Claude Code and Codex. Native Swift, free, open source
  <sub>★ 164 · Swift · MIT · brew · pushed 2026-10-21 · macOS</sub>
  <sub>`brew tap sorkila/lockpaw`</sub>
- **[unslop](https://github.com/MohamedAbdallah-14/unslop)** — CLI and MCP server that removes AI writing patterns from text: tricolons, em-dash overuse, hedging stacks, sycophancy openers, and overused vocabulary. Works with any MCP client including Gemini CLI. Five intensity levels and a lint-only audit mode. Useful for cleaning commit messages, PR descriptions, and documentation
  <sub>★ 161 · Python · MIT · pipx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install unslop`</sub>
- **[agenttrace](https://github.com/luoyuctl/agenttrace)** — Local-first TUI for Gemini CLI and AI coding agent session observability. Parses local logs for cost, tokens, tool failures, latency, anomalies, health gates, and diffs across Gemini CLI, Claude Code, Codex CLI, Aider, Cursor exports, OpenCode, and more
  <sub>★ 148 · Rust · MIT · psh · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/luoyuctl/agenttrace/master/install.ps1 | iex`</sub>
- **[Terminal Jarvis](https://github.com/BA-CalderonMorales/terminal-jarvis)** — Ultimate command center unifying multiple AI coding assistants in one elegant interface. Switch between tools seamlessly and manage sessions efficiently
  <sub>★ 138 · Rust · MIT · npm · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`npm install -g terminal-jarvis`</sub>
- **[aisw](https://github.com/burakdede/aisw)** — Saves Gemini CLI logins and API keys as named profiles and switches the live ~/.gemini state in one command, alongside Claude Code, Codex CLI and Antigravity CLI. Docs: aiswitcher.dev
  <sub>★ 134 · Rust · MIT · cargo · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install aisw`</sub>
- **[Hexis](https://github.com/Bevel-Software/Hexis)** — Git-backed platform for skills, tools, and context for AI agents, available to Gemini CLI through a remote OAuth MCP server
  <sub>★ 118 · TypeScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @bevel-software/hexis-mcp`</sub>
- **[authsome](https://github.com/agentrhq/authsome)** — Local credential broker for AI agents. OAuth2 and API key vault stored locally, a loopback HTTPS proxy injects credentials into outbound provider requests so the Gemini CLI agent never sees raw secrets. 45 providers bundled (GitHub, Google, OpenAI, Linear, Slack, Notion, Resend, Stripe, ...). Python 3.13+, MIT
  <sub>★ 97 · Python · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add agentrhq/authsome`</sub>
- **[Archcore](https://github.com/archcore-ai/archcore)** — Git-native context engineering CLI and MCP server for AI coding agents; archcore init --agent gemini-cli wires Gemini CLI hooks and MCP
  <sub>★ 71 · TypeScript · Apache-2.0 · psh · pushed 2026-10-22 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://archcore.ai/install.ps1 | iex`</sub>
- **[EGC](https://github.com/Fmarzochi/EGC)** — Persistent cross-session memory for Gemini CLI and 12 other AI coding tools. SQLite-backed state survives context resets, install with npm install -g @egchq/egc
  <sub>★ 67 · JavaScript · Apache-2.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @egchq/egc`</sub>
- **[ChatVault](https://github.com/ssanaullahrais/Chat-Vault)** — Windows app that reads, searches and backs up your Gemini CLI chats across accounts, and continues any chat in Gemini CLI through a handoff file that carries the whole conversation
  <sub>★ 67 · TypeScript · MIT · clone · pushed 2026-10-20 · Win</sub>
  <sub>`git clone https://github.com/ssanaullahrais/Chat-Vault.git`</sub>
- **[vsync](https://github.com/nicepkg/vsync)** — Sync Skills, MCP servers, Agents &amp; Commands across Claude Code, Cursor, OpenCode, Codex, and Gemini CLI with automatic format conversion (JSON ↔ TOML ↔ JSONC)
  <sub>★ 61 · TypeScript · MIT · npm · pushed 2026-01-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @nicepkg/vsync`</sub>
- **[andrej-karpathy-skills](https://github.com/swarmclawai/andrej-karpathy-skills)** — Npm installer for Karpathy-inspired GEMINI.md guidelines, plus adapters for Codex, Claude Code, Cursor, OpenCode, OpenClaw, Windsurf, and Aider
  <sub>★ 54 · JavaScript · MIT · npm · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @swarmclawai/andrej-karpathy-skills`</sub>
- **[LynxPrompt](https://github.com/GeiserX/LynxPrompt)** — Self-hosted web app that turns one set of AI coding rules into the file each tool reads: Gemini CLI's GEMINI.md, AGENTS.md, CLAUDE.md, Cursor rules and Copilot instructions, 30 rule-file formats in all. Blueprints carry variables so a team shares one set across projects, and the lynxp CLI writes the files into each repository. AGPL-3.0
  <sub>★ 53 · TypeScript · AGPL-3.0 · brew · pushed 2026-10-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install GeiserX/lynxprompt/lynxprompt`</sub>
- **[codebase-recon](https://github.com/yujiachen-y/codebase-recon-skill)** — AI agent skill that analyzes git history to reveal codebase hotspots, bug magnets, bus factor risks, and development momentum before reading any code. Works with Gemini CLI, Claude Code, Cursor, and 20+ other coding agents
  <sub>★ 41 · MIT · npx · pushed 2026-04-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add yujiachen-y/codebase-recon-skill`</sub>
- **[anotifier](https://github.com/DevinoSolutions/anotifier-for-claude-codex-cursor)** — Desktop toasts, ntfy phone push and webhooks when Gemini CLI finishes a task or needs input, wired through its hooks by a one-command setup. Zero-dependency Node CLI whose single config also covers Claude Code, Codex CLI and Cursor
  <sub>★ 33 · JavaScript · AGPL-3.0 · psh · pushed 2026-10-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/DevinoSolutions/anotifier-for-claude-codex-cursor/main/setup/install.ps1 | iex`</sub>
- **[laya-guard](https://github.com/scs0209/laya-guard)** — Local guardrail with a BeforeTool hook for Gemini CLI (laya-guard install gemini-cli) that judges each shell command before it runs, using regex rules, protected paths, and a small on-device model. Blocked commands are denied; ones marked for review pass with a note. Also hooks into Claude Code, Codex, Cursor, and other agents. MIT
  <sub>★ 31 · Python · MIT · pip · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --no-deps laya-guardrail pyyaml`</sub>
- **[Self Command](https://github.com/stevenAthompson/self-command)** — Allows the Gemini CLI to send commands to itself, run very long commands in the background and be woken, sleep for a specified amount of time, watch logs and receive notifications, etc by leveraging tmux. Reduces usage and improves reliability by avoiding loop detection. After installing the extension you must lauch gemini-cli into a tmux session named "gemini-cli"
  <sub>★ 30 · TypeScript · MIT · source · pushed 2026-03-12 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/stevenAthompson/self-command.git`</sub>
- **[Caprock](https://github.com/dspv/caprock)** — Local dashboard that starts Gemini CLI sessions and follows them through the telemetry file Gemini writes, on the same screens as Claude Code, Codex and OpenCode: live activity, token cost per repository, searchable history
  <sub>★ 25 · Go · Apache-2.0 · scoop · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add dspv https://github.com/dspv/scoop-bucket scoop install caprock`</sub>
- **[agy-powerline](https://github.com/wassim-azi/agy-powerline)** — Fast, configurable statusline for Antigravity CLI (agy), the successor to Gemini CLI, with real-time 5h/7d Gemini quota meters, pace markers, context usage, and interactive TUI editor. Zero dependencies, MIT
  <sub>★ 22 · JavaScript · MIT · npx · pushed 2026-10-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx agy-powerline init # install the statusline into agy`</sub>
- **[DOS](https://github.com/anthony-chaudhary/dos-kernel)** — Deterministic trust kernel for coding agents: hooks that verify "done" claims against git evidence and refuse file collisions between concurrent agents. Wires into Gemini CLI with dos init --hooks gemini; also ships an MCP server. Python, MIT
  <sub>★ 20 · Python · MIT · uv · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from dos-kernel dos quickstart`</sub>
- **[Docker Gemini CLI](https://github.com/tgagor/docker-gemini-cli)** — Gemini CLI wrapped as a Docker image, so you don't need to trash your OS with Node and its dependencies
  <sub>★ 19 · Dockerfile · GPL-2.0 · docker · pushed 2026-10-01 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -i ${tty_args} --rm \`</sub>
- **[Signum](https://github.com/heurema/signum)** — Evidence-driven development pipeline that uses Gemini CLI as one of three independent reviewers in a multi-model code audit panel (alongside Claude and Codex)
  <sub>★ 18 · Shell · MIT · source · pushed 2026-07-20</sub>
  <sub>`git clone https://github.com/heurema/signum.git`</sub>
- **[Wasla](https://github.com/The-Untitled-Org/wasla)** — TypeScript CLI that syncs agents, MCP configs, skills, commands, and workflow assets across Gemini CLI, Claude Code, Codex, OpenCode/OpenClaw, and GitHub Copilot workflows
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @untitled-devs/wasla`</sub>
- **[Devie AI Quota Tracker](https://github.com/mathdevie/devie-ai-quota-tracker)** — Dashboard and macOS menu bar for tracking AI subscription quotas in one place (Claude Code, Codex, Gemini CLI, GitHub Copilot, and Cursor). Supports multi-accounts, notifications, and session-timer start optimization
  <sub>★ 18 · Rust · MIT · clone · pushed 2026-10-19 · macOS</sub>
  <sub>`git clone https://github.com/mathdevie/devie-ai-quota-tracker.git`</sub>
- **[agentwatch](https://github.com/mishanefedov/agentwatch)** — Local-only TUI + web dashboard that tails Gemini CLI sessions alongside Claude Code, Codex, Cursor, Hermes, and OpenClaw on one unified timeline. Parses tokens, tools, and per-turn cost from each Gemini CLI session (gemini-2.5-pro / flash rates), plus context compaction visualizer, MAD z-score anomaly detection, MCP server mode, and OpenTelemetry exporter. No cloud, no telemetry. macOS + Linux. MI
  <sub>★ 17 · TypeScript · MIT · npm · pushed 2026-07-09 · WSL2 · macOS? · Linux</sub>
  <sub>`npm i -g @misha_misha/agentwatch`</sub>
- **[Tintpad](https://github.com/sorkila/tintpad)** — macOS menu bar launcher for the agentic-coding loop. One hotkey opens your terminal at the right repo with Gemini CLI (or Claude Code, Codex) already running. Frecency repo search, Safe/Default/YOLO run modes, git worktrees, headless background dispatch. Native Swift, local-only, free, open source
  <sub>★ 15 · Swift · MIT · brew · pushed 2026-10-13 · macOS</sub>
  <sub>`brew install --cask sorkila/tap/tintpad`</sub>
- **[Pluribus](https://github.com/caioribeiroclw-pixel/pluribus)** — Sync one canonical project context into native AI coding-agent rule files, including Gemini CLI GEMINI.md, Claude Code CLAUDE.md/AGENTS.md, Cursor, Cline, Roo Code, Amazon Q, Junie, Warp, Copilot, Windsurf, Continue, Zed, OpenCode, and OpenClaw
  <sub>★ 14 · JavaScript · MIT · npm · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pluribus-context@latest`</sub>
- **[Hermes Jailbench](https://github.com/hermes-labs-ai/hermes-jailbench)** — Repeatable jailbreak test harness for Anthropic/OpenAI-compatible endpoints. It emits deterministic refusal/partial/compliance classifications and includes a no-key dry-run and Gemini CLI extension
  <sub>★ 12 · Python · Apache-2.0 · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/hermes-labs-ai/hermes-jailbench --skill hermes-jailbench`</sub>
- **[tldr](https://github.com/SurefireStudios/tldr)** — Leads every response with a three-line TL;DR and folds the full detail underneath, so the answer is not buried. Never folds destructive commands, security findings, verbatim errors or diffs. Returns a parseable block for agent-to-agent reports. Ships a Gemini CLI extension
  <sub>★ 11 · Python · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SurefireStudios/tldr.git`</sub>
- **[rule-gen](https://github.com/nedcodes-ok/rule-gen)** — Generate AI coding rules from your actual codebase using Google Gemini. Feeds source files into Gemini's 1M token context window and produces project-specific rules. Supports Cursor (.mdc), Claude Code (CLAUDE.md), Copilot, and Windsurf output formats. Zero dependencies
  <sub>★ 9 · JavaScript · MIT · npx · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rulegen-ai`</sub>
- **[skillet](https://github.com/Brattlof/skillet)** — Zero-dependency Go CLI / package manager that installs Agent Skills and MCP servers into Gemini CLI (and other tools), plus Claude Code slash commands and hooks
  <sub>★ 8 · Go · MIT · go · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/Brattlof/skillet/cmd/skillet@latest`</sub>
- **[claude-skills-pro](https://github.com/Hahaknight/claude-skills-pro)** — 15 engineering-workflow skills (7-dimension code review, root-cause debugging, bug-catching test generation, behavior-preserving refactor, zero-downtime DB migration; 7 free/MIT) with CN/EN handbooks. Installs into Gemini CLI via the open skills installer: npx skills add Hahaknight/claude-skills-pro --agent gemini-cli (install path verified end-to-end in Gemini CLI)
  <sub>★ 5 · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Hahaknight/claude-skills-pro`</sub>
- **[yoink](https://github.com/MajidRaimi/yoink)** — Saves and switches Gemini CLI Google logins (oauth_creds.json and google_accounts.json) alongside Claude Code, Codex, Kimi Code and GitHub Copilot logins, from a CLI or a macOS menu bar app
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-10-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g yoink-cli`</sub>
- **[Gemini Dockerized CLI](https://github.com/nordluf/gemini-dockerized-cli)** — Gemini Dockerized CLI with small improvements
  <sub>★ 4 · Shell · Apache-2.0 · source · pushed 2026-07-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nordluf/gemini-dockerized-cli.git`</sub>
- **[fakegreen](https://github.com/fitzyracing1/fakegreen)** — Deterministic diff checker with an AfterAgent hook (npx fakegreen install gemini) that denies the turn when the agent skipped or deleted tests, weakened assertions, added suppressions, special-cased the test environment or forced CI green with || true, and feeds the findings back so Gemini fixes them. No LLM or API key. MIT
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx fakegreen`</sub>
- **[spillage](https://github.com/maximilianfeix/spillage)** — Finds API keys in the chats, logs and checkpoints Gemini CLI keeps under ~/.gemini/tmp and in the MCP servers of ~/.gemini/settings.json, redacts them in place, and installs BeforeAgent / BeforeTool / SessionEnd hooks (spillage guard install) that block a prompt with a key in it and reads of .env. Python, no dependencies, no network; also covers Claude Code, Codex CLI and Cursor
  <sub>★ 4 · Python · MIT · uv · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx spillage`</sub>
- **[Dazzler](https://github.com/jongos/Dazzler)** — Agent Skill for frontend and document design (typography, palettes, 30 templates, offline design checks) with setup instructions for Gemini CLI
  <sub>★ 3 · Python · Apache-2.0 · npx · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add jongos/Dazzler --skill dazzler-frontend`</sub>
- **[SafetyCard](https://github.com/safetycard/safetycard)** — Safety-check MCP servers and AI agents against the OWASP agentic Top 10, and get the safest setup to run them. Install with npx skills add safetycard/safetycard --agent gemini-cli
  <sub>★ 3 · Python · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add safetycard/safetycard --global --agent codex`</sub>
- **[ratchet](https://github.com/krishansubudhi/ratchet)** — Code-size budget CLI (pip install ratchet-size): ratchet check refuses changes that grow source or test line counts past a ceiling, and only ratchet grant raises it. For Gemini CLI it is wired through a GEMINI.md instruction snippet (no hook); a CI check or git pre-commit hook enforces it
  <sub>★ 3 · Python · Apache-2.0 · pipx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install ratchet-size`</sub>
- **[Tokenmeter](https://github.com/mugeshk97/tokenmeter)** — Desktop widget that shows Gemini CLI tokens today and over the last 7 days, alongside Claude Code, Codex and Copilot limits. Linux, Windows and macOS
  <sub>★ 2 · JavaScript · MIT · brew · pushed 2026-10-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask mugeshk97/tap/tokenmeter`</sub>
- **[agentvcr](https://github.com/tojacob03/agentvcr)** — Turns a Gemini CLI chat from ~/.gemini/tmp/*/chats (the JSONL format with rewinds and patches, or the older JSON files) into a self-contained HTML replay with a scrubbable timeline, diffs and terminal output, with API keys and other secrets masked locally first. Share it as a link through a secret gist on your own GitHub, embed it, export a Markdown transcript for a pull request, or have its GitHu
  <sub>★ 2 · JavaScript · MIT · npm · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g agentvcr-cli`</sub>
- **[tokenreceipt](https://github.com/henrikdukefoss/tokenreceipt)** — Local CLI that reads Gemini CLI chat logs (plus Claude Code, Codex, OpenCode and other agents) and prints a till-style receipt of tokens per agent and model, priced at public API list prices. Exports SVG/PNG cards or JSON; no account, no upload, no dependencies. MIT. Run: npx github:henrikdukefoss/tokenreceipt
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:henrikdukefoss/tokenreceipt`</sub>
- **[IssueDB](https://issue-queue.readthedocs.io/en/latest/llm_agents.html?utm_source=awesome-gemini-cli&utm_medium=referral)** — LLM frendly command-line issue tracking system for software development projects, with built-in interface, context support and prompt providers for Gemini CLI and others
  <sub>website</sub>
  <sub>`https://issue-queue.readthedocs.io/en/latest/llm_agents.html?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Gemini CLI Logs Prettifier](https://github.com/Manamama/Puzzles_for_AIs/tree/main/code/Gemini%20CLI%20logs%20prettifier)** — Renders the logs human readable (prettifies them) and browsable as interlinked HTML, with thoughtful explanations and clickable links
  <sub>Python · MIT · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/Manamama/Puzzles_for_AIs.git && cd Puzzles_for_AIs/code/Gemini%20CLI%20logs%20prettifier`</sub>
- **[MCP Config Doctor](https://mcpconfigdoctor.online/?utm_source=awesome-gemini-cli&utm_medium=referral)** — Browser-local diagnostic that validates Gemini CLI ~/.gemini/settings.json MCP server entries (shape, env/secret references, transport fields). Also covers Claude Code, Codex CLI, and VS Code MCP configs. No account, no telemetry, no remote calls — runs entirely in the browser
  <sub>website</sub>
  <sub>`https://mcpconfigdoctor.online/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Usage HUD](https://hud.thaliabloom.com/?utm_source=awesome-gemini-cli&utm_medium=referral)** — Native macOS menu-bar meter that shows your Gemini CLI usage window next to Claude, Codex, Grok and Ollama, with a confidence label on every number. Paid, $9
  <sub>website</sub>
  <sub>`https://hud.thaliabloom.com/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Agent Cat](https://agentcat.app?utm_source=awesome-gemini-cli&utm_medium=referral)** — Free macOS/Windows menu-bar app that shows Gemini CLI and Antigravity usage and limits next to Claude Code and Codex, read from local files
  <sub>website</sub>
  <sub>`https://agentcat.app?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Awakado](https://awakado.noodledragon.studio?utm_source=awesome-gemini-cli&utm_medium=referral)** — macOS menu-bar app that keeps the Mac awake while Gemini CLI is working, using Gemini CLI hooks, and lets it sleep when it finishes. Also supports Claude Code, Codex and other agents. Free, with a paid Pro tier
  <sub>website</sub>
  <sub>`https://awakado.noodledragon.studio?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[SkillKeeper](https://skillkeeper.app/?utm_source=awesome-gemini-cli&utm_medium=referral)** — macOS menu bar app that reads local Gemini CLI, Claude Code, Codex and Cursor sessions to show which skills, agents, MCP servers and tools ran, how often, and what they cost in tokens. Native Swift, free to track
  <sub>website</sub>
  <sub>`https://skillkeeper.app/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[MacMD Viewer](https://macmdviewer.com?utm_source=awesome-gemini-cli&utm_medium=referral)** — Read-only Markdown viewer for macOS 14+ for the GEMINI.md and plan files Gemini CLI writes. Renders Mermaid diagrams and highlighted code, reloads when the file changes on disk, and adds Quick Look previews in Finder. Paid, $19.99 one-time
  <sub>website</sub>
  <sub>`https://macmdviewer.com?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Check](https://github.com/golproductions/check-gemini)** — Extension with a BeforeTool hook that checks each file write on your own machine before Gemini CLI makes it (and, on Linux, each shell command): files, folders, programs, git refs and packages it names must exist, and scripts must parse; what the machine proves wrong is blocked with the machine's message. Install: gemini extensions install https://github.com/golproductions/check-gemini. Paid, 14-d
  <sub>JavaScript · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @golproductions/check@latest --key`</sub>
- **[Wardlume](https://wardlume.github.io?utm_source=awesome-gemini-cli&utm_medium=referral)** — Locks the Mac's keyboard, mouse, and trackpad while Gemini CLI runs unattended, so progress stays visible but nobody can type into the session. Unlocks with Touch ID or Apple Watch; sandboxed with no network access
  <sub>website</sub>
  <sub>`https://wardlume.github.io?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[session-handoff-kit](https://github.com/alapha888/session-handoff-kit)** — Agent Skill (open SKILL.md standard; installs into Gemini CLI with npx skills add alapha888/session-handoff-kit --agent gemini-cli) that ends a session with a structured handoff — goal state, decisions, files touched, open loops, next action — so the next session starts from facts instead of an over-full context. Also includes a context-hygiene checklist and a fill-in handoff template. MIT
  <sub>MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add alapha888/session-handoff-kit`</sub>

## Interfaces

- **[AionUi](https://github.com/iOfficeAI/AionUi)** — Free, local, open-source GUI app for Gemini CLI — Better Chat UI, File Management, AI image editing, multi-agent support, multi-LLMs &amp; apikey polling, code diff view &amp; more
  <sub>★ 33.7k · TypeScript · Apache-2.0 · brew · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install aionui`</sub>
- **[Gemini CLI Desktop](https://github.com/Piebald-AI/gemini-cli-desktop)** — Beautiful desktop and web UI that makes Gemini CLI accessible to non-terminal/mobile users while preserving all its powerful features
  <sub>★ 512 · TypeScript · MIT · clone · pushed 2026-10-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Piebald-AI/gemini-cli-desktop`</sub>
- **[Agent Workbench](https://github.com/cvelasquez/agent-workbench)** — Local web UI for Antigravity CLI (agy), the official successor to Gemini CLI: tabs, browsable history, conversations as cards, and its status and context meter through the status line. Runs Claude Code, Codex and OpenCode side by side and hands a conversation over from one CLI to another. It doesn't drive Gemini CLI itself; the repository includes a one-off importer for old Gemini CLI chats
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-workbench`</sub>
- **[Alchemist Coder](https://github.com/Alekla0126/alchemist-coder)** — Open-source desktop app for Windows, macOS and Linux that indexes your Gemini CLI chats, together with Claude Code, Codex and Grok Build sessions, into one local, read-only full-text search. Running Gemini CLI over ACP inside the app is planned for its upcoming Pro edition; the free edition runs Claude Code and Codex on local models
  <sub>★ 5 · TypeScript · AGPL-3.0 · source · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Alekla0126/alchemist-coder.git`</sub>
- **[Yaw](https://yaw.sh?utm_source=awesome-gemini-cli&utm_medium=referral)** — Cross-platform terminal that auto-detects Gemini CLI and opens a split-pane workflow with a companion terminal
  <sub>website</sub>
  <sub>`https://yaw.sh?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Termly](https://termly.dev/?utm_source=awesome-gemini-cli&utm_medium=referral)** — Free native iOS and Android app to monitor and control Gemini CLI (and other CLI AI assistants) remotely. Zero-knowledge E2E encryption, pairs in under 60 seconds via QR code. No subscriptions, no usage limits
  <sub>website</sub>
  <sub>`https://termly.dev/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[AnywhereDesign](https://anywheredesign.site?utm_source=awesome-gemini-cli&utm_medium=referral)** — Local-first voice cockpit and remote mobile interface for Claude Code &amp; Antigravity/Gemini CLI. Control terminal agent sessions from your phone via local QR code, real-time voice dictation, live terminal output streaming, and zero-token mobile Git sync
  <sub>website</sub>
  <sub>`https://anywheredesign.site?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Mobile SSH](https://mobile-ssh.github.io/?utm_source=awesome-gemini-cli&utm_medium=referral)** — Android and iOS (TestFlight beta) SSH client for running Gemini CLI on remote servers, with a Gemini CLI installer plugin, simultaneous terminal sessions, and tmux session management
  <sub>website</sub>
  <sub>`https://mobile-ssh.github.io/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[Bellows](https://bellowsai.app?utm_source=awesome-gemini-cli&utm_medium=referral)** — Desktop workspace that runs Gemini CLI over ACP alongside Claude and Codex, with diffs, permission prompts, team rules, a hash-linked audit trail and live session sharing. Windows, macOS and Linux
  <sub>website</sub>
  <sub>`https://bellowsai.app?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>

## Fun

- **[Oh My Logo](https://github.com/shinshin86/oh-my-logo)** — Adds personality to your terminal with giant ASCII-art logos featuring beautiful color gradients, perfect for customizing your Gemini CLI startup experience
  <sub>★ 1.6k · TypeScript · npm · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g oh-my-logo`</sub>

## Browser Extensions

- **[SRT Subtitle Translator Validator](https://github.com/VjayC/SRT-Subtitle-Translator-Validator)** — Browser-based tool to translate SRT subtitles using your Gemini subscription via CLI Proxy API with automatic validation/error correction - no API keys needed
  <sub>★ 112 · TypeScript · MIT · source · pushed 2026-05-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/VjayC/SRT-Subtitle-Translator-Validator.git`</sub>

## Neovim Plugins

- **[nvim Gemini Companion](https://github.com/gutsavgupta/nvim-gemini-companion)** — A Neovim plugin to integrate Gemini CLI well (+ Qwen Code now)
  <sub>★ 84 · Lua · source · pushed 2026-06-30 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/gutsavgupta/nvim-gemini-companion.git`</sub>
- **[gemini-cli.nvim](https://github.com/JonRoosevelt/gemini-cli.nvim)** — Native Neovim integration bringing Gemini's AI capabilities directly into your editor with keybindings, commands, and buffer manipulation support
  <sub>★ 57 · Lua · source · pushed 2025-08-25</sub>
  <sub>`git clone https://github.com/JonRoosevelt/gemini-cli.nvim.git`</sub>
- **[gemini-nvim](https://github.com/JunYang-tes/agents-parter.nvim)** — Gemini CLI in neovim - An unofficial Neovim plugin for interacting with Google Gemini CLI
  <sub>★ 6 · Lua · source · pushed 2026-02-09</sub>
  <sub>`git clone https://github.com/JunYang-tes/gemini-nvim.git`</sub>

## API Bridges &amp; Proxies

- **[CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)** — Wrap Gemini CLI as an OpenAI/Gemini/Claude compatible API service, allowing you to enjoy the free Gemini 2.5 Pro model through API
  <sub>★ 56k · Go · MIT · source · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/router-for-me/CLIProxyAPI.git`</sub>
- **[Bifrost](https://github.com/maximhq/bifrost)** — Self-hosted gateway for Gemini CLI that unifies cloud and local model providers with routing, fallbacks, load balancing, and MCP support
  <sub>★ 9k · Go · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @maximhq/bifrost`</sub>
- **[gemini-cli-openai](https://github.com/GewoonJaap/gemini-cli-openai)** — Transform Google's Gemini models into OpenAI-compatible endpoints using Cloudflare Workers, powered the same infrastructure that drives the official Gemini CLI
  <sub>★ 895 · TypeScript · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GewoonJaap/gemini-cli-openai.git`</sub>
- **[geminicli2api](https://github.com/gzzhongqi/geminicli2api)** — Powerful FastAPI proxy that transforms Gemini CLI into standard API endpoints, enabling integration with any OpenAI-compatible tool or service
  <sub>★ 591 · Python · MIT · source · pushed 2025-12-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gzzhongqi/geminicli2api.git`</sub>
- **[Gemini CLI Termux](https://github.com/print-yuhuan/Gemini-CLI-Termux)** — Provides a one-click deployment solution for Gemini CLI reverse proxy service for Android Termux users
  <sub>★ 175 · Python · MIT · source · pushed 2026-03-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/print-yuhuan/Gemini-CLI-Termux.git`</sub>
- **[gemini-cli-proxy](https://github.com/nettee/gemini-cli-proxy)** — OpenAI-compatible API wrapper for Gemini CLI as an OpenAI-compatible API service, allowing you to enjoy the free Gemini 2.5 Pro model through API!
  <sub>★ 152 · Python · MIT · uv · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx gemini-cli-proxy`</sub>
- **[gemini-cli-mcp-openai-bridge](https://github.com/Intelligent-Internet/gemini-cli-mcp-openai-bridge)** — Server application that extends the Google Gemini CLI with MCP toolkit and OpenAI-compatible API bridge
  <sub>★ 138 · TypeScript · Apache-2.0 · npm · pushed 2025-07-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @intelligentinternet/gemini-cli-mcp-openai-bridge`</sub>
- **[gemini-openai-proxy](https://github.com/Brioch/gemini-openai-proxy)** — Universal compatibility layer serving Gemini 2.5 Pro/Flash through OpenAI protocol. Works instantly with existing tools like LangChain, llama.cpp, and VS Code extensions
  <sub>★ 59 · TypeScript · MIT · docker · pushed 2025-08-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 11434:80 -e GEMINI_API_KEY gemini-openai-proxy`</sub>
- **[cliproxy-rs](https://github.com/vayungodara/cliproxy-rs)** — Rust rewrite of CLIProxyAPI with a built-in dashboard. Serves the Gemini API on a local endpoint (GOOGLE_GEMINI_BASE_URL), so Gemini CLI can run on Gemini API keys or on signed-in Claude and ChatGPT accounts
  <sub>★ 43 · Rust · scoop · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add vayungodara https://github.com/vayungodara/scoop-bucket scoop install vayungodara/cliproxy-rs`</sub>
- **[TeamoRouter](https://teamorouter.cn?utm_source=awesome-gemini-cli&utm_medium=referral)** — Hosted LLM gateway — managed alternative to self-hosted bridges. OpenAI-compatible and native Anthropic endpoints behind one API key; works with Gemini CLI, Claude Code, and Codex directly. Free permanent DeepSeek tiers (V4 Pro 200 req/day, V4 Flash 50 req/day, 1M ctx)
  <sub>website</sub>
  <sub>`https://teamorouter.cn?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>

## SDKs

- **[Gemini CLI Vercel AI SDK Provider](https://github.com/ben-vargas/ai-sdk-provider-gemini-cli)** — Seamless Vercel AI SDK integration that unlocks Gemini's capabilities in Next.js and React applications with minimal configuration
  <sub>★ 72 · TypeScript · MIT · source · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ben-vargas/ai-sdk-provider-gemini-cli.git`</sub>
- **[Python Gemini CLI SDK](https://github.com/oneryalcin/gemini-cli-sdk)** — Python SDK for Gemini CLI; API-compatible with Claude Code SDK
  <sub>★ 18 · Python · MIT · pip · pushed 2025-09-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install gemini-cli-sdk`</sub>

## Non-Gemini CLI

- **[toprank](https://github.com/nowork-studio/notfair-plugin)** — Claude Code plugin for SEO and Google Ads that includes a Gemini cross-model review skill. Uses Gemini for second-opinion reviews on Google Ads campaigns, SEO metadata, and schema markup — leveraging Gemini's native Google ecosystem knowledge for higher-quality decisions than Claude alone. MIT, 107 stars
  <sub>★ 4k · Python · MIT · clone · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nowork-studio/notfair-plugin.git`</sub>
- **[NotFair](https://github.com/nowork-studio/notfair-plugin)** — Open-source Claude Code skills for SEO, GEO, Google Ads, and Meta Ads. Connects to live data via Google Ads MCP, Meta Ads MCP, Google Search Console MCP, and Google Analytics (GA4) MCP. Includes a /notfair:gemini cross-model review skill that runs Gemini as a second-opinion gate on ad campaigns, SEO metadata, and schema markup. MIT, ~2.9k stars
  <sub>★ 4k · Python · MIT · clone · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nowork-studio/notfair-plugin.git`</sub>
- **[Git-Alchemist](https://github.com/abduznik/Git-Alchemist)** — A unified AI-powered CLI tool for automating GitHub repository management (issues, PRs, topics, profiles) powered by Gemini 3 and Gemma 3
  <sub>★ 22 · Python · MIT · source · pushed 2026-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/abduznik/Git-Alchemist.git`</sub>

## Documentation &amp; Examples

- **[Gemini CLI Tips by Addy Osmani](https://github.com/addyosmani/gemini-cli-tips)** — ~30 pro-tips for effectively using Gemini CLI for agentic coding
  <sub>★ 2.4k · source · pushed 2025-10-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/addyosmani/gemini-cli-tips.git`</sub>
- **[gemini-cli-extension](https://github.com/philschmid/gemini-cli-extension)** — Essential collection of extensions and commands that enhance Gemini CLI with additional capabilities and workflow improvements
  <sub>★ 147 · Apache-2.0 · source · pushed 2025-07-27</sub>
  <sub>`git clone https://github.com/philschmid/gemini-cli-extension.git`</sub>
- **[gemini-docs-ext](https://github.com/markmcd/gemini-docs-ext)** — Gemini CLI extension that adds Gemini API docs and MCP
  <sub>★ 55 · Apache-2.0 · clone · pushed 2026-01-22</sub>
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
  <sub>★ 11 · HTML · source · pushed 2026-10-15 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/ykdojo/antigravity-cli-tips.git`</sub>
- **[Gemini CLI limits &amp; pricing (QuotaBurn)](https://quotaburn.com/gemini-cli-limits/?utm_source=awesome-gemini-cli&utm_medium=referral)** — Source-linked guide to Gemini CLI daily request quotas, the free-tier change, and per-token API cost
  <sub>website</sub>
  <sub>`https://quotaburn.com/gemini-cli-limits/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>
- **[MCP servers, harness by harness (RigFit)](https://rigfit-harness.vercel.app/mcp-servers-by-harness/?utm_source=awesome-gemini-cli&utm_medium=referral)** — One MCP server (Context7) configured in Gemini CLI's settings.json alongside Claude Code, Codex CLI, OpenCode and goose, using each tool's documented syntax, with sources dated
  <sub>website</sub>
  <sub>`https://rigfit-harness.vercel.app/mcp-servers-by-harness/?utm_source=awesome-gemini-cli&utm_medium=referral`</sub>

## Education &amp; Study Tools

- **[Exam Cram Coach](https://github.com/ZeKaiNie/universal-examprep-skill)** — Agent Skill for exam prep that runs in Gemini CLI and other agents (npx skills add ZeKaiNie/universal-examprep-skill). Teaches from a student's own lecture slides, notes and past papers with file and page citations, crops figures from the PDFs, quizzes only from their homework and past papers, and keeps progress across sessions. English and Chinese
  <sub>★ 313 · Python · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ZeKaiNie/universal-examprep-skill`</sub>
- **[Shiori](https://github.com/kaorii-ako/Shiori-v1)** — Open-source AI study companion powered by Gemini AI. Assignments tracker, SRS flashcards, GPA predictor, AI quiz generator, Pomodoro focus timer, and Claude Code MCP server. Live demo
  <sub>★ 46 · JavaScript · MIT · clone · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kaorii-ako/Shiori-v1.git`</sub>


---

Snapshot 2026-10-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
