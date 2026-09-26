# MCP Servers (punkpeye)

A collection of MCP servers.

Curated by **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

4,295 entries · 4,269 distinct repos · 60 sections

[← back to the mega list](../README.md)

Page **2** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · **2** · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · [7](mcp-servers-punkpeye-7.md) — [continue on page 3 →](mcp-servers-punkpeye-3.md)

## Contents

- [Command Line](#command-line) (27)
- [OS Automation](#os-automation) (20)
- [Databases](#databases) (142)
- [Search &amp; Data Extraction](#search--data-extraction) (250)
- [Data Science Tools](#data-science-tools) (44)
- [Data Visualization](#data-visualization) (10)
- [Data Platforms](#data-platforms) (48)
- [end to end RAG platforms](#end-to-end-rag-platforms) (6)
- [Knowledge &amp; Memory](#knowledge--memory) (348)

## Command Line

<sub>Entries 20–27 of 27. The rest are on this page's other parts, linked above and below.</sub>

- **[HasanJahidul/localhost-mcp](https://github.com/HasanJahidul/localhost-mcp)** — Inspect, manage, and kill local dev servers. Lists what's listening on each port (pid, framework, project, uptime, memory, cpu), diagnoses port conflicts with free alternatives nearby, finds zombie processes, and kills by pid or port with a dry-run default
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g localhost-mcp`</sub>
- **[laszlopere/mcp-tmux](https://github.com/laszlopere/mcp-tmux)** — Universal tmux driver: sessions, windows, panes, keystrokes, and pane capture — local or remote over SSH. Curated tools plus a raw tmux_command passthrough; works against tmux 1.8+. Shared, visible sessions for pair-programming with the agent. uvx mcp-tmux
  <sub>★ 3 · Python · MIT · uv · pushed 2026-06-19 · WSL2 · macOS? · Linux</sub>
  <sub>`uvx mcp-tmux # run directly with uv (no install)`</sub>
- **[gerard-kanters/mcp-linux-tools](https://github.com/gerard-kanters/mcp-linux-tools)** — Administer a Linux server from an MCP client such as Cursor or VS Code: read files and tail logs, check/reload/restart systemd services, manage cron jobs inside a dedicated crontab section, run read-only MySQL queries, drive WP-CLI on WordPress sites, run safe Git commands, and execute sandboxed Python. Directories, services and WordPress sites are allowlisted in config.json, and every tool return
  <sub>★ 2 · Python · GPL-2.0 · source · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gerard-kanters/mcp-linux-tools.git`</sub>
- **[AICommander-dev/aicommander](https://github.com/AICommander-dev/aicommander)** — Outbound-only remote shell, detached long-running jobs, and temporary file courier for AI agents (https://aicommander.dev). Hosted Streamable HTTP; no exposed SSH/ports/VPN. Install via npx -y @aicommander/mcp
  <sub>★ 1 · Dockerfile · MIT · source · pushed 2026-09-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/AICommander-dev/aicommander.git`</sub>
- **[Easton-OU/rootpilot-mcp](https://github.com/Easton-OU/rootpilot-mcp)** — Safe, read-only SSH diagnostics for Linux/Docker servers: a fixed 38-command whitelist (no arbitrary execution), secret redaction, per-command timeouts. Collects evidence; your model does the reasoning. npx @rootpilot/mcp-ssh-diagnose
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Easton-OU/rootpilot-mcp.git`</sub>
- **[capsulerun/bash](https://github.com/capsulerun/bash/tree/main/packages/bash-mcp)** — Sandboxed bash for agents. Run untrusted commands in WebAssembly sandboxes with no setup required
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-05-16</sub>
  <sub>`git clone https://github.com/capsulerun/bash.git && cd bash/packages/bash-mcp`</sub>
- **[dbhq-uk/heliograph](https://github.com/heliograph-io/heliograph)** — Run commands on a machine you cannot SSH into. Publishes a step to a transport the far side already reaches (git, file share, S3-compatible storage, relay or a carried file); the whole run comes back as a log with every line timestamped in UTC, whether it passed or failed. For air-gapped, bastion-only and change-controlled estates: no tunnel, no proxy, nothing held open. The gates live on the far
  <sub>Shell · Apache-2.0 · npx · pushed 2026-09-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add heliograph-io/heliograph # any agent, via skills.sh`</sub>
- **[tarides/sudo-proxy](https://github.com/tarides/sudo-proxy)** — Run privileged, mutating commands — locally or over SSH — with a mandatory single-keypress human approval on every one. The model calls execute; a TUI Y/N prompt gates the command, then sudo escalates, and no password is ever stored. Sanitized env allowlist, no-shell argv execution, replay protection, and audit logging. cargo install sudo-proxy
  <sub>Rust · MIT · cargo · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`cargo install sudo-proxy`</sub>

## OS Automation

- **[Harusame64/desktop-touch-mcp](https://github.com/Harusame64/desktop-touch-mcp)** — Windows desktop automation for LLM agents with entity-based actions instead of coordinate-only clicking. Uses UIA, CDP, screenshots, keyboard/mouse/clipboard, and terminal control, plus entity leases, verified delivery, causal context, and interaction memory to reduce silent UI automation failures
  <sub>★ 22 · TypeScript · MIT · npx · pushed 2026-09-24 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx -y @harusame64/desktop-touch-mcp`</sub>
- **[JonathanRReed/Apple-MCPs](https://github.com/JonathanRReed/Apple-MCPs)** — Local macOS MCP servers for Mail, Calendar, Reminders, Messages, Contacts, Notes, Shortcuts, Files, Maps, and system tools. Use the unified server or standalone servers over stdio, with PyPI packages and MCPB bundles
  <sub>★ 17 · Python · MIT · uv · pushed 2026-09-25 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`uvx apple-tools-mcp`</sub>
- **[SunnyLich/OpenWand](https://github.com/SunnyLich/OpenWand)** — Local MCP stdio server that gives trusted AI clients read-only desktop context through OpenWand, including selection, clipboard, active-window, browser-page, and screen context
  <sub>★ 15 · Python · MIT · clone · pushed 2026-08-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/SunnyLich/OpenWand.git`</sub>
- **[faze79/WPFVisualTreeMcp](https://github.com/faze79/WPFVisualTreeMcp)** — #️⃣ 🏠 🪟 - Inspect, debug and drive running WPF (.NET desktop) apps: visual tree, dependency properties, data bindings and binding errors, DataContext, and screenshots with open popups/menus included, plus clicking, item selection, text input and keyboard shortcuts. Auto-injects into any running WPF process (x64/x86) with no source changes. dotnet tool install -g WpfVisualTreeMcp
  <sub>★ 15 · C# · MIT · clone · pushed 2026-07-23 · Win</sub>
  <sub>`git clone https://github.com/faze79/WpfVisualTreeMcp.git`</sub>
- **[fixed-width/glass](https://github.com/fixed-width/glass)** — Gives a coding agent a build → see → interact → debug loop over the native GUI app it is writing: launch the app, screenshot it, read its accessibility tree, inject mouse/keyboard/gestures, tail its logs, and diff frames to confirm a change landed. Drives apps as an external black box with no app integration, so any toolkit or language works. 30 tools with text-first responses (element ids, diffs,
  <sub>★ 15 · Rust · Apache-2.0 · source · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/fixed-width/glass.git`</sub>
- **[ostapondo/Plonk](https://github.com/ostapondo/Plonk)** — A Mac window manager an agent can drive, plus ten more menu bar utilities behind the same icon: see every monitor and window, arrange a layout across displays in one call, snap a window into zones you drew yourself, save workspaces that relaunch apps into their places, keep-awake, measure the screen, screenshot a window by name even when it is buried behind other windows, annotate it, and read tex
  <sub>★ 15 · Swift · MIT · brew · pushed 2026-09-22 · Win? · macOS</sub>
  <sub>`brew install --cask ostapondo/plonk/plonk`</sub>
- **[sbuysse/gnome-desktop-mcp](https://github.com/sbuysse/gnome-desktop-mcp)** — GNOME desktop automation for AI agents. 30 tools via D-Bus: screenshots, window management, mouse/keyboard injection, clipboard, workspaces, and system notifications. Works on any GNOME 45–49 Linux desktop
  <sub>★ 14 · JavaScript · GPL-3.0 · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install gnome-desktop-mcp`</sub>
- **[tinqiao-oss/clawtouch-mcp](https://github.com/tinqiao-oss/clawtouch-mcp)** — Physical USB HID keyboard/mouse control via a Raspberry Pi Pico 2 running open-source firmware. Exposes move, click, drag, type, key combos, and scroll as MCP tools for any MCP client. Genuine physical HID input on the standard driver path, with a --mock mode for hardware-free trials. pip install clawtouch-mcp
  <sub>★ 11 · Python · MIT · pip · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install clawtouch-mcp # minimal (serial only)`</sub>
- **[munimtechnologies/munim-computer-use](https://github.com/munimtechnologies/munim-computer-use)** — Accessibility-first Computer Use for any agent: element ids instead of guessed pixels, background input that never moves your mouse, an agent pointer overlay, zoom with correct coordinate mapping, and an own tab group in your signed-in Chrome. Same 30 tools on macOS, Windows and Linux; npm launcher munim-computer-use
  <sub>★ 10 · Rust · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/munimtechnologies/munim-computer-use.git`</sub>
- **[dimpagk92/cellar](https://github.com/dimpagk92/cellar)** — Hybrid computer-use runtime. Fuses accessibility tree + Chrome DevTools Protocol + vision into structured context with per-element confidence. 4 MCP tools (see/act/think/perceive). Continuous awareness engine (Cortex) with freshness + side-effect detection. Works offline with Ollama + local models
  <sub>★ 5 · Rust · Apache-2.0 · source · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/dimpagk92/cellar.git`</sub>
- **[suleyman416/mcp-applemusic](https://github.com/suleyman416/mcp-applemusic)** — FastMCP server for Apple Music on macOS with 74 tools, autonomous tokenless DJ daemon, DJ energy mixes, multi-room AirPlay, Spotify &amp; M3U playlist importers, listening journal, and Apple Replay analytics
  <sub>★ 2 · Python · MIT · npx · pushed 2026-09-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @smithery/cli install suleyman416/mcp-applemusic --client claude`</sub>
- **[yunfeng-enrich/usemymac](https://github.com/yunfeng-enrich/usemymac)** — Turn a Mac into a remote computer-use MCP server with one command. uvx usemymac up wraps CUA's computer-server (screenshot, mouse, keyboard, windows, apps, accessibility tree) in a per-run token, hides shell and file tools unless opted in, and opens a Cloudflare quick tunnel so Claude Code, Codex, or any MCP client on another machine can use the Mac. Rides an existing CuaDriver daemon when one is
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx usemymac up`</sub>
- **[juergenkoller-software/nemeton-mcp](https://github.com/juergenkoller-software/nemeton-mcp)** — MCP bridge for Nemeton — native macOS virtual machine manager built on Apples Virtualization.framework. Create/control Linux &amp; macOS VMs (no Parallels, no QEMU), CoW snapshots on APFS, 50+ MCP tools across VM lifecycle, console, files, networking, and host metrics
  <sub>★ 1 · Swift · MIT · clone · pushed 2026-06-08 · macOS · Linux</sub>
  <sub>`git clone https://github.com/juergenkoller-software/nemeton-mcp.git`</sub>
- **[juergenkoller-software/freezetext-mcp](https://github.com/juergenkoller-software/freezetext-mcp)** — MCP server for FreezeText — OCR anything on your Mac screen. Freeze the screen and extract text via Apple Vision (videos, popups, protected PDFs), OCR a region or base64 image, and manage a searchable capture history. 12 tools
  <sub>★ 1 · Swift · MIT · clone · pushed 2026-06-08 · macOS · Linux</sub>
  <sub>`git clone https://github.com/juergenkoller-software/freezetext-mcp.git`</sub>
- **[emazaheri/ios-agent](https://github.com/emazaheri/ios-agent)** — Drive a real iPhone or an iOS Simulator through XCUIAutomation and WebDriverAgent. Screens arrive as a compact digest rather than raw accessibility XML (37,000 tokens to 329 on a long list), element resolution runs server-side through six tiers so a retry costs no model tokens, every action returns the screen it produced, and destructive actions are classified before they run and ask first
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/emazaheri/ios-agent.git`</sub>
- **[chryaner/terrarium](https://github.com/chryaner/terrarium)** — Fork, break, and revert real VirtualBox VMs as MCP tools. Forks are linked clones (~0.1s) and revert restores a RAM snapshot in seconds. Drives GUI-only guests through the hypervisor with screenshot, click, scroll, type and keys, so an agent controls a machine with no SSH, guest agent, or network, including Windows XP. Windows host with VirtualBox required. npx -y terrarium-mcp mcp
  <sub>★ 1 · Go · Apache-2.0 · scoop · pushed 2026-09-08 · Win · WSL2 · macOS · Linux</sub>
  <sub>`scoop bucket add terrarium https://github.com/chryaner/terrarium scoop install terrarium`</sub>
- **[Dominic-DK/askew-mcp](https://github.com/Dominic-DK/askew-mcp)** — Let an agent use a real iPhone, iPad or Mac through Apple Shortcuts: run a Shortcut on a locked phone and get the result back, send lock-screen notifications, and read what the phone sends (Calendar, Reminders, Notes, HomeKit, Wallet events). End-to-end encrypted relay, one automation on the phone. npx -y askew-mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-26 · macOS</sub>
  <sub>`npx -y askew-mcp fingerprint # print this computer's six fingerprint words`</sub>
- **[glasswarp/mcp-server](https://github.com/glasswarp/mcp-server)** — See and control a real Windows PC you own from any MCP client, locally or remotely. Hosted MCP (https://mcp.glasswarp.com/mcp) or npx @glasswarp/mcp. Observe (UIA + screenshots), click/type/drag/scroll, launch apps, owner Live View. BYOH — your machine, your key; you bring the model
  <sub>TypeScript · Apache-2.0 · source · pushed 2026-08-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/glasswarp/mcp-server.git`</sub>
- **[dockndevai/mcp-mac-control](https://github.com/dockndevai/mcp-mac-control)** — Full control of a Mac — drive it like a human: shell, AppleScript, files, processes, and human-like GUI (move, click, double/right-click, drag, scroll, type, key combos) with a screenshot perception loop. Full control by default; MACCTL_SAFE_MODE=true inverts to safe-by-default (read-only, gated, confirmations). The powerful sibling of mcp-macos. npx -y @dockndevai/mcp-mac-control
  <sub>TypeScript · MIT · npx · pushed 2026-09-23 · macOS</sub>
  <sub>`npx -y @dockndevai/mcp-mac-control`</sub>
- **[dockndevai/mcp-macos](https://github.com/dockndevai/mcp-macos)** — Safe-by-default control of a Mac: read files, list processes &amp; apps, take screenshots, read the clipboard; and behind explicit opt-ins, run shell commands (allowlisted), AppleScript, move files to Trash, and inject GUI input. Read-only by default with layered access modes, per-path/command allowlists, and human confirmation (MCP elicitation) on the dangerous calls. npx -y @dockndevai/mcp-macos
  <sub>TypeScript · MIT · npx · pushed 2026-09-24 · macOS</sub>
  <sub>`npx -y @dockndevai/mcp-macos`</sub>

## Databases

- **[googleapis/genai-toolbox](https://github.com/googleapis/mcp-toolbox)** — Open source MCP server specializing in easy, fast, and secure tools for Databases
  <sub>★ 16.5k · Go · Apache-2.0 · npx · pushed 2026-09-26 · macOS</sub>
  <sub>`npx @toolbox-sdk/server --config tools.yaml`</sub>
- **[bram2w/baserow](https://github.com/baserow/baserow)** — Baserow database integration with table search, list, and row create, read, update, and delete capabilities
  <sub>★ 6k · Python · docker · pushed 2026-09-25 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -v baserow_data:/baserow/data -p 80:80 -p 443:443 baserow/baserow:2.3.4`</sub>
- **[crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp)** — All-in-one MCP server for Postgres development and operations, with tools for performance analysis, tuning, and health checks
  <sub>★ 3.3k · Python · MIT · pipx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install postgres-mcp`</sub>
- **[supabase-community/supabase-mcp](https://github.com/supabase/mcp)** — Official Supabase MCP server to connect AI assistants directly with your Supabase project and allows them to perform tasks like managing tables, fetching config, and querying data
  <sub>★ 2.9k · TypeScript · Apache-2.0 · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/supabase-community/supabase-mcp.git`</sub>
- **[benborla29/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql)** — MySQL database integration in NodeJS with configurable access controls and schema inspection
  <sub>★ 2.1k · JavaScript · MIT · clone · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/benborla/mcp-server-mysql.git`</sub>
- **[qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant)** — A Qdrant MCP server
  <sub>★ 1.5k · Python · Apache-2.0 · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @smithery/cli install mcp-server-qdrant --client claude`</sub>
- **[designcomputer/mysql_mcp_server](https://github.com/designcomputer/mysql_mcp_server)** — MySQL database integration with configurable access controls, schema inspection, and comprehensive security guidelines
  <sub>★ 1.4k · Python · MIT · npx · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install designcomputer/mysql-mcp-server --client claude`</sub>
- **[ArcadeData/arcadedb](https://github.com/ArcadeData/arcadedb)** — Built-in MCP server for ArcadeDB, a multi-model database (graph, document, key-value, time-series, vector) with SQL, Cypher, Gremlin, and MongoDB QL support
  <sub>★ 1.2k · Java · Apache-2.0 · source · pushed 2026-09-26 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ArcadeData/arcadedb.git`</sub>
- **[xing5/mcp-google-sheets](https://github.com/xing5/mcp-google-sheets)** — A Model Context Protocol server for interacting with Google Sheets. This server provides tools to create, read, update, and manage spreadsheets through the Google Sheets API
  <sub>★ 1k · Python · MIT · uv · pushed 2026-05-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-google-sheets@latest`</sub>
- **[neo4j-contrib/mcp-neo4j](https://github.com/neo4j-contrib/mcp-neo4j)** — Model Context Protocol with Neo4j (Run queries, Knowledge Graph Memory, Manaage Neo4j Aura Instances)
  <sub>★ 986 · Python · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/neo4j-contrib/mcp-neo4j.git`</sub>
- **[ClickHouse/mcp-clickhouse](https://github.com/ClickHouse/mcp-clickhouse)** — ClickHouse database integration with schema inspection and query capabilities
  <sub>★ 880 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install 'mcp-clickhouse[chdb]'`</sub>
- **[alexanderzuev/supabase-mcp-server](https://github.com/alexander-zuev/supabase-mcp-server)** — Supabase MCP Server with support for SQL query execution and database exploration tools
  <sub>★ 831 · Python · Apache-2.0 · pipx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install supabase-mcp-server`</sub>
- **[Canner/wren-engine](https://github.com/Canner/wren-engine)** — The Semantic Engine for Model Context Protocol(MCP) Clients and AI Agents
  <sub>★ 665 · Java · Apache-2.0 · source · pushed 2026-05-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Canner/wren-engine.git`</sub>
- **[neondatabase/mcp-server-neon](https://github.com/neondatabase/mcp-server-neon)** — An MCP Server for creating and managing Postgres databases using Neon Serverless Postgres
  <sub>★ 650 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/neondatabase/mcp-server-neon.git`</sub>
- **[redis/mcp-redis](https://github.com/redis/mcp-redis)** — The Redis official MCP Server offers an interface to manage and search data in Redis
  <sub>★ 626 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from git+https://github.com/redis/mcp-redis.git@0.2.0 redis-mcp-server --url redis://localhost:6379/0`</sub>
- **[chroma-core/chroma-mcp](https://github.com/chroma-core/chroma-mcp)** — Chroma MCP server to access local and cloud Chroma instances for retrieval capabilities
  <sub>★ 599 · Python · Apache-2.0 · source · pushed 2025-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chroma-core/chroma-mcp.git`</sub>
- **[centralmind/gateway](https://github.com/centralmind/gateway)** — MCP and MCP SSE Server that automatically generate API based on database schema and data. Supports PostgreSQL, Clickhouse, MySQL, Snowflake, BigQuery, Supabase
  <sub>★ 548 · Go · Apache-2.0 · clone · pushed 2025-07-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/centralmind/gateway.git`</sub>
- **[subnetmarco/pgmcp](https://github.com/subnetmarco/pgmcp)** — Natural language PostgreSQL queries with automatic streaming, read-only safety, and universal database compatibility
  <sub>★ 541 · Go · brew · pushed 2026-05-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install pgmcp`</sub>
- **[pab1it0/prometheus-mcp-server](https://github.com/pab1it0/prometheus-mcp-server)** — Query and analyze Prometheus, open-source monitoring system
  <sub>★ 517 · Python · MIT · helm · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`helm install prometheus-mcp-server \`</sub>
- **[domdomegg/airtable-mcp-server](https://github.com/domdomegg/airtable-mcp-server)** — Airtable database integration with schema inspection, read and write capabilities
  <sub>★ 458 · TypeScript · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/domdomegg/airtable-mcp-server.git`</sub>
- **[FreePeak/db-mcp-server](https://github.com/FreePeak/db-mcp-server)** — A high-performance multi-database MCP server built with Golang, supporting MySQL &amp; PostgreSQL (NoSQL coming soon). Includes built-in tools for query execution, transaction management, schema exploration, query building, and performance analysis, with seamless Cursor integration for enhanced database workflows
  <sub>★ 431 · Go · MIT · clone · pushed 2026-09-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/FreePeak/db-mcp-server.git`</sub>
- **[runekaagaard/mcp-alchemy](https://github.com/runekaagaard/mcp-alchemy)** — Universal SQLAlchemy-based database integration supporting PostgreSQL, MySQL, MariaDB, SQLite, Oracle, MS SQL Server and many more databases. Features schema and relationship inspection, and large dataset analysis capabilities
  <sub>★ 420 · Python · MPL-2.0 · clone · pushed 2026-09-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone git@github.com:runekaagaard/mcp-alchemy.git`</sub>
- **[cr7258/elasticsearch-mcp-server](https://github.com/cr7258/elasticsearch-mcp-server)** — MCP Server implementation that provides Elasticsearch interaction
  <sub>★ 308 · Python · Apache-2.0 · uv · pushed 2026-08-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx elasticsearch-mcp-server --transport sse`</sub>
- **[Snowflake-Labs/mcp](https://github.com/Snowflake-Labs/mcp)** — Open-source MCP server for Snowflake from official Snowflake-Labs supports prompting Cortex Agents, querying structured &amp; unstructured data, object management, SQL execution, semantic view querying, and more. RBAC, fine-grained CRUD controls, and all authentication methods supported
  <sub>★ 299 · Python · Apache-2.0 · npx · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx snowflake-labs-mcp --service-config-file <path_to_file>/tools_config.yaml --connection-name "default"`</sub>
- **[kiliczsh/mcp-mongo-server](https://github.com/kiliczsh/mcp-mongo-server)** — A Model Context Protocol Server for MongoDB
  <sub>★ 283 · TypeScript · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-mongo-server mongodb://localhost:27017/mydatabase`</sub>
- **[wenb1n-dev/mysql_mcp_server_pro](https://github.com/wenb1n-dev/mysql_mcp_server_pro)** — Supports SSE, STDIO; not only limited to MySQL's CRUD functionality; also includes database exception analysis capabilities; controls database permissions based on roles; and makes it easy for developers to extend tools with customization
  <sub>★ 248 · Python · MIT · pip · pushed 2025-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mysql_mcp_server_pro`</sub>
- **[gannonh/firebase-mcp](https://github.com/gannonh/firebase-mcp)** — Firebase services including Auth, Firestore and Storage
  <sub>★ 246 · TypeScript · MIT · npm · pushed 2025-10-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g firebase-tools`</sub>
- **[zilliztech/mcp-server-milvus](https://github.com/zilliztech/mcp-server-milvus)** — MCP Server for Milvus / Zilliz, making it possible to interact with your database
  <sub>★ 245 · Python · Apache-2.0 · clone · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zilliztech/mcp-server-milvus.git`</sub>
- **[XGenerationLab/xiyan_mcp_server](https://github.com/XGenerationLab/xiyan_mcp_server)** — An MCP server that supports fetching data from a database using natural language queries, powered by XiyanSQL as the text-to-SQL LLM
  <sub>★ 239 · Python · Apache-2.0 · pip · pushed 2026-02-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install xiyan-mcp-server`</sub>
- **[furey/mongodb-lens](https://github.com/furey/mongodb-lens)** — MongoDB Lens: Full Featured MCP Server for MongoDB Databases
  <sub>★ 208 · JavaScript · MIT · npx · pushed 2025-04-23 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y mongodb-lens`</sub>
- **[isaacwasserman/mcp-snowflake-server](https://github.com/isaacwasserman/mcp-snowflake-server)** — Snowflake integration implementing read and (optional) write operations as well as insight tracking
  <sub>★ 186 · Python · GPL-3.0 · npx · pushed 2025-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp_snowflake_server --client claude`</sub>
- **[ktanaka101/mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb)** — DuckDB database integration with schema inspection and query capabilities
  <sub>★ 179 · Python · MIT · npx · pushed 2025-05-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-server-duckdb --client claude`</sub>
- **[QuantGeekDev/mongo-mcp](https://github.com/QuantGeekDev/mongo-mcp)** — MongoDB integration that enables LLMs to interact directly with databases
  <sub>★ 175 · TypeScript · MIT · npx · pushed 2025-03-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install mongo-mcp --client claude`</sub>
- **[confluentinc/mcp-confluent](https://github.com/confluentinc/mcp-confluent)** — Confluent integration to interact with Confluent Kafka and Confluent Cloud REST APIs
  <sub>★ 169 · TypeScript · MIT · npx · pushed 2026-09-23 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @confluentinc/mcp-confluent --init-config`</sub>
- **[f4ww4z/mcp-mysql-server](https://github.com/f4ww4z/mcp-mysql-server)** — Node.js-based MySQL database integration that provides secure MySQL database operations
  <sub>★ 168 · JavaScript · MIT · npx · pushed 2025-11-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @f4ww4z/mcp-mysql-server --client claude`</sub>
- **[weaviate/mcp-server-weaviate](https://github.com/weaviate/mcp-server-weaviate)** — An MCP Server to connect to your Weaviate collections as a knowledge base as well as using Weaviate as a chat memory store
  <sub>★ 163 · source · pushed 2026-05-26</sub>
  <sub>`git clone https://github.com/weaviate/mcp-server-weaviate.git`</sub>
- **[aliyun/alibabacloud-tablestore-mcp-server](https://github.com/aliyun/alibabacloud-tablestore-mcp-server)** — MCP service for Tablestore, features include adding documents, semantic search for documents based on vectors and scalars, RAG-friendly, and serverless
  <sub>★ 157 · Java · Apache-2.0 · source · pushed 2026-03-19</sub>
  <sub>`git clone https://github.com/aliyun/alibabacloud-tablestore-mcp-server.git`</sub>
- **[sirmews/mcp-pinecone](https://github.com/sirmews/mcp-pinecone)** — Pinecone integration with vector search capabilities
  <sub>★ 149 · Python · MIT · npx · pushed 2025-01-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-pinecone --client claude`</sub>
- **[ergut/mcp-bigquery-server](https://github.com/ergut/mcp-bigquery-server)** — Server implementation for Google BigQuery integration that enables direct BigQuery database access and querying capabilities
  <sub>★ 148 · TypeScript · MIT · clone · pushed 2026-05-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ergut/mcp-bigquery-server`</sub>
- **[LucasHild/mcp-server-bigquery](https://github.com/LucasHild/mcp-server-bigquery)** — BigQuery database integration with schema inspection and query capabilities
  <sub>★ 130 · Python · MIT · npx · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-server-bigquery --client claude`</sub>
- **[jparkerweb/mcp-sqlite](https://github.com/jparkerweb/mcp-sqlite)** — Model Context Protocol (MCP) server that provides comprehensive SQLite database interaction capabilities
  <sub>★ 128 · JavaScript · MIT · source · pushed 2026-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jparkerweb/mcp-sqlite.git`</sub>
- **[tuannvm/mcp-trino](https://github.com/tuannvm/mcp-trino)** — A Go implementation of a Model Context Protocol (MCP) server for Trino
  <sub>★ 121 · Go · MIT · brew · pushed 2026-07-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install tuannvm/mcp/mcp-trino`</sub>
- **[hannesrudolph/sqlite-explorer-fastmcp-mcp-server](https://github.com/hannesrudolph/sqlite-explorer-fastmcp-mcp-server)** — An MCP server that provides safe, read-only access to SQLite databases through Model Context Protocol (MCP). This server is built with the FastMCP framework, which enables LLMs to explore and query SQLite databases with built-in safety features and query validation
  <sub>★ 108 · Python · clone · pushed 2025-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hannesrudolph/sqlite-explorer-fastmcp-mcp-server.git`</sub>
- **[ChristianHinge/dicom-mcp](https://github.com/ChristianHinge/dicom-mcp)** — DICOM integration to query, read, and move medical images and reports from PACS and other DICOM compliant systems
  <sub>★ 101 · Python · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run dicom-mcp /path/to/your_config.yaml --transport stdio`</sub>
- **[freema/mcp-gsheets](https://github.com/freema/mcp-gsheets)** — MCP server for Google Sheets API integration with comprehensive reading, writing, formatting, and sheet management capabilities
  <sub>★ 100 · TypeScript · MIT · clone · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/freema/mcp-gsheets.git`</sub>
- **[VictoriaMetrics-Community/mcp-victorialogs](https://github.com/VictoriaMetrics/mcp-victorialogs)** — Provides comprehensive integration with your VictoriaLogs instance APIs and documentation for working with logs, investigating and debugging tasks related to your VictoriaLogs instances
  <sub>★ 98 · Go · Apache-2.0 · go · pushed 2026-07-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/VictoriaMetrics/mcp-victorialogs/cmd/mcp-victorialogs@latest`</sub>
- **[TheRaLabs/legion-mcp](https://github.com/TheRaLabs/legion-mcp)** — Universal database MCP server supporting multiple database types including PostgreSQL, Redshift, CockroachDB, MySQL, RDS MySQL, Microsoft SQL Server, BigQuery, Oracle DB, and SQLite
  <sub>★ 94 · Python · GPL-3.0 · source · pushed 2025-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TheRaLabs/legion-mcp.git`</sub>
- **[rashidazarang/airtable-mcp](https://github.com/rashidazarang/airtable-mcp)** — Connect AI tools directly to Airtable. Query, create, update, and delete records using natural language. Features include base management, table operations, schema manipulation, record filtering, and data migration through a standardized MCP interface
  <sub>★ 88 · TypeScript · MIT · script · pushed 2026-09-10 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/rashidazarang/airtable-mcp/main/setup.sh | bash`</sub>
- **[wenb1n-dev/SmartDB_MCP](https://github.com/wenb1n-dev/SmartDB_MCP)** — A universal database MCP server supporting simultaneous connections to multiple databases. It provides tools for database operations, health analysis, SQL optimization, and more. Compatible with mainstream databases including MySQL, PostgreSQL, SQL Server, MariaDB, Dameng, and Oracle. Supports Streamable HTTP, SSE, and STDIO; integrates OAuth 2.0; and is designed for easy customization and extensi
  <sub>★ 80 · Python · MIT · pip · pushed 2025-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install SmartDB-MCP`</sub>
- **[edwinbernadus/nocodb-mcp-server](https://github.com/edwinbernadus/nocodb-mcp-server)** — Nocodb database integration, read and write capabilities
  <sub>★ 76 · JavaScript · npx · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y nocodb-mcp-server {NOCODB_URL} {NOCODB_BASE_ID} {NOCODB_API_TOKEN}`</sub>
- **[FROWNINGdev/django-orm-lens](https://github.com/FROWNINGdev/django-orm-lens)** — Django ORM static-analysis MCP server. Nine read-only tools (list_apps, list_models, describe_model, find_relations, cascade_preview, er_diagram, describe_migration_dependency, suggest_indexes, signal_graph) that expose Django schema, relationships (FK/M2M/O2O, on_delete, related_name), migration deps, missing indexes, and signal graphs — no DB, no Django boot, no credentials. Companion to a VS Co
  <sub>★ 74 · Python · MIT · uv · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx django-orm-lens scan # or: pipx run django-orm-lens scan`</sub>
- **[appwrite/mcp](https://github.com/appwrite/mcp)** — Official Appwrite MCP server. Connect via hosted OAuth at https://mcp.appwrite.io/ (no API keys) or self-host with a project API key to manage databases, auth, users, functions, storage, messaging, and more
  <sub>★ 73 · Python · MIT · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/appwrite/mcp.git`</sub>
- **[Zhwt/go-mcp-mysql](https://github.com/Zhwt/go-mcp-mysql)** — Easy to use, zero dependency MySQL MCP server built with Golang with configurable readonly mode and schema inspection
  <sub>★ 65 · Go · MIT · go · pushed 2026-01-21 · Win · WSL2? · macOS? · Linux</sub>
  <sub>`go install -v github.com/Zhwt/go-mcp-mysql@latest`</sub>
- **[pab1it0/adx-mcp-server](https://github.com/pab1it0/adx-mcp-server)** — Query and analyze Azure Data Explorer databases
  <sub>★ 59 · Python · MIT · source · pushed 2026-03-25 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/pab1it0/adx-mcp-server.git`</sub>
- **[yimindev/dati](https://github.com/yimindev/dati)** — Semantic gateway that turns mainstream databases into MCP services with business metadata enhancement and parameterized SQL tools
  <sub>★ 54 · Java · Apache-2.0 · clone · pushed 2026-09-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/yimindev/dati.git`</sub>
- **[joshuarileydev/supabase-mcp-server](https://github.com/JoshuaRileyDev/supabase-mcp-server)** — Supabase MCP Server for managing and creating projects and organisations in Supabase
  <sub>★ 52 · JavaScript · source · pushed 2024-12-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/joshuarileydev/supabase.git`</sub>
- **[prisma/mcp](https://github.com/prisma/mcp)** — Gives LLMs the ability to manage Prisma Postgres databases (e.g. spin up new databases and run migrations or queries)
  <sub>★ 49 · JavaScript · npx · pushed 2025-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-remote https://mcp.prisma.io/mcp`</sub>
- **[idoru/influxdb-mcp-server](https://github.com/idoru/influxdb-mcp-server)** — Run queries against InfluxDB OSS API v2
  <sub>★ 46 · JavaScript · MIT · npm · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g influxdb-mcp-server`</sub>
- **[agenticfabriq/mnemiq](https://github.com/agenticfabriq/mnemiq)** — Natural-language questions over Postgres, Oracle, Snowflake, Databricks, DuckDB and SQLite. The model only proposes SQL — shape, access, dialect and query plan are checked deterministically before any rows are read, and it refuses rather than guessing. uv run mnemiq serve
  <sub>★ 44 · Python · Apache-2.0 · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agenticfabriq/mnemiq.git`</sub>
- **[InfluxData/influxdb3_mcp_server](https://github.com/influxdata/influxdb3_mcp_server)** — Official MCP server for InfluxDB 3 Core/Enterprise/Cloud Dedicated
  <sub>★ 38 · TypeScript · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/influxdata/influxdb3_mcp_server.git`</sub>
- **[Couchbase-Ecosystem/mcp-server-couchbase](https://github.com/couchbase/mcp-server-couchbase)** — Couchbase MCP server provides unfied access to both Capella cloud and self-managed clusters for document operations, SQL++ queries and natural language data analysis
  <sub>★ 36 · Python · Apache-2.0 · uv · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx couchbase-mcp-server --disabled-tools upsert_document_by_id, delete_document_by_id`</sub>
- **[s2-streamstore/s2-sdk-typescript](https://github.com/s2-streamstore/s2-sdk-typescript)** — Official MCP server for the S2.dev serverless stream platform
  <sub>★ 35 · TypeScript · MIT · source · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/s2-streamstore/s2-sdk-typescript.git`</sub>
- **[fireproof-storage/mcp-database-server](https://github.com/fireproof-storage/mcp-database-server)** — Fireproof ledger database with multi-user sync
  <sub>★ 31 · JavaScript · source · pushed 2024-12-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fireproof-storage/mcp-database-server.git`</sub>
- **[GreptimeTeam/greptimedb-mcp-server](https://github.com/GreptimeTeam/greptimedb-mcp-server)** — MCP Server for querying GreptimeDB
  <sub>★ 29 · Python · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory . run -m greptimedb_mcp_server.server`</sub>
- **[pgtuner_mcp](https://github.com/isdaniel/pgtuner_mcp)** — provides AI-powered PostgreSQL performance tuning capabilities
  <sub>★ 29 · Python · Apache-2.0 · pip · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install pgtuner_mcp`</sub>
- **[schemacrawler/SchemaCrawler-MCP-Server-Usage](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage)** — Connect to any relational database, and be able to get valid SQL, and ask questions like what does a certain column prefix mean
  <sub>★ 29 · EPL-2.0 · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/schemacrawler/SchemaCrawler-MCP-Server-Usage.git`</sub>
- **[ydb/ydb-mcp](https://github.com/ydb-platform/ydb-mcp)** — MCP server for interacting with YDB databases
  <sub>★ 29 · Python · Apache-2.0 · pipx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install ydb-mcp`</sub>
- **[Aiven-Open/mcp-aiven](https://github.com/Aiven-Open/mcp-aiven)** — Navigate your Aiven projects and interact with the PostgreSQL®, Apache Kafka®, ClickHouse® and OpenSearch® services
  <sub>★ 28 · TypeScript · Apache-2.0 · source · pushed 2026-09-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Aiven-Open/mcp-aiven.git`</sub>
- **[c4pt0r/mcp-server-tidb](https://github.com/c4pt0r/mcp-server-tidb)** — TiDB database integration with schema inspection and query capabilities
  <sub>★ 24 · Python · Apache-2.0 · clone · pushed 2025-04-15 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/c4pt0r/mcp-server-tidb`</sub>
- **[openlink/mcp-server-sqlalchemy](https://github.com/OpenLinkSoftware/mcp-sqlalchemy-server)** — An MCP server for generic Database Management System (DBMS) Connectivity via SQLAlchemy using Python ODBC (pyodbc)
  <sub>★ 24 · Python · MIT · npx · pushed 2025-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-sqlalchemy-server run mcp-sqlalchemy-server`</sub>
- **[slotix/dbconvert-streams-public](https://github.com/slotix/dbconvert-streams-public)** — Read-only SQL across PostgreSQL, MySQL, S3-compatible buckets and folders of Parquet/CSV/JSON — and one query can join across all of them, federated in-process by DuckDB. No tool writes: they are absent rather than disabled, and every tool declares readOnlyHint. Runs from connection strings alone as docker run -i --rm slotix/stream-mcp postgres://… or as a one-click Claude extension
  <sub>★ 24 · Dockerfile · MIT · script · pushed 2026-09-05 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://dbconvert.nyc3.digitaloceanspaces.com/downloads/streams/latest/docker-install.sh | sh`</sub>
- **[antonorlov/mcp-postgres-server](https://github.com/antonorlov/mcp-postgres-server)** — PostgreSQL over MCP, including databases behind an SSH bastion
  <sub>★ 23 · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-postgres-server`</sub>
- **[xexr/mcp-libsql](https://github.com/Xexr/mcp-libsql)** — Production-ready MCP server for libSQL databases with comprehensive security and management tools
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pnpm install -g @xexr/mcp-libsql`</sub>
- **[Dataring-engineering/mcp-server-trino](https://github.com/Dataring-engineering/mcp-server-trino)** — Trino MCP Server to query and access data from Trino Clusters
  <sub>★ 18 · Python · MIT · source · pushed 2025-04-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Dataring-engineering/mcp-server-trino.git`</sub>
- **[iunera/druid-mcp-server](https://github.com/iunera/druid-mcp-server)** — Comprehensive MCP server for Apache Druid that provides extensive tools, resources, and prompts for managing and analyzing Druid clusters
  <sub>★ 18 · Java · Apache-2.0 · source · pushed 2026-08-31 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/iunera/druid-mcp-server.git`</sub>
- **[niledatabase/nile-mcp-server](https://github.com/niledatabase/nile-mcp-server)** — MCP server for Nile's Postgres platform - Manage and query Postgres databases, tenants, users, auth using LLMs
  <sub>★ 17 · TypeScript · MIT · clone · pushed 2025-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/nile-mcp-server.git`</sub>
- **[openlink/mcp-server-jdbc](https://github.com/OpenLinkSoftware/mcp-jdbc-server)** — An MCP server for generic Database Management System (DBMS) Connectivity via the Java Database Connectivity (JDBC) protocol
  <sub>★ 16 · Java · MIT · npx · pushed 2025-07-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector java -jar /path/to/mcp-jdbc-server/MCPServer-1.0.0-runner.jar`</sub>
- **[davewind/mysql-mcp-server](https://github.com/dave-wind/mysql-mcp-server)** — A – user-friendly read-only mysql mcp server for cursor and n8n
  <sub>★ 15 · JavaScript · MIT · source · pushed 2026-05-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dave-wind/mysql-mcp-server.git`</sub>
- **[codeurali/mcp-dataverse](https://github.com/codeurali/mcp-dataverse)** — Microsoft Dataverse MCP server with 63 tools for entity CRUD, FetchXML/OData queries, metadata inspection, workflow execution, audit logs, and Power Platform integration. Zero-config device code authentication
  <sub>★ 14 · JavaScript · MIT · npx · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-dataverse install`</sub>
- **[henilcalagiya/google-sheets-mcp](https://github.com/henilcalagiya/google-sheets-mcp)** — Your AI Assistant's Gateway to Google Sheets! 25 powerful tools for seamless Google Sheets automation via MCP
  <sub>★ 13 · Python · source · pushed 2025-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/henilcalagiya/google-sheets-mcp.git`</sub>
- **[wklee610/kafka-mcp](https://github.com/wklee610/kafka-mcp)** — MCP server for Apache Kafka that allows LLM agents to inspect topics, consumer groups, and safely manage offsets (reset, rewind)
  <sub>★ 13 · Python · Apache-2.0 · docker · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 kafka-mcp`</sub>
- **[amineelkouhen/mcp-cockroachdb](https://github.com/amineelkouhen/mcp-cockroachdb)** — A Model Context Protocol server for managing, monitoring, and querying data in CockroachDB
  <sub>★ 12 · Python · MIT · uv · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from git+https://github.com/amineelkouhen/mcp-cockroachdb.git@0.1.0 cockroachdb-mcp-server --url postgresql://localhost:26257/defaultdb`</sub>
- **[datacharter/datacharter](https://github.com/datacharter/datacharter)** — Local, contract-governed federation across files and databases (Postgres, Snowflake, BigQuery, DuckDB, Excel, and more) with read-only guards, PII masking, and per-column agent access
  <sub>★ 12 · Python · Apache-2.0 · uv · pushed 2026-09-16 · macOS</sub>
  <sub>`uvx datacharter serve # demo workspace, http://127.0.0.1:8321`</sub>
- **[devopam/MCPg](https://github.com/devopam/MCPg)** — Production-grade PostgreSQL MCP server with 100+ tools for catalog introspection, AST-validated safe query execution, index tuning, natural-language SQL, pgvector/TimescaleDB/AGE integrations, and HTTP/stdio transports
  <sub>★ 12 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install mcpg`</sub>
- **[jovezhong/mcp-timeplus](https://github.com/timeplus-io/mcp-timeplus)** — MCP server for Apache Kafka and Timeplus. Able to list Kafka topics, poll Kafka messages, save Kafka data locally and query streaming data with SQL via Timeplus
  <sub>★ 12 · Python · Apache-2.0 · script · pushed 2025-07-24 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl https://install.timeplus.com/oss | sh`</sub>
- **[openlink/mcp-server-odbc](https://github.com/OpenLinkSoftware/mcp-odbc-server)** — An MCP server for generic Database Management System (DBMS) Connectivity via the Open Database Connectivity (ODBC) protocol
  <sub>★ 12 · TypeScript · MIT · clone · pushed 2025-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenLinkSoftware/mcp-odbc-server.git`</sub>
- **[corebasehq/coremcp](https://github.com/CoreBaseHQ/coremcp)** — A secure, tunnel-native database bridge for AI agents. Connects localhost &amp; on-premise databases (MSSQL, etc.) to LLMs with AST-based query safety and PII masking
  <sub>★ 11 · Go · Apache-2.0 · script · pushed 2026-07-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://get.corebasehq.com | sh`</sub>
- **[hydrolix/mcp-hydrolix](https://github.com/hydrolix/mcp-hydrolix)** — Hydrolix time-series datalake integration providing schema exploration and query capabilities to LLM-based workflows
  <sub>★ 11 · Python · Apache-2.0 · pip · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-hydrolix`</sub>
- **[SidneyBissoli/ibge-br-mcp](https://github.com/SidneyBissoli/ibge-br-mcp)** — Brazilian Census Bureau (IBGE) data server with 23 tools for demographics, geography, economics, and statistics. Covers localities, SIDRA tables, Census data, population projections, and geographic meshes
  <sub>★ 11 · TypeScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ibge-br-mcp`</sub>
- **[ferrants/memvid-mcp-server](https://github.com/ferrants/memvid-mcp-server)** — Python Streamable HTTP Server you can run locally to interact with memvid storage and semantic search
  <sub>★ 10 · Python · source · pushed 2025-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ferrants/memvid-mcp-server.git`</sub>
- **[JaviMaligno/postgres_mcp](https://github.com/JaviMaligno/postgres_mcp)** — PostgreSQL MCP server with 14 tools for querying, schema exploration, and table analysis. Features security-first design with SQL injection prevention and read-only by default
  <sub>★ 10 · Python · MIT · npm · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @javiagui/postgresql-mcp`</sub>
- **[Arun-kc/schemabrain](https://github.com/Arun-kc/schemabrain)** — Read-only trust layer for Postgres: the agent never writes SQL — twelve tools compile it from definitions you control, PII and secret categories are refused before the query runs, and every call lands in a tamper-evident SHA-256 audit chain
  <sub>★ 9 · Python · Apache-2.0 · uv · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx schemabrain init`</sub>
- **[narekmalk/safedb-mcp](https://github.com/narekmalk/safedb-mcp)** — Secure MCP server for safe, read-only DB access by AI agents, with SQL guardrails, table allowlists, PII masking, and audit logs
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @safedb/safedb-mcp init --output safedb.yaml`</sub>
- **[skysqlinc/skysql-mcp](https://github.com/mariadb-corporation/skysql-mcp)** — Serverless MariaDB Cloud DB MCP server. Tools to launch, delete, execute SQL and work with DB level AI agents for accurate text-2-sql and conversations
  <sub>★ 8 · Python · MIT · clone · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:skysqlinc/skysql-mcp.git`</sub>
- **[yannbrrd/simple_snowflake_mcp](https://github.com/YannBrrd/simple_snowflake_mcp)** — Simple Snowflake MCP server that works behind a corporate proxy. Read and write (optional) operations
  <sub>★ 8 · Python · MIT · npx · pushed 2026-07-16 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run simple-snowflake-mcp`</sub>
- **[yincongcyincong/VictoriaMetrics-mcp-server](https://github.com/yincongcyincong/VictoriaMetrics-mcp-server)** — An MCP server for interacting with VictoriaMetrics database
  <sub>★ 8 · JavaScript · npx · pushed 2025-11-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @yincongcyincong/victoriametrics-mcp-server --client claude`</sub>
- **[mickelsamuel/migrationpilot](https://github.com/mickelsamuel/migrationpilot)** — Gate unsafe PostgreSQL migrations before an agent writes or runs them. check_before_apply returns pass/fail; 112 lock-safety rules, offline, no database required. npx migrationpilot-mcp
  <sub>★ 7 · TypeScript · MIT · npm · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g migrationpilot # global`</sub>
- **[tradercjz/dolphindb-mcp-server](https://github.com/tradercjz/dolphindb-mcp-server)** — TDolphinDB database integration with schema inspection and query capabilities
  <sub>★ 7 · Python · uv · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx install dolphindb-mcp-server`</sub>
- **[andyWang1688/sql-query-mcp](https://github.com/andyWang1688/sql-query-mcp)** — A general-purpose MCP server that lets AI work with multiple databases within clear boundaries. Supports PostgreSQL and MySQL today with schema discovery, sampling, read-only queries, and query-plan inspection
  <sub>★ 6 · Python · MIT · pipx · pushed 2026-06-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install sql-query-mcp`</sub>
- **[mbentham/SqlAugur](https://github.com/mbentham/SqlAugur)** — #️⃣ 🏠 🪟 🐧 - SQL Server MCP server with AST-based query validation, read-only safety, schema exploration, ER diagram generation, and DBA toolkit integration (First Responder Kit, DarlingData, sp_WhoIsActive)
  <sub>★ 6 · C# · MIT · clone · pushed 2026-09-01 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone git@github.com:mbentham/SqlAugur.git`</sub>
- **[KashiwaByte/vikingdb-mcp-server](https://github.com/KashiwaByte/vikingdb-mcp-server)** — VikingDB integration with collection and index introduction, vector store and search capabilities
  <sub>★ 5 · Python · npx · pushed 2025-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-server-vikingdb --client claude`</sub>
- **[nlqueries/nlqueries](https://github.com/nlqueries/nlqueries)** — Natural language to validated SQL engine with multi-connector support (PostgreSQL, MySQL, Snowflake, BigQuery, DuckDB), document QA, semantic caching, and self-hosted MCP server
  <sub>★ 4 · Python · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install nlqueries-core`</sub>
- **[pilat/mcp-datalink](https://github.com/pilat/mcp-datalink)** — MCP server for secure database access (PostgreSQL, MySQL, SQLite) with parameterized queries and schema inspection
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @pilat/mcp-datalink`</sub>
- **[astandrik/local-ydb-toolkit](https://github.com/astandrik/local-ydb-toolkit)** — Local YDB MCP is a TypeScript stdio MCP server for operating Docker-based local-ydb deployments via local or SSH-backed profiles. Supports bootstrap, diagnostics, auth hardening, storage workflows, dump/restore, upgrades, and plan-first mutating operations
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @astandrik/local-ydb-mcp`</sub>
- **[Eszetael/postgres-mcp-hardened](https://github.com/Eszetael/postgres-mcp-hardened)** — Maintained Rust replacement for the archived @modelcontextprotocol/server-postgres. Writes are refused twice: sqlparser AST validation rejects mutating statements before execution, and the session runs default_transaction_read_only with a per-session statement_timeout — so the read-only transaction is the fallback, not the only defence. Single self-contained binary, stdio and Streamable HTTP, sche
  <sub>★ 3 · Rust · MIT · npx · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx postgres-mcp-hardened --validate "/* comment */ DROP TABLE users"`</sub>
- **[Janadasroor/pg-mnemosyne-mcp](https://github.com/Janadasroor/pg-mnemosyne-mcp)** — A PostgreSQL Model Context Protocol (MCP) server acting as a robust persistent super memory, task tracker, and multi-agent coordination hub for AI assistants
  <sub>★ 3 · Python · MIT · pipx · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install pg-mnemosyne-mcp`</sub>
- **[montumodi/mongodb-atlas-mcp-server](https://github.com/montumodi/mongodb-atlas-mcp-server)** — A Model Context Protocol (MCP) that provides access to the MongoDB Atlas API. This server wraps the mongodb-atlas-api-client package to expose MongoDB Atlas functionality through MCP tools
  <sub>★ 3 · JavaScript · MIT · clone · pushed 2026-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/montumodi/mongodb-atlas-mcp-server.git`</sub>
- **[ofershap/mcp-server-sqlite](https://github.com/ofershap/mcp-server-sqlite)** — SQLite operations — query databases, inspect schemas, explain queries, and export data
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-sqlite-server`</sub>
- **[SurajKGoyal/amnesic](https://github.com/SurajKGoyal/amnesic)** — The MCP server that remembers your database — persists table/column annotations, an FK relationship graph, and searchable notes across sessions, so the model stops re-discovering your schema every time. PostgreSQL, MySQL, MSSQL, SQLite; read-only-enforced
  <sub>★ 3 · Python · MIT · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install amnesic`</sub>
- **[dockndevai/mcp-clickhouse](https://github.com/dockndevai/mcp-clickhouse)** — ClickHouse schema exploration, analytical queries &amp; management — every statement classified read/write/destructive and gated by access mode, with row caps and audit. npx -y @dockndevai/mcp-clickhouse
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-clickhouse.git`</sub>
- **[cvelasquez/mcp-sqlserver](https://github.com/cvelasquez/mcp-sqlserver)** — Manage dozens of SQL Server instances from one config file, grouped by client or environment and hot-reloaded, with execution plans, index audits and stored-procedure analysis
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @cevelas/mcp-sqlserver --init`</sub>
- **[Michael2150/flamerobin-mcp-server](https://github.com/Michael2150/flamerobin-mcp-server)** — #️⃣ 🏠 🪟 - Firebird database MCP server that reads connection details from FlameRobin's config — no credential setup required. Access all locally registered databases in one session with full schema introspection, DDL/DML execution, execution plans, and missing index analysis
  <sub>★ 2 · C# · MIT · source · pushed 2026-06-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Michael2150/flamerobin-mcp-server.git`</sub>
- **[izzzzzi/izTolkMcp](https://github.com/izzzzzi/izTolkMcp)** — MCP server for the Tolk smart contract compiler on TON blockchain. Compile, syntax-check, and generate deployment deeplinks for TON contracts directly from AI assistants
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g iz-tolk-mcp`</sub>
- **[kosminus/querywise-mcp](https://github.com/kosminus/querywise-mcp)** — Query SQL databases (SQLite, PostgreSQL, BigQuery, Databricks) in natural language through a business semantic layer — glossary, metrics, and a data dictionary grounded against your real schema
  <sub>★ 2 · Python · MIT · source · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kosminus/querywise-mcp.git`</sub>
- **[lintbase/lintbase-mcp](https://github.com/lintbase/lintbase)** — Ground-truth Firestore schema context for AI coding agents. Stops Cursor, Claude, and Windsurf from hallucinating field names and queries. Scans live collections, returns real field names, types, and presence rates
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx lintbase export-context firestore --key ./service-account.json`</sub>
- **[questdb/mcp-server-questdb](https://github.com/questdb/mcp-server-questdb)** — Official QuestDB MCP server that lets coding agents drive the QuestDB Web Console: notebook cells, SQL queries, and charts on live time-series data
  <sub>★ 2 · TypeScript · Apache-2.0 · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @questdb/mcp-server-questdb setup`</sub>
- **[ugurcl/dbridge-mcp](https://github.com/ugurcl/dbridge-mcp)** — Query SQLite, PostgreSQL, and MySQL in plain language — read-only by design, with column hiding/masking, row caps, per-query timeouts, cost-based rejection, and rate limiting
  <sub>★ 2 · TypeScript · npm · pushed 2026-07-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g dbridge-mcp`</sub>
- **[GetMystAdmin/urdb-mcp](https://github.com/GetMystAdmin/urdb-mcp)** — Search URDB's product integrity database for integrity scores, enshittification events, and change tracking across consumer products
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GetMystAdmin/urdb-mcp.git`</sub>
- **[dockndevai/mcp-percona-pg](https://github.com/dockndevai/mcp-percona-pg)** — Percona Operator for PostgreSQL: manage PostgreSQL + PgBouncer clusters, connection pooling, PostgreSQL tuning, backups/PITR, DR &amp; major upgrades — safe-by-default access modes, cluster allowlists, protected clusters, restore/upgrade/delete gating, and typed confirmation. npx -y @dockndevai/mcp-percona-pg
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-percona-pg.git`</sub>
- **[gigamori/mcp-run-sql-connectorx](https://github.com/gigamori/mcp-run-sql-connectorx)** — An MCP server that executes SQL via ConnectorX and streams the result to a CSV or Parquet file. Supports PostgreSQL, MariaDB, BigQuery, RedShift, MS SQL Server, etc
  <sub>★ 1 · Python · MIT · uv · pushed 2025-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx run-sql-connectorx \`</sub>
- **[mahAnuj/mcp-multi-db](https://github.com/mahAnuj/mcp-multi-db)** — One MCP server for PostgreSQL, MySQL, and SQLite. Unified read-only tools (list_databases, list_tables, describe_table, run_query) across all three engines with two-layer read-only enforcement (SQL-text guard + DB-level read-only transactions). Install: npx -y mcp-multi-db
  <sub>★ 1 · TypeScript · ISC · npm · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-multi-db`</sub>
- **[seob717/redash-mcp](https://github.com/seob717/redash-mcp)** — Connect Redash to Claude — natural-language SQL with safety guards (blocks DROP/TRUNCATE, PII detection), BIRD-based smart table selection, plus saved queries, dashboards, widgets, and alerts
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx redash-mcp setup`</sub>
- **[srmadscience/mcpdbwizard-open](https://github.com/srmadscience/mcpdbwizard-open)** — Oracle 12c–26ai with no run-sql tool. You select the PL/SQL packages, tables, sequences and your own tested SQL statements, and it generates a Java MCP server exposing exactly those as typed tools — each with a real JSON Schema derived from the procedure's signature, covering records, collections, %ROWTYPEs, REF CURSORs and any number of OUT parameters. Anything you did not select has no tool, no
  <sub>★ 1 · Java · Apache-2.0 · source · pushed 2026-09-26</sub>
  <sub>`git clone https://github.com/srmadscience/mcpdbwizard-open.git`</sub>
- **[ThinAirTelematics/thinair-data](https://github.com/ThinAirTelematics/thinair-data)** — Connect any AI to PostgreSQL, MySQL, or SQL Server — 24 dialect-aware tools for query, schema introspection, optimization, migrations, PII scan, and more. Hosted MCP server with OAuth 2.0 + Bearer auth, free trial available
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @thinairtelematics/data`</sub>
- **[croc100/Litescope](https://github.com/croc100/Litescope)** — MCP-first operations toolchain for SQLite, Cloudflare D1, and Turso. Inspect, diff, migrate, monitor, back up, and repair databases over stdio. Read-only by default; writes are opt-in, dry-run first, and auto-snapshot before applying. npx -y litescope mcp
  <sub>★ 1 · Go · AGPL-3.0 · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g litescope`</sub>
- **[gulmezeren2-byte/erp-report-engine](https://github.com/gulmezeren2-byte/erp-report-engine)** — Read-only MCP over the SQL database behind an ERP (Logo Tiger, Netsis, Mikro). The agent sees canonical entities like orders, never raw ERP tables, through a four-layer read-only guard that checks the statement, fails closed, and blocks side-effecting functions (pg_read_file, xp_cmdshell, …) — measured by a public 28-attack benchmark and an in-browser "break it" playground running the real guard v
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install erp-report-engine # or: uv tool install erp-report-engine`</sub>
- **[AIops-tools/Postgres-AIops](https://github.com/AIops-tools/Postgres-AIops)** — Governed PostgreSQL DBA operations — slow-query, bloat, and blocking-lock RCA, index management, vacuum/analyze, and replication lag (35 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, dry-run, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install postgres-aiops # or: pipx install postgres-aiops`</sub>
- **[get-convex/convex-backend](https://stack.convex.dev/convex-mcp-server)** — Convex database integration to introspect tables, functions, and run oneoff queries (Source)
  <sub>website</sub>
  <sub>`https://stack.convex.dev/convex-mcp-server`</sub>
- **[infino-ai/infino-mcp](https://github.com/infino-ai/infino-mcp)** — Retrieval over your own data with Infino (BM25 full-text, vector, hybrid, and SQL), an embedded engine on Apache Parquet over object storage
  <sub>JavaScript · Apache-2.0 · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @infino-ai/mcp-server`</sub>
- **[igorolv/jdbc-mcp-server](https://github.com/igorolv/jdbc-mcp-server)** — Read-only access to PostgreSQL, Oracle, and SQL Server for AI agents: schema discovery, query validation, execution plans, benchmarking, and index/statistics analysis. JDBC drivers bundled
  <sub>Java · Apache-2.0 · source · pushed 2026-09-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/igorolv/jdbc-mcp-server.git`</sub>
- **[memgraph/mcp-memgraph](https://github.com/memgraph/ai-toolkit/tree/main/integrations/mcp-memgraph)** — Memgraph MCP Server - includes a tool to run a query against Memgraph and a schema resource
  <sub>Python · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/memgraph/ai-toolkit.git && cd ai-toolkit/integrations/mcp-memgraph`</sub>
- **[modelcontextprotocol/server-postgres](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres)** — PostgreSQL database integration with schema inspection and query capabilities
  <sub>JavaScript · MIT · in-repo · pushed 2025-05-28</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers-archived.git && cd servers-archived/src/postgres`</sub>
- **[modelcontextprotocol/server-sqlite](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite)** — SQLite database operations with built-in analysis features
  <sub>JavaScript · MIT · in-repo · pushed 2025-05-28</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers-archived.git && cd servers-archived/src/sqlite`</sub>
- **[planetscale/mcp](https://github.com/planetscale/cli?tab=readme-ov-file#mcp-server-integration)** — The PlanetScale CLI includes an MCP server that provides AI tools direct access to your PlanetScale databases
  <sub>Go · Apache-2.0 · in-repo · pushed 2026-09-25</sub>
  <sub>`git clone https://github.com/planetscale/cli.git && cd cli/?tab=readme-ov-file#mcp-server-integration`</sub>
- **[quarkiverse/mcp-server-jdbc](https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/jdbc)** — Connect to any JDBC-compatible database and query, insert, update, delete, and more
  <sub>Java · Apache-2.0 · in-repo · pushed 2026-06-14</sub>
  <sub>`git clone https://github.com/quarkiverse/quarkus-mcp-servers.git && cd quarkus-mcp-servers/jdbc`</sub>
- **[Yusufihsangorgel/queue-inspector-mcp](https://github.com/Yusufihsangorgel/queue-inspector-mcp)** — Inspect and operate Redis-backed job queues (Asynq and BullMQ): per-state counts, job detail with decoded payload and last error, and faithful retry/delete running each library's own scripts. Read-only mode for production
  <sub>TypeScript · MIT · npm · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g queue-inspector-mcp`</sub>
- **[Rheopyrin/db-access-mcp](https://github.com/Rheopyrin/db-access-mcp)** — Query PostgreSQL, MySQL, Redshift and SQL Server over verified SSH / AWS SSM tunnels, with read-only enforcement, confined file exports, and pluggable secret providers (env, Vault, AWS Secrets Manager, RDS IAM). Published on the official MCP Registry
  <sub>TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @modelcontextprotocol/inspector npx -y @rheopyrin/db-access-mcp`</sub>
- **[Rufflet/mysql-legacy-mcp](https://github.com/Rufflet/mysql-legacy-mcp)** — MCP server for legacy MySQL 5.0–5.6: schema inspection and SELECT by default, with opt-in INSERT/UPDATE/DELETE/DDL. Live-verified against MySQL 5.0–8.0. npx -y mysql-legacy-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mysql-legacy-mcp`</sub>
- **[seedfast-ai/seedfast-mcp](https://github.com/seedfast-ai/seedfast-mcp)** — Fills a PostgreSQL database with synthetic test data generated from its live schema, so an agent can plan a seed, run it and follow it to completion without production data. Runs as npx -y seedfast mcp, published in the official MCP registry as st.seedfa/seedfast
  <sub>JavaScript · MIT · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g seedfast # any platform with Node.js`</sub>
- **[sqemo/sqemo-mcp](https://github.com/sqemo/sqemo-mcp)** — Design ERDs that follow your team's naming standards. Query and edit entities, relationships and domains, generate physical names from a shared glossary, import/export SQL (7 dialects) and DBML, and diff the model against a live database. Local .erd.json files work without an account
  <sub>Dockerfile · MIT · npx · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sqemo-mcp login # pick Google, GitHub, or email + password`</sub>
- **[wenerme/wener-mssql-mcp](https://github.com/wenerme/wode/tree/develop/packages/wener-mssql-mcp)** — MSSQL database integration with schema inspection and query capabilities
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/wenerme/wode.git && cd wode/packages/wener-mssql-mcp`</sub>
- **[rafim-dev/schema-bridge-mcp](https://github.com/rafim-dev/schema-bridge-mcp)** — Universal schema compiler (SQL/Prisma to Zod, TypeScript, Pydantic) and realistic synthetic mock API data generator
  <sub>TypeScript · MIT · clone · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rafim-dev/schema-bridge-mcp.git`</sub>

## Search &amp; Data Extraction

- **[KnockOutEZ/wigolo](https://github.com/KnockOutEZ/wigolo)** — Local-first, keyless web intelligence in one server: search, fetch, crawl, extract, cache, find-similar, and research. Multi-engine search with local ML reranking and a persistent SQLite cache, renders JS-heavy pages, and keeps everything on your machine. Install via npx wigolo init --non-interactive --agents=
  <sub>★ 5.4k · TypeScript · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx wigolo init # set up the local engine — any system`</sub>
- **[exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)** — A Model Context Protocol (MCP) server lets AI assistants like Claude use the Exa AI Search API for web searches. This setup allows AI models to get real-time web information in a safe and controlled way
  <sub>★ 5.1k · TypeScript · MIT · source · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/exa-labs/exa-mcp-server.git`</sub>
- **[blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server)** — Search ArXiv research papers
  <sub>★ 3.2k · Python · Apache-2.0 · npx · pushed 2026-08-26 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npx arxiv-mcp-server`</sub>
- **[luminati-io/brightdata-mcp](https://github.com/brightdata/brightdata-mcp)** — Discover, extract, and interact with the web - one interface powering automated access across the public internet
  <sub>★ 2.7k · JavaScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @brightdata/mcp`</sub>
- **[Aas-ee/open-webSearch](https://github.com/Aas-ee/open-webSearch)** — Web search using free multi-engine search (NO API KEYS REQUIRED) — Supports Bing, Baidu, DuckDuckGo, Brave, Exa, and CSDN
  <sub>★ 1.8k · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g open-websearch`</sub>
- **[nickclyde/duckduckgo-mcp-server](https://github.com/nickclyde/duckduckgo-mcp-server)** — Web search using DuckDuckGo
  <sub>★ 1.5k · Python · MIT · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx duckduckgo-mcp-server`</sub>
- **[brave/brave-search-mcp-server](https://github.com/brave/brave-search-mcp-server)** — Web search capabilities using Brave's Search API
  <sub>★ 1.5k · TypeScript · MIT · clone · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/brave/brave-search-mcp-server.git`</sub>
- **[Ihor-Sokoliuk/MCP-SearXNG](https://github.com/ihor-sokoliuk/mcp-searxng)** — /☁️ - A Model Context Protocol Server for SearXNG
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-searxng`</sub>
- **[jae-jae/fetcher-mcp](https://github.com/jae-jae/fetcher-mcp)** — MCP server for fetching web page content using Playwright headless browser, supporting Javascript rendering and intelligent content extraction, and outputting Markdown or HTML format
  <sub>★ 1.1k · TypeScript · MIT · npx · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y fetcher-mcp`</sub>
- **[us/crw](https://github.com/fastcrw/crw)** — fastCRW — open-source (AGPL-3.0), self-hostable Rust web crawler &amp; search API for AI agents. Tools: scrape, crawl, map, and SearXNG-backed search. Single ~6MB static binary; reproducible 1K-URL benchmarks faster than hosted alternatives. Hosted MCP at fastcrw.com/mcp (Streamable HTTP, OAuth) or self-host
  <sub>★ 1.1k · Rust · AGPL-3.0 · npx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y crw-mcp@latest install`</sub>
- **[kagisearch/kagimcp](https://github.com/kagisearch/kagimcp)** — Official Kagi Search MCP Server
  <sub>★ 528 · Python · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install kagimcp --client claude`</sub>
- **[mzxrai/mcp-webresearch](https://github.com/mzxrai/mcp-webresearch)** — Search Google and do deep web research on any topic
  <sub>★ 298 · JavaScript · MIT · source · pushed 2024-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mzxrai/mcp-webresearch.git`</sub>
- **[jae-jae/g-search-mcp](https://github.com/jae-jae/g-search-mcp)** — A powerful MCP server for Google search that enables parallel searching with multiple keywords simultaneously
  <sub>★ 273 · TypeScript · MIT · npx · pushed 2025-06-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y g-search-mcp`</sub>
- **[hellokaton/unsplash-mcp-server](https://github.com/hellokaton/unsplash-mcp-server)** — ) 🐍 ☁️ - A MCP server for Unsplash image search
  <sub>★ 237 · Python · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest install @hellokaton/unsplash-mcp-server --client cursor --key 7558c683-****-****`</sub>
- **[MarcellM01/TinySearch](https://github.com/TinySuiteHQ/TinySearch)** — Self-hosted web research for MCP agents: search (SearXNG, with DuckDuckGo fallback), crawl, dense+BM25 rerank, and dedupe into a source-grounded, cited prompt. Local ONNX embeddings by default, or bring an OpenAI-compatible embedding API
  <sub>★ 228 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from "tinysuite-search[server]" tinysearch setup`</sub>
- **[reading-plus-ai/mcp-server-deep-research](https://github.com/reading-plus-ai/mcp-server-deep-research)** — MCP server providing OpenAI/Perplexity-like autonomous deep research, structured query elaboration, and concise reporting
  <sub>★ 215 · Python · MIT · source · pushed 2025-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reading-plus-ai/mcp-server-deep-research.git`</sub>
- **[deadletterq/mcp-opennutrition](https://github.com/deadletterq/mcp-opennutrition)** — Local MCP server for searching 300,000+ foods, nutrition facts, and barcodes from the OpenNutrition database
  <sub>★ 208 · TypeScript · MIT · docker · pushed 2026-07-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 9113:3000 deadletterq/mcp-opennutrition`</sub>
- **[apify/mcp-server-rag-web-browser](https://github.com/apify/mcp-server-rag-web-browser)** — An MCP server for Apify's open-source RAG Web Browser Actor to perform web searches, scrape URLs, and return content in Markdown
  <sub>★ 206 · JavaScript · Apache-2.0 · clone · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/apify/mcp-server-rag-web-browser.git`</sub>
- **[andybrandt/mcp-simple-arxiv](https://github.com/andybrandt/mcp-simple-arxiv)** — MCP for LLM to search and read papers from arXiv
  <sub>★ 200 · Python · MIT · npx · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-simple-arxiv --client claude`</sub>
- **[tinyfish-io/agentql-mcp](https://github.com/tinyfish-io/agentql-mcp)** — MCP server that provides AgentQL's data extraction capabilities
  <sub>★ 181 · TypeScript · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentql-mcp`</sub>
- **[fatwang2/search1api-mcp](https://github.com/superagents-lab/search1api-mcp)** — Search via search1api (requires paid API key)
  <sub>★ 174 · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g search1api-cli`</sub>
- **[lfnovo/content-core](https://github.com/lfnovo/content-core)** — Extract content from URLs, documents, videos, and audio files using intelligent auto-engine selection. Supports web pages, PDFs, Word docs, YouTube transcripts, and more with structured JSON responses
  <sub>★ 174 · Python · MIT · uv · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx content-core extract "https://example.com"`</sub>
- **[serpapi/serpapi-mcp](https://github.com/serpapi/serpapi-mcp)** — SerpApi MCP Server for Google and other search engine results. Provides multi-engine search across Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay, and more with real-time weather data, stock market information, and flexible JSON response modes
  <sub>★ 173 · Python · MIT · clone · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/serpapi/serpapi-mcp.git`</sub>
- **[andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed)** — MCP to search and read medical / life sciences papers from PubMed
  <sub>★ 172 · Python · MIT · npx · pushed 2026-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-simple-pubmed --client claude`</sub>
- **[scrapeless-ai/scrapeless-mcp-server](https://github.com/scrapeless-ai/scrapeless-mcp-server)** — The Scrapeless Model Context Protocol service acts as an MCP server connector to the Google SERP API, enabling web search within the MCP ecosystem without leaving it
  <sub>★ 169 · TypeScript · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scrapeless-ai/scrapeless-mcp-server.git`</sub>
- **[just-every/mcp-read-website-fast](https://github.com/just-every/mcp-read-website-fast)** — Fast, token-efficient web content extraction for AI agents - converts websites to clean Markdown while preserving links. Features Mozilla Readability, smart caching, polite crawling with robots.txt support, and concurrent fetching
  <sub>★ 160 · TypeScript · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/just-every/mcp-read-website-fast.git`</sub>
- **[konippi/servo-fetch](https://github.com/konippi/servo-fetch)** — Chromium-free web content extraction in a single binary. Fetch, render, crawl, and screenshot powered by the Servo browser engine with a built-in MCP server
  <sub>★ 152 · Rust · Apache-2.0 · npx · pushed 2026-09-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx servo-fetch "https://example.com"`</sub>
- **[takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp)** — Get the LaTeX source of arXiv papers to handle mathematical content and equations
  <sub>★ 146 · Python · MIT · pip · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install arxiv-latex-mcp`</sub>
- **[nkapila6/mcp-local-rag](https://github.com/nkapila6/mcp-local-rag)** — "primitive" RAG-like web search model context protocol (MCP) server that runs locally. No APIs needed
  <sub>★ 135 · Python · MIT · source · pushed 2026-08-31 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nkapila6/mcp-local-rag.git`</sub>
- **[SecretiveShell/MCP-searxng](https://github.com/SecretiveShell/MCP-searxng)** — An MCP Server to connect to searXNG instances
  <sub>★ 131 · Python · MIT · uv · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-searxng`</sub>
- **[chanmeng/google-news-mcp-server](https://github.com/ChanMeng666/server-google-news)** — Google News integration with automatic topic categorization, multi-language support, and comprehensive search capabilities including headlines, stories, and related topics through SerpAPI
  <sub>★ 129 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @chanmeng666/google-news-server --client claude`</sub>
- **[mikechao/brave-search-mcp](https://github.com/mikechao/brave-search-mcp)** — Web, Image, News, Video, and Local Point of Interest search capabilities using Brave's Search API
  <sub>★ 126 · TypeScript · GPL-3.0 · docker · pushed 2026-05-28 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -p 3001:3001 -e BRAVE_API_KEY="YOUR_API_KEY_HERE" brave-search-mcp:latest --http`</sub>
- **[vectorize-io/vectorize-mcp-server](https://github.com/vectorize-io/vectorize-mcp-server/)** — Vectorize MCP server for advanced retrieval, Private Deep Research, Anything-to-Markdown file extraction and text chunking
  <sub>★ 112 · TypeScript · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @vectorize-io/vectorize-mcp-server@latest`</sub>
- **[lennney/agent-search-mcp](https://github.com/lennney/agent-search-mcp)** — Free multi-engine MCP search server — 8 free engines (DDG, Sogou, Bing, Baidu, Wikipedia, Startpage, Yandex, Mojeek), waterfall progressive search, multi-source verification, content enrichment, news search, language auto-detection, CLI. Zero API keys needed. npx agent-search-mcp
  <sub>★ 111 · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-search-mcp`</sub>
- **[just-every/mcp-screenshot-website-fast](https://github.com/just-every/mcp-screenshot-website-fast)** — Fast screenshot capture tool optimized for Claude Vision API. Automatically tiles full pages into 1072x1072 chunks for optimal AI processing with configurable viewports and wait strategies for dynamic content
  <sub>★ 110 · TypeScript · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/just-every/mcp-screenshot-website-fast.git`</sub>
- **[Sriram-PR/doc-scraper](https://github.com/Sriram-PR/doc-scraper)** — Crawl documentation sites into local Markdown/JSONL corpora and serve them to agents with offline BM25 search, page reads, freshness checks, and crawl diffs
  <sub>★ 101 · Go · Apache-2.0 · go · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/Sriram-PR/doc-scraper/v2/cmd/doc-scraper@latest`</sub>
- **[ConechoAI/openai-websearch-mcp](https://github.com/ConechoAI/openai-websearch-mcp/)** — This is a Python-based MCP server that provides OpenAI web_search built-in tool
  <sub>★ 94 · Python · MIT · npx · pushed 2025-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx openai-websearch-mcp`</sub>
- **[OctagonAI/octagon-deep-research-mcp](https://github.com/OctagonAI/octagon-deep-research-mcp)** — Lightning-Fast, High-Accuracy Deep Research Agent
  <sub>★ 93 · JavaScript · MIT · npm · pushed 2026-02-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g octagon-deep-research-mcp`</sub>
- **[zhsama/duckduckgo-mcp-server](https://github.com/zhsama/duckduckgo-mpc-server/)** — This is a TypeScript-based MCP server that provides DuckDuckGo search functionality
  <sub>★ 87 · TypeScript · MIT · source · pushed 2025-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zhsama/duckduckgo-mpc-server/.git`</sub>
- **[isnow890/naver-search-mcp](https://github.com/isnow890/naver-search-mcp)** — MCP server for Naver Search API integration, supporting blog, news, shopping search and DataLab analytics features
  <sub>★ 86 · TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @isnow890/naver-search-mcp`</sub>
- **[ricocf/mcp-wolframalpha](https://github.com/akalaric/mcp-wolframalpha)** — An MCP server lets AI assistants use the Wolfram Alpha API for real-time access to computational knowledge and data
  <sub>★ 86 · Python · MIT · docker · pushed 2026-01-12 · WSL2 · Linux · Docker</sub>
  <sub>`docker run wolframalphaui`</sub>
- **[NameetP/pdfmux](https://github.com/NameetP/pdfmux)** — PDF extraction router with built-in MCP server. Classifies each page (digital, scanned, tables) and routes to the best backend (PyMuPDF, Docling, OCR, or optional LLM fallback). Per-page confidence scoring flags low-quality pages and auto-reextracts them — prevents silent RAG failures. Zero config: pip install pdfmux. MIT licensed
  <sub>★ 82 · Python · MIT · pip · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pdfmux`</sub>
- **[zoomeye-ai/mcp_zoomeye](https://github.com/zoomeye-ai/mcp_zoomeye)** — Querying network asset information by ZoomEye MCP Server
  <sub>★ 82 · Python · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx mcp-server-zoomeye`</sub>
- **[leehanchung/bing-search-mcp](https://github.com/leehanchung/bing-search-mcp)** — Web search capabilities using Microsoft Bing Search API
  <sub>★ 80 · Python · MIT · uv · pushed 2025-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx bing-search-mcp`</sub>
- **[erithwik/mcp-hn](https://github.com/erithwik/mcp-hn)** — An MCP server to search Hacker News, get top stories, and more
  <sub>★ 76 · Python · MIT · npx · pushed 2025-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-hn --client claude`</sub>
- **[reflex-search/reflex](https://github.com/reflex-search/reflex)** — Local full-text code search for AI coding agents. Trigram-indexed, sub-100ms queries across large codebases, offline, 18 languages
  <sub>★ 75 · Rust · MIT · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g reflex-search`</sub>
- **[Linked-API/linkedapi-mcp](https://github.com/Linked-API/linkedapi-mcp)** — MCP server that lets AI assistants control LinkedIn accounts and retrieve real-time data
  <sub>★ 68 · TypeScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Linked-API/linkedapi-mcp.git`</sub>
- **[0xdaef0f/job-searchoor](https://github.com/0xDAEF0F/job-searchoor)** — An MCP server for searching job listings with filters for date, keywords, remote work options, and more
  <sub>★ 65 · JavaScript · MIT · source · pushed 2025-04-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0xDAEF0F/job-searchoor.git`</sub>
- **[zoharbabin/web-researcher-mcp](https://github.com/zoharbabin/web-researcher-mcp)** — Production-grade MCP server for web search (Google, Brave, Serper, SearXNG, SearchAPI.io), content extraction (4-tier pipeline), academic/patent search, and multi-source research. Single Go binary
  <sub>★ 63 · Go · MIT · winget · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`winget install zoharbabin.web-researcher-mcp`</sub>
- **[imprvhub/mcp-domain-availability](https://github.com/imprvhub/mcp-domain-availability)** — A Model Context Protocol (MCP) server that enables Claude Desktop to check domain availability across 50+ TLDs. Features DNS/WHOIS verification, bulk checking, and smart suggestions. Zero-clone installation via uvx
  <sub>★ 59 · Python · MPL-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli@latest mcp add imprvhub/mcp-domain-availability --client claude`</sub>
- **[tobocop2/lilbee](https://github.com/tobocop2/lilbee)** — Runs and manages its own local models, or uses your existing Ollama or LM Studio if you prefer. Indexes your files and code, crawls the websites you point it at, and answers with citations to the source
  <sub>★ 59 · Python · MIT · scoop · pushed 2026-09-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop install lilbee-cuda`</sub>
- **[ananddtyagi/webpage-screenshot-mcp](https://github.com/ananddtyagi/webpage-screenshot-mcp)** — A MCP server for taking screenshots of webpages to use as feedback during UI developement
  <sub>★ 57 · JavaScript · MIT · clone · pushed 2025-06-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ananddtyagi/webpage-screenshot-mcp.git`</sub>
- **[sifter-ai/sifter](https://github.com/sifter-ai/sifter)** — Structure any document, query it like a database. Open-source extraction engine that turns any document into typed, schema-defined records, queryable in natural language from Claude, ChatGPT, Gemini, or any MCP client
  <sub>★ 54 · Python · MIT · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install sifter-ai`</sub>
- **[Tomatio13/mcp-server-tavily](https://github.com/Tomatio13/mcp-server-tavily)** — Tavily AI search API
  <sub>★ 50 · Python · MIT · npx · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install tavily-search --client claude`</sub>
- **[goesByhc/cn-scraper-mcp](https://github.com/goesByhc/cn-scraper-mcp)** — MCP server that lets AI agents search and extract data from major Chinese internet platforms including Taobao, JD, Xiaohongshu, Zhihu, Weibo, Bilibili, ZSXQ, Douban, and Dianping, with local-first cookie storage and CDP-assisted login
  <sub>★ 47 · Python · MIT · pip · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install cn-scraper-mcp`</sub>
- **[pragmar/mcp-server-webcrawl](https://github.com/pragmar/mcp-server-webcrawl)** — Advanced search and retrieval for web crawler data. Supports WARC, wget, Katana, SiteOne, and InterroBot crawlers
  <sub>★ 46 · Python · pip · pushed 2026-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-server-webcrawl`</sub>
- **[ac3xx/mcp-servers-kagi](https://github.com/ac3xx/mcp-servers-kagi)** — Kagi search API integration
  <sub>★ 44 · TypeScript · MIT · source · pushed 2024-12-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ac3xx/mcp-servers-kagi.git`</sub>
- **[webscraping-ai/webscraping-ai-mcp-server](https://github.com/webscraping-ai/webscraping-ai-mcp-server)** — Interact with WebScraping.ai for web data extraction and scraping
  <sub>★ 44 · JavaScript · clone · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/webscraping-ai/webscraping-ai-mcp-server.git`</sub>
- **[DappierAI/dappier-mcp](https://github.com/DappierAI/dappier-mcp)** — Enable fast, free real-time web search and access premium data from trusted media brands—news, financial markets, sports, entertainment, weather, and more. Build powerful AI agents with Dappier
  <sub>★ 43 · Python · MIT · npx · pushed 2025-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @DappierAI/dappier-mcp --client claude`</sub>
- **[trendsmcp-ai/Trends-MCP](https://github.com/trendsmcp-ai/Trends-MCP)** — Live trend data from Google, TikTok, YouTube, Amazon, Reddit, npm, Steam, and 20+ other sources. Local stdio via uvx trends-mcp-server or hosted at https://api.trendsmcp.ai/mcp
  <sub>★ 43 · Python · MIT · pip · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install trendsmcp`</sub>
- **[czottmann/kagi-ken-mcp](https://github.com/czottmann/kagi-ken-mcp)** — Work with Kagi *without* API access (you'll need to be a customer, tho). Searches and summarizes. Uses Kagi session token for easy authentication
  <sub>★ 41 · JavaScript · MIT · npx · pushed 2026-02-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:czottmann/kagi-ken-mcp`</sub>
- **[yamanoku/baseline-mcp-server](https://github.com/yamanoku/baseline-mcp-server)** — MCP server that searches Baseline status using Web Platform API
  <sub>★ 37 · TypeScript · MIT · source · pushed 2026-09-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/yamanoku/baseline-mcp-server.git`</sub>
- **[pranciskus/newsmcp](https://github.com/pranciskus/newsmcp)** — Real-time world news for AI agents — events clustered from hundreds of sources, classified by topic and geography, ranked by importance. Free, no API key. npx -y @newsmcp/server
  <sub>★ 35 · TypeScript · MIT · npx · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @newsmcp/server --client claude`</sub>
- **[format37/youtube_mcp](https://github.com/format37/youtube_mcp)** — MCP server that transcribes YouTube videos to text. Uses yt-dlp to download audio and OpenAI's Whisper-1 for more precise transcription than youtube captions. Provide a YouTube URL and get back the full transcript splitted by chunks for long videos
  <sub>★ 32 · Python · clone · pushed 2025-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/format37/youtube_mcp.git`</sub>
- **[Dumpling-AI/mcp-server-dumplingai](https://github.com/DumplingAI/mcp-server-dumplingai)** — Access data, web scraping, and document conversion APIs by Dumpling AI
  <sub>★ 31 · JavaScript · MIT · npm · pushed 2025-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-server-dumplingai`</sub>
- **[cevatkerim/unsplash-mcp](https://github.com/cevatkerim/unsplash-mcp)** — Unsplash photo search with proper attribution. Returns ready-to-use attribution text and HTML for each photo, making it easy for LLMs to build content pages with properly credited images. Includes search, random photos, and download tracking
  <sub>★ 29 · Python · MIT · clone · pushed 2026-01-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cevatkerim/unsplash-mcp.git`</sub>
- **[dorukardahan/domain-search-mcp](https://github.com/dorukardahan/domain-search-mcp)** — Fast domain availability aggregator with pricing. Checks Porkbun, Namecheap, GoDaddy, RDAP &amp; WHOIS. Includes bulk search, registrar comparison, AI-powered suggestions, and social media handle checking
  <sub>★ 28 · TypeScript · MIT · npx · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y domain-search-mcp@latest`</sub>
- **[FayAndXan/spectrawl](https://github.com/Pyx-Corp/spectrawl)** — Unified web layer for AI agents. Search (8 engines), stealth browse, cookie auth, and act on 24 platforms. 5,000 free searches/month via Gemini Grounded Search
  <sub>★ 28 · JavaScript · MIT · npx · pushed 2026-03-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx spectrawl config set proxy '{"host":"brd.superproxy.io","port":22225,"username":"YOUR_ZONE_USER","password":"YOUR_PASS"}'`</sub>
- **[imprvhub/mcp-rss-aggregator](https://github.com/imprvhub/mcp-rss-aggregator)** — Model Context Protocol Server for aggregating RSS feeds in Claude Desktop
  <sub>★ 27 · TypeScript · MPL-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest mcp add imprvhub/mcp-rss-aggregator --client claude`</sub>
- **[joelio/stocky](https://github.com/joelio/stocky)** — An MCP server for searching and downloading royalty-free stock photography from Pexels and Unsplash. Features multi-provider search, rich metadata, pagination support, and async performance for AI assistants to find and access high-quality images
  <sub>★ 27 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install stocky-mcp # or: pipx install stocky-mcp`</sub>
- **[hbg/mcp-paperswithcode](https://github.com/hbg/mcp-paperswithcode)** — MCP to search through PapersWithCode API
  <sub>★ 26 · Python · MIT · npx · pushed 2025-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @hbg/mcp-paperswithcode --client claude`</sub>
- **[kehvinbehvin/json-mcp-filter](https://github.com/kehvinbehvin/json-mcp-filter)** — Stop bloating your LLM context. Query &amp; Extract only what you need from your JSON files
  <sub>★ 26 · JavaScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g json-mcp-filter@latest`</sub>
- **[telly6/searchpin](https://github.com/telly6/searchpin)** — Free web search for AI agents with smart re-ranking. Multi-engine parallel search, zero API keys. Works natively within China's network, no proxy/VPN needed. Install via pip install searchpin &amp;&amp; searchpin-setup
  <sub>★ 26 · Python · pip · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install searchpin`</sub>
- **[adawalli/nexus](https://github.com/adawalli/nexus)** — AI-powered web search server using Perplexity Sonar models with source citations. Zero-install setup via NPX
  <sub>★ 23 · TypeScript · MIT · npx · pushed 2026-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`bunx nexus-mcp`</sub>
- **[jhomen368/overseerr-mcp](https://github.com/jhomen368/overseerr-mcp)** — Integrate AI assistants with Overseerr and the Seerr (the unified successor) for automated media discovery, requests, and management in Plex, Jellyfin, and Emby ecosystems
  <sub>★ 23 · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @jhomen368/overseerr-mcp`</sub>
- **[r-huijts/opentk-mcp](https://github.com/r-huijts/opentk-mcp)** — Access Dutch Parliament (Tweede Kamer) information including documents, debates, activities, and legislative cases through structured search capabilities (based on opentk project by Bert Hubert)
  <sub>★ 22 · HTML · MIT · npx · pushed 2025-10-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @r-huijts/opentk-mcp`</sub>
- **[Himalayas-App/himalayas-mcp](https://github.com/Himalayas-App/himalayas-mcp)** — Access tens of thousands of remote job listings and company information. This public MCP server provides real-time access to Himalayas' remote jobs database
  <sub>★ 21 · MIT · npx · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-remote https://mcp.himalayas.app/mcp`</sub>
- **[oso95/domain-suite-mcp](https://github.com/oso95/domain-suite-mcp)** — Full domain lifecycle management: availability checking (zero config), registration, DNS, SSL, email auth (SPF/DKIM/DMARC), and WHOIS across Porkbun, Namecheap, GoDaddy, and Cloudflare. 21 tools
  <sub>★ 20 · TypeScript · MIT · npm · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g domain-suite-mcp`</sub>
- **[parallel-web/search-mcp](https://github.com/parallel-web/search-mcp)** — Highest Accuracy Web Search for AI
  <sub>★ 20 · MIT · source · pushed 2026-09-25</sub>
  <sub>`git clone https://github.com/parallel-web/search-mcp.git`</sub>
- **[rejifald/StitchAPI](https://github.com/rejifald/StitchAPI)** — Semantic search over the StitchAPI documentation (the hosted docs MCP): search_docs returns the most relevant doc sections with deep links, get_doc fetches a full page. Hosted endpoint https://stitchapi.dev/api/mcp, no auth
  <sub>★ 19 · TypeScript · Apache-2.0 · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rejifald/StitchAPI.git`</sub>
- **[angheljf/nyt](https://github.com/angheljf/nyt)** — Search articles using the NYTimes API
  <sub>★ 18 · JavaScript · MIT · npx · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install nyt --client claude`</sub>
- **[wd041216-bit/free-web-search-ultimate](https://github.com/wd041216-bit/zero-api-key-web-search)** — Zero-cost, privacy-first universal web search MCP server. Enforces a Search-First paradigm — instructs LLMs to retrieve real-time information before answering factual questions. Supports 10+ search engines (DuckDuckGo, Bing, Google, Brave, Wikipedia, Arxiv, YouTube, Reddit) and deep page browsing. No API key required
  <sub>★ 18 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zero-api-key-web-search # free search, no API key, no model download`</sub>
- **[n24q02m/wet-mcp](https://github.com/n24q02m/wet)** — Web search (embedded SearXNG), content extraction, and library docs indexing with hybrid search (FTS5 + semantic). Built-in Qwen3 embedding, no API keys required
  <sub>★ 18 · Python · Apache-2.0 · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from wet-mcp wet warmup # try a subcommand without a persistent install`</sub>
- **[the0807/GeekNews-MCP-Server](https://github.com/the0807/GeekNews-MCP-Server)** — An MCP Server that retrieves and processes news data from the GeekNews site
  <sub>★ 18 · Python · MIT · clone · pushed 2025-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/the0807/GeekNews-MCP-Server`</sub>
- **[cameronrye/activitypub-mcp](https://github.com/cameronrye/activitypub-mcp)** — A comprehensive MCP server that enables LLMs to explore and interact with the Fediverse through ActivityPub protocol. Features WebFinger discovery, timeline fetching, instance exploration, and cross-platform support for Mastodon, Pleroma, Misskey, and other ActivityPub servers
  <sub>★ 17 · TypeScript · MIT · npx · pushed 2026-09-13 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y activitypub-mcp`</sub>
- **[andyliszewski/webcrawl-mcp](https://github.com/andyliszewski/webcrawl-mcp)** — Local-first web scraping, search, and crawling. Static pages extracted locally via trafilatura; optional Firecrawl fallback only when JS rendering is needed. Four tools: scrape, search (DuckDuckGo), map, crawl
  <sub>★ 16 · Python · MIT · pip · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install webcrawl-mcp`</sub>
- **[gemy411/multi-research-agents](https://github.com/gemy411/multi-agents-research)** — a KTOR server/ MCP server written in Kotlin applying multi-agents schools in a flexible research system to be used with coding or for research any general case
  <sub>★ 16 · Kotlin · MIT · source · pushed 2026-03-19</sub>
  <sub>`git clone https://github.com/gemy411/multi-agents-research.git`</sub>
- **[parallel-web/task-mcp](https://github.com/parallel-web/task-mcp)** — Highest Accuracy Deep Research and Batch Tasks MCP
  <sub>★ 16 · TypeScript · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/parallel-web/task-mcp.git`</sub>
- **[tianqitang1/enrichr-mcp-server](https://github.com/tianqitang1/enrichr-mcp-server)** — A MCP server that provides gene set enrichment analysis using the Enrichr API
  <sub>★ 15 · TypeScript · npx · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install enrichr-mcp-server --client claude`</sub>
- **[KyuRish/fiverr-mcp-server](https://github.com/KyuRish/fiverr-mcp-server)** — Search Fiverr gigs, view seller profiles, compare pricing packages, and read reviews. No API key required
  <sub>★ 13 · Python · MIT · pip · pushed 2026-02-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install fiverr-mcp-server`</sub>
- **[MikkoParkkola/nab](https://github.com/MikkoParkkola/nab)** — Ultra-fast web fetcher and MCP server with HTTP/3, JS rendering, anti-fingerprinting, browser cookie auth, and 1Password integration. Fetches any URL as clean Markdown for AI context
  <sub>★ 13 · Rust · MIT · cargo · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo binstall nab`</sub>
- **[vitorpavinato/ncbi-mcp-server](https://github.com/vitorpavinato/ncbi-mcp-server)** — Comprehensive NCBI/PubMed literature search server with advanced analytics, caching, MeSH integration, related articles discovery, and batch processing for all life sciences and biomedical research
  <sub>★ 13 · Python · source · pushed 2025-06-28 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/vitorpavinato/ncbi-mcp-server.git`</sub>
- **[cameronrye/gopher-mcp](https://github.com/cameronrye/gopher-mcp)** — Modern, cross-platform MCP server enabling AI assistants to browse and interact with both Gopher protocol and Gemini protocol resources safely and efficiently. Features dual protocol support, TLS security, and structured content extraction
  <sub>★ 12 · Python · MIT · uv · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx gopher-mcp`</sub>
- **[emicklei/melrose-mcp](https://github.com/emicklei/melrose-mcp)** — Plays Melrōse music expressions as MIDI
  <sub>★ 12 · Go · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/emicklei/melrose-mcp.git`</sub>
- **[kshern/mcp-tavily](https://github.com/kshern/mcp-tavily.git)** — Tavily AI search API
  <sub>★ 12 · JavaScript · MIT · npx · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @kshern/mcp-tavily --client claude`</sub>
- **[Role1776/mcp-retrieval](https://github.com/Role1776/mcp-retrieval)** — Web search, image search, and page-to-Markdown scraping with no API keys: DuckDuckGo Lite for text, Bing Images for images, and a readability extractor for pages. Three read-only tools, stdio or streamable HTTP transport
  <sub>★ 12 · Go · MIT · go · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/Role1776/mcp-retrieval/app/cmd/mcp-retrieval@latest # needs Go 1.25.5+`</sub>
- **[HasData/web-scraping-mcp](https://github.com/HasData/web-scraping-mcp)** — Remote MCP server for web scraping: fetch any public page with optional JavaScript rendering, wait conditions and CSS or AI extraction rules, as markdown, text, HTML or JSON
  <sub>★ 11 · JavaScript · MIT · source · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/web-scraping-mcp.git`</sub>
- **[Crawleo/Crawleo-MCP](https://github.com/Crawleo/Crawleo-MCP)** — Crawleo Search &amp; Crawl API
  <sub>★ 11 · JavaScript · MIT · npm · pushed 2025-12-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g crawleo-mcp`</sub>
- **[serkan-ozal/driflyte-mcp-server](https://github.com/serkan-ozal/driflyte-mcp-server)** — The Driflyte MCP Server exposes tools that allow AI assistants to query and retrieve topic-specific knowledge from recursively crawled and indexed web pages
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2025-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @serkan-ozal/driflyte-mcp-server --client <SMITHERY-CLIENT-NAME> --key <SMITHERY-API-KEY>`</sub>
- **[whw23/searxng-http-mcp](https://github.com/whw23/searxng_http_mcp)** — Self-contained SearXNG MCP server in Docker. 200+ search engines, 30+ categories, multi-page fanout, autocomplete, and engine discovery. Dual transport (HTTP + stdio), API key auth, and built-in SearXNG Web UI reverse proxy. Zero-install deploy
  <sub>★ 11 · Python · MIT · uv · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx searxng-http-mcp`</sub>
- **[echology-io/decompose](https://github.com/echology-io/decompose)** — Decompose text into classified semantic units with authority, risk, attention scores, and entity extraction. No LLM. Deterministic. Works as MCP server or CLI
  <sub>★ 10 · Python · MIT · pip · pushed 2026-05-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install decompose-mcp`</sub>
- **[linxule/mineru-mcp](https://github.com/linxule/mineru-mcp)** — MCP server for MinerU document parsing API. Parse PDFs, images, DOCX, and PPTX with OCR (109 languages), batch processing (200 docs), page ranges, and local file upload. 73% token reduction with structured output
  <sub>★ 10 · TypeScript · MIT · bun · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bun add -g mineru-mcp`</sub>
- **[HasData/bing-mcp](https://github.com/HasData/bing-mcp)** — Remote MCP server for Bing search: organic results with the ad block and the Copilot answer, targeted by market, country, language and device, as JSON
  <sub>★ 9 · JavaScript · MIT · source · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/bing-mcp.git`</sub>
- **[HughesCuit/heventure-search-mcp](https://github.com/HughesCuit/heventure-search-mcp)** — Free MCP web search server with 5 engines (DuckDuckGo, Bing, Google SerpAPI, Tavily). No API key required. Auto rate limiting, 300s cache, multi-language support. Install: uvx heventure-search-mcp
  <sub>★ 9 · Python · pip · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install heventure-search-mcp`</sub>
- **[imprvhub/mcp-claude-hackernews](https://github.com/imprvhub/mcp-claude-hackernews)** — An integration that allows Claude Desktop to interact with Hacker News using the Model Context Protocol (MCP)
  <sub>★ 9 · TypeScript · MPL-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest mcp add imprvhub/mcp-claude-hackernews --client claude`</sub>
- **[Pearch-ai/mcp_pearch](https://github.com/Pearch-ai/mcp_pearch)** — Best people search engine that reduces the time spent on talent discovery
  <sub>★ 9 · Python · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pearch-ai/mcp_pearch.git`</sub>
- **[searchcraft-inc/searchcraft-mcp-server](https://github.com/searchcraft-inc/searchcraft-mcp-server)** — Official MCP server for managing Searchcraft clusters, creating a search index, generating an index dynamically given a data file and for easily importing data into a search index given a feed or local json file
  <sub>★ 9 · TypeScript · Apache-2.0 · source · pushed 2026-02-07 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/searchcraft-inc/searchcraft-mcp-server.git`</sub>
- **[shopsavvy/shopsavvy-mcp-server](https://github.com/shopsavvy/shopsavvy-mcp-server)** — Complete product and pricing data solution for AI assistants. Search for products by barcode/ASIN/URL, access detailed product metadata, access comprehensive pricing data from thousands of retailers, view and track price history, and more
  <sub>★ 9 · JavaScript · MIT · clone · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shopsavvy/shopsavvy-mcp-server`</sub>
- **[AutomateLab-tech/citation-intelligence](https://github.com/AutomateLab-tech/citation-intelligence)** — What LLMs cite, for agents. Check which URLs Perplexity, Claude, ChatGPT, Gemini, Bing, and Google AI Overviews cite for any query. Self-hosted, BYO API key. Install via npx @automatelab/citation-intelligence
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-06-08 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @automatelab/citation-intelligence`</sub>
- **[boikot-xyz/boikot](https://github.com/boikot-xyz/boikot)** — Model Context Protocol Server for looking up company ethics information. Learn about the ethical and unethical actions of major companies
  <sub>★ 8 · HTML · GPL-3.0 · source · pushed 2026-09-26</sub>
  <sub>`git clone https://github.com/boikot-xyz/boikot.git`</sub>
- **[scavio-ai/scavio-mcp](https://github.com/scavio-ai/scavio-mcp)** — Unified real-time search API for AI agents. Google, YouTube, Amazon, Walmart, Reddit, and TikTok through one endpoint. 21 tools for web search, e-commerce, product data, social media, and video platforms. Free tier included
  <sub>★ 7 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scavio-ai/scavio-mcp.git`</sub>
- **[mikusnuz/gsc-mcp](https://github.com/mikusnuz/gsc-mcp)** — MCP server for Google Search Console &amp; Indexing API — 13 tools for search analytics, sitemaps, URL inspection, and batch indexing
  <sub>★ 7 · TypeScript · MIT · source · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mikusnuz/gsc-mcp.git`</sub>
- **[JerryLiu369/agent-web-search](https://github.com/JerryLiu369/agent-web-search)** — Agent-native web search for AI agents: one provider-neutral web_search tool aggregating model-native grounding (ARK, Gemini, Grok, DeepSeek, Zhipu) and agent search APIs (Exa, Parallel, Brave, Perplexity, Tavily, You.com). Keyless free defaults, stdio + stateless Streamable-HTTP MCP, CLI, Python API, and Hermes plugin. Install via pipx install agent-web-search-mcp
  <sub>★ 6 · Python · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add JerryLiu369/agent-web-search --skill agent-web-search`</sub>
- **[Bigsy/Clojars-MCP-Server](https://github.com/Bigsy/Clojars-MCP-Server)** — Clojars MCP Server for upto date dependency information of Clojure libraries
  <sub>★ 6 · JavaScript · MIT · npm · pushed 2025-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g clojars-deps-server`</sub>
- **[HasData/hasdata-mcp](https://github.com/HasData/hasdata-mcp)** — Remote MCP server providing structured data APIs for Google (Search, Maps, Trends, Flights), Amazon, Airbnb, Zillow, Yelp, and more. 40+ tools returns clean JSON data instead of browser automation or raw HTML scraping. Designed for AI agents requiring reliable hosted data access
  <sub>★ 6 · JavaScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/hasdata-mcp.git`</sub>
- **[keenableai/keenable-mcp](https://github.com/keenableai/keenable-mcp)** — Live web search and clean-markdown page fetch over the Keenable web index. Two tools: search_web_pages, fetch_page_content. Keyless by default (1,000 req/hour); an optional API key lifts the cap. Hosted Streamable HTTP at https://api.keenable.ai/mcp, or run npx -y @keenable/mcp
  <sub>★ 6 · JavaScript · MIT · source · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/keenableai/keenable-mcp.git`</sub>
- **[shariqriazz/google-ai-search-mcp](https://github.com/shariqriazz/google-ai-search-mcp)** — Google AI-powered search, documentation retrieval, code analysis, and architecture research tools using Vertex AI or the Gemini API. Install with npx -y google-ai-search-mcp
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`bunx google-ai-search-mcp`</sub>
- **[Vincentwei1021/agent-toolbox](https://github.com/Vincentwei1021/agent-toolbox)** — Production-ready MCP server providing 13 tools for AI agents: web search, content extraction, screenshots, weather, finance, email validation, translation, news, GeoIP, WHOIS, DNS, PDF extraction, and QR code generation. 1,000 free calls/month, no setup required
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g agent-toolbox-mcp`</sub>
- **[zlatkoc/youtube-summarize](https://github.com/zlatkoc/youtube-summarize)** — MCP server that fetches YouTube video transcripts and optionally summarizes them. Supports multiple transcript formats (text, JSON, SRT, WebVTT), multi-language retrieval, and flexible YouTube URL parsing
  <sub>★ 6 · Python · MIT · uv · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx youtube-summarize`</sub>
- **[AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl)** — Crawl websites into clean Markdown, search pages, and extract structured data with LLMs. Built-in MCP server for web research and RAG pipelines
  <sub>★ 5 · Python · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx clawhub install markcrawl-skill`</sub>
- **[Khamel83/argus](https://github.com/Khamel83/argus)** — Multi-provider search broker with automatic fallback, RRF ranking, content extraction, and budget enforcement
  <sub>★ 5 · Python · MIT · pipx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install argus-search[mcp]`</sub>
- **[AntonG87/codearia-sieve](https://github.com/AntonG87/codearia-sieve)** — Turns a web page into decision-ready state for agents: dates as ISO fields, numbers with units as facts, token-budgeted chunks with anchors back to the page, and the token bill (median 53,718 → 1,106). Deterministic, no model or API key; pairs with decision models such as Jev. npx -y codearia-sieve
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx codearia-sieve # MCP server for Claude Code, Cursor and any agent`</sub>
- **[kc23go/anybrowse](https://github.com/kc23go/anybrowse)** — Convert any URL to LLM-ready Markdown via real Chrome browsers. 3 tools: scrape, crawl, search. Free via MCP, pay-per-use via x402. Remote MCP endpoint: https://anybrowse.dev/mcp
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kc23go/anybrowse.git`</sub>
- **[lulzasaur9192/marketplace-search-mcp](https://github.com/lulzasaur9192/marketplace-search-mcp)** — Search marketplaces (TCGPlayer, Reverb, Thumbtack), verify professional licenses (contractor, nurse across US states), and look up PSA card grading population data
  <sub>★ 5 · TypeScript · npx · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @lulzasaur9192/marketplace-search-mcp`</sub>
- **[nyxn-ai/NyxDocs](https://github.com/nyxn-ai/NyxDocs)** — Specialized MCP server for cryptocurrency project documentation management with multi-blockchain support (Ethereum, BSC, Polygon, Solana)
  <sub>★ 5 · Python · MIT · clone · pushed 2025-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nyxn-ai/NyxDocs.git`</sub>
- **[qune-tech/ocds-mcp](https://github.com/qune-tech/vergabe-mcp)** — German public procurement data (OCDS) — semantic search, tender matching with company profiles, and structured filtering
  <sub>★ 5 · Rust · MIT · npx · pushed 2026-07-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @qune-tech/vergabe-mcp --api-key sk_live_YOUR_KEY_HERE`</sub>
- **[scraperapi/scraperapi-mcp](https://github.com/scraperapi/scraperapi-mcp)** — MCP server for ScraperAPI web scraping with JavaScript rendering, geotargeting, premium proxies, and auto-parsing support
  <sub>★ 5 · Python · MIT · pip · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install scraperapi-mcp-server`</sub>
- **[talonicdev/talonic-mcp](https://github.com/talonicdev/talonic-mcp)** — Schema-validated document extraction with searchable workspace memory. Extract structured fields from PDFs, scans, images, and forms; AI agents can also search, filter, and query past extractions
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @talonic/mcp@latest --version`</sub>
- **[robbyczgw-cla/web-search-plus-mcp](https://github.com/robbyczgw-cla/web-search-plus-mcp)** — Multi-provider web search with intelligent auto-routing (Serper, Tavily, Exa). Available via uvx web-search-plus-mcp
  <sub>★ 5 · Python · MIT · uv · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx web-search-plus-mcp`</sub>
- **[mrslbt/rippr](https://github.com/mrslbt/rippr)** — YouTube transcript extraction for AI agents. Clean text, timestamps, or structured JSON from any video. No API keys required. Install via npx rippr-mcp
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rippr-mcp`</sub>
- **[hanselhansel/aeo-cli](https://github.com/hanselhansel/context-cli)** — Audit URLs for AI crawler readiness — checks robots.txt, llms.txt, JSON-LD schema, and content density with 0-100 AEO scoring
  <sub>★ 4 · Python · MIT · gh-action · pushed 2026-03-17</sub>
  <sub>`uses: hanselhansel/aeo-cli@main # in .github/workflows/*.yml`</sub>
- **[fouradata/mcp](https://github.com/fouradata/mcp)** — Web scraping for AI agents: one auto tool walks a cost-aware ladder (direct → rotating proxy → full browser), solving anti-bot challenges and reporting which rung delivered and what it cost. Pay-per-success, EU-hosted, free tier
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @fouradata/mcp`</sub>
- **[goofrey/zoom-search](https://github.com/goofrey/zoom-search)** — MCP search and evidence tool for AI agents. Rewrites queries, zooms into source domains, and returns sourced answers with metrics
  <sub>★ 4 · Python · MIT · pip · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zoom-search`</sub>
- **[lionkiii/rss-feeds-mcp](https://github.com/lionkiii/rss-feeds-mcp)** — RSS feeds MCP server with 8 tools — fetch, filter, search, and manage RSS feeds by category or source. Zero config, no API keys required
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lionkiii/rss-feeds-mcp.git`</sub>
- **[kimdonghwi94/Web-Analyzer-MCP](https://github.com/kimdonghwi94/web-analyzer-mcp)** — Extracts clean web content for RAG and provides Q&amp;A about web pages
  <sub>★ 4 · Python · MIT · npx · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @kimdonghwi94/web-analyzer-mcp --client claude`</sub>
- **[atlasprzetargow/mcp-server](https://github.com/atlasprzetargow/mcp-server)** — Search 800 000+ Polish public tenders (BZP + TED). Profiles of procuring entities and contractors by NIP, market statistics by CPV/province, 90+ term procurement glossary
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @atlasprzetargow/mcp`</sub>
- **[chasesaurabh/mcp-page-capture](https://github.com/chasesaurabh/mcp-page-capture)** — MCP server that captures webpage screenshots, with viewport or full-page options and base64 PNG output
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2025-12-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-page-capture`</sub>
- **[comparedge/mcp-server-comparedge](https://github.com/comparedge/mcp-server-comparedge)** — Verified SaaS, AI, and LLM pricing for 490+ tools: plans, hidden costs, alternatives, and comparisons. Free, no API key
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/comparedge/mcp-server-comparedge.git`</sub>
- **[gregm711/agent-domain-service-mcp](https://github.com/gregm711/agent-domain-service-mcp)** — AI-powered domain brainstorming, analysis, and availability checking via AgentDomainService.com. Generate creative domain names from descriptions, get AI scoring for brandability/memorability, and check real-time availability with pricing. No API keys required
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2025-12-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-domain-service-mcp`</sub>
- **[JessieJanie/skim402](https://github.com/JessieJanie/skim402)** — Convert any URL into clean, agent-ready Markdown with structured metadata (title, byline, published date, language). Pay-per-use via x402 (USDC on Base) — no signup, no API keys. Single tool read_url. Install via npx -y skim-mcp
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JessieJanie/skim402.git`</sub>
- **[maxylev/searchfetch](https://github.com/maxylev/searchfetch)** — A fault-tolerant, stealth-enabled Model Context Protocol (MCP) server for web searching and content fetching
  <sub>★ 3 · Python · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y searchfetch`</sub>
- **[paulieb89/govuk-mcp](https://github.com/paulieb89/govuk-mcp)** — Search GOV.UK content, retrieve full government pages, look up organisations, and resolve UK postcodes to local authorities. 5 read-only tools, no API keys required
  <sub>★ 3 · Python · MIT · source · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/paulieb89/govuk-mcp.git`</sub>
- **[Prototypr/feedbagel-mcp](https://github.com/Prototypr/feedbagel-mcp)** — Search the Feedbagel RSS catalog, follow feeds, and route new entries to webhooks
  <sub>★ 3 · TypeScript · npm · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g feedbagel-mcp`</sub>
- **[urlbox/urlbox-mcp-server](https://github.com/urlbox/urlbox-mcp-server/)** — A reliable MCP server for generating and managing screenshots, PDFs, and videos, performing AI-powered screenshot analysis, and extracting web content (Markdown, metadata, and HTML) via the Urlbox API
  <sub>★ 3 · TypeScript · MIT · source · pushed 2025-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/urlbox/urlbox-mcp-server/.git`</sub>
- **[ashlrai/webfetch](https://github.com/ashlrai/webfetch)** — License-first federated image search across 25 providers. Returns open/platform/editorial license tags, attribution strings, dimensions, and download-ready URLs via npx -y getwebfetch-mcp
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g getwebfetch`</sub>
- **[usestring/string-ai-mcp](https://github.com/usestring/string-ai-mcp)** — Search the web, fetch any URL and map a site — clean Markdown, past anti-bot blocks. Install via npx -y @usestring/mcp, or use the hosted endpoint at https://mcp.usestring.ai/v1/mcp
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @usestring/mcp`</sub>
- **[Alisammour/storyflo-mcp](https://github.com/Alisammour/storyflo-mcp)** — Curated audio-news with a market-aware news signal. Search articles, fetch narrated audio, subscribe topic feeds, surface stories matched to actively traded Kalshi event contracts (CFTC-regulated; qualitative signal tags + link-out to Kalshi, never raw market data). 8 tools (7 free + 1 x402-paid over USDC on Base). Install via npx -y storyflo-mcp
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-07-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx storyflo-mcp # or: node src/index.js`</sub>
- **[denyn1/aifeed-protocol](https://github.com/denyn1/aifeed-protocol)** — MCP server (packages/aifeed-mcp-server) for the AIFeed protocol: verify signed publisher manifests (Ed25519 + DNS _aifeed anchor), fetch token-budgeted AIFeed Markdown or MAKO pages, verify declared asset downloads, and rank delta-index entries. Install via npx -y aifeed-mcp-server
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx aifeed keygen --out .aifeed # Ed25519 key pair`</sub>
- **[lucasmartins-ai/lookacrawler](https://github.com/lucasmartins-ai/lookacrawler)** — Free, open-source, token-efficient local alternative to Firecrawl with native MCP Server for LLMs (>73% token reduction, Playwright stealth anti-bot bypass)
  <sub>★ 2 · TypeScript · MIT · docker · pushed 2026-09-04 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 lookacrawler`</sub>
- **[idapixl/idapixl-web-research-mcp](https://github.com/idapixl/idapixl-web-research-mcp)** — Pay-per-use web research for AI agents on Apify. Search (Brave + DuckDuckGo), fetch pages to clean markdown, and multi-step research with relevance scoring and key fact extraction
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/idapixl/idapixl-web-research-mcp.git`</sub>
- **[BenyD/haypile](https://github.com/BenyD/haypile)** — Hybrid semantic and keyword search over local documents (PDF, docx, pptx, markdown, HTML) with file and page citations. Single binary with the embedding model inside; the index never leaves the machine
  <sub>★ 2 · Go · AGPL-3.0 · psh · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://haypile.sh/install.ps1 | iex`</sub>
- **[capad-xyz/searchts](https://github.com/capad-xyz/searchts)** — Keyless web access for AI agents: an escalating open-source unlocker (browser-fingerprint fetch → JS-render relay → stealth browser) reads bot-walled pages as clean Markdown, plus multi-provider web search with rank fusion, subtitles-first video transcripts, and page asset grabbing. No API keys; ships a reproducible benchmark
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from "searchts[mcp]" searchts <verb>`</sub>
- **[dariomory/trendflow-js](https://github.com/dariomory/trendflow-js)** — Google Trends over MCP — interest over time, interest by region, trending now, related queries and topic search. Runs locally via npx or against a hosted endpoint
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:dariomory/trendflow-js.git`</sub>
- **[dealx/mcp-server](https://github.com/DealExpress/mcp-server)** — MCP Server for DealX platform
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @dealx/mcp-server`</sub>
- **[divyanshu-iitian/SearchForge](https://github.com/divyanshu-iitian/SearchForge)** — Free capability-routed search and web reading for agents: GitHub, Crossref, Hacker News, Wikipedia, private SearXNG, and URL-to-Markdown, with live health diagnostics and no telemetry. Exposes web_search, read_url, and search_status
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx --yes --package github:divyanshu-iitian/SearchForge \`</sub>
- **[ekas-io/open-sales-stack](https://github.com/ekas-io/open-sales-stack)** — Collection of B2B sales intelligence MCP servers. Includes website analysis, tech stack detection, hiring signals, review aggregation, ad tracking, social profiles, financial reporting and more for AI-powered prospecting by Ekas
  <sub>★ 2 · Python · MIT · clone · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ekas-io/open-sales-stack.git`</sub>
- **[echojobsio/jdl-mcp-server](https://github.com/echojobsio/jdl-mcp-server)** — Search 1M+ enriched job listings from 20,000+ companies. Filter by skills, salary, location, seniority, remote type, and more. Free — 500 calls/day, no signup required. Also available as a remote MCP server at https://mcp.jobdatalake.com
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/echojobsio/jdl-mcp-server.git`</sub>
- **[getrephonic/rephonic-mcp](https://github.com/getrephonic/rephonic-mcp)** — Search 3M+ podcasts and 170M+ episodes, with listener estimates, audience demographics, contacts, transcripts, chart rankings, sponsors, reviews, and audience-overlap data. Hosted by Rephonic
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/getrephonic/rephonic-mcp.git`</sub>
- **[hanoak/unsplash-mcp-server](https://github.com/hanoak/unsplash-mcp-server)** — Unsplash API server exposing 21 tools across photos, search, users, collections, topics, and stats. Ships Unsplash-guideline compliance built in — ready-to-use attribution with UTM parameters, a download-tracking tool, rate-limit surfacing, and content_filter=high by default. Install via npx -y @hanoak/unsplash-mcp-server
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @hanoak/unsplash-mcp-server login`</sub>
- **[mambalabsdev/mcp-domain-to-linkedin-url-resolver](https://github.com/mambalabsdev/mcp-domain-to-linkedin-url-resolver)** — Resolves a company domain or name to its LinkedIn company URL with confidence scoring and firmographic metadata
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-domain-to-linkedin-url-resolver.git`</sub>
- **[omniologynow-rgb/scout-intel-mcp](https://github.com/omniologynow-rgb/scout-intel-mcp)** — Web intelligence MCP server for AI agents. 7 tools for SERP analysis, competitor research, market trends, content gap analysis, keyword insights, audience discovery, and citation tracking. Install via pip install scout-intel-mcp
  <sub>★ 2 · Python · AGPL-3.0 · pip · pushed 2026-05-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install scout-mcp`</sub>
- **[QuentinCody/catalysishub-mcp-server](https://github.com/QuentinCody/catalysishub-mcp-server)** — Unofficial MCP server for searching and retrieving scientific data from the Catalysis Hub database, providing access to computational catalysis research and surface reaction data
  <sub>★ 2 · Python · source · pushed 2025-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/QuentinCody/catalysishub-mcp-server.git`</sub>
- **[securecoders/opengraph-io-mcp](https://github.com/securecoders/opengraph-io-mcp)** — OpenGraph.io API integration for extracting OG metadata, taking screenshots, scraping web content, querying sites with AI, and generating branded images (illustrations, diagrams, social cards, icons, QR codes) with iterative refinement
  <sub>★ 2 · TypeScript · ISC · npm · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g opengraph-io-mcp`</sub>
- **[Savirinc/unfragile-mcp-server](https://github.com/Savirinc/unfragile-mcp-server)** — Canonical MCP server resolver. Returns the right MCP for any agent intent with an invocation-ready snippet and an Ed25519-signed trust passport. Cross-registry coverage. npx -y @unfragile/mcp-server
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Savirinc/unfragile-mcp-server.git`</sub>
- **[Gaoshan0971/digeguigui](https://github.com/Gaoshan0971/digeguigui)** — Global reptile &amp; exotic pet knowledge base. 633 species, AI identification, genetics calculator, 12-dimension care, health diagnosis, pricing, and blockchain provenance. Free tier: 9 tools, 10 req/min. MCP: https://api.digeguigui.com/mcp
  <sub>★ 2 · Python · MIT · source · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Gaoshan0971/digeguigui.git`</sub>
- **[yubinkim444/ai-first-scraper-mcp](https://github.com/yubinkim444/ai-first-scraper-mcp)** — Three MCP tools for ad-free Markdown web scraping and search. fetch_page (URL → clean Markdown), fetch_pages_batch (up to 25 URLs in parallel), search_web (web search → top-k pages as Markdown). Works with Claude Desktop / Cursor / Cline. Install: uvx ai-first-scraper-mcp
  <sub>★ 2 · Python · MIT · pip · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ai-first-scraper-mcp`</sub>
- **[Newscatcher/catchall-mcp](https://github.com/Newscatcher/catchall-mcp)** — Recall-first web search: finds every relevant event across the open web, not just the top results
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Newscatcher/catchall-mcp.git`</sub>
- **[pgalyen1987/gate402-mcp](https://github.com/pgalyen1987/gate402-mcp)** — Pay-per-call agent APIs over x402 (USDC on Base): per-token LLM inference (Llama 3.1/Qwen/Mistral), per-second GPU/CPU compute, on-chain/DeFi + SEC-EDGAR + news data, and clean-Markdown/Cloudflare-stealth web scraping. Signed receipts, no signup — auto-claims a free-tier key. Install via npx -y gate402-mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g gate402-mcp`</sub>
- **[newsagentdata/newsagent-mcp](https://github.com/newsagentdata/newsagent-mcp)** — Real-time, ML-enriched news intelligence — urgency scoring, political lean &amp; event clustering across 190+ countries
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/newsagentdata/newsagent-mcp.git`</sub>
- **[qinisolabs/icdwise](https://github.com/qinisolabs/icdwise)** — Verified ICD-10-CM medical code lookup, validation &amp; reverse search — official descriptions, never guessed
  <sub>★ 1 · TypeScript · Apache-2.0 · source · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/qinisolabs/icdwise.git`</sub>
- **[AIweather-Anurag/ottasia-mcp-server](https://github.com/AIweather-Anurag/ottasia-mcp-server)** — Where to watch any movie or TV show across 30 Asian and Middle Eastern streaming markets (Netflix, Disney+ Hotstar, Wavve, Shahid, Hoichoi, ZEE5, JioCinema, and 17 more). npx -y @ottasia/mcp-server
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AIweather-Anurag/ottasia-mcp-server.git`</sub>
- **[AceDataCloud/MCPSerp](https://github.com/AceDataCloud/SerpMCP)** — Google SERP search including web, images, news, maps, places, videos, and knowledge graph results via Ace Data Cloud API
  <sub>★ 1 · Python · MIT · docker · pushed 2026-08-28 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-serp:latest`</sub>
- **[AllNewsAPI/mcp-server](https://github.com/AllNewsAPI/mcp-server)** — Get access to real-time and historical news data including top headlines from global sources via AllNewsAPI
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx allnewsapi-mcp@latest --apikey YOUR_API_KEY_HERE`</sub>
- **[bumbaRasch/searxng-mcp-server](https://github.com/bumbaRasch/searxng-mcp-server)** — Self-hosted SearXNG metasearch for MCP clients: web, image, news, video and music search plus page fetch. No API keys, no tracking; SSRF-guarded fetch with prompt-injection wrapping
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector npx -y searxng-mcp-server`</sub>
- **[CKBrennan/overtone-news-mcp](https://github.com/CKBrennan/overtone-news-mcp)** — Real-time news with tone analysis, brand safety, and narrative shift signals for AI agents
  <sub>★ 1 · Python · MIT · clone · pushed 2026-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CKBrennan/overtone-news-mcp`</sub>
- **[Crawlora-org/crawlora-mcp](https://github.com/Crawlora-org/crawlora-mcp)** — Hosted MCP for structured public web data — 319 tools across search, maps, commerce, social, and finance, each returning clean JSON. Free 2,000 credits/mo
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-26 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Crawlora-org/crawlora-mcp.git`</sub>
- **[deficlow/HyperStore-MCP](https://github.com/deficlow/HyperStore-MCP)** — Search 6,500+ curated AI applications from the HyperStore directory. 8 tools (keyword + semantic search, full details, browsing), 3 resources, 3 prompts. Install via uvx hyperstore-mcp or use the hosted endpoint at https://mcp.store.hypergpt.ai/mcp
  <sub>★ 1 · Python · MIT · npx · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx hyperstore-mcp`</sub>
- **[pepabo/muumuu-domain-mcp](https://github.com/pepabo/muumuu-domain-mcp)** — Official remote MCP server for Muumuu Domain (GMO Pepabo). Search and register domains, manage owned domains and contracts, and configure DNS records via natural language
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pepabo/muumuu-domain-mcp.git`</sub>
- **[VoxellInc/forge-mcp](https://github.com/VoxellInc/forge-mcp)** — Official MCP server for Forge, Voxell's hosted text-embedding API. Generate vector embeddings (turbo 1024d, pro 2560d, ultra 4096d; Matryoshka truncation) for semantic search and RAG. npx -y @voxell/forge-mcp
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/VoxellInc/forge-mcp.git`</sub>
- **[giskard09/giskard-search](https://github.com/giskard09/giskard-search)** — Pay-per-use semantic web search for AI agents. Powered by SearxNG, agents pay in sats via Lightning Network micropayments — no API keys required. Self-hosted with phoenixd
  <sub>★ 1 · Python · Apache-2.0 · pip · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mcp httpx duckduckgo-search python-dotenv fastapi uvicorn web3 x402`</sub>
- **[ip2whois/mcp-ip2whois](https://github.com/ip2whois/mcp-ip2whois)** — MCP server that provides comprehensive WHOIS lookup capabilities using the IP2WHOIS API. This server allows AI agents to query domain registration details, including expiry dates, registrar information, and registrant data
  <sub>★ 1 · Python · MIT · source · pushed 2026-05-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ip2whois/mcp-ip2whois.git`</sub>
- **[leadbrain/korean-data-mcp](https://github.com/leadbrain/korean-data-mcp)** — Real-time Korean web data — Naver place reviews, Melon music chart, Daangn/Bunjang marketplace listings, Naver news, Musinsa fashion rankings. 7 tools powered by Apify actors. Requires APIFY_TOKEN
  <sub>★ 1 · Python · MIT · pip · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install korean-data-mcp`</sub>
- **[mambalabsdev/mcp-company-firmographic-enricher](https://github.com/mambalabsdev/mcp-company-firmographic-enricher)** — Enriches a company domain into firmographics: employee band, industry, HQ, founded year, revenue estimate, logo, and description, with source provenance
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-firmographic-enricher.git`</sub>
- **[mambalabsdev/mcp-gtm-hiring-signal-scraper](https://github.com/mambalabsdev/mcp-gtm-hiring-signal-scraper)** — Detects GTM hiring signals across Greenhouse, Lever, and Ashby career pages, returning Clay-ready JSON with role counts, signal strength, and ATS detection
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-gtm-hiring-signal-scraper.git`</sub>
- **[mambalabsdev/mcp-gtm-tech-stack-signal-scraper](https://github.com/mambalabsdev/mcp-gtm-tech-stack-signal-scraper)** — Detects CRM, sequencer, and marketing automation tools from a company domain, returning flat boolean GTM tool signals for Clay enrichment
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-gtm-tech-stack-signal-scraper.git`</sub>
- **[Marvy101/pod-mcp](https://github.com/Marvy101/pod-mcp)** — Search firsthand observations that agents recorded while doing real work — what actually happened with a product, API, service, or place, rather than what its documentation claims. Agents can also write back what they observed. No API key; hosted Streamable HTTP at https://api.askpod.ai/mcp/read
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Marvy101/pod-mcp.git`</sub>
- **[MKirovBG/scribefy-mcp](https://github.com/MKirovBG/scribefy-mcp)** — Extract timestamped YouTube transcripts, plus search, video metadata, and related-video tools for Claude, Cursor, Windsurf, and AI agents
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y scribefy-mcp`</sub>
- **[Opedd/opedd-mcp](https://github.com/Opedd/opedd-mcp)** — Licensed, rights-cleared content for AI agents — discover, purchase, verify, and retrieve expert analysis with a verifiable license key per article, on-chain proof, and EU AI Act Article 53 attestation. The alternative to unlicensed scraping for RAG and AI search. npx opedd-mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g opedd-mcp`</sub>
- **[ni-c/freshrss-mcp](https://github.com/ni-c/freshrss-mcp)** — Read and manage a self-hosted FreshRSS instance through its Google Reader API: feeds, categories and labels, articles as plain text, read/star state, OPML import and export. Destructive tools require a server-issued confirmation token
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/freshrss-mcp.git`</sub>
- **[peter-j-thompson/semanticapi-mcp](https://github.com/peter-j-thompson/semanticapi-mcp)** — Natural language API discovery — search 700+ API capabilities, get endpoints, auth setup, and code snippets. Supports auto-discovery of new APIs
  <sub>★ 1 · Python · uv · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx semanticapi-mcp`</sub>
- **[rubenayla/partle-mcp](https://github.com/rubenayla/partle-mcp)** — Search products and stores in nearby physical stores. Find what you need locally instead of waiting for delivery. Remote MCP server (Streamable HTTP, no API key required)
  <sub>★ 1 · Python · Apache-2.0 · uv · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx partle-mcp`</sub>
- **[bartonguestier1725-collab/scout-mcp](https://github.com/bartonguestier1725-collab/scout-mcp)** — Multi-source search across code registries (GitHub, npm, PyPI), academic indexes (arXiv, Semantic Scholar), social platforms (HN, Reddit, X), and community blogs (Dev.to, Hashnode, Qiita, Zenn). Parallel fetch with structured JSON output. npx -y scout-cli
  <sub>★ 1 · TypeScript · MIT · docker · pushed 2026-05-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i scout-mcp`</sub>
- **[chefcohen/corroborate-mcp](https://github.com/chefcohen/corroborate-mcp)** — Tells AI agents how independently a claim is being reported: syndication-aware source counting (a wire story reprinted by 40 outlets counts as one origin), 0-1 confidence scores, and published error rates in-repo. Measures corroboration, not truth — no stance detection. Keyless, no accounts. Install: npx -y corroborate-mcp
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx corroborate-mcp # starts the stdio server (silent = healthy)`</sub>
- **[scrapercity/scrapercity-cli](https://github.com/scrapercity/scrapercity-cli)** — B2B lead generation with 20+ tools including Apollo, Google Maps, email finder, email validator, mobile finder, skip trace, and ecommerce store data
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx scrapercity login # enter your API key`</sub>
- **[ssatama/rescuedogs-mcp-server](https://github.com/ssatama/rescuedogs-mcp-server)** — Search and discover rescue dogs from European and UK organizations with AI-powered personality matching and detailed profiles
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g rescuedogs-mcp-server`</sub>
- **[theagenttimes/tat-mcp-server](https://github.com/theagenttimes/tat-mcp-server)** — Query articles, verified statistics, wire feed, and social tools from The Agent Times, the AI-native newspaper covering the agent economy. 13 tools including search, comments, citations, and agent leaderboards. No API key required
  <sub>★ 1 · Python · clone · pushed 2026-02-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/levfilimonov/tat-mcp-server.git`</sub>
- **[AI-Directory-Partners/tooldirectory-mcp](https://github.com/AI-Directory-Partners/tooldirectory-mcp)** — Search a catalog of 2,000+ AI tools, compare them, find alternatives, and check whether a tool is still active, defunct, or acquired. Hosted remote MCP at https://tooldirectory.ai/api/mcp or npx -y tooldirectory-mcp
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y tooldirectory-mcp`</sub>
- **[juergenkoller-software/pdf-content-search-mcp](https://github.com/juergenkoller-software/pdf-content-search-mcp)** — MCP bridge for PDF Content Search — full-text PDF search with Apple Vision OCR across thousands of documents in under a second. Advanced filters (date, category, sender, amount), wildcards, boolean operators
  <sub>★ 1 · Swift · MIT · clone · pushed 2026-06-08 · macOS · Linux</sub>
  <sub>`git clone https://github.com/juergenkoller-software/pdf-content-search-mcp.git`</sub>
- **[Grubbomatic/crawl-readiness-mcp](https://github.com/Grubbomatic/crawl-readiness-mcp)** — AI SEO audit and fix tools: score any site 0-100 against 50+ AI crawlers (ChatGPT, Claude, Perplexity, Google AI), validate JSON-LD and robots.txt, compare human vs AI-crawler views, and generate llms.txt, robots.txt, and JSON-LD schema. Install via npx -y crawl-readiness-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y crawl-readiness-mcp`</sub>
- **[ToolTrace-io/mcp-server](https://github.com/ToolTrace-io/mcp-server)** — Web page data for agents: scrape to Markdown, extract metadata, links and JSON-LD schema, audit on-page SEO, detect tech stacks, and validate XML sitemaps. Free tier, no card. Install via npx -y @tooltrace/mcp-server, or use the hosted endpoint at https://mcp.tooltrace.io/mcp
  <sub>TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @tooltrace/mcp-server`</sub>
- **[artemchuikin/youtube-mcp](https://github.com/artemchuikin/youtube-mcp)** — YouTube transcripts in five formats (text, JSON, SRT, VTT, srv3), video and channel search, playlists, and 4,000-video batch jobs over a hosted endpoint. 14 tools, free tier, no card
  <sub>MIT · clone · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/artemchuikin/youtube-mcp`</sub>
- **[jlucasmcrell/apify-scrapers](https://github.com/jlucasmcrell/apify-scrapers)** — Model Context Protocol server exposing verified public data scrapers and lead extractors for Google Maps, Glassdoor, SEC EDGAR, and state contractor registries. Run locally via Python stdio
  <sub>Python · MIT · uv · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx apify-data-scrapers`</sub>
- **[AgenticAdvertising/topalternativesto-mcp](https://github.com/AgenticAdvertising/topalternativesto-mcp)** — Verified software comparisons: pricing read from each vendor's own page with its source URL and the date it was checked, plus ranked alternatives for any tool
  <sub>JavaScript · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx topalternativesto-mcp`</sub>
- **[igorsaevets/page2ai-mcp](https://github.com/igorsaevets/page2ai-mcp)** — Convert any web page URL into clean Markdown for LLM context. Runs entirely on your machine with no external API calls and no API key. Preserves tables, code blocks and heading structure. Install via npx -y @page2ai/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y page2ai-mcp`</sub>
- **[quantumproxies/quantumproxies-mcp](https://github.com/quantumproxies/quantumproxies-mcp)** — Live web access through residential proxies: scrape any page to clean Markdown, structured SERP search on three engines, site map and crawl, and 74 ready-made collectors. Also returns ready-to-use proxy endpoints — residential, mobile, datacenter, ISP, IPv6 — from your plans. Billed per delivered result
  <sub>TypeScript · MIT · source · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/quantumproxies/quantumproxies-mcp.git`</sub>
- **[rozetyp/grounder-mcp](https://github.com/rozetyp/grounder-mcp)** — Live web grounding for local and cloud LLMs: web_search, fetch, deep_search (a token-capped, cited evidence pack sized to a small context window), and research (an agentic search-and-read loop). Flat monthly pricing, no query content stored, free tier. Install via uvx grounder-mcp
  <sub>Python · MIT · uv · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx grounder-mcp # or: pip install grounder-mcp`</sub>
- **[adjacentai/necl-hn-mcp](https://github.com/adjacentai/necl-hn-mcp)** — Hacker News tools for AI agents: top stories by time window, category feeds (top/new/best/ask/show/job), comment threads, and full-text search via Algolia. No API key required
  <sub>Python · MIT · pip · pushed 2026-06-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install git+https://github.com/adjacentai/necl-hn-mcp.git`</sub>
- **[einiba/canyougrab-api](https://github.com/einiba/canyougrab-api/tree/main/mcp-server)** — Confidence-scored domain availability checking with real-time DNS + WHOIS lookups. Bulk check up to 100 domains per request. Each result includes availability, confidence level, data source, and registration details
  <sub>Python · MIT · in-repo · pushed 2026-05-24</sub>
  <sub>`git clone https://github.com/einiba/canyougrab-api.git && cd canyougrab-api/mcp-server`</sub>
- **[eliottreich/crawdar-mcp](https://github.com/eliottreich/crawdar-mcp)** — Official hosted MCP server with an open-source stdio bridge for evidence-backed business discovery and lead-list research. Search by plain-language brief or structured criteria, inspect qualification evidence and exclusions, and use resumable jobs with cursor paging and export support
  <sub>JavaScript · MIT · docker · pushed 2026-09-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i crawdar-mcp`</sub>
- **[devflowinc/trieve](https://github.com/devflowinc/trieve/tree/main/clients/mcp-server)** — Crawl, embed, chunk, search, and retrieve information from datasets through Trieve
  <sub>Rust · MIT · in-repo · pushed 2026-01-25</sub>
  <sub>`git clone https://github.com/devflowinc/trieve.git && cd trieve/clients/mcp-server`</sub>
- **[djrobson5/agentmd-mcp](https://github.com/djrobson5/agentmd-mcp)** — Convert PDF, DOCX, HTML, and URLs to clean, LLM-ready markdown with tables preserved and boilerplate stripped. Hosted API — no local dependencies. 50 free conversions (self-serve key, no card), then $0.002/call. Install via npx -y agentmd-mcp
  <sub>JavaScript · MIT · docker · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e AGENTMD_API_KEY=<your-key> agentmd-mcp`</sub>
- **[evanatpizzarobot/vr-org-mcp](https://github.com/evanatpizzarobot/vr-org-mcp)** — Live VR / AR / XR news, full-text VR.org originals, events calendar, headset deals and comparisons
  <sub>TypeScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vr-org-mcp`</sub>
- **[FieldmodeLLC/scrapecheck-mcp](https://github.com/FieldmodeLLC/scrapecheck-mcp)** — Verify scraped data against the live source page: send a URL, the scraped field values, and what was asked, and get back an ed25519-signed verdict (pass, fail, or unverifiable). A claim is never certified unless the re-fetched page contains it, and anything unconfirmed is unverifiable, never pass; signatures verify offline against a published key. Pay-per-call x402 (USDC on Base) — $0.01 full veri
  <sub>TypeScript · MIT · source · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FieldmodeLLC/scrapecheck-mcp.git`</sub>
- **[foundrole/jobs-mcp-proxy](https://github.com/foundrole/jobs-mcp-proxy)** — Open-source stdio bridge to FoundRole's hosted job search: live listings pulled from company ATS pages with salary benchmarks, H-1B sponsorship history, E-Verify status, and ghost-job trust grades, plus a resume ATS-parsing check and a Kanban application tracker with reminders and job alerts. OAuth 2.1, free account
  <sub>TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @foundrole/ai-job-search-mcp`</sub>
- **[smeet666/mcp-wikibooks-cookbook](https://github.com/smeet666/mcp-wikibooks-cookbook)** — The Cookbook on the English Wikibooks: search recipes, read ingredients and steps, and rescale quantities without ending up with 2.4 eggs. Install via npx mcp-wikibooks-cookbook
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-wikibooks-cookbook.git`</sub>
- **[smeet666/mcp-recipes](https://github.com/smeet666/mcp-recipes)** — Asks Marmiton and the Wikibooks Cookbook at once and compares how each tradition writes a dish. Scales ingredient lists in French and English in one call, flagging what cannot be scaled. Install via npx mcp-recipes
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-recipes.git`</sub>
- **[githunt-agent/githunt-mcp](https://github.com/githunt-agent/githunt-mcp)** — Search, rank, and analyze GitHub developers for tech recruiting. Location/role/skill search over millions of ranked profiles with AI scoring and contact discovery. Install via npx githunt-mcp or use the hosted server at https://mcp.githunt.ai/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx githunt-mcp`</sub>
- **[johnsmalls22-rgb/domain-search-king-mcp](https://github.com/johnsmalls22-rgb/domain-search-king-mcp)** — Domain name search returning only .com domains verified available to register, checked live against Verisign RDAP - not AI-guessed names
  <sub>JavaScript · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/johnsmalls22-rgb/domain-search-king-mcp.git`</sub>
- **[litescrape/litescrape-mcp-server](https://github.com/litescrape/litescrape-mcp-server)** — Google Search, Bing, DuckDuckGo and Google Maps results as JSON with no API key (free daily allowance per network); Google AI Mode, AI Overview and Shopping with a key. npx -y litescrape-mcp-server
  <sub>TypeScript · MIT · source · pushed 2026-09-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/litescrape/litescrape-mcp-server.git`</sub>
- **[mambalabsdev/mcp-ai-tooling-detector](https://github.com/mambalabsdev/mcp-ai-tooling-detector)** — Detects whether a company only declares AI, actually deploys AI tooling on its site, or charges money for AI, returning a four-level AI maturity tier with the evidence behind the verdict
  <sub>TypeScript · MIT · source · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-ai-tooling-detector.git`</sub>
- **[mambalabsdev/mcp-company-contact-details-extractor](https://github.com/mambalabsdev/mcp-company-contact-details-extractor)** — Finds a company contact page and extracts role emails, a phone number, and a postal address
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-contact-details-extractor.git`</sub>
- **[mambalabsdev/mcp-company-social-presence-mapper](https://github.com/mambalabsdev/mcp-company-social-presence-mapper)** — Maps a company domain to its official LinkedIn, X, Instagram, Facebook, and YouTube URLs plus follower counts, returning flat Clay-ready JSON via an Apify actor
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-social-presence-mapper.git`</sub>
- **[mambalabsdev/mcp-event-presence-index](https://github.com/mambalabsdev/mcp-event-presence-index)** — Returns the third party conferences and trade shows a company publicly says it attends, with a year for each
  <sub>TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @mambalabsdev/mcp-event-presence-index`</sub>
- **[mambalabsdev/mcp-funding-press-signal-scanner](https://github.com/mambalabsdev/mcp-funding-press-signal-scanner)** — Scans Google News and PR wires for a company's funding rounds, exec moves, product launches, and acquisitions, returned as deduplicated, dated events in flat Clay-ready JSON
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-funding-press-signal-scanner.git`</sub>
- **[mambalabsdev/mcp-github-organization-signal-scanner](https://github.com/mambalabsdev/mcp-github-organization-signal-scanner)** — Resolves a company domain to its GitHub organization with repository, language, and activity signals
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-github-organization-signal-scanner.git`</sub>
- **[mambalabsdev/mcp-review-platform-reputation-enricher](https://github.com/mambalabsdev/mcp-review-platform-reputation-enricher)** — Resolves a company domain to its Trustpilot rating, review count, and claimed status
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-review-platform-reputation-enricher.git`</sub>
- **[modelcontextprotocol/server-fetch](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/fetch)** — Efficient web content fetching and processing for AI consumption
  <sub>JavaScript · MIT · in-repo · pushed 2025-05-28</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers-archived.git && cd servers-archived/src/fetch`</sub>
- **[Pexafy/pexafy-mcp](https://github.com/Pexafy/pexafy-mcp)** — Semantic stock-photo search across 9 free-license sources (Unsplash, Pexels, Pixabay and more): describe a scene in a full sentence, search from an example image URL, or ask for more like a previous result. Hosted remote server with OAuth — no API key to paste, just add https://mcp.pexafy.com/mcp. Results render as an inline thumbnail grid (MCP Apps) and each one carries its attribution string
  <sub>Python · MIT · docker · pushed 2026-08-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm pexafy-mcp`</sub>
- **[opendatalab/MinerU-Ecosystem](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/mcp)** — Official MinerU document parsing MCP (mineru-open-mcp on PyPI). Converts PDFs, doc/docx/ppt/pptx, images, and spreadsheets to Markdown via the MinerU API; free Flash mode without an API key (about 20 pages per file); optional MINERU_API_TOKEN for higher limits
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/opendatalab/MinerU-Ecosystem.git && cd MinerU-Ecosystem/mcp`</sub>
- **[phpcip/opensolr-mcp](https://github.com/phpcip/opensolr-mcp)** — Managed Apache Solr search for AI agents: hybrid (BM25 + kNN) and semantic search, document ingestion with server-side embeddings, grounded RAG answers, and index management. In the official MCP Registry as com.opensolr/opensolr-mcp. Install via uvx opensolr-mcp
  <sub>Python · MIT · uv · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx opensolr-mcp`</sub>
- **[quantumproxies/quanticdata-mcp-server](https://github.com/quantumproxies/quanticdata-mcp-server)** — Web data for AI agents: scrape any page to clean Markdown, structured SERP search across three engines, site crawl and map, 74 ready-made collectors, and datasets from a plain-language prompt — through residential proxies, billed per successful call
  <sub>TypeScript · MIT · source · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/quantumproxies/quanticdata-mcp-server.git`</sub>
- **[Rererr/amenbo](https://github.com/Rererr/amenbo)** — Japanese-web-native web fetching optimized for low target-site impact and token efficiency. Outline-first progressive disclosure, Shift_JIS/EUC-JP mojibake handling, PDF/CSV extraction, and polite crawling (robots.txt, rate limits, honest User-Agent). Install via npx -y amenbo
  <sub>TypeScript · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g amenbo`</sub>
- **[sascharo/gxtract](https://github.com/sascharo/gxtract)** — GXtract is a MCP server designed to integrate with VS Code and other compatible editors. It provides a suite of tools for interacting with the GroundX platform, enabling you to leverage its powerful document understanding capabilities directly within your development environment
  <sub>unavailable</sub>
- **[Seomarlboro/digmyname](https://github.com/Seomarlboro/digmyname/tree/main/mcp)** — Domain availability, 7-registrar price comparison, and domain age across 52 TLDs. Free, no API key
  <sub>TypeScript · in-repo · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/Seomarlboro/digmyname.git && cd digmyname/mcp`</sub>
- **[serpdive/serpdive-mcp](https://github.com/serpdive/serpdive-mcp)** — Web search that returns extracted, answer-ready page content (url, title, date, text) instead of links. A Tavily alternative: same speed, 20.2% fewer tokens, higher answer quality (60.7% of decided duels) on a public replayable benchmark. One tool with automatic localization and an optional synthesized answer. Hosted Streamable HTTP at https://mcp.serpdive.com, or run npx -y serpdive-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y serpdive-mcp`</sub>
- **[smeet666/mcp-ashby](https://github.com/smeet666/mcp-ashby)** — Search the public job boards companies publish through Ashby. Resolve a company name to its board token, filter its openings, read one posting in full, and compare the pay ranges it publishes without converting between currencies. No API key and no account
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-ashby.git`</sub>
- **[smeet666/mcp-animenewsnetwork](https://github.com/smeet666/mcp-animenewsnetwork)** — Search the Anime News Network encyclopedia for anime and manga, read cast, staff, episodes and studios, and follow the news wire. A name search upstream returns the full record of every match, 1.4 MB for a common query; this returns compact rows instead. No API key. npx -y mcp-animenewsnetwork
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-animenewsnetwork.git`</sub>
- **[smeet666/mcp-marmiton](https://github.com/smeet666/mcp-marmiton)** — Search Marmiton recipes, read their ingredients and steps, and rescale quantities to any number of servings. No API key. npx -y mcp-marmiton
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-marmiton.git`</sub>
- **[smeet666/mcp-pequerecetas](https://github.com/smeet666/mcp-pequerecetas)** — Read Spanish family recipes from Pequerecetas, rescale them to any number of servings, and browse by diet, main ingredient, appliance or the age of whoever eats them, from six months up. No API key. npx -y mcp-pequerecetas
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-pequerecetas.git`</sub>
- **[softvoyagers/linkmeta-api](https://github.com/softvoyagers/linkmeta-api)** — Free URL metadata extraction API (Open Graph, Twitter Cards, favicons, JSON-LD). No API key required
  <sub>unavailable</sub>
- **[srezai-team/srezai-mcp](https://github.com/srezai-team/srezai-mcp)** — Web and image search, page reading as clean Markdown, browser-rendered screenshots, schema-based extraction and agentic deep research. Strong Russian-web coverage. Remote (Streamable HTTP) at https://srezai.ru/api/mcp or via npx srezai-mcp for stdio-only clients
  <sub>TypeScript · MIT · source · pushed 2026-08-06 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/srezai-team/srezai-mcp.git`</sub>
- **[StripFeed/mcp-server](https://github.com/StripFeed/mcp-server)** — Convert any URL to clean, token-efficient Markdown for AI agents. API-backed extraction with token counting, CSS selector support, and configurable caching via StripFeed
  <sub>unavailable</sub>
- **[MarcinDudekDev/the-data-collector](https://github.com/MarcinDudekDev/the-data-collector)** — MCP server for scraping Hacker News, Bluesky, and Substack with x402 micropayment support. Tools: hn_search, bluesky_search, substack_search. $0.05/call via USDC on Base
  <sub>unavailable</sub>
- **[webpeel/webpeel](https://github.com/webpeel/webpeel)** — Smart web fetcher for AI agents with auto-escalation from HTTP to headless browser to stealth mode. Includes 9 MCP tools: fetch, search, crawl, map, extract, batch, screenshot, jobs, and agent. Achieved 100% success rate on a 30-URL benchmark
  <sub>unavailable</sub>
- **[WhaleCupl/ai-daily-insights-mcp](https://github.com/WhaleCupl/ai-daily-insights-mcp)** — Structured access to AI Daily Insights (aidailyinsights.cn), a Chinese daily AI-industry briefing built for agents. List, fetch and full-text search daily AI news as structured items — 6 tools (get_latest, list_latest, get_article, get_range, list_by_tag, search), no API key. Install via npx -y ai-daily-insights-mcp
  <sub>JavaScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/WhaleCupl/ai-daily-insights-mcp.git`</sub>
- **[Darko893/haunt-mcp-server](https://github.com/Darko893/haunt-mcp-server)** — Haunt web extraction for AI agents: structured JSON or clean Markdown from permitted public pages, including Cloudflare-protected ones, with honest blocked/login/captcha errors instead of fabricated data
  <sub>unavailable</sub>
- **[smeet666/mcp-ptitchef](https://github.com/smeet666/mcp-ptitchef)** — Search Ptitchef, browse its tree of ingredient categories, read a recipe with its ingredients, method, cost and nutrition, and ask what can be cooked from what is in the fridge. Rescales to any number of servings, and lists the other languages a recipe was published in. No API key. npx -y mcp-ptitchef
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-ptitchef.git`</sub>
- **[smeet666/mcp-bbc-goodfood](https://github.com/smeet666/mcp-bbc-goodfood)** — Search BBC Good Food and read a recipe in either of the two renditions the site writes, its own and the one restated for readers in the United States. Publishes the vocabulary each search facet accepts, since the site answers a value it does not know with a total of zero. Rescales to any number of people. No API key. npx -y mcp-bbc-goodfood
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-bbc-goodfood.git`</sub>
- **[smeet666/mcp-supertoinette](https://github.com/smeet666/mcp-supertoinette)** — Read Supertoinette's French recipes: ingredients with the quantity separated from the line, steps, difficulty, cost level, resting time, and the five wines the site ranks for a dish. Rescales any recipe to a number of people, saying on each line whether the arithmetic landed exactly. No API key. npx -y mcp-supertoinette
  <sub>TypeScript · MIT · source · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-supertoinette.git`</sub>
- **[AG-Bureau/mcp-search](https://github.com/AG-Bureau/mcp-search)** — Search, read, images, screenshots and multi-source answers over your own SearXNG. Every answer says which engines were asked and what to disbelieve; the engine pool maintains itself
  <sub>Python · AGPL-3.0 · docker · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`docker compose up -d --force-recreate ag-search`</sub>

## Data Science Tools

- **[zcaceres/markdownify-mcp](https://github.com/zcaceres/markdownify-mcp)** — An MCP server to convert almost any file or web content into Markdown
  <sub>★ 3k · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/zcaceres/markdownify-mcp.git`</sub>
- **[datalayer/jupyter-mcp-server](https://github.com/datalayer/jupyter-mcp-server)** — Model Context Protocol (MCP) Server for Jupyter
  <sub>★ 1.3k · Python · BSD-3-Clause · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "jupyter-mcp-server>=1.5.0" "code-sandboxes>=1.1.1"`</sub>
- **[DataEval/dingo](https://github.com/MigoXLab/dingo)** — MCP server for the Dingo: a comprehensive data quality evaluation tool. Server Enables interaction with Dingo's rule-based and LLM-based evaluation capabilities and rules&amp;prompts listing
  <sub>★ 757 · Python · Apache-2.0 · pip · pushed 2026-09-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install dingo-python`</sub>
- **[reading-plus-ai/mcp-server-data-exploration](https://github.com/reading-plus-ai/mcp-server-data-exploration)** — Enables autonomous data exploration on .csv-based datasets, providing intelligent insights with minimal effort
  <sub>★ 544 · Python · MIT · source · pushed 2025-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reading-plus-ai/mcp-server-data-exploration.git`</sub>
- **[jjsantos01/jupyter-notebook-mcp](https://github.com/jjsantos01/jupyter-notebook-mcp)** — connects Jupyter Notebook to Claude AI, allowing Claude to directly interact with and control Jupyter Notebooks
  <sub>★ 130 · Jupyter Notebook · MIT · clone · pushed 2025-04-02 · Win?</sub>
  <sub>`git clone https://github.com/jjsantos01/jupyter-notebook-mcp.git`</sub>
- **[ChronulusAI/chronulus-mcp](https://github.com/ChronulusAI/chronulus-mcp)** — Predict anything with Chronulus AI forecasting and prediction agents
  <sub>★ 112 · Python · MIT · pip · pushed 2025-07-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install chronulus-mcp`</sub>
- **[optuna/optuna-mcp](https://github.com/optuna/optuna-mcp)** — Official MCP server enabling seamless orchestration of hyperparameter search and other optimization tasks with Optuna
  <sub>★ 86 · Python · MIT · source · pushed 2026-08-05 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/optuna/optuna-mcp.git`</sub>
- **[kdqed/zaturn](https://github.com/kdqed/zaturn)** — Link multiple data sources (SQL, CSV, Parquet, etc.) and ask AI to analyze the data for insights and visualizations
  <sub>★ 75 · Python · MIT · source · pushed 2025-11-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kdqed/zaturn.git`</sub>
- **[arrismo/kaggle-mcp](https://github.com/arrismo/kaggle-mcp)** — Connects to Kaggle, ability to download and analyze datasets
  <sub>★ 39 · Python · MIT · docker · pushed 2026-05-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -i --env-file .env kaggle-mcp`</sub>
- **[HumanSignal/label-studio-mcp-server](https://github.com/HumanSignal/label-studio-mcp-server)** — Create, manage, and automate Label Studio projects, tasks, and predictions for data labeling workflows
  <sub>★ 37 · Python · Apache-2.0 · clone · pushed 2025-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HumanSignal/label-studio-mcp-server.git`</sub>
- **[phisanti/MCPR](https://github.com/phisanti/MCPR)** — Model Context Protocol for R: enables AI agents to participate in interactive live R sessions
  <sub>★ 26 · HTML · CC-BY-SA-4.0 · source · pushed 2026-09-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/phisanti/MCPR.git`</sub>
- **[growthbook/growthbook-mcp](https://github.com/growthbook/growthbook-mcp)** — Tools for creating and interacting with GrowthBook feature flags and experiments
  <sub>★ 24 · TypeScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @growthbook/mcp`</sub>
- **[abhiphile/fermat-mcp](https://github.com/abhiphile/fermat-mcp)** — The ultimate math engine unifying SymPy, NumPy &amp; Matplotlib in one powerful server. Perfect for developers &amp; researchers needing symbolic algebra, numerical computing, and data visualization
  <sub>★ 20 · Python · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @abhiphile/fermat-mcp --client gemini`</sub>
- **[Bright-L01/networkx-mcp-server](https://github.com/brightlikethelight/networkx-mcp-server)** — The first NetworkX integration for Model Context Protocol, enabling graph analysis and visualization directly in AI conversations. Supports 13 operations including centrality algorithms, community detection, PageRank, and graph visualization
  <sub>★ 20 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install networkx-mcp-server`</sub>
- **[subelsky/bundler_mcp](https://github.com/subelsky/bundler_mcp)** — Enables agents to query local information about dependencies in a Ruby project's Gemfile
  <sub>★ 20 · Ruby · MIT · npx · pushed 2025-06-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector ./bin/bundler_mcp`</sub>
- **[Whatsonyourmind/oraclaw](https://github.com/Whatsonyourmind/oraclaw)** — Decision intelligence MCP server with 19 algorithms (bandits, Monte Carlo, constraint optimization, forecasting, anomaly detection, risk analysis, graph algorithms), 28 MCP tools. Install via npx -y @oraclaw/mcp-server
  <sub>★ 13 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Whatsonyourmind/oraclaw.git`</sub>
- **[Archerkattri/mathlas](https://github.com/Archerkattri/mathlas)** — Airtight math for agents: 3.7M-theorem search, PSLQ constant ID, OEIS, real Lean kernel checks, applicability checklists. No LLM inside, no API key
  <sub>★ 12 · Python · Apache-2.0 · uv · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mathlas-mcp`</sub>
- **[phuongrealmax/code-guardian](https://github.com/phuongrealmax/code-guardian)** — AI-powered code refactor engine with 80+ MCP tools for code analysis, hotspot detection, complexity metrics, persistent memory, and automated refactoring plans
  <sub>★ 9 · TypeScript · npm · pushed 2025-12-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g codeguardian-studio`</sub>
- **[leap-laboratories/discovery-engine](https://github.com/leap-laboratories/discovery-engine)** — Superhuman exploratory data analysis that finds the feature interactions and subgroup effects that LLMs and manual exploration miss — with p-values, effect sizes, and literature citations. Data goes in, validated insights come out. Free for public data
  <sub>★ 7 · Python · MIT · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install discovery-engine-api`</sub>
- **[avisangle/calculator-server](https://github.com/avisangle/calculator-server)** — A comprehensive Go-based MCP server for mathematical computations, implementing 13 mathematical tools across basic arithmetic, advanced functions, statistical analysis, unit conversions, and financial calculations
  <sub>★ 6 · Go · source · pushed 2025-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/avisangle/calculator-server.git`</sub>
- **[clouatre-labs/math-mcp-learning-server](https://github.com/clouatre-labs/math-mcp-learning-server)** — Educational MCP server for math operations, statistics, visualization, and persistent workspaces. Built with FastMCP 2.0
  <sub>★ 5 · Python · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/clouatre-labs/math-mcp-learning-server.git`</sub>
- **[FantasyLab-ai/aurora](https://github.com/FantasyLab-ai/aurora)** — Glass-box statistical analysis: 19 research-grade methods, cited findings, integrity-hashed bundles, and measured detector false-fire rates shipped as a calibration corpus. Agents cite real math instead of inventing it. uvx aurora-mcp
  <sub>★ 5 · Python · Apache-2.0 · uv · pushed 2026-09-05 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx aurora-mcp`</sub>
- **[gpartin/WaveGuardClient](https://github.com/gpartin/WaveGuardClient)** — Physics-based anomaly detection via MCP. Uses Klein-Gordon wave equations on GPU to detect anomalies with high precision (avg 0.90). 9 tools: scan, fingerprint, compare, token risk, wallet profiling, volume check, price manipulation detection
  <sub>★ 4 · Python · MIT · pip · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install WaveGuardClient scikit-learn`</sub>
- **[pramod/kaggle](https://github.com/KrishnaPramodParupudi/kaggle-mcp-server)** — This Kaggle MCP Server makes Kaggle more accessible by letting you browse competitions, leaderboards, models, datasets, and kernels directly within MCP, streamlining discovery for data scientists and developers
  <sub>★ 4 · Python · MIT · source · pushed 2025-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KrishnaPramodParupudi/kaggle-mcp-server.git`</sub>
- **[ShipItAndPray/mcp-turboquant](https://github.com/ShipItAndPray/mcp-turboquant)** — LLM quantization via tool call. Convert models to GGUF, GPTQ, and AWQ formats. Recommend optimal quant settings, evaluate quality, and push to Hugging Face Hub
  <sub>★ 4 · Python · MIT · uv · pushed 2026-04-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-turboquant`</sub>
- **[bradleylab/stella-mcp](https://github.com/bradleylab/stella-mcp)** — Create, read, validate, and save Stella system dynamics models (.stmx files in XMILE format) for scientific simulation and modeling
  <sub>★ 3 · Python · MIT · pip · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install stella-mcp`</sub>
- **[aurelio-nakamura/dataloupe](https://github.com/aurelio-nakamura/dataloupe)** — Local, offline access to tabular data for AI assistants: list/describe/preview/query CSV/TSV/JSON/Parquet/Excel files, diff two datasets, and generate a self-contained interactive HTML explorer to open in any browser — nothing leaves your machine. Install via npx -y github:aurelio-nakamura/dataloupe mcp
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g dataloupe`</sub>
- **[Daichi-Kudo/llm-advisor-mcp](https://github.com/Daichi-Kudo/llm-advisor-mcp)** — Real-time LLM/VLM model comparison with benchmarks, pricing, and personalized recommendations from 5 data sources. No API key required
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Daichi-Kudo/llm-advisor-mcp.git`</sub>
- **[haiiibin/data-profiler-mcp](https://github.com/haiiibin/data-profiler-mcp)** — Profiles tabular data files (CSV, TSV, Parquet, Excel, JSON) for LLM agents: one-call dataset overview, per-column statistics, a data-quality audit (missing values, duplicates, mixed types, outliers), and memory-saving dtype suggestions. Pure Python (pandas); files are read locally and nothing leaves your machine. pip install data-profiler-mcp
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install data-profiler-mcp`</sub>
- **[ShipItAndPray/mcp-compress](https://github.com/ShipItAndPray/mcp-compress)** — Data compression MCP server. 7 tools for gzip, brotli, deflate, and TurboQuant quantization. Auto-selects best algorithm. 60x compression on docs. Zero dependencies
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-compress`</sub>
- **[98lukehall/renoun-mcp](https://github.com/98lukehall/renoun-mcp)** — Structural observability for AI conversations. Detects loops, stuck states, breakthroughs, and convergence across 17 channels without analyzing content
  <sub>★ 2 · Python · source · pushed 2026-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/98lukehall/renoun-mcp.git`</sub>
- **[tufantunc/axiom-advanced-math-mcp](https://github.com/tufantunc/axiom-advanced-math-mcp)** — Exact symbolic mathematics from a real computer algebra system (Giac/Xcas compiled to WebAssembly, no network calls): calculus, equation solving, linear algebra, combinatorics, and independent verification of a claim. Also runs as a shell command, so agents can use it as a skill with no MCP configuration. npx -y axiom-math
  <sub>★ 2 · TypeScript · GPL-3.0 · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g axiom-math`</sub>
- **[agmonetti/mathmethods-mcp](https://github.com/agmonetti/mathmethods-mcp)** — Numerical methods MCP server for root finding, numerical integration, differential equations (RK4), and Lagrange interpolation
  <sub>★ 1 · Python · MIT · npm · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @agmonetti/mathmethods-mcp`</sub>
- **[chohyerinn/filter-mcp-server](https://github.com/chohyerinn/filter-mcp-server)** — Compares approximate filter data structures (Bloom, Counting Bloom, Cuckoo, SuRF) via MCP
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chohyerinn/filter-mcp-server.git`</sub>
- **[lihtness/gnomon-mcp](https://github.com/lihtness/gnomon-mcp)** — Deterministic batch tools so LLM agents stop next-token-guessing dates and math. Rich now() snapshot (18 fields), calendar(ops) batch dispatcher (diff/until/since/add/weekday/business_days, natural-language parsing), calc(expressions) Python eval with math+stats pre-loaded, and Pint-based unit conversion. One wiring for dates + math + units. Listed in the official MCP Server Registry. uvx gnomon-m
  <sub>★ 1 · Python · MIT · uv · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx gnomon-mcp # serves stdio MCP, ready for any client`</sub>
- **[mrnh/rigor](https://github.com/mrnh/rigor)** — Classical hypothesis testing, effect sizes, power/sample-size, and multiple-comparisons correction, computed from scratch and returned as a cited, assumption-checked answer instead of a number recalled from training data. uvx rigor-mcp
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx rigor-mcp`</sub>
- **[playidea-lab/pcq](https://github.com/playidea-lab/pcq)** — Agent-operable ML experiment contract (cq.yaml + JSON contracts) with a built-in MCP server exposing 14 tools (resolve/inspect/run/validate/describe/compare/lineage) for running, validating, and tracing experiments across any framework (PyTorch / HF Trainer / Lightning / sklearn / XGBoost). Apache-2.0
  <sub>★ 1 · Python · Apache-2.0 · docker · pushed 2026-05-29 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm pcq # MCP client attaches to stdin/stdout`</sub>
- **[laszlopere/mcp-gnu-units](https://github.com/laszlopere/mcp-gnu-units)** — Unit conversion and dimensional analysis backed by the bundled GNU units database (3000+ units, compound expressions, reduction to SI base units). Offline and deterministic. uvx mcp-gnu-units
  <sub>★ 1 · Python · GPL-3.0 · source · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/laszlopere/mcp-gnu-units.git`</sub>
- **[inity13/decisionmatrix-mcp](https://github.com/inity13/decisionmatrix-mcp)** — Deterministic multi-criteria decision analysis (MCDA): score, rank &amp; explain options against weighted criteria with weighted-sum, weighted-product, or TOPSIS, plus sensitivity analysis (which weights would flip the winner). Exact decimals, stateless. Free hosted endpoint or self-host (MIT). https://decisionmatrix-mcp.pages.dev/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y decisionmatrix-mcp`</sub>
- **[BlackMount-ai/blackmount-nlp-mcp](https://github.com/BlackMount-ai/blackmount-nlp-mcp)** — Deterministic local text analysis: sentiment, readability scoring, keyword extraction, text similarity, summarization, and language detection across 18 languages. Pure Python, zero heavy dependencies, 42 KB wheel. Install: pip install blackmount-nlp-mcp
  <sub>unavailable</sub>
- **[headlessherm-creator/polymath-megablaster-mcp](https://github.com/headlessherm-creator/polymath-megablaster-mcp)** — Deterministic calculation for AI agents: exact-precision math (avoids float64 overflow), date arithmetic (leap years, business days), unit conversion, statistics, subnet math, haversine distance, base conversion, and Levenshtein distance. 15 tools, 100% local, no network calls, no API keys, no telemetry. npx -y polymath-megablaster-mcp
  <sub>JavaScript · MIT · clone · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/headlessherm-creator/polymath-megablaster-mcp.git`</sub>
- **[jonahthan433/cortexcloud-mcp](https://github.com/jonahthan433/cortexcloud-mcp)** — Pay-per-call QUBO/Ising optimization for AI agents: estimate free, solve per run (classical $0.05, hybrid $0.10, quantum $0.85) via x402 (USDC on Base). No API keys. Remote Streamable HTTP at https://api.cortexcloud.org/mcp
  <sub>Python · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jonahthan433/cortexcloud-mcp.git`</sub>
- **[mckinsey/vizro-mcp](https://github.com/mckinsey/vizro/tree/main/vizro-mcp)** — Tools and templates to create validated and maintainable data charts and dashboards
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-26</sub>
  <sub>`git clone https://github.com/mckinsey/vizro.git && cd vizro/vizro-mcp`</sub>
- **[hanshs474/jevx-mcp](https://github.com/hanshs474/jevx-mcp)** — Run Jev AI typed decisions (choice, score, noul) on jevx.org and get calibrated probabilities on every option. Zero-shot: criteria live in the request, no training or fine-tune to change the label set. npx jevx-mcp
  <sub>TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx jevx-mcp`</sub>

## Data Visualization

- **[nteract/semiotic](https://github.com/nteract/semiotic)** — React data visualization MCP server with 30+ chart types. 5 tools: suggest charts for a dataset, render validated React configs to SVG, diagnose configuration anti-patterns, get component schemas, and report issues
  <sub>★ 2.7k · TypeScript · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx semiotic-ai --list # list components with import paths and renderability`</sub>
- **[KyuRish/mcp-dashboards](https://github.com/KyuRish/mcp-dashboards)** — 45+ interactive chart types (bar, line, pie, candlestick, sankey, geo, radar, funnel, treemap, and more), dashboards with KPI cards, drill-down navigation, live API polling, 20 themes, and export to PNG/PPT/A4. Built on MCP Apps
  <sub>★ 48 · TypeScript · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-dashboards`</sub>
- **[kleinicke/ply-visualizer](https://github.com/kleinicke/ply-visualizer)** — 3D Visualizer: inspect, compare and export point clouds, meshes and calibrated depth data, with interactive previews in WebGL-capable MCP Apps clients. Supports labeled selections, measurements, NumPy/PyTorch inputs and COLMAP depth
  <sub>★ 20 · TypeScript · MIT · source · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kleinicke/ply-visualizer.git`</sub>
- **[Ratnaditya-J/csvglow](https://github.com/Ratnaditya-J/csvglow)** — Generate beautiful self-contained HTML dashboards from CSV/Excel files with interactive ECharts visualizations, dark gradient theme, and sortable data tables
  <sub>★ 13 · Python · MIT · npx · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx csvglow data.csv`</sub>
- **[marzukia/charted](https://github.com/marzukia/charted)** — Zero-dependency chart server that renders bar, line, pie, scatter, and more from JSON or CSV to SVG, HTML, PNG, or data URL. Built-in themes; PNG output renders inline in chat. Install via uvx --from charted[mcp] charted-mcp
  <sub>★ 11 · Python · MIT · uv · pushed 2026-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from charted[mcp] charted-mcp`</sub>
- **[MS-Teja/Glyphic](https://github.com/MS-Teja/Glyphic)** — Generate diagrams from structured JSON across 18 types (architecture, ERD, sequence, flowchart, Gantt…) — native SVG/PNG, no headless browser. Built for LLMs and agents
  <sub>★ 10 · TypeScript · source · pushed 2026-07-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MS-Teja/Glyphic.git`</sub>
- **[pushtodisplay/cli](https://github.com/pushtodisplay/cli)** — Push To Display MCP server send structured content to selected boards on iOS and android devices with app Push To Display, route updates to specific panels, and render in real time with display-focused multi-panel layouts
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pushtodisplay`</sub>
- **[ganapativs/microcharts](https://github.com/ganapativs/microcharts/tree/main/packages/mcp)** — Word-sized charts (sparklines, bars, bullets — 106 types) rendered to self-contained SVG with generated alt text. Three tools: find the right chart for a question, get its wiring, render it. Works in chat surfaces that can't run React. Install via npx -y @microcharts/mcp
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/ganapativs/microcharts.git && cd microcharts/packages/mcp`</sub>
- **[oscarleoo/chartlink-agents](https://github.com/oscarleoo/chartlink-agents)** — Charts and tables with live-updating embed links, built for agents: draft from one message, preview, publish, then update the numbers and every embed follows. 11 chart types including maps and sortable tables, brands, any Google Font. No account — signup returns a key. Hosted at https://chartlink.app/mcp, or npx -y chartlink-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx chartlink-mcp`</sub>
- **[subhatta123/twilize](https://github.com/subhatta123/twilize)** — Programmatic Tableau workbook (.twb/.twbx) generation — 47 MCP tools for charts, dashboards, calculated fields, dashboard actions, workbook migration, and CSV-to-dashboard pipelines. Install via uvx twilize
  <sub>unavailable</sub>

## Data Platforms

- **[dbt-labs/dbt-mcp](https://github.com/dbt-labs/dbt-mcp)** — Official MCP server for dbt (data build tool) providing integration with dbt Core/Cloud CLI, project metadata discovery, model information, and semantic layer querying capabilities
  <sub>★ 608 · Python · Apache-2.0 · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dbt-labs/dbt-mcp.git`</sub>
- **[gura105/operational-ontology](https://github.com/gura105/operational-ontology)** — Reference implementation of an "operational ontology": MCP tools are generated from a typed business domain model (objects, links, actions) — one tool per query shape and per action, deliberately no raw SQL tool. Writes pass business-rule preconditions, are audited, and write back to the systems of record; refusals are machine-readable. Demo scenario included (pnpm demo / pnpm mcp)
  <sub>★ 160 · TypeScript · MIT · source · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gura105/operational-ontology.git`</sub>
- **[keboola/keboola-mcp-server](https://github.com/keboola/mcp-server)** — interact with Keboola Connection Data Platform. This server provides tools for listing and accessing data from Keboola Storage API
  <sub>★ 86 · Python · MIT · uv · pushed 2026-09-25 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`uvx keboola_mcp_server login --api-url https://connection.YOUR_REGION.keboola.com`</sub>
- **[bintocher/mcp-superset](https://github.com/bintocher/mcp-superset)** — Full-featured Apache Superset MCP server with 135+ tools for dashboards, charts, datasets, SQL Lab, security (users, roles, RLS, groups), permissions audit, and 30+ built-in safety validations. Supports HTTP, SSE, and stdio transports
  <sub>★ 59 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-superset`</sub>
- **[JordiNei/mcp-databricks-server](https://github.com/JordiNeil/mcp-databricks-server)** — Connect to Databricks API, allowing LLMs to run SQL queries, list jobs, and get job status
  <sub>★ 50 · Python · source · pushed 2025-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JordiNeil/mcp-databricks-server.git`</sub>
- **[meal-inc/bonnard-cli](https://github.com/bonnard-data/bonnard-cli)** — Ultra-fast to deploy agentic-first MCP-ready semantic layer. Let your data be like water
  <sub>★ 50 · TypeScript · MIT · npm · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @bonnard/cli`</sub>
- **[aywengo/kafka-schema-reg-mcp](https://github.com/aywengo/kafka-schema-reg-mcp)** — Comprehensive Kafka Schema Registry MCP server with 48 tools for multi-registry management, schema migration, and enterprise features
  <sub>★ 32 · Python · MIT · docker · pushed 2026-09-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -e SCHEMA_REGISTRY_URL=http://localhost:8081 -e SLIM_MODE=true aywengo/kafka-schema-reg-mcp:stable`</sub>
- **[bruno-portfolio/agrobr-mcp](https://github.com/bruno-portfolio/agrobr-mcp)** — Brazilian agricultural data for LLMs — prices, crop estimates, climate, deforestation from 19 public sources via CEPEA, CONAB, IBGE, INPE and B3
  <sub>★ 27 · Python · MIT · pip · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install agrobr-mcp`</sub>
- **[mattijsdp/dbt-docs-mcp](https://github.com/mattijsdp/dbt-docs-mcp)** — MCP server for dbt-core (OSS) users as the official dbt MCP only supports dbt Cloud. Supports project metadata, model and column-level lineage and dbt documentation
  <sub>★ 23 · Python · MIT · source · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mattijsdp/dbt-docs-mcp.git`</sub>
- **[vikramgorla/mcp-swiss](https://github.com/vikramgorla/mcp-swiss)** — 68 tools for Swiss open data: transport, weather, geodata, companies, parliament, and more. Zero API keys required
  <sub>★ 22 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx mcp-swiss`</sub>
- **[yashshingvi/databricks-genie-MCP](https://github.com/yashshingvi/databricks-genie-MCP)** — A server that connects to the Databricks Genie API, allowing LLMs to ask natural language questions, run SQL queries, and interact with Databricks conversational agents
  <sub>★ 17 · Python · MIT · source · pushed 2025-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yashshingvi/databricks-genie-MCP.git`</sub>
- **[mbrummerstedt/powerbi-analyst-mcp](https://github.com/mbrummerstedt/powerbi-analyst-mcp)** — Connect LLMs to Power BI semantic models. Browse workspaces, tables, and measures, run DAX queries, and automatically page large results via local CSV
  <sub>★ 14 · Python · MIT · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install powerbi-analyst-mcp`</sub>
- **[jwaxman19/qlik-mcp](https://github.com/jwaxman19/qlik-mcp)** — MCP Server for Qlik Cloud API that enables querying applications, sheets, and extracting data from visualizations with comprehensive authentication and rate limiting support
  <sub>★ 11 · TypeScript · MIT · docker · pushed 2025-07-27 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --env-file .env qlik-mcp`</sub>
- **[flowcore/mcp-flowcore-platform](https://github.com/flowcore-io/mcp-flowcore-platform)** — Interact with Flowcore to perform actions, ingest data, and analyse, cross reference and utilise any data in your data cores, or in public data cores; all with human language
  <sub>★ 9 · TypeScript · npm · pushed 2025-05-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @flowcore/platform-mcp-server`</sub>
- **[alanpcf/brasil-data-mcp](https://github.com/alanpcf/brasil-data-mcp)** — Brazilian public data for AI agents — companies (CNPJ), addresses (CEP), banks (BACEN), national holidays — via BrasilAPI. No auth, no API key. Install: npx -y brasil-data-mcp
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y brasil-data-mcp`</sub>
- **[1luvc0d3/metabase-mcp](https://github.com/1luvc0d3/metabase-mcp)** — MCP server connecting Claude to Metabase with 28 tools for natural language data analysis, dashboard management, SQL queries, and automated insights. Features SQL guardrails, rate limiting, and audit logging
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ai-1luvc0d3/metabase-mcp`</sub>
- **[soil-dev/capsulemcp](https://github.com/soil-dev/capsulemcp)** — MCP server for Capsule CRM. 81 tools (49 in read-only mode) covering contacts, opportunities, projects, tasks, timeline activity, structured + saved filters, workflow tracks, and file attachments. Two transports — stdio (npx capsulemcp) and HTTP+OAuth for hosted Custom Connectors. Read-only-mode env flag for safer defaults. Apache 2.0
  <sub>★ 5 · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/soil-dev/capsulemcp.git`</sub>
- **[aegis-dq/aegis-dq](https://github.com/aegis-dq/aegis-dq)** — Agentic data quality framework that runs structured rules against warehouses (DuckDB, BigQuery, Athena, Databricks, Postgres), diagnoses failures with LLM root cause analysis, and proposes SQL remediations. Every LLM decision is audit-logged with cost and latency
  <sub>★ 4 · Python · pip · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install aegis-dq`</sub>
- **[alkemiai/alkemi-mcp](https://github.com/alkemi-ai/alkemi-mcp)** — MCP Server for natural language querying of Snowflake, Google BigQuery, and DataBricks Data Products through Alkemi.ai
  <sub>★ 4 · JavaScript · MIT · source · pushed 2025-10-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alkemi-ai/alkemi-mcp.git`</sub>
- **[Castaldo-Solutions/mcp-vtenext](https://github.com/Castaldo-Solutions/mcp-vtenext)** — MCP server for VTENext CRM (open-source vtiger-based). Query, create and update opportunities and contacts via the WebService API. Available on npm as @castaldosolutions/mcp-vtenext
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Castaldo-Solutions/mcp-vtenext.git`</sub>
- **[dan1d/mercadolibre-mcp](https://github.com/dan1d/mercadolibre-mcp)** — MercadoLibre marketplace integration for AI agents. Search products, get item details, browse categories, track trends, and convert currencies across Latin America (Argentina, Brazil, Mexico, Chile, Colombia)
  <sub>★ 4 · TypeScript · MIT · source · pushed 2026-03-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dan1d/mercadolibre-mcp.git`</sub>
- **[avisangle/method-crm-mcp](https://github.com/avisangle/method-crm-mcp)** — Production-ready MCP server for Method CRM API integration with 20 comprehensive tools for tables, files, users, events, and API key management. Features rate limiting, retry logic, and dual transport support (stdio/HTTP)
  <sub>★ 3 · Python · MIT · npx · pushed 2025-11-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector python src/method_mcp/server.py`</sub>
- **[Evan-Crx/permisapi-mcp](https://github.com/Evan-Crx/permisapi-mcp)** — 7 tools for French open-data building permits (Sitadel, 311k rows, ~2M permits/year, Etalab license). Search, details, DVF transactions cross-ref, real estate dealer opportunity score, PLU urban zoning, BRGM natural and technological risks, and a Vue 360 composite that fans out 6 sub-fetches in one tool call. Powered by permisapi.fr. Plan Free covers basic search and details, Pro+ unlocks the enri
  <sub>★ 3 · Python · MIT · uv · pushed 2026-05-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --python 3.11 permisapi-mcp`</sub>
- **[Hug0x0/mcp-reunion](https://github.com/Hug0x0/mcp-reunion)** — 96 tools across 21 modules for La Réunion (French overseas region) open data: economy, demographics, geography, transport, health, education, elections, tourism, housing, environment, and more. Powered by data.regionreunion.com and data.gouv.fr. Install: npx -y mcp-reunion
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Hug0x0/mcp-reunion.git`</sub>
- **[Osseni94/oyemi-mcp](https://github.com/Osseni94/oyemi-mcp)** — Deterministic semantic word encoding and valence/sentiment analysis using 145K+ word lexicon. Provides word-to-code mapping, semantic similarity, synonym/antonym lookup with zero runtime NLP dependencies
  <sub>★ 3 · Python · pip · pushed 2025-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install oyemi-mcp`</sub>
- **[paracetamol951/caisse-enregistreuse-mcp-server](https://github.com/paracetamol951/caisse-enregistreuse-mcp-server)** — Allows you to automate or monitor business operations, sales recorder, POS software, CRM
  <sub>★ 3 · TypeScript · GPL-3.0 · npx · pushed 2026-04-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx caisse-enregistreuse-mcp-server --shopid=YOUR_SHOPID --apikey=YOUR_APIKEY`</sub>
- **[Sugra-Systems/sugra-api-mcp](https://github.com/Sugra-Systems/sugra-api-mcp)** — Connector between LLM agents and world data - 1,500+ endpoints aggregating 160+ primary sources across 36 data domains: markets, macroeconomics, company fundamentals, government, news, climate, maritime, and entity screening. Install via pip install sugra-api-mcp or hosted at app.sugra.ai/mcp
  <sub>★ 3 · Python · MIT · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install sugra-api-mcp`</sub>
- **[Alessandro114/scala-mcp-server](https://github.com/Alessandro114/scala-mcp-server)** — Search and enrich data from 250M+ companies across 50+ countries. Company lookup by name, VAT, or ID, NACE sector search, and financial data from official EU business registries. Free tier: 50 lookups/month. Install: npx scala-mcp-server
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y scala-mcp-server`</sub>
- **[antonio-mello-ai/mcp-airflow](https://github.com/antonio-mello-ai/mcp-airflow)** — Manage Apache Airflow through its REST API — list DAGs, inspect DAG runs and task instances, trigger runs, and check failed-DAG and scheduler/metadatabase health. 7 tools, built with FastMCP. Install: uvx mcp-airflow
  <sub>★ 2 · Python · MIT · uv · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-airflow`</sub>
- **[Autario/autario-mcp](https://github.com/Autario/autario-mcp)** — Search, query, and publish charts across 2,300+ verified public datasets (World Bank, IMF, Eurostat, OECD, WHO). 28 MCP tools for data discovery, analysis, and visualization. Remote MCP + npm package
  <sub>★ 2 · JavaScript · source · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Autario/autario-mcp.git`</sub>
- **[vinvuk/apiverket-mcp](https://github.com/vinvuk/apiverket-mcp)** — Query Swedish public data through Apiverket, including company data, SCB statistics, weather, transport, and more. Install: npx -y apiverket-mcp-server
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vinvuk/apiverket-mcp.git`</sub>
- **[FreelexHo/power-bi-mcp](https://github.com/FreelexHo/power-bi-mcp)** — Power BI MCP server with device code auth, enhanced refresh (table-level polling with retry), refresh diagnostics with root-cause error catalog, DAX queries with RLS simulation, PBIP source locating, and scheduled refresh reports
  <sub>★ 2 · Python · MIT · clone · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FreelexHo/power-bi-mcp.git`</sub>
- **[meacheal-ai/mrc-data](https://github.com/meacheal-ai/mrc-data)** — China's apparel supply chain data for AI agents. 1,000+ verified suppliers, 350+ lab-tested fabrics, 170+ industrial clusters with AATCC / ISO / GB lab-test verification
  <sub>★ 2 · Shell · source · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/meacheal-ai/mrc-data.git`</sub>
- **[Osseni94/keyneg-mcp](https://github.com/Osseni94/keyneg-mcp)** — Enterprise-grade sentiment analysis with 95+ labels, keyword extraction, and batch processing for AI agents
  <sub>★ 2 · Python · pip · pushed 2025-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install keyneg-mcp`</sub>
- **[Kemetra/seshat-bi](https://github.com/Kemetra/Seshat-BI)** — Read-only readiness governance for BI pipelines. Six tools report where each table sits across a seven-stage source-to-Power-BI spine, explain what is blocking the next stage, run a static SQL/TMDL/PBIR governance check, and export an evidence pack. Tools never write files, execute warehouse work, or grant approvals -- human sign-off stays a separate seam. Install: pip install "seshat-bi[mcp]" the
  <sub>★ 2 · Python · Apache-2.0 · pipx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install seshat-bi`</sub>
- **[us-all/airflow-mcp-server](https://github.com/us-all/airflow-mcp-server)** — Airflow REST API — 7 tools (DAG list, runs, task instances, log tails, trigger, clear). dag-health-rollup aggregation. Airflow 3.x /api/v2 + JWT (SimpleAuthManager); pin 0.1.x for Airflow 2.x. Read-only by default; trigger/clear write-gated
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @us-all/airflow-mcp`</sub>
- **[dockndevai/mcp-debezium](https://github.com/dockndevai/mcp-debezium)** — Debezium / Kafka Connect CDC connector monitoring &amp; lifecycle — access modes, connector allowlists, protected connectors, delete gating, and credential redaction. npx -y @dockndevai/mcp-debezium
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-debezium.git`</sub>
- **[dockndevai/mcp-kafka](https://github.com/dockndevai/mcp-kafka)** — Apache Kafka cluster, topic &amp; consumer-group monitoring (with per-partition and total lag) and management — access modes, topic allowlists, protected internal topics, delete gating. npx -y @dockndevai/mcp-kafka
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-kafka.git`</sub>
- **[sam1siam/astrofabric-mcp](https://github.com/sam1siam/astrofabric-mcp)** — Agentic AI for business intelligence: company and contact discovery, verification, enrichment, business signals, lists and governed delivery. Remote Streamable HTTP with OAuth or API keys; mission_agent by default, granular tools with ?tools=all
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g astrofabric`</sub>
- **[carrierone/verilexdata-mcp](https://github.com/carrierone/verilexdata-mcp)** — 20 structured datasets (NPI healthcare, SEC filings, OFAC sanctions, crypto whales, Polymarket signals, patents, economic indicators) via x402 pay-per-query with USDC. Free stats/sample endpoints, MCP + HTTP transport
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-03-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/carrierone/verilexdata-mcp.git`</sub>
- **[flexorch/flexorch-mcp](https://github.com/flexorch/flexorch-mcp)** — Convert unstructured business documents (PDF, DOCX, invoices, contracts, payroll) into structured, LLM-ready datasets with automatic classification, field extraction, PII masking (10+ locales), and quality scoring. 6 async MCP tools covering the full pipeline: submit → poll → extract → build → export JSONL/RAG/CSV. Install: pip install flexorch-mcp
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install flexorch-mcp`</sub>
- **[r3dz4r/datapulse-my](https://github.com/r3dz4r/datapulse-my)** — Trust layer for 418 official Malaysian public datasets — freshness, licence, provenance, drift and signed-evidence checks, with an offline-verifiable attestation chain. Remote streamable-http at https://mcp.data-pulse.my/mcp, no API key
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/r3dz4r/datapulse-my.git`</sub>
- **[saikiyusuke/registep-mcp](https://github.com/asicojp/registep-mcp)** — AI-powered POS &amp; sales analytics MCP server with 67 tools for Airレジ, スマレジ, and BASE EC integration. Provides store management, sales data querying, AI chat analysis, and weather correlation features
  <sub>★ 1 · TypeScript · source · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/saikiyusuke/registep-mcp.git`</sub>
- **[Younghef/nutriref-api](https://github.com/Younghef/nutriref-api)** — USDA FoodData Central nutrition for AI agents — pay-per-call in USDC on Base via x402. Four tools (search, detail, compare, recipe) at $0.001–$0.005 per call. No signup, no API keys; MCPB-packaged for one-click install
  <sub>★ 1 · Python · MIT · uv · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx nutriref-mcp`</sub>
- **[Leekangbum/networklytics-mcp](https://github.com/Leekangbum/networklytics-mcp)** — YouTube comment social network analysis (SNA): influencer centrality ranking, community detection (Louvain), sentiment analysis, and public JSON API for AI agents
  <sub>★ 1 · Python · pip · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install networklytics-mcp`</sub>
- **[equinoxaifinance-rgb/civicdataforge-mcp](https://github.com/equinoxaifinance-rgb/civicdataforge-mcp)** — Ten source-bound government-record evidence tools covering US STR permits, lodging licenses, property violations, healthcare exclusions, inspections, childcare licensing, EPA ECHO facilities, and Norway company evidence. Public metadata discovery; execution uses the caller's own Apify token over Streamable HTTP
  <sub>JavaScript · MIT · source · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/equinoxaifinance-rgb/civicdataforge-mcp.git`</sub>
- **[datanika-io/datanika-core](https://github.com/datanika-io/datanika-core/tree/master/datanika-mcp)** — Read-only-by-default MCP server for Datanika, the open-source ELT + dbt platform: browse connections, preview data, run and compile dbt transforms, monitor runs, and manage pipelines. 25 tools; opt-in --allow-write enables create/trigger
  <sub>Python · AGPL-3.0 · in-repo · pushed 2026-09-26</sub>
  <sub>`git clone https://github.com/datanika-io/datanika-core.git && cd datanika-core/datanika-mcp`</sub>
- **[greencalculus/greencalculus-mcp](https://github.com/greencalculus/greencalculus-mcp)** — Sourced greenhouse-gas emission factors and audit-traced carbon calculations (activity, embodied EN 15978, PCAF financed emissions) — every value returns with its exact source reference and data version, so answers are citable and reproducible. 16,673 factors, 12 tools. Install: npx -y greencalculus-mcp, or connect remotely at https://mcp.greencalculus.com. Free tier, no card
  <sub>JavaScript · MIT · source · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/greencalculus/greencalculus-mcp.git`</sub>

## end to end RAG platforms

- **[vectara/vectara-mcp](https://github.com/vectara/vectara-mcp)** — An MCP server for accessing Vectara's trusted RAG-as-a-service platform
  <sub>★ 30 · Python · Apache-2.0 · pip · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install vectara-mcp`</sub>
- **[poll-the-people/customgpt-mcp](https://github.com/Poll-The-People/customgpt-mcp)** — An MCP server for accessing all of CustomGPT.ai's anti-hallucination RAG-as-a-service API endpoints
  <sub>★ 5 · Python · MIT · docker · pushed 2025-10-21 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 -e CUSTOMGPT_API_BASE=https://app.customgpt.ai customgpt-mcp`</sub>
- **[notwhiteblank/scholar-rag-mcp](https://github.com/notwhiteblank/scholar-rag-mcp)** — Academic-paper knowledge base over local PDFs: MinerU parsing, metadata normalization, section annotation, Qdrant vector search with reranking, and context-safe paginated full-text reading. 11 tools including two-phase KB deletion; runs against local or OpenAI-compatible embedding/rerank/chat models (vLLM)
  <sub>★ 4 · Python · MIT · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx scholar-rag-mcp # download and start the MCP server (stdio)`</sub>
- **[gogabrielordonez/mcp-ragchat](https://github.com/gogabrielordonez/mcp-ragchat)** — Add RAG-powered AI chat to any website with one command. Local vector store, multi-provider LLM (OpenAI/Anthropic/Gemini), self-contained chat server and embeddable widget
  <sub>★ 2 · TypeScript · clone · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gogabrielordonez/mcp-ragchat`</sub>
- **[andyliszewski/grounding-ai](https://github.com/andyliszewski/grounding-ai)** — Build a searchable index from PDFs, EPUBs, and Word docs. Claude queries it via MCP and pulls grounded answers with exact page-and-section citations. Local-first, no cloud dependency
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install grounding-ai`</sub>
- **[zaharajabeen13-create/ai-rete-rag-mcp](https://github.com/zaharajabeen13-create/ai-rete-rag-mcp)** — Decisions the model doesn't make: a Rete rule engine returns the verdict, retrieval over your own policy documents explains it — so an explanation can't invent a threshold your rulebook doesn't have. Turn a written policy into draft rules that cite the sentence each encodes, save them as YAML, then decide; every verdict names the rule that fired, and you can ask why any rule didn't
  <sub>Python · MIT · uv · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx ai-rete-rag-mcp`</sub>

## Knowledge &amp; Memory

<sub>Entries 1–192 of 348. The rest are on this page's other parts, linked above and below.</sub>

- **[upstash/context7](https://github.com/upstash/context7)** — Up-to-date code documentation for LLMs and AI code editors
  <sub>★ 62.4k · TypeScript · MIT · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upstash/context7.git`</sub>
- **[vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)** — Hindsight: Agent Memory That Works Like Human Memory - Built for AI Agents to manage Long Term Memory
  <sub>★ 31k · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[skill-seekers/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)** — Transform 17 source types (docs, GitHub repos, PDFs, videos, Jupyter, Confluence, Notion, Slack/Discord) into AI-ready skills and RAG knowledge. 35 MCP tools for scraping, packaging, enhancing, and exporting to vector databases (Weaviate, Chroma, FAISS, Qdrant). Supports 16+ target platforms
  <sub>★ 15k · Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install skill-seekers`</sub>
- **[basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory)** — Persistent, local-first AI memory: a semantic knowledge graph of plain Markdown files that humans and LLMs both read and write. Works with any MCP client, with optional cloud sync and team workspaces
  <sub>★ 4k · Python · AGPL-3.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add basicmachines-co/basic-memory/skills`</sub>
- **[gamosoft/NoteDiscovery](https://github.com/gamosoft/NoteDiscovery)** — Self-hosted plain-markdown knowledge base with a built-in MCP server. Lets Claude Desktop, Cursor, and any MCP client search, read, create, edit, tag, and template notes — same vault that powers the web UI. Pure-stdlib client, no extra deps, MIT-licensed. Can run in Docker
  <sub>★ 2.8k · JavaScript · MIT · docker · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -d --name notediscovery -p 8000:8000 \`</sub>
- **[doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)** — Universal memory service providing semantic search, persistent storage, and autonomous memory consolidation
  <sub>★ 2k · Python · Apache-2.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-memory-service`</sub>
- **[bitbonsai/mcp-obsidian](https://github.com/bitbonsai/mcpvault)** — Universal AI bridge for Obsidian vaults using MCP. Provides safe read/write access to notes with 11 comprehensive methods for vault operations including search, batch operations, tag management, and frontmatter handling. Works with Claude, ChatGPT, and any MCP-compatible AI assistant
  <sub>★ 1.7k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector npx @bitbonsai/mcpvault@latest /path/to/your/vault`</sub>
- **[apecloud/ApeRAG](https://github.com/apecloud/ApeRAG)** — Production-ready RAG platform combining Graph RAG, vector search, and full-text search. Best choice for building your own Knowledge Graph and for Context Engineering
  <sub>★ 1.3k · Python · Apache-2.0 · helm · pushed 2026-09-12 · WSL2 · Linux · Docker</sub>
  <sub>`helm install aperag ./deploy/aperag --namespace default --create-namespace`</sub>
- **[vshulcz/deja-vu](https://github.com/vshulcz/deja-vu)** — Local memory layer over the session histories coding agents already write (Claude Code, Codex CLI, opencode): lexical search, recall tools, session-start auto-recall, secret redaction at index time, cross-machine sync over SSH
  <sub>★ 1k · Go · MIT · scoop · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop install deja-vu`</sub>
- **[chatmcp/mcp-server-chatsum](https://github.com/chatmcp/mcp-server-chatsum)** — Query and summarize your chat messages with AI prompts
  <sub>★ 1k · TypeScript · source · pushed 2024-12-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chatmcp/mcp-server-chatsum.git`</sub>
- **[CodeAbra/iai-personal-memory-engine](https://github.com/CodeAbra/iai-personal-memory-engine)** — Local memory daemon for any MCP-over-stdio client with three-tier storage (episodic/semantic/procedural). Own SQLite + hnswlib store (Hippo) with bge-small-en-v1.5, MIT-licensed community-detection reranking (MOSAIC), and sleep-cycle consolidation. AES-256-GCM encrypted at rest, no telemetry. Verbatim recall >=99% and post-contradiction Rescue@10 1.000 at honest scale. Ambient capture via shell ho
  <sub>★ 894 · Python · MIT · script · pushed 2026-09-16 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/CodeAbra/iai-personal-memory-engine/main/scripts/bootstrap.sh | bash`</sub>
- **[riponcm/projectmem](https://github.com/riponcm/projectmem)** — Local-first memory and judgment layer for AI coding agents. Captures issues, failed attempts, fixes, and decisions in readable Markdown + JSONL, re-injects them into future sessions, and warns at git commit before you repeat a mistake. 14 tools, works with Claude, Cursor, Antigravity, and Codex
  <sub>★ 834 · Python · MIT · pip · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install projectmem`</sub>
- **[agentic-mcp-tools/memora](https://github.com/agentic-box/memora)** — Persistent memory with knowledge graph visualization, semantic/hybrid search, cloud sync (S3/R2), and cross-session context management
  <sub>★ 726 · Python · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx wrangler d1 create memora-graph`</sub>
- **[mem0ai/mem0-mcp](https://github.com/mem0ai/mem0-mcp)** — A Model Context Protocol server for Mem0 that helps manage coding preferences and patterns, providing tools for storing, retrieving and semantically handling code implementations, best practices and technical documentation in IDEs like Cursor and Windsurf
  <sub>★ 662 · Python · Apache-2.0 · pip · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mem0-mcp-server`</sub>
- **[samvallad33/vestige](https://github.com/samvallad33/vestige)** — Local-first cognitive memory for AI agents. FSRS-6 scheduling, smart ingest, SQLite storage, portable sync, embedded dashboard, and optional Cognitive Sandwich hooks for Claude Code, Cursor, Codex, and other MCP clients
  <sub>★ 635 · Rust · AGPL-3.0 · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g vestige-mcp-server@latest`</sub>
- **[fabio-rovai/open-ontologies](https://github.com/fabio-rovai/open-ontologies)** — AI-native ontology engineering with 39 tools and 5 prompts for OWL/RDF/SPARQL. Validate, query, diff, lint, version, and govern knowledge graphs via Oxigraph triple store
  <sub>★ 538 · Rust · MIT · source · pushed 2026-09-22 · macOS · Linux</sub>
  <sub>`git clone https://github.com/fabio-rovai/open-ontologies.git`</sub>
- **[Ikalus1988/MisakaNet](https://github.com/Ikalus1988/MisakaNet)** — Agent failure memory network. Search 235+ verified debugging lessons from real engineering sessions. BM25 + SAG-Lite search, 3 tools (search, get_lesson, submit_usage), 5 resources, 3 guided prompts. Works with Claude Code, Cursor, and any MCP client. python3 scripts/mcp_server.py
  <sub>★ 510 · Python · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx @misaka-net/misakanet-setup`</sub>
- **[TeleAI-UAGI/telemem](https://github.com/TeleAI-UAGI/telemem)** — Long-term and multimodal memory for AI agents, usable as a drop-in replacement for Mem0. Character-isolated memory profiles, LLM-based semantic deduplication, FAISS + JSON dual storage, optional fully-local stack (Ollama/Qwen, no cloud), and video memory with ReAct-style QA. 8 tools. pip install "telemem[mcp]" then telemem-mcp
  <sub>★ 492 · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx telemem`</sub>
- **[juyterman1000/entroly](https://github.com/juyterman1000/entroly)** — Auditable context control plane and MCP server for AI coding agents. Compresses context 70–95% (BM25 + entropy + dep-graph knapsack), stabilizes prompt prefixes for provider cache discounts, routes easy tasks to cheaper models (RAVS Bayesian router), and verifies answers locally with WITNESS hallucination guard (0.844 AUROC, $0, ~3 ms). MemoryOS adds local budget-aware working/episodic/semantic me
  <sub>★ 469 · Python · Apache-2.0 · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g entroly`</sub>
- **[Beever-AI/beever-atlas](https://github.com/Beever-AI/beever-atlas)** — Open-source LLM knowledge base for teams. 28-tool native MCP server turns Slack/Discord/Teams/Mattermost chat into a typed knowledge graph + auto-generated wiki with cited answers, semantic search, expert finding, and decision tracing. BYO LLM via LiteLLM, Apache 2.0, on-prem via Docker
  <sub>★ 448 · Python · Apache-2.0 · clone · pushed 2026-09-10 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/beever-ai/beever-atlas.git`</sub>
- **[shinpr/mcp-local-rag](https://github.com/shinpr/mcp-local-rag)** — Privacy-first document search server running entirely locally. Supports semantic search over PDFs, DOCX, TXT, and Markdown files with LanceDB vector storage and local embeddings - no API keys or cloud services required
  <sub>★ 405 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-local-rag ingest ./docs/`</sub>
- **[graphlit-mcp-server](https://github.com/graphlit/graphlit-mcp-server)** — Ingest anything from Slack, Discord, websites, Google Drive, Linear or GitHub into a Graphlit project - and then search and retrieve relevant knowledge within an MCP client like Cursor, Windsurf or Cline
  <sub>★ 380 · TypeScript · MIT · npx · pushed 2026-01-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y graphlit-mcp-server`</sub>
- **[Goldentrii/AgentRecall](https://github.com/Goldentrii/AgentRecall-X)** — Persistent, compounding memory for AI agents across sessions. Uses the Intelligent Distance Protocol to surface the most contextually relevant past memories. Five tools: session_start, remember, recall, check, session_end. npx agent-recall-mcp
  <sub>★ 371 · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-recall-cli recall "topic" # terminal`</sub>
- **[CheMiguel23/MemoryMesh](https://github.com/CheMiguel23/MemoryMesh)** — Enhanced graph-based memory with a focus on AI role-play and story generation
  <sub>★ 353 · TypeScript · MIT · clone · pushed 2026-03-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CheMiguel23/memorymesh.git`</sub>
- **[varun29ankuS/shodh-memory](https://github.com/varun29ankuS/shodh-memory)** — Cognitive memory for AI agents with Hebbian learning, 3-tier architecture, and knowledge graphs. Single ~15MB binary, runs offline on edge devices
  <sub>★ 293 · Rust · Apache-2.0 · npx · pushed 2026-09-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @shodh/memory-mcp setup-hooks`</sub>
- **[ohad6k/emulo](https://github.com/ohad6k/emulo)** — Loads your personal profile, mined from your local Claude Code/Codex/OpenCode logs, so your agent works like you instead of a cold start. One tool, load_emulo_profile. Run with uvx emulo mcp
  <sub>★ 292 · HTML · MIT · npx · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add ohad6k/emulo@emulo`</sub>
- **[jinzcdev/markmap-mcp-server](https://github.com/jinzcdev/markmap-mcp-server)** — An MCP server built on markmap that converts Markdown to interactive mind maps. Supports multi-format exports (PNG/JPG/SVG), live browser preview, one-click Markdown copy, and dynamic visualization features
  <sub>★ 288 · TypeScript · MIT · npx · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @jinzcdev/markmap-mcp-server`</sub>
- **[lyonzin/knowledge-rag](https://github.com/lyonzin/knowledge-rag)** — Local RAG system for Claude Code with hybrid search (BM25 + semantic), cross-encoder reranking, markdown-aware chunking, query expansion, and 28 MCP tools. Runs entirely offline with zero external servers
  <sub>★ 286 · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add lyonzin/knowledge-rag`</sub>
- **[sachitrafa/YourMemory](https://github.com/sachitrafa/YourMemory)** — Persistent memory for AI agents with Ebbinghaus forgetting-curve decay, hybrid BM25+vector retrieval, and entity graph for multi-hop reasoning. Memories auto-prune by importance and recall rate. Built-in browser dashboard, multi-agent support, and yourmemory ask for zero-API-call local queries. pip install yourmemory
  <sub>★ 270 · Python · pip · pushed 2026-09-19 · macOS</sub>
  <sub>`pip install yourmemory`</sub>
- **[hannesrudolph/mcp-ragdocs](https://github.com/hannesrudolph/mcp-ragdocs)** — An MCP server implementation that provides tools for retrieving and processing documentation through vector search, enabling AI assistants to augment their responses with relevant documentation context
  <sub>★ 265 · TypeScript · MIT · source · pushed 2025-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hannesrudolph/mcp-ragdocs.git`</sub>
- **[l33tdawg/sage](https://github.com/l33tdawg/sage)** — Institutional memory for AI agents with real BFT consensus. 4 application validators vote on every memory before it's committed — no more storing garbage. 13 MCP tools, runs locally, works with any MCP-compatible model. Backed by 4 published research papers
  <sub>★ 252 · Go · Apache-2.0 · docker · pushed 2026-09-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name sage \`</sub>
- **[omega-memory/omega-memory](https://github.com/omega-memory/omega-memory)** — Persistent memory for AI coding agents with semantic search, auto-capture, cross-session learning, and intelligent forgetting. 28 MCP tools, local-first
  <sub>★ 218 · Python · Apache-2.0 · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install omega-memory[server] # Full install (memory + MCP server)`</sub>
- **[GistPad-MCP](https://github.com/lostintangent/gistpad-mcp)** — Use GitHub Gists to manage and access your personal knowledge, daily notes, and reusable prompts. This acts as a companion to https://gistpad.dev and the GistPad VS Code extension
  <sub>★ 208 · TypeScript · MIT · source · pushed 2026-01-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lostintangent/gistpad-mcp.git`</sub>
- **[alibaizhanov/mengram](https://github.com/alibaizhanov/mengram)** — Human-like memory layer for AI agents with semantic, episodic, and procedural memory. Claude Code hooks (auto-save, auto-recall, cognitive profile). 29 MCP tools, knowledge graph, smart triggers, multi-user isolation. Python &amp; JS SDKs
  <sub>★ 201 · Python · Apache-2.0 · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mengram-ai # or: npm install mengram-ai`</sub>
- **[roomi-fields/notebooklm-mcp](https://github.com/roomi-fields/notebooklm-mcp)** — Full automation of Google NotebookLM — Q&amp;A with citations, audio podcasts, video, content generation, source management, and notebook library. MCP + HTTP REST API
  <sub>★ 182 · TypeScript · MIT · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @roomi-fields/notebooklm-mcp@<pinned-version>`</sub>
- **[pi22by7/In-Memoria](https://github.com/pi22by7/In-Memoria)** — Persistent intelligence infrastructure for agentic development that gives AI coding assistants cumulative memory and pattern learning. Hybrid TypeScript/Rust implementation with local-first storage using SQLite + SurrealDB for semantic analysis and incremental codebase understanding
  <sub>★ 174 · Rust · MIT · npm · pushed 2025-12-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g in-memoria`</sub>
- **[0xshellming/mcp-summarizer](https://github.com/0xshellming/mcp-summarizer)** — AI Summarization MCP Server, Support for multiple content types: Plain text, Web pages, PDF documents, EPUB books, HTML content
  <sub>★ 167 · JavaScript · source · pushed 2025-02-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0xshellming/mcp-summarizer.git`</sub>
- **[entanglr/zettelkasten-mcp](https://github.com/entanglr/zettelkasten-mcp)** — A Model Context Protocol (MCP) server that implements the Zettelkasten knowledge management methodology, allowing you to create, link, and search atomic notes through Claude and other MCP-compatible clients
  <sub>★ 164 · Python · MIT · clone · pushed 2025-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/entanglr/zettelkasten-mcp.git`</sub>
- **[kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero)** — A connector for LLMs to work with collections and sources on your Zotero Cloud
  <sub>★ 164 · TypeScript · MIT · npm · pushed 2025-02-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-zotero`</sub>
- **[Patdolitse/piia-engram](https://github.com/Patdolitse/piia-engram)** — Persistent user identity across AI tools. Stores preferences, lessons, and decisions as local JSON; 13 core MCP tools share them with Claude Code, Cursor, Codex, and any MCP client. Knowledge governance (staging→verified), AES-256-GCM encryption, cross-tool sync. pip install piia-engram
  <sub>★ 162 · Python · AGPL-3.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install piia-engram`</sub>
- **[dnotitia/akb](https://github.com/dnotitia/akb)** — Organizational knowledge base for AI agents. Vault-scoped Markdown docs, structured PostgreSQL tables, and files unified by a URI graph. Hybrid semantic + BM25 search, Git-backed version history, multi-tenant ACL with public-share links. Works with Claude Code, Cursor, Windsurf via npx akb-mcp
  <sub>★ 160 · Python · docker · pushed 2026-09-24 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -v "$AKB_NATIVE_CONFIG_DIR:/installation" \`</sub>
- **[dcostenco/prism-mcp](https://github.com/dcostenco/prism-coder)** — Zero-config persistent memory for AI agents with local SQLite. Mind Palace web dashboard, time travel (rewind/replay sessions), agent telepathy (cross-client memory sharing), code mode templates, morning briefings, and progressive context loading. 25 tools, 6 resources, 4 prompts
  <sub>★ 157 · TypeScript · Apache-2.0 · npm · pushed 2026-09-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g prism-mcp-server`</sub>
- **[redleaves/context-keeper](https://github.com/redleaves/context-keeper)** — LLM-driven context and memory management with wide-recall + precise-reranking RAG architecture. Features multi-dimensional retrieval (vector/timeline/knowledge graph), short/long-term memory, and complete MCP support (HTTP/WebSocket/SSE)
  <sub>★ 155 · Go · MIT · clone · pushed 2026-01-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/redleaves/context-keeper.git`</sub>
- **[sheawinkler/ContextLattice](https://github.com/sheawinkler/ContextLattice)** — Private-by-default memory and context layer for agents with Go/Rust runtime, staged retrieval across fused data backends, and long-horizon context continuity
  <sub>★ 152 · Go · Apache-2.0 · brew · pushed 2026-09-10 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew tap sheawinkler/contextlattice`</sub>
- **[cameronrye/openzim-mcp](https://github.com/cameronrye/openzim-mcp)** — Modern, secure MCP server for accessing ZIM format knowledge bases offline. Enables AI models to search and navigate Wikipedia, educational content, and other compressed knowledge archives with smart retrieval, caching, and comprehensive API
  <sub>★ 139 · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @smithery/cli mcp add rye/openzim-mcp --client claude`</sub>
- **[ProfessionalWiki/MediaWiki-MCP-Server](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server)** — Read, search, and edit any MediaWiki wiki (Wikipedia, Fandom, corporate wikis) with OAuth and multi-wiki support. 50+ tools, including Semantic MediaWiki, Cargo, Wikibase, NeoWiki, and Bucket queries. Listed in the official MCP registry. npx @professional-wiki/mediawiki-mcp-server
  <sub>★ 134 · TypeScript · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx add-mcp @professional-wiki/mediawiki-mcp-server`</sub>
- **[deusXmachina-dev/memorylane](https://github.com/deusXmachina-dev/memorylane)** — Desktop app that captures screen activity via event-driven screenshots, stores AI-generated summaries and OCR text locally in SQLite, and exposes your activity history to AI assistants via MCP with semantic search, timeline browsing, and event detail retrieval
  <sub>★ 122 · TypeScript · GPL-3.0 · source · pushed 2026-09-14 · Win? · macOS</sub>
  <sub>`git clone https://github.com/deusXmachina-dev/memorylane.git`</sub>
- **[dat999zx/knowl](https://github.com/dat999zx/knowl)** — Persistent memory for Claude Code, Cursor and Codex where a replaced fact is retired at write time, so what an agent reads back is the current answer rather than the one that was true in March. Facts are typed and carry provenance and a review trail; nothing is deleted, it stops being current. Local SQLite, queries answered from a local replica and never sent to a server, no API keys. npx -y @dat9
  <sub>★ 111 · TypeScript · Apache-2.0 · npm · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @dat999zx/knowl`</sub>
- **[elvismdev/mem0-mcp-selfhosted](https://github.com/elvismdev/mem0-mcp-selfhosted)** — Self-hosted mem0 MCP server for Claude Code with Qdrant vector search, Neo4j knowledge graph, and Ollama embeddings. Zero-config OAT auth, split-model graph routing, session hooks for automatic cross-session memory, and 11 tools. Supports both Anthropic and fully local Ollama setups
  <sub>★ 108 · Python · MIT · source · pushed 2026-03-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/elvismdev/mem0-mcp-selfhosted.git`</sub>
- **[kunwar-shah/claudex](https://github.com/kunwar-shah/claudex)** — Persistent memory + FTS5 full-text search for Claude Code conversation history. Indexes ~/.claude/projects/ JSONL into SQLite, exposes 10 MCP tools (store/recall/search memories, list sessions, get summaries) plus prompts. Includes a web UI for visual exploration with themes and exports. Works with Claude Code, Cursor, Codex, Windsurf, and any MCP-compatible client. npm install -g @kunwarshah/clau
  <sub>★ 95 · JavaScript · MIT · npm · pushed 2026-06-20 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @kunwarshah/claudex [https://www.npmjs.com/package/@kunwarshah/claudex]`</sub>
- **[ragieai/mcp-server](https://github.com/ragieai/ragie-mcp-server)** — Retrieve context from your Ragie (RAG) knowledge base connected to integrations like Google Drive, Notion, JIRA and more
  <sub>★ 91 · JavaScript · MIT · npx · pushed 2026-02-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @ragieai/mcp-server --partition optional_partition_id`</sub>
- **[DomDemetz/claude-soul](https://github.com/DomDemetz/claude-soul)** — Self-improving learning engine for Claude Code. Extracts signals from every session (corrections, successes, confusion), runs periodic reflections, and evolves behavioral frameworks through evidence tiers (hypothesis → observed → validated). Frameworks that keep working get promoted, bad ones get retired. 9 MCP tools, automatic hooks, phase-adaptive learning. Single dependency, local-only. npx cla
  <sub>★ 90 · TypeScript · MIT · npm · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-soul@latest`</sub>
- **[arthurpanhku/Arthor-Agent](https://github.com/arthurpanhku/DocSentinel)** — MCP server for AI agent for cybersecurity: automate assessment of documents, questionnaires &amp; reports. Multi-format parsing, RAG knowledge base,Risks, compliance gaps, remediations.
  <sub>★ 87 · Python · MIT · clone · pushed 2026-09-23 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/arthurpanhku/DocSentinel.git`</sub>
- **[Pantheon-Security/notebooklm-mcp-secure](https://github.com/Pantheon-Security/notebooklm-mcp-secure)** — Security-hardened NotebookLM MCP with post-quantum encryption (ML-KEM-768), GDPR/SOC2/CSSF compliance, and 14 security layers. Query Google's Gemini-grounded research from Claude and AI agents
  <sub>★ 84 · TypeScript · MIT · source · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Pantheon-Security/notebooklm-mcp-secure.git`</sub>
- **[decisionnode/DecisionNode](https://github.com/decisionnode/DecisionNode)** — Record development decisions as structured JSON, embed as vectors via Gemini, and search semantically over MCP. Shared store across Claude Code, Cursor, Windsurf, and any MCP client. CLI + MCP server, local-only, free Gemini embedding tier
  <sub>★ 83 · TypeScript · MIT · npm · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g decisionnode`</sub>
- **[adelinamart/robrain](https://github.com/adelinamart/robrain)** — Self-hosted decision memory for AI coding agents. Passively captures architectural decisions with the alternatives you rejected (structured rejected[]), then warns the agent before it re-proposes a rejected approach. Postgres + pgvector; cross-tool across Claude Code, Cursor, Copilot, and Codex. Install: npx robrain up &amp;&amp; npx robrain install
  <sub>★ 81 · TypeScript · Apache-2.0 · npx · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx robrain@latest up # start Postgres + Perception from ghcr.io`</sub>
- **[dodopayments/contextmcp](https://github.com/dodopayments/context-mcp)** — Self-hosted MCP server that indexes documentation from various sources and serves it to AI Agents with semantic search
  <sub>★ 77 · TypeScript · Apache-2.0 · npx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx contextmcp init my-docs-mcp`</sub>
- **[teolex2020/AuraSDK](https://github.com/teolex2020/aura-memory)** — Persistent cognitive memory for Claude Desktop. Sub-ms recall, offline, encrypted
  <sub>★ 77 · Rust · MIT · source · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/teolex2020/AuraSDK.git`</sub>
- **[cdeust/Cortex](https://github.com/cdeust/Cortex)** — Persistent memory for Claude Code grounded in computational neuroscience (41 cited papers). Thermodynamic decay, hippocampal-cortical consolidation, predictive-coding write gate, WRRF retrieval. PostgreSQL + pgvector, 33 MCP tools, 7 lifecycle hooks. Benchmarked 97.8% R@10 on LongMemEval. claude plugin marketplace add cdeust/Cortex
  <sub>★ 73 · Python · MIT · source · pushed 2026-09-26 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/cdeust/Cortex.git`</sub>
- **[tenequm/pond](https://github.com/tenequm/pond)** — Lossless archive and search for AI agent sessions across clients, exposed to agents over MCP
  <sub>★ 73 · Rust · Apache-2.0 · scoop · pushed 2026-09-26 · Win · WSL2 · macOS · Linux</sub>
  <sub>`scoop bucket add tenequm https://github.com/tenequm/scoop-bucket # Windows scoop install tenequm/pond`</sub>
- **[vbcherepanov/total-agent-memory](https://github.com/vbcherepanov/total-agent-memory)** — Persistent local memory for coding agents: temporal knowledge graph with fact invalidation, procedural memory, episodic recall, AST codebase ingest and cross-project analogy. 74 tools, 9 IDEs, and zero LLM or network calls in the default hot path. Reproducible benchmarks — LongMemEval R@5 95.1%, LoCoMo 0.607, BEAM 1M 0.448. pip install total-agent-memory
  <sub>★ 72 · Python · MIT · npx · pushed 2026-09-24 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx -y total-agent-memory connect claude-code`</sub>
- **[kunickiaj/codemem](https://github.com/kunickiaj/codemem)** — Persistent coding memory across sessions, machines, and teammates. Provides MCP tools for searching and managing memories, optional cross-machine sync, and project sharing. OpenCode, Claude Code, and Codex integrations add automatic capture and context injection
  <sub>★ 71 · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codemem`</sub>
- **[zcag/tela](https://github.com/zcag/tela)** — Self-hostable, markdown-native team wiki with a built-in MCP server: agents search, read, and write your wiki pages (ranked Postgres full-text + semantic search, backlink traversal). Plus Atlas, which auto-generates a cited, coverage-checked wiki from your git repos and Jira. Go + Postgres. npx tela-mcp
  <sub>★ 69 · Go · AGPL-3.0 · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/zcag/tela.git`</sub>
- **[Battam1111/Myco](https://github.com/Battam1111/Myco)** — Agent-first cognitive substrate with 18 manifest-driven verbs (germinate / eat / assimilate / sporulate / traverse / immune / molt / …) and 25 lint dimensions enforcing contract invariants mechanically (R1–R7). Cross-session / cross-project memory via a self-validating filesystem graph — AST + markdown-link derived, not embedding-based. Provider-agnostic by design: MP1/MP2 dims forbid LLM-SDK impo
  <sub>★ 65 · Rust · MIT · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Battam1111/Myco.git`</sub>
- **[tomohiro-owada/devrag](https://github.com/tomohiro-owada/devrag)** — Lightweight local RAG MCP server for semantic vector search over markdown documents. Reduces token consumption by 40x with sqlite-vec and multilingual-e5-small embeddings. Supports filtered search by directory and filename patterns
  <sub>★ 64 · Go · source · pushed 2026-04-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/tomohiro-owada/devrag.git`</sub>
- **[writerslogic/scrivener-mcp](https://github.com/writerslogic/scrivener-mcp)** — Connect Scrivener 3 writing projects to Claude and other AI assistants. 47 tools for document management, writing analysis, semantic search, character/plot memory, and content enhancement. Progressive skill loading, relationship engine with HMS triplets, and JS fallback for offline semantic search. npm i -g scrivener-mcp
  <sub>★ 62 · TypeScript · AGPL-3.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g scrivener-mcp`</sub>
- **[bh-rat/context-awesome](https://github.com/bh-rat/context-awesome)** — MCP server for querying 8,500+ curated awesome lists (1M+ items) and fetching the best resources for your agent
  <sub>★ 59 · TypeScript · MIT · npm · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g context-awesome`</sub>
- **[ccf/agentcairn](https://github.com/ccf/agentcairn)** — Local-first agent memory: a plain-Markdown Obsidian vault is the source of truth, with a rebuildable DuckDB index for hybrid BM25 + vector + graph recall. Non-lossy capture with secret redaction; works across Claude Code, Codex, Cursor, and any MCP host. uvx agentcairn
  <sub>★ 59 · Python · Apache-2.0 · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ccf/agentcairn --skill agentcairn-setup -g`</sub>
- **[ZengLiangYi/ChatCrystal](https://github.com/ZengLiangYi/ChatCrystal)** — Local-first AI PKM memory server for coding conversations. Imports Claude Code, Cursor, Codex CLI, Trae, and GitHub Copilot chats into notes, semantic search, tag graphs, Markdown exports, and reusable MCP memory. npx -y chatcrystal mcp
  <sub>★ 58 · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g chatcrystal`</sub>
- **[JinyangWang27/people-context](https://github.com/JinyangWang27/people-context)** — Local-first memory for AI agents about the people in your life: explainable identity resolution, relationships, roles, facts, interactions, reminders, and communication guidance in one SQLite file you own. Imports are review-gated, sensitive disclosure is operator-gated, and ordinary operation makes no network calls. uvx --from people-context people-context
  <sub>★ 56 · Python · MIT · uv · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from people-context pctx demo --reset`</sub>
- **[SecurityRonin/docx-mcp](https://github.com/SecurityRonin/docx-mcp)** — Read and edit Word (.docx) documents with track changes, comments, footnotes, and structural validation. The only MCP server combining w:ins/w:del tracked changes, threaded comments, and footnotes with OOXML-level paraId validation and document auditing. 18 tools, Python 3.10+
  <sub>★ 55 · Python · MIT · pip · pushed 2026-08-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install docx-mcp-server`</sub>
- **[roampal-ai/roampal-core](https://github.com/roampal-ai/roampal-core)** — Outcome-based persistent memory for AI coding tools. Memories that help get promoted, memories that mislead get demoted. Works with Claude Code and OpenCode via hooks + MCP
  <sub>★ 51 · Python · Apache-2.0 · pip · pushed 2026-08-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install roampal`</sub>
- **[tstockham96/engram](https://github.com/tstockham96/engram)** — Intelligent agent memory with semantic recall, automatic consolidation, contradiction detection, and bi-temporal knowledge graph. 80% on LOCOMO benchmark using 96% fewer tokens than full-context approaches
  <sub>★ 47 · TypeScript · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g engram-sdk`</sub>
- **[pinecone-io/assistant-mcp](https://github.com/pinecone-io/assistant-mcp)** — Connects to your Pinecone Assistant and gives the agent context from its knowledge engine
  <sub>★ 45 · Rust · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector -- docker run -i --rm -e PINECONE_API_KEY -e PINECONE_ASSISTANT_HOST pinecone/assistant-mcp`</sub>
- **[DollhouseMCP/mcp-server](https://github.com/DollhouseMCP/mcp-server)** — One-line installable MCP server that adds reusable customization elements — personas, skills, templates, agents, memory, and ensembles (collected customization tools) — to any MCP Client application. Dynamic permissioning for safe AI operations, a robust validation architecture, versioning, and a public collection of shareable content. Install: npx @dollhousemcp/mcp-server@latest --web
  <sub>★ 44 · TypeScript · AGPL-3.0 · npx · pushed 2026-09-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @dollhousemcp/mcp-server@latest --web`</sub>
- **[Abhigyan-Shekhar/Waggle-mcp](https://github.com/Abhigyan-Shekhar/Waggle-mcp)** — Persistent graph memory for AI agents. Drop a conversation turn in via observe_conversation() and facts are auto-extracted, stored as typed graph nodes with local semantic embeddings (no API key). Supports temporal queries ("what did we decide last week?"), conflict detection, and context priming. One-command setup with waggle-mcp init. SQLite locally, Neo4j in production
  <sub>★ 44 · Python · Apache-2.0 · pipx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install waggle-mcp`</sub>
- **[contextstream/mcp-server](https://github.com/contextstream/mcp-server)** — Universal persistent memory for AI coding tools. Semantic code search, knowledge graphs, impact analysis, and decision tracking. 90.0% on LongMemEval-S. Works across Cursor, Claude Code, Windsurf, and any MCP client. npx -y @contextstream/mcp-server
  <sub>★ 43 · Rust · MIT · npx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @contextstream/mcp-server@latest setup`</sub>
- **[Wuesteon/lean-memory](https://github.com/Wuesteon/lean-memory)** — Embedded, local-first agent memory in a single SQLite file per namespace (vec0 + FTS5 hybrid retrieval). ADD-only history queryable as-of any past time; offline sleep-time maintenance stages dedupe/summarize/evict proposals a human reviews. No Docker, no server, no cloud key. pip install 'lean-memory[mcp]'
  <sub>★ 42 · Python · Apache-2.0 · pip · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lean-memory`</sub>
- **[BetaBots-LLC/callimachus](https://github.com/BetaBots-LLC/callimachus)** — Local index and hybrid search (SQLite FTS5 + on-device vector KNN) over your AI coding-agent conversation history across 11 tools (Claude Code, Codex, Cursor, and more). Exposes search_threads, search_current_project, recent_threads, and get_thread so any agent can recall its own past work
  <sub>★ 40 · Rust · AGPL-3.0 · cargo · pushed 2026-07-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --path apps/desktop/src-tauri --bin callimachus-mcp`</sub>
- **[max-ramas/rms-memory-mcp](https://github.com/max-ramas/rms-memory-mcp)** — Local-first persistent memory for AI coding agents. Hybrid vector + full-text search (LanceDB + Tantivy), separate Markdown and Tree-sitter code indexes, per-project isolated vaults shared across IDEs (Cursor, Zed, Claude Code, Codex), bounded recall with abstain-on-low-confidence
  <sub>★ 39 · Rust · MIT · psh · pushed 2026-09-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/max-ramas/rms-memory-mcp/master/scripts/install.ps1 | iex`</sub>
- **[pallaprolus/mendeley-mcp](https://github.com/pallaprolus/mendeley-mcp)** — MCP server for Mendeley reference manager. Search your library, browse folders, get document metadata, search the global catalog, and add papers to your collection
  <sub>★ 39 · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector mendeley-mcp`</sub>
- **[linxule/lotus-wisdom-mcp](https://github.com/linxule/lotus-wisdom-mcp)** — Contemplative problem-solving using the Lotus Sutra's wisdom framework. Multi-perspective reasoning with skillful means, non-dual recognition, and meditation pauses. Available as local stdio or remote Cloudflare Worker
  <sub>★ 34 · TypeScript · MIT · source · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/linxule/lotus-wisdom-mcp.git`</sub>
- **[nonatofabio/local-faiss-mcp](https://github.com/nonatofabio/local_faiss_mcp)** — Local FAISS vector database for RAG with document ingestion (PDF/TXT/MD/DOCX), semantic search, re-ranking, and CLI tools for indexing and querying
  <sub>★ 34 · Python · MIT · pip · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install local-faiss-mcp`</sub>
- **[kage-core/Kage](https://github.com/kage-core/Kage)** — Verified, git-native memory for coding agents. Memory is plain JSON packets committed in your repo, each checked against the code it cites — hallucinated citations rejected at write, stale or changed memory withheld at recall, plus diff-time stale-catch. Local-only (BM25 + vectors), no account, no API key. npx -y @kage-core/kage-graph-mcp install
  <sub>★ 33 · TypeScript · GPL-3.0 · npx · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @kage-core/kage-graph-mcp install`</sub>
- **[oomkapwn/enquire-mcp](https://github.com/oomkapwn/enquire-mcp)** — Long-term memory for AI agents (Claude Code/Desktop, Cursor, ChatGPT, Codex, OpenClaw) backed by a local Obsidian markdown vault. Hybrid retrieval (BM25 + ML embeddings + BGE reranker, RRF-fused), HNSW + int8 quantization, agentic RAG (HyDE + sub-question), GraphRAG-light (Louvain wikilink community detection), standalone Obsidian Bases, PDFs + Tesseract OCR. 46 tools, 19 MCP prompts, MIT, SLSA L2
  <sub>★ 33 · TypeScript · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @oomkapwn/enquire-mcp`</sub>
- **[Shweta-Mishra-ai/tokenmizer](https://github.com/Shweta-Mishra-ai/tokenmizer)** — Graph-structured session memory for LLMs. Local OpenAI-compatible proxy that extracts tasks, decisions, and files into a typed knowledge graph, auto-checkpoints before context overflow, and resumes any session in ~250 tokens. 6 MCP tools including why_decision (traces why a decision changed, with reasons and evidence). pip install tokenmizer
  <sub>★ 32 · Python · MIT · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "tokenmizer[anthropic,cache]"`</sub>
- **[markmhendrickson/neotoma](https://github.com/markmhendrickson/neotoma)** — Deterministic state layer for AI agents. Stores versioned entities (contacts, tasks, transactions, decisions) with immutable observations, full provenance, and schema-first extraction. Local-first SQLite, cross-client memory across Claude, Cursor, ChatGPT, and OpenClaw. Website
  <sub>★ 32 · HTML · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g neotoma`</sub>
- **[majiayu000/remem](https://github.com/majiayu000/remem)** — Local-first persistent memory for Claude Code and Codex. Hooks capture sessions automatically, an LLM distills them into SQLite (optional SQLCipher encryption), and recall stays auditable via MCP, REST, and CLI with FTS + optional embeddings. Single Rust binary. npm install -g @remem-ai/remem
  <sub>★ 31 · Rust · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @remem-ai/remem`</sub>
- **[TT-Wang/cortex-plugin](https://github.com/TT-Wang/memem)** — Persistent, self-evolving memory plugin for Claude Code. Background miner extracts durable lessons (decisions, conventions, bug fixes) from completed sessions via Claude Haiku, stores them as human-readable markdown in an Obsidian vault, and assembles query-tailored context briefings at session start. Local-first, no cloud, no API keys. Self-healing install via uv bootstrap shim, /cortex-doctor pr
  <sub>★ 31 · Python · MIT · clone · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TT-Wang/memem.git`</sub>
- **[doobidoo/MCP-Context-Provider](https://github.com/doobidoo/MCP-Context-Provider)** — Static server that provides persistent tool-specific context and rules for AI models
  <sub>★ 30 · TypeScript · Apache-2.0 · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://codeberg.org/doobidoo/MCP-Context-Provider.git`</sub>
- **[rps321321/obsidian-mcp-pro](https://github.com/rps321321/obsidian-mcp-pro)** — Feature-complete Obsidian vault MCP server with 23 tools and 3 resources. Full-text search, note CRUD, frontmatter queries, tag management, backlinks, graph traversal (BFS up to 5 hops), orphan/broken link detection, and canvas support. Auto-detects vault, path traversal protection, MIT licensed
  <sub>★ 30 · TypeScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y obsidian-mcp-pro install`</sub>
- **[nicholasglazer/gnosis-mcp](https://github.com/nicholasglazer/gnosis-mcp)** — Zero-config MCP server for searchable documentation. Loads markdown into SQLite (default) or PostgreSQL with FTS5/tsvector keyword search and optional pgvector hybrid semantic search
  <sub>★ 29 · Python · MIT · uv · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx gnosis-mcp ingest ./docs/`</sub>
- **[IgorGanapolsky/mcp-memory-gateway](https://github.com/IgorGanapolsky/ThumbGate)** — Pre-action gates that prevent AI coding agents from repeating known mistakes. Captures explicit feedback, auto-promotes failures into prevention rules, and enforces them via hooks
  <sub>★ 27 · JavaScript · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx thumbgate init # Phase 1: hooks only`</sub>
- **[kael-bit/engram-rs](https://github.com/kael-bit/engram-rs)** — Hierarchical memory engine for AI agents with automatic decay, promotion, semantic dedup, and self-organizing topic tree. Single Rust binary, zero external dependencies
  <sub>★ 27 · Rust · MIT · psh · pushed 2026-03-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/kael-bit/engram-rs/main/install.ps1 | iex`</sub>
- **[wazionapps/nexo](https://github.com/wazionapps/nexo)** — Cognitive memory for AI agents with Atkinson-Shiffrin memory model (STM/LTM/sensory register), semantic RAG, Ebbinghaus decay, trust scoring, and 76+ MCP tools
  <sub>★ 27 · Python · source · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wazionapps/nexo.git`</sub>
- **[knaisoma/data-olympus](https://github.com/knaisoma/data-olympus)** — Governance-grade project knowledge MCP server for coding agents. Git-native Markdown knowledge base with proposed vs accepted guidance, validity windows, supersession chains, and status-aware retrieval of current in-force decisions and standards. pip install data-olympus
  <sub>★ 26 · Python · Apache-2.0 · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from data-olympus data-olympus --help`</sub>
- **[mnemoverse/mcp-memory-server](https://github.com/mnemoverse/mcp-memory-server)** — Hosted memory that learns and forgets — feedback re-ranks what helps, recall fades by recency, similar memories consolidate. One key across Claude, Cursor, VS Code &amp; ChatGPT
  <sub>★ 25 · TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mnemoverse/mcp-memory-server`</sub>
- **[pomazanbohdan/memory-mcp-1file](https://github.com/pomazanbohdan/memory-mcp-1file)** — A self-contained Memory server with single-binary architecture (embedded DB &amp; models, no dependencies). Provides persistent semantic and graph-based memory for AI agents
  <sub>★ 24 · Rust · MIT · npx · pushed 2026-09-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y memory-mcp-1file@0.9.2 -- --help`</sub>
- **[unibaseio/membase-mcp](https://github.com/unibaseio/membase-mcp)** — Save and query your agent memory in distributed way by Membase
  <sub>★ 24 · Python · clone · pushed 2025-05-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/unibaseio/membase-mcp.git`</sub>
- **[zensation-ai/zenbrain](https://github.com/zensation-ai/zenbrain)** — Seven-layer agent memory over MCP. zenbrain_store routes what it is given: a general statement becomes a semantic fact, a narrated event an episode, a sequence of instructions a procedure. zenbrain_recall searches every layer and tags each result with the layer it came from; zenbrain_consolidate runs one sleep-like maintenance pass that promotes repeated episodes into facts and decays stale slots.
  <sub>★ 24 · TypeScript · Apache-2.0 · clone · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zensation-ai/zenbrain.git`</sub>
- **[celiums/celiums-memory](https://github.com/terrizoaguimor/celiums-memory)** — Cognitive memory engine with 5,100+ knowledge modules, circadian rhythm awareness, and emotional state tracking (PAD model). Hybrid search (PostgreSQL + Qdrant vectors + Valkey cache), per-user memory isolation, and multi-protocol support (MCP, REST, OpenAI, LangChain, A2A). npx @celiums/memory Website
  <sub>★ 23 · Rust · Apache-2.0 · clone · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/terrizoaguimor/celiums-memory.git`</sub>
- **[hermes-labs-ai/fidelis](https://github.com/hermes-labs-ai/fidelis)** — Local-first memory for Codex, Claude Code, and other MCP clients. Four tools provide verbatim recall, query, health, and context-sensitive orientation through zero-LLM retrieval by default. Install fidelis-memory from PyPI, run fidelis init, then register the MCP server with the client
  <sub>★ 23 · Python · Apache-2.0 · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hermes-labs-ai/fidelis.git`</sub>
- **[sgx-labs/statelessagent](https://github.com/sgx-labs/statelessagent)** — Memory with provenance tracking — records where agent knowledge originated and detects when sources change. 17 MCP tools for session handoffs, decisions, semantic search, and knowledge graph. Works across Claude Code, Cursor, Windsurf, Codex CLI, and Gemini CLI. Single Go binary, SQLite + vector search, fully local
  <sub>★ 23 · Go · psh · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://statelessagent.com/install.ps1 | iex`</sub>
- **[s60yucca/mnemos](https://github.com/s60yucca/mnemos)** — Persistent memory engine for AI coding agents. Stores architecture decisions, bug root causes, and project conventions across sessions. Single Go binary with embedded SQLite, FTS5 search, context assembly within token budgets, and autopilot setup for Claude Code, Kiro, and Cursor
  <sub>★ 22 · Go · MIT · npx · pushed 2026-07-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @s60yucca/mnemos setup claude`</sub>
- **[SaravananJaichandar/world-model-mcp](https://github.com/SaravananJaichandar/world-model-mcp)** — Temporal knowledge graph for codebases. Captures decision traces, links test failures to code changes, learns co-edit patterns, predicts regression risk, and enforces learned constraints at the edit boundary via a PreToolUse hook. 22 MCP tools, 9 SQLite databases with FTS5, supports Python/TypeScript/JavaScript/Solidity/Go/Rust/Java. Install via pip install world-model-mcp
  <sub>★ 22 · Python · MIT · pip · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U world-model-mcp`</sub>
- **[whynowlab/jarvis-orb](https://github.com/TheStack-ai/jarvis-orb)** — Persistent 4-tier AI memory (episodic, semantic, project, procedural) with temporal scoring, contradiction detection, entity tracking, and real-time desktop visualization orb
  <sub>★ 22 · Python · MIT · psh · pushed 2026-04-28 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/thestack-ai/jarvis-orb/main/install.ps1 | iex`</sub>
- **[aliasunder/vault-cortex](https://github.com/aliasunder/vault-cortex)** — Standalone MCP server for Obsidian vaults — hybrid search, notes &amp; files, memory, tasks, OAuth 2.1. Run locally, self-host, or one-click deploy for remote access
  <sub>★ 21 · TypeScript · MIT · npx · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx vault-cortex@latest init`</sub>
- **[JamesANZ/memory-mcp](https://github.com/JamesANZ/memory-mcp)** — An MCP server that stores and retrieves memories from multiple LLMs using MongoDB. Provides tools for saving, retrieving, adding, and clearing conversation memories with timestamps and LLM identification
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2025-12-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @jamesanz/memory-mcp`</sub>
- **[VonderVuflya/Yggdrasil](https://github.com/VonderVuflya/Yggdrasil)** — Durable, local-first memory for AI coding agents over MCP. Zero-dependency (pure Python + SQLite/FTS5), curated and semantically de-duped — you own the data as plain rows. Works with Claude Code, Codex &amp; any MCP host. uvx --from yggdrasil-memory ygg mcp
  <sub>★ 21 · Python · AGPL-3.0 · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx yggdrasil-memory install`</sub>
- **[KVANTRA-dev/NOUZ-MCP](https://github.com/Semiotronika/NOUZ-MCP)** — Semantic knowledge graph for Obsidian. Three modes (pure graph / semantic classification / strict hierarchy), local embeddings, sign classification via cosine similarity to user-defined cores, bottom-up core_mix aggregation, semantic bridge discovery, and drift detection. pip install nouz-mcp
  <sub>★ 20 · Python · MIT · pip · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install nouz-mcp`</sub>
- **[olgasafonova/mediawiki-mcp-server](https://github.com/olgasafonova/mediawiki-mcp-server)** — Connect to any MediaWiki wiki (Wikipedia, Fandom, corporate wikis). 33+ tools for search, read, edit, link analysis, revision history, and Markdown conversion. Supports stdio and HTTP transport
  <sub>★ 20 · Go · MIT · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/olgasafonova/mediawiki-mcp-server.git`</sub>
- **[dengls24/annota](https://github.com/dengls24/annota)** — AI-powered paper annotation MCP server. Reads papers, highlights key findings with semantic color coding, explains formulas, and writes structured reading notes — all saved back to Zotero. Features two-phase workflow for large PDFs (63–80% context savings) and batch annotations
  <sub>★ 19 · Python · MIT · clone · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dengls24/annota.git`</sub>
- **[GetCacheOverflow/CacheOverflow](https://github.com/GetCacheOverflow/CacheOverflow)** — AI agent knowledge marketplace where agents share solutions and earn tokens. Search, publish, and unlock previously solved problems to reduce token usage and computational costs
  <sub>★ 19 · TypeScript · MIT · source · pushed 2026-02-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GetCacheOverflow/CacheOverflow.git`</sub>
- **[jagoff/memo](https://github.com/jagoff/memo)** — Local-first semantic memory server with hybrid search, plain Markdown storage, MLX or CPU embeddings, contradiction detection, time-travel history, synthesis, and cross-machine git sync
  <sub>★ 19 · Python · MIT · uv · pushed 2026-09-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install mlx-memo`</sub>
- **[Destrayon/Connapse](https://github.com/Destrayon/Connapse)** — #️⃣ 🏠 🍎 🪟 🐧 - Self-hosted knowledge backend for AI agents with hybrid vector + keyword search, container-isolated indexes, and 11 MCP tools. .NET, Docker-ready
  <sub>★ 18 · C# · MIT · clone · pushed 2026-09-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Destrayon/Connapse.git`</sub>
- **[dshakes/distil](https://github.com/dshakes/distil)** — Reversibly compress a large tool output to a recoverable 8-hex handle over stdio, expand it on demand, and report a local token/dollar savings ledger
  <sub>★ 18 · Python · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx distil-llm wrap -- <agent>`</sub>
- **[hjqcan/GoodMemory](https://github.com/hjqcan/GoodMemory)** — Local-first, auditable memory layer for Codex, Claude Code, and MCP clients. Stores scoped user/project memory in SQLite or Postgres, exposes read-only recall, trace, stats, and artifact tools by default, and supports opt-in governed writeback with review, forget, and audit controls. Published as io.github.hjqcan/goodmemory in the official MCP Registry
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g goodmemory@0.8.0`</sub>
- **[JinNing6/Noosphere](https://github.com/JinNing6/Noosphere)** — Digital consciousness repository and community MCP server. Upload epiphanies, decisions, warnings, and patterns as consciousness payloads, then retrieve them via semantic telepathic search. Features 3D interactive consciousness globe, soul imprint authentication, and automated content moderation via CI/CD
  <sub>★ 18 · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from noosphere-mcp noosphere-query "React Three Fiber mobile glowing node tap selects wrong instance"`</sub>
- **[louis030195/easy-obsidian-mcp](https://github.com/louis030195/easy-obsidian-mcp)** — Interact with Obsidian vaults for knowledge management. Create, read, update, and search notes. Works with local Obsidian vaults using filesystem access
  <sub>★ 18 · TypeScript · source · pushed 2025-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/louis030195/easy-obsidian-mcp.git`</sub>
- **[paladini/mcp-me](https://github.com/paladini/mcp-me)** — Digital identity layer for AI — your bio, career, skills, interests, and projects always available to every AI tool. Auto-generates profile from 342+ public APIs (GitHub, Medium, Strava, Goodreads, etc.), 13 real-time plugins (Spotify, Last.fm, Steam), YAML-based profiles with privacy-first local storage. Works with Claude Desktop, Cursor, Windsurf, and any MCP client
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-me`</sub>
- **[smith-and-web/obsidian-mcp-server](https://github.com/smith-and-web/obsidian-mcp-server)** — SSE-enabled MCP server for remote Obsidian vault management with 29 tools for notes, directories, frontmatter, tags, search, and link operations. Docker-ready with health monitoring
  <sub>★ 18 · TypeScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/smith-and-web/obsidian-mcp-server.git`</sub>
- **[ihorponom/agentpack](https://github.com/ihorponom/agentpack)** — Repo-native task continuity for AI coding agents: a reviewed task-state ledger (decisions, dead ends, evidence, checkpoints) in .agentpack/ that any next session or client resumes from
  <sub>★ 17 · TypeScript · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentpack-cli`</sub>
- **[besslframework-stack/project-tessera](https://github.com/besslframework-stack/project-tessera)** — Local workspace memory for Claude Desktop. Indexes your documents (Markdown, CSV, session logs) into a vector store with hybrid search, cross-session memory, auto-learn, and knowledge graph visualization. Zero external dependencies — fastembed + LanceDB, no Ollama or Docker required. 15 MCP tools
  <sub>★ 17 · Python · AGPL-3.0 · uv · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from project-tessera tessera setup`</sub>
- **[SecurityRonin/alaya](https://github.com/SecurityRonin/alaya)** — Neuroscience-inspired memory engine for AI agents. Stores episodes, consolidates knowledge through a Bjork-strength lifecycle (strengthening, transformation, forgetting), and builds a personal knowledge graph with emergent categories, preferences, and semantic recall. Local SQLite, zero config, 10 MCP tools. Install via npx alaya-mcp
  <sub>★ 17 · Rust · MIT · pip · pushed 2026-07-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install alaya-memory`</sub>
- **[syndicalt/zaxy](https://github.com/syndicalt/zaxy)** — Event-sourced agent memory on a hash-chained append-only log with an embedded temporal knowledge graph (Kuzu, no sidecar). Cited Memory Checkout context, salience-based forgetting that attenuates instead of deleting, compaction-recovery hooks for Claude Code, token-budgeted checkout, and review-gated consolidation. 47 MCP tools with an 8-tool core profile default. pip install zaxy-memory Docs
  <sub>★ 17 · Python · MIT · pipx · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install zaxy-memory`</sub>
- **[20alexl/claude-engram](https://github.com/20alexl/claude-engram)** — Persistent memory and session intelligence for Claude Code. Auto-tracks mistakes, decisions, and context via hooks. Mines session history for patterns and cross-session search. Loop detection, pre-edit warnings, context compaction survival. Runs locally with Ollama
  <sub>★ 16 · Python · MIT · clone · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/20alexl/claude-engram.git`</sub>
- **[JamesANZ/cross-llm-mcp](https://github.com/JamesANZ/cross-llm-mcp)** — An MCP server that enables cross-LLM communication and memory sharing, allowing different AI models to collaborate and share context across conversations
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cross-llm-mcp`</sub>
- **[AliceLJY/recallnest](https://github.com/AliceLJY/recallnest)** — Persistent memory MCP server for AI coding agents (Claude Code, Codex, Gemini CLI). Hybrid retrieval (vector + BM25), cross-encoder reranking, knowledge graph with PPR traversal, session checkpoint/resume, and multi-scope isolation. Local-first with LanceDB + SQLite, zero external dependencies
  <sub>★ 15 · TypeScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g recallnest # install globally`</sub>
- **[epicsagas/alcove](https://github.com/epicsagas/alcove)** — MCP server that gives AI coding agents on-demand access to private project docs via BM25 ranked search. One setup for Claude Code, Cursor, Codex, Gemini CLI, and more. Docs stay private, never in public repos
  <sub>★ 15 · Rust · Apache-2.0 · cargo · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install alcove --features full-cross`</sub>
- **[dot-RealityTest/obsidian-codex-mcp](https://github.com/aka-kika/kika-obsidian-mcp)** — Local-first Obsidian vault MCP server for Codex, Claude Desktop, and other MCP clients. Works directly with markdown files, no Obsidian plugin, API key, cloud service, or running Obsidian app required. Includes read-only mode, backup-on-write, path isolation, and setup examples
  <sub>★ 15 · Python · MIT · clone · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aka-kika/kika-obsidian-mcp.git`</sub>
- **[junnnnnw00/obsidian-everywhere](https://github.com/junnnnnw00/obsidian-everywhere)** — Graph-native Obsidian vault server with 31 tools for search, backlinks, n-hop neighborhoods, structured and paginated reads, and safe file, partial, and bulk edits with dry-run and rollback. Works with Codex, ChatGPT, Claude, and any MCP client. npx -y obsidian-everywhere /path/to/vault
  <sub>★ 15 · TypeScript · MIT · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y obsidian-everywhere demo`</sub>
- **[remembra-ai/remembra](https://github.com/remembra-ai/remembra)** — Persistent memory layer for AI agents with entity resolution, PII detection, AES-256-GCM encryption at rest, and hybrid search. 100% on LoCoMo benchmark. Self-hosted
  <sub>★ 15 · Python · MIT · pipx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install --force 'remembra[mcp]>=0.16'`</sub>
- **[Mnemosyne-OS/Mnemosyne-Neural-OS](https://github.com/Mnemosyne-OS/Mnemosyne-Neural-OS)** — Memory the human governs: vaults separated by domain (code, notes, journal) on your own machine, hybrid retrieval (BM25 fused with vectors by RRF), and a declared vault list, so a vault left out cannot be read by mistake. Also reads what the OTHER coding agents on this machine wrote to disk, and flags when two are live in the same git worktree. Needs the Mnemosyne OS desktop app running. npx -y @m
  <sub>★ 15 · TypeScript · npm · pushed 2026-09-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @mnemosyne_os/forge`</sub>
- **[ashlesh-t/cognirepo](https://github.com/ashlesh-t/cognirepo)** — Persistent memory and codebase context for AI coding agents. FAISS vector store, AST reverse index with O(1) symbol
  <sub>★ 14 · Python · MIT · pipx · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install cognirepo`</sub>
- **[Krzysztof318/MailFathom](https://github.com/Krzysztof318/MailFathom)** — #️ 🏠 🐧 - Security-first, self-hosted AI brain for email. Synchronizes IMAP mailboxes into user-owned PostgreSQL and exposes tools for listing, searching, reading, and cited questions across the archive. Supports local chat and embedding models through OpenAI-compatible endpoints; each deployment exposes its own Streamable HTTP /mcp endpoint
  <sub>★ 14 · C# · AGPL-3.0 · clone · pushed 2026-09-25 · Win · WSL2? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Krzysztof318/MailFathom.git`</sub>
- **[renezander030/agentic-task-system](https://github.com/renezander030/agentic-task-system)** — Turns your task manager into agent memory: hybrid (dense + sparse + keyword, RRF) retrieval over TickTick or an Obsidian vault via a six-method adapter contract. MCP server + CLI, no vector DB to build or maintain. npm i -g @reneza/ats-cli
  <sub>★ 14 · JavaScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/renezander030/agentic-task-system.git`</sub>
- **[maxkuminov/obsidian-mcp](https://github.com/maxkuminov/obsidian-mcp)** — Self-hosted MCP server for Obsidian with semantic + full-text search over PostgreSQL/pgvector, wikilink graph traversal, atomic note CRUD, OAuth 2.0, and a self-describing vault guide
  <sub>★ 14 · Python · MIT · clone · pushed 2026-09-25 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/maxkuminov/obsidian-mcp.git`</sub>
- **[michielinksee/linksee-memory](https://github.com/michielinksee/linksee-memory)** — Local-first cross-agent memory with a 6-layer structure, Ebbinghaus-style forgetting curve, and drift detection that catches when code diverges from past decisions. One SQLite file shared across Claude Code, Cursor, Codex, and Gemini — no account or API key. npx linksee-memory
  <sub>★ 14 · TypeScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y linksee-memory map where README.md # this file belongs to the README node — and what it touches`</sub>
- **[papersflow-ai/papersflow-mcp](https://github.com/papersflow-ai/papersflow-mcp)** — Hosted MCP server by PapersFlow for academic research with 7 specialized AI agents and 474M+ papers from Semantic Scholar and OpenAlex. Literature search, citation verification, citation graph exploration, and autonomous deep research workflows
  <sub>★ 14 · MIT · source · pushed 2026-03-11</sub>
  <sub>`git clone https://github.com/papersflow-ai/papersflow-mcp.git`</sub>
- **[TyKolt/kremis](https://github.com/TyKolt/kremis)** — Deterministic knowledge graph MCP server. Single binary, zero LLM/embedding calls in the bridge, BLAKE3 state hashing, canonical KREX export for byte-identical audit. Local-first via redb (ACID). Alpha
  <sub>★ 14 · Rust · Apache-2.0 · docker · pushed 2026-09-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -i --rm kremis`</sub>
- **[vornicx/Midas](https://github.com/vornicx/Midas)** — Local-first memory for long-horizon AI agents with no LLM at ingest — $0 per message, zero data egress, verbatim source-traceable recall. Typed belief revision, selective forgetting, and a provenance guard that blocks memory-justified destructive actions unless user-confirmed. One midas init wires Claude Code, Cursor, Codex, and 6 more clients to one shared SQLite memory; local web inspector and h
  <sub>★ 14 · Python · MIT · npx · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y midas-memory-mcp`</sub>
- **[Wynelson94/longhand](https://github.com/Wynelson94/longhand)** — Persistent local memory for Claude Code. Indexes every session JSONL verbatim into SQLite + ChromaDB for semantic recall (~126ms) across your entire history. Never summarizes, zero API calls, 17 MCP tools including fuzzy recall, deterministic replay_file, and git-aware recall_project_status. Published on PyPI as longhand and registered in the MCP Registry
  <sub>★ 14 · Python · MIT · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install longhand`</sub>
- **[yaminbkk/NexusMem](https://github.com/yaminbkk/NexusMem)** — Correlates a failed shell command (with its exit code) to whatever later fixed it, alongside git diffs and docs — recorded locally in SQLite, nothing sent anywhere
  <sub>★ 14 · TypeScript · MIT · npx · pushed 2026-09-23 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx nexusmem init`</sub>
- **[hubinoretros/deep-thinker](https://github.com/nachosystems/deep-thinker)** — Advanced cognitive reasoning MCP server with DAG-based thought graph, 5 reasoning strategies (sequential, dialectic, parallel, analogical, abductive), metacognitive engine with stuck detection, multi-factor confidence scoring, self-critique, knowledge integration, and thought pruning. npx deep-thinker
  <sub>★ 13 · TypeScript · MIT · npm · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g deep-thinker`</sub>
- **[Smart-AI-Memory/empathy-framework](https://github.com/Smart-AI-Memory/empathy-framework)** — Five-level AI collaboration system with persistent memory and anticipatory capabilities. MCP-native integration for Claude and other LLMs with local-first architecture via MemDocs
  <sub>★ 13 · HTML · Apache-2.0 · pip · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install empathy-framework[developer]`</sub>
- **[bluzername/lennys-quotes](https://github.com/bluzername/lennys-quotes)** — Query 269 episodes of Lenny's Podcast for product management wisdom. Search 51,000+ transcript segments with YouTube timestamps. Perfect for PRDs, strategy, and PM career advice
  <sub>★ 12 · TypeScript · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g lennys-podcast-wisdom`</sub>
- **[yonro/memory-os-cli](https://github.com/yonro/memory-os-cli)** — XMemo is user-owned memory for AI agents over a hosted Streamable HTTP MCP endpoint. Save, search, recall, and manage scoped memories across Copilot, Claude, ChatGPT, IDEs, and CLIs. https://xmemo.dev/mcp
  <sub>★ 12 · JavaScript · MIT · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yonro/memory-os-cli.git`</sub>
- **[grooverLab/fable](https://github.com/grooverLab/fable)** — MCP server over your Claude Code transcript history — full-text + semantic search, byte-identical thread recall, durable /remember facts. Local SQLite, stdlib-only
  <sub>★ 12 · Python · MIT · pipx · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/grooverLab/fable`</sub>
- **[Lians-ai/Lians](https://github.com/Lians-ai/Lians)** — Bitemporal agent memory with deterministic fact supersession, point-in-time recall, memory lineage, conflict tracking, and tamper-evident audit trails. Supports self-hosted and managed deployments. uvx --from 'lians-sdk[mcp]' lians-mcp
  <sub>★ 12 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install "lians-sdk[local]"`</sub>
- **[mattjoyce/mcp-persona-sessions](https://github.com/mattjoyce/mcp-persona-sessions)** — Enable AI assistants to conduct structured, persona-driven sessions including interview preparation, personal reflection, and coaching conversations. Built-in timer management and performance evaluation tools
  <sub>★ 12 · Python · GPL-3.0 · clone · pushed 2026-03-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mattjoyce/mcp-persona-sessions.git`</sub>
- **[rwnalds/engram](https://github.com/rwnalds/engram)** — Second brain your agents read and write, over a git-backed markdown vault. Authority-aware search ranks superseded and archived notes below live ones (from frontmatter, no vector DB), so agents quote the current doc, not the dead one. Per-agent read-only or write tokens, a git audit trail of every change with diffs, a knowledge-graph dashboard, and Obsidian compatibility
  <sub>★ 12 · TypeScript · MIT · source · pushed 2026-08-14 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rwnalds/engram.git`</sub>
- **[STiFLeR7/memex](https://github.com/STiFLeR7/memex)** — Developer context continuity system. Watches your git repos and builds a temporal knowledge graph of modules, symbols, decisions, and open problems via Graphiti + Neo4j, then serves it to any AI coding agent over MCP. Every edge carries a validity window and a confidence score that decays over time. 12 tools across read and write. Install via npx -y stifler-memex-mcp. MIT licensed
  <sub>★ 12 · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx stifler-memex-mcp <cmd>`</sub>
- **[Cavinooo/claude-find](https://github.com/Cavinooo/claude-find)** — Pull Deep Memory from across your Claude Code Sessions — when you need it
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx claude-find setup`</sub>
- **[n24q02m/mnemo-mcp](https://github.com/n24q02m/mnemo)** — Persistent AI memory with SQLite hybrid search (FTS5 + semantic). Built-in Qwen3 embedding, rclone sync across machines. Zero config, no cloud, no limits
  <sub>★ 11 · Python · Apache-2.0 · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mnemo-mcp`</sub>
- **[xChuCx/agent-memory](https://github.com/xChuCx/agent-memory)** — Git-native project memory for coding agents: Markdown source of truth committed to your repo, reviewable staged updates (review --diff → apply), secret/PII-safe, branch-aware — no cloud, no vector DB
  <sub>★ 11 · Go · Apache-2.0 · npx · pushed 2026-09-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @xchucx/agent-memory --help`</sub>
- **[AkashGoenka/coldstart](https://github.com/AkashGoenka/coldstart)** — Codebase memory for coding agents, with no embeddings and no API key. A deterministic AST index answers "which files are relevant to this task?" in milliseconds, and agents write durable notes about the repo that are content-hash checked — a note flags itself stale the moment the code it describes changes. Notes are markdown inside the repo, so they commit and review alongside your code. npm i -g
  <sub>★ 10 · TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @cstart/coldstart`</sub>
- **[lockstep-team-agent/lockstep](https://github.com/lockstep-team-agent/lockstep)** — Shared decision memory for teams building with AI coding agents: captures each engineering decision once, ranks it by blast radius, and briefs every MCP agent before it acts, so agents stop shipping conflicting changes. Apache-2.0. Install: npm i -g lockstep-cli
  <sub>★ 10 · TypeScript · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx lockstep-cli onboard`</sub>
- **[ailenshen/apple-notes-mcp](https://github.com/ailenshen/apple-notes-mcp)** — Read and write Apple Notes with bidirectional Markdown conversion. Fast SQLite queries for listing/searching, AppleScript + native import for full CRUD. Supports stdio and Streamable HTTP transports
  <sub>★ 10 · TypeScript · MIT · npx · pushed 2026-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @ailenshen/apple-notes-mcp@latest --http`</sub>
- **[mlorentedev/hive](https://github.com/mlorentedev/hive)** — On-demand Obsidian vault access via MCP. Adaptive context loading (67-82% token savings), full-text and ranked search, health checks, auto git commit, and worker delegation to cheaper models. 10 tools, works with any MCP client
  <sub>★ 10 · Python · MIT · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install --upgrade hive-vault # >= 1.32.0`</sub>
- **[TeamSafeAI/LIFE](https://github.com/TeamSafeAI/LIFE)** — Persistent identity architecture for AI agents. 16 MCP servers covering drives, emotional relationships, semantic memory with decay, working threads, learned patterns, journal, genesis (identity discovery), creative collision engine, forecasting, and voice. Zero dependencies beyond Python 3.8. Built across 938 conversations
  <sub>★ 10 · Python · MIT · source · pushed 2026-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TeamSafeAI/LIFE.git`</sub>
- **[tribal-memory/tribal](https://github.com/tribal-memory/tribal)** — Self-hosted semantic memory server, served over MCP, for an engineering team's tribal knowledge: the tacit decisions and hard-won reasoning behind the code, captured once and kept queryable for the team and the agents they work with. Postgres-backed (pgvector)
  <sub>★ 10 · Rust · npx · pushed 2026-08-06 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx skills add tribal-memory/skills`</sub>
- **[billy12151/memory-arbiter-mcp](https://github.com/billy12151/memory-arbiter-mcp)** — AI enhancement middleware: precise retrieval replaces full-memory loading (~80%+ token cut), rule-based conflict arbitration with explainable reasons, and one local SQLite shared across Claude Code/Codex/Cursor/ZCode. Local-first, zero cloud, MIT. pip install memory-arbiter-mcp
  <sub>★ 9 · Python · Apache-2.0 · pip · pushed 2026-09-25 · WSL2 · macOS? · Linux</sub>
  <sub>`pip install "memory-arbiter-mcp[vec,semantic-local]" # core + sqlite-vec + local GGUF runtime`</sub>
- **[michael-denyer/memory-mcp](https://github.com/michael-denyer/memory-mcp)** — Two-tier memory with hot cache (instant injection) and cold semantic search. Auto-promotes frequently-used patterns, extracts knowledge from Claude outputs, and organizes via knowledge graph relationships
  <sub>★ 9 · Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install hot-memory-mcp # or: pip install hot-memory-mcp`</sub>
- **[mnlt/wellread](https://github.com/mnlt/wellread)** — Shared research cache across AI agents. Hit → instant answer from verified sources. Miss → your research saves the next dev's tokens. npx wellread, free
  <sub>★ 9 · TypeScript · AGPL-3.0 · npx · pushed 2026-04-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx wellread`</sub>
- **[leonardsellem/hypermnesic](https://github.com/leonardsellem/hypermnesic)** — Git-first memory for AI agents: Markdown files are truth, the index is disposable, and writes are reviewable commits. Ships 7 MCP tools (hybrid search, read_note, build_context, resolve, think, list_folders, and a scope-gated commit_note write) over a Streamable HTTP endpoint, plus a CLI and a read-only Obsidian companion
  <sub>★ 9 · Python · AGPL-3.0 · uv · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install hypermnesic`</sub>
- **[dahshanlabs/klypix-mcp](https://github.com/dahshanlabs/klypix-mcp)** — Shared, versioned project brain for coding agents: one brain.klypix file committed with the repo holds current decisions, corrections that supersede (archived, never deleted), evidence anchors that flag drift when cited code changes, and open questions. Sessions declare their task and files and are warned about exact-file overlap. Lifecycle hooks for Claude Code; MCP config + rules for Codex, Curs
  <sub>★ 8 · JavaScript · Apache-2.0 · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx klypix-mcp install`</sub>
- **[catfish-1234/sessionmem](https://github.com/catfish-1234/sessionmem)** — Local-first memory layer for AI coding assistants. Watches your coding sessions and injects a compact summary at the start of each new session. No cloud, no account, just a SQLite file on your machine. Works with Claude Code, Cursor, Cline, Windsurf, and any other MCP host
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g sessionmem`</sub>
- **[cryptosquanch/legends-mcp](https://github.com/AytuncYildizli/legends-mcp)** — Chat with 36 legendary founders &amp; investors (Elon Musk, Warren Buffett, Steve Jobs, CZ). AI personas with authentic voices, frameworks, and principles. No API key required
  <sub>★ 8 · TypeScript · MIT · source · pushed 2025-12-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cryptosquanch/legends-mcp.git`</sub>
- **[HBarefoot/engram](https://github.com/HBarefoot/engram)** — Local-first persistent memory for AI agents. SQLite + local embeddings (all-MiniLM-L6-v2), hybrid semantic + FTS5 recall, secret detection, and contradiction handling. 6 MCP tools (remember, recall, forget, feedback, context, status) over stdio. Zero cloud, no API keys, fully offline. Works with Claude Desktop/Code, Cursor, and Windsurf. npm install -g @hbarefoot/engram
  <sub>★ 8 · JavaScript · MIT · npm · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @hbarefoot/engram`</sub>
- **[hyunjae-labs/lore](https://github.com/hyunjae-labs/lore)** — Semantic search across Claude Code conversations. Hybrid vector + keyword search with Reciprocal Rank Fusion, fully local, background indexing, project-selective
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g getlore`</sub>
- **[memstate-ai/memstate-mcp](https://github.com/memstate-ai/memstate-mcp)** — Versioned, structured memory for AI agents. Stores facts as keypaths with full version history, automatic conflict detection, and O(1) token retrieval
  <sub>★ 8 · TypeScript · Apache-2.0 · source · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/memstate-ai/memstate-mcp.git`</sub>
- **[NicolasPrimeau/artel](https://github.com/NicolasPrimeau/artel)** — Self-hosted coordination layer for AI agent fleets. Shared semantic memory, tasks, agent-to-agent messages, session handoffs, and a background archivist that synthesizes cross-agent knowledge. Any HTTP client participates — Claude Code, AutoGen, raw scripts
  <sub>★ 8 · Python · MIT · source · pushed 2026-09-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/NicolasPrimeau/artel.git`</sub>
- **[rushikeshmore/CodeCortex](https://github.com/rushikeshmore/CodeCortex)** — Persistent codebase knowledge layer for AI coding agents. Pre-digests codebases into structured knowledge (symbols, dependency graphs, co-change patterns, architectural decisions) via tree-sitter native parsing (28 languages) and serves via MCP. 14 tools, ~85% token reduction. Works with Claude Code, Cursor, Codex, and any MCP client
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codecortex-ai --legacy-peer-deps`</sub>
- **[XuebinMa/AIWiki](https://github.com/XuebinMa/AIWiki)** — Search and read AiWiki, an encyclopedia of AI-coding pitfalls and LLM privacy protection written from the AI's first-person perspective. 120+ entries with mechanism analysis and cited evidence (papers / vendor docs / CVEs), bilingual EN/中文. Content fetched live from the site index, never stale. npx -y aiwiki-mcp
  <sub>★ 8 · MDX · CC-BY-SA-4.0 · source · pushed 2026-09-15</sub>
  <sub>`git clone https://github.com/XuebinMa/AIWiki.git`</sub>
- **[NORTHTEKDevs/genome](https://github.com/NORTHTEKDevs/genome)** — Fully-local persistent agent memory with zero LLM calls (~10 ms writes, works air-gapped). Semantic recall over local SQLite with bi-temporal fact tracking; benchmarked at accuracy parity with Mem0 at ~1,000x lower ingest cost, nulls published. Tools: remember, recall, forget, reset_memories. pip install "genome-memory[mcp]" then genome-mcp
  <sub>★ 7 · Python · Apache-2.0 · pip · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "genome-memory[mcp]"`</sub>
- **[g1itchbot8888-del/agent-memory](https://github.com/g1itchbot8888-del/agent-memory)** — Three-layer memory system for agents (identity/active/archive) with semantic search, graph relationships, conflict detection, and LearningMachine. Built by an agent, for agents. No API keys required
  <sub>★ 7 · Python · MIT · pip · pushed 2026-02-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openclaw-memory`</sub>
- **[hifriendbot/cogmemai-mcp](https://github.com/hifriendbot/cogmemai-mcp)** — Persistent cognitive memory for Claude Code. Cloud-first with semantic search, AI-powered extraction, and project scoping. Zero local databases
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cogmemai-mcp setup`</sub>
- **[DanceNitra/inspeximus](https://github.com/DanceNitra/inspeximus)** — Persistent agent memory with a first-class correction channel: supersede or revert a fact so recall stops returning the stale value, an echo guard that blocks a restated old value from resurrecting it, and receipted erasure (a signed, content-free tombstone that makes a deletion provable). No LLM on the write path, zero dependencies, the core in one file, 73 MCP tools. uvx --from "inspeximus[mcp]"
  <sub>★ 7 · Python · MIT · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "inspeximus[crypto]"`</sub>
- **[udjin-labs/mnemostack](https://github.com/udjin-labs/mnemostack)** — Durable hybrid memory for AI agents. Combines vector search, BM25, temporal retrieval, and optional Memgraph knowledge graph via reciprocal rank fusion. 6 MCP tools: health, search, answer, feedback, graph_query, graph_add_triple. Self-hosted with Qdrant backend. 82.5% strict accuracy on LoCoMo benchmark. pip install 'mnemostack[mcp]'
  <sub>★ 7 · Python · Apache-2.0 · pip · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install 'mnemostack[mcp]'`</sub>
- **[jayasukuv11-beep/agenthelm](https://github.com/jayasukuv11-beep/agenthelm)** — Shared, versioned memory and governance control plane for AI coding agents. Compiler pipeline resolves architectural decision conflicts across Claude Code, Cursor, and custom agent fleets. npx -y agenthelm-mcp
  <sub>★ 6 · TypeScript · MIT · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agenthelm-sdk`</sub>
- **[afairai/afair](https://github.com/afairai/afair)** — The open-source, self-organizing memory for all your AI tools. Three frozen verbs (remember/recall/observe); background agents extract entities, resolve conflicts, consolidate and decay, so the vault structures itself instead of only storing. Append-only, content-addressed, encrypted (SQLCipher), single-tenant, self-hostable. uv run python -m afair
  <sub>★ 6 · Python · AGPL-3.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/afairai/afair.git`</sub>
- **[timmx7/acheron-mcp-server](https://github.com/timmx7/acheron-mcp-server)** — Cross-surface persistent memory for Claude. Bridges context between Claude Chat, Code, and Cowork via local SQLite with full-text search. Save decisions, preferences, and insights in one surface, retrieve them in any other
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/timmx7/acheron-mcp-server.git`</sub>
- **[cg3-llc/prior_mcp](https://github.com/cg3inc/prior_mcp)** — Shared knowledge base where AI agents exchange proven solutions — including failed approaches, so your agent skips the dead ends. Smaller models get instant access to frontier-model discoveries. Free to search indefinitely when feedback is provided on results. Website
  <sub>★ 6 · JavaScript · npm · pushed 2026-05-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g @cg3/prior-node`</sub>
- **[conversation-handoff-mcp](https://github.com/trust-delta/conversation-handoff-mcp)** — Hand off conversation context between Claude Desktop projects and across MCP clients. Memory-based, no file clutter
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g conversation-handoff-mcp`</sub>
- **[ErebusEnigma/context-memory](https://github.com/ErebusEnigma/context-memory)** — Persistent, searchable context storage across Claude Code sessions using SQLite FTS5. Save sessions with AI-generated summaries, two-tier full-text search, checkpoint recovery, and a web dashboard
  <sub>★ 6 · Python · MIT · clone · pushed 2026-02-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ErebusEnigma/context-memory.git`</sub>
- **[dl4rce/flaiwheel](https://github.com/dl4rce/flaiwheel)** — Self-hosted memory and governance layer for AI coding agents. 28 MCP tools with structured knowledge capture, hybrid search (semantic + BM25 + cross-encoder reranking), behavioral documentation nudges, cold-start codebase analyzer, and git-native storage. Single Docker container, zero cloud dependencies
  <sub>★ 6 · Python · docker · pushed 2026-09-11 · macOS</sub>
  <sub>`docker run --rm --entrypoint sh flaiwheel:latest -c \`</sub>
- **[krimto-labs/krimto](https://github.com/krimto-labs/krimto)** — Open-source team memory layer for AI coding agents. Markdown files in git as storage, a user→team→org hierarchy as the access primitive, and one cross-vendor MCP server (Claude Code, Cursor, Codex, Gemini CLI). Hybrid SQLite + sqlite-vec retrieval. Apache-2.0
  <sub>★ 6 · TypeScript · Apache-2.0 · npx · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @krimto-labs/krimto init`</sub>
- **[leesgit/passbaton](https://github.com/leesgit/passbaton)** — Zero-config session continuity for Claude Code, OpenAI Codex CLI &amp; Google Gemini CLI, sharing one local db. Auto context injection on start, compaction handover, and 24 tools for memory, tasks, solutions, and a knowledge graph. Multilingual semantic search (94+ languages), 100% local, $0 API cost. npm i -g passbaton
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g passbaton # installs the new package`</sub>
- **[mercurialsolo/counsel-mcp](https://github.com/mercurialsolo/counsel-mcp)** — Connect AI agents to the Counsel API for strategic reasoning, multi-perspective debate analysis, and interactive advisory sessions
  <sub>★ 6 · JavaScript · MIT · npx · pushed 2026-01-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y counsel-mcp-server http --port 3000`</sub>
- **[penfieldlabs/penfield-mcp](https://github.com/penfieldlabs/penfield-mcp)** — Penfield: persistent memory with hybrid search (BM25 + vector + graph), 24 relationship types for knowledge graphs, context checkpoints for cognitive handoff, artifact storage, and personality system. Works across Claude, Cursor, Windsurf, and any MCP client
  <sub>★ 6 · Dockerfile · AGPL-3.0 · source · pushed 2026-04-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/penfieldlabs/penfield-mcp.git`</sub>
- **[pipeshub-ai/mcp-server](https://github.com/pipeshub-ai/mcp-server)** — Permission-aware enterprise search and RAG that gives agents context from your business apps (Google Workspace, Microsoft 365, Slack, Jira, and others). Streamable HTTP or local stdio (npx @pipeshub-ai/mcp). Official registry: io.github.pipeshub-ai/mcp
  <sub>★ 6 · TypeScript · Apache-2.0 · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector node ./bin/mcp-server.js start --server-url PIPESHUB_INSTANCE_URL --bearer-auth YOUR_BEARER_TOKEN`</sub>
- **[The-40-Thieves/obsidian-tc](https://github.com/The-40-Thieves/obsidian-tc)** — Model-agnostic, agent-ready Obsidian MCP server with RBAC, SLSA provenance, and native search: 163 tools across 31 domains, multi-vault, pluggable embeddings, zero-config start with npx -y obsidian-tc /path/to/vault
  <sub>★ 6 · TypeScript · AGPL-3.0 · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g obsidian-tc`</sub>

Page **2** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · **2** · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · [7](mcp-servers-punkpeye-7.md) — [continue on page 3 →](mcp-servers-punkpeye-3.md)

---

Snapshot 2026-09-26. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
