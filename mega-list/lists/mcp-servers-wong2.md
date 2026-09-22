# MCP Servers (wong2)

A curated list of Model Context Protocol (MCP) servers

Curated by **[wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

532 entries · 484 distinct repos · 5 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/zed-industries/zed"><img src="https://opengraph.githubassets.com/1/zed-industries/zed" width="260"></a> | <a href="https://github.com/upstash/context7"><img src="https://raw.githubusercontent.com/upstash/context7/master/public/cover.png?raw=true" width="260"></a> | <a href="https://github.com/microsoft/playwright-mcp"><img src="https://opengraph.githubassets.com/1/microsoft/playwright-mcp" width="260"></a> |
| **[Zed](https://github.com/zed-industries/zed)**<br>★ 90.7k | **[Context 7](https://github.com/upstash/context7)**<br>★ 62.3k | **[Playwright](https://github.com/microsoft/playwright-mcp)**<br>★ 37.5k |
| <a href="https://github.com/continuedev/continue"><img src="https://raw.githubusercontent.com/continuedev/continue/main/media/github-readme.png" width="260"></a> | <a href="https://github.com/github/github-mcp-server"><img src="https://opengraph.githubassets.com/1/github/github-mcp-server" width="260"></a> | <a href="https://github.com/ScrapeGraphAI/Scrapegraph-ai"><img src="https://raw.githubusercontent.com/ScrapeGraphAI/Scrapegraph-ai/main/docs/assets/nodemaven-banner.png" width="260"></a> |
| **[Continue](https://github.com/continuedev/continue)**<br>★ 36k | **[GitHub](https://github.com/github/github-mcp-server)**<br>★ 33.1k | **[ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai)**<br>★ 31.2k |

## Contents

- [Clients](#clients) (16)
- [Official Servers](#official-servers) (252)
- [Community Servers](#community-servers) (250)
- [Frameworks](#frameworks) (7)
- [Reference Servers](#reference-servers) (7)

## Clients

- **[Zed](https://github.com/zed-industries/zed)** — multiplayer code editor from the creators of atom
  <sub>★ 90.7k · Rust · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/zed-industries/zed.git`</sub>
- **[Continue](https://github.com/continuedev/continue)** — vscode auto complete and chat tool (full feature support)
  <sub>★ 36k · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/continuedev/continue.git`</sub>
- **[gpt-computer-assistant](https://github.com/Upsonic/Upsonic)** — dockerized mcp client with Anthropic, OpenAI and Langchain
  <sub>★ 8k · Python · MIT · source · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Upsonic/gpt-computer-assistant.git`</sub>
- **[genkit](https://github.com/genkit-ai/genkit)** — agent and data transformation framework
  <sub>★ 6.5k · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g genkit-cli`</sub>
- **[mcphub.nvim](https://github.com/ravitemer/mcphub.nvim)** — A Neovim plugin that provides a UI and api to interact with MCP servers
  <sub>★ 1.8k · Lua · MIT · source · pushed 2026-01-18</sub>
  <sub>`git clone https://github.com/ravitemer/mcphub.nvim.git`</sub>
- **[Nerve](https://github.com/evilsocket/nerve)** — is an open source command line tool designed to be a simple yet powerful platform for creating and executing MCP integrated LLM-based agents
  <sub>★ 1.3k · Python · pip · pushed 2025-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install nerve-adk`</sub>
- **[MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge)** — an openAI middleware proxy to use mcp in any existing openAI compatible client
  <sub>★ 930 · Python · MIT · source · pushed 2025-12-08 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/SecretiveShell/MCP-Bridge.git`</sub>
- **[mcp-cli](https://github.com/wong2/mcp-cli)** — a cli inspector for MCP servers
  <sub>★ 446 · JavaScript · GPL-3.0 · npx · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @wong2/mcp-cli`</sub>
- **[Shinkai](http://github.com/dcSpark/shinkai-apps/)** — is a two click install AI manager (Local and Remote) that allows you to create AI agents in 5 minutes or less using a simple UI. Agents and tools are exposed as an MCP Server
  <sub>★ 433 · TypeScript · Apache-2.0 · npx · pushed 2026-06-15 · macOS</sub>
  <sub>`npx nx serve:tauri shinkai-desktop`</sub>
- **[MCP-Chatbot](https://github.com/3choff/mcp-chatbot)** — A simple yet powerful ⭐ CLI chatbot that integrates tool servers with any OpenAI-compatible LLM API
  <sub>★ 251 · Python · MIT · clone · pushed 2024-12-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/3choff/mcp-chatbot.git`</sub>
- **[MCP-Connect](https://github.com/EvalsOne/MCP-connect)** — A client that enables cloud-based AI services to access local Stdio based MCP servers by HTTP/HTTPS requests
  <sub>★ 240 · Python · MIT · clone · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/EvalsOne/MCP-connect.git`</sub>
- **[codemirror-mcp](https://github.com/marimo-team/codemirror-mcp)** — CodeMirror extension that implements the Model Context Protocol (MCP) for resource mentions and prompt commands
  <sub>★ 79 · TypeScript · Apache-2.0 · source · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/marimo-team/codemirror-mcp.git`</sub>
- **[mcp-client](https://github.com/rakesh-eltropy/mcp-client)** — MCP REST API and CLI client for interacting with MCP servers, supports OpenAI, Claude, Gemini, Ollama etc
  <sub>★ 49 · Python · MIT · clone · pushed 2025-03-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rakesh-eltropy/mcp-client.git`</sub>
- **[MBro](https://github.com/sitbon/magg/blob/main/docs/mbro.md)** — A powerful interactive terminal MCP Browser client with tab completion and automatic documentation that allows you to work with multiple MCP servers, manage tools, and create complex workflows using AI assistants
  <sub>Python · AGPL-3.0 · in-repo · pushed 2026-08-02</sub>
  <sub>`git clone https://github.com/sitbon/magg.git && cd magg/docs/mbro.md`</sub>
- **[LibreChat](https://www.librechat.ai/)** — Open-source AI Web UI, supporting multiple providers including OpenAI, Anthropic, Google, Ollama, and local models. Includes MCP support for Agents
  <sub>website</sub>
  <sub>`https://www.librechat.ai/`</sub>
- **[mcps-playground](https://mcpsplayground.com/chat)** — a playground for Remote MCP servers
  <sub>website</sub>
  <sub>`https://mcpsplayground.com/chat`</sub>

## Official Servers

- **[Context 7](https://github.com/upstash/context7)** — Context7 MCP - Up-to-date Docs For Any Cursor Prompt
  <sub>★ 62.3k · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upstash/context7-mcp.git`</sub>
- **[Playwright](https://github.com/microsoft/playwright-mcp)** — Playwright MCP server
  <sub>★ 37.5k · TypeScript · Apache-2.0 · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @playwright/mcp@latest --config path/to/config.json`</sub>
- **[GitHub](https://github.com/github/github-mcp-server)** — GitHub's official MCP Server
  <sub>★ 33.1k · Go · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/github/github-mcp-server.git`</sub>
- **[MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox)** — Open source MCP server specializing in easy, fast, and secure tools for Databases
  <sub>★ 16.5k · Go · Apache-2.0 · npx · pushed 2026-09-22 · macOS</sub>
  <sub>`npx @toolbox-sdk/server --config tools.yaml`</sub>
- **[Apify](https://github.com/apify/apify-mcp-server)** — Actors MCP Server: Use 3,000+ pre-built cloud tools to extract data from websites, e-commerce, social media, search engines, maps, and more
  <sub>★ 8.1k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @apify/mcpc`</sub>
- **[Firecrawl](https://github.com/firecrawl/firecrawl-mcp-server)** — Extract web data with Firecrawl
  <sub>★ 7.5k · JavaScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g firecrawl-mcp`</sub>
- **[21st.dev Magic](https://github.com/21st-dev/magic-mcp)** — Create crafted UI components inspired by the best 21st.dev design engineers
  <sub>★ 5.9k · TypeScript · ISC · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @21st-dev/magic@latest API_KEY="..."`</sub>
- **[Exa](https://github.com/exa-labs/exa-mcp-server)** — Search Engine made for AIs by Exa
  <sub>★ 5k · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/exa-labs/exa-mcp-server.git`</sub>
- **[Notion](https://github.com/makenotion/notion-mcp-server)** — Notion official MCP server
  <sub>★ 4.6k · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @notionhq/notion-mcp-server`</sub>
- **[Chart](https://github.com/antvis/mcp-server-chart)** — A Model Context Protocol server for generating visual charts using AntV
  <sub>★ 4.4k · TypeScript · MIT · npm · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @antv/mcp-server-chart`</sub>
- **[Cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)** — Deploy, configure &amp; interrogate your resources on the Cloudflare developer platform (e.g. Workers/KV/R2/D1)
  <sub>★ 4.3k · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cloudflare/mcp-server-cloudflare.git`</sub>
- **[Grafana](https://github.com/grafana/mcp-grafana)** — Search dashboards, investigate incidents and query datasources in your Grafana instance
  <sub>★ 3.5k · Go · Apache-2.0 · uv · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx mcp-grafana`</sub>
- **[Browserbase](https://github.com/browserbase/mcp-server-browserbase)** — Automate browser interactions in the cloud (e.g. web navigation, data extraction, form filling, and more)
  <sub>★ 3.4k · TypeScript · Apache-2.0 · clone · pushed 2026-07-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/browserbase/mcp-server-browserbase.git`</sub>
- **[Supabase](https://github.com/supabase/mcp)** — Connects to Supabase platform for database, auth, edge functions and more
  <sub>★ 2.9k · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/supabase-community/supabase-mcp.git`</sub>
- **[Bright Data](https://github.com/brightdata/brightdata-mcp)** — Discover, extract, and interact with the web - one interface powering automated access across the public internet
  <sub>★ 2.7k · JavaScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @brightdata/mcp`</sub>
- **[Perplexity](https://github.com/perplexityai/modelcontextprotocol)** — An MCP server that connects to Perplexity's Sonar API, enabling real-time web-wide research in conversational AI
  <sub>★ 2.5k · TypeScript · MIT · docker · pushed 2026-08-27 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 -e PERPLEXITY_API_KEY=your_key_here perplexity-mcp-server`</sub>
- **[Tavily](https://github.com/tavily-ai/tavily-mcp)** — Search engine for AI agents (search + extract) powered by Tavily
  <sub>★ 2.4k · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y tavily-mcp@latest`</sub>
- **[Financial Datasets](https://github.com/financial-datasets/mcp-server)** — Stock market API made for AI agents
  <sub>★ 2.3k · Python · MIT · clone · pushed 2025-06-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/financial-datasets/mcp-server`</sub>
- **[Azure DevOps](https://github.com/microsoft/azure-devops-mcp)** — The MCP server for Azure DevOps, bringing the power of Azure DevOps directly to your agents
  <sub>★ 2k · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/azure-devops-mcp.git`</sub>
- **[Stripe](https://github.com/stripe/ai)** — Interact with Stripe API
  <sub>★ 1.8k · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://docs.stripe.com`</sub>
- **[ElevenLabs](https://github.com/elevenlabs/elevenlabs-mcp)** — The official ElevenLabs MCP server
  <sub>★ 1.5k · Python · MIT · pip · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install elevenlabs-mcp`</sub>
- **[Qdrant](https://github.com/qdrant/mcp-server-qdrant/)** — Implement semantic memory layer on top of the Qdrant vector search engine
  <sub>★ 1.5k · Python · Apache-2.0 · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @smithery/cli install mcp-server-qdrant --client claude`</sub>
- **[Ref](https://github.com/ref-tools/ref-tools-mcp)** — Up-to-date documentation for your coding agent. Covers 1000s of public repos and sites. Built by ref.tools
  <sub>★ 1.2k · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ref-tools/ref-tools-mcp.git`</sub>
- **[Neo4j](https://github.com/neo4j-contrib/mcp-neo4j/)** — Neo4j graph database server (schema + read/write-cypher) and separate graph database backed memory
  <sub>★ 984 · Python · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/neo4j-contrib/mcp-neo4j/.git`</sub>
- **[JetBrains](https://github.com/JetBrains/mcp-jetbrains)** — Work on your code with JetBrains IDEs
  <sub>★ 964 · JavaScript · Apache-2.0 · source · pushed 2026-01-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JetBrains/mcp-jetbrains.git`</sub>
- **[Octocode](https://github.com/bgauryy/octocode)** — Leading AI-powered code assistant for advanced research, analysis and discovery across GitHub Repositories in large ecosystems
  <sub>★ 943 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx octocode --help`</sub>
- **[ClickHouse](https://github.com/ClickHouse/mcp-clickhouse)** — Query your ClickHouse database server
  <sub>★ 877 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install 'mcp-clickhouse[chdb]'`</sub>
- **[Sentry](https://github.com/getsentry/sentry-mcp)** — Official MCP server for Sentry
  <sub>★ 858 · TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @sentry/mcp-server@latest --access-token=sentry-user-token`</sub>
- **[Hyperbrowser](https://github.com/hyperbrowserai/mcp)** — Hyperbrowser is the next-generation platform empowering AI agents and enabling effortless, scalable browser automation
  <sub>★ 791 · TypeScript · MIT · npx · pushed 2025-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx hyperbrowser-mcp <YOUR-HYPERBROWSER-API-KEY>`</sub>
- **[LINE Official Account](https://github.com/line/line-bot-mcp-server)** — Integrates the LINE Messaging API to connect an AI Agent to the LINE Official Account
  <sub>★ 782 · TypeScript · Apache-2.0 · clone · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone git@github.com:line/line-bot-mcp-server.git`</sub>
- **[Semgrep](https://github.com/semgrep/mcp)** — Enable AI agents to secure code with Semgrep
  <sub>★ 688 · Python · MIT · uv · pushed 2025-10-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx semgrep-mcp # see --help for more options`</sub>
- **[SonarQube](https://github.com/SonarSource/sonarqube-mcp-server)** — Provides seamless integration with SonarQube Server or Cloud, and enables analysis of code snippets directly within the agent context
  <sub>★ 655 · Java · docker · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --init --pull=always -i --rm -e SONARQUBE_TOKEN -e SONARQUBE_ORG sonarsource/sonarqube-mcp`</sub>
- **[Neon](https://github.com/neondatabase/mcp-server-neon)** — Interact with the Neon serverless Postgres platform
  <sub>★ 650 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx neon@latest init`</sub>
- **[Google Cloud Run](https://github.com/GoogleCloudPlatform/cloud-run-mcp)** — Official MCP Server to deploy to Google Cloud Run
  <sub>★ 632 · JavaScript · Apache-2.0 · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GoogleCloudPlatform/cloud-run-mcp.git`</sub>
- **[dbt](https://github.com/dbt-labs/dbt-mcp)** — Official MCP server for dbt (data build tool) providing integration with dbt Core/Cloud CLI, project metadata discovery, model information, and semantic layer querying capabilities
  <sub>★ 610 · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dbt-labs/dbt-mcp.git`</sub>
- **[Chroma](https://github.com/chroma-core/chroma-mcp)** — Embeddings, vector search, document storage, and full-text search with the open-source AI application database
  <sub>★ 597 · Python · Apache-2.0 · source · pushed 2025-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chroma-core/chroma-mcp.git`</sub>
- **[Kagi Search](https://github.com/kagisearch/kagimcp)** — Search the web using Kagi's search API
  <sub>★ 527 · Python · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install kagimcp --client claude`</sub>
- **[MotherDuck](https://github.com/motherduckdb/mcp-server-motherduck)** — Query and analyze data with MotherDuck and local DuckDB
  <sub>★ 523 · Python · MIT · docker · pushed 2026-09-19 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 8000:8000 mcp-server-motherduck`</sub>
- **[GitKraken](https://github.com/gitkraken/gk-cli)** — A CLI for interacting with GitKraken APIs. Includes an MCP server via gk mcp that not only wraps GitKraken APIs, but also Jira, GitHub, GitLab, and more
  <sub>★ 460 · winget · pushed 2026-09-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install gitkraken.cli`</sub>
- **[EdgeOne Pages MCP](https://github.com/TencentEdgeOne/edgeone-makers-mcp)** — An MCP service for deploying HTML content to EdgeOne Pages and obtaining a publicly accessible URL
  <sub>★ 435 · TypeScript · MIT · source · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TencentEdgeOne/edgeone-pages-mcp.git`</sub>
- **[E2B](https://github.com/e2b-dev/mcp-server)** — Run code in secure sandboxes hosted by E2B
  <sub>★ 395 · JavaScript · Apache-2.0 · npx · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @smithery/cli install e2b --client claude`</sub>
- **[Graphlit](https://github.com/graphlit/graphlit-mcp-server)** — Ingest anything from Slack to Gmail to podcast feeds, in addition to web crawling, into a searchable Graphlit project
  <sub>★ 381 · TypeScript · MIT · npx · pushed 2026-01-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y graphlit-mcp-server`</sub>
- **[Xero](https://github.com/XeroAPI/xero-mcp-server)** — Interact with the accounting data in your business using our official MCP server
  <sub>★ 369 · TypeScript · MIT · source · pushed 2026-06-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/XeroAPI/xero-mcp-server.git`</sub>
- **[Mapbox](https://github.com/mapbox/mcp-server)** — Unlock geospatial intelligence through Mapbox APIs like geocoding, POI search, directions, isochrones and more
  <sub>★ 356 · TypeScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector docker run -i --rm --env MAPBOX_ACCESS_TOKEN="YOUR_TOKEN" mapbox-mcp-server`</sub>
- **[Apache Doris](https://github.com/apache/doris-mcp-server)** — MCP Server For Apache Doris, an MPP-based real-time data warehouse
  <sub>★ 348 · Python · Apache-2.0 · pip · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install doris-mcp-server==1.0.0`</sub>
- **[Plane](https://github.com/makeplane/plane-mcp-server)** — The official Plane MCP server provides integration with Plane APIs, enabling full AI automation of Plane projects, work items, cycles and more
  <sub>★ 325 · Python · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/makeplane/plane-mcp-server`</sub>
- **[Postman](https://github.com/postmanlabs/postman-mcp-server)** — Postman’s remote MCP server connects AI agents, assistants, and chatbots directly to your APIs on Postman
  <sub>★ 317 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @postman/postman-mcp-server`</sub>
- **[ECharts](https://github.com/hustcc/mcp-echarts)** — Generate visual charts using ECharts with AI MCP dynamically, used for chart generation and data analysis
  <sub>★ 270 · TypeScript · MIT · npm · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-echarts`</sub>
- **[Milvus](https://github.com/zilliztech/mcp-server-milvus)** — Search, Query and interact with data in your Milvus Vector Database
  <sub>★ 245 · Python · Apache-2.0 · clone · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zilliztech/mcp-server-milvus.git`</sub>
- **[Comet Opik](https://github.com/comet-ml/opik-mcp)** — Query and analyze your Opik logs, traces, prompts and all other telemtry data from your LLMs in natural language
  <sub>★ 221 · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx add-mcp https://www.comet.com/opik/api/v1/mcp --name opik-mcp`</sub>
- **[Meilisearch](https://github.com/meilisearch/meilisearch-mcp)** — Interact &amp; query with Meilisearch (Full-text &amp; semantic search API)
  <sub>★ 197 · Python · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector python -m src.meilisearch_mcp`</sub>
- **[PayPal](https://github.com/paypal/agent-toolkit)** — The PayPal Model Context Protocol server allows you to integrate with PayPal APIs through function calling. This protocol supports various tools to interact with different PayPal services
  <sub>★ 193 · TypeScript · Apache-2.0 · source · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/paypal/agent-toolkit.git`</sub>
- **[StarRocks](https://github.com/StarRocks/mcp-server-starrocks)** — Interact with StarRocks
  <sub>★ 188 · Python · Apache-2.0 · clone · pushed 2026-09-08 · macOS</sub>
  <sub>`git clone https://github.com/starrocks/mcp-server-starrocks.git`</sub>
- **[AgentQL](https://github.com/tinyfish-io/agentql-mcp)** — Enable AI agents to get structured data from unstructured web with AgentQL
  <sub>★ 180 · TypeScript · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentql-mcp`</sub>
- **[Armor Crypto MCP](https://github.com/armorwallet/armor-crypto-mcp)** — MCP to interface with multiple blockchains, staking, DeFi, swap, bridging, wallet management, DCA, Limit Orders, Coin Lookup, Tracking and more
  <sub>★ 179 · Python · GPL-3.0 · source · pushed 2025-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/armorwallet/armor-crypto-mcp.git`</sub>
- **[Search1API](https://github.com/superagents-lab/search1api-mcp)** — One API for Search, Crawling, and Sitemaps
  <sub>★ 173 · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g search1api-cli`</sub>
- **[Langfuse Prompt Management](https://github.com/langfuse/mcp-server-langfuse)** — Open-source tool for collaborative editing, versioning, evaluating, and releasing prompts
  <sub>★ 172 · TypeScript · MIT · source · pushed 2025-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langfuse/mcp-server-langfuse.git`</sub>
- **[Make](https://github.com/integromat/make-mcp-server)** — Turn your Make scenarios into callable tools for AI assistants
  <sub>★ 172 · TypeScript · MIT · source · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/integromat/make-mcp-server.git`</sub>
- **[AlibabaCloud DevOps MCP](https://github.com/aliyun/alibabacloud-devops-mcp-server)** — Yunxiao MCP Server provides AI assistants with the ability to interact with the Yunxiao platform
  <sub>★ 171 · TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y alibabacloud-devops-mcp-server --toolsets=code-management,project-management`</sub>
- **[Scrapeless](https://github.com/scrapeless-ai/scrapeless-mcp-server)** — Integrate real-time Scrapeless Google SERP(Google Search, Google Flight, Google Map, Google Jobs....) results into your LLM applications. This server enables dynamic context retrieval for AI workflows, chatbots, and research tools
  <sub>★ 169 · TypeScript · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scrapeless-ai/scrapeless-mcp-server.git`</sub>
- **[Taskade](https://github.com/taskade/mcp)** — Connect to the Taskade platform via MCP. Access tasks, projects, workflows, and AI agents in real-time through a unified workspace and API
  <sub>★ 164 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @taskade/mcp-server`</sub>
- **[Logfire](https://github.com/pydantic/logfire-mcp)** — Provides access to OpenTelemetry traces and metrics through Logfire
  <sub>★ 160 · Python · MIT · source · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pydantic/logfire-mcp.git`</sub>
- **[Hostinger](https://github.com/hostinger/api-mcp-server)** — Official Hostinger API MCP server for services managment
  <sub>★ 155 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @hostinger/mcp`</sub>
- **[BrowserStack](https://github.com/browserstack/mcp-server)** — Bring the full power of BrowserStack’s Test Platform to your AI tools, making testing faster and easier for every developer and tester on your team
  <sub>★ 151 · TypeScript · AGPL-3.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browserstack/mcp-server.git`</sub>
- **[Octagon](https://github.com/OctagonAI/octagon-mcp-server)** — Deliver real-time investment research with extensive private and public market data
  <sub>★ 148 · TypeScript · MIT · npm · pushed 2026-07-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g octagon-mcp`</sub>
- **[Webflow](https://github.com/webflow/mcp-server)** — Interact with Webflow APIs to list and edit your site and CMS data
  <sub>★ 141 · TypeScript · MIT · npx · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y webflow-mcp-server@latest`</sub>
- **[FHIR](https://github.com/wso2/fhir-mcp-server/)** — Model Context Protocol server for Fast Healthcare Interoperability Resources (FHIR) APIs, enabling seamless integration with healthcare data through SMART-on-FHIR authentication and comprehensive FHIR operations
  <sub>★ 137 · Python · Apache-2.0 · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx fhir-mcp-server`</sub>
- **[AgentRPC](https://github.com/agentrpc/agentrpc)** — Connect to any function, any language, across network boundaries using AgentRPC
  <sub>★ 135 · TypeScript · Apache-2.0 · source · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentrpc/agentrpc.git`</sub>
- **[Plugged.in](https://github.com/VeriTeknik/pluggedin-mcp-proxy)** — A comprehensive proxy that combines multiple MCP servers into a single MCP. It provides discovery and management of tools, prompts, resources, and templates across servers, plus a playground for debugging when building MCP servers
  <sub>★ 135 · TypeScript · Apache-2.0 · npx · pushed 2026-05-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @pluggedin/pluggedin-mcp-proxy@latest --pluggedin-api-key YOUR_API_KEY`</sub>
- **[Dart](https://github.com/its-dart/dart-mcp-server)** — Interact with task, doc, and project data in Dart, an AI-native project management tool
  <sub>★ 128 · TypeScript · MIT · source · pushed 2026-09-09 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/its-dart/dart-mcp-server.git`</sub>
- **[Mureka](https://github.com/SkyworkAI/Mureka-mcp)** — generate lyrics, song and background music(instrumental)
  <sub>★ 116 · Python · MIT · source · pushed 2025-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SkyworkAI/Mureka-mcp.git`</sub>
- **[Chronulus AI](https://github.com/ChronulusAI/chronulus-mcp)** — Predict anything with Chronulus AI forecasting and prediction agents
  <sub>★ 112 · Python · MIT · pip · pushed 2025-07-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install chronulus-mcp`</sub>
- **[DINO-X](https://github.com/IDEA-Research/DINO-X-MCP)** — Advanced computer vision and object detection MCP server powered by Dino-X, enabling AI agents to analyze images, detect objects, identify keypoints, and perform visual understanding tasks
  <sub>★ 112 · TypeScript · Apache-2.0 · clone · pushed 2026-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/IDEA-Research/DINO-X-MCP.git`</sub>
- **[Twilio](https://github.com/twilio-labs/mcp)** — Interact with Twilio APIs to send messages, manage phone numbers, configure your account, and more
  <sub>★ 111 · TypeScript · MIT · source · pushed 2026-02-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/twilio-labs/mcp.git`</sub>
- **[Vectorize](https://github.com/vectorize-io/vectorize-mcp-server/)** — Vectorize MCP server for advanced retrieval, Private Deep Research, Anything-to-Markdown file extraction and text chunking
  <sub>★ 110 · TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @vectorize-io/vectorize-mcp-server@latest`</sub>
- **[OceanBase](https://github.com/oceanbase/awesome-oceanbase-mcp)** — MCP Server for OceanBase database and its tools
  <sub>★ 109 · Python · Apache-2.0 · source · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/oceanbase/mcp-oceanbase.git`</sub>
- **[Square](https://github.com/square/square-mcp-server)** — A Model Context Protocol (MCP) server for square
  <sub>★ 108 · TypeScript · Apache-2.0 · npx · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx square-mcp-server start`</sub>
- **[Oxylabs](https://github.com/oxylabs/oxylabs-mcp)** — Scrape websites with Oxylabs Web API, supporting dynamic rendering and parsing for structured data extraction
  <sub>★ 106 · Python · MIT · source · pushed 2026-09-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/oxylabs/oxylabs-mcp.git`</sub>
- **[Needle](https://github.com/needle-ai/needle-mcp)** — Production-ready RAG out of the box to search and retrieve data from your own documents
  <sub>★ 103 · Python · MIT · npx · pushed 2025-07-27 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install needle-mcp --client claude`</sub>
- **[Harness](https://github.com/harness/mcp-server)** — Access and interact with Harness platform data, including pipelines, repositories, logs, and artifact registries
  <sub>★ 102 · TypeScript · MIT · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g harness-mcp-v2`</sub>
- **[Box](https://github.com/box-community/mcp-server-box)** — Interact with the Intelligent Content Management platform through Box AI
  <sub>★ 101 · Python · MIT · clone · pushed 2026-04-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/box-community/mcp-server-box.git`</sub>
- **[OP.GG](https://github.com/opgginc/opgg-mcp)** — Access real-time gaming data across popular titles like League of Legends, TFT, and Valorant, offering champion analytics, esports schedules, meta compositions, and character statistics
  <sub>★ 101 · TypeScript · MIT · source · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/opgginc/opgg-mcp.git`</sub>
- **[ThingsBoard](https://github.com/thingsboard/thingsboard-mcp)** — The ThingsBoard MCP Server provides a natural language interface for LLMs and AI agents to interact with your ThingsBoard IoT platform
  <sub>★ 98 · Java · Apache-2.0 · clone · pushed 2026-03-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/thingsboard/mcp-server.git`</sub>
- **[CircleCI](https://github.com/CircleCI-Public/mcp-server-circleci)** — Enable AI Agents to fix build failures from CircleCI
  <sub>★ 94 · TypeScript · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install @CircleCI-Public/mcp-server-circleci --client claude`</sub>
- **[DeepResearch](https://github.com/OctagonAI/octagon-deep-research-mcp)** — Lightning-Fast, High-Accuracy Deep Research Agent 👉 8–10x faster 👉 Greater depth &amp; accuracy 👉 Unlimited parallel runs
  <sub>★ 94 · JavaScript · MIT · npm · pushed 2026-02-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g octagon-deep-research-mcp`</sub>
- **[Keboola](https://github.com/keboola/mcp-server)** — Build robust data workflows, integrations, and analytics on a single intuitive platform
  <sub>★ 86 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`uvx keboola_mcp_server login --api-url https://connection.YOUR_REGION.keboola.com`</sub>
- **[Tinybird](https://github.com/tinybirdco/mcp-tinybird)** — Interact with Tinybird serverless ClickHouse platform
  <sub>★ 79 · Python · Apache-2.0 · source · pushed 2025-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tinybirdco/mcp-tinybird.git`</sub>
- **[Twelve Data](https://github.com/twelvedata/mcp)** — Interact with Twelve Data APIs to access real-time and historical financial market data for your AI agents
  <sub>★ 77 · Python · source · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/twelvedata/mcp.git`</sub>
- **[Debugg AI](https://github.com/debugg-ai/debugg-ai-mcp)** — Enable your code gen agents to create &amp; run 0-config end-to-end tests against new code changes in remote browsers via the Debugg AI testing platform
  <sub>★ 68 · TypeScript · Apache-2.0 · docker · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm --init -e DEBUGGAI_API_KEY=your_api_key quinnosha/debugg-ai-mcp`</sub>
- **[Linked API](https://github.com/Linked-API/linkedapi-mcp.git)** — MCP server that lets AI assistants control LinkedIn accounts and retrieve real-time data with Linked API
  <sub>★ 68 · TypeScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Linked-API/linkedapi-mcp.git.git`</sub>
- **[Alby Bitcoin Payments MCP](https://github.com/getAlby/mcp/)** — Connect any bitcoin lightning wallet to agents to send and receive payments instantly at low cost
  <sub>★ 66 · TypeScript · Apache-2.0 · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @getalby/mcp`</sub>
- **[Gitee](https://github.com/oschina/mcp-gitee)** — Gitee API integration, repository, issue, and pull request management, and more
  <sub>★ 65 · Go · MIT · go · pushed 2026-09-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install gitee.com/oschina/mcp-gitee@latest`</sub>
- **[Mailtrap](https://github.com/mailtrap/mailtrap-mcp)** — Integrates with Mailtrap Email API
  <sub>★ 65 · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @smithery/cli install mailtrap`</sub>
- **[Supadata](https://github.com/supadata-ai/mcp)** — Official MCP server for Supadata - YouTube, TikTok, X and Web data for makers
  <sub>★ 64 · TypeScript · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/supadata-ai/mcp.git`</sub>
- **[Globalping](https://github.com/jsdelivr/globalping-mcp-server)** — Network access with the ability to run commands like ping, traceroute, mtr, http, dns resolve
  <sub>★ 63 · TypeScript · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-remote https://mcp.globalping.dev/sse`</sub>
- **[Rember](https://github.com/rember/rember-mcp)** — Create spaced repetition flashcards in Rember to remember anything you learn in your chats
  <sub>★ 63 · TypeScript · MIT · npx · pushed 2025-03-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @getrember/mcp --api-key=YOUR_REMBER_API_KEY`</sub>
- **[Last9](https://github.com/last9/last9-mcp-server)** — Seamlessly bring real-time production context—logs, metrics, and traces—into your local environment to auto-fix code faster
  <sub>★ 62 · Go · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @last9/mcp-server@latest`</sub>
- **[Mailgun](https://github.com/mailgun/mailgun-mcp-server)** — Interact with Mailgun API
  <sub>★ 62 · TypeScript · Apache-2.0 · clone · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mailgun/mailgun-mcp-server.git`</sub>
- **[ScreenshotMCP](https://github.com/upnorthmedia/ScreenshotMCP/)** — Capture website screenshots including full page, elements, and device specific sizes
  <sub>★ 61 · JavaScript · MIT · source · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upnorthmedia/ScreenshotMCP/.git`</sub>
- **[Axiom](https://github.com/axiomhq/mcp-server-axiom)** — Query and analyze your Axiom logs, traces, and all other event data in natural language
  <sub>★ 60 · Go · MIT · go · pushed 2025-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/axiomhq/axiom-mcp@latest`</sub>
- **[Trade Agent](https://github.com/trade-it-inc/trade-it-mcp)** — Execute stock and crypto trades via Trade Agent
  <sub>★ 59 · CC0-1.0 · source · pushed 2026-03-26</sub>
  <sub>`git clone https://github.com/Trade-Agent/trade-agent-mcp.git`</sub>
- **[Crawlbase MCP](https://github.com/crawlbase/crawlbase-mcp)** — Enables AI agents to access real-time web data with HTML, markdown, and screenshot support. SDKs: Node.js, Python, Java, PHP, .NET
  <sub>★ 58 · JavaScript · clone · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/crawlbase/crawlbase-mcp.git`</sub>
- **[Norman Finance](https://github.com/norman-finance/norman-mcp-server)** — MCP server for managing accounting and taxes with Norman Finance
  <sub>★ 58 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install norman-mcp-server`</sub>
- **[Teradata](https://github.com/Teradata/teradata-mcp-server)** — A collection of tools for managing the platform, addressing data quality and reading and writing to Teradata Database
  <sub>★ 57 · Python · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Teradata/teradata-mcp-server.git`</sub>
- **[Buildkite](https://github.com/buildkite/buildkite-mcp-server)** — Manage Buildkite pipelines and builds
  <sub>★ 54 · Go · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/buildkite/buildkite-mcp-server.git`</sub>
- **[1mcpserver](https://github.com/particlefuture/1mcpserver)** — MCP of MCPs. Automatic discovery and configure MCP servers on your local machine. Fully REMOTE! Just use https://mcp.1mcpserver.com/mcp/
  <sub>★ 52 · Python · Apache-2.0 · npx · pushed 2025-12-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @1mcpserver/1mcpserver`</sub>
- **[gotoHuman](https://github.com/gotohuman/gotohuman-mcp-server)** — Human-in-the-loop platform - Allow AI agents and automations to send requests for approval to your gotoHuman inbox
  <sub>★ 52 · JavaScript · MIT · npx · pushed 2026-06-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @gotohuman/mcp-server`</sub>
- **[XRAY](https://github.com/srijanshukla18/xray)** — Progressive code-intelligence server: lets AI assistants map structure, fuzzy-find symbols, and assess change-impact across Python, JS/TS, and Go codebases (powered by ast-grep)
  <sub>★ 52 · Python · MIT · uv · pushed 2025-12-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from . xray-mcp`</sub>
- **[DataWorks](https://github.com/aliyun/alibabacloud-dataworks-mcp-server)** — A Model Context Protocol (MCP) server that provides tools for AI, allowing it to interact with the DataWorks Open API through a standardized interface. This implementation is based on the Aliyun Open API and enables AI agents to perform cloud resources operations seamlessly
  <sub>★ 51 · TypeScript · Apache-2.0 · npm · pushed 2026-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g alibabacloud-dataworks-mcp-server`</sub>
- **[Metoro](https://github.com/metoro-io/metoro-mcp-server)** — Query and interact with kubernetes environments monitored by Metoro
  <sub>★ 51 · Go · MIT · clone · pushed 2026-06-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/metoro-io/metoro-mcp-server.git`</sub>
- **[Prisma Postgres](https://github.com/prisma/mcp)** — Gives LLMs the ability to manage Prisma Postgres databases (e.g. spin up new databases and run migrations or queries)
  <sub>★ 49 · JavaScript · npx · pushed 2025-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-remote https://mcp.prisma.io/mcp`</sub>
- **[VeyraX](https://github.com/VeyraX/veyrax-mcp)** — Single tool to control all 100+ API integrations, and UI components
  <sub>★ 49 · TypeScript · source · pushed 2025-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/VeyraX/veyrax-mcp.git`</sub>
- **[ZenML](https://github.com/zenml-io/mcp-zenml)** — Interact with your MLOps and LLMOps pipelines through your ZenML MCP server
  <sub>★ 49 · Python · MIT · docker · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run --rm -d --name mcp-zenml-apps -p 127.0.0.1:8001:8001 \`</sub>
- **[YepCode](https://github.com/yepcode/mcp-server-js)** — Execute any LLM-generated code in the YepCode secure and scalable sandbox environment and create your own MCP tools using JavaScript or Python, with full support for NPM and PyPI packages
  <sub>★ 46 · TypeScript · MIT · source · pushed 2026-03-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/yepcode/mcp-server-js.git`</sub>
- **[Unstructured](https://github.com/Unstructured-IO/UNS-MCP)** — Set up and interact with your unstructured data processing workflows in Unstructured Platform
  <sub>★ 43 · Jupyter Notebook · source · pushed 2026-07-21</sub>
  <sub>`git clone https://github.com/Unstructured-IO/UNS-MCP.git`</sub>
- **[WebScraping.AI](https://github.com/webscraping-ai/webscraping-ai-mcp-server)** — Interact with WebScraping.AI for web data extraction and scraping
  <sub>★ 43 · JavaScript · clone · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/webscraping-ai/webscraping-ai-mcp-server.git`</sub>
- **[DexPaprika](https://github.com/coinpaprika/dexpaprika-mcp)** — Access real-time DEX analytics across 20+ blockchains with DexPaprika API, tracking 5M+ tokens, pools, volumes, and historical market data. Built by CoinPaprika
  <sub>★ 42 · JavaScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g dexpaprika-mcp`</sub>
- **[Powertool](https://github.com/aws-powertools/powertools-mcp)** — An MCP implementation that provides search functionality for the Powertools for AWS Lambda documentation across multiple runtimes
  <sub>★ 42 · TypeScript · source · pushed 2026-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aws-powertools/powertools-mcp.git`</sub>
- **[eSignatures](https://github.com/esignaturescom/mcp-server-esignatures)** — Contract and template management for drafting, reviewing, and sending binding contracts
  <sub>★ 40 · Python · MIT · source · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/esignaturescom/mcp-server-esignatures.git`</sub>
- **[Integration App](https://github.com/membranehq/mcp-server)** — Interact with any other SaaS applications on behalf of your customers
  <sub>★ 38 · TypeScript · ISC · docker · pushed 2026-03-04 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 membrane-mcp-server`</sub>
- **[Tencent Cloud COS MCP](https://github.com/Tencent/cos-mcp)** — Quickly integrate with Tencent Cloud Storage (COS) and Data Processing (CI) capabilities powered
  <sub>★ 38 · TypeScript · npm · pushed 2025-11-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cos-mcp@latest`</sub>
- **[Decodo](https://github.com/Decodo/mcp-server)** — Easy web data access. Simplified retrieval of information from websites and online sources
  <sub>★ 37 · TypeScript · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Decodo/mcp-server`</sub>
- **[Couchbase](https://github.com/couchbase/mcp-server-couchbase)** — Interact with the data stored in Couchbase clusters using natural language
  <sub>★ 36 · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx couchbase-mcp-server --disabled-tools upsert_document_by_id, delete_document_by_id`</sub>
- **[Hologres](https://github.com/aliyun/alibabacloud-hologres-mcp-server)** — Connect to a Hologres instance, get table metadata, query and analyze data
  <sub>★ 36 · Python · Apache-2.0 · uv · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx hologres-mcp-server --transport streamable-http --host 0.0.0.0 --port 8000`</sub>
- **[ScreenshotOne](https://github.com/screenshotone/mcp/)** — Render website screenshots with ScreenshotOne
  <sub>★ 36 · TypeScript · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/screenshotone/mcp/.git`</sub>
- **[Ramp](https://github.com/ramp-public/ramp_mcp)** — Interact with Ramp's Developer API to run analysis on your spend and gain insights leveraging LLMs
  <sub>★ 34 · Python · MIT · clone · pushed 2025-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:ramp/ramp-mcp.git`</sub>
- **[SingleStore](https://github.com/singlestore-labs/mcp-server-singlestore)** — Interact with the SingleStore database platform
  <sub>★ 34 · Python · MIT · uv · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx singlestore-mcp-server init --client=claude-desktop`</sub>
- **[FlyonUI](https://github.com/themeselection/flyonui-mcp)** — Build modern, production-ready UI blocks, components, and landing pages in minutes
  <sub>★ 32 · JavaScript · source · pushed 2025-11-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/themeselection/flyonui-mcp.git`</sub>
- **[Fireproof](https://github.com/fireproof-storage/mcp-database-server)** — Immutable ledger database with live synchronization
  <sub>★ 31 · JavaScript · source · pushed 2024-12-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fireproof-storage/mcp-database-server.git`</sub>
- **[Fibery](https://github.com/Fibery-inc/fibery-mcp-server)** — Perform queries and entity operations in your Fibery workspace
  <sub>★ 29 · Python · MIT · npx · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @Fibery-inc/fibery-mcp-server --client claude`</sub>
- **[GreptimeDB](https://github.com/GreptimeTeam/greptimedb-mcp-server)** — Provides AI assistants with a secure and structured way to explore and analyze data in GreptimeDB
  <sub>★ 29 · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory . run -m greptimedb_mcp_server.server`</sub>
- **[Aiven](https://github.com/Aiven-Open/mcp-aiven)** — Navigate your Aiven projects and interact with the PostgreSQL®, Apache Kafka®, ClickHouse® and OpenSearch® services
  <sub>★ 28 · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Aiven-Open/mcp-aiven.git`</sub>
- **[EduBase](https://github.com/EduBase/MCP)** — Interact with EduBase, a comprehensive e-learning platform with advanced quizzing, exam management, and content organization capabilities
  <sub>★ 28 · TypeScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @EduBase/MCP --client claude`</sub>
- **[Inspektor Gadget MCP server](https://github.com/inspektor-gadget/ig-mcp-server)** — Debug your Container and Kubernetes workloads with an AI interface powered by eBPF
  <sub>★ 27 · Go · Apache-2.0 · source · pushed 2026-08-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/inspektor-gadget/ig-mcp-server.git`</sub>
- **[Inkeep](https://github.com/inkeep/mcp-server-python)** — RAG Search over your content powered by Inkeep
  <sub>★ 25 · Python · MIT · clone · pushed 2025-04-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/inkeep/mcp-server-python.git`</sub>
- **[GrowthBook](https://github.com/growthbook/growthbook-mcp)** — Create and read feature flags, review experiments, generate flag types, search docs, and interact with GrowthBook's feature flagging and experimentation platform
  <sub>★ 24 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @growthbook/mcp`</sub>
- **[QA Sphere](https://github.com/Hypersequent/qasphere-mcp)** — Integration with QA Sphere test management system, enabling LLMs to discover, summarize, and interact with test cases directly from AI-powered IDEs
  <sub>★ 23 · TypeScript · MIT · npx · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y qasphere-mcp`</sub>
- **[GoLogin MCP server](https://github.com/gologinapp/gologin-mcp)** — Manage your GoLogin browser profiles and automation directly through AI conversations!
  <sub>★ 22 · TypeScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y gologin-mcp`</sub>
- **[Raygun](https://github.com/MindscapeHQ/mcp-server-raygun)** — Interact with your crash reporting and real using monitoring data on your Raygun account
  <sub>★ 22 · source · pushed 2026-09-02</sub>
  <sub>`git clone https://github.com/MindscapeHQ/mcp-server-raygun.git`</sub>
- **[Fewsats](https://github.com/Fewsats/fewsats-mcp)** — Enable AI Agents to purchase anything in a secure way using Fewsats
  <sub>★ 21 · Python · uv · pushed 2025-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx fewsats-mcp`</sub>
- **[Currents](https://github.com/currents-dev/currents-mcp)** — Enable AI Agents to fix Playwright test failures reported to Currents
  <sub>★ 20 · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/currents-dev/currents-mcp.git`</sub>
- **[Audiense Insights](https://github.com/AudienseCo/mcp-audiense-insights)** — Marketing insights and audience analysis from Audiense reports, covering demographic, cultural, influencer, and content engagement analysis
  <sub>★ 19 · TypeScript · Apache-2.0 · source · pushed 2025-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AudienseCo/mcp-audiense-insights.git`</sub>
- **[Hive Intelligence](https://github.com/hive-intel/hive-sdk)** — Hive Intelligence: Ultimate cryptocurrency MCP for AI assistants with unified access to crypto, DeFi, and Web3 analytics. Hive's remote mcp server guide remote server
  <sub>★ 19 · TypeScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add hive-intel/hive-skills`</sub>
- **[IPLocate](https://github.com/iplocate/mcp-server-iplocate)** — Look up IP address geolocation, network information, detect proxies and VPNs, and find abuse contact details using IPLocate.io
  <sub>★ 19 · JavaScript · MIT · npm · pushed 2025-06-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @iplocate/mcp-server`</sub>
- **[Atla](https://github.com/atla-ai/atla-mcp-server)** — Enable AI agents to interact with the Atla API for state-of-the-art LLMJ evaluation
  <sub>★ 17 · Python · MIT · source · pushed 2025-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/atla-ai/atla-mcp-server.git`</sub>
- **[Campertunity](https://github.com/campertunity/mcp-server)** — Search campgrounds around the world on campertunity, check availability, and provide booking links
  <sub>★ 17 · TypeScript · source · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/campertunity/mcp-server.git`</sub>
- **[ilert](https://github.com/iLert/mcp-ilert)** — Interact with ilert through natural language
  <sub>★ 17 · MIT · source · pushed 2025-09-04</sub>
  <sub>`git clone https://github.com/iLert/mcp-ilert.git`</sub>
- **[IP2Location.io](https://github.com/ip2location/mcp-ip2location-io)** — IP2Location.io API integration to retrieve the geolocation information for an IP address
  <sub>★ 16 · Python · MIT · source · pushed 2026-08-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ip2location/mcp-ip2location-io.git`</sub>
- **[Cloudbet](https://github.com/cloudbet/sports-mcp-server)** — Structured sports and esports data via Cloudbet API: fixtures, live odds, stake limits, and markets
  <sub>★ 14 · Go · MIT · source · pushed 2025-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cloudbet/sports-mcp-server.git`</sub>
- **[DAISYS](https://github.com/daisys-ai/daisys-mcp)** — Generate high-quality text-to-speech and text-to-voice outputs using the DAISYS platform
  <sub>★ 14 · Python · clone · pushed 2025-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/daisys-ai/daisys-mcp.git`</sub>
- **[SlideSpeak](https://github.com/SlideSpeak/slidespeak-mcp)** — Create presentations and PowerPoints using AI and SlideSpeak MCP
  <sub>★ 14 · Python · source · pushed 2026-04-30 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/SlideSpeak/slidespeak-mcp.git`</sub>
- **[ocireg](https://github.com/StacklokLabs/ocireg-mcp)** — An SSE-based MCP server that allows LLM-powered applications to interact with OCI registries. It provides tools for retrieving information about container images, listing tags, and more
  <sub>★ 13 · Go · Apache-2.0 · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/StacklokLabs/ocireg-mcp.git`</sub>
- **[Powerdrill](https://github.com/powerdrillai/powerdrill-mcp)** — An MCP server that provides tools to interact with Powerdrill datasets, enabling smart AI data analysis and insights
  <sub>★ 13 · TypeScript · MIT · npm · pushed 2025-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @powerdrillai/powerdrill-mcp`</sub>
- **[Riza](https://github.com/riza-io/riza-mcp)** — Arbitrary code execution and tool-use platform for LLMs by Riza
  <sub>★ 13 · JavaScript · source · pushed 2024-12-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/riza-io/riza-mcp.git`</sub>
- **[Scrapezy](https://github.com/Scrapezy/mcp)** — Turn websites into datasets with Scrapezy
  <sub>★ 13 · JavaScript · MIT · npm · pushed 2025-03-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @scrapezy/mcp`</sub>
- **[ALAPI](https://github.com/ALAPI-SDK/mcp-alapi-cn)** — ALAPI MCP Tools,Call hundreds of API interfaces via MCP
  <sub>★ 12 · Go · MIT · npx · pushed 2025-04-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @smithery/cli install @ALAPI-SDK/mcp-alapi-cn --client claude`</sub>
- **[Root Signals](https://github.com/root-signals/scorable-mcp)** — Equip AI agents with evaluation and self-improvement capabilities with Root Signals
  <sub>★ 12 · Python · docker · pushed 2026-07-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -e SCORABLE_API_KEY=<your_key> -p 0.0.0.0:9090:9090 --name=rs-mcp -d ghcr.io/scorable/scorable-mcp:latest`</sub>
- **[Adfin](https://github.com/Adfin-Engineering/mcp-server-adfin)** — The only platform you need to get paid - all payments in one place, invoicing and accounting reconciliations with Adfin
  <sub>★ 11 · Python · source · pushed 2025-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Adfin-Engineering/mcp-server-adfin.git`</sub>
- **[Buildable](https://github.com/chunkydotdev/bldbl-mcp)** — Official MCP server for Buildable AI-powered development platform. Enables AI assistants to manage tasks, track progress, get project context, and collaborate with humans on software projects
  <sub>★ 11 · TypeScript · MIT · npm · pushed 2025-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @bldbl/mcp`</sub>
- **[Digma](https://github.com/digma-ai/digma-mcp-server)** — A code observability MCP enabling dynamic code analysis based on OTEL/APM data to assist in code reviews, issues identification and fix, highlighting risky code etc
  <sub>★ 11 · C# · source · pushed 2025-05-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/digma-ai/digma-mcp-server.git`</sub>
- **[Driflyte](https://github.com/serkan-ozal/driflyte-mcp-server)** — MCP Server for Driflyte. The Driflyte MCP Server exposes tools that allow AI assistants to query and retrieve topic-specific knowledge from recursively crawled and indexed web pages
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2025-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @serkan-ozal/driflyte-mcp-server --client <SMITHERY-CLIENT-NAME> --key <SMITHERY-API-KEY>`</sub>
- **[Gcore Cloud](https://github.com/G-Core/gcore-mcp-server)** — Gcore's Cloud Official MCP Server
  <sub>★ 11 · Python · Apache-2.0 · uv · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from "gcore-mcp-server@git+https://github.com/G-Core/gcore-mcp-server.git" gcore-mcp-server`</sub>
- **[Hydrolix](https://github.com/hydrolix/mcp-hydrolix)** — Hydrolix time-series datalake integration providing schema exploration and query capabilities to LLM-based workflows
  <sub>★ 11 · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-hydrolix`</sub>
- **[Carbon Voice](https://github.com/PhononX/cv-mcp-server)** — MCP Server that connects AI Agents to Carbon Voice. Create, manage, and interact with voice messages, conversations, direct messages, folders, voice memos, AI actions and more in Carbon Voice
  <sub>★ 10 · TypeScript · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PhononX/cv-mcp-server.git`</sub>
- **[DevHub](https://github.com/devhub/devhub-cms-mcp)** — Manage and utilize website content within the DevHub CMS platform
  <sub>★ 9 · Python · npx · pushed 2025-03-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @devhub/devhub-cms-mcp --client claude`</sub>
- **[Kontent.ai](https://github.com/kontent-ai/mcp-server)** — Create, manage, and explore your content and content model using natural language in any MCP-compatible AI tool
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @kontent-ai/mcp-server@latest stdio`</sub>
- **[Pearch](https://github.com/Pearch-ai/mcp_pearch)** — Best people search engine that reduces the time spent on talent discovery
  <sub>★ 9 · Python · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pearch-ai/mcp_pearch.git`</sub>
- **[Reexpress](https://github.com/ReexpressAI/reexpress_mcp_server)** — Enable Similarity-Distance-Magnitude statistical verification for your search, software, and data science workflows
  <sub>★ 9 · Python · Apache-2.0 · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ReexpressAI/reexpress_mcp_server.git`</sub>
- **[ShopSavvy](https://github.com/shopsavvy/shopsavvy-mcp-server)** — Complete product and pricing data solution for AI assistants. Search for products by barcode/ASIN/URL, access detailed product metadata, access comprehensive pricing data from thousands of retailers, view and track price history, and more. Published as @shopsavvy/mcp-server
  <sub>★ 9 · JavaScript · MIT · clone · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shopsavvy/shopsavvy-mcp-server`</sub>
- **[Winston AI](https://github.com/gowinston-ai/winston-ai-mcp-server)** — AI detector MCP server with industry leading accuracy rates in detecting use of AI in text and images. The Winston AI MCP server also offers a robust plagiarism checker to help maintain integrity
  <sub>★ 9 · TypeScript · MIT · docker · pushed 2026-09-09 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -e WINSTONAI_API_KEY=your_api_key winston-ai-mcp`</sub>
- **[Allyson](https://github.com/isaiahbjork/allyson-mcp)** — AI-powered SVG animation generator that transforms static files into animated SVG components using the Allyson platform
  <sub>★ 8 · JavaScript · npx · pushed 2025-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx allyson-mcp --api-key YOUR_API_KEY`</sub>
- **[MailSandbox](https://github.com/btafoya/mailsandbox)** — MailSandbox (a fork of Mailpit) is a fast, zero-dependency email testing tool &amp; API with a web UI, SMTP server, Postmark API emulation, and MCP server for AI-assisted debugging
  <sub>★ 8 · Go · MIT · docker · pushed 2025-09-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name mailsandbox -p 8025:8025 -p 1025:1025 btafoya/mailsandbox`</sub>
- **[APIMatic MCP](https://github.com/apimatic/apimatic-validator-mcp)** — APIMatic MCP Server is used to validate OpenAPI specifications using APIMatic. The server processes OpenAPI files and returns validation summaries by leveraging APIMatic’s API
  <sub>★ 7 · TypeScript · clone · pushed 2025-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/apimatic/apimatic-validator-mcp.git`</sub>
- **[DreamFactory](https://github.com/dreamfactorysoftware/df-mcp/)** — An MCP server for securely (via RBAC) talking to on-premise and cloud MS SQL Server, MySQL, PostgreSQL databases and other data sources
  <sub>★ 7 · TypeScript · Apache-2.0 · source · pushed 2026-01-23 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/dreamfactorysoftware/df-mcp/.git`</sub>
- **[urlDNA](https://github.com/urldna/mcp)** — Dynamically scan and analyze potentially malicious URLs using the urlDNA
  <sub>★ 7 · Python · Apache-2.0 · docker · pushed 2026-08-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 -e x-api-key=<URLDNA_API_KEY> urldna-mcp-server`</sub>
- **[Fulcra Context](https://github.com/fulcradynamics/fulcra-context-mcp)** — Fulcra Context MCP server for accessing your personal health, workouts, sleep, location, and more, all privately. Built around Context by Fulcra
  <sub>★ 6 · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fulcradynamics/fulcra-context-mcp.git`</sub>
- **[RAD Security](https://github.com/rad-security/mcp-server)** — Interact with the RAD Security platform which provides AI-powered security insights for Kubernetes and cloud environments
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-09-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rad-security/mcp-server.git`</sub>
- **[VISO TRUST](https://github.com/visotrust/viso-mcp-server)** — Access and manage your VISO TRUST third-party risk program directly through your AI assistant
  <sub>★ 6 · Java · MIT · docker · pushed 2026-07-16 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e VISOTRUST_API_TOKEN=<your-api-token> viso-mcp-server`</sub>
- **[AnyCrawl](https://github.com/any4ai/anycrawl-mcp-server)** — AnyCrawl MCP Server, Powerful web scraping and crawling for Cursor, Claude, and other LLM clients via the Model Context Protocol (MCP)
  <sub>★ 6 · TypeScript · npm · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g anycrawl-mcp-server`</sub>
- **[UnifAI](https://github.com/unifai-network/unifai-mcp-server)** — Dynamically search and call tools using UnifAI Network
  <sub>★ 5 · source · pushed 2025-06-13</sub>
  <sub>`git clone https://github.com/unifai-network/unifai-mcp-server.git`</sub>
- **[CRIC Wuye AI](https://github.com/wuye-ai/mcp-server-wuye-ai)** — Interact with capabilities of the CRIC Wuye AI platform, an intelligent assistant specifically for the property management industry
  <sub>★ 4 · source · pushed 2026-04-14</sub>
  <sub>`git clone https://github.com/wuye-ai/mcp-server-wuye-ai.git`</sub>
- **[Agile Luminary](https://github.com/AgileLuminary/mcp-agile-luminary)** — Simpler Project Management - send Agile Luminary stories straight to your IDE
  <sub>★ 3 · JavaScript · MIT · source · pushed 2025-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgileLuminary/mcp-agile-luminary.git`</sub>
- **[Gluestack UI MCP Server](https://github.com/gauravsaini/gluestack-ui-mcp-server)** — An MCP server tailored for React Native–first development using Gluestack UI
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2025-08-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g gluestack-ui-mcp-server`</sub>
- **[Openfort](https://github.com/openfort-xyz/-DEPRECATED-mcp)** — Supercharge your AI assistant with plug-and-play access to authentication, project scaffolding, and smart wallet tooling
  <sub>★ 3 · TypeScript · source · pushed 2025-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/openfort-xyz/mcp.git`</sub>
- **[PlainSignal](https://github.com/plainsignal/plainsignal-mcp)** — Official MCP server that connects to PlainSignal's API and querying realtime website analytics data in conversational AI
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2025-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @plainsignal/plainsignal-mcp`</sub>
- **[Routine](https://github.com/routineco/mcp-server)** — MCP server to interact with Routine: calendars, tasks, notes, etc
  <sub>★ 3 · TypeScript · npx · pushed 2025-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx routine-mcp-server`</sub>
- **[4everland/4everland-hosting-mcp](https://github.com/4everland/4everland-hosting-mcp)** — An MCP server implementation for 4EVERLAND Hosting enabling instant deployment of AI-generated code to decentralized storage networks like Greenfield, IPFS, and Arweave
  <sub>★ 2 · TypeScript · clone · pushed 2025-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/4everland/4everland-hosting-mcp.git`</sub>
- **[CallHub](https://github.com/callhub/callhub-mcp)** — Python-based MCP tool providing a comprehensive set of functions for managing contacts, phonebooks, agents, teams, campaigns, and other CallHub resources
  <sub>★ 2 · Python · MIT · clone · pushed 2026-09-05 · macOS</sub>
  <sub>`git clone https://github.com/callhub/callhub-mcp.git`</sub>
- **[Coresignal](https://github.com/Coresignal-com/coresignal-mcp/)** — Access comprehensive B2B data on companies, employees, and job postings for your LLMs and AI workflows
  <sub>★ 2 · source · pushed 2026-08-07</sub>
  <sub>`git clone https://github.com/Coresignal-com/coresignal-mcp/.git`</sub>
- **[Dash0](https://github.com/dash0hq/mcp-dash0)** — Navigate your OpenTelemetry resources, investigate incidents and query metrics, logs and traces on Dash0
  <sub>★ 2 · MIT · source · pushed 2025-06-23</sub>
  <sub>`git clone https://github.com/dash0hq/mcp-dash0.git`</sub>
- **[DealX](https://github.com/DealExpress/mcp-server)** — MCP Server for DealX platform
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @dealx/mcp-server`</sub>
- **[TrackMage](https://github.com/trackmage/trackmage-mcp-server)** — Shipment tracking api and logistics management capabilities through the [TrackMage API] (https://trackmage.com/)
  <sub>★ 2 · JavaScript · MIT · clone · pushed 2025-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/trackmage-mcp-server.git`</sub>
- **[Nebula-Block-Data/nebulablock-mcp-server](https://github.com/Nebula-Block-Data/nebulablock-mcp-server)** — integrates with the fastmcp library to expose the full range of NebulaBlock API functionalities as accessible tools
  <sub>★ 1 · Python · clone · pushed 2025-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Nebula-Block-Data/api-mcp`</sub>
- **[Agent Mindshare](https://agentmindshare.com)** — Track and monitor AI agent mindshare across platforms - measure brand visibility in AI conversations with Agent Mindshare
  <sub>website</sub>
  <sub>`https://agentmindshare.com`</sub>
- **[AllVoiceLab](https://www.allvoicelab.com/mcp)** — An AI voice toolkit with TTS, voice cloning, and video translation, now available as an MCP server for smarter agent integration
  <sub>website</sub>
  <sub>`https://www.allvoicelab.com/mcp`</sub>
- **[Augments](https://augments.dev/)** — Comprehensive framework documentation and code examples for popular development tools and libraries
  <sub>website</sub>
  <sub>`https://augments.dev/`</sub>
- **[Atlan](https://github.com/atlanhq/agent-toolkit/tree/main/modelcontextprotocol)** — Official MCP Server from Atlan which enables you to bring the power of metadata to your AI tools
  <sub>Python · MIT · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/atlanhq/agent-toolkit.git && cd agent-toolkit/modelcontextprotocol`</sub>
- **[Audioscrape](https://www.audioscrape.com/docs/mcp)** — Search 1M+ hours of podcasts, interviews, talks and your private audio uploads with speaker identification and timestamps. Official Remote MCP server (via https://mcp.audioscrape.com) enabling AI assistants to access and analyze audio content through semantic and text-based search
  <sub>website</sub>
  <sub>`https://www.audioscrape.com/docs/mcp`</sub>
- **[AWS Bedrock KB Retrieval](https://github.com/awslabs/mcp/tree/main/src/bedrock-kb-retrieval-mcp-server)** — Query Amazon Bedrock Knowledge Bases using natural language to retrieve relevant information from your data sources
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git && cd mcp/src/bedrock-kb-retrieval-mcp-server`</sub>
- **[AWS CDK](https://github.com/awslabs/mcp/tree/main/src/cdk-mcp-server)** — Get prescriptive CDK advice, explain CDK Nag rules, check suppressions, generate Bedrock Agent schemas, and discover AWS Solutions Constructs patterns
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git && cd mcp/src/cdk-mcp-server`</sub>
- **[AWS Core](https://github.com/awslabs/mcp/tree/main/src/core-mcp-server)** — Core AWS MCP server providing prompt understanding and server management capabilities
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git && cd mcp/src/core-mcp-server`</sub>
- **[AWS Cost Analysis](https://github.com/awslabs/mcp/tree/main/src/cost-analysis-mcp-server)** — Analyze CDK projects to identify AWS services used and get pricing information from AWS pricing webpages and API
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git && cd mcp/src/cost-analysis-mcp-server`</sub>
- **[AWS Documentation](https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server)** — Fetch, convert, and search AWS documentation pages, with recommendations for related content
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git && cd mcp/src/aws-documentation-mcp-server`</sub>
- **[AWS Nova Canvas](https://github.com/awslabs/mcp/tree/main/src/nova-canvas-mcp-server)** — Generate images using Amazon Nova Canvas with text prompts and color guidance
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git && cd mcp/src/nova-canvas-mcp-server`</sub>
- **[Bankless Onchain](https://github.com/Bankless/onchain-mcp)** — Query Onchain data, like ERC20 tokens, transaction history, smart contract state
  <sub>source</sub>
  <sub>`git clone https://github.com/bankless/onchain-mcp.git`</sub>
- **[Baserow](https://baserow.io/user-docs/mcp-server)** — Read and write access to your Baserow tables
  <sub>website</sub>
  <sub>`https://baserow.io/user-docs/mcp-server`</sub>
- **[Bucket](https://github.com/bucketco/bucket-javascript-sdk/tree/main/packages/cli#model-context-protocol)** — Flag features, manage company data, and control feature access using Bucket
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/bucketco/bucket-javascript-sdk.git && cd bucket-javascript-sdk/packages/cli#model-context-protocol`</sub>
- **[Chargebee](https://github.com/chargebee/agentkit/tree/main/modelcontextprotocol)** — MCP Server that connects AI agents to Chargebee platform
  <sub>TypeScript · MIT · in-repo · pushed 2025-11-18</sub>
  <sub>`git clone https://github.com/chargebee/agentkit.git && cd agentkit/modelcontextprotocol`</sub>
- **[Chroma Package Search](https://trychroma.com/package-search)** — Add to coding agents like Claude or Cursor to give them the ability to understand and better use thousands of dependencies
  <sub>website</sub>
  <sub>`https://trychroma.com/package-search`</sub>
- **[CoinGecko](https://docs.coingecko.com/reference/mcp-server/)** — Official CoinGecko API MCP Server for Crypto Price &amp; Market Data, across 200+ blokchain networks and 8M+ tokens
  <sub>website</sub>
  <sub>`https://docs.coingecko.com/reference/mcp-server/`</sub>
- **[Convex](https://stack.convex.dev/convex-mcp-server)** — Introspect and query your apps deployed to Convex
  <sub>website</sub>
  <sub>`https://stack.convex.dev/convex-mcp-server`</sub>
- **[Cua](https://github.com/trycua/cua/tree/main/libs/mcp-server)** — MCP server for the Computer-Use Agent (CUA), allowing you to run CUA through Claude Desktop or other MCP clients
  <sub>HTML · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/trycua/cua.git && cd cua/libs/mcp-server`</sub>
- **[Cycode](https://github.com/cycodehq/cycode-cli#mcp-command-experiment)** — Boost security in your dev lifecycle via SAST, SCA, Secrets &amp; IaC scanning with Cycode
  <sub>Python · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/cycodehq/cycode-cli.git && cd cycode-cli/#mcp-command-experiment`</sub>
- **[DeepWiki by Devin](https://docs.devin.ai/work-with-devin/deepwiki-mcp)** — Remote, no-auth MCP server providing AI-powered codebase context and answers
  <sub>website</sub>
  <sub>`https://docs.devin.ai/work-with-devin/deepwiki-mcp`</sub>
- **[Drand](https://github.com/randa-mu/drand-mcp-server)** — An MCP server for fetching verifiable random numbers from the drand network
  <sub>TypeScript · MIT · source · pushed 2025-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/randa-mu/drand-mcp-server.git`</sub>
- **[ELEMENT.FM](https://gitlab.com/elementfm/mcp)** — Create and publish unlimited podcast shows and episodes with ELEMENT.FM
  <sub>website</sub>
  <sub>`https://gitlab.com/elementfm/mcp`</sub>
- **[FetchSERP](https://github.com/fetchSERP/fetchserp-mcp-server-node)** — All-in-One SEO &amp; Web Intelligence Toolkit API FetchSERP
  <sub>unavailable</sub>
- **[Find-A-Domain](https://findadomain.dev/mcp)** — Domain availability checking and WHOIS lookup tools
  <sub>website</sub>
  <sub>`https://findadomain.dev/mcp`</sub>
- **[IBM wxflows](https://github.com/IBM/wxflows/tree/main/examples/mcp/javascript)** — Tool platform by IBM to build, test and deploy tools for any data source
  <sub>MIT · in-repo · pushed 2025-09-18</sub>
  <sub>`git clone https://github.com/IBM/wxflows.git && cd wxflows/examples/mcp/javascript`</sub>
- **[ForeverVM](https://github.com/jamsocket/forevervm/tree/main/javascript/mcp-server)** — Run Python in a code sandbox
  <sub>Rust · MIT · in-repo · pushed 2025-04-17</sub>
  <sub>`git clone https://github.com/jamsocket/forevervm.git && cd forevervm/javascript/mcp-server`</sub>
- **[Inbox Zero](https://github.com/elie222/inbox-zero/tree/main/apps/mcp-server)** — AI personal assistant for email Inbox Zero
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/elie222/inbox-zero.git && cd inbox-zero/apps/mcp-server`</sub>
- **[InstantDB](https://github.com/instantdb/instant/tree/main/client/packages/mcp)** — Create, manage, and update applications on InstantDB, the modern Firebase
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/instantdb/instant.git && cd instant/client/packages/mcp`</sub>
- **[Jetty.io](https://github.com/jettyio/mlcbakery/tree/main/mcp_server)** — Work on dataset metadata with MLCommons Croissant validation and creation
  <sub>Python · MIT · in-repo · pushed 2026-03-11</sub>
  <sub>`git clone https://github.com/jettyio/mlcbakery.git && cd mlcbakery/mcp_server`</sub>
- **[Knit MCP](https://developers.getknit.dev/docs/knit-mcp-server-getting-started)** — Connect with 10,000+ tools across HRIS, ATS, CRM, Accounting, Calendar, Meeting, Ticketing, and more categories
  <sub>website</sub>
  <sub>`https://developers.getknit.dev/docs/knit-mcp-server-getting-started`</sub>
- **[Lingo.dev](https://github.com/lingodotdev/lingo.dev/blob/main/mcp.md)** — Make your AI agent speak every language on the planet, using Lingo.dev Localization Engine
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/lingodotdev/lingo.dev.git && cd lingo.dev/mcp.md`</sub>
- **[Mastra/mcp](https://github.com/mastra-ai/mastra/tree/main/packages/mcp)** — Client implementation for Mastra, providing seamless integration with MCP-compatible AI models and tools
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git && cd mastra/packages/mcp`</sub>
- **[Mastra/mcp-docs-server](https://github.com/mastra-ai/mastra/tree/main/packages/mcp-docs-server)** — Provides AI assistants with direct access to Mastra.ai's complete knowledge base
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git && cd mastra/packages/mcp-docs-server`</sub>
- **[Mercado Libre](https://mcp.mercadolibre.com/)** — Mercado Libre's official MCP server, offering tools to interact with our marketplace, simplifying tasks and product integration
  <sub>website</sub>
  <sub>`https://mcp.mercadolibre.com/`</sub>
- **[Mercado Pago](https://mcp.mercadopago.com/)** — Mercado Pago's official MCP server, offering tools to interact with our API, simplifying tasks and product integration
  <sub>website</sub>
  <sub>`https://mcp.mercadopago.com/`</sub>
- **[Mux](https://github.com/muxinc/mux-node-sdk/tree/master/packages/mcp-server)** — Mux is a video API for developers. With Mux's official MCP you can upload videos, create live streams, generate thumbnails, add captions, manage playback policies, dig through engagement data, monitor video performance, and more
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/muxinc/mux-node-sdk.git && cd mux-node-sdk/packages/mcp-server`</sub>
- **[Notte](https://github.com/nottelabs/notte/tree/main/packages/notte-mcp)** — Leverage Notte Web AI agents &amp; cloud browser sessions for scalable browser automation &amp; scraping workflows
  <sub>Python · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/nottelabs/notte.git && cd notte/packages/notte-mcp`</sub>
- **[OctoEverywhere For 3D Printing](https://octoeverywhere.com/mcp)** — A 3D Printing MCP server that allows for querying for live state, webcam snapshots, and 3D printer control
  <sub>website</sub>
  <sub>`https://octoeverywhere.com/mcp`</sub>
- **[PaddleOCR](https://paddlepaddle.github.io/PaddleOCR/latest/en/version3.x/deployment/mcp_server.html)** — An MCP server that brings enterprise-grade OCR and document parsing capabilities to AI applications
  <sub>website</sub>
  <sub>`https://paddlepaddle.github.io/PaddleOCR/latest/en/version3.x/deployment/mcp_server.html`</sub>
- **[Pearl](https://mcp.pearl.com)** — Official MCP Server to interact with Pearl API. Connect your AI Agents with 12,000+ certified experts instantly
  <sub>website</sub>
  <sub>`https://mcp.pearl.com`</sub>
- **[PGYER](https://github.com/PGYER/pgyer-mcp-server)** — MCP Server for PGYER platform, supports uploading, querying apps, etc
  <sub>JavaScript · source · pushed 2025-11-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PGYER/pgyer-mcp-server.git`</sub>
- **[ProdEAI](https://github.com/CuriousBox-AI/ProdE-mc)** — Your 24/7 production engineer that preserves context across multiple codebases Prode.ai
  <sub>unavailable</sub>
- **[Render](https://render.com/docs/mcp-server)** — The official Render MCP server: spin up new services, run queries against your databases, and debug rapidly with direct access to service metrics and logs
  <sub>website</sub>
  <sub>`https://render.com/docs/mcp-server`</sub>
- **[RevenueCat](https://www.revenuecat.com/docs/tools/mcp/overview)** — Manage your In-app-purchases in RevenueCat without leaving your AI coding environment
  <sub>website</sub>
  <sub>`https://www.revenuecat.com/docs/tools/mcp/overview`</sub>
- **[Rube](https://rube.composio.dev)** — Rube is a Model Context Protocol (MCP) server that connects your AI tools to 500+ apps like Gmail, Slack, GitHub, and Notion. Simply install it in your AI client, authenticate once with your apps, and start asking your AI to perform real actions like "Send an email" or "Create a task."
  <sub>website</sub>
  <sub>`https://rube.composio.dev`</sub>
- **[TalentoHQ](https://hr.talentohq.com/mcp)** — Connect to the TalentoHQ HR software via MCP. Transform your organization with the AI first HR software
  <sub>website</sub>
  <sub>`https://hr.talentohq.com/mcp`</sub>
- **[Taskeract](https://github.com/Acqusys/taskeract-mcp)** — Official Taskeract MCP Server for integrating your Taskeract project tasks and load the context of your tasks into your MCP enabled app
  <sub>unavailable</sub>
- **[Thirdweb](https://github.com/thirdweb-dev/ai/tree/main/python/thirdweb-mcp)** — Read/write to over 2k blockchains, enabling data querying, contract analysis/deployment, and transaction execution, powered by Thirdweb
  <sub>in-repo</sub>
  <sub>`git clone https://github.com/thirdweb-dev/ai.git && cd ai/python/thirdweb-mcp`</sub>
- **[Tldv](https://gitlab.com/tldv/tldv-mcp-server)** — Connect your AI agents to Google-Meet, Zoom &amp; Microsoft Teams through tl;dv
  <sub>website</sub>
  <sub>`https://gitlab.com/tldv/tldv-mcp-server`</sub>
- **[Token Metrics](https://github.com/token-metrics/mcp)** — Token Metrics integration for fetching real-time crypto market data, trading signals, price predictions, and advanced analytics
  <sub>unavailable</sub>
- **[Verodat](https://github.com/Verodat/verodat-mcp-server)** — Interact with Verodat AI Ready Data platform
  <sub>unavailable</sub>
- **[VideoDB](https://github.com/video-db/agent-toolkit/tree/main/modelcontextprotocol)** — Server for advanced AI-driven video editing, semantic search, multilingual transcription, generative media, voice cloning, and content moderation
  <sub>Python · in-repo · pushed 2026-03-26</sub>
  <sub>`git clone https://github.com/video-db/agent-toolkit.git && cd agent-toolkit/modelcontextprotocol`</sub>
- **[VpunaAiSearch](https://github.com/vpuna/vpuna-ai-search)** — Connect to Vpuna AI Search Service, a developer first platform for semantic search, summarization, and contextual chat. Each project dynamically exposes its own Remote HTTP MCP server, enabling real-time context injection from structured and unstructured data
  <sub>unavailable</sub>
- **[WayStation](https://waystation.ai/connect/mcp-server)** — A universal remote MCP server that connects to popular productivity tools such as Notion, Monday, AirTable, and many more
  <sub>website</sub>
  <sub>`https://waystation.ai/connect/mcp-server`</sub>
- **[WebDataSource](https://webdatasource.com/releases/latest/mcp/index.html)** — Web Crawler for AI Agents. Supercharge your AI agents with an MCP-ready web crawler that delivers real-time insights from the web and your private knowledge bases
  <sub>website</sub>
  <sub>`https://webdatasource.com/releases/latest/mcp/index.html`</sub>
- **[Willi MaKo Knowledge Service](https://mcp.stromhaltig.de)** — A knowledge service for Germany's complex Energy Market Communications (MaKo) regulations
  <sub>website</sub>
  <sub>`https://mcp.stromhaltig.de`</sub>
- **[Zapier](https://zapier.com/mcp)** — Connect your AI Agents to 8,000 apps instantly
  <sub>website</sub>
  <sub>`https://zapier.com/mcp`</sub>
- **[Zenable](https://docs.zenable.io/integrations/mcp/getting-started)** — Clean up sloppy AI code and prevent vulnerabilities
  <sub>website</sub>
  <sub>`https://docs.zenable.io/integrations/mcp/getting-started`</sub>

## Community Servers

- **[ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai)** — AI-powered web scraping library that creates scraping pipelines using natural language.- ScrapeGraphAI
  <sub>★ 31.2k · Python · MIT · pip · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install scrapegraphai`</sub>
- **[IDA Pro MCP](https://github.com/mrexodia/ida-pro-mcp)** — MCP Server for automated reverse engineering with IDA Pro
  <sub>★ 12.3k · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install https://github.com/mrexodia/ida-pro-mcp/archive/refs/heads/main.zip`</sub>
- **[Browser MCP](https://github.com/BrowserMCP/mcp)** — Automate your local browser
  <sub>★ 7.1k · TypeScript · Apache-2.0 · source · pushed 2025-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browsermcp/mcp.git`</sub>
- **[XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP)** —  Popular MCP server that enables AI agents to scaffold, build, run and test iOS, macOS, visionOS and watchOS apps or simulators and wired and wireless devices. It has powerful UI-automation capabilities like controlling the simulator, capturing run-time logs, as well as taking screenshots and viewing the accessibility hierarchy
  <sub>★ 6.4k · TypeScript · MIT · npm · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g xcodebuildmcp@latest`</sub>
- **[Godot MCP](https://github.com/Coding-Solo/godot-mcp)** — MCP server for interacting with the Godot game engine, providing tools for editing, running, debugging, and managing scenes in Godot projects
  <sub>★ 5.8k · JavaScript · MIT · npx · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @coding-solo/godot-mcp`</sub>
- **[Playwright MCP Server](https://github.com/executeautomation/mcp-playwright)** — An MCP server using Playwright for browser automation and webscrapping
  <sub>★ 5.7k · TypeScript · MIT · npm · pushed 2025-12-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @executeautomation/playwright-mcp-server`</sub>
- **[Peekaboo](https://github.com/openclaw/Peekaboo)** — a macOS-only MCP server that enables AI agents to capture screenshots of applications, or the entire system
  <sub>★ 5.2k · Swift · MIT · npx · pushed 2026-09-22 · macOS</sub>
  <sub>`npx -y @steipete/peekaboo --version`</sub>
- **[Obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)** — Interacting with Obsidian via REST API
  <sub>★ 4.4k · Python · MIT · npx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-obsidian run mcp-obsidian`</sub>
- **[Excel](https://github.com/haris-musa/excel-mcp-server)** — Excel manipulation including data reading/writing, worksheet management, formatting, charts, and pivot table
  <sub>★ 4.2k · Python · MIT · uv · pushed 2026-04-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx excel-mcp-server stdio`</sub>
- **[bytebase/dbhub](https://github.com/bytebase/dbhub)** — Universal database MCP server supporting mainstream databases.\
  <sub>★ 3.6k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @bytebase/dbhub@latest --transport http --port 8080 --dsn "postgres://user:password@localhost:5432/dbname?sslmode=disable"`</sub>
- **[Unity3d Game Engine](https://github.com/CoderGamester/mcp-unity)** — MCP Server to control and interact with Unity3d Game Engine for game development
  <sub>★ 1.9k · C# · MIT · source · pushed 2026-09-03 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CoderGamester/mcp-unity.git`</sub>
- **[Slack](https://github.com/korotovsky/slack-mcp-server)** — The most powerful MCP server for Slack Workspaces. This integration supports both Stdio and SSE transports, proxy settings and does not require any permissions or bots being created or approved by Workspace admins 😏
  <sub>★ 1.8k · Go · MIT · source · pushed 2026-07-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/korotovsky/slack-mcp-server.git`</sub>
- **[Language Server](https://github.com/isaacphi/mcp-language-server)** — MCP Language Server gives MCP enabled clients access to semantic tools like get definition, references, rename, and diagnostics
  <sub>★ 1.6k · Go · BSD-3-Clause · go · pushed 2026-03-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`go install github.com/isaacphi/mcp-language-server@latest`</sub>
- **[Kubernetes](https://github.com/Flux159/mcp-server-kubernetes)** — Connect to Kubernetes cluster and manage pods, deployments, services
  <sub>★ 1.6k · TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx mcp-chat --server "npx mcp-server-kubernetes"`</sub>
- **[MCP Installer](https://github.com/anaisbetts/mcp-installer)** — Set up MCP servers in Claude Desktop
  <sub>★ 1.5k · JavaScript · MIT · source · pushed 2024-11-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anaisbetts/mcp-installer.git`</sub>
- **[MySQL](https://github.com/designcomputer/mysql_mcp_server)** — MySQL database integration with configurable access controls and schema inspection
  <sub>★ 1.4k · Python · MIT · npx · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install designcomputer/mysql-mcp-server --client claude`</sub>
- **[MCPJungle](https://github.com/mcpjungle/MCPJungle)** — Open-source, Self-hosted MCP server Gateway that connects your AI Agents to MCP Servers (for developers and enterprises)
  <sub>★ 1.3k · Go · MPL-2.0 · brew · pushed 2026-08-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install mcpjungle/mcpjungle/mcpjungle`</sub>
- **[Meta Ads Remote MCP](https://github.com/pipeboard-co/meta-ads-mcp)** — Remote MCP server to interact with Meta Ads API - access, analyze, and manage Facebook, Instagram, and other Meta platforms advertising campaigns
  <sub>★ 1.3k · Python · brew · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install pipeboard-co/tap/pipeboard`</sub>
- **[SearXNG](https://github.com/ihor-sokoliuk/mcp-searxng)** — A Model Context Protocol Server for SearXNG
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-searxng`</sub>
- **[Web Search MCP](https://github.com/mrkrsl/web-search-mcp)** — A server that provides local, full web search, summaries and page extration for use with Local LLMs
  <sub>★ 1.1k · TypeScript · MIT · clone · pushed 2025-08-08 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/mrkrsl/web-search-mcp.git`</sub>
- **[QGIS](https://github.com/jjsantos01/qgis_mcp)** — connects QGIS Desktop to Claude AI through the MCP. This integration enables prompt-assisted project creation, layer loading, code execution, and more
  <sub>★ 1.1k · Python · clone · pushed 2025-10-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone git@github.com:jjsantos01/qgis_mcp.git`</sub>
- **[Minima](https://github.com/Minima-AI-Inc/minima)** — Local RAG (on-premises) with MCP server
  <sub>★ 1k · Python · MPL-2.0 · source · pushed 2026-01-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/dmayboroda/minima.git`</sub>
- **[Microsoft 365](https://github.com/Softeria/ms-365-mcp-server)** — MCP server that connects to the whole Microsoft 365 suite (Microsoft Office, Outlook, Excel) using Graph API (including mail, files, calendar)
  <sub>★ 991 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @softeria/ms-365-mcp-server --toon`</sub>
- **[weibaohui/k8m](https://github.com/weibaohui/k8m)** — Provides multi-cluster Kubernetes management and operations using MCP, featuring a management interface, logging, and nearly 50 built-in tools covering common DevOps and development scenarios. Supports both standard and CRD resources
  <sub>★ 887 · Go · MIT · source · pushed 2026-09-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/weibaohui/k8m.git`</sub>
- **[aymericzip/intlayer](https://github.com/aymericzip/intlayer)** — A MCP Server that enhance your IDE with AI-powered assistance for Intlayer i18n / CMS tool: smart CLI access, versioned docs
  <sub>★ 834 · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aymericzip/intlayer.git`</sub>
- **[Android MCP](https://github.com/minhalvp/android-mcp-server)** — An MCP server that provides control over Android devices through ADB. Offers device screenshot capture, UI layout analysis, package management, and ADB command execution capabilities
  <sub>★ 811 · Python · Apache-2.0 · clone · pushed 2025-05-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/minhalvp/android-mcp-server.git`</sub>
- **[clojure-mcp](https://github.com/bhauman/clojure-mcp)** — Clojure development tools, direct access to the running program via REPL
  <sub>★ 777 · Clojure · EPL-2.0 · source · pushed 2026-06-20</sub>
  <sub>`git clone https://github.com/bhauman/clojure-mcp.git`</sub>
- **[Mermaid](https://github.com/hustcc/mcp-mermaid)** — Generate mermaid diagram and chart with AI MCP dynamically
  <sub>★ 636 · TypeScript · MIT · npm · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-mermaid`</sub>
- **[Pandoc](https://github.com/vivekVells/mcp-pandoc)** — MCP server for seamless document format conversion using Pandoc, supporting Markdown, HTML, and plain text, with other formats like PDF, csv and docx in development
  <sub>★ 582 · Python · MIT · npx · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-pandoc --client claude`</sub>
- **[YouTube](https://github.com/anaisbetts/mcp-youtube)** — Fetch YouTube subtitles
  <sub>★ 546 · TypeScript · MIT · source · pushed 2026-08-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anaisbetts/mcp-youtube.git`</sub>
- **[Data Exploration](https://github.com/reading-plus-ai/mcp-server-data-exploration)** — MCP server for autonomous data exploration on .csv-based datasets, providing intelligent insights with minimal effort
  <sub>★ 544 · Python · MIT · source · pushed 2025-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reading-plus-ai/mcp-server-data-exploration.git`</sub>
- **[Docker](https://github.com/QuantGeekDev/docker-mcp)** — Run and manage docker containers, docker compose, and logs
  <sub>★ 503 · Python · MIT · npx · pushed 2024-12-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @smithery/cli install docker-mcp --client claude`</sub>
- **[Vibe Check](https://github.com/PV-Bhat/vibe-check-mcp-server)** — The definitive Vibe Coder's sanity check MCP server: Prevents cascading errors by calling a "Vibe-check" agent to ensure alignment and prevent scope creep
  <sub>★ 503 · TypeScript · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @pv-bhat/vibe-check-mcp start --stdio`</sub>
- **[Airtable](https://github.com/domdomegg/airtable-mcp-server)** — Read and write access to Airtable databases
  <sub>★ 458 · TypeScript · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/domdomegg/airtable-mcp-server.git`</sub>
- **[Binary Ninja](https://github.com/fosdickio/binary_ninja_mcp)** — A Binary Ninja plugin, MCP server, and bridge that seamlessly integrates Binary Ninja with your favorite MCP client
  <sub>★ 438 · Python · GPL-3.0 · npx · pushed 2026-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y binary-ninja-mcp`</sub>
- **[Apple Notes](https://github.com/RafalWilinski/mcp-apple-notes)** — Talk with your Apple Notes
  <sub>★ 415 · TypeScript · clone · pushed 2024-12-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/RafalWilinski/mcp-apple-notes`</sub>
- **[HuggingFace Spaces](https://github.com/evalstate/mcp-hfspace)** — Server for using HuggingFace Spaces, supporting Images, Audio, Text and more. Claude Desktop mode for ease-of-use
  <sub>★ 389 · TypeScript · MIT · source · pushed 2025-06-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/evalstate/mcp-hfspace.git`</sub>
- **[Odoo](https://github.com/ivnvxd/mcp-server-odoo)** — Connect AI assistants to Odoo ERP systems for business data access and workflow automation
  <sub>★ 389 · Python · MPL-2.0 · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx mcp-server-odoo`</sub>
- **[mcp-k8s-go](https://github.com/strowk/mcp-k8s-go)** — Golang-based Kubernetes MCP Server. Built to be extensible
  <sub>★ 384 · Go · MIT · go · pushed 2025-12-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/strowk/mcp-k8s-go`</sub>
- **[BloodHound-MCP](https://github.com/MorDavid/BloodHound-MCP-AI)** — (by MorDavid) - integration that connects BloodHound with AI through MCP, allowing security professionals to analyze Active Directory attack paths using natural language queries instead of Cypher
  <sub>★ 376 · Python · clone · pushed 2025-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/your-username/MCP-BloodHound.git`</sub>
- **[Facebook Ads](https://github.com/gomarble-ai/facebook-ads-mcp-server)** — MCP server acting as an interface to the Facebook Ads, enabling programmatic access to Facebook Ads data and management features
  <sub>★ 366 · Python · MIT · npx · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @gomarble-ai/facebook-ads-mcp-server --client claude`</sub>
- **[Everything Search](https://github.com/mamertofabian/mcp-everything-search)** — Fast Windows file search using Everything SDK
  <sub>★ 364 · Python · MIT · npx · pushed 2025-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @smithery/cli install mcp-server-everything-search --client claude`</sub>
- **[interactive-mcp](https://github.com/ttommyth/interactive-mcp)** — Enables interactive LLM workflows by adding local user prompts and chat capabilities directly into the MCP loop
  <sub>★ 352 · TypeScript · MIT · clone · pushed 2025-11-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ttommyth/interactive-mcp.git`</sub>
- **[Apple Shortcuts](https://github.com/recursechat/mcp-server-apple-shortcuts)** — An MCP Server Integration with Apple Shortcuts
  <sub>★ 348 · JavaScript · Apache-2.0 · clone · pushed 2024-12-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:recursechat/mcp-server-apple-shortcuts.git`</sub>
- **[Home Assistant](https://github.com/voska/hass-mcp)** — Interact with Home Assistant to control smart home devices, query states, manage automations, and troubleshoot your smart home setup
  <sub>★ 345 · Python · MIT · uv · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx hass-mcp --http --port 8000`</sub>
- **[Windows Control](https://github.com/claude-did-this/MCPControl)** — Programmatic control over Windows system operations including mouse, keyboard, window management, and screen capture using nut.js
  <sub>★ 332 · TypeScript · MIT · npm · pushed 2025-12-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-control`</sub>
- **[ImageSorcery MCP](https://github.com/sunriseapps/imagesorcery-mcp)** — ComputerVision-based 🪄 sorcery of image recognition and editing tools for AI assistants
  <sub>★ 331 · Python · MIT · uv · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx imagesorcery-mcp --post-install`</sub>
- **[llm-context](https://github.com/cyberchitta/llm-context.py)** — Share code context with LLMs via Model Context Protocol or clipboard
  <sub>★ 306 · Python · Apache-2.0 · uv · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "llm-context>=0.6.0"`</sub>
- **[Facebook Ads Library](https://github.com/proxy-intell/facebook-ads-library-mcp)** — Get any answer from the Facebook Ads Library, conduct deep research including messaging, creative testing and comparisons in seconds
  <sub>★ 302 · Python · MIT · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/proxy-intell/facebook-ads-library-mcp.git`</sub>
- **[FileScopeMCP](https://github.com/admica/FileScopeMCP)** — Analyzes your codebase identifying important files based on dependency relationships. Generates diagrams and importance scores per file, helping AI assistants understand the codebase. Automatically parses popular programming languages, Python, Lua, C, C++, Rust, Zig
  <sub>★ 302 · TypeScript · clone · pushed 2026-05-10 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/admica/FileScopeMCP.git`</sub>
- **[Tmux](https://github.com/nickgnd/tmux-mcp)** — Interact with your Tmux sessions, windows and pane, execute commands in tmux panes and retrieve result
  <sub>★ 302 · JavaScript · MIT · source · pushed 2026-02-14 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/nickgnd/tmux-mcp.git`</sub>
- **[consult7](https://github.com/szeider/consult7)** — Analyze large codebases and document collections using high-context models via OpenRouter, OpenAI, or Google AI -- very useful, e.g., with Claude Code
  <sub>★ 296 · Python · MIT · uv · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx consult7 <api-key> [--test]`</sub>
- **[MongoDB](https://github.com/kiliczsh/mcp-mongo-server)** — A Model Context Protocol Server for MongoDB
  <sub>★ 283 · TypeScript · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-mongo-server mongodb://localhost:27017/mydatabase`</sub>
- **[Google Search Console](https://github.com/ahonn/mcp-server-gsc)** — A Model Context Protocol (MCP) server providing access to Google Search Console
  <sub>★ 273 · TypeScript · source · pushed 2026-09-04 · macOS</sub>
  <sub>`git clone https://github.com/ahonn/mcp-server-gsc.git`</sub>
- **[Windows CLI](https://github.com/simon-ami/win-cli-mcp-server)** — MCP server for secure command-line interactions on Windows systems, enabling controlled access to PowerShell, CMD, and Git Bash shells
  <sub>★ 269 · JavaScript · MIT · npx · pushed 2025-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @simonb97/server-win-cli --init-config ./config.json`</sub>
- **[Notion](https://github.com/danhilse/notion_mcp)** — Integrates with Notion's API to manage personal todo list
  <sub>★ 208 · Python · MIT · clone · pushed 2024-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/notion-mcp.git`</sub>
- **[MongoDB Lens](https://github.com/furey/mongodb-lens)** — Full Featured MCP Server for MongoDB Database
  <sub>★ 207 · JavaScript · MIT · npx · pushed 2025-04-23 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y mongodb-lens`</sub>
- **[TikTok](https://github.com/Seym0n/tiktok-mcp)** — TikTok integration for getting post details and video subtitles
  <sub>★ 199 · JavaScript · MIT · clone · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Seym0n/tiktok-mcp.git`</sub>
- **[Snowflake](https://github.com/isaacwasserman/mcp-snowflake-server)** — Snowflake database integration with read/write capabilities and insight tracking
  <sub>★ 186 · Python · GPL-3.0 · npx · pushed 2025-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp_snowflake_server --client claude`</sub>
- **[Gru Sandbox](https://github.com/babelcloud/gbox)** — Gru-sandbox(gbox) is an open source project that provides a self-hostable sandbox for MCP integration or other AI agent usecases
  <sub>★ 181 · Go · Apache-2.0 · npm · pushed 2026-07-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @gbox.ai/cli`</sub>
- **[Instagram DMs](https://github.com/trypeggy/instagram_dm_mcp)** — Send Instagram DMs via your LLM
  <sub>★ 181 · Python · MIT · clone · pushed 2025-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trypeggy/instagram_dm_mcp.git`</sub>
- **[Mongo](https://github.com/QuantGeekDev/mongo-mcp)** — A Model Context Protocol (MCP) server that enables LLMs to interact directly with MongoDB databases
  <sub>★ 175 · TypeScript · MIT · npx · pushed 2025-03-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install mongo-mcp --client claude`</sub>
- **[Jean Memory](https://github.com/jean-technologies/jean-memory)** — Premium memory consistent across all AI applications
  <sub>★ 171 · Python · Apache-2.0 · clone · pushed 2026-01-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/jean-technologies/jean-memory.git`</sub>
- **[any-chat-completions-mcp](https://github.com/pyroprompts/any-chat-completions-mcp)** — Chat with any other OpenAI SDK Compatible Chat Completions API, like Perplexity, Groq, xAI and more
  <sub>★ 164 · JavaScript · MIT · npx · pushed 2025-05-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install any-chat-completions-mcp-server --client claude`</sub>
- **[just-every/mcp-read-website-fast](https://github.com/just-every/mcp-read-website-fast)** — Fast, token-efficient web content extraction that converts websites to clean Markdown. Features Mozilla Readability, smart caching, polite crawling with robots.txt support, and concurrent fetching with minimal dependencies
  <sub>★ 160 · TypeScript · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/just-every/mcp-read-website-fast.git`</sub>
- **[Calculator](https://github.com/githejie/mcp-server-calculator)** — This server enables LLMs to use calculator for precise numerical calculations
  <sub>★ 159 · Python · MIT · pip · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-server-calculator`</sub>
- **[Svelte Documentation](https://github.com/khromov/svelte-llm-mcp)** — Remote server (SSE/Streamable) for the latest Svelte and SvelteKit documentation
  <sub>★ 159 · TypeScript · MIT · source · pushed 2026-02-14 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/khromov/llmctx.git`</sub>
- **[weibaohui/kom](https://github.com/weibaohui/kom)** — Provides multi-cluster Kubernetes management and operations using MCP, It can be integrated as an SDK into your own project and includes nearly 50 built-in tools covering common DevOps and development scenarios. Supports both standard and CRD resources
  <sub>★ 149 · Go · MIT · source · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/weibaohui/kom.git`</sub>
- **[BigQuery](https://github.com/ergut/mcp-bigquery-server)** — (by ergut) - Server implementation for Google BigQuery integration that enables direct BigQuery database access and querying capabilities
  <sub>★ 148 · TypeScript · MIT · clone · pushed 2026-05-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ergut/mcp-bigquery-server`</sub>
- **[Linear](https://github.com/tacticlaunch/mcp-linear)** — Integrates with Linear project management systems
  <sub>★ 147 · TypeScript · MIT · npm · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @tacticlaunch/mcp-linear`</sub>
- **[Google Ads](https://github.com/gomarble-ai/google-ads-mcp-server)** — MCP server acting as an interface to the Google Ads, enabling programmatic access to Google Ads data and management features
  <sub>★ 144 · Python · MIT · clone · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/google-ads-mcp-server.git`</sub>
- **[Paperless-MCP](https://github.com/baruchiro/paperless-mcp)** — An MCP server for interacting with a Paperless-NGX API server. This server provides tools for managing documents, tags, correspondents, and document types in your Paperless-NGX instance
  <sub>★ 144 · TypeScript · ISC · source · pushed 2026-09-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/baruchiro/paperless-mcp.git`</sub>
- **[🧲 Magg 🧲](https://github.com/sitbon/magg)** — A meta-MCP server that acts as a universal hub, allowing LLMs to autonomously discover, install, and orchestrate multiple MCP servers - essentially giving AI assistants the power to extend their own capabilities on-demand
  <sub>★ 143 · Python · AGPL-3.0 · uv · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install magg`</sub>
- **[Hetzner Cloud MCP Server](https://github.com/dkruyt/mcp-hetzner)** — A Model Context Protocol (MCP) server for interacting with the Hetzner Cloud API. This server allows language models to manage Hetzner Cloud resources through structured functions
  <sub>★ 140 · Python · MIT · pip · pushed 2025-04-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/dkruyt/mcp-hetzner.git`</sub>
- **[BigQuery](https://github.com/LucasHild/mcp-server-bigquery)** — (by LucasHild) - BigQuery database integration with schema inspection and query capabilities
  <sub>★ 130 · Python · MIT · npx · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-server-bigquery --client claude`</sub>
- **[Google News](https://github.com/ChanMeng666/server-google-news)** — Google News search capabilities with automatic topic categorization and multi-language support via SerpAPI integration
  <sub>★ 129 · TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @chanmeng666/google-news-server --client claude`</sub>
- **[Reloaderoo](https://github.com/cameroncooke/reloaderoo)** — A local MCP server for developers that mirrors your in-development MCP server, allowing seamless restarts and tool updates so you can build, test, and iterate on your MCP server within the same AI session without interruption
  <sub>★ 125 · TypeScript · MIT · npm · pushed 2026-02-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g reloaderoo`</sub>
- **[Codesys-mcp-toolkit](https://github.com/johannesPettersson80/codesys-mcp-toolkit)** — A Model Context Protocol (MCP) server for CODESYS V3 programming environments
  <sub>★ 124 · TypeScript · MIT · npm · pushed 2025-05-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @codesys/mcp-toolkit`</sub>
- **[Trino MCP Server](https://github.com/tuannvm/mcp-trino)** — A Go implementation of a Model Context Protocol (MCP) server for Trino, enabling LLM models to query distributed SQL databases through standardized tools
  <sub>★ 121 · Go · MIT · brew · pushed 2026-07-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install tuannvm/mcp/mcp-trino`</sub>
- **[Sourcerer](https://github.com/st3v3nmw/sourcerer-mcp)** — MCP for semantic code search &amp; navigation that reduces token waste
  <sub>★ 119 · Go · MIT · go · pushed 2025-11-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`go install github.com/st3v3nmw/sourcerer-mcp/cmd/sourcerer@latest`</sub>
- **[just-every/mcp-screenshot-website-fast](https://github.com/just-every/mcp-screenshot-website-fast)** — High-quality screenshot capture optimized for Claude Vision API. Automatically tiles full pages into 1072x1072 chunks (1.15 megapixels) with configurable viewports and wait strategies for dynamic content
  <sub>★ 110 · TypeScript · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/just-every/mcp-screenshot-website-fast.git`</sub>
- **[LunchMoney](https://github.com/akutishevsky/lunchmoney-mcp)** — MCP server for LunchMoney personal finance and budgeting tool
  <sub>★ 107 · TypeScript · MIT · source · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/akutishevsky/lunchmoney-mcp.git`</sub>
- **[Google Keep](https://github.com/feuerdev/keep-mcp)** — Read, create, update and delete Google Keep notes
  <sub>★ 103 · Python · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/feuerdev/keep-mcp.git`</sub>
- **[Maya MCP](https://github.com/PatrickPalmer/MayaMCP)** — MCP server for Autodesk Maya
  <sub>★ 102 · Python · MIT · source · pushed 2025-05-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PatrickPalmer/MayaMCP.git`</sub>
- **[CalDAV MCP](https://github.com/dominik1001/caldav-mcp)** — A CalDAV MCP server to expose calendar operations as tools for AI assistants
  <sub>★ 101 · TypeScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dominik1001/caldav-mcp.git`</sub>
- **[FHIR MCP](https://github.com/the-momentum/fhir-mcp-server)** — MCP Server that connects AI agents to FHIR servers
  <sub>★ 100 · Python · MIT · source · pushed 2025-10-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/the-momentum/fhir-mcp-server.git`</sub>
- **[Vega-Lite](https://github.com/isaacwasserman/mcp-vegalite-server)** — Generate visualizations from fetched data using the VegaLite format and renderer
  <sub>★ 100 · Python · source · pushed 2025-05-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/isaacwasserman/mcp-vegalite-server.git`</sub>
- **[Basecamp](https://github.com/georgeantonopoulos/Basecamp-MCP-Server)** — Integration with Basecamp project management platform for managing projects, to-dos, card tables, documents, and team collaboration
  <sub>★ 99 · Python · MIT · clone · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/georgeantonopoulos/Basecamp-MCP-Server.git`</sub>
- **[Perplexity](https://github.com/tanigami/mcp-server-perplexity)** — Interacting with Perplexity
  <sub>★ 95 · Python · MIT · source · pushed 2024-12-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tanigami/mcp-server-perplexity.git`</sub>
- **[Database](https://github.com/TheRaLabs/legion-mcp)** — (by Legion AI) - Universal database MCP server supporting multiple database types including PostgreSQL, Redshift, CockroachDB, MySQL, RDS MySQL, Microsoft SQL Server, BigQuery, Oracle DB, and SQLite
  <sub>★ 94 · Python · GPL-3.0 · npx · pushed 2025-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run src/database_mcp/mcp_server.py`</sub>
- **[MCP Open Library](https://github.com/8enSmith/mcp-open-library)** — A Model Context Protocol (MCP) server for the Open Library API that enables AI assistants to search for book and author information
  <sub>★ 94 · TypeScript · MIT · docker · pushed 2026-09-03 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 mcp-open-library`</sub>
- **[CoinCap](https://github.com/QuantGeekDev/coincap-mcp)** — A MCP server that provides real-time cryptocurrency market data through CoinCap's public API without requiring authentication
  <sub>★ 92 · TypeScript · MIT · npx · pushed 2025-01-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install coincap-mcp --client claude`</sub>
- **[AniList](https://github.com/yuna0x0/anilist-mcp)** — AniList MCP server for accessing AniList API data
  <sub>★ 88 · TypeScript · MIT · npx · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector -e ANILIST_TOKEN=your_api_token npx anilist-mcp`</sub>
- **[OpenAI](https://github.com/pierrebrunelle/mcp-server-openai)** — Query OpenAI models directly from Claude using MCP protocol
  <sub>★ 84 · Python · MIT · clone · pushed 2024-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pierrebrunelle/mcp-server-openai`</sub>
- **[xcodebuild](https://github.com/ShenghaiWang/xcodebuild)** — Build iOS Xcode workspace/project and feed back errors to llm
  <sub>★ 84 · Python · MIT · pip · pushed 2025-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcpxcodebuild`</sub>
- **[Email](https://github.com/Shy2593666979/mcp-server-email)** — This server enables users to send emails through various email providers, including Gmail, Outlook, Yahoo, Sina, Sohu, 126, 163, and QQ Mail. It also supports attaching files from specified directories, making it easy to upload attachments along with the email content
  <sub>★ 80 · Python · MIT · source · pushed 2025-04-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Shy2593666979/mcp-server-email.git`</sub>
- **[QuantConnect](https://github.com/QuantConnect/mcp-server)** — Dockerized Python MCP server that lets LLMs like Claude or OpenAI o3 Pro autonomously create projects, backtest strategies, and deploy live-trading workflows via the QuantConnect API
  <sub>★ 77 · Python · Apache-2.0 · source · pushed 2026-05-07 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/QuantConnect/mcp-server.git`</sub>
- **[NocoDB](https://github.com/edwinbernadus/nocodb-mcp-server)** — Manage NocoDB server, support read and write databases
  <sub>★ 76 · JavaScript · npx · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y nocodb-mcp-server {NOCODB_URL} {NOCODB_BASE_ID} {NOCODB_API_TOKEN}`</sub>
- **[OpenAPI Schema Explorer](https://github.com/kadykov/mcp-openapi-schema-explorer)** — Token-efficient access to OpenAPI/Swagger specs via MCP Resources
  <sub>★ 76 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-openapi-schema-explorer`</sub>
- **[PiAPI](https://github.com/apinetwork/piapi-mcp-server)** — PiAPI MCP server makes user able to generate media content with Midjourney/Flux/Kling/Hunyuan/Udio/Trellis directly from Claude or any other MCP-compatible apps
  <sub>★ 75 · TypeScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install piapi-mcp-server --client claude`</sub>
- **[Ntfy](https://github.com/gitmotion/ntfy-me-mcp)** — An ntfy MCP server for sending/fetching ntfy notifications to your self-hosted ntfy server from AI Agents 📤 (supports secure token auth &amp; more - use with npx or docker!)
  <sub>★ 74 · TypeScript · GPL-3.0 · source · pushed 2026-04-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gitmotion/ntfy-me-mcp.git`</sub>
- **[MCP-CLI Adapter](https://github.com/inercia/MCPShell)** — Use command line tools in a secure fashion as MCP tools
  <sub>★ 70 · Go · MIT · source · pushed 2026-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/inercia/mcp-cli-adapter.git`</sub>
- **[GDB](https://github.com/pansila/mcp_server_gdb)** — A GDB/MI protocol server based on the MCP protocol, providing remote application debugging capabilities with AI assistants
  <sub>★ 68 · Rust · MIT · source · pushed 2025-09-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/pansila/mcp_server_gdb.git`</sub>
- **[HackMD](https://github.com/yuna0x0/hackmd-mcp)** — A Model Context Protocol server for integrating HackMD's note-taking platform with AI assistants
  <sub>★ 67 · TypeScript · MIT · npx · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector -e HACKMD_API_TOKEN=your_api_token npx hackmd-mcp`</sub>
- **[Miro](https://github.com/k-jarzyna/mcp-miro)** — Miro MCP server, exposing all functionalities available in official Miro SDK
  <sub>★ 66 · TypeScript · Apache-2.0 · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/k-jarzyna/mcp-miro.git`</sub>
- **[DeepView MCP](https://github.com/Mitek99/deepview-mcp)** — Enables IDEs like Cursor and Windsurf to analyze large codebases using Gemini's 1M context window
  <sub>★ 65 · Python · MIT · npx · pushed 2025-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @ai-1st/deepview-mcp --client claude`</sub>
- **[Todoist](https://github.com/stanislavlysenko0912/todoist-mcp-server)** — Full implementation of Todoist Rest API for MCP server
  <sub>★ 63 · TypeScript · MIT · source · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stanislavlysenko0912/todoist-mcp-server.git`</sub>
- **[Contentful](https://github.com/ivo-toby/contentful-mcp)** — Interact with your content on the Contentful platform
  <sub>★ 62 · TypeScript · MIT · npx · pushed 2026-01-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @ivotoby/contentful-management-mcp-server --client claude`</sub>
- **[fast-filesystem-mcp](https://github.com/efforthye/fast-filesystem-mcp)** — Advanced filesystem operations with large file handling capabilities and Claude-optimized features. Provides fast file reading/writing, sequential reading for large files, directory operations, file search, and streaming writes with backup &amp; recovery
  <sub>★ 62 · TypeScript · Apache-2.0 · npm · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g fast-filesystem-mcp`</sub>
- **[DifyWorkflow](https://github.com/gotoolkits/mcp-difyworkflow-server)** — Tools to the query and execute of Dify workflows
  <sub>★ 61 · Go · Apache-2.0 · clone · pushed 2024-12-26 · macOS</sub>
  <sub>`git clone https://github.com/gotoolkis/mcp-difyworkflow-server.git`</sub>
- **[Netbird](https://github.com/aantti/mcp-netbird)** — List and analyze Netbird network peers, groups, policies, and more
  <sub>★ 60 · Go · Apache-2.0 · npx · pushed 2025-04-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install @aantti/mcp-netbird --client claude`</sub>
- **[Whois MCP](https://github.com/bharathvaj-ganesan/whois-mcp)** — MCP server that performs whois lookup against domain, IP, ASN and TLD
  <sub>★ 60 · JavaScript · MIT · npx · pushed 2025-03-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @bharathvaj/whois-mcp@latest`</sub>
- **[context-awesome](https://github.com/bh-rat/context-awesome)** — A MCP server for querying 8,500+ curated awesome lists (1M+ items) and fetching the best resources for your agent
  <sub>★ 59 · TypeScript · MIT · npm · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g context-awesome`</sub>
- **[MKP](https://github.com/StacklokLabs/mkp)** — Model Kontext Protocol Server for Kubernetes that allows LLM-powered applications to interact with Kubernetes clusters through native Go implementation with direct API integration and comprehensive resource management
  <sub>★ 59 · Go · Apache-2.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/StacklokLabs/mkp.git`</sub>
- **[Memory-Plus](https://github.com/Yuchen20/Memory-Plus)** — a lightweight, local RAG memory store to record, retrieve, update, delete, and visualize persistent "memories" across sessions—perfect for developers working with multiple AI coders (like Windsurf, Cursor, or Copilot) or anyone who wants their AI to actually remember them
  <sub>★ 56 · Python · Apache-2.0 · npx · pushed 2025-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector fastmcp run run .\\memory_plus\\mcp.py`</sub>
- **[MCP-SearXNG-Enhanced Web Search](https://github.com/OvertliDS/mcp-searxng-enhanced)** — An enhanced MCP server for SearXNG web searching, utilizing a category-aware web-search, web-scraping, and includes a date/time retrieval tool
  <sub>★ 55 · Python · MIT · clone · pushed 2026-05-05 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/OvertliDS/mcp-searxng-enhanced.git`</sub>
- **[Django REST Framework MCP](https://github.com/zacharypodbela/django-rest-framework-mcp)** — Expose Django REST Framework APIs as MCP tools for LLMs and agentic applications
  <sub>★ 54 · Python · BSD-3-Clause · pip · pushed 2025-11-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install django-rest-framework-mcp`</sub>
- **[Trello](https://github.com/m0xai/trello-mcp-server)** — Trello integration for working with boards, lists in boards and cards in lists
  <sub>★ 54 · Python · clone · pushed 2026-06-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/m0xai/trello-mcp-server.git`</sub>
- **[BGG MCP](https://github.com/kkjdaniel/bgg-mcp)** — BGG MCP enables AI tools to interact with the BoardGameGeek API
  <sub>★ 53 · Go · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kkjdaniel/bgg-mcp.git`</sub>
- **[User Feedback](https://github.com/mrexodia/user-feedback-mcp)** — Simple MCP Server to enable a human-in-the-loop workflow in tools like Cline and Cursor
  <sub>★ 53 · Python · MIT · source · pushed 2025-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mrexodia/user-feedback-mcp.git`</sub>
- **[Random Number](https://github.com/zazencodes/random-number-mcp)** — Provides LLMs with essential random generation abilities, built entirely on Python's standard library
  <sub>★ 51 · Python · MIT · npx · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run random-number-mcp`</sub>
- **[elisp-dev-mcp](https://github.com/laurynas-biveinis/elisp-dev-mcp)** — elisp (Emacs Lisp) development support tools, running in Emacs
  <sub>★ 47 · Emacs Lisp · GPL-3.0 · source · pushed 2026-08-25</sub>
  <sub>`git clone https://github.com/laurynas-biveinis/elisp-dev-mcp.git`</sub>
- **[Jina Reader](https://github.com/wong2/mcp-jina-reader)** — Fetch the content of a remote URL as Markdown with Jina Reader
  <sub>★ 47 · TypeScript · source · pushed 2024-12-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wong2/mcp-jina-reader.git`</sub>
- **[Keycloak MCP Server](https://github.com/sshaaf/keycloak-mcp-server)** — designed to work with Keycloak for identity and access management, with about 40+ tools covering, Users, Realms, Clients, Roles, Groups, IDPs, Authentication. Native builds available
  <sub>★ 47 · Java · source · pushed 2026-08-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/sshaaf/keycloak-mcp-server.git`</sub>
- **[Tasks](https://github.com/flesler/mcp-tasks)** — An efficient task manager. Designed to minimize tool confusion and maximize LLM budget efficiency while providing powerful search, filtering, and organization capabilities across multiple file formats (Markdown, JSON, YAML)
  <sub>★ 47 · TypeScript · MIT · npx · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-tasks add "Your new task text" "To Do" 0`</sub>
- **[Rootly-AI-Labs/Rootly-MCP-server](https://github.com/rootlyhq/rootly-mcp-server)** — MCP server for the incident management platform Rootly
  <sub>★ 46 · Python · Apache-2.0 · go · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/rootlyhq/rootly-cli/cmd/rootly@latest`</sub>
- **[PiloTY](https://github.com/yiwenlu66/PiloTY)** — AI pilot for PTY operations that enables agents to control interactive terminals with stateful sessions, SSH connections, and background process management
  <sub>★ 45 · Python · uv · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from git+https://github.com/yiwenlu66/PiloTY.git piloty`</sub>
- **[Algorand](https://github.com/GoPlausible/algorand-mcp)** — A comprehensive MCP server for tooling interactions(40+) and resource accessibility(60+) plus many useful prompts to interact with Algorand Blockchain
  <sub>★ 44 · TypeScript · MIT · npm · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @goplausible/algorand-mcp`</sub>
- **[Kagi](https://github.com/ac3xx/mcp-servers-kagi)** — Kagi search API integration
  <sub>★ 44 · TypeScript · MIT · npx · pushed 2024-12-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @smithery/cli install kagi-server --client claude`</sub>
- **[OSV](https://github.com/StacklokLabs/osv-mcp)** — Access the OSV (Open Source Vulnerabilities) database for vulnerability information. Query vulnerabilities by package version or commit, batch query multiple packages, and get detailed vulnerability information by ID
  <sub>★ 42 · Go · Apache-2.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/StacklokLabs/osv-mcp.git`</sub>
- **[Microsoft Entra ID MCP Server](https://github.com/hieuttmmo/entraid-mcp-server)** — A Python MCP server for Microsoft Entra ID (Azure AD) directory, user, group, device, sign-in, and security operations via Microsoft Graph
  <sub>★ 41 · Python · source · pushed 2025-05-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hieuttmmo/entraid-mcp-server.git`</sub>
- **[Storyblok](https://github.com/Kiran1689/storyblok-mcp-server)** — Storyblok MCP server enables your AI assistants to directly access and manage your Storyblok spaces, stories, components, assets, workflows, and more
  <sub>★ 41 · Python · MIT · source · pushed 2025-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Kiran1689/storyblok-mcp-server.git`</sub>
- **[WebSearch-MCP](https://github.com/mnhlt/WebSearch-MCP)** — Self-hosted Websearch API
  <sub>★ 41 · JavaScript · npm · pushed 2025-04-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g websearch-mcp`</sub>
- **[Package Registry Search](https://github.com/Artmann/package-registry-mcp)** — Search and get up-to-date information about NPM, Cargo, PyPi, and NuGet packages
  <sub>★ 39 · TypeScript · MIT · npm · pushed 2025-12-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g package-registry-mcp`</sub>
- **[APISIX-MCP](https://github.com/api7/apisix-mcp)** — APISIX Model Context Protocol (MCP) server is used to bridge large language models (LLMs) with the APISIX Admin API, supporting querying and managing all resources in Apache APISIX
  <sub>★ 38 · TypeScript · Apache-2.0 · npx · pushed 2025-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @api7/apisix-mcp --client claude`</sub>
- **[godoc-mcp-server](https://github.com/yikakia/godoc-mcp-server)** — MCP server to provide golang packages and their information from pkg.go.dev
  <sub>★ 38 · Go · MIT · go · pushed 2026-03-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/yikakia/godoc-mcp-server/cmd/godoc-mcp-server@latest`</sub>
- **[Trello MCP](https://github.com/kocakli/Trello-Desktop-MCP)** — Trello Desktop MCP server that enables Claude Desktop to interact with Trello boards, cards, lists, and team members through natural language commands
  <sub>★ 38 · TypeScript · MIT · clone · pushed 2026-03-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kocakli/trello-desktop-mcp.git`</sub>
- **[gotoolkits/wecombot](https://github.com/gotoolkits/mcp-wecombot-server.git)** — An MCP server application that sends various types of messages to the WeCom group robot
  <sub>★ 37 · Go · GPL-3.0 · npx · pushed 2025-01-22 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npx -y @smithery/cli install @gotoolkits/mcp-wecombot-server --client claude-desktop`</sub>
- **[Weather](https://github.com/TimLukaHorstmann/mcp-weather)** — Accurate weather forecasts via the AccuWeather API (free tier available)
  <sub>★ 35 · TypeScript · MIT · npx · pushed 2025-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @timlukahorstmann/mcp-weather`</sub>
- **[Bluesky](https://github.com/laulauland/bluesky-context-server)** — integrates with Bluesky API to query and search feeds and posts
  <sub>★ 34 · TypeScript · MIT · npx · pushed 2025-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @laulauland/bluesky-context-server --client claude`</sub>
- **[Maven](https://github.com/Bigsy/maven-mcp-server)** — Tools to query latest Maven dependency information
  <sub>★ 34 · JavaScript · MIT · npm · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-maven-deps`</sub>
- **[MCP Aggregator](https://github.com/nazar256/combine-mcp)** — An MCP (Model Context Protocol) aggregator that allows you to combine multiple MCP servers into a single endpoint allowing to filter specific tools
  <sub>★ 34 · Go · go · pushed 2025-11-24 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/nazar256/combine-mcp/cmd/combine-mcp@latest`</sub>
- **[Maven Tools](https://github.com/arvindand/maven-tools-mcp)** — Enhanced Maven Central integration with intelligent caching, bulk operations, and version classification
  <sub>★ 33 · Java · MIT · source · pushed 2026-09-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/arvindand/maven-tools-mcp.git`</sub>
- **[Agentset](https://github.com/agentset-ai/mcp-server)** — RAG MCP for your Agentset data
  <sub>★ 31 · JavaScript · MIT · source · pushed 2025-06-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentset-ai/mcp-server.git`</sub>
- **[Gemsuite](https://github.com/PV-Bhat/gemsuite-mcp)** — The ultimate open-source server for advanced Gemini API interaction with MCP, intelligently selects models
  <sub>★ 30 · TypeScript · MIT · npx · pushed 2025-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest install @PV-Bhat/gemsuite-mcp --client claude`</sub>
- **[Homebrew MCP](https://github.com/jeannier/homebrew-mcp)** — Interact with Homebrew (the package manager for macOS and Linux) using natural language commands
  <sub>★ 29 · Python · MIT · clone · pushed 2025-06-23 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/jeannier/homebrew-mcp`</sub>
- **[SchemaCrawler](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage)** — Connect to any relational database, and be able to get valid SQL, and ask questions like what does a certain column prefix mean
  <sub>★ 29 · EPL-2.0 · source · pushed 2026-09-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/schemacrawler/SchemaCrawler-MCP-Server-Usage.git`</sub>
- **[Task Orchestrator](https://github.com/EchoingVesper/mcp-task-orchestrator)** — AI-powered task orchestration and workflow automation with specialized agent roles, intelligent task decomposition, and seamless integration across Claude Desktop, Cursor IDE, Windsurf, and VS Code
  <sub>★ 28 · Python · MIT · pipx · pushed 2025-08-15 · Win · WSL2 · macOS · Linux</sub>
  <sub>`pipx install mcp-task-orchestrator`</sub>
- **[SQLite](https://github.com/panasenco/mcp-sqlite)** — MCP server for SQLite files. Supports Datasette-compatible metadata!
  <sub>★ 27 · Python · Apache-2.0 · npx · pushed 2026-01-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx mcp-sqlite sample/titanic.db --metadata sample/titanic.yml`</sub>
- **[Jira Context MCP](https://github.com/rahulthedevil/Jira-Context-MCP)** — MCP server to provide Jira Tickets information to AI coding agents like Cursor
  <sub>★ 26 · TypeScript · MIT · npx · pushed 2025-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @rahulthedevil/Jira-Context-MCP --client claude`</sub>
- **[Multi Chat MCP Server (Google Chat)](https://github.com/siva010928/multi-chat-mcp-server)** — Connect AI assistants like Cursor to Google Chat and beyond — enabling smart, extensible collaboration across chat platforms
  <sub>★ 26 · Python · MIT · clone · pushed 2025-10-05 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/siva010928/multi-chat-mcp-server.git`</sub>
- **[shadcn-ui-mcp-server](https://github.com/heilgar/shadcn-ui-mcp-server)** — A powerful and flexible MCP server designed to enhance the development experience with Shadcn UI components, providing tools for component management, documentation, and installation
  <sub>★ 26 · TypeScript · MIT · source · pushed 2025-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/heilgar/shadcn-ui-mcp-server.git`</sub>
- **[Alertmanager](https://github.com/ntk148v/alertmanager-mcp-server)** — A Model Context Protocol (MCP) server that enables AI assistants to integrate with Prometheus Alertmanager
  <sub>★ 25 · Python · Apache-2.0 · npx · pushed 2026-06-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install @ntk148v/alertmanager-mcp-server --client claude`</sub>
- **[Bing Webmaster Tools](https://github.com/isiahw1/mcp-server-bing-webmaster)** — MCP server for Bing Webmaster Tools API integration providing access to search analytics, site management, URL submission, and SEO insights
  <sub>★ 25 · Python · MIT · npm · pushed 2026-02-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @isiahw1/mcp-server-bing-webmaster`</sub>
- **[Text-To-GraphQL](https://github.com/Arize-ai/text-to-graphql-mcp)** — MCP server for text-to-graphql, integrates with Claude Desktop and Cursor
  <sub>★ 25 · Python · pip · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install text-to-graphql-mcp`</sub>
- **[Time](https://github.com/TheoBrigitte/mcp-time)** — MCP server which provides utilities to work with time and dates, with natural language, multiple formats and timezone convertion capabilities
  <sub>★ 25 · Go · MIT · go · pushed 2026-03-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/TheoBrigitte/mcp-time/cmd/mcp-time@latest`</sub>
- **[AnkiConnect](https://github.com/spacholski1225/anki-connect-mcp)** — AnkiConnect MCP server for interacting with Anki via AnkiConnect
  <sub>★ 24 · TypeScript · MIT · clone · pushed 2025-07-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/spacholski1225/anki-connect-mcp.git`</sub>
- **[Creatify](https://github.com/TSavo/creatify-mcp)** — MCP Server that exposes Creatify AI API capabilities for AI video generation, including avatar videos, URL-to-video conversion, text-to-speech, and AI-powered editing tools
  <sub>★ 23 · TypeScript · npm · pushed 2025-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @tsavo/creatify-mcp`</sub>
- **[dbt-docs](https://github.com/mattijsdp/dbt-docs-mcp)** — MCP server for dbt-core (OSS) users as the official dbt MCP only supports dbt Cloud. Supports project metadata, model and column-level lineage and dbt documentation
  <sub>★ 23 · Python · MIT · source · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mattijsdp/dbt-docs-mcp.git`</sub>
- **[Nexus](https://github.com/adawalli/nexus)** — Web search server that integrates Perplexity Sonar models via OpenRouter API for real-time, context-aware search with citations
  <sub>★ 23 · TypeScript · MIT · npx · pushed 2026-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`bunx nexus-mcp`</sub>
- **[X (Twitter)](https://github.com/mbelinky/x-mcp-server)** — Enhanced MCP server for Twitter/X with OAuth 2.0 support, v2 API media uploads, smart v1.1 fallbacks, and comprehensive rate limiting. Post tweets with text/media, search, and delete tweets programmatically
  <sub>★ 23 · TypeScript · MIT · clone · pushed 2025-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mbelinky/x-mcp-server.git`</sub>
- **[GitHub Repos Manager MCP Server](https://github.com/kurdin/github-repos-manager-mcp)** — Token-based GitHub automation management. No Docker, Flexible configuration, 80+ tools with direct API integration
  <sub>★ 22 · JavaScript · npx · pushed 2025-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github-repos-manager-mcp`</sub>
- **[Spotify Player](https://github.com/vsaez/mcp-spotify-player)** — Control Spotify playback, queue, volume and playlists from Claude/Cursor via MCP. (Python)
  <sub>★ 22 · Python · MIT · source · pushed 2025-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vsaez/mcp-spotify-player.git`</sub>
- **[AWS EC2 Pricing](https://github.com/trilogy-group/aws-pricing-mcp)** — Get up-to-date EC2 pricing information with one call. Fast. Powered by a pre-parsed AWS pricing catalogue
  <sub>★ 21 · Python · MIT · source · pushed 2025-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trilogy-group/aws-pricing-mcp.git`</sub>
- **[libSQL by xexr](https://github.com/Xexr/mcp-libsql)** — MCP server for libSQL databases with comprehensive security and management tools. Supports file, local HTTP, and remote Turso databases with connection pooling, transaction support, and 6 specialized database tools
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2025-06-03 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pnpm install -g @xexr/mcp-libsql`</sub>
- **[User Prompt MCP](https://github.com/nazar256/user-prompt-mcp)** — An MCP server for Cursor that enables requesting user input during generation process
  <sub>★ 21 · Go · MIT · go · pushed 2025-04-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/nazar256/user-prompt-mcp/cmd/user-prompt-mcp@latest`</sub>
- **[Hippycampus](https://github.com/cromwellian/hippycampus)** — Turns any Swagger/OpenAPI REST endpoint with a yaml/json definition into an MCP Server with Langchain/Langflow integration automatically
  <sub>★ 20 · Python · MIT · source · pushed 2025-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cromwellian/hippycampus.git`</sub>
- **[Terragrunt-Docs](https://github.com/Excoriate/mcp-terragrunt-docs)** — Terragrunt documentation always up to date
  <sub>★ 20 · TypeScript · MIT · clone · pushed 2025-04-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Excoriate/mcp-terragrunt-docs.git`</sub>
- **[Danielpeter-99/calcom-mcp](https://github.com/Danielpeter-99/calcom-mcp)** — MCP server for Calcom (Also known as Cal.com). Manage event types, create bookings, and access Cal.com scheduling data through LLMs
  <sub>★ 19 · Python · MIT · clone · pushed 2025-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Danielpeter-99/calcom-mcp.git`</sub>
- **[Dolt](https://github.com/dolthub/dolt-mcp)** — The official MCP server for version-controlled Dolt databases
  <sub>★ 19 · Go · Apache-2.0 · clone · pushed 2026-08-18 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/dolthub/dolt-mcp`</sub>
- **[Imagician](https://github.com/flowy11/imagician)** — A MCP server for comprehensive image editing operations including resizing, format conversion, cropping, compression, and more based on sharp
  <sub>★ 19 · JavaScript · MIT · npm · pushed 2025-11-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @flowy11/imagician`</sub>
- **[Scaffold](https://github.com/Beer-Bears/scaffold)** — Scaffold is a Retrieval-Augmented Generation (RAG) system designed to structural understanding of large codebases. It transforms your source code into a living knowledge graph, allowing for precise, context-aware interactions that go far beyond simple file retrieval
  <sub>★ 19 · Python · MIT · clone · pushed 2025-10-29 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Beer-Bears/scaffold.git`</sub>
- **[Druid MCP Server](https://github.com/iunera/druid-mcp-server)** — STDIO/SEE MCP Server for Apache Druid by iunera that provides extensive tools, resources, and prompts for managing and analyzing Druid clusters
  <sub>★ 18 · Java · Apache-2.0 · source · pushed 2026-08-31 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/iunera/druid-mcp-server.git`</sub>
- **[Nile Postgres](https://github.com/niledatabase/nile-mcp-server)** — Manage and query databases, tenants, users, auth using LLMs
  <sub>★ 17 · TypeScript · MIT · clone · pushed 2025-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/nile-mcp-server.git`</sub>
- **[NPM Search](https://github.com/btwiuse/npm-search-mcp-server)** — Search for npm packages
  <sub>★ 16 · JavaScript · MIT · npm · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g npm-search-mcp-server`</sub>
- **[JSON MCP](https://github.com/VadimNastoyashchy/json-mcp)** — MCP server empowers LLMs to interact with JSON files efficiently. With JSON MCP, you can split, merge, etc
  <sub>★ 15 · JavaScript · MIT · npm · pushed 2025-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g json-mcp-server@latest`</sub>
- **[Local History MCP](https://github.com/xxczaki/local-history-mcp)** — MCP server for accessing VS Code/Cursor's Local History
  <sub>★ 15 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx local-history-mcp`</sub>
- **[Reminder](https://github.com/arifszn/reminder-mcp)** — MCP server for scheduling and triggering reminders via Slack or Telegram
  <sub>★ 15 · TypeScript · MIT · source · pushed 2026-01-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/arifszn/reminder-mcp.git`</sub>
- **[Screeny](https://github.com/rohanrav/screeny)** — Privacy-first macOS MCP server that provides visual context for AI agents through window screenshots
  <sub>★ 15 · Python · MIT · uv · pushed 2025-08-23 · macOS</sub>
  <sub>`uvx mcp-server-screeny --setup`</sub>
- **[IMAP MCP](https://github.com/dominik1001/imap-mcp)** — An IMAP Model Context Protocol (MCP) server to expose IMAP operations as tools for AI assistants
  <sub>★ 14 · TypeScript · MIT · source · pushed 2025-06-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dominik1001/imap-mcp.git`</sub>
- **[Backup](https://github.com/hexitex/MCP-Backup-Server)** — Add smart Backup ability to coding agents like Windsurf, Cursor, Cluade Coder, etc
  <sub>★ 12 · JavaScript · MIT · npx · pushed 2025-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @hexitex/MCP-Backup-Server --client claude`</sub>
- **[CockroachDB](https://github.com/amineelkouhen/mcp-cockroachdb)** — A Model Context Protocol server for managing, monitoring, and querying data in CockroachDB
  <sub>★ 12 · Python · MIT · uv · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from git+https://github.com/amineelkouhen/mcp-cockroachdb.git@0.1.0 cockroachdb-mcp-server --url postgresql://localhost:26257/defaultdb`</sub>
- **[Google PSE/CSE](https://github.com/rendyfebry/google-pse-mcp)** — A Model Context Protocol (MCP) server providing access to Google Programmable Search Engine (PSE) and Custom Search Engine (CSE)
  <sub>★ 12 · JavaScript · Apache-2.0 · source · pushed 2025-09-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rendyfebry/google-pse-mcp.git`</sub>
- **[TeamCity](https://github.com/itcaat/teamcity-mcp)** — MCP server for TeamCity, integrates with Claude Desktop and Cursor
  <sub>★ 12 · Go · MIT · helm · pushed 2025-12-09 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`helm install teamcity-mcp ./helm/teamcity-mcp \`</sub>
- **[Unified Diff MCP Server](https://github.com/gorosun/unified-diff-mcp)** — Beautiful HTML and PNG diff visualization using diff2html, designed for filesystem edit_file dry-run output with high-performance Bun runtime
  <sub>★ 12 · TypeScript · npx · pushed 2025-06-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`bunx @smithery/cli install @gorosun/unified-diff-mcp --client claude --config '{`</sub>
- **[Box](https://github.com/hmk/box-mcp-server)** — File access and search for Box
  <sub>★ 11 · JavaScript · BSD-3-Clause · clone · pushed 2025-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YOUR_USERNAME/box-mcp-server.git`</sub>
- **[Google Admin MCP](https://github.com/securityfortech/google-admin-mcp)** — A Model Context Protocol (MCP) server enabling interaction with Google Admin APIs
  <sub>★ 11 · JavaScript · MIT · docker · pushed 2025-07-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -e GOOGLE_TOKEN_JSON="your_base64_encoded_token" google-admin-mcp`</sub>
- **[Files](https://github.com/flesler/mcp-files)** — Enables agents to quickly find and edit code in a codebase with surgical precision. Find symbols, edit them everywhere
  <sub>★ 10 · TypeScript · MIT · npx · pushed 2026-08-06 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx mcp-files`</sub>
- **[Homey](https://github.com/pigmej/python-homey-mcp)** — Interact with Homey to control smart home system. Supports devices, flows, and zones. Contains a few goodies for better integrations with LLMs
  <sub>★ 9 · Python · uv · pushed 2025-09-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from . homey-mcp`</sub>
- **[MintMCP](https://github.com/mintmcp/servers)** — MCP servers for Google Calendar, Gmail, Outlook Calendar, and Outlook
  <sub>★ 9 · source · pushed 2025-09-10</sub>
  <sub>`git clone https://github.com/mintmcp/servers.git`</sub>
- **[OpenMF-mifosx-self-service](https://github.com/openMF/mcp-mifosx-self-service)** — Access Apache Fineract self-service APIs for registration, authentication, account management, and transactions via MCP
  <sub>★ 9 · Python · MPL-2.0 · clone · pushed 2026-09-12 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openMF/mcp-mifosx-self-service.git`</sub>
- **[Public APIs MCP](https://github.com/zazencodes/public-apis-mcp)** — Search for free APIs using MCP
  <sub>★ 9 · Python · MIT · npx · pushed 2025-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run public-apis-mcp`</sub>
- **[SchemaFlow](https://github.com/CryptoRadi/schemaflow-mcp-server)** — Real-time PostgreSQL &amp; Supabase database schema access for AI-IDEs via Model Context Protocol. Provides live database context through secure SSE connections with three powerful tools: get_schema, analyze_database, and check_schema_alignment. SchemaFlow
  <sub>★ 9 · JavaScript · MIT · source · pushed 2025-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CryptoRadi/schemaflow-mcp-server.git`</sub>
- **[Latex MCP Server](https://github.com/Yeok-c/latex-mcp-server)** — MCP Server to compile latex, download/organize/read cited papers, run visualization scripts and add figures/tables to latex
  <sub>★ 8 · Python · MIT · uv · pushed 2025-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install -e ./latex-mcp-server`</sub>
- **[Project Manager](https://github.com/croffasia/mcp-project-manager)** — Hierarchical task management (ideas → epics → tasks) with CLI dashboard
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2025-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-project-manager`</sub>
- **[Sonatype MCP Server](https://github.com/brianveltman/sonatype-mcp)** — MCP for Sonatype Nexus Repository Manager and Sonatype Repository Firewall. Manage your DevSecOps practices through AI-assisted Workflows
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-02-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @brianveltman/sonatype-mcp`</sub>
- **[Canvas LMS](https://github.com/ahnopologetic/canvas-lms-mcp)** — MCP server for easy access to education data through your Canvas LMS instance
  <sub>★ 7 · Python · MIT · npx · pushed 2026-02-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @ahnopologetic/canvas-lms-mcp --client claude`</sub>
- **[Chart](https://github.com/KamranBiglari/mcp-server-chart)** — This server offers a wide variety of chart types with comprehensive Zod schema validation for type-safe chart configuration
  <sub>★ 7 · TypeScript · MIT · clone · pushed 2025-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KamranBiglari/mcp-server-chart.git`</sub>
- **[Nextcloud Calendar](https://github.com/Cheffromspace/mcp-nextcloud-calendar)** — CalDAV Nectcloud calendar integration. Manage calendars, events, attendees, etc
  <sub>★ 7 · TypeScript · ISC · npm · pushed 2025-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-nextcloud-calendar`</sub>
- **[spm-mcp](https://github.com/simpleswift/spm-mcp)** — iOS Swift Package Manager server written in Swift
  <sub>★ 7 · Swift · MIT · source · pushed 2025-05-06 · macOS</sub>
  <sub>`git clone https://github.com/simpleswift/spm-mcp.git`</sub>
- **[KnowAir Weather](https://github.com/shuowang-ai/Weather-MCP)** — Real-time weather and air quality via the Caiyun Weather API (meteorology + AQI, CN &amp; US standards)
  <sub>★ 7 · Python · MIT · clone · pushed 2025-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shuowang/Weather-MCP.git`</sub>
- **[Webex](https://github.com/Kashyap-AI-ML-Solutions/webex-messaging-mcp-server)** — A Model Context Protocol (MCP) server that provides AI assistants with comprehensive access to Cisco Webex messaging capabilities
  <sub>★ 7 · JavaScript · MIT · pip · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "git+ssh://git@github.com/Kashyap-AI-ML-Solutions/agentic-media-harness.git#subdirectory=packages/amh"`</sub>
- **[Clojars](https://github.com/Bigsy/Clojars-MCP-Server)** — Obtains latest dependency details for Clojure libraries
  <sub>★ 6 · JavaScript · MIT · npm · pushed 2025-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g clojars-deps-server`</sub>
- **[Exa](https://github.com/theishangoswami/exa-mcp-server)** — Exa AI Search API
  <sub>★ 6 · JavaScript · clone · pushed 2024-11-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/exa-labs/exa-mcp-server.git`</sub>
- **[FrankfurterMCP](https://github.com/anirbanbasu/frankfurtermcp)** — MCP server acting as an interface to the Frankfurter API for currency exchange data
  <sub>★ 6 · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run frankfurtermcp`</sub>
- **[Gentoro](https://github.com/gentoro-GT/mcp-nodejs-server)** — Gentoro generates MCP Servers based on OpenAPI specifications
  <sub>★ 6 · TypeScript · Apache-2.0 · source · pushed 2025-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gentoro-GT/mcp-nodejs-server.git`</sub>
- **[scan-mcp](https://github.com/jacksenechal/scan-mcp)** — Minimal MCP server for scanner capture (ADF/duplex/page-size); typed tools; JSON Schema–validated I/O; multipage assembly; Node 22 + SANE
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx scan-mcp`</sub>
- **[Website Snapshot](https://github.com/gustavo-meilus/mcp-web-snapshot)** — A MCP server that provides comprehensive website snapshot capabilities using Playwright. This server enables LLMs to capture and analyze web pages through structured accessibility snapshots, network monitoring, and console message collection
  <sub>★ 6 · Python · MIT · clone · pushed 2025-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/your-username/mcp-web-snapshot.git`</sub>
- **[Windsor](https://github.com/windsor-ai/windsor_mcp)** — Windsor MCP (Model Context Protocol) enables your LLM to query, explore, and analyze your full-stack business data integrated into Windsor.ai with zero SQL writing or custom scripting
  <sub>★ 6 · MIT · source · pushed 2026-08-19 · Win?</sub>
  <sub>`git clone https://github.com/windsor-ai/windsor_mcp.git`</sub>
- **[Email Send MCP](https://github.com/YUHAI0/email-send-mcp)** — A fixed one from above one. More user-friendly
  <sub>★ 5 · Python · MIT · source · pushed 2025-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YUHAI0/email-send-mcp.git`</sub>
- **[Wassenger](https://github.com/wassengerhq/mcp-wassenger)** — Wassenger MCP server to chat, send messages and automate WhatsApp from any AI model client (free trial available)
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-08-15 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx mcp-wassenger $API_KEY --transport sse-only`</sub>
- **[clj-kondo-MCP](https://github.com/Bigsy/clj-kondo-MCP)** — Clojure linter
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2025-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx clj-kondo-mcp`</sub>
- **[DigitalOcean MCP Server](https://github.com/rohit-kaundal/digitalocean-mcp-server)** — A Model Context Protocol (MCP) server that provides programmatic access to DigitalOcean's API. This server exposes tools for managing droplets, Kubernetes clusters, and container registries through the MCP interface
  <sub>★ 4 · Go · MIT · go · pushed 2025-07-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`go install github.com/rohit-kaundal/digitalocean-mcp-server@latest`</sub>
- **[Fathom Analytics](https://github.com/mackenly/mcp-fathom-analytics)** — Access and analyze Fathom Analytics data and reports
  <sub>★ 4 · TypeScript · MIT · source · pushed 2025-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mackenly/mcp-fathom-analytics.git`</sub>
- **[gx-mcp-server](https://github.com/davidf9999/gx-mcp-server)** — Expose Great Expectations data validation and
  <sub>★ 4 · Python · MIT · docker · pushed 2025-12-14 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i davidf9999/gx-mcp-server:latest`</sub>
- **[Israel Statistics MCP](https://github.com/reuvenaor/israel-statistics-mcp)** — MCP server that provides programmatic access to the Israeli Central Bureau of Statistics (CBS) price indices and economic data
  <sub>★ 4 · TypeScript · MIT · source · pushed 2026-08-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reuvenaor/israel-statistics-mcp.git`</sub>
- **[Lazy Toggl MCP](https://github.com/movstox/lazy-toggl-mcp)** — Simple unofficial MCP server to track time via Toggl API
  <sub>★ 4 · Python · source · pushed 2025-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/movstox/lazy-toggl-mcp.git`</sub>
- **[PBS API](https://github.com/matthewdcage/pbs-mcp-server)** — Access Australian Pharmaceutical Benefits Scheme data for medicine information, pricing, and availability. Built with Python and FastAPI
  <sub>★ 4 · JavaScript · MIT · source · pushed 2025-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/matthewdcage/pbs-mcp-server.git`</sub>
- **[Poland KRS](https://github.com/pkolawa/krs-poland-mcp-server)** — Access to Polish National Court Register (KRS)—the government's authoritative registry of all businesses, foundations, and other legal entities
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx krs-poland-mcp-server`</sub>
- **[Salaah MCP](https://github.com/yusufk/salaah-mcp)** — FastAPI and MCP service providing Islamic prayer times and other useful calculations
  <sub>★ 3 · Python · clone · pushed 2025-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yourusername/salaah-mcp.git`</sub>
- **[Secure Fetch](https://github.com/appsec-innovation-labs/secure-mcp-fetch)** — Secure fetch to prevent access to local resources
  <sub>★ 3 · Python · MIT · source · pushed 2025-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/appsec-innovation-labs/secure-mcp-fetch.git`</sub>
- **[Yuga Planner](https://github.com/blackopsrepl/yuga-planner)** — AI Task schedule planning with LLamaIndex and Timefold: breaks down a task description and schedules it around an existing calendar
  <sub>★ 3 · Python · Apache-2.0 · docker · pushed 2025-08-05 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 7860:7860 yuga-planner`</sub>
- **[Chaitin IP Intelligence](https://github.com/co0ontty/chaitin-ip-intelligence-search-tool)** — Search for IP addresses using Chaitin's IP Intelligence API
  <sub>★ 2 · TypeScript · source · pushed 2025-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/co0ontty/chaitin-ip-intelligence-search-tool.git`</sub>
- **[Jira MCP Server](https://github.com/ahmetbarut/jira-mcp)** — A modular and extensible MCP server designed to interact with Jira Cloud, providing tools to query boards, issues, and user data — ideal for integrating Jira with AI agents, bots, or automation systems
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-02-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ahmetbarut/jira-mcp-server`</sub>
- **[Shadcn Registry Manager](https://github.com/reuvenaor/shadcn-registry-manager)** — MCP server for Shadcn UI, enabling automated, remote, or containerized project management via local or remote registries
  <sub>★ 2 · TypeScript · MIT · source · pushed 2025-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reuvenaor/shadcn-registry-manager.git`</sub>
- **[slite-mcp](https://github.com/fajarmf/slite-mcp)** — Model Context Protocol server for Slite integration. Search and retrieve notes, browse note hierarchies, and access content from your Slite workspace
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fajarmf/slite-mcp.git`</sub>
- **[Squad AI](https://github.com/the-basilisk-ai/squad-mcp)** — Product‑discovery and strategy platform integration. Create, query and update opportunities, solutions, outcomes, requirements and feedback from any MCP‑aware LLM
  <sub>★ 2 · TypeScript · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/the-basilisk-ai/squad-mcp.git`</sub>
- **[xctools](https://github.com/nzrsky/xctools-mcp-server)** — MCP server for Xcode's xctrace, xcrun, xcodebuild
  <sub>★ 2 · Python · MIT · uv · pushed 2025-05-27 · macOS</sub>
  <sub>`uvx xctools-mcp-server`</sub>
- **[AutoGen documentation](https://github.com/sykuang/mcp-autogen-doc)** — A Model Context Protocol (MCP) server that provides AI assistants with the ability to search and retrieve Microsoft AutoGen documentation
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2025-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @sykuang/mcp-autogen-doc`</sub>
- **[MCP Expr Lang](https://github.com/ivan-saorin/mcp-expr-lang)** — MCP Expr-Lang provides a seamless integration between Claude AI and the powerful expr-lang expression evaluation engine
  <sub>★ 1 · Go · MIT · npx · pushed 2025-05-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @ivan-saorin/mcp-expr-lang --client claude`</sub>
- **[Peliqan](https://github.com/Peliqan-io/mcp-server-peliqan)** — Data platform with ETL and built-in data warehouse, access all business applications (ERP, CRM, Accounting etc.) via MCP and run queries on your business data
  <sub>★ 1 · Python · pip · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-server-peliqan`</sub>
- **[run-sql-connectorx](https://github.com/gigamori/mcp-run-sql-connectorx)** — Execute SQL (PostgreSQL, MariaDB, BigQuery, MS SQL Server, RedShift, etc.) via ConnectorX and stream results to CSV/Parquet. MCP tool: run_sql
  <sub>★ 1 · Python · MIT · uv · pushed 2025-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx run-sql-connectorx \`</sub>
- **[xcsimctl](https://github.com/nzrsky/simctl-mcp-server)** — Manage Xcode simulators
  <sub>★ 1 · Python · MIT · uv · pushed 2025-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx simctl-mcp-server`</sub>
- **[AllInOneMCP](https://github.com/particlefuture/MCPDiscovery)** — MCP of MCPs. A central hub for MCP servers. Helps you discover available MCP servers and learn how to install and use them. REMOTE! Use the url https://mcp.pfvc.io/mcp/ to add the server. Remember the final backslash\*\
  <sub>unavailable</sub>
- **[Browser MCP](https://github.com/bytedance/UI-TARS-desktop/tree/main/packages/agent-infra/mcp-servers/browser)** — (by UI-TARS) - A fast, lightweight MCP server that empowers LLMs with browser automation via Puppeteer’s structured accessibility data, featuring optional vision mode for complex visual understanding and flexible, cross-platform configuration
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-09-11</sub>
  <sub>`git clone https://github.com/bytedance/UI-TARS-desktop.git && cd UI-TARS-desktop/packages/agent-infra/mcp-servers/browser`</sub>
- **[Career Site Jobs](https://apify.com/fantastic-jobs/career-site-job-listing-api/api/mcp)** — A MCP server to retrieve up-to-date jobs from company career sites
  <sub>website</sub>
  <sub>`https://apify.com/fantastic-jobs/career-site-job-listing-api/api/mcp`</sub>
- **[ChuckNorris](https://github.com/pollinations/chucknorris-mcp)** — A specialized MCP gateway for LLM enhancement prompts and jailbreaks with dynamic schema adaptation. Provides prompts for different LLMs using an enum-based approach
  <sub>unavailable</sub>
- **[DropBin](https://dropbin.org/mcp)** — Remote SSE MCP server for hosting HTML webpages and sharing content through temporary URLs without authentication
  <sub>website</sub>
  <sub>`https://dropbin.org/mcp`</sub>
- **[DynamoDB-Toolbox](https://www.dynamodbtoolbox.com/docs/databases/actions/mcp-toolkit)** — Leverages your Schemas and Access Patterns to interact with your DynamoDB Database using natural language
  <sub>website</sub>
  <sub>`https://www.dynamodbtoolbox.com/docs/databases/actions/mcp-toolkit`</sub>
- **[GXtract](https://github.com/sascharo/gxtract)** — GXtract is a MCP server designed to integrate with VS Code and other compatible editors (documentation: sascharo.github.io/gxtract). It provides a suite of tools for interacting with the GroundX platform, enabling you to leverage its powerful document understanding capabilities directly within your development environment
  <sub>unavailable</sub>
- **[HAL](https://github.com/dean/HAL)** — HTTP toolkit providing all 7 HTTP methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS) with secret substitution, comprehensive error handling, and support for JSON, XML, HTML, and form data
  <sub>unavailable</sub>
- **[HAP-MCP](https://github.com/mingdaocloud/hap-mcp.git)** — HAP (Super Application Platform) is developed by Mingdao（ https://www.mingdao.com ）The launched APaaS platform helps you build enterprise level applications quickly without coding. This is HAP's MCP (Model Context Protocol) server, used for seamless integration of AI. It enables every zero code application built through HAP to quickly become a tool for agents
  <sub>TypeScript · MIT · npx · pushed 2025-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mingdaocloud/hap-mcp`</sub>
- **[irulescan MCP](https://github.com/simonkowallik/irulescan?tab=readme-ov-file#mcp-server)** — shield: MCP enabled code security analyzer for F5 iRules
  <sub>Rust · MIT · in-repo · pushed 2025-07-07</sub>
  <sub>`git clone https://github.com/simonkowallik/irulescan.git && cd irulescan/?tab=readme-ov-file#mcp-server`</sub>
- **[Nanoleaf](https://github.com/srnetadmin/nanoleaf-mcp-server)** — Control Nanoleaf smart lights through MCP - turn on/off, adjust brightness, change colors, set effects, and discover devices
  <sub>TypeScript · MIT · source · pushed 2025-08-04 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/srnetadmin/nanoleaf-mcp-server.git`</sub>
- **[NodeCodeStudio](https://nodecodestudio.com)** — Activate MCP services (Gmail, Calendar, WordPress, etc.) and run browser automation workflows via a Chrome extension with importable sequences
  <sub>website</sub>
  <sub>`https://nodecodestudio.com`</sub>
- **[Pollinations](https://github.com/pollinations/model-context-protocol)** — Multimodal MCP server for generating images, audio, and text with no authentication required
  <sub>unavailable</sub>
- **[Phabricator](https://github.com/baba786/phabricator-mcp-server)** — Interacting with Phabricator API
  <sub>unavailable</sub>
- **[Repo Map](https://github.com.mcas.ms/pdavis68/RepoMapper)** — An MCP server (and command-line tool) to provide a dynamic map of chat-related files from the repository with their function prototypes and related files in order of relevance. Based on the "Repo Map" functionality in Aider.chat
  <sub>website</sub>
  <sub>`https://github.com.mcas.ms/pdavis68/RepoMapper`</sub>
- **[Renamify](https://docspring.github.io/renamify/mcp/overview/)** — Smart, case-aware search &amp; replace for codebases. Provides atomic renaming of symbols, files, and directories with full undo/redo. The MCP server lets AI assistants plan, preview, and apply rename operations safely, handling all naming conventions (snake_case, camelCase, PascalCase, etc.) automatically
  <sub>website</sub>
  <sub>`https://docspring.github.io/renamify/mcp/overview/`</sub>
- **[Skyvern](https://github.com/Skyvern-AI/skyvern/tree/main/integrations/mcp)** — MCP Server to let Claude / your AI control the browser
  <sub>Python · AGPL-3.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/Skyvern-AI/skyvern.git && cd skyvern/integrations/mcp`</sub>

## Frameworks

- **[ToolHive](https://github.com/stacklok/toolhive)** — A lightweight utility designed to simplify the deployment and management of MCP servers, ensuring ease of use, consistency, and security through containerization
  <sub>★ 2.2k · Go · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Stacklok/toolhive.git`</sub>
- **[mcp-framework](https://github.com/QuantGeekDev/mcp-framework)** — Fast and elegant Typescript framework for building MCP servers
  <sub>★ 930 · TypeScript · MIT · npm · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-framework`</sub>
- **[centralmind/gateway](https://github.com/centralmind/gateway)** — CLI that generates MCP tools based on your Database schema and data using AI and host as REST, MCP or MCP-SSE server
  <sub>★ 549 · Go · Apache-2.0 · clone · pushed 2025-07-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/centralmind/gateway.git`</sub>
- **[LiteMCP](https://github.com/wong2/litemcp)** — A TypeScript framework for building MCP servers elegantly
  <sub>★ 185 · TypeScript · MIT · npx · pushed 2025-04-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx litemcp dev server.js`</sub>
- **[oatpp-mcp](https://github.com/oatpp/oatpp-mcp)** — Anthropic's Model Context Protocol implementation for Oat++
  <sub>★ 49 · C++ · Apache-2.0 · source · pushed 2024-12-13</sub>
  <sub>`git clone https://github.com/oatpp/oatpp-mcp.git`</sub>
- **[MCP Plexus](https://github.com/Super-I-Tech/mcp_plexus)** — A secure, multi-tenant Python MCP server framework built to integrate easily with external services via OAuth 2.1, offering scalable and robust solutions for managing complex AI applications
  <sub>★ 30 · Python · Apache-2.0 · clone · pushed 2025-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Super-I-Tech/mcp_plexus`</sub>
- **[create-mcp-ts](https://github.com/stephencme/create-mcp-ts)** — Create a new MCP server in TypeScript, batteries included - supports user-defined templates!
  <sub>★ 21 · JavaScript · source · pushed 2025-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stephencme/create-mcp-ts.git`</sub>

## Reference Servers

- **[Everything](https://github.com/modelcontextprotocol/servers/blob/main/src/everything)** — Reference / test server with prompts, resources, and tools
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/everything`</sub>
- **[Fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)** — Web content fetching and conversion for efficient LLM usage
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/fetch`</sub>
- **[Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)** — Secure file operations with configurable access controls
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/filesystem`</sub>
- **[Git](https://github.com/modelcontextprotocol/servers/tree/main/src/git)** — Tools to read, search, and manipulate Git repositories
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/git`</sub>
- **[Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** — Knowledge graph-based persistent memory system
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/memory`</sub>
- **[Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)** — Dynamic and reflective problem-solving through thought sequences
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/sequentialthinking`</sub>
- **[Time](https://github.com/modelcontextprotocol/servers/blob/main/src/time)** — Time and timezone conversion capabilities
  <sub>TypeScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/time`</sub>


---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
