# Orchestrators

The original list this workbook grew from: tools that run several coding agents at once.

Curated by **[andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

194 entries · 194 distinct repos · 8 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/buhuipao/agent-console"><img src="https://raw.githubusercontent.com/buhuipao/agent-console/main/docs/assets/demo.gif" width="260"></a> | <a href="https://github.com/asheshgoplani/agent-deck"><img src="https://opengraph.githubassets.com/1/asheshgoplani/agent-deck" width="260"></a> | <a href="https://github.com/YoanWai/agent-manager"><img src="https://raw.githubusercontent.com/YoanWai/agent-manager/main/docs/demo.gif" width="260"></a> |
| **[agent-console](https://github.com/buhuipao/agent-console)**<br>★ 16 | **[agent-deck](https://github.com/asheshgoplani/agent-deck)**<br>★ 827 | **[agent-manager](https://github.com/YoanWai/agent-manager)**<br>★ 386 |
| <a href="https://github.com/agent-of-empires/agent-of-empires"><img src="https://raw.githubusercontent.com/agent-of-empires/agent-of-empires/main/docs/assets/demo.gif" width="260"></a> | <a href="https://github.com/madarco/agentbox"><img src="https://raw.githubusercontent.com/madarco/agentbox/main/docs/demo.gif" width="260"></a> | <a href="https://github.com/umputun/agterm"><img src="https://raw.githubusercontent.com/umputun/agterm/master/docs/screenshots/main.png" width="260"></a> |
| **[agent-of-empires](https://github.com/agent-of-empires/agent-of-empires)**<br>★ 3.2k | **[agentbox](https://github.com/madarco/agentbox)**<br>★ 382 | **[agterm](https://github.com/umputun/agterm)**<br>★ 559 |

## Contents

- [Parallel Coding Agents — Terminal (TUI/CLI)](#parallel-coding-agents--terminal-tuicli) (15)
- [Parallel Coding Agents — Desktop &amp; Web](#parallel-coding-agents--desktop--web) (56)
- [Multi-Agent Swarms](#multi-agent-swarms) (25)
- [Autonomous Loop Runners](#autonomous-loop-runners) (11)
- [Autonomous Task Runners](#autonomous-task-runners) (19)
- [Agent Infrastructure &amp; Primitives](#agent-infrastructure--primitives) (19)
- [Personal Assistants](#personal-assistants) (32)
- [Resting](#resting) (17)

## Parallel Coding Agents — Terminal (TUI/CLI)

- **[herdr](https://github.com/herdrdev/herdr)** — Background runtime that owns your agents' terminals: sessions survive reboot and reattach from any terminal or SSH, panes are marked working/blocked/idle, and agents themselves spawn panes and prompt each other over a CLI and socket API. One Rust binary.
  <sub>★ 34.7k · Rust · Apache-2.0 · brew · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`brew install herdr`</sub>
- **[cmux](https://github.com/manaflow-ai/cmux)** — Ghostty-based macOS terminal with vertical tabs and per-agent notifications, built for keeping many concurrent sessions legible.
  <sub>★ 26.7k · Swift · brew · pushed 2026-09-02 · macOS</sub>
  <sub>`brew tap manaflow-ai/cmux`</sub>
- **[claude-squad](https://github.com/smtg-ai/claude-squad)** — Runs each agent as a detached background session with its own worktree, so work continues after you close the pane. Claude Code, Codex, OpenCode, Amp.
  <sub>★ 8.4k · Go · AGPL-3.0 · brew · pushed 2026-08-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install claude-squad`</sub>
- **[agent-of-empires](https://github.com/agent-of-empires/agent-of-empires)** — Pairs a TUI with a matching web view, so the same sessions stay reachable from a phone. Claude Code, Codex, OpenCode, Gemini, Mistral Vibe.
  <sub>★ 3.2k · Rust · MIT · clone · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/agent-of-empires/agent-of-empires`</sub>
- **[dmux](https://github.com/standardagents/dmux)** — Dev agent multiplexer pairing coding agents with git worktrees over tmux.
  <sub>★ 1.8k · HTML · MIT · npm · pushed 2026-08-16 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g dmux`</sub>
- **[agent-deck](https://github.com/asheshgoplani/agent-deck)** — One TUI covering sessions across Claude Code, Codex, Gemini, and OpenCode, with live status and resume for each.
  <sub>★ 827 · Go · MIT · go · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/asheshgoplani/agent-deck/cmd/agent-deck@latest`</sub>
- **[agterm](https://github.com/umputun/agterm)** — Native macOS terminal with named workspaces, a live dashboard, attention states, and a scriptable control API.
  <sub>★ 559 · Swift · MIT · brew · pushed 2026-09-02 · macOS</sub>
  <sub>`brew install --cask umputun/apps/agterm`</sub>
- **[tmux-ide](https://github.com/wavyrai/tmux-ide)** — Turns any project into a tmux IDE from a checked-in `ide.yml`, including preset agent-team layouts.
  <sub>★ 541 · TypeScript · MIT · npm · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g tmux-ide@beta`</sub>
- **[agent-manager](https://github.com/YoanWai/agent-manager)** — tmux TUI with live status, a prompt that lands in the pane without attaching, and in-terminal diff review that sends line comments back to the agent. Claude Code, Codex, OpenCode, Grok, Gemini CLI, Pi, Hermes.
  <sub>★ 386 · Go · Apache-2.0 · brew · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`brew install yoanwai/tap/agent-manager`</sub>
- **[agentbox](https://github.com/madarco/agentbox)** — Gives each agent its own sandboxed VM — local Docker or cloud via Hetzner, Daytona, Vercel, or E2B — with sub-second checkpoint starts.
  <sub>★ 382 · TypeScript · MIT · clone · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/madarco/agentbox`</sub>
- **[amux](https://github.com/andyrewlee/amux)** — Minimal TUI for spawning parallel coding agents in git worktrees.
  <sub>★ 154 · Go · MIT · go · pushed 2026-08-27 · WSL2 · macOS · Linux</sub>
  <sub>`go install github.com/andyrewlee/amux/cmd/amux@latest`</sub>
- **[openkanban](https://github.com/TechDufus/openkanban)** — Kanban board for orchestrating coding agents, rendered entirely in the terminal.
  <sub>★ 142 · Go · AGPL-3.0 · go · pushed 2026-06-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/techdufus/openkanban@latest`</sub>
- **[thurbox](https://github.com/Thurbeen/thurbox)** — TUI orchestrator with remote SSH sessions, inter-session messaging, and a native code-review view. Works with any CLI agent you define.
  <sub>★ 60 · Rust · MIT · winget · pushed 2026-09-02 · macOS · Linux</sub>
  <sub>`winget install Thurbeen.thurbox`</sub>
- **[repomon](https://github.com/AliHamzaAzam/repomon)** — Rust TUI that supervises a fleet across many repositories at once, in durable tmux sessions you can approve from your phone.
  <sub>★ 17 · Rust · Apache-2.0 · psh · pushed 2026-08-29 · macOS · Linux</sub>
  <sub>`irm https://github.com/AliHamzaAzam/repomon/releases/latest/download/install.ps1 | iex`</sub>
- **[agent-console](https://github.com/buhuipao/agent-console)** — Rust TUI that finds Codex and Claude Code sessions from the providers' own transcripts, including ones started elsewhere, and resumes their native UI rather than replacing it. No tmux or worktrees.
  <sub>★ 16 · Rust · Apache-2.0 · cargo · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install agent-console`</sub>

## Parallel Coding Agents — Desktop &amp; Web

- **[Orca](https://github.com/stablyai/orca)** — Agentic development environment for running a fleet on your own subscription, available on desktop and mobile.
  <sub>★ 59.9k · TypeScript · MIT · brew · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask stablyai/orca/orca`</sub>
- **[t3code](https://github.com/pingdotgg/t3code)** — Harness control surface available as web, mobile, and desktop app. Claude Code, Codex, Cursor, Grok Build, OpenCode.
  <sub>★ 21.5k · TypeScript · MIT · winget · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install T3Tools.T3Code`</sub>
- **[Paseo](https://github.com/getpaseo/paseo)** — Self-hosted daemon running agents in parallel on your own machines, driven from desktop, iOS/Android, web, or CLI, with voice control, diff review, and no telemetry or forced log-ins. Claude Code, Codex, Copilot, OpenCode, Pi.
  <sub>★ 15.8k · TypeScript · npm · pushed 2026-09-02 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`npm install -g @getpaseo/cli`</sub>
- **[Aperant](https://github.com/AndyMik90/Aperant)** — Runs up to 12 agent terminals with a self-validating QA loop and automatic conflict resolution when merging back to main.
  <sub>★ 14.5k · TypeScript · AGPL-3.0 · source · pushed 2026-06-14 · macOS</sub>
  <sub>`git clone https://github.com/AndyMik90/Aperant.git`</sub>
- **[qm](https://github.com/yc-software/qm)** — Multiplayer harness where each teammate gets an isolated workspace to run agents independently, driven from Slack or the web.
  <sub>★ 14.5k · TypeScript · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:<org>/qm-private`</sub>
- **[superset](https://github.com/superset-sh/superset)** — Code editor built around running many agents on your machine at once.
  <sub>★ 13.7k · TypeScript · brew · pushed 2026-09-02 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install superset-sh/tap/superset`</sub>
- **[humanlayer](https://github.com/humanlayer/humanlayer)** — Human-in-the-loop control for coding agents on hard problems; the repo notes its code is now largely deprecated in favor of a rebuild.
  <sub>★ 11.4k · TypeScript · source · pushed 2026-06-19 · macOS</sub>
  <sub>`git clone https://github.com/humanlayer/humanlayer.git`</sub>
- **[agent-orchestrator](https://github.com/Untrivial-ai/agent-orchestrator)** — Agent IDE for fleets that plans the work, spawns the agents, then fixes CI failures and merge conflicts without being asked.
  <sub>★ 10.9k · Go · Apache-2.0 · clone · pushed 2026-09-02 · macOS</sub>
  <sub>`git clone https://github.com/Untrivial-ai/agent-orchestrator.git`</sub>
- **[OpenChamber](https://github.com/openchamber/openchamber)** — Open-source workspace for running, supervising, and reviewing AI coding work across desktop, browser, editor, and mobile, with parallel model runs and per-run worktrees.
  <sub>★ 9.5k · TypeScript · MIT · script · pushed 2026-09-02 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/openchamber/openchamber/main/scripts/install.sh | bash`</sub>
- **[Emdash](https://github.com/generalaction/emdash)** — Agentic development environment running parallel agents against any model provider.
  <sub>★ 5.6k · TypeScript · Apache-2.0 · brew · pushed 2026-09-02 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask emdash`</sub>
- **[automaker](https://github.com/AutoMaker-Org/automaker)** — Describe features on a Kanban board and agents implement them in isolated worktrees, running tests and committing as they go.
  <sub>★ 3.2k · TypeScript · clone · pushed 2026-05-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/AutoMaker-Org/automaker.git`</sub>
- **[bb](https://github.com/get-bb/bb)** — Self-controlling agentic IDE that orchestrates multiple coding agents in live threads you can follow, steer, or hand off, driven from a desktop app, web app, CLI, or HTTP API.
  <sub>★ 3k · TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`npx bb-app@latest`</sub>
- **[collaborator](https://github.com/collabs-inc/collab-public)** — Arranges terminals, editors, and files as tiles on an infinite pan-and-zoom canvas instead of tabs.
  <sub>★ 2.9k · TypeScript · script · pushed 2026-08-08 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/collaborator-ai/collab-public/main/install.sh | bash`</sub>
- **[CodeNomad](https://github.com/NeuralNomadsAI/CodeNomad)** — Desktop and web workspace around the OpenCode CLI whose SideCars embed local tools like VS Code and terminals as tabs.
  <sub>★ 2.5k · TypeScript · MIT · npx · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @neuralnomads/codenomad --password <your-password> --launch`</sub>
- **[supacode](https://github.com/supabitapp/supacode)** — Native macOS command center for worktree-per-agent development.
  <sub>★ 2.3k · Swift · source · pushed 2026-08-26 · macOS</sub>
  <sub>`git clone https://github.com/supabitapp/supacode.git`</sub>
- **[mux](https://github.com/coder/xum)** — Desktop app for isolated, parallel agentic development.
  <sub>★ 2k · TypeScript · AGPL-3.0 · source · pushed 2026-09-02 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/coder/mux.git`</sub>
- **[synara](https://github.com/Emanuele-web04/synara)** — GUI desktop workspace for running and managing agents across local projects.
  <sub>★ 1.6k · TypeScript · MIT · clone · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Emanuele-web04/synara.git`</sub>
- **[nimbalyst](https://github.com/nimbalyst/nimbalyst)** — Visual workspace pairing parallel worktree sessions with kanban and direct visual editing. Claude Code, Codex, OpenCode.
  <sub>★ 1.6k · TypeScript · MIT · source · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/nimbalyst/nimbalyst.git`</sub>
- **[Traycer](https://github.com/traycerai/traycer)** — Bring-your-own-agent workspace running many sessions in parallel with context shared across models and providers, plus agent-to-agent messaging, shareable boards, and cross-device sync.
  <sub>★ 1.4k · TypeScript · MIT · source · pushed 2026-09-02 · macOS · Linux</sub>
  <sub>`git clone https://github.com/traycerai/traycer.git`</sub>
- **[Waku](https://github.com/egoist/waku)** — Native macOS desktop app for working with local coding agents, keeping projects, sessions, and transcripts on your machine. Supports Amp, Claude Code, Codex CLI, Cursor CLI, Grok Build, OpenCode, and Pi.
  <sub>★ 1.3k · Rust · GPL-3.0 · script · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://waku.sh/install.sh | sh`</sub>
- **[jean](https://github.com/coollabsio/jean)** — Desktop and web app for orchestrating agents across multiple projects and their git worktrees. Claude, Codex, OpenCode.
  <sub>★ 1.3k · TypeScript · Apache-2.0 · brew · pushed 2026-08-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew tap coollabsio/jean`</sub>
- **[Comet](https://github.com/zeronsh/comet)** — Cross-device control plane for coding agents, syncing sessions across machines and keeping agents running on an always-on daemon. Claude Code, Codex, Cursor, Grok, Hermes, Pi.
  <sub>★ 1.2k · Rust · MIT · script · pushed 2026-08-25 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://zeron.sh/install.sh | sh`</sub>
- **[takopi](https://github.com/banteg/takopi)** — Telegram bridge that puts Codex, Claude Code, OpenCode, and Pi sessions in a chat thread.
  <sub>★ 1k · Python · MIT · uv · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install -U takopi`</sub>
- **[parallel-code](https://github.com/johannesjo/parallel-code)** — Desktop app running Claude Code, Codex, and Gemini CLI side by side in isolated worktrees, with a built-in diff viewer and one-click merge.
  <sub>★ 999 · TypeScript · MIT · clone · pushed 2026-08-29 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/johannesjo/parallel-code.git`</sub>
- **[IM.codes](https://github.com/im4codes/imcodes)** — Mobile and web control layer built for away-from-desk continuation, with terminal access, git views, localhost preview, and scheduled tasks. Claude Code, Codex, Gemini CLI.
  <sub>★ 973 · TypeScript · MIT · npm · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g imcodes`</sub>
- **[Berd](https://github.com/block/berd)** — Block's open-source desktop app for working with AI agents: project chats with per-folder worktree behavior over the Goose backend, with agents, skills, connections, and agent sharing in one place.
  <sub>★ 857 · TypeScript · Apache-2.0 · source · pushed 2026-09-02 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/block/berd.git`</sub>
- **[ai-maestro](https://github.com/23blocks-OS/ai-maestro)** — Dashboard spanning multiple machines, adding memory search, code-graph queries, and agent-to-agent messaging. Claude, Aider, Cursor.
  <sub>★ 762 · TypeScript · MIT · script · pushed 2026-08-29 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/23blocks-OS/ai-maestro/main/scripts/remote-install.sh | sh`</sub>
- **[kandev](https://github.com/kdlbs/kandev)** — Kanban workbench whose multi-step workflows assign a different agent per step behind human gates, running locally, in Docker, over SSH, or in cloud executors.
  <sub>★ 730 · Go · AGPL-3.0 · scoop · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`scoop bucket add kandev https://github.com/kdlbs/scoop-kandev scoop install kandev`</sub>
- **[Alethe](https://github.com/Kc1t/alethe-agents)** — Local-first desktop workspace where agents and shells run as real PTYs in split panes and custom grids across projects, surviving pane close and app restart. Suspend idle groups to reclaim memory and resume with scrollback intact. Claude Code, Codex, OpenCode.
  <sub>★ 518 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Kc1t/alethe-agents.git`</sub>
- **[omg.dev](https://github.com/BennyKok/omg.dev)** — Open-source parallel-agent harness: run coding agents on your own computer or a hosted one, controlled from a single web UI with a mobile client. Claude Code, Codex, Grok, Cursor, OpenCode, Copilot, Pi.
  <sub>★ 513 · TypeScript · MIT · bun · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`bun install --global @omg-dev/cli`</sub>
- **[Proliferate](https://github.com/proliferate-ai/proliferate)** — Agent IDE that runs sessions locally or in the cloud and lets you build reusable workflows from them.
  <sub>★ 457 · TypeScript · AGPL-3.0 · source · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/proliferate-ai/proliferate.git`</sub>
- **[Open Session](https://github.com/tellahq/opensession)** — Self-hosted server driving coding sessions in git worktrees on your own box or in isolated sandboxes, with a web UI, Slack/Linear/Plain/GitHub intake, diff and PR review, and multiple Codex and Claude subscriptions.
  <sub>★ 342 · TypeScript · MIT · script · pushed 2026-09-02 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/tellahq/opensession/main/install.sh | bash`</sub>
- **[dorothy](https://github.com/Charlie85270/Dorothy)** — Desktop app combining agent orchestration with automations, Kanban management, and MCP servers.
  <sub>★ 341 · TypeScript · MIT · clone · pushed 2026-07-07 · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/Charlie85270/Dorothy.git`</sub>
- **[aizen](https://github.com/vivy-company/aizen)** — macOS workspace that organizes worktrees, environments, and agent sessions per project.
  <sub>★ 302 · Swift · GPL-3.0 · clone · pushed 2026-08-01 · macOS</sub>
  <sub>`git clone https://github.com/vivy-company/aizen.git`</sub>
- **[diri](https://github.com/cristicretu/diri)** — Native macOS app running Claude Code, Codex, Cursor, Gemini, and shells in parallel across git worktrees or remote hosts, with live status, session persistence across restarts, a menu-bar rollup, and an MCP server for agents to spawn others.
  <sub>★ 279 · Rust · Apache-2.0 · brew · pushed 2026-09-01 · macOS</sub>
  <sub>`brew install --cask cristicretu/diri/diri`</sub>
- **[vibe-tree](https://github.com/sahithvibudhi/vibe-tree)** — One git worktree per agent, delivered as desktop, web, and CLI.
  <sub>★ 267 · TypeScript · MIT · brew · pushed 2026-07-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask --no-quarantine sahithvibudhi/tap/vibetree`</sub>
- **[constellagent](https://github.com/owengretzinger/constellagent)** — macOS app giving each agent its own terminal, editor, and git worktree in a single window.
  <sub>★ 215 · TypeScript · source · pushed 2026-05-05 · macOS</sub>
  <sub>`git clone https://github.com/owengretzinger/constellagent.git`</sub>
- **[ivy-tendril](https://github.com/Ivy-Interactive/Ivy-Tendril)** — Drives agents through a plan-based lifecycle with verification gates, self-improving memory, and human checkpoints. Claude Code, Codex, Antigravity, Copilot, OpenCode.
  <sub>★ 175 · C# · psh · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://cdn.ivy.app/install-tendril.ps1 | iex`</sub>
- **[Ouijit](https://github.com/ouijit/ouijit)** — Kanban board and terminals wired together by lifecycle hooks, scripts, and a session-aware CLI, so a task runs by hand, on a script, or delegated to the agent. Per-task worktrees, optional VM sandboxing. Claude Code, Codex, Pi, OpenCode.
  <sub>★ 164 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-02 · macOS · Linux</sub>
  <sub>`git clone https://github.com/ouijit/ouijit.git`</sub>
- **[Tempest](https://github.com/tempestai-dev/tempest)** — Tauri desktop ADE running CLI agents in parallel isolated worktrees, with a shared local code-knowledge graph that cuts token use across sessions, plus live status and built-in diff/PR review.
  <sub>★ 163 · TypeScript · Apache-2.0 · clone · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/tempestai-dev/tempest`</sub>
- **[clideck](https://github.com/rustykuntz/clideck)** — Chat-app-style dashboard with autopilot routing between agents and full control from a phone. Claude Code, Codex, Gemini CLI, OpenCode.
  <sub>★ 153 · JavaScript · MIT · npm · pushed 2026-08-19 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g clideck`</sub>
- **[Claude Command Center (CCC)](https://github.com/amirfish1/claude-command-center)** — Local dashboard for spawning, monitoring, and resuming sessions across Claude Code, Codex, Cursor, Antigravity, and Kilo Code.
  <sub>★ 135 · Python · psh · pushed 2026-09-02 · macOS</sub>
  <sub>`irm https://raw.githubusercontent.com/amirfish1/claude-command-center/main/scripts/install.ps1 | iex`</sub>
- **[tlbx](https://github.com/tlbx-ai/tlbx)** — Self-hosted browser workspace holding persistent real PTY sessions on your own machines, reachable from any browser or phone.
  <sub>★ 106 · C# · AGPL-3.0 · psh · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://get.tlbx.ai/install.ps1 | iex`</sub>
- **[Garcon](https://github.com/cfal/garcon)** — Self-hosted browser and mobile workspace with diff review, Git/PR workflows, mobile approvals, scheduling, and cross-agent transfers. Seven CLI agents.
  <sub>★ 66 · TypeScript · clone · pushed 2026-09-02 · Win · WSL2? · Linux · Docker</sub>
  <sub>`git clone https://github.com/cfal/garcon.git`</sub>
- **[GraphCode](https://github.com/scgopi/GraphCode)** — macOS app that wires agent sessions into a graph: each node is a live terminal you can attach to mid-run, each edge a hand-off, message, or spawn that fires while you're away. Claude Code, Copilot CLI, Codex.
  <sub>★ 62 · Swift · brew · pushed 2026-09-02 · macOS</sub>
  <sub>`brew install --cask scgopi/graphcode/graphcode`</sub>
- **[clave](https://github.com/codika-io/clave)** — Native macOS app with split and grid layouts, session groups, SSH remote sessions, and usage analytics for Claude Code.
  <sub>★ 47 · TypeScript · MIT · npx · pushed 2026-09-01 · macOS</sub>
  <sub>`npx plugins add codika-io/clave`</sub>
- **[Tortie](https://github.com/gregce/tortie)** — Native macOS agent multiplexer with familiar IDE features: all projects in one window, agents that survive restarts, and organized terminal sessions without tmux.
  <sub>★ 45 · TypeScript · Apache-2.0 · source · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/gregce/tortie.git`</sub>
- **[vibecraft](https://github.com/rayzhudev/vibecraft)** — RTS-style workspace for commanding coding agents.
  <sub>★ 35 · TypeScript · Apache-2.0 · source · pushed 2026-07-19 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/rayzhudev/vibecraft.git`</sub>
- **[intentic](https://github.com/intentic/intentic)** — Browser and mobile workspace where every agent gets a persistent Docker sandbox on a machine you own plus a git worktree of its own, reached over an outbound-only Cloudflare tunnel, so runs keep going after you close the tab. Plan mode, per-hunk diff review, an environment Dockerfile the agent proposes and you approve, credential capabilities injected per turn, and schedule, webhook or event triggers. Claude Code, Codex, Grok, Kimi Code, Gemini. MIT.
  <sub>★ 30 · TypeScript · MIT · script · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://intentic.dev/sync | sh`</sub>
- **[AGX](https://github.com/ramarlina/agx)** — Wake-work-sleep checkpointing keeps a persistent agent team on long objectives, with human gates between cycles.
  <sub>★ 27 · TypeScript · npm · pushed 2026-05-06 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g @mndrk/agx`</sub>
- **[Fletch](https://github.com/fwdai/fletch)** — Native macOS IDE that seals each agent in its own repo clone under Seatbelt or Docker, serves each a shared symbol and call-graph index over MCP, and gates every step on tests or your approval. Claude Code, Codex, Cursor, OpenCode.
  <sub>★ 24 · Rust · AGPL-3.0 · source · pushed 2026-08-26 · macOS</sub>
  <sub>`git clone https://github.com/fwdai/fletch.git`</sub>
- **[octomux](https://github.com/ShreyPaharia/octomux)** — Local dashboard with a kanban fleet view, one unified permission inbox across agents, and in-app diff review.
  <sub>★ 22 · TypeScript · MIT · npm · pushed 2026-09-01 · macOS</sub>
  <sub>`npm install -g octomux`</sub>
- **[agent-squid](https://github.com/agent-squid/squid)** — Browser UI organized into named lanes (`#topic@agent`), with context shared across agents and a realtime quota gauge.
  <sub>★ 15 · JavaScript · MIT · script · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://agentsquid.ai/install.sh | bash`</sub>
- **[Zaivern Code](https://github.com/tacyan/zaivern-code)** — Cross-platform Rust desktop cockpit for running Claude Code, Codex, Gemini CLI, and 30+ coding agents in parallel, with fleet monitoring, mobile control, and line-level ownership to prevent merge conflicts.
  <sub>★ 8 · Rust · Apache-2.0 · psh · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/tacyan/zaivern-code/main/install.ps1 | iex`</sub>
- **[Better Agent](https://github.com/ofekron/better-agent)** — Local web workspace with persistent state, approvals, and restart recovery for native Claude, Codex, and Gemini sessions.
  <sub>unavailable</sub>
- **[jat](https://github.com/joewinke/jat)** — Visual dashboard combining live sessions, task management, code editor, and terminal, with parallel swarm workflows.
  <sub>unavailable</sub>

## Multi-Agent Swarms

- **[paperclip](https://github.com/paperclipai/paperclip)** — Self-hosted platform where agents wake on heartbeats to claim tickets, governed by org charts, budgets, and approval gates.
  <sub>★ 79.9k · TypeScript · MIT · npx · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx --registry https://registry.npmjs.org paperclipai onboard --yes`</sub>
- **[ruflo](https://github.com/ruvnet/ruflo)** — Meta-harness for deploying coordinated swarms and conversational multi-agent workflows. Formerly claude-flow.
  <sub>★ 70.2k · TypeScript · MIT · npm · pushed 2026-09-02 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g ruflo@latest`</sub>
- **[buzz](https://github.com/block/buzz)** — Agents are first-class members of shared channels on a Nostr relay you own, with their own keys and audit trails. Claude Code, Codex, Goose.
  <sub>★ 32k · Rust · Apache-2.0 · clone · pushed 2026-09-02 · macOS</sub>
  <sub>`git clone https://github.com/block/buzz.git`</sub>
- **[gastown](https://github.com/gastownhall/gastown)** — Scales to 20-30 agents with a coordinator, git-backed issue tracking, health watchdogs, and a Bors-style merge queue.
  <sub>★ 17.9k · Go · MIT · go · pushed 2026-09-02 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/steveyegge/gastown/cmd/gt@latest`</sub>
- **[ClawTeam](https://github.com/HKUDS/ClawTeam)** — Agents spawn and manage their own teammates from one command, coordinating through file-based or P2P inboxes across tmux worktrees.
  <sub>★ 5.5k · Python · MIT · pip · pushed 2026-05-09 · WSL2 · macOS? · Linux</sub>
  <sub>`pip install clawteam`</sub>
- **[claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge)** — Workspace for mixing different vendors' CLI agents in one visible collaboration session.
  <sub>★ 3.5k · Python · npm · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @seemseam/ccb@latest`</sub>
- **[agentsmesh](https://github.com/AgentsMesh/AgentsMesh)** — Remote AI workstations with PTY sandboxes and worktree isolation, coordinating across channels and pod bindings. Claude Code, Codex, Gemini CLI, Aider, OpenCode.
  <sub>★ 2.3k · Go · script · pushed 2026-08-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentsmesh.ai/install.sh | sh`</sub>
- **[Agent Teams](https://github.com/777genius/agent-teams-ai)** — Desktop app where you give high-level commands to autonomous coding-agent teams across Claude Code, Codex, OpenCode, Cursor, Grok, GitHub Copilot, Kiro, Z.AI, MiniMax, Kimi, 200+ models, and 75+ LLM providers. Agents coordinate through inter-agent messaging, Kanban tasks, and built-in code review.
  <sub>★ 2k · TypeScript · AGPL-3.0 · clone · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/777genius/agent-teams-ai.git`</sub>
- **[scion](https://github.com/GoogleCloudPlatform/scion)** — Orchestration testbed running agents in parallel isolated containers with dynamic coordination and normalized telemetry.
  <sub>★ 1.7k · Go · Apache-2.0 · go · pushed 2026-09-02 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`go install github.com/GoogleCloudPlatform/scion/cmd/scion@latest`</sub>
- **[Orkas](https://github.com/Orkas-AI/Orkas)** — A commander agent decomposes goals and dispatches specialists with isolated skills and memory. Claude Code, Codex, OpenCode, Cline.
  <sub>★ 1.6k · TypeScript · MIT · clone · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Orkas-AI/Orkas.git`</sub>
- **[multi-agent-shogun](https://github.com/yohey-w/multi-agent-shogun)** — Shogun to karo to ashigaru hierarchy running up to 10 agents over tmux with no coordination API cost.
  <sub>★ 1.4k · Shell · MIT · clone · pushed 2026-08-06 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/yohey-w/multi-agent-shogun`</sub>
- **[Fusion](https://github.com/Runfusion/Fusion)** — Multi-node orchestrator with a kanban board, plan-review-execute gates, per-task worktrees, and hierarchical missions.
  <sub>★ 1.2k · TypeScript · MIT · npm · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @runfusion/fusion`</sub>
- **[loki-mode](https://github.com/asklokesh/loki-mode)** — PRD-to-deployed-product SDLC with 41 agents in 8 swarms, nine quality gates, and blind three-reviewer code review. Source-available under BUSL-1.1.
  <sub>★ 1.1k · Shell · npm · pushed 2026-08-31 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g loki-mode`</sub>
- **[hcom](https://github.com/aannoo/hcom)** — Lets agents message, watch, and spawn each other across terminals. Claude Code, Codex, Antigravity, Cursor, OpenCode, Kilo, and more.
  <sub>★ 473 · Rust · MIT · psh · pushed 2026-08-09 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://github.com/aannoo/hcom/releases/latest/download/hcom-installer.ps1 | iex`</sub>
- **[agent-kanban](https://github.com/saltbo/agent-kanban)** — Leader-worker task board with cryptographic agent identity. Claude Code, Codex, Gemini CLI.
  <sub>★ 466 · TypeScript · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/saltbo/agent-kanban.git`</sub>
- **[ORCH](https://github.com/oxgeneral/ORCH)** — CLI runtime managing agents as typed teams with an explicit state machine and goals. Claude Code, Codex, Cursor.
  <sub>★ 160 · TypeScript · MIT · npm · pushed 2026-08-01 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @oxgeneral/orch # Install`</sub>
- **[NXTG-Forge Orchestrator](https://github.com/nxtg-ai/forge-orchestrator)** — Coordinates Claude Code, Codex, and Gemini CLI on one shared repo through a research-plan-delegate-adversarial-verify-deploy pipeline, with file locking, knowledge capture, and drift detection. Single Rust binary.
  <sub>★ 158 · Rust · script · pushed 2026-08-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://forge.nxtg.ai/install.sh | sh`</sub>
- **[kodo](https://github.com/ikamensh/kodo)** — Directs agents through work cycles where a separate agent independently verifies each result. Claude Code, Codex, Gemini CLI.
  <sub>★ 130 · Python · MIT · uv · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install kodo-agent`</sub>
- **[tutti](https://github.com/nutthouse/tutti)** — Config-driven workflows passing typed artifacts between agents, each in its own worktree.
  <sub>★ 116 · Rust · MIT · cargo · pushed 2026-07-28 · WSL2 · macOS? · Linux</sub>
  <sub>`cargo install tutti`</sub>
- **[CompanyHelm](https://github.com/CompanyHelm/companyhelm)** — Distributed orchestrator with task management and direct agent-to-agent conversations.
  <sub>★ 74 · TypeScript · MIT · source · pushed 2026-08-28 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/CompanyHelm/companyhelm.git`</sub>
- **[5dive](https://github.com/5dive-ai/5dive)** — Named agents on a shared org chart and backlog hand work to each other and escalate to a human over Telegram. Claude Code, Codex, Grok, Antigravity, OpenCode.
  <sub>★ 54 · Shell · MIT · npx · pushed 2026-09-02 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npx -y skills add https://github.com/5dive-ai/skills --skill 5dive-cli --agent <runtime> --yes`</sub>
- **[Agon](https://github.com/AutoResearch-Factory/Agon)** — Orchestrates scientist, coder, and auditor loops from research topic through proposal to experiment.
  <sub>★ 45 · Python · MIT · clone · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AutoResearch-Factory/Agon.git`</sub>
- **[shire](https://github.com/victor36max/shire)** — Persistent team workspaces with inter-agent mailboxes and a shared drive. Claude Code, OpenCode, Pi.
  <sub>★ 39 · TypeScript · MIT · npm · pushed 2026-05-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agents-shire`</sub>
- **[corellis](https://github.com/CorellisOrg/Corellis)** — Multi-agent governance framework for OpenClaw — goal decomposition, fleet-wide memory, correction propagation, and approval workflows for 20+ agent fleets.
  <sub>★ 28 · Shell · MIT · clone · pushed 2026-04-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/CorellisOrg/corellis.git`</sub>
- **[orc](https://github.com/spencermarx/orc)** — Lightweight framework that piggybacks your existing CLI setup for planning, task decomposition, worktrees, and review.
  <sub>★ 23 · Shell · clone · pushed 2026-06-21 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/thefinalsource/orc.git`</sub>

## Autonomous Loop Runners

- **[Loop Engineering](https://github.com/cobusgreyling/loop-engineering)** — Designs repeatable coding-agent loops around automation, worktrees, skills, state, and verification, with starters and a Loop Ready score for Grok, Claude Code, Codex, and OpenCode.
  <sub>★ 10.8k · TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @cobusgreyling/loop init . --pattern daily-triage --tool claude`</sub>
- **[ralph-claude-code](https://github.com/frankbria/ralph-claude-code)** — Development loop for Claude Code with exit detection that recognizes when the work is actually finished.
  <sub>★ 9.6k · Shell · MIT · script · pushed 2026-07-18 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -sL https://raw.githubusercontent.com/frankbria/ralph-claude-code/main/uninstall.sh | bash`</sub>
- **[ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator)** — Hat-based orchestration that keeps agents looping until done, as a fuller implementation of the Ralph Wiggum technique.
  <sub>★ 3.1k · Rust · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ralph-orchestrator/ralph-cli`</sub>
- **[ralph-tui](https://github.com/subsy/ralph-tui)** — Drives an agent through a task list autonomously, with a TUI for watching the loop.
  <sub>★ 2.4k · TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx add-skill subsy/ralph-tui --all`</sub>
- **[ralphex](https://github.com/umputun/ralphex)** — Executes an implementation plan autonomously with a fresh session per task, plus validation, retries, multi-phase review, and automatic commits. Claude Code, Codex.
  <sub>★ 1.5k · Go · MIT · go · pushed 2026-09-01 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`go install github.com/umputun/ralphex/cmd/ralphex@latest`</sub>
- **[bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Keeps no model in the coordination loop, so orchestration costs zero tokens. Verifies with tests and auto-commits across 40+ CLI agents.
  <sub>★ 1.1k · Python · Apache-2.0 · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[fractal](https://github.com/plasma-ai/fractal)** — Loops that recursively delegate separable subtasks to child agents, bounded by configurable depth, cost, and time limits.
  <sub>★ 706 · Python · Apache-2.0 · uv · pushed 2026-09-02 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install plasma-fractal --with-executables-from plasma-wiki`</sub>
- **[LoopTroop](https://github.com/looptroop-ai/LoopTroop)** — An LLM council plans the work, then Ralph-style loops retry failed units with fresh context. Executes via OpenCode worktrees.
  <sub>★ 129 · TypeScript · MIT · scoop · pushed 2026-09-02 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`scoop bucket add looptroop https://github.com/looptroop-ai/scoop-bucket scoop install looptroop`</sub>
- **[MartinLoop](https://github.com/Keesan12/martin-loop)** — Caps spend, enforces policy, verifies output, and rolls back failures, leaving inspectable run receipts.
  <sub>★ 47 · TypeScript · Apache-2.0 · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g martin-loop`</sub>
- **[Dex](https://github.com/francescoalemanno/dex)** — Human-gated planning, multi-reviewer code review, and dead-end-aware research loops, shipped as cross-platform binaries for 7 CLI backends.
  <sub>★ 21 · Rust · MIT · psh · pushed 2026-06-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/francescoalemanno/dex/main/install.ps1 | iex`</sub>
- **[toryo](https://github.com/JesseRWeigel/toryo)** — Trust-based delegation with quality ratcheting that commits improvements and reverts regressions. Chains Claude Code, Aider, Gemini CLI, Ollama.
  <sub>★ 12 · TypeScript · MIT · npx · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @jweigel/toryo init # scaffold config + task specs`</sub>

## Autonomous Task Runners

- **[OpenHands](https://github.com/OpenHands/OpenHands)** — Self-hostable control center running its own agent or driving Claude Code, Codex, and any Agent Client Protocol agent, on schedules or webhooks.
  <sub>★ 86k · TypeScript · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[multica](https://github.com/multica-ai/multica)** — Managed agents platform where you assign tasks, track progress, and let agents compound skills between runs.
  <sub>★ 48.6k · Go · psh · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.ps1 | iex`</sub>
- **[symphony](https://github.com/openai/symphony)** — Turns project work into isolated autonomous runs, so teams manage the work rather than supervise the agent.
  <sub>★ 27k · Elixir · Apache-2.0 · source · pushed 2026-08-19 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/openai/symphony.git`</sub>
- **[open-swe](https://github.com/langchain-ai/open-swe)** — Invoked from Slack, Linear, or GitHub comments; each task runs in its own cloud sandbox and ends in a draft PR linked to the ticket.
  <sub>★ 10.7k · Python · MIT · clone · pushed 2026-09-02 · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/open-swe.git`</sub>
- **[claude-code-action](https://github.com/anthropics/claude-code-action)** — Anthropic's official GitHub Action, detecting from context whether to answer, review, or implement. Auth via Anthropic API, Bedrock, Vertex, or Foundry.
  <sub>★ 8.8k · TypeScript · MIT · gh-action · pushed 2026-09-01</sub>
  <sub>`uses: anthropics/claude-code-action@main # in .github/workflows/*.yml`</sub>
- **[gh-aw](https://github.com/github/gh-aw)** — Compiles agentic workflows written in Markdown into GitHub Actions YAML. Read-only by default, with writes only through sanitized safe-outputs. Copilot, Claude, Codex, Gemini.
  <sub>★ 5.1k · Go · MIT · gh-ext · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`gh extension install github/gh-aw`</sub>
- **[background-agents](https://github.com/ColeMurray/background-agents)** — Sessions trigger from a web UI, Slack, GitHub, Linear, webhooks, or cron, run in Modal, Daytona, Vercel, E2B, or OpenComputer sandboxes, and open attributed PRs.
  <sub>★ 2.7k · TypeScript · MIT · source · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ColeMurray/background-agents.git`</sub>
- **[run-gemini-cli](https://github.com/google-github-actions/run-gemini-cli)** — Google's official GitHub Action, running on event or schedule triggers or on demand via `@gemini-cli /review` and `/triage`.
  <sub>★ 2.1k · TypeScript · Apache-2.0 · gh-action · pushed 2026-08-21</sub>
  <sub>`uses: google-github-actions/run-gemini-cli@main # in .github/workflows/*.yml`</sub>
- **[codex-action](https://github.com/openai/codex-action)** — OpenAI's official GitHub Action, running Codex CLI headlessly under drop-sudo, unprivileged-user, or fully read-only sandboxes.
  <sub>★ 1.2k · TypeScript · Apache-2.0 · gh-action · pushed 2026-08-26</sub>
  <sub>`uses: openai/codex-action@main # in .github/workflows/*.yml`</sub>
- **[centaur](https://github.com/paradigmxyz/centaur)** — Multiplayer self-hosted agents with Slack-native conversations, Kubernetes sandboxes, shared tools, and durable workflows.
  <sub>★ 1.2k · Python · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/paradigmxyz/centaur.git`</sub>
- **[cyrus](https://github.com/cyrusagents/cyrus)** — Watches Linear, GitHub, GitLab, and Slack issues assigned to it, spinning up an isolated worktree per issue. Claude Code, Codex, Cursor, Gemini.
  <sub>★ 794 · TypeScript · Apache-2.0 · npm · pushed 2026-09-02 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g cyrus-ai`</sub>
- **[aeon](https://github.com/aeonfun/aeon)** — Runs unattended on GitHub Actions; dispatches skills to six coding-agent harnesses behind one contract (Claude Code, Grok, Codex, Pi, Vibe, Kimi), with quality scoring, git-persisted memory, a self-healing loop, and reactive triggers.
  <sub>★ 714 · TypeScript · MIT · clone · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/<you>/aeon`</sub>
- **[Factory](https://github.com/owainlewis/machinist)** — Keeps coding agents working on a repository without making a human orchestrate every step from a terminal, pulling tasks from trusted ticket queues into isolated Codex workspaces.
  <sub>★ 298 · Go · MIT · clone · pushed 2026-09-02 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/owainlewis/machinist.git`</sub>
- **[remote-swe-agents](https://github.com/aws-samples/remote-swe-agents)** — Serverless control plane on Lambda with a dedicated EC2 worker per session, triggered by issue comments, assignments, and PR reviews.
  <sub>★ 243 · TypeScript · MIT-0 · gh-action · pushed 2026-08-25</sub>
  <sub>`uses: aws-samples/remote-swe-agents@main # in .github/workflows/*.yml`</sub>
- **[Contrabass](https://github.com/junhoyeo/contrabass)** — Terminal-first orchestrator for issue-driven agent runs, pulling work from Linear, GitHub Issues, or a local board into git worktrees with TUI, headless, and dashboard modes.
  <sub>★ 220 · Go · Apache-2.0 · go · pushed 2026-07-17 · WSL2 · macOS · Linux</sub>
  <sub>`go install github.com/junhoyeo/contrabass/cmd/contrabass@latest`</sub>
- **[sortie](https://github.com/sortie-ai/sortie)** — Turns tracker tickets into agent sessions. Agent-agnostic and tracker-agnostic, as a single Go binary with SQLite persistence.
  <sub>★ 138 · Go · Apache-2.0 · brew · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask sortie-ai/tap/sortie`</sub>
- **[lalph](https://github.com/tim-smart/lalph)** — Orchestrator driven by whichever source of issues you point it at.
  <sub>★ 130 · TypeScript · MIT · npm · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g lalph`</sub>
- **[Taskuary](https://github.com/ldbumble/taskuary)** — Local-first work inbox that triages email, chat, issue trackers, and scheduled reports into supervised Claude Code, Codex, Gemini, Cursor, or Copilot CLI runs, with conflict-aware queuing, live terminals, and approval-gated replies.
  <sub>★ 43 · Python · MIT · pip · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install taskuary`</sub>
- **[NEEDLE](https://github.com/jedarden/NEEDLE)** — Runs unattended against a shared bead queue (SQLite, atomic claims), dispatching each bead to a headless CLI — Claude Code, Codex, OpenCode, Aider — with every outcome routed through an explicit state machine; no inter-agent channel, coordination is done at decomposition time.
  <sub>★ 18 · Rust · MIT · cargo · pushed 2026-09-02 · WSL2 · macOS? · Linux</sub>
  <sub>`cargo install --git https://github.com/jedarden/NEEDLE`</sub>

## Agent Infrastructure &amp; Primitives

- **[Archon](https://github.com/coleam00/Archon)** — Harness builder for deterministic AI coding workflows, combining agent steps with scripts, validation gates, approvals, and isolated git worktrees. Claude Code, Codex, and more.
  <sub>★ 23.3k · TypeScript · MIT · psh · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://archon.diy/install.ps1 | iex`</sub>
- **[NemoClaw](https://github.com/NVIDIA/NemoClaw)** — Runs Hermes, LangChain Deep Agents, and OpenClaw inside NVIDIA OpenShell with managed inference.
  <sub>★ 22.3k · TypeScript · Apache-2.0 · source · pushed 2026-09-02 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NVIDIA/NemoClaw.git`</sub>
- **[openfang](https://github.com/RightNow-AI/openfang)** — Open-source agent operating system.
  <sub>★ 18.2k · Rust · Apache-2.0 · psh · pushed 2026-07-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://openfang.sh/install.ps1 | iex`</sub>
- **[omnigent](https://github.com/omnigent-ai/omnigent)** — Meta-harness running Claude Code, Codex, Cursor, OpenCode, Hermes, Pi, or custom YAML agents against swappable sandbox backends, with policy enforcement.
  <sub>★ 9.6k · Python · Apache-2.0 · uv · pushed 2026-09-02 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`uv tool install omnigent # or: pip install "omnigent"`</sub>
- **[Open Multi-Agent](https://github.com/open-multi-agent/open-multi-agent)** — TypeScript-native runtime where a coordinator turns a goal into a task DAG and a deterministic scheduler runs specialized agents, with approvals, traces, evaluation, checkpoints, and resume support.
  <sub>★ 6.9k · TypeScript · MIT · source · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/open-multi-agent/open-multi-agent.git`</sub>
- **[sandbox-agent](https://github.com/rivet-dev/sandbox-agent)** — Daemon, HTTP/SSE API, and TypeScript SDK for driving six coding agents inside E2B, Daytona, Modal, Cloudflare Containers, or Docker.
  <sub>★ 1.6k · TypeScript · Apache-2.0 · npm · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @sandbox-agent/cli@0.4.x`</sub>
- **[Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS)** — Keeps specialist agents in a hub and spins up a temporary orchestrator per task, with A2A routing and governed memory gates. Formerly Hephaestus.
  <sub>★ 1.1k · Python · Apache-2.0 · script · pushed 2026-09-02 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/agentlas-ai/Agentlas-OS/main/scripts/install-all-runtimes.sh | bash`</sub>
- **[Claudexor](https://github.com/razzant/claudexor)** — Routes one coding thread across harnesses with quota-aware rotation between subscription profiles, Best-of-N runs, and cross-family review.
  <sub>★ 429 · TypeScript · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g claudexor`</sub>
- **[guild](https://github.com/mathomhaus/guild)** — Shared context, memory, and task coordination as a single Go binary over local SQLite with hybrid keyword and semantic search.
  <sub>★ 304 · Go · Apache-2.0 · psh · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://github.com/mathomhaus/guild/releases/latest/download/install.ps1 | iex`</sub>
- **[handoff](https://github.com/dazuiba/handoff)** — Delegates a task to DeepSeek, Codex, or Claude from inside your current Claude Code or Codex session, returning the result automatically.
  <sub>★ 88 · Python · uv · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install handoff-cli`</sub>
- **[sub-agents-skills](https://github.com/shinpr/sub-agents-skills)** — Portable Markdown definitions that route a task to a chosen backend, model, effort level, and permission set.
  <sub>★ 82 · Python · MIT · script · pushed 2026-09-01 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/shinpr/sub-agents-skills/main/install.sh | bash -s -- --target ~/.cursor/skills`</sub>
- **[agenttier](https://github.com/agenttier/agenttier)** — Kubernetes runtime giving each agent its own Pod and PVC sandbox behind a default-deny NetworkPolicy, with a streaming SSE invoke API.
  <sub>★ 61 · Go · Apache-2.0 · pip · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install agenttier # from PyPI`</sub>
- **[neuralyzer](https://github.com/gintasz/neuralyzer)** — Lets an agent wipe its own session context and re-run the first message, making Ralph loops easier to engineer.
  <sub>★ 39 · TypeScript · MIT · source · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gintasz/neuralyzer.git`</sub>
- **[Crewplane](https://github.com/crewplaneai/crewplane)** — CLI-first control plane that turns one-off coding-agent calls into reviewable Markdown workflows spanning Claude Code, Codex, Gemini CLI, or Copilot CLI. Explicit artifact handoffs keep execution inspectable on disk, while validated completed nodes let failed workflows resume instead of starting over.
  <sub>★ 36 · Python · Apache-2.0 · uv · pushed 2026-08-31 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install crewplane`</sub>
- **[codecast](https://github.com/codecast-sh/codecast)** — Watches your real local sessions and surfaces them in a live triage inbox, keeping a searchable record with line-level agent attribution. Claude Code, Codex, Cursor, Gemini.
  <sub>★ 30 · TypeScript · MIT · psh · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm codecast.sh/install.ps1 | iex`</sub>
- **[agent-runbook](https://github.com/KnoxOps/agent-runbook)** — Compiles YAML runbooks with loops, branching, and parallelism into SKILL.md files for Claude Code and Codex.
  <sub>★ 17 · Python · Apache-2.0 · pip · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/KnoxOps/agent-runbook.git`</sub>
- **[aGiTrack](https://github.com/core-aix/agitrack)** — Takes what a coding agent produces and commits each turn to git, recording the prompt, model, and that turn's token cost in the commit message, with the agent confined to its own worktree. Claude Code, Codex, and OpenCode.
  <sub>★ 17 · Python · Apache-2.0 · pipx · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`pipx install agitrack`</sub>
- **[LionClaw](https://github.com/moshthepitt/lionclaw)** — Local control plane running coding agents as durable, auditable workers with explicit state, skills, and checkpoints.
  <sub>★ 16 · Rust · MIT · clone · pushed 2026-09-01 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/moshthepitt/lionclaw.git`</sub>
- **[skillfold](https://github.com/byronxlg/skillfold)** — Declares skills in YAML and pins exact revisions in a lockfile so installs are reproducible across Claude Code and Codex.
  <sub>★ 12 · TypeScript · MIT · npm · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g skillfold # or: npx skillfold`</sub>

## Personal Assistants

- **[openclaw](https://github.com/openclaw/openclaw)** — Your own personal AI assistant, on any OS and any platform.
  <sub>★ 388.6k · TypeScript · npm · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g openclaw@latest --allow-scripts=openclaw`</sub>
- **[hermes-agent](https://github.com/NousResearch/hermes-agent)** — Self-improving harness with persistent cross-session memory and auto-generated skill documents.
  <sub>★ 240k · Python · MIT · script · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`</sub>
- **[nanobot](https://github.com/HKUDS/nanobot)** — Ultra-lightweight self-hosted assistant in Python with WebUI, tools, memory, MCP, and multi-agent workflows.
  <sub>★ 47.7k · Python · MIT · psh · pushed 2026-09-02 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/HKUDS/nanobot/main/scripts/install.ps1 | iex`</sub>
- **[QwenPaw](https://github.com/agentscope-ai/QwenPaw)** — Personal assistant that deploys to your own machine or the cloud and plugs into multiple chat apps. Formerly CoPaw.
  <sub>★ 34.8k · Python · Apache-2.0 · psh · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://qwenpaw.agentscope.io/install.ps1 | iex`</sub>
- **[zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)** — Fast, small, fully autonomous assistant infrastructure in Rust, deployable anywhere.
  <sub>★ 32.7k · Rust · Apache-2.0 · script · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/zeroclaw-labs/zeroclaw/master/install.sh | sh`</sub>
- **[nanoclaw](https://github.com/nanocoai/nanoclaw)** — Lightweight OpenClaw alternative running in containers, connecting to WhatsApp, Telegram, Slack, Discord, and Gmail.
  <sub>★ 30.7k · TypeScript · MIT · clone · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/nanocoai/nanoclaw.git`</sub>
- **[picoclaw](https://github.com/sipeed/picoclaw)** — Tiny and fast assistant deployable anywhere.
  <sub>★ 29.9k · Go · MIT · clone · pushed 2026-08-27 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/sipeed/picoclaw.git`</sub>
- **[leon](https://github.com/leon-ai/leon)** — Long-running open-source personal assistant with voice and text interfaces.
  <sub>★ 17.5k · TypeScript · MIT · clone · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leon-ai/leon.git`</sub>
- **[rowboat](https://github.com/rowboatlabs/rowboat)** — Open-source AI coworker with memory.
  <sub>★ 17.5k · TypeScript · Apache-2.0 · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rowboatlabs/rowboat.git`</sub>
- **[OpenWorker](https://github.com/andrewyng/openworker)** — Open-source desktop AI coworker that delivers finished work — security review with re-scanned fixes, cloud posture audits, triaged inboxes — from specialist coworkers, with every action governed and logged. BYO model key or fully local via Ollama.
  <sub>★ 17.2k · Python · MIT · clone · pushed 2026-08-31 · Win · WSL2 · macOS</sub>
  <sub>`git clone https://github.com/andrewyng/openworker`</sub>
- **[ironclaw](https://github.com/nearai/ironclaw)** — Agent OS in Rust focused on privacy, security, and extensibility.
  <sub>★ 12.6k · Rust · Apache-2.0 · psh · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm "https://github.com/nearai/ironclaw/releases/download/$IronClawReleaseTag/ironclaw-installer.ps1" | iex`</sub>
- **[Coworker](https://github.com/accomplish-ai/coworker)** — Open source AI coworker that lives on your desktop. Formerly accomplish.
  <sub>★ 10.9k · source · pushed 2026-08-13</sub>
  <sub>`git clone https://github.com/accomplish-ai/coworker.git`</sub>
- **[Cloudflare OS](https://github.com/cloudflare/cloudflare-os)** — Self-hostable "company OS" on Cloudflare Workers: a chat UI where agents preloaded with your company context do tasks, build sandboxed apps, and stay inside a Gatekeepers guardrail framework.
  <sub>★ 9.5k · TypeScript · Apache-2.0 · source · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/cloudflare/cloudflare-os.git`</sub>
- **[nullclaw](https://github.com/nullclaw/nullclaw)** — Fully autonomous assistant infrastructure written in Zig.
  <sub>★ 8.1k · Zig · MIT · brew · pushed 2026-07-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install nullclaw`</sub>
- **[lobsterai](https://github.com/netease-youdao/LobsterAI)** — Desktop-grade agent for data analysis, slides, docs, and web research.
  <sub>★ 6k · TypeScript · MIT · clone · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/netease-youdao/LobsterAI.git`</sub>
- **[MetaClaw](https://github.com/aiming-lab/MetaClaw)** — Assistant that learns and evolves from conversation alone.
  <sub>★ 3.5k · Python · MIT · source · pushed 2026-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aiming-lab/MetaClaw.git`</sub>
- **[zclaw](https://github.com/tnm/zclaw)** — Complete personal assistant in 888 KiB, running on an ESP32 with GPIO, cron, and custom tools.
  <sub>★ 2.2k · C · MIT · source · pushed 2026-05-17 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tnm/zclaw.git`</sub>
- **[OpenMausBot](https://github.com/milind-soni/OpenMausBot)** — Open-source Grok Bot-style team of bots in a chat-app sidebar, where every bot is a real local agent — Claude or Codex — with its own personality, model, cloud computer, and connected apps, behind approval gates. Local-first, bring-your-own-agent.
  <sub>★ 2k · TypeScript · Apache-2.0 · clone · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/milind-soni/OpenMausBot`</sub>
- **[Rakazo](https://github.com/elie222/rakazo)** — Self-hosted platform for persistent AI teammates with their own conversations, memory, and routines, running on shared team computers or isolated private ones, reachable from web, desktop, and mobile with voice mode. Bots delegate to peer bots or short-lived subagents. BYO model and sandbox.
  <sub>★ 1.8k · TypeScript · Apache-2.0 · clone · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/elie222/rakazo.git`</sub>
- **[denchclaw](https://github.com/DenchHQ/DenchClaw)** — Managed OpenClaw framework aimed at CRM, sales automation, and outreach.
  <sub>★ 1.6k · TypeScript · MIT · npx · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx denchclaw@latest bootstrap`</sub>
- **[row-bot](https://github.com/siddsachar/row-bot)** — Local-first desktop assistant that reasons through messy context, orchestrates tools and providers, and works inside your files, repos, and channels — durable memory, scheduled tasks, voice, visible browser automation, and parent-led child agents for research, review, and implementation. Runs on Ollama or opt-in cloud models. Formerly Thoth.
  <sub>★ 1.5k · Python · Apache-2.0 · script · pushed 2026-08-28 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/siddsachar/row-bot/main/installer/install-linux.sh | bash`</sub>
- **[Ouroboros](https://github.com/razzant/ouroboros)** — General-purpose agent with durable identity and memory, reviewed self-modification, multi-agent coordination, and desktop and headless interfaces.
  <sub>★ 1.3k · Python · MIT · uv · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install "git+https://github.com/razzant/ouroboros.git@ouroboros"`</sub>
- **[rho](https://github.com/mikeyobrien/rho)** — Stays running, remembers across sessions, and checks in on its own. macOS, Linux, Android.
  <sub>★ 372 · TypeScript · MIT · npm · pushed 2026-05-26 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g @rhobot-dev/rho`</sub>
- **[OpenInstinct](https://github.com/Merit-Systems/OpenInstinct)** — iMessage assistant that drives a real browser to do chores, book tickets, and handle groceries, keeping your passwords and cards in an encrypted vault it unlocks per action. Self-hosted on your own Vercel, any model.
  <sub>★ 258 · TypeScript · MIT · clone · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Merit-Systems/OpenInstinct.git`</sub>
- **[iva](https://github.com/smixs/iva-agent)** — Telegram assistant that turns your messages, voice notes and photos into an Obsidian-compatible markdown vault it remembers across sessions. Crons, skills, MCP and Google Workspace from an in-chat menu. Self-hosted in one command, MIT.
  <sub>★ 196 · TypeScript · MIT · script · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/smixs/iva-agent/main/install.sh | bash`</sub>
- **[Overlay](https://github.com/LayerNorm/overlay-web)** — Open-source workspace where humans and agents share context — knowledge, files, memory, connected apps — so you delegate repeatable work to agents, review what they produce, and take action through tools, provider-neutral.
  <sub>★ 132 · TypeScript · AGPL-3.0 · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LayerNorm/overlay-web.git`</sub>
- **[lemon](https://github.com/z80dev/lemon)** — Local-first assistant and coding agent runtime.
  <sub>★ 129 · Elixir · MIT · script · pushed 2026-09-02 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/z80dev/lemon/main/install.sh | sh`</sub>
- **[automata](https://github.com/sentientwave/automata)** — Matrix-native workspace where Temporal-backed durable workflows survive restarts and keep long tasks moving.
  <sub>★ 112 · Elixir · source · pushed 2026-05-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/sentientwave/automata.git`</sub>
- **[ghostclaw](https://github.com/b1rdmania/ghostclaw)** — An AI that lives on your computer and does things for you.
  <sub>★ 91 · TypeScript · MIT · script · pushed 2026-05-03 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://ghostclaw.io/install.sh | bash`</sub>
- **[assistant](https://github.com/kcosr/assistant)** — Panel-based assistant whose plugins share one workspace of notes, lists, and objects.
  <sub>★ 90 · TypeScript · clone · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kcosr/assistant`</sub>
- **[Hivekeep](https://github.com/MarlBurroW/hivekeep)** — Self-hosted team of specialized agents with persistent memory that delegate and build their own tools and mini-apps. Telegram, Slack, Discord, Matrix. Single container, MIT.
  <sub>★ 51 · TypeScript · MIT · script · pushed 2026-09-02 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/MarlBurroW/hivekeep/main/install.sh | bash`</sub>
- **[lucinate](https://github.com/lucinate-ai/lucinate)** — Terminal-native chat client for OpenClaw, Hermes, Ollama, and OpenAI-compatible providers, with cron management and session browsing.
  <sub>★ 11 · Go · Apache-2.0 · psh · pushed 2026-08-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/lucinate-ai/lucinate/main/install/lucinate.ps1 | iex`</sub>

## Resting

- **[vibe-kanban](https://github.com/BloopAI/vibe-kanban)** — Kanban board for managing AI coding agents.
  <sub>★ 28k · Rust · Apache-2.0 · npx · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibe-kanban`</sub>
- **[1code](https://github.com/21st-dev/1code)** — Orchestration layer for Claude Code and Codex.
  <sub>★ 5.6k · TypeScript · Apache-2.0 · source · pushed 2026-03-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/21st-dev/1code.git`</sub>
- **[CodexMonitor](https://github.com/Dimillian/CodexMonitor)** — Orchestrate multiple Codex agents across local workspaces.
  <sub>★ 4.3k · TypeScript · MIT · source · pushed 2026-03-26 · macOS</sub>
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
  <sub>★ 427 · TypeScript · MIT · npm · pushed 2026-04-12 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`npm i -g openclaw opengoat`</sub>
- **[subtask](https://github.com/zippoxer/subtask)** — Claude Skill that runs your tasks through subagents in git worktrees.
  <sub>★ 340 · Go · MIT · psh · pushed 2026-04-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://subtask.dev/install.ps1 | iex`</sub>
- **[lettabot](https://github.com/letta-ai/lettabot)** — Personal assistant that remembers everything.
  <sub>★ 327 · TypeScript · Apache-2.0 · clone · pushed 2026-05-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/letta-ai/lettabot.git`</sub>
- **[mercury](https://github.com/Michaelliv/mercury)** — Personal AI assistant that lives where you chat.
  <sub>★ 145 · TypeScript · npm · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mercury-ai`</sub>
- **[wreckit](https://github.com/mikehostetler/wreckit)** — Run the Ralph Wiggum loop over your roadmap.
  <sub>★ 130 · Elixir · MIT · npm · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g wreckit`</sub>
- **[babyagi3](https://github.com/yoheinakajima/babyagi3)** — A minimal AI agent you configure once, then run through natural language.
  <sub>★ 129 · Python · MIT · clone · pushed 2026-03-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yoheinakajima/babyagi3`</sub>
- **[gnap](https://github.com/farol-team/gnap)** — Git-native agent protocol coordinating agents through a shared repo as a task board, with no orchestrator process.
  <sub>★ 83 · MIT · source · pushed 2026-03-17</sub>
  <sub>`git clone https://github.com/farol-team/gnap.git`</sub>
- **[swarm-protocol](https://github.com/phuryn/swarm-protocol)** — Headless coordination over MCP: claim work, detect file conflicts, heartbeat, and hand off across sessions.
  <sub>★ 53 · TypeScript · MIT · clone · pushed 2026-03-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/phuryn/swarm-protocol.git`</sub>
- **[wit](https://github.com/amaar-mc/wit)** — Locks individual functions rather than files via Tree-sitter, warning agents of conflicts before they write.
  <sub>★ 46 · TypeScript · MIT · bun · pushed 2026-03-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bun install -g wit-protocol`</sub>
- **[ariana](https://github.com/ariana-dot-dev/ariana)** — The IDE of the future.
  <sub>unavailable</sub>


---

Snapshot 2026-09-03. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
