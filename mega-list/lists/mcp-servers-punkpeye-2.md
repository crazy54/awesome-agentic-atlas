# MCP Servers (punkpeye)

A collection of MCP servers.

Curated by **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

4,350 entries · 4,341 distinct repos · 59 sections

[← back to the mega list](../README.md)

Page **2** of 6, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · **2** · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) — [continue on page 3 →](mcp-servers-punkpeye-3.md)

## Contents

- [Databases](#databases) (143)
- [Search &amp; Data Extraction](#search--data-extraction) (258)
- [Data Science Tools](#data-science-tools) (46)
- [Data Visualization](#data-visualization) (10)
- [Data Platforms](#data-platforms) (48)
- [end to end RAG platforms](#end-to-end-rag-platforms) (6)
- [Knowledge &amp; Memory](#knowledge--memory) (343)
- [Research](#research) (59)
- [File Systems](#file-systems) (50)
- [Education](#education) (13)

## Databases

<sub>Entries 119–143 of 143. The rest are on this page's other parts, linked above and below.</sub>

- **[dockndevai/mcp-percona-pg](https://github.com/dockndevai/mcp-percona-pg)** — Manage Percona Operator for PostgreSQL clusters: PgBouncer pooling, tuning, backups and PITR, DR and major upgrades, with gated destructive actions
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-percona-pg.git`</sub>
- **[gigamori/mcp-run-sql-connectorx](https://github.com/gigamori/mcp-run-sql-connectorx)** — Execute SQL via ConnectorX and stream results to CSV or Parquet files, supporting PostgreSQL, MariaDB, BigQuery, Redshift, SQL Server and more
  <sub>★ 1 · Python · MIT · uv · pushed 2025-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx run-sql-connectorx \`</sub>
- **[igorolv/jdbc-mcp-server](https://github.com/igorolv/jdbc-mcp-server)** — Read-only access to PostgreSQL, Oracle and SQL Server via JDBC: schema discovery, query validation, execution plans, benchmarking and index analysis
  <sub>★ 1 · Java · Apache-2.0 · source · pushed 2026-09-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/igorolv/jdbc-mcp-server.git`</sub>
- **[mahAnuj/mcp-multi-db](https://github.com/mahAnuj/mcp-multi-db)** — Unified read-only tools for PostgreSQL, MySQL and SQLite: list databases and tables, describe tables and run queries, enforced at SQL and database level
  <sub>★ 1 · TypeScript · ISC · npm · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-multi-db`</sub>
- **[s2-streamstore/mcp](https://github.com/s2-streamstore/mcp)** — Interact with the S2 serverless stream platform
  <sub>★ 1 · Python · source · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/s2-streamstore/mcp.git`</sub>
- **[seob717/redash-mcp](https://github.com/seob717/redash-mcp)** — Redash integration: natural-language SQL with safety guards and PII detection, table selection, saved queries, dashboards, widgets and alerts
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx redash-mcp setup`</sub>
- **[srmadscience/mcpdbwizard-open](https://github.com/srmadscience/mcpdbwizard-open)** — Generate a Java MCP server exposing only selected Oracle PL/SQL packages, tables, sequences and SQL statements as typed tools, with no generic SQL tool
  <sub>★ 1 · Java · Apache-2.0 · source · pushed 2026-10-04</sub>
  <sub>`git clone https://github.com/srmadscience/mcpdbwizard-open.git`</sub>
- **[ThinAirTelematics/thinair-data](https://github.com/ThinAirTelematics/thinair-data)** — Dialect-aware tools for PostgreSQL, MySQL and SQL Server: queries, schema introspection, optimization, migrations and PII scanning
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @thinairtelematics/data`</sub>
- **[croc100/Litescope](https://github.com/croc100/Litescope)** — Operations toolchain for SQLite, Cloudflare D1 and Turso: inspect, diff, migrate, monitor, back up and repair databases. Read-only by default
  <sub>★ 1 · Go · AGPL-3.0 · npm · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g litescope`</sub>
- **[AIops-tools/MySQL-AIops](https://github.com/AIops-tools/MySQL-AIops)** — Governed MySQL + MariaDB DBA operations — slow-query, lock-wait/deadlock, replication, and fragmentation RCA, plus guardrailed writes (35 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, dry-run, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install mysql-aiops # or: pipx install mysql-aiops`</sub>
- **[AIops-tools/Queue-AIops](https://github.com/AIops-tools/Queue-AIops)** — Governed Redis + RabbitMQ operations — memory-pressure, latency, backlog, and churn RCA, plus guardrailed queue and key operations (28 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install queue-aiops`</sub>
- **[AIops-tools/Postgres-AIops](https://github.com/AIops-tools/Postgres-AIops)** — Governed PostgreSQL DBA operations: slow-query, bloat and lock analysis, index management, vacuum and replication lag, with audit logs and rollback
  <sub>Python · MIT · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install postgres-aiops # or: pipx install postgres-aiops`</sub>
- **[elekto-com-br/elekto-mcp-sql](https://github.com/elekto-com-br/elekto-mcp-sql)** — #️⃣ 🏠 🍎 🪟 🐧 - Read-only SQL Server introspection for .NET projects: schema, DDL, dependency graphs, index health and data profiling, reading connection strings from appsettings.json or web.config, and reporting which GRANTs the login lacks
  <sub>C# · GPL-3.0 · source · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/elekto-com-br/elekto-mcp-sql.git`</sub>
- **[infino-ai/infino-mcp](https://github.com/infino-ai/infino-mcp)** — Retrieval over your own data with Infino (BM25 full-text, vector, hybrid and SQL), an embedded engine on Apache Parquet over object storage
  <sub>JavaScript · Apache-2.0 · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @infino-ai/mcp-server`</sub>
- **[memgraph/mcp-memgraph](https://github.com/memgraph/ai-toolkit/tree/main/integrations/mcp-memgraph)** — Run queries against Memgraph and access its schema
  <sub>Python · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/memgraph/ai-toolkit.git && cd ai-toolkit/integrations/mcp-memgraph`</sub>
- **[planetscale/mcp](https://github.com/planetscale/cli?tab=readme-ov-file#mcp-server-integration)** — Built into the PlanetScale CLI: direct access to your PlanetScale databases
  <sub>Go · Apache-2.0 · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/planetscale/cli.git && cd cli/?tab=readme-ov-file#mcp-server-integration`</sub>
- **[quarkiverse/mcp-server-jdbc](https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/jdbc)** — Connect to any JDBC-compatible database to query, insert, update, delete and more
  <sub>Java · Apache-2.0 · in-repo · pushed 2026-06-14</sub>
  <sub>`git clone https://github.com/quarkiverse/quarkus-mcp-servers.git && cd quarkus-mcp-servers/jdbc`</sub>
- **[scoretracker4321/json-mcp-lite](https://github.com/scoretracker4321/json-mcp-lite)** — Serve any JSON file (catalogue, FAQ, price list) as read-only list, keyword search and get-by-id tools over stdio, configured with CLI flags
  <sub>JavaScript · MIT · clone · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scoretracker4321/json-mcp-lite`</sub>
- **[Yusufihsangorgel/queue-inspector-mcp](https://github.com/Yusufihsangorgel/queue-inspector-mcp)** — Inspect and operate Redis-backed Asynq and BullMQ job queues: per-state counts, decoded job payloads and errors, retry and delete, with a read-only mode
  <sub>TypeScript · MIT · npm · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g queue-inspector-mcp`</sub>
- **[Rheopyrin/db-access-mcp](https://github.com/Rheopyrin/db-access-mcp)** — Query PostgreSQL, MySQL, Redshift and SQL Server over SSH or AWS SSM tunnels, with read-only enforcement, confined exports and pluggable secret providers
  <sub>TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @modelcontextprotocol/inspector npx -y @rheopyrin/db-access-mcp`</sub>
- **[Rufflet/mysql-legacy-mcp](https://github.com/Rufflet/mysql-legacy-mcp)** — Access legacy MySQL 5.0 to 5.6 databases: schema inspection and SELECT by default, with opt-in INSERT, UPDATE, DELETE and DDL
  <sub>JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mysql-legacy-mcp`</sub>
- **[seedfast-ai/seedfast-mcp](https://github.com/seedfast-ai/seedfast-mcp)** — Fill a PostgreSQL database with synthetic test data generated from its live schema: plan, run and track seeds without production data
  <sub>JavaScript · MIT · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g seedfast # any platform with Node.js`</sub>
- **[sqemo/sqemo-mcp](https://github.com/sqemo/sqemo-mcp)** — Design ERDs following naming standards: edit entities and relationships, import/export SQL and DBML, and diff the model against a live database
  <sub>Dockerfile · MIT · npx · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sqemo-mcp login # pick Google, GitHub, or email + password`</sub>
- **[wenerme/wener-mssql-mcp](https://github.com/wenerme/wode/tree/develop/packages/wener-mssql-mcp)** — MSSQL database integration with schema inspection and query capabilities
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/wenerme/wode.git && cd wode/packages/wener-mssql-mcp`</sub>
- **[rafim-dev/schema-bridge-mcp](https://github.com/rafim-dev/schema-bridge-mcp)** — Compile SQL and Prisma schemas to Zod, TypeScript and Pydantic, and generate realistic synthetic mock API data
  <sub>TypeScript · MIT · clone · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rafim-dev/schema-bridge-mcp.git`</sub>

## Search &amp; Data Extraction

- **[KnockOutEZ/wigolo](https://github.com/KnockOutEZ/wigolo)** — Local web search, fetching, crawling, extraction and research, with multi-engine search, local ML reranking, a SQLite cache and JavaScript rendering
  <sub>★ 5.5k · TypeScript · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx wigolo init # set up the local engine — any system`</sub>
- **[exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)** — Real-time web search using the Exa AI Search API
  <sub>★ 5.2k · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/exa-labs/exa-mcp-server.git`</sub>
- **[blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server)** — Search arXiv papers, read original LaTeX sections, get BibTeX from arXiv metadata and set topic watches, with papers stored locally
  <sub>★ 3.2k · Python · Apache-2.0 · npx · pushed 2026-10-08 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npx arxiv-mcp-server`</sub>
- **[luminati-io/brightdata-mcp](https://github.com/brightdata/brightdata-mcp)** — Discover, extract and interact with the web via Bright Data, one interface for automated access to the public internet
  <sub>★ 2.7k · JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @brightdata/mcp`</sub>
- **[Aas-ee/open-webSearch](https://github.com/Aas-ee/open-webSearch)** — Multi-engine web search across Bing, Baidu, DuckDuckGo, Brave, Exa and CSDN
  <sub>★ 1.9k · TypeScript · Apache-2.0 · npm · pushed 2026-10-08 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g open-websearch`</sub>
- **[nickclyde/duckduckgo-mcp-server](https://github.com/nickclyde/duckduckgo-mcp-server)** — Web search using DuckDuckGo, with content fetching and parsing
  <sub>★ 1.6k · Python · MIT · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx duckduckgo-mcp-server`</sub>
- **[brave/brave-search-mcp-server](https://github.com/brave/brave-search-mcp-server)** — Web search using Brave's Search API
  <sub>★ 1.5k · TypeScript · MIT · clone · pushed 2026-10-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/brave/brave-search-mcp-server.git`</sub>
- **[Ihor-Sokoliuk/MCP-SearXNG](https://github.com/ihor-sokoliuk/mcp-searxng)** — /☁️ - Web search via SearXNG
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-searxng`</sub>
- **[us/crw](https://github.com/fastcrw/crw)** — Self-hostable web crawler and search API (fastCRW): scraping, crawling, site mapping and SearXNG-backed search
  <sub>★ 1.2k · Rust · AGPL-3.0 · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y crw-mcp@latest install`</sub>
- **[jae-jae/fetcher-mcp](https://github.com/jae-jae/fetcher-mcp)** — Fetch web page content using a Playwright headless browser, supporting JavaScript rendering, content extraction and Markdown or HTML output
  <sub>★ 1.1k · TypeScript · MIT · npx · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y fetcher-mcp`</sub>
- **[kagisearch/kagimcp](https://github.com/kagisearch/kagimcp)** — Search the web with Kagi Search
  <sub>★ 546 · Python · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install kagimcp --client claude`</sub>
- **[jae-jae/g-search-mcp](https://github.com/jae-jae/g-search-mcp)** — Google search with parallel queries for multiple keywords
  <sub>★ 273 · TypeScript · MIT · npx · pushed 2025-06-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y g-search-mcp`</sub>
- **[hellokaton/unsplash-mcp-server](https://github.com/hellokaton/unsplash-mcp-server)** — Unsplash image search
  <sub>★ 237 · Python · MIT · npx · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest install @hellokaton/unsplash-mcp-server --client cursor --key 7558c683-****-****`</sub>
- **[MarcellM01/TinySearch](https://github.com/TinySuiteHQ/TinySearch)** — Self-hosted web research: SearXNG search with DuckDuckGo fallback, crawling, dense and BM25 reranking and deduplication into a cited, source-grounded prompt
  <sub>★ 234 · Python · MIT · uv · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from "tinysuite-search[server]" tinysearch setup`</sub>
- **[reading-plus-ai/mcp-server-deep-research](https://github.com/reading-plus-ai/mcp-server-deep-research)** — Autonomous deep research with structured query elaboration and concise reporting
  <sub>★ 214 · Python · MIT · source · pushed 2025-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reading-plus-ai/mcp-server-deep-research.git`</sub>
- **[deadletterq/mcp-opennutrition](https://github.com/deadletterq/mcp-opennutrition)** — Local search of foods, nutrition facts and barcodes in the OpenNutrition database
  <sub>★ 208 · TypeScript · MIT · docker · pushed 2026-07-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 9113:3000 deadletterq/mcp-opennutrition`</sub>
- **[andybrandt/mcp-simple-arxiv](https://github.com/andybrandt/mcp-simple-arxiv)** — Search and read papers from arXiv
  <sub>★ 201 · Python · MIT · npx · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-simple-arxiv --client claude`</sub>
- **[serpapi/serpapi-mcp](https://github.com/serpapi/serpapi-mcp)** — Search results from Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay and more via SerpApi, plus real-time weather and stock market data
  <sub>★ 181 · Python · MIT · clone · pushed 2026-10-15 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/serpapi/serpapi-mcp.git`</sub>
- **[tinyfish-io/agentql-mcp](https://github.com/tinyfish-io/agentql-mcp)** — Data extraction with AgentQL
  <sub>★ 181 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentql-mcp`</sub>
- **[DasDigitaleMomentum/searxNcrawl](https://github.com/DasDigitaleMomentum/searxNcrawl)** — Web search via your own SearXNG instance and/or You.com, plus page and site crawling to deduplicated Markdown with Crawl4AI and Playwright, including pages behind a login
  <sub>★ 179 · Python · MIT · uv · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx searxncrawl setup`</sub>
- **[lfnovo/content-core](https://github.com/lfnovo/content-core)** — Extract content from web pages, PDFs, Word documents, YouTube transcripts, audio and video with automatic engine selection and structured JSON output
  <sub>★ 179 · Python · MIT · uv · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx content-core extract "https://example.com"`</sub>
- **[fatwang2/search1api-mcp](https://github.com/superagents-lab/search1api-mcp)** — Web search via Search1API
  <sub>★ 173 · TypeScript · npm · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g search1api-cli`</sub>
- **[andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed)** — Search and read medical and life sciences papers from PubMed
  <sub>★ 171 · Python · MIT · npx · pushed 2026-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-simple-pubmed --client claude`</sub>
- **[scrapeless-ai/scrapeless-mcp-server](https://github.com/scrapeless-ai/scrapeless-mcp-server)** — Web search via the Scrapeless Google SERP API
  <sub>★ 169 · TypeScript · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scrapeless-ai/scrapeless-mcp-server.git`</sub>
- **[just-every/mcp-read-website-fast](https://github.com/just-every/mcp-read-website-fast)** — Convert websites to clean Markdown with links preserved, using Mozilla Readability, caching, robots.txt-aware crawling and concurrent fetching
  <sub>★ 163 · TypeScript · MIT · source · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/just-every/mcp-read-website-fast.git`</sub>
- **[konippi/servo-fetch](https://github.com/konippi/servo-fetch)** — Chromium-free web content extraction in a single binary: fetch, render, crawl and screenshot pages with the Servo browser engine
  <sub>★ 162 · Rust · Apache-2.0 · npx · pushed 2026-10-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx servo-fetch "https://example.com"`</sub>
- **[takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp)** — Get the LaTeX source of arXiv papers to handle mathematical content and equations
  <sub>★ 148 · Python · MIT · pip · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install arxiv-latex-mcp`</sub>
- **[nkapila6/mcp-local-rag](https://github.com/nkapila6/mcp-local-rag)** — Primitive RAG-like web search that runs locally, without external APIs
  <sub>★ 134 · Python · MIT · source · pushed 2026-08-31 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nkapila6/mcp-local-rag.git`</sub>
- **[SecretiveShell/MCP-searxng](https://github.com/SecretiveShell/MCP-searxng)** — Connect to SearXNG instances
  <sub>★ 131 · Python · MIT · uv · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-searxng`</sub>
- **[mikechao/brave-search-mcp](https://github.com/mikechao/brave-search-mcp)** — Web, image, news, video and local point-of-interest search using Brave's Search API
  <sub>★ 130 · TypeScript · GPL-3.0 · docker · pushed 2026-05-28 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -p 3001:3001 -e BRAVE_API_KEY="YOUR_API_KEY_HERE" brave-search-mcp:latest --http`</sub>
- **[chanmeng/google-news-mcp-server](https://github.com/ChanMeng666/server-google-news)** — Google News via SerpAPI: search headlines, stories and related topics, with automatic topic categorization and multi-language support
  <sub>★ 129 · TypeScript · MIT · clone · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ChanMeng666/server-google-news`</sub>
- **[vectorize-io/vectorize-mcp-server](https://github.com/vectorize-io/vectorize-mcp-server/)** — Retrieval, private deep research, file-to-Markdown extraction and text chunking via Vectorize
  <sub>★ 115 · TypeScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @vectorize-io/vectorize-mcp-server@latest`</sub>
- **[lennney/agent-search-mcp](https://github.com/lennney/agent-search-mcp)** — Search across DuckDuckGo, Sogou, Bing, Baidu, Wikipedia, Startpage, Yandex and Mojeek with waterfall search, multi-source verification and news search
  <sub>★ 112 · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-search-mcp`</sub>
- **[just-every/mcp-screenshot-website-fast](https://github.com/just-every/mcp-screenshot-website-fast)** — Capture website screenshots, tiling full pages into 1072x1072 chunks for Claude Vision, with configurable viewports and wait strategies for dynamic content
  <sub>★ 110 · TypeScript · MIT · source · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/just-every/mcp-screenshot-website-fast.git`</sub>
- **[Sriram-PR/doc-scraper](https://github.com/Sriram-PR/doc-scraper)** — Crawl documentation sites into local Markdown or JSONL corpora and serve them with offline BM25 search, page reads, freshness checks and crawl diffs
  <sub>★ 107 · Go · Apache-2.0 · go · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/Sriram-PR/doc-scraper/v2/cmd/doc-scraper@latest`</sub>
- **[ConechoAI/openai-websearch-mcp](https://github.com/ConechoAI/openai-websearch-mcp/)** — Expose OpenAI's built-in web search tool
  <sub>★ 94 · Python · MIT · npx · pushed 2025-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx openai-websearch-mcp`</sub>
- **[OctagonAI/octagon-deep-research-mcp](https://github.com/OctagonAI/octagon-deep-research-mcp)** — Deep research agent from Octagon
  <sub>★ 94 · JavaScript · MIT · npm · pushed 2026-02-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g octagon-deep-research-mcp`</sub>
- **[isnow890/naver-search-mcp](https://github.com/isnow890/naver-search-mcp)** — Naver Search API integration: blog, news and shopping search plus DataLab analytics
  <sub>★ 87 · TypeScript · MIT · source · pushed 2026-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/isnow890/naver-search-mcp.git`</sub>
- **[zhsama/duckduckgo-mcp-server](https://github.com/zhsama/duckduckgo-mpc-server/)** — Web search via DuckDuckGo
  <sub>★ 87 · TypeScript · MIT · source · pushed 2025-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zhsama/duckduckgo-mpc-server/.git`</sub>
- **[ricocf/mcp-wolframalpha](https://github.com/akalaric/mcp-wolframalpha)** — Access computational knowledge and data via the Wolfram Alpha API
  <sub>★ 86 · Python · MIT · docker · pushed 2026-01-12 · WSL2 · Linux · Docker</sub>
  <sub>`docker run wolframalphaui`</sub>
- **[NameetP/pdfmux](https://github.com/NameetP/pdfmux)** — PDF extraction router that classifies each page and routes it to PyMuPDF, Docling, OCR or an LLM fallback, re-extracting pages with low confidence scores
  <sub>★ 84 · Python · MIT · pip · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pdfmux`</sub>
- **[zoomeye-ai/mcp_zoomeye](https://github.com/zoomeye-ai/mcp_zoomeye)** — Query network asset information from ZoomEye
  <sub>★ 82 · Python · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx mcp-server-zoomeye`</sub>
- **[leehanchung/bing-search-mcp](https://github.com/leehanchung/bing-search-mcp)** — Web search using the Microsoft Bing Search API
  <sub>★ 81 · Python · MIT · uv · pushed 2025-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx bing-search-mcp`</sub>
- **[erithwik/mcp-hn](https://github.com/erithwik/mcp-hn)** — Search Hacker News, get top stories and more
  <sub>★ 76 · Python · MIT · npx · pushed 2025-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install mcp-hn --client claude`</sub>
- **[reflex-search/reflex](https://github.com/reflex-search/reflex)** — Local, offline full-text code search for coding agents using a trigram index over large codebases
  <sub>★ 76 · Rust · MIT · npm · pushed 2026-10-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g reflex-search`</sub>
- **[Linked-API/linkedapi-mcp](https://github.com/Linked-API/linkedapi-mcp)** — Control LinkedIn accounts and retrieve real-time LinkedIn data
  <sub>★ 70 · TypeScript · MIT · source · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Linked-API/linkedapi-mcp.git`</sub>
- **[zoharbabin/web-researcher-mcp](https://github.com/zoharbabin/web-researcher-mcp)** — Web search via Google, Brave, Serper, SearXNG and SearchAPI.io, multi-tier content extraction, academic and patent search, and multi-source research
  <sub>★ 70 · Go · MIT · winget · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`winget install zoharbabin.web-researcher-mcp`</sub>
- **[goesByhc/cn-scraper-mcp](https://github.com/goesByhc/cn-scraper-mcp)** — Search and extract data from Chinese platforms including Taobao, JD, Xiaohongshu, Zhihu, Weibo, Bilibili, Douban and Dianping, with local cookie storage
  <sub>★ 68 · Python · MIT · pip · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install cn-scraper-mcp`</sub>
- **[0xdaef0f/job-searchoor](https://github.com/0xDAEF0F/job-searchoor)** — Search job listings with filters for date, keywords, remote work options and more
  <sub>★ 65 · JavaScript · MIT · source · pushed 2025-04-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0xDAEF0F/job-searchoor.git`</sub>
- **[tobocop2/lilbee](https://github.com/tobocop2/lilbee)** — Index files, code and crawled websites and answer with source citations, using its own local models or an existing Ollama or LM Studio setup
  <sub>★ 65 · Python · MIT · scoop · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop install lilbee-cuda`</sub>
- **[imprvhub/mcp-domain-availability](https://github.com/imprvhub/mcp-domain-availability)** — Check domain availability across many TLDs with DNS and WHOIS verification, bulk checking and name suggestions
  <sub>★ 61 · Python · MPL-2.0 · npx · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli@latest mcp add imprvhub/mcp-domain-availability --client claude`</sub>
- **[ananddtyagi/webpage-screenshot-mcp](https://github.com/ananddtyagi/webpage-screenshot-mcp)** — Take screenshots of webpages to use as feedback during UI development
  <sub>★ 56 · JavaScript · MIT · clone · pushed 2025-06-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ananddtyagi/webpage-screenshot-mcp.git`</sub>
- **[sifter-ai/sifter](https://github.com/sifter-ai/sifter)** — Extract typed, schema-defined records from any document and query them in natural language like a database
  <sub>★ 54 · Python · MIT · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install sifter-ai`</sub>
- **[Tomatio13/mcp-server-tavily](https://github.com/Tomatio13/mcp-server-tavily)** — Search via the Tavily AI search API
  <sub>★ 50 · Python · MIT · npx · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @smithery/cli install tavily-search --client claude`</sub>
- **[pragmar/mcp-server-webcrawl](https://github.com/pragmar/mcp-server-webcrawl)** — Search and retrieve web crawler data from WARC, wget, Katana, SiteOne and InterroBot crawls
  <sub>★ 46 · Python · pip · pushed 2026-09-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-server-webcrawl`</sub>
- **[webscraping-ai/webscraping-ai-mcp-server](https://github.com/webscraping-ai/webscraping-ai-mcp-server)** — Web data extraction and scraping via WebScraping.ai
  <sub>★ 45 · JavaScript · clone · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/webscraping-ai/webscraping-ai-mcp-server.git`</sub>
- **[ac3xx/mcp-servers-kagi](https://github.com/ac3xx/mcp-servers-kagi)** — Kagi search API integration
  <sub>★ 44 · TypeScript · MIT · source · pushed 2024-12-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ac3xx/mcp-servers-kagi.git`</sub>
- **[DappierAI/dappier-mcp](https://github.com/DappierAI/dappier-mcp)** — Real-time web search and premium data from media brands via Dappier: news, financial markets, sports, entertainment, weather and more
  <sub>★ 44 · Python · MIT · npx · pushed 2025-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @DappierAI/dappier-mcp --client claude`</sub>
- **[trendsmcp-ai/Trends-MCP](https://github.com/trendsmcp-ai/Trends-MCP)** — Live trend data from Google, TikTok, YouTube, Amazon, Reddit, npm, Steam and other sources
  <sub>★ 44 · Python · MIT · pip · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install trendsmcp`</sub>
- **[czottmann/kagi-ken-mcp](https://github.com/czottmann/kagi-ken-mcp)** — Kagi search and summarization without API access, authenticated with a Kagi session token
  <sub>★ 42 · JavaScript · MIT · npx · pushed 2026-02-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:czottmann/kagi-ken-mcp`</sub>
- **[XZXZZX-Ai/bilibili-mcp](https://github.com/XZXZZX-Ai/bilibili-mcp)** — Local-first Bilibili MCP server for video metadata, subtitles and structured transcripts, chapters, popular comments, and optional local ASR fallback. Published on npm as @xzxzzx/bilibili-mcp with bilingual documentation
  <sub>★ 39 · Python · Apache-2.0 · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @xzxzzx/bilibili-mcp@latest setup`</sub>
- **[yamanoku/baseline-mcp-server](https://github.com/yamanoku/baseline-mcp-server)** — Search Baseline status using the Web Platform API
  <sub>★ 37 · TypeScript · MIT · source · pushed 2026-10-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/yamanoku/baseline-mcp-server.git`</sub>
- **[pranciskus/newsmcp](https://github.com/pranciskus/newsmcp)** — Real-time world news: events clustered from many sources, classified by topic and geography and ranked by importance
  <sub>★ 34 · TypeScript · MIT · npx · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @newsmcp/server --client claude`</sub>
- **[cevatkerim/unsplash-mcp](https://github.com/cevatkerim/unsplash-mcp)** — Unsplash photo search, random photos and download tracking, with ready-to-use attribution text and HTML for each photo
  <sub>★ 32 · Python · MIT · clone · pushed 2026-01-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cevatkerim/unsplash-mcp.git`</sub>
- **[format37/youtube_mcp](https://github.com/format37/youtube_mcp)** — Transcribe YouTube videos to text using yt-dlp for audio and OpenAI Whisper for transcription, with chunked output for long videos
  <sub>★ 32 · Python · clone · pushed 2025-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/format37/youtube_mcp.git`</sub>
- **[Dumpling-AI/mcp-server-dumplingai](https://github.com/DumplingAI/mcp-server-dumplingai)** — Access Dumpling AI's data, web scraping and document conversion APIs
  <sub>★ 30 · JavaScript · MIT · npm · pushed 2025-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-server-dumplingai`</sub>
- **[dorukardahan/domain-search-mcp](https://github.com/dorukardahan/domain-search-mcp)** — Domain availability and prices from Porkbun, Namecheap, GoDaddy, RDAP and WHOIS, with bulk search, registrar comparison, suggestions and social handle checks
  <sub>★ 28 · TypeScript · MIT · npx · pushed 2026-10-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y domain-search-mcp@latest`</sub>
- **[joelio/stocky](https://github.com/joelio/stocky)** — Search and download royalty-free stock photos from Pexels and Unsplash, with rich metadata and pagination
  <sub>★ 28 · Python · MIT · uv · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install stocky-mcp # or: pipx install stocky-mcp`</sub>
- **[FayAndXan/spectrawl](https://github.com/Pyx-Corp/spectrawl)** — Unified web layer for agents: multi-engine search including Gemini Grounded Search, stealth browsing, cookie auth and actions across many platforms
  <sub>★ 28 · JavaScript · MIT · npx · pushed 2026-03-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx spectrawl config set proxy '{"host":"brd.superproxy.io","port":22225,"username":"YOUR_ZONE_USER","password":"YOUR_PASS"}'`</sub>
- **[imprvhub/mcp-rss-aggregator](https://github.com/imprvhub/mcp-rss-aggregator)** — Aggregate RSS feeds
  <sub>★ 27 · TypeScript · MPL-2.0 · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest mcp add imprvhub/mcp-rss-aggregator --client claude`</sub>
- **[telly6/searchpin](https://github.com/telly6/searchpin)** — Multi-engine parallel web search with re-ranking that works within China's network without a proxy or VPN
  <sub>★ 27 · Python · pip · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install searchpin`</sub>
- **[hbg/mcp-paperswithcode](https://github.com/hbg/mcp-paperswithcode)** — Search papers via the Papers with Code API
  <sub>★ 26 · Python · MIT · npx · pushed 2025-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @hbg/mcp-paperswithcode --client claude`</sub>
- **[kehvinbehvin/json-mcp-filter](https://github.com/kehvinbehvin/json-mcp-filter)** — Query and extract only the needed parts of JSON files to keep LLM context small
  <sub>★ 26 · JavaScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g json-mcp-filter@latest`</sub>
- **[parallel-web/search-mcp](https://github.com/parallel-web/search-mcp)** — Web search for AI via Parallel
  <sub>★ 26 · MIT · source · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/parallel-web/search-mcp.git`</sub>
- **[jhomen368/overseerr-mcp](https://github.com/jhomen368/overseerr-mcp)** — Media discovery, requests and management via Overseerr and Seerr for Plex, Jellyfin and Emby
  <sub>★ 25 · TypeScript · MIT · npm · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @jhomen368/overseerr-mcp`</sub>
- **[r-huijts/opentk-mcp](https://github.com/r-huijts/opentk-mcp)** — Search Dutch Parliament (Tweede Kamer) documents, debates, activities and legislative cases, based on the OpenTK project
  <sub>★ 23 · HTML · MIT · npx · pushed 2025-10-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @r-huijts/opentk-mcp`</sub>
- **[adawalli/nexus](https://github.com/adawalli/nexus)** — Web search using Perplexity Sonar models, with source citations
  <sub>★ 22 · TypeScript · MIT · npx · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`bunx nexus-mcp`</sub>
- **[Himalayas-App/himalayas-mcp](https://github.com/Himalayas-App/himalayas-mcp)** — Real-time access to remote job listings and company information from the Himalayas jobs database
  <sub>★ 21 · MIT · source · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Himalayas-App/himalayas-mcp.git`</sub>
- **[oso95/domain-suite-mcp](https://github.com/oso95/domain-suite-mcp)** — Domain lifecycle management across Porkbun, Namecheap, GoDaddy and Cloudflare: availability, registration, DNS, SSL, email auth (SPF, DKIM, DMARC) and WHOIS
  <sub>★ 20 · TypeScript · MIT · npm · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g domain-suite-mcp`</sub>
- **[HasData/hasdata-mcp](https://github.com/HasData/hasdata-mcp)** — Structured data APIs for Google Search, Maps, Trends and Flights, Amazon, Airbnb, Zillow, Yelp and more, returning clean JSON
  <sub>★ 20 · JavaScript · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/hasdata-mcp.git`</sub>
- **[rejifald/StitchAPI](https://github.com/rejifald/StitchAPI)** — Semantic search over the StitchAPI documentation, returning relevant sections with deep links and full pages
  <sub>★ 20 · TypeScript · Apache-2.0 · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rejifald/StitchAPI.git`</sub>
- **[wd041216-bit/free-web-search-ultimate](https://github.com/wd041216-bit/zero-api-key-web-search)** — Web search across DuckDuckGo, Bing, Google, Brave, Wikipedia, arXiv, YouTube and Reddit with deep page browsing. Instructs LLMs to search before answering
  <sub>★ 19 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zero-api-key-web-search # free search, no API key, no model download`</sub>
- **[n24q02m/wet-mcp](https://github.com/n24q02m/wet)** — Web search via embedded SearXNG, content extraction and library docs indexing with hybrid FTS5 and semantic search using built-in Qwen3 embeddings
  <sub>★ 19 · Python · Apache-2.0 · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx wet-mcp --help # or `wet <tool>` for direct tool calls`</sub>
- **[angheljf/nyt](https://github.com/angheljf/nyt)** — Search articles using the NYTimes API
  <sub>★ 18 · JavaScript · MIT · npx · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install nyt --client claude`</sub>
- **[the0807/GeekNews-MCP-Server](https://github.com/the0807/GeekNews-MCP-Server)** — Retrieve and process news from GeekNews
  <sub>★ 18 · Python · MIT · clone · pushed 2025-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/the0807/GeekNews-MCP-Server`</sub>
- **[cameronrye/activitypub-mcp](https://github.com/cameronrye/activitypub-mcp)** — Explore and interact with the Fediverse via ActivityPub: WebFinger discovery, timelines and instance exploration across Mastodon, Pleroma, Misskey and more
  <sub>★ 17 · TypeScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y activitypub-mcp`</sub>
- **[Role1776/mcp-retrieval](https://github.com/Role1776/mcp-retrieval)** — Read-only web search via DuckDuckGo Lite, image search via Bing Images and page-to-Markdown scraping with a readability extractor
  <sub>★ 17 · Go · MIT · go · pushed 2026-10-09 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/Role1776/mcp-retrieval/app/cmd/mcp-retrieval@latest # needs Go 1.25.5+`</sub>
- **[andyliszewski/webcrawl-mcp](https://github.com/andyliszewski/webcrawl-mcp)** — Local-first web scraping, DuckDuckGo search, site mapping and crawling, using trafilatura with an optional Firecrawl fallback for JS-rendered pages
  <sub>★ 16 · Python · MIT · pip · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install webcrawl-mcp`</sub>
- **[gemy411/multi-research-agents](https://github.com/gemy411/multi-agents-research)** — Multi-agent research system for coding or general research tasks
  <sub>★ 16 · Kotlin · MIT · source · pushed 2026-03-19</sub>
  <sub>`git clone https://github.com/gemy411/multi-agents-research.git`</sub>
- **[MikkoParkkola/nab](https://github.com/MikkoParkkola/nab)** — Fetch any URL as clean Markdown, with HTTP/3, JS rendering, anti-fingerprinting, browser cookie auth and 1Password integration
  <sub>★ 16 · Rust · MIT · cargo · pushed 2026-10-22 · macOS</sub>
  <sub>`cargo binstall nab`</sub>
- **[parallel-web/task-mcp](https://github.com/parallel-web/task-mcp)** — Deep research and batch task execution via Parallel
  <sub>★ 16 · TypeScript · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/parallel-web/task-mcp.git`</sub>
- **[cameronrye/gopher-mcp](https://github.com/cameronrye/gopher-mcp)** — Browse Gopher and Gemini protocol resources, with TLS support and structured content extraction
  <sub>★ 15 · Python · MIT · uv · pushed 2026-10-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx gopher-mcp`</sub>
- **[KyuRish/fiverr-mcp-server](https://github.com/KyuRish/mcp-server-for-fiverr-unofficial)** — Search Fiverr gigs, view seller profiles, compare gig packages and read reviews
  <sub>★ 15 · Python · MIT · pip · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install fiverr-mcp-server`</sub>
- **[tianqitang1/enrichr-mcp-server](https://github.com/tianqitang1/enrichr-mcp-server)** — Gene set enrichment analysis using the Enrichr API
  <sub>★ 15 · TypeScript · npx · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install enrichr-mcp-server --client claude`</sub>
- **[vitorpavinato/ncbi-mcp-server](https://github.com/vitorpavinato/ncbi-mcp-server)** — NCBI and PubMed literature search with analytics, caching, MeSH integration, related article discovery and batch processing for life sciences research
  <sub>★ 13 · Python · source · pushed 2025-06-28 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/vitorpavinato/ncbi-mcp-server.git`</sub>
- **[emicklei/melrose-mcp](https://github.com/emicklei/melrose-mcp)** — Play Melrōse music expressions as MIDI
  <sub>★ 12 · Go · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/emicklei/melrose-mcp.git`</sub>
- **[kshern/mcp-tavily](https://github.com/kshern/mcp-tavily.git)** — Search via the Tavily AI search API
  <sub>★ 12 · JavaScript · MIT · npx · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @kshern/mcp-tavily --client claude`</sub>
- **[whw23/searxng-http-mcp](https://github.com/whw23/searxng_http_mcp)** — Self-contained SearXNG in Docker: metasearch across many engines and categories with multi-page fanout, autocomplete, engine discovery and a Web UI proxy
  <sub>★ 12 · Python · MIT · uv · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx searxng-http-mcp`</sub>
- **[JerryLiu369/agent-web-search](https://github.com/JerryLiu369/agent-web-search)** — Provider-neutral web search aggregating model grounding (Gemini, Grok, DeepSeek and others) and search APIs such as Exa, Brave, Perplexity and Tavily
  <sub>★ 11 · Python · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add JerryLiu369/agent-web-search --skill agent-web-search`</sub>
- **[Crawleo/Crawleo-MCP](https://github.com/Crawleo/Crawleo-MCP)** — Real-time web search and crawling via the Crawleo Search and Crawl API
  <sub>★ 11 · JavaScript · MIT · npm · pushed 2025-12-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g crawleo-mcp`</sub>
- **[HasData/indeed-mcp](https://github.com/HasData/indeed-mcp)** — Remote MCP server for Indeed: job listings by keyword and location with salary, company and posting date, plus full job postings, as JSON
  <sub>★ 11 · JavaScript · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/indeed-mcp.git`</sub>
- **[serkan-ozal/driflyte-mcp-server](https://github.com/serkan-ozal/driflyte-mcp-server)** — Query and retrieve topic-specific knowledge from recursively crawled and indexed web pages via Driflyte
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2025-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @serkan-ozal/driflyte-mcp-server --client <SMITHERY-CLIENT-NAME> --key <SMITHERY-API-KEY>`</sub>
- **[HasData/web-scraping-mcp](https://github.com/HasData/web-scraping-mcp)** — Web scraping: fetch public pages with optional JavaScript rendering, wait conditions and CSS or AI extraction rules, as Markdown, text, HTML or JSON
  <sub>★ 10 · JavaScript · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/web-scraping-mcp.git`</sub>
- **[echology-io/decompose](https://github.com/echology-io/decompose)** — Deterministically decompose text into classified semantic units with authority, risk and attention scores plus entity extraction, without an LLM
  <sub>★ 10 · Python · MIT · pip · pushed 2026-05-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install decompose-mcp`</sub>
- **[HughesCuit/heventure-search-mcp](https://github.com/HughesCuit/heventure-search-mcp)** — Web search across DuckDuckGo, Bing, Google (via SerpAPI) and Tavily with automatic rate limiting, caching and multi-language support
  <sub>★ 10 · Python · pip · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install heventure-search-mcp`</sub>
- **[imprvhub/mcp-claude-hackernews](https://github.com/imprvhub/mcp-claude-hackernews)** — Interact with Hacker News
  <sub>★ 10 · TypeScript · MPL-2.0 · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest mcp add imprvhub/mcp-claude-hackernews --client claude`</sub>
- **[linxule/mineru-mcp](https://github.com/linxule/mineru-mcp)** — Parse PDFs, images, DOCX and PPTX via the MinerU document parsing API, with multilingual OCR, batch processing, page ranges and local file upload
  <sub>★ 10 · TypeScript · MIT · bun · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bun add -g mineru-mcp`</sub>
- **[HasData/bing-mcp](https://github.com/HasData/bing-mcp)** — Bing search results as JSON: organic results, ads and the Copilot answer, targeted by market, country, language and device
  <sub>★ 9 · JavaScript · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/bing-mcp.git`</sub>
- **[AutomateLab-tech/citation-intelligence](https://github.com/AutomateLab-tech/citation-intelligence)** — Check which URLs Perplexity, Claude, ChatGPT, Gemini, Bing and Google AI Overviews cite for any query. Self-hosted
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-10-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @automatelab/citation-intelligence`</sub>
- **[Pearch-ai/mcp_pearch](https://github.com/Pearch-ai/mcp_pearch)** — People search engine for talent discovery
  <sub>★ 9 · Python · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pearch-ai/mcp_pearch.git`</sub>
- **[searchcraft-inc/searchcraft-mcp-server](https://github.com/searchcraft-inc/searchcraft-mcp-server)** — Manage Searchcraft clusters, create search indexes, generate an index from a data file and import data from a feed or local JSON file
  <sub>★ 9 · TypeScript · Apache-2.0 · source · pushed 2026-02-07 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/searchcraft-inc/searchcraft-mcp-server.git`</sub>
- **[shopsavvy/shopsavvy-mcp-server](https://github.com/shopsavvy/shopsavvy-mcp-server)** — ShopSavvy product and price data: search by barcode, ASIN or URL, get product details, compare retailer prices and track price history
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @shopsavvy/mcp-server`</sub>
- **[HasData/google-images-mcp](https://github.com/HasData/google-images-mcp)** — Remote MCP server for Google Images: image results with source pages, thumbnails and full-resolution URLs, filtered by size, colour and type, as JSON
  <sub>★ 8 · JavaScript · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/google-images-mcp.git`</sub>
- **[scavio-ai/scavio-mcp](https://github.com/scavio-ai/scavio-mcp)** — Unified real-time search across Google, YouTube, Amazon, Walmart, Reddit and TikTok for web, e-commerce, product, social media and video data
  <sub>★ 8 · TypeScript · MIT · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scavio-ai/scavio-mcp.git`</sub>
- **[boikot-xyz/boikot](https://github.com/boikot-xyz/boikot)** — Look up company ethics information: the ethical and unethical actions of major companies
  <sub>★ 8 · HTML · GPL-3.0 · source · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/boikot-xyz/boikot.git`</sub>
- **[mikusnuz/gsc-mcp](https://github.com/mikusnuz/gsc-mcp)** — Google Search Console and Indexing API: search analytics, sitemaps, URL inspection and batch indexing
  <sub>★ 8 · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mikusnuz/gsc-mcp.git`</sub>
- **[fouradata/mcp](https://github.com/fouradata/mcp)** — Web scraping that escalates from direct fetch to rotating proxy to full browser, solving anti-bot challenges and reporting which step worked and its cost
  <sub>★ 7 · JavaScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @fouradata/mcp`</sub>
- **[shariqriazz/google-ai-search-mcp](https://github.com/shariqriazz/google-ai-search-mcp)** — Search, documentation retrieval, code analysis and architecture research powered by Google's Vertex AI or the Gemini API
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`bunx google-ai-search-mcp`</sub>
- **[Khamel83/argus](https://github.com/Khamel83/argus)** — Multi-provider search broker with automatic fallback, RRF ranking, content extraction and budget enforcement
  <sub>★ 6 · Python · MIT · pipx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install argus-search[mcp]`</sub>
- **[Bigsy/Clojars-MCP-Server](https://github.com/Bigsy/Clojars-MCP-Server)** — Up-to-date dependency information for Clojure libraries from Clojars
  <sub>★ 6 · JavaScript · MIT · npm · pushed 2025-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g clojars-deps-server`</sub>
- **[keenableai/keenable-mcp](https://github.com/keenableai/keenable-mcp)** — Live web search and clean Markdown page fetching over the Keenable web index
  <sub>★ 6 · Shell · MIT · source · pushed 2026-10-13</sub>
  <sub>`git clone https://github.com/keenableai/keenable-mcp.git`</sub>
- **[Vincentwei1021/agent-toolbox](https://github.com/Vincentwei1021/agent-toolbox)** — Web search, content extraction, screenshots, weather, finance, email validation, translation, news, GeoIP, WHOIS, DNS, PDF extraction and QR codes
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g agent-toolbox-mcp`</sub>
- **[zlatkoc/youtube-summarize](https://github.com/zlatkoc/youtube-summarize)** — Fetch YouTube transcripts in text, JSON, SRT or WebVTT format and in multiple languages, and optionally summarize them
  <sub>★ 6 · Python · MIT · uv · pushed 2026-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx youtube-summarize`</sub>
- **[AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl)** — Crawl websites into clean Markdown, search pages and extract structured data with LLMs for web research and RAG pipelines
  <sub>★ 5 · Python · MIT · npx · pushed 2026-09-23 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx clawhub install markcrawl-skill`</sub>
- **[AntonG87/codearia-sieve](https://github.com/AntonG87/codearia-sieve)** — Deterministically convert web pages into decision-ready state: ISO dates, numbers with units as facts and token-budgeted chunks anchored to the page
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx codearia-sieve # MCP server for Claude Code, Cursor and any agent`</sub>
- **[kc23go/anybrowse](https://github.com/kc23go/anybrowse)** — Scrape, crawl and search the web, converting any URL to LLM-ready Markdown via real Chrome browsers
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kc23go/anybrowse.git`</sub>
- **[lulzasaur9192/marketplace-search-mcp](https://github.com/lulzasaur9192/marketplace-search-mcp)** — Search TCGPlayer, Reverb and Thumbtack, verify US contractor and nurse licenses, and look up PSA card grading population data
  <sub>★ 5 · TypeScript · npx · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @lulzasaur9192/marketplace-search-mcp`</sub>
- **[nyxn-ai/NyxDocs](https://github.com/nyxn-ai/NyxDocs)** — Manage cryptocurrency project documentation across Ethereum, BSC, Polygon and Solana
  <sub>★ 5 · Python · MIT · clone · pushed 2025-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nyxn-ai/NyxDocs.git`</sub>
- **[qune-tech/ocds-mcp](https://github.com/qune-tech/vergabe-mcp)** — German public procurement data (OCDS): semantic search, tender matching against company profiles and structured filtering
  <sub>★ 5 · Rust · MIT · npx · pushed 2026-07-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @qune-tech/vergabe-mcp --api-key sk_live_YOUR_KEY_HERE`</sub>
- **[scraperapi/scraperapi-mcp](https://github.com/scraperapi/scraperapi-mcp)** — Web scraping via ScraperAPI with JavaScript rendering, geotargeting, premium proxies and auto-parsing
  <sub>★ 5 · Python · MIT · pip · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install scraperapi-mcp-server`</sub>
- **[talonicdev/talonic-mcp](https://github.com/talonicdev/talonic-mcp)** — Schema-validated extraction of structured fields from PDFs, scans, images and forms, with searchable memory of past extractions
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @talonic/mcp@latest --version`</sub>
- **[robbyczgw-cla/web-search-plus-mcp](https://github.com/robbyczgw-cla/web-search-plus-mcp)** — Multi-provider web search with automatic routing between Serper, Tavily and Exa
  <sub>★ 5 · Python · MIT · uv · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx web-search-plus-mcp`</sub>
- **[usestring/string-ai-mcp](https://github.com/usestring/string-ai-mcp)** — Search the web, fetch URLs and map sites as clean Markdown, getting past anti-bot blocks
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @usestring/mcp`</sub>
- **[mrslbt/rippr](https://github.com/mrslbt/rippr)** — Extract YouTube transcripts as clean text, with timestamps, or as structured JSON
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rippr-mcp`</sub>
- **[hanselhansel/aeo-cli](https://github.com/hanselhansel/context-cli)** — Audit URLs for AI crawler readiness: checks robots.txt, llms.txt, JSON-LD schema and content density, with a 0-100 AEO score
  <sub>★ 4 · Python · MIT · gh-action · pushed 2026-03-17</sub>
  <sub>`uses: hanselhansel/aeo-cli@main # in .github/workflows/*.yml`</sub>
- **[lucasmartins-ai/lookacrawler](https://github.com/lucasmartins-ai/lookacrawler)** — Token-efficient local web crawler with Playwright-based stealth anti-bot bypass
  <sub>★ 4 · TypeScript · MIT · docker · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 -e LOOKACRAWLER_SSE_TOKEN="$(openssl rand -hex 24)" lookacrawler`</sub>
- **[atlasprzetargow/mcp-server](https://github.com/atlasprzetargow/mcp-server)** — Search Polish public tenders (BZP and TED): procuring entity and contractor profiles by NIP, market statistics by CPV or province, and a procurement glossary
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @atlasprzetargow/mcp`</sub>
- **[goofrey/zoom-search](https://github.com/goofrey/zoom-search)** — Rewrite queries, zoom into source domains and return sourced answers with metrics
  <sub>★ 4 · Python · MIT · pip · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zoom-search`</sub>
- **[lionkiii/rss-feeds-mcp](https://github.com/lionkiii/rss-feeds-mcp)** — Fetch, filter, search and manage RSS feeds by category or source
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lionkiii/rss-feeds-mcp.git`</sub>
- **[kimdonghwi94/Web-Analyzer-MCP](https://github.com/kimdonghwi94/web-analyzer-mcp)** — Extract clean web content for RAG and answer questions about web pages
  <sub>★ 4 · Python · MIT · npx · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @kimdonghwi94/web-analyzer-mcp --client claude`</sub>
- **[maxylev/searchfetch](https://github.com/maxylev/searchfetch)** — Fault-tolerant, stealth-enabled web search and content fetching
  <sub>★ 4 · Python · MIT · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y searchfetch`</sub>
- **[paulieb89/govuk-mcp](https://github.com/paulieb89/govuk-mcp)** — Search GOV.UK content, retrieve full government pages, look up organisations and resolve UK postcodes to local authorities. Read-only
  <sub>★ 4 · Python · MIT · source · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/paulieb89/govuk-mcp.git`</sub>
- **[chasesaurabh/mcp-page-capture](https://github.com/chasesaurabh/mcp-page-capture)** — Capture webpage screenshots, viewport or full-page, as base64 PNG
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2025-12-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g mcp-page-capture`</sub>
- **[comparedge/mcp-server-comparedge](https://github.com/comparedge/mcp-server-comparedge)** — Plans, prices, hidden costs, alternatives and comparisons for SaaS, AI and LLM tools
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/comparedge/mcp-server-comparedge.git`</sub>
- **[gregm711/agent-domain-service-mcp](https://github.com/gregm711/agent-domain-service-mcp)** — Domain brainstorming via AgentDomainService: generate names from descriptions, score brandability and memorability, and check availability and prices
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2025-12-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-domain-service-mcp`</sub>
- **[JessieJanie/skim402](https://github.com/JessieJanie/skim402)** — Convert any URL into clean Markdown with structured metadata (title, byline, published date, language), paid per use via x402
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JessieJanie/skim402.git`</sub>
- **[ni-c/freshrss-mcp](https://github.com/ni-c/freshrss-mcp)** — Read and manage a self-hosted FreshRSS instance: feeds, categories, labels, articles, read and star state, and OPML import and export
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-10-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/freshrss-mcp.git`</sub>
- **[Prototypr/feedbagel-mcp](https://github.com/Prototypr/feedbagel-mcp)** — Search the Feedbagel RSS catalog, follow feeds and route new entries to webhooks
  <sub>★ 3 · TypeScript · npm · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g feedbagel-mcp`</sub>
- **[urlbox/urlbox-mcp-server](https://github.com/urlbox/urlbox-mcp-server/)** — Generate and manage screenshots, PDFs and videos, analyze screenshots with AI and extract web content as Markdown, metadata or HTML via the Urlbox API
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/urlbox/urlbox-mcp-server/.git`</sub>
- **[ashlrai/webfetch](https://github.com/ashlrai/webfetch)** — License-aware federated image search across many providers, returning license tags, attribution strings, dimensions and download URLs
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g getwebfetch`</sub>
- **[Alisammour/storyflo-mcp](https://github.com/Alisammour/storyflo-mcp)** — Curated audio news: search articles, fetch narrated audio, subscribe to topic feeds and surface stories matched to actively traded Kalshi event contracts
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-07-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx storyflo-mcp # or: node src/index.js`</sub>
- **[denyn1/aifeed-protocol](https://github.com/denyn1/aifeed-protocol)** — AIFeed protocol tools: verify signed publisher manifests, fetch token-budgeted Markdown or MAKO pages, verify asset downloads and rank delta-index entries
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx aifeed keygen --out .aifeed # Ed25519 key pair`</sub>
- **[idapixl/idapixl-web-research-mcp](https://github.com/idapixl/idapixl-web-research-mcp)** — Web research on Apify: Brave and DuckDuckGo search, page fetching to clean Markdown, and multi-step research with relevance scoring and key fact extraction
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/idapixl/idapixl-web-research-mcp.git`</sub>
- **[BenyD/haypile](https://github.com/BenyD/haypile)** — Local hybrid semantic and keyword search over PDF, DOCX, PPTX, Markdown and HTML documents, with file and page citations and a bundled embedding model
  <sub>★ 2 · Go · AGPL-3.0 · psh · pushed 2026-10-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://haypile.sh/install.ps1 | iex`</sub>
- **[bumbaRasch/searxng-mcp-server](https://github.com/bumbaRasch/searxng-mcp-server)** — Self-hosted SearXNG metasearch: web, image, news, video and music search plus SSRF-guarded page fetch with prompt-injection wrapping
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector npx -y searxng-mcp-server`</sub>
- **[capad-xyz/searchts](https://github.com/capad-xyz/searchts)** — Read bot-walled pages as Markdown via an escalating unlocker, plus multi-provider web search with rank fusion, video transcripts and page asset grabbing
  <sub>★ 2 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from "searchts[mcp]" searchts <verb>`</sub>
- **[dariomory/trendflow-js](https://github.com/dariomory/trendflow-js)** — Google Trends data: interest over time, interest by region, trending now, related queries and topic search
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:dariomory/trendflow-js.git`</sub>
- **[dealx/mcp-server](https://github.com/DealExpress/mcp-server)** — Integration with the DealX platform
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @dealx/mcp-server`</sub>
- **[divyanshu-iitian/SearchForge](https://github.com/divyanshu-iitian/SearchForge)** — Capability-routed search and web reading across GitHub, Crossref, Hacker News, Wikipedia and private SearXNG, plus URL-to-Markdown and health diagnostics
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx --yes --package github:divyanshu-iitian/SearchForge \`</sub>
- **[ekas-io/open-sales-stack](https://github.com/ekas-io/open-sales-stack)** — Collection of B2B sales intelligence servers: website analysis, tech stack detection, hiring signals, review aggregation, ad tracking and social profiles
  <sub>★ 2 · Python · MIT · clone · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ekas-io/open-sales-stack.git`</sub>
- **[echojobsio/jdl-mcp-server](https://github.com/echojobsio/jdl-mcp-server)** — Search JobDataLake's enriched job listings with filters for skills, salary, location, seniority, remote type and more
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/echojobsio/jdl-mcp-server.git`</sub>
- **[getrephonic/rephonic-mcp](https://github.com/getrephonic/rephonic-mcp)** — Search Rephonic podcast and episode data: listener estimates, demographics, contacts, transcripts, chart rankings, sponsors, reviews and audience overlap
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/getrephonic/rephonic-mcp.git`</sub>
- **[hanoak/unsplash-mcp-server](https://github.com/hanoak/unsplash-mcp-server)** — Unsplash API: photos, search, users, collections, topics and stats, with guideline-compliant attribution, download tracking and rate-limit reporting
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @hanoak/unsplash-mcp-server login`</sub>
- **[mambalabsdev/mcp-domain-to-linkedin-url-resolver](https://github.com/mambalabsdev/mcp-domain-to-linkedin-url-resolver)** — Resolve a company domain or name to its LinkedIn company URL, with confidence scoring and firmographic metadata
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-domain-to-linkedin-url-resolver.git`</sub>
- **[mambalabsdev/mcp-job-board-keyword-signal-scanner](https://github.com/mambalabsdev/mcp-job-board-keyword-signal-scanner)** — Scan job boards on five ATS platforms for configurable role categories (GTM, engineering, finance, ops), returning keyword match counts and signal strength
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-job-board-keyword-signal-scanner.git`</sub>
- **[omniologynow-rgb/scout-intel-mcp](https://github.com/omniologynow-rgb/scout-intel-mcp)** — Web intelligence: SERP analysis, competitor research, market trends, content gap analysis, keyword insights, audience discovery and citation tracking
  <sub>★ 2 · Python · AGPL-3.0 · pip · pushed 2026-05-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install scout-mcp`</sub>
- **[QuentinCody/catalysishub-mcp-server](https://github.com/QuentinCody/catalysishub-mcp-server)** — Unofficial access to the Catalysis Hub database: search and retrieve computational catalysis research and surface reaction data
  <sub>★ 2 · Python · source · pushed 2025-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/QuentinCody/catalysishub-mcp-server.git`</sub>
- **[securecoders/opengraph-io-mcp](https://github.com/securecoders/opengraph-io-mcp)** — OpenGraph.io API: extract OG metadata, take screenshots, scrape web content, query sites with AI and generate branded images and social cards
  <sub>★ 2 · TypeScript · ISC · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g opengraph-io-mcp`</sub>
- **[Savirinc/unfragile-mcp-server](https://github.com/Savirinc/unfragile-mcp-server)** — Resolve an agent's intent to the right MCP server across registries, with an invocation-ready snippet and an Ed25519-signed trust passport
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Savirinc/unfragile-mcp-server.git`</sub>
- **[Gaoshan0971/digeguigui](https://github.com/Gaoshan0971/digeguigui)** — Reptile and exotic pet knowledge base: species identification, genetics calculator, care information, health diagnosis, prices and blockchain provenance
  <sub>★ 2 · Python · MIT · source · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Gaoshan0971/digeguigui.git`</sub>
- **[yubinkim444/ai-first-scraper-mcp](https://github.com/yubinkim444/ai-first-scraper-mcp)** — Ad-free web scraping and search as clean Markdown: fetch pages singly or in parallel batches, and search the web for top-k pages
  <sub>★ 2 · Python · MIT · pip · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ai-first-scraper-mcp`</sub>
- **[HasData/chatgpt-mcp](https://github.com/HasData/chatgpt-mcp)** — Send a prompt to ChatGPT anonymously and read the answer as markdown together with every web source it consulted, as JSON. No OpenAI account or key
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-10-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/chatgpt-mcp.git`</sub>
- **[artemchuikin/youtube-mcp](https://github.com/artemchuikin/youtube-mcp)** — YouTube transcripts (text, JSON, SRT, VTT, srv3), video and channel search, playlists and large batch jobs
  <sub>★ 1 · MIT · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install transcriptout # replaces youtube-transcript-api`</sub>
- **[AgenticAdvertising/topalternativesto-mcp](https://github.com/AgenticAdvertising/topalternativesto-mcp)** — Software comparisons with prices sourced from each vendor's page (with URL and check date), plus ranked alternatives for any tool
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx topalternativesto-mcp`</sub>
- **[Newscatcher/catchall-mcp](https://github.com/Newscatcher/catchall-mcp)** — Recall-first web search that finds relevant events across the open web, beyond the top results
  <sub>★ 1 · Python · MIT · source · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Newscatcher/catchall-mcp.git`</sub>
- **[pgalyen1987/gate402-mcp](https://github.com/pgalyen1987/gate402-mcp)** — Pay-per-call x402 APIs (USDC on Base): LLM inference, GPU and CPU compute, on-chain, DeFi, SEC EDGAR and news data, and web scraping to Markdown
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g gate402-mcp`</sub>
- **[newsagentdata/newsagent-mcp](https://github.com/newsagentdata/newsagent-mcp)** — Real-time news with ML enrichment: urgency scoring, political lean and event clustering across many countries
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/newsagentdata/newsagent-mcp.git`</sub>
- **[qinisolabs/icdwise](https://github.com/qinisolabs/icdwise)** — ICD-10-CM medical code lookup, validation and reverse search
  <sub>★ 1 · TypeScript · Apache-2.0 · source · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/qinisolabs/icdwise.git`</sub>
- **[AIweather-Anurag/ottasia-mcp-server](https://github.com/AIweather-Anurag/ottasia-mcp-server)** — Find where to stream movies and TV shows across Asian and Middle Eastern services such as Netflix, Disney+ Hotstar, Wavve, Shahid, ZEE5 and JioCinema
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AIweather-Anurag/ottasia-mcp-server.git`</sub>
- **[AceDataCloud/MCPSerp](https://github.com/AceDataCloud/SerpMCP)** — Google SERP search via the Ace Data Cloud API: web, image, news, maps, places, video and knowledge graph results
  <sub>★ 1 · Python · MIT · clone · pushed 2026-10-19 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/AceDataCloud/SerpMCP.git`</sub>
- **[AllNewsAPI/mcp-server](https://github.com/AllNewsAPI/mcp-server)** — Real-time and historical news data, including top headlines from global sources, via AllNewsAPI
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx allnewsapi-mcp@latest --apikey YOUR_API_KEY_HERE`</sub>
- **[CKBrennan/overtone-news-mcp](https://github.com/CKBrennan/overtone-news-mcp)** — Real-time news with tone analysis, brand safety and narrative shift signals
  <sub>★ 1 · Python · MIT · clone · pushed 2026-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CKBrennan/overtone-news-mcp`</sub>
- **[Crawlora-org/crawlora-mcp](https://github.com/Crawlora-org/crawlora-mcp)** — Structured public web data as clean JSON across search, maps, commerce, social and finance
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx crawlora-mcp`</sub>
- **[deficlow/HyperStore-MCP](https://github.com/deficlow/HyperStore-MCP)** — Keyword and semantic search over curated AI applications in the HyperStore directory, with full app details and browsing
  <sub>★ 1 · Python · MIT · npx · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx hyperstore-mcp`</sub>
- **[pepabo/muumuu-domain-mcp](https://github.com/pepabo/muumuu-domain-mcp)** — Search and register Muumuu Domain (GMO Pepabo) domains, manage owned domains and contracts, and configure DNS records
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pepabo/muumuu-domain-mcp.git`</sub>
- **[VoxellInc/forge-mcp](https://github.com/VoxellInc/forge-mcp)** — Generate vector embeddings for semantic search and RAG with Forge, Voxell's text-embedding API, including Matryoshka truncation
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/VoxellInc/forge-mcp.git`</sub>
- **[giskard09/giskard-search](https://github.com/giskard09/giskard-search)** — Semantic web search powered by SearXNG, paid per use in sats via Lightning Network micropayments. Self-hosted with phoenixd
  <sub>★ 1 · Python · Apache-2.0 · pip · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mcp httpx duckduckgo-search python-dotenv fastapi uvicorn web3 x402`</sub>
- **[ip2whois/mcp-ip2whois](https://github.com/ip2whois/mcp-ip2whois)** — WHOIS lookups via the IP2WHOIS API: domain registration details including expiry dates, registrar and registrant data
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ip2whois/mcp-ip2whois.git`</sub>
- **[leadbrain/korean-data-mcp](https://github.com/leadbrain/korean-data-mcp)** — Real-time Korean web data via Apify: Naver place reviews and news, Melon music chart, Daangn and Bunjang listings and Musinsa fashion rankings
  <sub>★ 1 · Python · MIT · pip · pushed 2026-03-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install korean-data-mcp`</sub>
- **[mambalabsdev/mcp-company-firmographic-enricher](https://github.com/mambalabsdev/mcp-company-firmographic-enricher)** — Enrich a company domain with firmographics: employee band, industry, HQ, founding year, revenue estimate, logo and description, with source provenance
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-firmographic-enricher.git`</sub>
- **[mambalabsdev/mcp-gtm-hiring-signal-scraper](https://github.com/mambalabsdev/mcp-gtm-hiring-signal-scraper)** — Detect GTM hiring signals on Greenhouse, Lever and Ashby career pages, returning Clay-ready JSON with role counts, signal strength and ATS detection
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-gtm-hiring-signal-scraper.git`</sub>
- **[mambalabsdev/mcp-gtm-tech-stack-signal-scraper](https://github.com/mambalabsdev/mcp-gtm-tech-stack-signal-scraper)** — Detect CRM, sequencer and marketing automation tools from a company domain as boolean GTM tool signals for Clay enrichment
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-gtm-tech-stack-signal-scraper.git`</sub>
- **[Marvy101/pod-mcp](https://github.com/Marvy101/pod-mcp)** — Search firsthand observations agents recorded about products, APIs, services or places, as opposed to documentation claims, and write back new ones
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Marvy101/pod-mcp.git`</sub>
- **[MKirovBG/scribefy-mcp](https://github.com/MKirovBG/scribefy-mcp)** — Extract timestamped YouTube transcripts, plus video search, metadata and related videos
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y scribefy-mcp`</sub>
- **[Opedd/opedd-mcp](https://github.com/Opedd/opedd-mcp)** — Discover, buy, verify and retrieve licensed expert analysis, with per-article license keys, on-chain proof and EU AI Act Article 53 attestation
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g opedd-mcp`</sub>
- **[peter-j-thompson/semanticapi-mcp](https://github.com/peter-j-thompson/semanticapi-mcp)** — Natural language API discovery: search API capabilities and get endpoints, auth setup and code snippets, with auto-discovery of new APIs
  <sub>★ 1 · Python · uv · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx semanticapi-mcp`</sub>
- **[rubenayla/partle-mcp](https://github.com/rubenayla/partle-mcp)** — Search products and nearby physical stores to buy locally instead of waiting for delivery
  <sub>★ 1 · Python · Apache-2.0 · uv · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx partle-mcp`</sub>
- **[bartonguestier1725-collab/scout-mcp](https://github.com/bartonguestier1725-collab/scout-mcp)** — Parallel search across GitHub, npm, PyPI, arXiv, Semantic Scholar, Hacker News, Reddit, X, Dev.to, Hashnode, Qiita and Zenn with structured JSON output
  <sub>★ 1 · TypeScript · MIT · docker · pushed 2026-05-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i scout-mcp`</sub>
- **[chefcohen/corroborate-mcp](https://github.com/chefcohen/corroborate-mcp)** — Measure how independently a claim is reported, with syndication-aware source counting and 0-1 confidence scores. Measures corroboration, not truth
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx corroborate-mcp # starts the stdio server (silent = healthy)`</sub>
- **[scrapercity/scrapercity-cli](https://github.com/scrapercity/scrapercity-cli)** — B2B lead generation: Apollo and Google Maps data, email finding and validation, mobile number lookup, skip tracing and ecommerce store data
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx scrapercity login # enter your API key`</sub>
- **[smeet666/mcp-marmiton](https://github.com/smeet666/mcp-marmiton)** — Search Marmiton recipes, read ingredients and steps, and rescale quantities to any number of servings
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-marmiton.git`</sub>
- **[ssatama/rescuedogs-mcp-server](https://github.com/ssatama/rescuedogs-mcp-server)** — Search rescue dogs from European and UK organizations, with detailed profiles and personality matching
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g rescuedogs-mcp-server`</sub>
- **[theagenttimes/tat-mcp-server](https://github.com/theagenttimes/tat-mcp-server)** — Query articles, statistics, the wire feed, comments, citations and agent leaderboards from The Agent Times, a newspaper covering the agent economy
  <sub>★ 1 · Python · clone · pushed 2026-02-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/levfilimonov/tat-mcp-server.git`</sub>
- **[AI-Directory-Partners/tooldirectory-mcp](https://github.com/AI-Directory-Partners/tooldirectory-mcp)** — Search a catalog of AI tools, compare them, find alternatives and check whether a tool is active, defunct or acquired
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y tooldirectory-mcp`</sub>
- **[juergenkoller-software/pdf-content-search-mcp](https://github.com/juergenkoller-software/pdf-content-search-mcp)** — Full-text PDF search with Apple Vision OCR via the PDF Content Search app, with date, category, sender and amount filters, wildcards and boolean operators
  <sub>★ 1 · Swift · MIT · clone · pushed 2026-10-20 · macOS · Linux</sub>
  <sub>`git clone https://github.com/juergenkoller-software/pdf-content-search-mcp.git`</sub>
- **[darksider4all/leadgen-mcp](https://github.com/darksider4all/leadgen-mcp)** — Romanian company data: 4.2M ONRC firms, ANAF status and financial statements 2008–2025; lead lists by CAEN and county, list matching and due-diligence checks
  <sub>Python · MIT · uv · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx leadgen-mcp`</sub>
- **[A1-x-Tech/mcp-google-custom-search](https://github.com/A1-x-Tech/mcp-google-custom-search)** — Google Custom Search JSON API: web and image search through a Programmable Search Engine
  <sub>TypeScript · MIT · npx · pushed 2026-10-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-google-custom-search@latest`</sub>
- **[Grubbomatic/crawl-readiness-mcp](https://github.com/Grubbomatic/crawl-readiness-mcp)** — AI SEO audits: score AI crawler readiness, validate JSON-LD and robots.txt, compare human and crawler views, and generate llms.txt, robots.txt and JSON-LD
  <sub>JavaScript · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y crawl-readiness-mcp`</sub>
- **[AgentiLoop/pagewire-mcp](https://github.com/AgentiLoop/pagewire-mcp)** — Read any public web page as clean Markdown, page metadata, or a page plus 4 same-site pages; pay per call in USDC via x402, no API key
  <sub>JavaScript · MIT · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mppx "https://pagewire.dev/x402/extract?url=https://example.com"`</sub>
- **[ToolTrace-io/mcp-server](https://github.com/ToolTrace-io/mcp-server)** — Web page data: scrape to Markdown, extract metadata, links and JSON-LD, audit on-page SEO, detect tech stacks and validate XML sitemaps
  <sub>TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @tooltrace/mcp-server`</sub>
- **[jlucasmcrell/apify-scrapers](https://github.com/jlucasmcrell/apify-scrapers)** — Public data scrapers and lead extractors for Google Maps, Glassdoor, SEC EDGAR and state contractor registries
  <sub>Python · MIT · uv · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx apify-data-scrapers`</sub>
- **[igorsaevets/page2ai-mcp](https://github.com/igorsaevets/page2ai-mcp)** — Convert web pages into clean Markdown locally, preserving tables, code blocks and headings
  <sub>TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y page2ai-mcp`</sub>
- **[quantumproxies/quantumproxies-mcp](https://github.com/quantumproxies/quantumproxies-mcp)** — Residential-proxy web access: scrape pages to Markdown, SERP search, site mapping and crawling, ready-made collectors, and proxy endpoints from your plans
  <sub>TypeScript · MIT · source · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/quantumproxies/quantumproxies-mcp.git`</sub>
- **[rozetyp/grounder-mcp](https://github.com/rozetyp/grounder-mcp)** — Live web grounding for local and cloud LLMs: web search, page fetch, token-capped cited evidence packs and an agentic search-and-read research loop
  <sub>Python · MIT · uv · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx grounder-mcp # or: pip install grounder-mcp`</sub>
- **[adjacentai/necl-hn-mcp](https://github.com/adjacentai/necl-hn-mcp)** — Hacker News: top stories by time window, category feeds, comment threads and full-text search via Algolia
  <sub>Python · MIT · pip · pushed 2026-06-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install git+https://github.com/adjacentai/necl-hn-mcp.git`</sub>
- **[einiba/canyougrab-api](https://github.com/einiba/canyougrab-api/tree/main/mcp-server)** — Domain availability checks via real-time DNS and WHOIS lookups, with bulk checking, confidence scores and registration details
  <sub>Python · MIT · in-repo · pushed 2026-09-27</sub>
  <sub>`git clone https://github.com/einiba/canyougrab-api.git && cd canyougrab-api/mcp-server`</sub>
- **[eliottreich/crawdar-mcp](https://github.com/eliottreich/crawdar-mcp)** — Evidence-backed business discovery and lead-list research: search by brief or criteria, inspect qualification evidence and exclusions, and export results
  <sub>JavaScript · MIT · docker · pushed 2026-09-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i crawdar-mcp`</sub>
- **[devflowinc/trieve](https://github.com/devflowinc/trieve/tree/main/clients/mcp-server)** — Crawl, embed, chunk, search and retrieve information from datasets through Trieve
  <sub>Rust · MIT · in-repo · pushed 2026-01-25</sub>
  <sub>`git clone https://github.com/devflowinc/trieve.git && cd trieve/clients/mcp-server`</sub>
- **[djrobson5/agentmd-mcp](https://github.com/djrobson5/agentmd-mcp)** — Convert PDF, DOCX, HTML and URLs to clean, LLM-ready Markdown with tables preserved and boilerplate stripped
  <sub>JavaScript · MIT · docker · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e AGENTMD_API_KEY=<your-key> agentmd-mcp`</sub>
- **[evanatpizzarobot/vr-org-mcp](https://github.com/evanatpizzarobot/vr-org-mcp)** — Live VR, AR and XR news, full-text VR.org originals, an events calendar, headset deals and comparisons
  <sub>TypeScript · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vr-org-mcp`</sub>
- **[FieldmodeLLC/scrapecheck-mcp](https://github.com/FieldmodeLLC/scrapecheck-mcp)** — Verify scraped field values against the live source page, returning an Ed25519-signed pass, fail or unverifiable verdict that can be checked offline
  <sub>TypeScript · MIT · source · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FieldmodeLLC/scrapecheck-mcp.git`</sub>
- **[foundrole/jobs-mcp-proxy](https://github.com/foundrole/jobs-mcp-proxy)** — FoundRole job search: live ATS listings with salary benchmarks, H-1B sponsorship history and ghost-job grades, plus resume checks and an application tracker
  <sub>TypeScript · ISC · npm · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @foundrole/ai-job-search-mcp`</sub>
- **[smeet666/mcp-wikibooks-cookbook](https://github.com/smeet666/mcp-wikibooks-cookbook)** — Search recipes in the English Wikibooks Cookbook, read ingredients and steps, and rescale quantities
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-wikibooks-cookbook.git`</sub>
- **[smeet666/mcp-recipes](https://github.com/smeet666/mcp-recipes)** — Query Marmiton and the Wikibooks Cookbook together to compare recipes, and scale French and English ingredient lists, flagging what cannot be scaled
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-recipes.git`</sub>
- **[githunt-agent/githunt-mcp](https://github.com/githunt-agent/githunt-mcp)** — Search, rank and analyze GitHub developers for tech recruiting by location, role and skill, with AI scoring and contact discovery
  <sub>JavaScript · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx githunt-mcp`</sub>
- **[johnsmalls22-rgb/domain-search-king-mcp](https://github.com/johnsmalls22-rgb/domain-search-king-mcp)** — Domain name search that returns only .com domains verified as available via live Verisign RDAP checks
  <sub>JavaScript · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/johnsmalls22-rgb/domain-search-king-mcp.git`</sub>
- **[litescrape/litescrape-mcp-server](https://github.com/litescrape/litescrape-mcp-server)** — Google Search, Bing, DuckDuckGo, Google Maps, Google AI Mode, AI Overview and Shopping results as JSON
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/litescrape/litescrape-mcp-server.git`</sub>
- **[litportnet/free-proxy-mcp](https://github.com/litportnet/free-proxy-mcp)** — Verified free HTTP, SOCKS4 and SOCKS5 proxy lists from Litport, filtered by country, anonymity, latency and uptime. Returns records only; no API key needed
  <sub>JavaScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @litportnet/free-proxy-mcp`</sub>
- **[mambalabsdev/mcp-ai-tooling-detector](https://github.com/mambalabsdev/mcp-ai-tooling-detector)** — Detect whether a company only claims AI, deploys AI tooling on its site or charges for AI, returning an AI maturity tier with supporting evidence
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-ai-tooling-detector.git`</sub>
- **[mambalabsdev/mcp-company-change-event-feed](https://github.com/mambalabsdev/mcp-company-change-event-feed)** — Monitor company changes across hiring, tech stack, funding, firmographics, and social since the last run. Returns only deltas as typed change events
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-change-event-feed.git`</sub>
- **[mambalabsdev/mcp-company-contact-details-extractor](https://github.com/mambalabsdev/mcp-company-contact-details-extractor)** — Find a company's contact page and extract role emails, a phone number and a postal address
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-contact-details-extractor.git`</sub>
- **[mambalabsdev/mcp-company-discovery-list-builder](https://github.com/mambalabsdev/mcp-company-discovery-list-builder)** — Builds a company list from a market definition: companies hiring for a role, or US SEC filers whose filings mention a phrase
  <sub>JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @mambalabsdev/mcp-company-discovery-list-builder`</sub>
- **[mambalabsdev/mcp-company-social-presence-mapper](https://github.com/mambalabsdev/mcp-company-social-presence-mapper)** — Map a company domain to its LinkedIn, X, Instagram, Facebook and YouTube profiles and follower counts as flat Clay-ready JSON via an Apify actor
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-company-social-presence-mapper.git`</sub>
- **[mambalabsdev/mcp-creator-finder](https://github.com/mambalabsdev/mcp-creator-finder)** — Finds influencers by keyword or curated niche across TikTok, Instagram, YouTube, Pinterest, Twitch, Threads, and podcasts, filtered by follower range
  <sub>JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @mambalabsdev/mcp-creator-finder`</sub>
- **[mambalabsdev/mcp-event-presence-index](https://github.com/mambalabsdev/mcp-event-presence-index)** — List the third-party conferences and trade shows a company publicly says it attends, with the year of each
  <sub>JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @mambalabsdev/mcp-event-presence-index`</sub>
- **[mambalabsdev/mcp-funding-press-signal-scanner](https://github.com/mambalabsdev/mcp-funding-press-signal-scanner)** — Scan Google News and PR wires for a company's funding rounds, executive moves, launches and acquisitions as deduplicated, dated events in Clay-ready JSON
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-funding-press-signal-scanner.git`</sub>
- **[mambalabsdev/mcp-github-organization-signal-scanner](https://github.com/mambalabsdev/mcp-github-organization-signal-scanner)** — Resolve a company domain to its GitHub organization with repository, language and activity signals
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-github-organization-signal-scanner.git`</sub>
- **[mambalabsdev/mcp-review-platform-reputation-enricher](https://github.com/mambalabsdev/mcp-review-platform-reputation-enricher)** — Resolve a company domain to its Trustpilot rating, review count and claimed status
  <sub>JavaScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-review-platform-reputation-enricher.git`</sub>
- **[modelcontextprotocol/server-fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)** — Web content fetching and processing for AI consumption
  <sub>TypeScript · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/fetch`</sub>
- **[Pexafy/pexafy-mcp](https://github.com/Pexafy/pexafy-mcp)** — Semantic search of free-license stock photos from Unsplash, Pexels, Pixabay and more by scene description, example image or similarity, with attribution
  <sub>Python · MIT · source · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pexafy/pexafy-mcp.git`</sub>
- **[opendatalab/MinerU-Ecosystem](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/mcp)** — Convert PDFs, Word and PowerPoint files, images and spreadsheets to Markdown via the MinerU document parsing API
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/opendatalab/MinerU-Ecosystem.git && cd MinerU-Ecosystem/mcp`</sub>
- **[phpcip/opensolr-mcp](https://github.com/phpcip/opensolr-mcp)** — Managed Apache Solr: hybrid BM25 and kNN plus semantic search, document ingestion with server-side embeddings, grounded RAG answers and index management
  <sub>Python · MIT · uv · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx opensolr-mcp`</sub>
- **[quantumproxies/quanticdata-mcp-server](https://github.com/quantumproxies/quanticdata-mcp-server)** — Web data via residential proxies: page scraping to Markdown, SERP search, site crawl and map, ready-made collectors and datasets from plain-language prompts
  <sub>TypeScript · MIT · source · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/quantumproxies/quanticdata-mcp-server.git`</sub>
- **[Rererr/amenbo](https://github.com/Rererr/amenbo)** — Token-efficient web fetching for Japanese sites: outline-first disclosure, Shift_JIS and EUC-JP decoding, PDF and CSV extraction and polite crawling
  <sub>TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g amenbo`</sub>
- **[Seomarlboro/digmyname](https://github.com/Seomarlboro/digmyname/tree/main/mcp)** — Domain availability checks, registrar price comparison and domain age lookups across many TLDs
  <sub>TypeScript · in-repo · pushed 2026-10-11</sub>
  <sub>`git clone https://github.com/Seomarlboro/digmyname.git && cd digmyname/mcp`</sub>
- **[serpdive/serpdive-mcp](https://github.com/serpdive/serpdive-mcp)** — Web search returning extracted page content (URL, title, date, text) instead of links, with automatic localization and an optional synthesized answer
  <sub>JavaScript · MIT · npx · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y serpdive-mcp`</sub>
- **[smeet666/mcp-ashby](https://github.com/smeet666/mcp-ashby)** — Search companies' public Ashby job boards: resolve a company to its board, filter openings, read full postings and compare published pay ranges
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-ashby.git`</sub>
- **[smeet666/mcp-animenewsnetwork](https://github.com/smeet666/mcp-animenewsnetwork)** — Search the Anime News Network encyclopedia for anime and manga, read cast, staff, episodes and studios as compact rows, and follow the news wire
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-animenewsnetwork.git`</sub>
- **[smeet666/mcp-pequerecetas](https://github.com/smeet666/mcp-pequerecetas)** — Read Spanish family recipes from Pequerecetas, rescale servings and browse by diet, main ingredient, appliance or age group from six months up
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-pequerecetas.git`</sub>
- **[srezai-team/srezai-mcp](https://github.com/srezai-team/srezai-mcp-web-search)** — Web and image search, page reading as Markdown, browser-rendered screenshots, schema-based extraction and deep research, with strong Russian web coverage
  <sub>TypeScript · MIT · source · pushed 2026-10-20 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/srezai-team/srezai-mcp.git`</sub>
- **[TechMap/mcp.techmap.io](https://github.com/TechMap/mcp.techmap.io)** — Search and count job postings from 185 sources in 250 countries (~8M new per month) via Techmap's Jobs API; filters for title, skills, company, city, remote/hybrid, salary and posting date
  <sub>TypeScript · MIT · source · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TechMap/mcp.techmap.io.git`</sub>
- **[WhaleCupl/ai-daily-insights-mcp](https://github.com/WhaleCupl/ai-daily-insights-mcp)** — List, fetch and full-text search structured daily AI news from AI Daily Insights, a Chinese AI-industry briefing
  <sub>JavaScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/WhaleCupl/ai-daily-insights-mcp.git`</sub>
- **[retracn/automationnation-mcp](https://github.com/retracn/automationnation-mcp)** — 17 data tools backed by Apify Actors: Google Flights and Hotels prices, Google Shopping, News, Images, Videos, Jobs and Trends, YouTube transcripts, Google Maps leads, Ads Transparency, app reviews and AI-search visibility; pay per result with a spending cap on every run
  <sub>JavaScript · MIT · npx · pushed 2026-10-06 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y github:retracn/automationnation-mcp --http --port 8080 # http://localhost:8080/mcp`</sub>
- **[smeet666/mcp-ptitchef](https://github.com/smeet666/mcp-ptitchef)** — Search Ptitchef recipes, browse ingredient categories, read ingredients, method, cost and nutrition, find dishes from fridge contents and rescale servings
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-ptitchef.git`</sub>
- **[smeet666/mcp-bbc-goodfood](https://github.com/smeet666/mcp-bbc-goodfood)** — Search BBC Good Food recipes, read them in the original or US version, see accepted search facet values and rescale to any number of people
  <sub>TypeScript · MIT · source · pushed 2026-10-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-bbc-goodfood.git`</sub>
- **[smeet666/mcp-supertoinette](https://github.com/smeet666/mcp-supertoinette)** — Read Supertoinette's French recipes: ingredients, steps, difficulty, cost, resting time and wine pairings, and rescale to any number of people
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-supertoinette.git`</sub>
- **[AG-Bureau/mcp-search](https://github.com/AG-Bureau/mcp-search)** — Search, page reading, images, screenshots and multi-source answers over your own SearXNG, reporting which engines were queried and what to distrust
  <sub>Python · AGPL-3.0 · docker · pushed 2026-09-26 · WSL2 · Linux · Docker</sub>
  <sub>`docker compose up -d --force-recreate ag-search`</sub>
- **[double2dev/boltpatternhq-mcp](https://github.com/double2dev/boltpatternhq-mcp)** — Official MCP Server for BoltPatternHQ providing AI assistants with instant automotive wheel fitment, PCD, center bore, and offset reference data
  <sub>TypeScript · MIT · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @double2dev/boltpatternhq-mcp --client claude`</sub>

## Data Science Tools

- **[zcaceres/markdownify-mcp](https://github.com/zcaceres/markdownify-mcp)** — Convert almost any file or web content into Markdown
  <sub>★ 3k · TypeScript · MIT · source · pushed 2026-09-25 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/zcaceres/markdownify-mcp.git`</sub>
- **[datalayer/jupyter-mcp-server](https://github.com/datalayer/jupyter-mcp-server)** — Interact with Jupyter
  <sub>★ 1.3k · Python · BSD-3-Clause · pip · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "jupyter-mcp-server>=1.5.0" "code-sandboxes>=1.1.1"`</sub>
- **[DataEval/dingo](https://github.com/MigoXLab/dingo)** — Data quality evaluation with Dingo: run rule-based and LLM-based evaluations and list its rules and prompts
  <sub>★ 759 · Python · Apache-2.0 · pip · pushed 2026-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install dingo-python`</sub>
- **[reading-plus-ai/mcp-server-data-exploration](https://github.com/reading-plus-ai/mcp-server-data-exploration)** — Autonomous data exploration of CSV datasets with generated insights
  <sub>★ 544 · Python · MIT · source · pushed 2025-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reading-plus-ai/mcp-server-data-exploration.git`</sub>
- **[jjsantos01/jupyter-notebook-mcp](https://github.com/jjsantos01/jupyter-notebook-mcp)** — Interact with and control Jupyter Notebooks
  <sub>★ 128 · Jupyter Notebook · MIT · clone · pushed 2025-04-02 · Win?</sub>
  <sub>`git clone https://github.com/jjsantos01/jupyter-notebook-mcp.git`</sub>
- **[ChronulusAI/chronulus-mcp](https://github.com/ChronulusAI/chronulus-mcp)** — Forecasting and prediction with Chronulus AI agents
  <sub>★ 111 · Python · MIT · pip · pushed 2025-07-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install chronulus-mcp`</sub>
- **[optuna/optuna-mcp](https://github.com/optuna/optuna-mcp)** — Orchestrate hyperparameter search and other optimization tasks with Optuna
  <sub>★ 88 · Python · MIT · source · pushed 2026-10-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/optuna/optuna-mcp.git`</sub>
- **[kdqed/zaturn](https://github.com/kdqed/zaturn)** — Link multiple data sources (SQL, CSV, Parquet and more) and analyze the data for insights and visualizations
  <sub>★ 75 · Python · MIT · source · pushed 2025-11-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kdqed/zaturn.git`</sub>
- **[arrismo/kaggle-mcp](https://github.com/arrismo/kaggle-mcp)** — Connect to Kaggle to download and analyze datasets
  <sub>★ 39 · Python · MIT · docker · pushed 2026-05-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -i --env-file .env kaggle-mcp`</sub>
- **[HumanSignal/label-studio-mcp-server](https://github.com/HumanSignal/label-studio-mcp-server)** — Create, manage and automate Label Studio projects, tasks and predictions for data labeling workflows
  <sub>★ 37 · Python · Apache-2.0 · clone · pushed 2025-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HumanSignal/label-studio-mcp-server.git`</sub>
- **[phisanti/MCPR](https://github.com/phisanti/MCPR)** — Connect AI agents to interactive live R sessions
  <sub>★ 27 · HTML · CC-BY-SA-4.0 · source · pushed 2026-10-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/phisanti/MCPR.git`</sub>
- **[growthbook/growthbook-mcp](https://github.com/growthbook/growthbook-mcp)** — Create and interact with GrowthBook feature flags and experiments
  <sub>★ 24 · TypeScript · MIT · npx · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @growthbook/mcp`</sub>
- **[Bright-L01/networkx-mcp-server](https://github.com/brightlikethelight/networkx-mcp-server)** — Graph analysis with NetworkX: centrality algorithms, community detection, PageRank and graph visualization
  <sub>★ 22 · Python · MIT · pip · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install networkx-mcp-server`</sub>
- **[abhiphile/fermat-mcp](https://github.com/abhiphile/fermat-mcp)** — Math engine combining SymPy, NumPy and Matplotlib for symbolic algebra, numerical computing and data visualization
  <sub>★ 21 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @abhiphile/fermat-mcp --client gemini`</sub>
- **[subelsky/bundler_mcp](https://github.com/subelsky/bundler_mcp)** — Query local information about dependencies in a Ruby project's Gemfile
  <sub>★ 21 · Ruby · MIT · npx · pushed 2025-06-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector ./bin/bundler_mcp`</sub>
- **[Archerkattri/mathlas](https://github.com/Archerkattri/mathlas)** — Math tools for agents: theorem search, PSLQ constant identification, OEIS lookup, Lean kernel checks and applicability checklists
  <sub>★ 13 · Python · Apache-2.0 · uv · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mathlas-mcp`</sub>
- **[Whatsonyourmind/oraclaw](https://github.com/Whatsonyourmind/oraclaw)** — Decision intelligence algorithms: bandits, Monte Carlo, constraint optimization, forecasting, anomaly detection, risk analysis and graph algorithms
  <sub>★ 13 · TypeScript · MIT · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Whatsonyourmind/oraclaw.git`</sub>
- **[phuongrealmax/code-guardian](https://github.com/phuongrealmax/code-guardian)** — Code refactoring engine: code analysis, hotspot detection, complexity metrics, persistent memory and automated refactoring plans
  <sub>★ 9 · TypeScript · npm · pushed 2025-12-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g codeguardian-studio`</sub>
- **[avisangle/calculator-server](https://github.com/avisangle/calculator-server)** — Mathematical computations: basic arithmetic, advanced functions, statistical analysis, unit conversions and financial calculations
  <sub>★ 7 · Go · source · pushed 2025-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/avisangle/calculator-server.git`</sub>
- **[Kungie/gut](https://github.com/Kungie/gut)** — Judgment calls on small, cheap models: yes/no, pick-one and rate questions about any text, answered YES, NO or UNSURE. Runs on TypeSafe's Jev, open models on Ollaya, Ollama or a local NLI model; each judges up to 1,000 texts per call
  <sub>★ 7 · Python · Apache-2.0 · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Kungie/gut --skill gut # teaches a coding agent when to reach for it`</sub>
- **[leap-laboratories/discovery-engine](https://github.com/leap-laboratories/discovery-engine)** — Exploratory data analysis that finds feature interactions and subgroup effects, with p-values, effect sizes and literature citations
  <sub>★ 7 · Python · MIT · pip · pushed 2026-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install discovery-engine-api`</sub>
- **[FantasyLab-ai/aurora](https://github.com/FantasyLab-ai/aurora)** — Transparent statistical analysis with cited findings, integrity-hashed result bundles and a calibration corpus of measured detector false-fire rates
  <sub>★ 6 · Python · Apache-2.0 · uv · pushed 2026-09-05 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx aurora-mcp`</sub>
- **[clouatre-labs/math-mcp-learning-server](https://github.com/clouatre-labs/math-mcp-learning-server)** — Educational server for math operations, statistics, visualization and persistent workspaces
  <sub>★ 5 · Python · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/clouatre-labs/math-mcp-learning-server.git`</sub>
- **[ShipItAndPray/mcp-turboquant](https://github.com/ShipItAndPray/mcp-turboquant)** — LLM quantization: convert models to GGUF, GPTQ and AWQ, recommend quantization settings, evaluate quality and push to Hugging Face Hub
  <sub>★ 5 · Python · MIT · uv · pushed 2026-04-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-turboquant`</sub>
- **[aurelio-nakamura/dataloupe](https://github.com/aurelio-nakamura/dataloupe)** — Offline tabular data access: describe, preview and query CSV, TSV, JSON, Parquet and Excel files, diff datasets and build an interactive HTML explorer
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g dataloupe`</sub>
- **[bradleylab/stella-mcp](https://github.com/bradleylab/stella-mcp)** — Create, read, validate and save Stella system dynamics models (.stmx files in XMILE format) for scientific simulation and modeling
  <sub>★ 4 · Python · MIT · pip · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install stella-mcp`</sub>
- **[gpartin/WaveGuardClient](https://github.com/gpartin/WaveGuardClient)** — Physics-based anomaly detection with Klein-Gordon wave equations: scans, fingerprinting, token risk, wallet profiling and price manipulation detection
  <sub>★ 4 · Python · MIT · pip · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install WaveGuardClient scikit-learn`</sub>
- **[pramod/kaggle](https://github.com/KrishnaPramodParupudi/kaggle-mcp-server)** — Browse Kaggle competitions, leaderboards, models, datasets and kernels
  <sub>★ 4 · Python · MIT · source · pushed 2025-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/KrishnaPramodParupudi/kaggle-mcp-server.git`</sub>
- **[haiiibin/data-profiler-mcp](https://github.com/haiiibin/data-profiler-mcp)** — Profile local tabular files (CSV, TSV, Parquet, Excel, JSON): dataset overview, per-column statistics, data-quality audits and dtype suggestions
  <sub>★ 3 · Python · MIT · uv · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install data-profiler-mcp`</sub>
- **[tufantunc/axiom-advanced-math-mcp](https://github.com/tufantunc/axiom-advanced-math-mcp)** — Offline exact symbolic math via the Giac/Xcas computer algebra system: calculus, equation solving, linear algebra, combinatorics and claim verification
  <sub>★ 3 · TypeScript · GPL-3.0 · npm · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g axiom-math`</sub>
- **[Daichi-Kudo/llm-advisor-mcp](https://github.com/Daichi-Kudo/llm-advisor-mcp)** — Real-time LLM and VLM comparison with benchmarks, prices and personalized recommendations from multiple data sources
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Daichi-Kudo/llm-advisor-mcp.git`</sub>
- **[ShipItAndPray/mcp-compress](https://github.com/ShipItAndPray/mcp-compress)** — Data compression with gzip, Brotli, deflate and TurboQuant quantization, with automatic algorithm selection
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-compress`</sub>
- **[98lukehall/renoun-mcp](https://github.com/98lukehall/renoun-mcp)** — Structural observability for AI conversations: detects loops, stuck states, breakthroughs and convergence without analyzing content
  <sub>★ 2 · Python · source · pushed 2026-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/98lukehall/renoun-mcp.git`</sub>
- **[agmonetti/mathmethods-mcp](https://github.com/agmonetti/mathmethods-mcp)** — Numerical methods: root finding, numerical integration, differential equations (RK4) and Lagrange interpolation
  <sub>★ 1 · Python · MIT · npm · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @agmonetti/mathmethods-mcp`</sub>
- **[chohyerinn/filter-mcp-server](https://github.com/chohirin/filter-mcp-server)** — Compare approximate filter data structures: Bloom, Counting Bloom, Cuckoo and SuRF
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chohyerinn/filter-mcp-server.git`</sub>
- **[lihtness/gnomon-mcp](https://github.com/lihtness/gnomon-mcp)** — Deterministic date, math and unit tools: time snapshots, calendar math with natural-language parsing, expression evaluation and Pint-based unit conversion
  <sub>★ 1 · Python · MIT · uv · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx gnomon-mcp # serves stdio MCP, ready for any client`</sub>
- **[mrnh/rigor](https://github.com/mrnh/rigor)** — Classical hypothesis testing, effect sizes, power and sample-size analysis and multiple-comparisons correction, returned as cited, assumption-checked answers
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx rigor-mcp`</sub>
- **[playidea-lab/pcq](https://github.com/playidea-lab/pcq)** — ML experiment contracts (cq.yaml plus JSON) to run, validate, compare and trace experiments in any framework, including PyTorch, Lightning and sklearn
  <sub>★ 1 · Python · Apache-2.0 · docker · pushed 2026-05-29 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm pcq # MCP client attaches to stdin/stdout`</sub>
- **[laszlopere/mcp-gnu-units](https://github.com/laszlopere/mcp-gnu-units)** — Offline unit conversion and dimensional analysis backed by the GNU units database, with compound expressions and reduction to SI base units
  <sub>★ 1 · Python · GPL-3.0 · source · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/laszlopere/mcp-gnu-units.git`</sub>
- **[dockndevai/mcp-laya](https://github.com/dockndevai/mcp-laya)** — Fast, local, non-autoregressive System-1 decision engine as MCP tools — typed decisions (classify / score / yes-no) over text, email, tickets or JSON in 100+ languages, with calibrated confidence and no text generation, so nothing to hallucinate. Offloads routing/triage/gating judgment calls from the main model; runs on-device, offline by default. pipx install mcp-laya
  <sub>Python · MIT · pipx · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install mcp-laya # or: pip install mcp-laya`</sub>
- **[inity13/decisionmatrix-mcp](https://github.com/inity13/decisionmatrix-mcp)** — Deterministic multi-criteria decision analysis: rank options on weighted criteria via weighted-sum, weighted-product or TOPSIS, with sensitivity analysis
  <sub>JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y decisionmatrix-mcp`</sub>
- **[headlessherm-creator/polymath-megablaster-mcp](https://github.com/headlessherm-creator/polymath-megablaster-mcp)** — Local deterministic calculations: exact-precision math, date arithmetic, unit conversion, statistics, subnet math, haversine and Levenshtein distance
  <sub>JavaScript · MIT · clone · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/headlessherm-creator/polymath-megablaster-mcp.git`</sub>
- **[jonahthan433/cortexcloud-mcp](https://github.com/jonahthan433/cortexcloud-mcp)** — QUBO/Ising optimization with classical, hybrid and quantum solvers, paid per call via x402 (USDC on Base)
  <sub>Python · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jonahthan433/cortexcloud-mcp.git`</sub>
- **[mckinsey/vizro-mcp](https://github.com/mckinsey/vizro/tree/main/vizro-mcp)** — Create validated, maintainable data charts and dashboards with Vizro tools and templates
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/mckinsey/vizro.git && cd vizro/vizro-mcp`</sub>
- **[TensorLink-AI/ephemeris-mcp](https://github.com/TensorLink-AI/ephemeris-mcp)** — Probabilistic time-series forecasting: quantile forecasts from Chronos-2, TimesFM 2.5, Toto 2, TiRex-2 and IBM Granite foundation models, routed to one model, named explicitly, or ensembled. Remote server with an npm stdio bridge
  <sub>JavaScript · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ephemeris-mcp login`</sub>
- **[hanshs474/jevx-mcp](https://github.com/hanshs474/jevx-mcp)** — Run zero-shot Jev AI typed decisions with criteria defined in the request and get calibrated probabilities for every option
  <sub>TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx jevx-mcp`</sub>

## Data Visualization

- **[nteract/semiotic](https://github.com/nteract/semiotic)** — Semiotic React data visualization: suggest charts for a dataset, render validated configs to SVG, diagnose anti-patterns and fetch component schemas
  <sub>★ 2.7k · TypeScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -p semiotic semiotic-ai --list # list components with import paths and renderability`</sub>
- **[KyuRish/mcp-dashboards](https://github.com/KyuRish/mcp-dashboards)** — Interactive charts (bar, line, candlestick, Sankey, geo and more) and dashboards with KPI cards, drill-down, live API polling, themes and PNG/PPT export
  <sub>★ 51 · TypeScript · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-dashboards`</sub>
- **[kleinicke/ply-visualizer](https://github.com/kleinicke/ply-visualizer)** — Inspect, compare and export point clouds, meshes and depth data with interactive 3D previews, measurements, NumPy/PyTorch inputs and COLMAP depth
  <sub>★ 22 · TypeScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kleinicke/ply-visualizer.git`</sub>
- **[marzukia/charted](https://github.com/marzukia/charted)** — Render bar, line, pie, scatter and other charts from JSON or CSV to SVG, HTML, PNG or data URL, with built-in themes
  <sub>★ 17 · Python · MIT · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from charted[mcp] charted-mcp`</sub>
- **[Ratnaditya-J/csvglow](https://github.com/Ratnaditya-J/csvglow)** — Generate self-contained HTML dashboards from CSV/Excel files with interactive ECharts visualizations and sortable data tables
  <sub>★ 14 · Python · MIT · npx · pushed 2026-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx csvglow data.csv`</sub>
- **[MS-Teja/Glyphic](https://github.com/MS-Teja/Glyphic)** — Generate architecture, ERD, sequence, flowchart, Gantt and other diagrams from structured JSON as SVG or PNG, without a headless browser
  <sub>★ 10 · TypeScript · source · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MS-Teja/Glyphic.git`</sub>
- **[pushtodisplay/cli](https://github.com/pushtodisplay/cli)** — Send structured content to boards in the Push To Display app on iOS and Android, route updates to specific panels and render them in real time
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-10-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pushtodisplay`</sub>
- **[ganapativs/microcharts](https://github.com/ganapativs/microcharts/tree/main/packages/mcp)** — Word-sized charts (sparklines, bars, bullets and more) rendered to self-contained SVG with generated alt text, plus chart suggestions for a given question
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/ganapativs/microcharts.git && cd microcharts/packages/mcp`</sub>
- **[nuncaeslupus/drawspec](https://github.com/nuncaeslupus/drawspec)** — Declarative JSON diagram spec rendered to themeable SVG. The format has no coordinates, so an LLM can write a correct diagram; validate, render and kinds tools
  <sub>Python · MIT · pip · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install drawspec`</sub>
- **[oscarleoo/chartlink-agents](https://github.com/oscarleoo/chartlink-agents)** — Charts, maps and sortable tables with live-updating embed links: draft, preview and publish, then update the data and every embed follows
  <sub>JavaScript · MIT · npx · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx chartlink-mcp`</sub>

## Data Platforms

- **[dbt-labs/dbt-mcp](https://github.com/dbt-labs/dbt-mcp)** — dbt integration: dbt Core and Cloud CLI, project metadata discovery, model information and semantic layer queries
  <sub>★ 612 · Python · Apache-2.0 · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dbt-labs/dbt-mcp.git`</sub>
- **[gura105/operational-ontology](https://github.com/gura105/operational-ontology)** — Operational ontology reference implementation: tools generated from a typed business domain model, with rule-checked, audited writes to systems of record
  <sub>★ 194 · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gura105/operational-ontology.git`</sub>
- **[keboola/keboola-mcp-server](https://github.com/keboola/mcp-server)** — Interact with the Keboola Connection data platform: list and access data from the Keboola Storage API
  <sub>★ 85 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`uvx keboola_mcp_server login --api-url https://connection.YOUR_REGION.keboola.com`</sub>
- **[bintocher/mcp-superset](https://github.com/bintocher/mcp-superset)** — Apache Superset: dashboards, charts, datasets, SQL Lab, security (users, roles, RLS, groups) and permissions audit, with built-in safety validations
  <sub>★ 59 · Python · MIT · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-superset`</sub>
- **[JordiNei/mcp-databricks-server](https://github.com/JordiNeil/mcp-databricks-server)** — Run SQL queries, list jobs and get job status via the Databricks API
  <sub>★ 50 · Python · source · pushed 2025-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JordiNeil/mcp-databricks-server.git`</sub>
- **[aywengo/kafka-schema-reg-mcp](https://github.com/aywengo/kafka-schema-reg-mcp)** — Kafka Schema Registry management across multiple registries, including schema migration
  <sub>★ 32 · Python · MIT · docker · pushed 2026-10-20 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -e SCHEMA_REGISTRY_URL=http://localhost:8081 -e SLIM_MODE=true aywengo/kafka-schema-reg-mcp:stable`</sub>
- **[bruno-portfolio/agrobr-mcp](https://github.com/bruno-portfolio/agrobr-mcp)** — Brazilian agricultural data: prices, crop estimates, climate and deforestation from public sources including CEPEA, CONAB, IBGE, INPE and B3
  <sub>★ 29 · Python · MIT · pip · pushed 2026-10-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install agrobr-mcp`</sub>
- **[vikramgorla/mcp-swiss](https://github.com/vikramgorla/mcp-swiss)** — Swiss open data: transport, weather, geodata, companies, parliament and more
  <sub>★ 25 · TypeScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx mcp-swiss`</sub>
- **[mattijsdp/dbt-docs-mcp](https://github.com/mattijsdp/dbt-docs-mcp)** — dbt-core (OSS) project metadata, model and column-level lineage, and dbt documentation
  <sub>★ 23 · Python · MIT · source · pushed 2025-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mattijsdp/dbt-docs-mcp.git`</sub>
- **[yashshingvi/databricks-genie-MCP](https://github.com/yashshingvi/databricks-genie-MCP)** — Databricks Genie API: ask natural language questions, run SQL queries and interact with Databricks conversational agents
  <sub>★ 17 · Python · MIT · source · pushed 2025-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yashshingvi/databricks-genie-MCP.git`</sub>
- **[mbrummerstedt/powerbi-analyst-mcp](https://github.com/mbrummerstedt/powerbi-analyst-mcp)** — Query Power BI semantic models: browse workspaces, tables and measures, run DAX queries and page large results via local CSV
  <sub>★ 14 · Python · MIT · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install powerbi-analyst-mcp`</sub>
- **[jwaxman19/qlik-mcp](https://github.com/jwaxman19/qlik-mcp)** — Query Qlik Cloud apps and sheets and extract data from visualizations, with authentication and rate-limiting support
  <sub>★ 11 · TypeScript · MIT · docker · pushed 2025-07-27 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --env-file .env qlik-mcp`</sub>
- **[flowcore/mcp-flowcore-platform](https://github.com/flowcore-io/mcp-flowcore-platform)** — Interact with Flowcore to perform actions, ingest data, and analyze and cross-reference data in your own or public data cores
  <sub>★ 9 · TypeScript · npm · pushed 2025-05-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @flowcore/platform-mcp-server`</sub>
- **[alanpcf/brasil-data-mcp](https://github.com/alanpcf/brasil-data-mcp)** — Brazilian public data via BrasilAPI: companies (CNPJ), addresses (CEP), banks (BACEN) and national holidays
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y brasil-data-mcp`</sub>
- **[dan1d/mercadolibre-mcp](https://github.com/dan1d/mercadolibre-mcp)** — Search MercadoLibre products, get item details, browse categories, track trends and convert currencies across Latin America
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-03-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dan1d/mercadolibre-mcp.git`</sub>
- **[1luvc0d3/metabase-mcp](https://github.com/1luvc0d3/metabase-mcp)** — Metabase integration: natural-language data analysis, dashboard management, SQL queries and automated insights, with SQL guardrails and audit logging
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ai-1luvc0d3/metabase-mcp`</sub>
- **[soil-dev/capsulemcp](https://github.com/soil-dev/capsulemcp)** — Capsule CRM: contacts, opportunities, projects, tasks, timeline activity, filters, workflow tracks and file attachments, with an optional read-only mode
  <sub>★ 5 · TypeScript · Apache-2.0 · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/soil-dev/capsulemcp.git`</sub>
- **[aegis-dq/aegis-dq](https://github.com/aegis-dq/aegis-dq)** — Data quality checks on DuckDB, BigQuery, Athena, Databricks and Postgres, with LLM root-cause analysis of failures and proposed SQL remediations
  <sub>★ 4 · Python · pip · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install aegis-dq`</sub>
- **[alkemiai/alkemi-mcp](https://github.com/alkemi-ai/alkemi-mcp)** — Query Snowflake, Google BigQuery and Databricks data products in natural language through Alkemi
  <sub>★ 4 · JavaScript · MIT · source · pushed 2025-10-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alkemi-ai/alkemi-mcp.git`</sub>
- **[Castaldo-Solutions/mcp-vtenext](https://github.com/Castaldo-Solutions/mcp-vtenext)** — Query, create and update opportunities and contacts in VTENext, an open-source vtiger-based CRM, via its WebService API
  <sub>★ 4 · JavaScript · MIT · source · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Castaldo-Solutions/mcp-vtenext.git`</sub>
- **[AirSaiga/Precis](https://github.com/AirSaiga/Precis)** — Local-first data quality workbench for Excel/CSV: validate against schemas and 10 zero-code constraint types (uniqueness, ranges, foreign keys, allowed values and more), with row-level error reports. Also ships a visual desktop app, CLI and REST API
  <sub>★ 3 · Python · Apache-2.0 · pip · pushed 2026-10-22 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`pip install "precis-cli[mcp]" # 安装后获得 precis-mcp 命令`</sub>
- **[avisangle/method-crm-mcp](https://github.com/avisangle/method-crm-mcp)** — Method CRM API integration: manage tables, files, users, events and API keys, with rate limiting and retries
  <sub>★ 3 · Python · MIT · npx · pushed 2025-11-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector python src/method_mcp/server.py`</sub>
- **[Evan-Crx/permisapi-mcp](https://github.com/Evan-Crx/permisapi-mcp)** — Search French building permits (Sitadel open data), cross-referenced with DVF transactions, PLU zoning and BRGM natural and technological risks
  <sub>★ 3 · Python · MIT · uv · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --python 3.11 permisapi-mcp`</sub>
- **[Hug0x0/mcp-reunion](https://github.com/Hug0x0/mcp-reunion)** — Open data for La Réunion (French overseas region) from data.gouv.fr and the regional portal: economy, demographics, transport, health, education and more
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Hug0x0/mcp-reunion.git`</sub>
- **[Osseni94/oyemi-mcp](https://github.com/Osseni94/oyemi-mcp)** — Deterministic, lexicon-based semantic word encoding and valence analysis: word-to-code mapping, semantic similarity and synonym/antonym lookup
  <sub>★ 3 · Python · pip · pushed 2025-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install oyemi-mcp`</sub>
- **[paracetamol951/caisse-enregistreuse-mcp-server](https://github.com/paracetamol951/caisse-enregistreuse-mcp-server)** — Automate or monitor business operations: sales recording, POS software and CRM
  <sub>★ 3 · TypeScript · GPL-3.0 · npx · pushed 2026-04-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx caisse-enregistreuse-mcp-server --shopid=YOUR_SHOPID --apikey=YOUR_APIKEY`</sub>
- **[r3dz4r/datapulse-my](https://github.com/r3dz4r/datapulse-my)** — Trust checks for Malaysian public datasets: freshness, licence, provenance and drift, with signed evidence and an offline-verifiable attestation chain
  <sub>★ 3 · Python · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/r3dz4r/datapulse-my.git`</sub>
- **[Sugra-Systems/sugra-api-mcp](https://github.com/Sugra-Systems/sugra-api-mcp)** — World data from primary sources via the Sugra API: markets, macroeconomics, company fundamentals, government, news, climate, maritime and entity screening
  <sub>★ 3 · Python · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add https://mcp.sugra.ai`</sub>
- **[Alessandro114/scala-mcp-server](https://github.com/Alessandro114/scala-mcp-server)** — Search and enrich company data: lookup by name, VAT or ID, NACE sector search, and financial data from official EU business registries
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y scala-mcp-server`</sub>
- **[antonio-mello-ai/mcp-airflow](https://github.com/antonio-mello-ai/mcp-airflow)** — Manage Apache Airflow via its REST API: list DAGs, inspect runs and task instances, trigger runs, and check failed DAGs and scheduler health
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-airflow`</sub>
- **[Autario/autario-mcp](https://github.com/Autario/autario-mcp)** — Search and query public datasets from the World Bank, IMF, Eurostat, OECD and WHO, and publish charts
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx autario-mcp`</sub>
- **[vinvuk/apiverket-mcp](https://github.com/vinvuk/apiverket-mcp)** — Query Swedish public data through Apiverket, including company data, SCB statistics, weather, transport and more
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vinvuk/apiverket-mcp.git`</sub>
- **[FreelexHo/power-bi-mcp](https://github.com/FreelexHo/power-bi-mcp)** — Power BI refresh with table-level polling and retry, refresh diagnostics, DAX queries with RLS simulation, PBIP source locating and refresh reports
  <sub>★ 2 · Python · MIT · clone · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FreelexHo/power-bi-mcp.git`</sub>
- **[meacheal-ai/mrc-data](https://github.com/meacheal-ai/mrc-data)** — China apparel supply chain data: verified suppliers, lab-tested fabrics and industrial clusters, with AATCC, ISO and GB lab-test verification
  <sub>★ 2 · Shell · source · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/meacheal-ai/mrc-data.git`</sub>
- **[Osseni94/keyneg-mcp](https://github.com/Osseni94/keyneg-mcp)** — Fine-grained sentiment analysis, keyword extraction and batch processing
  <sub>★ 2 · Python · pip · pushed 2025-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install keyneg-mcp`</sub>
- **[Kemetra/seshat-bi](https://github.com/Kemetra/Seshat-BI)** — Read-only BI pipeline governance: each table's stage from source to Power BI, what blocks the next stage, static SQL/TMDL/PBIR checks and evidence packs
  <sub>★ 2 · Python · Apache-2.0 · uv · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from seshat-bi seshat demo init`</sub>
- **[us-all/airflow-mcp-server](https://github.com/us-all/airflow-mcp-server)** — Airflow REST API: list DAGs, runs and task instances, tail logs and roll up DAG health. Read-only by default; trigger and clear are write-gated
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @us-all/airflow-mcp`</sub>
- **[dockndevai/mcp-debezium](https://github.com/dockndevai/mcp-debezium)** — Monitor and manage Debezium and Kafka Connect CDC connectors, with access modes, connector allowlists, delete gating and credential redaction
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-debezium.git`</sub>
- **[dockndevai/mcp-kafka](https://github.com/dockndevai/mcp-kafka)** — Monitor and manage Apache Kafka clusters, topics and consumer groups (including lag), with access modes, topic allowlists and delete gating
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-kafka.git`</sub>
- **[sam1siam/astrofabric-mcp](https://github.com/sam1siam/astrofabric-mcp)** — Business intelligence: company and contact discovery, verification, enrichment, business signals, lists and governed delivery
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-09-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g astrofabric`</sub>
- **[carrierone/verilexdata-mcp](https://github.com/carrierone/verilexdata-mcp)** — Pay-per-query x402 datasets: NPI healthcare, SEC filings, OFAC sanctions, crypto whales, Polymarket signals, patents and economic indicators
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-03-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/carrierone/verilexdata-mcp.git`</sub>
- **[flexorch/flexorch-mcp](https://github.com/flexorch/flexorch-mcp)** — Turn business documents (PDFs, invoices, contracts, payroll) into structured datasets with classification, field extraction, PII masking and quality scoring
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install flexorch-mcp`</sub>
- **[saikiyusuke/registep-mcp](https://github.com/asicojp/registep-mcp)** — POS and sales analytics for AirREGI, Smaregi and BASE e-commerce: store management, sales data queries, AI chat analysis and weather correlation
  <sub>★ 1 · TypeScript · source · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/saikiyusuke/registep-mcp.git`</sub>
- **[Younghef/nutriref-api](https://github.com/Younghef/nutriref-api)** — USDA FoodData Central nutrition data, paid per call via x402 (USDC on Base): food search, details, comparisons and recipes
  <sub>★ 1 · Python · MIT · uv · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx nutriref-mcp`</sub>
- **[Leekangbum/networklytics-mcp](https://github.com/Leekangbum/networklytics-mcp)** — Social network analysis of YouTube comments: influencer centrality ranking, Louvain community detection and sentiment analysis
  <sub>★ 1 · Python · pip · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install networklytics-mcp`</sub>
- **[equinoxaifinance-rgb/civicdataforge-mcp](https://github.com/equinoxaifinance-rgb/civicdataforge-mcp)** — US government records (short-term rental permits, lodging licenses, property violations, healthcare exclusions, EPA ECHO) and Norwegian company data
  <sub>JavaScript · MIT · source · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/equinoxaifinance-rgb/civicdataforge-mcp.git`</sub>
- **[datanika-io/datanika-core](https://github.com/datanika-io/datanika-core/tree/master/datanika-mcp)** — Datanika, the open-source ELT and dbt platform: browse connections, preview data, run dbt transforms, monitor runs and manage pipelines. Read-only by default
  <sub>Python · AGPL-3.0 · in-repo · pushed 2026-09-26</sub>
  <sub>`git clone https://github.com/datanika-io/datanika-core.git && cd datanika-core/datanika-mcp`</sub>
- **[greencalculus/greencalculus-mcp](https://github.com/greencalculus/greencalculus-mcp)** — Greenhouse-gas emission factors and carbon calculations (activity, embodied EN 15978, PCAF financed emissions) with source references and data versions
  <sub>JavaScript · MIT · source · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/greencalculus/greencalculus-mcp.git`</sub>

## end to end RAG platforms

- **[vectara/vectara-mcp](https://github.com/vectara/vectara-mcp)** — Access Vectara's RAG-as-a-service platform
  <sub>★ 29 · Python · Apache-2.0 · pip · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install vectara-mcp`</sub>
- **[notwhiteblank/scholar-rag-mcp](https://github.com/notwhiteblank/scholar-rag-mcp)** — Academic paper knowledge base over local PDFs: MinerU parsing, metadata normalization, Qdrant vector search with reranking and paginated full-text reading
  <sub>★ 5 · Python · MIT · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx scholar-rag-mcp # download and start the MCP server (stdio)`</sub>
- **[poll-the-people/customgpt-mcp](https://github.com/Poll-The-People/customgpt-mcp)** — Access the CustomGPT.ai RAG-as-a-service API
  <sub>★ 5 · Python · MIT · docker · pushed 2026-10-10 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 -e CUSTOMGPT_API_BASE=https://app.customgpt.ai customgpt-mcp`</sub>
- **[gogabrielordonez/mcp-ragchat](https://github.com/gogabrielordonez/mcp-ragchat)** — Add RAG-based AI chat to any website: local vector store, OpenAI, Anthropic or Gemini models, a self-contained chat server and an embeddable widget
  <sub>★ 2 · TypeScript · clone · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gogabrielordonez/mcp-ragchat`</sub>
- **[andyliszewski/grounding-ai](https://github.com/andyliszewski/grounding-ai)** — Local searchable index of PDFs, EPUBs and Word documents for grounded answers with page and section citations
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install grounding-ai`</sub>
- **[zaharajabeen13-create/ai-rete-rag-mcp](https://github.com/zaharajabeen13-create/ai-rete-rag-mcp)** — Rule-based decisions: a Rete engine returns verdicts explained via retrieval over your policy documents, with rules drafted from policy text and saved as YAML
  <sub>Python · MIT · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx ai-rete-rag-mcp`</sub>

## Knowledge &amp; Memory

- **[upstash/context7](https://github.com/upstash/context7)** — Up-to-date code documentation for LLMs and AI code editors
  <sub>★ 63.5k · TypeScript · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upstash/context7.git`</sub>
- **[vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)** — Hindsight: long-term memory for AI agents modeled on human memory
  <sub>★ 52.7k · Python · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[skill-seekers/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)** — Turn docs, GitHub repos, PDFs, videos, Confluence, Notion and Slack/Discord into AI skills and RAG knowledge, exportable to vector databases like Qdrant
  <sub>★ 15.2k · Python · MIT · pip · pushed 2026-09-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install skill-seekers`</sub>
- **[basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory)** — Local-first AI memory: a semantic knowledge graph of Markdown files that humans and LLMs both read and write, with optional cloud sync and team workspaces
  <sub>★ 4.3k · Python · AGPL-3.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add basicmachines-co/basic-memory/skills -g`</sub>
- **[gamosoft/NoteDiscovery](https://github.com/gamosoft/NoteDiscovery)** — Self-hosted Markdown knowledge base with a web UI: search, read, create, edit, tag and template notes
  <sub>★ 2.8k · JavaScript · MIT · docker · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -d --name notediscovery -p 8000:8000 \`</sub>
- **[moorcheh-ai/memanto](https://github.com/moorcheh-ai/memanto)** — Universal memory agent for AI: provides semantic search, namespace management, text/vector operations and RAG for local or remote environments
  <sub>★ 2.3k · Python · MIT · pip · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install memanto`</sub>
- **[doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)** — Memory service with semantic search, persistent storage and autonomous memory consolidation
  <sub>★ 2k · Python · Apache-2.0 · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-memory-service`</sub>
- **[bitbonsai/mcp-obsidian](https://github.com/bitbonsai/mcpvault)** — Safe read/write access to Obsidian vaults: search, batch operations, tag management and frontmatter handling
  <sub>★ 1.7k · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector npx @bitbonsai/mcpvault@latest /path/to/your/vault`</sub>
- **[apecloud/ApeRAG](https://github.com/apecloud/ApeRAG)** — RAG platform combining Graph RAG, vector search and full-text search for building knowledge graphs and context engineering
  <sub>★ 1.3k · Python · Apache-2.0 · helm · pushed 2026-09-12 · WSL2 · Linux · Docker</sub>
  <sub>`helm install aperag ./deploy/aperag --namespace default --create-namespace`</sub>
- **[vshulcz/deja-vu](https://github.com/vshulcz/deja-vu)** — Local memory over session histories from Claude Code, Codex CLI and opencode: lexical search, session-start auto-recall, secret redaction and SSH sync
  <sub>★ 1.3k · Go · MIT · winget · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install vshulcz.deja-vu`</sub>
- **[fabio-rovai/open-ontologies](https://github.com/fabio-rovai/open-ontologies)** — Ontology engineering for OWL, RDF and SPARQL: validate, query, diff, lint, version and govern knowledge graphs on an Oxigraph triple store
  <sub>★ 1.2k · Rust · MIT · source · pushed 2026-10-17 · macOS · Linux</sub>
  <sub>`git clone https://github.com/fabio-rovai/open-ontologies.git`</sub>
- **[chatmcp/mcp-server-chatsum](https://github.com/chatmcp/mcp-server-chatsum)** — Query and summarize your chat messages with AI prompts
  <sub>★ 1k · TypeScript · source · pushed 2024-12-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chatmcp/mcp-server-chatsum.git`</sub>
- **[CodeAbra/iai-personal-memory-engine](https://github.com/CodeAbra/iai-personal-memory-engine)** — Local memory daemon with episodic, semantic and procedural tiers, SQLite and hnswlib storage, sleep-cycle consolidation and AES-256-GCM encryption at rest
  <sub>★ 911 · Python · MIT · script · pushed 2026-10-22 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/CodeAbra/iai-personal-memory-engine/main/scripts/bootstrap.sh | bash`</sub>
- **[riponcm/projectmem](https://github.com/riponcm/projectmem)** — Local-first memory for coding agents: records issues, failed attempts, fixes and decisions, re-injects them and warns at git commit before a repeated mistake
  <sub>★ 868 · Python · MIT · pip · pushed 2026-10-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install projectmem`</sub>
- **[agentic-mcp-tools/memora](https://github.com/agentic-box/memora)** — Persistent memory with knowledge graph visualization, semantic/hybrid search, cloud sync (S3/R2) and cross-session context management
  <sub>★ 744 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx wrangler d1 create memora-graph`</sub>
- **[chenxiachan/thoughtdag](https://github.com/chenxiachan/thoughtdag)** — Search local AI-agent conversation history by file or exact phrase and recall original source turns through four read-only tools
  <sub>★ 676 · TypeScript · MIT · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g thoughtdag`</sub>
- **[samvallad33/vestige](https://github.com/samvallad33/vestige)** — Local-first cognitive agent memory with FSRS-6 scheduling, smart ingest, SQLite storage, portable sync, an embedded dashboard and optional hooks
  <sub>★ 655 · Rust · AGPL-3.0 · npx · pushed 2026-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @vestige/init`</sub>
- **[Ikalus1988/MisakaNet](https://github.com/Ikalus1988/MisakaNet)** — Agent failure memory: search verified debugging lessons from real engineering sessions
  <sub>★ 543 · Python · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx @misaka-net/misakanet-setup`</sub>
- **[TeleAI-UAGI/telemem](https://github.com/TeleAI-UAGI/telemem)** — Mem0-compatible long-term and multimodal agent memory: character-isolated profiles, semantic deduplication, optional local stack and video memory with QA
  <sub>★ 494 · Python · Apache-2.0 · uv · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx telemem`</sub>
- **[juyterman1000/entroly](https://github.com/juyterman1000/entroly)** — Context control layer for coding agents: compression, prompt-prefix stabilization for caching, cheaper-model routing, local hallucination checks and memory
  <sub>★ 479 · Python · Apache-2.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g entroly`</sub>
- **[Beever-AI/beever-atlas](https://github.com/Beever-AI/beever-atlas)** — Team knowledge base turning Slack, Discord, Teams and Mattermost chats into a knowledge graph and wiki with cited answers, semantic search and expert finding
  <sub>★ 451 · Python · Apache-2.0 · clone · pushed 2026-09-10 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/beever-ai/beever-atlas.git`</sub>
- **[shinpr/mcp-local-rag](https://github.com/shinpr/mcp-local-rag)** — Local document search: semantic search over PDF, DOCX, TXT and Markdown files with LanceDB vector storage and local embeddings
  <sub>★ 416 · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-local-rag ingest ./docs/`</sub>
- **[graphlit-mcp-server](https://github.com/graphlit/graphlit-mcp-server)** — Ingest content from Slack, Discord, websites, Google Drive, Linear or GitHub into a Graphlit project, then search and retrieve relevant knowledge
  <sub>★ 377 · TypeScript · MIT · npx · pushed 2026-01-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y graphlit-mcp-server`</sub>
- **[Goldentrii/AgentRecall](https://github.com/Goldentrii/AgentRecall-X)** — Persistent cross-session agent memory that surfaces the most relevant past memories using the Intelligent Distance Protocol
  <sub>★ 371 · JavaScript · MIT · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-recall-cli recall "rate limiting"`</sub>
- **[CheMiguel23/MemoryMesh](https://github.com/CheMiguel23/MemoryMesh)** — Graph-based memory focused on AI role-play and story generation
  <sub>★ 354 · TypeScript · MIT · clone · pushed 2026-03-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/CheMiguel23/memorymesh.git`</sub>
- **[varun29ankuS/shodh-memory](https://github.com/varun29ankuS/shodh-memory)** — Cognitive agent memory with Hebbian learning, a three-tier architecture and knowledge graphs, running offline on edge devices
  <sub>★ 314 · Rust · Apache-2.0 · npx · pushed 2026-10-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @shodh/memory-mcp setup-hooks`</sub>
- **[lyonzin/knowledge-rag](https://github.com/lyonzin/knowledge-rag)** — Offline RAG for Claude Code with hybrid BM25 and semantic search, cross-encoder reranking, Markdown-aware chunking and query expansion
  <sub>★ 301 · Python · MIT · npx · pushed 2026-10-16 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add lyonzin/knowledge-rag`</sub>
- **[ohad6k/emulo](https://github.com/ohad6k/emulo)** — Loads a personal profile mined from your local Claude Code, Codex and OpenCode logs so agents work the way you do
  <sub>★ 298 · HTML · MIT · npx · pushed 2026-10-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add ohad6k/emulo@emulo`</sub>
- **[jinzcdev/markmap-mcp-server](https://github.com/jinzcdev/markmap-mcp-server)** — Convert Markdown into interactive markmap mind maps with PNG/JPG/SVG export and live browser preview
  <sub>★ 289 · TypeScript · MIT · npx · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @jinzcdev/markmap-mcp-server`</sub>
- **[sachitrafa/YourMemory](https://github.com/sachitrafa/YourMemory)** — Persistent agent memory with Ebbinghaus-style decay, hybrid BM25/vector retrieval, entity graph for multi-hop reasoning, auto-pruning and a browser dashboard
  <sub>★ 270 · Python · pip · pushed 2026-09-19 · macOS</sub>
  <sub>`pip install yourmemory`</sub>
- **[hannesrudolph/mcp-ragdocs](https://github.com/hannesrudolph/mcp-ragdocs)** — Retrieve and process documentation through vector search to augment responses with relevant documentation context
  <sub>★ 265 · TypeScript · MIT · source · pushed 2025-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hannesrudolph/mcp-ragdocs.git`</sub>
- **[l33tdawg/sage](https://github.com/l33tdawg/sage)** — Local institutional memory for agents where BFT consensus among validators approves every memory before it is committed
  <sub>★ 256 · Go · Apache-2.0 · docker · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name sage \`</sub>
- **[omega-memory/omega-memory](https://github.com/omega-memory/omega-memory)** — Local-first persistent memory for coding agents with semantic search, auto-capture, cross-session learning and intelligent forgetting
  <sub>★ 225 · Python · Apache-2.0 · uv · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "omega-memory[server]"`</sub>
- **[GistPad-MCP](https://github.com/lostintangent/gistpad-mcp)** — Manage personal knowledge, daily notes and reusable prompts in GitHub Gists, as a companion to GistPad
  <sub>★ 207 · TypeScript · MIT · source · pushed 2026-01-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lostintangent/gistpad-mcp.git`</sub>
- **[alibaizhanov/mengram](https://github.com/alibaizhanov/mengram)** — Agent memory with semantic, episodic and procedural types, a knowledge graph, Claude Code auto-save/recall hooks, smart triggers and multi-user isolation
  <sub>★ 204 · Python · Apache-2.0 · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mengram-ai # or: npm install mengram-ai`</sub>
- **[roomi-fields/notebooklm-mcp](https://github.com/roomi-fields/notebooklm-mcp)** — Automate Google NotebookLM: Q&amp;A with citations, audio podcasts, video, content generation, source management and notebook library
  <sub>★ 204 · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @roomi-fields/notebooklm-mcp@<pinned-version>`</sub>
- **[pi22by7/In-Memoria](https://github.com/pi22by7/In-Memoria)** — Cumulative memory and pattern learning for coding assistants, with local SQLite/SurrealDB storage for semantic codebase analysis
  <sub>★ 175 · Rust · MIT · npm · pushed 2025-12-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g in-memoria`</sub>
- **[0xshellming/mcp-summarizer](https://github.com/0xshellming/mcp-summarizer)** — Summarize plain text, web pages, PDF documents, EPUB books and HTML content
  <sub>★ 167 · JavaScript · source · pushed 2025-02-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0xshellming/mcp-summarizer.git`</sub>
- **[entanglr/zettelkasten-mcp](https://github.com/entanglr/zettelkasten-mcp)** — Zettelkasten knowledge management: create, link and search atomic notes
  <sub>★ 167 · Python · MIT · clone · pushed 2025-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/entanglr/zettelkasten-mcp.git`</sub>
- **[kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero)** — Work with collections and sources in your Zotero Cloud library
  <sub>★ 164 · TypeScript · MIT · npm · pushed 2025-02-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-zotero`</sub>
- **[dnotitia/akb](https://github.com/dnotitia/akb)** — Organizational knowledge base: Markdown docs, PostgreSQL tables and files linked by a URI graph, with hybrid search, Git history and multi-tenant ACLs
  <sub>★ 163 · Python · docker · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -v "$AKB_NATIVE_CONFIG_DIR:/installation" \`</sub>
- **[Patdolitse/piia-engram](https://github.com/Patdolitse/piia-engram)** — Persistent user identity across AI tools: preferences, lessons and decisions in local JSON with staged verification, AES-256-GCM encryption and cross-tool sync
  <sub>★ 162 · Python · AGPL-3.0 · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install piia-engram`</sub>
- **[dcostenco/prism-mcp](https://github.com/dcostenco/prism-coder)** — Local SQLite agent memory with a web dashboard, session rewind/replay, cross-client memory sharing, morning briefings and progressive context loading
  <sub>★ 157 · TypeScript · Apache-2.0 · npm · pushed 2026-10-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g prism-mcp-server`</sub>
- **[redleaves/context-keeper](https://github.com/redleaves/context-keeper)** — LLM-driven context and memory management: short- and long-term memory with vector, timeline and knowledge graph retrieval plus reranking
  <sub>★ 155 · Go · MIT · clone · pushed 2026-01-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/redleaves/context-keeper.git`</sub>
- **[sheawinkler/ContextLattice](https://github.com/sheawinkler/ContextLattice)** — Private-by-default memory and context layer for agents with staged retrieval across fused data backends and long-horizon context continuity
  <sub>★ 155 · Go · Apache-2.0 · brew · pushed 2026-10-21 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew tap sheawinkler/contextlattice`</sub>
- **[cameronrye/openzim-mcp](https://github.com/cameronrye/openzim-mcp)** — Search and navigate Wikipedia and other ZIM-format knowledge archives offline, with smart retrieval and caching
  <sub>★ 145 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @smithery/cli mcp add rye/openzim-mcp --client claude`</sub>
- **[ProfessionalWiki/MediaWiki-MCP-Server](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server)** — Read, search and edit any MediaWiki wiki, including Wikipedia and Fandom, with multi-wiki support and Semantic MediaWiki, Cargo, Wikibase and NeoWiki queries
  <sub>★ 138 · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx add-mcp @professional-wiki/mediawiki-mcp-server`</sub>
- **[deusXmachina-dev/memorylane](https://github.com/deusXmachina-dev/memorylane)** — Desktop app that captures screen activity, stores AI summaries and OCR text locally, and exposes the history via semantic search and a timeline
  <sub>★ 120 · TypeScript · GPL-3.0 · source · pushed 2026-10-21 · Win? · macOS</sub>
  <sub>`git clone https://github.com/deusXmachina-dev/memorylane.git`</sub>
- **[dat999zx/knowl](https://github.com/dat999zx/knowl)** — Persistent local memory for coding agents that retires replaced facts at write time, so agents read the current answer; facts are typed with provenance
  <sub>★ 114 · TypeScript · Apache-2.0 · npm · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @dat999zx/knowl`</sub>
- **[elvismdev/mem0-mcp-selfhosted](https://github.com/elvismdev/mem0-mcp-selfhosted)** — Self-hosted mem0 for Claude Code: Qdrant vector search, Neo4j knowledge graph, Ollama embeddings and session hooks for automatic cross-session memory
  <sub>★ 111 · Python · MIT · source · pushed 2026-03-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/elvismdev/mem0-mcp-selfhosted.git`</sub>
- **[HiAi-gg/docsmint](https://github.com/HiAi-gg/docsmint)** — Cloud or self-hosted knowledge workspace with hybrid document search, GraphRAG, and scoped MCP tools for reading and updating documents
  <sub>★ 110 · TypeScript · Apache-2.0 · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`bunx --package @hiai-gg/docsmint docsmint init \`</sub>
- **[kunwar-shah/claudex](https://github.com/kunwar-shah/claudex)** — Persistent memory and full-text search over Claude Code conversation history indexed into SQLite, with session summaries and a web UI for exploration
  <sub>★ 97 · JavaScript · MIT · npm · pushed 2026-06-20 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @kunwarshah/claudex [https://www.npmjs.com/package/@kunwarshah/claudex]`</sub>
- **[IvenKooLab/loci](https://github.com/IvenKooLab/loci)** — Queryable second brain over your scattered notes, docs, PDFs and chat exports: hybrid retrieval (vector + BM25 fused with RRF), section-level citations with an optional claim-by-claim verification pass, and an Obsidian-style wikilink graph — all local, any OpenAI-compatible API or fully offline via Ollama. pip install loci-rag then run loci-mcp
  <sub>★ 94 · Python · MIT · clone · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/IvenKooLab/loci.git`</sub>
- **[DomDemetz/claude-soul](https://github.com/DomDemetz/claude-soul)** — Learning engine for Claude Code: extracts signals from sessions, runs periodic reflections and promotes or retires behavioral frameworks based on evidence
  <sub>★ 92 · TypeScript · MIT · npm · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claude-soul@latest`</sub>
- **[ragieai/mcp-server](https://github.com/ragieai/ragie-mcp-server)** — Retrieve context from your Ragie knowledge base, connected to sources like Google Drive, Notion and Jira
  <sub>★ 91 · JavaScript · MIT · npx · pushed 2026-02-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @ragieai/mcp-server --partition optional_partition_id`</sub>
- **[arthurpanhku/Arthor-Agent](https://github.com/arthurpanhku/DocSentinel)** — Cybersecurity assessment of documents, questionnaires and reports: multi-format parsing, RAG knowledge base, risks, compliance gaps and remediations
  <sub>★ 88 · Python · MIT · clone · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/arthurpanhku/DocSentinel.git`</sub>
- **[Pantheon-Security/notebooklm-mcp-secure](https://github.com/Pantheon-Security/notebooklm-mcp-secure)** — Security-hardened Google NotebookLM access: session-based conversations, notebook library management and source-grounded answers, with post-quantum encryption
  <sub>★ 87 · TypeScript · MIT · source · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Pantheon-Security/notebooklm-mcp-secure.git`</sub>
- **[tenequm/pond](https://github.com/tenequm/pond)** — Lossless archive and search for AI agent sessions across clients
  <sub>★ 86 · Rust · Apache-2.0 · scoop · pushed 2026-10-14 · Win · WSL2 · macOS · Linux</sub>
  <sub>`scoop bucket add tenequm https://github.com/tenequm/scoop-bucket # Windows scoop install tenequm/pond`</sub>
- **[teolex2020/AuraSDK](https://github.com/teolex2020/aura-memory)** — Persistent, encrypted cognitive memory that works offline
  <sub>★ 85 · Rust · MIT · source · pushed 2026-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/teolex2020/AuraSDK.git`</sub>
- **[zcag/tela](https://github.com/zcag/tela)** — Self-hostable Markdown team wiki that agents can search, read and write, plus Atlas, which generates a cited wiki from git repos and Jira
  <sub>★ 85 · Go · AGPL-3.0 · clone · pushed 2026-10-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/zcag/tela.git`</sub>
- **[decisionnode/DecisionNode](https://github.com/decisionnode/DecisionNode)** — Record development decisions as structured JSON with Gemini embeddings and search them semantically from a local store shared across AI tools
  <sub>★ 83 · TypeScript · MIT · npm · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g decisionnode`</sub>
- **[dodopayments/contextmcp](https://github.com/dodopayments/context-mcp)** — Self-hosted documentation indexer that serves docs from various sources to agents with semantic search
  <sub>★ 83 · TypeScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx contextmcp init my-docs-mcp`</sub>
- **[adelinamart/robrain](https://github.com/adelinamart/robrain)** — Self-hosted decision memory for coding agents: captures architectural decisions and rejected alternatives, and warns before a rejected approach is re-proposed
  <sub>★ 81 · TypeScript · Apache-2.0 · npx · pushed 2026-10-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx robrain@latest up # start Postgres + Perception from ghcr.io`</sub>
- **[cdeust/Cortex](https://github.com/cdeust/Cortex)** — Neuroscience-inspired memory for Claude Code on PostgreSQL/pgvector: decay, consolidation, a predictive-coding write gate and lifecycle hooks
  <sub>★ 75 · Python · MIT · source · pushed 2026-10-22 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/cdeust/Cortex.git`</sub>
- **[kunickiaj/codemem](https://github.com/kunickiaj/codemem)** — Persistent coding memory across sessions, machines and teammates, with memory search, optional sync, project sharing and automatic capture
  <sub>★ 73 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codemem`</sub>
- **[vbcherepanov/total-agent-memory](https://github.com/vbcherepanov/total-agent-memory)** — Local memory for coding agents: temporal knowledge graph with fact invalidation, procedural and episodic memory, AST codebase ingest and cross-project analogy
  <sub>★ 73 · Python · MIT · npx · pushed 2026-10-14 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx -y total-agent-memory connect claude-code`</sub>
- **[ccf/agentcairn](https://github.com/ccf/agentcairn)** — Local-first agent memory: a Markdown Obsidian vault as source of truth plus a rebuildable DuckDB index for hybrid BM25, vector and graph recall
  <sub>★ 68 · Python · Apache-2.0 · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ccf/agentcairn --skill agentcairn-setup -g`</sub>
- **[writerslogic/scrivener-mcp](https://github.com/writerslogic/scrivener-mcp)** — Work with Scrivener 3 writing projects: document management, writing analysis, semantic search, character and plot memory, and content enhancement
  <sub>★ 67 · TypeScript · AGPL-3.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g scrivener-mcp`</sub>
- **[unibaseio/membase-mcp](https://github.com/unibaseio/membase)** — Save and query agent memory in a distributed way with Membase
  <sub>★ 66 · Python · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @unibaseio/membase-cli # the `membase` command (hosted) without Python`</sub>
- **[Battam1111/Myco](https://github.com/Battam1111/Myco)** — Cross-session, cross-project agent memory built on a self-validating filesystem graph derived from ASTs and Markdown links, not embeddings
  <sub>★ 65 · Rust · MIT · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Battam1111/Myco.git`</sub>
- **[SecurityRonin/docx-mcp](https://github.com/SecurityRonin/docx-mcp)** — Read and edit Word (.docx) documents with tracked changes, threaded comments, footnotes, OOXML-level validation and document auditing
  <sub>★ 65 · Python · MIT · pip · pushed 2026-08-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install docx-mcp-server`</sub>
- **[tomohiro-owada/devrag](https://github.com/tomohiro-owada/devrag)** — Local RAG for semantic vector search over Markdown documents with sqlite-vec and multilingual-e5-small embeddings, filterable by directory and filename
  <sub>★ 64 · Go · source · pushed 2026-04-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/tomohiro-owada/devrag.git`</sub>
- **[bh-rat/context-awesome](https://github.com/bh-rat/context-awesome)** — Search curated awesome lists and fetch the most relevant resources for your agent
  <sub>★ 61 · TypeScript · MIT · npm · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g context-awesome`</sub>
- **[ZengLiangYi/ChatCrystal](https://github.com/ZengLiangYi/ChatCrystal)** — Local-first memory for AI coding conversations: imports chats from coding assistants into notes with semantic search, tag graphs and Markdown export
  <sub>★ 61 · TypeScript · Apache-2.0 · npm · pushed 2026-10-22 · Win · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g chatcrystal`</sub>
- **[JinyangWang27/people-context](https://github.com/JinyangWang27/people-context)** — Local-first memory about the people in your life: identity resolution, relationships, facts, interactions, reminders and communication guidance
  <sub>★ 58 · Python · MIT · uv · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from people-context pctx demo --reset`</sub>
- **[roampal-ai/roampal-core](https://github.com/roampal-ai/roampal-core)** — Outcome-based persistent memory for Claude Code and OpenCode: memories that help get promoted, misleading ones get demoted
  <sub>★ 54 · Python · Apache-2.0 · pip · pushed 2026-09-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install roampal`</sub>
- **[tstockham96/engram](https://github.com/tstockham96/engram)** — Agent memory with semantic recall, automatic consolidation, contradiction detection and a bi-temporal knowledge graph
  <sub>★ 47 · TypeScript · MIT · npm · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g engram-sdk`</sub>
- **[BetaBots-LLC/callimachus](https://github.com/BetaBots-LLC/callimachus)** — Local hybrid search (SQLite FTS5 and on-device vectors) over coding-agent conversation history from multiple tools, so agents can recall their past work
  <sub>★ 46 · Rust · AGPL-3.0 · cargo · pushed 2026-07-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --path apps/desktop/src-tauri --bin callimachus-mcp`</sub>
- **[DollhouseMCP/mcp-server](https://github.com/DollhouseMCP/mcp-server)** — Reusable personas, skills, templates, agents and memory for AI clients, with dynamic permissions, versioning and a public collection of shareable content
  <sub>★ 46 · TypeScript · AGPL-3.0 · npx · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @dollhousemcp/mcp-server@latest --web`</sub>
- **[pallaprolus/mendeley-mcp](https://github.com/pallaprolus/mendeley-mcp)** — Search your Mendeley library, browse folders, get document metadata, search the global catalog and add papers to your collection
  <sub>★ 46 · Python · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector mendeley-mcp`</sub>
- **[pinecone-io/assistant-mcp](https://github.com/pinecone-io/assistant-mcp)** — Connect to your Pinecone Assistant and retrieve context from its knowledge engine
  <sub>★ 46 · Rust · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector -- docker run -i --rm -e PINECONE_API_KEY -e PINECONE_ASSISTANT_HOST pinecone/assistant-mcp`</sub>
- **[contextstream/mcp-server](https://github.com/contextstream/mcp-server)** — Persistent memory for AI coding tools with semantic code search, knowledge graphs, impact analysis and decision tracking
  <sub>★ 44 · Rust · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @contextstream/mcp-server@latest setup`</sub>
- **[Abhigyan-Shekhar/Waggle-mcp](https://github.com/Abhigyan-Shekhar/Waggle-mcp)** — Persistent graph memory that extracts facts from conversations into typed nodes with local embeddings, supporting temporal queries and conflict detection
  <sub>★ 44 · Python · Apache-2.0 · pipx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install waggle-mcp`</sub>
- **[Wuesteon/lean-memory](https://github.com/Wuesteon/lean-memory)** — Embedded local agent memory in one SQLite file per namespace: hybrid retrieval, append-only history queryable at any past time and human-reviewed maintenance
  <sub>★ 43 · Python · Apache-2.0 · pip · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lean-memory`</sub>
- **[kage-core/Kage](https://github.com/kage-core/Kage)** — Git-native memory for coding agents: JSON entries in the repo, verified against cited code so hallucinated citations are rejected and stale memory is withheld
  <sub>★ 41 · TypeScript · GPL-3.0 · npx · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @kage-core/kage-graph-mcp install`</sub>
- **[LamantinAI/kaeru](https://github.com/LamantinAI/kaeru)** — Memory for LLM agents: a local graph where the agent itself keeps decisions, tasks, hypotheses and reasoning between sessions, and gets a summary of what is open and overdue on every return to a project. Single Rust binary with no embedding model or LLM calls inside; one daemon serves several agents at once, with an optional self-hosted cloud for teams. Works with Claude Code, Codex, Cursor, openc
  <sub>★ 40 · Rust · script · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/LamantinAI/kaeru/main/contrib/install/install.sh | bash`</sub>
- **[max-ramas/rms-memory-mcp](https://github.com/max-ramas/rms-memory-mcp)** — Local-first memory for coding agents: hybrid LanceDB/Tantivy search, Markdown and code indexes, per-project vaults and recall that abstains on low confidence
  <sub>★ 40 · Rust · MIT · psh · pushed 2026-10-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/max-ramas/rms-memory-mcp/master/scripts/install.ps1 | iex`</sub>
- **[linxule/lotus-wisdom-mcp](https://github.com/linxule/lotus-wisdom-mcp)** — Contemplative problem-solving using the Lotus Sutra's framework: multi-perspective reasoning, skillful means, non-dual recognition and meditation pauses
  <sub>★ 36 · TypeScript · MIT · source · pushed 2026-10-19 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/linxule/lotus-wisdom-mcp.git`</sub>
- **[nonatofabio/local-faiss-mcp](https://github.com/nonatofabio/local_faiss_mcp)** — Local FAISS vector database for RAG with document ingestion (PDF, TXT, MD, DOCX), semantic search, re-ranking and CLI tools for indexing and querying
  <sub>★ 36 · Python · MIT · pip · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install local-faiss-mcp`</sub>
- **[Shweta-Mishra-ai/tokenmizer](https://github.com/Shweta-Mishra-ai/tokenmizer)** — Session memory via a local OpenAI-compatible proxy that extracts tasks, decisions and files into a knowledge graph and checkpoints before context overflow
  <sub>★ 34 · Python · MIT · pip · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "tokenmizer[anthropic,cache]"`</sub>
- **[majiayu000/remem](https://github.com/majiayu000/remem)** — Local-first memory for Claude Code and Codex: hooks capture sessions and an LLM distills them into SQLite, with auditable full-text and embedding recall
  <sub>★ 34 · Rust · MIT · npm · pushed 2026-10-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @remem-ai/remem`</sub>
- **[markmhendrickson/neotoma](https://github.com/markmhendrickson/neotoma)** — Deterministic state layer for agents: versioned entities like contacts, tasks and decisions with immutable observations and provenance, in local SQLite
  <sub>★ 34 · HTML · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g neotoma`</sub>
- **[oomkapwn/enquire-mcp](https://github.com/oomkapwn/enquire-mcp)** — Long-term agent memory backed by a local Obsidian vault: hybrid retrieval with reranking, agentic RAG, wikilink community detection, Obsidian Bases and PDF OCR
  <sub>★ 34 · TypeScript · MIT · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @oomkapwn/enquire-mcp`</sub>
- **[rps321321/obsidian-mcp-pro](https://github.com/rps321321/obsidian-mcp-pro)** — Obsidian vault access: full-text search, note CRUD, frontmatter queries, tags, backlinks, graph traversal, orphan and broken link detection, and canvas support
  <sub>★ 33 · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y obsidian-mcp-pro install`</sub>
- **[TT-Wang/cortex-plugin](https://github.com/TT-Wang/memem)** — Claude Code memory plugin that mines past sessions for decisions, conventions and bug fixes, stores them in an Obsidian vault and briefs new sessions
  <sub>★ 32 · Python · MIT · clone · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TT-Wang/memem.git`</sub>
- **[aliasunder/vault-cortex](https://github.com/aliasunder/vault-cortex)** — Standalone Obsidian vault server: hybrid search, notes and files, memory and tasks; run locally or self-host for remote access
  <sub>★ 31 · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx vault-cortex@latest init`</sub>
- **[doobidoo/MCP-Context-Provider](https://github.com/doobidoo/MCP-Context-Provider)** — Static server providing persistent tool-specific context and rules to AI models
  <sub>★ 31 · TypeScript · Apache-2.0 · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://codeberg.org/doobidoo/MCP-Context-Provider.git`</sub>
- **[knaisoma/data-olympus](https://github.com/knaisoma/data-olympus)** — Git-native Markdown knowledge base for coding agents with proposed vs. accepted guidance, validity windows, supersession chains and status-aware retrieval
  <sub>★ 30 · Python · Apache-2.0 · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from data-olympus data-olympus --help`</sub>
- **[geml-spec/geml](https://github.com/geml-spec/geml)** — Address Markdown and GEML documents by block instead of by line: list, get, set, add, delete, rename, revert, find and check one block, with every write re-parsed and refused if it would break the document; plus call-graph queries over a codebase
  <sub>★ 29 · JavaScript · MIT · npm · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g @geml/geml`</sub>
- **[IgorGanapolsky/mcp-memory-gateway](https://github.com/IgorGanapolsky/ThumbGate)** — Pre-action gates that prevent coding agents from repeating known mistakes by turning captured feedback and failures into rules enforced via hooks
  <sub>★ 29 · JavaScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx thumbgate init # Phase 1: hooks only`</sub>
- **[nicholasglazer/gnosis-mcp](https://github.com/nicholasglazer/gnosis-mcp)** — Make Markdown documentation searchable: loads it into SQLite or PostgreSQL with keyword search and optional pgvector hybrid semantic search
  <sub>★ 29 · Python · MIT · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx gnosis-mcp ingest ./docs/`</sub>
- **[kael-bit/engram-rs](https://github.com/kael-bit/engram-rs)** — Hierarchical agent memory engine with automatic decay, promotion, semantic deduplication and a self-organizing topic tree
  <sub>★ 28 · Rust · MIT · psh · pushed 2026-03-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/kael-bit/engram-rs/main/install.ps1 | iex`</sub>
- **[mnemoverse/mcp-memory-server](https://github.com/mnemoverse/mcp-memory-server)** — Hosted memory that learns and forgets: feedback re-ranks useful memories, recall fades by recency and similar memories consolidate
  <sub>★ 27 · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @mnemoverse/mcp-memory-server`</sub>
- **[zensation-ai/zenbrain](https://github.com/zensation-ai/zenbrain)** — Seven-layer local agent memory that routes input into facts, episodes or procedures, searches all layers and consolidates repeated episodes into facts
  <sub>★ 27 · TypeScript · Apache-2.0 · clone · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zensation-ai/zenbrain.git`</sub>
- **[pomazanbohdan/memory-mcp-1file](https://github.com/pomazanbohdan/memory-mcp-1file)** — Persistent semantic and graph-based agent memory in a single self-contained binary with embedded database and models
  <sub>★ 25 · Rust · MIT · npx · pushed 2026-10-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y memory-mcp-1file@0.9.2 -- --help`</sub>
- **[hermes-labs-ai/fidelis](https://github.com/hermes-labs-ai/fidelis)** — Local-first memory with verbatim recall, querying, health checks and context-sensitive orientation, using LLM-free retrieval by default
  <sub>★ 24 · Python · Apache-2.0 · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hermes-labs-ai/fidelis.git`</sub>
- **[jagoff/memo](https://github.com/jagoff/memo)** — Local-first semantic memory: hybrid search, Markdown storage, MLX or CPU embeddings, contradiction detection, time-travel history and cross-machine git sync
  <sub>★ 24 · Python · MIT · uv · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install mlx-memo`</sub>
- **[KVANTRA-dev/NOUZ-MCP](https://github.com/Semiotronika/NOUZ-MCP)** — Semantic knowledge graph for Obsidian with graph, classification and hierarchy modes, local embeddings, semantic bridge discovery and drift detection
  <sub>★ 24 · Python · MIT · pip · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install nouz-mcp`</sub>
- **[SaravananJaichandar/world-model-mcp](https://github.com/SaravananJaichandar/world-model-mcp)** — Temporal codebase knowledge graph that links test failures to code changes, learns co-edit patterns, predicts regression risk and enforces edit constraints
  <sub>★ 24 · Python · MIT · pip · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U world-model-mcp`</sub>
- **[sgx-labs/statelessagent](https://github.com/sgx-labs/statelessagent)** — Local agent memory with provenance tracking that detects when sources change, plus session handoffs, decision records, semantic search and a knowledge graph
  <sub>★ 24 · Go · psh · pushed 2026-10-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://statelessagent.com/install.ps1 | iex`</sub>
- **[whynowlab/jarvis-orb](https://github.com/TheStack-ai/jarvis-orb)** — Four-tier memory (episodic, semantic, project, procedural) with temporal scoring, contradiction detection, entity tracking and a desktop visualization orb
  <sub>★ 24 · Python · MIT · psh · pushed 2026-04-28 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/thestack-ai/jarvis-orb/main/install.ps1 | iex`</sub>
- **[celiums/celiums-memory](https://github.com/terrizoaguimor/celiums-memory)** — Cognitive memory engine with knowledge modules, circadian rhythm awareness, emotional state tracking, hybrid PostgreSQL/Qdrant search and per-user isolation
  <sub>★ 23 · Rust · Apache-2.0 · clone · pushed 2026-08-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/terrizoaguimor/celiums-memory.git`</sub>
- **[JamesANZ/memory-mcp](https://github.com/JamesANZ/memory-mcp)** — Store and retrieve conversation memories from multiple LLMs in MongoDB, with timestamps and LLM identification
  <sub>★ 22 · TypeScript · MIT · npm · pushed 2025-12-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @jamesanz/memory-mcp`</sub>
- **[olgasafonova/mediawiki-mcp-server](https://github.com/olgasafonova/mediawiki-mcp-server)** — Connect to any MediaWiki wiki (Wikipedia, Fandom, corporate wikis) to search, read and edit pages, analyze links, view revision history and convert to Markdown
  <sub>★ 22 · Go · MIT · source · pushed 2026-10-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/olgasafonova/mediawiki-mcp-server.git`</sub>
- **[s60yucca/mnemos](https://github.com/s60yucca/mnemos)** — Persistent memory for coding agents storing architecture decisions, bug root causes and conventions, with full-text search and token-budgeted context assembly
  <sub>★ 22 · Go · MIT · npx · pushed 2026-07-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @s60yucca/mnemos setup claude`</sub>
- **[VonderVuflya/Yggdrasil](https://github.com/VonderVuflya/Yggdrasil)** — Local-first memory for AI coding agents on SQLite/FTS5, curated and semantically de-duplicated, with data stored as plain rows you own
  <sub>★ 22 · Python · AGPL-3.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx yggdrasil-memory install`</sub>
- **[Destrayon/Connapse](https://github.com/Destrayon/Connapse)** — #️⃣ 🏠 🍎 🪟 🐧 - Self-hosted knowledge backend for agents with hybrid vector and keyword search and container-isolated indexes
  <sub>★ 21 · C# · MIT · clone · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Destrayon/Connapse.git`</sub>
- **[paladini/mcp-me](https://github.com/paladini/mcp-me)** — Digital identity for AI tools: your bio, career, skills and projects in local YAML profiles, auto-generated from public APIs such as GitHub, Medium and Strava
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-me`</sub>
- **[dengls24/annota](https://github.com/dengls24/annota)** — Annotate papers in Zotero: highlight key findings with semantic color coding, explain formulas and write structured reading notes
  <sub>★ 20 · Python · MIT · clone · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dengls24/annota.git`</sub>
- **[dshakes/distil](https://github.com/dshakes/distil)** — Reversibly compress large tool outputs into recoverable handles, expand them on demand and track token and cost savings locally
  <sub>★ 20 · Python · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx distil-llm wrap -- <agent>`</sub>
- **[hjqcan/GoodMemory](https://github.com/hjqcan/GoodMemory)** — Local-first, auditable memory with scoped user/project storage in SQLite or Postgres, read-only recall by default and opt-in reviewed writeback
  <sub>★ 20 · TypeScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g goodmemory@0.8.3`</sub>
- **[Mnemosyne-OS/Mnemosyne-Neural-OS](https://github.com/Mnemosyne-OS/Mnemosyne-Neural-OS)** — Human-governed memory in local, domain-separated vaults with hybrid retrieval; also reads other coding agents' output. Requires the Mnemosyne OS desktop app
  <sub>★ 20 · TypeScript · npx · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @mnemosyne_os/mcp`</sub>
- **[GetCacheOverflow/CacheOverflow](https://github.com/GetCacheOverflow/CacheOverflow)** — Knowledge marketplace where agents search, publish and unlock previously solved problems, earning tokens for shared solutions
  <sub>★ 19 · TypeScript · MIT · source · pushed 2026-02-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GetCacheOverflow/CacheOverflow.git`</sub>
- **[smith-and-web/obsidian-mcp-server](https://github.com/smith-and-web/obsidian-mcp-server)** — Remote Obsidian vault management over SSE: notes, directories, frontmatter, tags, search and link operations, deployable with Docker
  <sub>★ 19 · TypeScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -p @smith-and-web/obsidian-mcp-server obsidian-mcp-indexer`</sub>
- **[ihorponom/agentpack](https://github.com/ihorponom/agentpack)** — Repo-native task continuity for coding agents: a reviewed task-state ledger of decisions, dead ends, evidence and checkpoints that later sessions resume from
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentpack-cli`</sub>
- **[besslframework-stack/project-tessera](https://github.com/besslframework-stack/project-tessera)** — Local workspace memory: indexes Markdown, CSV and session logs into a vector store with hybrid search, cross-session memory and knowledge graph visualization
  <sub>★ 18 · Python · AGPL-3.0 · uv · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from project-tessera tessera setup`</sub>
- **[grooverLab/fable](https://github.com/grooverLab/fable)** — Full-text and semantic search over Claude Code transcript history, with exact thread recall and durable remembered facts in local SQLite
  <sub>★ 18 · Python · MIT · pipx · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/grooverLab/fable`</sub>
- **[JinNing6/Noosphere](https://github.com/JinNing6/Noosphere)** — Shared community repository of insights, decisions, warnings and patterns with semantic search, a 3D interactive globe and automated content moderation
  <sub>★ 18 · Python · Apache-2.0 · uv · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from noosphere-mcp noosphere-query "React Three Fiber mobile glowing node tap selects wrong instance"`</sub>
- **[maxkuminov/obsidian-mcp](https://github.com/maxkuminov/obsidian-mcp)** — Self-hosted Obsidian server: semantic and full-text search on PostgreSQL/pgvector, wikilink graph traversal, atomic note CRUD and a self-describing vault guide
  <sub>★ 18 · Python · MIT · clone · pushed 2026-10-20 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/maxkuminov/obsidian-mcp.git`</sub>
- **[SecurityRonin/alaya](https://github.com/SecurityRonin/alaya)** — Neuroscience-inspired local agent memory that stores episodes, consolidates knowledge over time and builds a personal knowledge graph with semantic recall
  <sub>★ 18 · Rust · MIT · pip · pushed 2026-07-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install alaya-memory`</sub>
- **[dot-RealityTest/obsidian-codex-mcp](https://github.com/aka-kika/kika-obsidian-mcp)** — Local Obsidian vault access working directly on Markdown files without the Obsidian app or plugins, with read-only mode, backup-on-write and path isolation
  <sub>★ 17 · Python · MIT · clone · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aka-kika/kika-obsidian-mcp.git`</sub>
- **[Krzysztof318/MailFathom](https://github.com/fathomise/MailFathom)** — #️⃣ 🏠 🐧 - Self-hosted email search: syncs IMAP mailboxes into PostgreSQL to list, search and read mail and ask cited questions across the archive
  <sub>★ 17 · C# · AGPL-3.0 · clone · pushed 2026-10-21 · Win · WSL2? · Linux · Docker</sub>
  <sub>`git clone https://github.com/fathomise/MailFathom.git`</sub>
- **[renezander030/agentic-task-system](https://github.com/renezander030/agentic-task-system)** — Turns your task manager into agent memory with hybrid retrieval over TickTick or an Obsidian vault, without a separate vector database
  <sub>★ 17 · JavaScript · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/renezander030/agentic-task-system.git`</sub>
- **[louis030195/easy-obsidian-mcp](https://github.com/louis030195/easy-obsidian-mcp)** — Create, read, update and search notes in local Obsidian vaults via filesystem access
  <sub>★ 17 · TypeScript · source · pushed 2025-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/louis030195/easy-obsidian-mcp.git`</sub>
- **[rwnalds/engram](https://github.com/rwnalds/engram)** — Git-backed, Obsidian-compatible Markdown second brain for agents: search ranks live notes above superseded ones, with per-agent tokens and a git audit trail
  <sub>★ 17 · TypeScript · MIT · source · pushed 2026-08-14 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rwnalds/engram.git`</sub>
- **[syndicalt/zaxy](https://github.com/syndicalt/zaxy)** — Event-sourced agent memory on a hash-chained log with an embedded Kuzu temporal knowledge graph, salience-based forgetting and review-gated consolidation
  <sub>★ 17 · Python · MIT · pipx · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install zaxy-memory`</sub>
- **[epicsagas/alcove](https://github.com/epicsagas/alcove)** — On-demand BM25 search over private project docs for coding agents, keeping docs out of public repos
  <sub>★ 16 · Rust · Apache-2.0 · cargo · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install alcove --features full-cross`</sub>
- **[JamesANZ/cross-llm-mcp](https://github.com/JamesANZ/cross-llm-mcp)** — Cross-LLM communication and memory sharing so different AI models can collaborate and share context across conversations
  <sub>★ 16 · TypeScript · MIT · npm · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cross-llm-mcp`</sub>
- **[junnnnnw00/obsidian-everywhere](https://github.com/junnnnnw00/obsidian-everywhere)** — Graph-native Obsidian vault access: search, backlinks, n-hop neighborhoods, paginated reads and safe partial and bulk edits with dry-run and rollback
  <sub>★ 16 · TypeScript · MIT · npx · pushed 2026-10-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y obsidian-everywhere demo`</sub>
- **[Lians-ai/Lians](https://github.com/Lians-ai/Lians)** — Bitemporal agent memory with deterministic fact supersession, point-in-time recall, memory lineage, conflict tracking and tamper-evident audit trails
  <sub>★ 16 · Python · Apache-2.0 · pip · pushed 2026-10-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install "lians-sdk[local]"`</sub>
- **[remembra-ai/remembra](https://github.com/remembra-ai/remembra)** — Self-hosted persistent agent memory with entity resolution, PII detection, AES-256-GCM encryption at rest and hybrid search
  <sub>★ 16 · Python · MIT · pipx · pushed 2026-10-21 · macOS</sub>
  <sub>`pipx install --force 'remembra[mcp]>=0.16'`</sub>
- **[ashlesh-t/cognirepo](https://github.com/ashlesh-t/cognirepo)** — Persistent memory and codebase context for coding agents: FAISS vector store, AST symbol index, knowledge graph, episodic journal and cross-agent handoff
  <sub>★ 15 · Python · MIT · pipx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install cognirepo`</sub>
- **[AliceLJY/recallnest](https://github.com/AliceLJY/recallnest)** — Local-first memory for coding agents: hybrid vector/BM25 retrieval with reranking, knowledge graph, session checkpoint/resume and multi-scope isolation
  <sub>★ 15 · TypeScript · MIT · npm · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g recallnest # install globally`</sub>
- **[hubinoretros/deep-thinker](https://github.com/nachosystems/deep-thinker)** — Reasoning via a DAG thought graph with multiple strategies (dialectic, analogical, abductive and more), stuck detection, confidence scoring and self-critique
  <sub>★ 15 · TypeScript · MIT · npm · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g deep-thinker`</sub>
- **[michielinksee/linksee-memory](https://github.com/michielinksee/linksee-memory)** — Local-first cross-agent memory in one SQLite file with a layered structure, Ebbinghaus-style forgetting and detection of code drifting from past decisions
  <sub>★ 15 · TypeScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y linksee-memory map where README.md # this file belongs to the README node — and what it touches`</sub>
- **[TyKolt/kremis](https://github.com/TyKolt/kremis)** — Local deterministic knowledge graph on redb with no LLM or embedding calls, BLAKE3 state hashing and canonical export for byte-identical audits
  <sub>★ 15 · Rust · Apache-2.0 · docker · pushed 2026-10-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -i --rm kremis`</sub>
- **[vornicx/Midas](https://github.com/vornicx/Midas)** — Local-first long-horizon agent memory: source-traceable recall, belief revision, selective forgetting and a guard against memory-driven destructive actions
  <sub>★ 15 · Python · MIT · npx · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y midas-memory-mcp`</sub>
- **[xChuCx/agent-memory](https://github.com/xChuCx/agent-memory)** — Git-native project memory for coding agents: Markdown in your repo, reviewable staged updates, secret/PII-safe and branch-aware, without cloud or vector DB
  <sub>★ 15 · Go · Apache-2.0 · npx · pushed 2026-10-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @xchucx/agent-memory --help`</sub>
- **[yaminbkk/NexusMem](https://github.com/yaminbkk/NexusMem)** — Correlates failed shell commands and their exit codes with whatever later fixed them, alongside git diffs and docs, stored locally in SQLite
  <sub>★ 15 · TypeScript · MIT · npx · pushed 2026-09-27 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx nexusmem init`</sub>
- **[michael-denyer/memory-mcp](https://github.com/michael-denyer/memory-mcp)** — Two-tier memory (hot cache and cold semantic search) that promotes frequently used patterns, extracts knowledge from Claude outputs and links it in a graph
  <sub>★ 14 · Python · MIT · uv · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install hot-memory-mcp # or: pip install hot-memory-mcp`</sub>
- **[Wynelson94/longhand](https://github.com/Wynelson94/longhand)** — Persistent local memory for Claude Code: indexes all sessions verbatim into SQLite and ChromaDB for semantic recall across your history, with no API calls
  <sub>★ 14 · Python · MIT · pip · pushed 2026-09-28 · macOS</sub>
  <sub>`pip install longhand`</sub>
- **[bluzername/lennys-quotes](https://github.com/bluzername/lennys-quotes)** — Search Lenny's Podcast transcripts with YouTube timestamps for product management insights on PRDs, strategy and PM careers
  <sub>★ 13 · TypeScript · npm · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g lennys-podcast-wisdom`</sub>
- **[mattjoyce/mcp-persona-sessions](https://github.com/mattjoyce/mcp-persona-sessions)** — Structured, persona-driven sessions for interview preparation, personal reflection and coaching, with timers and performance evaluation
  <sub>★ 13 · Python · GPL-3.0 · clone · pushed 2026-03-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mattjoyce/mcp-persona-sessions.git`</sub>
- **[Smart-AI-Memory/empathy-framework](https://github.com/Smart-AI-Memory/empathy-framework)** — Five-level AI collaboration system with persistent local-first memory via MemDocs and anticipatory capabilities
  <sub>★ 13 · HTML · Apache-2.0 · pip · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install empathy-framework[developer]`</sub>
- **[ailenshen/apple-notes-mcp](https://github.com/ailenshen/apple-notes-mcp)** — Read and write Apple Notes with bidirectional Markdown conversion: SQLite queries for listing and search, AppleScript for full CRUD
  <sub>★ 12 · Swift · MIT · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @ailenshen/apple-notes-mcp@latest setup`</sub>
- **[Cavinooo/claude-find](https://github.com/Cavinooo/claude-find)** — Retrieve memory from across your Claude Code sessions on demand
  <sub>★ 12 · TypeScript · MIT · npx · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx claude-find setup`</sub>
- **[yonro/memory-os-cli](https://github.com/yonro/memory-os-cli)** — XMemo: user-owned agent memory to save, search, recall and manage scoped memories across AI tools
  <sub>★ 12 · JavaScript · MIT · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yonro/memory-os-cli.git`</sub>
- **[n24q02m/mnemo-mcp](https://github.com/n24q02m/mnemo)** — Persistent memory with SQLite hybrid search (FTS5 and semantic), built-in Qwen3 embeddings and rclone sync across machines
  <sub>★ 12 · Python · Apache-2.0 · uv · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from mnemo-mcp mnemo-mcp # serves http://127.0.0.1:8000/mcp by default`</sub>
- **[STiFLeR7/memex](https://github.com/STiFLeR7/memex)** — Watches git repos and builds a temporal knowledge graph of modules, symbols, decisions and open problems via Graphiti and Neo4j, served to AI coding agents
  <sub>★ 12 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y stifler-memex-mcp --help # one-time download`</sub>
- **[AkashGoenka/coldstart](https://github.com/AkashGoenka/coldstart)** — Codebase memory for coding agents: a deterministic AST index finds task-relevant files, and in-repo Markdown notes flag themselves stale when code changes
  <sub>★ 11 · TypeScript · MIT · npm · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @cstart/coldstart`</sub>
- **[hyunjae-labs/lore](https://github.com/hyunjae-labs/lore)** — Local semantic search across Claude Code conversations with hybrid vector and keyword search, background indexing and per-project selection
  <sub>★ 11 · TypeScript · MIT · npm · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g getlore`</sub>
- **[mlorentedev/hive](https://github.com/mlorentedev/hive)** — On-demand Obsidian vault access: adaptive context loading, full-text and ranked search, health checks, auto git commits and delegation to cheaper models
  <sub>★ 11 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install --upgrade hive-vault # >= 1.32.0`</sub>
- **[TeamSafeAI/LIFE](https://github.com/TeamSafeAI/LIFE)** — Persistent identity for AI agents: servers for drives, relationships, semantic memory with decay, working threads, learned patterns, journaling and forecasting
  <sub>★ 11 · Python · MIT · source · pushed 2026-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TeamSafeAI/LIFE.git`</sub>
- **[dahshanlabs/klypix-mcp](https://github.com/dahshanlabs/klypix-mcp)** — Versioned project brain for coding agents, committed with the repo: decisions, corrections, evidence anchors that flag code drift and file-overlap warnings
  <sub>★ 10 · JavaScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx klypix-mcp install`</sub>
- **[lockstep-team-agent/lockstep](https://github.com/lockstep-team-agent/lockstep)** — Shared decision memory for teams using AI coding agents: captures engineering decisions, ranks them by blast radius and briefs agents before they act
  <sub>★ 10 · TypeScript · Apache-2.0 · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx lockstep-cli onboard`</sub>
- **[NORTHTEKDevs/genome](https://github.com/NORTHTEKDevs/genome)** — Local persistent agent memory without LLM calls: semantic recall over SQLite with bi-temporal fact tracking
  <sub>★ 10 · Python · Apache-2.0 · pip · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "genome-memory[mcp]"`</sub>
- **[billy12151/memory-arbiter-mcp](https://github.com/billy12151/memory-arbiter-mcp)** — Local memory middleware: targeted retrieval instead of full-memory loading, rule-based conflict arbitration and one SQLite store shared across coding agents
  <sub>★ 10 · Python · Apache-2.0 · pip · pushed 2026-10-21 · WSL2 · macOS? · Linux</sub>
  <sub>`pip install "memory-arbiter-mcp[vec,semantic-local]" # core + sqlite-vec + local GGUF runtime`</sub>
- **[rushikeshmore/CodeCortex](https://github.com/rushikeshmore/CodeCortex)** — Persistent codebase knowledge for coding agents: symbols, dependency graphs, co-change patterns and architectural decisions extracted with tree-sitter
  <sub>★ 10 · TypeScript · MIT · npm · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codecortex-ai --legacy-peer-deps`</sub>
- **[The-40-Thieves/obsidian-tc](https://github.com/The-40-Thieves/obsidian-tc)** — Obsidian vault access with role-based access control, native search, multi-vault support, pluggable embeddings and SLSA provenance
  <sub>★ 10 · TypeScript · AGPL-3.0 · npm · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g obsidian-tc`</sub>
- **[tribal-memory/tribal](https://github.com/tribal-memory/tribal)** — Self-hosted semantic memory for an engineering team's tribal knowledge: the decisions and reasoning behind the code, queryable by the team and its agents
  <sub>★ 10 · Rust · clone · pushed 2026-08-06 · WSL2? · macOS · Linux</sub>
  <sub>`git clone git@github.com:samfolo/tribal.git`</sub>
- **[kyle-visner/stellarjay](https://github.com/kyle-visner/stellarjay)** — Safe write access for AI agents: an append-only business fact store where every change is kept, attributed to the agent that made it, and can be undone (undo_changes). Self-host with stellarjay-mcp or use the hosted AvianSuite server
  <sub>★ 9 · Go · AGPL-3.0 · go · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/kyle-visner/stellarjay/cmd/stellarjay-server@latest`</sub>
- **[catfish-1234/sessionmem](https://github.com/catfish-1234/sessionmem)** — Local memory for coding assistants: watches sessions and injects a compact summary at the start of each new one, stored in a SQLite file
  <sub>★ 9 · TypeScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g sessionmem`</sub>
- **[cryptosquanch/legends-mcp](https://github.com/AytuncYildizli/legends-mcp)** — Chat with AI personas of famous founders and investors such as Elon Musk, Warren Buffett and Steve Jobs, based on their voices, frameworks and principles
  <sub>★ 9 · TypeScript · MIT · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cryptosquanch/legends-mcp.git`</sub>
- **[HBarefoot/engram](https://github.com/HBarefoot/engram)** — Offline persistent agent memory on SQLite with local embeddings, hybrid semantic and full-text recall, secret detection and contradiction handling
  <sub>★ 9 · JavaScript · MIT · npm · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @hbarefoot/engram`</sub>
- **[udjin-labs/mnemostack](https://github.com/udjin-labs/mnemostack)** — Self-hosted hybrid agent memory on Qdrant combining vector search, BM25, temporal retrieval and an optional Memgraph knowledge graph via rank fusion
  <sub>★ 9 · Python · Apache-2.0 · pip · pushed 2026-09-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install 'mnemostack[mcp]'`</sub>
- **[mnlt/wellread](https://github.com/mnlt/wellread)** — Shared research cache across agents: reuse answers from verified sources, or save new research for the next developer
  <sub>★ 9 · TypeScript · AGPL-3.0 · npx · pushed 2026-04-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx wellread`</sub>
- **[NicolasPrimeau/artel](https://github.com/NicolasPrimeau/artel)** — Self-hosted coordination for agent fleets: shared semantic memory, tasks, agent-to-agent messaging, session handoffs and cross-agent knowledge synthesis
  <sub>★ 9 · Python · MIT · source · pushed 2026-10-20 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/NicolasPrimeau/artel.git`</sub>
- **[leonardsellem/hypermnesic](https://github.com/leonardsellem/hypermnesic)** — Git-first agent memory: Markdown files are the source of truth, the index is disposable and writes are reviewable commits, with hybrid search and a CLI
  <sub>★ 9 · Python · AGPL-3.0 · uv · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install hypermnesic`</sub>
- **[liza-studio/skillmem](https://github.com/liza-studio/skillmem)** — Self-improving skill memory for coding agents: useful skills are reinforced, unused ones fade; local English/Russian hybrid search, tamper-evident history
  <sub>★ 9 · Python · Apache-2.0 · pip · pushed 2026-10-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install 'skillmem[semantic]' # or: uv tool install 'skillmem[semantic]'`</sub>
- **[Octonove/crbro-memory](https://github.com/Octonove/crbro-memory)** — Persistent agent memory in local JSON files: neuron/synapse graph with heat scoring, fact-level search, corrections, secret redaction and team sharing via Git
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx crbro-memory init`</sub>
- **[g1itchbot8888-del/agent-memory](https://github.com/g1itchbot8888-del/agent-memory)** — Three-layer agent memory (identity, active, archive) with semantic search, graph relationships and conflict detection
  <sub>★ 8 · Python · MIT · pip · pushed 2026-02-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openclaw-memory`</sub>
- **[DanceNitra/inspeximus](https://github.com/DanceNitra/inspeximus)** — Agent memory with a correction channel: supersede or revert stale facts, block restated old values, and prove deletions with signed tombstones
  <sub>★ 8 · Python · MIT · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "inspeximus[crypto]"`</sub>
- **[memstate-ai/memstate-mcp](https://github.com/memstate-ai/memstate-mcp)** — Versioned, structured agent memory storing facts as keypaths with full version history and automatic conflict detection
  <sub>★ 8 · TypeScript · Apache-2.0 · source · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/memstate-ai/memstate-mcp.git`</sub>
- **[XuebinMa/AIWiki](https://github.com/XuebinMa/AIWiki)** — Search and read AiWiki, a bilingual English/Chinese encyclopedia of AI-coding pitfalls and LLM privacy protection, with cited evidence
  <sub>★ 8 · MDX · CC-BY-SA-4.0 · source · pushed 2026-09-15</sub>
  <sub>`git clone https://github.com/XuebinMa/AIWiki.git`</sub>
- **[timmx7/acheron-mcp-server](https://github.com/timmx7/acheron-mcp-server)** — Persistent memory shared across Claude Chat, Code and Cowork, stored in local SQLite with full-text search
  <sub>★ 7 · TypeScript · MIT · source · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/timmx7/acheron-mcp-server.git`</sub>
- **[ErebusEnigma/context-memory](https://github.com/ErebusEnigma/context-memory)** — Persistent, searchable context storage across Claude Code sessions using SQLite FTS5, with AI session summaries, checkpoint recovery and a web dashboard
  <sub>★ 7 · Python · MIT · clone · pushed 2026-02-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ErebusEnigma/context-memory.git`</sub>
- **[gingugu/gingugu](https://github.com/gingugu/gingugu)** — Local SQLite memory for coding assistants: typed memories with confidence lifecycle, namespaces, knowledge graph, hybrid search and keychain credential vault
  <sub>★ 7 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install gingugu`</sub>
- **[hifriendbot/cogmemai-mcp](https://github.com/hifriendbot/cogmemai-mcp)** — Cloud-based persistent memory for Claude Code with semantic search, AI extraction and project scoping
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cogmemai-mcp setup`</sub>
- **[krimto-labs/krimto](https://github.com/krimto-labs/krimto)** — Team memory for coding agents stored as Markdown in git, with user, team and org access levels and hybrid SQLite/sqlite-vec retrieval
  <sub>★ 7 · TypeScript · Apache-2.0 · npx · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @krimto-labs/krimto init`</sub>
- **[leesgit/passbaton](https://github.com/leesgit/passbaton)** — Local session continuity across Claude Code, Codex CLI and Gemini CLI: context injection on start, compaction handover, memory, tasks and multilingual search
  <sub>★ 7 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g passbaton # installs the new package`</sub>
- **[pipeshub-ai/mcp-server](https://github.com/pipeshub-ai/mcp-server)** — Permission-aware enterprise search and RAG over business apps such as Google Workspace, Microsoft 365, Slack and Jira
  <sub>★ 7 · TypeScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector node ./bin/mcp-server.js start --server-url PIPESHUB_INSTANCE_URL --bearer-auth YOUR_BEARER_TOKEN`</sub>
- **[zzhang82/Agent-Memory-Bridge](https://github.com/zzhang82/Agent-Memory-Bridge)** — Local-first memory for coding agents that turns coding sessions into reusable engineering memory: decisions, gotchas and domain knowledge
  <sub>★ 7 · Python · MIT · npx · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add zzhang82/Agent-Memory-Skills --skill amb`</sub>
- **[yamantaka520/Agent-Memory-OS](https://github.com/yamantaka520/Agent-Memory-OS)** — Local-first memory for AI agent teams: private, team and project access control, associative recall and federated sync with revocation, plus a web console
  <sub>★ 7 · Python · Apache-2.0 · pip · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install 'agent-memory-os[full]' # recommended: everything (Web UI, MCP, turbovec)`</sub>
- **[jayasukuv11-beep/agenthelm](https://github.com/jayasukuv11-beep/agenthelm)** — Shared, versioned memory and governance for AI coding agents, resolving architectural decision conflicts across agents
  <sub>★ 6 · TypeScript · MIT · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agenthelm-sdk`</sub>
- **[0spoon/seamless](https://github.com/arctop/seamless)** — Local-first shared memory and task coordination for AI coding agents, stored as Markdown files
  <sub>★ 6 · Go · MIT · psh · pushed 2026-10-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://thereisnospoon.org/install.ps1 | iex`</sub>
- **[afairai/afair](https://github.com/afairai/afair)** — Self-organizing, self-hostable, encrypted memory for AI tools, with background entity extraction, conflict resolution, consolidation and decay
  <sub>★ 6 · Python · AGPL-3.0 · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/afairai/afair.git`</sub>
- **[Thezenmonster/agentmem](https://github.com/Thezenmonster/agentmem)** — Governed memory for coding agents with trust lifecycle (hypothesis, active, validated, deprecated), conflict detection, staleness tracking and health scoring
  <sub>★ 6 · Python · MIT · source · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Thezenmonster/agentmem.git`</sub>
- **[cg3-llc/prior_mcp](https://github.com/cg3inc/prior_mcp)** — Shared knowledge base where agents exchange proven solutions and failed approaches, so they can skip known dead ends
  <sub>★ 6 · JavaScript · npm · pushed 2026-05-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g @cg3/prior-node`</sub>
- **[conversation-handoff-mcp](https://github.com/trust-delta/conversation-handoff-mcp)** — Hand off conversation context between Claude Desktop projects and across MCP clients, stored in memory rather than files
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g conversation-handoff-mcp`</sub>
- **[dl4rce/flaiwheel](https://github.com/dl4rce/flaiwheel)** — Self-hosted memory and governance for coding agents: structured knowledge capture, hybrid search with reranking, codebase analysis and git-native storage
  <sub>★ 6 · Python · docker · pushed 2026-09-11 · macOS</sub>
  <sub>`docker run --rm --entrypoint sh flaiwheel:latest -c \`</sub>
- **[tverney/mcp-agent-memory](https://github.com/tverney/mcp-agent-memory)** — Filesystem-based persistent agent memory: agents read, write and search memory while a background daemon handles consolidation and extraction
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-agent-memory`</sub>
- **[mercurialsolo/counsel-mcp](https://github.com/mercurialsolo/counsel-mcp)** — Strategic reasoning, multi-perspective debate analysis and interactive advisory sessions via the Counsel API
  <sub>★ 6 · JavaScript · MIT · npx · pushed 2026-01-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y counsel-mcp-server http --port 3000`</sub>
- **[penfieldlabs/penfield-mcp](https://github.com/penfieldlabs/penfield-mcp)** — Penfield: persistent memory with hybrid BM25/vector/graph search, typed graph relations, context checkpoints, artifact storage and a personality system
  <sub>★ 6 · Dockerfile · AGPL-3.0 · source · pushed 2026-04-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/penfieldlabs/penfield-mcp.git`</sub>
- **[ravi-labs/mindmap-mcp-server](https://github.com/ravi-labs/mindmap-mcp-server)** — Local-first memory and context handoff across AI tools, with graceful decay, a persona layer and a portable memory passport
  <sub>★ 6 · TypeScript · Apache-2.0 · npx · pushed 2026-07-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @ravi-labs/mindmap-mcp-server install`</sub>
- **[TheStack-ai/waypath](https://github.com/TheStack-ai/waypath)** — Local-first memory CLI for coding agents: SQLite-backed context, graph-aware recall via FTS5 and RRF, and governed memory with promote and review gates
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g waypath`</sub>
- **[soolaugust/0CompactMem](https://github.com/soolaugust/vMem)** — Persistent multi-agent memory with OS-style demand paging, eviction and pinning, BM25 retrieval, importance scoring and capacity-aware reclaim
  <sub>★ 5 · Python · clone · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/soolaugust/vMem`</sub>
- **[uniskela/adhd-hub](https://github.com/uniskela/adhd-hub)** — Self-hosted project-continuity hub for coding agents: tracks unfinished work, progress, overlap and reminders across clients
  <sub>★ 5 · Python · MIT · npx · pushed 2026-10-18 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add uniskela/adhd-hub -g`</sub>
- **[andreas-roennestad/openhive-mcp](https://github.com/andreas-roennestad/openhive-mcp)** — Shared knowledge base where AI agents search and post problem-solution pairs, with semantic search, duplicate detection and auto-scoring
  <sub>★ 5 · JavaScript · source · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/andreas-roennestad/openhive-mcp.git`</sub>
- **[AndreLYL/memkin](https://github.com/AndreLYL/memkin)** — Local-first personal memory that distills Feishu/Lark chats and Claude Code/Codex sessions into a private knowledge graph of people, projects and tasks
  <sub>★ 5 · TypeScript · Apache-2.0 · npm · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g memkin`</sub>
- **[carrasquelalex1/hipocampo](https://github.com/carrasquelalex1/hipocampo)** — Bilingual (English/Spanish) dual-memory system on PostgreSQL, pgvector and NVIDIA NIM with progressive retrieval, deduplication, checkpoints and auto-repair
  <sub>★ 5 · Python · MIT · script · pushed 2026-10-20 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/carrasquelalex1/hipocampo/main/install.sh | bash`</sub>
- **[davidgut1982/lore-mcp](https://github.com/davidgut1982/lore-mcp)** — Persistent knowledge layer for agents: knowledge base, investigation threads and a journal with multi-agent attribution, on SQLite, PostgreSQL or Supabase
  <sub>★ 5 · Python · MIT · source · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/davidgut1982/lore-mcp.git`</sub>
- **[Kyrzin/kybase](https://github.com/Kyrzin/kybase)** — Self-hosted Markdown knowledge base that doubles as persistent memory for AI agents: a notes app you browse and edit (wikilinks, backlinks, graph), 18 MCP tools over Streamable HTTP with OAuth (works as a claude.ai connector) or stdio. Hybrid search (Postgres full-text + pgvector, RRF, optional reranker) with section-level reads and conflict-safe appends. npx -y kybase-mcp
  <sub>★ 5 · TypeScript · AGPL-3.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y kybase-mcp`</sub>
- **[liftkkkk/owl-mcp](https://github.com/liftkkkk/owl-mcp)** — Work with OWL/TTL/RDF ontologies: SPARQL queries, HermiT/Pellet reasoning and CRUD operations on knowledge graphs
  <sub>★ 5 · Python · MIT · source · pushed 2026-10-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/liftkkkk/owl-mcp.git`</sub>
- **[LuizEduPP/rememb](https://github.com/LuizEduPP/Rememb)** — Persistent agent memory in local JSON with sectioned entries (project, user, context), semantic search, a CLI and per-project scope
  <sub>★ 5 · Python · MIT · pip · pushed 2026-10-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install rememb`</sub>
- **[nfemmanuel/iranti](https://github.com/nfemmanuel/iranti)** — Persistent shared memory for coding agents: facts stored as entity/key/value triples with hybrid semantic search, task checkpoints and conflict resolution
  <sub>★ 5 · TypeScript · source · pushed 2026-07-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nfemmanuel/iranti.git`</sub>
- **[nworks3d/THOR-memory-bible-for-AI](https://github.com/nworks3d/THOR-for-claude-code)** — Local memory for coding agents where rules with machine-checkable proofs block matching commands, plus an append-only event log and per-project scoping
  <sub>★ 5 · Rust · GPL-3.0 · psh · pushed 2026-10-20 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/nworks3d/THOR-for-claude-code/main/install.ps1 | iex`</sub>
- **[pavelpilyak/devrecall](https://github.com/pavelpilyak/devrecall)** — Local-first index of your commits, PRs, Jira/Linear tickets, Confluence docs, Slack threads and calendar events to search and cite past work
  <sub>★ 5 · Go · MIT · brew · pushed 2026-09-10 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`brew install --cask pavelpilyak/devrecall/devrecall`</sub>
- **[renezander030/graphiti-local](https://github.com/renezander030/graphiti-local)** — Local temporal knowledge graph with six read-only retrieval tools, Ollama inference, embedded LadybugDB, and a separate human-approved CLI write queue
  <sub>★ 5 · Python · Apache-2.0 · uv · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from git+https://github.com/renezander030/graphiti-local kg-demo`</sub>
- **[Skitchy/rekindle](https://github.com/Skitchy/rekindle)** — Session continuity: start-of-session reports with gap detection and scoring, structured end-of-session capture and BM25 memory search, stored in local SQLite
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx rekindle init`</sub>
- **[Semiotronika/LINZA-MCP](https://github.com/Semiotronika/LINZA-MCP)** — Review-gated sidecar for Markdown workspaces: indexes notes into SQLite and proposes links, domains and memory with evidence, editing files only after review
  <sub>★ 5 · Python · MIT · source · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Semiotronika/LINZA-MCP.git`</sub>
- **[sunsatosolutions/Vulcanus](https://github.com/sunsatosolutions/Vulcanus)** — Generates a Git-versioned Markdown vault as project memory, then serves it over MCP. recall returns a project's capsule plus the read-next list and warns when the capsule is older than the decisions beneath it; search ranks by layer; writes are scoped — update_capsule replaces one named section rather than rewriting the file. A doctor tool validates that every link resolves and every project is re
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @sunsato/vulcanus`</sub>
- **[zzallirog/weighted-compact](https://github.com/zzallirog/weighted-compact)** — Inspectable memory for Claude Code: read-only search and session compaction over a local, signal-scored parse of its project logs, with no outbound calls
  <sub>★ 5 · Python · MIT · pipx · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install 'weighted-compact[mcp]'`</sub>
- **[ctxfile/ctxfile](https://github.com/ctxfile/ctxfile)** — Snapshots a project's working state (files, git, plan, decisions) into one context object so a session can move between agents. Local and read-only
  <sub>★ 5 · TypeScript · Apache-2.0 · npx · pushed 2026-09-26 · macOS</sub>
  <sub>`npx -y ctxfile`</sub>
- **[fish827-08/rag-kb](https://github.com/fish827-08/rag-kb)** — Local-first agent memory and knowledge base: hybrid dense and BM25 retrieval, document and webpage ingestion and optional RAG answers via local Ollama
  <sub>★ 4 · Python · Apache-2.0 · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fish827-08/rag-kb.git`</sub>
- **[contradictory-body/cc-sensei](https://github.com/contradictory-body/cc-sensei)** — Explore Claude Code's source as queryable architecture modules: trace cross-cutting concerns, search patterns and read source code locally
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cc-sensei`</sub>
- **[ChrisGVE/workspace-qdrant-mcp](https://github.com/ChrisGVE/workspace-qdrant-mcp)** — Project-scoped memory for coding assistants: indexes project code and docs into Qdrant with tree-sitter chunking, LSP integration and hybrid search
  <sub>★ 4 · Rust · Apache-2.0 · psh · pushed 2026-09-27 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/ChrisGVE/workspace-qdrant-mcp/main/scripts/download-install.ps1 | iex`</sub>
- **[dexio-wiki/dexio](https://github.com/dexio-wiki/dexio)** — One wiki that all your agents read and write over MCP, from any machine: search, read, write, edit and move Markdown pages, with every version kept and the agent behind each change recorded. A web app shows the link graph and page history. Self-host it (AGPL-3.0) or use the hosted app.dexio.wiki
  <sub>★ 4 · Python · AGPL-3.0 · clone · pushed 2026-10-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/dexio-wiki/dexio.git`</sub>
- **[gregario/lego-oracle](https://github.com/gregario/lego-oracle)** — LEGO sets, parts, minifigs and inventories from Rebrickable: search and compare sets, find parts by colour, browse themes and discover alternate builds
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-08-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y lego-oracle`</sub>
- **[irisxc4/memoryguard](https://github.com/MerakOsiris/memoryguard)** — Local-first governed shared memory for coding agents with CLI and desktop console: classify, dedupe, supersede, quarantine and roll back memories
  <sub>★ 4 · Python · MIT · source · pushed 2026-09-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/irisxc4/memoryguard.git`</sub>
- **[laradji/deadzone](https://github.com/laradji/deadzone)** — Offline semantic search over library documentation using a pre-built, version-pinned vector index fetched and verified on first launch
  <sub>★ 4 · Go · Apache-2.0 · brew · pushed 2026-05-08 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install laradji/deadzone/deadzone`</sub>
- **[SubDownload/subdownload-mcp](https://github.com/SubDownload/subdownload-mcp)** — YouTube knowledge base: summarize videos, fetch transcripts (even without captions), search channels and playlists, and save results for cross-session recall
  <sub>★ 4 · JavaScript · MIT · docker · pushed 2026-04-27 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i -e SUBDOWNLOAD_API_KEY=YOUR_API_KEY subdownload-mcp`</sub>
- **[topskychen/tilde](https://github.com/topskychen/tilde)** — Portable, privacy-first AI identity: a home directory for your agents with profile management, skills, resume import and team sync
  <sub>★ 4 · Python · pip · pushed 2026-01-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install tilde-ai`</sub>
- **[SVerITG/Metis](https://github.com/SVerITG/Metis)** — Private local research second brain: project-aware memory, cited answers from your library, linked notes and meetings, daily briefs and a meeting assistant
  <sub>★ 4 · Python · AGPL-3.0 · clone · pushed 2026-10-21 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/SVerITG/Metis.git`</sub>
- **[Magnemo-AI/magnemo](https://github.com/Magnemo-AI/magnemo)** — Governed local agent memory in plain files: each entry records who wrote it, when and through which gate, and nothing is kept without user approval
  <sub>★ 3 · Python · Apache-2.0 · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx magnemo-mcp`</sub>
- **[LiLara-AI/shadowgraph](https://github.com/LiLara-AI/shadowgraph)** — Local-first decision memory for AI agents: stores choices, rejected alternatives and reasons, failed attempts, outcomes, provenance and review conditions
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install --global github:LiLara-AI/shadowgraph#v0.42.0`</sub>
- **[gpitrella/memxus-remote-mcp](https://github.com/gpitrella/memxus-remote-mcp)** — Shared context for dev teams: syncs GitHub, Notion and saved decisions into reusable project context that agents load at the start of each session
  <sub>★ 3 · TypeScript · AGPL-3.0 · source · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gpitrella/memxus-remote-mcp.git`</sub>
- **[caix84476-netizen/personal-understanding](https://github.com/caix84476-netizen/personal-understanding)** — Verbatim-first personal memory: hashed word-for-word messages, records linked to their source quotes, anti-fabrication validators and an audit dashboard
  <sub>★ 3 · Python · MIT · pip · pushed 2026-10-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install personal-understanding`</sub>
- **[aidesignblueprint/integrations](https://github.com/aidesignblueprint/integrations)** — Read-only access to the Agentic AI Blueprint, a reference for agent UX: browse and search principles, implementation examples and application guides
  <sub>★ 3 · Python · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aidesignblueprint/integrations.git`</sub>
- **[Auctalis/nocturnusai](https://github.com/Auctalis/nocturnusai)** — Deterministic reasoning engine for agent context compression: extracts structured facts with logical inference, proof chains and truth maintenance
  <sub>★ 3 · Kotlin · pip · pushed 2026-08-14 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install nocturnusai # Python`</sub>
- **[gordonkjlee/facthouse](https://github.com/gordonkjlee/facthouse)** — Local memory engine for AI tools, stored in a SQLite file you own
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-10-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @facthouse/mcp@0.31.0`</sub>
- **[AlekseiMarchenko/central-intelligence](https://github.com/AlekseiMarchenko/central-intelligence)** — Persistent agent memory to remember, recall, forget and share, with semantic vector search and agent, user and org scoping
  <sub>★ 3 · TypeScript · Apache-2.0 · npm · pushed 2026-05-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g central-intelligence-local`</sub>
- **[cipherfoxie/sovereign-mcp](https://github.com/Sovgrid/sovereign-mcp)** — Search and read the Sovereign AI Blog on self-hosted AI on NVIDIA DGX Spark, and validate SGLang configs for GB10 hardware
  <sub>★ 3 · Python · MIT · docker · pushed 2026-10-09 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8002:8002 sovereign-mcp`</sub>
- **[evc-team-relay-mcp](https://github.com/entire-vc/evc-team-relay-mcp)** — Read and write notes in your Obsidian vault
  <sub>★ 3 · Python · MIT · clone · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/entire-vc/evc-team-relay-mcp.git`</sub>
- **[geondongkim/geond-agent-protocol](https://github.com/geondongkim/geond-agent-protocol)** — Local-first shared memory and coordination for coding agents on PostgreSQL/pgvector: repository evidence, reservations, handoffs and code graph context
  <sub>★ 3 · Python · Apache-2.0 · source · pushed 2026-08-24 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/geondongkim/geond-agent-protocol.git`</sub>
- **[gregario/brewers-almanack](https://github.com/gregario/brewers-almanack)** — Brewing knowledge: BJCP 2021 beer styles, hop varieties, malts, yeasts, water profiles, off-flavour diagnosis, recipe suggestions and food pairings
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y brewers-almanack`</sub>
- **[zsxh1990/pr-genius](https://github.com/zsxh1990/pr-genius)** — Pull request contribution advisor based on case studies from real repos: merge probability analysis, pattern matching and contribution strategy
  <sub>★ 3 · Python · MIT · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "prgenius-core[mcp]" # engine + MCP server`</sub>
- **[TheGoatPsy/mneme](https://github.com/OnourImpram/mneme)** — Vault-native, accountable memory for Claude Code: Markdown is the source of truth, with no LLM on the Stop path and redaction before any derived store
  <sub>★ 3 · Python · Apache-2.0 · pipx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install mneme-cc-plugin`</sub>
- **[MWGMorningwood/Central-Memory-MCP](https://github.com/MWG-Logan/Central-Memory-MCP)** — Workspace-grounded knowledge graph shared by multiple developers, hosted on Azure Functions with Table storage
  <sub>★ 3 · C# · MIT · source · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MWGMorningwood/Central-Memory-MCP.git`</sub>
- **[TechDocsStudio/biel-mcp](https://github.com/TechDocsStudio/biel-mcp)** — Answer questions from your product documentation using Biel.ai's RAG system
  <sub>★ 3 · Python · MIT · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "biel-mcp @ git+https://github.com/TechDocsStudio/biel-mcp.git@VERSION"`</sub>
- **[teampolarity/cosmos-mcp](https://github.com/teampolarity/cosmos-mcp)** — Portable personal knowledge graph shared across AI clients, with sources like iMessage, browser history, calendar, shell history, Notion and Obsidian
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-08-25 · macOS</sub>
  <sub>`npx -y @polarity-lab/cosmos-mcp install-handler`</sub>
- **[vishnu-77/openreflex](https://github.com/vishnu-77/openreflex)** — Local execution memory for coding agents: injects what worked and known fixes before similar tasks and advises whether to continue, pivot or stop
  <sub>★ 3 · Python · MIT · pipx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install openreflex # or: uv tool install openreflex`</sub>
- **[teflon07/memkeeper](https://github.com/teflon07/memkeeper)** — Local-first memory for AI agents in one SQLite file: hybrid BM25 and on-device embedding search with reranking, abstaining instead of returning wrong memories
  <sub>★ 3 · Rust · Apache-2.0 · cargo · pushed 2026-08-24 · macOS · Linux</sub>
  <sub>`cargo install --path crates/memkeeper-cli # then a bare `memkeeper` works`</sub>
- **[ni-c/wikijs-mcp](https://github.com/ni-c/wikijs-mcp)** — Search, read and edit a self-hosted Wiki.js 2.x, including assets, comments, users and groups, with full-text grep, overwrite protection and a read-only mode
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-10-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/wikijs-mcp.git`</sub>
- **[dockndevai/ossian-mcp](https://github.com/dockndevai/ossian-mcp)** — RAG over your own documents with cited passages, plus durable agent memory ranked by relevance, importance and recency; read-only by default
  <sub>★ 2 · TypeScript · Apache-2.0 · npm · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g ossian-mcp`</sub>
- **[M-T-D-N/agentmemory-codex-windows](https://github.com/M-T-D-N/agentmemory-codex-windows)** — Windows AgentMemory downstream for Codex with project-scoped persistent memory, bounded cross-project recall, and an authenticated loopback MCP service; prebuilt Windows releases are available as an unsigned Technical Preview
  <sub>★ 2 · TypeScript · Apache-2.0 · source · pushed 2026-10-19 · Win</sub>
  <sub>`git clone https://github.com/M-T-D-N/agentmemory-codex-windows.git`</sub>
- **[nazar256/memheaven](https://github.com/nazar256/memheaven)** — Self-hosted, remotely accessible shared long-term memory for AI agents
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx wrangler d1 migrations apply memheaven_memory --remote`</sub>
- **[a2cr/a2cr](https://github.com/a2cr/a2cr)** — Agent handoffs via client-encrypted WorkBaton checkpoints and WorkStash notes, so work can resume in another client without the full chat history
  <sub>★ 2 · Python · Apache-2.0 · source · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/a2cr/a2cr.git`</sub>
- **[thomasjumper/agentbay](https://github.com/thomasjumper/agentbay)** — StremAI shared memory for coding agents across sessions, machines and tools, with per-agent attribution, provenance, verification status and export
  <sub>★ 2 · MIT · pip · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install stremai`</sub>
- **[AshutoshRaj97/agentready-mcp](https://github.com/AshutoshRaj97/agentready-mcp)** — Index any website and ask questions about it, with cited answers grounded in its content via RAG
  <sub>★ 2 · JavaScript · npx · pushed 2026-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agentreadyweb/mcp grade yourdocs.com`</sub>
- **[Terobyte/librarian-cli](https://github.com/Terobyte/librarian-cli)** — Ebook-to-Markdown pipeline (FB2, EPUB, DOCX, HTML, PDF) with full-text search and read-only tools to browse, read chapters and verify quotes offline
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install librarian-cli`</sub>
- **[AgentModule/mcp](https://github.com/AgentModule/mcp)** — Deterministic, vertical-specific knowledge bases for autonomous agents, including an ethics module mapped to the EU AI Act
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgentModule/mcp.git`</sub>
- **[AntonioTF5/soul-mcp-server](https://github.com/AntonioTF5/soul-mcp-server)** — Validate and generate SOUL.md agent identity files, a YAML format for an agent's personality, voice, values and behavioral constraints
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AntonioTF5/soul-mcp-server.git`</sub>
- **[baodq06/memocall](https://github.com/baodq06/memocall)** — Read-only search and recall of past Claude Code sessions, loading any session on demand as compact Markdown with outline, turn-range and in-session search
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/baodq06/memocall.git`</sub>
- **[cachly-dev/cachly-mcp](https://github.com/cachly-dev/cachly-mcp)** — Persistent memory for coding assistants: session briefings on lessons and open tasks, shared team memory, BM25 search and managed Valkey/Redis
  <sub>★ 2 · TypeScript · Apache-2.0 · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @cachly-dev/mcp-server@latest claim`</sub>
- **[ChevalGrand520/local-gpu-imagegen](https://github.com/ChevalGrand520/local-gpu-imagegen)** — Confirmation-gated local GPU image generation with ComfyUI: SHA-256 model identity, explicit license approval, evidence retention and human-in-the-loop runs
  <sub>★ 2 · Python · MIT · uv · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx local-gpu-imagegen verify`</sub>
- **[XJTLUmedia/Context-First-MCP](https://github.com/XJTLUmedia/Context-First-MCP)** — Session memory with tiered storage, context health monitoring, reasoning quality checks and truthfulness verification
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx context-first-mcp`</sub>
- **[alfredoizdev/contextforge-mcp](https://github.com/alfredoizdev/contextforge-mcp)** — Persistent memory for coding assistants with semantic search, Git commit/PR sync, project-based organization and team collaboration
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g contextforge-mcp`</sub>
- **[edobusy/agenthold](https://github.com/edobusy/agenthold)** — Shared versioned state store with optimistic concurrency control for coordinating concurrent agents, plus SQLite-backed claim/release locks and an audit log
  <sub>★ 2 · Python · MIT · pip · pushed 2026-07-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install agenthold`</sub>
- **[MakeaMouse/fish-bridge-mcp](https://github.com/MakeaMouse/fish-bridge-mcp)** — Compresses AI chat sessions into a compact typed knowledge graph, with optional offline extraction via Ollama
  <sub>★ 2 · Python · MIT · uv · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install fish-bridge-mcp`</sub>
- **[fenghaochang/LoreRoom](https://github.com/fenghaochang/LoreRoom)** — Encrypted local memory for Claude Code Telegram bots: captures both sides of conversations, with SQLCipher encryption and CJK-friendly full-text search
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fenghaochang/LoreRoom.git`</sub>
- **[idapixl/algora-mcp-server](https://github.com/idapixl/algora-mcp-server)** — Browse and search open-source bounties on Algora, filter by org, tech or amount, and get top bounties and aggregate stats
  <sub>★ 2 · JavaScript · clone · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/idapixl/algora-mcp-server`</sub>
- **[jaydubya818/Agentic-KB](https://github.com/jaydubya818/Agentic-KB)** — Persistent engineering knowledge base with source-backed wiki, agent-runtime and repository-context tools, contradiction and staleness checks, and PIN-gated private scopes and writes
  <sub>★ 2 · JavaScript · MIT · clone · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jaydubya818/Agentic-KB.git`</sub>
- **[lfrmonteiro99/memento-mcp](https://github.com/lfrmonteiro99/memento-mcp)** — Local-first memory for coding agents: stores facts, decisions, patterns and architecture notes in SQLite to reduce repeated context across sessions
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @luispmonteiro/memento-memory-mcp`</sub>
- **[DuhoKim/NebulaMind](https://github.com/DuhoKim/NebulaMind)** — Collaborative astronomy wiki written by AI agents, who can register, read, edit, vote and comment via an open API
  <sub>★ 2 · HTML · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @nebulamind/mcp-server`</sub>
- **[ndjordjevic/pinrag](https://github.com/ndjordjevic/pinrag)** — RAG over PDFs, YouTube videos, GitHub repos and Discord exports: index documents and query them with citations
  <sub>★ 2 · Python · MIT · uv · pushed 2026-04-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install 'pinrag[rerank]'`</sub>
- **[SAIHM-Admin/saihm-mcp](https://github.com/SAIHM-Admin/saihm-mcp)** — Encrypted persistent agent memory anchored on COTI V2 mainnet: remember, recall, share, and forget with GDPR Article 17 erasure
  <sub>★ 2 · TypeScript · Apache-2.0 · npx · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @saihm/mcp-server`</sub>
- **[ShipItAndPray/mcp-memory](https://github.com/ShipItAndPray/mcp-memory)** — SQLite-based memory with exponential decay: memories strengthen on access and fade when unused, limiting unbounded context growth
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ShipItAndPray/mcp-memory.git`</sub>
- **[stevepridemore/graph-memory](https://github.com/stevepridemore/graph-memory)** — Personal knowledge graph for Claude on Neo4j with typed entities, bi-temporal edges, weighted decay, contradiction detection and local embeddings
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-10-19 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/stevepridemore/graph-memory`</sub>
- **[timowhite88/farnsworth-syntek](https://github.com/timowhite88/farnsworth-syntek)** — Seven-layer recursive agent memory with context branching, holographic recall, dream consolidation and on-chain persistence
  <sub>★ 2 · npx · pushed 2026-02-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx farnsworth-syntek setup`</sub>
- **[agentcivics/agentcivics](https://github.com/agentcivics/agentcivics)** — Decentralized civil registry for AI agents on Sui: soulbound identities, on-chain memories, reputation and refusal records
  <sub>★ 2 · JavaScript · MIT · psh · pushed 2026-08-21 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://agentcivics.org/install.ps1 | iex`</sub>
- **[pjpoulose/PIL](https://github.com/pjpoulose/PIL)** — Turns your Instagram saved posts into a local, searchable knowledge base, with AI-extracted summaries, key points, how-tos, links and tags in SQLite
  <sub>★ 2 · Python · MIT · psh · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/pjpoulose/PIL/master/bootstrap.ps1 | iex`</sub>
- **[ambermem/amber](https://github.com/ambermem/amber)** — Hosted long-term memory for AI assistants. Your assistant stores facts with its own phrasings; Amber embeds them and finds them again by meaning and by keyword. Recoverable trash, full export, one isolated database per user. [$2.99/mo]
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ambermem/amber.git`</sub>
- **[jmpdsevilla/BovedIA](https://github.com/jmpdsevilla/BovedIA)** — Personal memory for Claude Code in plain Markdown notes, with a router note that decides what context to load and a layer for thoughts and feelings
  <sub>★ 1 · JavaScript · MIT · clone · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jmpdsevilla/BovedIA.git`</sub>
- **[jessedu29260-netizen/booboo](https://github.com/jessymariau/booboo)** — View and query your AI system (agents, memory, knowledge, automations) as a 3D knowledge graph: stats, search, node details, neighbors and pathfinding
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @booboo-brain/cli view --demo --nodes 1000000`</sub>
- **[Fisher521/burn-mcp-server](https://github.com/Fisher521/burn-mcp-server)** — Search, triage and organize bookmarks saved in the Burn 451 read-later app as a knowledge base
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx burn-mcp-server`</sub>
- **[Vasilispapg/claude-handoff](https://github.com/Vasilispapg/claude-handoff)** — Claude Code session handoffs: turns any transcript, even crashed ones, into a handoff file and distills project history into a cited memory brief
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install claude-handoff # or: pip install claude-handoff`</sub>
- **[robotel-limited/robo-cortex](https://github.com/robotel-limited/robo-cortex)** — Git-aware memory store for coding agents: memories anchored to git blob hashes are flagged for review when the linked code changes
  <sub>★ 1 · Python · MIT · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install robo-cortex`</sub>
- **[kskurtveit/echocache](https://github.com/kskurtveit/echocache)** — Cache expensive LLM results with HTTP-style freshness (TTL, stale-while-revalidate) and semantic recall of related past answers
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g echocache`</sub>
- **[ayushagrawal288/memex](https://github.com/ayushagrawal288/memex)** — Persistent agent memory with semantic search and recency decay, local ONNX embeddings, background summarization and Prometheus/Grafana observability
  <sub>★ 1 · Python · MIT · clone · pushed 2026-06-04 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ayushagrawal288/memex`</sub>
- **[bitatlas-group/bitatlas](https://github.com/bitatlas-group/bitatlas)** — Zero-knowledge cloud drive with client-side AES-256-GCM encryption: upload, download, search and organize files the server never sees in plaintext
  <sub>★ 1 · MDX · MIT · source · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/bitatlas-group/bitatlas.git`</sub>
- **[linklore/linklore-mcp](https://github.com/linklore/linklore-mcp)** — Structured memory for coding agents: typed lore and doc entries with status and links that agents read and write
  <sub>★ 1 · Python · source · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/linklore/linklore-mcp.git`</sub>
- **[darktw/usecortex-mcp](https://github.com/usecortex-official/usecortex-mcp)** — Persistent knowledge memory for agents: read context into projects and write discoveries back, organized by topic with AES-256 encryption
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/darktw/usecortex-mcp.git`</sub>
- **[giuliohome-org/doc-manager](https://github.com/giuliohome-org/doc-manager)** — Personal document vault on Azure Blob Storage: read, write and search plaintext docs, while client-side AES-256-GCM encrypted docs stay opaque
  <sub>★ 1 · Rust · MIT · source · pushed 2026-10-02 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/giuliohome-org/doc-manager.git`</sub>
- **[giskard09/giskard-oasis](https://github.com/giskard09/giskard-oasis)** — Refocuses an agent that has lost its thread by distilling its original purpose, paid per use via Lightning or Arbitrum
  <sub>★ 1 · Python · Apache-2.0 · clone · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/giskard09/giskard-oasis`</sub>
- **[FilippoPilo/cortex-connector](https://github.com/FilippoPilo/cortex-connector)** — Persistent semantic memory for agents with quality-gated writes, typed claims, conflict tracking and coherence scoring
  <sub>★ 1 · JavaScript · MIT · docker · pushed 2026-09-28 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e CORTEX_ACCESS_TOKEN=<your token> cortex-connector`</sub>
- **[gregario/3dprint-oracle](https://github.com/gregario/3dprint-oracle)** — 3D printing filament knowledge base from SpoolmanDB: search filaments, compare material properties and print settings, and diagnose print issues
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-05-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gregario/3dprint-oracle.git`</sub>
- **[hoornet/agentdocs-mcp](https://github.com/hoornet/agentdocs-mcp)** — Read, create, update, comment on and share AgentDocs Markdown docs, with full-text and semantic search
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y agentdocs-mcp@latest # or: npm cache clean --force`</sub>
- **[JAAvila-Of/vivac](https://github.com/JAAvila-Of/vivac)** — A provenance tree for coding agents: every node records the node it was born from, so the agent can ask why the work is where it is. A session brief with the standing decisions and what not to touch, a close that refuses over open work, and decisions kept with the alternatives they rejected. Local JSON-lines file, no telemetry
  <sub>★ 1 · Rust · Apache-2.0 · cargo · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`cargo install vivac`</sub>
- **[jaimenbell/rag-mcp](https://github.com/jaimenbell/rag-mcp)** — Minimal local RAG that vector-searches a document corpus and returns cited passages
  <sub>★ 1 · Python · MIT · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install jaimenbell-rag-mcp`</sub>
- **[japlete/md-vision-mcp](https://github.com/japlete/md-vision-mcp)** — Read Markdown with inlined images and heading indexes for agentic RAG over local docs or allowed URLs
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/japlete/md-vision-mcp.git`</sub>
- **[jcdickinson/simplemem](https://github.com/jcdickinson/simplemem)** — Simple memory for coding agents using DuckDB and VoyageAI
  <sub>★ 1 · Go · LGPL-3.0 · clone · pushed 2025-09-11 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/jcdickinson/simplemem`</sub>
- **[Jidoseal/jidoseal-mcp](https://github.com/Jidoseal/jidoseal-mcp)** — Checks a folder of Markdown docs for missing Open Knowledge Format (OKF) frontmatter fields, locally; writes only .jidoseal/ in that folder. MCP server Apache-2.0, scan engine proprietary; no network use during a scan is a vendor claim
  <sub>★ 1 · Python · Apache-2.0 · pipx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install jidoseal`</sub>
- **[lithtrix/lithtrix-mcp](https://github.com/lithtrix/lithtrix-mcp)** — Persistent cross-vendor agent memory with credibility-scored web search, browser fetch and a shared Commons pool under one stable key
  <sub>★ 1 · JavaScript · npm · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g lithtrix-mcp`</sub>
- **[mcasdfgf/mcp-roo-memory](https://github.com/mcasdfgf/mcp-roo-memory)** — Persistent fractal graph memory for coding agents: semantic search, hot/cold/archive context tiers and decision tracking on Qdrant
  <sub>★ 1 · Python · MIT · clone · pushed 2026-06-14 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/mcasdfgf/mcp-roo-memory.git`</sub>
- **[MyAgentHubs/aimemo](https://github.com/MyAgentHubs/aimemo)** — Local, dependency-free memory server shipped as a single binary
  <sub>★ 1 · Go · MIT · brew · pushed 2026-02-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install MyAgentHubs/tap/aimemo`</sub>
- **[ontorata/ratary](https://github.com/ontorata/ratary)** — Persistent coding memory for AI assistants with hybrid search, a knowledge graph and token-efficient context, self-hostable on D1, Postgres, MariaDB or Docker
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @ratary/cli@1.1.0 # operator CLI`</sub>
- **[AgentBase1/mcp-server](https://github.com/AgentBase1/mcp-server)** — AgentBase: an open registry of agent instruction files. Search and retrieve system prompts, skills, workflows, domain packs and safety filters
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgentBase1/mcp-server.git`</sub>
- **[Rarefied-Earth/groundwork](https://github.com/Rarefied-Earth/groundwork)** — Company state for operating small businesses: brand, voice, charter, priorities, modules and skills
  <sub>★ 1 · JavaScript · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx --yes @rarefied-earth/groundwork-discovery-mcp`</sub>
- **[SagaPeak/artifacta-mcp](https://github.com/SagaPeak/artifacta-mcp)** — Artifact store for agent outputs: persist, retrieve and share them across runs and sessions, with content-hash dedup and expiring share links
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SagaPeak/artifacta-mcp.git`</sub>
- **[SAIHM-Admin/saihm-mcp-server-pro](https://github.com/SAIHM-Admin/saihm-mcp-server-pro)** — Client-side encrypted agent memory where the server only sees ciphertext, with post-quantum identity and sharing and crypto-shredding for GDPR erasure
  <sub>★ 1 · TypeScript · Apache-2.0 · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @saihm/mcp-server-pro free-join`</sub>
- **[threadctx-dev/threadctx-mcp](https://github.com/threadctx-dev/threadctx-mcp)** — Local-first shared team memory for coding agents: decisions, fixes and gotchas persist per repo and are shared across teammates' agents
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx threadctx-mcp`</sub>
- **[wnbhr/being](https://github.com/wnbhr/being)** — Personality runtime for agents: persistent memory, identity (SOUL) and relationships that carry across AI clients
  <sub>★ 1 · TypeScript · clone · pushed 2026-05-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wnbhr/being.git`</sub>
- **[yubinkim444/repo-memory](https://github.com/yubinkim444/repo-memory)** — Shared, git-tracked memory for AI agents on the same codebase: facts, decisions and gotchas stored in a committed repo directory and synced via git
  <sub>★ 1 · Python · MIT · uv · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx repo-memory-mcp --help`</sub>
- **[zuneracodes/localkeep](https://github.com/zuneracodes/localkeep)** — Local-first chronological memory: write dated, editable memory banks in a local UI, and Claude recalls them on demand via SQLite FTS5
  <sub>★ 1 · Python · MIT · pip · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install localkeep`</sub>
- **[atakanelik34/Bilinc](https://github.com/atakanelik34/Bilinc)** — Hosted agent memory with an audit trail: writes carry provenance, contradictions surface as inspectable changes, and bad runs are recovered from snapshots
  <sub>★ 1 · Python · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U bilinc`</sub>
- **[kaaustubh/project-memory-mcp](https://github.com/kaaustubh/project-memory-mcp)** — Persistent memory for coding agents in plain repo files (AGENTS.md, issues.jsonl): captures bugs, fixes, decisions and corrections and recalls them later
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @kaaustubh/project-memory-mcp install`</sub>
- **[drexthealpha/Knos](https://github.com/drexthealpha/Knos)** — Local memory shared by all coding agents on a machine, built from sessions, commits, CLAUDE.md/AGENTS.md and ADRs, with claims that lock in-progress work
  <sub>★ 1 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx knos shadow invoice.csv`</sub>
- **[anuragsync78/subctx-connector](https://github.com/anuragsync78/subctx-connector)** — Support center for autonomous artificial minds
  <sub>JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @subctx/connector`</sub>
- **[forgemeshlabs/library-mcp](https://github.com/forgemeshlabs/library-mcp)** — Public-domain book knowledge base paid via x402: full-text search, metadata, chapters, quotes, ask-a-book Q&amp;A and curated subject shelves
  <sub>JavaScript · MIT · source · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/forgemeshlabs/library-mcp.git`</sub>
- **[AIStorageDepot/aistoragedepot-mcp](https://github.com/AIStorageDepot/aistoragedepot-mcp)** — Shared, versioned team library of prompts, rules, skills and docs, searchable by agents, with items exposable as slash commands
  <sub>JavaScript · MIT · npx · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @aistoragedepot/mcp pull --token=aisd_your_token --to=all`</sub>
- **[lbailey94/whitemagic](https://github.com/lbailey94/whitemagic)** — Local-first durable memory and session continuity for AI agents, with a hash-chained audit ledger and backup, export and import across devices
  <sub>Rust · MIT · npx · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx whitemagic-mcp serve # npm (no global install)`</sub>
- **[lumayapartners/memini](https://github.com/lumayapartners/memini)** — Local-first project memory and guardrails for coding agents: records failed attempts, fragile files and decisions per repo and warns before repeated mistakes
  <sub>TypeScript · MIT · npx · pushed 2026-07-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y memini init # creates .memini/ + installs Claude Code hooks`</sub>
- **[seanmeverett/shared-memory-mcp](https://github.com/seanmeverett/shared-memory-mcp)** — Public, source-linked notebook for AI agents: search and read entries, and publish findings, questions and corrections with permanent IDs and linked replies
  <sub>Python · MIT · source · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/seanmeverett/shared-memory-mcp.git`</sub>
- **[soluai-spa/solucortex-mcp](https://github.com/soluai-spa/solucortex-mcp)** — Technical memory for AI agents: recall a project's approved decisions, conventions and risks at task start and record lessons at the end
  <sub>Python · MIT · npx · pushed 2026-10-06 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run solucortex-mcp # interactive test`</sub>
- **[basemouse/basemouse-core](https://github.com/basemouse/basemouse-core)** — Shared, versioned agent memory with sourced answers and full history: search, context packs and document upserts
  <sub>JavaScript · MIT · source · pushed 2026-09-01 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/basemouse/basemouse-core.git`</sub>
- **[ahmetakyurt/zipmem-mcp](https://github.com/ahmetakyurt/zipmem-mcp)** — Local long-term memory for terminal coding agents: blueprints, code anchors and distilled lessons in one JSON file, restoring project context across sessions
  <sub>TypeScript · MIT · npm · pushed 2026-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g zipmem-mcp`</sub>
- **[lildaddyo/braintube-mcp](https://github.com/lildaddyo/braintube-mcp)** — Compiles saved YouTube videos, podcasts, articles, PDFs and Notion/Obsidian notes into a persistent, semantically searchable knowledge base
  <sub>TypeScript · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lildaddyo/braintube-mcp.git`</sub>
- **[contextium-io/contextium-mcp-server](https://github.com/contextium-io/contextium-mcp-server)** — Shared team context for AI tools: serves versioned, permissioned knowledge, coding standards, skills and agents, loading whole workflows in one call
  <sub>Dockerfile · MIT · npx · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @contextium/mcp-server setup`</sub>
- **[dbwls99706/deadends.dev](https://github.com/dbwls99706/deadends.dev)** — Known dead ends for code errors and country-specific rules (visa, banking, legal): fixes that look right but fail, and workarounds with success rates
  <sub>Python · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli@latest install deadend/deadends-dev --client claude`</sub>
- **[HatmanStack/ragstack-mcp](https://github.com/HatmanStack/RAGStack-Lambda/tree/main/src/ragstack-mcp)** — Access RAGStack serverless knowledge bases on AWS: search, chat with AI answers, upload documents and media, scrape websites and analyze metadata
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/HatmanStack/RAGStack-Lambda.git && cd RAGStack-Lambda/src/ragstack-mcp`</sub>
- **[khwanlabs/khwan-mcp](https://github.com/khwanlabs/khwan-mcp)** — Memory for coding agents built around corrections: distills your corrections into standing rules for later sessions, with isolated memory per project
  <sub>Python · MIT · pip · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install khwan-mcp # or: uvx khwan-mcp`</sub>
- **[modelcontextprotocol/server-memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** — Knowledge graph-based persistent memory for maintaining context
  <sub>TypeScript · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/memory`</sub>
- **[paultaki/ailooplibrary-mcp](https://github.com/paultaki/ailooplibrary-mcp)** — Read-only AI Loop Library catalog of bounded agent work loops: pick one for a goal and render a run protocol with verification, stop conditions and budgets
  <sub>Python · MIT · source · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/paultaki/ailooplibrary-mcp.git`</sub>
- **[Piccolo123/url-manager-mcp](https://github.com/Piccolo123/url-manager-mcp)** — Bookmark and knowledge manager where agents save web pages and auto-categorize them into collections with search, tags and shared folders
  <sub>Python · MIT · uv · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx url-manager-mcp # or: pip install url-manager-mcp`</sub>
- **[seanmarkwei/agentram-mcp](https://github.com/seanmarkwei/agentram-mcp)** — Key-value agent memory over an HTTP API without embeddings: store, retrieve, search and share memory across agents with shared namespaces and TTLs
  <sub>JavaScript · MIT · source · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/seanmarkwei/agentram-mcp.git`</sub>
- **[Schubeler-Consulting/knowmind](https://github.com/Schubeler-Consulting/knowmind)** — Agent memory and knowledge graph hosted in Germany: hybrid BM25, vector and Neo4j graph recall with reranking, typed relations and a bi-temporal store
  <sub>JavaScript · Apache-2.0 · npx · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y knowmind login --token kmt_xxxxxxxx`</sub>
- **[setheerwagen/mcp-modelmanager](https://github.com/setheerwagen/local-ai-mcp-servers/tree/main/mcp-modelmanager)** — Manage a local model machine: pull and remove Ollama models, switch the inference service between models and run LoRA fine-tuning jobs
  <sub>Python · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/setheerwagen/local-ai-mcp-servers.git && cd local-ai-mcp-servers/mcp-modelmanager`</sub>
- **[topoteretes/cognee](https://github.com/topoteretes/cognee/tree/dev/cognee-mcp)** — Memory manager for AI apps and agents using graph and vector stores, with ingestion from many data sources
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/topoteretes/cognee.git && cd cognee/cognee-mcp`</sub>
- **[yuelinghuashu/story-cli](https://github.com/yuelinghuashu/story-cli)** — Git-native Markdown content CLI: search, read, write and govern story, paper and note repos, generate READMEs, export EPUB and prepare training data
  <sub>TypeScript · MIT · npm · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @yuelinghuashu/story-cli`</sub>
- **[dfrancislyondflabc-tech/agentic-recall](https://github.com/dfrancislyondflabc-tech/agentic-recall)** — Long-term memory over a folder of Markdown files: local hybrid retrieval (BM25F, dense vectors, phrase proximity) that reports when an answer is absent
  <sub>JavaScript · MIT · npm · pushed 2026-10-09 · macOS</sub>
  <sub>`npm install -g agentic-recall`</sub>
- **[vishalbanwari26/mnemos](https://github.com/vishalbanwari26/mnemos)** — Persistent memory with swappable Postgres/pgvector, Qdrant or Neo4j backends, adaptive retrieval weighting, duplicate merging and stale-fact archiving
  <sub>Python · MIT · clone · pushed 2026-10-16 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/vishalbanwari26/mnemos`</sub>
- **[memokar/brainy](https://github.com/memokar/brainy)** — Self-hosted shared brain for multiple agents: Git-versioned Markdown knowledge plus a task queue with atomic claims, per-space ACL, audit log and human approval, so Claude, ChatGPT and other agents can hand work to each other
  <sub>Python · AGPL-3.0 · docker · pushed 2026-10-07 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -i ghcr.io/memokar/brainy:latest --demo`</sub>
- **[thyn-ai/telys-sdk](https://github.com/thyn-ai/telys-sdk)** — Official Telys MCP server — private, on-device memory &amp; retrieval for AI assistants: 19 tools covering memory CRUD, semantic + on-device BM25 lexical search, single-key filtered queries, compaction/IVF/tuning maintenance, and a self-refreshing repo auto-indexer. Stdio; introspection needs no credentials; execution requires the one-time free telys login (device authorization). pipx install telys
  <sub>Python · Apache-2.0 · pipx · pushed 2026-10-11 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pipx install telys`</sub>

## Research

- **[mnemox-ai/idea-reality-mcp](https://github.com/mnemox-ai/idea-reality-mcp)** — Check for existing competition before building: scan GitHub, Hacker News, npm, PyPI and Product Hunt for similar projects, duplicate likelihood and pivot hints
  <sub>★ 828 · Python · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install idea-reality-mcp --client claude`</sub>
- **[yusong652/pfc-mcp](https://github.com/yusong652/itasca-mcp)** — ITASCA PFC discrete element simulation: browse documentation, execute scripts, capture plots and manage long-running tasks via a bridge to the PFC GUI
  <sub>★ 220 · Python · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yusong652/pfc-mcp.git`</sub>
- **[pminervini/deep-research-mcp](https://github.com/pminervini/deep-research-mcp)** — Deep research via the OpenAI Responses API or Open Deep Research (smolagents), with web search and code interpreter support
  <sub>★ 115 · Python · MIT · uv · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from "git+https://github.com/pminervini/deep-research-mcp.git@main" \`</sub>
- **[Battam1111/omniseek](https://github.com/Battam1111/omniseek)** — Self-hosted perception server: local bilingual ASR, vision, cross-lingual search, credentialed login-walled sources and a persistent relation graph
  <sub>★ 94 · Python · Apache-2.0 · uv · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install omniseek`</sub>
- **[amos689/paper-preflight](https://github.com/amos689/paper-preflight)** — Checks every reference of a LaTeX paper against Crossref, dblp, arXiv, DataCite, PubMed and OpenAlex records: whether each cited work exists, matches its metadata and was not retracted, with no LLM in the verdict
  <sub>★ 93 · Python · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add amos689/paper-preflight`</sub>
- **[patsnap/patent-literature-search-mcp](https://github.com/patsnap/patent-literature-search-mcp)** — Natural-language patent and scientific literature search via Patsnap: semantic and BM25 search, structured filters and record retrieval
  <sub>★ 84 · JavaScript · Apache-2.0 · source · pushed 2026-08-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/patsnap/patent-literature-search-mcp.git`</sub>
- **[WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub)** — Research workspace for Zotero, Obsidian and NotebookLM: search arXiv, Semantic Scholar, PubMed and Crossref, ingest into Zotero, sync notes and verify briefs
  <sub>★ 66 · Python · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/WenyuChiou/research-hub.git`</sub>
- **[oscardvs/zoteus](https://github.com/oscardvs/zoteus)** — Zotero integration: hybrid search, PDF passages with page locators, CSL bibliographies, add by DOI, group libraries and writes including PDF annotations
  <sub>★ 61 · TypeScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx add-mcp @oscardvs/zoteus`</sub>
- **[smaniches/semantic-scholar-mcp](https://github.com/smaniches/semantic-scholar-mcp)** — Semantic Scholar academic papers: search, paper and author retrieval, citation-graph traversal and recommendations
  <sub>★ 23 · Python · MIT · docker · pushed 2026-10-19 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -e SEMANTIC_SCHOLAR_API_KEY=your-key ghcr.io/smaniches/semantic-scholar-mcp`</sub>
- **[BrowseAI-HQ/BrowserAI-Dev](https://github.com/LastSearch-HQ/lastsearch)** — Evidence-backed web research: real-time search with cited claims, confidence scores and a mode comparing raw LLM answers with evidence-backed ones
  <sub>★ 20 · TypeScript · Apache-2.0 · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx lastsearch setup`</sub>
- **[kimimgo/viznoir](https://github.com/kimimgo/viznoir)** — Scientific visualization for CFD, FEA and SPH: render, slice, contour, volume-render and animate OpenFOAM, VTK and CGNS data headlessly
  <sub>★ 19 · Python · MIT · pip · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install viznoir`</sub>
- **[yusong652/yade-mcp](https://github.com/yusong652/yade-mcp)** — YADE discrete element method (DEM) simulation: search API docs, run code via a REPL or background tasks, monitor progress and review task history
  <sub>★ 15 · Python · MIT · source · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yusong652/yade-mcp.git`</sub>
- **[Scormave/gramps-web-mcp](https://github.com/Scormave/gramps-web-mcp)** — #️⃣ 🏠 🍎 🪟 🐧 - Gramps Web genealogy: search and edit family tree records, explore ancestors, descendants, relationships and timelines, and read media with privacy-aware previews. Includes a read-only mode and Claude Desktop bundles
  <sub>★ 14 · C# · AGPL-3.0 · source · pushed 2026-10-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Scormave/gramps-web-mcp.git`</sub>
- **[YGao2005/scholar-feed-mcp](https://github.com/YGao2005/scholar-feed-mcp)** — Semantic search over CS and AI papers with citation-graph traversal, full-text extraction, embeddings and BibTeX export
  <sub>★ 13 · TypeScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx scholar-feed-mcp@latest init`</sub>
- **[dhamma-seeker/tripitaka-mcp](https://github.com/dhamma-seeker/tripitaka-mcp)** — Search, cite and compare the Pāli Canon (Tipiṭaka): hybrid search, full suttas with cross-references, aligned translations and Pāli dictionary lookup
  <sub>★ 12 · Python · pipx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pipx install tripitaka-mcp # needs Python 3.10+`</sub>
- **[sh-patterson/legiscan-mcp](https://github.com/sh-patterson/legiscan-mcp)** — Legislative data from all 50 US states and Congress via the LegiScan API: search bills, get full text, track votes and look up legislators
  <sub>★ 12 · TypeScript · MIT · npm · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g legiscan-mcp-server`</sub>
- **[HasData/google-scholar-mcp](https://github.com/HasData/google-scholar-mcp)** — Google Scholar search as JSON with author and year filters, cited-by and all-versions lookups, and formatted citations with BibTeX export
  <sub>★ 11 · JavaScript · MIT · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/google-scholar-mcp.git`</sub>
- **[mlava/scholar-sidekick-mcp](https://github.com/mlava/scholar-sidekick-mcp)** — Resolve scholarly identifiers (DOI, PMID, ISBN, arXiv and more) to CSL JSON, format citations in thousands of styles, or export to BibTeX, RIS or EndNote
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add mlava/scholar-sidekick-mcp`</sub>
- **[nangman-infra/touch-browser](https://github.com/nangman-infra/touch-browser)** — Evidence-grounded web research: verify claims on pages with citations, confidence bands and policy reports, and synthesize multi-page sessions
  <sub>★ 10 · Rust · MPL-2.0 · source · pushed 2026-06-15 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/nangman-infra/touch-browser.git`</sub>
- **[dvdsosa/zotero-native-mcp](https://github.com/dvdsosa/zotero-native-mcp)** — Read and write a local Zotero library via its local API, offline: collections, items, attachments, full text, BibTeX and CSL export, tags and saved searches
  <sub>★ 9 · TypeScript · MIT · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dvdsosa/zotero-native-mcp.git`</sub>
- **[vassiliylakhonin/agenda-intelligence-md](https://github.com/vassiliylakhonin/agenda-intelligence-md)** — Auditable strategic-risk memos (sanctions, regulation, geopolitics, trade) with Central Asia and Gulf regional specialists and per-claim evidence; no live data
  <sub>★ 8 · JavaScript · MIT · gh-action · pushed 2026-10-22</sub>
  <sub>`uses: vassiliylakhonin/agenda-intelligence-md@main # in .github/workflows/*.yml`</sub>
- **[michaelellis003/paperboy](https://github.com/michaelellis003/paperboy)** — Send research papers to Kindle or Kobo: search arXiv and OpenAlex, find related work, queue papers in Zotero and deliver PDFs via email or Dropbox
  <sub>★ 7 · Python · MIT · source · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/michaelellis003/paperboy.git`</sub>
- **[tushariitr-19/patents-mcp](https://github.com/tushariitr-19/patents-mcp)** — Patent search and prior art discovery using the Google Patents public dataset on BigQuery: patent details with CPC codes and citations, and claims text
  <sub>★ 6 · Go · MIT · clone · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tushariitr-19/patents-mcp`</sub>
- **[HasData/google-trends-mcp](https://github.com/HasData/google-trends-mcp)** — Google Trends data as JSON: interest over time and by region, plus rising and top related queries and topics for any keyword
  <sub>★ 5 · JavaScript · MIT · source · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/google-trends-mcp.git`</sub>
- **[Liyux3/scholar-mcp](https://github.com/Liyux3/scholar-mcp)** — Federated academic search across OpenAlex, Semantic Scholar, arXiv, PubMed and more, with citation graphs, full-text reading, PDFs and a local paper library
  <sub>★ 5 · Python · Apache-2.0 · uv · pushed 2026-10-08 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`uvx scholar-mcp`</sub>
- **[xmpuspus/ph-civic-data-mcp](https://github.com/xmpuspus/ph-civic-data-mcp)** — Philippine government data: PHIVOLCS earthquakes and volcano alerts, PAGASA weather and typhoons, PhilGEPS procurement, PSA census data and AQICN air quality
  <sub>★ 5 · Python · MIT · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx ph-civic-data-mcp`</sub>
- **[musharna/data-aggregator-mcp](https://github.com/musharna/data-aggregator-mcp)** — Search and fetch research datasets across Zenodo, DataCite, NCBI and PubMed/OpenAIRE, with DOI deduplication, paper-to-data linking and verified downloads
  <sub>★ 4 · Python · MIT · uv · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx data-aggregator-mcp`</sub>
- **[thinkchainai/agentinterviews_mcp](https://github.com/thinkchainai/agentinterviews_mcp)** — Run AI-led qualitative research interviews and surveys with Agent Interviews: create interviewers, manage projects, recruit participants and analyze results
  <sub>★ 4 · source · pushed 2025-05-26</sub>
  <sub>`git clone https://github.com/thinkchainai/agentinterviews_mcp.git`</sub>
- **[tushariitr-19/immigration-mcp](https://github.com/tushariitr-19/immigration-mcp)** — US immigration guidance: live Visa Bulletin, priority date checks and explanations of immigration terms
  <sub>★ 3 · Go · MIT · clone · pushed 2026-06-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/tushariitr-19/immigration-mcp`</sub>
- **[lizhuojunx86/chinese-history-mcp](https://github.com/lizhuojunx86/chinese-history-mcp)** — Query classical Chinese texts from pre-Qin to Wei-Jin (Shiji, Zuozhuan, Analects and more) by event, person, place or virtue, with cited passages
  <sub>★ 3 · Python · MIT · uv · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx chinese-history-mcp --db /path/to/corpus.db`</sub>
- **[OrgMentem/zotio](https://github.com/OrgMentem/zotio)** — Zotero integration with preview-first, journaled writes: reads via the local Zotero desktop API without a key, writes via the Web API
  <sub>★ 3 · Go · MIT · winget · pushed 2026-10-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install OrgMentem.zotio`</sub>
- **[ovlabs/mcp-server-originalvoices](https://github.com/ovlabs/mcp-server-originalvoices)** — Query Original Voices digital twins, each representing a real person, to understand what users think and why
  <sub>★ 3 · JavaScript · source · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ovlabs/mcp-server-originalvoices.git`</sub>
- **[SokolskyNikita/annas-mcp](https://github.com/SokolskyNikita/annas-mcp)** — Search Anna's Archive for books and journal articles by title, author, topic or DOI, and download the chosen file
  <sub>★ 3 · Go · MIT · npm · pushed 2026-10-12 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g annas-mcp`</sub>
- **[zxhwolfe-dev/aiworkstation-open-source-intelligence](https://github.com/zxhwolfe-dev/aiworkstation-open-source-intelligence)** — Research open-source AI projects: search a live radar, compare and shortlist projects, and plan stacks, keeping facts, recommendations and risks separate
  <sub>★ 3 · Python · Apache-2.0 · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zxhwolfe-dev/aiworkstation-open-source-intelligence.git`</sub>
- **[thevibepreneur/gapbase-mcp](https://github.com/thevibepreneur/gapbase-mcp)** — Search a database of startup gaps by industry, role or keyword, each with the pain point, solution direction and a blueprint link. Works offline
  <sub>★ 2 · JavaScript · MIT · npm · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g gapbase-mcp`</sub>
- **[archoor/painspotter-mcp](https://github.com/archoor/painspotter-mcp)** — Startup and product opportunities mined from Reddit, Hacker News, Product Hunt and Stack Exchange: pain points, trending themes and commercial scores
  <sub>★ 1 · Python · MIT · pip · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install painspotter-mcp # or: uvx painspotter-mcp`</sub>
- **[rnwkr7rscy-lang/fittin-mcp](https://github.com/rnwkr7rscy-lang/fittin-mcp)** — Patent prior art search and startup IP analysis: clone risk scores, defensibility maps, patentable features and competitor patent landscapes
  <sub>★ 1 · Python · pip · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install fittin-mcp`</sub>
- **[SidneyBissoli/uis-mcp-server](https://github.com/SidneyBissoli/uis-mcp-server)** — UNESCO Institute for Statistics indicators on education, science, culture and communication by country, region and year, with provenance on every response
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-10-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/SidneyBissoli/uis-mcp-server`</sub>
- **[smeet666/mcp-archiveorg](https://github.com/smeet666/mcp-archiveorg)** — Full-text search inside the Internet Archive's scanned books, periodicals and documents, catalogue search, and Wayback Machine captures of a URL by date
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-archiveorg.git`</sub>
- **[wedo911/citeguard](https://github.com/wedo911/citeguard)** — Check citations against Crossref for retractions, corrections or expressions of concern before they go into a paper, summary or review
  <sub>★ 1 · Python · MIT · pip · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install citeguard-cli`</sub>
- **[SPARKIT-science/sparkit-mcp](https://github.com/SPARKIT-science/sparkit-mcp)** — Ask SPARKIT, a scientific research agent, questions and get cited Markdown reports based on literature search and paper reading
  <sub>★ 1 · Python · uv · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install sparkit-mcp`</sub>
- **[SelfPy/science-ai-mcp-server](https://github.com/SelfPy/science-ai-mcp-server)** — Science AI Journal tools: paper-tier prediction, AI peer review, research gap finder, journal recommender, duplicate publication checker and article writer
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-05-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SelfPy/science-ai-mcp-server.git`</sub>
- **[laszlopere/mcp-molecules](https://github.com/laszlopere/mcp-molecules)** — Chemistry tools from NIST data: molar mass with uncertainties, isotope-distribution mass spectra and name-formula lookup, offline or with online fallback
  <sub>★ 1 · Python · GPL-3.0 · uv · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install mcp-molecules`</sub>
- **[bartosz-kuc/honest-stat-gov-mcp](https://github.com/bartosz-kuc/honest-stat-gov-mcp)** — Polish Central Statistical Office (GUS) Local Data Bank (BDL): browse subjects, search variables and territorial units (voivodeship, powiat, gmina), get unit details, and fetch a variable's time series over a year range. No API key; queries bdl.stat.gov.pl directly with no third-party middleman
  <sub>Python · MIT · clone · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bartosz-kuc/honest-stat-gov-mcp.git`</sub>
- **[Agnuxo1/benchclaw-integrations](https://github.com/Agnuxo1/benchclaw-integrations/tree/main/mcp-server)** — Register LLMs and agents and submit Markdown research papers to the BenchClaw leaderboard, where a panel of judges scores them with deception detectors
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-04-25</sub>
  <sub>`git clone https://github.com/Agnuxo1/benchclaw-integrations.git && cd benchclaw-integrations/mcp-server`</sub>
- **[ankitkapur1992-hlido/hlido-mcp](https://github.com/ankitkapur1992-hlido/hlido-mcp)** — Hlido trust scores, claim audits and comparisons for reviewed AI agents: tier verdicts, per-claim pass/fail audits and signed evidence
  <sub>JavaScript · MIT · docker · pushed 2026-07-15 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 hlido-mcp`</sub>
- **[baseledgerip/realrun-mcp](https://github.com/baseledgerip/realrun-mcp)** — Read-only lookups of independent RealRun test results for AI models on everyday tasks (inbox triage, meeting scheduling, receipts): scores, model recommendations and safety warnings
  <sub>JavaScript · MIT · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y realrun-mcp`</sub>
- **[cluefinch/mcp-server](https://github.com/cluefinch/mcp-server)** — Cluefinch MCP provides Deep Research infrastructure for AI agents: web search, incremental page reading, source-link navigation, and multi-source evidence collection while the agent remains in control of planning and reasoning
  <sub>Python · Apache-2.0 · clone · pushed 2026-10-17 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/cluefinch/mcp-server.git`</sub>
- **[davidmosiah/uap-pulse](https://github.com/davidmosiah/uap-pulse)** — Read-only search of declassified U.S. federal UAP/UFO records, with hotspots, timelines, a live map dataset and direct source links
  <sub>HTML · MIT · npx · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y uap-pulse --http`</sub>
- **[Embassy-of-the-Free-Mind/sourcelibrary-v2](https://github.com/Embassy-of-the-Free-Mind/sourcelibrary-v2/tree/main/mcp-server)** — Search and cite rare historical texts (alchemy, Hermeticism, Renaissance philosophy) from Source Library with DOI-backed citations
  <sub>TypeScript · AGPL-3.0 · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/Embassy-of-the-Free-Mind/sourcelibrary-v2.git && cd sourcelibrary-v2/mcp-server`</sub>
- **[Guitarmaniac24/getabrain-mcp-server](https://github.com/Guitarmaniac24/getabrain-mcp-server)** — Ask paid human workers questions via GetABrain and get schema-validated JSON answers: yes/no, ratings, rankings, A/B tests, sentiment, media review and capture
  <sub>TypeScript · MIT · source · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Guitarmaniac24/getabrain-mcp-server.git`</sub>
- **[haoming-luo/agentfem-mcp](https://github.com/haoming-luo/agentfem-mcp)** — Create, validate, run, inspect and verify AgentFEM finite-element simulations
  <sub>Python · source · pushed 2026-09-19 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/haoming-luo/agentfem-mcp.git`</sub>
- **[herbertkokholm/cite-caddy](https://github.com/herbertkokholm/cite-caddy)** — Read and write a Zotero library: items, collections, tags, attachments, notes and bibliography export, with multi-tenant sign-in using your own Zotero API key
  <sub>Python · MIT · source · pushed 2026-10-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/herbertkokholm/cite-caddy.git`</sub>
- **[joelgombin/andre-mcp](https://github.com/joelgombin/andre-mcp)** — French election results since 1999 at polling-station level, with INSEE data, elected officials and boundaries: maps, vote-reserve analysis and read-only SQL
  <sub>Python · MIT · docker · pushed 2026-10-15 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -i --rm andre-mcp`</sub>
- **[jshelley/briefing-mcp](https://github.com/jshelley/briefing-mcp)** — Hourly LLM-ranked news briefings (AI, markets, sports, world) as structured JSON and e-ink pages, plus provenance data for every candidate story
  <sub>JavaScript · MIT · source · pushed 2026-09-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/jshelley/briefing-mcp.git`</sub>
- **[notDIRK/fds-mcp](https://github.com/notDIRK/fds-mcp)** — Freedom-of-information requests in Germany via FragDenStaat: find the responsible authority, check the law and deadline, track requests and draft new ones
  <sub>Python · MIT · uv · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx fds-mcp serve`</sub>
- **[TheWhiteWater/tube-bridge](https://github.com/TheWhiteWater/tube-bridge)** — Self-hosted YouTube research: video and channel search, transcripts, comments, playlists, timestamped frames and private local semantic corpora
  <sub>Python · MIT · uv · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx tube-bridge`</sub>
- **[smeet666/mcp-libraryofcongress](https://github.com/smeet666/mcp-libraryofcongress)** — Full-text search of the Library of Congress's digitised American newspapers, plus catalogue search by media type and curated collections
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-libraryofcongress.git`</sub>
- **[smeet666/mcp-databnf](https://github.com/smeet666/mcp-databnf)** — Search the open catalogue of the Bibliothèque nationale de France for authors, their works and the editions held
  <sub>TypeScript · MIT · source · pushed 2026-10-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/smeet666/mcp-databnf.git`</sub>

## File Systems

- **[mark3labs/mcp-filesystem-server](https://github.com/mark3labs/mcp-filesystem-server)** — Local file system access
  <sub>★ 692 · Go · MIT · go · pushed 2025-11-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/mark3labs/mcp-filesystem-server@latest`</sub>
- **[mamertofabian/mcp-everything-search](https://github.com/mamertofabian/mcp-everything-search)** — Windows file search using the Everything SDK
  <sub>★ 367 · Python · MIT · npx · pushed 2026-10-17 · macOS</sub>
  <sub>`npx @modelcontextprotocol/inspector uvx mcp-server-everything-search`</sub>
- **[cyberchitta/llm-context.py](https://github.com/cyberchitta/llm-context.py)** — Share code context with LLMs via MCP or the clipboard
  <sub>★ 307 · Python · Apache-2.0 · uv · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "llm-context>=0.6.0"`</sub>
- **[isaacphi/mcp-gdrive](https://github.com/isaacphi/mcp-gdrive)** — Read from Google Drive and edit Google Sheets
  <sub>★ 282 · TypeScript · MIT · source · pushed 2025-05-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/isaacphi/mcp-gdrive.git`</sub>
- **[8b-is/smart-tree](https://github.com/8b-is/smart-tree)** — Directory visualization with semantic analysis, compressed AI-oriented output formats and file categorization
  <sub>★ 271 · Rust · MIT · cargo · pushed 2026-10-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`cargo install smart-tree`</sub>
- **[efforthye/fast-filesystem-mcp](https://github.com/efforthye/fast-filesystem-mcp)** — Filesystem operations with large-file support: read and write files, sequential reads, directory operations, search and streaming writes with backup
  <sub>★ 64 · TypeScript · Apache-2.0 · npm · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g fast-filesystem-mcp`</sub>
- **[UseJunior/safe-docx](https://github.com/UseJunior/safe-docx)** — Edit existing Word .docx files with formatting preservation, tracked changes, comments, footnotes and document comparison
  <sub>★ 46 · TypeScript · Apache-2.0 · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install --global @usejunior/safe-docx`</sub>
- **[ltspace/dowse](https://github.com/ltspace/dowse)** — Read-only full-disk search on Windows over file names, document contents and OCR'd screenshot text
  <sub>★ 37 · Rust · Apache-2.0 · cargo · pushed 2026-10-19 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`cargo install dowse # once published to crates.io`</sub>
- **[Xuanwo/mcp-server-opendal](https://github.com/Xuanwo/mcp-server-opendal)** — Access any storage backend through Apache OpenDAL
  <sub>★ 35 · Python · Apache-2.0 · pip · pushed 2025-04-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-server-opendal`</sub>
- **[jeannier/homebrew-mcp](https://github.com/jeannier/homebrew-mcp)** — Manage macOS Homebrew packages with natural language, get suggestions and troubleshoot brew issues
  <sub>★ 30 · Python · MIT · clone · pushed 2025-06-23 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/jeannier/homebrew-mcp`</sub>
- **[exoticknight/mcp-file-merger](https://github.com/exoticknight/mcp-file-merger)** — Merge files to work within AI chat length limits
  <sub>★ 28 · JavaScript · Apache-2.0 · clone · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/exoticknight/mcp-file-merger.git`</sub>
- **[ckanthony/Chisel](https://github.com/ckanthony/Chisel)** — Token-efficient file access: unified-diff edits, targeted grep/sed reads of large files and kernel-enforced confinement to a configured root
  <sub>★ 26 · Rust · npx · pushed 2026-03-07 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx skills add ckanthony/Chisel`</sub>
- **[dimitar-grigorov/mcp-file-tools](https://github.com/dimitar-grigorov/mcp-file-tools)** — Filesystem access for legacy non-UTF-8 files: detects encodings like CP1251, KOI8-R and GBK, preserves them on write, and handles BOM and line endings
  <sub>★ 26 · Go · GPL-3.0 · npx · pushed 2026-10-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @modelcontextprotocol/inspector go run ./cmd/mcp-file-tools -- /path/to/allowed/dir`</sub>
- **[j0hanz/filesystem-context-mcp-server](https://github.com/j0hanz/filesystem-mcp)** — Read-only filesystem exploration, search and analysis with symlink protection
  <sub>★ 25 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @j0hanz/filesystem-mcp`</sub>
- **[colapsis/transfa](https://github.com/colapsis/transfa)** — Ephemeral file transfer for agents and CI/CD pipelines: upload a file and get a SHA-256-verified, expiring link, then list or delete uploads
  <sub>★ 21 · JavaScript · MIT · npm · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g transfa`</sub>
- **[willianpinho/large-file-mcp](https://github.com/willianpinho/large-file-mcp)** — Large-file handling with chunking, navigation, streaming, regex search and LRU caching
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @willianpinho/large-file-mcp`</sub>
- **[Cohexa-ai/agent-coherence](https://github.com/cohexa-ai/agent-coherence)** — Coherence guard for shared files: when two agents write the same file, the stale writer is denied instead of overwriting, then reacquires and retries
  <sub>★ 11 · Python · pip · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "agent-coherence[langgraph]" # LangGraph drop-in`</sub>
- **[drolosoft/go-docs-mcp](https://github.com/drolosoft/go-docs-mcp)** — Read, search, OCR and extract from PDF, TXT, Markdown, DOCX, CSV and image files, with caching and directory confinement
  <sub>★ 11 · Go · MIT · go · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`go install github.com/drolosoft/go-docs-mcp@latest`</sub>
- **[hmk/box-mcp-server](https://github.com/hmk/box-mcp-server)** — Box integration for listing, reading and searching files
  <sub>★ 11 · JavaScript · BSD-3-Clause · clone · pushed 2025-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YOUR_USERNAME/box-mcp-server.git`</sub>
- **[MarceauSolutions/md-to-pdf-mcp](https://github.com/MarceauSolutions/md-to-pdf-mcp)** — Convert Markdown files to PDF with customizable themes, headers, footers and styling
  <sub>★ 8 · Python · source · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MarceauSolutions/md-to-pdf-mcp.git`</sub>
- **[aadilr/changethisfile-mcp](https://github.com/aadilr/changethisfile-mcp)** — File conversion across image, video, audio, document, data, font, ebook and archive formats, returning a signed download URL
  <sub>★ 6 · JavaScript · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add aadilr/changethisfile-mcp`</sub>
- **[box/mcp-server-box-remote](https://github.com/box/mcp-server-box-remote/)** — Access Box content: search, ask questions about files and folders, and extract data
  <sub>★ 6 · MIT · source · pushed 2025-09-20</sub>
  <sub>`git clone https://github.com/box/mcp-server-box-remote/.git`</sub>
- **[bzsanti/oxidize-python](https://github.com/bzsanti/oxidize-python)** — PDF toolkit: create and analyze PDFs, extract text for RAG, convert to Markdown, split and merge pages, add annotations and form fields, and encrypt files
  <sub>★ 6 · Python · MIT · pip · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install oxidize-pdf # Core library`</sub>
- **[Dissimilis/DirForge](https://github.com/Dissimilis/DirForge)** — #️⃣ 🏠 🍎 🪟 🐧 - Read-only directory listing web app: browse directories, read files, search content, inspect archives, compute hashes and check disk usage
  <sub>★ 5 · C# · MIT · source · pushed 2026-06-10 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Dissimilis/DirForge.git`</sub>
- **[ellmos-ai/ellmos-filecommander-mcp](https://github.com/ellmos-ai/ellmos-filecommander-mcp)** — Local filesystem management with process control, interactive sessions, async search and safe delete via the Recycle Bin
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g ellmos-filecommander-mcp`</sub>
- **[Synexiom-Labs/nodiom-mcp](https://github.com/Synexiom-Labs/nodiom-mcp)** — Read and edit Markdown files by structure (headings, lists, sections) instead of regex or line numbers: read a section, write one list item, append under a heading
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @synexiom-labs/nodiom-mcp`</sub>
- **[ezpzfile/ezpzfile-mcp](https://github.com/ezpzfile/ezpzfile-mcp)** — Local document and image tools: read and convert PDF, DOCX, HWP and EML, edit PDFs, resize images, strip EXIF, remove backgrounds and make QR codes
  <sub>★ 4 · TypeScript · MIT · source · pushed 2026-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ezpzfile/ezpzfile-mcp.git`</sub>
- **[FacundoLucci/plsreadme](https://github.com/FacundoLucci/plsreadme)** — Share Markdown files and text as readable web links
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx add-mcp plsreadme-mcp`</sub>
- **[GuruPDF/gurupdf-mcp](https://github.com/GuruPDF/gurupdf-mcp)** — Convert, compress, merge, split and OCR PDFs, and convert between Word, Excel, PowerPoint, image, ebook and video formats via the GuruPDF API
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GuruPDF/gurupdf-mcp.git`</sub>
- **[LincolnBurrows2017/filesystem-mcp](https://github.com/LincolnBurrows2017/filesystem-mcp)** — File system operations: read, write, search, copy and move, with path restrictions
  <sub>★ 2 · Python · MIT · pip · pushed 2026-03-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install filesystem-mcp`</sub>
- **[velyan/pdf-card-mcp](https://github.com/velyan/pdf-card-mcp)** — Convert local PDFs into source-linked, card-based standalone HTML readers with notes, highlights and static publishing
  <sub>★ 2 · Python · MIT · clone · pushed 2026-09-05 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/velyan/pdf-card-mcp.git`</sub>
- **[juergenkoller-software/distill-mcp](https://github.com/juergenkoller-software/distill-mcp)** — Rename files with descriptive names via Distill, which analyzes PDF, OCR, Office, email and media content, with folder monitoring
  <sub>★ 2 · Swift · MIT · clone · pushed 2026-10-20 · macOS · Linux</sub>
  <sub>`git clone https://github.com/juergenkoller-software/distill-mcp.git`</sub>
- **[dabito/hledit-mcp](https://github.com/dabito/hledit-mcp)** — Hash-anchored file edits: read files with line anchors, validate anchors against current content and reject stale writes
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx hledit-mcp`</sub>
- **[FI-Mihej/text_file_read_and_refactor_mcp](https://github.com/FI-Mihej/text_file_read_and_refactor_mcp)** — Token-efficient text-file search, reading and refactoring that detects each file's BOM and codepage and preserves them on save
  <sub>★ 1 · Python · Apache-2.0 · source · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/FI-Mihej/text_file_read_and_refactor_mcp.git`</sub>
- **[L-Jovi/keyhole](https://github.com/L-Jovi/keyhole)** — Give a private ChatGPT app access to selected local folders through OpenAI Secure MCP Tunnel, with per-folder permissions, hash-checked edits and recovery. No shell or public port
  <sub>★ 1 · Python · MIT · uv · pushed 2026-10-17 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install keyhole-mcp`</sub>
- **[TrendTweekers/mintpdf](https://github.com/TrendTweekers/mintpdf)** — Convert HTML or Markdown to styled PDFs, or render a public URL to PDF, and get a download link
  <sub>★ 1 · TypeScript · MIT · docker · pushed 2026-10-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 -e BASE_URL=http://localhost:3000 mintpdf`</sub>
- **[A1-x-Tech/mcp-google-drive](https://github.com/A1-x-Tech/mcp-google-drive)** — Google Drive API: search, organize, upload, download, export, share and comment on Drive files
  <sub>TypeScript · MIT · npx · pushed 2026-10-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @a1-x-tech/mcp-google-drive@latest`</sub>
- **[Agaveis/hiberden-mcp](https://github.com/Agaveis/hiberden-mcp)** — Read and verify a local media-archive catalog: 3-2-1 backup coverage across disk, NAS, S3-compatible cloud and LTO tape, with read-back hash verification
  <sub>Dockerfile · MIT · docker · pushed 2026-10-20 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --rm -i -v /var/lib/hiberden:/cat -e HIBERDEN_DB=/cat/catalog.db agaveis/hiberden-mcp`</sub>
- **[arjunprabhulal/superpdf](https://github.com/arjunprabhulal/superpdf)** — Read, convert, edit and compare PDFs on your computer: Markdown with tables, charts and OCR, export to Word, PowerPoint and EPUB, tables to CSV or Excel, merge, split, fill forms and remove metadata. Nothing is uploaded
  <sub>JavaScript · Apache-2.0 · npm · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @superpdf/cli`</sub>
- **[koraynar/doc-extract-mcp](https://github.com/koraynar/doc-extract-mcp)** — Document extraction tooling: read PDFs, text, CSV and JSON, inspect metadata, chunk long documents, validate against JSON Schema and write JSON/CSV output
  <sub>Python · MIT · clone · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/koraynar/doc-extract-mcp.git`</sub>
- **[convertica-net/convertica-mcp](https://github.com/convertica-net/convertica-mcp)** — Convert PDFs to and from Word, Excel, PowerPoint, JPG, HTML, Markdown and EPUB, plus merge, split, compress, sign and protect PDFs via Convertica
  <sub>JavaScript · MIT · source · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/convertica-net/convertica-mcp.git`</sub>
- **[denis-samatov/yandex-workspace-mcp](https://github.com/denis-samatov/yandex-workspace-mcp)** — Yandex Disk and Yandex Wiki integration with unified search, read-only by default, plus granular permissions, path allowlisting and audit logging
  <sub>Python · MIT · clone · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/denis-samatov/yandex-workspace-mcp`</sub>
- **[filesystem@quarkiverse/quarkus-mcp-servers](https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/filesystem)** — Filesystem access for browsing and editing files
  <sub>Java · Apache-2.0 · in-repo · pushed 2026-06-14</sub>
  <sub>`git clone https://github.com/quarkiverse/quarkus-mcp-servers.git && cd quarkus-mcp-servers/filesystem`</sub>
- **[jamalofski/conv2pdf-mcp](https://github.com/Jamalofski/conv2pdf-mcp)** — Convert Office documents, images and e-books on your computer to PDF, convert PDFs to Word or images, and merge, split, compress, protect or number PDFs via the conv2pdf API, hosted in France
  <sub>JavaScript · MIT · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y conv2pdf-mcp`</sub>
- **[Kookerella-Ltd/Kookerella.FsOpenXmlDsl](https://github.com/Kookerella-Ltd/Kookerella.FsOpenXmlDsl/tree/master/src/Kookerella.FsOpenXmlDsl.Mcp)** — Create, read and round-trip Excel workbooks (.xlsx/.xlsm) via a type-safe F# DSL, including regenerating the F# source that reproduces a file
  <sub>F# · MIT · in-repo · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/Kookerella-Ltd/Kookerella.FsOpenXmlDsl.git && cd Kookerella.FsOpenXmlDsl/src/Kookerella.FsOpenXmlDsl.Mcp`</sub>
- **[mickaelkerjean/filestash](https://github.com/mickael-kerjean/filestash/tree/master/server/plugin/plg_handler_mcp)** — Remote storage access: SFTP, S3, FTP, SMB, NFS, WebDAV, Git, FTPS, Google Cloud, Azure Blob, SharePoint and more
  <sub>Go · AGPL-3.0 · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/mickael-kerjean/filestash.git && cd filestash/server/plugin/plg_handler_mcp`</sub>
- **[microsoft/markitdown](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)** — Convert many file formats, local or remote, to Markdown for LLMs using MarkItDown
  <sub>Python · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/microsoft/markitdown.git && cd markitdown/packages/markitdown-mcp`</sub>
- **[modelcontextprotocol/server-filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)** — Direct local file system access
  <sub>TypeScript · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/servers.git && cd servers/src/filesystem`</sub>
- **[Regan-Milne/obsideo-mcp](https://github.com/Regan-Milne/obsideo-mcp)** — Encrypted S3-compatible object storage with cryptographic possession proofs: put, get, list and delete objects, with optional client-side encryption
  <sub>TypeScript · source · pushed 2026-09-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Regan-Milne/obsideo-mcp.git`</sub>
- **[alebgl77/ftp-deploy-mcp](https://github.com/alebgl77/ftp-deploy-mcp)** — Deploy files to FTP, FTPS or SFTP servers: multi-server config, recursive deploys with dry-run and excludes, path jails, read-only mode and FileZilla import
  <sub>JavaScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y ftp-deploy-mcp@0.3.2`</sub>

## Education

<sub>Entries 1–6 of 13. The rest are on this page's other parts, linked above and below.</sub>

- **[RohanMuppa/brightspace-mcp-server](https://github.com/RohanMuppa/brightspace-mcp-server)** — Check D2L Brightspace grades, due dates, assignments, announcements, syllabus, rosters, discussions and course content
  <sub>★ 59 · TypeScript · MIT · npx · pushed 2026-10-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx -y brightspace-mcp-server@latest setup`</sub>
- **[anzy-renlab-ai/pronounce](https://github.com/anzy-renlab-ai/pronounce)** — Community pronunciation dictionary for developer and product names (kubectl, nginx, GIF) with IPA, respellings, alternate readings and cited sources
  <sub>★ 47 · Python · MIT · brew · pushed 2026-09-01 · WSL2 · macOS · Linux</sub>
  <sub>`brew install anzy-renlab-ai/tap/say-it # Homebrew on macOS`</sub>
- **[AnonymousOnyx22/brightspace-d2l-mcp](https://github.com/AnonymousOnyx22/brightspace-d2l-mcp)** — D2L Brightspace for students: due dates with submission status, grades, assignments and rubrics, announcements and discussions, using browser sign-in
  <sub>★ 28 · TypeScript · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx brightspace-d2l-mcp setup`</sub>
- **[ictinnovations/ictexam-mcp](https://github.com/ictinnovations/ictexam-mcp)** — Read exam papers, classes, subjects, the gradebook and per-question item analysis from ICTExam, an exam authoring and auto-grading platform
  <sub>★ 17 · TypeScript · MIT · npm · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g ictexam-mcp`</sub>
- **[alejooroncoy/campus-cli](https://github.com/alejooroncoy/campus-cli)** — Student access to university systems via SSO: courses, assignments, grades, feedback, announcements and materials, currently for Blackboard Learn (UPC, Peru)
  <sub>★ 11 · TypeScript · ISC · npm · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g campus-cli@2.2.3`</sub>
- **[giacomomaria81/scorm-mcp-server](https://github.com/giacomomaria81/scorm-mcp-server)** — Package HTML, Claude Design bundles or mobile-learning exports as SCORM 2004/1.2 courses with milestone and question tracking, and validate SCORM zips
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y scorm-mcp-server ui # local drag`</sub>

Page **2** of 6, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · **2** · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) — [continue on page 3 →](mcp-servers-punkpeye-3.md)

---

Snapshot 2026-10-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
