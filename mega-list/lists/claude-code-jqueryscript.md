# Claude Code (jqueryscript)

A curated list of awesome tools, IDE integrations, frameworks, and other resources for developers working with Anthropic's Claude Code.

Curated by **[jqueryscript/awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

683 entries · 659 distinct repos · 11 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/anthropics/skills"><img src="https://opengraph.githubassets.com/1/anthropics/skills" width="260"></a> | <a href="https://github.com/anthropics/claude-code"><img src="https://raw.githubusercontent.com/anthropics/claude-code/main/demo.gif" width="260"></a> | <a href="https://github.com/shareAI-lab/learn-claude-code"><img src="https://opengraph.githubassets.com/1/shareAI-lab/learn-claude-code" width="260"></a> |
| **[skills](https://github.com/anthropics/skills)**<br>★ 177.6k | **[claude-code](https://github.com/anthropics/claude-code)**<br>★ 147.6k | **[learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)**<br>★ 77.4k |
| <a href="https://github.com/shanraisshan/claude-code-best-practice"><img src="https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/%21/root/boris-slider.gif" width="260"></a> | <a href="https://github.com/anthropics/claude-cookbooks"><img src="https://opengraph.githubassets.com/1/anthropics/claude-cookbooks" width="260"></a> | <a href="https://github.com/luongnv89/claude-howto"><img src="https://opengraph.githubassets.com/1/luongnv89/claude-howto" width="260"></a> |
| **[claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)**<br>★ 66.2k | **[claude-cookbooks](https://github.com/anthropics/claude-cookbooks)**<br>★ 52.9k | **[claude-howto](https://github.com/luongnv89/claude-howto)**<br>★ 41.6k |

## Contents

- [Official Resources](#official-resources) (9)
- [Guides &amp; Learning](#guides--learning) (14)
- [Agents &amp; Orchestration](#agents--orchestration) (61)
- [Agent Skills](#agent-skills) (326)
- [Claude Plugins](#claude-plugins) (31)
- [IDE &amp; Editor Integrations](#ide--editor-integrations) (10)
- [Tools &amp; Utilities](#tools--utilities) (128)
- [Clients &amp; GUIs](#clients--guis) (27)
- [Infrastructure &amp; Proxies](#infrastructure--proxies) (32)
- [SDKs &amp; Development Kits](#sdks--development-kits) (7)
- [Usage &amp; Observability](#usage--observability) (38)

## Official Resources

- **[skills](https://github.com/anthropics/skills)** — (150.6k ⭐) - Public repository for Agent Skills
  <sub>★ 177.6k · Python · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/skills.git`</sub>
- **[claude-code](https://github.com/anthropics/claude-code)** — (132.3k ⭐) - Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routines
  <sub>★ 147.6k · TypeScript · winget · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`winget install Anthropic.ClaudeCode`</sub>
- **[claude-cookbooks](https://github.com/anthropics/claude-cookbooks)** — (45.4k ⭐) - A collection of notebooks/recipes showcasing some fun and effective ways of using Claude
  <sub>★ 52.9k · Jupyter Notebook · MIT · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/anthropics/claude-cookbooks.git`</sub>
- **[claude-plugins-official](https://github.com/anthropics/claude-plugins-official)** — (30.1k ⭐) - Anthropic-managed directory of high quality Claude Code Plugins
  <sub>★ 36.6k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/claude-plugins-official.git`</sub>
- **[financial-services](https://github.com/anthropics/financial-services)** — (31.1k ⭐) - Reference agents, skills, and data connectors for the financial-services workflows
  <sub>★ 36.1k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/financial-services.git`</sub>
- **[knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)** — (20.6k ⭐) - Open source repository of plugins primarily intended for knowledge workers to use in Claude Cowork &amp; Claude Code
  <sub>★ 25.4k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/knowledge-work-plugins.git`</sub>
- **[claude-code-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)** — (7.3k ⭐) - The official Python SDK for Claude Code
  <sub>★ 8.1k · Python · MIT · source · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/anthropics/claude-code-sdk-python.git`</sub>
- **[defending-code-reference-harness](https://github.com/anthropics/defending-code-reference-harness)** — (5.8k ⭐) - Skills for threat modeling, scanning, triage, patching, plus an autonomous scanning harness you can /customize
  <sub>★ 7.5k · Python · clone · pushed 2026-08-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/anthropics/defending-code-reference-harness`</sub>
- **[claude-code-security-review](https://github.com/anthropics/claude-code-security-review)** — (5.2k ⭐) - An AI-powered security review GitHub Action using Claude to analyze code changes for security vulnerabilities
  <sub>★ 6.3k · Python · MIT · gh-action · pushed 2026-02-11</sub>
  <sub>`uses: anthropics/claude-code-security-review@main # in .github/workflows/*.yml`</sub>

## Guides &amp; Learning

- **[learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)** — (76.5k ⭐) - A hands-on course for building a Claude Code-like agent harness from scratch
  <sub>★ 77.4k · Python · MIT · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @shareai-lab/kode`</sub>
- **[claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)** — (65.8k ⭐) - A practical collection of Claude Code best practices for skills, subagents, hooks, commands, and agentic workflows
  <sub>★ 66.2k · HTML · MIT · source · pushed 2026-09-22 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/shanraisshan/claude-code-best-practice.git`</sub>
- **[claude-howto](https://github.com/luongnv89/claude-howto)** — (41.4k ⭐) - Visual Claude Code guide with copy-ready templates and a learning path from basics to advanced agents
  <sub>★ 41.6k · Python · MIT · clone · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/luongnv89/claude-howto.git`</sub>
- **[claude-code-tips](https://github.com/ykdojo/claude-code-tips)** — (8.7k ⭐) - 45 tips for getting the most out of Claude Code, from basics to advanced - includes a custom status line script, cutting the system prompt in half, using Gemini CLI as Claude Code's minion, and Claude Code running itself in a container
  <sub>★ 10.1k · HTML · source · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/ykdojo/claude-code-tips.git`</sub>
- **[claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase)** — (6.0k ⭐) - Comprehensive Claude Code project configuration example with hooks, skills, agents, commands, and GitHub Actions workflows
  <sub>★ 6.1k · JavaScript · source · pushed 2026-01-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ChrisWiles/claude-code-showcase.git`</sub>
- **[agent-rules](https://github.com/steipete/agent-rules)** — (5.7k ⭐) - Rules and knowledge to work better with agents such as Claude Code or Cursor
  <sub>★ 5.7k · Shell · MIT · source · pushed 2026-05-03</sub>
  <sub>`git clone https://github.com/steipete/agent-rules.git`</sub>
- **[claude-code-guide](https://github.com/zebbern/claude-code-guide)** — (4.3k ⭐) - A full guide on Claude tips and tricks, optimizing Claude Code, and finding every command possible
  <sub>★ 4.6k · Python · MIT · source · pushed 2026-09-22 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/zebbern/claude-code-guide.git`</sub>
- **[claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)** — (3.8k ⭐) - A resource for mastering Claude Code hooks
  <sub>★ 3.9k · Python · source · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/disler/claude-code-hooks-mastery.git`</sub>
- **[Claude Code: Everything You Need to Know](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)** — (2.3k ⭐) - Practical guide to Claude Code setup, prompts, slash commands, skills, hooks, subagents, agent teams, and MCP servers
  <sub>★ 3k · Python · MIT · source · pushed 2026-07-28 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know.git`</sub>
- **[claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery)** — (535 ⭐) - Complete Claude Code guide covering CLAUDE.md, hooks, skills, MCP servers, and commands
  <sub>★ 549 · Shell · MIT · npm · pushed 2026-05-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @thedecipherist/mdd`</sub>
- **[claude-code-is-programmable](https://github.com/disler/claude-code-is-programmable)** — (307 ⭐) - Scale your compute with Claude Code as a programmable agentic coding tool
  <sub>★ 310 · Python · source · pushed 2025-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/disler/claude-code-is-programmable.git`</sub>
- **[claude-code-mcpinstall](https://github.com/undeadpickle/claude-code-mcpinstall)** — (235 ⭐) - Easy guide to installing Claude Code MCPs globally on your machine
  <sub>★ 234 · source · pushed 2025-03-19 · Win?</sub>
  <sub>`git clone https://github.com/undeadpickle/claude-code-mcpinstall.git`</sub>
- **[claude-code-system-prompt](https://github.com/matthew-lim-matthew-lim/claude-code-system-prompt)** — (154 ⭐) - Claude Code's system prompt
  <sub>★ 154 · source · pushed 2025-07-29</sub>
  <sub>`git clone https://github.com/matthew-lim-matthew-lim/claude-code-system-prompt.git`</sub>
- **[claudecode-best-practices](https://github.com/rosmur/claudecode-best-practices)** — (85 ⭐) - A collection of best practices and procedures for using Claude Code
  <sub>★ 84 · Python · source · pushed 2025-11-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rosmur/claudecode-best-practices.git`</sub>

## Agents &amp; Orchestration

- **[gstack](https://github.com/garrytan/gstack)** — (116.2k ⭐) - Garry Tan's Claude Code setup with opinionated agent roles for product, design, engineering, release, documentation, and QA work
  <sub>★ 133.9k · TypeScript · MIT · source · pushed 2026-09-21 · macOS</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git`</sub>
- **[Claude-Flow](https://github.com/ruvnet/ruflo)** — (59.4k ⭐) - An enterprise-grade AI orchestration platform that revolutionizes how developers build with AI
  <sub>★ 73.1k · TypeScript · MIT · npx · pushed 2026-09-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx claude-flow@latest federation init`</sub>
- **[herdr](https://github.com/herdrdev/herdr)** — (38.6k ⭐) - Terminal and desktop runtime for keeping coding-agent sessions running across local and remote machines
  <sub>★ 40.2k · Rust · Apache-2.0 · brew · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`brew install herdr`</sub>
- **[herdr](https://github.com/herdrdev/herdr)** — (5.7k ⭐) - Agent multiplexer that lives in your terminal
  <sub>★ 40.2k · Rust · Apache-2.0 · brew · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`brew install herdr`</sub>
- **[agents](https://github.com/wshobson/agents)** — (36.7k ⭐) - A collection of production-ready subagents for Claude Code
  <sub>★ 39.9k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx codex-marketplace add wshobson/agents # Codex`</sub>
- **[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)** — (39.1k ⭐) - Teams-first multi-agent orchestration for Claude Code
  <sub>★ 39.3k · TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/Yeachan-Heo/oh-my-claudecode.git`</sub>
- **[paseo](https://github.com/getpaseo/paseo)** — (17.4k ⭐) - Self-hosted interface for running Claude Code, Codex, Copilot, OpenCode, and Pi agents from desktop or mobile
  <sub>★ 18.1k · TypeScript · npm · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`npm install -g @getpaseo/cli`</sub>
- **[agents](https://github.com/contains-studio/agents)** — (12.4k ⭐) - A comprehensive collection of specialized AI agents designed to accelerate and enhance every aspect of rapid development
  <sub>★ 12.4k · clone · pushed 2025-07-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/contains-studio/agents.git`</sub>
- **[agent-orchestrator](https://github.com/Untrivial-ai/agent-orchestrator)** — (12.1k ⭐) - Plan, run, and supervise coding agents with separate workspaces, live Kanban tracking, pull requests, CI runs, and reviews
  <sub>★ 12.3k · Go · Apache-2.0 · clone · pushed 2026-09-22 · macOS</sub>
  <sub>`git clone https://github.com/Untrivial-ai/agent-orchestrator.git`</sub>
- **[omnigent](https://github.com/omnigent-ai/omnigent)** — (1.4k ⭐) - A meta-harness for all your AI agents
  <sub>★ 10.2k · Python · Apache-2.0 · uv · pushed 2026-09-22 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`uv tool install omnigent # or: pip install "omnigent"`</sub>
- **[claude-squad](https://github.com/smtg-ai/claude-squad)** — (7.8k ⭐) - Manage multiple AI terminal agents, including Claude Code, Aider, Codex, OpenCode, and Amp
  <sub>★ 8.5k · Go · AGPL-3.0 · brew · pushed 2026-08-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install claude-squad`</sub>
- **[munder-difflin](https://github.com/chaitanyagiri/munder-difflin)** — (7.7k ⭐) - Local multi-agent harness that works with existing Claude Code and Codex subscriptions to run an office of agents
  <sub>★ 7.8k · TypeScript · MIT · clone · pushed 2026-09-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/chaitanyagiri/munder-difflin.git`</sub>
- **[seomachine](https://github.com/TheCraigHewitt/seomachine)** — (7.1k ⭐) - A specialized Claude Code workspace for creating long-form, SEO-optimized blog content for any business
  <sub>★ 7.5k · Python · MIT · clone · pushed 2026-08-05 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/TheCraigHewitt/seomachine.git`</sub>
- **[mission-control](https://github.com/builderz-labs/mission-control)** — (6.2k ⭐) - Self-hosted control plane for dispatching agent tasks, reviewing runs, tracking token use and cost, and managing agent operations
  <sub>★ 6.2k · TypeScript · MIT · docker · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 3000:3000 ghcr.io/builderz-labs/mission-control:latest`</sub>
- **[loopx](https://github.com/loopx-project/loopx)** — (5.9k ⭐) - Long-horizon agent control plane for durable, governed work across Codex, Claude Code, and other harnesses
  <sub>★ 5.9k · Python · Apache-2.0 · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/loopx-project/loopx`</sub>
- **[awesome-claude-agents](https://github.com/vijaythecoder/awesome-claude-agents)** — (4.3k ⭐) - Supercharge Claude Code with a team of specialized AI agents that work together to build complete features, debug complex issues, and handle any technology stack with expert-level knowledge
  <sub>★ 4.4k · MIT · clone · pushed 2025-10-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vijaythecoder/awesome-claude-agents.git`</sub>
- **[raptor](https://github.com/gadievron/raptor)** — (3k ⭐) - Turns Claude Code into a general-purpose AI offensive/defensive security agent
  <sub>★ 3.8k · Python · clone · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gadievron/raptor.git`</sub>
- **[claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge)** — (3.5k ⭐) - Visible multi-agent CLI workspace for mixing Codex, Claude, Gemini, Kimi, Qwen, Cursor, Copilot, Pi, OpenCode, and other AI coding agents
  <sub>★ 3.5k · Python · npm · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @seemseam/ccb@latest`</sub>
- **[claude-code-subagents-collection](https://github.com/davepoon/buildwithclaude)** — (3.1k ⭐) - A comprehensive collection of specialized AI subagents for Claude Code, designed to enhance development workflows with domain-specific expertise
  <sub>★ 3.5k · Python · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/davepoon/buildwithclaude.git`</sub>
- **[claude-subconscious](https://github.com/letta-ai/claude-subconscious)** — (2.8k ⭐) - A background agent that whispers to Claude Code. A subconcious agent that watches your sessions, reads your files, builds up memory over time, and whispers guidance back
  <sub>★ 2.9k · TypeScript · MIT · npm · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @letta-ai/letta-code`</sub>
- **[deepclaude](https://github.com/aattaran/deepclaude)** — (2.1k ⭐) - A Claude Code skill for generating UI in the Nothing design language. Monochrome, typographic, industrial
  <sub>★ 2.3k · JavaScript · MIT · source · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aattaran/deepclaude.git`</sub>
- **[claude-agents](https://github.com/iannuttall/claude-agents)** — (2.1k ⭐) - Custom subagents to use with Claude Code
  <sub>★ 2k · MIT · source · pushed 2025-07-25</sub>
  <sub>`git clone https://github.com/iannuttall/claude-agents.git`</sub>
- **[openakita](https://github.com/openakita/openakita)** — (1.8k ⭐) - Open-source AI assistant framework with skills and agent workflows
  <sub>★ 2k · Python · AGPL-3.0 · pip · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install openakita[all]`</sub>
- **[roborev](https://github.com/kenn-io/roborev)** — (1.4k ⭐) - Continuous background code review database for agents, work faster and smarter with accountability for every line of generated code
  <sub>★ 1.7k · Go · MIT · go · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install go.kenn.io/roborev/cmd/roborev@latest`</sub>
- **[claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents)** — (1.6k ⭐) - Collection of specialized AI subagents for Claude Code for personal use
  <sub>★ 1.7k · MIT · clone · pushed 2025-08-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/lst97/claude-code-sub-agents.git`</sub>
- **[agent-flow](https://github.com/patoles/agent-flow)** — (974 ⭐) - Real-time visualization of Claude Code agent orchestration — see your agents think, branch, and coordinate as they work
  <sub>★ 1.7k · TypeScript · Apache-2.0 · npx · pushed 2026-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-flow-app`</sub>
- **[LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness)** — (1.4k ⭐) - Long-running computer-use harness for Claude Code, Codex, OpenCode, and DeepSeek Harness with checkpointed state, independent audits, and recovery across desktop and CLI tasks
  <sub>★ 1.6k · Python · MIT · uv · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install lh-harness # or: pip install lh-harness`</sub>
- **[awesome-claude-code-agents](https://github.com/hesreallyhim/a-list-of-claude-code-agents)** — (1.3k ⭐) - A curated list of awesome Claude Code Sub-Agents
  <sub>★ 1.4k · source · pushed 2025-11-10</sub>
  <sub>`git clone https://github.com/hesreallyhim/awesome-claude-code-agents.git`</sub>
- **[Pika-Skills](https://github.com/Pika-Labs/Pika-Skills)** — (1.1k ⭐) - A collection of open-source skills for AI coding agents (Claude Code, OpenClaw, etc.) powered by the Pika Developer API
  <sub>★ 1.2k · Python · Apache-2.0 · source · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pika-Labs/Pika-Skills.git`</sub>
- **[claude-code-subagents](https://github.com/0xfurai/claude-code-subagents)** — (928 ⭐) - A comprehensive collection of 100+ production-ready development subagents for Claude Code
  <sub>★ 1k · MIT · clone · pushed 2025-10-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/0xfurai/claude-code-subagents.git`</sub>
- **[claude-delegator](https://github.com/jarrodwatts/claude-delegator)** — (974 ⭐) - Delegate tasks to Codex GPT 5.2 directly from within Claude Code
  <sub>★ 1k · JavaScript · MIT · clone · pushed 2026-03-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jarrodwatts/claude-delegator`</sub>
- **[agentsys](https://github.com/agent-sh/agentsys)** — (878 ⭐) - Automation toolkit with plugins, agents, skills, and slash commands for Claude Code, OpenCode, Codex, Cursor, and Kiro
  <sub>★ 987 · JavaScript · MIT · npm · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agentsys`</sub>
- **[Citadel](https://github.com/SethGammon/Citadel)** — (607 ⭐) - An agent orchestration harness for Claude Code. It coordinates multiple AI agents in parallel, persists memory across sessions, and routes your intent to the cheapest execution path automatically
  <sub>★ 923 · JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SethGammon/Citadel.git`</sub>
- **[claude_code_agent_farm](https://github.com/Dicklesworthstone/claude_code_agent_farm)** — (841 ⭐) - A powerful orchestration framework that runs multiple Claude Code (cc) sessions in parallel to systematically improve your codebase
  <sub>★ 918 · Shell · clone · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/Dicklesworthstone/claude_code_agent_farm.git`</sub>
- **[ai-maestro](https://github.com/23blocks-OS/ai-maestro)** — (717 ⭐) - Agent orchestration dashboard with memory search, code graph queries, agent-to-agent messaging, and skills support
  <sub>★ 790 · TypeScript · MIT · script · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/23blocks-OS/ai-maestro/main/scripts/remote-install.sh | sh`</sub>
- **[ClaudeCodeAgents](https://github.com/darcyegb/ClaudeCodeAgents)** — (724 ⭐) - A set of useful QA agents for Claude Code
  <sub>★ 765 · MIT · source · pushed 2026-08-14</sub>
  <sub>`git clone https://github.com/darcyegb/ClaudeCodeAgents.git`</sub>
- **[claude-code-unified-agents](https://github.com/stretchcloud/claude-code-unified-agents)** — (734 ⭐) - A comprehensive collection of specialized Claude Code sub-agents combining the best features from multiple community repositories
  <sub>★ 751 · Shell · MIT · script · pushed 2025-08-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/stretchcloud/claude-code-unified-agents/main/scripts/quick-install.sh | bash`</sub>
- **[ralph-claude-code](https://github.com/CryptoDmitry/Ghost-Agent)** — (837 ⭐) - Autonomous AI development loop for Claude Code with intelligent exit detection
  <sub>★ 747 · Shell · MIT · source · pushed 2026-08-25 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/DmitrySolana/ralph-claude-code.git`</sub>
- **[pilotfish](https://github.com/Nanako0129/pilotfish)** — (425 ⭐) - Multi-model orchestration for Claude Code: a frontier model plans, lower-cost models execute, and verification checks the result
  <sub>★ 696 · Python · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Nanako0129/pilotfish.git`</sub>
- **[infinite-agentic-loop](https://github.com/disler/infinite-agentic-loop)** — (591 ⭐) - An experimental project demonstrating Infinite Agentic Loop in a two-prompt system using Claude Code
  <sub>★ 617 · HTML · source · pushed 2026-03-09</sub>
  <sub>`git clone https://github.com/disler/infinite-agentic-loop.git`</sub>
- **[dotclaude](https://github.com/FradSer/dotclaude)** — (557 ⭐) - A comprehensive development environment with specialized AI agents for code review, security analysis, and technical leadership
  <sub>★ 594 · JavaScript · MIT · source · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FradSer/dotclaude.git`</sub>
- **[claude-sub-agent](https://github.com/zhsama/claude-sub-agent)** — (586 ⭐) - AI-driven development workflow system built on Claude Code Sub-Agents
  <sub>★ 590 · clone · pushed 2025-08-08 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/zhsama/claude-sub-agent.git`</sub>
- **[GLM-skills](https://github.com/zai-org/GLM-skills)** — (414 ⭐) - Official skills for the GLM family of models
  <sub>★ 476 · Python · Apache-2.0 · clone · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zai-org/skills.git`</sub>
- **[OpenAgents](https://github.com/OpenAgentsInc/openagents)** — (424 ⭐) - Seamlessly integrate Claude Code's AI development capabilities across desktop and mobile with real-time synchronization
  <sub>★ 449 · Rust · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenAgentsInc/openagents.git`</sub>
- **[bux](https://github.com/browser-use/bux)** — (382 ⭐) - A 24/7 Claude Code agent with Browser Harness, on any box you own
  <sub>★ 448 · Python · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browser-use/bux.git`</sub>
- **[ClaudeNightsWatch](https://github.com/aniketkarne/ClaudeNightsWatch)** — (362 ⭐) - Autonomous task execution system for Claude CLI that monitors your usage windows and executes predefined tasks automatically
  <sub>★ 371 · Shell · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-plugins install @aniketkarne/claude-nights-watch-marketplace/claude-nights-watch`</sub>
- **[Specialized AI Agents](https://github.com/Dimillian/Claude)** — (359 ⭐) - This directory contains specialized AI agent definitions used by Claude Code to handle complex, domain-specific tasks
  <sub>★ 354 · source · pushed 2025-07-27 · macOS?</sub>
  <sub>`git clone https://github.com/Dimillian/Claude.git`</sub>
- **[visual-claude](https://github.com/narnia-sh/layrr)** — (258 ⭐) - A browser coding agent interface for selecting elements and sending instructions directly to Claude Code
  <sub>★ 266 · TypeScript · MIT · npm · pushed 2026-05-10 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g layrr`</sub>
- **[claude-code-subagents](https://github.com/NicholasSpisak/claude-code-subagents)** — (204 ⭐) - A collection of specialized AI agent personas designed to work seamlessly with Claude Code's Task tool, providing expert-level assistance across the full spectrum of software development challenges
  <sub>★ 212 · source · pushed 2025-08-11</sub>
  <sub>`git clone https://github.com/NicholasSpisak/claude-code-subagents.git`</sub>
- **[seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills)** — (2.1k ⭐) - 20 SEO &amp; GEO skills for Claude Code, Cursor, Codex, and 35+ AI agents. Keyword research, content writing, technical audits, rank tracking
  <sub>★ 209 · Apache-2.0 · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add aaron-he-zhu/aaron-marketing-skills`</sub>
- **[claude-user-memory](https://github.com/VAMFI/claude-user-memory)** — (193 ⭐) - A comprehensive Claude user memory system that enables intelligent, automatic orchestration of 12 specialized AI agents for Claude Code CLI
  <sub>★ 209 · Shell · clone · pushed 2025-11-23 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/VAMFI/claude-user-memory.git`</sub>
- **[sub-agents](https://github.com/webdevtodayjason/sub-agents)** — (198 ⭐) - A simple Manager for adding Claude Code Sub Agents with hooks and custom slash commands
  <sub>★ 199 · JavaScript · MIT · clone · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/webdevtodayjason/sub-agents.git`</sub>
- **[claude-code-agents](https://github.com/vizra-ai/claude-code-agents)** — (156 ⭐) - Meet 59 specialized AI agents that supercharge your development workflow
  <sub>★ 159 · MIT · clone · pushed 2025-08-29</sub>
  <sub>`git clone https://github.com/vizra-ai/claude-code-agents.git`</sub>
- **[sub-agents.directory](https://github.com/ayush-that/sub-agents.directory)** — (127 ⭐) - A curated collection of 100+ sub-agent prompts and MCP servers for Claude Code
  <sub>★ 144 · TypeScript · MIT · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ayush-that/sub-agents.directory.git`</sub>
- **[claude-code-merge-queue](https://github.com/funador/claude-code-merge-queue)** — (295 ⭐) - Local merge queue for coordinating parallel Claude Code agents and landing their work in a controlled order
  <sub>★ 125 · TypeScript · MIT · npx · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-code-merge-queue init`</sub>
- **[multi-agent-squad](https://github.com/bijutharakan/multi-agent-squad)** — (84 ⭐) - Production-ready multi-agent orchestration framework for Claude Code
  <sub>★ 86 · Python · MIT · clone · pushed 2025-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bijutharakan/multi-agent-squad.git`</sub>
- **[claude-code-heavy](https://github.com/gtrusler/claude-code-heavy)** — (77 ⭐) - Multi-agent research orchestration using Claude Code
  <sub>★ 77 · Shell · clone · pushed 2025-07-18 · WSL2 · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/claude-code-heavy`</sub>
- **[Agent-Fusion](https://github.com/krokozyab/Agent-Fusion)** — (67 ⭐) - A multi-agent orchestration system that enables Claude Code, Codex CLI, Amazon Q Developer, and Gemini Code Assist to collaborate bidirectionally through intelligent task routing and consensus-based decision making
  <sub>★ 73 · Kotlin · MIT · source · pushed 2026-06-20</sub>
  <sub>`git clone https://github.com/krokozyab/Agent-Fusion.git`</sub>
- **[Severance](https://github.com/blas0/UnseveredMemory)** — (47 ⭐) - A semantic memory system designed for Claude Code
  <sub>★ 49 · Shell · MIT · clone · pushed 2026-01-03</sub>
  <sub>`git clone https://github.com/blas0/UnseveredMemory.git`</sub>
- **[AgentCheck](https://github.com/devlyai/AgentCheck)** — (44 ⭐) - Local AI-powered code review agents for Claude Code
  <sub>★ 47 · MIT · clone · pushed 2025-08-28</sub>
  <sub>`git clone https://github.com/devlyai/AgentCheck.git`</sub>
- **[claude-agents](https://github.com/tddworks/claude-agents)** — (18 ⭐) - A collection of specialized AI agents for Claude Code that enhance software development workflows with focused expertise in specific domains
  <sub>★ 20 · Apache-2.0 · clone · pushed 2025-08-25</sub>
  <sub>`git clone https://github.com/tddworks/claude-agents.git`</sub>

## Agent Skills

- **[Superpowers](https://github.com/obra/superpowers)** — (227.6k ⭐) - Give Claude Code superpowers with a comprehensive skills library of proven techniques, patterns, and tools
  <sub>★ 290k · Shell · MIT · clone · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/obra/superpowers.git`</sub>
- **[mattpocock skills](https://github.com/mattpocock/skills)** — (128.5k ⭐) - Skills for Real Engineers
  <sub>★ 267.5k · Shell · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add mattpocock/skills`</sub>
- **[ECC](https://github.com/affaan-m/ECC)** — (222.0k ⭐) - Agent harness optimization system with skills, memory, security practices, and research-first workflows for Claude Code, Codex, OpenCode, Cursor, and related tools
  <sub>★ 265.1k · JavaScript · MIT · npm · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g ecc-universal@2.2.2`</sub>
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** — (175.2k ⭐) - A single CLAUDE.md file to improve Claude Code behavior, derived from Andrej Karpathy's observations on LLM coding pitfalls
  <sub>★ 214.6k · source · pushed 2026-04-20</sub>
  <sub>`git clone https://github.com/forrestchang/andrej-karpathy-skills.git`</sub>
- **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** — (91.5k ⭐) - An AI SKILL that provide design intelligence for building professional UI/UX multiple platforms
  <sub>★ 129.8k · Python · MIT · clone · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git`</sub>
- **[graphify](https://github.com/Graphify-Labs/graphify)** — (67.0k ⭐) - AI coding assistant skill (Claude Code, Codex, OpenCode, OpenClaw, Factory Droid, Trae)
  <sub>★ 120.4k · Python · Apache-2.0 · uv · pushed 2026-09-20 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`uv tool install graphifyy # install the CLI (or: pipx install graphifyy)`</sub>
- **[caveman](https://github.com/JuliusBrussee/caveman)** — (72.4k ⭐) - A Claude Code skill/plugin and Codex plugin that makes agent talk like caveman — cutting ~75% of output tokens while keeping full technical accuracy
  <sub>★ 107.3k · Go · psh · pushed 2026-09-22 · Win</sub>
  <sub>`irm https://raw.githubusercontent.com/JuliusBrussee/caveman/v2.7.0/install.ps1 | iex`</sub>
- **[agent-skills](https://github.com/addyosmani/agent-skills)** — (59.3k ⭐) - Production-grade engineering skills for AI coding agents
  <sub>★ 98.3k · JavaScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add addyosmani/agent-skills # install all 25 skills`</sub>
- **[taste-skill](https://github.com/Leonxlnx/taste-skill)** — (43.5k ⭐) - A collection of skills that improve how AI tools write frontend code
  <sub>★ 89.2k · JavaScript · MIT · npx · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add https://github.com/Leonxlnx/taste-skill`</sub>
- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)** — (59.1k ⭐) - Claude Code skills that turn any codebase into an interactive knowledge graph you can explore, search, and ask questions about (Multi-platform e.g., Codex are supported)
  <sub>★ 83.7k · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz /path/to/analyzed/project`</sub>
- **[archify](https://github.com/tt-a1i/archify)** — (1.2k ⭐) - Agent skill for generating architecture diagrams with dark and light themes plus PNG, JPEG, WebP, and SVG export
  <sub>★ 69.6k · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add tt-a1i/archify -g`</sub>
- **[last30days-skill](https://github.com/mvanhorn/last30days-skill)** — (41.8k ⭐) - Claude Code skill that researches any topic across Reddit + X from the last 30 days, then writes copy-paste-ready prompts
  <sub>★ 62.6k · Python · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add mvanhorn/last30days-skill -g`</sub>
- **[hyperframes](https://github.com/heygen-com/hyperframes)** — (27.6k ⭐) - Write HTML. Render video. Built for agents
  <sub>★ 52.3k · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add heygen-com/hyperframes`</sub>
- **[humanizer](https://github.com/blader/humanizer)** — (24.1k ⭐) - A Claude Code skill that removes signs of AI-generated writing from text, making it sound more natural and human
  <sub>★ 51.3k · Python · MIT · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add blader/humanizer --global`</sub>
- **[marketingskills](https://github.com/coreyhaines31/marketingskills)** — (33.3k ⭐) - Marketing skills for Claude Code and AI agents. CRO, copywriting, SEO, analytics, and growth engineering
  <sub>★ 51.2k · JavaScript · MIT · npx · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add coreyhaines31/marketingskills`</sub>
- **[i-have-adhd](https://github.com/ayghri/i-have-adhd)** — (6.2k ⭐) - A skill that keeps coding-agent answers direct, concise, and easy to scan
  <sub>★ 50.1k · Python · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ayghri/i-have-adhd.git`</sub>
- **[academic-research-skills](https://github.com/Imbad0202/academic-research-skills)** — (31.3k ⭐) - Academic Research Skills for Claude Code: research → write → review → revise → finalize
  <sub>★ 49.1k · Python · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Imbad0202/academic-research-skills.git`</sub>
- **[obsidian-skills](https://github.com/kepano/obsidian-skills)** — (35.6k ⭐) - Claude Skills for use with Obsidian
  <sub>★ 48.7k · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add git@github.com:kepano/obsidian-skills.git`</sub>
- **[agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)** — (43.7k ⭐) - A catalog of 1,900+ agentic skills with a CLI, local MCP server, plugins, and workbench for skill discovery and planning
  <sub>★ 46.8k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentic-awesome-skills --antigravity --skills brainstorming,systematic-debugging --dry-run`</sub>
- **[sickn33](https://github.com/sickn33/agentic-awesome-skills)** — (40.7k ⭐) - The Ultimate Collection of 130+ Agentic Skills for Claude Code/Antigravity/Cursor
  <sub>★ 46.8k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentic-awesome-skills --antigravity --skills brainstorming,systematic-debugging --dry-run`</sub>
- **[scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)** — (28.2k ⭐) - A set of ready to use Agent Skills for research, science, engineering, analysis, finance and writing
  <sub>★ 46.1k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx skills add K-Dense-AI/scientific-agent-skills`</sub>
- **[claude-scientific-skills](https://github.com/K-Dense-AI/scientific-agent-skills)** — (28.2k ⭐) - A set of ready to use scientific skills for Claude
  <sub>★ 46.1k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx skills add K-Dense-AI/scientific-agent-skills`</sub>
- **[emilkowalski/skills](https://github.com/emilkowalski/skills)** — (2.6k ⭐) - Design engineering skills for AI coding agents
  <sub>★ 40.1k · Markdown · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add emilkowalski/skills`</sub>
- **[reverse-skill](https://github.com/zhaoxuya520/reverse-skill)** — (2.1k ⭐) - Reverse engineering and authorized penetration testing skill for AI coding agents
  <sub>★ 36.9k · PowerShell · MIT · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/zhaoxuya520/reverse-skill.git`</sub>
- **[Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)** — (15.7k ⭐) - 753+ structured cybersecurity skills for AI agents
  <sub>★ 33.2k · Python · Apache-2.0 · npx · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add mukul975/Anthropic-Cybersecurity-Skills`</sub>
- **[add-skill](https://github.com/vercel-labs/skills)** — (22.3k ⭐) - Install agent skills onto your coding agents from any git repository
  <sub>★ 32.2k · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vercel-labs/agent-skills`</sub>
- **[book-to-skill](https://github.com/virgiliojr94/book-to-skill)** — (5.9k ⭐) - Turn any technical book PDF into a Claude Code skill — ready to study, reference, and use while you work
  <sub>★ 31.9k · Python · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add virgiliojr94/book-to-skill`</sub>
- **[agent-skills](https://github.com/vercel-labs/agent-skills)** — (27.9k ⭐) - A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities
  <sub>★ 31.5k · JavaScript · npx · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vercel-labs/agent-skills`</sub>
- **[frontend-slides](https://github.com/zarazhangrui/frontend-slides)** — (21.6k ⭐) - A Claude Code skill for creating stunning, animation-rich HTML presentations
  <sub>★ 29.7k · JavaScript · MIT · clone · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zarazhangrui/frontend-slides.git`</sub>
- **[hallmark](https://github.com/Nutlope/hallmark)** — (3.1k ⭐) - Anti-AI-slop design skill for Claude Code, Cursor, and Codex
  <sub>★ 29k · CSS · MIT · npx · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add nutlope/hallmark`</sub>
- **[planning-with-files](https://github.com/OthmanAdi/planning-with-files)** — (23.3k ⭐) - Claude Code skill implementing Manus-style persistent markdown planning — the workflow pattern behind the $2B acquisition
  <sub>★ 27.1k · Shell · MIT · npx · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g`</sub>
- **[guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)** — (17.2k ⭐) - A Claude Code Skill that turns prompts into horizontal-swipe magazine-style HTML decks
  <sub>★ 26.8k · HTML · AGPL-3.0 · npx · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill`</sub>
- **[claude-skills](https://github.com/alirezarezvani/claude-skills)** — (18.0k ⭐) - A Collection of Skills for Claude Code and Claude AI for real-world Usage
  <sub>★ 26.2k · Python · MIT · npx · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-skills-cli add alirezarezvani/claude-skills --agent codex`</sub>
- **[baoyu-skills](https://github.com/JimLiu/baoyu-skills)** — (24.7k ⭐) - A collection of 20+ skills for writing, image generation, presentations, social publishing, and other daily work with Claude Code, Codex, and compatible agents
  <sub>★ 26.1k · TypeScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add jimliu/baoyu-skills`</sub>
- **[Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)** — (21.6k ⭐) - Turn Claude Code into a full game dev studio — 49 AI agents, 72 workflow skills, and a complete coordination system mirroring real studio hierarchy
  <sub>★ 25.4k · Shell · MIT · clone · pushed 2026-05-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Donchitos/Claude-Code-Game-Studios.git`</sub>
- **[watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover)** — (15.8k ⭐) - Agent skill and Python service for removing AI provenance marks from text and file metadata, including C2PA, EXIF, and XMP
  <sub>★ 22.6k · Python · MIT · docker · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run --rm -p 127.0.0.1:8765:8765 --read-only --tmpfs /tmp watermarks-remover`</sub>
- **[Google Agent Skills](https://github.com/google/skills)** — (13.7k ⭐) - Agent Skills for Google products and technologies
  <sub>★ 20.3k · Python · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add google/skills`</sub>
- **[security-audit-skill](https://github.com/cloudflare/security-audit-skill)** — (943 ⭐) - Cloudflare coding-agent skill for multi-phase security audits with independently verified, machine-readable findings
  <sub>★ 19.7k · JavaScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/cloudflare/security-audit-skill \`</sub>
- **[notebooklm-py](https://github.com/teng-lin/notebooklm-py)** — (18.8k ⭐) - Unofficial Python API and agentic skill for Google NotebookLM, with programmatic access through Python, a CLI, and AI agents such as Claude Code, Codex, and OpenClaw
  <sub>★ 19.4k · Python · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add teng-lin/notebooklm-py`</sub>
- **[SkillSpector](https://github.com/NVIDIA/SkillSpector)** — (8.4k ⭐) - Security scanner for AI agent skills that detects vulnerabilities and risky instructions
  <sub>★ 18.1k · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install git+https://github.com/NVIDIA/skillspector.git`</sub>
- **[Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** — (16.5k ⭐) - A comprehensive collection of Agent Skills for context engineering, multi-agent architectures, and production agent systems
  <sub>★ 18k · Python · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering.git`</sub>
- **[claude-video](https://github.com/bradautomates/claude-video)** — (14.5k ⭐) - An Agent Skill and Claude Code plugin that downloads video, extracts frames and captions or transcripts, and answers questions about the on-screen and audio content
  <sub>★ 17.5k · Python · MIT · npx · pushed 2026-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add bradautomates/claude-video -g`</sub>
- **[stop-slop](https://github.com/hardikpandya/stop-slop)** — (10.4k ⭐) - A skill file for removing AI tells from prose
  <sub>★ 17.5k · MIT · source · pushed 2026-03-17</sub>
  <sub>`git clone https://github.com/hardikpandya/stop-slop.git`</sub>
- **[claude-seo](https://github.com/AgriciDaniel/claude-seo)** — (8.9k ⭐) - Universal SEO skill for Claude Code. Comprehensive SEO analysis for any website or business type
  <sub>★ 17.4k · Python · MIT · script · pushed 2026-09-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/uninstall.sh | bash`</sub>
- **[Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** — (12.1k ⭐) - Lightweight Markdown-only skills for autonomous ML research
  <sub>★ 16.5k · Python · MIT · clone · pushed 2026-09-18 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git`</sub>
- **[text-to-cad](https://github.com/earthtojake/text-to-cad)** — (6.3k ⭐) - An open source harness for generating CAD models
  <sub>★ 16.3k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx skills add earthtojake/text-to-cad`</sub>
- **[gsap-skills](https://github.com/greensock/gsap-skills)** — (9.2k ⭐) - Official AI skills for GSAP. These skills teach AI coding agents how to correctly use GSAP (GreenSock Animation Platform), including best practices, common animation patterns, and plugin usage
  <sub>★ 15.6k · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/greensock/gsap-skills`</sub>
- **[memU](https://github.com/NevaMind-AI/memU)** — (13.9k ⭐) - Personal memory for agents with fast retrieval, self-evolving skills, and lower context cost
  <sub>★ 14.4k · Python · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx memu-cli --help # CLI via npm launcher (engine: PyPI package memu-cli)`</sub>
- **[MiniMax-AI/skills](https://github.com/MiniMax-AI/skills)** — (12.6k ⭐) - Development skills for AI coding agents
  <sub>★ 13.6k · C# · MIT · clone · pushed 2026-04-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/MiniMax-AI/skills.git`</sub>
- **[prompt-master](https://github.com/nidhinjs/prompt-master)** — (9.2k ⭐) - A Claude skill that writes the accurate prompts for any AI tool
  <sub>★ 13.5k · MIT · clone · pushed 2026-08-24</sub>
  <sub>`git clone https://github.com/nidhinjs/prompt-master.git`</sub>
- **[AI-research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)** — (9.7k ⭐) - Visual Skills Pack for Obsidian: generate Canvas, Excalidraw, and Mermaid diagrams from text with Claude Code
  <sub>★ 12.9k · TeX · MIT · npx · pushed 2026-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @orchestra-research/ai-research-skills`</sub>
- **[garden-skills](https://github.com/ConardLi/garden-skills)** — (8.0k ⭐) - ConardLi's open-source Skills collection, featuring web design, knowledge retrieval, image generation, and more
  <sub>★ 12.6k · CSS · MIT · npx · pushed 2026-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ConardLi/garden-skills`</sub>
- **[fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)** — (7.7k ⭐) - Claude Code skill for generating production-quality SVG+PNG technical diagrams
  <sub>★ 11.5k · Python · MIT · clone · pushed 2026-09-05 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yizhiyanhua-ai/fireworks-tech-graph.git`</sub>
- **[huggingface skills](https://github.com/huggingface/skills)** — (10.7k ⭐) - Give your agents the power of the Hugging Face ecosystem
  <sub>★ 11.1k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/huggingface/skills.git`</sub>
- **[no-ai-slop](https://github.com/petergyang/no-ai-slop)** — (7.8k ⭐) - Editing skill that removes 20+ AI-writing patterns while preserving the writer's voice
  <sub>★ 11k · Python · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add petergyang/no-ai-slop --skill no-ai-slop --global --yes`</sub>
- **[geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude)** — (8.1k ⭐) - GEO-first SEO skill for Claude Code. Comprehensive AI search optimization for any website — citability scoring, AI crawler analysis, brand authority, schema markup, platform-specific optimization, and PDF reports
  <sub>★ 10.8k · Python · MIT · script · pushed 2026-09-22 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install.sh | bash`</sub>
- **[huggingface skills](https://github.com/numman-ali/openskills)** — (10.4k ⭐) - Universal skills loader for AI coding agents
  <sub>★ 10.8k · TypeScript · npx · pushed 2026-01-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx openskills install anthropics/skills`</sub>
- **[slavingia/skills](https://github.com/slavingia/skills)** — (9.1k ⭐) - Claude Code skills based on The Minimalist Entrepreneur by Sahil Lavingia
  <sub>★ 10.5k · clone · pushed 2026-04-14</sub>
  <sub>`git clone https://github.com/slavingia/skills.git`</sub>
- **[visual-explainer](https://github.com/nicobailon/visual-explainer)** — (8.8k ⭐) - Agent skill + prompt templates that generate rich HTML pages for visual diff reviews, architecture overviews, plan audits, data tables, and project recaps
  <sub>★ 9.9k · HTML · MIT · script · pushed 2026-08-28 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/nicobailon/visual-explainer/main/install-pi.sh | bash`</sub>
- **[drawio-skill](https://github.com/Agents365-ai/drawio-skill)** — (3.3k ⭐) - Generate draw.io diagrams from natural language — 6 presets, vision self-check + up to 5-round refinement, codebase-to-diagram, 10,000+ official shapes &amp; 321 AI/LLM brand logos
  <sub>★ 9.6k · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add Agents365-ai/drawio-skill -g`</sub>
- **[claude-ads](https://github.com/AgriciDaniel/claude-ads)** — (6.0k ⭐) - Comprehensive paid advertising audit &amp; optimization skill for Claude Code
  <sub>★ 9.5k · Python · MIT · clone · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/AgriciDaniel/claude-ads.git`</sub>
- **[scroll-world](https://github.com/oso95/scroll-world)** — (4.6k ⭐) - A skill for turning a brand into a scrollable 3D world
  <sub>★ 9.4k · JavaScript · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add oso95/scroll-world # pick your agent(s) when prompted`</sub>
- **[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)** — (2.2k ⭐) - Claude Code and Codex skill for creating cinematic product videos with Remotion shot recipes and templates
  <sub>★ 9.2k · TypeScript · Apache-2.0 · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Vincentwei1021/video-shotcraft`</sub>
- **[improve](https://github.com/shadcn/improve)** — (4.6k ⭐) - Use your most capable model to audit your codebase and write plans for cheaper models to execute
  <sub>★ 9.2k · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add shadcn/improve`</sub>
- **[ui-skills](https://github.com/ibelick/ui-skills)** — (2.8k ⭐) - A growing set of skills to polish interfaces built by agents
  <sub>★ 8.9k · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ui-skills start`</sub>
- **[html-ppt-skill](https://github.com/lewislulu/html-ppt-skill)** — (6.0k ⭐) - HTML PPT Studio — AgentSkill with 24 themes, 31 layouts, 20+ animations for building professional HTML presentations
  <sub>★ 8.5k · HTML · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g skills`</sub>
- **[stitch-skills](https://github.com/google-labs-code/stitch-skills)** — (6.0k ⭐) - A library of Agent Skills designed to work with the Stitch MCP server
  <sub>★ 8.3k · TypeScript · Apache-2.0 · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx plugins add google-labs-code/stitch-skills --scope project --target claude-code`</sub>
- **[android-reverse-engineering-skill](https://github.com/SimoneAvogadro/android-reverse-engineering-skill)** — (6.1k ⭐) - Claude Code skill to support Android app's reverse engineering
  <sub>★ 7.9k · Shell · Apache-2.0 · clone · pushed 2026-09-08 · Win?</sub>
  <sub>`git clone https://github.com/SimoneAvogadro/android-reverse-engineering-skill.git`</sub>
- **[notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill)** — (7.0k ⭐) - Use this skill to enable Claude Code to communicate directly with your Google NotebookLM notebooks
  <sub>★ 7.8k · Python · MIT · clone · pushed 2026-09-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/PleasePrompto/notebooklm-skill`</sub>
- **[architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)** — (5.9k ⭐) - Generate beautiful dark-themed system architecture diagrams as standalone HTML/SVG files
  <sub>★ 7.3k · HTML · MIT · source · pushed 2026-05-13</sub>
  <sub>`git clone https://github.com/Cocoon-AI/architecture-diagram-generator.git`</sub>
- **[skills](https://github.com/trailofbits/skills)** — (5.7k ⭐) - Trail of Bits Claude Code skills for security research, vulnerability detection, and audit workflows
  <sub>★ 7.2k · Python · CC-BY-SA-4.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trailofbits/skills.git`</sub>
- **[guizang-social-card-skill](https://github.com/op7418/guizang-social-card-skill)** — (3.5k ⭐) - Claude Code / Codex skill — generate Xiaohongshu carousels &amp; WeChat 21:9+1:1 cover pairs
  <sub>★ 7.2k · HTML · AGPL-3.0 · npx · pushed 2026-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/op7418/guizang-social-card-skill --skill guizang-social-card-skill`</sub>
- **[gc-minimal-zine-poster](https://github.com/LiamGvchi/gc-minimal-zine-poster)** — (1.0k ⭐) - Codex skill for generating quiet, minimal zine-style editorial poster prompts and images
  <sub>★ 7.2k · MIT · clone · pushed 2026-08-13</sub>
  <sub>`git clone https://github.com/LiamGvchi/gc-minimal-zine-poster.git`</sub>
- **[cheat-on-content](https://github.com/XBuilderLAB/cheat-on-content)** — (4.2k ⭐) - A skill that turns every post into a calibrated experiment
  <sub>★ 7.1k · Python · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/XBuilderLAB/cheat-on-content.git`</sub>
- **[Waza](https://github.com/tw93/Waza)** — (5.7k ⭐) - Engineering habits you already know, turned into skills Claude can run
  <sub>★ 7.1k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add tw93/Waza -a claude-code codex cursor -g -y`</sub>
- **[Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)** — (5.1k ⭐) - Product Management skills framework built on battle-tested methods for Claude Code, Cowork, Codex, and AI agents
  <sub>★ 7k · Shell · source · pushed 2026-09-01</sub>
  <sub>`git clone https://github.com/deanpeters/Product-Manager-Skills.git`</sub>
- **[Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills)** — (3.8k ⭐) - Skill package for ML/CV/NLP paper writing, curated and adapted from Prof. Peng Sida's open notes for Codex, Claude Code, and Gemini
  <sub>★ 7k · MIT · source · pushed 2026-06-23</sub>
  <sub>`git clone https://github.com/Master-cai/Research-Paper-Writing-Skills.git`</sub>
- **[jakubkrehel/skills](https://github.com/jakubkrehel/skills)** — (942 ⭐) - Agent skills for interface animation, UI polish, accessibility, and product writing
  <sub>★ 7k · Markdown · MIT · npx · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add jakubkrehel/skills`</sub>
- **[godogen](https://github.com/htdt/godogen)** — (3.4k ⭐) - Claude Code skills that build complete Godot 4 projects from a game description
  <sub>★ 7k · Python · MIT · source · pushed 2026-09-04 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/htdt/godogen.git`</sub>
- **[Claude-Red](https://github.com/SnailSploit/Claude-Red)** — (2.3k ⭐) - A curated library of offensive security skills designed for the Claude skills system
  <sub>★ 6.7k · Python · MIT · clone · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SnailSploit/claude-red`</sub>
- **[dev-browser](https://github.com/SawyerHood/dev-browser)** — (6.3k ⭐) - A Claude Skill to give your agent the ability to use a web browser
  <sub>★ 6.6k · TypeScript · MIT · npm · pushed 2026-09-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g dev-browser`</sub>
- **[BrowserSkill](https://github.com/Tencent/BrowserSkill)** — (5.9k ⭐) - CLI and browser extension that let AI agents use your logged-in browser without interrupting your work
  <sub>★ 6.5k · TypeScript · MIT · psh · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.ps1 | iex`</sub>
- **[autoresearch](https://github.com/uditgoenka/autoresearch)** — (5.0k ⭐) - Turn Claude Code into a relentless improvement engine
  <sub>★ 6.4k · Shell · MIT · npx · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add uditgoenka/autoresearch`</sub>
- **[n8n-skills](https://github.com/czlonkowski/n8n-skills)** — (5.4k ⭐) - n8n skillset for Claude Code to build flawless n8n workflows
  <sub>★ 6.3k · Shell · MIT · clone · pushed 2026-09-16 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/czlonkowski/n8n-skills.git`</sub>
- **[anysearch-skill](https://github.com/anysearch-ai/anysearch-skill)** — (3.2k ⭐) - Unified real-time search engine skill for AI agents
  <sub>★ 6.3k · Python · Apache-2.0 · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anysearch-ai/anysearch-skill.git`</sub>
- **[qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm)** — (5.5k ⭐) - Claude skill for processing WeChat articles, web pages, YouTube videos, PDFs, Markdown, and search queries into NotebookLM-ready materials
  <sub>★ 6.1k · Python · MIT · clone · pushed 2026-04-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/joeseesun/qiaomu-anything-to-notebooklm`</sub>
- **[codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill)** — (2.1k ⭐) - GPT-Image-2 PPT generator skill for creating image-based slide decks
  <sub>★ 6.1k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y skills@latest add ningzimu/codex-ppt-skill \`</sub>
- **[agents-cli](https://github.com/google/agents-cli)** — (2.9k ⭐) - The CLI and skills that turn any coding assistant into an expert at creating, evaluating, and deploying AI agents on Google Cloud
  <sub>★ 6k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add google/agents-cli`</sub>
- **[antfu's skills](https://github.com/antfu/skills)** — (5.3k ⭐) - Anthony Fu's curated collection of agent skills
  <sub>★ 5.9k · TypeScript · MIT · source · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/antfu/skills.git`</sub>
- **[internet-court-skill](https://github.com/internet-court/internet-court-skill)** — (1.4k ⭐) - Agent Skill for natural-language mandates, delegated permissions, payments, escrow, and dispute resolution
  <sub>★ 5.9k · TypeScript · npx · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add internet-court/internet-court-skill # installs the root skill`</sub>
- **[claude-design-engineer](https://github.com/Dammyjay93/interface-design)** — (5.0k ⭐) - Design engineering for Claude Code. Craft, memory, and enforcement for consistent UI
  <sub>★ 5.7k · Shell · MIT · npx · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/dammyjay93/interface-design --skill interface-design`</sub>
- **[SenseNova-Skills](https://github.com/OpenSenseNova/SenseNova-Skills)** — (4.5k ⭐) - Modular SenseNova skills for building AI-powered office assistants and productivity workflows
  <sub>★ 5.7k · JavaScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenSenseNova/SenseNova-Skills.git`</sub>
- **[codebase-to-course](https://github.com/zarazhangrui/codebase-to-course)** — (4.6k ⭐) - A Claude Code skill that turns any codebase into a beautiful, interactive single-page HTML course for non-technical vibe coders
  <sub>★ 5.6k · CSS · source · pushed 2026-03-30</sub>
  <sub>`git clone https://github.com/zarazhangrui/codebase-to-course.git`</sub>
- **[GPT-Image2-Skill](https://github.com/wuyoscar/GPT-Image2-Skill)** — (3.0k ⭐) - GPT Image 2 prompt gallery, image prompt library, agentic skill, and CLI for OpenAI image generation/editing
  <sub>★ 5.5k · Python · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes skills@latest add wuyoscar/gpt_image_2_skill \`</sub>
- **[gpt_image_2_skill](https://github.com/wuyoscar/GPT-Image2-Skill)** — (3.0k ⭐) - GPT Image 2 prompt gallery, image prompt library, agentic skill, and CLI for OpenAI image generation/editing
  <sub>★ 5.5k · Python · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes skills@latest add wuyoscar/gpt_image_2_skill \`</sub>
- **[lottie](https://github.com/diffusionstudio/lottie)** — (2.6k ⭐) - Generate production-ready Lottie animations with Claude Code or Codex
  <sub>★ 5.5k · TypeScript · MIT · npx · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add diffusionstudio/lottie`</sub>
- **[ip-as-logo-skill](https://github.com/s1dashu/ip-as-logo-skill)** — (3.9k ⭐) - Agent Skill for generating simple, rounded IP mascot logos with subtle neo-skeuomorphic styling
  <sub>★ 5.4k · MIT · npx · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add s1dashu/ip-as-logo-skill`</sub>
- **[excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill)** — (3.7k ⭐) - Skill to give Claude Code (and any coding agent) the ability to generate beautiful and practical Excalidraw diagrams
  <sub>★ 4.8k · Python · clone · pushed 2026-03-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/coleam00/excalidraw-diagram-skill.git`</sub>
- **[SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill)** — (4.1k ⭐) - SwiftUI agent skill for Claude Code, Codex, and other AI tools
  <sub>★ 4.8k · MIT · npx · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro`</sub>
- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** — (1.9k ⭐) - Skill that audits and rewrites text to remove common signs of AI-generated writing
  <sub>★ 4.7k · JavaScript · MIT · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g avoid-ai-writing-detector`</sub>
- **[Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)** — (2.5k ⭐) - A Claude Code skill bundle for bug hunting and external red-team work — 71 skills, 15 slash commands, 681 disclosed-report patterns curated across 24 core vulnerability classes, plus enterprise identity + infrastructure attack matrices
  <sub>★ 4.6k · Python · MIT · pipx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/elementalsouls/Claude-BugHunter`</sub>
- **[autoharness](https://github.com/tigerless-labs/autoharness)** — (1.2k ⭐) - A self-learning skill layer for Claude Code that distills reusable skills from sessions, updates them over time, and prunes unused ones
  <sub>★ 4.4k · Python · MIT · source · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tigerless-labs/autoharness.git`</sub>
- **[Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills)** — (3.5k ⭐) - Multi-modal Generative Media Skills for AI Agents (Claude Code, Cursor, Gemini CLI)
  <sub>★ 4.3k · Shell · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add SamurAIGPT/Generative-Media-Skills --all`</sub>
- **[adhd](https://github.com/UditAkhourii/adhd)** — (814 ⭐) - A skill for coding agents. Tree-of-thought with pruning, built on the Claude &amp; Codex Agent SDK
  <sub>★ 4.3k · TypeScript · MIT · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g adhd-agent # CLI`</sub>
- **[gemini-skills](https://github.com/google-gemini/gemini-skills)** — (3.6k ⭐) - Skills for the Gemini API, SDK and model/agent interactions
  <sub>★ 4.2k · Python · Apache-2.0 · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add google-gemini/gemini-skills --list`</sub>
- **[agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge)** — (2.7k ⭐) - Agent Skill for generating 2D sprite sheets and map, transparent PNG frames, and animated GIFs from prompts
  <sub>★ 4.2k · Python · MIT · clone · pushed 2026-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0x0funky/agent-sprite-forge.git`</sub>
- **[baoyu-design](https://github.com/JimLiu/baoyu-design)** — (1.0k ⭐) - Run Claude Design locally as an Agent Skill
  <sub>★ 4.1k · JavaScript · MIT · npx · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add JimLiu/baoyu-design`</sub>
- **[design-extract](https://github.com/Manavarya09/design-extract)** — (4.0k ⭐) - Extract a website's complete design system into design tokens, UI themes, component anatomy, and platform-specific code
  <sub>★ 4.1k · HTML · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g designlang # global`</sub>
- **[davidondrej/skills](https://github.com/davidondrej/skills)** — (2.5k ⭐) - Reusable Agent Skills for coding, research, workflow orchestration, documentation, operations, and skill authoring
  <sub>★ 4.1k · Shell · MIT · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/davidondrej/skills.git`</sub>
- **[Dimillian Skills](https://github.com/Dimillian/Skills)** — (3.7k ⭐) - A collection of reusable development skills for Apple platforms, GitHub workflows, refactoring, diff review swarms, bug investigation swarms, code review, React performance work, and skill curation
  <sub>★ 4k · Shell · MIT · source · pushed 2026-03-29 · macOS?</sub>
  <sub>`git clone https://github.com/Dimillian/Skills.git`</sub>
- **[sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills)** — (3.6k ⭐) - Expert code review skill: SOLID, security, performance, error handling, boundary conditions
  <sub>★ 3.9k · Python · MIT · npx · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sanyuan0704/sanyuan-skills --path skills/<skill-name>`</sub>
- **[AI-research-SKILLs](https://github.com/sanyuan0704/sanyuan-skills)** — (3.6k ⭐) - A comprehensive code review skill for AI agents
  <sub>★ 3.9k · Python · MIT · npx · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sanyuan0704/sanyuan-skills --path skills/<skill-name>`</sub>
- **[seedance2-skill](https://github.com/dexhunter/seedance2-skill)** — (2.1k ⭐) - Skill to create best prompts for generating videos with seedance2.0
  <sub>★ 3.9k · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add dexhunter/seedance2-skill`</sub>
- **[NotFair](https://github.com/nowork-studio/notfair-plugin)** — (2.8k ⭐) - Open-source Claude Code skills for SEO, GEO, Google Ads, Meta Ads
  <sub>★ 3.8k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[Swift-Agent-Skills](https://github.com/nowork-studio/notfair-plugin)** — (2.8k ⭐) - A curated directory of open-source AI agent skills for Swift and Apple platform development
  <sub>★ 3.8k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[Browserbase Skills](https://github.com/browserbase/skills)** — (3.6k ⭐) - Browserbase's official collection of agent skills to access the web
  <sub>★ 3.7k · JavaScript · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browserbase/skills.git`</sub>
- **[Acontext](https://github.com/memodb-io/Acontext)** — (3.6k ⭐) - Agent Skills used as a memory layer for context engineering and self-learning agent workflows
  <sub>★ 3.7k · JavaScript · Apache-2.0 · pip · pushed 2026-07-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install acontext`</sub>
- **[social-media-skills](https://github.com/charlie947/social-media-skills)** — (1.5k ⭐) - Agent skills for planning, writing, and managing social media content
  <sub>★ 3.6k · Python · MIT · clone · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/charlie947/social-media-skills.git`</sub>
- **[SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill)** — (3.3k ⭐) - Agent Skill guidance for building SwiftUI apps with current best practices
  <sub>★ 3.6k · Python · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add https://github.com/avdlee/swiftui-agent-skill --skill swiftui-expert-skill`</sub>
- **[Kami](https://github.com/ericosiu/ai-marketing-skills)** — (2.6k ⭐) - Good content deserves good paper
  <sub>★ 3.6k · Python · MIT · clone · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ericosiu/ai-marketing-skills.git`</sub>
- **[unlazy](https://github.com/Leonxlnx/unlazy)** — (1.3k ⭐) - Agent skill that uses a depth-tree method to break tasks into deeper work units and counter premature completion
  <sub>★ 3.5k · JavaScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Leonxlnx/unlazy`</sub>
- **[make-interfaces-feel-better](https://github.com/jakubkrehel/make-interfaces-feel-better)** — (2.0k ⭐) - Interface design skill based on the "Details that make interfaces feel better" article
  <sub>★ 3.5k · Markdown · MIT · npx · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add jakubkrehel/make-interfaces-feel-better`</sub>
- **[SimpleEnglish](https://github.com/AminBlg/SimpleEnglish)** — (2.0k ⭐) - An Agent Skill that applies ASD-STE100 Simplified Technical English rules to documentation produced by Claude Code, Codex, and other compatible agents
  <sub>★ 3.5k · Python · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add AminBlg/SimpleEnglish`</sub>
- **[everything-claude-code](https://github.com/WorldFlowAI/everything-claude-code)** — (1.1k ⭐) - A Claude Code toolkit with agents, skills, hooks, commands, rules, and MCP configurations for day-to-day development
  <sub>★ 3.5k · JavaScript · clone · pushed 2026-01-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/affaan-m/everything-claude-code.git`</sub>
- **[AlphaGBM/skills](https://github.com/AlphaGBM/skills)** — (1.0k ⭐) - Real-data options intelligence skills for AI agents, with Claude Code and Cursor support
  <sub>★ 3.4k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add AlphaGBM/skills --skill alphagbm-research-reader`</sub>
- **[Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills)** — (2.3k ⭐) - An all-in-one AI skills package
  <sub>★ 3.4k · Python · Apache-2.0 · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/foryourhealth111-pixel/Vibe-Skills.git`</sub>
- **[NVIDIA skills](https://github.com/NVIDIA/skills)** — (2.1k ⭐) - AI agent skills published by NVIDIA
  <sub>★ 3.4k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add nvidia/skills`</sub>
- **[threejs-skills](https://github.com/CloudAI-X/threejs-skills)** — (2.4k ⭐) - A curated collection of Three.js skill files that provide Claude Code with foundational knowledge for creating 3D elements and interactive experiences
  <sub>★ 3.4k · clone · pushed 2026-07-09</sub>
  <sub>`git clone https://github.com/pinkforest/threejs-playground.git`</sub>
- **[finance-skills](https://github.com/himself65/finance-skills)** — (2.8k ⭐) - A collection of skills for AI financial analysis and trading
  <sub>★ 3.3k · JavaScript · MIT · npx · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx plugins add himself65/finance-skills`</sub>
- **[markdown-viewer skills](https://github.com/markdown-viewer/skills)** — (3.0k ⭐) - Opinionated skills for AI coding agents to create stunning diagrams and visualizations directly in Markdown
  <sub>★ 3.3k · npx · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add markdown-viewer/skills`</sub>
- **[ctf-skills](https://github.com/ljagiello/ctf-skills)** — (2.4k ⭐) - Agent skills for solving CTF challenges - web exploitation, binary pwn, crypto, reverse engineering, forensics, OSINT, and more
  <sub>★ 3.3k · Python · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ljagiello/ctf-skills`</sub>
- **[cc-skills-golang](https://github.com/samber/cc-skills-golang)** — (2.2k ⭐) - A collection of Golang agentic skills that works
  <sub>★ 3.3k · Go · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/samber/cc-skills-golang --all`</sub>
- **[chrome-cdp-skill](https://github.com/pasky/chrome-cdp-skill)** — (3.1k ⭐) - Give your AI agent access to your live Chrome session — works out of the box, connects to tabs you already have open
  <sub>★ 3.3k · JavaScript · MIT · source · pushed 2026-06-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/pasky/chrome-cdp-skill.git`</sub>
- **[effective-html](https://github.com/plannotator/effective-html)** — (866 ⭐) - Agent skill for elegant and simple html plans, architecture diagrams, or whatever else you can think of
  <sub>★ 3.3k · HTML · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add plannotator/effective-html`</sub>
- **[mono-color-skill](https://github.com/yanliudesign/mono-color-skill)** — (2.1k ⭐) - One-ink editorial print image skill with warm paper, halftone photography, active negative space, and restrained typography
  <sub>★ 3.2k · Python · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yanliudesign/mono-color-skill.git`</sub>
- **[9arm-skills](https://github.com/thananon/9arm-skills)** — (2.8k ⭐) - Agent skills loaded by Claude Code
  <sub>★ 3.2k · Shell · npx · pushed 2026-06-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add thananon/9arm-skills`</sub>
- **[loopy](https://github.com/Forward-Future/loopy)** — (2.1k ⭐) - Practical AI-agent loops and an installable skill for finding, adapting, and designing repeatable agent workflows
  <sub>★ 3.1k · JavaScript · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Forward-Future/loopy \`</sub>
- **[playwright-skill](https://github.com/lackeyjb/playwright-skill)** — (2.8k ⭐) - Claude Code Skill for browser automation with Playwright. Model-invoked - Claude autonomously writes and executes custom automation for testing and validation
  <sub>★ 3.1k · JavaScript · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add lackeyjb/playwright-skill --skill playwright-skill --global --yes`</sub>
- **[science-skills](https://github.com/google-deepmind/science-skills)** — (2.0k ⭐) - Google DeepMind science skills for agentic scientific workflows
  <sub>★ 3.1k · Python · Apache-2.0 · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add google-deepmind/science-skills/`</sub>
- **[linkedin-skills](https://github.com/sergebulaev/linkedin-skills)** — (2.9k ⭐) - Claude skills for LinkedIn: write human-sounding posts, craft comments, analyze your feed, and build a publishing cadence from the terminal
  <sub>★ 3.1k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sergebulaev/linkedin-skills`</sub>
- **[comet](https://github.com/rpamis/comet)** — (1.5k ⭐) - Agent skill harness for phase-guarded automation from idea to implementation
  <sub>★ 3.1k · JavaScript · MIT · npm · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @rpamis/comet`</sub>
- **[skills](https://github.com/microsoft/skills)** — (2.6k ⭐) - Skills, MCP servers, Custom Agents, Agents.md for SDKs to ground Coding Agents
  <sub>★ 3k · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add microsoft/skills`</sub>
- **[Flutter Agent Skills](https://github.com/flutter/agent-plugins)** — (2.4k ⭐) - A collection of skills providing tailored instructions for happy path Flutter app development workflows
  <sub>★ 3k · Dart · BSD-3-Clause · source · pushed 2026-09-17 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/flutter/skills.git`</sub>
- **[awesome-design-skills](https://github.com/bergside/awesome-design-skills)** — (1.3k ⭐) - Design skill directory for agentic tools, covering DESIGN.md and SKILL.md files for Claude Design, Codex, Cursor, and related AI tools
  <sub>★ 2.9k · MIT · npx · pushed 2026-06-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx typeui.sh pull <slug>`</sub>
- **[Claude-to-IM-skill](https://github.com/op7418/Claude-to-IM-skill)** — (2.7k ⭐) - Bridge Claude Code / Codex to IM platforms — chat with AI coding agents from Telegram, Discord, or Feishu/Lark
  <sub>★ 2.9k · TypeScript · MIT · npx · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add op7418/Claude-to-IM-skill`</sub>
- **[claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)** — (2.0k ⭐) - Claude Code skills for equity investors and traders, including market research and analysis workflows
  <sub>★ 2.9k · Python · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/tradermonty/claude-trading-skills.git`</sub>
- **[vue-skills](https://github.com/vuejs-ai/skills)** — (2.6k ⭐) - Agent skills for Vue 3 development
  <sub>★ 2.9k · MIT · npx · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vuejs-ai/skills`</sub>
- **[vue-skills](https://github.com/vuejs-ai/skills)** — (2.6k ⭐) - Agent skills for Vue 3 development
  <sub>★ 2.9k · MIT · npx · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vuejs-ai/skills`</sub>
- **[agent-rules-books](https://github.com/ciembor/agent-rules-books)** — (1.9k ⭐) - AGENTS.md rules and skills for Codex, Cursor, Claude Code, Gemini CLI, and related coding agents
  <sub>★ 2.8k · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ciembor/agent-rules-books --all`</sub>
- **[seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill)** — (1.9k ⭐) - A Claude Code custom skill that turns Claude into a professional AI video prompt engineer for ByteDance's Seedance 2.0 (鍗虫ⅵ) video generation platform
  <sub>★ 2.8k · clone · pushed 2026-02-12</sub>
  <sub>`git clone https://github.com/songguoxs/seedance-prompt-skill.git`</sub>
- **[automotive-skills-suite](https://github.com/jherrodthomas/automotive-skills-suite)** — (1.6k ⭐) - Installable Claude skills for automotive engineering, diagnostics, safety, and service workflows
  <sub>★ 2.8k · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jherrodthomas/automotive-skills-suite.git`</sub>
- **[web-quality-skills](https://github.com/addyosmani/web-quality-skills)** — (2.3k ⭐) - Agent Skills for optimizing web quality based on Lighthouse and Core Web Vitals
  <sub>★ 2.8k · Shell · MIT · npx · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add addyosmani/web-quality-skills`</sub>
- **[nothing-design-skill](https://github.com/dominikmartn/nothing-design-skill)** — (2.5k ⭐) - A Claude Code skill for generating UI in the Nothing design language. Monochrome, typographic, industrial
  <sub>★ 2.8k · MIT · clone · pushed 2026-04-01</sub>
  <sub>`git clone https://github.com/dominikmartn/nothing-design-skill.git`</sub>
- **[claude-code-plugins-plus-skills](https://github.com/jeremylongshore/tons-of-skills-marketplace)** — (2.4k ⭐) - 270+ Claude Code plugins with 739 agent skills
  <sub>★ 2.8k · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jeremylongshore/claude-code-plugins-plus-skills.git`</sub>
- **[sepia](https://github.com/Nanako0129/sepia)** — (782 ⭐) - A writing skill for Claude Code, Codex, Grok Build, and Antigravity that repairs narrative structure in fiction and applies venue-specific rules to professional prose
  <sub>★ 2.8k · Python · MIT · npx · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add Nanako0129/sepia -g # -g = user scope`</sub>
- **[designer-skills](https://github.com/Owl-Listener/designer-skills)** — (1.6k ⭐) - Designer skills, commands, and templates for agentic design workflows
  <sub>★ 2.7k · Markdown · MIT · clone · pushed 2026-09-05</sub>
  <sub>`git clone https://github.com/Owl-Listener/designer-skills`</sub>
- **[agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)** — (966 ⭐) - AWS-supported MCP servers, skills, and plugins for agents that build on AWS
  <sub>★ 2.7k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add aws/agent-toolkit-for-aws/skills`</sub>
- **[ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude)** — (1.9k ⭐) - A comprehensive marketing analysis and automation skill system for Claude Code
  <sub>★ 2.7k · Python · MIT · script · pushed 2026-03-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/main/install.sh | bash`</sub>
- **[diagram-design](https://github.com/supabase/agent-skills)** — (2.2k ⭐) - Thirteen editorial diagram types for Claude Code. Self-contained HTML + SVG. No shadows, no Mermaid-slop
  <sub>★ 2.6k · TypeScript · MIT · npx · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add supabase/agent-skills`</sub>
- **[Claude-OSINT](https://github.com/elementalsouls/Claude-OSINT)** — (1.8k ⭐) - Paired Claude skills for OSINT work, with recon modules, search patterns, and investigation workflows
  <sub>★ 2.6k · Python · MIT · clone · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/elementalsouls/Claude-OSINT.git`</sub>
- **[SkillClaw](https://github.com/AMAP-ML/SkillClaw)** — (2.0k ⭐) - Agentic evolver for creating and improving agent skills collectively
  <sub>★ 2.6k · Python · MIT · clone · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AMAP-ML/SkillClaw.git`</sub>
- **[social-media-research-skills](https://github.com/ScrapeCreators/social-media-research-skills)** — (927 ⭐) - Social-media research skills for AI agents powered by ScrapeCreators
  <sub>★ 2.6k · Python · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ScrapeCreators/social-media-research-skills`</sub>
- **[Expo-Skills](https://github.com/expo/skills)** — (2.1k ⭐) - A collection of AI agent skills for working with Expo projects and Expo Application Services
  <sub>★ 2.6k · Shell · MIT · npx · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills@latest add expo/skills --skill '*'`</sub>
- **[agent-toolkit](https://github.com/softaworks/agent-toolkit)** — (2.0k ⭐) - A curated collection of skills for AI coding agents
  <sub>★ 2.5k · Python · MIT · npx · pushed 2026-03-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add softaworks/agent-toolkit`</sub>
- **[mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw)** — (2.0k ⭐) - MCP server and Claude Code skill for Excalidraw — programmatic canvas toolkit to create, edit, and export diagrams via AI agents with real-time canvas sync
  <sub>★ 2.5k · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g mcp-excalidraw-server`</sub>
- **[learning-opportunities](https://github.com/DrCatHicks/learning-opportunities)** — (2.2k ⭐) - A Claude or Codex skill for deliberate skill development during AI-assisted coding
  <sub>★ 2.5k · Shell · CC-BY-4.0 · source · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/DrCatHicks/learning-opportunities.git`</sub>
- **[oil-motion](https://github.com/oil-oil/oil-motion)** — (1.9k ⭐) - Agent-agnostic interactive animation skill for creating smooth web motion that responds to scroll, mouse, drag, touch, or device orientation
  <sub>★ 2.4k · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add oil-oil/oil-motion`</sub>
- **[Claudeception](https://github.com/blader/Claudeception)** — (2.4k ⭐) - A Claude Code skill for autonomous skill extraction and continuous learning. Have Claude Code get smarter as it works
  <sub>★ 2.4k · Shell · MIT · clone · pushed 2026-02-21</sub>
  <sub>`git clone https://github.com/blader/Claudeception.git`</sub>
- **[blader](https://github.com/blader/Claudeception)** — (2.4k ⭐) - A Claude Code skill for autonomous skill extraction and continuous learning. Have Claude Code get smarter as it works
  <sub>★ 2.4k · Shell · MIT · clone · pushed 2026-02-21</sub>
  <sub>`git clone https://github.com/blader/Claudeception.git`</sub>
- **[claudex-loop](https://github.com/chaseai-yt/claudex-loop)** — (1.6k ⭐) - Claude Code skill for hardening implementation plans through reconnaissance, focused questioning, adversarial Codex review, and cross-model build inspection
  <sub>★ 2.4k · Python · source · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/chaseai-yt/claudex-loop.git`</sub>
- **[crucible](https://github.com/chaseai-yt/claudex-loop)** — (1.2k ⭐) - Claude Code skill that hardens implementation plans through reconnaissance, focused questioning, and adversarial Codex review
  <sub>★ 2.4k · Python · source · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/chaseai-yt/crucible.git`</sub>
- **[ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills)** — (852 ⭐) - Career and job-search skills for resume writing, ATS optimization, interview preparation, and applications
  <sub>★ 2.4k · MIT · npx · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Paramchoudhary/ResumeSkills -g -y`</sub>
- **[agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skills-platform)** — (1.6k ⭐) - Skill for turning repeatable workflows into reusable AI agent skills
  <sub>★ 2.4k · Python · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FrancyJGLisboa/agent-skill-creator.git`</sub>
- **[Apify Agent Skills](https://github.com/apify/agent-skills)** — (2.1k ⭐) - Production-grade web scraping and automation skills for AI coding agents
  <sub>★ 2.4k · Python · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g apify-cli`</sub>
- **[terraform-skill](https://github.com/antonbabenko/terraform-skill)** — (2.0k ⭐) - Terraform &amp; OpenTofu Skill for AI Agents - testing, modules, CI/CD, and production patterns
  <sub>★ 2.4k · npx · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/antonbabenko/terraform-skill`</sub>
- **[agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices)** — (2.0k ⭐) - Provider-neutral agent skill for Codex, Claude Code, and other AI coding tools
  <sub>★ 2.3k · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add DenisSergeevitch/agents-best-practices -g`</sub>
- **[modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)** — (1.4k ⭐) - Google Chrome guidance for modern web development, with a companion site for current web platform recommendations
  <sub>★ 2.3k · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx modern-web-guidance@latest install`</sub>
- **[fable-method](https://github.com/Sahir619/fable-method)** — (2.2k ⭐) - Four evidence-tested skills that guide coding agents through planning, execution, verification, and creation of domain-specific workflows
  <sub>★ 2.3k · Python · MIT · clone · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Sahir619/fable-method`</sub>
- **[ai-design-skills](https://github.com/elayadesign/ai-design-skills)** — (598 ⭐) - A collection of design skills for Claude Code, Cursor, Codex, Windsurf, and other tools that read Markdown rules
  <sub>★ 2.3k · MIT · clone · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/elayadesign/ai-design-skills.git`</sub>
- **[hack-skills](https://github.com/yaklang/hack-skills)** — (1.2k ⭐) - Practical hacking skills for AI agents working on security research and offensive security workflows
  <sub>★ 2.3k · CSS · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add yaklang/hack-skills`</sub>
- **[interview-coach-skill](https://github.com/noamseg/interview-coach-skill)** — (2.2k ⭐) - Claude Code interview coach for the full job-search lifecycle, from JD analysis and resume optimization through mock interviews and post-offer negotiation
  <sub>★ 2.3k · MIT · clone · pushed 2026-05-29</sub>
  <sub>`git clone https://github.com/noamseg/interview-coach-skill.git`</sub>
- **[wondelai/skills](https://github.com/wondelai/skills)** — (1.4k ⭐) - Agent skills for Claude Code and agentskills.io-compatible coding agents
  <sub>★ 2.2k · Shell · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add wondelai/skills --all --global`</sub>
- **[claude-blog](https://github.com/AgriciDaniel/claude-blog)** — (1.1k ⭐) - Claude Code blog skill suite with sub-skills, agents, and quality gates for SEO-focused and AI-citation-ready publishing workflows
  <sub>★ 2.2k · Python · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgriciDaniel/claude-blog.git`</sub>
- **[Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills)** — (1.3k ⭐) - Structured deep research skill for Claude Code, OpenCode, and Codex, with human-in-the-loop controls for research workflows
  <sub>★ 2.2k · Python · MIT · clone · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Weizhena/deep-research-skills.git`</sub>
- **[Youtube-clipper-skill](https://github.com/op7418/Youtube-clipper-skill)** — (2.0k ⭐) - Download videos, generate semantic chapters, clip segments, translate subtitles to bilingual format, and burn subtitles into videos
  <sub>★ 2.2k · Python · MIT · npx · pushed 2026-01-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/op7418/Youtube-clipper-skill`</sub>
- **[claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council)** — (753 ⭐) - Claude Code skill that routes decisions through a council of AI advisors with peer review
  <sub>★ 2.2k · source · pushed 2026-04-26</sub>
  <sub>`git clone https://github.com/aiwithremy/claude-skills-llm-council.git`</sub>
- **[asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)** — (1.4k ⭐) - Claude Code skill that applies ASD-STE100 Simplified Technical English rules to ambiguous instructions for agents
  <sub>★ 2.2k · Python · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add danyuchn/asd-ste100-skill`</sub>
- **[claude-real-video](https://github.com/HUANGCHIHHUNGLeo/claude-real-video)** — (1.4k ⭐) - Claude Code skill for real-video generation workflows, including planning, prompts, and production steps
  <sub>★ 2.2k · Python · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add HUANGCHIHHUNGLeo/claude-real-video # one command, installs the skill into Claude Code, Cursor, Codex, Copilot, Gemini CLI`</sub>
- **[agent-skills](https://github.com/WordPress/agent-skills/)** — (1.7k ⭐) - Expert-level WordPress knowledge for AI coding assistants - blocks, themes, plugins, and best practices
  <sub>★ 2.2k · JavaScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add WordPress/agent-skills --skill wp-plugin-development`</sub>
- **[delegate-skills](https://github.com/amElnagdy/delegate-skills)** — (2.1k ⭐) - Delegate coding tasks to a separate agent CLI, review the diff, and land the commit yourself
  <sub>★ 2.1k · JavaScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx skills add amElnagdy/delegate-skills`</sub>
- **[logo-generator-skill](https://github.com/op7418/logo-generator-skill)** — (1.3k ⭐) - Professional SVG logo generator with high-end showcase presentations
  <sub>★ 2.1k · HTML · npx · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/op7418/logo-generator-skill.git`</sub>
- **[aso-skills](https://github.com/appeeky/aso-skills)** — (2.1k ⭐) - AI agent skills for App Store Optimization and app marketing, including keyword research, metadata optimization, competitor analysis, and app growth
  <sub>★ 2.1k · MDX · MIT · npx · pushed 2026-08-22 · macOS</sub>
  <sub>`npx skills add eronred/aso-skills -a cursor`</sub>
- **[aso-skills](https://github.com/appeeky/aso-skills)** — (1.5k ⭐) - AI agent skills for App Store Optimization and app growth workflows
  <sub>★ 2.1k · MDX · MIT · npx · pushed 2026-08-22 · macOS</sub>
  <sub>`npx skills add eronred/aso-skills -a cursor`</sub>
- **[story-to-handdrawn-video](https://github.com/gnipbao/story-to-handdrawn-video)** — (665 ⭐) - Agent skill that turns Chinese stories or ordered images into hand-drawn diary-comic animations
  <sub>★ 2k · HTML · MIT · clone · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/gnipbao/story-to-handdrawn-video.git`</sub>
- **[code-review-skill](https://github.com/awesome-skills/code-review-skill)** — (1.1k ⭐) - Comprehensive code review skill for Claude Code, covering React, Vue, Rust, TypeScript, TanStack Query, and related stacks
  <sub>★ 2k · HTML · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add awesome-skills/code-review-skill`</sub>
- **[appllama-skills](https://github.com/Appllama/appllama-skills)** — (1.9k ⭐) - Agent skills that turn top-grossing app patterns into native-quality mobile screens
  <sub>★ 2k · MIT · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add appllama/appllama-skills`</sub>
- **[translate-book](https://github.com/deusyu/translate-book)** — (794 ⭐) - Claude Code skill that translates full books in PDF, DOCX, or EPUB format with parallel subagents
  <sub>★ 2k · Python · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add deusyu/translate-book -a codex -g`</sub>
- **[claude-design-system-prompt](https://github.com/Trystan-SA/claude-design-system-prompt)** — (1.9k ⭐) - A reverse-engineered design system prompt with 14 procedural skills for accessible interface design, prototyping, review, and visual refinement
  <sub>★ 2k · MIT · source · pushed 2026-07-06</sub>
  <sub>`git clone https://github.com/Trystan-SA/claude-design-system-prompt.git`</sub>
- **[chops](https://github.com/Shpigford/chops)** — (1.4k ⭐) - macOS app for browsing, organizing, and using AI agent skills
  <sub>★ 1.9k · Swift · clone · pushed 2026-08-23 · macOS</sub>
  <sub>`git clone https://github.com/Shpigford/chops.git`</sub>
- **[native-feel-skill](https://github.com/yetone/native-feel-skill)** — (1.8k ⭐) - An Agent Skill for designing cross-platform desktop apps that feel native — distilled from Raycast's 2.0 deep-dive and reverse engineering of Raycast Beta.app
  <sub>★ 1.9k · MIT · npx · pushed 2026-05-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add yetone/native-feel-skill -g`</sub>
- **[medical-research-skills](https://github.com/aipoch/medical-research-skills)** — (1.2k ⭐) - Agent skills for medical research tasks, including protocol design, data analysis, evidence review, and academic writing
  <sub>★ 1.9k · Python · MIT · clone · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aipoch/medical-research-skills.git`</sub>
- **[nano-banana-pro-prompts-recommend-skill](https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill)** — (1.6k ⭐) - Claude Code / Cursor skill to recommend from 6000+ Nano Banana Pro image prompts
  <sub>★ 1.9k · TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills i YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill`</sub>
- **[investorskills](https://github.com/questflowai/investorskills)** — (1.5k ⭐) - A library of structured investing frameworks drawn from durable investor decision patterns, built for study and use by AI finance agents
  <sub>★ 1.9k · Swift · MIT · npx · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/xuboyuebobb/investorskills`</sub>
- **[opc-skills](https://github.com/ReScienceLab/opc-skills)** — (937 ⭐) - Agent Skills for solopreneur workflows, including AI tooling, SEO, GEO, and operations tasks
  <sub>★ 1.8k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ReScienceLab/opc-skills`</sub>
- **[ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude)** — (1.5k ⭐) - AI legal assistant skill for contract review, legal research, and compliance workflows
  <sub>★ 1.7k · Python · script · pushed 2026-03-27 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/install.sh | bash`</sub>
- **[claude-skill-aso-appstore-screenshots](https://github.com/adamlyttleapps/claude-skill-aso-appstore-screenshots)** — (1.5k ⭐) - Claude skill for planning and producing App Store screenshot sets for ASO
  <sub>★ 1.7k · Python · MIT · source · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/adamlyttleapps/claude-skill-aso-appstore-screenshots.git`</sub>
- **[context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit)** — (1.2k ⭐) - Hand-crafted Claude Code skills for improving agent output quality, with compatibility across OpenCode, Cursor, Gemini CLI, and related tools
  <sub>★ 1.7k · TypeScript · GPL-3.0 · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add NeoLabHQ/context-engineering-kit`</sub>
- **[marketing-skills](https://github.com/irinabuht12-oss/marketing-skills)** — (1.6k ⭐) - 48 free Claude marketing skills for Google Ads, Meta Ads, SEO, and AI visibility, plus Ryze MCP
  <sub>★ 1.7k · clone · pushed 2026-09-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/irinabuht12-oss/marketing-skills`</sub>
- **[evals-skills](https://github.com/hamelsmu/evals-skills)** — (1.4k ⭐) - Skills for AI evaluation workflows and the AI Evals for Engineers course
  <sub>★ 1.7k · MIT · npx · pushed 2026-08-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/hamelsmu/evals-skills`</sub>
- **[academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)** — (155 ⭐) - Academic writing skill for revising research text into clearer, more natural prose while preserving technical meaning
  <sub>★ 1.7k · clone · pushed 2026-07-03</sub>
  <sub>`git clone https://github.com/AIScientists-Dev/academic-humanizer`</sub>
- **[Swift-Concurrency-Agent-Skill](https://github.com/AvdLee/Swift-Concurrency-Agent-Skill)** — (1.6k ⭐) - Expert Swift Concurrency guidance for AI coding agents working on Swift projects
  <sub>★ 1.7k · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add https://github.com/avdlee/swift-concurrency-agent-skill --skill swift-concurrency`</sub>
- **[callstackincubator](https://github.com/callstackincubator/agent-skills)** — (1.4k ⭐) - A collection of agent-optimized React Native skills for AI coding assistants
  <sub>★ 1.7k · Shell · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add callstackincubator/agent-skills --skill '*'`</sub>
- **[icm-architect](https://github.com/RinDig/icm-architect)** — (1.2k ⭐) - Claude skill for turning a process, idea, or problem into an ICM workspace organized as an agent architecture
  <sub>★ 1.6k · MIT · source · pushed 2026-08-25</sub>
  <sub>`git clone https://github.com/RinDig/icm-architect.git`</sub>
- **[headcount](https://github.com/cbrock84/headcount)** — (498 ⭐) - An agent organization for Claude Code with 15+ departments and 125+ independently installable skills
  <sub>★ 1.6k · Markdown · MIT · source · pushed 2026-09-17</sub>
  <sub>`git clone https://github.com/cbrock84/headcount.git`</sub>
- **[keep-codex-fast](https://github.com/vibeforge1111/keep-codex-fast)** — (1.5k ⭐) - A backup-first Codex skill for inspecting and maintaining local sessions, worktrees, logs, and project state
  <sub>★ 1.6k · Python · MIT · source · pushed 2026-05-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vibeforge1111/keep-codex-fast.git`</sub>
- **[Memento-Skills](https://github.com/Memento-Teams/Memento-Skills)** — (1.5k ⭐) - Agent skills that help agents design and refine other agents
  <sub>★ 1.6k · Python · Apache-2.0 · clone · pushed 2026-08-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Memento-Teams/Memento-Skills.git`</sub>
- **[skillkit](https://github.com/rohitg00/skillkit)** — (1.2k ⭐) - Portable skill toolkit for installing, translating, and sharing skills across Claude Code, Cursor, Codex, Copilot, and other coding agents
  <sub>★ 1.5k · TypeScript · Apache-2.0 · npm · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g skillkit # npm`</sub>
- **[female-portrait-director](https://github.com/liyue-aigc/female-portrait-director)** — (1.1k ⭐) - Modular Codex Skill for developing detailed AI female-portrait prompts
  <sub>★ 1.5k · MIT · npx · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/liyue-aigc/female-portrait-director/tree/main/skills/female-portrait-director -g`</sub>
- **[paper2code](https://github.com/PrathamLearnsToCode/paper2code)** — (1.4k ⭐) - Agent skill for turning arXiv papers into working code implementations
  <sub>★ 1.5k · Python · MIT · npx · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add PrathamLearnsToCode/paper2code/skills/paper2code`</sub>
- **[dream-loop](https://github.com/achimala/dream-loop)** — (1.1k ⭐) - Agent skill that builds games, apps, and scenes through image-generated targets, implementation, and AI critic feedback
  <sub>★ 1.5k · JavaScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add achimala/dream-loop`</sub>
- **[azure-skills](https://github.com/microsoft/azure-skills)** — (1.2k ⭐) - Microsoft agent plugin with skills and MCP server configurations for Azure development scenarios
  <sub>★ 1.5k · Shell · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills -a github-copilot -g -y`</sub>
- **[rust-skills](https://github.com/actionbook/rust-skills)** — (1.3k ⭐) - Rust Developer AI Assistance System — Meta-Problem-Driven Knowledge Indexing
  <sub>★ 1.5k · Shell · npx · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add actionbook/rust-skills`</sub>
- **[ELI5](https://github.com/DreambigOu/ELI5)** — (1.4k ⭐) - Claude Code skill that explains anything to different audiences with the right tone, vocabulary, and analogies
  <sub>★ 1.4k · Python · MIT · clone · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/DreambigOu/ELI5.git`</sub>
- **[skill-codex](https://github.com/skills-directory/skill-codex)** — (1.3k ⭐) - Claude Code skill for delegating prompts to Codex
  <sub>★ 1.4k · MIT · source · pushed 2026-09-13</sub>
  <sub>`git clone https://github.com/skills-directory/skill-codex.git`</sub>
- **[ux-ui-agent-skills](https://github.com/plugin87/ux-ui-agent-skills)** — (1.4k ⭐) - Design workflow with DTCG tokens, 50 components, WCAG 2.2, 138 design systems, framework-agnostic code, and objective quality gates
  <sub>★ 1.4k · JavaScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ux-ui-agent-skills demo # copies the rendered examples and opens them`</sub>
- **[claude-code-skills](https://github.com/daymade/claude-code-skills)** — (1.2k ⭐) - Marketplace-style collection of production-ready Claude Code skills for development workflows
  <sub>★ 1.4k · Python · MIT · npx · pushed 2026-09-22 · macOS</sub>
  <sub>`npx skills add`</sub>
- **[material-3-skill](https://github.com/hamen/material-3-skill)** — (1.0k ⭐) - Material Design 3 skill for Claude Code, with components, design tokens, theming, responsive layout, and MD3 audit support
  <sub>★ 1.4k · Shell · MIT · npx · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes skills add hamen/material-3-skill --skill material-3 -y`</sub>
- **[pm-claude-skills](https://github.com/mohitagw15856/pm-claude-skills)** — (1.0k ⭐) - Product-management skill pack with Agent Skills, subagents, and slash commands for Claude, ChatGPT, Gemini, Cursor, Codex, and Hermes
  <sub>★ 1.4k · HTML · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx pm-claude-skills add`</sub>
- **[ai-sales-team-claude](https://github.com/zubair-trabzada/ai-sales-team-claude)** — (768 ⭐) - Sales workflow system for Claude Code with prospect research, lead qualification, outreach, proposals, and pipeline reports
  <sub>★ 1.4k · Python · MIT · script · pushed 2026-03-27 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-sales-team-claude/main/install.sh | bash`</sub>
- **[app-store-preflight-skills](https://github.com/truongduy2611/app-store-preflight-skills)** — (1.2k ⭐) - AI agent skill that scans iOS and macOS projects for App Store rejection risks before submission
  <sub>★ 1.4k · MIT · npx · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add truongduy2611/app-store-preflight-skills`</sub>
- **[Pretty-mermaid-skills](https://github.com/imxv/Pretty-mermaid-skills)** — (756 ⭐) - To provide AI with Mermaid chart rendering capability, supporting both SVG and ASCII output formats
  <sub>★ 1.4k · JavaScript · MIT · npx · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add imxv/pretty-mermaid-skills@pretty-mermaid -g -y`</sub>
- **[ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill)** — (919 ⭐) - Local FFmpeg Agent Skill for Claude Code, Cursor, and Codex with structured video and audio editing tools
  <sub>★ 1.4k · Python · MIT · winget · pushed 2026-09-22 · macOS</sub>
  <sub>`winget install Gyan.FFmpeg`</sub>
- **[screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills)** — (1.3k ⭐) - Agent skills for screenwriting, television writing, and dramaturgy
  <sub>★ 1.3k · Python · MIT · clone · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jtydhr88/screenwriting-skills.git`</sub>
- **[lenny-skills](https://github.com/RefoundAI/lenny-skills)** — (1.1k ⭐) - Product management skill collection based on Lenny's Podcast, covering hiring, user research, strategy, shipping, and related PM workflows
  <sub>★ 1.3k · MIT · clone · pushed 2026-07-16</sub>
  <sub>`git clone https://github.com/RefoundAI/lenny-skills.git`</sub>
- **[academic-paper-skills](https://github.com/lishix520/academic-paper-skills)** — (932 ⭐) - Claude Code framework for planning and writing academic papers with strategist and composer skills
  <sub>★ 1.3k · Python · MIT · clone · pushed 2026-01-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/academic-paper-skills.git`</sub>
- **[gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills)** — (1.2k ⭐) - Claude Code skill for website AEO and GEO audits, with checks for AI search visibility, structured data, and framework-specific fixes
  <sub>★ 1.3k · HTML · MIT · clone · pushed 2026-06-07</sub>
  <sub>`git clone https://github.com/onvoyage-ai/gtm-engineer-skills.git`</sub>
- **[VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill)** — (945 ⭐) - This skill helps Claude write secure code and prevent common vulnerabilities
  <sub>★ 1.3k · Apache-2.0 · clone · pushed 2026-02-17</sub>
  <sub>`git clone https://github.com/BehiSecc/VibeSec-Skill`</sub>
- **[ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill)** — (1.1k ⭐) - iOS Simulator skill for Claude Code that helps agents build, run, and interact with apps while preserving token context
  <sub>★ 1.3k · Python · MIT · clone · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/conorluddy/ios-simulator-skill.git`</sub>
- **[autoprompt-skill](https://github.com/Spielewoy/autoprompt-skill)** — (739 ⭐) - Coding-agent skill that improves prompts for agentic coding tasks
  <sub>★ 1.3k · JavaScript · MIT · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g https://github.com/Spielewoy/autoprompt-skill/releases/download/v2.0.0/autoprompt-skill-2.0.0.tgz`</sub>
- **[guard-skills](https://github.com/amElnagdy/guard-skills)** — (881 ⭐) - Quality-gate skills that catch AI-generated failure modes in code, tests, and documentation
  <sub>★ 1.2k · MIT · npx · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add amElnagdy/guard-skills --list`</sub>
- **[kill-ai-slop](https://github.com/yetone/kill-ai-slop)** — (792 ⭐) - Field guide and Agent Skill for finding and removing AI-generated visual and copywriting clichés
  <sub>★ 1.2k · TypeScript · Apache-2.0 · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add yetone/kill-ai-slop`</sub>
- **[langchain-skills](https://github.com/langchain-ai/langchain-skills)** — (814 ⭐) - LangChain skills repository for agent workflows and LangChain project work
  <sub>★ 1.2k · TypeScript · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add langchain-ai/langchain-skills --skill '*' --yes`</sub>
- **[x-research-skill](https://github.com/rohunvora/x-research-skill)** — (1.1k ⭐) - X/Twitter research skill for Claude Code and OpenClaw
  <sub>★ 1.2k · TypeScript · clone · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rohunvora/x-research-skill.git`</sub>
- **[Xcode-Build-Optimization-Agent-Skill](https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill)** — (1.1k ⭐) - An Agent Skill helping you to optimize Xcode incremental and clean builds by running benchmarks and optimizing build settings
  <sub>★ 1.2k · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill`</sub>
- **[ppt-image-first](https://github.com/NyxTides/ppt-image-first)** — (1.2k ⭐) - Codex, Claude Code, and OpenCode skill for image-first PowerPoint workflows
  <sub>★ 1.2k · Python · Apache-2.0 · source · pushed 2026-05-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NyxTides/ppt-image-first.git`</sub>
- **[moai-adk](https://github.com/modu-ai/moai-adk)** — (1.1k ⭐) - Spec-first agentic development kit for Claude Code, with agents, skills, TDD and DDD quality gates, multilingual project support, and a Go CLI
  <sub>★ 1.2k · Go · Apache-2.0 · clone · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/modu-ai/moai-adk.git`</sub>
- **[COG-second-brain](https://github.com/huytieu/COG-second-brain)** — (554 ⭐) - A self-evolving second brain for Claude Code, Cursor, Kiro, Gemini CLI, and Codex, with AI skills, worker agents, and a people CRM
  <sub>★ 1.2k · HTML · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add huytieu/COG-second-brain`</sub>
- **[bioSkills](https://github.com/GPTomics/bioSkills)** — (945 ⭐) - SKILLS.md files for bioinformatics work with agents such as Claude Code
  <sub>★ 1.2k · Python · MIT · clone · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:GPTomics/bioSkills.git`</sub>
- **[app-onboarding-questionnaire](https://github.com/adamlyttleapps/claude-skill-app-onboarding-questionnaire)** — (1.1k ⭐) - Claude Code skill for designing questionnaire-style app onboarding flows based on subscription app conversion patterns
  <sub>★ 1.2k · MIT · clone · pushed 2026-04-06</sub>
  <sub>`git clone https://github.com/adamlyttleapps/claude-skill-app-onboarding-questoinnaire.git`</sub>
- **[webgpu-claude-skill](https://github.com/dgreenheck/webgpu-claude-skill)** — (1.0k ⭐) - A Claude skill for developing WebGPU applications with Three.js
  <sub>★ 1.2k · JavaScript · source · pushed 2026-04-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dgreenheck/webgpu-claude-skill.git`</sub>
- **[skillpack](https://github.com/CreminiAI/skillpack)** — (754 ⭐) - Tooling for packaging and deploying local AI agents and reusable skill packs for teams
  <sub>★ 1.2k · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @cremini/skillpack create`</sub>
- **[dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills)** — (1.0k ⭐) - Claude Code skills and sub-agents for .NET developers
  <sub>★ 1.2k · Shell · MIT · clone · pushed 2026-09-17</sub>
  <sub>`git clone https://github.com/Aaronontheweb/dotnet-skills.git`</sub>
- **[skills-for-fabric](https://github.com/microsoft/skills-for-fabric)** — (632 ⭐) - Skills and MCP systems for using Microsoft Fabric from CLI, VS Code, Claude, and related agent workflows
  <sub>★ 1.2k · Python · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/skills-for-fabric.git`</sub>
- **[Axiom](https://github.com/CharlesWiltgen/Axiom)** — (973 ⭐) - Battle-tested Claude Code skills for modern xOS (iOS, iPadOS, watchOS, tvOS) development
  <sub>★ 1.2k · TypeScript · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CharlesWiltgen/Axiom.git`</sub>
- **[tutor-skills](https://github.com/bevibing/tutor-skills)** — (974 ⭐) - Claude Code skill that turns PDFs, documents, and codebases into Obsidian study vaults
  <sub>★ 1.2k · Shell · MIT · npx · pushed 2026-02-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add RoundTable02/tutor-skills`</sub>
- **[aws-agent-skills](https://github.com/itsmostafa/aws-agent-skills)** — (1.1k ⭐) - AWS cloud engineering skills for Claude Code across 18 core AWS services
  <sub>★ 1.2k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/itsmostafa/aws-agent-skills.git`</sub>
- **[flyai-skill](https://github.com/alibaba-flyai/flyai-skill)** — (755 ⭐) - FlyAI agent skill repository
  <sub>★ 1.2k · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @fly-ai/flyai-cli`</sub>
- **[swift-ios-skills](https://github.com/dpearson2699/swift-ios-skills)** — (790 ⭐) - Agent Skills for iOS, Swift, SwiftUI, and modern Apple framework development
  <sub>★ 1.1k · Python · npx · pushed 2026-07-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add dpearson2699/swift-ios-skills`</sub>
- **[manim_skill](https://github.com/adithya-s-k/manim_skill)** — (918 ⭐) - Agent skills for Manim to create 3Blue1Brown style animations
  <sub>★ 1.1k · Python · MIT · npx · pushed 2026-01-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices`</sub>
- **[design-engineer-auditor-package](https://github.com/kylezantos/design-motion-principles)** — A Claude Code skill for motion design audits, trained on Emil Kowalski, Jakub Krehel, and Jhey Tompkins
  <sub>★ 1.1k · HTML · MIT · npx · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add kylezantos/design-motion-principles`</sub>
- **[claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill)** — (791 ⭐) - Deep research skill for Claude Code with a phased pipeline, source credibility scoring, and validation checks
  <sub>★ 1.1k · Python · brew · pushed 2026-04-11 · macOS</sub>
  <sub>`brew tap 199-biotechnologies/tap`</sub>
- **[Higgsfield AI Skills](https://github.com/higgsfield-ai/skills)** — (554 ⭐) - Agent Skills for image and video generation, product photography, marketplace assets, and website creation through Higgsfield AI
  <sub>★ 1.1k · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add higgsfield-ai/skills`</sub>
- **[codex-first-customer-finder-skill](https://github.com/Kappaemme-git/codex-first-customer-finder-skill)** — (878 ⭐) - A Codex skill that finds evidence-backed potential first customers from recent public signals
  <sub>★ 1.1k · Python · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes codex-first-customer-finder-skill@latest`</sub>
- **[Day1Global-Skills](https://github.com/star23/Day1Global-Skills)** — (928 ⭐) - Agent skills for U.S. stocks, macro markets, and crypto research
  <sub>★ 1.1k · MIT · npx · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/star23/Day1Global-Skills --all`</sub>
- **[kotlin-agent-skills](https://github.com/Kotlin/kotlin-agent-skills)** — (886 ⭐) - AI agent skills for projects that use the Kotlin language
  <sub>★ 1.1k · Shell · Apache-2.0 · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Kotlin/kotlin-agent-skills`</sub>
- **[banana-claude](https://github.com/AgriciDaniel/banana-claude)** — (751 ⭐) - AI image generation skill for Claude Code with a creative-director workflow powered by Gemini
  <sub>★ 1.1k · Python · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgriciDaniel/banana-claude.git`</sub>
- **[chrisbanes skills](https://github.com/chrisbanes/skills)** — (779 ⭐) - Skills for Kotlin, Jetpack Compose, and Android development
  <sub>★ 1.1k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add chrisbanes/skills`</sub>
- **[synalinks-skills](https://github.com/numman-ali/n-skills)** — (996 ⭐) - Claude skills for Synalinks
  <sub>★ 1k · TypeScript · Apache-2.0 · npm · pushed 2026-09-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g openskills`</sub>
- **[ai-copywriter](https://github.com/mikiarlo3/ai-copywriter)** — (919 ⭐) - Copywriting skill with marketing knowledge and a human tone
  <sub>★ 1k · Python · MIT · npx · pushed 2026-08-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add mikiarlo3/ai-copywriter --global`</sub>
- **[app-store-connect-cli-skills](https://github.com/rorkai/app-store-connect-cli-skills)** — (871 ⭐) - Skills for automating App Store Connect, TestFlight, deployment, and related asc CLI workflows
  <sub>★ 1k · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add rorkai/app-store-connect-cli-skills`</sub>
- **[vibe-security-skill](https://github.com/raroque/vibe-security-skill)** — (785 ⭐) - Security audit skill for finding common vulnerabilities in apps built with AI coding assistants
  <sub>★ 1k · MIT · npx · pushed 2026-03-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/raroque/vibe-security-skill --skill vibe-security`</sub>
- **[getsentry/skills](https://github.com/getsentry/skills)** — (807 ⭐) - Agent Skills used by the Sentry team for development work
  <sub>★ 1k · Python · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add getsentry/skills`</sub>
- **[next-skills](https://github.com/vercel-labs/next-skills)** — (929 ⭐) - Agent skills for common Next.js workflows
  <sub>★ 983 · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vercel/next.js`</sub>
- **[claude-skill-homeassistant](https://github.com/komal-SkyNET/claude-skill-homeassistant)** — (425 ⭐) - Claude Code skill to supercharge and manage all Home Assistant workflows
  <sub>★ 961 · MIT · pipx · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install homeassistant-cli`</sub>
- **[self-learning-skills](https://github.com/Kulaxyz/self-learning-skills)** — (848 ⭐) - Self-learning skill pack that helps coding agents capture lessons from past work and reuse them in later sessions
  <sub>★ 957 · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add kulaxyz/self-learning-skills # this project (auto-detects agents)`</sub>
- **[bolt-slides](https://github.com/stackblitz/bolt-slides)** — (691 ⭐) - A React presentation framework with a bundled Agent Skill for building interactive slide decks as responsive web apps
  <sub>★ 941 · TypeScript · MIT · clone · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stackblitz/bolt-slides`</sub>
- **[dzhng/skills](https://github.com/dzhng/skills)** — (534 ⭐) - Personal collection of Claude Code skills for repeatable engineering and knowledge-work tasks
  <sub>★ 926 · JavaScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add dzhng/skills`</sub>
- **[power-bi-agentic-development](https://github.com/data-goblin/power-bi-agentic-development)** — (732 ⭐) - Power BI and Microsoft Fabric skills, subagents, and hooks for semantic models, DAX, TMDL, reports, and dashboards
  <sub>★ 923 · C# · GPL-3.0 · source · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/data-goblin/power-bi-agentic-development.git`</sub>
- **[autocli-skill](https://github.com/nashsu/autocli-skill)** — (872 ⭐) - Claude Code and agent skill for fetching real-time web data across many platforms through a Chrome login session
  <sub>★ 920 · npx · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/nashsu/AutoCLI-skill`</sub>
- **[SkillForge](https://github.com/tripleyak/SkillForge)** — (694 ⭐) - The ultimate meta-skill for generating best-in-class Claude Code skills
  <sub>★ 899 · Python · MIT · clone · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tripleyak/SkillForge.git`</sub>
- **[ui-design-brain](https://github.com/carmahhawwari/ui-design-brain)** — (826 ⭐) - UI component knowledge skill for agents, with layout patterns and design-system conventions for interface work
  <sub>★ 888 · clone · pushed 2026-02-28</sub>
  <sub>`git clone https://github.com/carmahhawwari/ui-design-brain.git`</sub>
- **[claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)** — (810 ⭐) - Toolkit for building and deploying Claude Skills, code agents, slash commands, and LLM prompts
  <sub>★ 869 · Python · MIT · source · pushed 2025-11-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/alirezarezvani/claude-code-skill-factory.git`</sub>
- **[x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill)** — (802 ⭐) - Claude Code skill for publishing Markdown articles to X (Twitter) Articles
  <sub>★ 866 · Python · MIT · clone · pushed 2026-01-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/wshuyi/x-article-publisher-skill.git`</sub>
- **[cc-design](https://github.com/ZeroZ-lab/cc-design)** — (805 ⭐) - High-fidelity HTML design and prototype guidance skill for AI agents
  <sub>★ 831 · JavaScript · source · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ZeroZ-lab/cc-design.git`</sub>
- **[claude-office-skills](https://github.com/tfriedel/claude-office-skills)** — (740 ⭐) - Office document creation and editing skills for Claude Code - PPTX, DOCX, XLSX, and PDF workflows with automation support
  <sub>★ 831 · Python · source · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tfriedel/claude-office-skills.git`</sub>
- **[second-brain-skills](https://github.com/coleam00/second-brain-skills)** — (781 ⭐) - Claude Skills that turn Claude Code into a second-brain workspace
  <sub>★ 829 · Python · source · pushed 2026-01-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/coleam00/second-brain-skills.git`</sub>
- **[claude-code-tresor](https://github.com/alirezarezvani/claude-code-tresor)** — (738 ⭐) - Claude Code collection with autonomous skills, expert agents, slash commands, and reusable prompts for development workflows
  <sub>★ 776 · Shell · MIT · clone · pushed 2026-07-03</sub>
  <sub>`git clone https://github.com/alirezarezvani/claude-code-tresor.git`</sub>
- **[advertising-skills](https://github.com/realkimbarrett/advertising-skills)** — (663 ⭐) - Advertising Skills for Open Claw, Claude Code &amp; AI agents
  <sub>★ 753 · source · pushed 2026-03-26</sub>
  <sub>`git clone https://github.com/realkimbarrett/advertising-skills.git`</sub>
- **[Agent-Skills](https://github.com/MicrosoftDocs/Agent-Skills)** — (617 ⭐) - Microsoft and Azure Agent Skills that give coding assistants structured expertise from Microsoft Learn documentation
  <sub>★ 750 · CC-BY-4.0 · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MicrosoftDocs/agent-skills.git`</sub>
- **[cloudflare-skill](https://github.com/dmmulroy/cloudflare-skill)** — (725 ⭐) - Comprehensive Cloudflare platform reference docs for AI/LLM consumption
  <sub>★ 728 · Shell · MIT · script · pushed 2026-01-29 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/dmmulroy/cloudflare-skill/main/install.sh | bash`</sub>
- **[SkillSpec](https://github.com/modiqo/skillspec)** — (943 ⭐) - Open-source CLI and contract format for checking, testing, and documenting how Agent Skills should run
  <sub>★ 725 · Rust · Apache-2.0 · cargo · pushed 2026-08-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install skillspec`</sub>
- **[nuxt-skills](https://github.com/onmax/nuxt-skills)** — (683 ⭐) - Vue, Nuxt, and NuxtHub skills for AI coding assistants
  <sub>★ 711 · TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add onmax/nuxt-skills`</sub>
- **[viserys-agent](https://github.com/rizqinrr/viserys-agent)** — (665 ⭐) - Self-contained pack of 28 Markdown workflow skills covering DEFINE, PLAN, BUILD, VERIFY, REVIEW, and SHIP
  <sub>★ 709 · JavaScript · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rizqinrr/viserys-agent.git`</sub>
- **[qmd-skill](https://github.com/levineam/qmd-skill)** — (690 ⭐) - A Codex/Clawd skill definition for qmd (Quick Markdown Search)
  <sub>★ 700 · source · pushed 2026-02-25</sub>
  <sub>`git clone https://github.com/levineam/qmd-skill.git`</sub>
- **[napkin](https://github.com/blader/napkin)** — (560 ⭐) - A Claude Code skill that gives the agent persistent memory of its mistakes via a per-repo markdown scratchpad
  <sub>★ 612 · MIT · clone · pushed 2026-02-21</sub>
  <sub>`git clone https://github.com/blader/napkin.git`</sub>
- **[Semia](https://github.com/berabuddies/Semia)** — (549 ⭐) - Security audit tooling for reviewing AI agent skills before they are used in agent workflows
  <sub>★ 609 · Python · Apache-2.0 · pip · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install semia-audit`</sub>
- **[agentkits-marketing](https://github.com/aitytech/agentkits-marketing)** — (552 ⭐) - Marketing automation skills and agent workflows for Claude Code, Cursor, GitHub Copilot, and compatible AI assistants
  <sub>★ 606 · Python · MIT · npx · pushed 2026-08-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @aitytech/agentkits-marketing install`</sub>
- **[solid-skills](https://github.com/ramziddin/solid-skills)** — (443 ⭐) - AI agent skill for writing senior-engineer quality code through SOLID principles, TDD, and clean architecture
  <sub>★ 593 · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ramziddin/solid-skills`</sub>
- **[skill.color-expert](https://github.com/meodai/skill.color-expert)** — (505 ⭐) - Agent skill for color science, accessibility checks, palette generation, pigment mixing, and historical color theory
  <sub>★ 591 · CC-BY-4.0 · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add meodai/skill.color-expert`</sub>
- **[agent-skills](https://github.com/elastic/agent-skills)** — (513 ⭐) - Official Elastic skills for AI agents that work with Elastic products and workflows
  <sub>★ 584 · JavaScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add elastic/agent-skills`</sub>
- **[agent-skills-standard](https://github.com/HoangNguyen0403/agent-skills-standard)** — (511 ⭐) - Agent Skills standards and best-practice packs for programming languages, frameworks, and common development workflows
  <sub>★ 571 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-skills-standard@latest init`</sub>
- **[claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)** — (502 ⭐) - Plugin suite and bundled MCP servers for delivery workflows, codebase audits, documentation, performance optimization, and remote SSH work
  <sub>★ 566 · PowerShell · MIT · source · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/levnikolaevich/claude-code-skills.git`</sub>
- **[solana-dev-skill](https://github.com/solana-foundation/solana-dev-skill)** — (524 ⭐) - Claude Code skill for modern Solana development
  <sub>★ 559 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add solana-foundation/solana-dev-skill`</sub>
- **[vibecosystem](https://github.com/vibeeval/vibecosystem)** — (507 ⭐) - An AI software-team system for Claude Code with agents, skills, hooks, and self-learning workflow support
  <sub>★ 535 · C# · MIT · npx · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibecosystem init`</sub>
- **[token-diet](https://github.com/Kulaxyz/token-diet)** — (562 ⭐) - Always-on token-efficiency skill for Claude Code, Codex, Cursor, Windsurf, and Cline
  <sub>★ 472 · Shell · script · pushed 2026-07-04 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Kulaxyz/token-diet/main/install.sh | bash`</sub>
- **[csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill)** — (407 ⭐) - A Claude Skill that automatically analyzes uploaded CSV files — generating summary statistics, detecting missing data, and creating quick visualizations using Python and pandas
  <sub>★ 467 · Python · clone · pushed 2025-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:coffeefuelbump/csv-data-summarizer-claude-skill.git`</sub>
- **[elevenlabs skills](https://github.com/elevenlabs/skills)** — (347 ⭐) - ElevenLabs skill collection for building agents that work with speech, sound effects, music, transcription, and text-to-speech workflows
  <sub>★ 458 · Python · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @elevenlabs/cli`</sub>
- **[awesome-pm-skills](https://github.com/menkesu/awesome-pm-skills)** — (371 ⭐) - Product-management skill collection for research, planning, prioritization, launch work, and stakeholder communication
  <sub>★ 406 · source · pushed 2026-02-19</sub>
  <sub>`git clone https://github.com/menkesu/awesome-pm-skills.git`</sub>
- **[skill-threat-modeling](https://github.com/fr33d3m0n/threat-modeling)** — Code-First Deep Risk Analysis Skill for Claude Code - 8-Phase Workflow with Security design review, STRIDE Threat modeling, PenTest and attack chain analysis, Software compliance assessment
  <sub>★ 345 · Python · BSD-3-Clause · clone · pushed 2026-05-12 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/fr33d3m0n/threat-modeling.git`</sub>
- **[awesome-dfir-skills](https://github.com/tsale/awesome-dfir-skills)** — (318 ⭐) - A curated collection of DFIR skills and workflows for InfoSec practitioners
  <sub>★ 323 · Python · Apache-2.0 · source · pushed 2026-05-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tsale/awesome-dfir-skills.git`</sub>
- **[google-ai-mode-skill](https://github.com/PleasePrompto/google-ai-mode-skill)** — Claude Code skill for free Google AI Mode search with citations
  <sub>★ 295 · Python · clone · pushed 2026-09-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/PleasePrompto/google-ai-mode-skill`</sub>
- **[PPT-Design-Skill](https://github.com/sunchaokun/PPT-Design-Skill)** — (1.2k ⭐) - Precision PPT design skill for OpenCode, Claude Code, and Codex, with 40,000+ styles, Build Mode control, AI image generation, and fully editable PPTX output
  <sub>★ 282 · Python · MIT · clone · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sunchaokun/PPT-Design-Skill.git`</sub>
- **[claude-code-skills](https://github.com/whawkinsiv/solo-founder-skills)** — (222 ⭐) - Complete software development lifecycle skills optimized for non-technical founders building SaaS applications with AI tools (Lovable, Replit, Claude Code)
  <sub>★ 246 · MIT · clone · pushed 2026-08-27</sub>
  <sub>`git clone https://github.com/whawkinsiv/solo-founder-skills.git`</sub>
- **[claude-code-voice-skill](https://github.com/abracadabra50/claude-code-voice-skill)** — (167 ⭐) - Skill to talk to Claude about your projects over the phone
  <sub>★ 172 · Python · MIT · pip · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install claude-code-voice`</sub>
- **[Apple-Hig-Designer](https://github.com/axiaoge2/Apple-Hig-Designer)** — A Claude Code Skill for designing professional interfaces following Apple Human Interface Guidelines
  <sub>★ 153 · JavaScript · MIT · source · pushed 2026-02-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/axiaoge2/Apple-Hig-Designer.git`</sub>
- **[nano-image-generator-skill](https://github.com/lxfater/nano-image-generator-skill)** — (126 ⭐) - A Claude Code skill for generating images using Gemini 3 Pro Preview (Nano Banana Pro)
  <sub>★ 128 · Python · clone · pushed 2026-01-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YOUR_USERNAME/nano-image-generator-skill.git`</sub>
- **[claude-cs](https://github.com/nbashaw/claude-cs)** — A Claude Code skill that helps you build custom customer support automation for your company
  <sub>★ 91 · MIT · clone · pushed 2026-01-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/nbashaw/claude-cs`</sub>
- **[claude-skills-supercharged](https://github.com/jefflester/claude-skills-supercharged)** — A "supercharged" implementation of Claude Code Skills — using Haiku prompt analysis/critical skill scoring and skill auto-injection for friction-free, context-driven workflows
  <sub>★ 42 · TypeScript · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jefflester/claude-skills-supercharged.git`</sub>
- **[claude-skills](https://github.com/Jeffallan/claude-skills)** — (9.9k ⭐) - 66 Specialized Skills for Full-Stack Developers
  <sub>source</sub>
  <sub>`git clone https://github.com/Jeffallan/claude-skills.git`</sub>
- **[book-to-skill](https://github.com/Leutenegger/book-to-skill)** — (1.2k ⭐) - Turn any technical book PDF into a Claude Code skill — ready to study, reference, and use while you work
  <sub>unavailable</sub>
- **[happy-claude-skills](https://github.com/iamzhihuix/happy-claude-skills)** — (296 ⭐) - A collection of practical skill plugins designed for Claude Code
  <sub>unavailable</sub>
- **[remotion-dev/skills](https://www.remotion.dev/docs/ai/skills)** — Create videos programmatically
  <sub>website</sub>
  <sub>`https://www.remotion.dev/docs/ai/skills`</sub>
- **[BFL Agent Skills](https://docs.bfl.ai/api_integration/skills_integration)** — Reusable capabilities that teach AI agents how to work with FLUX models
  <sub>website</sub>
  <sub>`https://docs.bfl.ai/api_integration/skills_integration`</sub>
- **[Manus Skills](https://manus.im/blog/manus-skills)** — Manus' official agent skills
  <sub>website</sub>
  <sub>`https://manus.im/blog/manus-skills`</sub>
- **[Firecrawl Skills](https://docs.firecrawl.dev/sdks/cli)** — An easy way for AI agents such as Claude Code, Antigravity and OpenCode to use Firecrawl through the CLI
  <sub>website</sub>
  <sub>`https://docs.firecrawl.dev/sdks/cli`</sub>
- **[meta_skilld](https://github.com/Dicklesworthstone/meta_skilld)** — Rust CLI for managing Claude Code skills: indexing, building, bundling, and sharing
  <sub>unavailable</sub>

## Claude Plugins

- **[ponytail](https://github.com/DietrichGebert/ponytail)** — Makes your AI agent think like the laziest senior dev in the room
  <sub>★ 144.1k · JavaScript · MIT · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/DietrichGebert/ponytail`</sub>
- **[claude-hud](https://github.com/jarrodwatts/claude-hud)** — A Claude Code plugin that shows what's happening - context usage, active tools, running agents, and todo progress
  <sub>★ 28.1k · JavaScript · MIT · clone · pushed 2026-09-19 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/jarrodwatts/claude-hud`</sub>
- **[compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)** — (25.1k ⭐) - Official Compound Engineering plugin for Claude Code, Codex, Cursor, and other coding agents
  <sub>★ 25.2k · TypeScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/EveryInc/compound-engineering-plugin`</sub>
- **[harness](https://github.com/revfactory/harness)** — A meta-skill that designs domain-specific agent teams, defines specialized agents, and generates the skills they use
  <sub>★ 9.1k · HTML · Apache-2.0 · source · pushed 2026-07-24</sub>
  <sub>`git clone https://github.com/revfactory/harness.git`</sub>
- **[fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction)** — (4.8k ⭐) - Claude Code plugin that replaces compaction summaries with fast Jev decisions while keeping retained tool results verbatim
  <sub>★ 6.2k · TypeScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tamaratran/fast-jev-compaction.git`</sub>
- **[interface-design](https://github.com/Dammyjay93/interface-design)** — Design engineering for Claude Code. Craft, memory, and enforcement for consistent UI
  <sub>★ 5.7k · Shell · MIT · npx · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/dammyjay93/interface-design --skill interface-design`</sub>
- **[claude-octopus](https://github.com/nyldn/claude-octopus)** — (4.1k ⭐) - Run multiple AI models against the same research, design, or coding task and surface disagreements before you ship
  <sub>★ 4.1k · Shell · MIT · clone · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nyldn/claude-octopus.git`</sub>
- **[notfair-plugin](https://github.com/nowork-studio/notfair-plugin)** — (3.4k ⭐) - Open-source SEO, GEO, and marketing skills for AI agents
  <sub>★ 3.8k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[arscontexta](https://github.com/agenticnotetaking/arscontexta)** — Claude Code plugin that generates individualized knowledge systems from conversation
  <sub>★ 3.5k · Shell · MIT · source · pushed 2026-02-24 · Win?</sub>
  <sub>`git clone https://github.com/agenticnotetaking/arscontexta.git`</sub>
- **[call-me](https://github.com/ZeframLou/call-me)** — Minimal plugin that lets Claude Code call you on the phone
  <sub>★ 2.6k · TypeScript · source · pushed 2026-04-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ZeframLou/call-me.git`</sub>
- **[Claude Code Toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)** — (2.3k ⭐) - A Claude Code marketplace with plugins, agents, skills, commands, hooks, rules, templates, and MCP configurations
  <sub>★ 2.6k · JavaScript · Apache-2.0 · npx · pushed 2026-05-12 · macOS</sub>
  <sub>`npx skillkit@latest install claude-code-toolkit/tdd-mastery`</sub>
- **[pg-aiguide](https://github.com/timescale/pg-aiguide)** — MCP server and Claude plugin for Postgres skills, documentation, and database guidance
  <sub>★ 1.8k · Python · Apache-2.0 · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add timescale/pg-aiguide --skill postgres`</sub>
- **[claude-code-safety-net](https://github.com/kenryu42/cc-safety-net)** — A Claude Code plugin that acts as a safety net, catching destructive git and filesystem commands before they execute
  <sub>★ 1.6k · TypeScript · MIT · npm · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g cc-safety-net`</sub>
- **[claude-workflow-v2](https://github.com/CloudAI-X/claude-workflow-v2)** — Universal Claude Code workflow plugin with agents, skills, hooks, and commands
  <sub>★ 1.4k · Python · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add CloudAI-X/claude-workflow-v2`</sub>
- **[hackingtool-plugin](https://github.com/AKCodez/hackingtool-plugin)** — 183+ pentesting &amp; OSINT tools from Z4nzu/hackingtool
  <sub>★ 1.1k · Python · source · pushed 2026-04-25 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/AKCodez/hackingtool-plugin.git`</sub>
- **[fablize](https://github.com/fivetaku/fablize)** — Claude Code plugin that changes Opus behavior with a Fable-inspired response style
  <sub>★ 898 · Python · MIT · source · pushed 2026-07-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fivetaku/fablize.git`</sub>
- **[claude-forge](https://github.com/sangrokjung/claude-forge)** — (756 ⭐) - Claude Code plugin framework with agents, commands, skills, and security hooks
  <sub>★ 841 · Shell · MIT · script · pushed 2026-09-03 · macOS</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/sangrokjung/claude-forge/main/install.sh | bash`</sub>
- **[plugins-for-claude-natives](https://github.com/team-attention/plugins-for-claude-natives)** — A collection of Claude Code plugins for power users who want to extend Claude Code's capabilities beyond the defaults
  <sub>★ 826 · Python · MIT · source · pushed 2026-04-20 · macOS</sub>
  <sub>`git clone https://github.com/team-attention/plugins-for-claude-natives.git`</sub>
- **[ralph-wiggum-marketer](https://github.com/muratcankoylan/ralph-wiggum-marketer)** — A Claude Code Plugin that provides an autonomous AI copywriter
  <sub>★ 777 · JavaScript · clone · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/muratcankoylan/ralph-wiggum-marketer.git`</sub>
- **[design-plugin](https://github.com/0xdesign/design-plugin)** — A Claude Code plugin that helps you make confident UI design decisions through rapid iteration
  <sub>★ 757 · TypeScript · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0xdesign/design-plugin.git`</sub>
- **[claude-review-loop](https://github.com/hamelsmu/claude-review-loop)** — Claude Code plugin: automated code review loop with Codex
  <sub>★ 723 · Shell · source · pushed 2026-03-15 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hamelsmu/claude-review-loop.git`</sub>
- **[claude-code](https://github.com/laravel/agent-skills)** — A collection of Claude Code plugins tailored for PHP / Laravel development
  <sub>★ 720 · Shell · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/laravel/agent-skills/tree/main/laravel-cloud/skills/deploying-to-cloud`</sub>
- **[cartographer](https://github.com/kingbootoshi/cartographer)** — Claude Code plugin that maps and documents codebases of any size using parallel AI subagents
  <sub>★ 720 · TypeScript · source · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kingbootoshi/cartographer.git`</sub>
- **[hello2cc](https://github.com/hellowind777/hello2cc)** — Native-first Claude Code plugin for third-party models with silent Agent model injection and output styles
  <sub>★ 692 · JavaScript · Apache-2.0 · clone · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hellowind777/hello2cc.git`</sub>
- **[claude-dashboard](https://github.com/uppinote20/claude-dashboard)** — Comprehensive status line plugin for Claude Code with context usage, API rate limits, and cost tracking
  <sub>★ 572 · TypeScript · MIT · clone · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/uppinote20/claude-dashboard.git`</sub>
- **[adversarial-spec](https://github.com/zscole/adversarial-spec)** — A Claude Code plugin that iteratively refines product specifications by debating between multiple LLMs until all models reach consensus
  <sub>★ 557 · Python · MIT · source · pushed 2026-01-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zscole/adversarial-spec.git`</sub>
- **[ensue-skill](https://github.com/mutable-state-inc/ensue-skill)** — A persistent knowledge tree that grows with you - what you learn today enriches tomorrow's reasoning
  <sub>★ 422 · Shell · source · pushed 2026-01-29</sub>
  <sub>`git clone https://github.com/mutable-state-inc/ensue-skill.git`</sub>
- **[homunculus](https://github.com/humanplane/homunculus)** — A Claude Code plugin that watches how you work, learns your patterns, and evolves itself to help you better
  <sub>★ 391 · Shell · source · pushed 2026-01-23</sub>
  <sub>`git clone https://github.com/humanplane/homunculus.git`</sub>
- **[compact-plus](https://github.com/u-ichi/compact-plus)** — (151 ⭐) - Claude Code plugin that preserves and restores working state around /compact
  <sub>★ 203 · Shell · MIT · source · pushed 2026-07-27</sub>
  <sub>`git clone https://github.com/u-ichi/compact-plus.git`</sub>
- **[claude-code-plugin](https://github.com/browserbase/claude-code-plugin)** — Browserbase plugin for Claude Code - Use cloud browsers with Claude Code instead of local Chrome
  <sub>★ 73 · JavaScript · clone · pushed 2025-12-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browserbase/claude-code-plugin.git`</sub>
- **[CloudBase AI Toolkit](https://github.com/TencentCloudBase/CloudBase-AI-Toolkit)** — (1.1k ⭐) - Claude Code plugin, Agent Skills, and MCP server for using Tencent CloudBase databases, authentication, functions, storage, and deployment from coding agents
  <sub>source</sub>
  <sub>`git clone https://github.com/TencentCloudBase/CloudBase-AI-Toolkit.git`</sub>

## IDE &amp; Editor Integrations

- **[CC GUI](https://github.com/zhukunpenglinyutong/jetbrains-cc-gui)** — (6.2k ⭐) - IntelliJ IDEA plugin with a visual interface for Claude Code, OpenAI Codex, and other AI coding CLIs
  <sub>★ 6.5k · Java · MIT · source · pushed 2026-09-20 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zhukunpenglinyutong/jetbrains-cc-gui.git`</sub>
- **[claudecode.nvim](https://github.com/coder/claudecode.nvim)** — (2.8k ⭐) - A Claude Code Neovim IDE Extension
  <sub>★ 3.1k · Lua · MIT · source · pushed 2026-09-13 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/coder/claudecode.nvim.git`</sub>
- **[claude-code.nvim](https://github.com/greggh/claude-code.nvim)** — (2.1k ⭐) - Seamless integration between the Claude Code AI assistant and Neovim
  <sub>★ 2.1k · Lua · MIT · source · pushed 2026-02-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/greggh/claude-code.nvim.git`</sub>
- **[claude-code-ide.el](https://github.com/manzaltu/claude-code-ide.el)** — (1.6k ⭐) - Claude Code IDE for Emacs provides native integration with Claude Code CLI through the Model Context Protocol (MCP)
  <sub>★ 1.7k · Emacs Lisp · GPL-3.0 · source · pushed 2026-09-14 · Win?</sub>
  <sub>`git clone https://github.com/manzaltu/claude-code-ide.el.git`</sub>
- **[minuet-ai.nvim](https://github.com/milanglacier/minuet-ai.nvim)** — (1.3k ⭐) - Code completion as-you-type from popular LLMs including OpenAI, Gemini, Claude, Ollama
  <sub>★ 1.4k · Lua · GPL-3.0 · source · pushed 2026-08-14 · Win?</sub>
  <sub>`git clone https://github.com/milanglacier/minuet-ai.nvim.git`</sub>
- **[getspecstory](https://github.com/specstoryai/getspecstory)** — (1.2k ⭐) - Extensions for GH Copilot, Cursor, and Claude Code
  <sub>★ 1.3k · Go · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add specstoryai/getspecstory --skill lore`</sub>
- **[claude-code-chat](https://github.com/andrepimenta/claude-code-chat)** — (1.1k ⭐) - Beautiful Claude Code Chat Interface for VS Code
  <sub>★ 1.1k · JavaScript · clone · pushed 2026-09-18 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/andrepimenta/claude-code-chat`</sub>
- **[claude-code.el](https://github.com/stevemolitor/claude-code.el)** — (714 ⭐) - Claude Code Emacs integration
  <sub>★ 746 · Emacs Lisp · Apache-2.0 · source · pushed 2026-04-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/stevemolitor/claude-code.el.git`</sub>
- **[Claude-Autopilot](https://github.com/benbasha/Claude-Autopilot)** — (234 ⭐) - VS Code/Cursor extension for automating Claude Code tasks with intelligent queuing, batch processing, and auto-resume
  <sub>★ 249 · TypeScript · MIT · clone · pushed 2025-08-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/benbasha/Claude-Autopilot.git`</sub>
- **[n8n-nodes-claudecode](https://github.com/holt-web-ai/n8n-nodes-claudecode)** — (96 ⭐) - Bring the power of Claude Code directly into your n8n automation workflows!
  <sub>★ 98 · TypeScript · MIT · source · pushed 2026-05-23 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/holt-web-ai/n8n-nodes-claudecode.git`</sub>

## Tools &amp; Utilities

- **[claude-mem](https://github.com/thedotmack/claude-mem)** — (82.2k ⭐) - A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions
  <sub>★ 94.5k · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-mem`</sub>
- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)** — (64.2k ⭐) - Codebase understanding tool that turns repositories into searchable, explainable knowledge graphs
  <sub>★ 83.7k · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz /path/to/analyzed/project`</sub>
- **[headroom](https://github.com/headroomlabs-ai/headroom)** — (62.8k ⭐) - Compresses tool outputs, logs, files, and retrieval chunks before they reach the language model
  <sub>★ 73.5k · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install --python 3.13 "headroom-ai[all]" # CLI in a self-contained env`</sub>
- **[headroom](https://github.com/headroomlabs-ai/headroom)** — (39.8k ⭐) - Compresses tool outputs, logs, files, and retrieval chunks before they enter an agent context
  <sub>★ 73.5k · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install --python 3.13 "headroom-ai[all]" # CLI in a self-contained env`</sub>
- **[codegraph](https://github.com/colbymchenry/codegraph)** — (54.9k ⭐) - Local code knowledge graph for Claude Code, Codex, Gemini, Cursor, OpenCode, Antigravity, Kiro, and Hermes Agent
  <sub>★ 71.8k · C · MIT · psh · pushed 2026-09-22 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex`</sub>
- **[claude-code-router](https://github.com/musistudio/claude-code-router)** — (35.0k ⭐) - Use Claude Code as the foundation for coding infrastructure, allowing you to decide how to interact with the model while enjoying updates from Anthropic
  <sub>★ 37.4k · TypeScript · MIT · npm · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @musistudio/claude-code-router`</sub>
- **[claude-code-templates](https://github.com/davila7/claude-code-templates)** — (28.0k ⭐) - A CLI tool for configuring and monitoring Claude Code
  <sub>★ 30.9k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-code-templates@latest --agent development-team/frontend-developer --command testing/generate-tests --mcp development/github-integration --yes`</sub>
- **[context-mode](https://github.com/mksglu/context-mode)** — (23.0k ⭐) - MCP server that reduces context usage by sandboxing tool output, indexing session memory, and routing work across coding agents
  <sub>★ 23.9k · TypeScript · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g context-mode`</sub>
- **[claude-context-mode](https://github.com/mksglu/context-mode)** — (17.4k ⭐) - An MCP server that sits between Claude Code and these outputs. 315 KB becomes 5.4 KB. 98% reduction
  <sub>★ 23.9k · TypeScript · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g context-mode`</sub>
- **[SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework)** — (23.3k ⭐) - A configuration framework that enhances Claude Code with specialized commands, cognitive personas, and development methodologies
  <sub>★ 23.9k · Python · MIT · pipx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install superclaude`</sub>
- **[SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)** — (23.3k ⭐) - A configuration framework that enhances Claude Code with specialized commands, cognitive personas, and development methodologies
  <sub>★ 23.9k · Python · MIT · pipx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install superclaude`</sub>
- **[claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)** — (6.8k ⭐) - Claude + Obsidian knowledge companion. A running notetaker that builds and maintains a persistent, compounding wiki vault
  <sub>★ 15.1k · Python · MIT · clone · pushed 2026-09-10 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgriciDaniel/claude-obsidian.git`</sub>
- **[Graft](https://github.com/trailhq/Graft)** — (8.0k ⭐) - Codebase-aware context and code graph tool for Claude Code, Cursor, Codex, Gemini, and other coding agents
  <sub>★ 9k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @nanonets/graft # install the CLI, once`</sub>
- **[Graft](https://github.com/trailhq/Graft)** — (3.8k ⭐) - Codebase-aware developer tool for Claude Code, Cursor, Codex, Gemini, and other coding agents
  <sub>★ 9k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @nanonets/graft # install the CLI, once`</sub>
- **[claude-code-action](https://github.com/anthropics/claude-code-action)** — (8.0k ⭐) - A general-purpose Claude Code action for GitHub PRs and issues that can answer questions and implement code changes
  <sub>★ 8.9k · TypeScript · MIT · gh-action · pushed 2026-09-19</sub>
  <sub>`uses: anthropics/claude-code-action@main # in .github/workflows/*.yml`</sub>
- **[ccpm](https://github.com/automazeio/ccpm)** — (8.2k ⭐) - Project management system for Claude Code using GitHub Issues and Git worktrees for parallel agent execution
  <sub>★ 8.4k · Shell · MIT · clone · pushed 2026-03-18</sub>
  <sub>`git clone https://github.com/automazeio/ccpm.git`</sub>
- **[manifest](https://github.com/mnfst/llm-gateway)** — (7.1k ⭐) - Connects agents and coding harnesses with different model providers through one manifest
  <sub>★ 7.5k · TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/mnfst/manifest.git`</sub>
- **[claude-token-efficient](https://github.com/drona23/claude-token-efficient)** — (5.6k ⭐) - One CLAUDE.md file. Keeps Claude responses terse. Reduces output verbosity on heavy workflows. Drop-in, no code changes
  <sub>★ 6k · Python · MIT · clone · pushed 2026-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/drona23/claude-token-efficient`</sub>
- **[peon-ping](https://github.com/PeonPing/peon-ping)** — (4.8k ⭐) - Warcraft III Peon voice notifications (+ more!) for Claude Code, Codex, IDEs, and any AI agent
  <sub>★ 5k · Shell · MIT · brew · pushed 2026-08-30 · macOS</sub>
  <sub>`brew install PeonPing/tap/peon-ping`</sub>
- **[cipher](https://github.com/campfirein/byterover-cli)** — (4.9k ⭐) - An opensource memory layer specifically designed for coding agents
  <sub>★ 5k · TypeScript · source · pushed 2026-06-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/campfirein/cipher.git`</sub>
- **[skills-manager](https://github.com/xingkongliang/skills-manager)** — (2.3k ⭐) - A lightweight desktop app to manage, sync, and organize AI agent skills across 15+ coding tools
  <sub>★ 4.9k · Rust · MIT · npx · pushed 2026-09-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add xingkongliang/skills-manager`</sub>
- **[obsidian-mind](https://github.com/breferrari/obsidian-mind)** — (4.6k ⭐) - Self-organizing Obsidian vault that gives Claude Code, Codex CLI, and Gemini CLI persistent memory
  <sub>★ 4.7k · TypeScript · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/breferrari/obsidian-mind.git`</sub>
- **[LongMemory](https://github.com/CaviraOSS/LongMemory)** — (4.5k ⭐) - Local persistent memory store for LLM applications, including Claude Desktop, GitHub Copilot, Codex, and Antigravity
  <sub>★ 4.5k · TypeScript · Apache-2.0 · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install --global longmemory`</sub>
- **[Continuous-Claude-v2](https://github.com/parcadei/Continuous-Claude-v3)** — (3.8k ⭐) - Context management for Claude Code. Hooks maintain state via ledgers and handoffs. MCP execution without context pollution. Agent orchestration with isolated context windows
  <sub>★ 3.9k · Python · MIT · clone · pushed 2026-01-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/parcadei/Continuous-Claude-v3.git`</sub>
- **[claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow)** — (3.8k ⭐) - Automated Kiro-style Spec workflow for Claude Code. Transform feature ideas into complete implementations through Requirements → Design → Tasks → Implementation
  <sub>★ 3.9k · TypeScript · MIT · npm · pushed 2025-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @pimzino/claude-code-spec-workflow`</sub>
- **[agent-of-empires](https://github.com/agent-of-empires/agent-of-empires)** — (2.6k ⭐) - Claude Code, OpenCode, Mistral Vibe, Codex CLI, Gemini CLI Coding Agent Terminal Session manager via tmux and git Worktrees
  <sub>★ 3.3k · Rust · MIT · clone · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/agent-of-empires/agent-of-empires`</sub>
- **[crystal](https://github.com/stravu/crystal)** — (3.1k ⭐) - Run multiple Claude Code AI sessions in parallel git worktrees
  <sub>★ 3.1k · TypeScript · MIT · source · pushed 2026-02-26 · macOS</sub>
  <sub>`git clone https://github.com/stravu/crystal.git`</sub>
- **[Observal](https://github.com/Observal/Observal)** — (2.1k ⭐) - A sandboxed artifactory and analytics platform for your AI development stack
  <sub>★ 2.9k · Python · Apache-2.0 · uv · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install observal-cli`</sub>
- **[CCPlugins](https://github.com/brennercruvinel/CCPlugins)** — (2.7k ⭐) - Claude Code Plugins that actually save time. Built by a dev tired of typing please act like a senior engineer in every conversation
  <sub>★ 2.8k · Python · MIT · script · pushed 2026-09-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/brennercruvinel/CCPlugins/main/install.sh | bash`</sub>
- **[skillshare](https://github.com/runkids/skillshare)** — (2.2k ⭐) - Sync skills across all AI CLI tools with one command and simplify team sharing
  <sub>★ 2.7k · Go · MIT · psh · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/runkids/skillshare/main/install.ps1 | iex`</sub>
- **[commands](https://github.com/wshobson/commands)** — (2.5k ⭐) - A collection of production-ready slash commands for Claude Code
  <sub>★ 2.6k · MIT · clone · pushed 2025-10-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/wshobson/commands.git`</sub>
- **[skill-scanner](https://github.com/cisco-ai-defense/skill-scanner)** — (2.2k ⭐) - Security Scanner for Agent Skills
  <sub>★ 2.5k · Python · pip · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`pip install cisco-ai-skill-scanner`</sub>
- **[tweakcc](https://github.com/Piebald-AI/tweakcc)** — (2.2k ⭐) - Command-line tool to customize your Claude Code styling
  <sub>★ 2.5k · TypeScript · MIT · npx · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx tweakcc unpack <output-js-path> [binary-path]`</sub>
- **[claude-island](https://github.com/farouqaldori/vibe-notch)** — (2.4k ⭐) - Claude Code notifications without the context switch
  <sub>★ 2.5k · Swift · Apache-2.0 · source · pushed 2026-04-20 · macOS</sub>
  <sub>`git clone https://github.com/farouqaldori/claude-island.git`</sub>
- **[tdd-guard](https://github.com/nizos/tdd-guard)** — (2.2k ⭐) - Automated TDD enforcement for Claude Code
  <sub>★ 2.3k · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nizos/tdd-guard.git`</sub>
- **[better-harness](https://github.com/QoderAI/better-harness)** — (2.0k ⭐) - A harness engineering platform for analyzing coding-agent workflows, identifying evidence-backed gaps, and defining verifiable improvements
  <sub>★ 2.3k · JavaScript · MIT · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/QoderAI/better-harness.git`</sub>
- **[cc-mirror](https://github.com/numman-ali/cc-mirror)** — (2.2k ⭐) - Create multiple isolated Claude Code variants with custom providers (Z.ai, MiniMax, OpenRouter, LiteLLM)
  <sub>★ 2.3k · TypeScript · MIT · npx · pushed 2026-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cc-mirror quick --provider mirror --name mirror`</sub>
- **[clawgod](https://github.com/0Chencc/clawgod)** — (1.4k ⭐) - Claude Code companion tool for agent sessions, workflows, and local control
  <sub>★ 2k · PowerShell · GPL-3.0 · psh · pushed 2026-09-22 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://github.com/0Chencc/clawgod/releases/latest/download/install.ps1 | iex`</sub>
- **[memmy-agent](https://github.com/MemTensor/memmy-agent)** — (614 ⭐) - A personal AI agent and shared memory hub that gives Claude Code, Codex, OpenClaw, and other agents persistent context under user control
  <sub>★ 2k · TypeScript · MIT · script · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/MemTensor/memmy-agent/main/scripts/install.sh | bash`</sub>
- **[claude-code-prompt-improver](https://github.com/severity1/claude-code-prompt-improver)** — (1.6k ⭐) - Intelligent prompt improver hook for Claude Code. Type vibes, ship precision
  <sub>★ 1.9k · Python · MIT · clone · pushed 2026-06-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/severity1/claude-code-prompt-improver.git`</sub>
- **[claude-code-transcripts](https://github.com/simonw/claude-code-transcripts)** — (1.6k ⭐) - Tools for publishing transcripts for Claude Code sessions
  <sub>★ 1.7k · Python · Apache-2.0 · uv · pushed 2026-02-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install claude-code-transcripts`</sub>
- **[claude-code-settings](https://github.com/feiskyer/claude-code-settings)** — (1.6k ⭐) - Claude Code settings and commands for vibe coding
  <sub>★ 1.7k · Python · MIT · npx · pushed 2026-08-13 · WSL2 · macOS? · Linux</sub>
  <sub>`npx -y skills add -l feiskyer/claude-code-settings`</sub>
- **[cc-sessions](https://github.com/GWUDCAP/cc-sessions)** — (1.5k ⭐) - An opinionated extension set for Claude Code (hooks, subagents, commands, task/git management infrastructure)
  <sub>★ 1.6k · JavaScript · MIT · npx · pushed 2025-12-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cc-sessions`</sub>
- **[claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)** — (1.5k ⭐) - Real-time monitoring for Claude Code agents through simple hook event tracking
  <sub>★ 1.5k · Python · source · pushed 2026-02-08 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/disler/claude-code-hooks-multi-agent-observability.git`</sub>
- **[claude-canvas](https://github.com/dvdsgl/claude-canvas)** — (1.5k ⭐) - A TUI toolkit that gives Claude Code its own display
  <sub>★ 1.5k · TypeScript · MIT · source · pushed 2026-01-08 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/dvdsgl/claude-canvas.git`</sub>
- **[engram](https://github.com/nagisanzenin/engram)** — (400 ⭐) - Learning engine for Claude Code and Codex that records patterns from previous sessions and turns them into reusable guidance
  <sub>★ 1.4k · Python · MIT · source · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nagisanzenin/engram.git`</sub>
- **[ccundo](https://github.com/RonitSachdev/ccundo)** — (1.4k ⭐) - Integrates seamlessly with Claude Code to provide granular undo functionality by reading directly from Claude Code's session files
  <sub>★ 1.4k · JavaScript · npm · pushed 2025-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ccundo`</sub>
- **[Continuous Claude](https://github.com/AnandChowdhary/continuous-claude)** — (1.4k ⭐) - Run Claude Code in a continuous loop, autonomously creating PRs, waiting for checks, and merging
  <sub>★ 1.4k · Shell · MIT · psh · pushed 2026-08-24 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/AnandChowdhary/continuous-claude/main/install.ps1 | iex`</sub>
- **[Claude-Command-Suite](https://github.com/qdhenry/Claude-Command-Suite)** — (1.3k ⭐) - Professional slash commands for Claude Code that provide structured workflows for software development tasks, including code review and feature implementation
  <sub>★ 1.3k · Shell · clone · pushed 2026-03-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/qdhenry/Claude-Command-Suite.git`</sub>
- **[claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler)** — (1.2k ⭐) - Give Claude Code a memory that evolves with your codebase
  <sub>★ 1.3k · Python · source · pushed 2026-04-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/coleam00/claude-memory-compiler.git`</sub>
- **[Claude-Code-Remote](https://github.com/JessyTsui/Claude-Code-Remote)** — (1.3k ⭐) - Control Claude Code remotely via email. Start tasks locally, receive notifications when Claude completes them, and send new commands by simply replying to emails
  <sub>★ 1.3k · JavaScript · MIT · clone · pushed 2025-12-06 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/JessyTsui/Claude-Code-Remote.git`</sub>
- **[ccmanager](https://github.com/kbwo/ccmanager)** — (1.1k ⭐) - Claude Code / Gemini CLI / Codex CLI Session Manager
  <sub>★ 1.2k · TypeScript · MIT · npm · pushed 2026-09-13 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g ccmanager`</sub>
- **[claude-code-log](https://github.com/daaain/claude-code-log)** — (1.1k ⭐) - A Python CLI tool that converts Claude Code transcript JSONL files into readable HTML format
  <sub>★ 1.2k · Python · MIT · uv · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx claude-code-log@latest --open-browser`</sub>
- **[pireel](https://github.com/pireel/pireel)** — (915 ⭐) - A browser-based, backend-free video editor for talking-head footage, with captions, graphics, themes, timeline editing, export, and MCP control
  <sub>★ 1.2k · TypeScript · AGPL-3.0 · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add pireel/pireel-agent`</sub>
- **[claude-sessions](https://github.com/iannuttall/claude-sessions)** — (1.2k ⭐) - Custom slash commands for Claude Code that provide comprehensive development session tracking and documentation
  <sub>★ 1.2k · MIT · clone · pushed 2025-06-16</sub>
  <sub>`git clone git@github.com:iannuttall/claude-sessions.git`</sub>
- **[OpenContext](https://github.com/0xranx/OpenContext)** — (592 ⭐) - Personal context store for Codex, Claude, OpenCode, and other agents, with skills, tools, search, and a desktop GUI
  <sub>★ 1.2k · JavaScript · MIT · clone · pushed 2026-06-16 · Win · macOS</sub>
  <sub>`git clone https://github.com/0xranx/OpenContext.git`</sub>
- **[claude-powerline](https://github.com/Owloops/claude-powerline)** — (1.1k ⭐) - Beautiful vim-style powerline statusline for Claude Code
  <sub>★ 1.2k · TypeScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/Owloops/claude-powerline.git`</sub>
- **[claudebox](https://github.com/RchGrav/claudebox)** — (1.1k ⭐) - A Claude Code Docker Development Environment for running Claude AI's coding assistant in a fully containerized, reproducible environment
  <sub>★ 1.2k · Shell · MIT · clone · pushed 2026-09-17 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/RchGrav/claudebox.git`</sub>
- **[vibecode-pro-max-kit](https://github.com/withkynam/vibecode-pro-max-kit)** — (951 ⭐) - Spec-driven coding harness that keeps project memory and implementation context organized for AI agents
  <sub>★ 1.1k · JavaScript · MIT · script · pushed 2026-06-21 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/withkynam/vibecode-pro-max-kit/main/install.sh | bash`</sub>
- **[ctx](https://github.com/ctxrs/ctx)** — (729 ⭐) - Local search for coding-agent history across Claude Code, Codex, Cursor, and related tools
  <sub>★ 1.1k · Rust · Apache-2.0 · psh · pushed 2026-09-22 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://ctx.rs/install.ps1 | iex`</sub>
- **[backpass](https://github.com/kunchenguid/backpass)** — (597 ⭐) - Improve AGENTS.md or CLAUDE.md from evidence in local agent session transcripts, with reviewable, evidence-gated edits
  <sub>★ 1.1k · JavaScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g backpass`</sub>
- **[medusa](https://github.com/Pantheon-Security/medusa)** — (643 ⭐) - AI-first security scanner for repositories, secrets, hooks, permissions, and agent skills
  <sub>★ 991 · Python · AGPL-3.0 · pip · pushed 2026-08-10 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install medusa-security`</sub>
- **[claude-code-base-action](https://github.com/anthropics/claude-code-base-action)** — (874 ⭐) - A Claude Code base action
  <sub>★ 987 · TypeScript · MIT · gh-action · pushed 2026-09-19</sub>
  <sub>`uses: anthropics/claude-code-base-action@main # in .github/workflows/*.yml`</sub>
- **[asm](https://github.com/luongnv89/asm)** — (637 ⭐) - Universal skill manager for AI coding agents
  <sub>★ 939 · TypeScript · MIT · script · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/luongnv89/asm/main/install.sh | bash`</sub>
- **[ai-data-extractor](https://github.com/kruzovic7/ai-data-extractor)** — (814 ⭐) - Local Python extractor for chat histories from Claude Code, Cursor, Windsurf, Aider, Cline/Roo Code, and other coding assistants
  <sub>★ 842 · Python · MIT · source · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/kruzovic7/ai-data-extractor.git`</sub>
- **[claude-replay](https://github.com/es617/claude-replay)** — (720 ⭐) - Convert AI coding agent sessions (Claude Code, Cursor, Codex, Gemini, OpenCode) into self-contained, embeddable HTML replays
  <sub>★ 836 · JavaScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g claude-replay`</sub>
- **[claude-on-rails](https://github.com/obie/claude-on-rails)** — (806 ⭐) - A development framework for Ruby on Rails developers using Claude Code, inspired by SuperClaude
  <sub>★ 815 · Ruby · MIT · source · pushed 2025-09-26</sub>
  <sub>`git clone https://github.com/obie/claude-on-rails.git`</sub>
- **[context-infrastructure](https://github.com/grapeot/context-infrastructure)** — (623 ⭐) - Context and memory system for AI coding agents with persistent memory, personal rules, skills, and scheduled observations
  <sub>★ 767 · Python · clone · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/grapeot/context-infrastructure`</sub>
- **[storybloq](https://github.com/Storybloq/storybloq)** — (627 ⭐) - Cross-session context tool for Claude Code with a CLI, MCP server, and /story skill for tickets, handovers, and roadmaps
  <sub>★ 755 · TypeScript · npm · pushed 2026-09-22 · macOS</sub>
  <sub>`npm install -g @storybloq/storybloq@latest`</sub>
- **[recall](https://github.com/raiyanyahya/recall)** — (448 ⭐) - Offline durable memory for Claude Code that reduces repeated project explanation across sessions
  <sub>★ 753 · Python · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/raiyanyahya/recall`</sub>
- **[looper](https://github.com/ksimback/looper)** — (440 ⭐) - Visual planning tool for review-gated Claude Code agent loops before they run
  <sub>★ 712 · Python · MIT · psh · pushed 2026-08-09 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/ksimback/looper/main/install.ps1 | iex`</sub>
- **[ccmate](https://github.com/djyde/ccmate)** — (624 ⭐) - Configure your Claude Code without pain
  <sub>★ 627 · TypeScript · brew · pushed 2026-05-12 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask ccmate`</sub>
- **[claude-code-configs](https://github.com/Matt-Dionis/claude-code-configs)** — (623 ⭐) - A comprehensive collection of production-grade Claude Code configurations, specialized agents, and automation workflows for optimizing AI-assisted development
  <sub>★ 623 · TypeScript · MIT · clone · pushed 2025-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Matt-Dionis/claude-code-configs.git`</sub>
- **[skillhub-desktop](https://github.com/skillhub-club/skillhub-desktop)** — (590 ⭐) - Desktop app for managing agent skills in one place
  <sub>★ 600 · TypeScript · source · pushed 2026-03-07 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/skillhub-club/skillhub-desktop.git`</sub>
- **[claude-simone](https://github.com/Helmi/claude-simone)** — (555 ⭐) - A project management framework for AI-assisted development with Claude Code
  <sub>★ 556 · TypeScript · MIT · source · pushed 2025-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Helmi/claude-simone.git`</sub>
- **[smart-ralph](https://github.com/tzachbon/smart-ralph)** — (348 ⭐) - Claude Code plugin for spec-driven development with smart compaction and Ralph-style autonomous loops
  <sub>★ 549 · Shell · MIT · source · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/tzachbon/smart-ralph.git`</sub>
- **[async-code](https://github.com/ObservedObserver/async-code)** — (534 ⭐) - Use Claude Code or CodeX CLI to perform multiple tasks in parallel with a Codex-style UI, functioning as a personal codex or cursor-background agent
  <sub>★ 535 · TypeScript · Apache-2.0 · source · pushed 2025-11-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ObservedObserver/async-code.git`</sub>
- **[claude-code-hooks](https://github.com/karanb192/claude-code-hooks)** — (421 ⭐) - A growing collection of useful Claude Code hooks. Copy, paste, customize
  <sub>★ 524 · JavaScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/karanb192/claude-code-hooks.git`</sub>
- **[claude-commands](https://github.com/badlogic/claude-commands)** — (506 ⭐) - Global Claude Code commands and workflows
  <sub>★ 522 · source · pushed 2025-08-11</sub>
  <sub>`git clone https://github.com/badlogic/claude-commands.git`</sub>
- **[agent-manager](https://github.com/YoanWai/agent-manager)** — (421 ⭐) - Terminal UI for managing AI coding agents with live status, quick prompts, worktrees, and diff review
  <sub>★ 492 · Go · Apache-2.0 · brew · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`brew install agent-manager`</sub>
- **[claude-hub](https://github.com/claude-did-this/claude-hub)** — (481 ⭐) - Deploy Claude Code as a fully autonomous GitHub bot
  <sub>★ 486 · TypeScript · clone · pushed 2025-10-27 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/claude-did-this/claude-hub.git`</sub>
- **[claude-cognitive](https://github.com/GMaN1911/claude-cognitive)** — (449 ⭐) - Working memory for Claude Code - persistent context and multi-instance coordination
  <sub>★ 452 · Python · MIT · clone · pushed 2026-01-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GMaN1911/claude-cognitive.git`</sub>
- **[greplica](https://github.com/Autoloops/greplica)** — (418 ⭐) - Persistent engineering memory that indexes repository structure, code, and session transcripts for Claude Code and Codex
  <sub>★ 437 · TypeScript · MIT · npm · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g greplica@latest`</sub>
- **[Claude Code Tamagotchi](https://github.com/Ido-Levi/claude-code-tamagotchi)** — (425 ⭐) - A digital friend that lives in your Claude Code statusline and keeps you company while you build cool stuff
  <sub>★ 435 · TypeScript · MIT · npm · pushed 2025-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-code-tamagotchi`</sub>
- **[ClaudeForge](https://github.com/alirezarezvani/ClaudeForge)** — (388 ⭐) - A CLAUDE.md Generator and Maintenance tool for for Claude Code to create high-quality CLAUDE.md instruction files — aligned with Anthropic's best practices for Claude Code
  <sub>★ 428 · Python · MIT · script · pushed 2026-05-19 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/alirezarezvani/ClaudeForge/main/install.sh | bash`</sub>
- **[ClaudeUsageBar](https://github.com/Artzainnn/ClaudeUsageBar)** — (211 ⭐) - Track your Claude.ai usage right from your Mac menu bar
  <sub>★ 333 · HTML · MIT · source · pushed 2026-09-14 · macOS</sub>
  <sub>`git clone https://github.com/Artzainnn/ClaudeUsageBar.git`</sub>
- **[SuperClaude](https://github.com/gwendall/superclaude)** — (325 ⭐) - Supercharge your GitHub workflow with Claude AI
  <sub>★ 326 · Shell · MIT · npm · pushed 2025-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g superclaude`</sub>
- **[claude-code-sandbox](https://github.com/textcortex/claude-code-sandbox)** — (318 ⭐) - Run Claude Code safely in local Docker containers without having to approve every permission
  <sub>★ 322 · TypeScript · npm · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @textcortex/claude-code-sandbox`</sub>
- **[claude-cmd](https://github.com/kiliczsh/claude-cmd)** — (305 ⭐) - Claude Code Commands Manager
  <sub>★ 312 · TypeScript · MIT · npm · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-cmd@latest`</sub>
- **[claude-blocker](https://github.com/T3-Content/claude-blocker)** — (294 ⭐) - Block distracting websites unless Claude Code is actively running inference
  <sub>★ 296 · TypeScript · MIT · npx · pushed 2026-01-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-blocker --setup`</sub>
- **[laravel-claude-code-setup](https://github.com/laraben/laravel-claude-code-setup)** — (288 ⭐) - One-command setup for AI-powered Laravel development with Claude Code and MCP servers
  <sub>★ 288 · Shell · MIT · script · pushed 2026-03-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/laraben/laravel-claude-code-setup/main/install.sh | bash`</sub>
- **[claude-modular](https://github.com/oxygen-fragment/claude-modular)** — (284 ⭐) - Production-ready modular Claude Code framework with 30+ commands, token optimization, and MCP server integration
  <sub>★ 282 · MIT · clone · pushed 2025-07-16</sub>
  <sub>`git clone https://github.com/your-username/claude-modular.git`</sub>
- **[claude-code-studio](https://github.com/arnaldo-delisio/claude-code-studio)** — (273 ⭐) - Transform Claude Code into a complete development studio with 40+ specialized AI agents, MCP integrations, and enterprise-grade workflows
  <sub>★ 276 · JavaScript · MIT · clone · pushed 2025-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/your-username/claude-code-studio.git`</sub>
- **[claude-setup](https://github.com/AizenvoltPrime/claude-setup)** — (271 ⭐) - A comprehensive configuration setup for Claude Code with Model Context Protocol (MCP) servers, custom commands, and automated workflows
  <sub>★ 268 · Python · source · pushed 2026-01-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/AizenvoltPrime/claude-setup.git`</sub>
- **[claude-config-editor](https://github.com/gagarinyury/claude-config-editor)** — (253 ⭐) - A lightweight web tool that helps you clean and optimize your Claude Code/Desktop config files (.claude.json)
  <sub>★ 261 · HTML · MIT · clone · pushed 2025-10-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/gagarinyury/claude-config-editor.git`</sub>
- **[claude-code-containers](https://github.com/ghostwriternr/claude-code-containers)** — (244 ⭐) - Use Claude Code on Cloudflare to solve GitHub issues
  <sub>★ 244 · TypeScript · MIT · source · pushed 2025-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ghostwriternr/claude-code-containers.git`</sub>
- **[claude-context-local](https://github.com/FarhanAliRaza/claude-context-local)** — (232 ⭐) - Code search MCP for Claude Code. Make entire codebase the context for any coding agent. Embeddings are created and stored locally. No API cost
  <sub>★ 237 · Python · script · pushed 2025-11-13 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/FarhanAliRaza/claude-context-local/main/scripts/install.sh | bash`</sub>
- **[win-claude-code](https://github.com/somersby10ml/win-claude-code)** — (231 ⭐) - Claude Code for Windows: No WSL. No Docker. Just code
  <sub>★ 228 · JavaScript · MIT · npx · pushed 2025-07-11 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx win-claude-code@latest`</sub>
- **[claude-self-reflect](https://github.com/ramakay/claude-self-reflect)** — (216 ⭐) - Claude forgets everything. This fixes that
  <sub>★ 226 · Rust · MIT · npm · pushed 2026-09-21 · macOS</sub>
  <sub>`npm install -g claude-self-reflect`</sub>
- **[claude-thermos](https://github.com/izeigerman/claude-thermos)** — (171 ⭐) - Keeps a Claude session warm between tasks
  <sub>★ 226 · Python · MIT · uv · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx claude-thermos # instead of: claude`</sub>
- **[cctrace](https://github.com/jimmc414/cctrace)** — (193 ⭐) - Export Claude Code chat sessions into markdown and XML
  <sub>★ 200 · Python · MIT · clone · pushed 2026-01-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jimmc414/cctrace.git`</sub>
- **[recall](https://github.com/zippoxer/recall)** — (187 ⭐) - Full-text search and resume for Claude/Codex conversations
  <sub>★ 198 · Rust · MIT · winget · pushed 2026-01-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install zippoxer.recall`</sub>
- **[Grov](https://github.com/TonyStef/Grov)** — (194 ⭐) - Captures private AI-session context, shares it with a team memory, and injects relevant memories into later sessions
  <sub>★ 192 · TypeScript · Apache-2.0 · npm · pushed 2026-01-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g grov # Install`</sub>
- **[claude-agent-server](https://github.com/forayconsulting/gemini_cli_skill)** — (187 ⭐) - A Claude Code skill enabling Claude to use Gemini 3 Pro via Gemini CLI
  <sub>★ 190 · clone · pushed 2025-11-19</sub>
  <sub>`git clone https://github.com/forayconsulting/gemini_cli_skill.git`</sub>
- **[meridian](https://github.com/markmdev/meridian)** — (177 ⭐) - Zero-config Claude Code setup with enforced task scaffolding, structured memory, persistent context after compaction, plug-in code standards, optional TDD mode, and zero behavior changes for developers
  <sub>★ 185 · Python · script · pushed 2026-03-11 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/markmdev/meridian/main/install.sh | bash`</sub>
- **[claude-code-boost](https://github.com/yifanzz/claude-code-boost)** — (165 ⭐) - Hook utilities for Claude Code with intelligent auto-approval
  <sub>★ 166 · TypeScript · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g claude-code-boost`</sub>
- **[claude-code-auto-memory](https://github.com/severity1/claude-code-auto-memory)** — (149 ⭐) - Claude Code plugin that automatically maintains CLAUDE.md files
  <sub>★ 158 · Python · MIT · source · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/severity1/claude-code-auto-memory.git`</sub>
- **[context-forge](https://github.com/webdevtodayjason/context-forge)** — (142 ⭐) - CLI tool that scaffolds context engineering documentation for Claude Code projects
  <sub>★ 148 · TypeScript · MIT · npm · pushed 2026-05-11 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g context-forge`</sub>
- **[spec-based-claude-code](https://github.com/papaoloba/spec-based-claude-code)** — (130 ⭐) - Implementation of a Spec-Driven Development workflow in Claude Code using custom slash commands
  <sub>★ 138 · TypeScript · source · pushed 2025-07-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/papaoloba/spec-based-claude-code.git`</sub>
- **[claude-code-personal-assistant](https://github.com/c0dezli/claude-code-personal-assistant)** — (133 ⭐) - AI personal assistant setup for Claude Code
  <sub>★ 135 · Python · MIT · source · pushed 2025-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/c0dezli/claude-code-personal-assistant.git`</sub>
- **[rins_hooks](https://github.com/rinadelph/Rapala)** — (107 ⭐) - Universal Claude Code hooks collection with cross-platform installer
  <sub>★ 108 · JavaScript · npm · pushed 2025-08-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g rins_hooks`</sub>
- **[claude-select](https://github.com/LLMpsycho/claude-select)** — (100 ⭐) - A unified launcher for Claude Code that lets you interactively choose which LLM backend to use
  <sub>★ 100 · Shell · source · pushed 2025-12-12 · macOS?</sub>
  <sub>`git clone https://github.com/aeitroc/claude-select.git`</sub>
- **[claude-code-container](https://github.com/tintinweb/claude-code-container)** — (92 ⭐) - A Docker container for running Claude Code in "dangerously skip permissions" mode
  <sub>★ 97 · Shell · source · pushed 2025-08-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/tintinweb/claude-code-container.git`</sub>
- **[run-claude-docker](https://github.com/icanhasjonas/run-claude-docker)** — (84 ⭐) - Run claude code in somewhat safe and isolated yolo mode
  <sub>★ 84 · Shell · MIT · docker · pushed 2025-08-14 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -v $(pwd):/workspace claude-code:latest sudo chown -R claude:claude /workspace`</sub>
- **[claude-prune](https://github.com/DannyAziz/claude-prune)** — (85 ⭐) - A fast CLI tool for pruning Claude Code sessions
  <sub>★ 83 · TypeScript · MIT · npm · pushed 2025-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-prune`</sub>
- **[claude-code-thinking-patch](https://github.com/aleks-apostle/claude-code-patches)** — (64 ⭐) - Make Claude Code's thinking blocks visible by default without pressing ctrl+o
  <sub>★ 67 · JavaScript · source · pushed 2025-12-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/aleks-apostle/claude-code-thinking-patch.git`</sub>
- **[flashbacker](https://github.com/agentsea/flashbacker)** — (57 ⭐) - Claude Code state management with session continuity and AI personas, subagents and agent discussion
  <sub>★ 57 · TypeScript · MIT · npm · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g flashbacker`</sub>
- **[ccguard](https://github.com/pomterre/ccguard)** — (47 ⭐) - Automated enforcement of net-negative LOC, complexity constraints, and quality standards for Claude code
  <sub>★ 44 · TypeScript · MIT · npm · pushed 2025-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ccguard`</sub>
- **[claude-code-specs-generator](https://github.com/kellemar/claude-code-specs-generator)** — (42 ⭐) - A documentation and context management system for AI-assisted development, inspired by Amazon's Kiro IDE
  <sub>★ 42 · source · pushed 2025-07-27</sub>
  <sub>`git clone https://github.com/kellemar/claude-code-specs-generator.git`</sub>
- **[claude-code-voice](https://github.com/mckaywrigley/claude-code-voice)** — (41 ⭐) - Hands-free voice control for Claude Code on macOS
  <sub>★ 41 · Python · source · pushed 2025-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mckaywrigley/claude-code-voice.git`</sub>
- **[claudecode-macmenu](https://github.com/PiXeL16/claudecode-macmenu)** — (36 ⭐) - A Mac Menu for Claude Code that notifies when Claude is done and shows insights
  <sub>★ 36 · TypeScript · brew · pushed 2025-11-07 · macOS</sub>
  <sub>`brew install --cask claudecode-macmenu`</sub>
- **[ccheckpoints](https://github.com/p32929/ccheckpoints)** — (32 ⭐) - A checkpoint system for Claude Code CLI that automatically tracks your coding sessions
  <sub>★ 34 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ccheckpoints`</sub>
- **[cc-monitor-rs](https://github.com/ZhangHanDong/cc-monitor-rs)** — (24 ⭐) - Real-time Claude Code usage monitor with native UI built using Rust and Makepad
  <sub>★ 24 · Rust · Apache-2.0 · clone · pushed 2025-07-29 · macOS</sub>
  <sub>`git clone https://github.com/zhanghandong/cc-monitor-rs.git`</sub>
- **[claude-code-test-runner](https://github.com/firstloophq-archive/claude-code-test-runner)** — (22 ⭐) - An automated E2E natural language test runner built on Claude Code
  <sub>★ 24 · TypeScript · source · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/firstloophq/claude-code-test-runner.git`</sub>
- **[cc-monitor-worker](https://github.com/cometkim/cc-monitor-worker)** — (21 ⭐) - Claude Code monitoring with Cloudflare Workers &amp; Workers Analytics Engine
  <sub>★ 22 · TypeScript · MIT · source · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cometkim/cc-monitor-worker.git`</sub>
- **[shotgun-alpha](https://github.com/shotgun-sh/shotgun-alpha)** — (3 ⭐) - Codebase-aware spec engine for Cursor, Claude Code &amp; Lovable
  <sub>★ 3 · MIT · source · pushed 2025-10-07</sub>
  <sub>`git clone https://github.com/shotgun-sh/shotgun-alpha.git`</sub>
- **[ai-data-extractor](https://github.com/bawadou/ai-data-extractor)** — (541 ⭐) - Local extractor that exports chat histories from Claude Code, Codex, Cursor, Windsurf, Aider, Cline, and other coding assistants to normalized JSONL
  <sub>unavailable</sub>
- **[conductor](https://conductor.build/)** — (0 ⭐) - Run a bunch of Claude Codes in parallel
  <sub>website</sub>
  <sub>`https://conductor.build/`</sub>

## Clients &amp; GUIs

- **[cc-switch](https://github.com/farion1231/cc-switch)** — (132.1k ⭐) - Cross-platform desktop assistant for Claude Code, Codex, OpenCode, OpenClaw, Grok Build, and Hermes Agent
  <sub>★ 134.1k · Rust · MIT · brew · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask cc-switch`</sub>
- **[vibe-kanban](https://github.com/BloopAI/vibe-kanban)** — (27.0k ⭐) - Get 10X more out of Claude Code, Gemini CLI, Codex, Amp and other coding agents
  <sub>★ 28.2k · Rust · Apache-2.0 · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibe-kanban`</sub>
- **[happy](https://github.com/slopus/happy)** — (21.9k ⭐) - Mobile and Web client for Claude Code, with realtime voice, encryption and fully featured
  <sub>★ 23.9k · TypeScript · MIT · npm · pushed 2026-09-22 · macOS</sub>
  <sub>`npm install -g happy`</sub>
- **[t3code](https://github.com/pingdotgg/t3code)** — (12.6k ⭐) - A minimal web GUI for coding agents
  <sub>★ 23.3k · TypeScript · MIT · winget · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install T3Tools.T3Code`</sub>
- **[claudia](https://github.com/winfunc/opcode)** — (22.1k ⭐) - A powerful GUI app and Toolkit for Claude Code - Create custom agents, manage interactive Claude Code sessions, run secure background agents, and more
  <sub>★ 22.4k · TypeScript · AGPL-3.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/getAsterisk/opcode.git`</sub>
- **[cc-haha](https://github.com/NanmiCoder/cc-haha)** — (14.2k ⭐) - Local-first cross-platform desktop workspace for Claude Code and other agents, with multi-agent sessions, Git worktrees, code diffs, and a skill marketplace
  <sub>★ 14.7k · TypeScript · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/NanmiCoder/cc-haha.git`</sub>
- **[claudecodeui](https://github.com/siteboon/claudecodeui)** — (11.9k ⭐) - A desktop and mobile UI for Claude Code, Anthropic's official CLI for AI-assisted coding
  <sub>★ 13.8k · TypeScript · AGPL-3.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @cloudcli-ai/cloudcli`</sub>
- **[CodePilot](https://github.com/op7418/CodePilot)** — (6.0k ⭐) - A native desktop GUI for Claude Code — chat, code, and manage projects visually
  <sub>★ 6.5k · TypeScript · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/op7418/CodePilot.git`</sub>
- **[clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)** — (6.2k ⭐) - Pixel desktop pet that reacts to Claude Code, Codex, Cursor, and other AI coding agents as they work
  <sub>★ 6.3k · JavaScript · AGPL-3.0 · brew · pushed 2026-09-21 · Win · WSL2 · macOS · Linux?</sub>
  <sub>`brew install --cask clawd-on-desk`</sub>
- **[1code](https://github.com/21st-dev/1code)** — (5.6k ⭐) - Best UI for Claude Code with local and remote agent execution
  <sub>★ 5.6k · TypeScript · Apache-2.0 · source · pushed 2026-03-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/21st-dev/1code.git`</sub>
- **[hapi](https://github.com/tiann/hapi)** — (5.1k ⭐) - Mobile app for Codex, Claude Code, Pi, OpenCode, Kimi Code, and other coding agents
  <sub>★ 5.1k · TypeScript · AGPL-3.0 · npx · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @twsxtd/hapi hub --relay # start hub with E2E encrypted relay`</sub>
- **[companion](https://github.com/The-Vibe-Company/companion)** — (2.4k ⭐) - Open-source Claude Code / Codex Web UI
  <sub>★ 2.4k · TypeScript · MIT · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm --env-file .env.production companions.build migrate`</sub>
- **[mindwalk](https://github.com/cosmtrek/mindwalk)** — (871 ⭐) - A visualization tool that replays coding-agent sessions on a 3D map of your codebase
  <sub>★ 1.4k · Go · MIT · script · pushed 2026-08-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/cosmtrek/mindwalk/master/scripts/install.sh | sh`</sub>
- **[claude-code-viewer](https://github.com/d-kimuson/claude-code-viewer)** — (1.2k ⭐) - A full-featured web-based Claude Code client that provides complete interactive functionality for managing Claude Code projects
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-08-18 · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @kimuson/claude-code-viewer`</sub>
- **[Sniffly](https://github.com/chiphuyen/sniffly)** — (1.2k ⭐) - Claude Code dashboard with usage stats, error analysis, and sharable feature
  <sub>★ 1.3k · Python · MIT · uv · pushed 2025-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx sniffly@latest init`</sub>
- **[clui-cc](https://github.com/lcoutodemos/clui-cc)** — (1.2k ⭐) - A lightweight, transparent desktop overlay for Claude Code on macOS. Clui CC wraps the Claude Code CLI in a floating pill interface with multi-tab sessions, a permission approval UI, voice input, and a skills marketplace
  <sub>★ 1.2k · TypeScript · MIT · clone · pushed 2026-03-26 · macOS</sub>
  <sub>`git clone https://github.com/lcoutodemos/clui-cc.git`</sub>
- **[cui](https://github.com/wbopan/cui)** — (1.2k ⭐) - A web UI for Claude Code agents
  <sub>★ 1.1k · TypeScript · Apache-2.0 · source · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BMPixel/cui.git`</sub>
- **[codexia](https://github.com/milisp/codexia)** — (737 ⭐) - Lightweight agent workstation for Codex CLI and Claude Code with scheduling, worktree control, remote control, and skills management
  <sub>★ 918 · TypeScript · MIT · scoop · pushed 2026-09-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add milisp https://github.com/milisp/scoop-bucket scoop install codexia`</sub>
- **[claude-run](https://github.com/nilbuild/claude-run)** — (604 ⭐) - A beautiful web UI for browsing Claude Code conversation history
  <sub>★ 671 · TypeScript · MIT · npm · pushed 2026-02-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-run`</sub>
- **[Claude-code-ChatInWindows](https://github.com/LKbaba/Claude-code-ChatInWindows)** — (217 ⭐) - A Native UI for Windows That Makes Claude Code Instantly Better!
  <sub>★ 223 · TypeScript · MIT · clone · pushed 2026-08-15 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LKbaba/Claude-code-ChatInWindows.git`</sub>
- **[claude-code-costs](https://github.com/philipp-spiess/claude-code-costs)** — (193 ⭐) - Analyze your Claude Code conversation costs with interactive visualizations
  <sub>★ 204 · JavaScript · npx · pushed 2025-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-code-costs`</sub>
- **[claude-quest](https://github.com/Michaelliv/claude-quest)** — (187 ⭐) - An RPG-style viewer that shows Claude Code sessions with pixel-art reactions to tool use
  <sub>★ 196 · Go · npm · pushed 2026-04-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g claude-quest`</sub>
- **[Claudiatron](https://github.com/Haleclipse/Claudiatron)** — (160 ⭐) - A Powerful Claude Code GUI Desktop Application
  <sub>★ 159 · TypeScript · AGPL-3.0 · clone · pushed 2025-08-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Haleclipse/Claudiatron.git`</sub>
- **[Claude-Code-Web-GUI](https://github.com/binggg/Claude-Code-Web-GUI)** — (72 ⭐) - Browse, view and share your Claude Code sessions - runs entirely in browser, no server required!
  <sub>★ 73 · JavaScript · MIT · clone · pushed 2025-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/binggg/Claude-Code-Web-GUI.git`</sub>
- **[ccmate-release](https://github.com/djyde/ccmate-release)** — (56 ⭐) - A GUI for Claude Code
  <sub>★ 56 · source · pushed 2026-05-13 · Win? · macOS</sub>
  <sub>`git clone https://github.com/djyde/ccmate-release.git`</sub>
- **[Claude in a Box](https://github.com/juancgarza/claude-in-a-box)** — (51 ⭐) - A ChatGPT Canvas-style interface for Claude Code running in E2B sandboxes
  <sub>★ 51 · TypeScript · MIT · clone · pushed 2025-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/claude-in-a-box.git`</sub>
- **[claude-code-webui](https://github.com/DevAgentForge/claude-code-webui)** — (149 ⭐) - A web-based Claude Code that runs on desktop, mobile phones, and iPads
  <sub>unavailable</sub>

## Infrastructure &amp; Proxies

- **[CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)** — (51.2k ⭐) - API service that wraps Antigravity, Codex, Claude Code, and Grok Build behind OpenAI-, Gemini-, Claude-, and Codex-compatible endpoints
  <sub>★ 52.8k · Go · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/router-for-me/CLIProxyAPI.git`</sub>
- **[9router](https://github.com/decolua/9router)** — (23.7k ⭐) - Routes Claude Code, Codex, Cursor, Cline, and other coding agents to dozens of model providers with automatic fallback
  <sub>★ 29.6k · JavaScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g 9router`</sub>
- **[opencodex](https://github.com/lidge-jun/opencodex)** — (8.5k ⭐) - A local provider proxy and dashboard that routes Codex CLI, the Codex app, SDKs, and Claude Code to multiple LLM providers
  <sub>★ 15.9k · TypeScript · MIT · npm · pushed 2026-09-22 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npm install -g @bitkyc08/opencodex`</sub>
- **[cc-connect](https://github.com/chenhg5/cc-connect)** — (15.5k ⭐) - Bridge for connecting local AI coding agents to Feishu/Lark, DingTalk, Slack, Telegram, Discord, LINE, WeChat Work, and other messaging platforms
  <sub>★ 15.6k · Go · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g cc-connect`</sub>
- **[zen-mcp-server](https://github.com/BeehiveInnovations/pal-mcp-server)** — (11.6k ⭐) - The power of Claude Code + Gemini / OpenAI / Grok / OpenRouter / Ollama / Custom Model working as one
  <sub>★ 11.8k · Python · clone · pushed 2025-12-15 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BeehiveInnovations/pal-mcp-server.git`</sub>
- **[open-connector](https://github.com/oomol-lab/open-connector)** — (913 ⭐) - Auth gateway that connects SaaS APIs to AI agents through SDK, CLI, MCP, HTTP, and OpenAPI access
  <sub>★ 5.9k · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/oomol-lab/open-connector.git`</sub>
- **[copilot-api](https://github.com/ericc-ch/copilot-api)** — (4.0k ⭐) - Turns GitHub Copilot into an OpenAI/Anthropic API compatible server, usable with Claude Code
  <sub>★ 4.1k · TypeScript · MIT · npx · pushed 2025-11-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx copilot-api@latest start`</sub>
- **[claude-code-proxy](https://github.com/1rgs/claude-code-proxy)** — (3.6k ⭐) - Run Claude Code on OpenAI models
  <sub>★ 3.7k · Python · docker · pushed 2026-06-23 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --env-file .env -p 8082:8082 ghcr.io/1rgs/claude-code-proxy:latest`</sub>
- **[claude-code-proxy](https://github.com/fuergaosi233/claude-code-proxy)** — (2.7k ⭐) - A Claude Code to OpenAI API Proxy
  <sub>★ 2.8k · Python · MIT · source · pushed 2026-03-12 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/fuergaosi233/claude-code-proxy.git`</sub>
- **[kimi-cc](https://github.com/LLM-Red-Team/kimi-cc)** — (1.7k ⭐) - Use Kimi's latest model (kimi-k2-0711-preview) to drive Claude Code
  <sub>★ 1.7k · Shell · source · pushed 2025-07-15</sub>
  <sub>`git clone https://github.com/LLM-Red-Team/kimi-cc.git`</sub>
- **[codemcp](https://github.com/ezyang/codemcp)** — (1.6k ⭐) - Coding assistant MCP for Claude Desktop
  <sub>★ 1.6k · Python · Apache-2.0 · uv · pushed 2025-12-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from git+https://github.com/ezyang/codemcp@prod codemcp serve`</sub>
- **[agentapi](https://github.com/coder/agentapi)** — (1.4k ⭐) - An HTTP API for Claude Code, Goose, Aider, and Codex
  <sub>★ 1.5k · Go · MIT · source · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/coder/agentapi.git`</sub>
- **[claude-code-mcp](https://github.com/steipete/claude-code-mcp)** — (1.3k ⭐) - Claude Code as a one-shot MCP server to have an agent in your agent
  <sub>★ 1.3k · JavaScript · MIT · source · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/steipete/claude-code-mcp.git`</sub>
- **[claude-balancer](https://github.com/snipeship/ccflare)** — (992 ⭐) - A load balancer proxy for multiple Claude OAuth accounts with automatic failover, request tracking, and web dashboard
  <sub>★ 1k · TypeScript · MIT · clone · pushed 2026-04-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/snipeship/ccflare`</sub>
- **[ccflare](https://github.com/snipeship/ccflare)** — (992 ⭐) - The ultimate Claude API proxy with intelligent load balancing across multiple accounts
  <sub>★ 1k · TypeScript · MIT · clone · pushed 2026-04-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/snipeship/ccflare`</sub>
- **[ccNexus](https://github.com/lich0821/ccNexus)** — (962 ⭐) - A smart API endpoint rotation proxy for Claude Code
  <sub>★ 974 · Go · MIT · source · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/lich0821/ccNexus.git`</sub>
- **[Context-Gateway](https://github.com/Compresr-ai/Context-Gateway)** — (614 ⭐) - An agentic proxy that enhances any AI agent workflow with instant history compaction and context optimization tools
  <sub>★ 643 · Go · Apache-2.0 · script · pushed 2026-08-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://compresr.ai/api/install | sh`</sub>
- **[my-free-code](https://github.com/hkqr/my-free-code)** — (623 ⭐) - Open-source multi-provider AI gateway for Claude Code and other coding agents, with model routing, streaming, tools, reasoning, fallbacks, and local model support
  <sub>★ 639 · Python · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hkqr/my-free-code.git`</sub>
- **[claude-code-proxy](https://github.com/seifghazi/claude-code-proxy)** — (480 ⭐) - Proxy that captures and visualizes in-flight Claude Code requests and conversations
  <sub>★ 507 · TypeScript · MIT · docker · pushed 2026-01-04 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3001:3001 -p 5173:5173 claude-code-proxy`</sub>
- **[anthropic-proxy](https://github.com/maxnowack/anthropic-proxy)** — (415 ⭐) - A proxy server that converts Anthropic API requests to OpenAI format and sends them to OpenRouter, used to use Claude Code with OpenRouter
  <sub>★ 415 · JavaScript · source · pushed 2025-04-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/maxnowack/anthropic-proxy.git`</sub>
- **[claude-gemini-bridge](https://github.com/tkaufmann/claude-gemini-bridge)** — (406 ⭐) - Intelligent integration between Claude Code and Google Gemini for large-scale code analysis
  <sub>★ 408 · Shell · MIT · clone · pushed 2025-08-17</sub>
  <sub>`git clone https://github.com/your-username/claude-gemini-bridge.git`</sub>
- **[claude-code-kimi-groq](https://github.com/fakerybakery/openbridge)** — (390 ⭐) - A basic proxy to use Kimi K2 on Claude Code through Groq
  <sub>★ 395 · Python · BSD-3-Clause · source · pushed 2025-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fakerybakery/claude-code-kimi-groq.git`</sub>
- **[y-router](https://github.com/luohy15/y-router)** — (384 ⭐) - A Simple Proxy enabling Claude Code to work with OpenRouter
  <sub>★ 384 · TypeScript · MIT · source · pushed 2026-01-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/luohy15/y-router.git`</sub>
- **[gemini-for-claude-code](https://github.com/coffeegrind123/gemini-for-claude-code)** — (348 ⭐) - A Python program allowing the use of Claude Code with Google's Gemini models
  <sub>★ 354 · Python · WTFPL · clone · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/coffeegrind123/gemini-code.git`</sub>
- **[mcp-claude-code](https://github.com/SDGLBL/mcp-claude-code)** — (301 ⭐) - MCP implementation of Claude Code capabilities and more
  <sub>★ 304 · Python · MIT · source · pushed 2025-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SDGLBL/mcp-claude-code.git`</sub>
- **[claude-code-nexus](https://github.com/KroMiose/claude-code-nexus)** — (253 ⭐) - Seamlessly forward Claude Code requests to any OpenAI-compatible API service with smart model mapping, streaming support, deployed on Cloudflare Worker
  <sub>★ 253 · TypeScript · MIT · source · pushed 2025-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KroMiose/claude-code-nexus.git`</sub>
- **[claude_code-gemini-mcp](https://github.com/RaiAnsar/claude_code-gemini-mcp)** — (245 ⭐) - Connect Claude Code with Google's Gemini AI for powerful AI collaboration
  <sub>★ 249 · Python · MIT · script · pushed 2025-06-10 · WSL2 · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/RaiAnsar/claude_code-gemini-mcp/main/install.sh | bash`</sub>
- **[claude-gemini-mcp-slim](https://github.com/cmdaltctr/claude-gemini-mcp-slim)** — (232 ⭐) - A lightweight integration that brings Google's Gemini AI capabilities to Claude Code through MCP (Model Context Protocol)
  <sub>★ 233 · Python · MIT · clone · pushed 2025-11-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/claude-gemini-mcp-slim.git`</sub>
- **[claude-historian](https://github.com/Vvkmnn/claude-historian-mcp)** — (178 ⭐) - An MCP server for Claude Code conversation history
  <sub>★ 178 · TypeScript · MIT · npm · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g claude-historian-mcp`</sub>
- **[castari-proxy](https://github.com/castari/castari-proxy)** — (90 ⭐) - Use Claude Agent SDK and Claude Code with other providers/models
  <sub>★ 89 · TypeScript · MIT · clone · pushed 2025-11-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/castari/castari-proxy.git`</sub>
- **[claude-code-open](https://github.com/Davincible/claude-code-open)** — (68 ⭐) - Claude Code with any LLM provider (OpenRouter, Gemini, Kimi K2)
  <sub>★ 69 · Go · go · pushed 2025-08-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/Davincible/claude-code-open@latest`</sub>
- **[Claudify](https://github.com/neno-is-ooo/claudify)** — (32 ⭐) - Use Claude Code as an LLM provider with your subscription flat fee instead of pay-per-token API keys
  <sub>★ 32 · TypeScript · MIT · npm · pushed 2025-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claudify`</sub>

## SDKs &amp; Development Kits

- **[vibekit](https://github.com/superagent-ai/vibekit)** — (1.8k ⭐) - A simple SDK for safely running Codex, Gemini CLI, and Claude Code in a secure sandbox
  <sub>★ 1.9k · TypeScript · MIT · npm · pushed 2026-01-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g vibekit`</sub>
- **[claude-code-requirements-builder](https://github.com/rizethereum/claude-code-requirements-builder)** — (1.8k ⭐) - A tool for building Claude Code requirements
  <sub>★ 1.8k · MIT · clone · pushed 2025-06-28</sub>
  <sub>`git clone https://github.com/rizethereum/claude-code-requirements-builder.git`</sub>
- **[Claude-Code-Development-Kit](https://github.com/peterkrueck/Claude-Code-Development-Kit)** — (1.4k ⭐) - A personal Claude Code Development Kit
  <sub>★ 1.4k · Shell · MIT · script · pushed 2026-07-22 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/peterkrueck/Claude-Code-Development-Kit/main/install.sh | bash`</sub>
- **[dotai](https://github.com/udecode/dotai)** — (1.2k ⭐) - The ultimate AI development stack, including Claude Code, Task Master, and Curso
  <sub>★ 1.2k · JavaScript · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add udecode/dotai`</sub>
- **[claude-code-sdk-ts](https://github.com/instantlyeasy/claude-code-sdk-ts)** — (206 ⭐) - Configure models, enable tools, stream events, then fetch text, JSON, run details or token stats in one call via .asText() or .allowTools('Read', 'Write')
  <sub>★ 207 · TypeScript · MIT · source · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/instantlyeasy/claude-code-sdk-ts.git`</sub>
- **[claude-code-typescript-hooks](https://github.com/bartolli/claude-code-typescript-hooks)** — (177 ⭐) - Fast, intelligent quality checks for different project types
  <sub>★ 178 · JavaScript · MIT · source · pushed 2025-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bartolli/claude-code-typescript-hooks.git`</sub>
- **[claude-code-api-rs](https://github.com/ZhangHanDong/claude-code-api-rs)** — (170 ⭐) - A high-performance Rust implementation of an OpenAI-compatible API gateway for Claude Code CLI
  <sub>★ 177 · Rust · clone · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ZhangHanDong/claude-code-api-rs.git`</sub>

## Usage &amp; Observability

- **[CodexBar](https://github.com/steipete/CodexBar)** — (14.8k ⭐) - Show usage stats for OpenAI Codex and Claude Code, without having to login
  <sub>★ 21.7k · Swift · MIT · brew · pushed 2026-09-22 · macOS</sub>
  <sub>`brew install --cask codexbar`</sub>
- **[ccusage](https://github.com/ccusage/ccusage)** — (16.1k ⭐) - A CLI tool for analyzing Claude Code usage from local JSONL files
  <sub>★ 18.7k · Rust · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ryoppippi/ccusage.git`</sub>
- **[ccstatusline](https://github.com/sirmalloc/ccstatusline)** — (10.7k ⭐) - A customizable status line formatter for Claude Code CLI that displays model info, git branch, token usage, and other metrics in your terminal
  <sub>★ 13k · TypeScript · MIT · npx · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx -y ccstatusline@latest`</sub>
- **[codeburn](https://github.com/getagentseal/codeburn)** — (8.0k ⭐) - See where your AI coding tokens go. Interactive TUI dashboard for Claude Code, Codex, and Cursor cost observability
  <sub>★ 11.2k · TypeScript · MIT · npm · pushed 2026-09-21 · macOS</sub>
  <sub>`npm install -g codeburn`</sub>
- **[codeburn](https://github.com/getagentseal/codeburn)** — (8.0k ⭐) - See where your AI coding tokens go. Interactive TUI dashboard for Claude Code, Codex, and Cursor cost observability
  <sub>★ 11.2k · TypeScript · MIT · npm · pushed 2026-09-21 · macOS</sub>
  <sub>`npm install -g codeburn`</sub>
- **[Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)** — (8.2k ⭐) - A real-time Claude Code usage monitor with predictions and warnings
  <sub>★ 8.7k · Python · MIT · uv · pushed 2026-07-05 · macOS</sub>
  <sub>`uv tool install claude-monitor`</sub>
- **[agentsview](https://github.com/kenn-io/agentsview)** — (5.9k ⭐) - Local-first session search, analytics, insights, and token-use statistics for Claude Code, Codex, and more than 20 coding agents
  <sub>★ 6k · Go · MIT · brew · pushed 2026-09-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install --cask agentsview`</sub>
- **[tokscale](https://github.com/junhoyeo/tokscale)** — (5.4k ⭐) - Terminal token-usage tracker for AI coding agents with interactive reports, model and project breakdowns, and a global leaderboard
  <sub>★ 5.5k · Rust · MIT · npx · pushed 2026-09-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx tokscale@latest`</sub>
- **[failproofai](https://github.com/FailproofAI/failproofai)** — (4.4k ⭐) - Observability and policy enforcement for AI agent harnesses, with run capture and runtime reliability checks
  <sub>★ 5.1k · MDX · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g failproofai`</sub>
- **[CCometixLine](https://github.com/Haleclipse/CCometixLine)** — (3.2k ⭐) - A high-performance Claude Code statusline tool written in Rust with Git integration and real-time usage tracking
  <sub>★ 3.5k · Rust · clone · pushed 2026-03-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Haleclipse/CCometixLine.git`</sub>
- **[claude-usage](https://github.com/phuryn/claude-usage)** — (1.8k ⭐) - A local dashboard for tracking your Claude Code token usage, costs, and session history
  <sub>★ 2.2k · Python · MIT · uv · pushed 2026-07-10 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install git+https://github.com/phuryn/claude-usage`</sub>
- **[zoetrope](https://github.com/furkankly/zoetrope)** — (173 ⭐) - A read-only terminal and browser flow graph for following live Claude Code sessions or replaying saved transcripts
  <sub>★ 924 · Rust · MIT · cargo · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install zoetrope`</sub>
- **[tokentap](https://github.com/jmuncor/tokentap)** — (798 ⭐) - Intercept LLM API traffic and visualize token usage in a real-time terminal dashboard
  <sub>★ 814 · Python · MIT · pip · pushed 2026-06-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install tokentap`</sub>
- **[ccglass](https://github.com/jianshuo/ccglass)** — (495 ⭐) - See what your coding agent (Claude Code, Codex, Kimi) sends to the model — local proxy + web dashboard
  <sub>★ 811 · JavaScript · MIT · npm · pushed 2026-07-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ccglass # or: brew install jianshuo/tap/ccglass`</sub>
- **[CCSeva](https://github.com/Iamshankhadeep/ccseva)** — (796 ⭐) - A beautiful macOS menu bar app for tracking your Claude Code usage in real-time
  <sub>★ 807 · TypeScript · MIT · clone · pushed 2026-08-03 · macOS</sub>
  <sub>`git clone https://github.com/Iamshankhadeep/ccseva.git`</sub>
- **[claude-task-viewer](https://github.com/L1AD/claude-task-viewer)** — (626 ⭐) - A web-based Kanban board for viewing Claude Code tasks
  <sub>★ 766 · HTML · MIT · npx · pushed 2026-02-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx claude-task-viewer`</sub>
- **[agentacct](https://github.com/mikehasa/agentacct)** — (467 ⭐) - Local-first work intelligence for coding agents, based on read-only session logs
  <sub>★ 750 · Python · MIT · pipx · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pipx install agentacct`</sub>
- **[agenttrail](https://github.com/sodiumsun/agenttrail)** — (454 ⭐) - Local observability map for Claude Code, Codex, and Cursor that tracks plans, tool calls, file changes, and progress in real time
  <sub>★ 697 · JavaScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agenttrail`</sub>
- **[cc-statusline](https://github.com/chongdashu/cc-statusline)** — (617 ⭐) - Transform your Claude Code experience with a beautiful, informative statusline
  <sub>★ 641 · TypeScript · MIT · npm · pushed 2026-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @chongdashu/cc-statusline`</sub>
- **[claude-doctor](https://github.com/millionco/claude-doctor)** — (594 ⭐) - Diagnostic tool for reviewing Claude Code sessions and finding problems in local agent workflows
  <sub>★ 622 · TypeScript · npm · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g claude-doctor`</sub>
- **[ClaudeCodeStatusLine](https://github.com/daniel3303/ClaudeCodeStatusLine)** — (531 ⭐) - Custom status line for Claude Code showing model, tokens, rate limits, and git info in real-time
  <sub>★ 609 · Shell · MIT · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/daniel3303/ClaudeCodeStatusLine.git`</sub>
- **[agentlytics](https://github.com/f/agentlytics)** — (537 ⭐) - Analytics dashboard for AI coding agents including Claude Code, Cursor, Windsurf, VS Code Copilot, Zed, Antigravity, OpenCode, and Command Code
  <sub>★ 580 · JavaScript · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentlytics`</sub>
- **[claude-code-otel](https://github.com/ColeMurray/claude-code-otel/)** — (440 ⭐) - A comprehensive observability solution for monitoring Claude Code usage, performance, and costs
  <sub>★ 503 · Makefile · MIT · source · pushed 2025-06-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ColeMurray/claude-code-otel/.git`</sub>
- **[claude-code-ui](https://github.com/KyleAMathews/claude-code-ui)** — (413 ⭐) - A real-time dashboard for monitoring Claude Code sessions across multiple projects
  <sub>★ 413 · TypeScript · source · pushed 2026-01-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KyleAMathews/claude-code-ui.git`</sub>
- **[claude-code-usage-bar](https://github.com/leeguooooo/claude-code-usage-bar)** — (270 ⭐) - Real-time statusline for Claude Code: token usage, remaining budget, burn rate, and depletion time
  <sub>★ 377 · Python · MIT · script · pushed 2026-09-16 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/leeguooooo/claude-code-usage-bar/main/install.sh | bash`</sub>
- **[claude-code-monitor](https://github.com/onikan27/claude-code-monitor)** — (237 ⭐) - Real-time dashboard for monitoring multiple Claude Code sessions from a CLI and mobile web UI on macOS
  <sub>★ 310 · TypeScript · MIT · npm · pushed 2026-01-29 · macOS</sub>
  <sub>`npm install -g claude-code-monitor`</sub>
- **[claude-pulse](https://github.com/nikitadoudikov/claude-pulse)** — (116 ⭐) - Live Claude Code dashboard for token use, context health, tool calls, session recovery, and mobile approvals
  <sub>★ 247 · JavaScript · MIT · npm · pushed 2026-07-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pulse-for-claude-code`</sub>
- **[claude-code-leaderboard](https://github.com/grp06/claude-code-leaderboard)** — (189 ⭐) - This CLI automatically monitors your token usage and posts your stats to the leaderboard after each Claude Code session
  <sub>★ 188 · JavaScript · npx · pushed 2025-08-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx claude-code-leaderboard`</sub>
- **[Claude / Codex Usage Dashboard](https://github.com/frankchiu-dev/claude-codex-usage-dashboard)** — (165 ⭐) - Local dashboard for viewing Claude Code and Codex usage limits on a phone, tablet, or small display
  <sub>★ 173 · JavaScript · MIT · clone · pushed 2026-06-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/frankchiu-dev/claude-codex-usage-dashboard.git`</sub>
- **[inferock-bench](https://github.com/inferock/inferock-bench)** — (140 ⭐) - Local LLM cost-tracking proxy for OpenAI, Anthropic, Gemini, and pinned OpenRouter calls, with token usage, failure, and billing-integrity receipts
  <sub>★ 141 · TypeScript · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx inferock-bench`</sub>
- **[claude-statusline](https://github.com/luongnv89/context-stats)** — (107 ⭐) - Customize the status line in Claude Code
  <sub>★ 118 · Python · MIT · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/luongnv89/claude-statusline.git`</sub>
- **[pyccsl](https://github.com/wolfdenpublishing/pyccsl)** — (83 ⭐) - Python Claude Code Status Line (PyCCSL, pronounced "pixel")
  <sub>★ 83 · Python · MIT · source · pushed 2025-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wolfdenpublishing/pyccsl.git`</sub>
- **[Claude-Monitor](https://github.com/RISCfuture/Claude-Monitor)** — (43 ⭐) - A menulet that tracks your Claude Code token usage
  <sub>★ 43 · Swift · MIT · source · pushed 2026-06-05 · macOS</sub>
  <sub>`git clone https://github.com/RISCfuture/Claude-Monitor.git`</sub>
- **[cccost](https://github.com/badlogic/cccost)** — (25 ⭐) - Instrument Claude Code to track actual token usage and cost
  <sub>★ 25 · TypeScript · npm · pushed 2025-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @mariozechner/cccost`</sub>
- **[tokentab](https://github.com/crwdla/tokentab)** — (1.1k ⭐) - Local CLI that reads Claude Code, Codex, and Gemini CLI session logs to calculate token usage and cost by model, project, and day
  <sub>unavailable</sub>
- **[tokentab](https://github.com/damejan80/tokentab)** — (288 ⭐) - A local CLI that reads Claude Code, Codex, Cursor, and Gemini CLI session logs and calculates token usage and cost by model, project, and day
  <sub>unavailable</sub>
- **[tokentab](https://github.com/wzchav/tokentab)** — (225 ⭐) - A CLI that reads Claude Code, Codex, and Gemini CLI session logs and works out how much they cost, by model, project, and day
  <sub>unavailable</sub>
- **[tokentab](https://github.com/sequilade/tokentab)** — (122 ⭐) - CLI for calculating Claude Code, Codex, and Gemini CLI session costs by model, project, and day
  <sub>unavailable</sub>


---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
