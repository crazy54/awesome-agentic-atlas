# MCP Servers

The Model Context Protocol ecosystem: reference and third-party servers, inspectors, gateways, transports, and the sibling agent-to-agent protocols.

**11 projects** · 11 with stars to rank by · 253,120 combined stars

[← every topic](README.md) · [← back to the mega list](../README.md) · [**filter this live →**](https://crazy54.github.io/awesome-agentic-atlas/#topic=mcp-servers)

|   |   |   |
|---|---|---|
| <a href="https://github.com/modelcontextprotocol/servers"><img src="https://opengraph.githubassets.com/1/modelcontextprotocol/servers" width="260"></a> | <a href="https://github.com/ChromeDevTools/chrome-devtools-mcp"><img src="https://opengraph.githubassets.com/1/ChromeDevTools/chrome-devtools-mcp" width="260"></a> | <a href="https://github.com/microsoft/playwright-mcp"><img src="https://opengraph.githubassets.com/1/microsoft/playwright-mcp" width="260"></a> |
| **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)**<br>★ 90k | **[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)**<br>★ 50.8k | **[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)**<br>★ 36.8k |
| <a href="https://github.com/a2aproject/A2A"><img src="https://img.youtube.com/vi/4gYm0Rp7VHc/maxresdefault.jpg" width="260"></a> | <a href="https://github.com/ag-ui-protocol/ag-ui"><img src="https://github.com/user-attachments/assets/00ec7366-713e-443f-a8f0-8db52ad28ef4" width="260"></a> | <a href="https://github.com/modelcontextprotocol/inspector"><img src="https://opengraph.githubassets.com/1/modelcontextprotocol/inspector" width="260"></a> |
| **[A2A Protocol](https://github.com/a2aproject/A2A)**<br>★ 25.6k | **[AG-UI](https://github.com/ag-ui-protocol/ag-ui)**<br>★ 15.7k | **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)**<br>★ 10.8k |

## Ranked by stars (11)

| # | Project | ★ | Lists | Plugs into | Runs on | Install / Run | What it does |
|--:|---|--:|--:|---|---|---|---|
| 1 | **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)**<br><sub>modelcontextprotocol/servers</sub> | 90k | 2 | <sub>Claude / Anthropic, MCP</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `npx -y @modelcontextprotocol/server-memory` | Anthropic's official reference MCP server implementations (GitHub, Slack, Postgres, Puppeteer, etc.). The authoritative source for understanding correct MCP server structure befor… |
| 2 | **[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)**<br><sub>ChromeDevTools/chrome-devtools-mcp</sub> | 50.8k | 1 | <sub>MCP, Gemini / Google</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `git clone https://github.com/ChromeDevTools/chrome-devtools-mcp.git` | Official Google MCP server that exposes live Chrome debugging surfaces — network analysis, performance profiling, console messages, memory snapshots, and Lighthouse audits — as st… |
| 3 | **[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)**<br><sub>microsoft/playwright-mcp</sub> | 36.8k | 2 | <sub>MCP</sub> | <sub>Win? · WSL2? · macOS? · Linux? · Docker</sub> | `npx @playwright/mcp@latest --config path/to/config.json` | Browser automation via accessibility tree snapshots rather than screenshots, dramatically reducing token cost. The canonical example of structured tool output design in an MCP ser… |
| 4 | **[A2A Protocol](https://github.com/a2aproject/A2A)**<br><sub>a2aproject/A2A</sub> | 25.6k | 2 | <sub>MCP, Gemini / Google</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `pip install a2a-sdk` | Google's open Agent-to-Agent protocol: JSON-RPC over HTTP(S)/SSE with Agent Card service discovery and a task/message/artifact communication model. The emerging standard for cross… |
| 5 | **[AG-UI](https://github.com/ag-ui-protocol/ag-ui)**<br><sub>ag-ui-protocol/ag-ui</sub> | 15.7k | 1 | <sub>MCP</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `npx create-ag-ui-app my-agent-app` | Lightweight event-driven protocol standardizing how AI agents connect to frontend applications: streaming state updates, tool call rendering, and HITL interrupts over a shared eve… |
| 6 | **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)**<br><sub>modelcontextprotocol/inspector</sub> | 10.8k | 1 | <sub>MCP</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `npx @modelcontextprotocol/inspector # web UI (default)` | Interactive debugging UI for MCP servers: inspect tool definitions, send test calls, and validate responses without wiring up a full agent. The essential development tool for anyo… |
| 7 | **[mcp-agent](https://github.com/lastmile-ai/mcp-agent)**<br><sub>lastmile-ai/mcp-agent</sub> | 8.5k | 1 | <sub>MCP</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `uvx mcp-agent init --template basic # Scaffold a new project` | Production-grade framework for building agents with MCP: composable workflows, built-in observability, and provider-agnostic model routing. The clearest reference for turning MCP… |
| 8 | **[oomol-lab/open-connector](https://github.com/oomol-lab/open-connector)**<br><sub>oomol-lab/open-connector</sub> | 5.5k | 1 | <sub>MCP</sub> | <sub>WSL2 · Linux · Docker</sub> | `git clone https://github.com/oomol-lab/open-connector.git` | Open-source auth gateway connecting 1000+ SaaS providers to AI agents through SDK, CLI, MCP, HTTP, and OpenAPI. Treats external-tool onboarding as a unified, self-hosted harness l… |
| 9 | **[agentgateway](https://github.com/agentgateway/agentgateway)**<br><sub>agentgateway/agentgateway</sub> | 4.7k | 1 | <sub>MCP</sub> | <sub>WSL2? · macOS · Linux</sub> | `git clone https://github.com/agentgateway/agentgateway.git` | Open-source agentic proxy that unifies LLM gateway, MCP gateway, and A2A gateway into a single control plane for managing multi-agent, multi-tool connectivity at scale. Provides d… |
| 10 | **[agent-device](https://github.com/callstack/agent-device)**<br><sub>callstack/agent-device</sub> | 4.3k | 1 | <sub>MCP</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `npm install -g agent-device@latest` | MCP-native control layer for iOS and Android devices: snapshots, semantic targeting, typed client access, diagnostics, and replayable workflows. Fills a critical gap in the mobile… |
| 11 | **[vurb.ts](https://github.com/vinkius-labs/mcpfusion)**<br><sub>vinkius-labs/mcpfusion</sub> | 256 | 1 | <sub>Claude / Anthropic, MCP, Codex / OpenAI</sub> | <sub>Win? · WSL2? · macOS? · Linux?</sub> | `git clone https://github.com/vinkius-labs/vurb.ts.git` | TypeScript framework for building production MCP servers with a "Presenter" perception layer that strips undeclared fields, redacts PII, and gates tool visibility by workflow stat… |


---

Snapshot 2026-09-03. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
