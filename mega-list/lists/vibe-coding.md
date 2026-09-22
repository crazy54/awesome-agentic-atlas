# Vibe Coding

A curated list of vibe coding references, collaborating with AI to write code.

Curated by **[filipecalegario/awesome-vibe-coding](https://github.com/filipecalegario/awesome-vibe-coding)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

100 entries · 48 distinct repos · 8 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/anthropics/claude-code"><img src="https://raw.githubusercontent.com/anthropics/claude-code/main/demo.gif" width="260"></a> | <a href="https://github.com/openai/codex"><img src="https://raw.githubusercontent.com/openai/codex/main/.github/codex-cli-splash.png" width="260"></a> | <a href="https://github.com/google-gemini/gemini-cli"><img src="https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/assets/gemini-screenshot.png" width="260"></a> |
| **[anthropics/claude-code](https://github.com/anthropics/claude-code)**<br>★ 147.6k | **[OpenAI Codex CLI](https://github.com/openai/codex)**<br>★ 125.9k | **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**<br>★ 107.1k |
| <a href="https://github.com/OpenHands/OpenHands"><img src="https://assets.openhands.dev/screenshot/automation-preview.png" width="260"></a> | <a href="https://github.com/upstash/context7"><img src="https://raw.githubusercontent.com/upstash/context7/master/public/cover.png?raw=true" width="260"></a> | <a href="https://github.com/PatrickJS/awesome-cursorrules"><img src="https://opengraph.githubassets.com/1/PatrickJS/awesome-cursorrules" width="260"></a> |
| **[OpenHands](https://github.com/OpenHands/OpenHands)**<br>★ 88.8k | **[Context7](https://github.com/upstash/context7)**<br>★ 62.3k | **[awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)**<br>★ 40.8k |

## Contents

- [Command Line Tools](#command-line-tools) (29)
- [Documentation for AI Coding](#documentation-for-ai-coding) (11)
- [Plugins and Extensions](#plugins-and-extensions) (18)
- [Task Management for AI Coding](#task-management-for-ai-coding) (6)
- [Local Apps](#local-apps) (5)
- [Browser-based Tools](#browser-based-tools) (22)
- [IDEs and Code Editors](#ides-and-code-editors) (8)
- [Mobile Apps](#mobile-apps) (1)

## Command Line Tools

- **[anthropics/claude-code](https://github.com/anthropics/claude-code)** — Coding agent that understands your codebase, automates tasks, explains code, and manages Git, all via natural language
  <sub>★ 147.6k · TypeScript · winget · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`winget install Anthropic.ClaudeCode`</sub>
- **[OpenAI Codex CLI](https://github.com/openai/codex)** — OpenAI's coding agent in the terminal with Codex Cloud, IDE extension, and multi-model support
  <sub>★ 125.9k · Rust · Apache-2.0 · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @openai/codex`</sub>
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — An open-source AI agent from Google that brings the power of Gemini directly into your terminal. Generous free tier (60 req/min, 1000/day)
  <sub>★ 107.1k · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @google/gemini-cli`</sub>
- **[OpenHands](https://github.com/OpenHands/OpenHands)** — Open-source AI-driven development agent with CLI, GUI, and cloud modes, supporting Claude, GPT, and other models
  <sub>★ 88.8k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[charmbracelet/crush](https://github.com/charmbracelet/crush)** — "The glamorous AI coding agent for your favourite terminal", multi-model with beautiful TUI
  <sub>★ 28.2k · Go · winget · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`winget install charmbracelet.crush`</sub>
- **[QwenLM/qwen-code](https://github.com/QwenLM/qwen-code)** — "qwen-code is a coding agent that lives in digital world"
  <sub>★ 28.1k · TypeScript · Apache-2.0 · psh · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.ps1 | iex`</sub>
- **[HKUDS/DeepCode](https://github.com/HKUDS/DeepCode)** — Deep learning for code analysis and generation. Achieves SOTA on PaperBench
  <sub>★ 16.6k · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install --python 3.12 deepcode-hku`</sub>
- **[Plandex](https://github.com/plandex-ai/plandex)** — Terminal-based AI coding agent with REPL mode for planning and executing complex tasks across multiple files, 2M token context
  <sub>★ 15.7k · Go · MIT · script · pushed 2025-10-03 · Win · WSL2 · macOS · Linux</sub>
  <sub>`curl -sL https://plandex.ai/install.sh | bash`</sub>
- **[kimi-cli](https://github.com/MoonshotAI/kimi-cli)** — Official command-line interface for Kimi, an AI assistant that helps with coding tasks and development workflows
  <sub>★ 11.4k · Python · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @moonshot-ai/kimi-code`</sub>
- **[claude-engineer](https://github.com/Doriandarko/claude-engineer)** — A self-improving AI coding assistant CLI built on Claude that can generate and manage its own tools
  <sub>★ 11.2k · Python · clone · pushed 2024-12-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Doriandarko/claude-engineer.git`</sub>
- **[GitHub Copilot CLI](https://github.com/github/copilot-cli)** — Full agentic development environment in the terminal with Autopilot mode, multi-model support, and GitHub integration. GA since Feb 2026
  <sub>★ 11.2k · Shell · winget · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install GitHub.Copilot`</sub>
- **[aichat](https://github.com/sigoden/aichat)** — All-in-one LLM CLI tool featuring shell assistant, REPL mode, RAG, AI tools and agents, supporting 20+ providers
  <sub>★ 10.5k · Rust · Apache-2.0 · scoop · pushed 2026-02-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop install aichat`</sub>
- **[Cloudflare/vibesdk](https://github.com/cloudflare/vibesdk)** — Cloudflare's SDK for vibe coding
  <sub>★ 5.4k · TypeScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cloudflare/vibesdk.git`</sub>
- **[mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe)** — Mistral AI's vibe coding tool
  <sub>★ 5k · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`uv tool install mistral-vibe`</sub>
- **[gptme](https://github.com/gptme/gptme)** — A personal AI agent in your terminal, equipped with local tools for coding, shell commands, file editing, and web browsing
  <sub>★ 4.4k · Python · MIT · uv · pushed 2026-09-22 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install gptme`</sub>
- **[superagent-ai/grok-cli](https://github.com/superagent-ai/grok-cli)** — Command-line interface for AI-powered coding assistance
  <sub>★ 3.5k · TypeScript · MIT · script · pushed 2026-07-06 · macOS</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/superagent-ai/grok-cli/main/install.sh | bash`</sub>
- **[ai-christianson/RA.Aid](https://github.com/ai-christianson/RA.Aid)** — A standalone coding agent built on LangGraph's agent-based task execution framework
  <sub>★ 2.2k · Python · Apache-2.0 · pip · pushed 2026-01-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ra-aid`</sub>
- **[superagent-ai/vibekit](https://github.com/superagent-ai/vibekit)** — A toolkit for building vibe coding applications
  <sub>★ 1.9k · TypeScript · MIT · npm · pushed 2026-01-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g vibekit`</sub>
- **[Gentleman-Programming/gentleman-guardian-angel](https://github.com/Gentleman-Programming/gentleman-guardian-angel)** — Provider-agnostic code review using AI. Use Claude, Gemini, Codex, Ollama to enforce your coding standards
  <sub>★ 1.2k · Shell · MIT · brew · pushed 2026-07-08 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install gentleman-programming/tap/gga`</sub>
- **[pyscn](https://github.com/ludo-technologies/pyscn)** — Code quality analyzer for vibe-coded Python. Detects dead code, clones, complexity issues, and coupling problems with MCP integration for AI assistants
  <sub>★ 1.1k · Go · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`uvx add-skills ludo-technologies/pyscn`</sub>
- **[onWatch](https://github.com/onllm-dev/onWatch)** — Open-source Go CLI that tracks AI API quota usage across 7 providers (Anthropic, OpenAI, GitHub Copilot, MiniMax, and more). Works with Claude Code, Codex CLI, Cursor, Cline, and other vibe coding tools. Background daemon, &lt;50MB RAM, zero telemetry
  <sub>★ 743 · Go · GPL-3.0 · psh · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/onllm-dev/onwatch/main/install.ps1 | iex`</sub>
- **[MyCoder.ai](https://github.com/bhouston/mycoder)** — Open source AI-powered coding assistant with Git and GitHub integration, featuring parallel execution and self-modification capabilities
  <sub>★ 568 · TypeScript · MIT · npm · pushed 2026-01-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g mycoder`</sub>
- **[langchain-code](https://github.com/zamalali/langchain-code)** — LangChain-based coding agent for AI-assisted development. Supports Gemini, Anthropic, OpenAI, and Ollama
  <sub>★ 439 · Python · Apache-2.0 · pip · pushed 2025-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langchain-code`</sub>
- **[CodeSelect](https://github.com/maynetee/codeselect)** — A Python-based command-line tool that efficiently communicates project source code to AIs
  <sub>★ 235 · Python · GPL-3.0 · script · pushed 2025-03-10 · WSL2 · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/maynetee/codeselect/main/install.sh | bash`</sub>
- **[aider](https://aider.chat/)** — AI pair programming in your terminal. Git-first with multi-file coordinated changes across 100+ languages
  <sub>website</sub>
  <sub>`https://aider.chat/`</sub>
- **[goose](https://block.github.io/goose/)** — Open-source, on-machine AI agent by Block that connects to systems via MCP for extensible automation
  <sub>website</sub>
  <sub>`https://block.github.io/goose/`</sub>
- **[Warp](https://warp.dev/)** — A modern, AI-powered terminal built for teams and individuals, featuring AI command search and workflows
  <sub>website</sub>
  <sub>`https://warp.dev/`</sub>
- **[Warp](https://www.warp.dev/)** — Agentic development environment with Oz orchestration platform for running unlimited parallel coding agents
  <sub>website</sub>
  <sub>`https://www.warp.dev/`</sub>
- **[OpenCode](https://opencode.ai/)** — Open-source AI coding agent for the terminal with LSP support, 75+ LLM providers, and multi-session workflows
  <sub>website</sub>
  <sub>`https://opencode.ai/`</sub>

## Documentation for AI Coding

- **[Context7](https://github.com/upstash/context7)** — Delivers up-to-date, version-specific documentation directly into LLM prompts. MCP server + CLI
  <sub>★ 62.3k · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upstash/context7.git`</sub>
- **[awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)** — Curated collection of .cursorrules configuration files for the Cursor AI editor
  <sub>★ 40.8k · JavaScript · CC0-1.0 · source · pushed 2026-05-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/PatrickJS/awesome-cursorrules.git`</sub>
- **[EnzeD/vibe-coding](https://github.com/EnzeD/vibe-coding)** — The Ultimate Guide to Vibe Coding with best practices and tips
  <sub>★ 4.8k · source · pushed 2026-05-25</sub>
  <sub>`git clone https://github.com/EnzeD/vibe-coding.git`</sub>
- **[KhazP/vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template)** — A prompt template for vibe coding
  <sub>★ 3.1k · TypeScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibeworkflow`</sub>
- **[llms.txt](https://github.com/AnswerDotAI/llms-txt)** — Standardized markdown file specification for making website documentation LLM-friendly
  <sub>★ 2.6k · Jupyter Notebook · Apache-2.0 · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/AnswerDotAI/llms-txt.git`</sub>
- **[claude-reflect](https://github.com/BayramAnnakov/claude-reflect)** — Self-learning system for Claude Code that captures corrections and syncs approved learnings to CLAUDE.md files
  <sub>★ 1.7k · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BayramAnnakov/claude-reflect.git`</sub>
- **[awesome-ralph](https://github.com/snwfdhmp/awesome-ralph)** — A curated list of resources about Ralph, the vibe coding technique that runs vibe coding agents in automated loops until specifications are fulfilled
  <sub>★ 922 · source · pushed 2026-02-03 · Win?</sub>
  <sub>`git clone https://github.com/snwfdhmp/awesome-ralph.git`</sub>
- **[Claude Code Organizer](https://github.com/mcpware/cross-code-organizer)** — Visual dashboard and MCP server to organize Claude Code memories, skills, MCP servers, and hooks with scope hierarchy and drag-and-drop
  <sub>★ 380 · JavaScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx @mcpware/cross-code-organizer --distill <session.jsonl>`</sub>
- **[CodeGuide](https://www.codeguide.dev/)** — Creates detailed Documentation for your AI Coding Projects
  <sub>website</sub>
  <sub>`https://www.codeguide.dev/`</sub>
- **[AGENTS.md](https://agents.md/)** — A simple, open format for guiding coding agents, stewarded by the Linux Foundation
  <sub>website</sub>
  <sub>`https://agents.md/`</sub>
- **[getdesign.md](https://getdesign.md/)** — Browsable library of DESIGN.md files curated from real websites
  <sub>website</sub>
  <sub>`https://getdesign.md/`</sub>

## Plugins and Extensions

- **[continuedev/continue](https://github.com/continuedev/continue)** — Open-source AI code agent with IDE extensions, CLI tool, and source-controlled AI checks enforceable in CI
  <sub>★ 36k · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/continuedev/continue.git`</sub>
- **[Tabby](https://github.com/TabbyML/tabby)** — Self-hosted AI coding assistant, open-source alternative to GitHub Copilot with code completion and repository-level context
  <sub>★ 33.9k · Rust · source · pushed 2026-06-30 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/TabbyML/tabby.git`</sub>
- **[avante.nvim](https://github.com/avante-corp/avante.nvim)** — Neovim plugin designed to emulate the behavior of the Cursor AI IDE with AI-driven code suggestions
  <sub>★ 18.2k · Lua · Apache-2.0 · source · pushed 2026-09-21 · Win · macOS</sub>
  <sub>`git clone https://github.com/yetone/avante.nvim.git`</sub>
- **[copilot.vim](https://github.com/github/copilot.vim)** — Official GitHub Copilot plugin for Vim/Neovim
  <sub>★ 11.7k · Vim Script · source · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/github/copilot.vim.git`</sub>
- **[CodeCompanion.nvim](https://github.com/olimorris/codecompanion.nvim)** — Neovim plugin for AI-assisted coding with agents, slash commands, and multiple LLM support
  <sub>★ 6.9k · Lua · Apache-2.0 · source · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/olimorris/codecompanion.nvim.git`</sub>
- **[Junie](https://github.com/JetBrains/junie)** — LLM-agnostic coding agent by JetBrains for terminal, IDE, and CI/CD
  <sub>★ 454 · Shell · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @jetbrains/junie`</sub>
- **[backnotprop/prompt-tower](https://github.com/backnotprop/prompt-tower)** — A tool that helps you build prompts with many code blocks
  <sub>★ 388 · TypeScript · AGPL-3.0 · clone · pushed 2025-12-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/backnotprop/prompt-tower.git`</sub>
- **[Cline](https://cline.bot/)** — Autonomous AI coding agent for VS Code that plans, creates files, runs builds, and fixes errors using MCP
  <sub>website</sub>
  <sub>`https://cline.bot/`</sub>
- **[Roo Code](https://roocode.com/)** — AI dev team with multiple Modes (Code, Architect, Debug), Cloud Agents, and Slack/GitHub integration
  <sub>website</sub>
  <sub>`https://roocode.com/`</sub>
- **[Kilo Code](https://kilocode.ai/)** — Open-source AI coding agent for VS Code, JetBrains, and CLI with Orchestrator mode and Memory Bank
  <sub>website</sub>
  <sub>`https://kilocode.ai/`</sub>
- **[Amp](https://ampcode.com/)** — Frontier coding agent with smart, rush, and deep agent modes. Spun out from Sourcegraph as standalone company
  <sub>website</sub>
  <sub>`https://ampcode.com/`</sub>
- **[Augment Code](https://www.augmentcode.com/)** — An AI coding assistant built for professional software engineers and large codebases, with MCP support
  <sub>website</sub>
  <sub>`https://www.augmentcode.com/`</sub>
- **[GitHub Copilot](https://github.com/features/copilot)** — AI pair programmer with agent mode, multi-model support (Claude, GPT, Gemini), and agentic coding across VS Code and JetBrains
  <sub>website</sub>
  <sub>`https://github.com/features/copilot`</sub>
- **[Amazon Q Developer – AWS](https://aws.amazon.com/q/developer)** — Amazon's Generative AI Assistant for Software Development
  <sub>website</sub>
  <sub>`https://aws.amazon.com/q/developer`</sub>
- **[Superdesign.dev](https://www.superdesign.dev/)** — Open Source Design Agent
  <sub>website</sub>
  <sub>`https://www.superdesign.dev/`</sub>
- **[Cody](https://sourcegraph.com/cody)** — Free AI code assistant by Sourcegraph with deep codebase understanding and code indexing
  <sub>website</sub>
  <sub>`https://sourcegraph.com/cody`</sub>
- **[Qodo Gen](https://www.qodo.ai/)** — AI-powered coding platform for VS Code with testing, code review, and agentic tools
  <sub>website</sub>
  <sub>`https://www.qodo.ai/`</sub>
- **[Skills.sh](https://skills.sh/)** — Open ecosystem by Vercel for installing reusable AI agent skills with a single command across 18+ platforms
  <sub>website</sub>
  <sub>`https://skills.sh/`</sub>

## Task Management for AI Coding

- **[vibe-kanban](https://github.com/BloopAI/vibe-kanban)** — A kanban board to manage and orchestrate AI coding agents. Supports 10+ coding agents
  <sub>★ 28.2k · Rust · Apache-2.0 · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibe-kanban`</sub>
- **[Claude Task Master](https://github.com/eyaltoledano/claude-task-master)** — An AI-powered task-management system you can drop into Cursor, Lovable, Windsurf, Roo, and others
  <sub>★ 28.1k · JavaScript · npm · pushed 2026-04-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g task-master-ai`</sub>
- **[Archon](https://github.com/coleam00/Archon)** — Knowledge and task management backbone for AI coding assistants via MCP
  <sub>★ 23.5k · TypeScript · MIT · psh · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://archon.diy/install.ps1 | iex`</sub>
- **[CCPM (Claude Code PM)](https://github.com/automazeio/ccpm)** — Project management for Claude Code using GitHub Issues and Git worktrees for parallel agent execution
  <sub>★ 8.4k · Shell · MIT · clone · pushed 2026-03-18</sub>
  <sub>`git clone https://github.com/automazeio/ccpm.git`</sub>
- **[AI-DLC Workflows (AWS Labs)](https://github.com/awslabs/aidlc-workflows)** — AI-Driven Development Life Cycle workflow rules for coding agents. Supports Kiro, Q Developer, Cursor, Cline, Claude Code
  <sub>★ 4.8k · TypeScript · MIT-0 · psh · pushed 2026-09-22 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://github.com/awslabs/aidlc-workflows/releases/latest/download/install.ps1 | iex`</sub>
- **[Boomerang Tasks](https://docs.roocode.com/features/boomerang-tasks)** — Automatically break down complex projects into smaller, manageable pieces
  <sub>website</sub>
  <sub>`https://docs.roocode.com/features/boomerang-tasks`</sub>

## Local Apps

- **[bolt.diy](https://github.com/stackblitz-labs/bolt.diy)** — Open-source version of Bolt.new with Electron desktop apps, 19+ AI providers, and local model support via Ollama
  <sub>★ 19.9k · TypeScript · MIT · source · pushed 2026-02-07 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/stackblitz-labs/bolt.diy.git`</sub>
- **[Superset](https://github.com/superset-sh/superset)** — Desktop app to orchestrate multiple AI coding agents in parallel (Claude Code, Codex, etc.) with Git worktree isolation
  <sub>★ 14.5k · TypeScript · brew · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install superset-sh/tap/superset`</sub>
- **[Parallel Code](https://github.com/johannesjo/parallel-code)** — Desktop app for running multiple AI coding agents (Claude Code, Codex CLI, Gemini CLI) simultaneously in isolated git worktrees
  <sub>★ 1k · TypeScript · MIT · clone · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/johannesjo/parallel-code.git`</sub>
- **[CCHub](https://github.com/Moresl/cchub)** — Desktop app for managing the Claude Code ecosystem — MCP server marketplace, config profile switching, workflow templates, security audit, and autopilot. Built with Tauri + React + Rust
  <sub>unavailable</sub>
- **[Dyad](https://www.dyad.sh/)** — Free, local, open-source AI app builder. Model-agnostic, supports cloud models and local via Ollama
  <sub>website</sub>
  <sub>`https://www.dyad.sh/`</sub>

## Browser-based Tools

- **[Bolt.new](https://bolt.new/)** — Prompt, run, edit, and deploy full-stack web and mobile apps
  <sub>website</sub>
  <sub>`https://bolt.new/`</sub>
- **[Lovable](https://lovable.dev/)** — "Idea to app in seconds. Lovable is your superhuman full stack engineer"
  <sub>website</sub>
  <sub>`https://lovable.dev/`</sub>
- **[v0 by Vercel](https://v0.dev/chat)** — Vibe coding platform for building production apps and agents with Next.js
  <sub>website</sub>
  <sub>`https://v0.dev/chat`</sub>
- **[Capacity](https://capacity.so/)** — Turn your ideas into fully functional web apps in minutes using AI
  <sub>website</sub>
  <sub>`https://capacity.so/`</sub>
- **[Command.new by Langbase](https://command.new)** — Prompt to vibe code any AI agent and deploy (agent, app, api)
  <sub>website</sub>
  <sub>`https://command.new`</sub>
- **[Replit](https://replit.com/)** — "Simply describe your idea above and let the Agent build it for you"
  <sub>website</sub>
  <sub>`https://replit.com/`</sub>
- **[Anything](https://www.create.xyz/)** — AI-powered app builder that turns natural language prompts into fully functional web applications (formerly Create.xyz)
  <sub>website</sub>
  <sub>`https://www.create.xyz/`</sub>
- **[Trickle AI](https://www.trickle.so/)** — "Build stunning websites, AI apps, and forms with ease"
  <sub>website</sub>
  <sub>`https://www.trickle.so/`</sub>
- **[Tempo](https://www.tempo.new/)** — "Build React apps 10x faster with AI". Visual IDE with Figma plugin and MCP App Store
  <sub>website</sub>
  <sub>`https://www.tempo.new/`</sub>
- **[Softgen](https://softgen.ai/)** — "Describe your vision, give instructions, and build full-stack web apps"
  <sub>website</sub>
  <sub>`https://softgen.ai/`</sub>
- **[Lazy AI](https://getlazy.ai/)** — "Build reliable business apps with prompts"
  <sub>website</sub>
  <sub>`https://getlazy.ai/`</sub>
- **[HeyBoss](https://heyboss.ai/)** — "Build app &amp; sites in minutes" with a full AI team (CEO, Designer, Developer, Marketer &amp; Copywriter)
  <sub>website</sub>
  <sub>`https://heyboss.ai/`</sub>
- **[Creatr](https://getcreatr.com/)** — "Create and deploy web apps and landing pages in seconds"
  <sub>website</sub>
  <sub>`https://getcreatr.com/`</sub>
- **[Rork](https://rork.com/)** — "Build any mobile app, fast" with React Native and Expo
  <sub>website</sub>
  <sub>`https://rork.com/`</sub>
- **[Firebase Studio](https://studio.firebase.google.com/)** — Google's agentic cloud-based development environment that helps build and ship production-quality full-stack AI apps
  <sub>website</sub>
  <sub>`https://studio.firebase.google.com/`</sub>
- **[Napkins.dev](https://www.napkins.dev/)** — Screenshot to code using Llama vision models
  <sub>website</sub>
  <sub>`https://www.napkins.dev/`</sub>
- **[HeroUI Chat](https://heroui.chat/)** — Generate beautiful apps regardless of your design experience
  <sub>website</sub>
  <sub>`https://heroui.chat/`</sub>
- **[Rocket.new](https://www.rocket.new/)** — "Build Web &amp; Mobile Apps 10x Faster Without Code"
  <sub>website</sub>
  <sub>`https://www.rocket.new/`</sub>
- **[Google AI Studio](https://aistudio.google.com/)** — "Another way to vibecode with Gemini. Great for experimenting"
  <sub>website</sub>
  <sub>`https://aistudio.google.com/`</sub>
- **[Emergent](https://emergent.sh/)** — Multi-agent AI app builder that plans, codes, tests, and deploys full-stack web and mobile apps autonomously
  <sub>website</sub>
  <sub>`https://emergent.sh/`</sub>
- **[Manus](https://manus.im/)** — Autonomous AI agent for end-to-end project automation, from research to deployment
  <sub>website</sub>
  <sub>`https://manus.im/`</sub>
- **[Same.new](https://same.new/)** — AI web builder for cloning and creating websites from descriptions
  <sub>website</sub>
  <sub>`https://same.new/`</sub>

## IDEs and Code Editors

- **[Windsurf](https://windsurf.com/)** — Agentic IDE (acquired by Cognition, makers of Devin) with Cascade for multi-step coding and Tab/Supercomplete for completions
  <sub>website</sub>
  <sub>`https://windsurf.com/`</sub>
- **[Cursor](https://www.cursor.com/)** — AI Code Editor with Cloud Agents, JetBrains integration, and 30+ plugins from partners like Atlassian, Datadog, and GitLab
  <sub>website</sub>
  <sub>`https://www.cursor.com/`</sub>
- **[Zed](https://zed.dev/)** — First "Agentic IDE" built in Rust with built-in AI agents and real-time collaboration at 120fps
  <sub>website</sub>
  <sub>`https://zed.dev/`</sub>
- **[Amazon Kiro](https://kiro.dev)** — The AI IDE for prototype to production, with spec-driven development and AWS integrations
  <sub>website</sub>
  <sub>`https://kiro.dev`</sub>
- **[Google Antigravity](https://antigravity.google/)** — Google's agentic development platform with Manager view for orchestrating multiple agents in parallel. Free, cross-platform
  <sub>website</sub>
  <sub>`https://antigravity.google/`</sub>
- **[Orchids](https://www.orchids.app/)** — The Vibe Coding IDE that can build, watch, and listen on par with a human developer
  <sub>website</sub>
  <sub>`https://www.orchids.app/`</sub>
- **[Trae IDE](https://www.trae.ai/)** — Free AI IDE by ByteDance with Builder Mode, free access to GPT-4o, Claude Sonnet, and DeepSeek R1
  <sub>website</sub>
  <sub>`https://www.trae.ai/`</sub>
- **[Devin](https://devin.ai/)** — Autonomous AI software engineer by Cognition with its own IDE, shell, browser, and cloud sandbox
  <sub>website</sub>
  <sub>`https://devin.ai/`</sub>

## Mobile Apps

- **[VibeCode](https://www.vibecodeapp.com/)** — The app that builds apps. Available on iOS and Android
  <sub>website</sub>
  <sub>`https://www.vibecodeapp.com/`</sub>


---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
