# Orchestrators

The original list this workbook grew from: tools that run several coding agents at once.

Curated by **[andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

366 entries · 366 distinct repos · 8 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/buhuipao/agent-console"><img src="https://raw.githubusercontent.com/buhuipao/agent-console/main/docs/assets/demo.gif" width="260"></a> | <a href="https://github.com/asheshgoplani/agent-deck"><img src="https://opengraph.githubassets.com/1/asheshgoplani/agent-deck" width="260"></a> | <a href="https://github.com/wainmann/agent-manager"><img src="https://opengraph.githubassets.com/1/wainmann/agent-manager" width="260"></a> |
| **[agent-console](https://github.com/buhuipao/agent-console)**<br>★ 41 | **[agent-deck](https://github.com/asheshgoplani/agent-deck)**<br>★ 1.3k | **[agent-manager](https://github.com/wainmann/agent-manager)**<br>★ 702 |
| <a href="https://github.com/izll/agent-session-manager"><img src="https://opengraph.githubassets.com/1/izll/agent-session-manager" width="260"></a> | <a href="https://github.com/agent-of-empires/agent-of-empires"><img src="https://opengraph.githubassets.com/1/agent-of-empires/agent-of-empires" width="260"></a> | <a href="https://github.com/madarco/agentbox"><img src="https://opengraph.githubassets.com/1/madarco/agentbox" width="260"></a> |
| **[agent-session-manager](https://github.com/izll/agent-session-manager)**<br>★ 16 | **[agent-of-empires](https://github.com/agent-of-empires/agent-of-empires)**<br>★ 4.6k | **[agentbox](https://github.com/madarco/agentbox)**<br>★ 584 |

## Contents

- [Parallel Coding Agents — Terminal (TUI/CLI)](#parallel-coding-agents--terminal-tuicli) (37)
- [Parallel Coding Agents — Desktop &amp; Web](#parallel-coding-agents--desktop--web) (130)
- [Multi-Agent Swarms](#multi-agent-swarms) (46)
- [Autonomous Loop Runners](#autonomous-loop-runners) (15)
- [Autonomous Task Runners](#autonomous-task-runners) (29)
- [Agent Infrastructure &amp; Primitives](#agent-infrastructure--primitives) (47)
- [Personal Assistants](#personal-assistants) (46)
- [Resting](#resting) (16)

## Parallel Coding Agents — Terminal (TUI/CLI)

- **[herdr](https://github.com/herdrdev/herdr)** — Background runtime that owns your agents' terminals: sessions survive reboot and reattach from any terminal or SSH, panes are marked working/blocked/idle, and agents themselves spawn panes and prompt each other over a CLI and socket API. One Rust binary.
  <sub>★ 52k · Rust · Apache-2.0 · brew · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`brew install herdr`</sub>
- **[cmux](https://github.com/manaflow-ai/cmux)** — Ghostty-based macOS terminal with vertical tabs and per-agent notifications, built for keeping many concurrent sessions legible.
  <sub>★ 28.8k · Swift · brew · pushed 2026-11-20 · macOS</sub>
  <sub>`brew tap manaflow-ai/cmux`</sub>
- **[claude-squad](https://github.com/smtg-ai/claude-squad)** — Runs each agent as a detached background session with its own worktree, so work continues after you close the pane. Claude Code, Codex, OpenCode, Amp.
  <sub>★ 8.8k · Go · AGPL-3.0 · brew · pushed 2026-11-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install claude-squad`</sub>
- **[tuios](https://github.com/Gaurav-Gosain/tuios)** — A terminal window manager that knows what your agents are doing. Tile panes across nine workspaces in the terminal you already use. A daemon keeps sessions running when you detach and reaches your other machines. The coding agents in your panes report what they are doing, and one Inbox holds everything they are waiting on. Agent integration for claude-code, codex, gemini-cli, opencode, amp, antigravity, copilot, crush, cursor-agent, devin, droid, grok, hermes, kilo, kimi, pi, omp, qoder, qwen.
  <sub>★ 6.6k · Go · MIT · go · pushed 2026-11-20 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/Gaurav-Gosain/tuios/cmd/tuios@latest`</sub>
- **[agent-of-empires](https://github.com/agent-of-empires/agent-of-empires)** — Pairs a TUI with a matching web view, so the same sessions stay reachable from a phone. Claude Code, Codex, OpenCode, Gemini, Mistral Vibe.
  <sub>★ 4.6k · Rust · MIT · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/agent-of-empires/agent-of-empires/main/scripts/install.sh | bash`</sub>
- **[dmux](https://github.com/standardagents/dmux)** — Dev agent multiplexer pairing coding agents with git worktrees over tmux.
  <sub>★ 1.8k · HTML · MIT · npm · pushed 2026-08-16 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g dmux`</sub>
- **[ai-devkit](https://github.com/codeaholicguy/ai-devkit)** — CLI control plane that runs agent sessions in managed tmux, sends prompts and logs to running agents from the terminal or a TUI console, and gives every agent one setup with shared local memory, verification skills, and lifecycle workflows. Claude Code, Codex, Pi, and more.
  <sub>★ 1.7k · TypeScript · Apache-2.0 · npx · pushed 2026-11-19 · WSL2 · macOS? · Linux</sub>
  <sub>`npx ai-devkit@latest setup`</sub>
- **[agent-deck](https://github.com/asheshgoplani/agent-deck)** — One TUI covering sessions across Claude Code, Codex, Gemini, and OpenCode, with live status and resume for each.
  <sub>★ 1.3k · Go · MIT · brew · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`brew install asheshgoplani/tap/agent-deck`</sub>
- **[Termio](https://github.com/termio-sh/termio)** — Terminal-first agentic development environment where agents' own hooks report working, idle, or needs-you per session; a daemon keeps sessions alive across laptop closes, and remote sessions run on any SSH VPS. Claude Code, Codex, OpenCode, Pi, Amp, Cursor, Copilot. MIT.
  <sub>★ 789 · Swift · MIT · npx · pushed 2026-11-19 · WSL2 · macOS? · Linux</sub>
  <sub>`npx skills add termio-sh/termio --skill termio`</sub>
- **[agterm](https://github.com/umputun/agterm)** — Native macOS terminal with named workspaces, a live dashboard, attention states, and a scriptable control API.
  <sub>★ 757 · Swift · MIT · brew · pushed 2026-11-20 · macOS</sub>
  <sub>`brew install --cask umputun/apps/agterm`</sub>
- **[agent-manager](https://github.com/wainmann/agent-manager)** — Live-status tmux TUI with a prompt that lands in the pane without attaching, and in-terminal diff review that sends line comments back to the agent. Claude Code, Codex, OpenCode, Grok, Gemini CLI, Pi, Hermes.
  <sub>★ 702 · Go · Apache-2.0 · scoop · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`scoop bucket add yoanwai https://github.com/YoanWai/scoop-bucket scoop install yoanwai/agent-manager`</sub>
- **[Prowl](https://github.com/onevcat/Prowl)** — Native macOS command center for running coding agents in parallel, with vertical tabs, a live canvas view of every running session, and a command palette. Claude Code, Codex, and more.
  <sub>★ 680 · Swift · brew · pushed 2026-11-20 · macOS</sub>
  <sub>`brew install --cask onevcat/tap/prowl`</sub>
- **[agentbox](https://github.com/madarco/agentbox)** — Gives each agent its own sandboxed VM — local Docker or cloud via Hetzner, Daytona, Vercel, or E2B — with sub-second checkpoint starts.
  <sub>★ 584 · TypeScript · MIT · clone · pushed 2026-11-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/madarco/agentbox`</sub>
- **[tmux-ide](https://github.com/wavyrai/tmux-ide)** — Turns any project into a tmux IDE from a checked-in `ide.yml`, including preset agent-team layouts.
  <sub>★ 569 · TypeScript · MIT · npm · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g tmux-ide`</sub>
- **[amux (mixpeek)](https://github.com/mixpeek/amux)** — Web dashboard plus iPhone, iPad, and Mac apps for running many agents in parallel in tmux, with a shared task board, agent-to-agent messages, and schedules. Claude Code, Codex, Gemini CLI.
  <sub>★ 565 · Rust · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://amux.io/install.sh | bash`</sub>
- **[termany](https://github.com/thinkany-ai/termany)** — Terminal that keeps many agent sessions in one window, tagging each pane working/done/needs-attention from the running job rather than the shell prompt, with diffs, worktrees, port handling, remote hosts, and token cost in the same place. Claude, Codex, Gemini, Grok Build, OpenClaw, Hermes, OpenCode, Cursor, Kimi, OMP.
  <sub>★ 513 · TypeScript · source · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/thinkany-ai/termany.git`</sub>
- **[Calyx](https://github.com/yuuichieguchi/Calyx)** — Native macOS terminal built on libghostty with an approval inbox for permission prompts, a working/blocked/idle sidebar, and in-terminal diff review.
  <sub>★ 367 · Swift · MIT · brew · pushed 2026-10-23 · macOS</sub>
  <sub>`brew install --cask calyx`</sub>
- **[Rove](https://github.com/Sma1lboy/rove)** — TUI orchestrator that gives each task its own git worktree and branch, with sessions that survive detach or dropped SSH, a Kanban board whose cards launch sessions and get moved by agents, and a `rove api` for agents to dispatch tasks that report back. Claude Code, Codex, Copilot, Kimi, Pi, Gemini CLI, OpenCode, Cursor Agent, and any CLI you register.
  <sub>★ 188 · TypeScript · MIT · npm · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @sma1lboy/rove # offers to install Bun on first launch`</sub>
- **[amux](https://github.com/andyrewlee/amux)** — Minimal TUI for spawning parallel coding agents in git worktrees.
  <sub>★ 168 · Go · MIT · go · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`go install github.com/andyrewlee/amux/cmd/amux@latest`</sub>
- **[openkanban](https://github.com/TechDufus/openkanban)** — Kanban board for orchestrating coding agents, rendered entirely in the terminal.
  <sub>★ 155 · Go · AGPL-3.0 · go · pushed 2026-06-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/techdufus/openkanban@latest`</sub>
- **[thurbox](https://github.com/Thurbeen/thurbox)** — TUI orchestrator with remote SSH sessions, inter-session messaging, and a native code-review view. Works with any CLI agent you define.
  <sub>★ 120 · Rust · MIT · psh · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/Thurbeen/thurbox/main/scripts/install.ps1 | iex`</sub>
- **[ReevesAgents](https://github.com/mertkayacs/reevesagents)** — TUI, Web UI, and CLI that run coding CLIs side by side in tmux windows, plus an opt-in MCP server so one agent can spawn, read, steer, and stop the others. Claude Code, Codex, OpenCode, Hermes, Kimi, DeepSeek, Qwen, Pi, Aider, and more.
  <sub>★ 107 · TypeScript · Apache-2.0 · npm · pushed 2026-11-18 · WSL2 · macOS? · Linux</sub>
  <sub>`pnpm add -g reevesagents`</sub>
- **[YYLO](https://github.com/yylo-dev/yylo)** — Command-line orchestrator for coding agents with typed task, validation, merge, and release-readiness boundaries: each task runs in a dedicated branch and worktree, and a risk-based merge queue reviews the result with receipt-backed changes. Pi and Codex subagents.
  <sub>★ 69 · Python · MIT · npm · pushed 2026-11-13 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install --global '@yylo/cli@latest'`</sub>
- **[summon](https://github.com/juan294/summon)** — Opens a project's agent workspace with one command from a checked-in `.summon` file, as native Ghostty splits or a Rex session with one block per pane, and switches back to it when it is already running. Any CLI agent, such as Claude Code or Codex.
  <sub>★ 60 · TypeScript · MIT · npm · pushed 2026-11-20 · macOS</sub>
  <sub>`npm i -g summon-ws`</sub>
- **[agent-console](https://github.com/buhuipao/agent-console)** — Rust TUI that finds Codex and Claude Code sessions from the providers' own transcripts, including ones started elsewhere, and resumes their native UI rather than replacing it. No tmux or worktrees.
  <sub>★ 41 · Rust · Apache-2.0 · cargo · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install agent-console`</sub>
- **[Mercury CLI](https://github.com/Whq02/MercuryCLI)** — Terminal coding agent that runs parallel sessions and delegates to crewmates in isolated Git worktrees with file leases, using 22 model providers or local models.
  <sub>★ 31 · TypeScript · Apache-2.0 · psh · pushed 2026-11-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://mercury-cli.ai/install.ps1 | iex # Windows (x64 and arm64), in PowerShell 7`</sub>
- **[Vigil](https://github.com/butterlatte-zhang/vigil)** — Native macOS terminal where a manager agent runs the tree — spawning workers and sub-managers, detail flowing down, summaries rolling up — while every node stays the CLI's own TUI you can take over. Claude Code, Codex, OpenCode.
  <sub>★ 29 · Swift · GPL-3.0 · clone · pushed 2026-11-19 · macOS</sub>
  <sub>`git clone https://github.com/butterlatte-zhang/vigil.git`</sub>
- **[repomon](https://github.com/AliHamzaAzam/repomon)** — Rust TUI that supervises a fleet across many repositories at once, in durable tmux sessions you can approve from your phone.
  <sub>★ 24 · Rust · Apache-2.0 · psh · pushed 2026-10-04 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://github.com/AliHamzaAzam/repomon/releases/latest/download/install.ps1 | iex`</sub>
- **[pappardelle](https://github.com/chardigio/pappardelle)** — TUI that turns a description into a Linear, Jira, or beads issue, a git worktree, a PR, and a Claude Code session beside a companion pane, wired together in a 3-pane tmux layout.
  <sub>★ 17 · TypeScript · MIT · script · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/chardigio/pappardelle/main/install.sh | bash`</sub>
- **[agent-session-manager](https://github.com/izll/agent-session-manager)** — Live tmux TUI with session groups, resume and fork, diff review, and mobile push when an agent needs an answer. Claude Code, Codex, Gemini, Aider, Amazon Q, OpenCode.
  <sub>★ 16 · Go · MIT · script · pushed 2026-09-25 · Win · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/izll/agent-session-manager/main/install.sh | bash`</sub>
- **[herduck](https://github.com/wenhanweime/herduck)** — Terminal app derived from Herdr: keeps its agent panes and adds a Work view that groups the Claude Code, Codex, OpenCode, and Pi sessions behind one piece of work with its goal, blocker, and next step. Early alpha.
  <sub>★ 15 · Rust · npm · pushed 2026-11-10 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g herduck@alpha`</sub>
- **[Cyclops](https://github.com/cyclops-team/cyclops)** — Coordinates coding agents running in tmux through a durable mailbox with guarded terminal notifications, FIFO delivery per recipient, and fail-closed human-composer protection, with an optional workspace UI for overseeing the team. Codex CLI, Claude Code, Antigravity, Cursor Agent.
  <sub>★ 14 · Rust · MIT · script · pushed 2026-09-08 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://www.usecyclops.dev/install.sh | sh`</sub>
- **[pando](https://github.com/xseman/pando)** — Go daemon and TUI that give each session its own Git worktree, mark it running, blocked, or idle, keep agents alive when the TUI closes and resume their conversations after a restart, with diff review and commit in the TUI and a CLI that blocks on a status or screen match. Claude Code, Codex, Gemini CLI, OpenCode, or any CLI.
  <sub>★ 9 · Go · Apache-2.0 · script · pushed 2026-11-15 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/xseman/pando/master/install.sh | sh`</sub>
- **[Craig](https://github.com/hallsamuel90/craig)** — Keyboard-driven TUI for running Claude Code, Codex, and Cursor in isolated Git worktrees, with diffs, pull requests, and checks.
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-11-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g craig-cli`</sub>
- **[pohunek](https://github.com/zajca/pohunek)** — Per-machine Rust daemon that keeps agent sessions alive across disconnects, each in its own git worktree, marks them working, blocked, or idle, and has a JSON CLI so agents can drive other sessions, across machines over NetBird or Tailscale. Codex, Claude Code, and Hermes Agent.
  <sub>★ 8 · Rust · MIT · brew · pushed 2026-11-20 · WSL2? · macOS · Linux</sub>
  <sub>`brew install zajca/pohunek/pohunek`</sub>
- **[taskpods](https://github.com/yanairon/taskpods)** — Lightweight, agent-agnostic CLI that runs parallel coding-agent tasks in isolated Git worktrees and branches, with list, PR, cleanup, and abort lifecycle commands.
  <sub>★ 5 · Python · MIT · pip · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install taskpods`</sub>
- **[DevThrottle](https://github.com/thefrederiksen/devthrottle)** — Orchestration tool for command-line coding agents. MIT.
  <sub>unavailable</sub>

## Parallel Coding Agents — Desktop &amp; Web

- **[Orca](https://github.com/stablyai/orca)** — Agentic development environment for running a fleet on your own subscription, available on desktop and mobile.
  <sub>★ 130.4k · TypeScript · MIT · brew · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask stablyai/orca/orca`</sub>
- **[t3code](https://github.com/pingdotgg/t3code)** — Harness control surface available as web, mobile, and desktop app. Claude Code, Codex, Cursor, Grok Build, OpenCode.
  <sub>★ 67.1k · TypeScript · MIT · winget · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`winget install T3Tools.T3Code`</sub>
- **[AionUi](https://github.com/iOfficeAI/AionUi)** — Desktop app that runs several agent CLIs side by side in one window, each in its own session, with MCP and ACP support, file preview, scheduled tasks, and a WebUI for reaching the same sessions from another device. Linux, macOS, Windows. Claude Code, Codex, Gemini CLI, Qwen Code, OpenCode.
  <sub>★ 34.4k · TypeScript · Apache-2.0 · brew · pushed 2026-11-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install aionui`</sub>
- **[Happy](https://github.com/slopus/happy)** — Desktop app and CLI running agent sessions side by side on your own machine or server, with an end-to-end encrypted iOS/Android app for the same sessions. Claude Code, Codex, and Grok in the desktop app; Claude Code, Codex, and any ACP agent from the CLI.
  <sub>★ 24.7k · Swift · MIT · npm · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g happy`</sub>
- **[Paseo](https://github.com/getpaseo/paseo)** — Self-hosted daemon running agents in parallel on your own machines, driven from desktop, iOS/Android, web, or CLI, with voice control, diff review, and no telemetry or forced log-ins. Claude Code, Codex, Copilot, OpenCode, Pi.
  <sub>★ 24.5k · TypeScript · npm · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`npm install -g @getpaseo/cli`</sub>
- **[Paradev](https://github.com/ParadevAI/Paradev)** — Code editor built around running many agents on your machine at once.
  <sub>★ 16.4k · TypeScript · MIT · brew · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install paradevai/tap/superset`</sub>
- **[qm](https://github.com/yc-software/qm)** — Multiplayer harness where each teammate gets an isolated workspace to run agents independently, driven from Slack or the web.
  <sub>★ 15.7k · TypeScript · MIT · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yc-software/qm.git`</sub>
- **[Orchestrator.inc](https://github.com/OrchestratorInc/agent-orchestrator)** — Desktop workspace that runs and supervises teams of coding agents from planning to merge: project-aware orchestration splits work into workers with isolated workspaces, tracked on a live Kanban with PRs, CI, and review, plus iPhone and Android apps. Claude Code, Codex, and 30+ harnesses.
  <sub>★ 15k · TypeScript · Apache-2.0 · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OrchestratorInc/agent-orchestrator.git`</sub>
- **[Aperant](https://github.com/AndyMik90/Aperant)** — Runs up to 12 agent terminals with a self-validating QA loop and automatic conflict resolution when merging back to main.
  <sub>★ 14.6k · TypeScript · AGPL-3.0 · source · pushed 2026-06-14 · macOS</sub>
  <sub>`git clone https://github.com/AndyMik90/Aperant.git`</sub>
- **[OpenChamber](https://github.com/openchamber/openchamber)** — Open-source workspace for running, supervising, and reviewing AI coding work across desktop, browser, editor, and mobile, with parallel model runs and per-run worktrees.
  <sub>★ 13.1k · TypeScript · MIT · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/openchamber/openchamber/main/scripts/install.sh | bash`</sub>
- **[humanlayer](https://github.com/humanlayer/humanlayer)** — Human-in-the-loop control for coding agents on hard problems; the repo notes its code is now largely deprecated in favor of a rebuild.
  <sub>★ 12.9k · TypeScript · Apache-2.0 · source · pushed 2026-11-16 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/humanlayer/humanlayer.git`</sub>
- **[Emdash](https://github.com/generalaction/emdash)** — Agentic development environment running parallel agents against any model provider.
  <sub>★ 6.3k · TypeScript · Apache-2.0 · brew · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask emdash`</sub>
- **[bb](https://github.com/get-bb/bb)** — Self-controlling agentic IDE that orchestrates multiple coding agents in live threads you can follow, steer, or hand off, driven from a desktop app, web app, CLI, or HTTP API.
  <sub>★ 5.8k · TypeScript · MIT · npx · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`npx bb-app@latest`</sub>
- **[MonoCode](https://github.com/hardbeat920/monocode)** — Tauri desktop UI where tabs are agent sessions, running Claude Code, Codex, Cursor, Grok Build, OpenCode, Pi, omp, and fx on your existing subscriptions. macOS, Linux, and Windows.
  <sub>★ 4.1k · Rust · MIT · source · pushed 2026-11-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/hardbeat920/monocode.git`</sub>
- **[Zeron](https://github.com/zeronsh/zeron)** — Cross-device control plane for coding agents, syncing sessions across machines and keeping agents running on an always-on daemon. Claude Code, Codex, Cursor, Grok, Hermes, Pi.
  <sub>★ 3.7k · Rust · MIT · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://zeron.sh/install.sh | sh`</sub>
- **[Maestro](https://github.com/RunMaestro/Maestro)** — Cross-platform desktop command center for orchestrating a fleet of AI agents and projects; spec-driven Auto Run executes each task in a fresh session, built for long unattended runs. AGPL.
  <sub>★ 3.6k · TypeScript · AGPL-3.0 · clone · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/RunMaestro/Maestro.git`</sub>
- **[herdr-app](https://github.com/herdrdev/herdr-app)** — Desktop app for terminals and coding agents: keeps work in spaces, shows which agents need you, and leaves terminals running when you close the window.
  <sub>★ 3.2k · Rust · Apache-2.0 · psh · pushed 2026-11-18 · macOS</sub>
  <sub>`irm https://releases.herdr.dev/app/install.ps1 | iex`</sub>
- **[automaker](https://github.com/AutoMaker-Org/automaker)** — Describe features on a Kanban board and agents implement them in isolated worktrees, running tests and committing as they go.
  <sub>★ 3.2k · TypeScript · clone · pushed 2026-05-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/AutoMaker-Org/automaker.git`</sub>
- **[collaborator](https://github.com/collabs-inc/collab-public)** — Arranges terminals, editors, and files as tiles on an infinite pan-and-zoom canvas instead of tabs.
  <sub>★ 3.1k · TypeScript · script · pushed 2026-08-08 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/collaborator-ai/collab-public/main/install.sh | bash`</sub>
- **[CodeNomad](https://github.com/NeuralNomadsAI/CodeNomad)** — Desktop and web workspace around the OpenCode CLI whose SideCars embed local tools like VS Code and terminals as tabs.
  <sub>★ 2.7k · TypeScript · MIT · npx · pushed 2026-11-20 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx @neuralnomads/codenomad --password "your-password" --launch`</sub>
- **[supacode](https://github.com/supabitapp/supacode)** — Native macOS command center for worktree-per-agent development.
  <sub>★ 2.4k · Swift · source · pushed 2026-11-19 · macOS</sub>
  <sub>`git clone https://github.com/supabitapp/supacode.git`</sub>
- **[synara](https://github.com/Emanuele-web04/synara)** — GUI desktop workspace for running and managing agents across local projects.
  <sub>★ 2.3k · TypeScript · MIT · clone · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Emanuele-web04/synara.git`</sub>
- **[Happier](https://github.com/happier-dev/happier)** — Open-source, end-to-end encrypted, cross-device app to orchestrate Claude Code, Codex and other coding agents on your own machines from desktop, phone and web.
  <sub>★ 2.2k · TypeScript · MIT · npm · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @happier-dev/cli`</sub>
- **[Cate](https://github.com/0-AI-UG/cate)** — Open-source canvas IDE for agentic coding: editor, terminal, and browser panels in one infinite zoomable spatial workspace. MIT.
  <sub>★ 2.2k · TypeScript · MIT · brew · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask cate`</sub>
- **[nimbalyst](https://github.com/nimbalyst/nimbalyst)** — Visual workspace pairing parallel worktree sessions with kanban and direct visual editing. Claude Code, Codex, OpenCode.
  <sub>★ 2.1k · TypeScript · MIT · source · pushed 2026-11-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/nimbalyst/nimbalyst.git`</sub>
- **[xum](https://github.com/coder/xum)** — Desktop app for isolated, parallel agentic development.
  <sub>★ 2.1k · TypeScript · AGPL-3.0 · source · pushed 2026-11-20 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/coder/xum.git`</sub>
- **[Cloudroom](https://github.com/davidondrej/cloudroom)** — Desktop app for AI coding agents on your Mac or in the cloud: each thread gets its own sandbox and Git branch, running threads teleport between local and cloud, and the core is self-hostable.
  <sub>★ 1.8k · TypeScript · Apache-2.0 · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`git clone https://github.com/davidondrej/cloudroom.git`</sub>
- **[Traycer](https://github.com/traycerai/traycer)** — Bring-your-own-agent workspace running many sessions in parallel with context shared across models and providers, plus agent-to-agent messaging, shareable boards, and cross-device sync.
  <sub>★ 1.8k · TypeScript · MIT · source · pushed 2026-11-20 · macOS · Linux</sub>
  <sub>`git clone https://github.com/traycerai/traycer.git`</sub>
- **[Ghostex](https://github.com/maddada/Ghostex)** — Native macOS workspace (Rust/GPUI) running CLI agents side by side in low-RAM Ghostty terminals, with embedded browser and editor panes, a Kanban board, and iOS/Android session access. Claude Code, Codex, OpenCode.
  <sub>★ 1.7k · Rust · MIT · psh · pushed 2026-11-20 · Win · WSL2 · macOS · Linux?</sub>
  <sub>`irm https://ghostex.dev/install.ps1 | iex`</sub>
- **[Waku](https://github.com/egoist/waku)** — Native macOS desktop app for working with local coding agents, keeping projects, sessions, and transcripts on your machine. Supports Amp, Claude Code, Codex CLI, Cursor CLI, Grok Build, OpenCode, and Pi.
  <sub>★ 1.6k · Rust · GPL-3.0 · script · pushed 2026-10-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://waku.sh/install.sh | sh`</sub>
- **[Harness by Autonomous](https://github.com/autonomous-ai/openharness)** — Open-source desktop and mobile command center for supervising Claude Code, Codex, OpenCode, and other coding agents across machines.
  <sub>★ 1.5k · TypeScript · MIT · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://harness.autonomous.ai/cli/install.sh | bash`</sub>
- **[jean](https://github.com/coollabsio/jean)** — Desktop and web app for orchestrating agents across multiple projects and their git worktrees. Claude, Codex, OpenCode.
  <sub>★ 1.4k · TypeScript · Apache-2.0 · brew · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew tap coollabsio/jean`</sub>
- **[PandaCode](https://github.com/aicodeking/pandacode)** — Calm desktop workspace for coding agents, built with Tauri 2 on your OS webview; free, no account, no telemetry. MIT-based license requiring public forks to link back.
  <sub>★ 1.3k · TypeScript · npx · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx pandacode`</sub>
- **[Alethe](https://github.com/Kc1t/alethe-agents)** — Local-first desktop workspace where agents and shells run as real PTYs in split panes and custom grids across projects, surviving pane close and app restart. Suspend idle groups to reclaim memory and resume with scrollback intact. Claude Code, Codex, OpenCode.
  <sub>★ 1.2k · TypeScript · AGPL-3.0 · npx · pushed 2026-11-08 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx skills add Kc1t/alethe-orchestrate-skill`</sub>
- **[kandev](https://github.com/kdlbs/kandev)** — Kanban workbench whose multi-step workflows assign a different agent per step behind human gates, running locally, in Docker, over SSH, or in cloud executors.
  <sub>★ 1.2k · Go · AGPL-3.0 · scoop · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`scoop bucket add kandev https://github.com/kdlbs/scoop-kandev scoop install kandev`</sub>
- **[Cezar](https://github.com/open-mercato/cezar)** — Open-source orchestrator and ADE for running Claude Code, Codex, OpenCode, Pi, and other coding agents in parallel — locally or 24/7 on your own server.
  <sub>★ 1.1k · TypeScript · MIT · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cezar-run`</sub>
- **[parallel-code](https://github.com/johannesjo/parallel-code)** — Desktop app running Claude Code, Codex, and Gemini CLI side by side in isolated worktrees, with a built-in diff viewer and one-click merge.
  <sub>★ 1.1k · TypeScript · MIT · clone · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/johannesjo/parallel-code.git`</sub>
- **[takopi](https://github.com/banteg/takopi)** — Telegram bridge that puts Codex, Claude Code, OpenCode, and Pi sessions in a chat thread.
  <sub>★ 1.1k · Python · MIT · uv · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install -U takopi`</sub>
- **[Berd](https://github.com/block/berd)** — Block's open-source desktop app for working with AI agents: project chats with per-folder worktree behavior over the Goose backend, with agents, skills, connections, and agent sharing in one place.
  <sub>★ 1.1k · TypeScript · Apache-2.0 · source · pushed 2026-11-12 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/block/berd.git`</sub>
- **[IM.codes](https://github.com/im4codes/imcodes)** — Mobile and web control layer built for away-from-desk continuation, with terminal access, git views, localhost preview, and scheduled tasks. Claude Code, Codex, Gemini CLI.
  <sub>★ 965 · TypeScript · MIT · npm · pushed 2026-11-20 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g imcodes`</sub>
- **[ai-maestro](https://github.com/23blocks-OS/ai-maestro)** — Dashboard spanning multiple machines, adding memory search, code-graph queries, and agent-to-agent messaging. Claude, Aider, Cursor.
  <sub>★ 857 · TypeScript · MIT · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL aimaestro.sh/install | bash`</sub>
- **[Nuphos](https://github.com/nuphos/nuphos)** — Desktop and web workspace where a team runs Claude Code and Codex via ACP adapters across people and machines, with sessions that outlive any single laptop.
  <sub>★ 749 · TypeScript · source · pushed 2026-11-20 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/nuphos/nuphos.git`</sub>
- **[omg.dev](https://github.com/BennyKok/omg.dev)** — Open-source parallel-agent harness: run coding agents on your own computer or a hosted one, controlled from a single web UI with a mobile client. Claude Code, Codex, Grok, Cursor, OpenCode, Copilot, Pi.
  <sub>★ 560 · TypeScript · MIT · bun · pushed 2026-11-19 · WSL2 · macOS? · Linux</sub>
  <sub>`bun install --global @omg-dev/cli`</sub>
- **[Vicoa](https://github.com/vicoa-ai/vicoa)** — Agentic IDE and AI orchestrator for running a team of coding agents from desktop, web, or mobile, with real-time sync, parallel git worktrees, and push notifications. Claude Code, Codex, OpenCode, Gemini, Cursor, GitHub Copilot, Kimi, Hermes.
  <sub>★ 544 · Python · AGPL-3.0 · npm · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm i -g @vicoa/cli # Node.js 18+`</sub>
- **[Runner](https://github.com/yicheng47/runner)** — Native macOS and Windows app running CLI agents side by side in split panes, each keeping its own TUI in a real terminal, and putting them on one mission as a crew with a lead. Claude Code, Codex, Copilot CLI, pi.
  <sub>★ 542 · Rust · MIT · source · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/yicheng47/runner.git`</sub>
- **[diri](https://github.com/cristicretu/diri)** — Native macOS app running Claude Code, Codex, Cursor, Gemini, and shells in parallel across git worktrees or remote hosts, with live status, session persistence across restarts, a menu-bar rollup, and an MCP server for agents to spawn others.
  <sub>★ 498 · Rust · AGPL-3.0 · brew · pushed 2026-11-19 · macOS</sub>
  <sub>`brew install --cask diri`</sub>
- **[wmux](https://github.com/openwong2kim/wmux)** — Terminal workspace app for macOS and Windows that runs the real agent CLIs in parallel, with git worktree fan-out, agent-to-agent messaging, a fleet board, and a phone companion. Supports Claude Code, Codex, Gemini CLI, and OpenCode.
  <sub>★ 457 · TypeScript · MIT · winget · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`winget install openwong2kim.wmux # or: choco install wmux`</sub>
- **[Intent](https://github.com/intent-hq/intent)** — Desktop app for coordinating coding agents at scale: workspaces, notes, tasks, git, and terminals in one place, backed by a Rust daemon, with an iOS companion.
  <sub>★ 454 · JavaScript · Apache-2.0 · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/intent-hq/intent.git`</sub>
- **[Agentbox](https://github.com/savannahfeder/agentbox)** — Desktop app that runs each task in its own git worktree and brings it back as a row in an inbox or on a board, so you only hear from agents that finished or need you. Claude Code, Codex, OpenCode.
  <sub>★ 448 · TypeScript · GPL-3.0 · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentbox-app`</sub>
- **[Open Session](https://github.com/tellahq/opensession)** — Self-hosted server driving coding sessions in git worktrees on your own box or in isolated sandboxes, with a web UI, Slack/Linear/Plain/GitHub intake, diff and PR review, and multiple Codex and Claude subscriptions.
  <sub>★ 426 · TypeScript · MIT · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/tellahq/opensession/main/install.sh | bash`</sub>
- **[dorothy](https://github.com/Charlie85270/Dorothy)** — Desktop app combining agent orchestration with automations, Kanban management, and MCP servers.
  <sub>★ 357 · TypeScript · MIT · clone · pushed 2026-10-23 · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/Charlie85270/Dorothy.git`</sub>
- **[agentglass](https://github.com/SirAllap/agentglass)** — Desktop workspace for a fleet of coding agents: terminals that survive reboot, a built-in browser agents drive, live cost per session, a hold on risky actions, PR and task boards, and a phone companion. Claude Code, Codex, OpenCode, Gemini CLI.
  <sub>★ 349 · TypeScript · MIT · clone · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/SirAllap/agentglass`</sub>
- **[Termic](https://github.com/simion/termic)** — Open-source Conductor.build alternative that runs the real claude/gemini/codex CLIs in real terminals, no SDK middleman. AGPL.
  <sub>★ 336 · TypeScript · AGPL-3.0 · brew · pushed 2026-11-20 · macOS</sub>
  <sub>`brew install --cask simion/termic/termic`</sub>
- **[dev-3.0](https://github.com/h0x91b/dev-3.0)** — Mission control for the one-person studio: kanban, git worktrees, and tmux running a fleet of AI coding agents in parallel. Claude Code, Codex, Gemini CLI, OpenCode, and any shell agent. Apache.
  <sub>★ 335 · TypeScript · Apache-2.0 · brew · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`brew tap h0x91b/dev3`</sub>
- **[Kander](https://github.com/dualface/kander)** — Kanban board for coordinating multiple AI coding agents, with isolated git worktrees and independent reviewer agents. MIT.
  <sub>★ 331 · Go · MIT · brew · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install dualface/tap/kander`</sub>
- **[Roamgate](https://github.com/powerfooI/roamgate)** — Browser and PWA client for Herdr that controls parallel terminals, monitors coding agents, and reviews files and diffs from desktop or mobile. Requires a running Herdr server. Codex, Claude Code, Kimi, Grok Build, Pi, and more.
  <sub>★ 329 · TypeScript · MIT · source · pushed 2026-11-18 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/powerfooI/roamgate.git`</sub>
- **[aizen](https://github.com/vivy-company/aizen)** — macOS workspace that organizes worktrees, environments, and agent sessions per project.
  <sub>★ 311 · Swift · GPL-3.0 · clone · pushed 2026-08-01 · macOS</sub>
  <sub>`git clone https://github.com/vivy-company/aizen.git`</sub>
- **[Sculptor](https://github.com/imbue-ai/sculptor)** — Imbue's open-source tool for building product with grounded, parallel coding agents. MIT.
  <sub>★ 281 · Python · MIT · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/imbue-ai/sculptor.git`</sub>
- **[MulmoTerminal](https://github.com/receptron/mulmoterminal)** — Browser grid of live Claude Code / Codex sessions started with one `npx` command. Each cell is a real PTY with a colour-coded status, tmux-backed persistence, and a git worktree per cell. For Claude Code, needs-you is shown separately from done, read from the CLI's own hooks.
  <sub>★ 275 · TypeScript · MIT · npm · pushed 2026-11-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g mulmoterminal`</sub>
- **[vibe-tree](https://github.com/sahithvibudhi/vibe-tree)** — One git worktree per agent, delivered as desktop, web, and CLI.
  <sub>★ 273 · TypeScript · MIT · brew · pushed 2026-07-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask --no-quarantine sahithvibudhi/tap/vibetree`</sub>
- **[UpComputer](https://github.com/krl-gr/upcomputer)** — Desktop, web, and PWA app for task-based self-orchestration: task tags and statuses trigger agents that run on a schedule or from a webhook, in parallel or as a queue. Claude Code, Codex, Grok, OpenCode, Cursor, and more.
  <sub>★ 252 · TypeScript · MIT · source · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/krl-gr/upcomputer.git`</sub>
- **[zuse](https://github.com/swarajbachu/zuse)** — Chat-first desktop app wrapping Claude Code, Codex, Grok, Gemini, Cursor, and OpenCode in persistent sessions. macOS and Linux.
  <sub>★ 249 · TypeScript · AGPL-3.0 · script · pushed 2026-11-18 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/swarajbachu/zuse/main/scripts/install-linux.sh | sh`</sub>
- **[Claude Command Center (CCC)](https://github.com/amirfish1/claude-command-center)** — Local dashboard for spawning, monitoring, and resuming sessions across Claude Code, Codex, Cursor, Antigravity, and Kilo Code.
  <sub>★ 220 · Python · psh · pushed 2026-11-20 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/amirfish1/claude-command-center/main/scripts/install.ps1 | iex`</sub>
- **[constellagent](https://github.com/owengretzinger/constellagent)** — macOS app giving each agent its own terminal, editor, and git worktree in a single window.
  <sub>★ 217 · TypeScript · source · pushed 2026-05-05 · macOS</sub>
  <sub>`git clone https://github.com/owengretzinger/constellagent.git`</sub>
- **[ivy-tendril](https://github.com/Ivy-Interactive/Ivy-Tendril)** — Drives agents through a plan-based lifecycle with verification gates, self-improving memory, and human checkpoints. Claude Code, Codex, Antigravity, Copilot, OpenCode.
  <sub>★ 203 · C# · psh · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://cdn.ivy.app/install-tendril.ps1 | iex`</sub>
- **[Tempest](https://github.com/tempestai-dev/tempest)** — Tauri desktop ADE running CLI agents in parallel isolated worktrees, with a shared local code-knowledge graph that cuts token use across sessions, plus live status and built-in diff/PR review.
  <sub>★ 200 · TypeScript · Apache-2.0 · clone · pushed 2026-11-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/tempestai-dev/tempest`</sub>
- **[Antumi](https://github.com/flyhero/antumi)** — Multi-agent workbench for Claude Code, Codex, Cursor and more: see your quota, keep working when it runs out, run tasks in parallel, and let agents delegate. Apache.
  <sub>★ 196 · TypeScript · Apache-2.0 · clone · pushed 2026-11-20 · Win · WSL2 · macOS · Linux?</sub>
  <sub>`git clone https://github.com/flyhero/antumi.git`</sub>
- **[Ouijit](https://github.com/ouijit/ouijit)** — Kanban board and terminals wired together by lifecycle hooks, scripts, and a session-aware CLI, so a task runs by hand, on a script, or delegated to the agent. Per-task worktrees, optional VM sandboxing. Claude Code, Codex, Pi, OpenCode.
  <sub>★ 184 · TypeScript · AGPL-3.0 · clone · pushed 2026-11-20 · macOS · Linux</sub>
  <sub>`git clone https://github.com/ouijit/ouijit.git`</sub>
- **[clideck](https://github.com/rustykuntz/clideck)** — Chat-app-style dashboard with autopilot routing between agents and full control from a phone. Claude Code, Codex, Gemini CLI, OpenCode.
  <sub>★ 162 · JavaScript · MIT · npm · pushed 2026-10-30 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g clideck@2`</sub>
- **[GraphCode](https://github.com/scgopi/GraphCode)** — macOS app that wires agent sessions into a graph: each node is a live terminal you can attach to mid-run, each edge a hand-off, message, or spawn that fires while you're away. Claude Code, Codex, Copilot CLI, OpenCode, pi.
  <sub>★ 159 · Swift · brew · pushed 2026-11-19 · Win? · macOS</sub>
  <sub>`brew install --cask scgopi/graphcode/graphcode`</sub>
- **[KanVibe](https://github.com/rookedsysc/kanvibe)** — Keyboard-first desktop Kanban workspace for AI coding agents with embedded terminals, git worktrees, and hook-driven task tracking. AGPL.
  <sub>★ 151 · TypeScript · AGPL-3.0 · brew · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask rookedsysc/kanvibe/kanvibe`</sub>
- **[Kangentic](https://github.com/Kangentic/kangentic)** — Agentic development environment for AI coding agents. AGPL.
  <sub>★ 149 · TypeScript · AGPL-3.0 · npx · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx kangentic`</sub>
- **[ADE](https://github.com/arul28/ADE)** — Local-first desktop app for orchestrating parallel AI coding agents, with isolated git worktrees, automation rules, and built-in agent tools, synced across desktop, web, and iPhone. AGPL.
  <sub>★ 146 · TypeScript · AGPL-3.0 · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`irm https://ade-app.dev/install.ps1 | iex`</sub>
- **[Dray](https://github.com/monorepo-labs/dray)** — Native desktop app wrapping Claude Code, Codex, fx, and pi in a chat UI, with one worktree per session plus diff, PR, and issue panels and an embedded browser.
  <sub>★ 143 · Rust · Apache-2.0 · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://www.drayhq.com/install.sh | sh`</sub>
- **[Sesori](https://github.com/sesori-ai/sesori_apps_monorepo)** — Free desktop app (macOS, Linux) and iOS/Android app that follow the same agent sessions on your computer and phone, notify you the moment an agent needs an answer, and let you reply or dictate from either; code stays on your computer and the relay sees only ciphertext. Claude Code, Codex, OpenCode, GitHub Copilot CLI, Cursor, Pi, OMP, Hermes, DeepSeek Harness, Grok Build. FSL-1.1-ALv2.
  <sub>★ 143 · Dart · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://sesori.com/install.ps1 | iex`</sub>
- **[Open Walnut](https://github.com/EvanZhang008/open-walnut)** — Self-hosted web UI for coding sessions on your laptop and remote dev boxes, with a daemon on each host that keeps sessions running when SSH drops, a per-session diff of every file changed, and tasks and notes alongside. Claude Code.
  <sub>★ 140 · TypeScript · MIT · npm · pushed 2026-11-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g open-walnut`</sub>
- **[Agetor](https://github.com/alamops/agetor)** — The harness orchestrator: local-first kanban for running Claude Code, Codex, and other CLI coding agents in parallel, each in its own git worktree. MIT.
  <sub>★ 136 · TypeScript · MIT · script · pushed 2026-11-20 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://github.com/alamops/agetor/releases/latest/download/install.sh | sh`</sub>
- **[Poracode](https://github.com/Porabuild/Poracode)** — One window for all your AI coding agents: run Claude, Codex, OpenCode, Gemini, Antigravity, Cursor, and Copilot side-by-side with terminal and chat in any layout. Apache.
  <sub>★ 123 · TypeScript · Apache-2.0 · psh · pushed 2026-11-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://poracode.com/install.ps1 | iex # Windows PowerShell`</sub>
- **[tlbx](https://github.com/tlbx-ai/tlbx)** — Self-hosted browser workspace holding persistent real PTY sessions on your own machines, reachable from any browser or phone.
  <sub>★ 119 · C# · AGPL-3.0 · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://get.tlbx.ai/install.ps1 | iex`</sub>
- **[Muxflow](https://github.com/gal064/muxflow)** — Remote-first tmux IDE for desktop and Android: sessions stay in tmux on local or SSH hosts, with notifications when Claude Code, Codex, or Pi needs input, screenshot paste over SSH, and files, Git, and ports panels.
  <sub>★ 118 · TypeScript · MIT · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/gal064/muxflow/releases/latest/download/install.sh | bash`</sub>
- **[Helicon](https://github.com/HarjjotSinghh/helicon)** — Unofficial desktop and web app, not affiliated with Meta, that puts threads from every project in one sidebar with inline diffs, approvals, cost tracking, and a VS Code and Cursor extension. Muse Code.
  <sub>★ 114 · TypeScript · MIT · source · pushed 2026-11-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/HarjjotSinghh/helicon.git`</sub>
- **[Garcon](https://github.com/cfal/garcon)** — Self-hosted browser and mobile workspace with diff review, Git/PR workflows, mobile approvals, scheduling, and cross-agent transfers. Seven CLI agents.
  <sub>★ 105 · TypeScript · clone · pushed 2026-11-20 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/cfal/garcon.git`</sub>
- **[Tortie](https://github.com/gregce/tortie)** — Native macOS agent multiplexer with familiar IDE features: all projects in one window, agents that survive restarts, and organized terminal sessions without tmux.
  <sub>★ 97 · TypeScript · Apache-2.0 · source · pushed 2026-11-18 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/gregce/tortie.git`</sub>
- **[intentic](https://github.com/intentic/intentic)** — Browser and mobile workspace where every agent gets a persistent Docker sandbox on a machine you own plus a git worktree of its own, reached over an outbound-only Cloudflare tunnel, so runs keep going after you close the tab. Plan mode, per-hunk diff review, an environment Dockerfile the agent proposes and you approve, credential capabilities injected per turn, and schedule, webhook or event triggers. Claude Code, Codex, Grok, Kimi Code, Gemini. MIT.
  <sub>★ 96 · TypeScript · MIT · script · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://intentic.dev/connect | sh -s -- <SETUP_CODE>`</sub>
- **[Claudette](https://github.com/utensils/claudette)** — Companion app for Claude Code that runs parallel agents in isolated git worktrees, with plan approvals, checkpoints, workspace forking, and a CLI a main agent can use to fan out work. MIT.
  <sub>★ 88 · TypeScript · MIT · source · pushed 2026-11-09 · macOS · Linux</sub>
  <sub>`git clone https://github.com/utensils/claudette.git`</sub>
- **[Friday](https://github.com/splashxmoon/friday)** — Cross-platform desktop app where agents split work on a shared task board, message each other, and hand a task to another agent with its progress when one hits its usage limit, each in its own git worktree with diff review. Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, and any ACP agent.
  <sub>★ 83 · TypeScript · MIT · npx · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx github:splashxmoon/friday`</sub>
- **[Prometeu](https://github.com/prometeucorp/prometeu)** — Free, open-source desktop app to run Claude Code, Codex, Cursor CLI, and Antigravity agents in parallel with git worktrees and diff review. MIT.
  <sub>★ 67 · Rust · MIT · source · pushed 2026-11-19 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`git clone https://github.com/prometeucorp/prometeu.git`</sub>
- **[Zaivern Code](https://github.com/tacyan/zaivern-code)** — Cross-platform Rust desktop cockpit for running Claude Code, Codex, Gemini CLI, and 30+ coding agents in parallel, with fleet monitoring, mobile control, and line-level ownership to prevent merge conflicts.
  <sub>★ 58 · Rust · Apache-2.0 · psh · pushed 2026-11-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/tacyan/zaivern-code/main/install.ps1 | iex`</sub>
- **[Novadeck](https://github.com/novadeck-org/novadeck)** — Desktop terminal that runs Claude Code, Codex, and Antigravity side by side in Focus, Grid, and Canvas views, with one Inbox for their questions, approvals, and reports. GPL-3.0.
  <sub>★ 54 · TypeScript · GPL-3.0 · script · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://novadeck.dev/install.sh | sh`</sub>
- **[AI4Kanban](https://github.com/wildcrane-ai/wildcrane)** — AI project manager that turns rough ideas into actionable tasks, coordinates coding agents through planning and implementation, and builds shared project memory from decisions. Humans steer priorities and make key decisions through a desktop and web interface.
  <sub>★ 52 · TypeScript · Apache-2.0 · source · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ai4kanban/ai4kanban.git`</sub>
- **[DockTerm](https://github.com/munvard/dockterm)** — Cross-platform terminal workspace that runs the real Claude Code in one pane per project, with a live sub-agent view, diff review, Git, and permission prompts that pop out of the Mac notch.
  <sub>★ 52 · TypeScript · MIT · brew · pushed 2026-10-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask munvard/dockterm/dockterm`</sub>
- **[clave](https://github.com/antasphere/clave)** — Native macOS app with split and grid layouts, session groups, SSH remote sessions, and usage analytics for Claude Code.
  <sub>★ 51 · TypeScript · MIT · npx · pushed 2026-11-19 · macOS</sub>
  <sub>`npx plugins add antasphere/clave`</sub>
- **[Podium ADE](https://github.com/madeinorbit/podium)** — Open-source workspace for taking ideas from conversation to coordinated work with coding agents. A shared task system lets them organize the effort while developers follow progress and change direction.
  <sub>★ 51 · TypeScript · Apache-2.0 · script · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://podium.do/install.sh | sh`</sub>
- **[Caprock](https://github.com/dspv/caprock)** — Desktop app with a phone companion that runs coding agents side by side and shows who is waiting on you, what each session and pull request cost at API list prices, and how close the plan limit is; local, no account. Linux, macOS, Windows. Claude Code, Codex, OpenCode, Gemini CLI. Apache-2.0.
  <sub>★ 50 · Go · Apache-2.0 · scoop · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add dspv https://github.com/dspv/scoop-bucket scoop install caprock`</sub>
- **[Threadlines](https://github.com/Threadlines/threadlines)** — Desktop app where each thread can run in its own Git worktree beside a live browser, terminal, and source control, and a second agent can join a thread to answer questions or review the first one's changes. Claude Code, Codex, OpenCode, Cursor, Antigravity, fx, and agents from the ACP registry.
  <sub>★ 50 · TypeScript · MIT · npx · pushed 2026-11-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @threadlines/server@latest --help`</sub>
- **[muxel](https://github.com/ProjectHax/muxel)** — GPU-accelerated native desktop multiplexer (not a TUI) where every pane embeds a real terminal running a coding agent, with first-class git worktrees, live agent status, scheduled runs, and notifications.
  <sub>★ 46 · Rust · GPL-3.0 · psh · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://muxel.sh/install.ps1 | iex`</sub>
- **[Yardlet](https://github.com/zzunkie/yardlet)** — Native macOS app that runs each agent's own CLI and sign-in side by side, keeping sessions in the agent's own store, with handoff between tasks, usage limits across accounts, shared MCP connectors, and a browser the agents drive. Claude Code, Codex, OpenCode, Cursor Agent, Antigravity CLI, Pi.
  <sub>★ 46 · Swift · MIT · brew · pushed 2026-11-20 · macOS · Linux</sub>
  <sub>`brew install --cask zzunkie/tap/yardlet`</sub>
- **[Delegatus](https://github.com/Latand/delegatus)** — Local web board run by an orchestrator agent you message: it turns requests into tasks, runs each through build and fresh read-only review stages in its own git worktree until a pull request is ready, and brings decisions to you in the browser, on your phone or in Telegram. Claude Code and Codex, with Copilot for single agents.
  <sub>★ 40 · TypeScript · MIT · npx · pushed 2026-11-20 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`bunx delegatus-cli`</sub>
- **[Superagent](https://github.com/pungme/superagent-desktop)** — macOS desktop app giving Claude Code and Codex a real browser to drive, an iOS Simulator to install and screenshot apps in, and a phone companion app for remote monitoring.
  <sub>★ 37 · TypeScript · MIT · source · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/pungme/superagent-desktop.git`</sub>
- **[Sikemux](https://github.com/nodelike/sikemux)** — A whole team of AI coders in one window: native Rust app for macOS and Linux that runs Claude Code, Codex, OpenCode, Hermes and Pi at once, each chat with its own worktree and browser tabs, still running after you quit, with iOS and Android apps. MIT.
  <sub>★ 36 · Rust · MIT · brew · pushed 2026-11-20 · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask nodelike/tap/sikemux`</sub>
- **[Verde](https://github.com/JonathanRiche/verde)** — Native Zig desktop workspace running Claude Code, Codex, Cursor, OpenCode and more side by side with built-in terminal and browser; local-first, MIT, Linux/macOS/Windows. [verdeai.dev](https://verdeai.dev)
  <sub>★ 36 · Zig · MIT · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://verdeai.dev/install.ps1 | iex`</sub>
- **[vibecraft](https://github.com/rayzhudev/vibecraft)** — RTS-style workspace for commanding coding agents.
  <sub>★ 36 · TypeScript · Apache-2.0 · source · pushed 2026-11-04 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/rayzhudev/vibecraft.git`</sub>
- **[Fletch](https://github.com/fwdai/fletch)** — Native macOS IDE that seals each agent in its own repo clone under Seatbelt or Docker, serves each a shared symbol and call-graph index over MCP, and gates every step on tests or your approval. Claude Code, Codex, Cursor, OpenCode.
  <sub>★ 35 · Rust · AGPL-3.0 · source · pushed 2026-11-20 · macOS</sub>
  <sub>`git clone https://github.com/fwdai/fletch.git`</sub>
- **[AGX](https://github.com/ramarlina/agx)** — Wake-work-sleep checkpointing keeps a persistent agent team on long objectives, with human gates between cycles.
  <sub>★ 33 · TypeScript · npm · pushed 2026-05-06 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g @mndrk/agx`</sub>
- **[Volt](https://github.com/LeulAria/volt)** — Open-source agentic workspace on the VS Code core that runs agent chats side by side, each optionally in its own Git worktree, with subagents, hunk-level keep or undo of agent edits, and a Git checkpoint per turn. Claude Code, Codex, OpenCode, Cursor, Grok, Antigravity, Kimi, and any ACP agent, plus local models through Ollama.
  <sub>★ 33 · TypeScript · MIT · script · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/LeulAria/volt/main/install.sh | bash`</sub>
- **[Reemoat](https://github.com/rends-east/reemoat)** — Self-hosted remote control for any coding agent: run coding agents on your own machines and supervise them from anywhere, end-to-end encrypted.
  <sub>★ 32 · TypeScript · AGPL-3.0 · script · pushed 2026-11-04 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/rends-east/reemoat/releases/latest/download/install.sh | sh`</sub>
- **[Perch](https://github.com/asafofer/perch)** — Native macOS app in the notch for supervising parallel agent sessions: shows when one finishes or needs approval, lets you allow, deny, or reply with one key, and jumps to the exact terminal tab, cmux split, herdr pane, or Conductor workspace. Local-only, no account. Claude Code, Codex, OpenCode, Pi.
  <sub>★ 31 · Swift · MIT · clone · pushed 2026-11-16 · macOS</sub>
  <sub>`git clone https://github.com/asafofer/perch.git`</sub>
- **[agent-session-manager-desktop](https://github.com/izll/agent-session-manager-desktop)** — Desktop GUI over tmux where each session holds agent and shell tabs with per-tab working directories; waiting agents raise a header counter you can answer without switching tabs, and ntfy push carries it to your phone. Linux, macOS, Windows. Claude Code, Codex, Gemini, Aider.
  <sub>★ 30 · Go · MIT · source · pushed 2026-11-13 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/izll/agent-session-manager-desktop.git`</sub>
- **[alas](https://github.com/mrmans0n/alas)** — Native macOS workspace for the whole agent loop: libghostty terminals or native chat panes across every worktree, on your Mac or over SSH, with comment-based review, in-app merge, and pickup from your phone.
  <sub>★ 25 · Swift · MIT · brew · pushed 2026-11-20 · macOS</sub>
  <sub>`brew install --cask mrmans0n/tap/alas`</sub>
- **[octomux](https://github.com/ShreyPaharia/octomux)** — Local dashboard with a kanban fleet view, one unified permission inbox across agents, and in-app diff review.
  <sub>★ 25 · TypeScript · MIT · npm · pushed 2026-09-18 · macOS</sub>
  <sub>`npm install -g octomux`</sub>
- **[Pragma](https://github.com/pragma-sh/pragma)** — Native desktop app running agent teams in parallel worktrees, each with its own branch and GPU-accelerated terminals, with a task board from prompt to PR, fan-out races that compare agents on one prompt, and a public plugin API. Desktop, web, and mobile, locally, over SSH, or in WSL. Claude Code, Codex, OpenCode, Cursor.
  <sub>★ 25 · TypeScript · AGPL-3.0 · clone · pushed 2026-11-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/pragma-sh/pragma.git`</sub>
- **[Althar](https://github.com/AltharIDE/althar)** — Desktop ADE that assigns coding tasks to agents such as Claude Code, Codex, and OpenCode and hands their changes to a separate model for review.
  <sub>★ 22 · TypeScript · Apache-2.0 · brew · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask altharide/tap/althar`</sub>
- **[pitwall](https://github.com/quanticstudios/pitwall)** — Desktop terminal for parallel coding agents with workers in separate Git worktrees, a live status sidebar, an inbox for waiting agents, and diff review. Linux, macOS, Windows. Claude Code, Codex, OpenCode, Gemini CLI, Cursor CLI, pi, Oh My Pi.
  <sub>★ 22 · Go · MIT · scoop · pushed 2026-11-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop bucket add quanticstudios https://github.com/quanticstudios/scoop-bucket scoop install pitwall # Windows, with Scoop`</sub>
- **[Skiff](https://github.com/solutionscay/skiff)** — Desktop app where Skipper agents hand tasks to other agent sessions and track them in a ledger, with a Mission control view of the whole tree. A daemon keeps every terminal alive when the window closes. Linux, macOS. Claude Code, Codex, Gemini, Grok, OpenCode, Hermes.
  <sub>★ 21 · Rust · MIT · source · pushed 2026-11-20 · macOS · Linux</sub>
  <sub>`git clone https://github.com/solutionscay/skiff.git`</sub>
- **[Solenta](https://github.com/currentbits/solenta)** — Desktop app where every thread shares one local memory and the plan is your GitHub issues, with worktrees, Git review in the loop, and verify-gated completion. Claude Code, Codex, Cursor, Kimi, Grok, OpenCode.
  <sub>★ 20 · JavaScript · MIT · source · pushed 2026-11-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/currentbits/solenta.git`</sub>
- **[SpaceApp](https://github.com/oll4com/spaceapp)** — Self-hosted web workspace that runs coding CLIs side by side as terminal panes in persistent rooms, reachable from a computer or phone, with managed browser panes and shared MCP servers. OpenCode, Codex, Claude Code, Gemini CLI, Qwen, Kimi, Grok, DeepSeek, and more.
  <sub>★ 20 · TypeScript · MIT · npm · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g run-spaceapp`</sub>
- **[agent-squid](https://github.com/agent-squid/squid)** — Browser UI organized into named lanes (`#topic@agent`), with context shared across agents and a realtime quota gauge.
  <sub>★ 19 · Python · MIT · script · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://agentsquid.ai/install.sh | bash`</sub>
- **[ateam](https://github.com/clawnify/ateam)** — macOS and iPhone app orchestrating Claude Code, OpenCode, and Codex crews, each isolated in its own git worktree.
  <sub>★ 18 · TypeScript · script · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/clawnify/ateam/main/packages/server/scripts/install.sh | bash`</sub>
- **[EvoFlux](https://github.com/evoelsewhere/evo-harness)** — Local-first desktop workspace coordinating specialist AI agents across conversations, files, terminal, browser, Git, memory, and verification.
  <sub>★ 16 · Rust · Apache-2.0 · clone · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/evoelsewhere/evo-harness.git`</sub>
- **[MultiCC](https://github.com/lsjwzh/MultiCC)** — Self-hosted workspace where one chat task and its git worktree survive switching from Claude Code to Codex, OpenCode, or another agent; parallel tasks run in isolated worktrees and the same host is reachable from desktop, web, and mobile.
  <sub>★ 15 · JavaScript · MIT · psh · pushed 2026-11-20 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/lsjwzh/MultiCC/v2.21.0/install.ps1 | iex`</sub>
- **[WSP](https://github.com/wsp-labs/wsp)** — Orchestrates Claude Code, Codex, OpenCode, and Cursor across machines and cloud workspaces, syncing memory, skills, MCPs, plugins, tools, and configuration into each workspace; its desktop app, CLI, and MCP let developers or agents coordinate the same thread fleet from their preferred environment.
  <sub>★ 15 · TypeScript · AGPL-3.0 · npm · pushed 2026-11-13 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g @wsp-labs/wsp`</sub>
- **[OpenTandem](https://github.com/opentandem/opentandem)** — Web and mobile workspace that connects the computers you run agents on, so you can start, switch, and follow tasks from your phone. Claude Code, Codex, OpenCode, and 15 more; the CLI and Runner are open source (AGPL-3.0).
  <sub>★ 14 · JavaScript · AGPL-3.0 · psh · pushed 2026-11-05 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://opentandem.org/install.ps1 | iex; opentandem remote`</sub>
- **[Yardsort](https://github.com/joaoh82/yardsort)** — Cross-platform Tauri desktop app giving each task its own git worktree and real terminal, with live per-file diffs, agent hand-offs, YAML workflows, and terminals that keep running after the window closes.
  <sub>★ 14 · Rust · GPL-3.0 · winget · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install joaoh82.Yardsort`</sub>
- **[Sillage](https://github.com/MarlBurroW/sillage)** — Self-hosted, mobile-first web UI that drives the native CLIs on your own machine, with server-side event journals so sessions outlive the client, git worktrees, per-conversation full-text search, an IDE panel (file explorer, editor, diffs, terminal), a board the agents read over its own MCP server, and an installable PWA with push. Single Docker container. Claude Code, Codex. MIT.
  <sub>★ 13 · TypeScript · MIT · script · pushed 2026-11-19 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/MarlBurroW/sillage/main/install.sh | bash`</sub>
- **[TaskHandoff](https://github.com/edgestorage/task-handoff)** — Self-hosted web control plane that runs Codex sessions in isolated Docker workspaces on local and remote machines, with per-task checkouts, a diff review gate, and planner/executor/human handoff.
  <sub>★ 11 · TypeScript · Apache-2.0 · script · pushed 2026-11-20 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://github.com/edgestorage/task-handoff/releases/latest/download/install-server.sh | sudo sh`</sub>
- **[Agent Console](https://github.com/cyl-castillo/agent-console)** — Terminal-first Tauri desktop app that runs the real agent CLIs in PTYs with per-turn snapshots, diff review, and rewind, and witnesses every prompt, approval, and tool result into a hash-chained ledger exportable as a signed proof packet or an IETF audit trail anyone verifies offline; multi-engine rooms, push-to-talk voice with local TTS, and an MCP server so agents can drive the console. Linux, macOS, Windows. Claude Code, Codex.
  <sub>★ 10 · Rust · AGPL-3.0 · winget · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install CylCastillo.AgentConsole`</sub>
- **[Alchemist Coder](https://github.com/Alekla0126/alchemist-coder)** — Desktop app that shows each agent and every subagent it spawns as a live tree, runs up to four agents on one approved plan in separate Git worktrees, and has a coordinator agent that hands work to agents you configure. Runs Claude Code and Codex over ACP on local models (Ollama, LM Studio); macOS, Windows, Linux.
  <sub>★ 10 · TypeScript · AGPL-3.0 · source · pushed 2026-11-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Alekla0126/alchemist-coder.git`</sub>
- **[Lookout for VS Code](https://github.com/nimrod-teich/lookout)** — VS Code extension that puts every agent session on one board in the side bar, quotes what a waiting session asks (the command, file or question), jumps to a session's tab or terminal in any VS Code window with one key, and searches every conversation. Reads only what the agents already write on disk, with no hooks, and does not launch agents. Claude Code, Codex, Copilot CLI. MIT.
  <sub>★ 6 · TypeScript · MIT · clone · pushed 2026-11-16 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nimrod-teich/lookout.git`</sub>
- **[Moonfold](https://github.com/Mr-Dark-debug/Moonfold)** — Desktop and web workspace running agents in git worktrees on your own machine, with an Android app paired by QR code and a handoff that continues a task in another agent when one hits its usage limit. Codex, Claude Code, Cursor, Gemini CLI, OpenCode, and more.
  <sub>★ 6 · TypeScript · MIT · psh · pushed 2026-11-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/Mr-Dark-debug/Moonfold/main/scripts/install.ps1 | iex`</sub>
- **[Proliferate](https://github.com/proliferate-ai/proliferate)** — Agent IDE that runs sessions locally or in the cloud and lets you build reusable workflows from them.
  <sub>unavailable</sub>

## Multi-Agent Swarms

- **[paperclip](https://github.com/paperclipai/paperclip)** — Self-hosted platform where agents wake on heartbeats to claim tickets, governed by org charts, budgets, and approval gates.
  <sub>★ 115.3k · TypeScript · MIT · npx · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx paperclipai@latest onboard --yes`</sub>
- **[ruflo](https://github.com/ruvnet/ruflo)** — Meta-harness for deploying coordinated swarms and conversational multi-agent workflows. Formerly claude-flow.
  <sub>★ 82.1k · TypeScript · MIT · npm · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g ruflo@latest`</sub>
- **[crewAI](https://github.com/crewAIInc/crewAI)** — Framework for orchestrating role-playing, autonomous AI agents that collaborate through defined roles, tools, and task delegation.
  <sub>★ 61.1k · Python · MIT · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add crewaiinc/skills`</sub>
- **[buzz](https://github.com/block/buzz)** — Agents are first-class members of shared channels on a Nostr relay you own, with their own keys and audit trails. Claude Code, Codex, Goose.
  <sub>★ 37.6k · Rust · Apache-2.0 · clone · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/block/buzz.git`</sub>
- **[Mastra](https://github.com/mastra-ai/mastra)** — TypeScript framework for building and orchestrating AI agents and workflows, with memory, tools, evals, and MCP support.
  <sub>★ 29.7k · TypeScript · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git`</sub>
- **[gastown](https://github.com/gastownhall/gastown)** — Scales to 20-30 agents with a coordinator, git-backed issue tracking, health watchdogs, and a Bors-style merge queue.
  <sub>★ 18.8k · Go · MIT · go · pushed 2026-11-14 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/steveyegge/gastown/cmd/gt@latest`</sub>
- **[Orkas](https://github.com/Orkas-AI/Orkas)** — A commander agent decomposes goals and dispatches specialists with isolated skills and memory. Claude Code, Codex, OpenCode, OpenClaw, Hermes.
  <sub>★ 9.5k · JavaScript · MIT · clone · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Orkas-AI/Orkas.git`</sub>
- **[OpenRig](https://github.com/mvschwarz/openrig)** — YAML-defined agent team with a lead agent that runs Claude Code and Codex together as one persistent system in tmux. npm CLI.
  <sub>★ 8.9k · TypeScript · Apache-2.0 · npm · pushed 2026-11-20 · macOS</sub>
  <sub>`npm install -g @openrig/cli`</sub>
- **[Raven](https://github.com/EverMind-AI/Raven)** — Host agent that plans a complex task as a DAG and coordinates dependencies and parallel execution across built-in research, coding, design, and on-call agents and third-party agents over ACP, CLI, or OpenAI-compatible APIs. Presets include Claude Code, Codex, OpenCode, OpenClaw, Hermes Agent, GitHub Copilot, Qwen Code, and Kimi Code.
  <sub>★ 6.3k · Python · Apache-2.0 · psh · pushed 2026-11-20 · Win · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`irm https://raven.evermind.ai/install.ps1 | iex`</sub>
- **[ClawTeam](https://github.com/HKUDS/ClawTeam)** — Agents spawn and manage their own teammates from one command, coordinating through file-based or P2P inboxes across tmux worktrees.
  <sub>★ 5.6k · Python · MIT · pip · pushed 2026-05-09 · WSL2 · macOS? · Linux</sub>
  <sub>`pip install clawteam`</sub>
- **[Switch](https://github.com/sandbox-quantum/switch)** — Self-hosted server and desktop console that run coding agents as members of Slack, Microsoft Teams, Discord, Telegram and Mattermost channels, where people and several agents work in one thread with shared context. Claude Code, Codex, Cursor, OpenCode, GitHub Copilot, Goose, Kiro, Qwen Code and 7 more. Source-available under Apache-2.0 with Commons Clause.
  <sub>★ 4.7k · Python · source · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/sandbox-quantum/switch.git`</sub>
- **[claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge)** — Workspace for mixing different vendors' CLI agents in one visible collaboration session.
  <sub>★ 3.6k · Python · npm · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @seemseam/ccb@latest`</sub>
- **[Atomic Agent](https://github.com/AtomicBot-ai/atomic-agent)** — Local-first desktop and terminal agent whose Fusion mode has one model plan, brief and review while a pool of worker sessions builds the parts in parallel, with a spend cap per turn and optional git worktree per worker. Local llama.cpp models, OpenRouter and other OpenAI-compatible providers, on either side.
  <sub>★ 3.6k · TypeScript · MIT · psh · pushed 2026-11-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm "https://atomicagent.io/install.ps1?from=github" | iex`</sub>
- **[Agent Teams](https://github.com/777genius/agent-teams-ai)** — Desktop app where you give high-level commands to autonomous coding-agent teams across Claude Code, Codex, OpenCode, Cursor, Grok, GitHub Copilot, Kiro, Z.AI, MiniMax, Kimi, 200+ models, and 75+ LLM providers. Agents coordinate through inter-agent messaging, Kanban tasks, and built-in code review.
  <sub>★ 2.5k · TypeScript · AGPL-3.0 · clone · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/777genius/agent-teams-ai.git`</sub>
- **[scion](https://github.com/GoogleCloudPlatform/scion)** — Orchestration testbed running agents in parallel isolated containers with dynamic coordination and normalized telemetry.
  <sub>★ 2.1k · Go · Apache-2.0 · brew · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew tap homebrew-scion/scion`</sub>
- **[CLI Agent Orchestrator (CAO)](https://github.com/awslabs/cli-agent-orchestrator)** — Multi-agent orchestration for AI coding CLIs — Claude Code, Kiro, Codex, and more, coordinated in isolated tmux sessions.
  <sub>★ 1.6k · Python · Apache-2.0 · uv · pushed 2026-11-20 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install git+https://github.com/awslabs/cli-agent-orchestrator.git@main --upgrade`</sub>
- **[Alook](https://github.com/alookai/alook)** — Shared rooms where people and agents collaborate: local coding agents get persistent identities with handles, inboxes, and memberships, while agents keep running on your own machine.
  <sub>★ 1.5k · TypeScript · Apache-2.0 · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @alook/app onboard`</sub>
- **[multi-agent-shogun](https://github.com/yohey-w/multi-agent-shogun)** — Shogun to karo to ashigaru hierarchy running up to 10 agents over tmux with no coordination API cost.
  <sub>★ 1.4k · Shell · MIT · clone · pushed 2026-08-06 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/yohey-w/multi-agent-shogun`</sub>
- **[Commonly](https://github.com/Team-Commonly/commonly)** — Open-source workspace where people and agents share a pod with chat, memory, a task board and files. Claude Code and Codex (on a Mac) attach with one command and answer @mentions.
  <sub>★ 1.4k · JavaScript · Apache-2.0 · npm · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @commonlyai/cli@latest`</sub>
- **[Fusion](https://github.com/Runfusion/Fusion)** — Multi-node orchestrator with a kanban board, plan-review-execute gates, per-task worktrees, and hierarchical missions.
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-11-08 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @runfusion/fusion`</sub>
- **[loki-mode](https://github.com/asklokesh/loki-mode)** — PRD-to-deployed-product SDLC with 41 agents in 8 swarms, nine quality gates, and blind three-reviewer code review. Source-available under BUSL-1.1.
  <sub>★ 1.1k · Shell · npm · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g loki-mode`</sub>
- **[agent-swarm](https://github.com/desplega-ai/agent-swarm)** — Self-hosted AI company operating system where a lead agent delegates goals to workers in isolated containers, with persistent memory, schedules, and review gates. Claude Code, Codex, pi, OpenCode, Cursor, Amp, Grok, Devin, and ACP agents.
  <sub>★ 1.1k · TypeScript · MIT · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add desplega-ai/agent-swarm`</sub>
- **[Sno Station](https://github.com/sno-ai/sno-station)** — Local runtime where agents share one encrypted memory and a mailbox, hand a task to another agent when one hits its usage limit, and review each other's work across vendors. Codex, Claude Code, Cursor, Hermes, OpenClaw.
  <sub>★ 1k · TypeScript · Apache-2.0 · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://sno.ai/install | sh`</sub>
- **[openswarm](https://github.com/openswarm-ai/openswarm)** — Local mission-control center for launching, monitoring, approving, and coordinating multiple AI agents in parallel.
  <sub>★ 826 · JavaScript · source · pushed 2026-11-18 · Win · macOS</sub>
  <sub>`git clone https://github.com/openswarm-ai/openswarm.git`</sub>
- **[hcom](https://github.com/aannoo/hcom)** — Lets agents message, watch, and spawn each other across terminals. Claude Code, Codex, Antigravity, Cursor, OpenCode, Kilo, and more.
  <sub>★ 665 · Rust · MIT · psh · pushed 2026-10-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://github.com/aannoo/hcom/releases/latest/download/hcom-installer.ps1 | iex`</sub>
- **[agent-kanban](https://github.com/saltbo/agent-kanban)** — Leader-worker task board with cryptographic agent identity. Claude Code, Codex, Gemini CLI.
  <sub>★ 506 · TypeScript · clone · pushed 2026-11-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/saltbo/agent-kanban.git`</sub>
- **[Coworkers](https://github.com/fayazara/coworkers)** — AI teammates that each get their own computer and browser, built entirely on Cloudflare: give each bot a job and it works while you're away, asking before anything risky.
  <sub>★ 445 · TypeScript · MIT · clone · pushed 2026-11-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fayazara/coworkers`</sub>
- **[AgentBridge](https://github.com/raysonmeng/agent-bridge)** — Local MIT CLI that keeps Claude Code and Codex as live peers in one session for mid-turn review, task split, and quota-boundary handoff.
  <sub>★ 434 · TypeScript · MIT · npm · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @raysonmeng/agentbridge`</sub>
- **[Rovai AI](https://github.com/murray17/rovai-ai)** — Desktop and web workspace where persistent teams of Claude Code, Codex CLI, OpenCode, and Pi agents collaborate through shared conversations, task delegation, and collaborative memory.
  <sub>★ 275 · Rust · MIT · clone · pushed 2026-11-20 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/murray17/rovai-ai.git`</sub>
- **[Markus](https://github.com/markus-global/markus)** — The all-in-one AI workforce platform for building AI agent teams: role-based agents that coordinate, delegate tasks, and work toward a shared goal with persistent memory.
  <sub>★ 219 · TypeScript · Apache-2.0 · npm · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @markus-global/cli`</sub>
- **[OtoDock](https://github.com/OtoDock/oto-dock)** — Self-hosted "company OS" where agents work in departments, delegate to each other, and keep working unwatched on your Anthropic/OpenAI subscriptions — company map, per-agent dashboards, artifacts, meetings, and terminals. Source-available under FSL-1.1.
  <sub>★ 202 · Python · source · pushed 2026-11-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/OtoDock/oto-dock.git`</sub>
- **[ORCH](https://github.com/oxgeneral/ORCH)** — CLI runtime managing agents as typed teams with an explicit state machine and goals. Claude Code, Codex, Cursor.
  <sub>★ 182 · TypeScript · MIT · npm · pushed 2026-11-18 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @oxgeneral/orch # Install`</sub>
- **[NXTG-Forge Orchestrator](https://github.com/nxtg-ai/forge-orchestrator)** — Coordinates Claude Code, Codex, and Gemini CLI on one shared repo through a research-plan-delegate-adversarial-verify-deploy pipeline, with file locking, knowledge capture, and drift detection. Single Rust binary.
  <sub>★ 167 · Rust · script · pushed 2026-11-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://forge.nxtg.ai/install.sh | sh`</sub>
- **[kodo](https://github.com/ikamensh/kodo)** — Directs agents through work cycles where a separate agent independently verifies each result. Claude Code, Codex, Gemini CLI.
  <sub>★ 138 · Python · MIT · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install kodo-agent`</sub>
- **[tutti](https://github.com/nutthouse/tutti)** — Config-driven workflows passing typed artifacts between agents, each in its own worktree.
  <sub>★ 133 · Rust · MIT · cargo · pushed 2026-07-28 · WSL2 · macOS? · Linux</sub>
  <sub>`cargo install tutti`</sub>
- **[5dive](https://github.com/5dive-ai/5dive)** — Named agents on a shared org chart and backlog hand work to each other and escalate to a human over Telegram. Claude Code, Codex, Grok, Antigravity, OpenCode.
  <sub>★ 122 · Shell · MIT · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://install.5dive.ai | sudo bash`</sub>
- **[Crewly](https://github.com/stevehuang0115/crewly)** — Runs teams of role-based coding agents with task delegation, shared memory and a live web dashboard. Claude Code, Codex, Gemini CLI, OpenCode.
  <sub>★ 91 · TypeScript · MIT · npm · pushed 2026-11-20 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npm install -g crewly`</sub>
- **[CompanyHelm](https://github.com/CompanyHelm/companyhelm)** — Distributed orchestrator with task management and direct agent-to-agent conversations.
  <sub>★ 78 · TypeScript · MIT · source · pushed 2026-08-28 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/CompanyHelm/companyhelm.git`</sub>
- **[Agon](https://github.com/AutoResearch-Factory/Agon)** — Orchestrates scientist, coder, and auditor loops from research topic through proposal to experiment.
  <sub>★ 57 · Python · MIT · clone · pushed 2026-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AutoResearch-Factory/Agon.git`</sub>
- **[shire](https://github.com/victor36max/shire)** — Persistent team workspaces with inter-agent mailboxes and a shared drive. Claude Code, OpenCode, Pi.
  <sub>★ 41 · TypeScript · MIT · npm · pushed 2026-05-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agents-shire`</sub>
- **[corellis](https://github.com/CorellisOrg/Corellis)** — Multi-agent governance framework for OpenClaw — goal decomposition, fleet-wide memory, correction propagation, and approval workflows for 20+ agent fleets.
  <sub>★ 30 · Shell · MIT · clone · pushed 2026-04-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/CorellisOrg/corellis.git`</sub>
- **[orc](https://github.com/spencermarx/orc)** — Lightweight framework that piggybacks your existing CLI setup for planning, task decomposition, worktrees, and review.
  <sub>★ 27 · Shell · clone · pushed 2026-06-21 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/thefinalsource/orc.git`</sub>
- **[Brigade](https://github.com/gmpetrov/brigade)** — AI teammates for support, marketing, sales, and code, each with its own job, computer, apps, and shared memory, starting from triggers or schedules and asking a person before the app actions you choose. Claude Code, Codex.
  <sub>★ 16 · TypeScript · MIT · clone · pushed 2026-11-20 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/gmpetrov/brigade.git`</sub>
- **[Agora](https://github.com/CaffeinatedSoftwareLLC/agora)** — Self-hosted chat where coding agents on different machines coordinate in shared channels and threads, with turn-taking, file reservations, and handoffs, while humans watch and steer from a web UI. Claude Code, Codex, and any MCP client.
  <sub>★ 6 · TypeScript · AGPL-3.0 · npm · pushed 2026-11-18 · macOS</sub>
  <sub>`npm install -g https://github.com/CaffeinatedSoftwareLLC/agora/releases/download/agora-mcp-latest/agora-mcp.tgz`</sub>
- **[squad](https://github.com/bradygaster/squad)** — Human-led AI agent teams for any project built on GitHub Copilot: repo-native specialist agents, coordinator routing, and parallel work, with persistent memory across sessions.
  <sub>★ 6 · TypeScript · MIT · winget · pushed 2026-11-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install --id bradygaster.Squad --exact`</sub>
- **[Codex Autopilot Kit](https://github.com/crunaldo/codex-autopilot-kit)** — Project-scoped multi-agent workflow layer for Codex, installing supervisor, explorer, worker, and reviewer roles with reusable autonomous Goal contracts, preview/diff tooling, and safety verification without replacing the native harness.
  <sub>★ 5 · JavaScript · MIT · npm · pushed 2026-11-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codex-autopilot-kit`</sub>

## Autonomous Loop Runners

- **[Loop Engineering](https://github.com/cobusgreyling/loop-engineering)** — Designs repeatable coding-agent loops around automation, worktrees, skills, state, and verification, with starters and a Loop Ready score for Grok, Claude Code, Codex, and OpenCode.
  <sub>★ 11.8k · TypeScript · MIT · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @cobusgreyling/loop init . --pattern daily-triage --tool claude`</sub>
- **[ralph-claude-code](https://github.com/frankbria/ralph-claude-code)** — Development loop for Claude Code with exit detection that recognizes when the work is actually finished.
  <sub>★ 9.7k · Shell · MIT · script · pushed 2026-11-14 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -sL https://raw.githubusercontent.com/frankbria/ralph-claude-code/main/uninstall.sh | bash`</sub>
- **[ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator)** — Hat-based orchestration that keeps agents looping until done, as a fuller implementation of the Ralph Wiggum technique.
  <sub>★ 3.2k · Rust · MIT · npm · pushed 2026-11-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ralph-orchestrator/ralph-cli`</sub>
- **[ralph-tui](https://github.com/subsy/ralph-tui)** — Drives an agent through a task list autonomously, with a TUI for watching the loop.
  <sub>★ 2.5k · TypeScript · MIT · npx · pushed 2026-11-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx add-skill subsy/ralph-tui --all`</sub>
- **[LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness)** — Long-running computer-use harness with fresh-context execution, independent auditing, and verified checkpoints across desktop apps and CLI workflows. Claude Code, Codex, OpenCode, DeepSeek Harness.
  <sub>★ 1.9k · Python · MIT · uv · pushed 2026-11-11 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`uv tool install lh-harness # or: pip install lh-harness`</sub>
- **[ralphex](https://github.com/umputun/ralphex)** — Executes an implementation plan autonomously with a fresh session per task, plus validation, retries, multi-phase review, and automatic commits. Claude Code, Codex.
  <sub>★ 1.5k · Go · MIT · go · pushed 2026-11-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/umputun/ralphex/cmd/ralphex@latest`</sub>
- **[bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Keeps no model in the coordination loop, so orchestration costs zero tokens. Verifies with tests and auto-commits across 40+ CLI agents.
  <sub>★ 1.2k · Python · Apache-2.0 · uv · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[fractal](https://github.com/plasma-ai/fractal)** — Loops that recursively delegate separable subtasks to child agents, bounded by configurable depth, cost, and time limits.
  <sub>★ 795 · Python · Apache-2.0 · uv · pushed 2026-11-05 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install plasma-fractal --with-executables-from plasma-wiki`</sub>
- **[MartinLoop](https://github.com/Keesan12/martin-loop)** — Caps spend, enforces policy, verifies output, and rolls back failures, leaving inspectable run receipts.
  <sub>★ 263 · TypeScript · Apache-2.0 · npm · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g martin-loop`</sub>
- **[ordewell](https://github.com/ordewell/ordewell)** — Turns one goal into an editable plan of tasks, each carrying its own runner, model and mode, then runs each task as its own agent session and passes it only when evidence of completion shows up in that session's output. Claude Code, Codex, OpenCode.
  <sub>★ 211 · TypeScript · Apache-2.0 · winget · pushed 2026-11-19 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`winget install Ordewell.Ordewell # Windows`</sub>
- **[LoopTroop](https://github.com/looptroop-ai/LoopTroop)** — An LLM council plans the work, then Ralph-style loops retry failed units with fresh context. Executes via OpenCode worktrees.
  <sub>★ 179 · TypeScript · MIT · winget · pushed 2026-11-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`winget install LoopTroopAI.LoopTroop`</sub>
- **[AgenC Core](https://github.com/tetsuo-ai/agenc-core)** — Open source agent harness whose Goal mode drives one goal through implementation, testing and an independent review, with any model provider or a local model.
  <sub>★ 144 · TypeScript · MIT · npm · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`npm install -g @tetsuo-ai/agenc`</sub>
- **[future-os](https://github.com/futuregene/future-os)** — One agent everywhere (terminal, desktop, mobile, CLI, IM bots) with a built-in loop control plane: durable goals, event-sourced state, and verification gates for 24h+ runs.
  <sub>★ 118 · Rust · MIT · script · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://dl.future-os.cn/install.sh | bash`</sub>
- **[jinka](https://github.com/yegor256/jinka)** — 24x7 runner of multiple agents to make one wish to come true, mostly related to GitHub repositories maintenance, like issue triaging, PR reviewing and merging, bug reporting and fixing, CI stabilizing.
  <sub>★ 19 · JavaScript · MIT · npm · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @yegor256/jinka`</sub>
- **[toryo](https://github.com/JesseRWeigel/toryo)** — Trust-based delegation with quality ratcheting that commits improvements and reverts regressions. Chains Claude Code, Aider, Gemini CLI, Ollama.
  <sub>★ 12 · TypeScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @jweigel/toryo init # scaffold config + task specs`</sub>

## Autonomous Task Runners

- **[OpenHands](https://github.com/OpenHands/OpenHands)** — Self-hostable control center running its own agent or driving Claude Code, Codex, and any Agent Client Protocol agent, on schedules or webhooks.
  <sub>★ 93.9k · TypeScript · MIT · npm · pushed 2026-11-20 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[multica](https://github.com/multica-ai/multica)** — Managed agents platform where you assign tasks, track progress, and let agents compound skills between runs.
  <sub>★ 56.9k · Go · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.ps1 | iex`</sub>
- **[symphony](https://github.com/openai/symphony)** — Turns project work into isolated autonomous runs, so teams manage the work rather than supervise the agent.
  <sub>★ 28.1k · Elixir · Apache-2.0 · source · pushed 2026-09-15 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/openai/symphony.git`</sub>
- **[open-swe](https://github.com/langchain-ai/open-swe)** — Invoked from Slack, Linear, or GitHub comments; each task runs in its own cloud sandbox and ends in a draft PR linked to the ticket.
  <sub>★ 11.2k · Python · MIT · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/open-swe.git`</sub>
- **[SuperPlane](https://github.com/superplanehq/superplane)** — Coordinates coding agents, source control, CI, review, approvals and feedback to turn routine backlog issues into review-ready pull requests. Supports Claude, Cursor and OpenAI.
  <sub>★ 10.1k · Go · source · pushed 2026-11-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/superplanehq/superplane.git`</sub>
- **[claude-code-action](https://github.com/anthropics/claude-code-action)** — Anthropic's official GitHub Action, detecting from context whether to answer, review, or implement. Auth via Anthropic API, Bedrock, Vertex, or Foundry.
  <sub>★ 10k · TypeScript · MIT · gh-action · pushed 2026-11-19</sub>
  <sub>`uses: anthropics/claude-code-action@main # in .github/workflows/*.yml`</sub>
- **[gh-aw](https://github.com/github/gh-aw)** — Compiles agentic workflows written in Markdown into GitHub Actions YAML. Read-only by default, with writes only through sanitized safe-outputs. Copilot, Claude, Codex, Gemini.
  <sub>★ 5.7k · Go · MIT · gh-ext · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`gh extension install github/gh-aw`</sub>
- **[background-agents](https://github.com/open-inspect/background-agents)** — Sessions trigger from a web UI, Slack, GitHub, Linear, webhooks, or cron, run in Modal, Daytona, Vercel, E2B, or OpenComputer sandboxes, and open attributed PRs.
  <sub>★ 3.5k · TypeScript · MIT · source · pushed 2026-11-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/open-inspect/background-agents.git`</sub>
- **[run-gemini-cli](https://github.com/google-github-actions/run-gemini-cli)** — Google's official GitHub Action, running on event or schedule triggers or on demand via `@gemini-cli /review` and `/triage`.
  <sub>★ 2.1k · TypeScript · Apache-2.0 · gh-action · pushed 2026-11-19</sub>
  <sub>`uses: google-github-actions/run-gemini-cli@main # in .github/workflows/*.yml`</sub>
- **[centaur](https://github.com/paradigmxyz/centaur)** — Multiplayer self-hosted agents with Slack-native conversations, Kubernetes sandboxes, shared tools, and durable workflows.
  <sub>★ 1.4k · Rust · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/paradigmxyz/centaur.git`</sub>
- **[codex-action](https://github.com/openai/codex-action)** — OpenAI's official GitHub Action, running Codex CLI headlessly under drop-sudo, unprivileged-user, or fully read-only sandboxes.
  <sub>★ 1.3k · JavaScript · Apache-2.0 · gh-action · pushed 2026-11-18</sub>
  <sub>`uses: openai/codex-action@main # in .github/workflows/*.yml`</sub>
- **[cyrus](https://github.com/cyrusagents/cyrus)** — Watches Linear, GitHub, GitLab, and Slack issues assigned to it, spinning up an isolated worktree per issue. Claude Code, Codex, Cursor, Gemini.
  <sub>★ 909 · TypeScript · Apache-2.0 · npm · pushed 2026-11-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g cyrus-ai`</sub>
- **[agent-qa](https://github.com/vostride/agent-qa)** — Runs natural-language web and mobile test suites through a self-healing execution loop, persists memory between runs, and exposes a dashboard, CLI, MCP server, and coding-agent skills.
  <sub>★ 819 · TypeScript · npx · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-qa init`</sub>
- **[aeon](https://github.com/aeonfun/aeon)** — Runs unattended on GitHub Actions; dispatches skills to six coding-agent harnesses behind one contract (Claude Code, Grok, Codex, Pi, Vibe, Kimi), with quality scoring, git-persisted memory, a self-healing loop, and reactive triggers.
  <sub>★ 796 · JavaScript · MIT · clone · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aeonfun/aeon`</sub>
- **[Machinist](https://github.com/owainlewis/machinist)** — Keeps coding agents working on a repository without making a human orchestrate every step from a terminal, pulling tasks from trusted ticket queues into isolated Codex workspaces.
  <sub>★ 540 · Go · MIT · clone · pushed 2026-11-19 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/owainlewis/machinist.git`</sub>
- **[no_human](https://github.com/no-human-ai/no_human)** — Takes a ticket (Jira, Linear, monday.com, GitHub/GitLab issues) to a reviewed pull request on your own machine: a second model in a fresh session reviews each diff and is told to refute "done", a tamper guard blocks net test reductions before that review, and merging stays human. Claude Code as the coder; Codex and local backends optional. MIT.
  <sub>★ 322 · Python · MIT · uv · pushed 2026-10-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uv tool install no-human # or: pipx install no-human — the wheel ships the board`</sub>
- **[Orbi](https://github.com/orbi-build/orbi)** — Picks up GitHub Issues labeled `ai-ready`, implements each in an isolated worktree, has a separate session review the PR against the Issue's acceptance criteria, then merges only the reviewed head and cuts a tagged release. Runs on Pi with any OpenAI-compatible API or a Codex subscription.
  <sub>★ 260 · Python · AGPL-3.0 · uv · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install orbi-cli`</sub>
- **[remote-swe-agents](https://github.com/aws-samples/remote-swe-agents)** — Serverless control plane on Lambda with a dedicated EC2 worker per session, triggered by issue comments, assignments, and PR reviews.
  <sub>★ 243 · TypeScript · MIT-0 · gh-action · pushed 2026-10-06</sub>
  <sub>`uses: aws-samples/remote-swe-agents@main # in .github/workflows/*.yml`</sub>
- **[Contrabass](https://github.com/junhoyeo/contrabass)** — Terminal-first orchestrator for issue-driven agent runs, pulling work from Linear, GitHub Issues, or a local board into git worktrees with TUI, headless, and dashboard modes.
  <sub>★ 228 · Go · Apache-2.0 · go · pushed 2026-07-17 · WSL2 · macOS · Linux</sub>
  <sub>`go install github.com/junhoyeo/contrabass/cmd/contrabass@latest`</sub>
- **[sortie](https://github.com/sortie-ai/sortie)** — Turns tracker tickets into agent sessions. Agent-agnostic and tracker-agnostic, as a single Go binary with SQLite persistence.
  <sub>★ 224 · Go · Apache-2.0 · brew · pushed 2026-11-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install --cask sortie-ai/tap/sortie`</sub>
- **[Taskuary](https://github.com/ldbumble/taskuary)** — Local-first work inbox that triages email, chat, issue trackers, and scheduled reports into supervised Claude Code, Codex, Gemini, Cursor, or Copilot CLI runs, with conflict-aware queuing, live terminals, and approval-gated replies.
  <sub>★ 152 · Python · MIT · pip · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install taskuary`</sub>
- **[lalph](https://github.com/tim-smart/lalph)** — Orchestrator driven by whichever source of issues you point it at.
  <sub>★ 137 · TypeScript · MIT · npm · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g lalph`</sub>
- **[Frink](https://github.com/benord-labs/frink)** — Desktop app that starts a Flow from a ticket (Linear, Jira, Shortcut, ClickUp), an alert or event (Sentry, PostHog, Vercel, Cloudflare, Supabase, and more), any webhook, or a schedule, then runs it as a graph of agent, shell, condition, and approval steps in its own worktree and parks blocked agents in a Work Queue. Claude Code, Codex.
  <sub>★ 65 · TypeScript · MIT · source · pushed 2026-11-20 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/benord-labs/frink.git`</sub>
- **[dsh-action](https://github.com/Lixiaoyiao/DSH-action)** — Runs DeepSeek Harness from GitHub PRs, issues, and CI failures for code reviews, diagnostics, and validated fixes with explicit write controls.
  <sub>★ 64 · TypeScript · MIT · gh-action · pushed 2026-10-31</sub>
  <sub>`uses: lixiaoyiao/dsh-action@main # in .github/workflows/*.yml`</sub>
- **[Tale](https://github.com/tale-project/tale)** — Runs project-board tasks in persistent sandboxes, with manager-agent delegation and deliverable review. Supports Claude Code, Codex, OpenCode, and other configured runtimes.
  <sub>★ 47 · TypeScript · MIT · script · pushed 2026-11-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/tale-project/tale/main/scripts/install-cli.sh | bash`</sub>
- **[NEEDLE](https://github.com/jedarden/NEEDLE)** — Runs unattended against a shared bead queue (SQLite, atomic claims), dispatching each bead to a headless CLI — Claude Code, Codex, OpenCode, Aider — with every outcome routed through an explicit state machine; no inter-agent channel, coordination is done at decomposition time.
  <sub>★ 34 · Rust · MIT · cargo · pushed 2026-11-13 · WSL2 · macOS? · Linux</sub>
  <sub>`cargo install --git https://git.ardenone.com/jedarden/NEEDLE`</sub>
- **[Kombinat](https://github.com/Danilqa/kombinat)** — Runs agents on a schedule or webhook from markdown routines in your repo that go live once merged, on a Mac or Linux machine with your own logins, MCP servers and subscription, with run history, transcripts, timeouts and budget caps in a browser and terminal dashboard. Claude Code, Codex, and any other CLI agent. MIT.
  <sub>★ 16 · TypeScript · MIT · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx kombinat init my-routines`</sub>
- **[MindFlock](https://github.com/MindFlock/MindFlock)** — Cross-platform desktop app that polls the Jira, Linear, GitHub Issues, Shortcut and Asana tickets assigned to you and starts a seeded agent session for each in its own git worktree on your machine, then walks it along a route of checks and approval stops to a PR you merge. Any agent CLI via a TOML adapter, including Claude Code, Codex, Copilot CLI, Aider, OpenCode and Goose. Apache-2.0.
  <sub>★ 15 · Python · Apache-2.0 · psh · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/MindFlock/MindFlock/main/install.ps1 | iex`</sub>
- **[Kraft](https://github.com/itsOmidKarami/kraft)** — Local orchestrator that takes each task from spec to pull request in its own git worktree: steps run in order from a YAML chain file, tests and CI are checked in steps of their own, attempts and spend are capped, and a person approves the spec, the plan and the final review from the web UI, a phone or the CLI. Claude Code by default; Codex, Cursor, Gemini CLI, OpenCode, Amp and Antigravity can run steps. Apache-2.0.
  <sub>★ 14 · Python · Apache-2.0 · uv · pushed 2026-11-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`uv tool install kraft-sdlc`</sub>

## Agent Infrastructure &amp; Primitives

- **[oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)** — Workflow layer for OpenAI Codex CLI: stronger default sessions, reusable skills, native hooks, HUD/status surfaces, project guidance, and team-style execution commands.
  <sub>★ 33.8k · TypeScript · MIT · npm · pushed 2026-11-18 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g oh-my-codex`</sub>
- **[Archon](https://github.com/coleam00/Archon)** — Harness builder for deterministic AI coding workflows, combining agent steps with scripts, validation gates, approvals, and isolated git worktrees. Claude Code, Codex, and more.
  <sub>★ 24k · TypeScript · MIT · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://archon.diy/install.ps1 | iex # Windows (PowerShell)`</sub>
- **[NemoClaw](https://github.com/NVIDIA/NemoClaw)** — Runs Hermes, LangChain Deep Agents, and OpenClaw inside NVIDIA OpenShell with managed inference.
  <sub>★ 23.1k · TypeScript · Apache-2.0 · source · pushed 2026-11-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NVIDIA/NemoClaw.git`</sub>
- **[openfang](https://github.com/RightNow-AI/openfang)** — Open-source agent operating system.
  <sub>★ 18.3k · Rust · Apache-2.0 · psh · pushed 2026-07-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://openfang.sh/install.ps1 | iex`</sub>
- **[AX](https://github.com/google/ax)** — Google's declarative runtime for running autonomous agent workloads at cluster scale: Kubernetes-style task specs, sandboxed workspaces, and network fencing.
  <sub>★ 14.8k · Go · Apache-2.0 · script · pushed 2026-11-20 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://github.com/google/ax/releases/latest/download/install.sh | sh`</sub>
- **[omnigent](https://github.com/omnigent-ai/omnigent)** — Meta-harness running Claude Code, Codex, Cursor, OpenCode, Hermes, Pi, or custom YAML agents against swappable sandbox backends, with policy enforcement.
  <sub>★ 11.5k · Python · Apache-2.0 · uv · pushed 2026-11-20 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`uv tool install omnigent # or: pip install "omnigent"`</sub>
- **[sandcastle](https://github.com/mattpocock/sandcastle)** — Orchestrate sandboxed coding agents in TypeScript with sandcastle.run().
  <sub>★ 9.2k · TypeScript · MIT · source · pushed 2026-11-18 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mattpocock/sandcastle.git`</sub>
- **[Flue](https://github.com/withastro/flue)** — Sandbox agent framework from the Astro team: give each coding agent its own isolated environment with the tools and access it needs.
  <sub>★ 8.7k · TypeScript · Apache-2.0 · source · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/withastro/flue.git`</sub>
- **[Open Multi-Agent](https://github.com/open-multi-agent/open-multi-agent)** — TypeScript-native runtime where a coordinator turns a goal into a task DAG and a deterministic scheduler runs specialized agents, with approvals, traces, evaluation, checkpoints, and resume support.
  <sub>★ 7.1k · TypeScript · MIT · source · pushed 2026-11-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/open-multi-agent/open-multi-agent.git`</sub>
- **[Heym](https://github.com/heymrun/heym)** — Self-hosted runtime for tool-using LLM agents and OpenCode workflows, with sub-agent orchestration, MCP integration, approval checkpoints, and execution traces.
  <sub>★ 1.8k · Python · clone · pushed 2026-11-20 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/heymrun/heym.git`</sub>
- **[Rivet Agents](https://github.com/rivet-dev/agents)** — Daemon, HTTP/SSE API, and TypeScript SDK for driving six coding agents inside E2B, Daytona, Modal, Cloudflare Containers, or Docker.
  <sub>★ 1.7k · TypeScript · Apache-2.0 · source · pushed 2026-11-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rivet-dev/agents.git`</sub>
- **[deja-vu](https://github.com/vshulcz/deja-vu)** — Indexes the session transcripts forty-three coding agents already write to disk into a local BM25 memory, handing relevant history, file blame, and prior fixes back over MCP, skills, and hooks with credentials redacted. Claude Code, Codex, Cursor, Gemini CLI, Antigravity, OpenCode, and more.
  <sub>★ 1.6k · Go · MIT · winget · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install vshulcz.deja-vu`</sub>
- **[Concord MCP](https://github.com/Get-Concord-AI/concord-mcp)** — Shared coordination protocol for Claude Code, Codex, Cursor, Gemini CLI, and Grok Build agents to claim work, detect edit collisions, exchange durable messages, transfer ownership, and hand off review evidence without replacing their existing harnesses.
  <sub>★ 1.4k · TypeScript · MIT · npm · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @concord-ai/concord-mcp`</sub>
- **[Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS)** — Keeps specialist agents in a hub and spins up a temporary orchestrator per task, with A2A routing and governed memory gates. Formerly Hephaestus.
  <sub>★ 1.4k · Python · Apache-2.0 · script · pushed 2026-11-18 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/agentlas-ai/Agentlas-OS/main/scripts/install-all-runtimes.sh | bash`</sub>
- **[kanzo](https://github.com/emanuele-em/kanzo)** — Self-hosted kanban for humans and agents: a browser board and an MCP server in one 4 MB binary, so you and your coding agents work on the same tasks and agents move cards while you watch.
  <sub>★ 1.2k · Rust · AGPL-3.0 · cargo · pushed 2026-11-18 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`cargo install kanzo`</sub>
- **[OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay)** — Records a coding agent at the process and socket boundary so model traffic, shell exit codes, per-turn file changes and MCP JSON-RPC share one timeline, then replays the run offline with the network off or forks it from a checkpoint onto a different model.
  <sub>★ 1k · TypeScript · Apache-2.0 · npm · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g orcareplay # the package is orcareplay`</sub>
- **[herdr-core](https://github.com/herdrdev/herdr-core)** — Headless runtime (hc) that runs programs and coding agents in terminals that stay alive after you leave: agents start other agents, send them work, and hear back; nothing is drawn - attach from your shell, an agent, or your own app.
  <sub>★ 825 · Rust · Apache-2.0 · script · pushed 2026-11-16 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://releases.herdr.dev/core/install.sh | sh`</sub>
- **[LazyMind](https://github.com/LazyAGI/LazyMind)** — Self-hosted Skill runtime for Codex and DeepSeek Harness, with persisted workflow state, review checkpoints, and artifacts.
  <sub>★ 789 · Go · Apache-2.0 · source · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/LazyAGI/LazyMind.git`</sub>
- **[Claudexor](https://github.com/razzant/claudexor)** — Routes one coding thread across harnesses with quota-aware rotation between subscription profiles, Best-of-N runs, and cross-family review.
  <sub>★ 525 · TypeScript · MIT · npm · pushed 2026-11-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g claudexor`</sub>
- **[foremerge](https://github.com/naw103/foremerge)** — Coordination protocol above Git: agents declare intent, semantic scope, and operation before writing code, deterministic rules raise findings when plans collide, and acceptance is gated on a verification run it executes itself. One Rust binary over local SQLite, with MCP for Claude Code, Codex, and Cursor.
  <sub>★ 410 · Rust · Apache-2.0 · npm · pushed 2026-11-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g foremerge`</sub>
- **[Cotal](https://github.com/Cotal-AI/Cotal)** — Open pub/sub standard over NATS JetStream where mixed coding agents share a space with presence, channels, durable direct messages, and role-addressed anycast, in any topology you wire. Claude Code, Codex, OpenCode, Hermes, Jcode, and pi.
  <sub>★ 404 · TypeScript · Apache-2.0 · npm · pushed 2026-11-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g cotal-ai`</sub>
- **[guild](https://github.com/mathomhaus/guild)** — Shared context, memory, and task coordination as a single Go binary over local SQLite with hybrid keyword and semantic search.
  <sub>★ 297 · Go · Apache-2.0 · psh · pushed 2026-11-09 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://github.com/mathomhaus/guild/releases/latest/download/install.ps1 | iex`</sub>
- **[Speakeasy control plane](https://github.com/speakeasy-api/gram)** — MCP gateway for Claude Code, Cursor, Codex, and custom agents, with identity-based tool access, per-action security policies, and audit logs.
  <sub>★ 278 · Go · AGPL-3.0 · source · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/speakeasy-api/gram.git`</sub>
- **[AIWG](https://github.com/jmagly/aiwg)** — Deploys versioned agents, skills, rules, and governed workflows into the native project paths used by Claude Code, Codex, Copilot, Cursor, and other coding agents.
  <sub>★ 231 · TypeScript · MIT · npm · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g aiwg`</sub>
- **[Loom](https://github.com/ClickHouse/loom)** — Self-hosted MCP backend for shared memory, document search, and code indexing on ClickHouse. Claude Code, Codex, and Cursor.
  <sub>★ 172 · Python · Apache-2.0 · source · pushed 2026-11-20 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ClickHouse/loom.git`</sub>
- **[Agent Barn](https://github.com/aai-labs/agent-barn)** — Open-source (Apache-2.0) control plane for AI agents: teams talk to agents in Slack, Teams, Telegram, Discord or email, agents work across Jira, GitHub, Confluence and more, and every conversation, tool call, log and cost is recorded. Runs agent runtimes like Hermes and OpenClaw on your own Kubernetes cluster, deployed with Helm.
  <sub>★ 111 · Python · Apache-2.0 · clone · pushed 2026-11-20 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/aai-labs/agent-barn.git`</sub>
- **[handoff](https://github.com/dazuiba/handoff)** — Delegates a task to DeepSeek, Codex, or Claude from inside your current Claude Code or Codex session, returning the result automatically.
  <sub>★ 101 · Python · uv · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install handoff-cli`</sub>
- **[sub-agents-skills](https://github.com/shinpr/sub-agents-skills)** — Portable Markdown definitions that route a task to a chosen backend, model, effort level, and permission set.
  <sub>★ 101 · Python · MIT · script · pushed 2026-10-22 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/shinpr/sub-agents-skills/main/install.sh | bash -s -- --target ~/.cursor/skills`</sub>
- **[ox](https://github.com/sageox/ox)** — The team hivemind: persistent context recorded once and recalled across agents, machines, and teammates, as a Go CLI.
  <sub>★ 68 · Go · MIT · npx · pushed 2026-11-20 · macOS · Linux</sub>
  <sub>`npx @sageox/ox@latest install`</sub>
- **[Scalekit](https://github.com/scalekit-inc/scalekit-sdk-python)** — Integration layer that gives agents per-user OAuth and scoped tool access to 600+ connectors and 35,000+ tools, callable from LangChain, OpenAI Agents SDK, Claude, Hermes or any MCP client.
  <sub>★ 67 · Python · MIT · pip · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "scalekit-sdk-python[flask]" # or "scalekit-sdk-python[fastapi]" or "scalekit-sdk-python[django]"`</sub>
- **[Crewplane](https://github.com/crewplaneai/crewplane)** — CLI-first control plane that turns one-off coding-agent calls into reviewable Markdown workflows spanning Claude Code, Codex, Gemini CLI, or Copilot CLI. Explicit artifact handoffs keep execution inspectable on disk, while validated completed nodes let failed workflows resume instead of starting over.
  <sub>★ 56 · Python · Apache-2.0 · uv · pushed 2026-11-16 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install crewplane`</sub>
- **[codecast](https://github.com/codecast-sh/codecast)** — Watches your real local sessions and surfaces them in a live triage inbox, keeping a searchable record with line-level agent attribution. Claude Code, Codex, Cursor, Gemini.
  <sub>★ 50 · TypeScript · MIT · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm codecast.sh/install.ps1 | iex`</sub>
- **[aisync](https://github.com/MaxonT/aisync)** — Multi-agent context management, coordination, and observability: one shared rules file and hash-chained journal across tools, plus file claims that exit with code 3 when two agents overlap. Claude Code, Codex, Cursor, and more.
  <sub>★ 48 · Python · MIT · npx · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @mingyang2026/aisync-cli --version # npm 0.2.9`</sub>
- **[agenttier](https://github.com/agenttier/agenttier)** — Kubernetes runtime giving each agent its own Pod and PVC sandbox behind a default-deny NetworkPolicy, with a streaming SSE invoke API.
  <sub>★ 46 · Go · Apache-2.0 · pip · pushed 2026-10-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install agenttier # from PyPI`</sub>
- **[Agent Messaging Protocol](https://github.com/agentmessaging/protocol)** — Open standard for agent-to-agent messaging with Ed25519-signed envelopes, federation across providers, and delivery that must be proven rather than assumed. Reference server, TypeScript SDK, and a Claude Code plugin.
  <sub>★ 39 · Apache-2.0 · source · pushed 2026-11-20</sub>
  <sub>`git clone https://github.com/agentmessaging/protocol.git`</sub>
- **[neuralyzer](https://github.com/gintasz/neuralyzer)** — Lets an agent wipe its own session context and re-run the first message, making Ralph loops easier to engineer.
  <sub>★ 38 · TypeScript · MIT · source · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gintasz/neuralyzer.git`</sub>
- **[claude-bulkhead](https://github.com/dooly6276/claude-bulkhead)** — PreToolUse hooks for Claude Code that stop parallel sessions and their subagents on one machine from killing each other's processes, clashing on ports, committing each other's edits, or running heavy commands when RAM is low.
  <sub>★ 35 · JavaScript · MIT · npm · pushed 2026-11-14 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g claude-bulkhead`</sub>
- **[Mnemoverse](https://github.com/mnemoverse/mcp-memory-server)** — Hosted memory engine over MCP: decisions, preferences, and lessons follow an agent between sessions and tools, and recall re-ranks from reported outcomes rather than similarity alone. Remote endpoint with sign-in, or `npx -y @mnemoverse/mcp-memory-server@latest` with an API key. Claude Code, Cursor, Gemini CLI, VS Code, Windsurf, ChatGPT. MIT server, free tier.
  <sub>★ 30 · TypeScript · MIT · npx · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mnemoverse/mcp-memory-server`</sub>
- **[dsh-super-agent](https://github.com/vicfei/dsh-super-agent)** — Standalone admission-control layer for coding-agent orchestrators, implementing the DeepSeek Super-agent authorization design: host-enforced admission tables where messages can never change permissions, explicit/inferred strength, and an off→observe→auto trust ladder with shadow records before autonomy. Polls GitHub issues/PRs, runs any CLI agent (Claude Code, Codex, OpenCode, or custom scripts) in per-ticket git worktrees, and reports back in-thread under a 100-word discipline. (MIT)
  <sub>★ 26 · TypeScript · MIT · npm · pushed 2026-11-20 · macOS</sub>
  <sub>`npm i -g @vicfei/dsh-super-agent`</sub>
- **[aGiTrack](https://github.com/core-aix/agitrack)** — Takes what a coding agent produces and commits each turn to git, recording the prompt, model, and that turn's token cost in the commit message, with the agent confined to its own worktree. Claude Code, Codex, and OpenCode.
  <sub>★ 25 · Python · Apache-2.0 · pipx · pushed 2026-11-09 · WSL2 · macOS · Linux</sub>
  <sub>`pipx install agitrack`</sub>
- **[LionClaw](https://github.com/moshthepitt/lionclaw)** — Local control plane running coding agents as durable, auditable workers with explicit state, skills, and checkpoints.
  <sub>★ 19 · Rust · MIT · clone · pushed 2026-10-01 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/moshthepitt/lionclaw.git`</sub>
- **[skillfold](https://github.com/byronxlg/skillfold)** — Declares skills in YAML and pins exact revisions in a lockfile so installs are reproducible across Claude Code and Codex.
  <sub>★ 15 · TypeScript · MIT · npm · pushed 2026-11-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g skillfold # or: npx skillfold`</sub>
- **[agent-runbook](https://github.com/KnoxOps/agent-runbook)** — Compiles YAML runbooks with loops, branching, and parallelism into SKILL.md files for Claude Code and Codex.
  <sub>★ 14 · Python · Apache-2.0 · pip · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/KnoxOps/agent-runbook.git`</sub>
- **[MAIster](https://github.com/maister-dev/maister)** — Self-hosted control plane with version-pinned workflow packages and role-based platform agents for triage, review, and knowledge maintenance. Runs development workflows in Git worktrees, combining coding agents, CLI steps, human approvals, and evidence checks before PR creation or local merge. Claude Code, Codex, Gemini CLI, OpenCode, and MiMo via ACP.
  <sub>★ 10 · TypeScript · MIT · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://imaister.dev/quickstart.sh | bash`</sub>
- **[Unified AI System](https://github.com/happy520ai/unified-ai-system)** — Self-hosted gateway and agent control plane that puts prompt enhancement, virtual-key budgets, response caching and a hash-chained audit trail in front of OpenAI-compatible, Anthropic and Gemini traffic, and re-exposes governed tools over MCP to Codex, Cursor and Cline.
  <sub>★ 10 · JavaScript · Apache-2.0 · npx · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add happy520ai/unified-ai-system --skill unified-ai-gateway --agent codex --copy --yes`</sub>
- **[Cognipeer Agent SDK](https://github.com/Cognipeer/agent-sdk)** — TypeScript agent runtime with planning, sub-agents, human-in-the-loop approvals, MCP tools, and OpenTelemetry tracing. OpenAI, Anthropic, Azure, Bedrock, Vertex, and OpenAI-compatible models.
  <sub>★ 7 · TypeScript · MIT · source · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Cognipeer/agent-sdk.git`</sub>
- **[fanout](https://github.com/Breadstick-Crumbs/fanout)** — Runs under parallel coding sessions and tests their branches merged together before main, sends a break back to the session that caused it, and stops two sessions doing the same task. Claude Code, Codex, and agents that read AGENTS.md. MIT.
  <sub>★ 5 · JavaScript · MIT · npx · pushed 2026-11-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:Breadstick-Crumbs/fanout demo`</sub>

## Personal Assistants

- **[openclaw](https://github.com/openclaw/openclaw)** — Your own personal AI assistant, on any OS and any platform.
  <sub>★ 394.9k · TypeScript · MIT · npm · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g openclaw@latest --allow-scripts=openclaw`</sub>
- **[hermes-agent](https://github.com/NousResearch/hermes-agent)** — Self-improving harness with persistent cross-session memory and auto-generated skill documents.
  <sub>★ 264.9k · Python · MIT · script · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`</sub>
- **[nanobot](https://github.com/HKUDS/nanobot)** — Ultra-lightweight self-hosted assistant in Python with WebUI, tools, memory, MCP, and multi-agent workflows.
  <sub>★ 50.2k · Python · MIT · psh · pushed 2026-11-20 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/HKUDS/nanobot/main/scripts/install.ps1 | iex`</sub>
- **[OpenHuman](https://github.com/tinyhumansai/openhuman)** — Open-source personal agent harness: desktop app and Rust library with built-in memory, token compression, and instant tool search, efficient enough to run hundreds of agents on a $10 server.
  <sub>★ 42.8k · Rust · GPL-3.0 · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.ps1 | iex`</sub>
- **[QwenPaw](https://github.com/agentscope-ai/QwenPaw)** — Personal assistant that deploys to your own machine or the cloud and plugs into multiple chat apps. Formerly CoPaw.
  <sub>★ 38k · Python · Apache-2.0 · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://qwenpaw.agentscope.io/install.ps1 | iex`</sub>
- **[zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)** — Fast, small, fully autonomous assistant infrastructure in Rust, deployable anywhere.
  <sub>★ 33.5k · Rust · Apache-2.0 · script · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/zeroclaw-labs/zeroclaw/master/install.sh | sh`</sub>
- **[nanoclaw](https://github.com/nanocoai/nanoclaw)** — Lightweight OpenClaw alternative running in containers, connecting to WhatsApp, Telegram, Slack, Discord, and Gmail.
  <sub>★ 31.1k · TypeScript · MIT · clone · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/nanocoai/nanoclaw.git`</sub>
- **[picoclaw](https://github.com/sipeed/picoclaw)** — Tiny and fast assistant deployable anywhere.
  <sub>★ 30.1k · Go · MIT · clone · pushed 2026-11-05 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/sipeed/picoclaw.git`</sub>
- **[OpenMausBot](https://github.com/milind-soni/OpenMausBot)** — Open-source Grok Bot-style team of bots in a chat-app sidebar, where every bot is a real local agent — Claude or Codex — with its own personality, model, cloud computer, and connected apps, behind approval gates. Local-first, bring-your-own-agent.
  <sub>★ 26k · TypeScript · Apache-2.0 · npm · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g openmausbot`</sub>
- **[OpenWorker](https://github.com/andrewyng/openworker)** — Open-source desktop AI coworker that delivers finished work — security review with re-scanned fixes, cloud posture audits, triaged inboxes — from specialist coworkers, with every action governed and logged. BYO model key or fully local via Ollama.
  <sub>★ 19.5k · Python · MIT · clone · pushed 2026-11-20 · Win · WSL2 · macOS · Linux?</sub>
  <sub>`git clone https://github.com/andrewyng/openworker`</sub>
- **[rowboat](https://github.com/rowboatlabs/rowboat)** — Open-source AI coworker with memory.
  <sub>★ 18.3k · TypeScript · Apache-2.0 · source · pushed 2026-11-19 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rowboatlabs/rowboat.git`</sub>
- **[leon](https://github.com/leon-ai/leon)** — Long-running open-source personal assistant with voice and text interfaces.
  <sub>★ 17.7k · TypeScript · MIT · clone · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leon-ai/leon.git`</sub>
- **[ironclaw](https://github.com/nearai/ironclaw)** — Agent OS in Rust focused on privacy, security, and extensibility.
  <sub>★ 12.7k · Rust · Apache-2.0 · psh · pushed 2026-11-09 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm "https://github.com/nearai/ironclaw/releases/download/$IronClawReleaseTag/ironclaw-installer.ps1" | iex`</sub>
- **[Octop](https://github.com/TencentCloud/Octop)** — Self-hosted multi-user assistant with a built-in expert team operating in parallel, reachable from web, Telegram, Feishu, DingTalk, QQ, and WeCom.
  <sub>★ 12.3k · Python · MIT · psh · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://download.octop.cloud/octop/scripts/install.ps1 | iex`</sub>
- **[Cloudflare OS](https://github.com/cloudflare/cloudflare-os)** — Self-hostable "company OS" on Cloudflare Workers: a chat UI where agents preloaded with your company context do tasks, build sandboxed apps, and stay inside a Gatekeepers guardrail framework.
  <sub>★ 11.8k · TypeScript · Apache-2.0 · source · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/cloudflare/cloudflare-os.git`</sub>
- **[Coworker](https://github.com/accomplish-ai/coworker)** — Open source AI coworker that lives on your desktop. Formerly accomplish.
  <sub>★ 10.8k · source · pushed 2026-08-13</sub>
  <sub>`git clone https://github.com/accomplish-ai/coworker.git`</sub>
- **[Rakazo](https://github.com/elie222/rakazo)** — Self-hosted platform for persistent AI teammates with their own conversations, memory, and routines, running on shared team computers or isolated private ones, reachable from web, desktop, and mobile with voice mode. Bots delegate to peer bots or short-lived subagents. BYO model and sandbox.
  <sub>★ 9.3k · TypeScript · Apache-2.0 · clone · pushed 2026-11-20 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/elie222/rakazo.git`</sub>
- **[nullclaw](https://github.com/nullclaw/nullclaw)** — Fully autonomous assistant infrastructure written in Zig.
  <sub>★ 8.2k · Zig · MIT · brew · pushed 2026-10-08 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install nullclaw`</sub>
- **[lobsterai](https://github.com/netease-youdao/LobsterAI)** — Desktop-grade agent for data analysis, slides, docs, and web research.
  <sub>★ 6.2k · TypeScript · MIT · clone · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/netease-youdao/LobsterAI.git`</sub>
- **[MetaClaw](https://github.com/aiming-lab/MetaClaw)** — Assistant that learns and evolves from conversation alone.
  <sub>★ 3.5k · Python · MIT · source · pushed 2026-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aiming-lab/MetaClaw.git`</sub>
- **[zclaw](https://github.com/tnm/zclaw)** — Complete personal assistant in 888 KiB, running on an ESP32 with GPIO, cron, and custom tools.
  <sub>★ 2.2k · C · MIT · source · pushed 2026-05-17 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tnm/zclaw.git`</sub>
- **[row-bot](https://github.com/siddsachar/row-bot)** — Local-first desktop assistant that reasons through messy context, orchestrates tools and providers, and works inside your files, repos, and channels — durable memory, scheduled tasks, voice, visible browser automation, and parent-led child agents for research, review, and implementation. Runs on Ollama or opt-in cloud models. Formerly Thoth.
  <sub>★ 1.7k · Python · Apache-2.0 · script · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/siddsachar/row-bot/main/installer/install-linux.sh | bash`</sub>
- **[Ouroboros](https://github.com/razzant/ouroboros)** — General-purpose agent with durable identity and memory, reviewed self-modification, multi-agent coordination, and desktop and headless interfaces.
  <sub>★ 1.7k · Python · MIT · uv · pushed 2026-11-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install "git+https://github.com/razzant/ouroboros.git@ouroboros"`</sub>
- **[denchclaw](https://github.com/DenchHQ/DenchClaw)** — Managed OpenClaw framework aimed at CRM, sales automation, and outreach.
  <sub>★ 1.7k · TypeScript · MIT · npx · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx denchclaw@latest bootstrap`</sub>
- **[Talorys](https://github.com/rociiu/talorys)** — Personal AI assistant that runs entirely in your own Cloudflare account: chat, durable memory, tasks, notes, and scheduled routines, deployed with one command; single-user and free-tier friendly.
  <sub>★ 1.5k · TypeScript · MIT · npx · pushed 2026-11-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx create-talorys@latest`</sub>
- **[kwant](https://github.com/alexsergivan/kwant)** — Self-hosted team of AI bots in one binary, with separate spaces for work and home, @mention handoffs between bots, approvals, and scheduled routines. Runs on a laptop, a VPS, or as a Mac app, with cloud or local models.
  <sub>★ 681 · Rust · AGPL-3.0 · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://kwant.si/install.sh | sh`</sub>
- **[Comma](https://github.com/AFK-surf/Comma)** — Sessionless personal agent that breaks goals into tasks and keeps working through agentic loops across your computer, phone, and browser, with computer use, files, and remote control; self-hostable (AGPL-3.0).
  <sub>★ 616 · Elixir · AGPL-3.0 · source · pushed 2026-11-18 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/AFK-surf/Comma.git`</sub>
- **[taOS](https://github.com/jaylfc/taOS)** — Self-hosted AI agent OS where memory, conversations, agents, and files live on hardware you own, offline by default with cloud by choice, including multi-framework group chat and a desktop GUI.
  <sub>★ 609 · Python · AGPL-3.0 · pip · pushed 2026-11-20 · Win · WSL2 · macOS · Linux</sub>
  <sub>`pip install taosmd`</sub>
- **[OpenInstinct](https://github.com/Merit-Systems/OpenInstinct)** — iMessage assistant that drives a real browser to do chores, book tickets, and handle groceries, keeping your passwords and cards in an encrypted vault it unlocks per action. Self-hosted on your own Vercel, any model.
  <sub>★ 494 · TypeScript · MIT · clone · pushed 2026-11-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Merit-Systems/OpenInstinct.git`</sub>
- **[Dodaios](https://github.com/Dodaios/Dodaios)** — Desktop voice and chat assistant for Windows, macOS, and Linux that runs CLI coding agents such as Claude Code, Codex, and Gemini CLI side by side in Git worktrees, with memory, scheduled routines, and any single model key or local models via Ollama.
  <sub>★ 444 · Python · Apache-2.0 · psh · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/Dodaios/Dodaios/main/install/install.ps1 | iex`</sub>
- **[Xiryn](https://github.com/SouravBeraAkaSpeed/xiryn)** — Open-source personal agent on your own machine: each agent gets its own Linux desktop in Docker, with an encrypted vault, any model under your keys, and Telegram control.
  <sub>★ 440 · TypeScript · MIT · psh · pushed 2026-11-02 · Win · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/SouravBeraAkaSpeed/xiryn/main/setup.ps1 | iex`</sub>
- **[lorca](https://github.com/egoist/lorca)** — E2E-encrypted personal agent chat: create bots, talk 1:1 or in group chats, and let them hand work to each other. Rust CLI, native macOS client, and phone apps.
  <sub>★ 380 · Rust · GPL-3.0 · source · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/egoist/lorca.git`</sub>
- **[rho](https://github.com/mikeyobrien/rho)** — Stays running, remembers across sessions, and checks in on its own. macOS, Linux, Android.
  <sub>★ 378 · TypeScript · MIT · npm · pushed 2026-11-12 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g @rhobot-dev/rho`</sub>
- **[iva](https://github.com/smixs/iva-agent)** — Telegram assistant that turns your messages, voice notes and photos into an Obsidian-compatible markdown vault it remembers across sessions. Crons, skills, MCP and Google Workspace from an in-chat menu. Self-hosted in one command, MIT.
  <sub>★ 301 · TypeScript · MIT · script · pushed 2026-11-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/smixs/iva-agent/main/install.sh | bash`</sub>
- **[Overlay](https://github.com/LayerNorm/overlay-web)** — Open-source workspace where humans and agents share context — knowledge, files, memory, connected apps — so you delegate repeatable work to agents, review what they produce, and take action through tools, provider-neutral.
  <sub>★ 197 · HTML · AGPL-3.0 · source · pushed 2026-11-20</sub>
  <sub>`git clone https://github.com/LayerNorm/overlay-web.git`</sub>
- **[lemon](https://github.com/z80dev/lemon)** — Local-first assistant and coding agent runtime.
  <sub>★ 138 · Elixir · script · pushed 2026-11-19 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/z80dev/lemon/main/install.sh | sh`</sub>
- **[automata](https://github.com/sentientwave/automata)** — Matrix-native workspace where Temporal-backed durable workflows survive restarts and keep long tasks moving.
  <sub>★ 115 · Elixir · source · pushed 2026-09-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/sentientwave/automata.git`</sub>
- **[assistant](https://github.com/kcosr/assistant)** — Panel-based assistant whose plugins share one workspace of notes, lists, and objects.
  <sub>★ 92 · TypeScript · clone · pushed 2026-11-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kcosr/assistant`</sub>
- **[Hivekeep](https://github.com/MarlBurroW/hivekeep)** — Self-hosted team of specialized agents with persistent memory that delegate and build their own tools and mini-apps. Telegram, Slack, Discord, Matrix. Single container, MIT.
  <sub>★ 83 · TypeScript · MIT · script · pushed 2026-11-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/MarlBurroW/hivekeep/main/install.sh | bash`</sub>
- **[ghostclaw](https://github.com/b1rdmania/ghostclaw)** — An AI that lives on your computer and does things for you.
  <sub>★ 67 · TypeScript · MIT · script · pushed 2026-10-24 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://ghostclaw.io/install.sh | bash`</sub>
- **[jelly](https://github.com/dctanner/jelly)** — Local-first multi-bot system for running your operation from one VM: persistent agents grouped into project directories, phone-friendly web UI via Tailscale, browser control, and sudo on request.
  <sub>★ 67 · TypeScript · MIT · clone · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dctanner/jelly.git`</sub>
- **[Grux](https://github.com/dotcomjack/grux)** — Native macOS agent that runs agent swarms in parallel, opens terminal sessions it can undo, and reaches your mail, calendar and meetings; runs on a local Ollama model or your own Anthropic key, and any coding agent can drive it over MCP or its CLI.
  <sub>★ 32 · Swift · MIT · npx · pushed 2026-11-13 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npx @dotcomjack/grux`</sub>
- **[Hotline](https://github.com/1broseidon/hotline)** — Self-hosted chat room for a team of agents you reach from desktop or phone, each with its own Linux computer in a container, plus scheduled jobs, voice calls, and teammates that hand work to each other. Any model; Claude Code and Codex over ACP.
  <sub>★ 16 · Rust · Apache-2.0 · script · pushed 2026-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://hotline.dev/install | sh`</sub>
- **[lucinate](https://github.com/lucinate-ai/lucinate)** — Terminal-native chat client for OpenClaw, Hermes, Ollama, and OpenAI-compatible providers, with cron management and session browsing.
  <sub>★ 13 · Go · Apache-2.0 · psh · pushed 2026-11-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/lucinate-ai/lucinate/main/install/lucinate.ps1 | iex`</sub>
- **[Borg](https://github.com/adelphidata/borg)** — Security-first assistant in Rust built to run unattended, with a sandbox on by default, self-healing, long-term memory, schedules, and sub-agents, reachable over Telegram, Slack, Discord, Signal, WhatsApp, iMessage, a TUI, or a desktop app.
  <sub>★ 9 · Rust · MIT · script · pushed 2026-11-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/adelphidata/borg/main/scripts/install.sh | bash`</sub>
- **[OpenAmer](https://github.com/openamer/openamer)** — Windows-native personal agent runtime that drives the real desktop in the background (filesystem, terminal, GUI, browser via CDP), keeps persistent memory, runs scheduled jobs, and coordinates peer instances over a local A2A mesh.
  <sub>★ 8 · Python · Apache-2.0 · script · pushed 2026-11-20 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/openamer/openamer/main/scripts/install.sh | bash`</sub>

## Resting

- **[vibe-kanban](https://github.com/BloopAI/vibe-kanban)** — Kanban board for managing AI coding agents.
  <sub>★ 28.8k · Rust · Apache-2.0 · npx · pushed 2026-11-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibe-kanban`</sub>
- **[1code](https://github.com/21st-dev/1code)** — Orchestration layer for Claude Code and Codex.
  <sub>★ 5.6k · TypeScript · Apache-2.0 · source · pushed 2026-03-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/21st-dev/1code.git`</sub>
- **[CodexMonitor](https://github.com/Dimillian/CodexMonitor)** — Orchestrate multiple Codex agents across local workspaces.
  <sub>★ 4.4k · TypeScript · MIT · source · pushed 2026-03-26 · macOS</sub>
  <sub>`git clone https://github.com/Dimillian/CodexMonitor.git`</sub>
- **[ralphy](https://github.com/michaelshimeles/ralphy)** — Bash script that loops Claude Code, Codex, OpenCode, Cursor, Qwen, or Droid until the task is done.
  <sub>★ 3k · TypeScript · npm · pushed 2026-02-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g ralphy-cli`</sub>
- **[antfarm](https://github.com/snarktank/antfarm)** — Build your agent team in OpenClaw with one command.
  <sub>★ 2.5k · TypeScript · MIT · script · pushed 2026-02-26 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/snarktank/antfarm/v0.5.1/scripts/install.sh | bash`</sub>
- **[cashclaw](https://github.com/moltlaunch/cashclaw)** — An autonomous agent that takes work, does work, gets paid, and gets better at it.
  <sub>★ 1.2k · TypeScript · MIT · npm · pushed 2026-03-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cashclaw-agent`</sub>
- **[clawe](https://github.com/getclawe/clawe)** — Multi-agent coordination system: think Trello for OpenClaw agents.
  <sub>★ 751 · TypeScript · AGPL-3.0 · clone · pushed 2026-02-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/getclawe/clawe.git`</sub>
- **[opengoat](https://github.com/marian2js/opengoat)** — Build organizations of OpenClaw agents coordinating across Codex, Claude Code, Cursor, and OpenCode.
  <sub>★ 428 · TypeScript · MIT · npm · pushed 2026-04-12 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`npm i -g openclaw opengoat`</sub>
- **[subtask](https://github.com/zippoxer/subtask)** — Claude Skill that runs your tasks through subagents in git worktrees.
  <sub>★ 338 · Go · MIT · psh · pushed 2026-10-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/zippoxer/subtask/main/scripts/install.ps1 | iex`</sub>
- **[lettabot](https://github.com/letta-ai/lettabot)** — Personal assistant that remembers everything.
  <sub>★ 328 · TypeScript · Apache-2.0 · clone · pushed 2026-05-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/letta-ai/lettabot.git`</sub>
- **[mercury](https://github.com/Michaelliv/mercury)** — Personal AI assistant that lives where you chat.
  <sub>★ 143 · TypeScript · npm · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mercury-ai`</sub>
- **[babyagi3](https://github.com/yoheinakajima/babyagi3)** — A minimal AI agent you configure once, then run through natural language.
  <sub>★ 130 · Python · MIT · clone · pushed 2026-03-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yoheinakajima/babyagi3`</sub>
- **[wreckit](https://github.com/mikehostetler/wreckit)** — Run the Ralph Wiggum loop over your roadmap.
  <sub>★ 129 · Elixir · MIT · npm · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g wreckit`</sub>
- **[gnap](https://github.com/farol-team/gnap)** — Git-native agent protocol coordinating agents through a shared repo as a task board, with no orchestrator process.
  <sub>★ 87 · MIT · source · pushed 2026-03-17</sub>
  <sub>`git clone https://github.com/farol-team/gnap.git`</sub>
- **[swarm-protocol](https://github.com/phuryn/swarm-protocol)** — Headless coordination over MCP: claim work, detect file conflicts, heartbeat, and hand off across sessions.
  <sub>★ 56 · TypeScript · MIT · clone · pushed 2026-03-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/phuryn/swarm-protocol.git`</sub>
- **[wit](https://github.com/amaar-mc/wit)** — Locks individual functions rather than files via Tree-sitter, warning agents of conflicts before they write.
  <sub>★ 46 · TypeScript · MIT · bun · pushed 2026-03-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bun install -g wit-protocol`</sub>


---

Snapshot 2026-11-20. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
