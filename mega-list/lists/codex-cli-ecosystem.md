# Codex CLI Ecosystem

Curated list of 150+ tools, skills, subagents & plugins for OpenAI Codex CLI

Curated by **[RoggeOhta/awesome-codex-cli](https://github.com/RoggeOhta/awesome-codex-cli)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

272 entries · 214 distinct repos · 22 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/openai/codex-plugin-cc"><img src="https://opengraph.githubassets.com/1/openai/codex-plugin-cc" width="260"></a> | <a href="https://github.com/openai/skills"><img src="https://opengraph.githubassets.com/1/openai/skills" width="260"></a> | <a href="https://github.com/openai/codex-action"><img src="https://opengraph.githubassets.com/1/openai/codex-action" width="260"></a> |
| **[Codex Plugin for Claude Code](https://github.com/openai/codex-plugin-cc)**<br>★ 33.5k | **[Skills Catalog](https://github.com/openai/skills)**<br>★ 27.5k | **[Codex Action](https://github.com/openai/codex-action)**<br>★ 1.2k |
| <a href="https://developers.openai.com/codex"><img src="https://learn.chatgpt.com/og/docs.png" width="260"></a> | <a href="https://developers.openai.com/codex/skills"><img src="https://learn.chatgpt.com/og/docs/build-skills.png" width="260"></a> | <a href="https://developers.openai.com/codex/subagents"><img src="https://learn.chatgpt.com/og/docs/agent-configuration/subagents.png" width="260"></a> |
| **[Documentation](https://developers.openai.com/codex)**<br>★ — | **[Skills Docs](https://developers.openai.com/codex/skills)**<br>★ — | **[Subagents Docs](https://developers.openai.com/codex/subagents)**<br>★ — |

## Contents

- [Official Resources](#official-resources) (21)
- [Getting Started](#getting-started) (5)
- [Skills](#skills) (48)
- [AGENTS.md Templates](#agentsmd-templates) (7)
- [Subagents](#subagents) (15)
- [MCP Servers](#mcp-servers) (20)
- [GUI &amp; Desktop Apps](#gui--desktop-apps) (18)
- [Remote Access](#remote-access) (8)
- [IDE &amp; Editor Integrations](#ide--editor-integrations) (10)
- [Shell &amp; Terminal](#shell--terminal) (5)
- [Hooks](#hooks) (5)
- [Plugins](#plugins) (5)
- [Model Providers &amp; Proxies](#model-providers--proxies) (10)
- [Account &amp; Auth](#account--auth) (9)
- [Cross-Agent Tools](#cross-agent-tools) (15)
- [Session &amp; Workflow Management](#session--workflow-management) (21)
- [CI/CD &amp; Automation](#cicd--automation) (2)
- [Monitoring &amp; Analytics](#monitoring--analytics) (9)
- [Docker &amp; Sandboxing](#docker--sandboxing) (4)
- [Comparisons](#comparisons) (9)
- [Tutorials &amp; Articles](#tutorials--articles) (15)
- [Community](#community) (11)

## Official Resources

- **[Codex Plugin for Claude Code](https://github.com/openai/codex-plugin-cc)** — Official plugin to use Codex from Claude Code for code reviews and task delegation
  <sub>★ 33.5k · JavaScript · Apache-2.0 · npm · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @openai/codex`</sub>
- **[Skills Catalog](https://github.com/openai/skills)** — Official skills catalog: .system, .curated, and .experimental skills. The authoritative upstream source
  <sub>★ 27.5k · Python · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/openai/skills.git`</sub>
- **[Codex Action](https://github.com/openai/codex-action)** — Official GitHub Action for running codex exec in CI with sandbox controls
  <sub>★ 1.2k · TypeScript · Apache-2.0 · gh-action · pushed 2026-09-19</sub>
  <sub>`uses: openai/codex-action@main # in .github/workflows/*.yml`</sub>
- **[Documentation](https://developers.openai.com/codex)** — Official docs covering setup, config, security, and all features
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex`</sub>
- **[Config Reference](https://developers.openai.com/codex/config-reference)** — Configuration options for config.toml
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/config-reference`</sub>
- **[Skills Docs](https://developers.openai.com/codex/skills)** — How to create and use SKILL.md files
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/skills`</sub>
- **[Subagents Docs](https://developers.openai.com/codex/subagents)** — Multi-agent orchestration with .toml agent definitions
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/subagents`</sub>
- **[Plugins Docs](https://developers.openai.com/codex/plugins)** — Distributable bundles of skills + apps + MCP servers
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/plugins`</sub>
- **[MCP Docs](https://developers.openai.com/codex/mcp)** — Using Codex as MCP client and server
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/mcp`</sub>
- **[Hooks Docs](https://developers.openai.com/codex/hooks)** — User-defined shell scripts in the agentic loop (beta)
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/hooks`</sub>
- **[Security &amp; Sandboxing](https://developers.openai.com/codex/security)** — Seatbelt (macOS), Landlock/Bubblewrap (Linux), restricted-token (Windows)
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/security`</sub>
- **[Non-interactive Mode](https://developers.openai.com/codex/noninteractive)** — codex exec for CI/CD and scripting
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/noninteractive`</sub>
- **[Slash Commands](https://developers.openai.com/codex/cli/slash-commands)** — Built-in commands including: /plan, /skills, /fast, /fork, /review, etc
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/cli/slash-commands`</sub>
- **[Best Practices](https://developers.openai.com/codex/learn/best-practices)** — Official tips for getting the most out of Codex
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/learn/best-practices`</sub>
- **[Multi-Agent Guide](https://developers.openai.com/codex/multi-agent/)** — Parallel fan-out, max_threads, depth control
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/multi-agent/`</sub>
- **[Workflows](https://developers.openai.com/codex/workflows/)** — Automation recipes and patterns
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/workflows/`</sub>
- **[Exec Policy](https://developers.openai.com/codex/exec-policy)** — Starlark-based fine-grained permission rules
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/exec-policy`</sub>
- **[Speed / Fast Mode](https://developers.openai.com/codex/speed)** — 1.5x speed, 2x credits
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/speed`</sub>
- **[AGENTS.md Guide](https://developers.openai.com/codex/guides/agents-md)** — Project-level instructions for Codex
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/guides/agents-md`</sub>
- **[Codex Web](https://chatgpt.com/codex)** — Cloud-hosted Codex via ChatGPT
  <sub>website</sub>
  <sub>`https://chatgpt.com/codex`</sub>
- **[Codex for OSS Fund](https://openai.com/form/codex-for-oss/)** — Free Codex access for open-source maintainers
  <sub>website</sub>
  <sub>`https://openai.com/form/codex-for-oss/`</sub>

## Getting Started

- **[DataCamp Tutorial](https://www.datacamp.com/tutorial/open-ai-codex-cli-tutorial)** — Beginner-friendly walkthrough with screenshots. Good first read
  <sub>website</sub>
  <sub>`https://www.datacamp.com/tutorial/open-ai-codex-cli-tutorial`</sub>
- **[Blott Studio Guide](https://www.blott.studio/blog/post/openai-codex-cli-build-faster-code-right-from-your-terminal)** — Practical getting-started guide focused on real development workflow
  <sub>website</sub>
  <sub>`https://www.blott.studio/blog/post/openai-codex-cli-build-faster-code-right-from-your-terminal`</sub>
- **[Medium Quick Setup](https://medium.com/ai-software-engineer/how-to-install-and-use-openai-codex-cli-in-2-minutes-29e9fdd0e8c5)** — 2-minute install-to-first-prompt guide. No fluff
  <sub>website</sub>
  <sub>`https://medium.com/ai-software-engineer/how-to-install-and-use-openai-codex-cli-in-2-minutes-29e9fdd0e8c5`</sub>
- **[OpenReplay Integration Guide](https://blog.openreplay.com/integrate-openais-codex-cli-tool-development-workflow/)** — How to weave Codex into an existing dev workflow
  <sub>website</sub>
  <sub>`https://blog.openreplay.com/integrate-openais-codex-cli-tool-development-workflow/`</sub>
- **[Machine Learning Mastery](https://machinelearningmastery.com/understanding-openai-codex-cli-commands/)** — Command reference with examples for each mode
  <sub>website</sub>
  <sub>`https://machinelearningmastery.com/understanding-openai-codex-cli-commands/`</sub>

## Skills

- **[affaan-m/ECC](https://github.com/affaan-m/ECC)** — Skills, memory, security checks, and workflow configuration for Codex and other coding agents
  <sub>★ 265.1k · JavaScript · MIT · npm · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g ecc-universal@2.2.2`</sub>
- **[Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)** — Turn any codebase into an interactive knowledge graph you can explore, search, and query. Multi-platform including Codex
  <sub>★ 83.7k · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz /path/to/analyzed/project`</sub>
- **[sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)** — Searchable agent skills catalog with CLI, local MCP, and plugin integrations for Codex and other coding agents
  <sub>★ 46.8k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentic-awesome-skills --antigravity --skills brainstorming,systematic-debugging --dry-run`</sub>
- **[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)** — 1,000+ agent skills from official dev teams and community. Works with Codex, Claude Code, Gemini CLI, Cursor
  <sub>★ 34.7k · MIT · source · pushed 2026-09-21 · macOS</sub>
  <sub>`git clone https://github.com/VoltAgent/awesome-agent-skills.git`</sub>
- **[Mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)** — Security-focused skills: vulnerability scanning, dependency auditing, OWASP checks. Works in Codex too despite the name
  <sub>★ 33.2k · Python · Apache-2.0 · npx · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add mukul975/Anthropic-Cybersecurity-Skills`</sub>
- **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** — 220+ skills across engineering, marketing, compliance, C-level advisory. Works with Codex despite the name
  <sub>★ 26.2k · Python · MIT · npx · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-skills-cli add alirezarezvani/claude-skills --agent codex`</sub>
- **[JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)** — Large curated skills repository with broad category coverage
  <sub>★ 26.1k · TypeScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add jimliu/baoyu-skills`</sub>
- **[composio-community/awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills)** — Community collection of practical Codex skills for development, productivity, and SaaS workflows
  <sub>★ 16.6k · Python · clone · pushed 2026-07-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ComposioHQ/awesome-codex-skills.git`</sub>
- **[wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** — ARIS - lightweight Markdown-only skills for autonomous ML research: cross-model review loops, idea discovery, experiment automation
  <sub>★ 16.5k · Python · MIT · clone · pushed 2026-09-18 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git`</sub>
- **[deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)** — Product management skills framework built on battle-tested methods for Claude Code, Codex, and AI agents
  <sub>★ 7k · Shell · source · pushed 2026-09-01</sub>
  <sub>`git clone https://github.com/deanpeters/Product-Manager-Skills.git`</sub>
- **[Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills)** — ML/CV/NLP paper writing skill package curated from Prof. Peng Sida's open notes
  <sub>★ 7k · MIT · source · pushed 2026-06-23</sub>
  <sub>`git clone https://github.com/Master-cai/Research-Paper-Writing-Skills.git`</sub>
- **[heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)** — Cross-platform skills that work in Codex, Claude Code, and Gemini CLI
  <sub>★ 6.2k · TypeScript · MIT · npx · pushed 2026-04-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills find [query] # Search for related skills`</sub>
- **[twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill)** — SwiftUI agent skill by Paul Hudson. Covers navigation, layout, animations, state management, VoiceOver
  <sub>★ 4.8k · MIT · npx · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro`</sub>
- **[Dimillian/Skills](https://github.com/Dimillian/Skills)** — Codex skills by Thomas Ricouard: App Store changelog, iOS debugging, macOS packaging, SwiftUI perf audits
  <sub>★ 4k · Shell · MIT · source · pushed 2026-03-29 · macOS?</sub>
  <sub>`git clone https://github.com/Dimillian/Skills.git`</sub>
- **[white0dew/XiaohongshuSkills](https://github.com/white0dew/XiaohongshuSkills)** — Xiaohongshu (Little Red Book) auto-publish, auto-comment, auto-search skill for Codex and Claude Code
  <sub>★ 3.4k · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/white0dew/XiaohongshuSkills.git`</sub>
- **[ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills)** — Agent skills for CTF challenges - web exploitation, binary pwn, crypto, reverse engineering, forensics, OSINT
  <sub>★ 3.3k · Python · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ljagiello/ctf-skills`</sub>
- **[runkids/skillshare](https://github.com/runkids/skillshare)** — CLI to sync skills across 55+ AI CLI tools from a single source. Security-audited Go binary
  <sub>★ 2.7k · Go · MIT · psh · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/runkids/skillshare/main/install.ps1 | iex`</sub>
- **[leo-lilinxiao/codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch)** — Self-directed iterative research skill that continuously cycles through modify, verify, and improve
  <sub>★ 2.6k · Python · MIT · source · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leo-lilinxiao/codex-autoresearch.git`</sub>
- **[badlogic/pi-skills](https://github.com/badlogic/pi-skills)** — Skills for Pi coding agent, compatible with Claude Code and Codex CLI
  <sub>★ 2.5k · JavaScript · MIT · clone · pushed 2026-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/badlogic/pi-skills`</sub>
- **[Shpigford/chops](https://github.com/Shpigford/chops)** — macOS app to browse, edit, and manage skills across Claude Code, Cursor, Codex, and more
  <sub>★ 1.9k · Swift · clone · pushed 2026-08-23 · macOS</sub>
  <sub>`git clone https://github.com/Shpigford/chops.git`</sub>
- **[Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills)** — Platform-agnostic skills organized by use case
  <sub>★ 1.8k · Python · source · pushed 2026-07-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Prat011/awesome-llm-skills.git`</sub>
- **[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills)** — Agent-optimized React Native skills by Callstack: best practices, optimization, upgrade workflows
  <sub>★ 1.7k · Shell · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add callstackincubator/agent-skills --skill '*'`</sub>
- **[Dimillian/CodexSkillManager](https://github.com/Dimillian/CodexSkillManager)** — macOS SwiftUI app to manage local Codex and Claude Code skills. Browse and download from Clawdhub
  <sub>★ 1.4k · Swift · MIT · source · pushed 2026-01-18 · macOS</sub>
  <sub>`git clone https://github.com/Dimillian/CodexSkillManager.git`</sub>
- **[aklofas/kicad-happy](https://github.com/aklofas/kicad-happy)** — KiCad PCB design assistant. Proof that skills can go deep into niche domains
  <sub>★ 1.3k · Python · MIT · gh-action · pushed 2026-09-13</sub>
  <sub>`uses: aklofas/kicad-happy@main # in .github/workflows/*.yml`</sub>
- **[dpearson2699/swift-ios-skills](https://github.com/dpearson2699/swift-ios-skills)** — 76 agent skills for iOS 26+, Swift 6.3, SwiftUI, and modern Apple frameworks
  <sub>★ 1.1k · Python · npx · pushed 2026-07-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add dpearson2699/swift-ios-skills`</sub>
- **[jiweiyeah/Skills-Manager](https://github.com/jiweiyeah/Skills-Manager)** — Cross-platform desktop app (Tauri 2.0 + React 19 + Rust) for managing skills across multiple AI tools
  <sub>★ 997 · TypeScript · MIT · brew · pushed 2026-09-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask jiweiyeah/tap/skills-manager`</sub>
- **[Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill)** — LLM-first SEO analysis with 16 sub-skills, 10 specialist agents, and 33 utility scripts
  <sub>★ 925 · Python · MIT · script · pushed 2026-07-23 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/install.sh | bash -s -- --online`</sub>
- **[Upskill](https://github.com/huggingface/upskill)** — Hugging Face's official skill pack for ML/AI development workflows
  <sub>★ 750 · Python · Apache-2.0 · uv · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx upskill`</sub>
- **[skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills)** — Community-driven skill marketplace with quality ratings
  <sub>★ 680 · CC0-1.0 · source · pushed 2026-05-14</sub>
  <sub>`git clone https://github.com/skillmatic-ai/awesome-agent-skills.git`</sub>
- **[aldefy/compose-skill](https://github.com/aldefy/compose-skill)** — Jetpack Compose agent skill with actual androidx source code receipts. Works with Codex CLI, Claude Code, Gemini CLI
  <sub>★ 588 · Kotlin · clone · pushed 2026-07-23</sub>
  <sub>`git clone https://github.com/aldefy/compose-skill.git`</sub>
- **[codexstar69/bug-hunter](https://github.com/codexstar69/bug-hunter)** — Adversarial AI bug hunter with auto-fix - multi-agent pipeline finds security vulnerabilities, logic errors, and runtime bugs
  <sub>★ 514 · JavaScript · MIT · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes https://github.com/codexstar69/bug-hunter/archive/refs/heads/main.tar.gz install --agent codex`</sub>
- **[mxyhi/ok-skills](https://github.com/mxyhi/ok-skills)** — 55 curated skills and AGENTS.md playbooks: research, planning, GitHub automation, browser QA, frontend design
  <sub>★ 490 · HTML · Apache-2.0 · clone · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/mxyhi/ok-skills.git`</sub>
- **[aiskillstore/marketplace](https://github.com/aiskillstore/marketplace)** — Security-audited skills marketplace. One-click install with automated security analysis
  <sub>★ 429 · Python · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skillstore add author/skill-name`</sub>
- **[nicepkg/ai-workflow](https://github.com/nicepkg/ai-workflow)** — Workflow automation skills - chained multi-step tasks with conditional logic
  <sub>★ 283 · HTML · MIT · npx · pushed 2026-01-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx add-skill nicepkg/ai-workflow/workflows/content-creator-workflow`</sub>
- **[cathrynlavery/codex-skill](https://github.com/cathrynlavery/codex-skill)** — Clean, well-documented single-purpose skills. Good reference for writing your own
  <sub>★ 218 · Python · MIT · clone · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cathrynlavery/codex-skill.git`</sub>
- **[SkyworkAI/Skywork-Skills](https://github.com/SkyworkAI/Skywork-Skills)** — Agent skills for AI office suites: PPT, Document, Excel, Image, Search, Music
  <sub>★ 203 · Python · MIT · npx · pushed 2026-04-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add git@github.com:SkyworkAI/Skywork-Skills.git`</sub>
- **[Frankieli123/grok-skill](https://github.com/Frankieli123/grok-skill)** — Log analysis and pattern matching. Useful for debugging production issues
  <sub>★ 183 · Python · clone · pushed 2026-03-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Frankieli123/grok-skill.git`</sub>
- **[Karanjot786/agent-skills-cli](https://github.com/Karanjot786/agent-skills-cli)** — CLI tool to discover, install, and manage skills from the community
  <sub>★ 181 · TypeScript · MIT · npm · pushed 2026-05-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-skills-cli`</sub>
- **[proflead/codex-skills-library](https://github.com/proflead/codex-skills-library)** — Focused collection: code review, Git workflow, documentation generation
  <sub>★ 148 · source · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/proflead/codex-skills-library.git`</sub>
- **[voidful/academic-skills](https://github.com/voidful/academic-skills)** — Complete academic research skill suite for Claude Code, Codex CLI, and Gemini CLI
  <sub>★ 127 · TeX · MIT · source · pushed 2026-04-04</sub>
  <sub>`git clone https://github.com/voidful/academic-skills.git`</sub>
- **[qtzx06/yolodex](https://github.com/qtzx06/yolodex)** — Computer vision / YOLO model training workflow
  <sub>★ 96 · Python · clone · pushed 2026-04-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/qtzx06/yolodex`</sub>
- **[simota/agent-skills](https://github.com/simota/agent-skills)** — 100+ specialized AI agent skills for Claude Code / Codex CLI / Gemini CLI - dev, security, design, FinOps, compliance, testing
  <sub>★ 80 · Python · MIT · clone · pushed 2026-09-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/simota/agent-skills.git`</sub>
- **[DargonLee/skill-switch](https://github.com/DargonLee/skill-switch)** — Cross-platform desktop app for managing AI tool skill files - unified interface for Codex CLI, Claude Code, Gemini CLI, Cursor
  <sub>★ 70 · TypeScript · source · pushed 2026-05-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/DargonLee/skill-switch.git`</sub>
- **[mrvladd-d/memobank](https://github.com/mrvladd-d/memobank)** — Agent-first Memory Bank skill pack for Codex CLI, Claude Code, and similar runtimes
  <sub>★ 55 · JavaScript · MIT · source · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mrvladd-d/memobank.git`</sub>
- **[gmh5225/awesome-skills](https://github.com/gmh5225/awesome-skills)** — Curated list of agent skills and tools for Claude Code, Codex, Gemini CLI, GitHub Copilot, and more
  <sub>★ 48 · MIT · npx · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add yaklang/hack-skills`</sub>
- **[Cpp1022/concise](https://github.com/Cpp1022/concise)** — Chinese-first instructions for concise Codex replies, with a shared SKILL.md rule source
  <sub>★ 3 · PowerShell · MIT · psh · pushed 2026-06-13 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/Cpp1022/concise/main/install.ps1 | iex`</sub>
- **[legendaryvibecoder/gigabrain](https://github.com/legendaryvibecoder/gigabrain)** — Local-first memory layer for Codex CLI: capture, recall, dedupe, and native sync across sessions
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx gigabrainctl init --project-root /path/to/repo`</sub>
- **[Gitmaxd/deepagents-cli-codex-skill](https://github.com/Gitmaxd/deepagents-cli-codex-skill)** — Deep Agents CLI skill - scaffolds Codex skills and launches production subagent pipelines
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-02-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx deepagents-cli-codex-skill init`</sub>

## AGENTS.md Templates

- **[agentsmd/agents.md](https://github.com/agentsmd/agents.md)** — The open AGENTS.md specification under Linux Foundation. 60k+ adopting projects
  <sub>★ 24.6k · TypeScript · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentsmd/agents.md.git`</sub>
- **[caliber-ai-org/ai-setup](https://github.com/caliber-ai-org/ai-setup)** — Cross-tool config generator - outputs AGENTS.md, CLAUDE.md, and .cursorrules from one source
  <sub>★ 1.3k · TypeScript · MIT · npx · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @rely-ai/caliber bootstrap`</sub>
- **[claude-codex-settings](https://github.com/fcakyon/claude-codex-settings)** — Dual AGENTS.md + CLAUDE.md setup for teams running both agents side-by-side
  <sub>★ 1.1k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx skills add https://github.com/fcakyon/claude-codex-settings/tree/main/plugins/anthropic-office-skills --skill '*'`</sub>
- **[codex-cli-best-practice](https://github.com/shanraisshan/codex-cli-best-practice)** — Battle-tested AGENTS.md patterns with sandbox mode recommendations and approval policies
  <sub>★ 997 · Python · MIT · source · pushed 2026-06-04 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/shanraisshan/codex-cli-best-practice.git`</sub>
- **[Ischca/awesome-agents-md](https://github.com/Ischca/awesome-agents-md)** — Curated list of real-world AGENTS.md files, templates, guides, and tools for Codex-based agents
  <sub>★ 81 · source · pushed 2025-08-20</sub>
  <sub>`git clone https://github.com/Ischca/awesome-agents-md.git`</sub>
- **[danielrosehill/Agents.md-Templates](https://github.com/danielrosehill/Agents.md-Templates)** — Collection of AGENTS.md templates following the standard suggested by OpenAI
  <sub>★ 9 · Python · source · pushed 2025-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/danielrosehill/Agents.md-Templates.git`</sub>
- **[agents.md (Open Standard)](https://agents.md)** — The cross-agent standard used by 20k+ projects. Works with Codex, Claude Code, Gemini CLI, and more
  <sub>website</sub>
  <sub>`https://agents.md`</sub>

## Subagents

- **[Untrivial-ai/agent-orchestrator](https://github.com/Untrivial-ai/agent-orchestrator)** — Agentic orchestrator for parallel coding agents - plans tasks, spawns agents, handles CI fixes and merge conflicts autonomously
  <sub>★ 12.3k · Go · Apache-2.0 · clone · pushed 2026-09-22 · macOS</sub>
  <sub>`git clone https://github.com/Untrivial-ai/agent-orchestrator.git`</sub>
- **[VoltAgent/awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents)** — The definitive collection. 136+ agents across 10 categories (core dev, language specialists, infra, security, data/AI, DX, domains, business, meta, orchestration). Just clone and use
  <sub>★ 6.2k · MIT · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/VoltAgent/awesome-codex-subagents.git`</sub>
- **[GreenSheep01201/claw-empire](https://github.com/GreenSheep01201/claw-empire)** — Local-first AI agent office simulator. Orchestrates CLI, OAuth, and API-connected agents as a virtual autonomous company
  <sub>★ 1.4k · TypeScript · Apache-2.0 · clone · pushed 2026-03-16 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/GreenSheep01201/claw-empire.git`</sub>
- **[mco-org/mco](https://github.com/mco-org/mco)** — Neutral orchestration layer for Claude Code, Codex CLI, Gemini CLI, OpenCode, Qwen Code. Works from any IDE or shell
  <sub>★ 523 · Python · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @tt-a1i/mco@latest install`</sub>
- **[aannoo/hcom](https://github.com/aannoo/hcom)** — Hierarchical agent communication framework. Agents delegate subtasks with context preservation
  <sub>★ 511 · Rust · MIT · psh · pushed 2026-09-13 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://github.com/aannoo/hcom/releases/latest/download/hcom-installer.ps1 | iex`</sub>
- **[waltstephen/ArgusBot](https://github.com/waltstephen/ArgusBot)** — 24/7 supervisor agent that keeps Codex and Claude Code running, reviewing, and planning until tasks are done
  <sub>★ 316 · Python · MIT · clone · pushed 2026-04-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone <your-ArgusBot-repo-url>`</sub>
- **[atticus98/codex-turbo](https://github.com/atticus98/codex-turbo)** — Multi-agent parallel scheduling config templates for primary agent coordination and sub-agent distribution
  <sub>★ 203 · MIT · source · pushed 2026-05-28</sub>
  <sub>`git clone https://github.com/atticus98/codex-turbo.git`</sub>
- **[shinpr/sub-agents-skills](https://github.com/shinpr/sub-agents-skills)** — Cross-LLM sub-agent orchestration - routes tasks to Codex for fast refactors, Claude Code for long reasoning, Gemini for large-context analysis
  <sub>★ 88 · Python · MIT · script · pushed 2026-09-06 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/shinpr/sub-agents-skills/main/install.sh | bash -s -- --target ~/.cursor/skills`</sub>
- **[leonardsellem/codex-specialized-subagents](https://github.com/leonardsellem/codex-specialized-subagents)** — Niche agents: accessibility auditor, i18n extractor, performance profiler. Fills gaps VoltAgent doesn't cover
  <sub>★ 69 · TypeScript · MIT · source · pushed 2025-12-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leonardsellem/codex-specialized-subagents.git`</sub>
- **[CoderMageFox/claudecode-codex-subagents](https://github.com/CoderMageFox/claudecode-codex-subagents)** — Agents that work across both Codex and Claude Code. Good for mixed teams
  <sub>★ 49 · Shell · MIT · clone · pushed 2025-11-07 · macOS?</sub>
  <sub>`git clone https://github.com/CoderMageFox/claudecode-codex-subagents.git`</sub>
- **[sehoon787/my-codex](https://github.com/sehoon787/my-codex)** — All-in-one agent harness for Codex CLI - Boss meta-orchestrator, 400+ agents, 200+ skills, 3 MCP servers
  <sub>★ 28 · Shell · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sehoon787/my-codex -y -g`</sub>
- **[obra/external-subagents](https://github.com/obra/external-subagents)** — Run subagents as external processes with custom sandboxing
  <sub>★ 24 · JavaScript · clone · pushed 2025-12-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/obra/external-subagents`</sub>
- **[RBraga01/a-team](https://github.com/RBraga01/a-team)** — Specialist agents and workflow skills for planning, implementation, and review, with Codex integration
  <sub>★ 19 · JavaScript · MIT · psh · pushed 2026-08-09 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/RBraga01/a-team/main/install.ps1 | iex`</sub>
- **[betterup/codex-cli-subagents](https://github.com/betterup/codex-cli-subagents)** — Enterprise-focused agents for code review, migration, and compliance
  <sub>★ 18 · Python · MIT · source · pushed 2025-11-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/betterup/codex-cli-subagents.git`</sub>
- **[Alexin09/cc-subagent-codex](https://github.com/Alexin09/cc-subagent-codex)** — Lightweight subagent pack focused on TypeScript/React projects
  <sub>★ 17 · Shell · MIT · npx · pushed 2026-03-25 · WSL2 · macOS? · Linux</sub>
  <sub>`npx cc-subagent-codex`</sub>

## MCP Servers

- **[DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)** — Persistent project memory across sessions. Codex remembers decisions, patterns, and context
  <sub>★ 44.1k · C · MIT · psh · pushed 2026-09-22 · macOS</sub>
  <sub>`irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/scripts/setup-windows.ps1 | iex`</sub>
- **[PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp)** — Connect Codex to NotebookLM for research-augmented coding
  <sub>★ 3.4k · TypeScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx notebooklm-mcp@latest`</sub>
- **[tuannvm/codex-mcp-server](https://github.com/tuannvm/codex-mcp-server)** — General-purpose MCP server for Codex with file operations, web search, and database queries
  <sub>★ 636 · TypeScript · source · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tuannvm/codex-mcp-server.git`</sub>
- **[Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server](https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server)** — Web search MCP with rate limiting and caching
  <sub>★ 389 · Python · MIT · uv · pushed 2026-09-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx --from git+https://github.com/Shelpuk-AI-Technology-Consulting/kindly-web-search-mcp-server \`</sub>
- **[milisp/mcp-linker](https://github.com/milisp/mcp-linker)** — Link multiple MCP servers together. Chain tools across servers
  <sub>★ 326 · TypeScript · AGPL-3.0 · brew · pushed 2026-09-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask milisp/mcp-linker/mcp-linker`</sub>
- **[mrphrazer/agentic-malware-analysis](https://github.com/mrphrazer/agentic-malware-analysis)** — Agentic malware analysis environment with MCP-connected disassemblers and RE tooling
  <sub>★ 306 · YARA · GPL-2.0 · clone · pushed 2026-03-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/mrphrazer/agentic-malware-analysis.git`</sub>
- **[Wildcard-Official/deepcontext-mcp](https://github.com/Wildcard-Official/deepcontext-mcp)** — Codebase understanding server - builds semantic index for smarter code navigation
  <sub>★ 279 · TypeScript · Apache-2.0 · clone · pushed 2025-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Wildcard-Official/deepcontext-mcp.git`</sub>
- **[sandbaseai/cli](https://github.com/sandbaseai/cli)** — Connect Codex to model and API discovery, schema inspection, and execution through a local MCP bridge; free starter credits, then usage-based billing
  <sub>★ 188 · TypeScript · Apache-2.0 · npx · pushed 2026-08-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y https://github.com/sandbaseai/cli/releases/download/v0.1.17/sandbaseai-cli-0.1.17.tgz connect`</sub>
- **[cexll/codex-mcp-server](https://github.com/cexll/codex-mcp-server)** — Lightweight MCP server with minimal dependencies. Good starting point for custom servers
  <sub>★ 179 · TypeScript · MIT · npm · pushed 2026-06-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @cexll/codex-mcp-server@latest`</sub>
- **[FYZAFH/mcp-codex-dev](https://github.com/FYZAFH/mcp-codex-dev)** — Development-focused MCP server: linting, testing, deployment tools
  <sub>★ 166 · TypeScript · source · pushed 2026-02-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FYZAFH/mcp-codex-dev.git`</sub>
- **[Dekelelz/let-them-talk](https://github.com/Dekelelz/let-them-talk)** — MCP message broker + web dashboard for inter-agent communication. Lets Codex, Claude Code, Gemini CLI talk to each other
  <sub>★ 53 · JavaScript · npx · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx let-them-talk init`</sub>
- **[agency-ai-solutions/openai-codex-mcp](https://github.com/agency-ai-solutions/openai-codex-mcp)** — Full-featured Codex MCP bridge with streaming support
  <sub>★ 51 · Python · source · pushed 2025-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agency-ai-solutions/openai-codex-mcp.git`</sub>
- **[ching-kuo/claude-codex](https://github.com/ching-kuo/claude-codex)** — Claude Code workflow integrating Codex as an MCP server - plan, implement, and review loops with smart routing
  <sub>★ 24 · MIT · clone · pushed 2026-04-01</sub>
  <sub>`git clone https://github.com/<your-username>/claude-codex`</sub>
- **[Mr-Tomahawk/codex-cli-mcp-tool](https://github.com/Mr-Tomahawk/codex-cli-mcp-tool)** — Wrap Codex CLI as an MCP tool for use in other agent frameworks
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codex-cli-mcp-tool`</sub>
- **[xiaolai/codex-octopus](https://github.com/xiaolai/codex-octopus)** — One brain, many arms - spawns multiple specialized Codex agents as MCP servers
  <sub>★ 20 · TypeScript · ISC · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/xiaolai/codex-octopus.git`</sub>
- **[karad/seiro-mcp](https://github.com/karad/seiro-mcp)** — MCP server and skills for autonomous build workflows for visionOS (Swift) apps using Codex CLI
  <sub>★ 16 · Rust · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector seiro-mcp`</sub>
- **[alexanderclapp/clirank-mcp-server](https://github.com/alexanderclapp/clirank-mcp-server)** — API discovery and comparison MCP server with documented Codex setup and agent-readable integration guides
  <sub>★ 6 · JavaScript · MIT · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y clirank-mcp-server@latest`</sub>
- **[vanthienha199/agent-cost-mcp](https://github.com/vanthienha199/agent-cost-mcp)** — MCP server for tracking AI agent costs in real time - per-message spending, budget alerts, visual dashboard
  <sub>★ 1 · HTML · MIT · pip · pushed 2026-03-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-cost-mcp`</sub>
- **[Leonard013/BigBrain](https://github.com/Leonard013/BigBrain)** — MCP server that lets Claude Code talk to Codex (OpenAI) and Gemini (Google) CLIs for free
  <sub>★ 1 · Python · pip · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/Leonard013/BigBrain.git`</sub>
- **[salparadi-labs/brain](https://github.com/salparadi-labs/brain)** — Persistent memory MCP server for Codex sessions - stores decisions, tasks, preferences in SQLite
  <sub>Python · MIT · source · pushed 2026-03-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/salparadi-labs/brain.git`</sub>

## GUI &amp; Desktop Apps

- **[farion1231/cc-switch](https://github.com/farion1231/cc-switch)** — Cross-platform desktop all-in-one assistant for Claude Code, Codex, OpenCode, OpenClaw, and Gemini CLI
  <sub>★ 134.1k · Rust · MIT · brew · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask cc-switch`</sub>
- **[slopus/happy](https://github.com/slopus/happy)** — Mobile and web client for Codex and Claude Code with end-to-end encryption. iOS/Android, push notifications, open-source
  <sub>★ 23.9k · TypeScript · MIT · npm · pushed 2026-09-22 · macOS</sub>
  <sub>`npm install -g happy`</sub>
- **[Dimillian/CodexMonitor](https://github.com/Dimillian/CodexMonitor)** — Tauri/React/Rust desktop app for orchestrating multiple Codex agents across workspaces. Multi-workspace, Git integration, prompt library
  <sub>★ 4.3k · TypeScript · MIT · source · pushed 2026-03-26 · macOS</sub>
  <sub>`git clone https://github.com/Dimillian/CodexMonitor.git`</sub>
- **[just-every/code](https://github.com/just-every/code)** — Enhanced Codex CLI fork with browser integration, multi-agent automation, Auto Drive orchestration, and theming
  <sub>★ 4k · Rust · Apache-2.0 · npm · pushed 2026-09-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @just-every/code`</sub>
- **[ilysenko/codex-desktop-linux](https://github.com/ilysenko/codex-desktop-linux)** — Automated installer to run the OpenAI Codex Desktop app on Linux
  <sub>★ 3.8k · JavaScript · MIT · clone · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ilysenko/codex-desktop-linux.git`</sub>
- **[xintaofei/codeg](https://github.com/xintaofei/codeg)** — Electron-based GUI with project templates and one-click sandboxing
  <sub>★ 3.6k · Rust · Apache-2.0 · psh · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/xintaofei/codeg/main/install.ps1 | iex`</sub>
- **[nexu-io/nexu](https://github.com/nexu-io/nexu)** — Local-first desktop client bridging agents to WeChat, Feishu, Slack, Discord. BYOK
  <sub>★ 3.3k · TypeScript · MIT · source · pushed 2026-04-26 · macOS</sub>
  <sub>`git clone https://github.com/nexu-io/nexu.git`</sub>
- **[The-Vibe-Company/companion](https://github.com/The-Vibe-Company/companion)** — Web and mobile UI for Claude Code and Codex. Launch sessions, stream responses, approve tools from browser/mobile
  <sub>★ 2.4k · TypeScript · MIT · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm --env-file .env.production companions.build migrate`</sub>
- **[dou-jiang/codex-console](https://github.com/dou-jiang/codex-console)** — Integrated console for Codex: task management, batch processing, data export, auto-upload, log viewing
  <sub>★ 2.2k · Python · MIT · source · pushed 2026-08-06 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/dou-jiang/codex-console.git`</sub>
- **[cnlimiter/codex-manager](https://github.com/cnlimiter/codex-manager)** — Desktop manager for Codex CLI with task management and batch processing
  <sub>★ 2k · Python · MIT · clone · pushed 2026-03-28 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/cnlimiter/codex-register.git`</sub>
- **[DeadWaveWave/opencove](https://github.com/DeadWaveWave/opencove)** — Infinite canvas workspace for agents, tasks, knowledge, and research
  <sub>★ 1.6k · TypeScript · MIT · script · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/DeadWaveWave/opencove/releases/latest/download/opencove-install.sh | sh`</sub>
- **[milisp/codexia](https://github.com/milisp/codexia)** — Desktop GUI for Codex CLI. macOS/Windows/Linux. Visual session management, file tree, diff viewer
  <sub>★ 918 · TypeScript · MIT · scoop · pushed 2026-09-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add milisp https://github.com/milisp/scoop-bucket scoop install codexia`</sub>
- **[nkmr-jp/prompt-line](https://github.com/nkmr-jp/prompt-line)** — Minimal prompt-centric UI. Stays out of your way
  <sub>★ 148 · TypeScript · MIT · brew · pushed 2026-09-18 · macOS</sub>
  <sub>`brew install --cask nkmr-jp/tap/prompt-line`</sub>
- **[zhu1090093659/CodeConductor](https://github.com/zhu1090093659/CodeConductor)** — Orchestrator GUI for managing multiple Codex agents visually
  <sub>★ 80 · TypeScript · Apache-2.0 · source · pushed 2026-01-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/zhu1090093659/CodeConductor.git`</sub>
- **[onewesong/codex-viz](https://github.com/onewesong/codex-viz)** — Local-first dashboard for Codex sessions - trends, token usage, tool insights, and word cloud from session history
  <sub>★ 74 · TypeScript · MIT · source · pushed 2026-01-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/onewesong/codex-viz.git`</sub>
- **[Cocoanetics/CodexMonitor](https://github.com/Cocoanetics/CodexMonitor)** — macOS menu bar app to list, inspect, and watch local Codex CLI sessions. Includes VS Code integration
  <sub>★ 7 · Swift · source · pushed 2026-02-11 · macOS</sub>
  <sub>`git clone https://github.com/Cocoanetics/CodexMonitor.git`</sub>
- **[michaelversus/BuildrAIApp](https://github.com/michaelversus/BuildrAIApp)** — Free macOS app for reviewing local Codex sessions, token usage, tool activity, and exportable reports; repository hosts support resources
  <sub>★ 1 · source · pushed 2026-06-14 · macOS?</sub>
  <sub>`git clone https://github.com/michaelversus/BuildrAIApp.git`</sub>
- **[LZY-Ricardo/AIDevHub](https://github.com/LZY-Ricardo/AIDevHub)** — Desktop app (Tauri v2 + Rust + React) for managing MCP server configs and skills of Claude Code and Codex
  <sub>Rust · MIT · source · pushed 2026-05-01 · Win · WSL2? · macOS? · Linux</sub>
  <sub>`git clone https://github.com/LZY-Ricardo/AIDevHub.git`</sub>

## Remote Access

- **[Emanuele-web04/remodex](https://github.com/Emanuele-web04/remodex)** — Local-first iOS app + Mac bridge for remote Codex control. Encrypted sessions, Git integration, App Store available
  <sub>★ 3.3k · Swift · Apache-2.0 · npm · pushed 2026-09-20 · macOS</sub>
  <sub>`npm install -g remodex@latest`</sub>
- **[K9i-0/ccpocket](https://github.com/K9i-0/ccpocket)** — Access Codex from mobile devices via web UI
  <sub>★ 1.1k · Dart · MIT · npx · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @ccpocket/bridge@latest`</sub>
- **[PleasePrompto/ductor](https://github.com/PleasePrompto/ductor)** — Control Claude Code, Codex CLI, and Gemini CLI from Telegram. Live streaming, persistent memory, cron jobs, webhooks, Docker sandboxing
  <sub>★ 458 · Python · MIT · pipx · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install ductor # or: uv tool install ductor`</sub>
- **[ShunmeiCho/cc-clip](https://github.com/ShunmeiCho/cc-clip)** — Paste images into remote Claude Code and Codex CLI over SSH. Clipboard bridging for macOS and Windows
  <sub>★ 160 · Go · MIT · script · pushed 2026-08-29 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/ShunmeiCho/cc-clip/main/scripts/install.sh | sh`</sub>
- **[demoadminjie/codex-wechat](https://github.com/demoadminjie/codex-wechat)** — WeChat bridge for controlling local Codex CLI
  <sub>★ 85 · JavaScript · MIT · source · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/demoadminjie/codex-wechat.git`</sub>
- **[Headcrab/telecodex](https://github.com/Headcrab/telecodex)** — Telegram bridge for running local Codex CLI remotely with topic-aware sessions, attachments, and streamed replies
  <sub>★ 57 · Rust · MIT · clone · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Headcrab/telecodex.git`</sub>
- **[chuvadenovembro/script-to-use-codex-cli-on-remote-server](https://github.com/chuvadenovembro/script-to-use-codex-cli-on-remote-server-without-visual-environment)** — Headless server setup guide with auth workarounds
  <sub>★ 48 · Shell · source · pushed 2025-08-31 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/chuvadenovembro/script-to-use-codex-cli-on-remote-server-without-visual-environment.git`</sub>
- **[MackDing/CodexClaw](https://github.com/MackDing/CodexClaw)** — Telegram bot that proxies commands to a remote Codex instance
  <sub>★ 34 · TypeScript · MIT · clone · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MackDing/CodexClaw.git`</sub>

## IDE &amp; Editor Integrations

- **[folke/sidekick.nvim](https://github.com/folke/sidekick.nvim)** — Neovim AI sidekick supporting Claude, Gemini, Grok, Codex, Copilot CLI and more. Built-in AI terminal
  <sub>★ 2.8k · Lua · Apache-2.0 · source · pushed 2026-09-08 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/folke/sidekick.nvim.git`</sub>
- **[xenodium/agent-shell](https://github.com/xenodium/agent-shell)** — Emacs integration that works with Codex, Claude Code, and other terminal agents. Best-in-class Emacs experience
  <sub>★ 1.9k · Emacs Lisp · GPL-3.0 · source · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/xenodium/agent-shell.git`</sub>
- **[smallmain/vscode-unify-chat-provider](https://github.com/smallmain/vscode-unify-chat-provider)** — Unify multiple AI agents (Codex, Claude, Copilot) under one VS Code chat interface
  <sub>★ 721 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/smallmain/vscode-unify-chat-provider.git`</sub>
- **[tninja/ai-code-interface.el](https://github.com/tninja/ai-code-interface.el)** — Emacs interface for multiple AI coding agents including Codex
  <sub>★ 283 · Emacs Lisp · Apache-2.0 · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tninja/ai-code-interface.el.git`</sub>
- **[johnseth97/codex.nvim](https://github.com/johnseth97/codex.nvim)** — Neovim plugin with floating terminal, keybindings, and context passing
  <sub>★ 265 · Lua · source · pushed 2025-11-20</sub>
  <sub>`git clone https://github.com/johnseth97/codex.nvim.git`</sub>
- **[milanglacier/yarepl.nvim](https://github.com/milanglacier/yarepl.nvim)** — REPL framework for Neovim. Supports Codex as a REPL target alongside Python, R, etc
  <sub>★ 252 · Lua · GPL-3.0 · source · pushed 2026-08-02 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/milanglacier/yarepl.nvim.git`</sub>
- **[Haleclipse/Codex-JetBrains](https://github.com/Haleclipse/Codex-JetBrains)** — Run VS Code-based coding agents and extensions (including Codex) seamlessly within JetBrains IDEs
  <sub>★ 125 · Kotlin · Apache-2.0 · source · pushed 2025-12-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Haleclipse/Codex-JetBrains.git`</sub>
- **[dliedke/ClaudeCodeExtension](https://github.com/dliedke/ClaudeCodeExtension)** — Visual Studio .NET extension that supports both Claude Code and Codex CLI
  <sub>★ 70 · C# · MIT · source · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dliedke/ClaudeCodeExtension.git`</sub>
- **[bennfocus/codex-cli.el](https://github.com/bennfocus/codex-cli.el)** — Lightweight Emacs wrapper. Minimal, focused
  <sub>★ 29 · Emacs Lisp · MIT · source · pushed 2025-09-14 · Win?</sub>
  <sub>`git clone https://github.com/bennfocus/codex-cli.el.git`</sub>
- **[VS Code Extension (Official)](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)** — The official extension. Inline chat, terminal integration, code actions
  <sub>website</sub>
  <sub>`https://marketplace.visualstudio.com/items?itemName=openai.chatgpt`</sub>

## Shell &amp; Terminal

- **[tom-doerr/zsh_codex](https://github.com/tom-doerr/zsh_codex)** — Zsh plugin for AI-powered command completion using Codex
  <sub>★ 1.7k · Python · MIT · clone · pushed 2025-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tom-doerr/zsh_codex.git`</sub>
- **[sadjow/codex-cli-nix](https://github.com/sadjow/codex-cli-nix)** — Nix flake for reproducible Codex CLI installation
  <sub>★ 155 · Shell · MIT · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/sadjow/codex-cli-nix`</sub>
- **[tom-doerr/codex.fish](https://github.com/tom-doerr/codex.fish)** — Fish shell plugin for AI-powered command completion using Codex
  <sub>★ 87 · Python · MIT · source · pushed 2024-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tom-doerr/codex.fish.git`</sub>
- **[gravtice/ohmyzsh-ai-cli-plugins](https://github.com/gravtice/ohmyzsh-ai-cli-plugins)** — Oh My Zsh plugins for AI coding agents
  <sub>★ 19 · Shell · MIT · clone · pushed 2026-03-05 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YOUR_USERNAME/ohmyzsh-plugins.git`</sub>
- **[MengnanTech/SplitMux](https://github.com/MengnanTech/SplitMux)** — macOS terminal multiplexer with Claude Code and Codex CLI agent integration
  <sub>★ 13 · Swift · MIT · source · pushed 2026-04-11 · macOS</sub>
  <sub>`git clone https://github.com/MengnanTech/SplitMux.git`</sub>

## Hooks

- **[Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)** — OmX (Oh My codeX) - add hooks, agent teams, HUDs, and more to your Codex CLI. The most popular hooks framework
  <sub>★ 33.3k · TypeScript · MIT · npm · pushed 2026-09-22 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g oh-my-codex`</sub>
- **[PeonPing/peon-ping](https://github.com/PeonPing/peon-ping)** — Warcraft III Peon voice notifications for Codex, Claude Code, and IDEs. Stop babysitting your terminal
  <sub>★ 5k · Shell · MIT · brew · pushed 2026-08-30 · macOS</sub>
  <sub>`brew install PeonPing/tap/peon-ping`</sub>
- **[shanraisshan/codex-cli-hooks](https://github.com/shanraisshan/codex-cli-hooks)** — Starter hooks collection: pre-commit validation, cost tracking, notification triggers
  <sub>★ 71 · Python · source · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shanraisshan/codex-cli-hooks.git`</sub>
- **[vcz-Gray/loophaus](https://github.com/vcz-Gray/loophaus)** — Cross-platform iterative development loops via Stop hooks
  <sub>★ 23 · TypeScript · MIT · npm · pushed 2026-04-29 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @graypark/loophaus`</sub>
- **[liewcf/codex-notify-macos](https://github.com/liewcf/codex-notify-macos)** — macOS notification hook - get alerted when long-running tasks complete
  <sub>★ 4 · Shell · MIT · source · pushed 2026-02-26 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/liewcf/codex-notify-macos.git`</sub>

## Plugins

- **[EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)** — Compound Engineering plugin for Claude Code, Codex, and more. Structured multi-agent workflows
  <sub>★ 25.2k · TypeScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/EveryInc/compound-engineering-plugin`</sub>
- **[hashgraph-online/awesome-codex-plugins](https://github.com/hashgraph-online/awesome-codex-plugins)** — The first plugin directory. Lists 12 official + ~20 community plugins with install instructions
  <sub>★ 1.1k · Python · Apache-2.0 · source · pushed 2026-09-22 · macOS</sub>
  <sub>`git clone https://github.com/hashgraph-online/awesome-codex-plugins.git`</sub>
- **[agent-sh/agentsys](https://github.com/agent-sh/agentsys)** — Plugin framework with dependency resolution and version management
  <sub>★ 987 · JavaScript · MIT · npm · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agentsys`</sub>
- **[regenrek/codex-1up](https://github.com/regenrek/codex-1up)** — Bootstrap tool that installs Codex CLI plus curated power tools and an AGENTS.md template. Three profiles: balanced, safe, yolo
  <sub>★ 437 · TypeScript · npm · pushed 2026-02-19 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g codex-1up`</sub>
- **[xmm/codex-bmad-skills](https://github.com/xmm/codex-bmad-skills)** — BMAD methodology plugin - structured planning, design, and implementation workflow
  <sub>★ 47 · Shell · source · pushed 2026-05-19 · Win?</sub>
  <sub>`git clone https://github.com/xmm/codex-bmad-skills.git`</sub>

## Model Providers &amp; Proxies

- **[router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)** — Wrap Codex, Claude Code, Gemini CLI as OpenAI-compatible API endpoints. Multi-account load balancing, streaming
  <sub>★ 52.8k · Go · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/router-for-me/CLIProxyAPI.git`</sub>
- **[icebear0828/codex-proxy](https://github.com/icebear0828/codex-proxy)** — Lightweight local relay that converts Codex Desktop's Responses API to multiple protocol interfaces (OpenAI, Anthropic, Gemini)
  <sub>★ 1.8k · TypeScript · npm · pushed 2026-09-21 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g @icebear0828/codex-proxy`</sub>
- **[lich0821/ccNexus](https://github.com/lich0821/ccNexus)** — Intelligent API gateway for Claude Code and Codex CLI. Rotate endpoints, monitor usage, seamlessly integrate OpenAI, Gemini, and others
  <sub>★ 974 · Go · MIT · source · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/lich0821/ccNexus.git`</sub>
- **[codingmoh/open-codex](https://github.com/codingmoh/open-codex)** — Open-source Codex-inspired CLI running 100% locally with Ollama. No API key required, offline capable
  <sub>★ 695 · Python · MIT · pipx · pushed 2025-07-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pipx install open-codex`</sub>
- **[feiskyer/codex-settings](https://github.com/feiskyer/codex-settings)** — Ready-to-use configs for LiteLLM, Ollama, LM Studio, OpenRouter, and Azure OpenAI
  <sub>★ 239 · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add feiskyer/codex-settings`</sub>
- **[teabranch/open-responses-server](https://github.com/teabranch/open-responses-server)** — OpenAI Responses API-compatible server. Run Codex with local models
  <sub>★ 184 · Python · MIT · pip · pushed 2026-04-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install open-responses-server`</sub>
- **[ben-vargas/ai-sdk-provider-codex-cli](https://github.com/ben-vargas/ai-sdk-provider-codex-cli)** — Vercel AI SDK provider for Codex. Use Codex in your AI applications
  <sub>★ 68 · TypeScript · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ben-vargas/ai-sdk-provider-codex-cli.git`</sub>
- **[maksimzayats/acodex](https://github.com/maksimzayats/acodex)** — Typed Python SDK for the Codex CLI (sync/async, streaming JSONL events, structured items)
  <sub>★ 57 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install acodex`</sub>
- **[lzjever/air-gapped](https://github.com/lzjever/air-gapped)** — Portable Codex CLI + vLLM for air-gapped/offline use
  <sub>★ 22 · Shell · MIT · source · pushed 2026-03-02 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/lzjever/air-gapped.git`</sub>
- **[RomaCredit/codex-provider-switcher](https://github.com/RomaCredit/codex-provider-switcher)** — Switch local provider profiles and align Codex Desktop history metadata, with backups before changes
  <sub>★ 5 · Python · MIT · psh · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/RomaCredit/codex-provider-switcher/v0.3.2/install.ps1 | iex`</sub>

## Account &amp; Auth

- **[jlcodes99/cockpit-tools](https://github.com/jlcodes99/cockpit-tools)** — Universal AI IDE account manager for Codex, GitHub Copilot, Windsurf, Kiro, Cursor, Gemini CLI. Multi-account switching, quota monitoring
  <sub>★ 18.2k · Rust · brew · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew tap jlcodes99/cockpit-tools https://github.com/jlcodes99/cockpit-tools`</sub>
- **[qxcnm/Codex-Manager](https://github.com/qxcnm/Codex-Manager)** — Codex CLI account management and switching tool with local gateway forwarding
  <sub>★ 3k · Rust · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/qxcnm/Codex-Manager.git`</sub>
- **[Loongphy/codex-auth](https://github.com/Loongphy/codex-auth)** — CLI to switch and manage multiple Codex accounts with usage stats and automatic switching
  <sub>★ 2.7k · Zig · MIT · npm · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @loongphy/codex-auth`</sub>
- **[numman-ali/opencode-openai-codex-auth](https://github.com/numman-ali/opencode-openai-codex-auth)** — Use your ChatGPT Plus/Pro subscription as a Codex auth source. The most popular auth tool
  <sub>★ 2.2k · TypeScript · npx · pushed 2026-01-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y opencode-openai-codex-auth@latest`</sub>
- **[Lampese/codex-switcher](https://github.com/Lampese/codex-switcher)** — Switch between multiple OpenAI accounts. Useful for work/personal separation
  <sub>★ 835 · Rust · clone · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Lampese/codex-switcher.git`</sub>
- **[Ducksss/codex-profiles](https://github.com/Ducksss/codex-profiles)** — Run Codex CLI with named CODEX_HOME profiles that keep account configuration and local session state separate
  <sub>★ 164 · Shell · MIT · brew · pushed 2026-09-15 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install Ducksss/tap/codex-profile`</sub>
- **[burakdede/aisw](https://github.com/burakdede/aisw)** — AI Switcher (aisw) - CLI utility to manage multiple accounts for Claude Code, Codex CLI, and Gemini CLI
  <sub>★ 119 · Rust · MIT · cargo · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install aisw`</sub>
- **[bashar94/codex-cli-account-switcher](https://github.com/bashar94/codex-cli-account-switcher)** — Simple account switcher with profile support
  <sub>★ 84 · Shell · MIT · clone · pushed 2026-04-19 · macOS</sub>
  <sub>`git clone https://github.com/bashar94/codex-cli-account-switcher.git`</sub>
- **[bddiudiu/cpa-codex-auth-sweep-cliproxy](https://github.com/bddiudiu/cpa-codex-auth-sweep-cliproxy)** — Auth proxy for enterprise SSO environments
  <sub>★ 27 · Python · source · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bddiudiu/cpa-codex-auth-sweep-cliproxy.git`</sub>

## Cross-Agent Tools

- **[chenhg5/cc-connect](https://github.com/chenhg5/cc-connect)** — Bridge Codex/Claude Code to 10 messaging platforms (Telegram, Slack, DingTalk, WeChat Work, LINE). No public IP required
  <sub>★ 15.6k · Go · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g cc-connect`</sub>
- **[SeemSeam/claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge)** — Real-time multi-AI collaboration: Claude, Codex, Gemini in simultaneous split-pane sessions with persistent context
  <sub>★ 3.5k · Python · npm · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @seemseam/ccb@latest`</sub>
- **[op7418/Claude-to-IM-skill](https://github.com/op7418/Claude-to-IM-skill)** — Bridge Claude Code / Codex to IM platforms. Chat with AI coding agents from Telegram, Discord, or Feishu/Lark
  <sub>★ 2.9k · TypeScript · MIT · npx · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add op7418/Claude-to-IM-skill`</sub>
- **[AgentsMesh/AgentsMesh](https://github.com/AgentsMesh/AgentsMesh)** — AI Agent Fleet Command Center. Orchestrate Codex, Claude Code, Gemini CLI, Aider from a single platform with Kanban and SSO/RBAC
  <sub>★ 2.4k · Go · script · pushed 2026-08-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentsmesh.ai/install.sh | sh`</sub>
- **[pchalasani/claude-code-tools](https://github.com/pchalasani/claude-code-tools)** — Practical productivity tools for Claude Code and Codex CLI: session management, terminal automation, voice integration
  <sub>★ 2k · Python · MIT · source · pushed 2026-09-22 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/pchalasani/claude-code-tools.git`</sub>
- **[DeepMyst/Mysti](https://github.com/DeepMyst/Mysti)** — Universal agent orchestrator. Route tasks between Codex, Claude Code, and Gemini CLI based on model strengths
  <sub>★ 1.1k · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/DeepMyst/Mysti.git`</sub>
- **[catlog22/maestro-flow](https://github.com/catlog22/maestro-flow)** — Workflow orchestration with Codex and other CLI backends; successor to the archived Claude Code Workflow
  <sub>★ 556 · TypeScript · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g maestro-flow@0.5.82`</sub>
- **[josstei/maestro-orchestrate](https://github.com/josstei/maestro-orchestrate)** — Multi-agent orchestration platform for Gemini CLI, Claude Code, and Codex - 22 specialists, parallel subagents, persistent sessions
  <sub>★ 463 · JavaScript · Apache-2.0 · clone · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/josstei/maestro-orchestrate`</sub>
- **[dsifry/metaswarm](https://github.com/dsifry/metaswarm)** — Self-improving multi-agent orchestration: 18 agents, 13 skills, TDD enforcement, quality gates
  <sub>★ 419 · Shell · MIT · npx · pushed 2026-06-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx metaswarm init`</sub>
- **[oil-oil/codex](https://github.com/oil-oil/codex)** — Claude Code skill for delegating coding tasks to Codex CLI
  <sub>★ 99 · PowerShell · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add oil-oil/codex -g -y`</sub>
- **[athola/skrills](https://github.com/athola/skrills)** — Cross-platform skill format. Write once, use in Codex and Claude Code
  <sub>★ 69 · Rust · MIT · cargo · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install skrills`</sub>
- **[abhishekgahlot2/codex-claude-bridge](https://github.com/abhishekgahlot2/codex-claude-bridge)** — Run Codex and Claude Code in tandem on the same codebase
  <sub>★ 58 · JavaScript · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/abhishekgahlot2/codex-claude-bridge.git`</sub>
- **[lbb00/ai-rules-sync](https://github.com/lbb00/ai-rules-sync)** — Sync AGENTS.md ↔ CLAUDE.md ↔ .cursorrules. One source, all formats
  <sub>★ 38 · TypeScript · Unlicense · npm · pushed 2026-08-20 · macOS</sub>
  <sub>`npm install -g ai-rules-sync`</sub>
- **[jcputney/agent-peer-review](https://github.com/jcputney/agent-peer-review)** — Codex reviews Claude Code's output (and vice versa). Catches model-specific blind spots
  <sub>★ 34 · Shell · MIT · source · pushed 2026-08-06 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jcputney/agent-peer-review.git`</sub>
- **[Leoyang183/sync-agents-settings](https://github.com/Leoyang183/sync-agents-settings)** — Sync MCP server configs from Claude Code to Gemini CLI, Codex CLI, OpenCode, Kiro, Cursor. One command, all agents
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g sync-agents-settings`</sub>

## Session &amp; Workflow Management

- **[UfoMiao/zcf](https://github.com/UfoMiao/zcf)** — Zero-config workflow framework. Chain prompts, branch on results, auto-retry failures
  <sub>★ 6.1k · TypeScript · MIT · npx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx zcf i # Full initialization: install + workflows + API/CCR + MCP`</sub>
- **[gotalab/cc-sdd](https://github.com/gotalab/cc-sdd)** — Spec-driven development workflow. Write specs, Codex implements, auto-validates against spec
  <sub>★ 3.7k · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cc-sdd@latest`</sub>
- **[ryfineZ/codex-session-patcher](https://github.com/ryfineZ/codex-session-patcher)** — Lightweight Python tool to clean AI refusal responses from Codex CLI session files
  <sub>★ 2.8k · Python · clone · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ryfineZ/codex-session-patcher.git`</sub>
- **[the-open-engine/zeroshot](https://github.com/the-open-engine/zeroshot)** — Zero-shot task runner. Describe what you want in plain English, get a working codebase
  <sub>★ 1.9k · Rust · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @the-open-engine-company/zeroshot`</sub>
- **[standardagents/dmux](https://github.com/standardagents/dmux)** — Dev agent multiplexer: isolated tmux pane + Git worktree per task. Supports 11+ agents including Codex
  <sub>★ 1.8k · HTML · MIT · npm · pushed 2026-08-16 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g dmux`</sub>
- **[kbwo/ccmanager](https://github.com/kbwo/ccmanager)** — TUI session manager for Claude Code / Gemini CLI / Codex CLI / Cursor Agent / Copilot CLI / OpenCode and more
  <sub>★ 1.2k · TypeScript · MIT · npm · pushed 2026-09-13 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g ccmanager`</sub>
- **[Dicklesworthstone/coding_agent_session_search](https://github.com/Dicklesworthstone/coding_agent_session_search)** — Unified TUI and CLI to index and search local coding agent session history across 11+ providers including Codex
  <sub>★ 1.1k · Rust · scoop · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add dicklesworthstone https://github.com/Dicklesworthstone/scoop-bucket scoop install dicklesworthstone/cass`</sub>
- **[kunal12203/GrapeRoot](https://github.com/kunal12203/GrapeRoot)** — Persistent context and a code knowledge graph for coding agents, with a Codex CLI launcher
  <sub>★ 1k · PowerShell · Apache-2.0 · scoop · pushed 2026-09-03 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`scoop bucket add dual-graph https://github.com/kunal12203/scoop-dual-graph scoop install dual-graph`</sub>
- **[es617/claude-replay](https://github.com/es617/claude-replay)** — Convert AI coding agent sessions (Claude Code, Cursor, Codex) into self-contained, embeddable HTML replays
  <sub>★ 836 · JavaScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g claude-replay`</sub>
- **[mixpeek/amux](https://github.com/mixpeek/amux)** — Open-source agent multiplexer. Run dozens of parallel Codex/Claude agents unattended via tmux. Self-healing watchdog
  <sub>★ 492 · Rust · pipx · pushed 2026-09-22 · WSL2 · macOS? · Linux</sub>
  <sub>`pipx install amux`</sub>
- **[digipulse-engineering/GAAI-framework](https://github.com/digipulse-engineering/GAAI-framework)** — Drop a .gaai/ folder into any project to turn AI coding tools into reliable delivery systems. Markdown + YAML + bash
  <sub>★ 161 · Shell · clone · pushed 2026-09-22 · macOS</sub>
  <sub>`git clone https://github.com/Fr-e-d/GAAI-framework.git`</sub>
- **[GreenSheep01201/Claw-Kanban](https://github.com/GreenSheep01201/Claw-Kanban)** — AI Agent Orchestration Kanban Board. Route tasks to Claude Code, Codex CLI, and Gemini CLI with role-based auto-assignment
  <sub>★ 73 · TypeScript · Apache-2.0 · psh · pushed 2026-02-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/GreenSheep01201/Claw-Kanban/main/install.ps1 | iex`</sub>
- **[2ue/ccman](https://github.com/2ue/ccman)** — Tool for managing Claude Code + Codex API + Gemini CLI + OpenCode service provider configurations
  <sub>★ 52 · TypeScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/2ue/ccman.git`</sub>
- **[re-cinq/shift-log](https://github.com/re-cinq/shift-log)** — Automatically saves coding agents' conversations in Git Notes. Works with Codex, Claude Code, Gemini CLI, OpenCode
  <sub>★ 49 · Go · script · pushed 2026-09-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/re-cinq/shift-log/master/scripts/install.sh | bash`</sub>
- **[waskosky/agent-cli-farm](https://github.com/waskosky/agent-cli-farm)** — Tmux manager for running, monitoring, saving, and restoring Codex and other agent CLI sessions
  <sub>★ 34 · Python · MIT · source · pushed 2026-09-18 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/waskosky/agent-cli-farm.git`</sub>
- **[joseferben/hands-please](https://github.com/joseferben/hands-please)** — Human-in-the-loop workflow. Codex pauses at decision points and asks for your input
  <sub>★ 33 · TypeScript · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx hands-please --agent <agent-command> --check <check-command> --file-check <file-check-command> [options]`</sub>
- **[rxdt/loopgate_harness](https://github.com/rxdt/loopgate_harness)** — LoopGate runs Codex and other coding agents through repeated tasks with repository specs, commit gates, and quality checks
  <sub>★ 23 · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rxdt/loopgate_harness.git`</sub>
- **[lsm1103/session-dashboard](https://github.com/lsm1103/session-dashboard)** — Browse and monitor historical session records of AI programming tools (Claude Code, Codex CLI, Cursor, Aider)
  <sub>★ 16 · TypeScript · npm · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g session-dashboard`</sub>
- **[miniLV/coding-agent-memory](https://github.com/miniLV/coding-agent-memory)** — Compile local Codex and Claude Code sessions into an auditable Markdown wiki with a retrieval skill and Codex App automations
  <sub>★ 12 · JavaScript · Apache-2.0 · clone · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/miniLV/coding-agent-memory.git`</sub>
- **[yazcaleb/rses](https://github.com/yazcaleb/rses)** — Cross-resume between Claude Code, Codex CLI, and OpenCode. Pick up where one AI left off in another
  <sub>★ 10 · JavaScript · npm · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g rses-cli`</sub>
- **[manitofigh/codex-share](https://github.com/manitofigh/codex-share)** — Share and view Codex CLI conversations in the web
  <sub>★ 7 · Svelte · clone · pushed 2026-03-19</sub>
  <sub>`git clone https://github.com/user/codex-share.git`</sub>

## CI/CD &amp; Automation

- **[onurkanbakirci/awesome-codex-automations](https://github.com/onurkanbakirci/awesome-codex-automations)** — 35 automation recipes organized by category: code quality, CI/CD, releases, deps, security
  <sub>★ 46 · MIT · source · pushed 2026-02-03</sub>
  <sub>`git clone https://github.com/onurkanbakirci/awesome-codex-automations.git`</sub>
- **[Adashuai5/quota-autopilot](https://github.com/Adashuai5/quota-autopilot)** — Schedule background Codex and Claude Code tasks around subscription quota, reset windows, and recent human activity
  <sub>Python · MIT · source · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Adashuai5/quota-autopilot.git`</sub>

## Monitoring &amp; Analytics

- **[steipete/CodexBar](https://github.com/steipete/CodexBar)** — macOS menu bar app showing usage stats for Codex, Claude, Cursor, Gemini without login. On-device parsing
  <sub>★ 21.7k · Swift · MIT · brew · pushed 2026-09-22 · macOS</sub>
  <sub>`brew install --cask codexbar`</sub>
- **[ccusage/ccusage](https://github.com/ccusage/ccusage)** — Analyze local Codex and Claude Code usage with CLI reports and token-cost breakdowns
  <sub>★ 18.7k · Rust · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ccusage/ccusage.git`</sub>
- **[junhoyeo/tokscale](https://github.com/junhoyeo/tokscale)** — CLI + TUI + web dashboard tracking token usage across 16+ AI coding platforms. Rust core, contribution graphs, leaderboard
  <sub>★ 5.5k · Rust · MIT · npx · pushed 2026-09-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx tokscale@latest`</sub>
- **[graykode/abtop](https://github.com/graykode/abtop)** — Like htop but for AI coding agents. Monitor Claude Code and Codex CLI sessions, tokens, context window, rate limits in real-time
  <sub>★ 3.6k · Rust · MIT · cargo · pushed 2026-09-14 · WSL2 · macOS · Linux</sub>
  <sub>`cargo install abtop`</sub>
- **[fahd09/watchtower](https://github.com/fahd09/watchtower)** — Monitor, inspect, and debug all API traffic between AI coding agents and their APIs with a real-time web dashboard
  <sub>★ 65 · HTML · MIT · npm · pushed 2026-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g watchtower-ai`</sub>
- **[NihilDigit/waybar-ai-usage](https://github.com/NihilDigit/waybar-ai-usage)** — Waybar widget showing real-time Codex token usage and costs. Linux desktop integration
  <sub>★ 53 · Python · MIT · uv · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install git+https://github.com/NihilDigit/waybar-ai-usage`</sub>
- **[HizTam/codex-history-viewer](https://github.com/HizTam/codex-history-viewer)** — Browse and search past Codex sessions with full context
  <sub>★ 37 · TypeScript · MIT · source · pushed 2026-09-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/HizTam/codex-history-viewer.git`</sub>
- **[yoavf/ai-sessions-mcp](https://github.com/yoavf/ai-sessions-mcp)** — MCP server that tracks session history, token usage, and cost across agents
  <sub>★ 30 · Go · MIT · script · pushed 2026-08-17 · Win · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://aisessions.dev/install.sh | bash`</sub>
- **[lorytek/PulseMeter](https://github.com/lorytek/PulseMeter)** — Windows tray app showing Codex usage limits, reset credits, and local project usage estimates
  <sub>★ 4 · C# · Apache-2.0 · source · pushed 2026-09-21 · Win</sub>
  <sub>`git clone https://github.com/lorytek/PulseMeter.git`</sub>

## Docker &amp; Sandboxing

- **[Codex Universal](https://github.com/openai/codex-universal)** — Official Docker base image. Pre-configured sandbox, multi-language support
  <sub>★ 1.1k · Dockerfile · source · pushed 2026-05-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openai/codex-universal.git`</sub>
- **[DeepBlueDynamics/gnosis-container](https://github.com/DeepBlueDynamics/gnosis-container)** — Codex CLI in Docker with 275+ MCP tools, cron/file-watcher/webhook triggers, multi-model support
  <sub>★ 111 · Python · source · pushed 2026-02-26 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/DeepBlueDynamics/gnosis-container.git`</sub>
- **[libops/cli-sandbox](https://github.com/libops/cli-sandbox)** — Docker sandbox container for Claude Code, Codex, Gemini CLI, and OpenCode
  <sub>★ 6 · Shell · source · pushed 2026-09-16 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/libops/cli-sandbox.git`</sub>
- **[itscooleric/clide](https://github.com/itscooleric/clide)** — Dockerized agentic terminal - Claude Code, Copilot, Codex CLI in one sandboxed container with egress firewall and web terminal
  <sub>★ 2 · Shell · MIT · clone · pushed 2026-04-23 · macOS</sub>
  <sub>`git clone https://github.com/itscooleric/clide`</sub>

## Comparisons

- **[duanyytop/agents-radar](https://github.com/duanyytop/agents-radar)** — Side-by-side benchmark of terminal AI agents on real coding tasks
  <sub>★ 1.1k · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/duanyytop/agents-radar.git`</sub>
- **[GitHub stars](https://img.shields.io/github/stars/openai/codex?style=flat-square)** — Closed source
  <sub>website</sub>
  <sub>`https://img.shields.io/github/stars/openai/codex?style=flat-square`</sub>
- **[Hacker News Discussion](https://news.ycombinator.com/item?id=43708025)** — Community comparison thread with real-world experiences
  <sub>website</sub>
  <sub>`https://news.ycombinator.com/item?id=43708025`</sub>
- **[Reddit AMA with Codex Team](https://www.reddit.com/r/ChatGPT/comments/1ko3tp1/ama_with_openai_codex_team/)** — Team answers questions about design decisions and how Codex differs from alternatives
  <sub>website</sub>
  <sub>`https://www.reddit.com/r/ChatGPT/comments/1ko3tp1/ama_with_openai_codex_team/`</sub>
- **[Codex vs Claude Code (Builder.io)](https://www.builder.io/blog/codex-vs-claude-code)** — Side-by-side comparison with concrete benchmarks and use-case recommendations
  <sub>website</sub>
  <sub>`https://www.builder.io/blog/codex-vs-claude-code`</sub>
- **[Claude Code vs OpenAI Codex (Northflank)](https://northflank.com/blog/claude-code-vs-openai-codex)** — Infrastructure-focused comparison covering deployment scenarios and cloud sandbox use cases
  <sub>website</sub>
  <sub>`https://northflank.com/blog/claude-code-vs-openai-codex`</sub>
- **[Claude Code vs Codex vs Gemini Code Assist (Educative)](https://www.educative.io/blog/claude-code-vs-codex-vs-gemini-code-assist)** — Three-way comparison covering benchmarks, pricing, IDE integrations, and developer experience
  <sub>website</sub>
  <sub>`https://www.educative.io/blog/claude-code-vs-codex-vs-gemini-code-assist`</sub>
- **[Testing AI Coding Agents Benchmark (Render)](https://render.com/blog/ai-coding-agents-benchmark)** — Real-world benchmark from Render comparing all major terminal coding agents on actual deployment and build tasks
  <sub>website</sub>
  <sub>`https://render.com/blog/ai-coding-agents-benchmark`</sub>
- **[Codex vs Gemini CLI (UI Bakery)](https://uibakery.io/blog/codex-vs-gemini-cli)** — Head-to-head comparison focusing on developer tooling, context window, and free tier access
  <sub>website</sub>
  <sub>`https://uibakery.io/blog/codex-vs-gemini-cli`</sub>

## Tutorials &amp; Articles

- **[Codex Windows Permissions Guide](https://tgwise.com/guides/codex-windows-permissions/)** — Community guide to approval prompts, sandbox modes, and checking effective Windows permissions
  <sub>website</sub>
  <sub>`https://tgwise.com/guides/codex-windows-permissions/`</sub>
- **[How Codex is Built (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/how-codex-is-built)** — Deep technical dive into Codex's architecture. Rust, sandboxing, the TUI. Essential reading
  <sub>website</sub>
  <sub>`https://newsletter.pragmaticengineer.com/p/how-codex-is-built`</sub>
- **[Dogfood: Codex Builds Codex (Stack Overflow)](https://stackoverflow.blog/2026/02/24/dogfood-so-nutritious-it-s-building-the-future-of-sdlcs/)** — How the Codex team uses their own tool. Real-world workflow patterns
  <sub>website</sub>
  <sub>`https://stackoverflow.blog/2026/02/24/dogfood-so-nutritious-it-s-building-the-future-of-sdlcs/`</sub>
- **[How Codex Team Uses Their Agent (Every)](https://every.to/podcast/transcript-how-openai-s-codex-team-uses-their-coding-agent)** — Transcript of the team discussing daily usage, tips, and antipatterns
  <sub>website</sub>
  <sub>`https://every.to/podcast/transcript-how-openai-s-codex-team-uses-their-coding-agent`</sub>
- **[Why Humans are AI's Biggest Bottleneck (Lenny's Newsletter)](https://www.lennysnewsletter.com/p/why-humans-are-ais-biggest-bottleneck)** — Broader perspective on AI coding agents, with Codex as a case study
  <sub>website</sub>
  <sub>`https://www.lennysnewsletter.com/p/why-humans-are-ais-biggest-bottleneck`</sub>
- **[Apidog: OpenAI Codex CLI](https://apidog.com/blog/openai-codex-cli/)** — API-focused guide. Good for integrating Codex into existing toolchains
  <sub>website</sub>
  <sub>`https://apidog.com/blog/openai-codex-cli/`</sub>
- **[First Few Days with Codex CLI (Aman Mittal)](https://amanhimself.dev/blog/first-few-days-with-codex-cli/)** — Developer diary covering setup friction, AGENTS.md discovery, and honest first impressions
  <sub>website</sub>
  <sub>`https://amanhimself.dev/blog/first-few-days-with-codex-cli/`</sub>
- **[Codex CLI Quick Start: AGENTS.md, Prompts, Safety (JP Caparas)](https://jpcaparas.medium.com/codex-cli-quick-start-agents-md-better-prompts-safer-runs-36d7060fcf68)** — Focused guide on writing effective AGENTS.md files, prompt structuring, and approval-mode safety settings
  <sub>website</sub>
  <sub>`https://jpcaparas.medium.com/codex-cli-quick-start-agents-md-better-prompts-safer-runs-36d7060fcf68`</sub>
- **[From Broken Install to Multi-Agent Orchestration (Reza Rezvani)](https://alirezarezvani.medium.com/openai-codex-cli-from-broken-install-to-multi-agent-orchestration-production-guide-07d8b7d513ef)** — Battle-tested production guide from common install failures to multi-agent fan-out patterns
  <sub>website</sub>
  <sub>`https://alirezarezvani.medium.com/openai-codex-cli-from-broken-install-to-multi-agent-orchestration-production-guide-07d8b7d513ef`</sub>
- **[Commands, Agents, and Advanced Workflows (Another Coding Blog)](https://www.anothercodingblog.com/p/working-with-openais-codex-cli-commands)** — Full walkthrough of commands, AGENTS.md, subagent orchestration, MCP server setup, and CI/CD integration
  <sub>website</sub>
  <sub>`https://www.anothercodingblog.com/p/working-with-openais-codex-cli-commands`</sub>
- **[Porting Skills to OpenAI Codex (fsck.com)](https://blog.fsck.com/2025/10/27/skills-for-openai-codex/)** — Deep-dive on porting Claude Code's skills system to Codex CLI with a working SKILL.md authoring walkthrough
  <sub>website</sub>
  <sub>`https://blog.fsck.com/2025/10/27/skills-for-openai-codex/`</sub>
- **[Skills in OpenAI Codex (fsck.com)](https://blog.fsck.com/2025/12/19/codex-skills/)** — Follow-up covering the official skills feature flag launch, skill discovery, and invocation syntax
  <sub>website</sub>
  <sub>`https://blog.fsck.com/2025/12/19/codex-skills/`</sub>
- **[Codex CLI Automation: 3 Workflow Patterns (SmartScope)](https://smartscope.blog/en/generative-ai/chatgpt/codex-cli-automation-workflow-patterns/)** — Production-ready automation patterns: GitHub Actions integration, cron-triggered runs, and CI pipeline embedding
  <sub>website</sub>
  <sub>`https://smartscope.blog/en/generative-ai/chatgpt/codex-cli-automation-workflow-patterns/`</sub>
- **[How to Run Codex CLI Safely in GitHub Actions (SmartScope)](https://smartscope.blog/en/generative-ai/chatgpt/codex-cli-github-actions/)** — Security-focused guide to sandboxing Codex in CI, secret management, and approval policy configuration
  <sub>website</sub>
  <sub>`https://smartscope.blog/en/generative-ai/chatgpt/codex-cli-github-actions/`</sub>
- **[Deployment Workflows with Codex CLI (DeployHQ)](https://www.deployhq.com/blog/getting-started-with-openai-codex-cli-ai-powered-code-generation-from-your-terminal)** — Deployment-focused guide with practical examples for CI/CD pipelines and code review automation
  <sub>website</sub>
  <sub>`https://www.deployhq.com/blog/getting-started-with-openai-codex-cli-ai-powered-code-generation-from-your-terminal`</sub>

## Community

- **[GitHub Discussions](https://github.com/openai/codex/discussions)** — Official discussion forum. Feature requests, bug reports, tips
  <sub>Rust · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/openai/codex.git && cd codex/discussions`</sub>
- **[Reddit r/ChatGPT](https://www.reddit.com/r/ChatGPT/)** — Active discussions about Codex CLI in the broader ChatGPT community
  <sub>website</sub>
  <sub>`https://www.reddit.com/r/ChatGPT/`</sub>
- **[OpenAI Developer Forum](https://community.openai.com/)** — Official OpenAI community with Codex-specific threads
  <sub>website</sub>
  <sub>`https://community.openai.com/`</sub>
- **[@OpenAIDevs on X](https://x.com/OpenAIDevs)** — Official announcements and tips
  <sub>website</sub>
  <sub>`https://x.com/OpenAIDevs`</sub>
- **[@thsottiaux](https://x.com/thsottiaux)** — Tibo, Codex team
  <sub>website</sub>
  <sub>`https://x.com/thsottiaux`</sub>
- **[@embirico](https://x.com/embirico)** — Embiricos, Codex team
  <sub>website</sub>
  <sub>`https://x.com/embirico`</sub>
- **[@jxnlco](https://x.com/jxnlco)** — Jason, Codex team
  <sub>website</sub>
  <sub>`https://x.com/jxnlco`</sub>
- **[@romainhuet](https://x.com/romainhuet)** — Romain Huet, OpenAI DevRel
  <sub>website</sub>
  <sub>`https://x.com/romainhuet`</sub>
- **[@dkundel](https://x.com/dkundel)** — Dominik Kundel, OpenAI DevRel
  <sub>website</sub>
  <sub>`https://x.com/dkundel`</sub>
- **[@fouadmatin](https://x.com/fouadmatin)** — Fouad Matin, Codex team
  <sub>website</sub>
  <sub>`https://x.com/fouadmatin`</sub>
- **[@bolinfest](https://x.com/bolinfest)** — Bolin Fest, Codex team
  <sub>website</sub>
  <sub>`https://x.com/bolinfest`</sub>


---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
