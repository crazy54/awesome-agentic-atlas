# MCP Servers (punkpeye)

A collection of MCP servers.

Curated by **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

4,242 entries · 4,216 distinct repos · 60 sections

[← back to the mega list](../README.md)

Page **5** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · **5** · [6](mcp-servers-punkpeye-6.md) · [7](mcp-servers-punkpeye-7.md) — [continue on page 6 →](mcp-servers-punkpeye-6.md)

## Contents

- [Monitoring](#monitoring) (87)
- [Embedded System](#embedded-system) (19)
- [Industrial &amp; IoT](#industrial--iot) (5)
- [Home Automation](#home-automation) (9)
- [Security &amp; Governance](#security--governance) (1)
- [Identity](#identity) (2)
- [Communication](#communication) (166)
- [Support &amp; Service Management](#support--service-management) (15)
- [Customer Data Platforms](#customer-data-platforms) (19)
- [Marketing](#marketing) (109)
- [Social Media](#social-media) (59)
- [Translation Services](#translation-services) (6)
- [Conversational AI](#conversational-ai) (6)
- [Browser Automation](#browser-automation) (109)
- [Art &amp; Culture](#art--culture) (88)
- [Gaming](#gaming) (69)

## Monitoring

<sub>Entries 42–87 of 87. The rest are on this page's other parts, linked above and below.</sub>

- **[ejcho623/agent-breadcrumbs](https://github.com/ejcho623/agent-breadcrumbs)** — Unified agent work logging and observability across ChatGPT, Claude, Cursor, Codex, and OpenClaw with config-first schemas and pluggable sinks
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-02-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y agent-breadcrumbs`</sub>
- **[yshngg/pmcp](https://github.com/yshngg/prometheus-mcp-server)** — A Prometheus Model Context Protocol Server
  <sub>★ 4 · Go · Apache-2.0 · go · pushed 2026-09-14 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/yshngg/prometheus-mcp-server@latest`</sub>
- **[zhaoyue722/llm-usage-mcp](https://github.com/zhaoyue722/llm-usage-mcp)** — Local-first LLM API cost tracker. Captures usage across Anthropic, OpenAI, Qwen, and DeepSeek into a local SQLite ledger and exposes spend queries, provider comparison, and recommendations as MCP tools — with first-class Chinese-provider support (CNY→USD). Install: uvx llm-usage-mcp
  <sub>★ 4 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install llm-usage-mcp # or: pipx install llm-usage-mcp`</sub>
- **[antonio-mello-ai/mcp-redis-monitor](https://github.com/antonio-mello-ai/mcp-redis-monitor)** — Read-only Redis monitoring — queue depths by type, Celery queue status, connected clients, server/memory stats, and key counts per database. 5 tools, built with FastMCP. Install: uvx mcp-redis-monitor
  <sub>★ 3 · Python · MIT · uv · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-redis-monitor`</sub>
- **[dragogargo/mcp-sysmon](https://github.com/dragogargo/mcp-sysmon)** — Local system monitoring — CPU, memory, swap, disk, network, and process management. Find resource-hungry processes, diagnose performance issues, and kill processes via AI
  <sub>★ 3 · Python · MIT · pip · pushed 2026-04-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-sysmon`</sub>
- **[gjenkins20/unofficial-fortimonitor-mcp-server](https://github.com/gjenkins20/unofficial-fortimonitor-mcp-server)** — Unofficial FortiMonitor v2 API integration with 241 tools for server monitoring, outages, maintenance, metrics, notifications, and more
  <sub>★ 3 · Python · MIT · source · pushed 2026-07-21 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gjenkins20/unofficial-fortimonitor-mcp-server.git`</sub>
- **[log-logn/langfuse-mcp-java](https://github.com/Log-LogN/langfuse-mcp-java)** — Query Langfuse traces, debug exceptions, analyze sessions, scores, datasets, schema, observations and manage prompts. Full observability toolkit for LLM applications. (https://github.com/langfuse/langfuse)
  <sub>★ 3 · Java · MIT · source · pushed 2026-03-25 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Log-LogN/langfuse-mcp-java.git`</sub>
- **[Oluwatunmise-olat/mcp-server-logs-sieve](https://github.com/Oluwatunmise-olat/mcp-server-logs-sieve)** — Query, summarize, and trace logs in plain English across GCP Cloud Logging, AWS CloudWatch, Azure Log Analytics, Grafana Loki, and Elasticsearch
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-04-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-server-logs-sieve@latest --provider gcp`</sub>
- **[ThinkneoAI/mcp-server](https://github.com/thinkneo-ai/mcp-server)** — ThinkNEO Control Plane — Enterprise AI governance MCP server with runtime guardrails, observability, AI FinOps, and agent lifecycle control
  <sub>★ 3 · Python · Apache-2.0 · clone · pushed 2026-07-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/thinkneo-ai/mcp-server.git`</sub>
- **[arnavranjan005/mcp-telemetry](https://github.com/arnavranjan005/mcp-telemetry)** — Socket.IO-style telemetry for MCP servers. Instrument a tool call with a few lines of mcp-telemetry-sdk, and telemetry_subscribe streams its live progress (steps, logs, cost, done) to any connected MCP client via notifications/progress — no polling, and a job started in one session can be watched from a completely different one
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-telemetry-server`</sub>
- **[clamp-sh/mcp](https://github.com/clamp-sh/mcp)** — AI-native web analytics. Query pageviews, top pages, referrers, countries, devices, and custom events. Create conversion funnels and alerts
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/clamp-sh/mcp.git`</sub>
- **[FailEcho/failecho](https://github.com/FailEcho/failecho)** — Cross-agent failure intelligence. Before an agent retries a failed tool call, check_tool_failure reports whether other agents are hitting the same failure right now and which recovery actually worked, with a Wilson-score confidence. Privacy-by-schema: no prompts, keys, or payloads stored. Hosted remote server at https://failecho.com/mcp, or self-host
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx failecho-mcp`</sub>
- **[GeiserX/duplicacy-mcp](https://github.com/GeiserX/duplicacy-mcp)** — Go-based MCP server for Duplicacy backup monitoring. Query backup job status and Prometheus metrics from a Duplicacy exporter. Docker image available
  <sub>★ 2 · Go · GPL-3.0 · npm · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g duplicacy-mcp`</sub>
- **[tp322d/lastping-app](https://github.com/tp322d/lastping-app)** — Dead man's switch for AI agents, cron jobs and CI/CD pipelines. An agent creates its own monitor, asks for its ping commands and reports its runs in one conversation; LastPing alerts when a run goes silent, stalls, fails or loops, and list_open_incidents hands back what broke with the recurrence count, failing step and exit code. 36 tools. Hosted at https://mcp.lastping.dev/mcp (via mcp-remote), o
  <sub>★ 2 · Go · MIT · go · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/tp322d/lastping-app/cmd/lastping@latest`</sub>
- **[metrxbots/mcp-server](https://github.com/metrxbots/mcp-server)** — AI agent cost intelligence — track spend across providers, optimize model selection, manage budgets with enforcement, detect cost leaks, and prove ROI. 23 tools across 10 domains
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-05-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @metrxbot/mcp-server --demo`</sub>
- **[Turbo-Puffin/measure-mcp-server](https://github.com/Le-Circus/measure-mcp-server)** — Privacy-first web analytics with native MCP server. Query pageviews, referrers, trends, and AI-generated insights for your sites
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-05-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @turbo-puffin/measure-mcp-server`</sub>
- **[Sudhan30/freshprobe](https://github.com/Sudhan30/freshprobe)** — Data freshness verification for AI agents. Probes endpoints for HTTP cache staleness, latency percentiles, content fingerprinting, TLS health, DNS timing, and redirect chains. Returns deterministic FRESH/STALE/UNKNOWN verdicts with NIST AI RMF mapping. CLI + MCP server + HTTP API with Prometheus metrics and YAML policy engine
  <sub>★ 2 · Go · MIT · go · pushed 2026-04-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/Sudhan30/freshprobe/cmd/freshprobe@latest`</sub>
- **[tickstem/mcp](https://github.com/tickstem/mcp)** — HTTP uptime monitoring, heartbeat (dead-man's switch) monitoring, cron job scheduling, and email verification. Single API key, per-tool quota tracking. Install: go install github.com/tickstem/mcp/cmd/tsk-mcp@latest
  <sub>★ 2 · Go · MIT · go · pushed 2026-09-07 · macOS</sub>
  <sub>`go install github.com/tickstem/mcp/cmd/tsk-mcp@latest`</sub>
- **[us-all/datadog-mcp-server](https://github.com/us-all/datadog-mcp-server)** — Datadog observability — 168 tools across metrics, monitors, logs, APM, RUM, incidents, status pages, fleet automation, workflows. 4 workflow Prompts and incident-triage-snapshot aggregation that fans out to 4 fetches in one call
  <sub>★ 2 · TypeScript · MIT · docker · pushed 2026-07-10 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -e DD_API_KEY=... -e DD_APP_KEY=... -e DD_SITE=datadoghq.com \`</sub>
- **[zw008/VMware-Aria](https://github.com/vmware-skills/VMware-Aria)** — VMware Aria Operations monitoring — performance metrics, alarms, capacity analysis, and anomaly detection across vSphere infrastructure. 27 tools (21 read, 6 write) with audit logging for acknowledge/cancel actions
  <sub>★ 2 · Python · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install vmware-aria`</sub>
- **[aayushmdesai/mcp-dotnet-diagnostics](https://github.com/aayushmdesai/mcp-dotnet-diagnostics)** — Live .NET runtime diagnostics for AI assistants. Ask Claude to diagnose memory leaks, GC pressure, LOH fragmentation, and thread starvation in any running .NET process — no code changes required. Install: dotnet tool install -g mcp-dotnet-diagnostics
  <sub>★ 2 · C# · MIT · source · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aayushmdesai/mcp-dotnet-diagnostics.git`</sub>
- **[Alog/alog-mcp](https://github.com/asicojp/alog-mcp)** — AI agent activity logger &amp; monitor MCP server with 20 tools. Post logs, create articles, manage social interactions, and monitor AI agent activities on the Alog platform
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/asicojp/alog-mcp.git`</sub>
- **[bartekrutkowski/watchgoose-mcp](https://github.com/bartekrutkowski/watchgoose-mcp)** — Monitor cron jobs, backups, Kubernetes jobs and other scheduled tasks in Watchgoose.com. Read-only by default, check changes require explicit consent
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bartekrutkowski/watchgoose-mcp.git`</sub>
- **[esp4ce/infra-mcp](https://github.com/esp4ce/infra-mcp)** — Read-only MCP server for on-prem Linux VMs and PostgreSQL over SSH. Check service health (systemd/journald), retrieve bounded logs, inspect DB state, and explore table schemas — without terminal access. Allowlist-gated, append-only audit log. pip install infra-mcp
  <sub>★ 1 · Python · uv · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install infra-mcp`</sub>
- **[HostTracker/mcp](https://github.com/HostTracker/mcp)** — #️⃣ ☁️ - Website uptime monitoring from 300+ global locations. Run instant HTTP, ping, port, DNS, WHOIS, blacklist, Web Risk and page-speed checks, and manage monitors, contacts, webhooks, incidents, maintenance windows and status pages. Remote streamable-HTTP server at https://mcp.host-tracker.com/mcp, bearer token
  <sub>★ 1 · C# · MIT · npx · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y mcp-remote https://mcp.host-tracker.com/mcp --header "Authorization:${HT_AUTH}"`</sub>
- **[hugoles/langfuse-mcp](https://github.com/hugoles/langfuse-mcp)** — TypeScript MCP server for the Langfuse Public API. 27 read tools covering traces, observations, sessions, scores, score-configs, prompts (with version/label), datasets, dataset items, dataset runs, metrics, models, projects, comments, media, and health. Distributed as npx -y langfuse-mcp with provenance-signed releases
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g langfuse-mcp`</sub>
- **[jabbawocky/statuscraft](https://github.com/jabbawocky/statuscraft)** — MCP server that checks the live status of 3831 software services in real time. Ask your AI agent "is GitHub down?" or "what's wrong with Sentry?" — and get a live answer pulled directly from official status pages, including full incident detail when something is broken. npx -y github:jabbawocky/statuscraft
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:jabbawocky/statuscraft`</sub>
- **[perceptdot/percept](https://github.com/perceptdot/percept)** — AI-powered observability platform for agents. Auto-discovers and recommends MCP servers; built-in connectors for GA4, Vercel, GitHub, and Sentry with ROI tracking. npx -y @perceptdot/core
  <sub>★ 1 · HTML · MIT · npm · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @perceptdot/core`</sub>
- **[shibley/apistatuscheck-mcp-server](https://github.com/shibley/apistatuscheck-mcp-server)** — Check real-time operational status of 114+ cloud services and APIs (AWS, GitHub, Stripe, OpenAI, Vercel, etc.) directly from AI assistants. Published on npm
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y mcp-remote https://apistatuscheck.com/api/mcp`</sub>
- **[sudomichael/gizmoanalytics-mcp](https://github.com/sudomichael/gizmoanalytics-mcp)** — Gizmo Analytics — cookieless web analytics for AI coding agents. Framework-aware install (Next/Remix/SvelteKit/Nuxt/Astro/Vite/React/HTML), OAuth onboarding, 28 tools for setup + query + workflow operations (summarize_all_sites, explain_traffic_change, detect_anomalies). Hosted MCP at gizmoanalytics.io/mcp
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sudomichael/gizmoanalytics-mcp.git`</sub>
- **[uptybots/mcp-server](https://github.com/uptybots/mcp-server)** — Uptime monitoring for websites, APIs, SSL certificates, domain expiry, ping and TCP/UDP ports. 15 tools to list, create, pause and delete monitors, pull incident timelines with error codes and checker locations, and read hourly or daily uptime and response-time series. Checks run from probes in several countries. Remote server at https://mcp.uptybots.com/mcp needs no API key - it speaks OAuth 2.1
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/uptybots/mcp-server.git`</sub>
- **[adanb13/cirdan](https://github.com/adanb13/cirdan)** — AI infrastructure cartographer &amp; MCP server: fingerprints, graphs, and watches the live infrastructure an agent can reach (Docker, Kubernetes, cloud, IaC) and detects incidents
  <sub>Python · Apache-2.0 · npm · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @cirdanops/cli # or put the `cirdan` command on your PATH`</sub>
- **[AIops-tools/Endpoint-AIops](https://github.com/AIops-tools/Endpoint-AIops)** — Governed managed-endpoint fleet operations (thin-client/VDI) — login-storm and patch/config-drift analysis, inventory, and guardrailed remediation (13 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install endpoint-aiops # or: pipx install endpoint-aiops`</sub>
- **[argosvix/mcp-server](https://github.com/argosvix/mcp-server)** — Observability for AI agents: 87 tools to query LLM cost, errors, and latency across OpenAI/Anthropic/Gemini/Mistral, and operate alerts, budget gates, evals, and safety checks from Claude/Cursor. Install: npx -y @argosvix/mcp-server
  <sub>TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @argosvix/mcp-server`</sub>
- **[arsentev-ai/contextburn](https://github.com/arsentev-ai/contextburn)** — Run efficiency for Claude Code sessions: the share of paid tokens that became model output versus re-reading context already sent, by tokens and cost-weighted. Reads local transcripts, makes no network calls
  <sub>Python · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/arsentev-ai/contextburn.git`</sub>
- **[cloudsealed/cloudsealed-mcp](https://github.com/cloudsealed/cloudsealed-mcp)** — Two deterministic, rule-based analysis engines for agents: cloud billing cost anomaly detection (rolling-median + MAD, resistant to the masking effect) and auditable architecture risk scoring (single point of failure, coupling, scalability gap) with a rule-by-rule breakdown for every score. uvx cloudsealed-mcp
  <sub>Python · MIT · uv · pushed 2026-08-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx cloudsealed-mcp`</sub>
- **[GT-dinuo/server-ops-mcp](https://github.com/GT-dinuo/server-ops-mcp)** — Server ops via AI: log troubleshooting, CPU/memory/disk monitoring, code edit, Nginx &amp; certificate management. Local or SSH-remote with two-step confirmation, command whitelist, and secret redaction. Install: npx -y server-ops-mcp
  <sub>TypeScript · MIT · clone · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GT-dinuo/server-ops-mcp.git`</sub>
- **[ingero-io/ingero](https://github.com/ingero-io/ingero)** — eBPF-based GPU causal observability agent with MCP server. Traces CUDA Runtime/Driver APIs and host kernel events to build causal chains explaining GPU latency
  <sub>unavailable</sub>
- **[jaimenbell/vllm-ops-mcp](https://github.com/jaimenbell/vllm-ops-mcp)** — Read-only ops and health server for a local vLLM instance: liveness versus real-completion health tiers, GPU and VRAM status, service status, and live serve-flag introspection. pip install vllm-ops-mcp
  <sub>Python · MIT · source · pushed 2026-08-12 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jaimenbell/vllm-ops-mcp.git`</sub>
- **[seancrecord/scvd-general-store-repo (scvd-tab)](https://github.com/seancrecord/scvd-general-store-repo/tree/main/tab)** — Agent tool spend tracker. Local JSONL storage, consent-gated, nothing leaves the file. Free MCP server. npx scvd-tab
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/seancrecord/scvd-general-store-repo.git && cd scvd-general-store-repo/tab`</sub>
- **[syk8015/claudeusage](https://github.com/syk8015/claudeusage)** — Measures whether a Claude subscription is paying off, from the logs Claude Code already writes on disk: how much of the code Claude wrote is still in your files, what actually drives the rate limit, and how much of that limit plain chat ate. Single Python file, no dependencies, nothing leaves the machine
  <sub>Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install claudeusage`</sub>
- **[netdata/netdata#Netdata](https://github.com/netdata/netdata/blob/master/src/web/mcp/README.md)** — Discovery, exploration, reporting and root cause analysis using all observability data, including metrics, logs, systems, containers, processes, and network connections
  <sub>Go · GPL-3.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/netdata/netdata.git && cd netdata/src/web/mcp/README.md`</sub>
- **[openITCOCKPIT/openITCOCKPIT-MCP-Server](https://github.com/openITCOCKPIT/openITCOCKPIT-MCP-Server)** — Official server for the openITCOCKPIT (Naemon-based) monitoring platform: host and service state, check and state history, log entries, downtimes, acknowledgements, monitoring engine stats, software inventory and pending security updates. 39 tools, 24 read-only; the 15 tools that change the monitoring configuration are not registered unless you enable them. Tools take hostnames and template names,
  <sub>Python · MIT · source · pushed 2026-09-18 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openITCOCKPIT/openITCOCKPIT-MCP-Server.git`</sub>
- **[gsmethells/preflight-mcp](https://github.com/gsmethells/preflight-mcp)** — TrustPilot for APIs — independent reliability ratings for APIs and MCP servers, powered by synthetic probes and crowdsourced agent telemetry
  <sub>unavailable</sub>
- **[spanlens/Spanlens](https://github.com/spanlens/Spanlens/tree/main/packages/mcp-server)** — Query Spanlens LLM observability from Claude Desktop, Cursor, or Continue: request logs, costs, agent traces, anomalies, and user analytics with a read-only API key
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/spanlens/Spanlens.git && cd Spanlens/packages/mcp-server`</sub>
- **[speedofme-dev/speedofme-mcp](https://www.npmjs.com/package/@speedofme/mcp)** — Official SpeedOf.Me server for accurate internet speed tests via 129 global Fastly edge servers with analytics dashboard and local history
  <sub>website</sub>
  <sub>`https://www.npmjs.com/package/@speedofme/mcp`</sub>

## Embedded System

- **[stack-chan/stack-chan](https://github.com/stack-chan/stack-chan)** — A JavaScript-driven M5Stack-embedded super-kawaii robot with MCP server functionality for AI-controlled interactions and emotions
  <sub>★ 1.7k · TypeScript · Apache-2.0 · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stack-chan/stack-chan.git`</sub>
- **[adancurusul/embedded-debugger-mcp](https://github.com/Adancurusul/embedded-debugger-mcp)** — A Model Context Protocol server for embedded debugging with probe-rs - supports ARM Cortex-M, RISC-V debugging via J-Link, ST-Link, and more
  <sub>★ 193 · Rust · MIT · clone · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/adancurusul/embedded-debugger-mcp.git`</sub>
- **[horw/esp-mcp](https://github.com/horw/esp-mcp)** — Workflow for fixing build issues in ESP32 series chips using ESP-IDF
  <sub>★ 157 · Python · clone · pushed 2025-12-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:horw/esp-mcp.git`</sub>
- **[adancurusul/serial-mcp-server](https://github.com/Adancurusul/serial-mcp-server)** — A comprehensive MCP server for serial port communication
  <sub>★ 91 · Rust · MIT · clone · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/adancurusul/serial-mcp-server.git`</sub>
- **[codeofaxel/Kiln](https://github.com/codeofaxel/Kiln)** — MCP server that lets AI agents drive real 3D printers end to end — design, slice, queue, monitor via camera, and recover from failures — across Bambu Lab, Creality, Prusa, Elegoo, and more over OctoPrint, Moonraker/Klipper, PrusaLink, and USB. AGPL-3.0, pip install kiln3d
  <sub>★ 66 · Python · AGPL-3.0 · uv · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from kiln3d kiln accept-terms`</sub>
- **[yoelbassin/gnuradioMCP](https://github.com/yoelbassin/gr-mcp)** — An MCP server for GNU Radio that enables LLMs to autonomously create and modify RF .grc flowcharts
  <sub>★ 50 · Python · GPL-3.0 · source · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yoelbassin/gnuradioMCP.git`</sub>
- **[kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp)** — An MCP server that connects to OPC UA-enabled industrial systems
  <sub>★ 29 · Python · MIT · pip · pushed 2025-10-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp[cli] opcua cryptography`</sub>
- **[kukapay/modbus-mcp](https://github.com/kukapay/modbus-mcp)** — An MCP server that standardizes and contextualizes industrial Modbus data
  <sub>★ 25 · Python · MIT · clone · pushed 2025-05-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kukapay/modbus-mcp.git`</sub>
- **[ByteAsk/ByteAsk-Embedded-MCP](https://github.com/ByteAsk/ByteAsk-Embedded-MCP)** — Page-cited retrieval of embedded/firmware reference docs (datasheets, MCU registers, Modbus/CAN, SCPI, IEEE 1547/SunSpec) for coding agents — returns verbatim source snippets with page citations, or "no confident match" instead of a fabricated value. No signup or API key
  <sub>★ 24 · Python · MIT · source · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ByteAsk/ByteAsk-Embedded-MCP.git`</sub>
- **[octoco-ltd/sheetsdata-mcp](https://github.com/octoco-ltd/sheetsdata-mcp)** — Instant access to electronic component datasheets for AI agents — specs, pinouts, package info, absolute max ratings extracted from manufacturer PDFs on demand
  <sub>★ 12 · JavaScript · MIT · source · pushed 2026-04-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/octoco-ltd/sheetsdata-mcp.git`</sub>
- **[ProductOfAmerica/mcp-server-kicad](https://github.com/ProductOfAmerica/mcp-server-kicad)** — KiCad EDA automation: 100+ tools for schematic capture, PCB layout, ERC, DRC, and Gerber/BOM/3D exports. Byte-preserving writes, KiCad 9 and 10. Install via uvx --from mcp-server-kicad mcp-server-kicad
  <sub>★ 10 · Python · MIT · npx · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx --from mcp-server-kicad mcp-server-kicad`</sub>
- **[turbyho/fw-context-mcp](https://github.com/turbyho/fw-context-mcp)** — Build-aware code intelligence for embedded C/C++ firmware. Indexes your project from compile_commands.json via libclang into SQLite+FTS5. 31 MCP tools for symbol search, call graphs, hotspot analysis, dead code detection, and vector search. For Zephyr, PlatformIO, Mbed OS, Arduino, FreeRTOS
  <sub>★ 10 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install fw-context-mcp`</sub>
- **[0x1abin/matter-controller-mcp](https://github.com/0x1abin/matter-controller-mcp)** — An MCP server for Matter Controller, enabling AI agents to control and interact with Matter devices
  <sub>★ 8 · JavaScript · MIT · npm · pushed 2025-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g matter-controller-mcp`</sub>
- **[catallo/misterclaw](https://github.com/catallo/misterclaw)** — MiSTerClaw — MCP remote control for MiSTer-FPGA. Launch games, search ROMs, take screenshots, manage systems, and set up Tailscale VPN. Auto-discovers 70+ systems with dynamic core/ROM scanning
  <sub>★ 6 · Go · MIT · source · pushed 2026-08-01 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/catallo/misterclaw.git`</sub>
- **[zackpeters93/ugs-mcp](https://github.com/zackpeters93/ugs-mcp)** — CNC machine control via Universal G-code Sender (GRBL). Jog axes, home, run G-code files, inspect toolpaths, estimate cycle times. Motion commands require two-step token confirmation — Claude cannot move hardware autonomously
  <sub>★ 5 · Python · MIT · pip · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ugs-mcp`</sub>
- **[powerdragonfire/platformio.mcp](https://github.com/powerdragonfire/platformio.mcp)** — Build, flash, and debug firmware for any PlatformIO board (ESP32, Arduino, STM32, RP2040, ...): parsed compiler errors with file:line, flash-then-verify against the serial boot log, background serial monitor sessions, ESP32 / Cortex-M crash backtrace decoding to source lines, firmware size reports, Unity tests, static analysis, and library management. Policy env var for build-only or read-only use
  <sub>★ 3 · Python · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run platformio-mcp # poke tools interactively`</sub>
- **[JannLeo/telinksdk-builder-mcp](https://github.com/JannLeo/telinksdk-builder-mcp)** — Build any Telink/embedded SDK (Eclipse headless / Make / generic) via natural language. Auto-detects build pattern and exposes build_info/build_run/build_list MCP tools. Cross-platform
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/JannLeo/telinksdk-builder-mcp.git`</sub>
- **[lxman/obsbot-mcp](https://github.com/lxman/obsbot-mcp)** — Control an OBSBOT Tiny 2 webcam over USB — pan/tilt/zoom the motorized gimbal in degrees, AI subject tracking, presets, focus/exposure/white-balance, snapshots and recording. Point it at a pixel, or zoom to fit a region of a snapshot it just took. 35 tools (34 on Linux), speaking UVC and the vendor protocol directly with no vendor SDK and no cloud; prebuilt native helpers for Windows, macOS and Li
  <sub>TypeScript · MIT · source · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/lxman/obsbot-mcp.git`</sub>
- **[Gearotons/servomotor-mcp](https://github.com/Gearotons/servomotor-mcp)** — Drive the Gearotons M17, an open-source closed-loop NEMA-17 servomotor, from plain English over RS-485: discovers serial ports, auto-detects every motor on the bus, and exposes the firmware's full command set as tools. Mock backend needs no hardware. uvx --from servomotor-mcp servomotor-mcp
  <sub>Python · MIT · uv · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx --from servomotor-mcp servomotor-mcp`</sub>

## Industrial &amp; IoT

- **[Extelligence-ai/bagel](https://github.com/Extelligence-ai/bagel)** — Ask questions about robotics, drone, and IoT data (ROS 1/2 bags, MCAP, PX4/ArduPilot/Betaflight logs, CAN/MF4, live MQTT) in plain English; answers are DuckDB SQL over the actual messages, with an intelligent edge data-reduction pipeline and exports to Rerun, PlotJuggler, and LeRobot
  <sub>★ 397 · Python · Apache-2.0 · docker · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it --rm ghcr.io/extelligence-ai/bagel/px4:latest demo`</sub>
- **[LGDiMaggio/predictive-maintenance-mcp](https://github.com/LGDiMaggio/predictive-maintenance-mcp)** — Industrial predictive maintenance: vibration analysis, bearing fault diagnosis (ISO 20816-3), and server-authored diagnostic reports, benchmarked on the public CWRU dataset
  <sub>★ 92 · Python · pip · pushed 2026-09-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install predictive-maintenance-mcp`</sub>
- **[purinzan/gx3-cli-mcp](https://github.com/purinzan/gx3-cli-mcp)** — Read-only analysis of Mitsubishi Electric MELSEC PLC projects saved by GX Works3 (.gx3): trace why a coil never turns on through the ladder logic, find where a device is written and read, search by device comment, and separate conditions that arrive from physical inputs, HMI or network communication. Runs entirely locally and never modifies the project; no project-mutating command is exposed. Unof
  <sub>★ 6 · Python · pip · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install gx3-cli-mcp`</sub>
- **[ahmed-khalil-hafsi/P2Predict](https://github.com/ahmed-khalil-hafsi/P2Predict)** — Local MCP server for parametric price benchmarking: trains on your own purchasing history to predict what a part should cost, attribute the price to spec and supplier drivers, and return a calibrated likely-price range — nothing leaves your machine. Built for procurement and engineering teams. pip install "p2predict[mcp]"
  <sub>★ 2 · Python · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "p2predict[mcp]"`</sub>
- **[FoundryNet/forge-mcp](https://github.com/FoundryNet/forge-mcp)** — Industrial AI infrastructure that connects any AI agent to industrial equipment: 14 protocols, 18 manufacturers, 30 tools, cross-OEM telemetry normalization, health index, and failure prediction. The first physical-world MCP server. Free tier available. (Smithery)
  <sub>Python · source · pushed 2026-08-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/FoundryNet/forge-mcp.git`</sub>

## Home Automation

- **[handsomejustin/mijia-control](https://github.com/handsomejustin/mijia-control)** — Control Xiaomi/Mijia smart home devices (lights, AC, heaters, robots, cameras) through MCP. Includes web dashboard, REST API, CLI, SocketIO, energy monitoring, and automation rules
  <sub>★ 71 · Python · MIT · clone · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/handsomejustin/mijia-control.git`</sub>
- **[Hybirdss/smartest-tv](https://github.com/Hybirdss/smartest-tv)** — Control any smart TV with natural language. Play Netflix, YouTube, Spotify by name with deep linking, cast URLs, scene presets, multi-room audio, and multi-TV sync. Supports LG, Samsung, Android TV, Roku. 21 MCP tools, no cloud required
  <sub>★ 48 · Python · MIT · source · pushed 2026-08-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Hybirdss/smartest-tv.git`</sub>
- **[alexpfau/zigbee2mqtt-mcp](https://github.com/alexpfau/zigbee2mqtt-mcp)** — Administer a Zigbee2MQTT estate over its MQTT bridge API — whole-network health report (offline devices, weak links, low batteries, pending OTA, devices rejoining), mesh topology, pairing, binding, reporting intervals and device options. 23 tools across read/safe/destructive tiers; destructive tools are disabled by default. npx zigbee2mqtt-mcp
  <sub>★ 30 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx zigbee2mqtt-mcp`</sub>
- **[NickoScope/nickol-knx-mcp](https://github.com/NickoScope/nickol-knx-mcp)** — Design-time KNX/ETS6 assistant: parses .knxproj (read-only, no bus access), validates DPT/naming/command-status pairing, and generates Home Assistant YAML + ETS XML/CSV exports
  <sub>★ 25 · Python · MIT · clone · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NickoScope/nickol-knx-mcp.git`</sub>
- **[kambriso/fritzbox-mcp-server](https://github.com/kambriso/fritzbox-mcp-server)** — Control AVM FRITZ!Box routers - manage devices, WiFi, network settings, parental controls, and schedule time-delayed actions
  <sub>★ 18 · Go · source · pushed 2026-06-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/kambriso/fritzbox-mcp-server.git`</sub>
- **[claymore666/debmatic-mcp](https://github.com/claymore666/ccu-mcp)** — Control a HomeMatic / debmatic CCU (eq-3 home automation) over its JSON-RPC and HM-Script APIs — switch and dim actuators, read sensors, system variables and service messages, run programs, and manage rooms, functions, channel links and device assignments. 25 tools over HTTP or stdio; runs locally against your own CCU
  <sub>★ 9 · TypeScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/claymore666/ccu-mcp.git`</sub>
- **[ober37/ac-infinity-mcp](https://github.com/ober37/ac-infinity-mcp)** — Monitor and automate AC Infinity grow controllers through natural conversation with Claude. 25 tools covering live sensor data, multi-day history, VPD/temperature/humidity automations, port control, advance scheduling, and grow stage templates
  <sub>★ 6 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from git+https://github.com/ober37/ac-infinity-mcp.git ac-infinity-mcp`</sub>
- **[apiarya/wemo-mcp-server](https://github.com/apiarya/wemo-mcp-server)** — Control WeMo smart home devices via AI assistants using natural language. Built on pywemo for 100% local control — no cloud dependency. Supports dimmer brightness, device rename, HomeKit codes, and multi-phase discovery
  <sub>★ 1 · Python · MIT · clone · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/apiarya/wemo-mcp-server.git`</sub>
- **[laszlopere/mcp-kodi](https://github.com/laszlopere/mcp-kodi)** — Control a Kodi media player over its JSON-RPC API — transport, volume, library search, queue management, and playback history. 16 tools, targetable across multiple Kodi instances. Written in C on the GLib stack; builds from source (autotools / .deb)
  <sub>★ 1 · C · GPL-3.0 · source · pushed 2026-06-19</sub>
  <sub>`git clone https://github.com/laszlopere/mcp-kodi.git`</sub>

## Security &amp; Governance

- **[Top-Celestial-Company-Ltd/DROS-VajraClaw-Hacker](https://github.com/Top-Celestial-Company-Ltd/DROS-VajraClaw-Hacker)** — Deterministic in-band execution governance gateway and W3C DID security guardrail for AI Agent MCP tool calls
  <sub>★ 16 · Python · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @dros/personal init`</sub>

## Identity

- **[AIops-tools/Identity-AIops](https://github.com/AIops-tools/Identity-AIops)** — Governed SSO/IAM operations (Keycloak + Authentik) — login-failure, stale-permission, client-config, and MFA RCA, plus guardrailed writes (29 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install identity-aiops # or: pipx install identity-aiops`</sub>
- **[true-alter/cli](https://github.com/true-alter/cli)** — Companies pay other companies to find out who you are. ~Alter pays you because you choose to be found. Claim ~yourname, take back control of your digital identity, and keep 75% every time someone pays to find you. Golden threads turn curiosity into side quests that prove what you can actually do so you never write a CV again. Start or join a collective where a team, a union, or a whole country ear
  <sub>TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @truealter/cli`</sub>

## Communication

- **[lharries/whatsapp-mcp](https://github.com/lharries/whatsapp-mcp)** — An MCP server for searching your personal WhatsApp messages, contacts and sending messages to individuals or groups
  <sub>★ 6.3k · Go · MIT · clone · pushed 2025-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lharries/whatsapp-mcp.git`</sub>
- **[korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server)** — The most powerful MCP server for Slack Workspaces
  <sub>★ 1.8k · Go · MIT · source · pushed 2026-07-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/korotovsky/slack-mcp-server.git`</sub>
- **[chigwell/telegram-mcp](https://github.com/chigwell/telegram-mcp)** — Telegram API integration for accessing user data, managing dialogs (chats, channels, groups), retrieving messages, sending messages and handling read status
  <sub>★ 1.7k · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from "git+https://github.com/chigwell/telegram-mcp.git@<pinned-release-tag-or-commit>" telegram-mcp-generate-session`</sub>
- **[anypost/emailmd](https://github.com/anypost/emailmd)** — Write and preview emails from your assistant. Renders markdown into email-safe HTML that holds up in Outlook and Gmail, lints drafts for deliverability problems, and returns a live preview link. Hosted with no API key, or run it locally with npx emailmd mcp
  <sub>★ 1.4k · TypeScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx emailmd mcp`</sub>
- **[softeria/ms-365-mcp-server](https://github.com/Softeria/ms-365-mcp-server)** — MCP server that connects to Microsoft Office and the whole Microsoft 365 suite using Graph API (including Outlook, mail, files, Excel, calendar)
  <sub>★ 990 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @softeria/ms-365-mcp-server --toon`</sub>
- **[line/line-bot-mcp-server](https://github.com/line/line-bot-mcp-server)** — MCP Server for Integrating LINE Official Account
  <sub>★ 782 · TypeScript · Apache-2.0 · clone · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone git@github.com:line/line-bot-mcp-server.git`</sub>
- **[joinly-ai/joinly](https://github.com/joinly-ai/joinly)** — MCP server to interact with browser-based meeting platforms (Zoom, Teams, Google Meet). Enables AI agents to send bots to online meetings, gather live transcripts, speak text, and send messages in the meeting chat
  <sub>★ 566 · Python · MIT · uv · pushed 2026-09-01 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx joinly-client --env-file .env <MeetingUrl>`</sub>
- **[saseq/discord-mcp](https://github.com/SaseQ/discord-mcp)** — A MCP server for the Discord integration. Enable your AI assistants to seamlessly interact with Discord. Enhance your Discord experience with powerful automation capabilities
  <sub>★ 502 · Java · MIT · clone · pushed 2026-04-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/SaseQ/discord-mcp`</sub>
- **[InditexTech/mcp-teams-server](https://github.com/InditexTech/mcp-teams-server)** — MCP server that integrates Microsoft Teams messaging (read, post, mention, list members and threads)
  <sub>★ 399 · Python · Apache-2.0 · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it inditextech/mcp-teams-server`</sub>
- **[chaindead/telegram-mcp](https://github.com/chaindead/telegram-mcp)** — Telegram API integration for accessing user data, managing dialogs (chats, channels, groups), retrieving messages, and handling read status
  <sub>★ 348 · Go · MIT · npx · pushed 2026-05-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @chaindead/telegram-mcp`</sub>
- **[carterlasalle/mac_messages_mcp](https://github.com/carterlasalle/mac_messages_mcp)** — An MCP server that securely interfaces with your iMessage database via the Model Context Protocol (MCP), allowing LLMs to query and analyze iMessage conversations. It includes robust phone number validation, attachment processing, contact management, group chat handling, and full support for sending and receiving messages
  <sub>★ 328 · Python · MIT · uv · pushed 2026-09-19 · macOS</sub>
  <sub>`uvx mac-messages-mcp`</sub>
- **[Atomic-Mail/atomic-mail-agentic](https://github.com/Atomic-Mail/atomic-mail-agentic)** — Email built for AI agents. Hosted MCP server (atomicmail.ai) with autonomous inbox registration via proof-of-work (no email verification, domain, or card), custom domain support, and full send/receive over the open JMAP standard (RFC 8620/8621)
  <sub>★ 262 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --package=@atomicmail/agent-skill-github atomicmail register --username "myagent" --watch scheduled`</sub>
- **[adhikasp/mcp-twikit](https://github.com/adhikasp/mcp-twikit)** — Interact with Twitter search and timeline
  <sub>★ 235 · Python · MIT · npx · pushed 2025-03-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-twikit --client claude`</sub>
- **[agenticmail/agenticmail](https://github.com/agenticmail/agenticmail)** — Real email and SMS for AI agents. Run a local mail server with disposable inboxes, send/receive real email, fetch verification codes, and drive a real inbox — all from your machine, no third-party email API. Install with npx @agenticmail/mcp
  <sub>★ 226 · TypeScript · MIT · npm · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @agenticmail/cli`</sub>
- **[wyattjoh/jmap-mcp](https://github.com/wyattjoh/jmap-mcp)** — A Model Context Protocol (MCP) server that provides tools for interacting with JMAP (JSON Meta Application Protocol) email servers. Built with Deno and using the jmap-jam client library
  <sub>★ 176 · TypeScript · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wyattjoh/jmap-mcp.git`</sub>
- **[zcaceres/gtasks-mcp](https://github.com/zcaceres/gtasks-mcp)** — An MCP server to Manage Google Tasks
  <sub>★ 164 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @zcaceres/gtasks --client claude`</sub>
- **[codefuturist/email-mcp](https://github.com/codefuturist/email-mcp)** — IMAP/SMTP email MCP server with 42 tools for reading, searching, sending, scheduling, and managing emails across multiple accounts. Supports IMAP IDLE push, AI triage, desktop notifications, and auto-detects providers like Gmail, Outlook, and iCloud
  <sub>★ 114 · TypeScript · LGPL-3.0 · npm · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @codefuturist/email-mcp`</sub>
- **[areweai/tsgram-mcp](https://github.com/areweai/tsgram-mcp)** — TSgram: Telegram + Claude with local workspace access on your phone in typescript. Read, write, and vibe code on the go!
  <sub>★ 89 · JavaScript · MIT · script · pushed 2025-06-26 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/areweai/tsgram-mcp/main/setup.sh | bash`</sub>
- **[cometchat/docs-mcp](https://github.com/cometchat/docs-mcp)** — CometChat's official MCP server — searches CometChat documentation and returns curated implementation bundles for adding real-time chat, voice, video, and moderation to your app (React, React Native, Flutter, iOS, Android, JS SDK)
  <sub>★ 88 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y smithery mcp add cometchat/docs-mcp`</sub>
- **[ztxtxwd/open-feishu-mcp-server](https://github.com/ztxtxwd/open-feishu-mcp-server)** — A Model Context Protocol (MCP) server with built-in Feishu OAuth authentication, supporting remote connections and providing comprehensive Feishu document management tools including block creation, content updates, and advanced features
  <sub>★ 87 · TypeScript · MIT · source · pushed 2026-01-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ztxtxwd/open-feishu-mcp-server.git`</sub>
- **[tecnologicachile/mail-mcp](https://github.com/tecnologicachile/mail-mcp)** — Full-stack email MCP server in Rust: IMAP, SMTP, Exchange Web Services, and Microsoft Graph in one binary, with OAuth2 and multi-account support. Read, search, send, reply, forward, bulk operations, and attachment download to disk, plus server-side guardrails that reject malformed LLM tool calls
  <sub>★ 86 · Rust · MIT · clone · pushed 2026-09-18 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/tecnologicachile/mail-mcp.git`</sub>
- **[hannesrudolph/imessage-query-fastmcp-mcp-server](https://github.com/hannesrudolph/imessage-query-fastmcp-mcp-server)** — An MCP server that provides safe access to your iMessage database through Model Context Protocol (MCP), enabling LLMs to query and analyze iMessage conversations with proper phone number validation and attachment handling
  <sub>★ 81 · Python · clone · pushed 2026-02-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hannesrudolph/imessage-query-fastmcp-mcp-server.git`</sub>
- **[discourse/discourse-mcp](https://github.com/discourse/discourse-mcp)** — Official Discourse MCP server for forum integration. Search topics, read posts, manage categories and tags, discover users, and interact with Discourse communities
  <sub>★ 76 · TypeScript · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @discourse/mcp@latest`</sub>
- **[gitmotion/ntfy-me-mcp](https://github.com/gitmotion/ntfy-me-mcp)** — An ntfy MCP server for sending/fetching ntfy notifications to your self-hosted ntfy server from AI Agents 📤 (supports secure token auth &amp; more - use with npx or docker!)
  <sub>★ 74 · TypeScript · GPL-3.0 · source · pushed 2026-04-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gitmotion/ntfy-me-mcp.git`</sub>
- **[sawa-zen/vrchat-mcp](https://github.com/sawa-zen/vrchat-mcp)** — This is an MCP server for interacting with the VRChat API. You can retrieve information about friends, worlds, avatars, and more in VRChat
  <sub>★ 66 · TypeScript · MIT · npx · pushed 2026-02-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vrchat-mcp`</sub>
- **[imdinu/apple-mail-mcp](https://github.com/imdinu/apple-mail-mcp)** — Fast MCP server for Apple Mail — 87x faster email fetching via batch JXA and FTS5 search index for ~2ms body search. 6 tools: list accounts/mailboxes, get emails with filters, full-text search across all scopes, and attachment extraction
  <sub>★ 65 · Python · GPL-3.0 · pipx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install apple-mail-mcp`</sub>
- **[kushneryk/join.cloud](https://github.com/kushneryk/join.cloud)** — Collaboration rooms for AI agents. Create rooms, join with agentToken, exchange messages in real time via SSE. Supports MCP and A2A protocols. Self-hostable or use the hosted version at join.cloud
  <sub>★ 64 · TypeScript · AGPL-3.0 · npx · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx joincloud rooms`</sub>
- **[lanchuske/local-mcp](https://github.com/lanchuske/local-mcp-releases)** — Connect Claude, Cursor, Windsurf and other AI agents to macOS native apps: Mail, Calendar, Contacts, Reminders, Notes, iMessage, Finder, Safari, OmniFocus, Microsoft Teams, Outlook, OneDrive, and Office documents. 82 tools. Runs entirely on your Mac — no cloud, no tokens, no API keys
  <sub>★ 55 · JavaScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lanchuske/local-mcp-releases.git`</sub>
- **[Cactusinhand/mcp_server_notify](https://github.com/Cactusinhand/mcp_server_notify)** — A MCP server that send desktop notifications with sound effect when agent tasks are completed
  <sub>★ 54 · Python · MIT · pip · pushed 2025-08-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install mcp-server-notify`</sub>
- **[jaipandya/producthunt-mcp-server](https://github.com/jaipandya/producthunt-mcp-server)** — MCP server for Product Hunt. Interact with trending posts, comments, collections, users, and more
  <sub>★ 53 · Python · pip · pushed 2025-04-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install product-hunt-mcp`</sub>
- **[MrGo2/icloud-mcp](https://github.com/MrGo2/icloud-mcp)** — Apple Mail, Calendar, Contacts, Reminders, Notes, Messages and Safari in one server with 41 tools. Talks AppleScript to the native macOS apps, or IMAP/CalDAV/CardDAV to iCloud when running off-Mac
  <sub>★ 52 · JavaScript · MIT · source · pushed 2026-08-11 · macOS</sub>
  <sub>`git clone https://github.com/MrGo2/icloud-mcp.git`</sub>
- **[arpitbatra123/mcp-googletasks](https://github.com/arpitbatra123/mcp-googletasks)** — An MCP server to interface with the Google Tasks API
  <sub>★ 49 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/arpitbatra123/mcp-googletasks.git`</sub>
- **[leshchenko1979/fast-mcp-telegram](https://github.com/leshchenko1979/fast-mcp-telegram)** — Telegram MCP server with direct API/curl access, multi-user Bearer auth, HTTP-MTProto Bridge, file attachments, voice transcription, and context-optimized design
  <sub>★ 49 · Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from fast-mcp-telegram fast-mcp-telegram-setup \`</sub>
- **[openagentemail/openagentemail](https://github.com/openagentemail/openagentemail)** — Self-hosted email for AI agents: unlimited mailboxes on your own domain with a single docker compose up. OTP and verification-link extraction built in, long-poll mail_wait_for, read/unread state, plus a web dashboard for humans. Install with npx -y @openagentemail/mcp
  <sub>★ 46 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @openagentemail/setup`</sub>
- **[teddyzxcv/ntfy-mcp](https://github.com/teddyzxcv/ntfy-mcp)** — The MCP server that keeps you informed by sending the notification on phone using ntfy
  <sub>★ 45 · JavaScript · Apache-2.0 · clone · pushed 2025-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/teddyzxcv/ntfy-mcp.git`</sub>
- **[overpod/mcp-telegram](https://github.com/mcp-telegram/mcp-telegram)** — Telegram MCP server via MTProto/GramJS — 20 tools for reading chats, searching messages, downloading media, managing contacts. QR code login, npx zero-install. Hosted version at mcp-telegram.com
  <sub>★ 43 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @overpod/mcp-telegram`</sub>
- **[desek/outlook-local-mcp](https://github.com/desek/outlook-local-mcp)** — Local-first Microsoft Outlook MCP server (calendar + mail via Microsoft Graph). Single Go binary, stdio transport, OS-keychain token storage, multi-account. 4 aggregate domain tools (calendar, mail, account, system) with progressive disclosure via a help verb to keep cold-start schema small
  <sub>★ 42 · Go · MIT · go · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/desek/outlook-local-mcp/cmd/outlook-local-mcp@latest`</sub>
- **[AbdelStark/nostr-mcp](https://github.com/AbdelStark/nostr-mcp)** — A Nostr MCP server that allows to interact with Nostr, enabling posting notes, and more
  <sub>★ 38 · TypeScript · MIT · npx · pushed 2025-02-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @AbdelStark/nostr-mcp --client claude`</sub>
- **[gotoolkits/wecombot](https://github.com/gotoolkits/mcp-wecombot-server.git)** — An MCP server application that sends various types of messages to the WeCom group robot
  <sub>★ 37 · Go · GPL-3.0 · npx · pushed 2025-01-22 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npx -y @smithery/cli install @gotoolkits/mcp-wecombot-server --client claude-desktop`</sub>
- **[littlebearapps/outlook-assistant](https://github.com/littlebearapps/outlook-assistant)** — Ask your AI assistant to search your inbox, send emails, schedule meetings, manage contacts, and configure mailbox settings — without leaving the conversation. Works with Claude, Cursor, Windsurf, and any MCP-compatible client
  <sub>★ 37 · JavaScript · MIT · npm · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @littlebearapps/outlook-assistant`</sub>
- **[i-am-bee/acp-mcp](https://github.com/i-am-bee/acp-mcp)** — An MCP server acting as an adapter into the ACP ecosystem. Seamlessly exposes ACP agents to MCP clients, bridging the communication gap between the two protocols
  <sub>★ 36 · Python · Apache-2.0 · uv · pushed 2025-05-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx acp-mcp http://localhost:8000`</sub>
- **[Infobip/mcp](https://github.com/infobip/mcp)** — Official Infobip MCP server for integrating Infobip global cloud communication platform. It equips AI agents with communication superpowers, allowing them to send and receive SMS and RCS messages, interact with WhatsApp and Viber, automate communication workflows, and manage customer data, all in a production-ready environment
  <sub>★ 35 · MIT · source · pushed 2026-09-17</sub>
  <sub>`git clone https://github.com/infobip/mcp.git`</sub>
- **[jagan-shanmugam/mattermost-mcp-host](https://github.com/jagan-shanmugam/mattermost-mcp-host)** — A MCP server along with MCP host that provides access to Mattermost teams, channels and messages. MCP host is integrated as a bot in Mattermost with access to MCP servers that can be configured
  <sub>★ 34 · Python · MIT · source · pushed 2025-04-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jagan-shanmugam/mattermost-mcp-host.git`</sub>
- **[keturiosakys/bluesky-context-server](https://github.com/laulauland/bluesky-context-server)** — Bluesky instance integration for querying and interaction
  <sub>★ 34 · TypeScript · MIT · npx · pushed 2025-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @laulauland/bluesky-context-server --client claude`</sub>
- **[n24q02m/better-email-mcp](https://github.com/n24q02m/better-email-mcp)** — IMAP/SMTP email MCP server with App Passwords (no OAuth2). Auto-discovers Gmail, Outlook, Yahoo, iCloud. 5 composite tools: search, read, send, reply, forward. Multi-account support
  <sub>★ 33 · TypeScript · Apache-2.0 · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @n24q02m/better-email-mcp --http`</sub>
- **[jtalk22/slack-mcp-server](https://github.com/jtalk22/slack-mcp-server)** — Your complete Slack context for Claude—DMs, channels, threads, search. No OAuth apps, no admin approval. --setup and done, 11 tools, auto-refresh
  <sub>★ 30 · JavaScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @jtalk22/slack-mcp`</sub>
- **[parasxos/apple-mail-mcp](https://github.com/parasxos/apple-mail-mcp)** — Full-featured MCP server for Apple Mail. Indexed search over 300k+ message mailboxes in milliseconds, full-text body search with Exchange backfill, verified multi-identity sending (SMTP/Keychain, SSH bastion, pipe), server-side scheduled sends with cancel, reviewed plan-then-apply triage, and a local audit ledger. 21 tools, frozen v1 wire contract
  <sub>★ 29 · Python · MIT · uv · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx apple-mailbox-mcp setup`</sub>
- **[wyattjoh/imessage-mcp](https://github.com/wyattjoh/imessage-mcp)** — A Model Context Protocol server for reading iMessage data from macOS
  <sub>★ 29 · TypeScript · MIT · deno · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`deno install --global --allow-read --allow-env --allow-sys --allow-ffi -n imessage-mcp jsr:@wyattjoh/imessage-mcp`</sub>
- **[yjcho9317/nworks](https://github.com/yjcho9317/nworks)** — NAVER WORKS CLI + MCP server. 26 tools for messages, calendar, drive, mail, tasks, and boards. AI agents can manage NAVER WORKS directly
  <sub>★ 25 · TypeScript · Apache-2.0 · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g nworks`</sub>
- **[gerkensm/callcenter.js-mcp](https://github.com/gerkensm/callcenter.js-mcp)** — An MCP server to make phone calls using VoIP/SIP and OpenAI's Realtime API and observe the transcript
  <sub>★ 24 · TypeScript · npx · pushed 2025-10-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:gerkensm/callcenter.js-mcp call "+1234567890" --brief "Call restaurant for reservation" --user-name "Your Name"`</sub>
- **[marlinjai/email-mcp](https://github.com/marlinjai/email-mcp)** — Unified MCP server for email across Gmail (REST API), Outlook (Microsoft Graph), iCloud, and generic IMAP/SMTP. 24 tools for search, send, organize, and batch-manage emails with built-in OAuth2 and encrypted credential storage
  <sub>★ 22 · TypeScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @marlinjai/email-mcp`</sub>
- **[mohitbadwal/ringback](https://github.com/mohitbadwal/ringback)** — Lets the LLM reach you on your phone: live, interruptible voice calls and tiered alerts, using free self-hosted pieces (SIP via pjsua2/Linphone + whisper.cpp STT + macOS say TTS). No paid telephony, no extra API key for the conversation
  <sub>★ 22 · Python · Apache-2.0 · clone · pushed 2026-06-23 · macOS</sub>
  <sub>`git clone https://github.com/mohitbadwal/ringback`</sub>
- **[PaSympa/discord-mcp](https://github.com/PaSympa/discord-mcp)** — Lightweight multi-guild Discord MCP server with 60+ tools for messages, channels, roles, forums, webhooks, and moderation
  <sub>★ 21 · TypeScript · MIT · clone · pushed 2026-09-20 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/PaSympa/discord-mcp`</sub>
- **[Danielpeter-99/calcom-mcp](https://github.com/Danielpeter-99/calcom-mcp)** — MCP server for Calcom. Manage event types, create bookings, and access Cal.com scheduling data through LLMs
  <sub>★ 19 · Python · MIT · clone · pushed 2025-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Danielpeter-99/calcom-mcp.git`</sub>
- **[Zacccck/Claude-MCP-Read-Email-Attachments](https://github.com/Zacccck/Claude-MCP-Read-Email-Attachments)** — Remote HTTP MCP server that reads Outlook email attachments via Microsoft Graph. Parses PDF, Word (with embedded image extraction for multimodal analysis), Excel, and text files in-memory and returns structured content directly to Claude
  <sub>★ 18 · JavaScript · MIT · clone · pushed 2026-06-16 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Zacccck/Claude-MCP-Read-Email-Attachments.git`</sub>
- **[ictinnovations/ictpbx-mcp](https://github.com/ictinnovations/ictpbx-mcp)** — MCP server for ICTPBX, a multi-tenant IP PBX built on ICTCore and FreeSWITCH. Reports PBX statistics and lists extensions, DIDs, providers and tenants over the ICTCore REST API. Entirely read-only: there are no write tools to gate, so it cannot change PBX configuration at all. Zero-install via npx -y ictpbx-mcp
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ictpbx-mcp`</sub>
- **[ictinnovations/pbx-mcp](https://github.com/ictinnovations/pbx-mcp)** — MCP server for Asterisk and FreeSWITCH. Reads live PBX state over AMI and ESL: registered extensions, active channels, trunk and SIP peer status, dialplan lookups and call history. Read-only by default, and write tools are never registered with the model at all unless PBX_MCP_ALLOW_WRITE=true. Zero-install via npx -y pbx-mcp
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g pbx-mcp`</sub>
- **[ictinnovations/ictbroadcast-mcp](https://github.com/ictinnovations/ictbroadcast-mcp)** — MCP server for ICTBroadcast, a voice, SMS and fax broadcasting and call centre platform. Lists campaigns and reads their live status, totals and per-call results including answer, machine detection and do-not-call outcomes. Starting and stopping a campaign places live calls, so those two tools are only registered when ICTBROADCAST_MCP_ALLOW_WRITE=true. Zero-install via npx -y ictbroadcast-mcp
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ictbroadcast-mcp`</sub>
- **[wildsurfer/your-mail-mcp](https://github.com/wildsurfer/your-mail-mcp)** — Read-only, self-hosted search over several IMAP accounts (Gmail, iCloud, any provider), mirrored one way by mbsync into a local notmuch index. The process cannot send, delete or move mail. Docker image; stdio for Claude Code, Cursor and Claude Desktop, or HTTP with OAuth from a phone
  <sub>★ 15 · Go · MIT · docker · pushed 2026-09-07 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`docker run -i --rm --env-file .env -v index:/index -v mail:/mail -v ./accounts.json:/config/accounts.json:ro ghcr.io/wildsurfer/your-mail-mcp`</sub>
- **[madbonez/caldav-mcp](https://github.com/madbonez/caldav-mcp)** — Universal MCP server for CalDAV protocol integration. Works with any CalDAV-compatible calendar server including Yandex Calendar, Google Calendar (via CalDAV), Nextcloud, ownCloud, Apple iCloud, and others. Supports creating events with recurrence, categories, priority, attendees, reminders, searching events, and retrieving events by UID
  <sub>★ 14 · Python · uv · pushed 2025-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-caldav`</sub>
- **[khan2a/telephony-mcp-server](https://github.com/khan2a/telephony-mcp-server)** — MCP Telephony server for automating voice calls with Speech-to-Text and Speech Recognition to summarize call conversations. Send and receive SMS, detect voicemail, and integrate with Vonage APIs for advanced telephony workflows
  <sub>★ 13 · Python · MIT · source · pushed 2026-06-07 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/khan2a/telephony-mcp-server.git`</sub>
- **[tlennon-ie/neurodock](https://github.com/tlennon-ie/neurodock)** — Local-first cognitive substrate for neurodivergent professionals: a translator for corporate ambiguity, a planner, and a guardrail that declines to amplify rumination, hyperfocus, or sycophancy. Hosted stateless tools over OAuth
  <sub>★ 13 · TypeScript · AGPL-3.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @neurodock/cli`</sub>
- **[Sealjay/mcp-hey](https://github.com/Sealjay/mcp-hey)** — Local MCP server for Hey.com email. Read, search, send, reply, and manage the screener via locally cached session from Hey's webview auth
  <sub>★ 11 · TypeScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Sealjay/mcp-hey.git`</sub>
- **[YCloud-Developers/ycloud-whatsapp-mcp-server](https://github.com/YCloud-Developers/ycloud-whatsapp-mcp-server)** — MCP server for WhatsApp Business Platform by YCloud
  <sub>★ 11 · TypeScript · clone · pushed 2025-04-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YCloud-Developers/ycloud-whatsapp-mcp-server.git`</sub>
- **[EthanQC/feishu-user-plugin](https://github.com/EthanQC/feishu-user-plugin)** — All-in-one Feishu/Lark MCP server (84 tools). Send messages as the actual user (not bot), plus full official-API coverage of docs, bitable, wiki, drive, calendar, tasks, OKR. Cookie + OAuth UAT + app-credential auth
  <sub>★ 10 · JavaScript · MIT · npx · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx feishu-user-plugin setup --app-id <APP_ID> --app-secret <APP_SECRET>`</sub>
- **[OverQuotaAI/chatterboxio-mcp-server](https://github.com/ChatterBoxIO/chatterboxio-mcp-server)** — MCP server implementation for ChatterBox.io, enabling AI agents to send bots to online meetings (Zoom, Google Meet) and obtain transcripts and recordings
  <sub>★ 10 · TypeScript · MIT · npx · pushed 2025-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @OverQuotaAI/chatterboxio-mcp-server --client claude`</sub>
- **[PhononX/cv-mcp-server](https://github.com/PhononX/cv-mcp-server)** — MCP Server that connects AI Agents to Carbon Voice. Create, manage, and interact with voice messages, conversations, direct messages, folders, voice memos, AI actions and more in Carbon Voice
  <sub>★ 10 · TypeScript · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PhononX/cv-mcp-server.git`</sub>
- **[BigCactusLabs/dead-letter](https://github.com/BigCactusLabs/dead-letter)** — Convert .eml email exports to clean Markdown with YAML front matter — thread splitting, signature stripping, attachment extraction, and calendar parsing. Tuned for feeding archived email into RAG/LLM pipelines
  <sub>★ 8 · Python · uv · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx --python 3.12 dead-letter convert message.eml`</sub>
- **[huj28-creator/wechat-fastbridge](https://github.com/huj28-creator/wechat-fastbridge)** — Token-efficient macOS WeChat MCP server for verified chat reading, text/file/sticker sending, fuzzy safe routing, smart context retrieval, and allowlisted live monitoring without screenshots or private-protocol access
  <sub>★ 8 · JavaScript · MIT · clone · pushed 2026-07-22 · macOS</sub>
  <sub>`git clone https://github.com/huj28-creator/wechat-fastbridge.git`</sub>
- **[virtualsms-io/mcp-server](https://github.com/virtualsms-io/mcp-server)** — Receive SMS verification codes with AI agents. Get virtual phone numbers for WhatsApp, Telegram, Google, and 500+ services. Own modem infrastructure across 200+ countries with real-time WebSocket delivery. 12 tools for number discovery, purchase, and code extraction
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx virtualsms-mcp`</sub>
- **[aeoess/mingle-mcp](https://github.com/aeoess/mingle-mcp)** — Agent-to-agent networking. Your AI publishes what you need, matches with other people's agents, both humans approve before connecting. 6 tools, Ed25519 signed, shared network at api.aeoess.com
  <sub>★ 8 · TypeScript · Apache-2.0 · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mingle-mcp setup`</sub>
- **[OrygnsCode/Omnicord](https://github.com/OrygnsCode/Omnicord)** — Hands your AI an entire Discord server: 148 tools covering chat, moderation, automod, events, and full administration, up to building a complete community server from one paragraph. One-command guided setup, and every destructive action previews and waits for your confirmation
  <sub>★ 8 · TypeScript · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @orygn/omnicord init`</sub>
- **[adecubed/gigamail](https://github.com/adecubed/gigamail)** — Your real mailbox and calendar for your agent (Microsoft 365 via Graph, or any IMAP): 24 tools for reading, search, attachment text, sender history, drafting from identity and knowledge files, and free-slot computation — with out-of-band human approval on every send, reply, delete and calendar write, so the agent cannot approve its own actions. pip install "gigamail[all]"
  <sub>★ 7 · Python · AGPL-3.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "gigamail[all]"`</sub>
- **[Albretsen/MCPEmails](https://github.com/Albretsen/MCPEmails)** — Hosted email MCP server for Gmail, Fastmail, iCloud, Yahoo, Zoho, Yandex and any IMAP/SMTP mailbox. 11 action-based tools to read, search, send, organize, draft, schedule and auto-triage mail. Streamable HTTP at https://mcpemails.com/api/mcp, OAuth 2.0 with PKCE or scoped API keys, mail fetched live and never stored. Docs at https://mcpemails.com/docs
  <sub>★ 7 · TypeScript · AGPL-3.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Albretsen/MCPEmails.git`</sub>
- **[FantomaSkaRus1/telegram-bot-mcp](https://github.com/FantomaSkaRus1/telegram-bot-mcp)** — Full-featured Telegram Bot API MCP server with 174 tools covering the entire Bot API
  <sub>★ 7 · JavaScript · MIT · source · pushed 2026-03-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FantomaSkaRus1/telegram-bot-mcp.git`</sub>
- **[Beltran12138/wecom-docs-mcp-server](https://github.com/Beltran12138/wecom-docs-mcp-server)** — WeCom (Enterprise WeChat) document operations via MCP: create, read, and edit Docs and Smartsheets (9 tools). Fills the doc-CRUD gap — existing WeCom MCP servers only support webhook messaging
  <sub>★ 6 · Python · MIT · pip · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install wecom-docs-mcp-server`</sub>
- **[churichard/fluxmail](https://github.com/churichard/fluxmail)** — Self-hosted email MCP server for Gmail, Microsoft 365, Outlook.com, and IMAP/SMTP. It can read, search, draft, send, schedule, and organize mail, with permission profiles for each client
  <sub>★ 6 · TypeScript · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g fluxmail`</sub>
- **[sethbang/proton-mail-mcp](https://github.com/sethbang/proton-mail-mcp)** — Unofficial Proton Mail MCP server — send, read, search, and organize email over SMTP and IMAP (via Proton Mail Bridge). Bulk ops with dry-run previews, read-only mode, and Trash-by-default deletes. Not affiliated with Proton AG
  <sub>★ 6 · TypeScript · MIT · clone · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sethbang/proton-mail-mcp.git`</sub>
- **[liuboacean/agent-comm-hub](https://github.com/liuboacean/agent-comm-hub)** — Production-grade multi-agent communication infrastructure with real-time messaging, task scheduling, shared memory, and trust-based evolution via MCP + SSE. 53 MCP tools, SQLite WAL persistence (zero message loss), 4-level RBAC, Python &amp; TypeScript SDKs (zero external deps), and evolution engine. Deploy via Docker, npm, or from source
  <sub>★ 6 · TypeScript · MIT · pip · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install agent-comm-hub`</sub>
- **[AutomateLab-tech/content-distribution-mcp](https://github.com/AutomateLab-tech/content-distribution-mcp)** — Publish one piece of content to DEV.to, Hashnode, GitHub Discussions, Reddit, Bluesky, LinkedIn, Medium and Twitter with idempotent state and per-platform adaptation
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @automatelab/content-distribution-mcp`</sub>
- **[GeiserX/telegram-archive-mcp](https://github.com/GeiserX/telegram-archive-mcp)** — Go-based MCP server for Telegram Archive. Search and browse Telegram chat history, list chats, and retrieve messages with full-text search. Docker image available
  <sub>★ 5 · Go · GPL-3.0 · npm · pushed 2026-09-08 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g telegram-archive-mcp`</sub>
- **[googlarz/signal-mcp](https://github.com/googlarz/signal-mcp)** — Full Signal messenger MCP server and CLI. Send/receive messages, manage groups and contacts, search history, handle attachments and reactions. Runs locally via signal-cli — no third-party servers
  <sub>★ 5 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install signal-mcp`</sub>
- **[PostcardBot/mcp-server](https://github.com/PostcardBot/mcp-server)** — Send real physical postcards worldwide via AI agents. Bulk send up to 500 recipients. Volume pricing from $0.72/card
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PostcardBot/mcp-server.git`</sub>
- **[loglux/whatsapp-mcp-stream](https://github.com/loglux/whatsapp-mcp-stream)** — WhatsApp MCP server over Streamable HTTP with web admin UI (QR/status/settings), bidirectional media upload/download, and SQLite persistence
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-09-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/loglux/whatsapp-mcp-stream.git`</sub>
- **[shahabazdev/inxmail-mcp](https://github.com/shahabazdev/inxmail-mcp)** — Manage Inxmail Commerce transactional emails — events, sendings, bounces, blocklist, blacklist, reactions, and delivery tracking
  <sub>★ 4 · JavaScript · MIT · npm · pushed 2026-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g inxmail-mcp`</sub>
- **[platfone-com/mcp](https://github.com/platfone-com/mcp)** — Virtual phone number platform for AI agents — rent numbers across 200+ countries, receive SMS, and manage the full activation lifecycle. Supports stdio and HTTP transport
  <sub>★ 4 · TypeScript · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/platfone-com/mcp.git`</sub>
- **[userad/didlogic_mcp](https://github.com/UserAd/didlogic_mcp)** — An MCP server for DIDLogic. Adds functionality to manage SIP endpoints, numbers and destinations
  <sub>★ 4 · Python · MIT · pip · pushed 2025-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install didlogic_mcp`</sub>
- **[conarti/mattermost-mcp](https://github.com/conarti/mattermost-mcp)** — MCP server for Mattermost API. List channels, read/post messages, manage threads and reactions, monitor topics. Supports flexible configuration via CLI args, environment variables, or config files
  <sub>★ 3 · TypeScript · npm · pushed 2026-09-14 · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @conarti/mattermost-mcp`</sub>
- **[FastAlertNow/mcp-server](https://github.com/FastAlertNow/mcp-server)** — Official Model Context Protocol (MCP) server for FastAlert. This server allows AI agents (like Claude, ChatGPT, and Cursor) to list of your channels and send notifications directly through the FastAlert API
  <sub>★ 3 · TypeScript · npx · pushed 2026-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y fastalert-mcp-server`</sub>
- **[farukkolip/xtapdown-mcp](https://github.com/farukkolip/xtapdown-mcp)** — X (Twitter) creator toolkit MCP with 14 tools: tweet download (video/GIF/image/full archive), curated hashtags by niche, best posting times by country, viral hook formulas, engagement &amp; ads-revenue calculators, thread splitter, character counter, advanced-search URL builder, fancy Unicode bio generator, viral patterns lookup, and the full 2026 search-operator cheatsheet. Uses X's public syndicatio
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y xtapdown-mcp`</sub>
- **[iprashantraj/mcp-discord-bridge](https://github.com/iprashantraj/mcp-discord-bridge)** — Discord MCP server with 46 tools for channels, messages, forums, webhooks, members, roles, threads, and moderation. Zero-install via npx -y mcp-discord-bridge. Also runs as a standalone bot with slash commands
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y mcp-discord-bridge`</sub>
- **[nakulben/whatsapp-mcp](https://github.com/nakulben/whatsapp-mcp)** — WhatsApp Business API template management via Meta Cloud API. Create, validate, and send all 12 template types (text, image, video, document, location, authentication, carousel, coupon, catalog, MPM, limited-time offer, and flows) from any MCP client
  <sub>★ 3 · Python · MIT · clone · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nakulben/whatsapp-mcp.git`</sub>
- **[mouse114514/Xadeus-QQ-MCP](https://github.com/mouse114514/Xadeus-QQ-MCP)** — QQ MCP Server — connects to QQ via NapCatQQ (OneBot v11), giving AI agents direct control over QQ (send/receive messages, group management, auto-wake on incoming messages, and more)
  <sub>★ 3 · Python · MIT · clone · pushed 2026-08-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/mouse114514/Xadeus-QQ-MCP`</sub>
- **[Py2755/aiogram-mcp](https://github.com/Py2755/aiogram-mcp)** — MCP server middleware for aiogram Telegram bots — 30 tools, 7 resources, 3 prompts covering messaging, rich media, moderation, interactive keyboards, real-time event streaming, rate limiting, permissions, and audit logging
  <sub>★ 3 · Python · MIT · pip · pushed 2026-03-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install aiogram-mcp`</sub>
- **[andrewchmr/mxprobe](https://github.com/andrewchmr/mxprobe)** — Email verification for AI agents: one call returns send, hold or kill for an address, with the reason. The free DNS tier runs locally with no key; the hosted SMTP probe costs 9 USD per 10,000 checks. Signup and credits are API calls too, so an outreach agent provisions itself (no dashboard, no CAPTCHA). npx -y mxprobe mcp
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mxprobe check hello@example.com # free DNS tier, local, no key`</sub>
- **[arbengine/mailbox-mcp](https://github.com/arbengine/mailbox-mcp)** — Physical mail API for AI agents. Send letters, certified mail, postcards, and batch mailings with cost previews, approval controls, tracking, and webhooks
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/arbengine/mailbox-mcp.git`</sub>
- **[bababoi-bibilabu/agent-mq](https://github.com/bababoi-bibilabu/agent-mq)** — Message queue for AI coding assistants. Let AI agents (Claude Code, Cursor, Codex) send messages to each other across sessions and machines. UUID-based auth, self-hostable
  <sub>★ 2 · Python · MIT · clone · pushed 2026-03-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/bababoi-bibilabu/agent-mq`</sub>
- **[clawaimail/mcp](https://github.com/joansongjr/clawaimail)** — Email infrastructure for AI agents. Create inboxes on the fly, send and receive real emails, search messages, and manage threads via API. Install with npx clawaimail-mcp
  <sub>★ 2 · HTML · MIT · pip · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install clawaimail`</sub>
- **[cseguinlz/doubletick-cli](https://github.com/cseguinlz/doubletick-cli)** — Email read tracking via Gmail. Send tracked emails, check if they were opened with open count, device, and timing
  <sub>★ 2 · JavaScript · MIT · npm · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g doubletick-cli`</sub>
- **[farukkolip/instapdown-mcp](https://github.com/farukkolip/instapdown-mcp)** — Instagram creator toolkit MCP with 16 tools: Reels / video / Story / carousel / photo / profile-pic downloaders, Reels-to-MP3 audio extractor, engagement health check + weighted engagement-rate calculator, live hashtag search + 25 curated niches + creator hashtag audit, 900 Reels hook templates by niche and country, 22 Unicode font styles, best-time-to-post for 17 markets (Buffer 2026 verified dat
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y instapdown-mcp`</sub>
- **[iletimerkezi/iletimerkezi-mcp-server](https://github.com/iletimerkezi/iletimerkezi-mcp-server)** — Send SMS, query delivery reports, manage senders / blacklists, register and check İYS (Turkish messaging consent registry) records through the iletiMerkezi BTK-licensed SMS API. 11 tools, runtime-fetched manifest stays in lock-step with the live API. Install: npx -y @iletimerkezi/mcp-server
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/iletimerkezi/iletimerkezi-mcp-server.git`</sub>
- **[krystiangw/meet-live-assist-extension](https://github.com/krystiangw/meet-live-assist-extension)** — Puts the agent you already run inside a live Google Meet or Zoom call. A Chrome extension reads the on-screen captions, a local server hands them over MCP, and the agent answers in a side panel while people are still talking, posts to the meeting chat, and reads screenshots of a shared screen. Transcripts and screenshots are files on your own disk; there is no hosted service and no account. Needs
  <sub>★ 2 · JavaScript · npx · pushed 2026-08-18 · macOS</sub>
  <sub>`npx meet-live-assist-server`</sub>
- **[Leximo-AI/leximo-ai-call-assistant-mcp-server](https://github.com/Leximo-AI/leximo-ai-call-assistant-mcp-server)** — Make AI-powered phone calls on your behalf — book reservations, schedule appointments, and view call transcripts
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-02-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Leximo-AI/leximo-ai-call-assistant-mcp-server.git`</sub>
- **[multimail-dev/mcp-server](https://github.com/multimail-dev/mcp-server)** — Email for AI agents. Send and receive as markdown with configurable human oversight (monitor, gate, or fully autonomous)
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @mvanhorn/printing-press install multimail`</sub>
- **[Sequenzy/mcp](https://github.com/Sequenzy/mcp)** — Email marketing automation MCP server for Sequenzy. Manage subscribers, lists, segments, templates, campaigns, sequences, transactional emails, analytics, and AI-generated email content. Install: npx -y @sequenzy/mcp
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @sequenzy/mcp`</sub>
- **[wazionapps/mcp-server](https://github.com/wazionapps/mcp-server)** — 244 WhatsApp Business tools: send messages, automate workflows, run campaigns, and manage CRM. Streamable HTTP + stdio
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-03-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @wazion/mcp-server`</sub>
- **[ExpertVagabond/solmail-mcp](https://github.com/ExpertVagabond/solmail-mcp)** — Send physical mail with Solana payments — AI agents can compose, price, and send letters and postcards via cryptocurrency
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx solmail-mcp@latest`</sub>
- **[getpoststack/mcp](https://github.com/getpoststack/mcp)** — EU-hosted email API exposed as MCP tools — send transactional and marketing email, manage contacts and segments, run broadcasts, render templates, and read analytics from Claude/Cursor. GDPR compliant, EU-only data residency (Germany + Finland). npx -y @poststack.dev/mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @poststack.dev/mcp --print-config claude-desktop`</sub>
- **[grzgrzgrz3/pingwa-client](https://github.com/grzgrzgrz3/pingwa-client)** — WhatsApp notifications for AI agents with zero setup — no Meta account, no templates, no dashboard: text "join", get an API key, send in 60 seconds (uvx pingwa mcp or remote at pingwa.dev/mcp). Two-way: ask with tap-to-answer buttons, check_replies. Official Meta Cloud API — won't ban your number
  <sub>★ 1 · Python · MIT · uv · pushed 2026-07-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx pingwa send "build finished ✅" # notify your own phone`</sub>
- **[hgn/mcp-server-notmuch](https://github.com/hgn/mcp-server-notmuch)** — notmuch MCP server. Wraps the notmuch CLI to give your LLM access to a local Maildir: full-text search, tag filtering, thread view, attachment reading (PDF, office docs, .ics), related-thread lookup, and unanswered-mail tracking. Optionally write plain-text drafts into a local maildir (--allow-drafts) or manage tags (--allow-tags). No SMTP, no sendmail
  <sub>★ 1 · Python · MIT · pip · pushed 2026-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install 'mcp-server-notmuch[image]'`</sub>
- **[helbertparanhos/resend-email-mcp](https://github.com/helbertparanhos/resend-email-mcp)** — The most complete Resend email MCP — full API coverage (75 tools) plus a unique debug/diagnostics layer: deliverability analysis, DNS troubleshooting, email inspection, bounce explanation, and account audit. npx -y resend-email-mcp
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/helbertparanhos/resend-email-mcp.git`</sub>
- **[markmnl/fmsg-mcp](https://github.com/markmnl/fmsg-mcp)** — Give any AI agent its own address on fmsg, an open federated messaging protocol: inbox, threads, replies, reactions, attachments and a wait-for-message tool for agent-to-agent and human-to-agent conversations. Runs locally over stdio or as a hosted endpoint where each user brings their own API key. Install with npx -y @markmnl/fmsg-mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @markmnl/fmsg-mcp --http 0.0.0.0:8765`</sub>
- **[jcoulaud/shipmail-mcp](https://github.com/shipmail-to/shipmail-mcp)** — Business email MCP server for AI agents. Manage custom-domain mailboxes, read and send messages, draft replies, inspect threads, and automate Shipmail REST API/webhook workflows
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y shipmail-mcp`</sub>
- **[TheSameAbramovych/qmailing-mcp-server](https://github.com/TheSameAbramovych/qmailing-mcp-server)** — AI agents read &amp; send email, manage mailboxes, custom domains and webhooks via the QMailing API (npm stdio + hosted OAuth connector)
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-06-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TheSameAbramovych/qmailing-mcp-server.git`</sub>
- **[rchanllc/joltsms-mcp-server](https://github.com/rchanllc/joltsms-mcp-server)** — Provision dedicated real-SIM US phone numbers, receive inbound SMS, poll for messages, and extract OTP codes. Built for AI agents automating phone verification across platforms
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-02-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/rchanllc/joltsms-mcp-server.git`</sub>
- **[kudosity/mcp](https://github.com/kudosity/mcp)** — Official Kudosity server for SMS, MMS and WhatsApp messaging: send messages, pull delivery reports and replies, manage contacts and contact lists, configure webhooks, check balance, and discover the live API. 19 tools, API key auth. Install: npx -y kudosity-mcp
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kudosity/mcp`</sub>
- **[marras0914/agent-toolbelt](https://github.com/marras0914/agent-toolbelt)** — 20 focused API tools for AI agents: schema generation, text extraction, token counting, regex/cron building, prompt optimization, web summarization, document comparison, and more. TypeScript SDK + LangChain wrappers included
  <sub>★ 1 · TypeScript · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y agent-toolbelt-mcp`</sub>
- **[Pingfyr/mcp](https://github.com/Pingfyr/mcp)** — The scheduled delivery API for developers. Schedule reminders, notifications, and webhooks with one API call
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @pingfyr/mcp`</sub>
- **[qq418716640/botbell-mcp](https://github.com/qq418716640/botbell-mcp)** — Send push notifications to iPhone, iPad, and Mac from AI assistants. Two-way messaging — users reply in the BotBell app, AI reads and continues. Supports action buttons, Markdown, and multi-bot management via PAT
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @botbell/mcp-server`</sub>
- **[serhiizghama/viber-mcp](https://github.com/serhiizghama/viber-mcp)** — MCP server for the Viber Bot REST API. Send text, pictures, videos, files, locations, and contacts; broadcast to up to 300 recipients; manage webhooks and inspect account/user state — 13 tools, fully typed, available on npm as @serhii.zghama/viber-mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @serhii.zghama/viber-mcp`</sub>
- **[SirGreed808/zoho-mail-mcp](https://github.com/SirGreed808/zoho-mail-mcp)** — MCP server for Zoho Mail. Read, search, and send email from Claude
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-04-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SirGreed808/zoho-mail-mcp`</sub>
- **[Spix-HQ/spix-mcp](https://github.com/Spix-HQ/spix-mcp)** — Give AI agents a real phone number and voice. Make outbound calls, handle inbound calls, send email, and manage contacts via 26 MCP tools. ~500ms voice latency (Deepgram Nova-3 + Claude + Cartesia Sonic-3). Install: pip install spix-mcp. Free tier available
  <sub>★ 1 · Python · MIT · uv · pushed 2026-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx spix-mcp`</sub>
- **[textbee/textbee-mcp](https://github.com/textbee/textbee-mcp)** — Send and read SMS through your own Android phone via textbee.dev, the open-source SMS gateway. Three tools: send_sms, get_messages (replies, codes, delivery status), list_devices. Self-hosted friendly. npx -y @textbee/mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @textbee/mcp`</sub>
- **[webtoolbox/websitetoolbox-mcp](https://github.com/webtoolbox/websitetoolbox-mcp)** — MCP server for the Website Toolbox forum platform. Exposes the Forum REST API as MCP tools for Categories, Topics, Posts, Users, User Groups, Conversations, Messages, Moderators, Tags, and Page Views
  <sub>★ 1 · JavaScript · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g websitetoolbox-mcp`</sub>
- **[YS-projectcalc/agent-cold-email](https://github.com/YS-projectcalc/agent-cold-email)** — Coldrig: cold-email infrastructure your agent operates end to end — buy domains, provision mailboxes, warm up, run sequences, and handle replies (28 tools, remote streamable-HTTP or stdio via npx agent-cold-email). Free sandbox: npx agent-cold-email demo
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-cold-email demo`</sub>
- **[starnikovoleg/tgatlas-mcp](https://github.com/starnikovoleg/tgatlas-mcp)** — Public Telegram channels without a user session: channel profiles, posts with view and forward counts, the discussion thread under a post, and the channels Telegram itself recommends
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx tgatlas-mcp`</sub>
- **[agentmail-toolkit/mcp](https://github.com/agentmail-to/agentmail-toolkit/tree/main/mcp)** — An MCP server to create inboxes on the fly to send, receive, and take actions on email. We aren't AI agents for email, but email for AI Agents
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/agentmail-to/agentmail-toolkit.git && cd agentmail-toolkit/mcp`</sub>
- **[aisenseapi/aamio-python](https://github.com/aisenseapi/aamio-python)** — Ephemeral rendezvous for agents: threads with a secret read key and a public write address that expire on time, receipts that outlive them, and an open board where agents that have never met find each other. Hosted at aamio.at/mcp with no account, or as a local runtime that keeps the key
  <sub>Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install aamio # or: pipx install aamio`</sub>
- **[Choppaaahh/sendgrid-mcp-secure](https://github.com/Choppaaahh/sendgrid-mcp-secure)** — Security-first SendGrid MCP server: recipient/domain allowlists, send caps per time window, review-mode, audit log, and no silent BCC (off at the server, not a caller argument). Hardened against the postmark-mcp BCC-exfil incident class
  <sub>Python · MIT · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Choppaaahh/sendgrid-mcp-secure.git`</sub>
- **[dialgoodian/clawdcall-mcp](https://github.com/dialgoodian/clawdcall-mcp)** — Let AI agents place consent-based outbound phone calls and retrieve transcripts, summaries, and outcomes. Use the hosted Streamable HTTP server or install with npx -y clawdcall-mcp
  <sub>TypeScript · MIT · clone · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dialgoodian/clawdcall-mcp.git`</sub>
- **[dockndevai/mcp-outlook](https://github.com/dockndevai/mcp-outlook)** — Safe-by-default Microsoft Outlook mail server (Microsoft Graph). Read, search, draft, send, reply, forward and organize email. Browser sign-in (OAuth authorization-code + PKCE; tokens cached locally, no password handling); read-only by default with layered access modes, a send gate, folder allowlists/protected folders, dry-run and JSON audit logging, plus human-in-the-loop confirmation on send and
  <sub>TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @dockndevai/mcp-outlook`</sub>
- **[csitte/mailwarden](https://github.com/csitte/mailwarden)** — Native Gmail MCP server with full mailbox control — search, read, label, archive, trash, download attachments, and the feature no other Gmail server ships: snooze threads until a date. Every call hits the live Gmail API (no synced index that silently misses mail). Install with npx -y mailwarden
  <sub>TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mailwarden --auth`</sub>
- **[drsound/markdown-to-whatsapp](https://github.com/drsound/markdown-to-whatsapp)** — Convert Markdown into WhatsApp's formatting, so agent output renders as bold, lists and quotes instead of showing raw asterisks. Tables become monospace boxes sized to the reader's bubble width, degrading through padding removal, compact borders and word wrapping before falling back to a list. No API key, runs locally with npx markdown-to-whatsapp mcp
  <sub>JavaScript · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx markdown-to-whatsapp notes.md # a file…`</sub>
- **[elie222/inbox-zero](https://github.com/elie222/inbox-zero/tree/main/apps/mcp-server)** — An MCP server for Inbox Zero. Adds functionality on top of Gmail like finding out which emails you need to reply to or need to follow up on
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/elie222/inbox-zero.git && cd inbox-zero/apps/mcp-server`</sub>
- **[flovoice53-tech/sms-florin-mcp](https://github.com/flovoice53-tech/sms-florin-mcp)** — Rent real UK phone numbers (EE/Three SIM cards, not VoIP) and receive SMS/OTP codes for WhatsApp, Telegram, Google, Discord, and more. 4 tools: list services, rent a number, check rental status, wait for the code. Install: npx -y sms-florin-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y sms-florin-mcp`</sub>
- **[gambot-ai/gambot-mcp](https://github.com/gambot-ai/gambot-mcp)** — Official Gambot WhatsApp Business API server — send WhatsApp messages &amp; templates and manage CRM: contacts, leads, cases, tasks, quotes, invoices, orders, forms, e-signatures, documents and campaigns. Meta-approved Cloud API. Install: npx -y gambot-mcp (set GAMBOT_TOKEN)
  <sub>TypeScript · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gambot-ai/gambot-mcp.git`</sub>
- **[giggal-ai/giggal-mcp](https://github.com/giggal-ai/giggal-mcp)** — Runs a deep mailbox existence check on every address and verifies catch-all, accept-all, and even SEG protected emails (Proofpoint, Mimecast, Barracuda). Keeps bounce rates under 5%, single or bulk
  <sub>TypeScript · MIT · docker · pushed 2026-08-19 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e GIGGAL_API_KEY=tp_live_... giggal-mcp`</sub>
- **[gopalrajsuresh/covalent-bond](https://github.com/gopalrajsuresh/covalent-bond)** — Pair two AI coding agents on different machines over an end-to-end-encrypted channel: files and messages travel through a relay that only ever sees ciphertext - it can never read your data - authenticated by a short code shared out-of-band, with human consent before any file is written. Install with npx covalent-bond
  <sub>JavaScript · MIT · clone · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gopalrajsuresh/covalent-bond.git`</sub>
- **[sendchamp/ai](https://github.com/sendchamp/ai)** — Official Sendchamp docs MCP server for AI coding agents. Read-only search and retrieval over SMS, OTP verification, and Africa-specific routing documentation. Endpoint: https://mcp.sendchamp.com/docs. Pair with Agent Skills via npx skills add sendchamp/ai
  <sub>TypeScript · MIT · npx · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sendchamp/ai --skill sendchamp-sms-send-message --agent cursor`</sub>
- **[shichuanqiong/AgoraDM](https://github.com/shichuanqiong/AgoraDM)** — DM / IM layer for AI agents over the A2A 1.0 protocol: give your assistant an inbox, a friend list, group threads, and per-friend persistent memory to message other people's agents in real time — with SSE wake daemons so it answers while you're away. pip install agoradm-mcp
  <sub>Python · Apache-2.0 · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agoradm`</sub>
- **[radmail-ai/radmail-mcp](https://github.com/radmail-ai/radmail-mcp)** — Email operating system for agents: a search tool to find the one message by sender/subject/content (no filesystem grep), two-axis triage (importance × urgency), an explainable "Right Now" lane, commitment follow-through, and reviewable drafts. A machine-verifiable hard-stop keeps money/banking-change/first-contact human-only (BEC defense). Zero-auth HTTP sandbox at radmail.ai/api/mcp/sandbox — no
  <sub>TypeScript · MIT · clone · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/radmail-ai/radmail-mcp`</sub>
- **[redditapis/redditapis-mcp](https://github.com/redditapis/redditapis-mcp)** — MCP server for the Reddit API: 22 read-only tools covering subreddit listings, post/comment/community/user search, comment trees, and top posts. Bearer token auth
  <sub>JavaScript · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/redditapis/redditapis-mcp.git`</sub>
- **[Rheopyrin/ox-mcp](https://github.com/Rheopyrin/ox-mcp)** — Email (IMAP/SMTP), mail filters (Sieve), calendar (CalDAV), contacts (CardDAV), and free/busy scheduling for Open-Xchange and standards-based mail platforms. Published on the official MCP Registry
  <sub>TypeScript · MIT · npx · pushed 2026-07-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @rheopyrin/ox-mcp`</sub>
- **[flovoice53-tech/agent-identity-mcp](https://github.com/flovoice53-tech/agent-identity-mcp)** — Give AI agents a disposable email address and a real UK phone number to complete signup/OTP verification flows end-to-end. 5 tools covering test email inbox + SMS code retrieval
  <sub>TypeScript · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/flovoice53-tech/agent-identity-mcp.git`</sub>
- **[jaimenbell/discord-mcp](https://github.com/jaimenbell/discord-mcp)** — MCP server over the Discord REST API: read-only tools for listing channels, categories, roles, member roles and permission overwrites, plus write tools for channel, role, guild and message management that stay gated off by default. pip install jaimenbell-discord-mcp
  <sub>Python · MIT · source · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jaimenbell/discord-mcp.git`</sub>
- **[jaspertvdm/mcp-server-rabel](https://github.com/jaspertvdm/mcp-server-rabel)** — AI-to-AI messaging via I-Poll protocol and AInternet. Enables agents to communicate using .aint domains, semantic messaging, and trust-based routing
  <sub>unavailable</sub>
- **[kojott/mailmcp-dist](https://github.com/kojott/mailmcp-dist)** — Self-hosted multi-account email server for ChatGPT and Claude: Gmail, iCloud, Fastmail or any IMAP/SMTP mailbox, as many as you like. Search, read, threaded replies, drafts, allowlisted sending and attachments; passwords are encrypted in the browser and the server stores nothing. Remote (OAuth) or Claude Desktop (.mcpb)
  <sub>JavaScript · source · pushed 2026-09-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/kojott/mailmcp-dist.git`</sub>
- **[lettio-eu/mcp](https://github.com/lettio-eu/mcp)** — Private, EU-hosted email for AI agents over the open JMAP standard. Read, search, reply in-thread, organize and send from your own mailbox. Hosted remote server with OAuth at https://mcp.lettio.eu/mcp, or run locally via npx -y @lettio/mcp. Sending is pinned to the signed-in mailbox, so an agent can never send from another address
  <sub>TypeScript · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lettio-eu/mcp.git`</sub>
- **[LimzoCom/limzo-mcp](https://github.com/LimzoCom/limzo-mcp)** — Read-only stats for public Telegram groups tracked by Limzo, the Telegram anti-spam and moderation bot: search groups, then pull leaderboards, activity trends, member levels and moderation summaries. No API key; run npx -y limzo-mcp or connect to https://limzo.com/api/public/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx limzo-mcp`</sub>
- **[loicfontaine-max/qorami-sdk](https://github.com/loicfontaine-max/qorami-sdk/tree/main/mcp)** — Check an email before an AI agent sends it: returns send / ask-a-human / block, with machine reason codes and prompt-injection detection
  <sub>Python · MIT · in-repo · pushed 2026-07-03</sub>
  <sub>`git clone https://github.com/loicfontaine-max/qorami-sdk.git && cd qorami-sdk/mcp`</sub>
- **[ma2no4413/outlook-mcp](https://github.com/ma2no4413/outlook-mcp)** — Restructure a large Outlook / Hotmail mailbox. move_folder relocates a whole folder subtree in one API call — thousands of messages change place without being moved, their IDs stay valid, and inbox rules pointing at that folder keep working. Also bulk move and bulk mark-read with dry-run previews, and server-side inbox rules as first-class tools. Replies are written to Drafts; there is no send too
  <sub>Python · MIT · docker · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it --rm -e OUTLOOK_CLIENT_ID=<your-id> \`</sub>
- **[MailFlat/mailflat-sdks](https://github.com/MailFlat/mailflat-sdks/tree/main/packages/mcp)** — Email inboxes for agents, with the one-time code returned as a field instead of a regex over the message body. Addresses are permanent; only the messages expire, on a retention window you choose. uvx mailflat-mcp
  <sub>Python · MIT · in-repo · pushed 2026-08-23</sub>
  <sub>`git clone https://github.com/MailFlat/mailflat-sdks.git && cd mailflat-sdks/packages/mcp`</sub>
- **[Metaverse-Cloud/engagelab-email-mcp](https://github.com/Metaverse-Cloud/engagelab-email-mcp)** — Official EngageLab Email MCP server for AI agents to send, receive, monitor, and reply to email with thread context. Install with npx -y @engagelabemail/mcp
  <sub>TypeScript · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Metaverse-Cloud/engagelab-email-mcp`</sub>
- **[ni-c/carddav-mcp](https://github.com/ni-c/carddav-mcp)** — Contacts, groups and photos over CardDAV, on any server that speaks the standard — Radicale, Baikal, Nextcloud, SOGo, Fastmail, iCloud. 17 tools. Writes are read-modify-write over the parsed card guarded by ETags, so an X- property some phone wrote in 2014 survives an edit; both group conventions are read and the one written follows what the book already uses; an address book allowlist is enforced
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/carddav-mcp.git`</sub>
- **[ni-c/caldav-mcp](https://github.com/ni-c/caldav-mcp)** — Events, tasks and journal entries over CalDAV, on any server that speaks the standard — Radicale, Baikal, Nextcloud, SOGo, Fastmail, iCloud. 22 tools. Recurring events are expanded client-side rather than trusted to the server, a calendar allowlist is enforced where ids are decoded, writes are read-modify-write guarded by ETags, and deleting or changing a whole series asks a person first. Calendar
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/caldav-mcp.git`</sub>
- **[ni-c/smtp-mcp](https://github.com/ni-c/smtp-mcp)** — Sends, replies to and forwards mail over plain SMTP, so it works with the mail account you already have. Sending is off until you name the recipients it may write to: every address in To, Cc and Bcc is checked against that allowlist before a connection is opened, and each message is then approved by a person through an MCP elicitation, with recipients and subject on their own labelled lines. There
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/smtp-mcp.git`</sub>
- **[ni-c/ntfy-mcp](https://github.com/ni-c/ntfy-mcp)** — Send push notifications through ntfy, read back what was sent, and revise a notification in place while a job runs, so subscribers watch one message change instead of collecting five. Thirteen tools including user and topic-access administration; the tool list narrows to a curated six. npx -y @ni-c/ntfy-mcp
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/ntfy-mcp.git`</sub>
- **[paigy-ai/mcp](https://github.com/paigy-ai/mcp)** — Call, text, or push the user's phone when an agent needs input mid-task — reply by voice instead of babysitting a long-running or blocked terminal. Works with any MCP client, not just Claude. Install: npx -y @paigy/mcp@latest
  <sub>Shell · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y -p @paigy/mcp@latest paigy-mcp-onboard`</sub>
- **[Sendmux/sendmux-sdk](https://github.com/Sendmux/sendmux-sdk/tree/main/packages/python/mcp)** — Email inbox API MCP server for AI agents to receive, search, and send mail through hosted or local Sendmux Product MCP
  <sub>PHP · MIT · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/Sendmux/sendmux-sdk.git && cd sendmux-sdk/packages/python/mcp`</sub>
- **[sounny/sounnyforms-mcp](https://github.com/sounny/sounnyforms-mcp)** — Zero-API-key serverless form backend, lead triage, and instant contact form generator for static sites, React, and JAMstack apps. Install with npx -y sounnyforms-mcp
  <sub>JavaScript · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sounny/sounnyforms-mcp.git`</sub>
- **[liagha/termgram](https://github.com/liagha/termgram)** — MTProto Telegram from your terminal: CLI for messages, media and contacts, an MCP server that pushes server-to-client notifications when new messages land, and an SSE stream for external consumers
  <sub>Rust · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/liagha/termgram.git`</sub>
- **[timkulbaev/mcp-gmail](https://github.com/timkulbaev/mcp-gmail)** — Full Gmail operations via Unipile API: send, reply, list, read, delete, search, manage labels, attachments, and drafts. Dry-run by default on destructive actions
  <sub>unavailable</sub>
- **[trycourier/courier-mcp](https://github.com/trycourier/courier-mcp)** — Build multi-channel notifications into your product, send messages, update lists, invoke automations, all without leaving your AI coding space
  <sub>unavailable</sub>
- **[vaemail/vaemail-mcp](https://github.com/vaemail/vaemail-mcp)** — Send transactional email, authenticate sending domains, track delivery and diagnose deliverability. Scoped API keys, idempotent requests and dry-run. npx -y vaemail mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y vaemail mcp`</sub>
- **[windborne/zulipmcp](https://github.com/windborne/zulipmcp)** — Run AI agents in Zulip as @mentionable bots — or wire into any MCP client. Real-time listening, session management, file handling
  <sub>Python · Apache-2.0 · source · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/windborne/zulipmcp.git`</sub>
- **[zerodrop-dev/zerodrop-mcp](https://github.com/zerodrop-dev/zerodrop-mcp)** — Disposable email inboxes for AI agents — OTPs and magic links auto-extracted from verification emails. Test signups and auth flows, no signup needed
  <sub>JavaScript · MIT · source · pushed 2026-07-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zerodrop-dev/zerodrop-mcp.git`</sub>

## Support &amp; Service Management

- **[sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)** — MCP server for Atlassian products (Confluence and Jira). Supports Confluence Cloud, Jira Cloud, and Jira Server/Data Center. Provides comprehensive tools for searching, reading, creating, and managing content across Atlassian workspaces
  <sub>★ 5.9k · Python · MIT · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-atlassian`</sub>
- **[aikts/yandex-tracker-mcp](https://github.com/aikts/yandex-tracker-mcp)** — MCP Server for Yandex Tracker. Provides tools for searching and retrieving information about issues, queues, users
  <sub>★ 118 · Python · Apache-2.0 · uv · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx yandex-tracker-mcp@latest`</sub>
- **[nguyenvanduocit/jira-mcp](https://github.com/nguyenvanduocit/jira-mcp)** — A Go-based MCP connector for Jira that enables AI assistants like Claude to interact with Atlassian Jira. This tool provides a seamless interface for AI models to perform common Jira operations including issue management, sprint planning, and workflow transitions
  <sub>★ 97 · Go · MIT · go · pushed 2026-04-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/nguyenvanduocit/jira-mcp/cmd/jira-cli@latest`</sub>
- **[effytech/freshdesk-mcp](https://github.com/effytech/freshdesk_mcp)** — MCP server that integrates with Freshdesk, enabling AI models to interact with Freshdesk modules and perform various support operations
  <sub>★ 68 · Python · MIT · npx · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @effytech/freshdesk_mcp --client claude`</sub>
- **[incentivai/quickchat-ai-mcp](https://github.com/quickchatai/quickchat-ai-mcp)** — Launch your conversational Quickchat AI agent as an MCP to give AI apps real-time access to its Knowledge Base and conversational capabilities
  <sub>★ 24 · Python · MIT · source · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/incentivai/quickchat-ai-mcp.git`</sub>
- **[Berckan/bugherd-mcp](https://github.com/Berckan/bugherd-mcp)** — MCP server for BugHerd bug tracking. List projects, view tasks with filtering by status/priority/tags, get task details, and read comments
  <sub>★ 7 · JavaScript · MIT · clone · pushed 2026-05-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/berckan/bugherd-mcp.git`</sub>
- **[michaelrice/zendesk-mcp](https://github.com/michaelrice/zendesk-mcp)** — MCP server for Zendesk. Read/write tools for tickets, comments, views, macros, users, groups, organizations, and time tracking; optional Help Center knowledge base and Git-Zen GitLab integration
  <sub>★ 7 · Python · Apache-2.0 · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/michaelrice/zendesk-mcp.git`</sub>
- **[raalarcon9705/jira-mcp](https://github.com/raalarcon9705/jira-mcp)** — Full-featured open source Jira &amp; Confluence MCP server with 24 tools: issue CRUD, sprint lifecycle, comments, transitions, user management, and wiki pages
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx raalarcon-jira-mcp-server`</sub>
- **[selic/mcp-itglue](https://github.com/mspstack/mcp-itglue)** — MCP server for IT Glue, the MSP documentation platform. Semantic vector search over documentation, document and flexible-asset read/write, role-based access control, and bring-your-own-key support
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y mcp-itglue --transport http --port 3000`</sub>
- **[crisphive/crisphive-mcp](https://github.com/crisphive/crisphive-mcp)** — Field-service dispatch and technician scheduling: book jobs against live availability, quote and confirm, and absorb P0 emergencies with sub-3-second cascade rescheduling. 43 tools generated from the same OpenAPI spec as the SDKs, preview/commit on every mutating flow, OAuth 2.1 with an isolated sandbox mode
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/crisphive/crisphive-mcp.git`</sub>
- **[tracegazer/invgate-service-desk-mcp](https://github.com/tracegazer/invgate-service-desk-mcp)** — MCP server for InvGate Service Desk: 96 tools across 11 domains (incidents, users, knowledge base, assets, custom fields, workflows, time tracking), read-only by default with opt-in writes
  <sub>★ 3 · Python · MIT · uv · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx invgate-service-desk-mcp`</sub>
- **[webmilmind1/deskcrew-mcp](https://github.com/webmilmind1/deskcrew-mcp)** — Hosted multi-tenant support-desk MCP; AI agents run tickets over MCP and pay per action in USDC (x402) across six chains, or create and run their own bounty board (the paying wallet owns it); remote streamable-HTTP, no account
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx deskcrew-mcp # public demo desk`</sub>
- **[asyntai/mcp-bridge](https://github.com/asyntai/mcp-bridge)** — Run your website's Asyntai AI support agent from any MCP client: manage the knowledge base, edit agent instructions, read conversations and leads, reply live to visitors and check plan usage
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @asyntai/mcp # run the bridge`</sub>
- **[omnom62/freshdesk-mcp](https://github.com/omnom62/freshdesk-mcp)** — Self-hosted Go MCP server for Freshdesk with 15 tools: ticket search, conversations, attachment text extraction, Vision AI OCR for images, and status/group/company enrichment
  <sub>Go · MIT · source · pushed 2026-09-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/omnom62/freshdesk-mcp.git`</sub>
- **[tom28881/mcp-jira-server](https://github.com/tom28881/mcp-jira-server)** — Comprehensive TypeScript MCP server for Jira with 20+ tools covering complete project management workflow: issue CRUD, sprint management, comments/history, attachments, batch operations
  <sub>unavailable</sub>

## Customer Data Platforms

- **[antv/mcp-server-chart](https://github.com/antvis/mcp-server-chart)** — A Model Context Protocol server for generating visual charts using AntV
  <sub>★ 4.4k · TypeScript · MIT · npm · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @antv/mcp-server-chart`</sub>
- **[hustcc/mcp-mermaid](https://github.com/hustcc/mcp-mermaid)** — Generate mermaid diagram and chart with AI MCP dynamically
  <sub>★ 635 · TypeScript · MIT · npm · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-mermaid`</sub>
- **[saurabhsharma2u/search-console-mcp](https://github.com/saurabhsharma2u/search-console-mcp)** — An MCP server to interact with Google Search Console and Bing Webmasters
  <sub>★ 293 · TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx search-console-mcp setup`</sub>
- **[QuackbackIO/quackback](https://github.com/QuackbackIO/quackback)** — Open-source customer feedback platform with built-in MCP server. Agents can search feedback, triage posts, update statuses, create and comment on posts, vote, manage roadmaps, merge duplicates, and publish changelogs
  <sub>★ 284 · TypeScript · AGPL-3.0 · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 --env-file .env quackback`</sub>
- **[hustcc/mcp-echarts](https://github.com/hustcc/mcp-echarts)** — Generate visual charts using Apache ECharts with AI MCP dynamically
  <sub>★ 270 · TypeScript · MIT · npm · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-echarts`</sub>
- **[OpenDataMCP/OpenDataMCP](https://github.com/OpenDataMCP/OpenDataMCP)** — Connect any Open Data to any LLM with Model Context Protocol
  <sub>★ 154 · Python · MIT · clone · pushed 2024-12-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenDataMCP/OpenDataMCP.git`</sub>
- **[tinybirdco/mcp-tinybird](https://github.com/tinybirdco/mcp-tinybird)** — An MCP server to interact with a Tinybird Workspace from any MCP client
  <sub>★ 79 · Python · Apache-2.0 · source · pushed 2025-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tinybirdco/mcp-tinybird.git`</sub>
- **[sergehuber/inoyu-mcp-unomi-server](https://github.com/inoyu-dev/inoyu-mcp-unomi-server)** — An MCP server to access and updates profiles on an Apache Unomi CDP server
  <sub>★ 10 · JavaScript · Apache-2.0 · source · pushed 2025-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sergehuber/inoyu-mcp-unomi-server.git`</sub>
- **[iaptic/mcp-server-iaptic](https://github.com/iaptic/mcp-server-iaptic)** — Connect with iaptic to ask about your Customer Purchases, Transaction data and App Revenue statistics
  <sub>★ 9 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-server-iaptic`</sub>
- **[ckalima/pipedrive-mcp-server](https://github.com/ckalima/pipedrive-mcp-server)** — MCP server for Pipedrive CRM. 155 tools covering deals, persons, organizations, activities, products, projects, tasks, leads, notes, mail, and fields. stdio transport, API-key auth, delete tools gated behind an env flag. Published on npm as @ckalima/pipedrive-mcp-server. MIT
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @ckalima/pipedrive-mcp-server init`</sub>
- **[embeddedlayers/mcp-analytics](https://github.com/embeddedlayers/mcp-analytics)** — Statistical analysis, forecasting, and ML for business data (Shopify, Stripe, WooCommerce, eBay, GA4, Search Console). Upload a CSV or connect live data sources — ask a question in Claude or Cursor, get an interactive HTML report
  <sub>★ 7 · JavaScript · MIT · source · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/embeddedlayers/mcp-analytics.git`</sub>
- **[lionkiii/google-searchconsole-mcp](https://github.com/lionkiii/google-searchconsole-mcp)** — Google Search Console MCP server with 13 SEO tools — search analytics, URL inspection, sitemap management, keyword opportunities, brand analysis, and performance comparison
  <sub>★ 7 · JavaScript · MIT · npm · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g google-searchconsole-mcp`</sub>
- **[Aleksey-Panf/b2b-enrichment-mcp](https://github.com/Aleksey-Panf/b2b-enrichment-mcp)** — B2B lead enrichment server integrating Hunter.io and Apollo APIs. 9 tools for email discovery, domain search, company data, and contact verification
  <sub>★ 3 · Python · clone · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Aleksey-Panf/b2b-enrichment-mcp.git`</sub>
- **[azmartone67/dchub-mcp-server](https://github.com/azmartone67/dchub-mcp-server)** — Data-center, power &amp; gas intelligence MCP server. 33 tools covering 21,000+ data-center facilities (170+ countries), 232 US power markets scored by the DC Hub Power Index (DCPI), 2,000+ tracked M&amp;A deals, ISO grid telemetry (PJM, ERCOT, CAISO, MISO, SPP, NYISO), fiber routes, and energy pricing. Free to cite (CC-BY-4.0)
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @azmartone67/dchub --client claude`</sub>
- **[mambalabsdev/mcp-icp-fit-scorer](https://github.com/mambalabsdev/mcp-icp-fit-scorer)** — Scores a company against a weighted ideal customer profile, returning a 0-100 score, A/B/C tier, and per-signal breakdown
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-icp-fit-scorer.git`</sub>
- **[skippedaga/yanifend-mcp](https://github.com/skippedaga/yanifend-mcp)** — Hosted MCP server for YaniFend, a WordPress feedback widget — manage your questionary (list / create / update / delete questions and options) and read collected answers via natural language
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y yanifend-mcp`</sub>
- **[ictinnovations/ictcrm-mcp](https://github.com/ictinnovations/ictcrm-mcp)** — MCP server for ICTCRM, an open source CRM with built-in telephony. Reads contact groups by default. Creating and deleting contacts, and adding them to a calling campaign, are only registered when ICTCRM_MCP_ALLOW_WRITE=true, so a default install cannot enrol anyone into an outbound campaign. Zero-install via npx -y ictcrm-mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ictcrm-mcp`</sub>
- **[bouncewatch/mcp](https://github.com/bouncewatch/mcp)** — Find out what changed at a company and when — funding, senior hires, partnerships, expansion, office openings, customer wins. 40+ event types, each carrying the date it happened and a 1-10 weight, so a funding round outranks a conference booth and you can set a floor that removes the noise. Ask in plain language ("which Dutch companies under 50 people raised in the last month") or put a watch on a
  <sub>JavaScript · MIT · source · pushed 2026-08-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/bouncewatch/mcp.git`</sub>
- **[echoloc-ai/echoloc-mcp](https://github.com/echoloc-ai/echoloc-mcp)** — Company technographics from hiring data: search 760K+ companies by the technologies they use with direction of change (adopting / replacing / evaluating), enrich any domain with firmographics and hiring signals, and browse a 10,000+ technology catalog. Free tier, remote server at api.echoloc.ai/mcp
  <sub>Python · MIT · docker · pushed 2026-07-29 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e ECHOLOC_API_KEY=YOUR_API_KEY echoloc-mcp`</sub>

## Marketing

- **[pipeboard-co/meta-ads-mcp](https://github.com/pipeboard-co/meta-ads-mcp)** — Meta Ads automation that just works. Trusted by 10,000+ businesses to analyze performance, test creatives, optimize spend, and scale results — simply and reliably
  <sub>★ 1.3k · Python · brew · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install pipeboard-co/tap/pipeboard`</sub>
- **[gomarble-ai/facebook-ads-mcp-server](https://github.com/gomarble-ai/facebook-ads-mcp-server)** — MCP server acting as an interface to the Facebook Ads, enabling programmatic access to Facebook Ads data and management features
  <sub>★ 366 · Python · MIT · npx · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @gomarble-ai/facebook-ads-mcp-server --client claude`</sub>
- **[open-strategy-partners/osp_marketing_tools](https://github.com/open-strategy-partners/osp_marketing_tools)** — A suite of marketing tools from Open Strategy Partners including writing style, editing codes, and product marketing value map creation
  <sub>★ 272 · Python · CC-BY-SA-4.0 · source · pushed 2025-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/open-strategy-partners/osp_marketing_tools.git`</sub>
- **[stape-io/google-tag-manager-mcp-server](https://github.com/stape-io/google-tag-manager-mcp-server)** — This server supports remote MCP connections, includes built-in Google OAuth, and provide an interface to the Google Tag Manager API
  <sub>★ 218 · TypeScript · Apache-2.0 · clone · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stape-io/google-tag-manager-mcp-server`</sub>
- **[gomarble-ai/google-ads-mcp-server](https://github.com/gomarble-ai/google-ads-mcp-server)** — MCP server acting as an interface to the Google Ads, enabling programmatic access to Google Ads data and management features
  <sub>★ 144 · Python · MIT · clone · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/google-ads-mcp-server.git`</sub>
- **[PascaleBeier/hitkeep](https://github.com/PascaleBeier/hitkeep)** — Privacy-first web analytics with a read-only MCP server for aggregate traffic, events, goals, funnels, ecommerce, Search Console, and AI visibility reporting
  <sub>★ 89 · Go · MIT · brew · pushed 2026-09-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install PascaleBeier/hitkeep/hitkeep`</sub>
- **[mikusnuz/meta-ads-mcp](https://github.com/mikusnuz/meta-ads-mcp)** — MCP server for Meta Marketing API v25.0 — 123 tools for Facebook &amp; Instagram ad campaigns, audiences, creatives, insights, catalogs, and automated rules
  <sub>★ 79 · TypeScript · MIT · source · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mikusnuz/meta-ads-mcp.git`</sub>
- **[AdsMCP/tiktok-ads-mcp-server](https://github.com/AdsMCP/tiktok-ads-mcp-server)** — A Model Context Protocol server for TikTok Ads API integration, enabling AI assistants to manage campaigns, analyze performance metrics, handle audiences and creatives with OAuth authentication flow
  <sub>★ 49 · Python · MIT · clone · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AdsMCP/tiktok-ads-mcp-server.git`</sub>
- **[AKzar1el/mcp-geo](https://github.com/AKzar1el/mcp-geo)** — DigestSEO GEO Tracker for measuring brand citations and visibility across ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews. Hosted OAuth endpoint: https://geo-mcp.digestseo.com/mcp
  <sub>★ 45 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx wrangler d1 create mcp-geo-db`</sub>
- **[logly/mureo](https://github.com/logly/mureo)** — Framework for AI agents (Claude Code, Cursor, Codex, Gemini) to operate Google Ads, Meta Ads, and Search Console. Grounded in a local STRATEGY.md — not metric-chasing. Defense-in-depth security, local-first. Apache 2.0
  <sub>★ 45 · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install mureo`</sub>
- **[marketplaceadpros/amazon-ads-mcp-server](https://github.com/MarketplaceAdPros/amazon-ads-mcp-server)** — Enables tools to interact with Amazon Advertising, analyzing campaign metrics and configurations
  <sub>★ 29 · JavaScript · MIT · source · pushed 2025-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MarketplaceAdPros/amazon-ads-mcp-server.git`</sub>
- **[damientilman/mailchimp-mcp-server](https://github.com/damientilman/mailchimp-mcp-server)** — Mailchimp Marketing API integration with 53 tools for managing campaigns, audiences, reports, automations, landing pages, e-commerce data, and batch operations
  <sub>★ 24 · Python · MIT · uv · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mailchimp-mcp # no install required`</sub>
- **[Citedy/citedy-seo-agent](https://github.com/citedy/citedy-seo-agent)** — Full-stack AI marketing toolkit with 41 MCP tools. Scout X/Reddit trends, analyze competitors, find content gaps, generate SEO articles in 55 languages with AI illustrations and voice-over, create social adaptations for 9 platforms, generate AI avatar videos with subtitles, ingest any URL (YouTube, PDF, audio), create lead magnets, and run content autopilot
  <sub>★ 19 · JavaScript · MIT · npx · pushed 2026-06-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx openskills install Citedy/citedy-seo-agent`</sub>
- **[MatiousCorp/google-ad-manager-mcp](https://github.com/MatiousCorp/google-ad-manager-mcp)** — Google Ad Manager API integration for managing campaigns, orders, line items, creatives, and advertisers with bulk upload support
  <sub>★ 18 · Python · MIT · pip · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install google-ad-manager-mcp`</sub>
- **[stape-io/stape-mcp-server](https://github.com/stape-io/stape-mcp-server)** — This project implements an MCP (Model Context Protocol) server for the Stape platform. It allows interaction with the Stape API using AI assistants like Claude or AI-powered IDEs like Cursor
  <sub>★ 17 · Apache-2.0 · source · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/stape-io/stape-mcp-server.git`</sub>
- **[Synter-Media-AI/mcp-server](https://github.com/Synter-Media-AI/mcp-server)** — Cross-platform ad management MCP server with full read and write capabilities across Google, Meta, LinkedIn, Microsoft, Reddit, and TikTok. Create campaigns, adjust budgets, generate creatives, and pull performance data through natural language
  <sub>★ 17 · TypeScript · MIT · npx · pushed 2026-09-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @synterai/mcp-server`</sub>
- **[alexey-pelykh/lhremote](https://github.com/alexey-pelykh/lhremote)** — Open-source CLI and MCP server for LinkedHelper automation — 32 tools for campaign management, messaging, and profile queries via Chrome DevTools Protocol
  <sub>★ 14 · TypeScript · AGPL-3.0 · npm · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g lhremote # or: npx lhremote --help`</sub>
- **[Brand-System/brandsystem-mcp](https://github.com/Brandcode-Studio/brandsystem-mcp)** — Make your brand machine-readable. Extract brand identity (colors, fonts, logo, voice, visual rules) from any website via static CSS + rendered-page extraction, compile into DTCG tokens, brand runtime contracts, and interaction policies. 34 tools across 4 progressive sessions. Subscribable brand://runtime and brand://policy MCP resources. Content compliance scoring (0-100), pass/fail gate, and HTML
  <sub>★ 14 · TypeScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @brandsystem/mcp install --client codex --write`</sub>
- **[AppVisionOS/apple-search-ads-mcp](https://github.com/AppVisionOS/apple-search-ads-mcp)** — Apple Ads (formerly Apple Search Ads) Campaign Management API v5 with 1:1 endpoint coverage — 74 typed tools across campaigns, ad groups, ads, creatives, custom product pages, targeting + negative keywords, performance reports, async impression-share reports, budget orders, ACLs, app/geo discovery, and rejection-reason audits. Multi-org support via per-call override. Install: npm i -g apple-search
  <sub>★ 11 · TypeScript · MIT · clone · pushed 2026-05-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AppVisionOS/apple-search-ads-mcp.git`</sub>
- **[sharozdawa/ai-visibility](https://github.com/sharozdawa/ai-visibility)** — Track brand visibility across ChatGPT, Perplexity, Claude, and Gemini. Visibility scores, sentiment analysis, competitor detection, and trend charts
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-03-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx ai-visibility-mcp`</sub>
- **[acamolese/google-search-console-mcp](https://github.com/acamolese/google-search-console-mcp)** — Google Search Console MCP server: query performance data, inspect URLs, check indexing, and generate brandable HTML SEO audit reports with a 30/60/90-day roadmap. Read-only OAuth scope, installable via uvx mcp-google-search-console
  <sub>★ 8 · Python · MIT · uv · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-google-search-console auth`</sub>
- **[askads/mcp-vk-ads](https://github.com/askads/mcp-vk-ads)** — VK Ads (VK Реклама) API — manage ad plans, ad groups, banners, and pull statistics. Read + write
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-vk-ads@latest`</sub>
- **[tomba-io/tomba-mcp-server](https://github.com/tomba-io/tomba-mcp-server)** — Email discovery, verification, and enrichment tools. Find email addresses, verify deliverability, enrich contact data, discover authors and LinkedIn profiles, validate phone numbers, and analyze technology stacks
  <sub>★ 8 · TypeScript · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tomba-io/tomba-mcp-server.git`</sub>
- **[shensi8312/blogburst-mcp-server](https://github.com/shensi8312/blogburst-mcp-server)** — AI content generation, repurposing, and multi-platform publishing with BlogBurst. Generate blogs, repurpose content for 9+ platforms (Twitter, LinkedIn, Reddit, Bluesky, Threads, Telegram, Discord, TikTok, YouTube), get trending topics, and publish directly
  <sub>★ 7 · JavaScript · MIT · source · pushed 2026-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shensi8312/blogburst-mcp-server.git`</sub>
- **[dkships/substack-publisher-mcp](https://github.com/dkships/substack-publisher-mcp)** — Read-only access to posts, engagement stats, subscriber counts, and subscriber lookup through Substack's official Publisher API. Supports multiple publications
  <sub>★ 6 · TypeScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dkships/substack-publisher-mcp.git`</sub>
- **[AKzar1el/mcp-gsc](https://github.com/AKzar1el/mcp-gsc)** — Google Search Console MCP server for Cloudflare Workers with Google OAuth, organic-search analytics, URL inspection, sitemap management, indexing, and SEO insights
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @digestseo/mcp-gsc`</sub>
- **[askads/mcp-yandex-wordstat](https://github.com/askads/mcp-yandex-wordstat)** — Yandex Wordstat (Яндекс Вордстат) keyword search-demand — top &amp; related queries, demand dynamics, and regional distribution. Read-only, dual-flavor (Yandex Cloud Search API v2 / api.wordstat.yandex.net)
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yandex-wordstat@latest`</sub>
- **[pucilpet/crawlgraph-mcp](https://github.com/pucilpet/crawlgraph-mcp)** — Backlink intelligence and competitor gap analysis on the public Common Crawl webgraph (4.4B edges, 120M domains) via CrawlGraph. 4 tools: backlink lookups, gap analysis, and a composite outreach-targets finder (domains linking to all your competitors but not you, de-noised and ranked by authority). Install: npx -y crawlgraph-mcp
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y crawlgraph-mcp`</sub>
- **[MendleM/Pipepost](https://github.com/MendleM/Pipepost)** — Publish from your terminal. Drafts SEO-scored articles, cross-publishes to Dev.to, Ghost, Hashnode, WordPress, and Medium with auto-wired canonical URLs, generates social posts for Twitter/LinkedIn/Reddit/Bluesky/HN, fetches Unsplash cover images, and submits URLs to IndexNow — all as local stdio, no cloud relay
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-04-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx pipepost-mcp init`</sub>
- **[optifeed/optifeed-radar](https://github.com/optifeed/optifeed-radar)** — Asks ChatGPT, Claude, Gemini and Perplexity real buyer questions and scores whether a brand or its products are actually recommended (AI visibility, GEO/AEO). Brand and product checks, competitor share of voice, cited sources; runs locally with your own API keys
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx optifeed-radar audit yourbrand.com`</sub>
- **[louis030195/apollo-io-mcp](https://github.com/louis030195/apollo-io-mcp)** — B2B sales intelligence and prospecting with Apollo.io. Search for prospects, enrich contacts with emails and phone numbers, discover companies by industry and size, and access Apollo's database of 275M+ contacts
  <sub>★ 4 · JavaScript · MIT · clone · pushed 2025-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/louis030195/apollo-io-mcp.git`</sub>
- **[AIOProductOS/studio-mcp](https://github.com/AIOProductOS/studio-mcp)** — Turns your AI host into a product videographer: scripted screen recordings of your own web app with a visible gliding cursor, camera zooms, highlight callouts, captions, and designed scene transitions, plus marketing-grade screenshots; deterministic dark-frame cleanup and MP4/GIF export. Free and fully local. npx -y @aioproductoscom/mcp-studio
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AIOProductOS/studio-mcp.git`</sub>
- **[adsagents/adsagent-ai-skills](https://github.com/adsagents/adsagent-ai-skills)** — AdsAgent tri-channel plugin + hosted Meta/Google/TikTok MCP (OAuth). Meta: https://adsagent.md/mcp/v2. Registry: md.adsagent/meta-mcp. Docs: https://adsagent.md/docs/mcp-onboarding
  <sub>★ 3 · Python · MIT · clone · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/adsagents/adsagent-ai-skills.git`</sub>
- **[aitit-inc/leadace](https://github.com/aitit-inc/leadace)** — Outbound sales agent for Claude Code. Per-prospect website research, one email per prospect, sending from the user's own Gmail, reply tracking, and structured rejection feedback published as JSON Schema. Open source, self-hostable backend
  <sub>★ 3 · TypeScript · source · pushed 2026-09-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/aitit-inc/leadace.git`</sub>
- **[competlab/competlab-mcp-server](https://github.com/competlab/competlab-mcp-server)** — Competitive intelligence platform with 24 tools. Monitor competitor pricing, content, positioning, tech stacks, and AI visibility — track how ChatGPT, Claude, and Gemini rank your brand
  <sub>★ 3 · TypeScript · MIT · clone · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/competlab/competlab-mcp-server.git`</sub>
- **[localseodata/mcp-server](https://github.com/localseodata/mcp-server)** — 42 local SEO tools for AI assistants. SERP tracking, Google Business Profile data, review monitoring, keyword research, citation audits, geogrid rank scans, AI visibility scoring, and competitive analysis. Install: npx @localseodata/mcp-server or connect to the hosted endpoint at mcp.localseodata.com
  <sub>★ 3 · TypeScript · MIT · clone · pushed 2026-05-11 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/localseodata/mcp-server.git`</sub>
- **[Nolas-Shadow/agent1st-ads-mcp](https://github.com/Nolas-Shadow/agent1st-ads-mcp)** — Meta (Facebook/Instagram) and TikTok ad campaign management for AI agents. One tool call creates a complete campaign — targeting, creative, budget, and ad. Requires license from agent1st.io/ads
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Nolas-Shadow/agent1st-ads-mcp.git`</sub>
- **[meyusufdemirci/app-store-operator](https://github.com/meyusufdemirci/app-store-operator)** — App Store competitive research for indie iOS developers. Ranked keyword search, competitor download/revenue/rating estimates, and iOS In-App Event copy in 14 locales with App Store Connect character limits enforced. Results cached locally for 24 hours; no API key required (competitor estimates use a one-time free SensorTower sign-in). Install: npx -y app-store-operator
  <sub>★ 3 · JavaScript · MIT · docker · pushed 2026-09-08 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm app-store-operator`</sub>
- **[opusforge/gorilla-mcp](https://github.com/opusforge/gorilla-mcp)** — Lead discovery for solo SaaS founders. Searches Reddit, X, YouTube, and TikTok for posts where people describe a problem your product solves, ranks each by buying intent, and returns ranked leads. Includes find_leads, draft_outreach, and plan_acquisition_funnel for the full acquisition flow. Hosted, $0.99 per run. Install: npx -y github:opusforge/gorilla-mcp. Sign up: usegorilla.app
  <sub>★ 3 · JavaScript · MIT · clone · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/opusforge/gorilla-mcp`</sub>
- **[OrbiAds/Orbiads-GAM-MCP](https://github.com/OrbiAds/Orbiads-GAM-MCP)** — Hosted Google Ad Manager MCP server for Claude, ChatGPT, Gemini, and Codex. 200+ tools across campaign management, line items, creatives (image/video/HTML5/native), interactive reporting, inventory exploration, and ad-ops compliance audits. OAuth on-behalf-of-user, GAM API v202602. Free trial at orbiads.com — 5 credits, no credit card
  <sub>★ 3 · Python · MIT · pip · pushed 2026-08-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install orbiads-cli`</sub>
- **[antohins/seo-tools-mcp](https://github.com/antohins/seo-tools-mcp)** — Five read-only SEO servers for the Google/Yandex (RU/CIS) market: SERP (XMLStock), Yandex Wordstat, Google Search Console (Search Analytics + URL Inspection), Yandex.Webmaster, and Yandex.Metrica. ~38 tools, multi-account, OAuth with auto-refresh. Install: npx -y seo-tools-mcp
  <sub>★ 3 · TypeScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/antohins/seo-tools-mcp.git`</sub>
- **[AutomateLab-tech/ai-seo-mcp](https://github.com/AutomateLab-tech/ai-seo-mcp)** — AI-SEO / AEO / GEO audit MCP for any public URL. Scores schema.org coverage, robots.txt and llms.txt health, canonical and OpenGraph setup, and AI-citation likelihood; suggests rewrites tuned for Answer Engine and Generative Engine surfaces. No vendor keys, no crawls of private data. Install: npx -y @automatelab/ai-seo-mcp
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @automatelab/ai-seo-mcp`</sub>
- **[rampify-dev/rampify-mcp](https://github.com/rampify-dev/rampify-mcp)** — The SEO MCP server that acts on your data, not just reads it: crawl your site, find where you're invisible in AI answers, generate the meta/schema/content fix as a spec, and ship it as a PR from Claude Code or Cursor. Built-in DataForSEO keyword data and Google Search Console
  <sub>★ 3 · TypeScript · source · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rampify-dev/rampify-mcp.git`</sub>
- **[AutomateLab-tech/seo-performance-mcp](https://github.com/AutomateLab-tech/seo-performance-mcp)** — Post-publish SEO performance MCP that unifies Google Search Console, Matomo, GA4, Clarity, and AI-citation signals per URL and emits a verdict (refresh / expand / merge / kill / double_down / hold) per post with reason codes
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @automatelab/seo-performance-mcp`</sub>
- **[askads/mcp-yandex-metrica](https://github.com/askads/mcp-yandex-metrica)** — Yandex Metrica (Яндекс Метрика) web analytics — list counters and goals, and pull traffic/conversion statistics. Read-only
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yandex-metrica@latest`</sub>
- **[grovs-io/mcp](https://github.com/grovs-io/mcp)** — Deep linking, attribution, analytics, and campaign management for mobile apps with Grovs — an open-source, privacy-first alternative to Branch and AppsFlyer. 16 tools for creating links, tracking installs and revenue, and configuring app settings
  <sub>★ 2 · TypeScript · MIT · docker · pushed 2026-05-13 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 grovs-mcp`</sub>
- **[live-direct-marketing/ldm-inbox-check-mcp](https://github.com/live-direct-marketing/ldm-inbox-check-mcp)** — Email inbox placement testing across Gmail, Outlook, Yahoo, Mail.ru and Yandex. Create a test, get seed addresses, see per-provider placement (Inbox/Spam/Promotions), SPF/DKIM/DMARC verdicts, and screenshots. Install: npx -y ldm-inbox-check-mcp
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ldm-inbox-check-mcp`</sub>
- **[marykovziridze/screaming-frog-mcp](https://github.com/marykovziridze/screaming-frog-mcp)** — Screaming Frog SEO Spider headless crawls, data export, and technical SEO audit skill for Claude. 8 tools, cross-platform (Mac + Windows), includes a ready-to-use technical SEO scan skill
  <sub>★ 2 · Python · MIT · uv · pushed 2026-04-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx --from git+https://github.com/marykovziridze/screaming-frog-mcp screaming-frog-mcp`</sub>
- **[pghdma/callrail-mcp](https://github.com/pghdma/callrail-mcp)** — CallRail REST API v3 integration with 49 tools for call tracking, form submissions, transcripts, full CRUD on tags/trackers/companies/users, plus agency-specific aggregation tools (usage_summary for per-client cost attribution, compare_periods for MoM deltas, bulk_update_calls with dry-run, spam_detector, call_eligibility_check for Google Ads conversion debugging). Built by an actual CallRail cust
  <sub>★ 2 · Python · MIT · pipx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install callrail-mcp`</sub>
- **[SearchAtlas](https://github.com/search-atlas-group/searchatlas-mcp-server)** — SEO, content generation, PPC, keyword research, site auditing, authority building, and LLM
  <sub>★ 2 · HTML · MIT · npm · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g searchatlas-mcp-server`</sub>
- **[SEOcrawl/seocrawl-mcp](https://github.com/SEOcrawl/seocrawl-mcp)** — SEO + GEO MCP server: live Google Search Console &amp; GA4 data, keyword and page analysis, AI-visibility tracking across ChatGPT, Claude, Gemini &amp; Perplexity, site audit and SEO task management — all from chat
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SEOcrawl/seocrawl-mcp.git`</sub>
- **[Sweeppea-Development-Lab/sweeppea-mcp-info](https://github.com/Sweeppea-Development-Lab/sweeppea-mcp-info)** — Sweepstakes management platform with 70 MCP tools for legally compliant promotions in the US and Canada. Manage participants, official rules, winner drawings, entry pages, billing, and more. Requires a Sweeppea subscription
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Sweeppea-Development-Lab/sweeppea-mcp-info.git`</sub>
- **[smythmyke/markitup-mcp-server](https://github.com/smythmyke/markitup-mcp-server)** — AI image annotation and marketing-visual generator powered by MarkItUp. Five tools: generate polished marketing visuals from a screenshot (Claude writes copy → Gemini renders across 50+ templates including glassmorphic, bold marketing, documentation, and app store), regen, AI outpaint, and HD background removal. Install: npx -y markitup-mcp-server
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/markitup/mcp-server.git`</sub>
- **[Natden444/pickanagency-mcp](https://github.com/Natden444/pickanagency-mcp)** — Search 47,000+ marketing agencies and get AI-matched with fitted agencies (Get Matched engine), from Pick an Agency
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:Natden444/pickanagency-mcp`</sub>
- **[artgas1/yandex-metrika-mcp](https://github.com/artgas1/yandex-metrika-mcp)** — Yandex Metrika (Яндекс Метрика) — complete API coverage: all 108 methods of the Stat, Management and Logs APIs as one tool each, generated from a spec parsed out of Yandex's own documentation, with a drift test that fails when the API changes. Writes disabled by default, tool annotations on every tool, response size ceiling with declared truncation. npx -y yandex-metrika-mcp-server
  <sub>★ 1 · JavaScript · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y yandex-metrika-mcp-server`</sub>
- **[askads/mcp-yandex-direct](https://github.com/askads/mcp-yandex-direct)** — Yandex Direct (Яндекс Директ) API v5 — manage PPC campaigns, ad groups, ads, keywords, bid modifiers, sitelinks/callouts/vcards, and pull statistics. Read + write, sandbox and agency-account aware
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yandex-direct@latest`</sub>
- **[camlowe/mcp-server-reddit-ads](https://github.com/camlowe/mcp-server-reddit-ads)** — Reddit Ads API v3 with working write operations and tiered write-safety controls (read, safe, spend). Manage campaigns, ad groups, ads, budgets, bids, and targeting, pull performance reports, and mint OAuth credentials with a built-in auth command
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-server-reddit-ads auth`</sub>
- **[carlosalvite/foundersignal-mcp](https://github.com/carlosalvite/foundersignal-mcp)** — Ask Claude what SaaS ideas are worth building. Aggregates revenue data, growth signals and pain points from AppSumo, TrustMRR, Product Hunt, Indie Hackers, Reddit and more
  <sub>★ 1 · JavaScript · npx · pushed 2026-05-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx foundersignal-mcp`</sub>
- **[tankstellen/firmenliste-mcp](https://github.com/tankstellen/firmenliste-mcp)** — B2B company address data for the DACH region: search 6,400+ industry lists, check availability and field coverage, get binding price quotes
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tankstellen/firmenliste-mcp.git`</sub>
- **[mukul-dutt/mentionsapi-mcp](https://github.com/mukul-dutt/mentionsapi-mcp)** — Check whether AI recommends your brand — mentions, ranks, and citations across ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews, AI Mode, and Bing Copilot
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @mentionsapi/mcp@latest`</sub>
- **[vibeads/mcp](https://github.com/vibeads/mcp)** — Google Ads for local service businesses — plumbers, HVAC, dentists, roofers. Read tools score the account 0–100 across 6 dimensions, surface wasted spend in search terms, and list active diagnostics from VibeAds' 35+ optimization rules. Write tools (Pro/Max) draft a whole campaign (keywords, ad copy, ad groups), apply it, and execute one approved optimization at a time; anything that spends real m
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @vibeads/mcp`</sub>
- **[drjerryrelth/ghl-command-feedback](https://github.com/drjerryrelth/ghl-command-feedback)** — GoHighLevel (GHL) MCP server. 212 tools across 43 modules including the only programmatic GHL workflow builder (private API, reverse-engineered), funnel + page editor, form builder, pipeline builder, goal event builder, pre-deploy validator, multi-sub-account switching, bulk operations, and full account export. Built for agency operators managing many client GHL sub-accounts. Paid, $97 one-time, 3
  <sub>★ 1 · Dockerfile · MIT · source · pushed 2026-07-26</sub>
  <sub>`git clone https://github.com/drjerryrelth/ghl-command-feedback.git`</sub>
- **[Linkly-HQ/linkly-mcp-server](https://github.com/Linkly-HQ/linkly-mcp-server)** — Official Linkly URL shortener server: create branded short links, read click analytics by country/platform/referrer, manage custom domains and click webhooks. Hosted at mcp.linklyhq.com with OAuth (no API keys); listed in the Claude connector directory
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Linkly-HQ/linkly-mcp-server.git`</sub>
- **[LLM-Pulse/llmpulse-mcp](https://github.com/LLM-Pulse/llmpulse-mcp)** — Hosted MCP server for LLM Pulse AI visibility analytics, including brand mentions, citations, sentiment, share of voice, recommendations, GEO Writer, Search Console, and AI traffic via a Streamable HTTP endpoint
  <sub>★ 1 · JavaScript · MIT · docker · pushed 2026-09-19 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i -e LLMPULSE_API_KEY=llmpulse_your_key_here llmpulse-mcp`</sub>
- **[MailboxValidator/mcp-mailboxvalidator](https://github.com/MailboxValidator/mcp-mailboxvalidator)** — Validates email addresses to reduce email bounces during marketing campaigns
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-06-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/MailboxValidator/mcp-mailboxvalidator.git`</sub>
- **[maxaeo/maxaeo-ai-visibility-mcp](https://github.com/maxaeo/maxaeo-ai-visibility-mcp)** — Local-first AI visibility, GEO/AEO, and llms.txt audit MCP server for Claude, Codex, Cursor, and other agents. Checks AI crawler access, robots, sitemap, canonical, metadata, noindex, and JSON-LD; returns local-only and technical foundation scores, top issues, and action plans. Install: npx -y maxaeo-ai-visibility-mcp
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g maxaeo-ai-visibility-mcp`</sub>
- **[qr-maker-io/mcp-server](https://github.com/qr-maker-io/mcp-server)** — Generate styled QR codes, manage dynamic short links with click analytics, and publish micro-landing pages. Install: npx @qr-maker/mcp-server --api-key=YOUR_KEY
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @qr-maker/mcp-server -- \`</sub>
- **[rooquiz/rooquiz-mcp](https://github.com/rooquiz/rooquiz-mcp)** — Build and run assessments on RooQuiz — knowledge quizzes, scored quizzes, and outcome ("which X are you") quizzes with AI-assisted authoring and mirrored translations — then work the funnel: leads captured from results pages (tag, assign, comment), respondents, submissions, bookings, and conversion stats. Hosted Streamable HTTP endpoint at https://payload.rooquiz.com/api/mcp, OAuth 2.1 with dynami
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rooquiz/rooquiz-mcp.git`</sub>
- **[krissanders/ai-visibility-mcp](https://github.com/bestaiinsider/ai-visibility-mcp)** — Audit how AI sees your website. Per-bot robots.txt verdicts for 22 known AI user-agents (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bytespider, etc), Cloudflare AI-default flags, on-page schema, sitemap, llms.txt, SPA-shell detection, and cross-model brand mentions via Perplexity + OpenRouter. 0-100 score with explainable deductions; parallel competitor compare. SSRF-guarded, per-call and
  <sub>★ 1 · Python · MIT · clone · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bestaiinsider/ai-visibility-mcp`</sub>
- **[integrallis/rankcli-mcp-server](https://github.com/integrallis/rankcli-mcp-server)** — Free SEO + GEO (AI search) analysis, 13 tools: Core Web Vitals, structured data, security headers, mobile SEO, image audits, internal linking, and AI crawler access (GPTBot, ClaudeBot, PerplexityBot). No signup, no API key — run locally via npx @rankcli/mcp-server or use the free hosted endpoint at mcp.rankcli.dev/mcp/free
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @rankcli/mcp-server`</sub>
- **[tracetify/tracetify-mcp](https://github.com/tracetify/tracetify-mcp)** — Trace how any product actually grew: growth history rebuilt from 12 public sources with dated, linked evidence. Also reads your own Google Search Console, runs site audits, and serves a hand-verified dofollow directory list. Reading existing growth reports is free. npx -y tracetify-mcp or hosted Streamable HTTP at https://tracetify.com/api/mcp
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tracetify/tracetify-mcp.git`</sub>
- **[whdrnr2583-cmd/token-meter](https://github.com/whdrnr2583-cmd/token-meter)** — Local-first dashboard + MCP server for Claude Code and Codex token usage. Cost, per-MCP/per-tool breakdown, hourly distribution, and session drill-down — your data never leaves your machine
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @whdrnr2583/token-meter audit`</sub>
- **[andrealufino/aapl-ads-mcp](https://github.com/andrealufino/aapl-ads-mcp)** — MCP server for Apple Search Ads API v5 — read-only, self-hosted
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-04-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/andrealufino/aapl-ads-mcp.git`</sub>
- **[atomno-mcp/mcp-seo-audit](https://github.com/atomno-mcp/mcp-seo-audit)** — Technical SEO audit powered by the detail.web engine. audit_site(url) returns a 0-100 health score, issues across 8 categories, and a GEO (Generative Engine Optimization) sub-score for visibility in AI search (ChatGPT, Perplexity, Google AI Overviews). Plus validators for robots.txt, sitemap.xml, JSON-LD, and meta tags. Install: pipx install atomno-mcp-seo-audit
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx atomno-mcp-seo-audit`</sub>
- **[A1-x-Tech/mcp-yandex-audience](https://github.com/A1-x-Tech/mcp-yandex-audience)** — Yandex Audience API — build and manage ad-targeting segments (CRM uploads, lookalike, pixel-based) and access grants. Read + write
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yandex-audience@latest`</sub>
- **[D4umak/linkedin-outreach-mcp](https://github.com/D4umak/linkedin-outreach-mcp)** — LinkedIn outreach agent: finds the right people, writes to them in your voice, follows up and handles replies, for sales prospecting, recruiting, user-interview recruitment and job search. Campaigns stay drafts until you launch them. Install: uvx heylead
  <sub>Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx heylead`</sub>
- **[InstantStudioAI/instantclips-mcp](https://github.com/InstantStudioAI/instantclips-mcp)** — InstantClips turns an e-commerce product into short-form vertical video for TikTok, Instagram Reels and Stories. Import a product from its page URL or photos, generate on-brand video ads, and manage brands/products through 10 tools. Remote server at https://app.instantclips.ai/mcp (OAuth 2.1)
  <sub>JavaScript · MIT · source · pushed 2026-09-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/InstantStudioAI/instantclips-mcp.git`</sub>
- **[Agent-Prod/muze-mcp](https://github.com/Agent-Prod/muze-mcp)** — Run your ecommerce ads from Claude &amp; ChatGPT. Meta, Google, Amazon and Shopify: 150+ tools to read performance, inspect campaigns, research competitor ads, and take confirm-gated writes (pause, budgets, launches) that always stage paused. Hosted; connect via OAuth or an API key at https://backend.muzecmo.com/mcp
  <sub>unavailable</sub>
- **[hardeyhemy/revnuvo-dev](https://github.com/hardeyhemy/revnuvo-dev)** — Revnuvo Company Intelligence — tells AI agents what changed at a company, with evidence
  <sub>JavaScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx revnuvo mcp-config --key "$REVNUVO_API_KEY"`</sub>
- **[atomno-mcp/mcp-erid](https://github.com/atomno-mcp/mcp-erid)** — MCP-проверка маркировки интернет-рекламы (erid/ЕРИР): валидация токена, аудит страницы на соответствие 38-ФЗ. Волна 1, роль «читалки», ответственность не на нас
  <sub>Python · MIT · pipx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install atomno-mcp-erid`</sub>
- **[alexcloudstar/makers.page-mcp](https://github.com/alexcloudstar/makers.page-mcp)** — Local MCP server that drafts channel-native X posts from your coding agent with human approval. Draft → approve → publish via X API v2; drafts and credentials stay on your machine. Part of makers.page. npx -y makers-page-mcp
  <sub>unavailable</sub>
- **[Bishop81/wpgoldmine-mcp](https://github.com/Bishop81/wpgoldmine-mcp)** — MCP server to find WordPress and WooCommerce plugin opportunities: large, established plugins weakened by abandonment, low ratings, or poor support that you could realistically replace. Powered by wpgoldmine.io
  <sub>JavaScript · MIT · source · pushed 2026-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Bishop81/wpgoldmine-mcp.git`</sub>
- **[BlockRunAI/x-grow](https://github.com/BlockRunAI/x-grow)** — X/Twitter algorithm optimizer with post drafting, review scoring, and AI image generation for maximum engagement
  <sub>unavailable</sub>
- **[BRNDMK/brandomica-mcp-server](https://github.com/BRNDMK/brandomica-mcp-server)** — Brand name verification across domains (with pricing), social handles, trademarks (USPTO), web presence, app stores, and SaaS channels. Safety scoring, linguistic/phonetic screening, and filing readiness
  <sub>unavailable</sub>
- **[Citlyze/citlyze-mcp](https://github.com/Citlyze/citlyze-mcp)** — Track how your brand shows up in AI search with Citlyze: visibility scores, tracked prompts, citations, competitor comparison, recommendations, and AI crawler analytics across ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews. Read-only hosted endpoint at app.citlyze.com/api/mcp
  <sub>JavaScript · MIT · source · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/citlyze/citlyze-mcp.git`</sub>
- **[conorbronsdon/gsc-mcp](https://github.com/conorbronsdon/gsc-mcp)** — Google Search Console for agents: search analytics by query, page, country, and device; a striking-distance report for queries ranking just off page one; sitemap listing, submission, and removal; and URL inspection. Read and write tools carry separate MCP annotations
  <sub>TypeScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/conorbronsdon/gsc-mcp.git`</sub>
- **[davidmosiah/agent-seo-engine](https://github.com/davidmosiah/agent-seo-engine)** — Local-first SEO quality, search-intent, and opportunity engine for agents. Scores Markdown content and GSC-style opportunities before rewrites or publishing
  <sub>Python · MIT · pipx · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install agent-seo-engine`</sub>
- **[elfsight/beamtrace-mcp](https://github.com/elfsight/beamtrace-mcp)** — AI visibility tracking &amp; website fixes for better AI search presence
  <sub>JavaScript · MIT · docker · pushed 2026-09-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm beamtrace-mcp`</sub>
- **[epistemedeus/ai-readiness](https://github.com/epistemedeus/ai-readiness)** — Check whether a website is visible to AI search (ChatGPT, Perplexity, Claude, Google AI Overviews). Scores AI-crawler access, JSON-LD structured data, title/meta, Open Graph, sitemap, and llms.txt, with a specific fix for each gap. Dependency-free, no API keys. Install: npx -y github:epistemedeus/ai-readiness mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:epistemedeus/ai-readiness yoursite.com`</sub>
- **[forgemeshlabs/seo-authority-mcp](https://github.com/forgemeshlabs/seo-authority-mcp)** — SEO authority scores, keyword opportunities, competitor gaps, content briefs, site audits, and internal-link intelligence, paid per call via x402. npx -y @forgemeshlabs/seo-authority-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @forgemeshlabs/seo-authority-mcp`</sub>
- **[forgemeshlabs/x402-ads-mcp](https://github.com/forgemeshlabs/x402-ads-mcp)** — Install one middleware to monetize unused 402 responses. 7 tools for agent demand analytics, recommendations, and discovery over the ForgeMesh x402 Ads network — paid per call in USDC on Base, free for publishers on their own traffic. npx -y @forgemeshlabs/x402-ads-mcp
  <sub>JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/forgemeshlabs/x402-ads-mcp.git`</sub>
- **[GlobalMatchHub/searchlink-lite](https://github.com/GlobalMatchHub/searchlink-lite)** — Google Search Console in Claude, Cursor or any MCP client. Six read-only tools: site overview with period comparison and biggest drops, any breakdown by query, page, country, device or date, opportunities (high impressions and low CTR, queries at #8-20), URL indexing status and sitemaps. Totals use the date dimension so they match the Search Console UI. Runs locally with a service account or gclou
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GlobalMatchHub/searchlink-lite.git`</sub>
- **[moiosintel/kd-scout](https://github.com/moiosintel/kd-scout)** — Zero-dependency MCP server for keyword research arithmetic: difficulty estimation, opportunity scoring, and structured content briefs. Install: pip install kd-scout
  <sub>Python · MIT · pip · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install kd-scout`</sub>
- **[ni-c/google-search-console-mcp](https://github.com/ni-c/google-search-console-mcp)** — Google Search Console across three APIs, so it can create a property and prove ownership instead of only reading one somebody else set up — setup_site reports which of the four verification steps is missing and hands over the DNS record to paste. Plus sitemaps, URL inspection and the full Performance report with impression-weighted position. 21 tools, narrowable to a curated five; irreversible cal
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/google-search-console-mcp.git`</sub>
- **[growsurf/growsurf-mcp](https://github.com/growsurf/growsurf-mcp)** — Build and manage GrowSurf referral and affiliate programs through AI assistants. Connect via OAuth at https://mcp.growsurf.com or run npx -y @growsurfteam/growsurf-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @growsurfteam/growsurf-mcp`</sub>
- **[hermoso-ai/hermoso](https://github.com/hermoso-ai/hermoso)** — AI ad studio for agents: generate finished video, image, and UGC avatar ads for any brand (script, voiceover, music, brand end card), and research competitor ads across the Meta, Google, and LinkedIn ad libraries plus TikTok/Instagram/YouTube organic. 52 tools. Install: npx -y hermoso mcp, or connect to the hosted endpoint at app.hermoso.ai/mcp. Free signup grant, no card
  <sub>JavaScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g hermoso`</sub>
- **[juan-sibbo/gam-seller-mcp-node](https://github.com/juan-sibbo/gam-seller-mcp-node)** — Governed, GDPR-first sell-side MCP server: exposes Google Ad Manager inventory to buyer AI agents with read-only product discovery, firm pricing, and a revocable commitment primitive — no ad-server writes, no sensitive data, every decision audited. npx gam-seller-mcp-node
  <sub>TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y gam-seller-mcp-node`</sub>
- **[sarefe12-sudo/visibilityradar-mcp](https://github.com/sarefe12-sudo/visibilityradar-mcp)** — Analyze how AI models (Claude, GPT-4o, Gemini, Perplexity, Grok, DeepSeek) see your brand. Returns AI Visibility Score, per-model breakdowns, sentiment analysis, competitor comparison, and top recommendations. Results saved to dashboard automatically. npx visibilityradar-mcp
  <sub>unavailable</sub>
- **[Davison-Francis/min8t-sdks](https://github.com/Davison-Francis/min8t-sdks/tree/main/deliveriq-mcp)** — @deliveriq/mcp — email-deliverability tools for AI agents. 12 tools: single + batch verification, email finder, DNSBL across 50 zones, SPF/DKIM/DMARC/MTA-STS/BIMI infrastructure analysis, spam-trap scoring on 13 weighted signals, composite domain trust report, account credits. 5-stage / 21-check pipeline under the hood. Free tier, no card. Install: npx -y @deliveriq/mcp
  <sub>TypeScript · MIT · in-repo · pushed 2026-05-02</sub>
  <sub>`git clone https://github.com/Davison-Francis/min8t-sdks.git && cd min8t-sdks/deliveriq-mcp`</sub>
- **[meser10/meser10-mcp](https://github.com/meser10/meser10-mcp)** — Official MCP server for Meser 10, an Israeli email and SMS marketing platform. All 61 tools are generated from the live API contract at start-up rather than hand-written, so coverage cannot drift when the platform ships an operation. Four permission tiers starting read-only (tools above the chosen tier are absent from tools/list, not merely refused), credentials are injected server-side and never
  <sub>TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @meser10/mcp-server`</sub>
- **[PageRankCafe/mcp-server](https://github.com/PageRankCafe/mcp-server)** — Create and post link, banner, YouTube, and press-release ads on PageRankCafe, read placement performance, and query platform insights
  <sub>TypeScript · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PageRankCafe/mcp-server.git`</sub>
- **[pickelfintech/sentisift-sdks](https://github.com/pickelfintech/sentisift-sdks/tree/main/mcp)** — Comment moderation and intelligence for any article: bot/spam detection, multilingual sentiment analysis, and Influence (constructive comment generation on paid tiers). Free tier: 1,000 comments, no credit card
  <sub>Python · MIT · in-repo · pushed 2026-07-18</sub>
  <sub>`git clone https://github.com/pickelfintech/sentisift-sdks.git && cd sentisift-sdks/mcp`</sub>
- **[sparrow84001/mcp-seo](https://github.com/sparrow84001/mcp-seo)** — Comprehensive SEO, AEO (Google AI Overviews, Perplexity), GEO, Local SEO, and CRO growth auditor with framework-aware surgical code fixes, multi-page sitemap crawling, HTTP security headers inspection (HSTS, CSP), and universal WebMCP multi-language support
  <sub>TypeScript · MIT · npm · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @sparrow84001/mcp-seo`</sub>
- **[trysonar/mcp](https://github.com/trysonar/mcp)** — App Store Optimization for AI agents — keyword research with difficulty and popularity scores, daily rank tracking, review mining, competitor gap analysis, and revenue estimation across the iOS App Store and Google Play. 32 tools. npx @sonarapp/mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @sonarapp/mcp`</sub>
- **[TopicForge/topicforge-mcp](https://github.com/TopicForge/topicforge-mcp)** — Programmatic SEO batch jobs for agents: run_batch, get_batch_status, export_markdown, plus topic cluster, FAQ schema, and meta description tools. Pay per article, no subscription. Install: npx -y @topicforge/mcp
  <sub>TypeScript · MIT · npx · pushed 2026-07-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @topicforge/mcp`</sub>
- **[ZLeventer/salesforce-marketing-mcp](https://github.com/ZLeventer/salesforce-marketing-mcp)** — Salesforce MCP server built for marketing and revenue ops teams. 47 tools for leads, contacts, accounts, campaigns, campaign members, tasks, and 17 reporting tools including campaign ROI, lead-source attribution, pipeline-by-campaign, multi-touch campaign influence, MQL trend, forecast summary, and the native SFDC Reports API
  <sub>unavailable</sub>
- **[vruum-gtm/mcp](https://github.com/vruum-gtm/mcp)** — AI revenue platform. Operate outbound, deals, pipeline, and CRM automation from your agent: people, deals, outreach, engagement, and research tools over one MCP. Remote server at https://api.vruum.ai/mcp (OAuth 2.1, or Authorization: Bearer vk_live_…); npx -y @vruum/mcp runs the stdio bridge for clients without remote support
  <sub>TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @vruum/cli`</sub>
- **[zaialamm/citable-mcp](https://github.com/zaialamm/citable-mcp)** — SEO and AI-visibility checks an agent pays for per call, with no account: keyword research, on-page audits, AI-citation checks across ChatGPT, Claude, Gemini and Perplexity, plus rank, SERP, domain and backlink data. 17 endpoints at $0.005–0.30 each, settled in USDC on Solana over x402; a failed call is never charged. Install: npx -y citable-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx citable-mcp`</sub>
- **[prepublish/prepublish-mcp](https://github.com/prepublish/prepublish-mcp)** — Audits a YouTube script before it is recorded, rather than fetching the transcript of a video that is already published. Hook, structure and pacing scores, the passages most likely to lose attention, an inauthentic-content check, a YouTube policy pre-flight citing YouTube's own pages, and words to runtime from speaking rates measured across 349 videos. Remote, anonymous, no API key: https://mcp.pr
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/prepublish/prepublish-mcp.git`</sub>

## Social Media

- **[karanb192/reddit-mcp-buddy](https://github.com/karanb192/reddit-mcp-buddy)** — Browse Reddit posts, search content, and analyze user activity without API keys. Works out-of-the-box with Claude Desktop
  <sub>★ 831 · TypeScript · MIT · npm · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g reddit-mcp-buddy`</sub>
- **[king-of-the-grackles/reddit-research-mcp](https://github.com/dialog-tools/reddit-research-mcp)** — AI-powered Reddit intelligence for market research and competitive analysis. Discover subreddits via semantic search across 20k+ indexed communities, fetch posts/comments with full citations, and manage research feeds. No Reddit API credentials needed
  <sub>★ 246 · Python · MIT · clone · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/king-of-the-grackles/reddit-research-mcp.git`</sub>
- **[HagaiHen/facebook-mcp-server](https://github.com/HagaiHen/facebook-mcp-server)** — Integrates with Facebook Pages to enable direct management of posts, comments, and engagement metrics through the Graph API for streamlined social media management
  <sub>★ 225 · Python · MIT · clone · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/your-org/facebook-mcp-server.git`</sub>
- **[taisly/agent](https://github.com/taisly/agent)** — Taisly Agent Kit MCP server for AI agent social media video publishing. Discover connected accounts, validate videos, publish or schedule posts to TikTok, Instagram Reels, YouTube Shorts, X, and Facebook through Taisly. Install: npx -y @taisly/agent mcp. Requires a Taisly API key and connected accounts
  <sub>★ 213 · JavaScript · MIT · npm · pushed 2026-07-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @taisly/agent`</sub>
- **[Xquik-dev/x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper)** — Remote X (Twitter) MCP server with 121 endpoints via 2 tools. Post tweets, reply, like, retweet, follow, DM, search, extract data, run giveaways, and monitor accounts. StreamableHTTP at xquik.com/mcp with API key auth
  <sub>★ 205 · JavaScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx skills@1.5.3 add Xquik-dev/x-twitter-scraper`</sub>
- **[ihuzaifashoukat/x-use](https://github.com/ihuzaifashoukat/x-use)** — Multi-account X (Twitter) automation with no X API key: it drives a real Chrome session using your own cookies. 33 tools for posting, replies, keyword search, engagement, single-tweet reads that return images as MCP content, per-account personas, proxy pools, and a persistent scheduled-action queue. Draft-approval mode is on by default, so write tools return a draft and nothing goes live until you
  <sub>★ 168 · Python · MIT · npx · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ihuzaifashoukat/x-use`</sub>
- **[kunallunia/twitter-mcp](https://github.com/LuniaKunal/mcp-twitter)** — All-in-one Twitter management solution providing timeline access, user tweet retrieval, hashtag monitoring, conversation analysis, direct messaging, sentiment analysis of a post, and complete post lifecycle control - all through a streamlined API
  <sub>★ 60 · Python · source · pushed 2025-05-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LuniaKunal/mcp-twitter.git`</sub>
- **[anwerj/youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp)** — AI‑powered YouTube uploader—no CLI, no YouTube Studio. Uploade videos directly from MCP clients with all AI capabilities
  <sub>★ 54 · Go · MIT · source · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/anwerj/youtube-uploader-mcp.git`</sub>
- **[conorbronsdon/substack-mcp](https://github.com/conorbronsdon/substack-mcp)** — MCP server for Substack — read posts, manage drafts, publish Notes, get comments, and upload images. Safe by design: cannot publish or delete posts
  <sub>★ 35 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx substack-mcp login https://yourblog.substack.com --user-id 12345`</sub>
- **[macrocosm-os/macrocosmos-mcp](https://github.com/macrocosm-os/macrocosmos-mcp)** — Access real-time X/Reddit/YouTube data directly in your LLM applications with search phrases, users, and date filtering
  <sub>★ 29 · Python · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/macrocosm-os/macrocosmos-mcp.git`</sub>
- **[mikusnuz/meta-mcp](https://github.com/mikusnuz/meta-mcp)** — Full-coverage MCP server for Instagram Graph API v25.0, Threads API &amp; Meta platform — 57 tools for publishing, comments, insights, hashtags, DMs, and token management
  <sub>★ 24 · TypeScript · MIT · clone · pushed 2026-08-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/mikusnuz/meta-mcp.git`</sub>
- **[HasData/instagram-mcp](https://github.com/HasData/instagram-mcp)** — Remote MCP server for public Instagram data: profiles and post feeds by handle with follower counts, captions, hashtags and mentions parsed, as JSON
  <sub>★ 16 · JavaScript · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/HasData/instagram-mcp.git`</sub>
- **[gwbischof/bluesky-social-mcp](https://github.com/gwbischof/bluesky-social-mcp)** — An MCP server for interacting with Bluesky via the atproto client
  <sub>★ 16 · Python · MIT · source · pushed 2025-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gwbischof/bluesky-social-mcp.git`</sub>
- **[AstaBlackClove/posthive](https://github.com/AstaBlackClove/posthive)** — Schedule and manage social media posts across 13 platforms (Bluesky, Threads, Instagram, LinkedIn, Mastodon, YouTube, Facebook, Pinterest, Telegram, Nostr, X/Twitter, Discord, Tumblr). OAuth 2.0 + PKCE, 10 tools, draft-first workflow
  <sub>★ 15 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/AstaBlackClove/posthive.git`</sub>
- **[checkra1neth/xbird](https://github.com/checkra1neth/xbird-skill)** — Twitter/X MCP server with 34 tools — post tweets, search, read timelines, manage engagement, upload media. No API keys needed, uses browser cookies. Pay per call from $0.001 via x402 micropayments
  <sub>★ 15 · MIT · npx · pushed 2026-07-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add checkra1neth/xbird-skill`</sub>
- **[sinanefeozler/reddit-summarizer-mcp](https://github.com/sinanefeozler/reddit-summarizer-mcp)** — MCP server for summarizing users's Reddit homepage or any subreddit based on posts and comments
  <sub>★ 12 · Python · MIT · clone · pushed 2025-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sinanefeozler/reddit-summarizer-mcp.git`</sub>
- **[bulatko/vk-mcp-server](https://github.com/bulatko/vk-mcp-server)** — MCP server for VK (VKontakte) social network API. Access users, walls, groups, friends, newsfeed, photos, and community stats
  <sub>★ 11 · JavaScript · MIT · npm · pushed 2026-07-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g vk-mcp-server`</sub>
- **[HasData/tiktok-mcp](https://github.com/HasData/tiktok-mcp)** — Remote MCP server for public TikTok data: profile lookup, an account's videos, video comments and reply threads, and keyword search over videos or creators, as JSON
  <sub>★ 10 · JavaScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/tiktok-mcp.git`</sub>
- **[arjun1194/insta-mcp](https://github.com/arjun1194/insta-mcp)** — Instagram MCP server for analytics and insights. Get account overviews, posts, followers, following lists, post insights, and search for users, hashtags, or places
  <sub>★ 10 · TypeScript · clone · pushed 2025-12-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/your-repo/insta-mcp.git`</sub>
- **[devag7/linkedin-mcp](https://github.com/devag7/linkedin-mcp)** — LinkedIn for AI assistants over an authenticated browser session — profiles, people/job/company search, feed, messaging, and gated writes (connect, message, post, react, comment) returned as structured JSON, with built-in rate limiting. npx -y linkedin-mcp-tools
  <sub>★ 10 · TypeScript · MIT · npx · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y linkedin-mcp-tools@latest --login`</sub>
- **[pendpost/pendpost](https://github.com/pendpost/pendpost)** — Local-first social media MCP server. An AI agent drafts and schedules posts across Instagram, Facebook, LinkedIn, YouTube, X, Telegram, Discord, Mastodon, Nostr, and more, including long-form blogs on WordPress and Ghost, behind a human approval gate you control; read-only tools can never publish
  <sub>★ 9 · JavaScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`npx pendpost`</sub>
- **[jj-cheng25/weixin-articles-mcp](https://github.com/jj-cheng25/weixin-articles-mcp)** — Read WeChat (微信) Official Account articles with native multimodal output — body, images, and video keyframes as MCP content blocks. Handles all three embed types: Tencent Video (yt-dlp keyframes), WeChat-native (mp4 keyframes), Channels/视频号 (metadata + cover via public API)
  <sub>★ 7 · Python · MIT · pip · pushed 2026-05-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install weixin-articles-mcp`</sub>
- **[Upload-Post/upload-post-mcp](https://github.com/Upload-Post/upload-post-mcp)** — Publish, schedule and analyze social media across TikTok, Instagram, YouTube, LinkedIn, Facebook, X, Threads, Pinterest, Reddit, Bluesky, Google Business, Discord and Telegram from one API. 50 tools covering uploads, scheduling queues, analytics, comments, DMs/auto-DMs and GPU video encoding. Hosted (OAuth 2.1 / API key) at https://mcp.upload-post.com/mcp or local stdio via npx -y @upload-post/mcp
  <sub>★ 7 · TypeScript · MIT · docker · pushed 2026-09-09 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 8080:8080 upload-post-mcp`</sub>
- **[HasData/youtube-mcp](https://github.com/HasData/youtube-mcp)** — Remote MCP server for YouTube: search, video and channel data and transcripts, as JSON, with no Google Cloud project or YouTube Data API key to manage
  <sub>★ 6 · JavaScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/youtube-mcp.git`</sub>
- **[peturgeorgievv-factory/postfast-mcp](https://github.com/peturgeorgievv-factory/postfast-mcp)** — Schedule and manage social media posts across 10 platforms (Instagram, Facebook, TikTok, X, LinkedIn, YouTube, Threads, Pinterest, Bluesky, Telegram) from any MCP-compatible AI assistant
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/peturgeorgievv-factory/postfast-mcp.git`</sub>
- **[publora/mcp-server](https://github.com/publora/mcp-server)** — Official Publora MCP server — schedule and publish posts across 10 social platforms (Twitter/X, LinkedIn, Instagram, Threads, TikTok, YouTube, Facebook, Bluesky, Mastodon, Telegram) from Claude, Cursor, or any MCP client. 18 tools for cross-platform posting, scheduling, media upload, and LinkedIn analytics. Hosted at mcp.publora.com
  <sub>★ 5 · JavaScript · MIT · clone · pushed 2026-06-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/publora/mcp-server.git`</sub>
- **[Vovala14/vynly-mcp](https://github.com/Vovala14/vynly-mcp)** — Post AI-generated images to Vynly, an AI-only social feed built for agents. Four tools — vynly_post_image, vynly_post_spark, vynly_read_feed, vynly_search. Auto-claims a 10-write demo token on first run via a public no-auth endpoint, so it works out of the box with no signup. Provenance-aware (C2PA / SynthID / XMP)
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @vynly/mcp`</sub>
- **[posteverywhere/mcp](https://github.com/posteverywhere/mcp)** — Hosted MCP server to schedule and publish across 11 social platforms (Instagram, LinkedIn, TikTok, X, YouTube, Facebook, Threads, Pinterest, Bluesky, Discord, Telegram). 32 tools covering posts, campaigns, bulk operations, media, analytics, webhooks, and AI captions. Connect with one URL, or run locally via npx -y @posteverywhere/mcp
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/posteverywhere/mcp.git`</sub>
- **[signal-found/sf-mcp](https://github.com/signal-found/sf-mcp)** — Connect AI agents to Signal Found's proprietary Reddit outreach network. Find prospects posting about problems your product solves, send personalized DMs at scale via your own Reddit account or a managed bot network of hundreds of accounts, and manage a full outreach CRM — all without leaving your AI client
  <sub>★ 3 · Python · MIT · pip · pushed 2026-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install sf-mcp`</sub>
- **[abhineet34/linkedin-mcp-server](https://github.com/abhineet34/linkedin-mcp-server)** — Local LinkedIn MCP server for posting to LinkedIn from Claude. 9 tools — create/edit/delete posts (text, image, article), upload images, fetch profile, look up company pages, and check follower counts. Uses the official LinkedIn REST API with OAuth 2.0 (w_member_social, OIDC)
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/abhineet34/linkedin-mcp-server.git`</sub>
- **[BelleKou/mcp-viral-transformer](https://github.com/BelleKou/mcp-viral-transformer)** — Turn URLs into viral posts via "remake" command
  <sub>★ 2 · Python · MIT · clone · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BelleKou/mcp-viral-transformer.git`</sub>
- **[scrape-badger/scrapebadger-mcp](https://github.com/scrape-badger/scrapebadger-mcp)** — Access Twitter/X data including user profiles, tweets, followers, trends, lists, and communities via the ScrapeBadger API
  <sub>★ 2 · Python · MIT · uv · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx scrapebadger-mcp`</sub>
- **[timkulbaev/mcp-linkedin](https://github.com/timkulbaev/mcp-linkedin)** — LinkedIn publishing, commenting, and reacting via Unipile API. Dry-run by default, SKILL.md included, CLI-first design for AI automation workflows
  <sub>★ 2 · JavaScript · MIT · clone · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/timkulbaev/mcp-linkedin.git`</sub>
- **[06ketan/substack-ops](https://github.com/06ketan/substack-ops)** — Substack with zero AI API keys. 26 tools (posts, notes, comments, replies, reactions, restacks). Host LLM drafts via propose_reply → confirm_reply tokens. SQLite dedup, JSONL audit, dry-run default. Install: uvx substack-ops mcp install cursor
  <sub>★ 1 · Python · MIT · uv · pushed 2026-05-24 · macOS</sub>
  <sub>`uvx substack-ops mcp install cursor # or claude-desktop, claude-code, opencode, print`</sub>
- **[davidmosiah/tiktok-agent-publisher](https://github.com/davidmosiah/tiktok-agent-publisher)** — Local-first TikTok Content Posting API MCP and CLI for agents, with OAuth readiness checks, dry-run publish flows and live uploads only when explicitly enabled
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g tiktok-agent-publisher`</sub>
- **[farukkolip/tiktapdown-mcp](https://github.com/farukkolip/tiktapdown-mcp)** — TikTok creator toolkit MCP — download videos without watermark, get curated 15-hashtag sets across 15 niches with strategy tips, look up best posting times for 12 countries, and generate viral hook formulas across 8 categories. No API keys, no signup, free. Install: npx -y tiktapdown-mcp. Companion to tiktapdown.com
  <sub>★ 1 · TypeScript · clone · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/farukkolip/tiktapdown-mcp`</sub>
- **[helbertparanhos/postforme-mcp-pro](https://github.com/helbertparanhos/postforme-mcp-pro)** — Post for Me MCP server with 27 typed tools to publish, schedule, edit, delete and analyze social posts across 9 platforms (Instagram, Facebook, TikTok, YouTube, X, LinkedIn, Pinterest, Bluesky, Threads), plus a postforme_raw escape hatch and a readonly safety mode
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y postforme-mcp-pro`</sub>
- **[drashrafsaiyed-cyber/instagram-mcp](https://github.com/dr-ashraf-s-MCP-LABS/instagram-mcp)** — Control Instagram from Claude: publish photos, reels, and carousels, read account insights, manage comments, and reply to DMs. 14 tools via the Instagram Login API. One-click free Render deploy for Claude Web and mobile
  <sub>★ 1 · Python · MIT · clone · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/drashrafsaiyed-cyber/instagram-mcp`</sub>
- **[jorgenclaw/nostr-mcp-server](https://github.com/jorgenclaw/nostr-mcp-server)** — Lightning-paid Nostr signing MCP server. AI agents pay sats per call to sign and publish Nostr events — no API keys, just Lightning. Live at https://mcp.jorgenclaw.ai/sse. Tools: nostr_sign_event (2 sats), nostr_publish_event (3 sats)
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jorgenclaw/nostr-mcp-server.git`</sub>
- **[MarceauSolutions/fitness-influencer-mcp](https://github.com/MarceauSolutions/fitness-influencer-mcp)** — Fitness content creator workflow automation - video editing with jump cuts, revenue analytics, and branded content creation
  <sub>★ 1 · Python · source · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MarceauSolutions/fitness-influencer-mcp.git`</sub>
- **[milcho0604/velog-mcp](https://github.com/milcho0604/velog-mcp)** — Velog (velog.io) blog server with 23 tools. Reading, search, stats, tags and series work without authentication; writing defaults to drafts and private posts, and public publishing stays behind an opt-in VELOG_ALLOW_PUBLIC=1 flag. Documents velog's undocumented GraphQL behaviour measured against the live API. 2 runtime dependencies, Node 22.18+, MIT
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/milcho0604/velog-mcp.git`</sub>
- **[mobileshop9991-star/clipwise-mcp](https://github.com/mobileshop9991-star/clipwise-mcp)** — AI platform for short-form video creators (TikTok, Instagram Reels, YouTube Shorts, Facebook Reels). Three tools — viral TikTok trend search across 20+ countries, service info, and use-case scenarios for video analysis, competitor research, and content strategy. Install: npx -y clipwise-mcp-server. Free plan at tryclipwise.com
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-05-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mobileshop9991-star/clipwise-mcp.git`</sub>
- **[socialintel/socialintel-mcp](https://github.com/socialintel/socialintel-mcp)** — Instagram influencer search API for AI agents — search by niche, country, demographics, or follower count, returns usernames, bios, follower counts, business categories, and public business emails. Single-profile lookup at $0.01; full search $0.50–$1.30 (1–100 leads). USDC on Base, Solana, Polygon, Arbitrum via x402 micropayments. No signup, no API keys
  <sub>★ 1 · Python · MIT · uv · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from git+https://github.com/socialintel/socialintel-mcp socialintel-mcp`</sub>
- **[sofya-co/sofya-mcp](https://github.com/sofya-co/sofya-mcp)** — Web tools for AI agents through the Sofya API. Search the web for full page content instead of snippets, fetch URLs as clean markdown (including PDFs), extract structured data from a page with a prompt, and run multi-source deep research that returns a cited report
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sofya-mcp --list-tools`</sub>
- **[solnk-dev/solnk-mcp](https://github.com/solnk-dev/solnk-mcp)** — Official Solnk MCP server — publish and schedule content across 9 platforms (X, Instagram, TikTok, YouTube, Facebook, LinkedIn, Pinterest, Threads, Bluesky) from any MCP client. 11 tools for publishing, drafts, scheduling, media upload, and post analytics. Hosted at mcp.solnk.com with bearer API key auth
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-06-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/solnk-dev/solnk-mcp.git`</sub>
- **[ilyautov/vk-mcp-ru](https://github.com/ilyautov/vk-mcp-ru)** — VK API for AI assistants: wall posts, communities, messages, market items, ads and stats through 373 schema-driven methods with a read/write/destructive safety gate. The agent searches methods in plain language instead of getting 373 tools. PyPI (uvx vk-mcp-ru)
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx vk-mcp-ru`</sub>
- **[AdesiaHQ/bangermap-integrations](https://github.com/AdesiaHQ/bangermap-integrations)** — YouTube outlier research on your own free Data API key. Ranks a channel's uploads by their multiple against that channel's own baseline, Shorts and long-form scored separately, compares channels, and sweeps a niche for recent overperformers. Four tools, no account and no metering. npx -y bangermap-mcp
  <sub>TypeScript · MIT · source · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AdesiaHQ/bangermap-integrations.git`</sub>
- **[adaptlypost/agent](https://github.com/adaptlypost/agent)** — Schedule and publish posts to Instagram, TikTok, YouTube, X, Facebook, LinkedIn, Pinterest, Threads, and Bluesky from any MCP client: cross-posting with per-platform captions, bulk scheduling, draft approval, and media upload. Hosted at https://mcp.adaptlypost.com/mcp (OAuth or API token)
  <sub>TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add adaptlypost/agent`</sub>
- **[arslan2012/qpost-mcp](https://github.com/arslan2012/qpost-mcp)** — Video-first publishing for agents: schedule and publish video and image posts to YouTube, TikTok, and Instagram. 7 tools covering connected-account discovery, create/schedule, update, delete, and retry of failed posts. Scoped API keys (read/write/delete). Connect with one URL at https://qpost.dev/mcp, or run locally via npx -y qpost-mcp
  <sub>JavaScript · MIT · source · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/arslan2012/qpost-mcp.git`</sub>
- **[conorbronsdon/postlint-mcp](https://github.com/conorbronsdon/postlint-mcp)** — Check a post against a platform's real character limit before publishing: X weights every URL at 23 and CJK, Hangul, and emoji at 2, while Bluesky and Mastodon count grapheme clusters. Covers X, Bluesky, LinkedIn, Threads, Mastodon, Discord. No credentials and no network access
  <sub>TypeScript · Apache-2.0 · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @conorbronsdon/postlint-mcp`</sub>
- **[hiroata/meltbook-mcp-server](https://github.com/hiroata/meltbook)** — MCP server for meltbook, an AI-agent political discussion board. 50 AI agents autonomously post, vote, and debate Japanese politics. 11 tools for thread creation, posting, voting, and monitoring
  <sub>unavailable</sub>
- **[Kadenzo/kadenzo-mcp](https://github.com/Kadenzo/kadenzo-mcp)** — Schedule, manage, generate, and analyze social posts across 11 networks (Instagram, TikTok, X, LinkedIn, YouTube, Facebook, Pinterest, Threads, Bluesky, Mastodon, Telegram) — 13 tools for scheduling, media upload, AI caption generation, best-times, analytics, listening, and comments. npx -y kadenzo-mcp
  <sub>JavaScript · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Kadenzo/kadenzo-mcp.git`</sub>
- **[llmops-pro/marketplace-mcp](https://github.com/llmops-pro/marketplace-mcp)** — Run a Shopstr / NOSTR marketplace storefront from an agent: create and update stalls and products in both the NIP-15 dialect (kind 30017/30018) and the Shopstr-modern dialect (kind 30019 shop + kind 30402 NIP-99 listings), including the Shopstr cache POST that makes cards actually render. 7 tools. npx -y marketplace-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y marketplace-mcp`</sub>
- **[Perufitlife/postwire-mcp](https://github.com/Perufitlife/postwire-mcp)** — Post to TikTok, Instagram, YouTube, X, LinkedIn, Bluesky, Telegram, Mastodon &amp; Discord from any AI agent via one MCP tool (post_to_social). Connect accounts once; flat per-brand pricing. Install: npx -y postwire-mcp
  <sub>JavaScript · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Perufitlife/postwire-mcp.git`</sub>
- **[postmcp/postmcp-mcp-server](https://github.com/postmcp/postmcp-mcp-server)** — Publish and schedule posts to LinkedIn, X, Facebook, Instagram, Threads, Bluesky and YouTube Shorts from one API key. 16 tools for preflight checks, scheduling, per-profile copy, brand kits and image generation; stdio or Streamable HTTP. On the official MCP Registry. npx -y @postmcpai/server
  <sub>JavaScript · MIT · npx · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @postmcpai/server`</sub>
- **[glennprime/synthnet-mcp](https://github.com/glennprime/synthnet-mcp)** — Official MCP server for SynthNet (synthnet.io), an independent social network for AI agents. Agents join with an ed25519 keypair they hold, paint one self-portrait a day with their own image model (SVG or p5.js as a fallback), reply to the humans and agents who talk to them, and keep a reputation that persists across context resets. Free, no API key needed. Install: npx -y @synthnet/mcp
  <sub>TypeScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/glennprime/synthnet-mcp.git`</sub>
- **[tokportal/tokportal-mcp](https://github.com/tokportal/tokportal-mcp)** — Official TokPortal MCP server: managed social infrastructure — real TikTok, Instagram and YouTube accounts created, warmed and operated by human account managers in 16+ countries, plus video upload/scheduling at scale, analytics, ban lifecycle and webhooks (91 tools with readOnlyHint/destructiveHint annotations). No per-account OAuth, no 25-posts/day cap. Remote (OAuth 2.1) at app.tokportal.com/ap
  <sub>TypeScript · MIT · npm · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g tokportal-mcp@1.15.1`</sub>
- **[realMNohgee/hermtica](https://github.com/realMNohgee/hermtica)** — AI agent social network and marketplace with native MCP server. 6 tools: browse_feed, search, get_trending, get_agent_profile, search_marketplace, get_marketplace_stats. Endpoint: hermtica.com/api/mcp. Free
  <sub>TypeScript · MIT · docker · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 hermtica-mcp`</sub>
- **[veezeehq/veezee-mcp](https://github.com/veezeehq/veezee-mcp)** — Real-time LinkedIn, X (Twitter) and Reddit data: profiles, companies, posts, search, sentiment. Hosted at mcp.veezee.io with OAuth or self-serve keys
  <sub>JavaScript · MIT · npx · pushed 2026-07-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx github:veezeehq/veezee-mcp`</sub>

## Translation Services

- **[translated/lara-mcp](https://github.com/translated/lara-mcp)** — MCP Server for Lara Translate API, enabling powerful translation capabilities with support for language detection and context-aware translations
  <sub>★ 97 · TypeScript · MIT · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/translated/lara-mcp.git`</sub>
- **[mmntm/weblate-mcp](https://github.com/mmntm/weblate-mcp)** — Comprehensive Model Context Protocol server for Weblate translation management, enabling AI assistants to perform translation tasks, project management, and content discovery with smart format transformations
  <sub>★ 23 · TypeScript · npx · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mmntm/weblate-mcp`</sub>
- **[KyaniteLabs/DialectOS](https://github.com/KyaniteLabs/DialectOS)** — Spanish dialect localization server and CLI. Translates and QA-checks across 25 regional variants with register control, structure preservation, and adversarial quality gates
  <sub>★ 4 · TypeScript · Apache-2.0 · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pnpm add -g https://github.com/KyaniteLabs/DialectOS/releases/download/v0.3.0/dialectos-cli-0.3.0.tgz`</sub>
- **[waxberry-dev/live-translate-mcp](https://github.com/waxberry-dev/live-translate-mcp)** — Real-time English ↔ Mandarin Chinese speech translation. Transcribes audio locally with Whisper, translates via Claude API, and synthesises speech locally with Piper TTS. Pass a WAV file path and Claude handles the rest
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g live-translate-mcp`</sub>
- **[shuji-bonji/xcomet-mcp-server](https://github.com/shuji-bonji/xcomet-mcp-server)** — Translation quality evaluation using xCOMET models. Provides quality scoring (0-1), error detection with severity levels (minor/major/critical), and optimized batch processing with 25x speedup
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g xcomet-mcp-server`</sub>
- **[RaiGanja/kaeris-mcp](https://github.com/RaiGanja/kaeris-mcp)** — AI localization: translate an app's string files into 46 languages (JSON, .arb, .po, .strings, Android XML, …) with placeholder-safe, reproducible output — from Claude/Cursor
  <sub>Python · MIT · pip · pushed 2026-08-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install kaeris-mcp`</sub>

## Conversational AI

- **[Perspective-AI/mcp](https://github.com/Perspective-AI/mcp)** — Official MCP server for Perspective AI. An AI Concierge replaces static forms with adaptive AI conversations for lead qualification, customer research, onboarding feedback, and advocacy. Design conversation agents (Concierge, Interviewer, Evaluator, Advocate), analyze conversations, deploy embeds, and automate follow-ups (webhook, email, Slack, HubSpot)
  <sub>★ 5 · Shell · MIT · source · pushed 2026-09-01</sub>
  <sub>`git clone https://github.com/Perspective-AI/mcp.git`</sub>
- **[TsvetanG2/cognigy-ai-mcp-management-server](https://github.com/TsvetanG2/cognigy-ai-mcp-management-server)** — Management and automation server for the Cognigy.AI conversational AI platform, exposing 132 tools across flows, agents, snapshots, NLU, functions, and deployment. Published to the official MCP Registry. npx mcp-cognigy
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cognigy-ai-mcp-management-server`</sub>
- **[bodyegypt/lobbyvoices-mcp](https://github.com/bodyegypt/lobbyvoices-mcp)** — Official remote MCP server for Lobby, an AI receptionist for small businesses. Seven free no-auth tools: write business phone scripts and IVR menus (English + Mexican Spanish), generate ElevenLabs agent system prompts, calculate missed-call cost, get a hire-a-receptionist verdict, role-play a call against the live receptionist engine, and get a real demo number to call. Typed structured outputs
  <sub>JavaScript · MIT · source · pushed 2026-07-03 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/bodyegypt/lobbyvoices-mcp.git`</sub>
- **[puspoaditya/cloudflare-workers-ai-mcp](https://github.com/puspoaditya/cloudflare-workers-ai-mcp)** — Cloudflare Workers AI inference for AI agents: LLM chat completions (Llama 3.3 70B, Llama 3.1 8B, Llama 4 Scout, Qwen Coder 32B, DeepSeek R1 Distill), text embeddings (BGE small/base), and image generation (Flux 1 Schnell) — generous free tier, no infrastructure to run. npx -y @puspoaditya/cloudflare-workers-ai-mcp
  <sub>JavaScript · MIT · source · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/puspoaditya/cloudflare-workers-ai-mcp.git`</sub>
- **[kiro0x/five-mcp](https://github.com/kiro0x/five-mcp)** — LLM character consistency engine — generates structured JSON constraints from 4 multiple-choice questions about an AI's psychology. Drop the JSON into any LLM's system prompt to prevent persona drift; reduces inference cost from retries. 160,000 personality patterns; works with any LLM
  <sub>unavailable</sub>
- **[guillaumehussong/standard-vocal-mcp](https://github.com/guillaumehussong/standard-vocal-mcp)** — Voice Agent Factory for Vapi phone agents: vertical templates, self-testing agents, audio forensics, prompt versioning, and CI regression gates. npx -y standard-vocal-mcp
  <sub>TypeScript · MIT · source · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/guillaumehussong/standard-vocal-mcp.git`</sub>

## Browser Automation

- **[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)** — Official Microsoft Playwright MCP server, enabling LLMs to interact with web pages through structured accessibility snapshots
  <sub>★ 37.5k · TypeScript · Apache-2.0 · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @playwright/mcp@latest --config path/to/config.json`</sub>
- **[seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)** — A Python-based MCP server for browser automation, testing, and bypassing bot-detection using SeleniumBase CDP Mode with a Chromium browser. The solve_captcha tool can handle CAPTCHAs that expect a click
  <sub>★ 13k · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install seleniumbase`</sub>
- **[firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server)** — Official Firecrawl server with live browser interaction (firecrawl_interact) — navigate, click, type, and scroll on a page before extraction, for JS-heavy or auth-gated sites. Also scrape, crawl, map, search, and extract
  <sub>★ 7.5k · JavaScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g firecrawl-mcp`</sub>
- **[browsermcp/mcp](https://github.com/BrowserMCP/mcp)** — Automate your local Chrome browser
  <sub>★ 7.1k · TypeScript · Apache-2.0 · source · pushed 2025-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browsermcp/mcp.git`</sub>
- **[executeautomation/playwright-mcp-server](https://github.com/executeautomation/mcp-playwright)** — An MCP server using Playwright for browser automation and webscrapping
  <sub>★ 5.7k · TypeScript · MIT · npm · pushed 2025-12-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @executeautomation/playwright-mcp-server`</sub>
- **[browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase)** — Automate browser interactions in the cloud (e.g. web navigation, data extraction, form filling, and more)
  <sub>★ 3.4k · TypeScript · Apache-2.0 · clone · pushed 2026-07-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/browserbase/mcp-server-browserbase.git`</sub>
- **[operative_sh/web-eval-agent](https://github.com/refreshdotdev/web-eval-agent)** — An MCP Server that autonomously debugs web applications with browser-use browser agents
  <sub>★ 1.2k · Python · Apache-2.0 · uv · pushed 2026-02-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from git+https://github.com/Operative-Sh/web-eval-agent.git playwright install`</sub>
- **[co-browser/browser-use-mcp-server](https://github.com/kontext-security/browser-use-mcp-server)** — browser-use packaged as an MCP server with SSE transport. includes a dockerfile to run chromium in docker + a vnc server
  <sub>★ 843 · Python · MIT · uv · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install dist/browser_use_mcp_server-*.whl`</sub>
- **[LvcidPsyche/auto-browser](https://github.com/LvcidPsyche/auto-browser)** — Open-source MCP-native browser agent with human takeover via noVNC, reusable auth profiles, and approval/audit rails. Playwright + FastAPI, Docker-based isolated sessions, stdio bridge for Claude Desktop and Cursor
  <sub>★ 793 · Python · MIT · uv · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx auto-browser-mcp`</sub>
- **[eat-pray-ai/yutu](https://github.com/eat-pray-ai/yutu)** — A fully functional MCP server and CLI for YouTube to automate YouTube operation
  <sub>★ 690 · Go · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/eat-pray-ai/yutu.git`</sub>
- **[kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript)** — Fetch YouTube subtitles and transcripts for AI analysis
  <sub>★ 596 · TypeScript · MIT · npx · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @kimtaeyoon83/mcp-server-youtube-transcript --client claude`</sub>
- **[pskill9/web-search](https://github.com/pskill9/web-search)** — An MCP server that enables free web searching using Google search results, with no API keys required
  <sub>★ 470 · JavaScript · source · pushed 2024-12-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pskill9/web-search.git`</sub>
- **[freema/firefox-devtools-mcp](https://github.com/mozilla/firefox-devtools-mcp)** — Firefox browser automation via WebDriver BiDi for testing, scraping, and browser control. Supports snapshot/UID-based interactions, network monitoring, console capture, and screenshots
  <sub>★ 431 · TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @mozilla/firefox-devtools-mcp@latest -- --headless --viewport 1280x720`</sub>
- **[recursechat/mcp-server-apple-shortcuts](https://github.com/recursechat/mcp-server-apple-shortcuts)** — An MCP Server Integration with Apple Shortcuts
  <sub>★ 348 · JavaScript · Apache-2.0 · clone · pushed 2024-12-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:recursechat/mcp-server-apple-shortcuts.git`</sub>
- **[eyalzh/browser-control-mcp](https://github.com/eyalzh/browser-control-mcp)** — An MCP server paired with a browser extension that enables LLM clients to control the user's browser (Firefox)
  <sub>★ 324 · TypeScript · MIT · source · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/eyalzh/browser-control-mcp.git`</sub>
- **[automatalabs/mcp-server-playwright](https://github.com/VikashLoomba/MCP-Server-Playwright)** — An MCP server for browser automation using Playwright
  <sub>★ 299 · JavaScript · MIT · npx · pushed 2025-06-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @automatalabs/mcp-server-playwright --client claude`</sub>
- **[fradser/mcp-server-apple-reminders](https://github.com/FradSer/mcp-server-apple-events)** — An MCP server for interacting with Apple Reminders on macOS
  <sub>★ 208 · TypeScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-server-apple-events`</sub>
- **[achiya-automation/safari-mcp](https://github.com/achiya-automation/safari-mcp)** — Native Safari browser automation for AI agents with 80+ tools. No Chrome dependency, optimized for Apple Silicon with 60% less CPU overhead
  <sub>★ 204 · JavaScript · MIT · npm · pushed 2026-09-22 · macOS</sub>
  <sub>`npm install -g safari-mcp`</sub>
- **[34892002/bilibili-mcp-js](https://github.com/34892002/bilibili-mcp-js)** — A MCP server that supports searching for Bilibili content. Provides LangChain integration examples and test scripts
  <sub>★ 193 · JavaScript · MIT · source · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/34892002/bilibili-mcp-js.git`</sub>
- **[blackwhite084/playwright-plus-python-mcp](https://github.com/blackwhite084/playwright-plus-python-mcp)** — An MCP python server using Playwright for browser automation,more suitable for llm
  <sub>★ 189 · Python · Apache-2.0 · npx · pushed 2025-01-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory C:\Users\YUNYING\Documents\project\python\mcp\playwright-server run playwright-server`</sub>
- **[hanzili/comet-mcp](https://github.com/hanzili/comet-mcp)** — Connect to Perplexity Comet browser for agentic web browsing, deep research, and real-time task monitoring
  <sub>★ 180 · TypeScript · MIT · source · pushed 2026-01-13 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hanzili/comet-mcp.git`</sub>
- **[alex-on-ai/WebReaper](https://github.com/alex-on-ai/WebReaper)** — #️⃣ 🏠 🍎 🪟 🐧 - AI-native web scraper MCP server. Single binary, returns clean markdown, MIT-licensed Firecrawl alternative
  <sub>★ 148 · C# · MIT · brew · pushed 2026-07-11 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install alex-on-ai/webreaper/webreaper`</sub>
- **[lightpanda-io/gomcp](https://github.com/lightpanda-io/gomcp)** — /☁️ 🐧/🍎 - An MCP server in Go for Lightpanda, the ultra fast headless browser designed for web automation
  <sub>★ 67 · Go · Apache-2.0 · source · pushed 2026-03-13 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/lightpanda-io/gomcp.git`</sub>
- **[swimmwatch/cloakbrowser-mcp](https://github.com/swimmwatch/cloakbrowser-mcp)** — Playwright MCP-compatible browser automation using CloakBrowser Chromium, available as an npm package and Docker image
  <sub>★ 63 · TypeScript · MIT · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y cloakbrowser-mcp@latest`</sub>
- **[ndthanhdev/mcp-browser-kit](https://github.com/ndthanhdev/mcp-browser-kit)** — An MCP Server that enables AI assistants to interact with your local browsers
  <sub>★ 54 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mcp-browser-kit/server@latest --transport http`</sub>
- **[apireno/DOMShell](https://github.com/apireno/DOMShell)** — Browse the web using filesystem commands (ls, cd, grep, click). 38 MCP tools map Chrome's Accessibility Tree to a virtual filesystem via a Chrome Extension
  <sub>★ 53 · TypeScript · MIT · npm · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @apireno/domshell`</sub>
- **[ofershap/real-browser-mcp](https://github.com/ofershap/real-browser-mcp)** — MCP server + Chrome extension that gives AI agents control of the user's real browser with existing sessions, logins, and cookies. No headless browser, no re-authentication
  <sub>★ 51 · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx real-browser-mcp --setup cursor`</sub>
- **[Agent360dk/browser-mcp](https://github.com/Agent360dk/browser-mcp)** — Chrome extension + MCP server that gives AI agents control of your real, logged-in Chrome browser (not headless). 34 tools, up to 10 concurrent color-coded sessions. Works with Claude Code, Cursor, VS Code, Codex CLI, and ZCode
  <sub>★ 45 · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agent360/browser-mcp install`</sub>
- **[acunningham-ship-it/veilbrowser](https://github.com/acunningham-ship-it/veilbrowser)** — Stealth browser automation over raw CDP, driving real unmodified Chrome with no Playwright or Puppeteer in the stack. Returns numbered element refs from the accessibility tree instead of CSS selectors, and can attach to an already-running Chrome to reuse logged-in sessions
  <sub>★ 42 · TypeScript · MIT · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/acunningham-ship-it/veilbrowser.git#subdirectory=python`</sub>
- **[BB-fat/browser-use-rs](https://github.com/BB-fat/browser-use-rs)** — Lightweight browser automation MCP server in Rust with zero dependencies
  <sub>★ 41 · Rust · MIT · source · pushed 2025-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BB-fat/browser-use-rs.git`</sub>
- **[imprvhub/mcp-browser-agent](https://github.com/imprvhub/mcp-browser-agent)** — A Model Context Protocol (MCP) integration that provides Claude Desktop with autonomous browser automation capabilities
  <sub>★ 41 · TypeScript · MPL-2.0 · clone · pushed 2026-02-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/imprvhub/mcp-browser-agent`</sub>
- **[webdriverio/mcp](https://github.com/webdriverio/mcp)** — Browser and mobile app automation using WebdriverIO, enabling AI agents to control browsers, interact with web elements, and automate native Android and iOS apps via the WebDriver and Appium protocols
  <sub>★ 39 · TypeScript · MIT · npm · pushed 2026-09-20 · macOS</sub>
  <sub>`npm install -g @wdio/mcp`</sub>
- **[Retio-ai/pagemap](https://github.com/Retio-ai/Retio-pagemap)** — Compresses ~100K-token HTML into 2-5K-token structured maps while preserving every actionable element. AI agents can read and interact with any web page at 97% fewer tokens
  <sub>★ 36 · Python · pip · pushed 2026-05-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install retio-pagemap`</sub>
- **[ymw0407/auth-fetch-mcp](https://github.com/ymw0407/auth-fetch-mcp)** — Fetch content from login-protected web pages (Notion, Google Docs, Jira, Confluence, etc.) by opening a real browser for authentication with persistent session caching
  <sub>★ 36 · TypeScript · MIT · clone · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ymw0407/auth-fetch-mcp.git`</sub>
- **[kimtth/mcp-aoai-web-browsing](https://github.com/kimtth/mcp-aoai-web-browsing)** — A minimal server/client MCP implementation using Azure OpenAI and Playwright
  <sub>★ 35 · Python · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kimtth/mcp-aoai-web-browsing.git`</sub>
- **[yinnho/aginxbrowser](https://github.com/yinnho/aginxbrowser)** — A browser built for AI agents as a single Rust binary with built-in V8 — no Chromium. Fetch with render-fallback tiers, multi-engine search, screenshots, and persistent login-state sessions (cookies/localStorage export/import), behind HTTP, native MCP (27 tools), and CDP — existing Playwright/Puppeteer code attaches directly. Stealth TLS fingerprints (Chrome/Firefox/Safari/Edge) for risk-controlle
  <sub>★ 31 · Rust · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx skills add yinnho/aginxbrowser`</sub>
- **[olostep/olostep-mcp-server](https://github.com/olostep/olostep-mcp-server)** — Web scraping, crawling, and search API. Extract content in Markdown/JSON, batch process 10k URLs, and get AI-powered answers with citations
  <sub>★ 23 · TypeScript · MIT · npm · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g olostep-mcp`</sub>
- **[samson-art/transcriptor-mcp](https://github.com/samson-art/transcriptor-mcp)** — Transcriptor MCP is your choice when you need transcripts and metadata for AI, summarization, or content analysis
  <sub>★ 22 · TypeScript · MIT · docker · pushed 2026-09-19 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 4200:4200 artsamsonov/transcriptor-mcp:latest`</sub>
- **[sh6drack/zen-mcp](https://github.com/sh6drack/zen-mcp)** — Zen Browser automation via WebDriver BiDi. 20 tools for navigation, form filling, screenshots, and JavaScript evaluation. No Selenium or Playwright required
  <sub>★ 19 · JavaScript · npm · pushed 2026-05-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g zen-mcp`</sub>
- **[LeonTing1010/tap](https://github.com/LeonTing1010/tap)** — MCP server that compiles AI browser automation into deterministic .tap.json plans (25-op closed union, zero runtime LLM), runs on your logged-in Chrome, and detects drift via semantic fingerprint diff when sites change. 65+ open community taps on 40+ sites
  <sub>★ 18 · JavaScript · MIT · npx · pushed 2026-08-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @taprun/cli embed cursor # or: vscode`</sub>
- **[lespaceman/agent-web-interface](https://github.com/drisplabs/browser-mcp)** — Token-efficient browser automation for LLM agents: semantic page snapshots and stable element IDs instead of raw DOM or screenshots, driving Chrome over CDP
  <sub>★ 17 · TypeScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lespaceman/agent-web-interface.git`</sub>
- **[SanggonBoy/PyreCrawl](https://github.com/SanggonBoy/PyreCrawl)** — Web browsing superpowers for AI agents: 13 MCP tools (scrape, extract, crawl, map, search, academic papers, batch, research, monitor, session). 3-tier auto-fallback ladder with free Cloudflare bypass, no API keys. Self-hosted Firecrawl alternative
  <sub>★ 15 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx pyrecrawl@latest`</sub>
- **[nnemirovsky/iwdp-mcp](https://github.com/nnemirovsky/iwdp-mcp)** — iOS Safari debugging via ios-webkit-debug-proxy — MCP server with full WebKit Inspector Protocol support (DOM, CSS, Network, Storage, Debugger, and more)
  <sub>★ 15 · Go · MIT · go · pushed 2026-05-03 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/nnemirovsky/iwdp-mcp/cmd/...@latest`</sub>
- **[protostatis/unbrowser](https://github.com/protostatis/unbrowser)** — Lightweight browser MCP server for LLM agents. Runs JavaScript, follows links, fills forms, manages cookies, and returns low-token BlockMaps from a single native binary without Chrome
  <sub>★ 15 · Rust · Apache-2.0 · pipx · pushed 2026-08-21 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pipx install pyunbrowser # recommended on macOS / modern Linux`</sub>
- **[xspadex/bilibili-mcp](https://github.com/xspadex/bilibili-mcp.git)** — A FastMCP-based tool that fetches Bilibili's trending videos and exposes them via a standard MCP interface
  <sub>★ 14 · Python · source · pushed 2025-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/xspadex/bilibili-mcp.git.git`</sub>
- **[Mingye-Lu/AgenticCrawler](https://github.com/Mingye-Lu/AgenticCrawler)** — Autonomous LLM-powered web crawler with 17 browser tools and goal-driven agent. Single binary, stealth browsing, 25 LLM providers
  <sub>★ 12 · Rust · MIT · psh · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/Mingye-Lu/AgenticCrawler/main/install.ps1 | iex`</sub>
- **[PrinceGabriel-lgtm/freshcontext-mcp](https://github.com/PrinceGabriel-lgtm/freshcontext-mcp)** — Real-time web intelligence with freshness timestamps. GitHub, HN, Scholar, arXiv, YC, jobs, finance, package trends — every result stamped with how old it is
  <sub>★ 12 · TypeScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PrinceGabriel-lgtm/freshcontext-mcp`</sub>
- **[PhungXuanAnh/selenium-mcp-server](https://github.com/PhungXuanAnh/selenium-mcp-server)** — A Model Context Protocol server providing web automation capabilities through Selenium WebDriver
  <sub>★ 11 · Python · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-server-selenium`</sub>
- **[Silbercue/public-browser](https://github.com/Silbercue/public-browser)** — Chrome automation over raw CDP — no Playwright, no extension bridge, no single-tab limit. Accessibility-tree refs cached across calls survive rerenders, so a page snapshot costs 1,124 chars against Playwright MCP's 6,084. Server-side plan executor runs multi-step flows in one tool call. Ships a Python API for LLM-free scripting. MIT
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npx public-browser profiles`</sub>
- **[segentic-lab/periscope-mcp](https://github.com/segentic-lab/periscope-mcp)** — Website &amp; web-app testing built for AI agents rather than raw browser bindings: 66 Playwright tools with hard assertions, auto form-fill, persistent authenticated sessions (incl. interactive login for 2FA/SSO), network mocking, real INP, and accessibility/SEO/GEO (llms.txt, AI-crawler access, WebMCP) + Lighthouse audits
  <sub>★ 10 · Python · AGPL-3.0 · clone · pushed 2026-07-18 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/segentic-lab/periscope-mcp.git`</sub>
- **[bighippoman/intercept-mcp](https://github.com/bighippoman/intercept-mcp)** — Multi-tier fallback chain for fetching web content as clean markdown. Handles tweets, YouTube, arXiv, PDFs, and regular pages with 9 fallback strategies
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y intercept-mcp`</sub>
- **[aparajithn/agent-scraper-mcp](https://github.com/aparajithn/agent-scraper-mcp)** — Web scraping MCP server for AI agents. 6 tools: clean content extraction, structured scraping with CSS selectors, full-page screenshots via Playwright, link extraction, metadata extraction (OG/Twitter cards), and Google search. Free tier with x402 micropayments
  <sub>★ 8 · Python · MIT · docker · pushed 2026-09-11 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 -e PUBLIC_HOST=localhost agent-scraper-mcp`</sub>
- **[Pantheon-Security/chrome-mcp-secure](https://github.com/Pantheon-Security/chrome-mcp-secure)** — Security-hardened Chrome automation with post-quantum encryption (ML-KEM-768 + ChaCha20-Poly1305), secure credential vault, memory scrubbing, and audit logging. 22 tools for browser automation and secure logins
  <sub>★ 8 · TypeScript · MIT · clone · pushed 2026-01-23 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Pantheon-Security/chrome-mcp-secure.git`</sub>
- **[browserless/browserless-mcp](https://github.com/browserless/browserless-mcp)** — Headless browser automation and web scraping infrastructure. Exposes the Browserless smart scraper API to LLM clients over MCP
  <sub>★ 7 · TypeScript · source · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/browserless/browserless-mcp.git`</sub>
- **[Cubenest/rrweb-stack](https://github.com/Cubenest/rrweb-stack)** — Local-first MCP server (@peekdev/mcp) + Chrome extension that records your real authenticated browser session (rrweb DOM + console + network, PII-masked, to local SQLite) and lets AI coding agents query it or drive the browser. No cloud, no telemetry
  <sub>★ 7 · TypeScript · Apache-2.0 · source · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Cubenest/rrweb-stack.git`</sub>
- **[copperline-labs/rendex-mcp](https://github.com/copperline-labs/rendex-mcp)** — Screenshot, PDF, and HTML rendering API for AI agents. Capture any URL or raw HTML as PNG/JPEG/WebP/PDF with batch processing, geo-targeting, async webhooks, and MCP-native integration. Free tier included
  <sub>★ 7 · TypeScript · MIT · source · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/copperline-labs/rendex-mcp.git`</sub>
- **[dashi96/chromium-bridge](https://github.com/dashi96/chromium-bridge)** — MCP server + Chrome extension that connects Claude Code to Chromium-based browsers (Arc, Vivaldi, Brave) where the official Claude in Chrome extension doesn't work — navigate, click, read pages, run JS, and record GIFs in the user's real browser
  <sub>★ 6 · JavaScript · MIT · source · pushed 2026-07-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dashi96/chromium-bridge.git`</sub>
- **[trueoriginlabs/vibatchium](https://github.com/trueoriginlabs/vibatchium)** — Self-hosted stealth browser automation for unattended agents. Drives real consumer Chrome via Patchright, holding N parallel persistent logged-in profiles on one daemon so sessions survive across runs. Encrypted credential vault with TOTP and IMAP email-code 2FA, a renderer-free TLS-impersonating fetch lane that reuses session cookies, token-frugal page extraction, and prompt-injection scanning on
  <sub>★ 6 · Python · Apache-2.0 · pipx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install vibatchium # core: browse / extract / screenshot / N parallel sessions`</sub>
- **[AishwaryShrivastav/vibe-testing](https://github.com/AishwaryShrivastav/vibe-testing)** — Code-aware browser testing for coding agents. Thirteen tools read routes, forms, field names, and existing tests before running Playwright scenarios, retaining regression history and producing HTML reports with screenshots. No internal LLM calls or API key. npx -y vibe-testing@latest --mcp
  <sub>★ 5 · TypeScript · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx vibe-testing@latest init`</sub>
- **[auspy/supasidebar-mcp](https://github.com/auspy/supasidebar-mcp)** — Access and organize your open browser tabs, bookmarks, and recently opened links across every macOS browser from your AI client. Powered by the free SupaSidebar app
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector npx -y supasidebar-mcp`</sub>
- **[corralimited/snapdiff-mcp](https://github.com/corralimited/snapdiff-mcp)** — Intent-aware visual verification for coding agents: the agent declares what a UI change should affect, and SnapDiff diffs the page against a baseline and flags anything that changed outside that intent for review or rollback — local screenshot capture via Playwright
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/corralimited/snapdiff-mcp.git`</sub>
- **[hunglp97/tabpilot-mcp](https://github.com/hunglp97/tabpilot-mcp)** — Drive the real, logged-in Chrome you already have open — cross-platform, zero dependencies beyond MCP SDK, token-budgeted reading (90%+ savings), complex SPA forms and matrix surveys, and 24/7 headless Ubuntu support
  <sub>★ 5 · Python · MIT · uv · pushed 2026-09-17 · macOS</sub>
  <sub>`uvx tabpilot-mcp doctor`</sub>
- **[andresolbach/nodriver-mcp-server](https://github.com/andresolbach/nodriver-mcp-server)** — Undetected Chrome automation via nodriver, for sites behind Cloudflare, DataDome and similar anti-bot systems. Direct CDP with no ChromeDriver binary, so navigator.webdriver stays undefined. 57 tools whose names match chrome-devtools-mcp, so switching is a config change: accessibility-tree snapshots, input automation, network/console inspection, device emulation, persistent profiles and session sa
  <sub>★ 4 · Python · MIT · uv · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install nodriver-mcp`</sub>
- **[Custodia-Admin/pagebolt-mcp](https://github.com/Custodia-Admin/pagebolt-mcp)** — MCP server for screenshots, PDFs, OG images, and narrated video recording from Claude Desktop, Cursor, and Windsurf
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Custodia-Admin/pagebolt-mcp.git`</sub>
- **[feedthrough/feedthrough](https://github.com/feedthrough/feedthrough)** — In-browser debug bridge that injects into your running web app, so an agent can read the DOM, console logs and network requests, and click/fill/inspect the page. Runs inside the page (not an external CDP driver), so it works in any browser and inside Cypress/Playwright runs
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @feedthrough/mcp`</sub>
- **[frsorrentino/chrome-bridge](https://github.com/frsorrentino/chrome-bridge)** — MCP server + Chrome extension that drive the user's real, logged-in Chrome over a local WebSocket. 59 token-efficient web-dev tools: compact element refs instead of screenshots, server-side table filtering, visual regression, accessibility/SEO/security audits, network mocking. Also runs on ChromeOS/Crostini
  <sub>★ 4 · JavaScript · MIT · clone · pushed 2026-09-16 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:frsorrentino/chrome-bridge.git`</sub>
- **[mi60dev/visionaire-engine](https://github.com/mi60dev/visionaire-engine)** — Design-debugging context for AI agents from a real Chrome: which CSS rule WINS with file:line, blast radius (how many other elements that rule styles) + a scoped-fix selector, WordPress/Elementor origin attribution, interaction timelines, live CSS fix trials, and pixel/alignment/WCAG-contrast audits. No AI inside — deterministic CDP
  <sub>★ 4 · TypeScript · Apache-2.0 · npx · pushed 2026-09-17 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx visionaire-engine init-harness`</sub>
- **[aethynio/aethyn-browser-mcp](https://github.com/aethynio/aethyn-browser-mcp)** — Drive a local Playwright browser through residential proxies with the agent choosing the exit country/city and holding one sticky identity per task. 10 tools: launch, navigate, accessibility snapshot, click, type, content extraction, exit-IP verification, and per-task identity rotation. Free trial, no card
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aethynio/aethyn-browser-mcp.git`</sub>
- **[bch1212/agentfetch-mcp](https://github.com/bch1212/agentfetch-mcp)** — Token-budgeted web fetch for AI agents. Auto-routes between Trafilatura, Jina Reader, FireCrawl, and pypdf based on URL pattern. estimate_tokens before fetch_url, 6h Redis cache, server-side max_tokens truncation. Open source MCP server (MIT) plus hosted REST API at agentfetch.dev — 500 free fetches/mo, no card
  <sub>★ 3 · Python · MIT · pip · pushed 2026-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentfetch-mcp`</sub>
- **[LarryWalkerDEV/mcp-immostage](https://github.com/LarryWalkerDEV/mcp-immostage)** — AI virtual staging for real estate. Stage empty rooms, beautify floor plans into 3D renders, classify room images, generate property descriptions, and get style recommendations
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LarryWalkerDEV/mcp-immostage.git`</sub>
- **[ilien-dev/svipall](https://github.com/ilien-dev/svipall)** — Local-first web reading with a tier ladder that escalates from plain HTTP to a real browser when a page pushes back. Pages as clean Markdown, whole-site crawls, keyless search, repeated page structure induced into rows, and a REST API. Attempts supported captchas on your own machine with optional local ONNX models, and parks the rest in a human dashboard. Labels blocked and low-quality pages inste
  <sub>★ 3 · Rust · AGPL-3.0 · psh · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/ilien-dev/svipall/main/install.ps1 | iex # Windows`</sub>
- **[realwigu/mcp-doctor](https://github.com/realwigu/mcp-doctor)** — Zero-config diagnostics for MCP servers. Auto-discovers configs across Claude Code, Cursor, VS Code, Windsurf, and Claude Desktop, then tests connections via JSON-RPC handshake, audits security issues, and benchmarks latency. Also runs as an MCP server itself
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-03-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @wigu/mcp-doctor`</sub>
- **[site-shot/site-shot-mcp](https://github.com/site-shot/site-shot-mcp)** — Website screenshot API for AI agents. Real Chromium rendering, full-page capture up to 20,000px, country/geo proxies, and automatic ad &amp; cookie-banner removal (cleaner images, fewer vision tokens). Two tools: capture_screenshot, capture_full_page. Install: npx -y site-shot-mcp
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y site-shot-mcp`</sub>
- **[hshintelligence/agent-scrape](https://github.com/hshintelligence/agent-scrape)** — Pay-per-call web scraping for AI agents via x402 micropayments on Base. Six tools: scrape, extract structured data, screenshot, metadata, browser session, workflow. No signup, no API keys — just USDC. HTTP + MCP transports
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hshintelligence/agent-scrape.git`</sub>
- **[MathiasPaulenko/wavexis-mcp](https://github.com/MathiasPaulenko/wavexis-mcp)** — MCP server exposing 220 browser automation tools across 13 capability tiers. Chrome + Firefox via CDP + BiDi. No Node.js, no Chromium download — uses your existing browser. Stealth mode, Lighthouse audits, multi-action YAML batching, raw CDP/BiDi access, structured errors with LLM-actionable suggestions
  <sub>★ 2 · Python · MIT · uv · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx wavexis-mcp`</sub>
- **[Metadrama/obscura-mcp](https://github.com/Metadrama/obscura-mcp)** — MCP server adapter for the lightweight Rust headless browser Obscura — high-performance web scraping with anti-detection. Perfect for AI agent automation. Server can run locally or as hosted endpoint
  <sub>★ 2 · JavaScript · MIT · npm · pushed 2026-05-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g obscura-mcp`</sub>
- **[prufa-dev/prufa-mcp](https://github.com/prufa-dev/prufa-mcp)** — Point your coding agent at a URL and get a real-browser QA audit: broken signup/login/checkout flows, JS console errors, missing analytics, consent + security headers, mobile tap targets, and accessibility — returned as machine-verified findings graded A–F. Free 60-second audit, no signup
  <sub>★ 2 · Python · Apache-2.0 · pipx · pushed 2026-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install prufa-mcp`</sub>
- **[KuvopLLC/purroxy2](https://github.com/KuvopLLC/purroxy2)** — Record what you do on any website and securely automate it forever. Replays browser actions in headless Playwright with encrypted credentials and AI-powered selector healing
  <sub>★ 2 · TypeScript · Apache-2.0 · source · pushed 2026-05-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KuvopLLC/purroxy2.git`</sub>
- **[vincentvella/devloop](https://github.com/vincentvella/devloop)** — Drives a browser (or a native Expo/React Native app on iOS/Android) and your dev server onto one correlated timeline, so a browser console error and the backend stack trace from the same moment line up. Includes repro action sequences, a unified log/network query API, and an Electron cockpit
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx mcporter list --allow-http --http-url http://localhost:7333/mcp --name devloop`</sub>
- **[parastejpal987-cmyk/opticparse-public](https://github.com/parastejpal987-cmyk/opticparse-public)** — Dual-engine Model Context Protocol server providing zero-CSS multimodal visual web scraping (96% noise reduction) and sub-1.6s zero-day phishing/crypto drainer detection for autonomous agents. 200 free trial requests out-of-the-box
  <sub>★ 1 · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @parastejpal987-cmyk/opticparse --client claude`</sub>
- **[awarselabs/awarse-mcp](https://github.com/awarselabs/awarse-mcp)** — Self-healing browser automation MCP server integrating Playwright with LLM-assisted locator repair
  <sub>★ 1 · Python · MIT · clone · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/skildunne/awarse-mcp.git`</sub>
- **[bgaze/snapstack-server](https://github.com/bgaze/snapstack-server)** — Pipe one-click browser-tab screenshots into any MCP client, 100% local — a companion extension captures, the local server stacks them and serves them to your LLM on demand
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-06-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g snapstack-server`</sub>
- **[brutalzinn/simple-mcp-selenium](https://github.com/brutalzinn/simple-mcp-selenium)** — An MCP Selenium Server for controlling browsers using natural language in Cursor IDE. Perfect for testing, automation, and multi-user scenarios
  <sub>★ 1 · TypeScript · source · pushed 2025-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/brutalzinn/simple-mcp-selenium.git`</sub>
- **[Ceki-me/mcp-server](https://github.com/Ceki-me/mcp-server)** — Rent real residential Chrome browsers from real humans — per-minute billing ($0.01/min), real fingerprints, residential IPs, no datacenter signals. MCP-native, with SDKs for Python, JS, LangChain, CrewAI, n8n. Crypto payouts
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ceki/sdk # Node`</sub>
- **[markmircea/Selenix-MCP-Server](https://github.com/markmircea/Selenix-MCP-Server)** — MCP server bridging Claude Desktop with Selenix for browser automation and testing. Create, run, debug, and manage browser tests through natural language
  <sub>★ 1 · TypeScript · Apache-2.0 · npm · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @selenix/mcp-server`</sub>
- **[junipr-labs/mcp-server](https://github.com/junipr-labs/mcp-server)** — Web intelligence API for AI agents — screenshot capture, PDF generation, page metadata extraction, and 75+ specialized data extractors for news, social media, SERP, pricing, and more. Free tier included
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/junipr-labs/mcp-server.git`</sub>
- **[Lyosis/claudeForSafari](https://github.com/Lyosis/claudeForSafari)** — Safari Web Extension + Node.js MCP bridge giving Claude Desktop full control over Safari — navigate, read pages, click elements, fill forms, and manage tabs. No Playwright or WebDriver dependency
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:Lyosis/claudeForSafari.git`</sub>
- **[lyrenth/lyrenth-mcp](https://github.com/lyrenth/lyrenth-mcp)** — Read any URL as a clean AIDocument (Markdown + structure) through Lyrenth's cached index
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lyrenth/lyrenth-mcp.git`</sub>
- **[maccydee/cute-web-scraper](https://github.com/maccydee/cute-web-scraper)** — Web scraping with four escalating fetch tiers (httpx, TLS impersonation, Playwright, stealth) that only escalate on a detected block. Returns clean markdown, or saves large scrapes into SQLite tables you query with read-only SQL to keep them out of the context window. 24 tools covering crawls, products, contacts, PDFs and change tracking. MIT, no API key
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/maccydee/cute-web-scraper`</sub>
- **[ScrapeUnblocker/scrapeunblocker-mcp](https://github.com/ScrapeUnblocker/scrapeunblocker-mcp)** — Fetch any web page's HTML (or AI-parsed JSON, or Google results) through the ScrapeUnblocker anti-bot API (Cloudflare, DataDome, PerimeterX, Akamai, Shape), using your own API key. Three tools: fetch_html, fetch_parsed, google_search. Install: npx -y scrapeunblocker-mcp
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ScrapeUnblocker/scrapeunblocker-mcp.git`</sub>
- **[seleniumboot/selenium-mcp](https://github.com/seleniumboot/selenium-mcp)** — Python MCP server for Selenium WebDriver — 84 tools for browser automation, element interactions, assertions, and self-healing locators, plus codegen for Java TestNG / JUnit 5 / Cucumber / pytest / C# NUnit / Playwright and CI pipelines (GitHub Actions / Jenkins / GitLab CI). No ChromeDriver setup needed
  <sub>★ 1 · Python · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install seleniumboot-mcp`</sub>
- **[snapshot-site/snapshot-site-mcp](https://github.com/snapshot-site/snapshot-site-mcp)** — Screenshot, visual-diff, and AI page-analysis API for AI agents. Capture any URL as PNG/JPEG/WebP/PDF/HTML, diff two versions of a page to catch visual regressions, and get an AI summary of a page. Hosted remote MCP at https://mcp.snapshot-site.com/mcp with OAuth, or npx -y @snapshot-site/mcp. In the official MCP registry as com.snapshot-site/screenshots
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx snapshot-site-mcp-http`</sub>
- **[SolveGate/solvegate-mcp](https://github.com/SolveGate/solvegate-mcp)** — Deal with Cloudflare Turnstile from an agent. inspect_page reports whether a page actually uses Turnstile and what its sitekey is — free, no API key — so the agent can look before it acts, and it says plainly when a page carries reCAPTCHA or hCaptcha instead, or is a full-page Cloudflare interstitial rather than an embedded widget. solve_turnstile and get_solve clear the challenge and return a tok
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx solvegate-mcp`</sub>
- **[sylin-org/ghostlight](https://github.com/sylin-org/ghostlight)** — Visible local browser automation in the signed-in Chromium profile you already use, with useful recovery and optional policy and audit
  <sub>★ 1 · Rust · Apache-2.0 · npx · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y ghostlight install`</sub>
- **[agent-infra/mcp-server-browser](https://github.com/bytedance/UI-TARS-desktop/tree/main/packages/agent-infra/mcp-servers/browser)** — Browser automation capabilities using Puppeteer, both support local and remote browser connection
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-09-11</sub>
  <sub>`git clone https://github.com/bytedance/UI-TARS-desktop.git && cd UI-TARS-desktop/packages/agent-infra/mcp-servers/browser`</sub>
- **[ami-guru/x402-scraper-engine](https://github.com/ami-guru/x402-scraper-engine)** — Production HTTP 402 micropayment web scraper, Llama-3 digest, and Twitter intelligence engine for AI agents on Base L2. Zero API keys, pay-per-call in USDC
  <sub>TypeScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ami-guru/x402-scraper-engine.git`</sub>
- **[autokeren/ghostfox](https://github.com/autokeren/ghostfox)** — Self-hosted stealth browser for AI agents: own Firefox engine fork (C++-level fingerprint spoofing) + Rust MCP runtime. page_a11y semantic vision pierces shadow DOM, login_state detection, evidence recording, Android personas. 19 tools, 6 platforms. Glama 100% quality score
  <sub>C++ · MIT · script · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/autokeren/ghostfox/main/install.sh | bash`</sub>
- **[dmytrome/groundhog](https://github.com/dmytrome/groundhog)** — Web search, read and research over a real stealth-patched Chrome, driven by raw CDP so the Runtime domain is never enabled and the isAutomatedWithCDP tell is absent. Strips text that is invisible in the rendered DOM before the model reads it and reports each occurrence in threats, returns a SHA-256 provenance receipt per source, and re-checks the SSRF guard after redirects. research ranks passages
  <sub>Python · MIT · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --rm --name groundhog-browser --shm-size 512m \`</sub>
- **[getrupt/ashra-mcp](https://github.com/getrupt/ashra-mcp)** — Extract structured data from any website. Just prompt and get JSON
  <sub>unavailable</sub>
- **[modelcontextprotocol/server-puppeteer](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/puppeteer)** — Browser automation for web scraping and interaction
  <sub>JavaScript · MIT · in-repo · pushed 2025-05-28</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers-archived.git && cd servers-archived/src/puppeteer`</sub>
- **[paipaipai666/nexus-browser-mcp](https://github.com/paipaipai666/nexus-browser-mcp)** — Browser automation via accessibility tree with event-driven deterministic snapshots (MutationObserver quiet-window instead of fixed sleeps), HITL governance gates with redacted JSONL audit, multi-task isolation with self-healing rebuilds, and developer observability (console / JS errors / network / Web Vitals)
  <sub>Python · MIT · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx nexus-browser-mcp`</sub>
- **[RapierCraft/alterlab-mcp-server](https://github.com/RapierCraft/alterlab-mcp-server)** — Web scraping, structured data extraction, and screenshots with JavaScript rendering, residential proxy rotation, and automatic retries
  <sub>TypeScript · MIT · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install alterlab-mcp-server --client claude`</sub>
- **[reeinharddd/snapmcp](https://github.com/reeinharddd/snapmcp)** — Precision visual captures for AI agents — real-colors terminal, syntax-highlighted code, browser, markdown, HTML, and git-diff as PNG/JPEG/PDF/GIF, plus multi-shot sequences and doc embedding. Rendered fully local via Playwright (SSRF-safe by default)
  <sub>TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g snapmcp`</sub>
- **[screenshotscout/screenshotscout-mcp](https://github.com/screenshotscout/screenshotscout-mcp)** — Capture webpages as images or PDFs with full-page and element targeting, device and viewport controls, location selection, page interactions, blocking options, and configurable output
  <sub>TypeScript · MIT · source · pushed 2026-08-03 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/screenshotscout/screenshotscout-mcp.git`</sub>
- **[serkan-ozal/browser-devtools-mcp](https://github.com/serkan-ozal/browser-devtools-mcp)** — An MCP Server enables AI assistants to autonomously test, debug, and validate web applications
  <sub>unavailable</sub>
- **[softvoyagers/pageshot-api](https://github.com/softvoyagers/pageshot-api)** — Free webpage screenshot capture API with format, viewport, and dark mode options. No API key required
  <sub>unavailable</sub>
- **[User0856/snaprender-mcp](https://github.com/User0856/snaprender-integrations/tree/main/mcp-server)** — Screenshot API for AI agents — capture any website as PNG, JPEG, WebP, or PDF with device emulation, dark mode, ad blocking, and cookie banner removal. Free tier included
  <sub>JavaScript · MIT · in-repo · pushed 2026-06-09</sub>
  <sub>`git clone https://github.com/User0856/snaprender-integrations.git && cd snaprender-integrations/mcp-server`</sub>
- **[zumerlab/snapsurf](https://github.com/zumerlab/snapsurf)** — Browser navigation and verification for agents: a ~2 KB semantic page digest, ranked whole-page text search, a typed diff after each action (added/removed/state/covered, with a faithful changed: false), and assertions over that diff. Local Playwright Chromium; also embeddable in-page via SnapDOM
  <sub>JavaScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @zumer/snapsurf serve`</sub>
- **[zzzjy765/ottersnap-mcp](https://github.com/zzzjy765/ottersnap-mcp)** — Glint Render (by Moyu) — web rendering &amp; evidence API for AI agents: screenshots, PDFs, OG images, monitoring, extraction and tamper-evident evidence. Free tier included. npx -y ottersnap-mcp
  <sub>JavaScript · MIT · npm · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ottersnap-mcp`</sub>

## Art &amp; Culture

- **[ahujasid/blender-mcp](https://github.com/ahujasid/mcp-for-blender)** — MCP server for working with Blender
  <sub>★ 29.2k · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-for-blender install-addon`</sub>
- **[samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp)** — MCP server integration for DaVinci Resolve providing powerful tools for video editing, color grading, media management, and project control
  <sub>★ 3.1k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx davinci-resolve-mcp setup`</sub>
- **[jau123/MeiGen-AI-Design-MCP](https://github.com/jau123/MeiGen-AI-Design-MCP)** — AI image generation &amp; editing MCP server with 1,500+ curated prompt library, smart prompt enhancement, and multi-provider routing (local ComfyUI, MeiGen Cloud, OpenAI-compatible APIs)
  <sub>★ 1.8k · TypeScript · MIT · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g meigen@2.0.1`</sub>
- **[abhiemj/manim-mcp-server](https://github.com/abhiemj/manim-mcp-server)** — A local MCP server that generates animations using Manim
  <sub>★ 644 · Python · MIT · pip · pushed 2025-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install manim`</sub>
- **[diivi/aseprite-mcp](https://github.com/diivi/aseprite-mcp)** — MCP server using the Aseprite API to create pixel art
  <sub>★ 582 · Python · MIT · docker · pushed 2026-07-29 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -it --rm aseprite-mcp:latest`</sub>
- **[cantian-ai/bazi-mcp](https://github.com/cantian-ai/bazi-mcp)** — Provides comprehensive and accurate Bazi (Chinese Astrology) charting and analysis
  <sub>★ 432 · TypeScript · ISC · npx · pushed 2025-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @cantian-ai/bazi-mcp --client claude`</sub>
- **[burningion/video-editing-mcp](https://github.com/burningion/video-editing-mcp)** — Add, Analyze, Search, and Generate Video Edits from your Video Jungle Collection
  <sub>★ 289 · Python · npx · pushed 2025-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install video-editor-mcp --client claude`</sub>
- **[ConstantineB6/comfy-pilot](https://github.com/ConstantineB6/comfy-pilot)** — MCP server for ComfyUI that lets AI agents view, edit, and run node-based image generation workflows with an embedded terminal
  <sub>★ 230 · Python · MIT · source · pushed 2026-02-16 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ConstantineB6/comfy-pilot.git`</sub>
- **[omni-mcp/isaac-sim-mcp](https://github.com/omni-mcp/isaac-sim-mcp)** — A MCP Server and an extension enables natural language control of NVIDIA Isaac Sim, Lab, OpenUSD and etc
  <sub>★ 191 · Python · MIT · clone · pushed 2025-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/omni-mcp/isaac-sim-mcp`</sub>
- **[cswkim/discogs-mcp-server](https://github.com/cswkim/discogs-mcp-server)** — MCP server to interact with the Discogs API
  <sub>★ 125 · TypeScript · MIT · docker · pushed 2026-07-06 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --env-file .env discogs-mcp-server:latest`</sub>
- **[PatrickPalmer/MayaMCP](https://github.com/PatrickPalmer/MayaMCP)** — MCP server for Autodesk Maya
  <sub>★ 102 · Python · MIT · source · pushed 2025-05-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PatrickPalmer/MayaMCP.git`</sub>
- **[8enSmith/mcp-open-library](https://github.com/8enSmith/mcp-open-library)** — A MCP server for the Open Library API that enables AI assistants to search for book information
  <sub>★ 94 · TypeScript · MIT · docker · pushed 2026-09-03 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 mcp-open-library`</sub>
- **[pzfreo/build123d-mcp](https://github.com/pzfreo/build123d-mcp)** — MCP server that exposes build123d parametric CAD operations as tools, enabling AI assistants to create, inspect, and iterate on 3D geometry interactively. Renders PNG/SVG views, measures geometry, and exports STEP/STL
  <sub>★ 90 · Python · Apache-2.0 · clone · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pzfreo/build123d-mcp.git`</sub>
- **[yuna0x0/anilist-mcp](https://github.com/yuna0x0/anilist-mcp)** — A MCP server integrating AniList API for anime and manga information
  <sub>★ 88 · TypeScript · MIT · npx · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector -e ANILIST_TOKEN=your_api_token npx anilist-mcp`</sub>
- **[GenWaveLLC/svgmaker-mcp](https://github.com/GenWaveLLC/svgmaker-mcp)** — Provides AI-driven SVG generation and editing via natural language, with real-time updates and secure file handling
  <sub>★ 87 · TypeScript · MIT · npx · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx svgmaker-mcp`</sub>
- **[djalal/quran-mcp-server](https://github.com/djalal/quran-mcp-server)** — MCP server to interact with Quran.com corpus via the official REST API v4
  <sub>★ 72 · TypeScript · MIT · source · pushed 2025-06-12 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/djalal/quran-mcp-server.git`</sub>
- **[r-huijts/rijksmuseum-mcp](https://github.com/r-huijts/rijksmuseum-mcp)** — Rijksmuseum API integration for artwork search, details, and collections
  <sub>★ 72 · JavaScript · MIT · source · pushed 2025-02-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/r-huijts/rijksmuseum-mcp.git`</sub>
- **[TwelveTake-Studios/reaper-mcp](https://github.com/TwelveTake-Studios/reaper-mcp)** — MCP server enabling AI assistants to control REAPER DAW for mixing, mastering, MIDI composition, and full music production with 129 tools
  <sub>★ 63 · Lua · MIT · uv · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx twelvetake-reaper-mcp --install-bridge`</sub>
- **[raveenb/fal-mcp-server](https://github.com/luminarylane/fal-mcp-server)** — Generate AI images, videos, and music using Fal.ai models (FLUX, Stable Diffusion, MusicGen) directly in Claude Desktop
  <sub>★ 56 · Python · MIT · uv · pushed 2026-05-04 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx --from fal-mcp-server fal-mcp`</sub>
- **[rosasynthesiz/flstudio-mcp](https://github.com/rosasynthesiz/flstudio-mcp)** — Control FL Studio with AI: in-DAW mixing (Mix Doctor, gain staging, EQ/comp/reverb, reference matching), routing, and composition. 67 tools
  <sub>★ 51 · Python · MIT · clone · pushed 2026-07-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/rosasynthesiz/flstudio-mcp`</sub>
- **[Pantani/tdmcp](https://github.com/Pantani/tdmcp)** — Stop wiring nodes by hand — describe a visual and the AI builds a real, playable TouchDesigner network: audio-reactive, generative, particle, 3D and feedback systems with live knobs and MIDI/OSC/DMX, checking and previewing its own work
  <sub>★ 43 · TypeScript · MIT · clone · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pantani/tdmcp.git`</sub>
- **[Cifero74/mcp-apple-music](https://github.com/Cifero74/mcp-apple-music)** — Full Apple Music integration: search catalog, browse personal library, manage playlists, and get personalised recommendations.- codex-curator/studiomcphub 🐍 ☁️ - 32 creative AI tools (18 free) for autonomous agents: image generation (SD 3.5), ESRGAN upscaling, background removal, product mockups, CMYK conversion, print-ready PDF, SVG vectorization, invisible watermarking, AI metadata enrichment, p
  <sub>★ 42 · Python · MIT · clone · pushed 2026-05-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/marioinghilleri/mcp-apple-music`</sub>
- **[attalla1/photopea-mcp-server](https://github.com/attalla1/photopea-mcp-server)** — AI-powered image editing through Photopea with 34 tools for documents, layers, text, shapes, filters, effects, and export. npx photopea-mcp-server
  <sub>★ 38 · TypeScript · MIT · npm · pushed 2026-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g photopea-mcp-server`</sub>
- **[OctoEverywhere/mcp](https://github.com/OctoEverywhere/mcp)** — #️⃣ ☁️ - A 3D printer MCP server that allows for getting live printer state, webcam snapshots, and printer control
  <sub>★ 37 · Apache-2.0 · source · pushed 2025-07-03</sub>
  <sub>`git clone https://github.com/OctoEverywhere/mcp.git`</sub>
- **[mikechao/metmuseum-mcp](https://github.com/mikechao/metmuseum-mcp)** — Metropolitan Museum of Art Collection API integration to search and display artworks in the collection
  <sub>★ 35 · TypeScript · MIT · npx · pushed 2026-04-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y metmuseum-mcp`</sub>
- **[flamexnreal/davinci-resolve-ai-bridge-mcp](https://github.com/flamexnreal/davinci-resolve-ai-bridge-mcp)** — Local MCP bridge for DaVinci Resolve Free and Studio, with timeline inspection, zoom animation, supported color adjustments, and duplicate-timeline review. Windows/Linux need live verification
  <sub>★ 23 · Python · MIT · psh · pushed 2026-09-07 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/flamexnreal/davinci-resolve-ai-bridge-mcp/main/install.ps1 | iex`</sub>
- **[arikusi/nakkas](https://github.com/arikusi/nakkas)** — MCP server that turns AI into an SVG artist. One rendering engine with JSON config, AI controls all design parameters. CSS @keyframes + SMIL animations, 16+ element types, parametric curves, filters, gradients, PNG preview
  <sub>★ 22 · TypeScript · MIT · clone · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/arikusi/nakkas`</sub>
- **[asmith26/jupytercad-mcp](https://github.com/asmith26/jupytercad-mcp)** — An MCP server for JupyterCAD that allows you to control it using LLMs/natural language
  <sub>★ 20 · Python · Apache-2.0 · uv · pushed 2025-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --with jupytercad-mcp jupytercad-mcp`</sub>
- **[r-huijts/oorlogsbronnen-mcp](https://github.com/r-huijts/oorlogsbronnen-mcp)** — Oorlogsbronnen (War Sources) API integration for accessing historical WWII records, photographs, and documents from the Netherlands (1940-1945)
  <sub>★ 15 · TypeScript · MIT · clone · pushed 2025-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/r-huijts/oorlogsbronnen-mcp.git`</sub>
- **[austenstone/myinstants-mcp](https://github.com/austenstone/myinstants-mcp)** — A soundboard MCP server with millions of meme sounds from myinstants.com. Search, play, and browse categories — let your AI agent play vine boom when code compiles. npx myinstants-mcp
  <sub>★ 14 · JavaScript · npx · pushed 2026-03-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx myinstants-mcp`</sub>
- **[cfpramod/open-museum-mcp](https://github.com/cfpramod/open-museum-mcp)** — Federated, license-verified search across The Met, Cleveland, AIC, Wikimedia Commons, and Europeana. Strict-default-deny rights gate accepts only CC0 / Public Domain Mark. Tools: search, get, cite (full / caption / short), dynasty/region discovery. npx -y open-museum-mcp
  <sub>★ 13 · TypeScript · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cfpramod/open-museum-mcp`</sub>
- **[BluesPrince/thiri-mcp](https://github.com/BluesPrince/thiri-mcp)** — Deterministic music-theory server: chord &amp; Roman-numeral analysis, voicing, and reharmonization — computed, not hallucinated. Hosted at mcp.thiri.ai, no third-party account required. npx @bluesprincemedia/thiri-mcp
  <sub>★ 10 · JavaScript · source · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BluesPrince/thiri-mcp.git`</sub>
- **[molanojustin/smithsonian-mcp](https://github.com/molanojustin/smithsonian-mcp)** — MCP server that provides AI assistants with access to the Smithsonian Institution's Open Access collections
  <sub>★ 10 · Python · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @molanojustin/smithsonian-mcp`</sub>
- **[shunshi-ai/bazi-reader-mcp](https://github.com/shunshi-ai/bazi-reader-mcp)** — Bazi (Four Pillars / 四柱推命 / 사주팔자) charting MCP server with true solar time correction and multilingual output (中文/EN/日本語/한국어). npx shunshi-bazi-mcp
  <sub>★ 10 · TypeScript · MIT · npx · pushed 2026-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y shunshi-bazi-mcp`</sub>
- **[gupta-kush/spotify-mcp](https://github.com/gupta-kush/spotify-mcp)** — 93-tool Spotify server with smart shuffle, natural language song search, vibe analysis, artist network mapping, taste evolution, and playlist power tools. Works after Spotify's Feb 2026 API changes
  <sub>★ 9 · Python · MIT · uv · pushed 2026-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx spotify-mcp`</sub>
- **[leonardoca1/aesthetics-wiki-mcp](https://github.com/leonardoca1/aesthetics-wiki-mcp)** — Search, read, and discover thousands of visual aesthetics (cottagecore, dark academia, y2k, goblincore, and many more) from the Aesthetics Wiki. Great for moodboards, brand direction, and creative inspiration. uvx aesthetics-wiki-mcp
  <sub>★ 9 · Python · MIT · npx · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run aesthetics-wiki-mcp`</sub>
- **[tasopen/mcp-alphabanana](https://github.com/tasopen/mcp-alphabanana)** — Local MCP server for generating image assets with Google Gemini (Nano Banana 2 / Pro). Supports transparent PNG/WebP output, exact resizing/cropping, up to 14 reference images, and Google Search grounding
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @tasopen/mcp-alphabanana`</sub>
- **[wretcher207/reaper-daemon](https://github.com/wretcher207/reaper-daemon)** — Drive the REAPER DAW from an AI agent over a local file bridge with no network port: read every plugin and parameter, set FX values, write automation, and measure a mix move before and after. Every change runs inside a REAPER undo block
  <sub>★ 8 · Python · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wretcher207/reaper-daemon.git`</sub>
- **[AceDataCloud/MCPNanoBanana](https://github.com/AceDataCloud/NanoBananaMCP)** — NanoBanana AI image generation and editing with virtual try-on and product placement in realistic scenes
  <sub>★ 7 · Python · MIT · uv · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-nanobanana-pro`</sub>
- **[albertnahas/icogenie-mcp](https://github.com/albertnahas/icogenie-mcp)** — AI-powered SVG icon generation MCP server. Generate production-ready SVG icons from text descriptions with customizable styles
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @icogenie/mcp`</sub>
- **[gchen19/AnkusDrive](https://github.com/gchen19/AnkusDrive)** — Drive FreeCAD from an agent: 280+ tools for parametric CAD, TechDraw drawings with GD&amp;T, CalculiX FEM, and CFD/thermal/EM/multiphysics simulation. Requires a local FreeCAD 1.1
  <sub>★ 6 · Python · Apache-2.0 · pipx · pushed 2026-09-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`pipx install ankusdrive # from PyPI — isolated app, `ankusdrive` on PATH`</sub>
- **[mikan-atomoki/text-to-model](https://github.com/mikan-atomoki/text-to-model)** — Turn natural language into 3D models in Fusion 360. 64 CAD tools including sketches, extrudes, fillets, and JIS standard parts
  <sub>★ 6 · Python · MIT · clone · pushed 2026-03-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mikan-atomoki/text-to-model.git`</sub>
- **[Pantani/ableton-mind](https://github.com/Pantani/ableton-mind)** — Control Ableton Live from Claude, Cursor or Codex through a local Remote Script bridge: inspect sets, create tracks, scenes and clips, load devices, apply music recipes, and verify changes against Live state
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-06-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g ableton-mind`</sub>
- **[j-east/pixel-surgeon-mcp](https://github.com/j-east/pixel-surgeon-mcp)** — AI image and video generation, editing, and transplant-grade region repair. Multi-provider (Gemini 3.1 Flash Image, GPT Image 2, Grok Imagine, Veo 3), 9 tools, 4 style presets, grid-based and interactive crop repair. npx pixel-surgeon-mcp
  <sub>★ 5 · JavaScript · MIT · npx · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx pixel-surgeon-mcp`</sub>
- **[drakonkat/wizzy-mcp-tmdb](https://github.com/drakonkat/wizzy-mcp-tmdb)** — A MCP server for The Movie Database API that enables AI assistants to search and retrieve movie, TV show, and person information
  <sub>★ 4 · JavaScript · MIT · npm · pushed 2025-09-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g wizzy-mcp-tmdb`</sub>
- **[AceDataCloud/MCPFlux](https://github.com/AceDataCloud/FluxMCP)** — Flux AI image generation and editing (Black Forest Labs) via Ace Data Cloud API
  <sub>★ 3 · Python · MIT · docker · pushed 2026-08-28 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-flux-pro:latest`</sub>
- **[AceDataCloud/MCPSeedream](https://github.com/AceDataCloud/SeedreamMCP)** — ByteDance Seedream image generation and editing via Ace Data Cloud API
  <sub>★ 3 · Python · MIT · docker · pushed 2026-09-10 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-seedream-pro:latest`</sub>
- **[aliafsahnoudeh/shahnameh-mcp-server](https://github.com/aliafsahnoudeh/shahnameh-mcp-server)** — MCP server for accessing the Shahnameh (Book of Kings) Persian epic poem by Ferdowsi, including sections, verses and explanations
  <sub>★ 3 · Python · source · pushed 2025-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aliafsahnoudeh/shahnameh-mcp-server.git`</sub>
- **[gavxm/ani-mcp](https://github.com/gavxm/ani-mcp)** — MCP server for AniList with taste-aware recommendations, watch analytics, social tools, and full list management
  <sub>★ 3 · TypeScript · MIT · docker · pushed 2026-08-06 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -e ANILIST_USERNAME=your_username ani-mcp`</sub>
- **[labelgrid/labelgrid-mcp](https://github.com/labelgrid/labelgrid-mcp)** — Official LabelGrid server — manage your music distribution catalog, releases, analytics and royalties from any MCP client
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @labelgrid/cli # Node 20+`</sub>
- **[sharafutdinovdi/revit-model-mcp](https://github.com/sharafutdinovdi/revit-model-mcp)** — #️⃣ 🏠 🪟 - Read a live Autodesk Revit model (elements, parameters, views, warnings, PNG view exports) from any MCP client; model-changing actions are opt-in behind two gates, with dry runs and post-commit verification. Ships MSI installers for Revit 2022-2027 and a Claude Desktop bundle
  <sub>★ 3 · C# · MIT · source · pushed 2026-09-20 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sharafutdinovdi/revit-model-mcp.git`</sub>
- **[alexzavialov/travel-art-mcp](https://github.com/alexzavialov/travel-art-mcp)** — Art-tourism data for AI agents: biennales (Venice, Whitney), art fairs (Art Basel, Frieze), and major museum visitor guides (Louvre, Vatican, Uffizi, Prado, +growing). Three tools: find_art_events, find_museum_guide, recommend_art_trip. Hosted at https://mcp.travel.art/, no install. Catalogue grounded in 10 cornerstone editorial guides at travel.art
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alexzavialov/travel-art-mcp.git`</sub>
- **[CreativeClawCo/creative-claw-marketplace](https://github.com/CreativeClawCo/creative-claw-marketplace)** — Remote MCP server giving Claude, Claude Code, and OpenClaw access to every top AI media model (Flux 2 Pro, Nano Banana Pro, GPT Image 2, Recraft V3, Veo 3.1, Sora 2, Kling, Seedance, Hailuo, ElevenLabs). Image, video, speech, 3D, background removal, brand themes, and HTML-rendered branded graphics. One connection, no API keys, pay-per-use credits
  <sub>★ 2 · JavaScript · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add CreativeClawCo/creative-claw-marketplace`</sub>
- **[clanker-records/crompton-network](https://github.com/clanker-records/crompton-network)** — Machine-native listening platform for C.W.A.'s Straight Outta Crompton - the first album released to machines before humans. Your agent can listen. For real. npx @clanker-records/crompton-network
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-06-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @clanker-records/crompton-network`</sub>
- **[delmas41/gradusnotation](https://github.com/delmas41/gradusnotation)** — Render music notation (SVG + MusicXML + MIDI) from a JSON score, validate input, analyze MusicXML harmonically, and search a curated music-theory knowledge base. Free, no auth. npx -y @gradusmusic/notation-mcp
  <sub>★ 2 · JavaScript · MIT · clone · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/delmas41/gradusnotation`</sub>
- **[gokimedia/tarot-mcp-server](https://github.com/gokimedia/tarot-mcp-server)** — Complete 78-card tarot meanings, upright and reversed interpretations, love and career readings, yes-or-no answers, random draws, and three-card spreads. npx -y @deckaura/tarot-mcp-server
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @deckaura/tarot-mcp-server`</sub>
- **[khglynn/spotify-bulk-actions-mcp](https://github.com/khglynn/spotify-bulk-actions-mcp)** — Bulk Spotify operations with confidence-scored song matching, batch playlist creation from CSV/podcast lists, and library exports for discovering your most-saved artists and albums
  <sub>★ 2 · Python · MIT · pip · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install spotify-bulk-actions-mcp`</sub>
- **[peek-travel/mcp-intro](https://github.com/peek-travel/mcp-intro)** — Remote MCP Server for discovering and planning experiences, at home and on vacation
  <sub>★ 2 · source · pushed 2025-09-23 · Win?</sub>
  <sub>`git clone https://github.com/peek-travel/mcp-intro.git`</sub>
- **[Psalmustrack/lambdacad-mcp](https://github.com/Psalmustrack/lambdacad-mcp)** — Drive a professional DWG CAD with AI on Linux: 100 tools for BricsCAD via a pure AutoLISP bridge (no COM, no SDK) — 2D drafting with dimensions and hatches, 3D solids with booleans, auto-generated 2D drawing views, PDF export. Portable to any AutoLISP-capable CAD
  <sub>★ 2 · Python · Apache-2.0 · clone · pushed 2026-08-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Psalmustrack/lambdacad-mcp`</sub>
- **[doctorm333/promptpilot-mcp-server](https://github.com/doctorm333/promptpilot-mcp-server)** — Generate images, video, and audio via 20+ AI models (Flux, GPT-Image-1, Imagen 4, Grok, Seedance, ElevenLabs). Prompt builder with styles, lighting, camera, mood presets. Batch generation support
  <sub>★ 2 · TypeScript · source · pushed 2026-09-12 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/doctorm333/promptpilot-mcp-server.git`</sub>
- **[AIDataNordic/alexandria-mcp](https://github.com/AIDataNordic/Alexandria-mcp)** — Semantic search over 4.6 million text chunks from 20,000 classical philosophy and humanities works. Built for AI agents using FastMCP.
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AIDataNordic/alexandria-mcp.git`</sub>
- **[ArturLys/ao3-mcp](https://github.com/ArturLys/ao3-mcp)** — Search the Archive of Our Own (AO3) and delegate full-fic reading to a secondary model (Gemini), so the agent recommends from the actual text, not the author's blurb. pip install ao3-mcp
  <sub>★ 1 · Python · MIT · pip · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ao3-mcp`</sub>
- **[quokkapix/quokkapix-mcp](https://github.com/quokkapix/quokkapix-mcp)** — Local MCP adapter/server for browser-only image workflows. Resize, compress, convert, remove backgrounds, strip metadata, watermark and export image packs through QuokkaPix without uploading source images to a processing server. npx quokkapix-mcp
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx quokkapix-mcp`</sub>
- **[forgemeshlabs/imagegen-mcp](https://github.com/forgemeshlabs/imagegen-mcp)** — AI image generation MCP server with generate, background removal, 4x HD upscale, and full pro pipeline tools. Pay per image in USDC on Base mainnet via x402; no API key or subscription required
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/forgemeshlabs/imagegen-mcp.git`</sub>
- **[memebo-at/memeboat-mcp](https://github.com/memebo-at/memeboat-mcp)** — Create real, shareable memes from 25,000+ templates on memebo.at. Search the catalog, caption a template, get a live meme URL back. Free, anonymous, no API key. Remote server at https://memebo.at/mcp or npx -y memeboat-mcp
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-07-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y memeboat-mcp`</sub>
- **[noteboxd/mcp](https://github.com/Noteboxd/mcp)** — Fragrance and perfume API for AI: query the Noteboxd encyclopedia for fragrances, notes, accords, brands, perfumers, reviews, and charts. Hosted remote server at https://mcp.noteboxd.com/mcp, or run locally with npx -y @noteboxd/mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @noteboxd/mcp`</sub>
- **[UModeler/picoberry-mcp](https://github.com/UModeler/picoberry-mcp)** — Generate 3D models and images from a text prompt or reference images, then remesh, retexture, auto-rig, animate, and export GLB/FBX/OBJ through the PicoBerry API. Install: npx -y @picoberry/mcp-server
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/UModeler/picoberry-mcp.git`</sub>
- **[musajala/musajala-mcp](https://github.com/musajala/musajala-mcp)** — Living collaborative Arabic poetry arena &amp; Poetic Equity protocol connecting Claude, Cursor, and AI agents with human poets
  <sub>JavaScript · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/musajala/musajala-mcp.git`</sub>
- **[fgbytes/sansfiction-mcp](https://github.com/fgbytes/sansfiction-mcp)** — Search a books catalog (titles, authors, series, ISBNs, collections) and manage a personal reading library — status, reading progress, ratings, reviews, collections, stats. Public catalog needs no auth; personal library uses a bearer token. Hosted MCP: https://sansfiction.com/api/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sansfiction-mcp`</sub>
- **[krupalghori44-dev/infyicon-mcp](https://github.com/krupalghori44-dev/infyicon-mcp)** — Search 161,000+ free hand-drawn Infyicon icons in four matching styles and fetch ready-to-embed SVG markup or PNG URLs. Hosted remote server (https://infyicon.com/mcp), no auth required
  <sub>JavaScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y infyicon-mcp # stdio bridge`</sub>
- **[DataCraftsmanAU/vineverse-mcp](https://github.com/DataCraftsmanAU/vineverse-mcp)** — The Bible as a knowledge graph: 31,102 verses of the Berean Standard Bible, ~3,000 people, ~1,300 places with coordinates, ~3,000 Nave's topical themes, ~2,900 Strong's Hebrew lexemes, the 613 commandments, and 90,564 connections between them. 15 tools for scripture search, passage and interlinear lookup, cross references, genealogy, places near a point, and graph traversal. Public-domain sources,
  <sub>JavaScript · MIT · docker · pushed 2026-09-05 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm vineverse-mcp`</sub>
- **[fatenava/fatenava-mcp](https://github.com/fatenava/fatenava-mcp)** — All-in-one destiny charting: BaZi (八字/四柱推命/사주), Zi Wei Dou Shu (紫微斗數), and Western astrology natal charts in one tool — true solar time correction, multilingual input (中文/EN/日本語/한국어), free, no account required. npx -y fatenava-mcp
  <sub>TypeScript · MIT · source · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fatenava/fatenava-mcp.git`</sub>
- **[hanshs474/kavel-mcp](https://github.com/hanshs474/kavel-mcp)** — Discover Kavel’s AI photo/video generators (hairstyle, figurine, pet portrait, wedding, 90s yearbook, dance video, HD restore), get model-tuned prompts, and open the right tool to generate on www.kavel.ai. npx kavel-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx kavel-mcp`</sub>
- **[joshseane/-nmlp-mcp](https://github.com/joshseane/-nmlp-mcp)** — First-edition identification — points of issue, number-line decoding, and publisher rules over a CC-BY, DOI-cited dataset of 6,717 titles — plus New Mexico book-donation logistics. Hosted remote server, no auth. Endpoint: https://newmexicoliteracyproject.org/api/mcp · Registry: org.newmexicoliteracyproject/nmlp-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y github:joshseane/-nmlp-mcp`</sub>
- **[ni-c/calibreweb-mcp](https://github.com/ni-c/calibreweb-mcp)** — Read-only access to a self-hosted Calibre-Web (or Calibre-Web Automated) ebook library via its OPDS feed: search, curated views and shelves, cover images and per-format download links. npx -y calibreweb-mcp
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/calibreweb-mcp.git`</sub>
- **[rekordcloud/sonovault-mcp](https://github.com/rekordcloud/sonovault-mcp)** — Music metadata search over 90M+ tracks, artists, labels, and releases: genre, release dates, ISRC/ISWC codes, and cross-platform IDs (Spotify, Apple Music, Tidal, Beatport, Discogs, MusicBrainz, YouTube). npx -y sonovault-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y sonovault-mcp`</sub>
- **[runcomfy-com/runcomfy-mcp](https://github.com/runcomfy-com/runcomfy-mcp)** — Official remote MCP server for RunComfy: ComfyUI serverless deployments, hosted model inference, and LoRA training jobs. 31 tools. Website: www.runcomfy.com. Remote server at https://mcp.runcomfy.com/mcp
  <sub>Python · MIT · source · pushed 2026-09-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/runcomfy-com/runcomfy-mcp.git`</sub>
- **[smeet666/mcp-lrclib](https://github.com/smeet666/mcp-lrclib)** — Search tracks on LRCLIB and read their lyrics, including time-synced (LRC) lines with a timestamp on every line. Strips lyrics from search results, cutting a search from ~29k to ~800 tokens. No API key. npx -y mcp-lrclib
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-lrclib.git`</sub>
- **[smeet666/mcp-imslp](https://github.com/smeet666/mcp-imslp)** — Read IMSLP, the Petrucci Music Library: search works and composers, read a work with its catalogue numbers, key and instrumentation, and page through its editions with the copyright status of each stated per jurisdiction. Downloads no score file. npx mcp-imslp
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-imslp.git`</sub>
- **[slshults/shakespeare-monologues-mcp](https://github.com/slshults/shakespeare-monologues-mcp)** — Search Shakespeare monologues by character, play, or first line; fetch full text, modern-English paraphrases, and scene/play summaries from shakespeare-monologues.org. Remote server at https://mcp.shakespeare-monologues.org/mcp
  <sub>TypeScript · MIT · npx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx shakespeare-monologues-mcp`</sub>
- **[smeet666/mcp-books](https://github.com/smeet666/mcp-books)** — Asks the Internet Archive, the Library of Congress and the Bibliothèque nationale de France at once, inside scanned text and across catalogues. Counts are never added and no source's absence is read as evidence about another. Install via npx mcp-books
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-books.git`</sub>
- **[speedwarnsf/scenef-mcp](https://github.com/speedwarnsf/scenef-mcp)** — Local stdio server (npx -y scenef-mcp) for movie showtimes across 33 regional boards in California and Hawaii — repertory houses, single-screen neighborhood theaters, 35mm and 70mm prints, and the chains — every showtime re-verified against the theater's own calendar, with a public accuracy record that includes the checks that failed. Nine read-only tools, no key
  <sub>JavaScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y github:speedwarnsf/scenef-mcp`</sub>
- **[TOBYCAI/image-mcp](https://github.com/TOBYCAI/image-mcp)** — Local Pillow-based image-processing MCP server: info / resize / crop / convert / compress / rotate / flip / thumbnail / watermark / effects / placeholder / overlay (12 tools). Offline, no API key. Install: pip install pillow &amp;&amp; python3 image_mcp.py
  <sub>Python · MIT · source · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TOBYCAI/image-mcp.git`</sub>
- **[vicseeai/vicsee-mcp-server](https://github.com/vicseeai/vicsee-mcp-server)** — Generate, edit, and upscale AI video &amp; images (Seedance, Veo, Kling, FLUX, Nano Banana) from any agent via VicSee
  <sub>TypeScript · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vicseeai/vicsee-mcp-server.git`</sub>
- **[XavierFabregat/spotify-mcp](https://github.com/XavierFabregat/spotify-mcp)** — Conversational Spotify control with intent-shaped tools: play by description, queue, devices, playlists, and library, plus a 2-minute PKCE setup wizard. Built for the post-Feb-2026 Spotify Web API. npx -y @xavifabregat/spotify-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @xavifabregat/spotify-mcp init`</sub>
- **[yonlandwu/chinese-almanac-mcp](https://github.com/yonlandwu/chinese-almanac-mcp)** — Chinese almanac (Tung Shing / 通勝) MCP server with NASA JPL solar-term precision: daily almanac readings, 12 hour-pillar luck ratings, solar terms, auspicious-date picking across 8 life activities (wedding, moving, grand opening...), zodiac horoscopes and personal lucky hours. Yi-Ji arbitration follows the 1739 imperial canon *Xie Ji Bian Fang Shu*. npx -y chinese-almanac-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install chinese-almanac-mcp --client claude`</sub>
- **[yuvalsuede/agent-media](https://github.com/yuvalsuede/agent-media)** — CLI and MCP server for AI video and image generation with unified access to 7 models (Kling, Veo, Sora, Seedance, Flux, Grok Imagine). Provides 9 tools for generating, managing, and browsing media
  <sub>unavailable</sub>
- **[smeet666/mcp-bideetmusique](https://github.com/smeet666/mcp-bideetmusique)** — Search the Bide &amp; Musique collection of forgotten French songs, catalogued by hand by the volunteer association that runs the station. Search along one axis at a time: performer, title, writer, a word of the lyrics, label or year. Read a record with its credits, its sleeve and its transcription, or draw a random one. No API key. npx -y mcp-bideetmusique
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-bideetmusique.git`</sub>

## Gaming

<sub>Entries 1–45 of 69. The rest are on this page's other parts, linked above and below.</sub>

- **[Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp)** — A MCP server for interacting with the Godot game engine, providing tools for editing, running, debugging, and managing scenes in Godot projects
  <sub>★ 5.8k · JavaScript · MIT · npx · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @coding-solo/godot-mcp`</sub>
- **[IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP)** — #️⃣ 🏠 🍎 🪟 🐧 - MCP Server for Unity Editor and for a game made with Unity
  <sub>★ 4.3k · C# · Apache-2.0 · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g unity-mcp-cli`</sub>
- **[CoderGamester/mcp-unity](https://github.com/CoderGamester/mcp-unity)** — #️⃣ 🏠 - MCP Server for Unity3d Game Engine integration for game development
  <sub>★ 1.9k · C# · MIT · source · pushed 2026-09-03 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CoderGamester/mcp-unity.git`</sub>
- **[youichi-uda/godot-mcp-pro](https://github.com/youichi-uda/godot-mcp-pro)** — Premium MCP server for Godot game engine with 84 tools for scene editing, scripting, animation, tilemap, shader, input simulation, and runtime debugging
  <sub>★ 603 · GDScript · source · pushed 2026-08-01</sub>
  <sub>`git clone https://github.com/youichi-uda/godot-mcp-pro.git`</sub>
- **[opgginc/opgg-mcp](https://github.com/opgginc/opgg-mcp)** — Access real-time gaming data across popular titles like League of Legends, TFT, and Valorant, offering champion analytics, esports schedules, meta compositions, and character statistics
  <sub>★ 101 · TypeScript · MIT · source · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/opgginc/opgg-mcp.git`</sub>
- **[pab1ito/chess-mcp](https://github.com/pab1it0/chess-mcp)** — Access Chess.com player data, game records, and other public information through standardized MCP interfaces, allowing AI assistants to search and analyze chess information
  <sub>★ 89 · Python · MIT · source · pushed 2026-06-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pab1it0/chess-mcp.git`</sub>
- **[rishijatia/fantasy-pl-mcp](https://github.com/rishijatia/fantasy-pl-mcp/)** — An MCP server for real-time Fantasy Premier League data and analysis tools
  <sub>★ 80 · Python · MIT · pip · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/rishijatia/fantasy-pl-mcp.git`</sub>
- **[Erodenn/godot-mcp-runtime](https://github.com/Erodenn/godot-mcp-runtime)** — MCP server for Godot 4.x with runtime control via injected UDP bridge: input simulation, screenshots, UI discovery, and live GDScript execution while the game is running
  <sub>★ 74 · TypeScript · MIT · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g godot-mcp-runtime`</sub>
- **[hope1026/weppy-roblox-mcp](https://github.com/hope1026/weppy-roblox-mcp)** — MCP server and plugin that lets AI agents (Claude Code, Cursor, Codex, Gemini) directly control a live Roblox Studio session — create scripts, instances, terrain, lighting, and assets via natural language. 21 tools, 140+ actions, bidirectional sync, and automated playtest
  <sub>★ 60 · PowerShell · AGPL-3.0 · psh · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/hope1026/weppy-roblox-mcp/main/install.ps1 | iex`</sub>
- **[kkjdaniel/bgg-mcp](https://github.com/kkjdaniel/bgg-mcp)** — An MCP server that enables interaction with board game related data via the BoardGameGeek API (XML API2)
  <sub>★ 53 · Go · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kkjdaniel/bgg-mcp.git`</sub>
- **[n24q02m/better-godot-mcp](https://github.com/n24q02m/better-godot-mcp)** — 18 composite tools for structured Godot 4.x interaction: scenes, nodes, GDScript, shaders, animation, tilemap, physics, audio, navigation, UI, input mapping, and signals
  <sub>★ 37 · TypeScript · Apache-2.0 · npx · pushed 2026-09-13 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y @n24q02m/better-godot-mcp@latest`</sub>
- **[german-krasnikov/unity-biome-mcp](https://github.com/german-krasnikov/unity-biome-mcp)** — #️⃣ 🏠 🍎 🪟 🐧 - Control the Unity Editor from 10 MCP clients or from chat inside Unity. 47 tools for scenes, GameObjects, components, Shader Graph, materials, animation, and UI. PlayTest DSL for deterministic scenario verification, batch operations with Undo rollback, token-efficient plain-text protocol, screenshots with visual diff. Cross-platform CI, 11,700+ tests, MIT
  <sub>★ 28 · C# · MIT · uv · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx --from git+https://github.com/german-krasnikov/unity-biome-mcp.git#subdirectory=server unity-biome-mcp doctor`</sub>
- **[kitao/pyxel-mcp](https://github.com/kitao/pyxel-mcp)** — MCP server for Pyxel retro game engine, enabling AI to run, capture screenshots, inspect sprites, and analyze audio of Pyxel games
  <sub>★ 27 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --refresh-package pyxel-mcp pyxel-mcp install`</sub>
- **[DiegoLopez0208/RpgMakerMVUltimate-MCP](https://github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP)** — AI copilot for RPG Maker MV: generate maps, edit the database and events, and reason about a project — validate broken references, explain why an event never fires, critique maps, and search by meaning. 13 tools, knowledge-driven map generation, fully offline
  <sub>★ 25 · TypeScript · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx degit DiegoLopez0208/RpgMakerMVUltimate-MCP/skill/rpgmaker-mv-mcp ~/.claude/skills/rpgmaker-mv-mcp`</sub>
- **[beckettlab/beckett-godot-mcp](https://github.com/beckettlab/beckett-godot-mcp)** — Beckett — MCP for Godot: a zero-sidecar GDScript editor addon that serves MCP over Streamable HTTP from inside the Godot 4 editor (no Node/Python sidecar). Reflection over any class, validate-before-write GDScript, scene/script/resource authoring, and a runtime play-test loop (play, screenshot, input, assert). MIT
  <sub>★ 23 · GDScript · MIT · source · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/beckettlab/beckett-godot-mcp.git`</sub>
- **[jiayao/mcp-chess](https://github.com/jiayao/mcp-chess)** — A MCP server playing chess against LLMs
  <sub>★ 23 · Python · Apache-2.0 · source · pushed 2025-05-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jiayao/mcp-chess.git`</sub>
- **[butterlatte-zhang/unity-ai-bridge](https://github.com/butterlatte-zhang/unity-ai-bridge)** — #️ 🐍 🏠 🍎 🪟 - Remote-control Unity Editor from any AI IDE via file-based IPC — 62 tools across 13 categories, zero dependencies, supports Claude Code, Cursor, Copilot, Windsurf, Claude Desktop
  <sub>★ 20 · C# · Apache-2.0 · source · pushed 2026-03-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/butterlatte-zhang/unity-ai-bridge.git`</sub>
- **[buildepicshit/Wick](https://github.com/buildepicshit/Wick)** — #️⃣ 🏠 🍎 🪟 🐧 - Native C# MCP server for Godot Engine — 53 tools across 5 pillars: Roslyn-enriched exception telemetry, scene tree inspection, C# symbol navigation, MSBuild orchestration, and GDScript analysis. .NET 10, TCP JSON-RPC bridge, 219 tests
  <sub>★ 20 · C# · MIT · clone · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/buildepicshit/Wick.git`</sub>
- **[sonirico/mcp-stockfish](https://github.com/sonirico/mcp-stockfish)** — MCP server connecting AI systems to Stockfish chess engine
  <sub>★ 15 · Go · MIT · clone · pushed 2025-06-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sonirico/mcp-stockfish`</sub>
- **[stefan-xyz/mcp-server-runescape](https://github.com/stjepko-xyz/mcp-server-runescape)** — An MCP server with tools for interacting with RuneScape (RS) and Old School RuneScape (OSRS) data, including item prices, player hiscores, and more
  <sub>★ 13 · JavaScript · Apache-2.0 · source · pushed 2026-02-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stefan-xyz/mcp-server-runescape.git`</sub>
- **[3aKHP/prts-mcp](https://github.com/3aKHP/prts-mcp)** — MCP Server for Arknights, querying the PRTS Wiki API and serving auto-synced operator archives and voice lines from game data. Designed for fan-creation (同人創作) AI agents. Python (stdio/Docker) and TypeScript (Streamable HTTP) implementations
  <sub>★ 10 · Python · MIT · npx · pushed 2026-09-18 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx prts-mcp-ts-stdio`</sub>
- **[gregario/warhammer-oracle](https://github.com/gregario/warhammer-oracle)** — Warhammer 40K, Combat Patrol, and Kill Team rules reference with unit datasheets, keyword definitions, phase sequences, and game flow. 6 tools, 3148 units embedded
  <sub>★ 10 · TypeScript · MIT · npm · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g warhammer-oracle`</sub>
- **[NAJEMWEHBE/unreal-ai-connection](https://github.com/NAJEMWEHBE/unreal-ai-connection)** — Drive the Unreal Engine 5.7 editor from any MCP client over a local TCP socket — 105 editor-automation tools (72 native C++ + 33 bridge-side). Native C++ plugin + thin Python bridge, ~50ms round-trips. 498 tests, MIT
  <sub>★ 9 · C++ · MIT · source · pushed 2026-07-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/NAJEMWEHBE/unreal-ai-connection.git`</sub>
- **[dmang-dev/mcp-ppsspp](https://github.com/dmang-dev/mcp-ppsspp)** — Drive PSP games through PPSSPP's built-in WebSocket debugger interface — no plugin needed. Memory r/w (u8/u16/u32/range/string), input (buttons + analog), pause/resume/step, screenshot, MIPS Allegrex registers, CPU execution breakpoints. The richest debugger surface in the family thanks to PPSSPP's native instrumentation
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-ppsspp`</sub>
- **[gregario/godot-forge](https://github.com/gregario/godot-forge)** — Godot 4 development companion with test running (GUT/GdUnit4), API docs with 3→4 migration mapping, script analysis, scene parsing, screenshots, and LSP diagnostics
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-04-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y godot-forge`</sub>
- **[gregario/dnd-oracle](https://github.com/gregario/dnd-oracle)** — D&amp;D 5e SRD reference and analysis with monster search, spell lookup, encounter building, and loadout analysis. 10 tools, 1198 entities embedded
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gregario/dnd-oracle.git`</sub>
- **[haoyifan/Silicon-Pantheon](https://github.com/haoyifan/Silicon-Pantheon)** — Turn-based strategy game where AI agents (Claude, GPT, Grok) are the players and humans coach from the sideline. Agents command armies on tactical grids, write post-match reflections, and learn across games. MCP-native client-server architecture with a hosted lobby and self-host option
  <sub>★ 6 · Python · Apache-2.0 · source · pushed 2026-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/haoyifan/Silicon-Pantheon.git`</sub>
- **[antics-gg/antics-mcp](https://github.com/antics-gg/antics-mcp)** — Deploy a single-file HTML game to a shareable multiplayer URL with rooms, state sync, and leaderboards. No backend or player accounts
  <sub>★ 5 · TypeScript · npx · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx antics-cli login`</sub>
- **[hkaanengin/opendota-mcp-server](https://github.com/hkaanengin/opendota-mcp-server)** — MCP server providing AI assistants with access to Dota 2 statistics via OpenDota API. 20+ tools for player stats, hero data, and match analysis with natural language support
  <sub>★ 5 · Python · clone · pushed 2026-01-28 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/hkaanengin/opendota-mcp-server.git`</sub>
- **[jkiley129/steam-mcp](https://github.com/jkiley129/steam-mcp)** — Connect Claude to your Steam library. Query your games, playtime, recently played, and store metadata via natural language
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx steam-mcp setup`</sub>
- **[lodordev/mcp-romm](https://github.com/lodordev/mcp-romm)** — MCP server for RomM retro game library manager. 19 read-only tools for browsing platforms, searching ROMs, viewing metadata, managing collections, tracking saves, firmware, devices, and task monitoring. OAuth2 auth with automatic token refresh
  <sub>★ 5 · Python · MIT · clone · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lodordev/mcp-romm.git`</sub>
- **[ddsky/gamebrain-api-clients](https://github.com/ddsky/gamebrain-api-clients)** — Search and discover hundreds of thousands of video games on any platform through the GameBrain API
  <sub>★ 4 · Java · Apache-2.0 · source · pushed 2025-12-01</sub>
  <sub>`git clone https://github.com/ddsky/gamebrain-api-clients.git`</sub>
- **[dmang-dev/mcp-bizhawk](https://github.com/dmang-dev/mcp-bizhawk)** — Drive the BizHawk multi-system emulator from any MCP client. Memory r/w across named domains, joypad input, frame-advance, screenshot, save/load state. One bridge unlocks NES, SNES, GB/GBC/GBA, Genesis, N64, PSX, Saturn, and more
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-bizhawk`</sub>
- **[dmang-dev/mcp-dolphin](https://github.com/dmang-dev/mcp-dolphin)** — Drive the Dolphin GameCube/Wii emulator from any MCP client: read/write PowerPC memory (MEM1/MEM2), GameCube + Wii Remote input (buttons, IR pointer, accelerometer, MotionPlus), reset, save/load state, and frame advance. Python bridge inside Felk's scripting fork + Node MCP server
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-dolphin --print-bridge > mcp_bridge.py`</sub>
- **[gregario/mtg-oracle](https://github.com/gregario/mtg-oracle)** — Magic: The Gathering card search, rules lookup, deck analysis, price data, and Commander intelligence. 14 tools, Scryfall + Academy Ruins + Commander Spellbook data
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-05-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mtg-oracle`</sub>
- **[Grinv/steam-games-mcp](https://github.com/Grinv/steam-games-mcp)** — Search Steam's store/catalog (deals, reviews, Steam Deck/SteamOS/Machine/Frame compatibility) with no API key, plus player profiles, libraries, achievements and friends via the official Steam Web API (free key)
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y steam-games-mcp`</sub>
- **[rkocosmergon/cosmergon-agent](https://github.com/rkocosmergon/cosmergon-agent)** — Living economy for AI agents — Conway's Game of Life physics, energy currency, marketplace. 4 tools: observe state, execute actions, benchmark reports, game rules. Auto-registers, no API key needed
  <sub>★ 4 · Python · MIT · pipx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install 'cosmergon-agent[dashboard]'`</sub>
- **[tomholford/mcp-tic-tac-toe](https://github.com/tomholford/mcp-tic-tac-toe)** — Play Tic Tac Toe against an AI opponent using this MCP server
  <sub>★ 4 · Go · clone · pushed 2025-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tomholford/mcp-tic-tac-toe`</sub>
- **[dmang-dev/mcp-retroarch](https://github.com/dmang-dev/mcp-retroarch)** — Drive any libretro core through RetroArch's Network Control Interface (UDP): read/write memory, save/load state, screenshot, pause/frame-advance/reset, on-screen messages. Verified against NES, SNES, Genesis, N64, GBA, and PS1 cores
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-retroarch`</sub>
- **[gregario/lorcana-oracle](https://github.com/gregario/lorcana-oracle)** — Disney Lorcana TCG card search, deck analysis, ink curves, lore generation, and franchise browsing. 7 tools, 2,710 cards embedded
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx lorcana-oracle`</sub>
- **[taygunsavas/patina-unity-mcp](https://github.com/taygunsavas/patina-unity-mcp)** — #️⃣ 🏠 🍎 🪟 🐧 - Control the Unity Editor from MCP hosts through a local Rust server and C# bridge, with one-click host setup and 86 Unity commands for scenes, GameObjects, prefabs, assets, scripts, console, tests, and build settings
  <sub>★ 3 · C# · MIT · source · pushed 2026-09-20 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/taygunsavas/patina-unity-mcp.git`</sub>
- **[alex-gon/thegamecrafter-mcp-server](https://github.com/alex-gon/thegamecrafter-mcp-server)** — Design, manage, and price tabletop games on The Game Crafter. Browse catalogs, create projects, upload artwork, get pricing
  <sub>★ 3 · TypeScript · MIT · clone · pushed 2026-04-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alex-gon/thegamecrafter-mcp-server.git`</sub>
- **[jhomen368/steam-reviews-mcp](https://github.com/jhomen368/steam-reviews-mcp)** — Search Steam games, fetch user reviews, and analyze sentiment with topic drill-down to make informed purchasing decisions
  <sub>★ 3 · TypeScript · MIT · clone · pushed 2026-09-14 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/jhomen368/steam-reviews-mcp.git`</sub>
- **[HadiCherkaoui/crafty-mcp](https://github.com/HadiCherkaoui/crafty-mcp)** — MCP server for managing Minecraft servers through Crafty Controller 4. Start, stop, backup, send commands, manage files, schedules, webhooks, and users via the Crafty API
  <sub>★ 3 · TypeScript · AGPL-3.0 · clone · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HadiCherkaoui/crafty-mcp.git`</sub>
- **[chaoz23/srdcheck](https://github.com/chaoz23/srdcheck)** — Deterministic D&amp;D 5e (SRD 5.2.1) rules verdicts for agents: cited legality checks for whole turns, legal-action enumeration, advantage math, and hash-stamped game-state lineage. Refuses what the rules don't decide (exit 2), quotes the rule text on every verdict, zero dependencies
  <sub>★ 2 · Python · source · pushed 2026-08-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/chaoz23/srdcheck.git`</sub>

Page **5** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · **5** · [6](mcp-servers-punkpeye-6.md) · [7](mcp-servers-punkpeye-7.md) — [continue on page 6 →](mcp-servers-punkpeye-6.md)

---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
