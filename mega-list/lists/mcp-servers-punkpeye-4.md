# MCP Servers (punkpeye)

A collection of MCP servers.

Curated by **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

4,242 entries · 4,216 distinct repos · 60 sections

[← back to the mega list](../README.md)

Page **4** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · **4** · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · [7](mcp-servers-punkpeye-7.md) — [continue on page 5 →](mcp-servers-punkpeye-5.md)

## Contents

- [Finance &amp; Fintech](#finance--fintech) (463)
- [Delivery](#delivery) (19)
- [E-Commerce](#e-commerce) (42)
- [Legal](#legal) (35)
- [Real Estate](#real-estate) (13)
- [Cryptography](#cryptography) (5)
- [Aggregators](#aggregators) (137)
- [Security](#security) (242)
- [Cloud Platforms](#cloud-platforms) (135)
- [Monitoring](#monitoring) (87)

## Finance &amp; Fintech

<sub>Entries 452–463 of 463. The rest are on this page's other parts, linked above and below.</sub>

- **[Faouzi122/Arsenal-Quant-Project](https://github.com/Faouzi122/Arsenal-Quant-Project)** — Deterministic MEV &amp; Slippage Risk Oracle for DeFAI Agents. Free tier open; L402 paid layer not yet in service
  <sub>Python · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Faouzi122/Arsenal-Quant-Project.git`</sub>
- **[true402/mcp-server](https://github.com/true402/mcp-server)** — Pay-per-call AI + web + on-chain tools for agents over x402 (USDC on Base) — no accounts, no API keys; the wallet is the identity. 11 tools incl. token rug/honeypot safety (0–100 score, risk band, buy/sell simulation), new-pairs / liquidity-pull / whale-swap signals, SEO/GEO audit, web extract, link preview, robots &amp; security-headers checks, and LLM inference. Tools auto-discover from the live cat
  <sub>TypeScript · MIT · source · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/true402/mcp-server.git`</sub>
- **[Nikolife2016/pulsefeed-x402](https://github.com/Nikolife2016/pulsefeed-x402)** — Trust &amp; safety layer for x402 agent payments: before your agent pays an x402 endpoint, verify it is safe — liveness, scam/anomaly scan (payTo hijack, bait-and-switch, honeypot), and on-chain receiver verification. ~70% of x402 endpoints are dead or scams; only ~half of "healthy" listings work. Free /verify + an open Trust Score. npx -y pulsefeed-x402-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx pulsefeed-x402-mcp`</sub>
- **[slenderongithub/fix-protocol-mcp](https://github.com/slenderongithub/fix-protocol-mcp)** — Parse, validate, build, and explain FIX protocol trading messages (Logon, NewOrderSingle, ExecutionReport, and the rest of the session/order workflow). Fully offline — bundled FIX 4.4 field dictionary, no API keys or network calls. Install pip install ., run fix-protocol-mcp
  <sub>Python · MIT · source · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/slenderongithub/fix-protocol-mcp.git`</sub>
- **[amitesh-m/wealthville-integrations](https://github.com/amitesh-m/wealthville-integrations)** — Solana + EVM liquidity-pool scores for AI agents: Enter/Hold/Exit verdicts and a composite 0–100 Wealthville Score, plus a live, immutable, miss-inclusive track record. 4 read-only tools (pool score, top pools, track record, signals feed). In the official MCP Registry. npx @wealthville/mcp-server
  <sub>TypeScript · MIT · npx · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @wealthville/mcp-server`</sub>
- **[SynderAccounting/gl-importer-plugin](https://github.com/SynderAccounting/gl-importer-plugin)** — Import CSV/XLSX accounting data into QuickBooks Online or Xero via the Synder Importer API. 19 tools covering imports, field mapping rules, post-import rules, and entity discovery. Install with npx -y @cloudbusiness/gl-importer-mcp
  <sub>TypeScript · MIT · clone · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SynderAccounting/gl-importer-plugin`</sub>
- **[sturs49/cryptotaxedge-mcp](https://github.com/sturs49/cryptotaxedge-mcp)** — US tax classification for on-chain transactions: submit a transaction hash, get the canonical category, US tax treatment, a confidence score, and an explicit route-to-review flag on uncertain rows. 80+ chains. Remote streamable-HTTP server at https://mcp.cryptotaxedge.com/ (free Developer tier); on the official MCP registry as io.github.sturs49/cryptotaxedge
  <sub>JavaScript · MIT · docker · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 8080:8080 cryptotaxedge-mcp`</sub>
- **[sand0vvv/hyperevm-mcp](https://github.com/sand0vvv/hyperevm-mcp)** — Read-only Hyperliquid / HyperEVM: every way to earn on HYPE in one table — liquid staking, lending with utilisation and max LTV, LP pools, and the HLP vault — with yield a pool earns separated from yield paid in emitted tokens. Also protocol TVL, fees actually paid, perp and spot markets, funding history, and order-book depth with a straight answer when a size will not fill. Where a source publish
  <sub>TypeScript · MIT · source · pushed 2026-07-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sand0vvv/hyperevm-mcp.git`</sub>
- **[polyorderbooks/mcp-server](https://github.com/polyorderbooks/mcp-server)** — Historical Polymarket order book depth — full L2 bid/ask ladders at 1-second resolution on resolved markets, plus prices, spread and liquidity. Polymarket archives no order book history, so this serves depth captured live
  <sub>unavailable</sub>
- **[ravndex/ravn-mcp-glama](https://github.com/ravndex/ravn-mcp-glama)** — Cross-chain swap execution across 12 venues and 16 chains, including native (non-wrapped) Bitcoin as either source or destination. No signup, no API key, 0% protocol fee — same routing engine the app itself uses. Hosted remote server (no install) at https://app.ravn.exchange/api/mcp; this repo is a local/stdio alternative. On the official MCP registry as exchange.ravn/ravn
  <sub>TypeScript · MIT · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ravndex/ravn-mcp-glama`</sub>
- **[parkyucheol-del/alphapipeline](https://github.com/parkyucheol-del/alphapipeline)** — Pay-per-call ($0.005-$0.03 USDC via x402 on Base) market and on-chain data for AI agents and trading bots: token-unlock dump-risk, Upbit/Binance kimchi-premium arbitrage alerts, GoPlus honeypot &amp; LP-lock contract-health audits, DEX liquidity/slippage estimates, funding-rate APR &amp; carry-trade breakeven, and a URL-to-clean-markdown tool. No signup, no API key. 12 tools; remote at https://alphapipeli
  <sub>Python · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/parkyucheol-del/alphapipeline.git`</sub>
- **[yourmatematt/agent-billboard-mcp](https://github.com/yourmatematt/agent-billboard-mcp)** — Read and post to The Agent Billboard, a single on-chain message slot on Solana where AI agents advertise to one another. Posting rights are acquired by outbidding the previous poster; the server enforces operator spend limits before signing and logs the agent's reasoning with every write. npx -y agent-billboard-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y agent-billboard-mcp`</sub>

## Delivery

- **[childrentime/reactuse](https://github.com/childrentime/reactuse)** — MCP server for the ReactUse library — 110+ React Hooks (TypeScript-first, SSR-compatible, tree-shakable). Lets AI assistants discover hook signatures, demos, and usage patterns directly from the docs
  <sub>★ 1.1k · MDX · Unlicense · source · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/childrentime/reactuse.git`</sub>
- **[jordandalton/doordash-mcp-server](https://github.com/JordanDalton/DoorDash-MCP-Server)** — DoorDash Delivery (Unofficial)
  <sub>★ 25 · TypeScript · source · pushed 2025-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JordanDalton/DoorDash-MCP-Server.git`</sub>
- **[arthurpanhku/DragonMCP](https://github.com/arthurpanhku/DragonMCP)** — MCP server for Greater China local life services: Meituan/Ele.me food delivery, Didi/Meituan ride-hailing, WeChat Pay/Alipay, Amap/Baidu Maps, 12306 high-speed rail, Taobao/JD/Xianyu e-commerce, Hong Kong government e-services, and more
  <sub>★ 21 · TypeScript · MIT · npx · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx dragon-mcp`</sub>
- **[Dudude-bit/yandex-lavka-mcp](https://github.com/Dudude-bit/yandex-lavka-mcp)** — Order groceries from Yandex Lavka (Russia): search the catalog, build a cart, and place an order with a two-step confirmation before any charge. Unofficial (reverse-engineered private web API); local stdio or remote HTTP with OAuth. uvx yandex-lavka-mcp
  <sub>★ 20 · Python · MIT · source · pushed 2026-09-10 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Dudude-bit/yandex-lavka-mcp.git`</sub>
- **[warpfreight/warp-agent-mcp](https://github.com/warpfreight/warp-agent-mcp)** — Book real LTL/FTL/van/box-truck freight through the Warp network. 20 tools, in-chat login, Stripe-charged bookings, real carrier dispatch. Live demo at wearewarp.com/agents/mcp
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y warp-agent-mcp`</sub>
- **[catrinmdonnelly/royalmail-mcp](https://github.com/catrinmdonnelly/royalmail-mcp)** — Book, label, track and cancel Royal Mail and Parcelforce shipments. 33 UK and international services via friendly keys or raw Service Register codes. npx royalmail-mcp
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g royalmail-mcp`</sub>
- **[kannajune/mcp-architect](https://github.com/kannajune/mcp-architect)** — Gives any AI assistant real architectural understanding of a codebase: tech-stack overview, internal dependency graph with cycle detection, risk hotspots, and module summaries. Local, zero-config, no API keys. uvx mcp-architect
  <sub>★ 3 · Python · MIT · pip · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-architect`</sub>
- **[deslay1/amendor-mcp](https://github.com/deslay1/amendor-mcp)** — Lets the non-technical people you build for request UI changes directly on your live site, then pulls each request (with the exact element and page) into your coding agent so it builds it on a branch and opens a pull request. Works with Claude Code, Cursor, Cline, Codex, and remote agents over HTTP. npx -y amendor-mcp
  <sub>★ 2 · JavaScript · source · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/deslay1/amendor-mcp.git`</sub>
- **[LS-SIEM-LLP/qa-probe](https://github.com/LS-SIEM-LLP/qa-probe)** — Probes your live API and classifies why each endpoint failed (root cause + evidence + calibrated confidence) over MCP, so your AI assistant debugs from evidence instead of guessing. Deterministic rules, no black box. Works with FastAPI, Express, Next.js, tRPC, and GraphQL. npm i -g qa-probe
  <sub>★ 2 · JavaScript · Apache-2.0 · npm · pushed 2026-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g qa-probe`</sub>
- **[zyqzyq/Unfour](https://github.com/zyqzyq/Unfour)** — Local-first backend developer workspace exposing API debugging, SSH, database, workspace, and diagnostics tools to AI agents through a local MCP server, with workspace-scoped safety policies and confirmation for risky actions
  <sub>★ 2 · Rust · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/zyqzyq/Unfour.git`</sub>
- **[smklog/parcel-shipping-rates-mcp](https://github.com/smklog/parcel-shipping-rates-mcp)** — Live USPS, UPS, FedEx and DHL parcel rates from the US (domestic, Canada, UK, Germany, Australia) from a plain-words item description, plus checkout links, checkout status and tracking. No API key
  <sub>★ 1 · JavaScript · MIT · docker · pushed 2026-09-05 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm smklog-parcel-shipping-rates-mcp`</sub>
- **[Yang1Bai/claw-tsaver](https://github.com/Yang1Bai/claw-tsaver)** — __ 🐍 🏠 🍎 🪟 🐧 - Token-saving MCP proxy that intercepts oversized tool returns and replaces them with a preview + on-demand handle. Real benchmark: 11,507 tokens → 104 tokens (99.1% saved) on a Wikipedia fetch. Works with OpenClaw + Claude
  <sub>★ 1 · Python · MIT · npm · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g claw-tsaver`</sub>
- **[todah-zg/codemagic-mcp](https://github.com/todah-zg/codemagic-mcp)** — Build, sign, and publish iOS and Android apps through AI agents. Integrates Codemagic CI/CD, App Store Connect, and Google Play in one server
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g codemagic-mcp-server`</sub>
- **[A1-x-Tech/mcp-yandex-dostavka](https://github.com/A1-x-Tech/mcp-yandex-dostavka)** — Yandex Delivery B2B API — express-courier claims (price check, create, track, cancel) and pickup-point/NDD orders
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yandex-dostavka@latest`</sub>
- **[A1-x-Tech/mcp-yango-delivery](https://github.com/A1-x-Tech/mcp-yango-delivery)** — Yango Delivery B2B API (international Yandex Delivery) — express-courier price checks, delivery claims, courier tracking and confirmation codes
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yango-delivery@latest`</sub>
- **[aarsiv-groups/shipi-mcp-server](https://github.com/aarsiv-groups/shipi-mcp-server)** — Shipi MCP server to create shipments, track packages, and compare rates with 18 tools for various carriers. Supports remote MCP
  <sub>unavailable</sub>
- **[CydVilla/peckish](https://github.com/CydVilla/peckish)** — Order food on DoorDash: searches stores, compares real fee-included totals from live quotes, builds carts, plus groceries, promos, pickup, reorders and spend history. Placing an order always requires a client elicitation dialog you approve — clients without elicitation can browse and build carts but cannot order (fail closed). Built on DoorDash's official CLI (waitlist-gated, macOS arm64). npx -y
  <sub>TypeScript · MIT · npm · pushed 2026-08-10 · macOS</sub>
  <sub>`npm install -g peckish`</sub>
- **[iafanasov/packzoo-mcp](https://github.com/IAfanasov/packzoo-mcp)** — Compare parcel and letter delivery prices across 60+ carriers in 27 European countries. Remote MCP: packzoo.com/api/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:IAfanasov/packzoo-mcp`</sub>
- **[getproxykit/proxykit-mcp](https://github.com/getproxykit/proxykit-mcp)** — Drive a local ProxyKit MITM debugging proxy from any MCP client: inspect captured HTTP(S)/gRPC/WebSocket traffic, create mocks and rewrites, replay requests, run chaos scenarios, and triage privacy/security findings — 50 tools across read-only and opt-in write tiers, all on your own machine. Install: brew install getproxykit/tap/proxykit-cli
  <sub>Dockerfile · MIT · winget · pushed 2026-09-11 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`winget install ProxyKit.ProxyKitCLI`</sub>

## E-Commerce

- **[jlsookiki/secondhand-mcp](https://github.com/jlsookiki/secondhand-mcp)** — Search Facebook Marketplace, eBay, Depop, and Poshmark for secondhand items. Filter by price, condition, category, size, and color; full listing details with photos and seller info; deep-research search/fetch tools. eBay uses the official Browse API (bring your own keys); a hosted version at secondhandmcp.com connects to Claude.ai and ChatGPT. Install via npx -y secondhand-mcp
  <sub>★ 78 · TypeScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jlsookiki/secondhand-mcp.git`</sub>
- **[TonyWang-hub/mcp-cn-commerce](https://github.com/TonyWang-hub/mcp-cn-commerce)** — Read-only merchant data connector for 8 Chinese e-commerce platforms — Tmall/Taobao, JD.com, Pinduoduo, Douyin Shop + Qianchuan ads, Kuaishou, Xiaohongshu, and WeChat Store. Orders, products, after-sales, inventory, and ad reports for AI agents. Published on the official MCP Registry. Install via pip install mcp-cn-commerce
  <sub>★ 61 · Python · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/TonyWang-hub/mcp-cn-commerce.git`</sub>
- **[ilyautov/marketplaces-mcp-ru](https://github.com/ilyautov/marketplaces-mcp-ru)** — Wildberries and Ozon Seller APIs for Russian marketplace sellers: sales, stocks, prices, finance, reviews and ads through 793 schema-driven methods with a read/write/destructive safety gate, multi-store switching and ready-made seller workflows. PyPI (uvx marketplaces-mcp-ru), Docker image, one-click Claude Desktop .mcpb bundle
  <sub>★ 34 · Python · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y marketplaces-mcp-ru doctor --live # то же через npm, без Python`</sub>
- **[nicktcode/swissgroceries-mcp](https://github.com/nicktcode/swissgroceries-mcp)** — Swiss grocery search, weekly promotions, and multi-store shopping plans across Migros, Coop, Aldi, Denner, Lidl, Farmy, Volg, and Otto's. Cross-chain unit-price comparison and three planning strategies (single_store / split_cart / absolute_cheapest). Install via npx -y @nicktcode/swissgroceries-mcp
  <sub>★ 32 · TypeScript · npx · pushed 2026-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @nicktcode/swissgroceries-mcp`</sub>
- **[PCDCK/ozon-mcp](https://github.com/PCDCK/ozon-mcp)** — Knowledge-rich MCP server for the full Ozon Seller + Performance API (466 methods, 15 MCP tools). Auto-pagination over 4 cursor styles, subscription-tier pre-flight, rate-limit management with exponential back-off, and 13 curated analytical workflows (OOS risk, cabinet health, content audit, pricing, warehouse distribution). Russian + English BM25 search across the catalog
  <sub>★ 20 · Python · MIT · clone · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PCDCK/ozon-mcp.git`</sub>
- **[BuyWhere/buywhere-mcp](https://github.com/BuyWhere/buywhere-mcp)** — Cross-border e-commerce product catalog for AI agents. Search 3M+ products across Singapore, SEA, and US markets with price comparison and deal discovery. Install via npx @buywhere/mcp-server
  <sub>★ 14 · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @buywhere/mcp-server`</sub>
- **[HasData/walmart-mcp](https://github.com/HasData/walmart-mcp)** — Remote MCP server for Walmart: search results, product pages with the buy-box seller, and customer reviews on walmart.com and walmart.ca, as JSON
  <sub>★ 10 · JavaScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/walmart-mcp.git`</sub>
- **[justadityaraj/amazon-in-mcp](https://github.com/justadityaraj/amazon-in-mcp)** — Shop on amazon.in via LLM. Three tools: product search with "cheapest in stock" + "best value" picks, full product details (price, MRP, discount, rating, stock, seller), and Keepa price history chart links. No API keys, direct HTML scraping with retry on bot-check. Install: npx amazon-in-mcp-server
  <sub>★ 9 · TypeScript · MIT · npx · pushed 2026-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y amazon-in-mcp-server`</sub>
- **[HasData/amazon-mcp](https://github.com/HasData/amazon-mcp)** — Remote MCP server for Amazon: keyword search, product details by ASIN, product reviews, seller profiles and seller catalogues across marketplaces, as JSON
  <sub>★ 8 · JavaScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/amazon-mcp.git`</sub>
- **[agentcentral-to/agent-central-mcp](https://github.com/agentcentral-to/agent-central-mcp)** — Hosted Amazon Seller Central and Amazon Ads MCP server for Claude, ChatGPT, and other AI clients, exposing inventory, orders, catalog, finance, fulfillment, and advertising data through a remote MCP endpoint
  <sub>★ 6 · JavaScript · MIT · docker · pushed 2026-06-01 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i agentcentral-mcp`</sub>
- **[mrslbt/rakuten-mcp](https://github.com/mrslbt/rakuten-mcp)** — Rakuten API integration for product search, hotel and travel booking, and recipe lookup across Japan's largest e-commerce platform. Install via npx rakuten-mcp
  <sub>★ 5 · TypeScript · MIT · npm · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g rakuten-mcp`</sub>
- **[ilyautov/moysklad-mcp-ru](https://github.com/ilyautov/moysklad-mcp-ru)** — MoySklad cloud ERP for Russian retail and wholesale: stock, products, orders, counterparties and profit/turnover/cash reports, plus document writes (supplies, shipments, invoices, returns) over the JSON API 1.2. 892 schema-driven methods reached through 8 generic meta-tools, kopecks converted to rubles, and a read/write/destructive safety gate that needs an explicit confirmation before a document
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx moysklad-mcp-ru`</sub>
- **[jasp-nerd/marktplaats-mcp](https://github.com/jasp-nerd/marktplaats-mcp)** — Search Marktplaats.nl and 2dehands.be, the Dutch and Belgian second-hand marketplaces. Listings with price, condition and distance filters, full ad details, seller verification and reviews, categories, and new-listing monitoring. No account or API key needed. Install via uvx marktplaats-mcp
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login`</sub>
- **[samrothschild23/intelligence-api](https://github.com/samrothschild23/intelligence-api)** — E-commerce and business intelligence MCP server. Analyze any Shopify store, research Amazon products with Opportunity Score and FBA profitability estimates, and find qualified sales leads from Google Maps with Lead Quality Scoring. Pay-per-call via x402 (USDC on Base)
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/samrothschild23/intelligence-api.git`</sub>
- **[the402ai/mcp-server](https://github.com/the402ai/mcp-server)** — AI agent service marketplace with x402 micropayments (USDC on Base). 30 tools for browsing services, purchasing, managing conversation threads, listing services as a provider, handling subscriptions, and tracking earnings. Install via npx -y @the402/mcp-server
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/the402ai/mcp-server.git`</sub>
- **[slookisen/lokal](https://github.com/slookisen/lokal)** — Search and discover 1,400+ verified local food producers in Norway — farms, REKO rings, farmers' markets, and farm shops. Natural-language search (NO/EN), geo-filtered discovery, and A2A protocol support, backed by rettfrabonden.com. Install via npx lokal-mcp
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/slookisen/lokal.git`</sub>
- **[wppoland/woocommerce-mcp](https://github.com/wppoland/woocommerce-mcp)** — Read-only MCP server for WordPress + WooCommerce. Five tools over the existing WP/WooCommerce REST APIs: list/search products, product details, recent orders, sales reports (week/month/last_month/year), and public blog-post search. No writes, no store-side plugin to install. Built by WPPoland. Install: git clone + npm run build
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @wppoland/woocommerce-mcp`</sub>
- **[ztemerbekov/a1-yandex-kit-skills](https://github.com/ztemerbekov/a1-yandex-kit-skills)** — Yandex KIT (Яндекс KIT) e-commerce platform — manage products and variants, prices, orders, discounts, promo codes, collections, warehouses and webhooks. 61 curated tools plus a kit_request escape hatch covering all 133 API operations
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add ztemerbekov/a1-yandex-kit-skills -y`</sub>
- **[ilyautov/chestny-znak-mcp-ru](https://github.com/ilyautov/chestny-znak-mcp-ru)** — Chestny ZNAK (Russian mandatory product marking, GIS MT and SUZ) API for AI assistants: marking codes, emission orders, circulation documents and code checks through 33 schema-driven methods with a read/write/destructive safety gate. PyPI (uvx chestny-znak-mcp-ru)
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx chestny-znak-mcp-ru`</sub>
- **[agentlux/agentlux-mcp](https://github.com/agentlux/agentlux-mcp)** — Agent marketplace and services MCP server for AgentLux. Browse marketplace items, manage agent identity, creator workflows, service hires, social flows, and Base/x402 commerce through 33 tools. Install via npx -y @agentlux/mcp-server
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @agentlux/mcp-server`</sub>
- **[anhmtk/agentshare-mcp](https://github.com/anhmtk/agentshare-mcp)** — Solana DeFi intelligence MCP (Meteora DLMM meteora_brief + meteora_pool_detail, Solana DEX + DefiLlama scout). Commerce tools are secondary. Hosted at https://agentshare.dev/mcp
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anhmtk/agentshare-mcp.git`</sub>
- **[malinoto/tracepass-mcp-server](https://github.com/malinoto/tracepass-mcp-server)** — EU Digital Product Passport automation for AI agents. Create products, build and audit DPPs (battery, electronics, textiles, and more), set economic-operator parties, and read or capture GS1 EPCIS 2.0 supply-chain events via the TracePass platform. 6 tools, hosted (https://ai.tracepass.eu/mcp) or local. Install via npx -y tracepass-mcp-server
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/malinoto/tracepass-mcp-server.git`</sub>
- **[melbis/melbis-shop](https://github.com/melbis/melbis-shop)** — Official MCP server of Melbis Shop, a self-hosted e-commerce platform: an AI agent works in the store as an employee — project files with version history, database, catalogue trees, product files, storefront pages — under a staff login with per-command permissions. Ships with the Windows client (6.5.1 beta)
  <sub>★ 1 · PHP · source · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/melbis/melbis-shop.git`</sub>
- **[ncosic/logimu-shopping-mcp](https://github.com/ncosic/logimu-shopping-mcp)** — Real Amazon (US, UK, DE, CA, AU) and Walmart shopping data for AI assistants — ranked product shortlists, current prices, live stock, real ratings, and 30-day price/BSR history from a 17M+ product warehouse. Free hosted endpoint, no signup (30 queries/day). Remote streamable-http at api.logimu.com/mcp
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ncosic/logimu-shopping-mcp.git`</sub>
- **[OFODevelopment/cerebrochain-mcp-server](https://github.com/CerebroChain/cerebrochain-mcp-server)** — Supply chain &amp; logistics intelligence — rate shopping across 85+ carriers, inventory management, order tracking, fleet logistics, and AI-powered demand forecasting. 20 tools and 3 resources for warehouse and supply chain operations
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @cerebrochain/mcp-server`</sub>
- **[ONE8943/ai-furniture-hub](https://github.com/ONE8943/ai-furniture-hub)** — Japan-focused furniture &amp; home product hub for AI agents. 15 tools for mm-precision search across 300+ products and 31 categories, curated sets (bundles, room presets, influencer picks), dimension-compatible replacement finder with fit_score, AI visibility diagnosis, Rakuten live API, and OpenAPI 3.1 schema. Install via npx ai-furniture-hub
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ai-furniture-hub`</sub>
- **[patchistry/patchistry-mcp-server](https://github.com/patchistry/patchistry-mcp-server)** — Official MCP server for Patchistry, the first DTC fashion brand listed in the official MCP Registry. AI agent commerce tools for the velcro-patch hat system: list_canvases, list_patches, recommend_build, get_shipping, and contact. Helps ChatGPT, Claude, Cursor, and Perplexity recommend complete hat + patch builds when shoppers ask about custom hats, bachelorette gifts, dad gifts, or 4th of July dr
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/patchistry/patchistry-mcp-server.git`</sub>
- **[Pangolin-spg/amazon-data-mcp](https://github.com/Pangolin-spg/amazon-data-mcp)** — Official read-only Amazon research MCP server maintained by Pangolinfo. Query product details, keyword results, reviews, niche signals, Alexa shopping recommendations, and AI-search data through MCP-compatible clients. Supports remote Streamable HTTP and local npm/Docker installation; users bring their own Pangolinfo API key
  <sub>★ 1 · TypeScript · MIT · docker · pushed 2026-09-02 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i -e PANGOLINFO_API_KEY pangolinfo-amazon-data-mcp`</sub>
- **[vitrine3d/mcp](https://github.com/vitrine3d/mcp)** — 3D product viewer platform with a visual editor. Upload GLB models, style scenes with lighting, camera, and backgrounds, and embed on any website. npx @vitrine3d/mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-05-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @vitrine3d/mcp --http # default port 3000`</sub>
- **[pepabo/colormeshop-mcp](https://github.com/pepabo/colormeshop-mcp)** — Official remote MCP server for Color Me Shop (GMO Pepabo), a Japanese e-commerce platform. Manage orders, products, inventory, customers, coupons, and shop settings via natural language
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pepabo/colormeshop-mcp.git`</sub>
- **[tokenofesteem/mcp](https://github.com/tokenofesteem/mcp)** — An agent can commission a funny, personalized printed booklet and have it printed and mailed as a gift, including a surprise for its own user. Pay with an account token, or tokenless with a single-use Stripe payment over HTTP 402. Remote MCP, US shipping, $19.99
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tokenofesteem/mcp.git`</sub>
- **[A1-x-Tech/mcp-yandex-merchants](https://github.com/A1-x-Tech/mcp-yandex-merchants)** — Yandex Merchants (Яндекс Товары) API — product feeds, offer prices, discounts, and hiding/unhiding offers in Yandex Search
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yandex-merchants@latest`</sub>
- **[A1-x-Tech/mcp-yango-retail](https://github.com/A1-x-Tech/mcp-yango-retail)** — Yango Tech Retail (grocery platform) B2B API — orders, receipts, products, prices, discounts, stocks and stores
  <sub>TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-yango-retail@latest`</sub>
- **[koraynar/trendyol-seller-mcp](https://github.com/koraynar/trendyol-seller-mcp)** — Unofficial Trendyol Marketplace seller API server: products, order packages, customer questions, claims, plus stock/price updates and answering questions. Write operations are env-gated and customer PII is redacted by default
  <sub>Python · MIT · clone · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/koraynar/trendyol-seller-mcp`</sub>
- **[RPER2001/rigshare-mcp](https://github.com/RPER2001/rigshare-mcp)** — Rent GPUs, robots, drones, and construction equipment on RIGShare, and onboard equipment owners; agents can quote, book, run remote sessions, and publish listings
  <sub>TypeScript · MIT · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y rigshare-mcp`</sub>
- **[hypawave/mcp](https://github.com/hypawave/mcp)** — Non-custodial Bitcoin Lightning commerce for agents: browse a public offer marketplace, buy and sell files, data, APIs and compute where verified settlement proof releases the content, plus free ECIES-encrypted agent-to-agent messaging and file handoffs in private waves. No accounts — agents authenticate with a secp256k1 keypair. npx -y @hypawave/mcp
  <sub>TypeScript · MIT-0 · npx · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @hypawave/mcp inbox # plain text (Claude Code, Codex)`</sub>
- **[laundromatic/shopgraph](https://github.com/laundromatic/shopgraph)** — Structured product data from the open web — Schema.org + AI extraction for e-commerce enrichment. Pay per call via Stripe. shopgraph.dev
  <sub>unavailable</sub>
- **[lofder/dsers-mcp-product](https://github.com/lofder/dsers-mcp-product)** — Automate AliExpress/Alibaba dropshipping product import to Shopify or Wix via DSers. Bulk import, variant editing, pricing rules, and multi-store push with a single command
  <sub>unavailable</sub>
- **[TheBestCo/bestprice-mcp](https://github.com/TheBestCo/bestprice-mcp)** — Read-only Greek price comparison: product search, offer comparison, and price history. Public streamable HTTP MCP at https://mcp.bestprice.gr/mcp, no API key
  <sub>JavaScript · Apache-2.0 · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/TheBestCo/bestprice-mcp.git`</sub>
- **[cmcgrabby-hue/syndicate-links](https://github.com/cmcgrabby-hue/syndicate-links/tree/master/mcp)** — Affiliate commission infrastructure for AI agents. 7 tools for program discovery, attribution tracking, commission status, and payouts. Search programs, get details, track conversions with signed attribution tokens, and trigger settlement cycles. Install via npx syndicate-links-mcp
  <sub>in-repo</sub>
  <sub>`git clone https://github.com/cmcgrabby-hue/syndicate-links.git && cd syndicate-links/mcp`</sub>
- **[ncosic/webotee-mcp](https://github.com/ncosic/webotee-mcp)** — Hosted Amazon market-intelligence MCP for Claude, ChatGPT, and other clients (Webotee AI Connect). Query brands, sellers, ASINs, under-competed niches, the cross-seller operator network, observed buy-box history, and Amazon/Walmart cross-marketplace overlap from a pre-collected research dataset. 76 read-only research tools at the remote endpoint https://app.webotee.com/mcp (paid plan, 7-day free t
  <sub>Python · source · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ncosic/webotee-mcp.git`</sub>
- **[dearlordylord/voila-sdk](https://github.com/dearlordylord/voila-sdk)** — Personal Voila grocery automation via MCP. Search products, inspect discounts, list delivery slots, read cart and order history, and update cart quantities
  <sub>TypeScript · MIT · npx · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @firfi/voila-mcp`</sub>

## Legal

- **[open-agreements/open-agreements](https://github.com/open-agreements/open-agreements)** — Fill standard legal agreement templates (NDAs, SAFEs, NVCA docs, employment, cloud terms) and produce signable DOCX files
  <sub>★ 58 · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g open-agreements`</sub>
- **[JamesANZ/us-legal-mcp](https://github.com/JamesANZ/us-legal-mcp)** — An MCP server that provides comprehensive US legislation
  <sub>★ 38 · TypeScript · MIT · npm · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g us-legal-mcp`</sub>
- **[librejustice/librejustice](https://github.com/librejustice/librejustice)** — French and European case law (Conseil d'État, Cour de cassation, courts of appeal, first-instance courts, Conseil constitutionnel, CNDA, ECHR, CJEU), linked article by article to consolidated legal texts as they stood on any date: codes, statutes, the Journal officiel, EU law and treaties. ~3.8M decisions and ~3.7M articles in one database, refreshed daily, hybrid lexical and semantic search. Host
  <sub>★ 29 · Rust · Apache-2.0 · npx · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add librejustice/librejustice`</sub>
- **[philrox/ris-mcp-ts](https://github.com/Honeyfield-Org/ris-mcp-ts)** — Access Austrian federal laws, state laws, court decisions, and legal documents via the RIS (Rechtsinformationssystem) API with 12 specialized tools
  <sub>★ 18 · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pnpm add -g ris-mcp-ts`</sub>
- **[ark-forge/mcp-eu-ai-act](https://github.com/ark-forge/mcp-eu-ai-act)** — EU AI Act compliance scanner that detects regulatory violations in AI codebases with risk classification and remediation guidance
  <sub>★ 11 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install eu-ai-act-scanner # or: pip install mcp-eu-ai-act`</sub>
- **[smilemin07/korean-rnd-regs-mcp](https://github.com/smilemin07/korean-rnd-regs-mcp)** — Natural-language search and review of South Korea's national R&amp;D (research &amp; development) regulations (acts, decrees, and administrative rules), returning the current in-force provisions with citations, fetched live from the official national law database
  <sub>★ 11 · Python · Apache-2.0 · uv · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --refresh korean-rnd-regs-mcp --version`</sub>
- **[SFHAJJI/lex](https://github.com/SFHAJJI/lex)** — Point-in-time Luxembourg and EU law: what did this article say on this date. Ten read-only tools for search, as-of retrieval, article history, diff, timeline, citations, provenance and coverage over the official Legilux and EUR-Lex texts, with publisher permalinks and content hashes on every answer. Remote server at law.soufien.lu/mcp
  <sub>★ 9 · C# · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SFHAJJI/lex.git`</sub>
- **[buildsyncinc/gibs-mcp](https://github.com/gibbrdev/gibs-mcp)** — Regulatory compliance (AI Act, GDPR, DORA) with article-level citations
  <sub>★ 7 · source · pushed 2026-02-15</sub>
  <sub>`git clone https://github.com/buildsyncinc/gibs-mcp.git`</sub>
- **[Vaquill-AI/canlii-mcp](https://github.com/Vaquill-AI/canlii-mcp)** — Canadian case law and legislation metadata via CanLII. Bring-your-own free CanLII API key. Hosted endpoint at canlii-mcp.vaquill.ai. MIT
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx wrangler secret put CANLII_API`</sub>
- **[ilyautov/sbis-mcp-ru](https://github.com/ilyautov/sbis-mcp-ru)** — SBIS (Saby) API for AI assistants: documents and their workflow stages, electronic signature, certificates, employees and organizations through 45 schema-driven methods with a read/write/destructive safety gate. PyPI (uvx sbis-mcp-ru)
  <sub>★ 4 · Python · MIT · uv · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx sbis-mcp-ru`</sub>
- **[Lex-API/lexapi-mcp](https://github.com/Lex-API/lexapi-mcp)** — EU legal research over EUR-Lex — 10 tools for structured search, CELEX/URL document fetch, recent Official Journal publications, inbound/outbound citation graph, and semantic search over case law + legislation. FREE tier available; semantic tools require a paid plan. Install: npx -y @lexapi/mcp
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @lexapi/mcp`</sub>
- **[atomno-mcp/mcp-sudact](https://github.com/atomno-mcp/mcp-sudact)** — Russian court practice (Sudact): case search by article, court, instance and dates; full decision text
  <sub>★ 2 · Python · MIT · pipx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install atomno-mcp-sudact`</sub>
- **[atomno-mcp/mcp-zakupki](https://github.com/atomno-mcp/mcp-zakupki)** — Russian public procurement (zakupki.gov.ru) tenders and contract search
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx atomno-mcp-zakupki --help`</sub>
- **[aydincan/turk-hukuku-mevzuat-mcp](https://github.com/aydincan/turk-hukuku-mevzuat-mcp)** — Turkish legislation live from the official source (mevzuat.gov.tr): current article text by law and article number, with verification links. Install: uvx turk-hukuku-mevzuat-mcp
  <sub>★ 2 · Python · MIT · pip · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install turk-hukuku-mevzuat-mcp`</sub>
- **[ChangkeunJ/australian-law-mcp](https://github.com/ChangkeunJ/australian-law-mcp)** — Australian Commonwealth law from the Federal Register of Legislation: read an act as it stood on any date back to 1901, compare two dates, and verify statute citations against the register before relying on them. No API key, no sign-up. Install: npx -y australian-law-mcp. Official MCP Registry: io.github.ChangkeunJ/australian-law-mcp
  <sub>★ 2 · TypeScript · MIT · docker · pushed 2026-09-12 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm australian-law-mcp`</sub>
- **[djtellado/nexus-legal-mcp](https://github.com/djtellado/nexus-legal-mcp)** — Multi-jurisdictional legal analysis (ISO 31000) for Spanish, Latin American and European law. 11 tools: analyze, draft, audit, monte_carlo, doctrina (DGT/TEAC), jurisprudencia (CENDOJ ~141k + Colombian CC/CSJ/CE ~106k), opinion, redteam, cross_border_compare, consulta. Install: npx -y @nexus-legal/mcp with API key from https://nexusquantum.legal/developers
  <sub>★ 2 · TypeScript · Apache-2.0 · source · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/djtellado/nexus-legal-mcp.git`</sub>
- **[smythmyke/patent-search-mcp-server](https://github.com/smythmyke/patent-search-mcp-server)** — Patent intelligence and prior-art research for the AI Patent Search Generator. Eleven tools: full patent dossier (bibliography, claims, citations, family, classifications, examiner stats); USPTO prosecution-history file wrappers; AI Office Action analysis (rejection grounds, cited prior art, suggested response arguments); Boolean query generator; multi-strategy patent search (telescoping / onion-r
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/smythmyke/patent-search-mcp-server.git`</sub>
- **[ad0750/regintel-mcp](https://github.com/regintelapi/regintel-mcp)** — MCP server for the RegIntel API: structured regulatory data across 41 jurisdictions and 212 regulations (GDPR, MiCA, DORA, SEC, FINRA, FCA, APRA, ASIC, MAS). Tools for search, lookup, recent updates, and compliance checks
  <sub>★ 1 · Python · MIT · uv · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx regintel-mcp # or: pip install regintel-mcp`</sub>
- **[Angelthebestone/Normativa-colombiana-MCP](https://github.com/Angelthebestone/Normativa-colombiana-MCP)** — Colombian law and jurisprudence: Gestor Normativo (laws, decrees, resolutions), Corte Constitucional (49,000+ rulings), SUIN-Juriscol with validity status, Corte Suprema de Justicia, Consejo de Estado, and DIAN Normograma (tax, customs, forex). Install: npx -y normativa-colombia-mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g normativa-colombia-mcp`</sub>
- **[cm2489/oravan](https://github.com/cm2489/oravan)** — Nonpartisan U.S. Congress data: plain-language bill decodes (bilingual EN/ES), representative lookup by ZIP with district-office phone numbers, and what’s-moving urgency ranking. Read-only, keyless, no accounts. Remote server at oravan.org/api/mcp/mcp, listed in the MCP registry as org.oravan/mcp
  <sub>★ 1 · TypeScript · AGPL-3.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cm2489/oravan.git`</sub>
- **[edithatogo/fyi-cli](https://github.com/edithatogo/fyi-cli)** — Multi-jurisdiction Freedom of Information / Official Information request tracker (fyi-mcp) for Alaveteli platforms (FYI.org.nz, WhatDoTheyKnow, RightToKnow, and more). Local SQLite storage with tools for requests, authorities, correspondence, offline sync, and health checks. Official MCP Registry: io.github.edithatogo/fyi-mcp
  <sub>★ 1 · Python · MIT · cargo · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install --path crates/fyi-cli`</sub>
- **[forgemeshlabs/gov-transparency-mcp](https://github.com/forgemeshlabs/gov-transparency-mcp)** — Watch the watchers: congressional stock trades, federal contracts, campaign finance, lobbying, and new regulations as nine MCP tools over official US government data, paid per call with x402 USDC on Base — no account or API key. npx -y @forgemeshlabs/gov-transparency-mcp
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/forgemeshlabs/gov-transparency-mcp.git`</sub>
- **[gavelin-ai/mcp](https://github.com/gavelin-ai/mcp)** — State legislative intelligence for AI agents. Speaker-attributed hearing transcripts, bills, votes, and AI-generated reports from US state legislatures. Remote server at mcp.gavelin.ai/mcp
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gavelin-ai/mcp.git`</sub>
- **[NexusFeed/nexusfeed-mcp](https://github.com/NexusFeed/nexusfeed-mcp)** — US state ABC liquor license compliance lookup (CA, TX, NY, FL) — search by trade name, owner, or license number and verify status, expiration, and address against state portals. Every response includes a verifiability block with extraction confidence and source URL
  <sub>★ 1 · Python · MIT · uv · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx nexusfeed-mcp`</sub>
- **[Patent-PreCheck/patent-precheck-mcp](https://github.com/Patent-PreCheck/patent-precheck-mcp)** — Patentability pre-check for code — USPTO statutory pillar scores (§101 eligibility, §102 novelty, §103 non-obviousness, §112 documentation), filing-readiness, and prior-art signals. No API keys; runs as a CLI or MCP server. Tools: precheck_score, precheck_pillars, precheck_start_review. Install: npx -y @patentprecheck/mcp
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @patentprecheck/mcp`</sub>
- **[ilyautov/diadoc-mcp-ru](https://github.com/ilyautov/diadoc-mcp-ru)** — Kontur Diadoc API for AI assistants: legally significant document exchange, signing, counteragents, machine-readable powers of attorney and docflow status through 114 schema-driven methods with a read/write/destructive safety gate. PyPI (uvx diadoc-mcp-ru)
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx diadoc-mcp-ru`</sub>
- **[atomno-mcp/mcp-fssp](https://github.com/atomno-mcp/mcp-fssp)** — FSSP enforcement proceedings lookup for Russian debtors and compliance checks
  <sub>Python · MIT · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx atomno-mcp-fssp`</sub>
- **[conformi-eu/conformi-search-mcp](https://github.com/conformi-eu/conformi-search-mcp)** — EU legal research with verifiable CELEX citations from the EUR-Lex corpus (DE/EN/FR). Semantic search, knowledge reports and application-date timelines for GDPR, AI Act, NIS2, DORA and more. Remote server at conformi.eu/api/mcp, listed in the MCP registry as eu.conformi/conformi-search
  <sub>unavailable</sub>
- **[CSOAI-ORG/eu-ai-act-compliance-mcp](https://github.com/CSOAI-ORG/eu-ai-act-compliance-mcp)** — EU AI Act measurement corpus — 417 frozen provisions (the Act's 113 Articles at provision-level granularity) with risk classification, a 42-point audit, Article 11 documentation drafts, and a penalty calculator. Measurement, not certification. Install: pip install eu_ai_act_compliance_mcp
  <sub>unavailable</sub>
- **[lmaniraruta/license-verify-mcp](https://github.com/lmaniraruta/license-verify-mcp)** — Verify a US contractor's license, surety bond, and insurance from official state data (WA L&amp;I live, CA CSLB beta). Agent-payable pay-per-success, MCP-native
  <sub>TypeScript · MIT · npx · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx apify run`</sub>
- **[meridian-silkdev/meridian-mcp](https://github.com/meridian-silkdev/meridian-mcp)** — Toolbox for startups and founders: browse services, create/track service requests, verify payments (Flouci Tunisia / Stripe international), and schedule meetings for company incorporation, visas, and other founder-related business services. Listed in the official MCP Registry as io.github.meridian-silkdev/meridian-mcp. Install: npx -y @meridiantoolkit/mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @meridiantoolkit/mcp`</sub>
- **[Pactlio-ai/pactlio-mcp](https://github.com/Pactlio-ai/pactlio-mcp)** — Contract tools for AI agents: statute-cited requirements per contract type × US state/country, non-compete enforceability for all 50 states + DC, intake schemas, async multi-agent contract drafting with free previews, and contract risk analysis. Anonymous remote server at www.pactlio.com/api/mcp, listed as a hosted connector on Glama
  <sub>JavaScript · MIT · source · pushed 2026-08-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Pactlio-ai/pactlio-mcp.git`</sub>
- **[PolicyForge/mcp](https://github.com/PolicyForge/mcp)** — Generate, audit and maintain legal policies from your codebase — privacy policies, terms of service, cookie policies, EULAs, refund policies and disclaimers, each hosted at a permanent URL. Audits the gap between what the code actually does and what the policy claims, and detects drift when the stack changes. 15 tools. Remote Streamable HTTP at policyforge.co/api/mcp with OAuth, or npx -y @policyf
  <sub>TypeScript · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PolicyForge/mcp.git`</sub>
- **[ptrinh/finalnotice-mcp](https://github.com/ptrinh/finalnotice-mcp)** — Generate localized debt-collection demand-letter PDFs (formal letter + matching envelope) across 100+ jurisdictions and 33 languages. No auth, no key — tools: list_jurisdictions, preview_demand_letter, generate_demand_letter. Hosted Streamable HTTP at finalnotice.io/mcp
  <sub>JavaScript · MIT · docker · pushed 2026-07-06 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm finalnotice-mcp`</sub>
- **[sebastianfoerste/eu-reg-mcp](https://github.com/sebastianfoerste/eu-reg-mcp)** — ESMA MiCAR register grounding for agents: entity/LEI search, register summary, and change tracking including removals, with weekly snapshots of the public register. Optional deterministic MiCAR white paper linting (Annex I-III, cited candidate findings) and EU AI Act risk-tier classification with pinpoint citations. Register tools need no API key; findings are review-gated. MIT
  <sub>Python · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sebastianfoerste/eu-reg-mcp`</sub>

## Real Estate

- **[HasData/redfin-mcp](https://github.com/HasData/redfin-mcp)** — Remote MCP server for Redfin: for-sale, for-rent and sold listings with the full filter set, plus complete property pages, as JSON
  <sub>★ 10 · JavaScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/redfin-mcp.git`</sub>
- **[HasData/zillow-mcp](https://github.com/HasData/zillow-mcp)** — Remote MCP server for Zillow: for-sale, for-rent and sold listings with rich filters, and full property details (price and tax history, schools, agent), as JSON
  <sub>★ 10 · JavaScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/HasData/zillow-mcp.git`</sub>
- **[ashev87/propstack-mcp](https://github.com/ashev87/propstack-mcp)** — Propstack CRM MCP: search contacts, manage properties, track deals, schedule viewings for real estate agents (Makler)
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y propstack-mcp-server`</sub>
- **[jbechtel-97/dealflowpro-mcp-server](https://github.com/jbechtel-97/dealflowpro-mcp-server)** — Multifamily real estate deal analysis — cap rate, DSCR, cash-on-cash, IRR, DFP Score (0-100), max offer price, and market intelligence for 2-200 unit properties
  <sub>★ 3 · JavaScript · MIT · source · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jbechtel-97/dealflowpro-mcp-server.git`</sub>
- **[Capital-W-Holdings/us-property-parcel-real-estate-debt](https://github.com/Capital-W-Holdings/us-property-parcel-real-estate-debt)** — US commercial and federal-programme real estate debt: loan maturities across 52 state codes, HUD subsidy contract expiries and LIHTC compliance period endings nationally, plus 291,914 Massachusetts and New York parcels with ownership and assessed value, and 95,494 recorded sale instruments. Hosted remote MCP over Streamable HTTP, no key and no signup; 11 of 12 tools free and permanent, one $1.00 l
  <sub>★ 2 · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Capital-W-Holdings/us-property-parcel-real-estate-debt.git`</sub>
- **[forgemeshlabs/disruption-intelligence-mcp](https://github.com/forgemeshlabs/disruption-intelligence-mcp)** — AI-native commercial disruption intelligence for MCP clients and x402-powered agents. Supports WARN/layoff intelligence, company context, geospatial territory disruption, and x402 payment challenge inspection via the hosted Forgemesh API
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @forgemeshlabs/disruption-intelligence-mcp`</sub>
- **[pedra-ai/pedra-mcp](https://github.com/pedra-ai/pedra-mcp)** — AI photo and video editing for real-estate listings via the Pedra API: virtual staging, renovation, room emptying, photo enhancement, sky replacement, object removal/blur, and property video generation. npx @pedra-ai/mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @pedra-ai/mcp`</sub>
- **[atifnayeem-oss/saveproptax-mcp](https://github.com/atifnayeem-oss/saveproptax-mcp)** — California property tax appeals: check whether a home qualifies for a Proposition 8 decline-in-value reduction from recent comparable sales, then prepare the county's own review form. Hosted remote server at https://saveproptax.com/mcp, no API key. The signing link is emailed to the homeowner, who signs and pays a flat $29
  <sub>JavaScript · MIT · source · pushed 2026-08-19 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/atifnayeem-oss/saveproptax-mcp.git`</sub>
- **[beshogun/planwire-mcp](https://github.com/beshogun/planwire-mcp)** — UK planning application data for AI agents: search planning applications by council, postcode, keyword, status, type, or date range; find applications near a lat/lng point; fetch a specific application; and list supported councils. Requires a PlanWire API key. npx -y planwire-mcp
  <sub>TypeScript · npx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y planwire-mcp`</sub>
- **[hyperionxmota/cook-county-property-mcp](https://github.com/hyperionxmota/cook-county-property-mcp)** — Cook County / Chicago property records — parcels, recorded sales, building permits, tax assessments, and comparable sales by street address or PIN. Hosted remote MCP, pay-per-call via x402 (USDC on Base/Solana)
  <sub>Python · source · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hyperionxmota/cook-county-property-mcp.git`</sub>
- **[RantumBits/addressintel-mcp](https://github.com/RantumBits/addressintel-mcp)** — SF Peninsula (California) building permits and parcel buildability: search issued permits by city, keyword, contractor or valuation; SB 9 lot-split eligibility with per-parcel block reasons; ADU feasibility with estimated units and buildable square footage; and underbuilt-parcel redevelopment leads. Read-only, works keyless on a demo tier. npx -y addressintel-mcp
  <sub>JavaScript · MIT · clone · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/RantumBits/addressintel-mcp.git`</sub>
- **[TargetGrps/partelisto-mcp](https://github.com/TargetGrps/partelisto-mcp)** — #️⃣ ☁️ - Guest check-in and SES.HOSPEDAJES (Spanish short-term-rental police registration) for property operators: booking status, guest-form completion, SES filing status, create a booking, and resend a guest's check-in link. OAuth-scoped read/write, no guest PII exposed. Listed in the official MCP Registry as io.github.TargetGrps/partelisto-mcp
  <sub>C# · MIT · source · pushed 2026-09-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/TargetGrps/partelisto-mcp.git`</sub>
- **[zornade/zornade-mcp](https://github.com/zornade/zornade-mcp)** — Italian cadastral, geospatial and real-estate data for AI agents: geocoding on 18.7M+ addresses, parcel profiles for the whole Italian territory (risk, solar potential, valuations, POI), parcel lookup by point/bbox, and administrative lists. Requires a free Zornade API key. Remote: https://mcp.zornade.com/mcp, or self-host via Docker in the repo
  <sub>TypeScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zornade/zornade-mcp.git`</sub>

## Cryptography

- **[denismaggior8/enigma-python-mcp](https://github.com/denismaggior8/enigma-python-mcp)** — A Model Context Protocol server that brings the capabilities of enigmapython library to LLMs, allowing them to encrypt and decrypt messages using historically accurate Enigma machine emulators
  <sub>★ 5 · Python · uv · pushed 2026-07-31 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx enigmapython-mcp`</sub>
- **[degenlegion-com/waxseal-sdk](https://github.com/degenlegion-com/waxseal-sdk)** — On-chain Ed25519 identity for AI agents — verify seals by fingerprint, validate document signatures, and gate irreversible actions behind human-signed approval tokens. Hosted at api.waxseal.id/mcp; local install (npx @waxseal/mcp) for signing
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @waxseal/mcp`</sub>
- **[laszlopere/mcp-bytesmith](https://github.com/laszlopere/mcp-bytesmith)** — Local byte-wrangling toolbox: encoding (hex/Base64/Base32/Base58/Base45…), cryptographic + CRC hashing, base conversion, and CSPRNG tokens/passphrases, plus an opt-in Ethereum/EVM toolset (keccak, ABI/RLP codecs, EIP-191/712 hashing, function/event selectors, EIP-55). No network calls. uvx mcp-bytesmith
  <sub>★ 2 · Python · GPL-3.0 · source · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/laszlopere/mcp-bytesmith.git`</sub>
- **[ogasurfproject-jpg/horizon-shield](https://github.com/ogasurfproject-jpg/horizon-shield/tree/main/workers/hs-jidec-mcp)** — Bitcoin-anchored, trustless public verification ledger (JIDEC) for AI-agent evidence: fetch the record bytes, recompute the SHA-256, and check the OpenTimestamps/Bitcoin timestamp — no trust in the issuer required
  <sub>HTML · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/ogasurfproject-jpg/horizon-shield.git && cd horizon-shield/workers/hs-jidec-mcp`</sub>
- **[Fulcrum-Enterprises/verify-proof](https://github.com/Fulcrum-Enterprises/verify-proof)** — Verify blockchain-anchored timestamp proofs locally: recompute a file's SHA-256, walk the Merkle path, and check the anchor on Polygon or Bitcoin. Verification makes no network call and needs no account or API key, and never asks the issuing service whether its own proof is good; an optional tool anchors a new hash through ProofLedger. pip install "verify-proof[mcp]"
  <sub>Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install verify-proof`</sub>

## Aggregators

- **[mindsdb/mindsdb](https://github.com/mindsdb/mindshub)** — Connect and unify data across various platforms and databases with MindsDB as a single MCP server
  <sub>★ 39.8k · Makefile · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mindsdb/mindsdb.git`</sub>
- **[metatool-ai/metatool-app](https://github.com/metatool-ai/metamcp)** — MetaMCP is the one unified middleware MCP server that manages your MCP connections with GUI
  <sub>★ 2.7k · TypeScript · MIT · clone · pushed 2026-06-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/metatool-ai/metamcp.git`</sub>
- **[julien040/anyquery](https://github.com/julien040/anyquery)** — Query more than 40 apps with one binary using SQL. It can also connect to your PostgreSQL, MySQL, or SQLite compatible database. Local-first and private by design
  <sub>★ 1.8k · Go · winget · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install JulienCagniart.anyquery`</sub>
- **[duaraghav8/MCPJungle](https://github.com/mcpjungle/MCPJungle)** — Self-hosted MCP Server registry for enterprise AI Agents
  <sub>★ 1.3k · Go · MPL-2.0 · brew · pushed 2026-08-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install mcpjungle/mcpjungle/mcpjungle`</sub>
- **[opentabs-dev/opentabs](https://github.com/opentabs-dev/opentabs)** — Plugin-based MCP server + Chrome extension that gives AI agents access to web applications through the user's authenticated browser session. 100+ plugins with a plugin SDK for building new ones
  <sub>★ 956 · TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @opentabs-dev/cli`</sub>
- **[1mcp/agent](https://github.com/1mcp-app/agent)** — A unified Model Context Protocol server implementation that aggregates multiple MCP servers into one
  <sub>★ 507 · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @1mcp/agent`</sub>
- **[K-Dense-AI/claude-skills-mcp](https://github.com/K-Dense-AI/claude-skills-mcp)** — Intelligent search capabilities to let every model and client use Claude Agent Skills like native
  <sub>★ 405 · Python · Apache-2.0 · uv · pushed 2026-07-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx claude-skills-mcp`</sub>
- **[blockrunai/blockrun-mcp](https://github.com/BlockRunAI/blockrun-mcp)** — Access 30+ AI models (GPT-5, Claude, Gemini, Grok, DeepSeek) without API keys. Pay-per-use via x402 micropayments with USDC on Base
  <sub>★ 394 · TypeScript · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @blockrun/mcp@latest`</sub>
- **[smart-mcp-proxy/mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go)** — Local MCP proxy with BM25 tool filtering, quarantine security, activity logging, and web UI. Routes multiple servers through a single endpoint
  <sub>★ 379 · Go · MIT · go · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/smart-mcp-proxy/mcpproxy-go/cmd/mcpproxy@latest`</sub>
- **[wegotdocs/open-mcp](https://github.com/boltmcp/boltmcp)** — Turn a web API into an MCP server in 10 seconds and add it to the open source registry: https://open-mcp.org
  <sub>★ 371 · Shell · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/wegotdocs/open-mcp.git`</sub>
- **[HelpCode-ai/anythingmcp](https://github.com/HelpCode-ai/anythingmcp)** — Self-hosted source-available MCP gateway and API-to-MCP bridge. Converts REST, SOAP/WSDL, GraphQL, and SQL/NoSQL databases (PostgreSQL, MySQL, MariaDB, MSSQL, Oracle, MongoDB, SQLite) into MCP tools — no SDK, no code. Imports OpenAPI / Postman / WSDL / GraphQL specs; bridges multiple MCP servers behind one endpoint. Ships with 29 pre-built adapters (DHL, DATEV, Weclapp, Personio, Handelsregister,
  <sub>★ 322 · TypeScript · AGPL-3.0 · source · pushed 2026-09-22 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/HelpCode-ai/anythingmcp.git`</sub>
- **[tsouth89/toolport](https://github.com/btsouth/toolport)** — One local gateway and manager for all your MCP servers, shared across every AI coding tool (Claude, Cursor, VS Code, Codex, and more). Set up and authenticate each server once; lazy discovery keeps each agent's context small, and keys stay in your OS keychain. No Docker, no cloud
  <sub>★ 218 · Rust · MIT · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/tsouth89/toolport.git`</sub>
- **[activeing123/mcptoon](https://github.com/activeing123/mcptoon)** — Zero-dependency CLI that connects any AI agent to every MCP server: one config, synced to Claude Code, Cursor, Codex, Cline, Windsurf and VS Code. Tool discovery drops from 71,929 to 581 tokens across 255 tools (-99.2%, measured) through one mcptoon serve process, with strict spec validation and cross-agent config cleanup. pip install mcptoon
  <sub>★ 203 · HTML · Apache-2.0 · npx · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add https://github.com/activeing123/mcptoon --skill mcptoon`</sub>
- **[sxhxliang/mcp-access-point](https://github.com/sxhxliang/mcp-access-point)** — Turn a web service into an MCP server in one click without making any code changes
  <sub>★ 184 · Rust · MIT · docker · pushed 2026-03-11 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --name mcp-access-point --rm \`</sub>
- **[api7/aisix](https://github.com/api7/aisix)** — MCP gateway that registers upstream MCP servers and fronts them behind one governed Streamable HTTP endpoint (/mcp): per-tool access control by caller API key, guardrails over tool arguments and results, rate limits, and usage logs. The same self-hosted gateway also proxies LLM and A2A agent traffic
  <sub>★ 160 · Rust · Apache-2.0 · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --name aisix \`</sub>
- **[sitbon/magg](https://github.com/sitbon/magg)** — Magg: A meta-MCP server that acts as a universal hub, allowing LLMs to autonomously discover, install, and orchestrate multiple MCP servers - essentially giving AI assistants the power to extend their own capabilities on-demand
  <sub>★ 143 · Python · AGPL-3.0 · uv · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install magg`</sub>
- **[juspay/neurolink](https://github.com/juspay/neurolink)** — Making enterprise AI infrastructure universally accessible. Edge-first platform unifying 12 providers and 100+ models with multi-agent orchestration, HITL workflows, guardrails middleware, and context summarization
  <sub>★ 138 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @juspay/neurolink --help`</sub>
- **[VeriTeknik/pluggedin-mcp-proxy](https://github.com/VeriTeknik/pluggedin-mcp-proxy)** — A comprehensive proxy server that combines multiple MCP servers into a single interface with extensive visibility features. It provides discovery and management of tools, prompts, resources, and templates across servers, plus a playground for debugging when building MCP servers
  <sub>★ 135 · TypeScript · Apache-2.0 · npx · pushed 2026-05-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @pluggedin/pluggedin-mcp-proxy@latest --pluggedin-api-key YOUR_API_KEY`</sub>
- **[askbudi/roundtable](https://github.com/yylo-dev/roundtable)** — Meta-MCP server that unifies multiple AI coding assistants (Codex, Claude Code, Cursor, Gemini) through intelligent auto-discovery and standardized MCP interface, providing zero-configuration access to the entire AI coding ecosystem
  <sub>★ 125 · Python · npx · pushed 2025-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @roundtable/mcp-server`</sub>
- **[SureScaleAI/openai-gpt-image-mcp](https://github.com/SureScaleAI/openai-gpt-image-mcp)** — OpenAI GPT image generation/editing MCP server
  <sub>★ 111 · TypeScript · MIT · clone · pushed 2025-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SureScaleAI/openai-gpt-image-mcp.git`</sub>
- **[portel-dev/ncp](https://github.com/portel-dev/ncp)** — NCP orchestrates your entire MCP ecosystem through intelligent discovery, eliminating token overhead while maintaining 98.2% accuracy
  <sub>★ 99 · TypeScript · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @portel/ncp`</sub>
- **[Jovancoding/Network-AI](https://github.com/Jovancoding/Network-AI)** — Multi-agent orchestration MCP server with race-condition-safe shared blackboard. 20+ MCP tools: blackboard read/write, agent spawn/stop, FSM transitions, budget tracking, token management, and audit log query. npx network-ai-server --port 3001
  <sub>★ 76 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx network-ai-server --port 3001`</sub>
- **[MikkoParkkola/mcp-gateway](https://github.com/MikkoParkkola/mcp-gateway)** — Universal MCP gateway with single-port multiplexing and Meta-MCP. 4 meta-tools replace 100+ registrations, saving 95% context window. Hot-reloadable capabilities, OpenAPI auto-import, 42 starter capabilities (25 zero-config)
  <sub>★ 75 · Rust · cargo · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install mcp-gateway`</sub>
- **[hamflx/imagen3-mcp](https://github.com/hamflx/imagen3-mcp)** — A powerful image generation tool using Google's Imagen 3.0 API through MCP. Generate high-quality images from text prompts with advanced photography, artistic, and photorealistic controls
  <sub>★ 70 · Rust · source · pushed 2025-05-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/hamflx/imagen3-mcp.git`</sub>
- **[WayStation-ai/mcp](https://github.com/waystation-ai/mcp)** — Seamlessly and securely connect Claude Desktop and other MCP hosts to your favorite apps (Notion, Slack, Monday, Airtable, etc.). Takes less than 90 secs
  <sub>★ 63 · JavaScript · source · pushed 2025-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/waystation-ai/mcp.git`</sub>
- **[depwire/depwire](https://github.com/depwire/depwire)** — Dependency graph + 15 MCP tools for AI coding assistants. Parses TypeScript, JavaScript, Python, Go, Rust, and C. Arc diagram visualization, health scoring, dead code detection, and temporal graph
  <sub>★ 62 · TypeScript · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g depwire-cli`</sub>
- **[YangLiangwei/PersonalizationMCP](https://github.com/YangLiangwei/PersonalizationMCP)** — Comprehensive personal data aggregation MCP server with Steam, YouTube, Bilibili, Spotify, Reddit and other platforms integrations. Features OAuth2 authentication, automatic token management, and 90+ tools for gaming, music, video, and social platform data access
  <sub>★ 60 · Python · MIT · clone · pushed 2026-03-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/YangLiangwei/PersonalizationMCP.git`</sub>
- **[particlefuture/MCPDiscovery](https://github.com/particlefuture/1mcpserver)** — MCP of MCPs. Automatic discovery and configure MCP servers on your local machine
  <sub>★ 52 · Python · Apache-2.0 · npx · pushed 2025-12-31 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @1mcpserver/1mcpserver`</sub>
- **[merterbak/Grok-MCP](https://github.com/merterbak/Grok-MCP)** — MCP server for xAI's Grok API with agentic tool calling, image generation, vision, and file support
  <sub>★ 51 · Python · MIT · clone · pushed 2026-08-29 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/merterbak/Grok-MCP.git`</sub>
- **[profullstack/mcp-server](https://github.com/profullstack/mcp-server)** — A comprehensive MCP server aggregating 20+ tools including SEO optimization, document conversion, domain lookup, email validation, QR generation, weather data, social media posting, security scanning, and more developer utilities
  <sub>★ 45 · JavaScript · ISC · docker · pushed 2026-09-14 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 mcp-server`</sub>
- **[rhein1/agoragentic-integrations](https://github.com/rhein1/agoragentic-integrations)** — Agent-to-agent marketplace where AI agents discover, invoke, and pay for services from other agents using USDC on Base L2
  <sub>★ 39 · JavaScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agoragentic-harness-core@latest init`</sub>
- **[glenngillen/mcpmcp-server](https://github.com/glenngillen/mcpmcp-server)** — A list of MCP servers so you can ask your client which servers you can use to improve your daily workflow
  <sub>★ 38 · Apache-2.0 · source · pushed 2025-04-24 · macOS?</sub>
  <sub>`git clone https://github.com/glenngillen/mcpmcp-server.git`</sub>
- **[Rendeverance/toolfunnel](https://github.com/Rendeverance/toolfunnel)** — Zero-dependency gateway that funnels multiple MCP servers through one endpoint, with live attach/detach, tool filtering/gating and hiding, hot config reload, and an optional OAuth-protected HTTP transport
  <sub>★ 37 · JavaScript · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Rendeverance/toolfunnel.git`</sub>
- **[MikeyPetrillo/Agent402](https://github.com/MikeyPetrillo/Agent402)** — The headless browser, live web search, OCR, and durable wallet-keyed memory an agent's sandbox doesn't have - a catalog of 500+: 400+ pay-per-call tools + 100+ curated skill packs, every one tested, priced, and settled on-chain - rented per call via x402 (USDC on Base + 10 more chains (Solana, Polygon, Arbitrum, Monad, Celo, Avalanche, Sei, Optimism, Stellar, Algorand), or USDG on Robinhood Chain
  <sub>★ 34 · JavaScript · AGPL-3.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y agent402-mcp`</sub>
- **[mcccsm/x402-list-mcp](https://github.com/mcccsm/x402-list-mcp)** — Find and vet x402 payment APIs before your agent pays one: search and rank listed services, live uptime and health windows, per-endpoint USD pricing, and on-chain-verified facilitator settlement volume, over the public x402-list directory. Free REST API, no auth for reads. npx -y x402-list-mcp. Web: x402-list.com
  <sub>★ 27 · TypeScript · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y x402-list-mcp`</sub>
- **[Wolido/OpenAaaS](https://github.com/Wolido/OpenAaaS)** — Python MCP adapter connecting Claude/Cursor/Cline to the OpenAaaS scientific agent network. Submit tasks to remote research agents (literature analysis, materials databases, etc.) — data stays local, only KB~MB results flow. Install: uvx openaaas-mcp-adapter
  <sub>★ 26 · Rust · MIT · uv · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`uvx openaaas-mcp-adapter`</sub>
- **[tadas-github/a2asearch-mcp](https://github.com/tadas-github/a2asearch-mcp)** — MCP server to search 4,800+ MCP servers, AI agents, CLI tools and agent skills. Install: npx -y a2asearch-mcp. Ask Claude: "Find MCP servers for database access". Free, no auth required
  <sub>★ 21 · JavaScript · MIT · npm · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g a2asearch-mcp`</sub>
- **[Data-Everything/mcp-server-templates](https://github.com/Data-Everything/mcp-server-templates)** — One server. All tools. A unified MCP platform that connects many apps, tools, and services behind one powerful interface—ideal for local devs or production agents
  <sub>★ 21 · Python · pip · pushed 2025-08-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mcp-templates`</sub>
- **[gzoonet/cortex](https://github.com/gzoonet/cortex)** — Local-first knowledge graph for developers. Watches project files, extracts entities and relationships via LLMs, builds a queryable knowledge graph with web dashboard and CLI. Provides 4 MCP tools: get_status, list_projects, find_entity, query_cortex
  <sub>★ 21 · TypeScript · MIT · npm · pushed 2026-09-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @gzoo/cortex`</sub>
- **[ViperJuice/mcp-gateway](https://github.com/Consiliency/pmcp)** — A meta-server for minimal Claude Code tool bloat with progressive disclosure and dynamic server provisioning. Exposes 9 stable meta-tools, auto-starts Playwright and Context7, and can dynamically provision 25+ MCP servers on-demand from a curated manifest
  <sub>★ 20 · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ViperJuice/mcp-gateway.git`</sub>
- **[arikusi/deepseek-mcp-server](https://github.com/arikusi/deepseek-mcp-server)** — MCP server for DeepSeek AI with chat, reasoning, multi-turn sessions, function calling, thinking mode, and cost tracking
  <sub>★ 19 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @arikusi/deepseek-mcp-server`</sub>
- **[robhunter/agentdeals](https://github.com/robhunter/agentdeals)** — 1,500+ developer infrastructure deals, free tiers, and startup programs across 54 categories. Search deals, compare vendors, plan stacks, and track pricing changes. REST API and web browser at agentdeals.dev
  <sub>★ 18 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/robhunter/agentdeals.git`</sub>
- **[elisymlabs/elisym](https://github.com/elisymlabs/elisym)** — AI agent discovery and marketplace on Nostr with Solana payments (SOL, USDC). NIP-89 discovery, NIP-90 jobs, NIP-44 v2 encryption, on-chain micropayments
  <sub>★ 17 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @elisym/mcp init #Create an agent`</sub>
- **[isaac-levine/forage](https://github.com/isaac-levine/forage)** — Self-improving tool discovery for AI agents. Searches registries, installs MCP servers as subprocesses, and persists tool knowledge across sessions — no restarts needed
  <sub>★ 17 · TypeScript · MIT · npx · pushed 2026-02-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx forage-mcp init --client cursor`</sub>
- **[Continuum-AI-Corp/orcarouter-mcp-server](https://github.com/Continuum-AI-Corp/orcarouter-mcp-server)** — Browse 160+ LLM models (OpenAI, Anthropic, Google, Qwen, DeepSeek, …) with live pricing — no API key required for catalog tools. Routes chat completions through the OrcaRouter gateway with automatic fallback. npx -y @orcarouter/mcp
  <sub>★ 13 · TypeScript · MIT · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Continuum-AI-Corp/orcarouter-mcp-server.git`</sub>
- **[hashgraph-online/hashnet-mcp-js](https://github.com/hashgraph-online/hashnet-mcp-js)** — MCP server for the Registry Broker. Discover, register, and chat with AI agents on the Hashgraph network
  <sub>★ 13 · TypeScript · npx · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @hol-org/hashnet-mcp --help`</sub>
- **[Markgatcha/universal-mcp-toolkit](https://github.com/Markgatcha/universal-mcp-toolkit)** — A universal MCP aggregator toolkit that connects AI agents to multiple MCP servers through a single unified configuration. Features ready-made templates, cross-repo prompt workflows, and an npm package for zero-config installation.universal MCP aggregator toolkit that connects AI agents to multiple MCP servers through a single unified configuration. Features ready-made templates, cross-repo prompt
  <sub>★ 13 · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g universal-mcp-toolkit`</sub>
- **[withoneai/mcp](https://github.com/withoneai/mcp)** — Search, document and execute authenticated API calls across all your apps (Gmail, Slack, Stripe, Notion, GitHub, and more) through 4 universal tools whose context footprint stays constant no matter how many connections you add. Hosted remote server with OAuth at https://mcp.withone.ai/mcp, or run locally via npx @withone/mcp. By One
  <sub>★ 11 · TypeScript · MIT · npx · pushed 2026-09-16 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @withone/mcp`</sub>
- **[Work90210/APIFold](https://github.com/Work90210/APIFold)** — Turn any REST API into a hosted MCP server. 18 free public servers (GitHub, Stripe, Slack, OpenAI, Notion, and more) — no setup required, bring your own API key
  <sub>★ 10 · TypeScript · AGPL-3.0 · npm · pushed 2026-06-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @apifold/cli`</sub>
- **[whiteknightonhorse/APIbase](https://github.com/whiteknightonhorse/APIbase)** — Unified API hub for AI agents with 56+ tools across travel (Amadeus, Sabre), prediction markets (Polymarket), crypto, and weather. Pay-per-call via x402 micropayments in USDC
  <sub>★ 10 · TypeScript · MIT · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/whiteknightonhorse/APIbase.git`</sub>
- **[2s-io/sdk](https://github.com/2s-io/sdk)** — Unified API for AI agents — 180+ tools across geocoding, weather (NWS), climate stations (NOAA), earthquakes (USGS), tides (NOAA), points of interest (OpenStreetMap), patents (USPTO ODP), US case law (CourtListener / Free Law Project), Federal Register, Wikipedia, scientific papers (arXiv / PubMed / Semantic Scholar), AI summarize / translate / extract / screenshot / image-describe, image compress
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @2sio/mcp --trial # MCP host with free trial calls`</sub>
- **[gzchenhao/openhire](https://github.com/gzchenhao/openhire)** — Agent-native job search over employer ATS APIs (Greenhouse, Lever, Ashby, Beisen) — 125 companies and ~15k live postings with freshness verification, ghost-job scoring and deep-link apply channels. Résumés never transit the server; matching runs client-side
  <sub>★ 7 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx openhire@latest serve`</sub>
- **[aidevelopers2/remoteopenclaw-mcp](https://github.com/aidevelopers2/remoteopenclaw-mcp)** — MCP server and CLI to search the Remote OpenClaw directory of 13,870+ MCP servers, 4,384+ agent skills, and plugins. Returns names, links, and install commands. Install: claude mcp add remoteopenclaw -- npx -y remoteopenclaw. CLI: npx remoteopenclaw search . Free, no API key
  <sub>★ 6 · JavaScript · MIT · source · pushed 2026-07-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aidevelopers2/remoteopenclaw-mcp.git`</sub>
- **[alexanderclapp/clirank-mcp-server](https://github.com/alexanderclapp/clirank-mcp-server)** — API intelligence for AI coding agents. 387 APIs scored on agent-friendliness with tools to recommend, compare, check scores, and discover APIs. Install: npx clirank-mcp-server. Web: clirank.dev
  <sub>★ 6 · JavaScript · MIT · npx · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y clirank-mcp-server@latest`</sub>
- **[carlosahumada89/govrider-mcp-server](https://github.com/carlosahumada89/govrider-mcp-server)** — Match your tech product or consulting service to thousands of live government tenders, RFPs, grants, and frameworks from 25+ official sources worldwide
  <sub>★ 6 · TypeScript · MIT · clone · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/carlosahumada89/govrider-mcp-server.git`</sub>
- **[khalidsaidi/ragmap](https://github.com/khalidsaidi/ragmap)** — MapRag: RAG-focused subregistry + MCP server to discover and route to retrieval-capable MCP servers using structured constraints and explainable ranking
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @khalidsaidi/ragmap-mcp@latest`</sub>
- **[mroops0111/openapi-mcp-gateway](https://github.com/mroops0111/openapi-mcp-gateway)** — Mount many OpenAPI specs (or your existing FastAPI app) as MCP servers in one process. Auto-promotes eligible GETs to MCP resources, exposes huge specs via three list/get/call meta-tools instead of N tool schemas, and ships per-user OAuth2 token relay with audience-bound tokens
  <sub>★ 6 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx openapi-mcp-gateway --spec https://petstore3.swagger.io/api/v3/openapi.json`</sub>
- **[nimbus-agent/Nimbus](https://github.com/nimbus-agent/Nimbus)** — Read-only access to a local index of your engineering stack: full-text search plus recent incidents, pull requests, deployments, DORA metrics and connector status. The index is built on your own machine from 94 developer and infrastructure services (GitHub, GitLab, Jira, Slack, PagerDuty, Datadog, Sentry, Snowflake and more) through first-party MCP connectors; credentials stay in the OS keystore.
  <sub>★ 6 · TypeScript · AGPL-3.0 · winget · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`winget install NimbusAgent.Nimbus`</sub>
- **[rupinder2/mcp-orchestrator](https://github.com/rupinder2/mcp-orchestrator)** — Central hub that aggregates tools from multiple MCP servers with unified BM25/regex search and deferred loading
  <sub>★ 6 · Python · MIT · pip · pushed 2026-02-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-orchestrator`</sub>
- **[espadaw/Agent47](https://github.com/espadaw/Agent47)** — Unified job aggregator for AI agents across 9+ platforms (x402, RentAHuman, Virtuals, etc)
  <sub>★ 5 · TypeScript · source · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/espadaw/Agent47.git`</sub>
- **[entire-vc/evc-spark-mcp](https://github.com/entire-vc/evc-spark-mcp)** — Search and discover AI agents, skills, prompts, bundles and MCP connectors from a curated catalog of 4500+ assets
  <sub>★ 5 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx evc-spark-mcp`</sub>
- **[thinkchainai/mcpbundles](https://github.com/thinkchainai/mcpbundles)** — MCP Bundles: Create custom bundles of tools and connect providers with OAuth or API keys. Use one MCP server across thousands of integrations, with programmatic tool calling and MCP UI for managing bundles and credentials
  <sub>★ 5 · source · pushed 2026-08-19</sub>
  <sub>`git clone https://github.com/thinkchainai/mcpbundles.git`</sub>
- **[Aganium/agenium](https://github.com/Aganium/agenium)** — Bridge any MCP server to the agent:// network — DNS-like identity, discovery, and trust for AI agents. Makes your tools discoverable and callable by other agents via agent:// URIs with mTLS, trust scores, and capability search
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agenium/create-agent my-agent`</sub>
- **[doggychip/agentforge](https://github.com/doggychip/agentforge)** — Unified API gateway and marketplace for 300+ AI agents. One API key, REST + streaming, 90% creator revenue share, health monitoring. Self-hostable (MIT)
  <sub>★ 4 · TypeScript · clone · pushed 2026-04-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/doggychip/agentforge.git`</sub>
- **[garasegae/aiskillstore](https://github.com/garasegae/aiskillstore)** — Agent-first skill marketplace where AI agents discover, purchase, and integrate skills via MCP protocol. Supports 7+ platforms including Claude, hGPT, and Gemini
  <sub>★ 4 · Python · MIT · docker · pushed 2026-05-14 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run --rm -i aiskillstore-mcp`</sub>
- **[reefapi/reefapi-mcp](https://github.com/reefapi/reefapi-mcp)** — One MCP for 160+ live web-data APIs — search engines, social (Reddit, TikTok, Threads, Bluesky), e-commerce (Amazon, eBay, AliExpress, Etsy), real estate (Zillow, Redfin), jobs, travel, news, finance and company/people intel. Clean JSON from sites that block scrapers; one key, one shared credit pool, free tier. Remote streamable-http at api.reefapi.com/mcp
  <sub>★ 4 · Python · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reefapi/reefapi-mcp.git`</sub>
- **[cinderwright-ai/cinderwright-api](https://github.com/cinderwright-ai/cinderwright-api)** — x402 Discovery Hub. Search engine for the agent economy with 1450+ services indexed. Pay with USDC on Base via x402
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx cinderwright-mcp-server`</sub>
- **[Jackalope-Dev/allmcps-server](https://github.com/Jackalope-Dev/allmcps-server)** — Official MCP server for the AllMCPs.com registry: search and browse MCP servers, get ready-to-use install configs for Claude Desktop/Cursor/etc., and submit or claim listings directly from your agent. Install: npx -y allmcps-server
  <sub>★ 4 · JavaScript · MIT · npx · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx allmcps-server search postgres # search the directory`</sub>
- **[jaspertvdm/mcp-server-gemini-bridge](https://github.com/jaspertvdm/mcp-server-gemini-bridge)** — Bridge to Google Gemini API. Access Gemini Pro and Flash models through MCP
  <sub>★ 4 · Dockerfile · MIT · pip · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mcp-server-gemini-bridge`</sub>
- **[jaspertvdm/mcp-server-ollama-bridge](https://github.com/jaspertvdm/mcp-server-ollama-bridge)** — Bridge to local Ollama LLM server. Run Llama, Mistral, Qwen and other local models through MCP
  <sub>★ 4 · Dockerfile · MIT · pip · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mcp-server-ollama-bridge`</sub>
- **[malamutemayhem/unclick](https://github.com/malamutemayhem/unclick)** — The universal remote for AI: one MCP install gives any compatible agent 450+ callable endpoints across 60+ integrations, plus persistent cross-session memory. npx @unclick/mcp-server
  <sub>★ 4 · TypeScript · AGPL-3.0 · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g https://github.com/malamutemayhem/unclick/releases/latest/download/unclick.tgz`</sub>
- **[MastadoonPrime/sylex-search](https://github.com/MastadoonPrime/sylex-search)** — Universal search engine for AI agents. Discover products, services, and businesses across every category. 10 MCP tools, zero LLM calls, millisecond responses. npx sylex-search
  <sub>★ 4 · Python · AGPL-3.0 · npx · pushed 2026-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sylex-search`</sub>
- **[supertrained/rhumb](https://github.com/supertrained/rhumb)** — Agent-native tool intelligence across 1,000+ scored services. 21 MCP tools: discover services, check AN Scores, compare alternatives, resolve capabilities to ranked providers, execute through 3 credential modes (managed, BYOK, agent vault), track costs with receipts, and inspect failure modes. Zero-signup option via x402 micropayments
  <sub>★ 4 · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y --package rhumb-mcp@latest rhumb-mcp`</sub>
- **[rplryan/x402-discovery-mcp](https://github.com/rplryan/x402-discovery-mcp)** — Runtime discovery layer for x402-payable APIs. Agents discover and route to pay-per-call x402 endpoints by capability, get quality-ranked results with trust scores (0-100), and pay per query via x402. Includes MCP server, Python SDK, and CLI (npm install -g x402scout)
  <sub>★ 4 · Python · MIT · npm · pushed 2026-03-11 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g x402scout`</sub>
- **[GTCC777/pulsenetwork-mcp](https://github.com/GTCC777/mcp-pulsenetwork)** — One MCP server exposing 66 specialized intelligence APIs (660+ endpoints) — finance, crypto, legal, immigration, healthcare cost, real estate, tax, climate, sports, science, and more — each an x402 pay-per-call tool in USDC on Base and Solana. Includes a discover meta-tool over the whole network and a cross-vertical referral graph. No API keys. npx mcp-pulsenetwork
  <sub>★ 3 · TypeScript · Apache-2.0 · npm · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-pulsenetwork`</sub>
- **[agentbodegastore/agentbodega](https://github.com/agentbodegastore/agentbodega)** — AgentBodega MCP gives agents a live catalog of 65 x402-payable HTTP tools across search, public data, social media, status checks, media conversion, and agent-readiness checks. No API keys; install with npx -y @agentbodega/mcp
  <sub>★ 3 · JavaScript · MIT · npx · pushed 2026-07-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agentbodega/mcp`</sub>
- **[AgentHotspot](https://github.com/agenthotspot/agenthotspot-mcp)** — Search, integrate and monetize MCP connectors on the AgentHotspot MCP marketplace
  <sub>★ 3 · Python · MIT · clone · pushed 2026-01-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AgentHotspot/agenthotspot-mcp.git`</sub>
- **[doteyeso-ops/mcp-server-vibes-coded](https://github.com/doteyeso-ops/mcp-server-vibes-coded)** — Remote MCP server with 26 curated tools for agent supply-chain security, scanner consensus, x402 reliability, and access to Vibes-Coded's 344-resource commerce catalog. Live at https://vibes-coded-mcp-production.up.railway.app/mcp; no API key required
  <sub>★ 3 · Python · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @doteyeso-ops/mcp-server-vibes-coded`</sub>
- **[sF1nX/x402station](https://github.com/sF1nX/x402station-mcp)** — Preflight by x402station.io — infrastructure for x402 agentic commerce. Six capability directions (Discover/Evaluate/Pay/Monitor/Recover/Analyze). Agents call it before every PAYMENT-SIGNATURE to detect decoys, zombie endpoints, dead services, and price traps. Tools: preflight ($0.001), forensics ($0.001), catalog_decoys ($0.005), alternatives ($0.005), whats_new ($0.001), buy_credits ($0.50 = 100
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g x402station-mcp`</sub>
- **[sonnyflylock/voxie-ai-directory-mcp](https://github.com/sonnyflylock/voxie-ai-directory-mcp)** — AI Phone Number Directory providing access to AI services via webchat. Query Voxie AI personas and third-party services like ChatGPT, with instant webchat URLs for free interactions
  <sub>★ 3 · JavaScript · source · pushed 2026-01-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sonnyflylock/voxie-ai-directory-mcp.git`</sub>
- **[ikoskela/wisepanel-mcp](https://github.com/ikoskela/wisepanel-mcp)** — Multi-agent deliberation with divergent context enhancement. Roles are dynamically generated to surround the question-space and maximize divergent dialog across ChatGPT, Claude, Gemini, and Perplexity
  <sub>★ 3 · TypeScript · MIT · clone · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ikoskela/wisepanel-mcp.git`</sub>
- **[Swarmwage/swarmwage](https://github.com/Swarmwage/swarmwage)** — Open MCP-native agent hire protocol — discovery + hiring + reputation layer above x402 payment rails. Find specialized agents, hire them with one function call, settle in USDC on Base. Sub-second sync, on-chain receipts via EIP-3009, zero protocol fee. Live mainnet 2026-05-10
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-07-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @swarmwage/mcp`</sub>
- **[8randonpickart5/alderpost-mcp](https://github.com/8randonpickart5/alderpost-mcp)** — 8 bundled intelligence endpoints (security, company, threat, compliance, sales, sports, property, health) via x402 micropayments on Base
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y alderpost-mcp`</sub>
- **[Alepha188838884/context-firewall](https://github.com/Alepha188838884/context-firewall)** — Local proxy that collapses N downstream MCP servers into 4 meta-tools with progressive tool discovery (measured: 122 tools → 4, ~28.6K tokens of definitions saved), compresses large tool outputs (HTML→Markdown, JSON structure summarization, base64 stripping — 60–95% measured on real pages/APIs) with full-output retrieval via read_more, and prints a per-session token-savings report. Security-releva
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx context-firewall --config context-firewall.json`</sub>
- **[gamaze-labs/hicortex](https://github.com/gamaze-labs/hicortex)** — Shared fleet memory for AI agents: the store corrects itself nightly (stale facts rewritten in place, duplicates merged), recall is injected into every prompt in supported coding agents — what one agent learns, the whole fleet knows. Website
  <sub>★ 2 · TypeScript · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @gamaze/hicortex init`</sub>
- **[gpu-bridge/mcp-server](https://github.com/gpu-bridge/mcp-server)** — Unified GPU inference API with 30 AI services (LLM, image gen, video, TTS, whisper, embeddings, reranking, OCR) as MCP tools. Pay-per-use via x402 USDC or API key credits
  <sub>★ 2 · JavaScript · MIT · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gpu-bridge/mcp-server.git`</sub>
- **[jabbawocky/proposalcraft](https://github.com/jabbawocky/proposalcraft)** — MCP server that drafts client proposals in your own voice. Save 2-3 of your winning proposals, paste a new brief, and Claude generates a ready-to-send draft. No API key, no cloud — local storage only. npx -y github:jabbawocky/proposalcraft
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:jabbawocky/proposalcraft`</sub>
- **[jaspertvdm/mcp-server-openai-bridge](https://github.com/jaspertvdm/mcp-server-openai-bridge)** — Bridge to OpenAI API. Access GPT-4, GPT-4o and other OpenAI models through MCP
  <sub>★ 2 · Dockerfile · MIT · pip · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mcp-server-openai-bridge`</sub>
- **[ni-c/mcp-hub](https://github.com/ni-c/mcp-hub)** — Serve many stdio MCP servers from one container, published over HTTPS for Claude Web custom connectors and any Streamable-HTTP client. Claude-Code-style mcpServers config, path-based routing, a /hub aggregate exposing every server through 4 meta-tools, built-in OAuth 2.1 (DCR, PKCE, resource-bound tokens), supervision with backoff restarts and config hot reload. docker pull ghcr.io/ni-c/mcp-hub or
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @ni-c/mcp-hub`</sub>
- **[x402-index/x402search-mcp](https://github.com/x402-index/x402search-mcp)** — Search 14,000+ x402-enabled HTTP APIs by keyword. Agents pay $0.01 USDC per search via x402 micropayments on Base mainnet — no API keys required. Larger index than any other x402 discovery layer
  <sub>★ 2 · JavaScript · pip · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install x402search-mcp`</sub>
- **[ertad-family/liquid](https://github.com/ertad-family/liquid)** — Connect your agent to any HTTP API on the fly — discovers + maps any REST API once, then fetches typed data deterministically (no per-call LLM). Self-hosted MCP server (uvx --from 'liquid-api[mcp]' liquid-mcp); works with OpenAI/Gemini/Anthropic/local or any provider via LiteLLM. Open source (AGPL)
  <sub>★ 2 · Python · pip · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install liquid-api # core + bundled MCP server (the `liquid-mcp` command)`</sub>
- **[forgemeshlabs/coinopai-mcp](https://github.com/forgemeshlabs/coinopai-mcp)** — Local stdio MCP server for x402-powered paid crypto intelligence: preflight checks, trade decisions with decision_id, later audit against real prices, risk state, signal history, and agent automation search over USDC micropayments on Base
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx coinopai-mcp@...`</sub>
- **[minia2auk/minia2a-mcp](https://github.com/minia2auk/minia2a-mcp)** — Pay-per-call x402 gateway: one remote MCP server for 1,680+ agent tools (crypto data, web scraping, AI inference, CAPTCHA solving, token security, DNS/WHOIS, gas monitoring, DeFi data). USDC on Base, 5 free trial calls per registered wallet. Remote https://minia2a.uk/mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g minia2a-mcp`</sub>
- **[PHONGUIT22/nostrpulse-full](https://github.com/PHONGUIT22/nostrpulse-full)** — Autonomous Agent-to-Agent (A2A) commerce framework via Nostr NIP-90 and Cashu eCash micro-settlements
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector npx -y nostrpulse-mcp`</sub>
- **[getanyapi-com/mcp](https://github.com/getanyapi-com/mcp)** — AnyAPI: hundreds of scraping and data APIs (social media, search results, Google Maps, e-commerce, general web data) behind one MCP server - one key, USD pay-per-request, no subscriptions, normalized JSON schemas, and automatic failover across upstream providers. Agents discover, inspect, price and run any of them with the same loop (search_apis, get_api, quote_api, run_api); failed calls are neve
  <sub>★ 1 · TypeScript · Apache-2.0 · source · pushed 2026-09-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/getanyapi-com/mcp.git`</sub>
- **[alexar76/aimarket-plugins](https://github.com/alexar76/aimarket-plugins)** — aimarket-mcp-packager hub plugin: turn AIMarket capabilities into self-hosted MCP servers (Docker image + mcp_manifest + Claude Desktop mcpServers config). Part of 15-plugin AIMarket Hub (modelmarket.dev); protocol discovery at /.well-known/ai-market.json. Install: pip install aimarket-mcp-packager
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -e plugins/aimarket-zk`</sub>
- **[ariekogan/ateam-mcp](https://github.com/ariekogan/ateam-mcp)** — Build, validate, and deploy multi-agent AI solutions on the ADAS platform. Design skills with tools, manage solution lifecycle, and connect from any AI environment via stdio or HTTP
  <sub>★ 1 · JavaScript · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ariekogan/ateam-mcp.git`</sub>
- **[bridgenode-ai/bridgenode-mcp](https://github.com/bridgenode-ai/bridgenode-mcp)** — Pay-per-request AI inference for agents: chat completions across any supported model via x402 with automatic Solana USDC payments. No API keys, no registration, fail-closed spending caps. npx -y @bridgenode/mcp or remote https://bridgenode.cc/mcp
  <sub>★ 1 · TypeScript · MIT-0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install bridgenode-llm`</sub>
- **[kansei-link/kansei-mcp-server](https://github.com/kansei-link/kansei-mcp-server)** — Local-first MCP navigator with verified data on 11,000+ SaaS services, 200 workflow recipes, and 89-97% token savings vs web search
  <sub>★ 1 · HTML · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @kansei-link/mcp-server`</sub>
- **[mambalabsdev/mcp-gtm-suite](https://github.com/mambalabsdev/mcp-gtm-suite)** — Six GTM signal tools in one MCP server, covering hiring signals, tech stack detection, job board scanning, LinkedIn URL resolution, ICP scoring, and signal aggregation via Apify actors
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mambalabsdev/mcp-gtm-suite.git`</sub>
- **[mirastacklabs-ai/mirastack-redfish-mcp](https://github.com/mirastacklabs-ai/mirastack-redfish-mcp)** — Governed MCP access to DMTF Redfish BMCs (iDRAC, iLO, XCC, OpenBMC) for power, thermal, firmware, and BIOS management. Read-only by default with tiered write modes
  <sub>★ 1 · Python · Apache-2.0 · pip · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install mirastack-redfish-mcp`</sub>
- **[Octodamus/octodamus-core](https://github.com/Octodamus/octodamus-core)** — AI consensus market oracle for crypto traders and autonomous agents. 11-signal BUY/SELL/HOLD consensus (RSI, MACD, funding rate, L/S ratio, on-chain flow, Fear &amp; Greed, congressional trading), Polymarket prediction market edges with EV scoring, Grok X crowd sentiment divergence. Ed25519-signed, on-chain verifiable. x402 micropayments at $0.01/call on Base, or 500 req/day free
  <sub>★ 1 · Python · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @smithery/cli install octodamusai/market-intelligence`</sub>
- **[oxgeneral/agentnet](https://github.com/oxgeneral/agentnet)** — Agent-to-agent referral network where AI agents discover, recommend, and refer users to each other. Features bilateral trust model, credit economy, and 7 MCP tools for agent registration, discovery, and referral tracking
  <sub>★ 1 · Python · npx · pushed 2026-02-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @smithery/cli mcp add https://agentnet--mouse-7fea.run.tools`</sub>
- **[mrfelfel/taghvim](https://github.com/mrfelfel/taghvim)** — Deterministic temporal reasoning engine for AI agents. 12 tools for date/time arithmetic, timezone conversion with DST, business days across 100+ countries, public holidays, RFC 5545 recurrence, Gregorian/Persian calendar conversion, and temporal claim verification. npx taghvim-mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx taghvim-mcp`</sub>
- **[forcedreamai/forcedream-mcp](https://github.com/forcedreamai/forcedream-mcp)** — Discover, invoke, and cryptographically verify AI agents on a paid agent marketplace. 13 tools spanning code generation (6-module engineering verification), security scanning (OSV.dev + GitGuardian), and lead scoring (8 real sources). Every result is Ed25519-signed and independently verifiable -- no trust in the platform required. Install: npx -y @forcedream/mcp-server
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @forcedream/mcp-server`</sub>
- **[402signalhq/402signal](https://github.com/402signalhq/402signal)** — Checks live x402 routes across Base, Solana, and Algorand. $0.003 USDC settles only for a valid live eligible route; normal typed misses are not settled. Free preview and validate tools. Seller payment is separate; the agent keeps its wallet. Remote MCP: https://402signal.com/mcp (x402-capable client required for paid routing)
  <sub>JavaScript · MIT · pip · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install 402signal==0.1.2`</sub>
- **[GarphenGate/moltline-mcp](https://github.com/GarphenGate/moltline-mcp)** — Zero-dependency stdio bridge to Moltline Studio's 22 hosted MCP servers (160 tools, 110 free) — code review, agent governance, data &amp; business math, regulatory deadlines, crypto tax lots, routing/optimization and more. Free tier needs no account or API key. Remote streamable-http at mcp.moltlinestudio.com/
  <sub>Python · MIT · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm moltline-mcp timeops # any of the 22 slugs; default: catalog`</sub>
- **[team886/findagent-mcp](https://github.com/team886/findagent-mcp)** — Cross-LLM marketplace of vetted "doer" agents — itself an MCP server. Automated security scan + human review, credential-to-host binding, and sandboxed hosted code with default-deny egress. Remote endpoint https://mcp.findagent.cloud/mcp
  <sub>JavaScript · MIT · docker · pushed 2026-09-11 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i findagent-mcp`</sub>
- **[BotHireAgent/BotHireMCPServer](https://github.com/BotHireAgent/BotHireMCPServer)** — Discover BotHire, the machine-to-machine marketplace where autonomous AI agents hire each other and settle in USDT &amp; USDC (gasless) across Base, Arbitrum, BNB Chain &amp; Solana. Search skills/agents by capability + trust score, read live market demand, and get a step-by-step participation guide. npx -y bothire-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx bothire-mcp`</sub>
- **[@neoninnovationlab/neon-mcp-gateway](https://github.com/neoninnovationlab/neon-mcp-gateway)** — An edge firewall for AI agents to securely expose internal PostgreSQL databases and APIs with strict validation
  <sub>JavaScript · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/neoninnovationlab/neon-mcp-gateway.git`</sub>
- **[Correctover/mcp-server](https://github.com/Correctover/mcp-server)** — Contract validation and self-healing failover for LLM APIs. 6-dimension verification (structure, schema, latency, cost, identity, integrity) in 22μs P50. 87 self-healing rules with MAPE-K autonomic loop. BYOK direct connect to 9 providers (OpenAI, Anthropic, DeepSeek, Moonshot, Zhipu AI, Qwen, SiliconFlow, Groq, Together AI). L3 failover in 949ms E2E. Install: npx -y correctover-mcp-server
  <sub>unavailable</sub>
- **[daedalusdevelopmentgroup/ddg-agent-payable-services](https://github.com/daedalusdevelopmentgroup/ddg-agent-payable-services)** — Pay-per-call x402 gateway: one MCP server for 90+ agent tools (utilities, DNS/WHOIS, blockchain RPC, market data, prediction markets, DEX data, security audits) plus an OpenAI-compatible LLM gateway. USDC on Base, free-trial calls per agent. pip install ddg-agent-services-mcp or remote https://mcp.daedalusdevelopmentgroup.com/mcp
  <sub>Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ddg-agent-services-mcp`</sub>
- **[forgemeshlabs/anomaly-mcp](https://github.com/forgemeshlabs/anomaly-mcp)** — Real-time anomaly detection powered by NASA-derived sequence mining across blockchain, mempool, stablecoin depeg, aviation, and GitHub signals via x402 USDC micropayments on Base. npx -y @forgemeshlabs/anomaly-mcp
  <sub>TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @forgemeshlabs/anomaly-mcp`</sub>
- **[forgemeshlabs/utility-grid-mcp](https://github.com/forgemeshlabs/utility-grid-mcp)** — Discover and call 400+ practical APIs through six MCP tools: search OCR, image, audio, web, math, conversion, and geodata utilities for free, then pay per call with x402 USDC on Base — no account or API key. npx -y @forgemeshlabs/utility-grid-mcp
  <sub>JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/forgemeshlabs/utility-grid-mcp.git`</sub>
- **[mcpqueen/mcpqueen](https://github.com/mcpqueen/mcpqueen)** — The graded MCP registry: live-probes every remote server in the official registry (initialize, tools/list, schema quality, latency, provenance) and publishes evidence-backed grades — searchable by agents via its own MCP endpoint at mcpqueen.com
  <sub>JavaScript · MIT · docker · pushed 2026-09-13 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i mcpqueen-bridge`</sub>
- **[szp2005/llm-prices-cn](https://github.com/szp2005/llm-prices-cn)** — Daily-verified LLM API pricing dataset (44+ models, CN &amp; global) with a hosted MCP server for live price queries and token cost estimation
  <sub>Python · CC-BY-4.0 · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm llm-prices-mcp # stdio MCP server`</sub>
- **[AIsa-public/AIsa-mcp-server](https://github.com/AIsa-public/AIsa-mcp-server)** — One MCP server in front of 950+ data APIs — SEO and AI visibility, finance, social, web search, sales and agent mail. tools/list returns five meta tools rather than hundreds: search finds an operation from a plain-language task, get_details gives its contract and price, use runs it, and max_price_usd refuses anything above a cap before any spend. OAuth, nothing to paste. Install: npx -y @aisa-one/
  <sub>JavaScript · MIT · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AIsa-public/AIsa-mcp-server.git`</sub>
- **[RightOnPar-LLC/mesh-connector](https://github.com/RightOnPar-LLC/meshmarket-mcp)** — Agent-to-agent capability exchange (MeshMarket): agents browse keylessly, self-onboard via mesh_signup, rent memory/reasoning/safety per call, list their own tools with mesh_publish, and settle in closed-loop credits on a debit-first ledger
  <sub>JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mesh-connector init # auto-wire Claude Code / Cursor / Claude Desktop / VS Code`</sub>
- **[adw0rd/awesome-mcp-tools-mcp](https://github.com/adw0rd/awesome-mcp-tools-mcp)** — CLI + stdio MCP bridge for the awesome-mcp.tools catalog (2,000+ MCP servers, refreshed every 6h). Search from terminal (npx awesome-mcp search postgres) or wire the hosted server into Claude / Cursor / Codex / Cline / Windsurf. Endpoint: https://awesome-mcp.tools/mcp (Streamable HTTP, no auth). Zero deps, MIT
  <sub>JavaScript · MIT · npm · pushed 2026-06-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g awesome-mcp # or use npx (no install)`</sub>
- **[avotsai/avots-mcp](https://github.com/avotsai/avots-mcp)** — Hosted multi-model AI media + chat: image, video, audio, face-swap and talking-avatar generation plus chat across 300+ models (Claude, GPT, Gemini, DeepSeek…) from one balance and one key
  <sub>JavaScript · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/avotsai/avots-mcp.git`</sub>
- **[edgarriba/prolink](https://github.com/edgarriba/prolink)** — Agent-to-agent marketplace middleware — MCP-native discovery, negotiation, and transaction between AI agents
  <sub>unavailable</sub>
- **[Proofpane/releases](https://github.com/Proofpane/releases)** — Governance proxy for MCP: pair once and route your MCP servers through policy gates (allow / deny / human-in-the-loop approval), DLP redaction before the model, and cost caps, with every tool call recorded to a hash-chained audit log exportable as an Ed25519-signed, offline-verifiable evidence pack. Single-file binary daemon (macOS / Linux / Windows); downloads and install docs in the linked repo
  <sub>Python · MIT · docker · pushed 2026-08-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run --rm -i proofpane-mcp # speaks stdio MCP`</sub>
- **[Gliana-Labs/gliana-mcp](https://github.com/Gliana-Labs/gliana-mcp)** — Pay-per-call access to 90+ AI models (LLM chat, image, video, music, speech) plus utility and data tools — web scraping, screenshots, OCR, face matching, crypto and FX rates. No signup and no API key: HTTP 402 settles each call from your own wallet in USDC on Base, Solana, BNB Chain or Algorand. The tool list is read live from the gateway, so it is never stale. npx -y gliana-ai-mcp or remote https
  <sub>JavaScript · source · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Gliana-Labs/gliana-mcp.git`</sub>
- **[hedging8563/tokenlab-mcp-server](https://github.com/hedging8563/tokenlab-mcp-server)** — TokenLab AI gateway MCP server for model and pricing discovery, OpenAI-compatible Chat Completions, and native Responses, Anthropic Messages, and Gemini inference. Catalog tools require no API key; inference tools use an optional TokenLab key
  <sub>JavaScript · MIT · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @tokenlabai/mcp-server`</sub>
- **[codeislaw101/katzilla](https://github.com/codeislaw101/katzilla)** — Unified data API for AI agents — 300+ free, public, and government data sources behind a single API key. Access economic (FRED, BLS), environmental (EPA, NOAA), health (CDC, FDA), weather (NWS), financial (SEC, CFPB), science (NASA, arXiv), and 30+ more categories. Install: npx @katzilla/mcp
  <sub>unavailable</sub>
- **[kevmoz/macaroonnetwork-mcp](https://github.com/kevmoz/macaroonnetwork-mcp)** — Discovery and purchase client for a predicate-gated scientific and data marketplace. Search the live catalogue and inspect metadata for free, then pay via x402 (USDC on Base mainnet, the live primary rail) or Lightning L402. Install with pip install macaroonnetwork-mcp
  <sub>Python · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install macaroonnetwork-mcp`</sub>
- **[mediiiiium/mcp-jp](https://github.com/mediiiiium/mcp-jp)** — Collection of MCP servers for Japanese SMB SaaS that have no official MCP (KING OF TIME, SmartHR, kaonavi, Smaregi, LINE Lstep, CloudSign, and 30+ more). Each connector is an independent pip-installable package
  <sub>Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mediiiiium/mcp-jp.git`</sub>
- **[PipedreamHQ/pipedream](https://github.com/PipedreamHQ/pipedream/tree/master/modelcontextprotocol)** — Connect with 2,500 APIs with 8,000+ prebuilt tools, and manage servers for your users, in your own app
  <sub>JavaScript · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/PipedreamHQ/pipedream.git && cd pipedream/modelcontextprotocol`</sub>
- **[RipperMercs/tensorfeed](https://github.com/RipperMercs/tensorfeed/tree/main/mcp-server)** — Real-time AI industry intelligence MCP server. 6 free tools (AI news, service status, model pricing, today summary, agent activity, MCP registry snapshot) and 13 paid premium tools (routing recommendations, news search, history series, cost projection, provider deep-dive, model comparison, agents directory, what's new brief, MCP registry series, webhook watches with daily/weekly digest tier). Pay-
  <sub>in-repo</sub>
  <sub>`git clone https://github.com/RipperMercs/tensorfeed.git && cd tensorfeed/mcp-server`</sub>
- **[scotia1973-bot/api-hub](https://github.com/scotia1973-bot/api-hub)** — Memory Vault: 49 MCP tools with persistent agent memory (store/recall/search), plus 45 utility tools (QR codes, crypto prices, weather, DNS, geolocation, passwords, UUIDs, text, finance, code). Free tier + $2.99/mo Pro. Install: pip install gadgethumans-api-hub-mcp or uvx gadgethumans-api-hub-mcp. Hosted at api.gadgethumans.com/mcp
  <sub>unavailable</sub>
- **[thebrierfox/the-stall](https://github.com/thebrierfox/the-stall)** — 209 pay-per-call AI capabilities via x402 USDC micropayments on Base mainnet. Covers US/global equities, crypto/DeFi analytics, options chains, dealer GEX, macro indicators, congressional trades, prediction markets, on-chain intelligence, EVM &amp; Solana analysis, SEC filings, weather, aviation, and more. No API key — pay per call from $0.001 USDC
  <sub>JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/thebrierfox/the-stall.git`</sub>
- **[swaltersjrtest/microtap-mcp](https://github.com/swaltersjrtest/microtap-mcp)** — 19 pay-per-call APIs for AI agents via x402 USDC micropayments on Base — prediction markets (Polymarket, Kalshi), DeFi/crypto data, multi-chain on-chain reads across 5 EVM chains, live weather, and real-time web search. No API key or signup — from $0.001/call. npx -y microtap-mcp
  <sub>TypeScript · MIT · source · pushed 2026-08-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/swaltersjrtest/microtap-mcp.git`</sub>
- **[TheLunarCompany/lunar#mcpx](https://github.com/TheLunarCompany/lunar/tree/main/mcpx)** — MCPX is a production-ready, open-source gateway to manage MCP servers at scale—centralize tool discovery, access controls, call prioritization, and usage tracking to simplify agent workflows
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/TheLunarCompany/lunar.git && cd lunar/mcpx`</sub>
- **[tigranbs/mcgravity](https://github.com/tigranbs/mcgravity)** — A proxy tool for composing multiple MCP servers into one unified endpoint. Scale your AI tools by load balancing requests across multiple MCP servers, similar to how Nginx works for web servers
  <sub>unavailable</sub>
- **[toadlyBroodle/satring](https://github.com/toadlyBroodle/satring/tree/main/mcp)** — Discover and compare L402 + x402 paid API services from satring.com, the best curated Lightning and USDC API directory
  <sub>Python · MIT · in-repo · pushed 2026-07-23</sub>
  <sub>`git clone https://github.com/toadlyBroodle/satring.git && cd satring/mcp`</sub>
- **[skillselion/skillselion-mcp](https://github.com/skillselion/skillselion-mcp)** — Search thousands of community-vetted Claude Code skills, MCP servers and marketplaces from the Skillselion catalog, ranked by real install counts + GitHub stars. load_skill fetches a real SKILL.md mid-task. Install: npx -y skillselion-mcp
  <sub>JavaScript · MIT · npx · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y skillselion-mcp setup # interactive - pick your packs`</sub>
- **[singhpratech/crimson-crab-mcp-template](https://github.com/singhpratech/crimson-crab-mcp-template)** — A ready-to-clone Rust MCP server that calls Anthropic's Claude API via the crimson-crab SDK. Exposes an ask_claude tool. MIT/Apache-2.0
  <sub>Rust · Apache-2.0 · clone · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/singhpratech/crimson-crab-mcp-template`</sub>

## Security

- **[mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp)** — MCP server for IDA Pro, allowing you to perform binary analysis with AI assistants. This plugin implement decompilation, disassembly and allows you to generate malware analysis reports automatically
  <sub>★ 12.3k · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install https://github.com/mrexodia/ida-pro-mcp/archive/refs/heads/main.zip`</sub>
- **[LaurieWired/GhidraMCP](https://github.com/LaurieWired/GhidraMCP)** — A Model Context Protocol server for Ghidra that enables LLMs to autonomously reverse engineer applications. Provides tools for decompiling binaries, renaming methods and data, and listing methods, classes, imports, and exports
  <sub>★ 10.2k · Java · Apache-2.0 · source · pushed 2025-06-23</sub>
  <sub>`git clone https://github.com/LaurieWired/GhidraMCP.git`</sub>
- **[zinja-coder/jadx-ai-mcp](https://github.com/zinja-coder/jadx-ai-mcp)** — JADX-AI-MCP is a plugin and MCP Server for the JADX decompiler that integrates directly with Model Context Protocol (MCP) to provide live reverse engineering support with LLMs like Claude
  <sub>★ 2.8k · Java · Apache-2.0 · uv · pushed 2026-08-30 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`uv tool install git+https://github.com/zinja-coder/jadx-mcp-server`</sub>
- **[mariocandela/beelzebub](https://github.com/beelzebub-labs/beelzebub)** — Beelzebub is a honeypot framework that lets you build honeypot tools using MCP. Its purpose is to detect prompt injection or malicious agent behavior. The underlying idea is to provide the agent with tools it would never use in its normal work
  <sub>★ 2.2k · Go · GPL-3.0 · clone · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/beelzebub-labs/beelzebub.git`</sub>
- **[duriantaco/skylos](https://github.com/duriantaco/skylos)** — Dead code detection, security scanning, and code quality analysis for Python, TypeScript, and Go. 98% recall with fewer false positives than Vulture. Includes AI-powered remediation
  <sub>★ 828 · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install skylos`</sub>
- **[jtang613/GhidrAssistMCP](https://github.com/symgraph/GhidrAssistMCP)** — A native Model Context Protocol server for Ghidra. Includes GUI configuration and logging, 31 powerful tools and no external dependencies
  <sub>★ 745 · Java · MIT · source · pushed 2026-08-03 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/jtang613/GhidrAssistMCP.git`</sub>
- **[semgrep/mcp](https://github.com/semgrep/mcp)** — Allow AI agents to scan code for security vulnerabilites using Semgrep
  <sub>★ 688 · Python · MIT · uv · pushed 2025-10-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx semgrep-mcp # see --help for more options`</sub>
- **[zinja-coder/apktool-mcp-server](https://github.com/zinja-coder/apktool-mcp-server)** — APKTool MCP Server is a MCP server for the Apk Tool to provide automation in reverse engineering of Android APKs
  <sub>★ 656 · Python · Apache-2.0 · source · pushed 2026-07-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zinja-coder/apktool-mcp-server.git`</sub>
- **[emiliaprotocol/emilia-protocol](https://github.com/emiliaprotocol/emilia-protocol)** — Human sign-off + trust receipts for AI agents: requires a named human's approval before an irreversible action (payment release, record change, deploy), then mints an offline-verifiable Ed25519 Trust Receipt. Also exposes trust profiles, receipt verification, disputes, and delegation. Apache-2.0; policy engine formally verified. Install: npx -y @emilia-protocol/mcp-server
  <sub>★ 617 · TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @emilia-protocol/verify aeb-conformance --reference`</sub>
- **[fosdickio/binary_ninja_mcp](https://github.com/fosdickio/binary_ninja_mcp)** — A Binary Ninja plugin, MCP server, and bridge that seamlessly integrates Binary Ninja with your favorite MCP client. It enables you to automate the process of performing binary analysis and reverse engineering
  <sub>★ 438 · Python · GPL-3.0 · npx · pushed 2026-04-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y binary-ninja-mcp`</sub>
- **[ucsandman/DashClaw](https://github.com/ucsandman/DashClaw)** — Fail-closed approval layer for unattended agent runs: guard evaluates each declared action against org policy before it executes (allow/warn/block/require-approval with one-click human approval), records every decision to a causal ledger, and adds plan preflight, scoped delegation grants, and containment verdicts. npx -y @dashclaw/mcp-server
  <sub>★ 307 · TypeScript · MIT · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @dashclaw/cli`</sub>
- **[radareorg/r2mcp](https://github.com/radareorg/radare2-mcp)** — MCP server for Radare2 disassembler. Provides AI with capability to disassemble and look into binaries for reverse engineering
  <sub>★ 307 · C · MIT · source · pushed 2026-09-16 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/radareorg/radare2-mcp.git`</sub>
- **[dengyier/OpenWorkProof](https://github.com/dengyier/OpenWorkProof)** — Verifiable execution protocol for AI agent tool calls. Ed25519-signed PolicyDecisions, causal evidence chains (RFC 8785 JCS), and offline verification from SQLite ledger. 2,281 tests, 2 real-world bugs demonstrated end-to-end. pip install openworkproof
  <sub>★ 288 · Python · Apache-2.0 · clone · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dengyier/OpenWorkProof.git`</sub>
- **[BurtTheCoder/mcp-maigret](https://github.com/w0h1v/mcp-maigret)** — MCP server for maigret, a powerful OSINT tool that collects user account information from various public sources. This server provides tools for searching usernames across social networks and analyzing URLs
  <sub>★ 264 · JavaScript · MIT · npm · pushed 2026-01-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-maigret`</sub>
- **[bx33661/Wireshark-MCP](https://github.com/bx33661/Wireshark-MCP)** — Wireshark network packet analysis MCP Server with capture, protocol stats, field extraction, and security analysis capabilities
  <sub>★ 260 · Python · MIT · pip · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install wireshark-mcp`</sub>
- **[gbrigandi/mcp-server-wazuh](https://github.com/gbrigandi/mcp-server-wazuh)** — A Rust-based MCP server bridging Wazuh SIEM with AI assistants, providing real-time security alerts and event data for enhanced contextual understanding
  <sub>★ 237 · Rust · MIT · clone · pushed 2025-12-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/gbrigandi/mcp-server-wazuh.git`</sub>
- **[securityfortech/secops-mcp](https://github.com/securityfortech/secops-mcp)** — All-in-one security testing toolbox that brings together popular open source tools through a single MCP interface. Connected to an AI agent, it enables tasks like pentesting, bug bounty hunting, threat hunting, and more
  <sub>★ 213 · Python · MIT · docker · pushed 2025-09-17 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it --rm secops-mcp`</sub>
- **[BurtTheCoder/mcp-shodan](https://github.com/w0h1v/mcp-shodan)** — MCP server for querying the Shodan API and Shodan CVEDB. This server provides tools for IP lookups, device searches, DNS lookups, vulnerability queries, CPE lookups, and more
  <sub>★ 173 · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @burtthecoder/mcp-shodan`</sub>
- **[BurtTheCoder/mcp-virustotal](https://github.com/w0h1v/mcp-virustotal)** — MCP server for querying the VirusTotal API. This server provides tools for scanning URLs, analyzing file hashes, and retrieving IP address reports
  <sub>★ 150 · TypeScript · MIT · npm · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @burtthecoder/mcp-virustotal`</sub>
- **[timescale/rsigma](https://github.com/timescale/rsigma)** — Exposes the RSigma Sigma detection-engineering toolkit to AI agents over stdio or Streamable HTTP with rsigma mcp serve. Tools to author, lint, validate, and convert Sigma detection rules, evaluate and explain detections against log events, and inspect correlation state, all backed by a native Rust engine
  <sub>★ 142 · Rust · MIT · cargo · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install --locked rsigma`</sub>
- **[13bm/GhidraMCP](https://github.com/13bm/GhidraMCP)** — MCP server for integrating Ghidra with AI assistants. This plugin enables binary analysis, providing tools for function inspection, decompilation, memory exploration, and import/export analysis via the Model Context Protocol
  <sub>★ 140 · Java · Apache-2.0 · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/13bm/GhidraMCP.git`</sub>
- **[jnMetaCode/shellward](https://github.com/jnMetaCode/shellward)** — AI Agent Security Middleware &amp; MCP Server with 8-layer defense including prompt injection detection, DLP data flow tracking, command blocking, and PII detection. 7 MCP tools, zero dependencies
  <sub>★ 136 · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g shellward`</sub>
- **[roadwy/cve-search_mcp](https://github.com/roadwy/cve-search_mcp)** — A Model Context Protocol (MCP) server for querying the CVE-Search API. This server provides comprehensive access to CVE-Search, browse vendor and product、get CVE per CVE-ID、get the last updated CVEs
  <sub>★ 107 · Python · MIT · clone · pushed 2025-07-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/roadwy/cve-search_mcp.git`</sub>
- **[arthurpanhku/DocSentinel](https://github.com/arthurpanhku/DocSentinel)** — MCP server for AI agent for cybersecurity: automate assessment of documents, questionnaires &amp; reports. Multi-format parsing, RAG knowledge base,Risks, compliance gaps, remediations
  <sub>★ 87 · Python · MIT · clone · pushed 2026-09-18 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/arthurpanhku/DocSentinel.git`</sub>
- **[vespo92/OPNSenseMCP](https://github.com/vespo92/OPNSenseMCP)** — MCP Server for managing &amp; interacting with Open Source NGFW OPNSense via Natural Language
  <sub>★ 85 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g opnsense-mcp-server`</sub>
- **[gebalamariusz/cloud-audit](https://github.com/gebalamariusz/cloud-audit)** — Open-source AWS security scanner with attack chain detection, breach cost estimation, and copy-paste remediation (CLI + Terraform). 47 checks, 16 attack chain rules. First free standalone AWS security MCP server
  <sub>★ 72 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from cloud-audit cloud-audit scan # no install`</sub>
- **[dtkmn/mcp-zap-server](https://github.com/dtkmn/mcp-zap-server)** — Self-hosted OWASP ZAP integration for MCP clients, with guided security scans, findings summaries, and report generation
  <sub>★ 66 · Java · Apache-2.0 · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/dtkmn/mcp-zap-server.git`</sub>
- **[82ch/MCP-Dandan](https://github.com/82ch/MCP-Dandan)** — Real-time security framework for MCP servers that detects and blocks malicious AI agent behavior by analyzing tool call patterns and intent across multiple threat detection engines
  <sub>★ 66 · Python · MIT · clone · pushed 2026-08-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/82ch/MCP-Dandan.git`</sub>
- **[Kzino/vorim-mcp-server](https://github.com/Vorim-AI-Labs/vorim-mcp-server)** — AI agent identity, trust, and audit trail infrastructure. 17 MCP tools: register agents with Ed25519 keypairs, check permissions (sub-5ms), emit tamper-evident audit events, verify trust scores (0-100), delegate credentials, and manage ephemeral agents. IETF Internet-Draft filed (draft-vorim-vaip-00). Works with LangChain, OpenAI, CrewAI, Stripe ACP, and 4 more frameworks. npx @vorim/mcp-server
  <sub>★ 66 · JavaScript · MIT · npm · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @vorim/mcp-server`</sub>
- **[26zl/cybersec-toolkit](https://github.com/26zl/cybersec-toolkit)** — One command installs 670+ security tools; an authorization-gated MCP server lets AI clients discover and run them for CTF, pentest, bug bounty, and DFIR
  <sub>★ 59 · Python · MIT · docker · pushed 2026-09-21 · macOS</sub>
  <sub>`docker run --rm ghcr.io/26zl/cybersec-toolkit --profile ctf`</sub>
- **[kastelldev/kastell](https://github.com/kastelldev/kastell)** — Server security auditing and hardening toolkit. 413 security checks across 29 categories (SSH, Firewall, Docker, TLS, HTTP Headers), CIS/PCI-DSS/HIPAA compliance mapping, 19-step production hardening, fleet management, and forensic evidence collection. Supports Hetzner, DigitalOcean, Vultr, and Linode. 13 MCP tools
  <sub>★ 59 · TypeScript · Apache-2.0 · npm · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g kastell`</sub>
- **[qianniuspace/mcp-security-audit](https://github.com/qianniuspace/mcp-security-audit)** — A powerful MCP (Model Context Protocol) Server that audits npm package dependencies for security vulnerabilities. Built with remote npm registry integration for real-time security checks
  <sub>★ 57 · TypeScript · MIT · npx · pushed 2025-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @qianniuspace/mcp-security-audit --client claude`</sub>
- **[snyk/studio-mcp](https://github.com/snyk/studio-mcp)** — Embeds Snyk's security engines into agentic workflows. Secures AI-generated code in real-time and accelerates the fixing vulnerability backlogs
  <sub>★ 55 · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/snyk/studio-mcp.git`</sub>
- **[girste/mcp-cybersec-watchdog](https://github.com/girste/CHIHUAUDIT)** — Comprehensive Linux server security audit with 89 CIS Benchmark controls, NIST 800-53, and PCI-DSS compliance checks. Real-time monitoring with anomaly detection across 23 analyzers: firewall, SSH, fail2ban, Docker, CVE, rootkit, SSL/TLS, filesystem, network, and more
  <sub>★ 53 · Go · MIT · source · pushed 2026-02-07 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/girste/mcp-cybersec-watchdog.git`</sub>
- **[atomicchonk/roadrecon_mcp_server](https://github.com/atomicchonk/roadrecon_mcp_server)** — MCP server for analyzing ROADrecon gather results from Azure tenant enumeration
  <sub>★ 52 · Python · MIT · source · pushed 2025-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/atomicchonk/roadrecon_mcp_server.git`</sub>
- **[Gaffx/volatility-mcp](https://github.com/Gaffx/volatility-mcp)** — MCP server for Volatility 3.x, allowing you to perform memory forensics analysis with AI assistant. Experience memory forensics without barriers as plugins like pslist and netscan become accessible through clean REST APIs and LLMs
  <sub>★ 52 · Python · Apache-2.0 · source · pushed 2025-07-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Gaffx/volatility-mcp.git`</sub>
- **[BurtTheCoder/mcp-dnstwist](https://github.com/w0h1v/mcp-dnstwist)** — MCP server for dnstwist, a powerful DNS fuzzing tool that helps detect typosquatting, phishing, and corporate espionage
  <sub>★ 51 · JavaScript · MIT · npm · pushed 2025-03-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-dnstwist`</sub>
- **[fr0gger/MCP_Security](https://github.com/fr0gger/MCP_Security)** — MCP server for querying the ORKL API. This server provides tools for fetching threat reports, analyzing threat actors, and retrieving intelligence sources
  <sub>★ 51 · Python · source · pushed 2025-01-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fr0gger/MCP_Security.git`</sub>
- **[panther-labs/mcp-panther](https://github.com/panther-labs/mcp-panther)** — MCP server that enables security professionals to interact with Panther's SIEM platform using natural language for writing detections, querying logs, and managing alerts
  <sub>★ 47 · Python · Apache-2.0 · source · pushed 2026-09-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/panther-labs/mcp-panther.git`</sub>
- **[Synvoya/codeinspectus](https://github.com/Synvoya/codeinspectus)** — Local-first, zero-egress security scanner for AI-generated / "vibe-coded" JS/TS. Bundles Opengrep, Gitleaks &amp; Trivy behind one CWE-keyed schema and adds AI-code-specific checks (client-side secret exposure, Supabase RLS, prompt-injection &amp; LLM-output XSS sinks). No account, no telemetry
  <sub>★ 47 · TypeScript · Apache-2.0 · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx codeinspectus setup`</sub>
- **[firstorderai/authenticator_mcp](https://github.com/firstorderai/authenticator_mcp)** — A secure MCP (Model Context Protocol) server that enables AI agents to interact with the Authenticator App
  <sub>★ 45 · TypeScript · MIT · source · pushed 2026-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/firstorderai/authenticator_mcp.git`</sub>
- **[slouchd/cyberchef-api-mcp-server](https://github.com/slouchd/cyberchef-api-mcp-server)** — MCP server for interacting with the CyberChef server API which will allow an MCP client to utilise the CyberChef operations
  <sub>★ 44 · Python · MIT · source · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/slouchd/cyberchef-api-mcp-server.git`</sub>
- **[StacklokLabs/osv-mcp](https://github.com/StacklokLabs/osv-mcp)** — Access the OSV (Open Source Vulnerabilities) database for vulnerability information. Query vulnerabilities by package version or commit, batch query multiple packages, and get detailed vulnerability information by ID
  <sub>★ 42 · Go · Apache-2.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/StacklokLabs/osv-mcp.git`</sub>
- **[hieutran/entraid-mcp-server](https://github.com/hieuttmmo/entraid-mcp-server)** — A MCP server for Microsoft Entra ID (Azure AD) directory, user, group, device, sign-in, and security operations via Microsoft Graph Python SDK
  <sub>★ 41 · Python · source · pushed 2025-05-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hieuttmmo/entraid-mcp-server.git`</sub>
- **[arian-gogani/nobulex](https://github.com/arian-gogani/nobulex)** — Proof-of-behavior enforcement for AI agents. Define behavioral covenant rules (permit/forbid/require), enforce at runtime before execution, get SHA-256 hash-chained tamper-evident audit logs, and verify compliance independently. Cross-agent verification handshake — no proof, no transaction. MIT licensed, 4,244 tests
  <sub>★ 40 · TypeScript · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install nobulex`</sub>
- **[UPinar/contrastapi](https://github.com/UPinar/contrastapi)** — Security intelligence API with 31 MCP tools for CVE/EPSS/KEV lookup, domain recon (DNS/WHOIS/SSL/subdomains/CT logs), IOC/threat intel, OSINT (email/phone/username), and code security scanning (secrets, injection). Free 100 req/hr
  <sub>★ 34 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install contrastapi # Python 3.10+ — sync + async, typed responses, shortcut helpers`</sub>
- **[msaad00/agent-bom](https://github.com/msaad00/agent-bom)** — AI supply chain security scanner with 18 MCP tools. Auto-discovers 20 MCP clients, scans dependencies for CVEs (OSV/NVD/EPSS/CISA KEV), maps blast radius from vulnerabilities to exposed credentials and tools, runs CIS benchmarks, generates CycloneDX/SPDX SBOMs, and enforces compliance across OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF, and EU AI Act
  <sub>★ 31 · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx agent-bom check requests@2.33.0 --ecosystem pypi`</sub>
- **[nickpending/mcp-recon](https://github.com/nickpending/mcp-recon)** — Conversational recon interface and MCP server powered by httpx and asnmap. Supports various reconnaissance levels for domain analysis, security header inspection, certificate analysis, and ASN lookup
  <sub>★ 30 · Go · clone · pushed 2025-04-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/nickpending/mcp-recon.git`</sub>
- **[gaoharimran29-glitch/Cybersecurity-MCP-Server](https://github.com/AynOps/AynOps)** — Cybersecurity reconnaissance server for Claude. WHOIS lookup, DNS enumeration with subdomain brute-forcing, Nmap port scanning with service detection, SSL/TLS certificate inspection, technology stack fingerprinting, CVE lookup, and IP reputation checking. Runs fully locally via FastMCP
  <sub>★ 27 · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/gaoharimran29-glitch/Cybersecurity-MCP-Server.git`</sub>
- **[intruder-io/intruder-mcp](https://github.com/intruder-io/intruder-mcp)** — MCP server to access Intruder, helping you identify, understand, and fix security vulnerabilities in your infrastructure
  <sub>★ 26 · Python · BSD-3-Clause · source · pushed 2026-04-28 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/intruder-io/intruder-mcp.git`</sub>
- **[operantlabs/operant-mcp](https://github.com/operantlabs/operant-mcp)** — Security testing MCP server with 51 tools for penetration testing, network forensics, memory analysis, and vulnerability assessment
  <sub>★ 23 · TypeScript · MIT · npm · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g operant-mcp`</sub>
- **[AIM-Intelligence/AIM-Guard-MCP](https://github.com/AIM-Intelligence/AIM-MCP)** — Security-focused MCP server that provides safety guidelines and content analysis for AI agents
  <sub>★ 22 · TypeScript · ISC · npm · pushed 2025-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g aim-guard-mcp`</sub>
- **[pullkitsan/mobsf-mcp-server](https://github.com/pullkitsan/mobsf-mcp-server)** — A MCP server for MobSF which can be used for static and dynamic analysis of Android and iOS application
  <sub>★ 22 · TypeScript · MIT · source · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pullkitsan/mobsf-mcp-server.git`</sub>
- **[CTRLRun/ctrlrun](https://github.com/CTRLRun/ctrlrun)** — Execution safety for AI agent actions. ctrlrun mcp-operator exposes the approval queue as tools (list_pending_approvals, approve, deny, resolve, plus receipts, effects, stats and inspect_action), so the human who has to answer a held action answers it from the assistant they are already in; read tools answer without a credential and write tools refuse without one that names a person. Separately, t
  <sub>★ 22 · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ctrlrun`</sub>
- **[co-browser/attestable-mcp-server](https://github.com/kontext-security/attestable-mcp-server)** — An MCP server running inside a trusted execution environment (TEE) via Gramine, showcasing remote attestation using RA-TLS. This allows an MCP client to verify the server before conencting
  <sub>★ 21 · Python · docker · pushed 2026-05-20 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 --rm gsc-attestable-mcp-server`</sub>
- **[agentward-ai/agentward](https://github.com/agentward-ai/agentward)** — Permission control plane for AI agents. MCP proxy that enforces least-privilege YAML policies on every tool call, classifies sensitive data (PII/PHI), detects dangerous skill chains, and generates compliance audit trails. Supports stdio and HTTP proxy modes
  <sub>★ 19 · Python · pip · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentward`</sub>
- **[doublegate/CyberChef-MCP](https://github.com/doublegate/CyberChef-MCP)** — GCHQ CyberChef's 504 data-transformation operations as MCP tools — encryption, encoding, compression and forensics — plus 19 analysis tools for work a single operation cannot express, such as hash identification, RSA and ECDSA attacks, XOR key-length recovery, cipher solving, X.509 chain validation and NIST post-quantum identification (ML-KEM/ML-DSA/SLH-DSA). Runs in-process with no separate servi
  <sub>★ 19 · JavaScript · GPL-3.0 · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g cyberchef-mcp`</sub>
- **[ajipurn/fida](https://github.com/ajipurn/fida)** — Local-first MCP gateway for coding agents that redacts detected secrets from file reads and command output before they reach model context
  <sub>★ 18 · Rust · MIT · cargo · pushed 2026-06-28 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --git https://github.com/ajipurn/fida fida-cli`</sub>
- **[mastyf-ai/mastyf.ai](https://github.com/mastyf-ai/mastyf.ai)** — Open-source runtime security proxy for MCP. Transparently intercepts every tools/call through an 18-class attack defense pipeline (prompt injection, SSRF, shell injection, SQL injection, credential exfil, polyglot attacks) with a YAML policy engine and 304-entry adversarial corpus. Trust scoring for npm MCP packages with 0-100 badges. Cloud dashboard, Docker image, Python SDK. MIT
  <sub>★ 18 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mastyf-ai/mastyf.ai.git`</sub>
- **[Chimera-Protocol/csl-core](https://github.com/Chimera-Protocol/csl-core)** — Deterministic AI safety policy engine with Z3 formal verification. Write, verify, and enforce machine-verifiable constraints for AI agents via MCP
  <sub>★ 17 · Python · Apache-2.0 · pip · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install csl-core`</sub>
- **[icoretech/warden-mcp](https://github.com/icoretech/warden-mcp)** — MCP server for Bitwarden and Vaultwarden vault management. Search, create, edit, and organize logins, notes, cards, identities, SSH keys, folders, collections, attachments, and Sends via the official bw CLI
  <sub>★ 17 · TypeScript · MIT · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @bitwarden/cli@2026.8.0`</sub>
- **[jyjune/mcp_vms](https://github.com/jyjune/mcp_vms)** — A Model Context Protocol (MCP) server designed to connect to a CCTV recording program (VMS) to retrieve recorded and live video streams. It also provides tools to control the VMS software, such as showing live or playback dialogs for specific channels at specified times
  <sub>★ 17 · Python · MIT · source · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jyjune/mcp_vms.git`</sub>
- **[Acacian/aegis](https://github.com/Acacian/aegis)** — Policy-based governance for AI agent tool calls. YAML policies, approval gates, risk assessment, and audit logging. Cross-platform: LangChain, OpenAI, Anthropic, MCP
  <sub>★ 16 · Python · MIT · pip · pushed 2026-08-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install agent-aegis`</sub>
- **[gbrigandi/mcp-server-cortex](https://github.com/gbrigandi/mcp-server-cortex)** — A Rust-based MCP server to integrate Cortex, enabling observable analysis and automated security responses through AI
  <sub>★ 16 · Rust · MIT · source · pushed 2025-12-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/gbrigandi/mcp-server-cortex.git`</sub>
- **[mopanc/depguard](https://github.com/mopanc/depguard)** — Pre-install guardian for npm packages with static code analysis, supply-chain attack detection, vulnerability audit (npm + GitHub Advisory Database), AI hallucination guard, and CycloneDX 1.6 SBOM generation with VEX. 28 MCP tools. Zero runtime dependencies — the SBOM serializer is implemented natively against the public CycloneDX schema
  <sub>★ 16 · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g depguard-cli # or use directly with npx`</sub>
- **[jimmyracheta/AI-Runtime-Guard](https://github.com/runtimeguard/runtime-guard)** — Runtime policy enforcement for AI agents - prevents accidental damage to your systems, unauthorized agent access and automates backup-before-write for any touched files
  <sub>★ 15 · Python · MIT · pipx · pushed 2026-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install ai-runtime-guard`</sub>
- **[mcp-hangar/mcp-hangar](https://github.com/mcp-hangar/mcp-hangar)** — The policy enforcement plane for MCP -- deterministic admission and egress policy, attributable audit, and SIEM export for your MCP server fleet. MIT, self-hosted, no SaaS
  <sub>★ 15 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-hangar`</sub>
- **[creatorrmode-lead/avp-sdk](https://github.com/agentveil-protocol/agentveil-sdk)** — Trust, identity (W3C DID), and EigenTrust reputation for AI agents. Attestations, disputes, sybil detection, IPFS audit anchoring
  <sub>★ 15 · Python · MIT · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentveil-mcp-proxy`</sub>
- **[gbrigandi/mcp-server-thehive](https://github.com/gbrigandi/mcp-server-thehive)** — A Rust-based MCP server to integrate TheHive, facilitating collaborative security incident response and case management via AI
  <sub>★ 15 · Rust · MIT · source · pushed 2025-12-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/gbrigandi/mcp-server-thehive.git`</sub>
- **[sgateway/s-gw](https://github.com/sgateway/s-gw)** — Local credential approval and execution gateway for AI coding agents. Agents receive typed handles instead of raw API tokens, SSH keys, and cloud credentials; one-time approvals bind the credential, command, arguments, working directory, environment bindings, and target. Injects credentials only into the approved child process, sanitizes output, and records a local audit trail. Install with npm in
  <sub>★ 15 · TypeScript · Apache-2.0 · npm · pushed 2026-09-19 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g @s-gw/s-gw`</sub>
- **[getaegis/aegis](https://github.com/getaegis/aegis)** — Credential isolation proxy for AI agents. Injects secrets at the network boundary with domain restrictions, agent authentication, and audit logging. No SDK required — works as a transparent HTTP proxy or MCP server
  <sub>★ 14 · TypeScript · Apache-2.0 · npm · pushed 2026-08-06 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @getaegis/cli`</sub>
- **[HaroldFinchIFT/vuln-nist-mcp-server](https://github.com/HaroldFinchIFT/vuln-nist-mcp-server)** — A Model Context Protocol (MCP) server for querying NIST National Vulnerability Database (NVD) API endpoints
  <sub>★ 14 · Python · MIT · docker · pushed 2025-09-23 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -it vuln-nist-mcp-server`</sub>
- **[sidclawhq/platform](https://github.com/sidclawhq/platform)** — Governance proxy for MCP servers. Wraps any upstream server with policy evaluation, human approval workflows, and hash-chain audit trails. 18+ framework integrations. Apache 2.0 SDK
  <sub>★ 14 · TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx sidclaw-demo`</sub>
- **[sint-ai/sint-protocol](https://github.com/sint-ai/sint-protocol)** — Security-first MCP governance proxy (sint-mcp) with capability tokens, T0-T3 approval tiers, fail-closed execution, and tamper-evident audit receipts. Includes a separate sint-scan CLI for preflight MCP tool-risk audits
  <sub>★ 14 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y sint-mcp --stdio`</sub>
- **[loglux/authmcp-gateway](https://github.com/loglux/authmcp-gateway)** — glama 🐍 ☁️ 🏠 🍎 🪟 🐧 - Auth proxy for MCP servers: OAuth2 + DCR, JWT, RBAC, rate limiting, multi-server aggregation, and monitoring dashboard
  <sub>★ 12 · Python · MIT · pip · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install authmcp-gateway`</sub>
- **[AperionAI/shield](https://github.com/AperionAI/shield)** — Local guardrail proxy for AI coding agents. Wraps any MCP server (stdio or Streamable HTTP) and blocks destructive tool calls — DROP TABLE, rm -rf, force-push — before they execute. MCP supply-chain protection: TOFU tool-catalog pinning against rug pulls, plus tool-description and tool-result scanning for tool poisoning and prompt injection. 51 starter rules, approval gates, audit logging. Single
  <sub>★ 11 · Rust · cargo · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install aperion-shield`</sub>
- **[quantakrypto/pqc-tools](https://github.com/quantakrypto/pqc-tools)** — Post-quantum readiness for AI coding agents: scan code for quantum-vulnerable cryptography (RSA/ECDH/ECDSA/DH), explain the harvest-now-decrypt-later exposure, get NIST ML-KEM/ML-DSA/SLH-DSA (and hybrid) migration guidance, verify fixes, and check dependencies. Content-based/advisory tools only. Run local (npx @quantakrypto/mcp) or the hosted OAuth endpoint at mcp.quantakrypto.com
  <sub>★ 11 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @quantakrypto/sieve --impl "node ./my-impl.js" --param ml-kem-768`</sub>
- **[coreyhines/opnsense-mcp](https://github.com/coreyhines/opnsense-mcp)** — OPNsense firewall operations via API. Query ARP, DHCP, firewall rules, logs, interfaces, system status, and packet capture via STDIO or SSE
  <sub>★ 10 · Python · MIT · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/coreyhines/opnsense-mcp.git`</sub>
- **[forest6511/secretctl](https://github.com/forest6511/secretctl)** — AI-safe secrets manager with MCP integration. Run commands with credentials injected as environment variables - AI agents never see plaintext secrets. Features output sanitization, AES-256-GCM encryption, and Argon2id key derivation
  <sub>★ 10 · Go · Apache-2.0 · clone · pushed 2026-01-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/forest6511/secretctl.git`</sub>
- **[Rul1an/assay](https://github.com/Rul1an/assay)** — Policy-as-code gate for MCP. A fail-closed proxy that denies risky tool calls before they run, produces offline-verifiable evidence bundles of what executed, and enforces IPv4/TCP egress in-kernel via eBPF/LSM and Landlock on Linux. Deterministic and offline-first
  <sub>★ 10 · Rust · MIT · cargo · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`cargo install assay-cli --version 6.6.2 --locked`</sub>
- **[tomjwxf/scopeblind-gateway](https://github.com/tomjwxf/scopeblind-gateway)** — Security gateway that wraps any MCP server with per-tool policies, approval gates, and optional Ed25519-signed receipts. Shadow mode logs every tool call; enforce mode blocks, rate-limits, or requires approval
  <sub>★ 10 · TypeScript · MIT · npx · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @scopeblind/passport wrap --runtime openclaw --config ./openclaw.json --policy email-safe`</sub>
- **[takleb3rry/zitadel-mcp](https://github.com/takleb3rry/zitadel-mcp)** — MCP server for Zitadel identity management — manage users, projects, OIDC apps, roles, and service accounts through natural language
  <sub>★ 10 · TypeScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/takleb3rry/zitadel-mcp.git`</sub>
- **[sanyambassi/ciphertrust-manager-mcp-server](https://github.com/sanyambassi/ciphertrust-manager-mcp-server)** — MCP server for Thales CipherTrust Manager integration, enabling secure key management, cryptographic operations, and compliance monitoring through AI assistants
  <sub>★ 9 · Python · MIT · npx · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv run --no-sync ciphertrust-mcp-server`</sub>
- **[OrygnsCode/opa-mcp-server](https://github.com/OrygnsCode/opa-mcp-server)** — Open Policy Agent (OPA) and Rego policy toolkit. 32 tools spanning authoring (format, lint, check, deps), evaluation (eval, test, bench, coverage), and OPA REST control (policies, data, decisions, compile). Wraps the OPA CLI and the Regal linter, with AI-assisted helpers for explaining decisions, generating test skeletons, and suggesting fixes
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-09-10 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @orygn/opa-mcp`</sub>
- **[zyx77550/sparda](https://github.com/zakariagharzouli/sparda)** — Injects a live, reversible MCP server into a running Express / FastAPI / Next.js app — reads safe by default, writes gated behind human confirmation. The same engine also proves deploys and PRs (apocalypse / review)
  <sub>★ 8 · JavaScript · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sparda-mcp apocalypse # prove the tree is safe to deploy — exit 1 on any real risk, or on an unverified premise`</sub>
- **[yessGlory17/job-verify](https://github.com/yessGlory17/job-verify)** — Check whether a recruiter or job offer is a scam before you reply. Extracts entities (company, links, email, phone, wallets) from a pasted message and cross-checks company registration, domain age, look-alike/typosquat domains, phishing &amp; malware blocklists, email deliverability, crypto-scam databases, and Internet Archive history — free OSINT, no API keys
  <sub>★ 8 · Python · MIT · source · pushed 2026-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yessGlory17/job-verify.git`</sub>
- **[luiacuaniello/perspectivegraph](https://github.com/luiacuaniello/perspectivegraph)** — Attack-path engine for cloud and Kubernetes. Eight read-only tools let an agent list the reachable routes from internet exposure to sensitive assets, explain each hop and the evidence behind its probability, find choke points, and simulate cutting a relationship before recommending the fix. Connects to a running PerspectiveGraph: perspectivegraph mcp --api http://localhost:8080
  <sub>★ 7 · Go · Apache-2.0 · helm · pushed 2026-09-22 · macOS</sub>
  <sub>`helm install perspectivegraph oci://ghcr.io/luiacuaniello/charts/perspectivegraph \`</sub>
- **[P4ST4S/mcp-audit](https://github.com/P4ST4S/mcp-audit)** — Transparent Go proxy that intercepts, signs, rate-limits, redacts, and audits all MCP JSON-RPC tool calls without modifying client or server
  <sub>★ 7 · Go · Apache-2.0 · go · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/P4ST4S/mcp-audit/cmd/mcp-audit@latest`</sub>
- **[piiiico/proof-of-commitment](https://github.com/piiiico/proof-of-commitment)** — Supply chain risk scoring for npm, PyPI, Cargo, and Go packages. 9 tools for behavioral trust signals — publisher depth, release consistency, maintenance patterns. Both axios and node-ipc scored CRITICAL before they got attacked. Free CLI, CI gate, REST API. No API key required
  <sub>★ 7 · TypeScript · MIT · npm · pushed 2026-07-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g proof-of-commitment # then:`</sub>
- **[velvetway/minreestr-mcp](https://github.com/velvetway/minreestr-mcp)** — Search каталогпо.рф (Russian software registry, 26k+ products) for import-substitution and ФСТЭК/ФСБ-certified software discovery. Three tools: full-text search, manufacturer listing, featured products. Ideal for Russian security/compliance teams (152-ФЗ, 187-ФЗ) using Claude
  <sub>★ 7 · Python · MIT · pip · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install minreestr-mcp`</sub>
- **[taniwhaai/arai](https://github.com/taniwhaai/arai)** — Policy enforcement for AI coding agents derived from existing instruction files (CLAUDE.md, .cursorrules, .windsurfrules, .github/copilot-instructions.md) — no separate YAML to maintain. Rules with prohibitive predicates (never, forbids, must_not) emit permissionDecision: deny to block tool calls in Claude Code; advisory rules inject context. PostToolUse is correlated with PreToolUse to produce pe
  <sub>★ 7 · Rust · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g @taniwhaai/arai`</sub>
- **[urldna/mcp](https://github.com/urldna/mcp)** — MCP server for automated URL scanning and forensic phishing triage. Captures full DOM snapshots, network requests, and visual screenshots to identify malicious redirects and infrastructure. Supports historical threat hunting using Custom Query Language (CQL) to map actor patterns across millions of recorded scans
  <sub>★ 7 · Python · Apache-2.0 · docker · pushed 2026-08-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 8080:8080 -e x-api-key=<URLDNA_API_KEY> urldna-mcp-server`</sub>
- **[Gowthaman90/mcp-bastion](https://github.com/Gowthaman90/mcp-bastion)** — Reliability + security proxy that sits in front of MCP servers: TOFU tool-definition pinning against rug pulls, tool-poisoning and cross-server-exfiltration detection, argument/command-injection blocking, inline secret redaction, MCP 2026-07-28 header/body validation (-32020) and cache-policy clamping, and a compliance-mapped audit trail (NIST AI RMF / OWASP). Coverage measured on an open benchmar
  <sub>★ 6 · TypeScript · Apache-2.0 · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Gowthaman90/mcp-bastion.git`</sub>
- **[rad-security/mcp-server](https://github.com/rad-security/mcp-server)** — MCP server for RAD Security, providing AI-powered security insights for Kubernetes and cloud environments. This server provides tools for querying the Rad Security API and retrieving security findings, reports, runtime data and many more
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-09-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rad-security/mcp-server.git`</sub>
- **[MARUCIE/authbox](https://github.com/MARUCIE/authbox)** — Zero-knowledge password manager with MCP credential gateway. BIP-39 seed phrase recovery, deterministic passwords, policy-gated AI agent access (scope, rate limits, time windows, step-up approval), 70+ API key providers, and hash-chain audit trail. Go + Next.js + TypeScript
  <sub>★ 5 · HTML · MIT · source · pushed 2026-06-18 · Win?</sub>
  <sub>`git clone https://github.com/MARUCIE/authbox.git`</sub>
- **[goklab/guardvibe](https://github.com/goklab/guardvibe)** — Security MCP for vibe coding with 330 rules and 29 tools. Purpose-built for AI-generated code — scans Next.js, Supabase, Clerk, Stripe, Prisma, Hono, GraphQL, and 25+ modules. Cross-file taint analysis, host security audit, auto-fix, SARIF export, pre-commit hook, and CVE version detection. Zero config, runs locally
  <sub>★ 5 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx guardvibe init claude`</sub>
- **[I4cTime/quantum_ring](https://github.com/I4cTime/q-ring)** — Quantum-inspired keyring for AI coding agents. Secure secrets with superposition, entanglement, tunneling, and teleportation
  <sub>★ 5 · TypeScript · AGPL-3.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pnpm add -g @i4ctime/q-ring`</sub>
- **[scalekit-inc/scalekit-mcp-server](https://github.com/scalekit-inc/scalekit-mcp-server)** — Hosted Scalekit MCP. Manage orgs, users, and SSO from the agent. https://mcp.scalekit.com
  <sub>★ 5 · TypeScript · Apache-2.0 · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scalekit-inc/scalekit-mcp-server.git`</sub>
- **[sekera-radim/impri](https://github.com/sekera-radim/impri)** — Human-in-the-loop approval inbox for AI agents. An agent submits a proposed action (send email, post comment, run a command) via impri_push_action, a human approves, rejects, or edits it from a web, mobile, or Slack/Discord/Telegram inbox, and the agent only proceeds on an approved decision. The gate is a data dependency, not a prompt. Full audit trail, self-hostable (MIT, Docker Compose). npx @im
  <sub>★ 5 · HTML · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @impri/mcp`</sub>
- **[ScopeBlind/verify-mcp](https://github.com/ScopeBlind/verify-mcp)** — Offline verification of signed artifacts -- receipts, manifests, audit bundles. Ed25519 + JCS. No accounts, no API calls. Apache-2.0
  <sub>★ 5 · JavaScript · Apache-2.0 · npm · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @scopeblind/verify-mcp`</sub>
- **[aeoess/agent-passport-mcp](https://github.com/aeoess/agent-passport-mcp)** — Agent identity, scoped delegation, and governance: issue passports, build and verify narrowing-only delegation chains, enforce policy at a gateway, and emit signed admission and outcome records. 150 tools. npx -y agent-passport-system-mcp
  <sub>★ 4 · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-passport-system-mcp`</sub>
- **[AgentAvow/AgentAvow](https://github.com/AgentAvow/AgentAvow)** — Signed, independently-recomputable safety scores for the MCP servers, packages, and tools an agent connects to: a 0–100 score plus an Ed25519/JWS attestation you can recompute offline against a public JWKS, a README badge, and a GitHub Action to gate CI merges on a minimum score. Free, no account (formerly agentgraph-co/agentgraph)
  <sub>★ 4 · Python · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install agentavow-trust`</sub>
- **[behrensd/mcp-firewall](https://github.com/behrensd/mcpwall)** — Deterministic security proxy (iptables for MCP) that intercepts tool calls, enforces YAML policies, scans for secret leakage, and logs everything. No AI, no cloud
  <sub>★ 4 · TypeScript · Apache-2.0 · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcpwall`</sub>
- **[Buggy1111/anonymize-mcp](https://github.com/Buggy1111/anonymize-mcp)** — Anonymize PII and redact text for GDPR across Czech and 35+ languages. Real NLP via ÚFAL/LINDAT (MasKIT + NameTag NER, not just regex), 80+ PII patterns, plus morphology, translation, and spellcheck. Czech-first, non-commercial. Install: pip install anonymize-mcp
  <sub>★ 4 · Python · pip · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install anonymize-mcp`</sub>
- **[cyntrisec/cyntrisec-cli](https://github.com/cyntrisec/cyntrisec-cli)** — Local-first AWS security analyzer that discovers attack paths and generates remediations using graph theory
  <sub>★ 4 · Python · Apache-2.0 · pip · pushed 2026-05-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install cyntrisec`</sub>
- **[jonnybottles/patch-tuesday-mcp](https://github.com/jonnybottles/patch-tuesday-mcp)** — Microsoft Patch Tuesday triage from the official MSRC Security Update Guide. Monthly rollups, CVE/KB lookups, supersedence chains, product watchlists, and urgency-ranked results enriched with EPSS scores and the CISA KEV catalog. No API keys; also available as a free hosted remote endpoint. uvx patch-tuesday-mcp
  <sub>★ 4 · Python · uv · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx patch-tuesday-mcp`</sub>
- **[MoltyCel/moltrust-mcp-server](https://github.com/MoltyCel/moltrust-mcp-server)** — Trust infrastructure for AI agents — register DIDs, verify identities, query reputation scores, rate agents, manage W3C Verifiable Credentials, and handle USDC credit deposits on Base
  <sub>★ 4 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install moltrust-mcp-server`</sub>
- **[toan203/osv-ui](https://github.com/toan203/osv-ui)** — Visual CVE audit dashboard for npm, Python, Go, and Rust. Scan from Claude/Cursor, opens a browser UI for human review (human-in-the-loop), applies fixes with explicit confirmation. Powered by OSV.dev
  <sub>★ 4 · HTML · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx osv-ui`</sub>
- **[layervai/qurl-mcp](https://github.com/layervai/qurl-mcp)** — Mint, resolve, audit, and rotate expiring scope-limited access links (qURLs) for AI agents — secure URL gateway for the qURL API. 9 tools (create / resolve / list / get / delete / extend / update / mint-link / batch-create), 3 resources, 3 guided prompts. stdio transport, OIDC-attested npm provenance
  <sub>★ 4 · TypeScript · MIT · docker · pushed 2026-09-21 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i -e QURL_API_KEY=lv_live_xxx qurl-mcp`</sub>
- **[nagameTW/mcp-server-malcolm](https://github.com/nagameTW/mcp-server-malcolm)** — The first MCP server for Malcolm, the open-source network traffic analysis suite (Zeek + Suricata + Arkime + OpenSearch + NetBox). Gives AI agents structured, threat-hunting access: search and aggregate traffic, discover fields, query Suricata alerts, browse Arkime sessions, and resolve NetBox assets. Read-only by default; opt-in, audited write classes for alerts, tagging, hunts, and PCAP upload.
  <sub>★ 3 · Python · MIT · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from /path/to/mcp-server-malcolm mcp-server-malcolm`</sub>
- **[kent-tokyo/shohei](https://github.com/kent-tokyo/shohei)** — Rust infrastructure diagnostics MCP server for AI agents: DNS checks, TLS certificate chain inspection, email security, global DNS propagation, and DNS latency benchmarking
  <sub>★ 3 · Rust · MIT · cargo · pushed 2026-06-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install shohei`</sub>
- **[adeptus-innovatio/solvitor-mcp](https://github.com/Adeptus-Innovatio/solvitor-mcp)** — Solvitor MCP server provides tools to access reverse engineering tools that help developers extract IDL files from closed-source Solana smart contracts and decompile them
  <sub>★ 3 · Rust · cargo · pushed 2025-10-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`cargo install solvitor-mcp`</sub>
- **[rudraneel93/mcp-guardian](https://github.com/rudraneel93/mcp-guardian)** — Security and governance proxy for MCP infrastructure. Enforces YAML-configurable policies (blocklists, rate limits, token budgets), tracks real token costs via tiktoken, monitors server health with live JSON-RPC probes. Features include OAuth 2.1/OIDC with RBAC, web dashboard with Prometheus metrics, payload normalization against encoding bypasses, semantic shell AST analysis, mTLS zero-trust netw
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @mcp-guardian/server@latest`</sub>
- **[datanexusmcp/mcp-server](https://github.com/datanexusmcp/mcp-server)** — 55 tools for verified public data lookups — CVE/SBOM security audits, licence compliance, patents, federal contracts, NPI provider lookups, nonprofit 990 filings, and domain intelligence. No API key required
  <sub>★ 3 · Python · npx · pushed 2026-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @datanexusmcp/mcp-server`</sub>
- **[inkog-io/inkog-mcp](https://github.com/inkog-io/inkog-mcp)** — AI agent security scanner. Audits MCP servers for vulnerabilities, detects prompt injection, infinite loops, token bombing, and missing human oversight across 20+ frameworks. Maps findings to EU AI Act, OWASP LLM Top 10
  <sub>★ 3 · TypeScript · Apache-2.0 · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @inkog-io/mcp`</sub>
- **[sanyambassi/thales-cdsp-cakm-mcp-server](https://github.com/sanyambassi/thales-cdsp-cakm-mcp-server)** — MCP server for Thales CDSP CAKM integration, enabling secure key management, cryptographic operations, and compliance monitoring through AI assistants for Ms SQL and Oracle Databases
  <sub>★ 3 · Python · MIT · clone · pushed 2025-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sanyambassi/thales-cdsp-cakm-mcp-server.git`</sub>
- **[sanyambassi/thales-cdsp-crdp-mcp-server](https://github.com/sanyambassi/thales-cdsp-crdp-mcp-server)** — MCP server for Thales CipherTrust Manager RestFul Data Protection service
  <sub>★ 3 · JavaScript · MIT · clone · pushed 2025-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sanyambassi/thales-cdsp-crdp-mcp-server.git`</sub>
- **[Skyrxin/sast-mcp-server](https://github.com/Skyrxin/sast-mcp-server)** — SAST/DAST server exposing 11 security scanners (Bandit, Semgrep, Trivy, CodeQL, Checkov, Gitleaks, OSV-Scanner, Grype, OWASP ZAP, and more) with closed-loop remediation (scan→patch→re-scan→verify), SARIF/SBOM/VEX export, compliance reporting, and CI integrations (GitHub Advanced Security, DefectDojo, Slack, Jira)
  <sub>★ 3 · Python · MIT · uv · pushed 2026-06-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx sast-mcp-server # run without installing`</sub>
- **[UnboundCompute/lachesis](https://github.com/UnboundCompute/lachesis)** — Compiler-precise code property graph for C, Python, and TypeScript, navigable over MCP. Exposes callers/callees, data- and taint-flow with source→sink witnesses, points-to, and guard/sink structure so an agent can reason about how a value moves and where it reaches a sink unguarded — not just where a name appears. Zero-config: uvx --from lachesis-cpg lachesis-mcp
  <sub>★ 3 · Python · AGPL-3.0 · clone · pushed 2026-09-07 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/UnboundCompute/lachesis`</sub>
- **[shyshlakov/pci-dss-mcp](https://github.com/shyshlakov/pci-dss-mcp)** — PCI DSS v4.0.1 static-analysis MCP server for Go payment codebases. 12 scanners detect PAN/CVV exposure, weak crypto, missing audit logs, vulnerable deps, TLS misconfig, auth weaknesses, plus CycloneDX 1.6 SBOM generation - each finding mapped to the exact PCI requirement. AI-assisted triage via triage_findings. Keyless-signed multi-arch Docker image on ghcr.io
  <sub>★ 3 · Go · MIT · go · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/shyshlakov/pci-dss-mcp@latest`</sub>
- **[zw008/VMware-Harden](https://github.com/vmware-skills/VMware-Harden)** — VMware vSphere compliance and hardening — read-only baseline scanning plus drift detection across CIS, vSphere SCG, China DJCP 2.0, and PCI-DSS frameworks. 6 read-only tools with LLM-powered remediation suggestions (apply-side gated through vmware-pilot approval workflow)
  <sub>★ 3 · Python · MIT · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "vmware-harden[collectors]"`</sub>
- **[oleg-vdv/kepil](https://github.com/oleg-vdv/kepil)** — Accountability layer for AI agents: a passport per agent version, a per-job mandate (allowed actions and systems, spending limits, expiry), a fail-closed gate that checks every action before a model is called, and an append-only hash-chained journal verified by a separate implementation in another language. Irreversible actions stop and wait for a person: the server deliberately has no confirm too
  <sub>★ 3 · Python · AGPL-3.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install kepil`</sub>
- **[boy-offi9-inc/hexforge-gateway](https://github.com/boy-offi9-inc/hexforge-gateway)** — AI-assisted APK reverse-engineering workspace. Orchestrates jadx, apktool, adb, and frida as MCP agents through a Workflow engine, with a stdio MCP Server Frontend for Claude Desktop/Code/Cursor. Runs on Termux (Android) or PC; Supabase persistence is opt-in
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/boy-offi9-inc/hexforge-gateway.git`</sub>
- **[felixpg13-glitch/spendshield](https://github.com/felixpg13-glitch/spendshield)** — Payment guardrails for AI agents: spend-capped digital identity (KYA), dry-run / budget / amount-limit / approval gates, prompt-injection defense (new recipients &amp; large amounts require human sign-off), AES-encrypted secret vault with audited access, full audit trail. Python library + stdio MCP server. pip install spendshield
  <sub>★ 2 · Python · MIT · uv · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from spendshield spendshield-mcp`</sub>
- **[M2M-Sentinel/m2m-sentinel-sdk](https://github.com/M2M-Sentinel/m2m-sentinel-sdk)** — Deterministic EVM bytecode capability intelligence, EIP-1967 proxy resolution, gas recommendations, and preflight safety intelligence for autonomous agents on Base (Chain ID: 8453). Supports stdio and hosted SSE. npx -y m2m-sentinel-sdk
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli mcp add M2M-Sentinel/m2m-sentinel-sdk --client claude`</sub>
- **[moxno/privacyscrubber-mcp](https://github.com/moxno/privacyscrubber-mcp)** — Zero-trust local PII and secrets masking server for Cursor, Windsurf, and Claude Desktop. npx pii-masking-run
  <sub>★ 2 · JavaScript · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @privacyscrubber/mcp-server --write-to-clients`</sub>
- **[RoscoNL/intodns-mcp-server](https://github.com/RoscoNL/intodns-mcp-server)** — Free DNS and email security scanner for AI assistants. DNS, SPF, DKIM, DMARC, DNSSEC, MTA-STS, BIMI, TLS/STARTTLS, FCrDNS, CAA, TLSA/DANE, blacklist and full-deliverability checks, plus security-header/CSP analysis and bookmarkable report snapshots, via the IntoDNS.ai API. No signup or API key. npx intodns-mcp
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y intodns-mcp`</sub>
- **[honeylabshq/honeylabs-mcp](https://github.com/honeylabshq/honeylabs-mcp)** — Honeypot threat intelligence for AI agents: 90 days of probe data from a sensor network for IP reputation, scanner classification, CVE probing trends, and JA4/JA4H/HASSH fingerprints. Remote MCP, free tier
  <sub>★ 2 · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/honeylabshq/honeylabs-mcp.git`</sub>
- **[teodorofodocrispin-cmyk/trustboost-pii-sanitizer](https://github.com/teodorofodocrispin-cmyk/trustboost-api)** — PII sanitization layer for autonomous AI agent pipelines. Detects and redacts emails, phone numbers, national IDs, private keys, and financial data before text reaches LLMs. Supports EN, ES (LATAM), PT (BR/PT), DE, JA. Solana-native payments via Helius oracle
  <sub>★ 2 · Python · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/teodorofodocrispin-cmyk/trustboost-api.git`</sub>
- **[beeswaxpat/chronoverify-mcp](https://github.com/beeswaxpat/chronoverify-mcp)** — Verify a photo's capture time and provenance before an agent trusts it: cryptographic C2PA Content Credentials validation against the official trust lists, EXIF and XMP consistency checks, and classical pixel forensics fused into one typed verdict with a 0 to 100 confidence. Free keyless tier, opt-in shareable verdict permalinks, and key-gated signed PDF audit reports. Provenance validation, not a
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/beeswaxpat/chronoverify-mcp.git`</sub>
- **[AgentValet/AgentValet](https://github.com/AgentValet/AgentValet)** — Identity and credential governance broker for MCP servers. Issues scoped, short-lived credentials per agent to stop credential inheritance. Audit log, human approval gates, AIMS-aligned
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @agentvalet/register`</sub>
- **[9hannahnine-jpg/arc-gate-mcp](https://github.com/9hannahnine-jpg/arc-gate-mcp)** — Runtime governance for MCP tool calls. Blocks prompt injection and capability abuse before tool results reach your agent
  <sub>★ 2 · Python · pip · pushed 2026-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install arc-gate-mcp`</sub>
- **[airblackbox/air-blackbox-mcp](https://github.com/airblackbox/air-blackbox-mcp)** — EU AI Act compliance scanner for Python AI agents. Scans, analyzes, and remediates LangChain/CrewAI/AutoGen/OpenAI code across 6 articles with 10 tools including prompt injection detection, risk classification, and trust layer integration. The only MCP compliance server that generates fix code, not just findings
  <sub>★ 2 · Python · Apache-2.0 · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install air-blackbox-mcp`</sub>
- **[ark-forge/arkforge-mcp](https://github.com/ark-forge/arkforge-mcp)** — Third-party certifying proxy — sign any HTTP call (AI agents, webhooks, microservices) with an independent Ed25519 signature, RFC 3161 timestamp, and Sigstore Rekor anchor. Works with Claude, GPT-4, Mistral, LangChain, AutoGen, or any HTTP client
  <sub>★ 2 · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ark-forge/arkforge-mcp.git`</sub>
- **[mirajmahmudul/agentdevx-sdk](https://github.com/mirajmahmudul/agentdevx-sdk)** — Give your AI hands. Identity and credential vault gateway for autonomous agents. Ed25519 cryptographic identity (not OAuth), AES-256-GCM encrypted credential vault, OPA policy engine with full audit logging (captures allowed and denied actions), persistent per-agent memory, and web scraping tools. Self-bootstrapping — an agent can discover, register, and start calling tools with zero human setup.
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agentdevx/install`</sub>
- **[FoundryNet/mint-mcp](https://github.com/FoundryNet/mint-mcp)** — MINT Protocol — universal work attestation for autonomous agents. Cryptographically attest, verify, rate, and discover agent work to build portable, on-chain trust and reputation across the agent economy. 6 tools
  <sub>★ 2 · Python · pip · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mint-attest`</sub>
- **[Declade/lucairn-sdks](https://github.com/Declade/lucairn-sdks)** — Privacy-preserving AI gateway. Sanitises PII (German + English; Microsoft Presidio + custom recognisers) before prompts reach Anthropic / OpenAI / your LLM, then emits a signed cryptographic certificate per call (Ed25519 + RFC 3161 timestamp + Sigstore Rekor anchoring). EU GDPR + AI Act ready. Free tier 500 calls/month, BYOK. Install: npx -y @lucairn/mcp-server. Docs: https://lucairn.eu/developer/
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @lucairn/mcp-server`</sub>
- **[dnsdoctor/claude-plugin](https://github.com/dnsdoctor/claude-plugin)** — Scan and fix a domain's email authentication — SPF, DMARC, DKIM, MX, blacklists, domain/SSL expiry. Deterministic, validated fix records (never LLM-generated); hosted server at dnsdoctor.dev/mcp with anonymous access
  <sub>★ 2 · TypeScript · Apache-2.0 · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @dnsdoctor/mcp`</sub>
- **[eliottreich/taskbounty-check](https://github.com/eliottreich/taskbounty-check)** — Local-only GitHub Actions and CI maintenance scanner for AI-built apps. Exposes scan_repo, explain_finding, and generate_fix_plan to MCP clients; reads only allowlisted workflow and update configuration, modifies nothing, makes no outbound requests by default, and has zero runtime dependencies. Run with npx -y taskbounty-check@0.1.6 mcp
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-06-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y taskbounty-check@0.1.6 mcp`</sub>
- **[mrz1880/mcp-keycloak-admin](https://github.com/mrz1880/mcp-keycloak-admin)** — Administer Keycloak through its Admin REST API — users, roles, clients, groups, identity providers, federation and events. Safe by default: read-only mode, realm allow-list, and confirmation for destructive actions. npx -y mcp-keycloak-admin
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-keycloak-admin`</sub>
- **[muhannad-hash/mcp-shield](https://github.com/muhannad-hash/mcp-shield)** — Security scanner for MCP servers. Detects backdoors, exfiltration code, obfuscation, dangerous code execution, prompt injection, and supply chain risks before you install. Four tools: scan npm packages, scan local directories, check prompt injection, and audit supply chain trust score. npx @muhannad-hash/mcp-shield
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-shield`</sub>
- **[ppcvote/misp-mcp-server](https://github.com/ppcvote/misp-mcp-server)** — MISP (Malware Information Sharing Platform) MCP server with built-in prompt injection defense via prompt-defense-audit. 8 read-only threat-intel tools (events, attributes, search, tags, feeds, galaxies). Scans every MISP response for adversarial seeding before returning to LLM. Tracks MISP/MISP#10745. MIT
  <sub>★ 2 · TypeScript · MIT · npm · pushed 2026-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @ultralab/misp-mcp-server`</sub>
- **[Chronolapse411/sicarius-guard](https://github.com/Chronolapse411/sicarius-guard)** — Solana token safety oracle for AI agents and trading bots. Byte-level SPL mint analysis, honeypot detection, freeze/mint authority checks, Birdeye market enrichment, and composite risk scoring. Deployed on Google Cloud Run
  <sub>★ 2 · TypeScript · MIT · npx · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sicarius-guard`</sub>
- **[jstibal/openterms-mcp](https://github.com/jstibal/openterms-mcp)** — Ed25519-signed consent receipts and programmable policy engine for AI agents. Spending caps, action whitelists, escalation thresholds, and JWKS-backed provider verification. Independently verifiable
  <sub>★ 2 · Python · Apache-2.0 · source · pushed 2026-04-20 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/jstibal/openterms-mcp.git`</sub>
- **[WRG-11/wrg-sigma-rules](https://github.com/WRG-11/wrg-sigma-rules)** — Sigma detection rule writing, validation, and conversion (Splunk/Elastic/Kibana/Wazuh) via 3 MCP tools (draft_rule, validate_rule, convert_rule) backed by a 61-rule production corpus across 11 MITRE ATT&amp;CK tactic categories. Standalone server + Claude Code plugin distribution
  <sub>★ 2 · Python · MIT · pip · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install pysigma pysigma-backend-splunk pysigma-backend-elasticsearch`</sub>
- **[calllint/calllint](https://github.com/calllint/calllint)** — Pre-flight security linter for MCP servers, agent tools, and skills. Scans a config *before* it runs — offline, deterministic, evidence-backed — and returns SAFE / REVIEW / BLOCK / UNKNOWN verdicts without executing the server it judges. CLI (npx calllint scan), MCP server (npx calllint-mcp), SARIF + CI gate. UNKNOWN is never SAFE
  <sub>★ 2 · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g calllint`</sub>
- **[rudimentall1/agentic-wallet-guardian-v3](https://github.com/rudimentall1/agentic-wallet-guardian-v3)** — Self-hosted security and policy layer for AI agents interacting with blockchain wallets. Agents submit a proposed transaction/action and Guardian evaluates wallet, token, contract, threat-intelligence, simulation, policy and reputation signals before returning an explainable ALLOW / WARN / BLOCK decision. Includes an MCP stdio server, real RPC/Blockscout/DexScreener/GoPlus providers, transaction s
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/rudimentall1/agentic-wallet-guardian-v3.git`</sub>
- **[askalf/truecopy](https://github.com/askalf/truecopy)** — Supply-chain gate for agent skills and MCP servers — scans tool definitions for poisoned instructions, pins vetted servers by content hash in a committed lock, and verifies drift in CI; the bundled truecopy-mcp proxy exposes only pinned, unmodified tools from a live server
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @askalf/truecopy # latest, from npm`</sub>
- **[astafford8488/agentaegis-mcp](https://github.com/astafford8488/agentaegis-mcp)** — Security &amp; trust layer for AI agents. Scan an MCP server or skill *before* you install it (scan_mcp_plugin, scan_skill) — flags exfiltration, prompt-injection sinks, dangerous capabilities, install hooks and obfuscation → PROCEED/CAUTION/BLOCK. Plus vet_endpoint (endpoint safety verdict before an agent calls or pays it) and 25 more tools: vuln scans, threat intel, compliance (SOC 2/ISO 27001/HIPAA
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-08-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/astafford8488/agentaegis-mcp.git`</sub>
- **[Fronesis-Labs/dcl-webhook](https://github.com/Fronesis-Labs/dcl-webhook)** — Deterministic AI audit layer: evaluates LLM/agent outputs against configurable policies (jailbreak, safety, quality, wallet, trade, MEV compliance) and writes every verdict to a tamper-evident SHA-256 hash chain — metadata only, never raw content. 17 tools including a full crypto-trading compliance suite. Pay-per-call via x402 (USDC on Base), from $0.01. mcp.fronesislabs.com/mcp
  <sub>★ 1 · Python · Apache-2.0 · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Fronesis-Labs/dcl-webhook.git`</sub>
- **[qinisolabs/qiniso](https://github.com/qinisolabs/qiniso)** — 56 deterministic fact-checkers in one server (IBAN, VAT, VIN, GTIN/barcodes, national &amp; tax IDs, crypto addresses, phone, dates, holidays) — verify the structured facts an agent emits against checksums and curated data
  <sub>★ 1 · TypeScript · Apache-2.0 · source · pushed 2026-06-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/qinisolabs/qiniso.git`</sub>
- **[node-man/dechonet-mcp](https://github.com/node-man/dechonet-mcp)** — Domain security reconnaissance for AI agents. 13 tools — DNS + DNSSEC, SSL/TLS chain &amp; grade, HTTP security headers, SPF/DKIM/DMARC email auth, TCP port scan, ASN, RDAP/WHOIS — plus a one-shot security_scan returning a 0-100 Health Score (A–F). Free, no API key. npx -y dechonet-mcp
  <sub>★ 1 · JavaScript · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g dechonet-mcp`</sub>
- **[kakunin-ai/kakunin-mcp](https://github.com/kakunin-ai/kakunin-mcp)** — Compliance and identity for AI agents — verify an agent's certificate scope, read its behavioral risk score, and append to an immutable audit trail. X.509 identity issued via AWS KMS; MiCA / EU AI Act aligned. npx -y @kakunin/mcp
  <sub>★ 1 · TypeScript · Apache-2.0 · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @kakunin/mcp`</sub>
- **[srinivasan-sundaresan95/orihime](https://github.com/srinivasan-sundaresan95/orihime)** — Cross-repository code knowledge graph MCP server for Java, Kotlin, JavaScript, and TypeScript. Indexes source into embedded KuzuDB via tree-sitter; 30+ tools for call-flow tracing, multi-hop taint analysis (OWASP/CWE/PCI/STIG reports), entry-point reachability filtering, performance hotspot detection, and license compliance — without reading source files. 95% fewer tokens vs source-reading baselin
  <sub>★ 1 · Python · clone · pushed 2026-05-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/srinivasan-sundaresan95/orihime.git`</sub>
- **[suhui-organization/pod](https://github.com/suhui-organization/pod)** — Least-privilege compiler for AI agents. Run your agent in record-only mode, compile the smallest policy it actually needs from its real tool calls, enforce it at an MCP gateway (deny > approve > allow), and keep a SHA-256 hash-chained audit that verifies offline. curl -fsSL https://raw.githubusercontent.com/suhui-organization/pod/v0.3.2/scripts/install.sh | sh
  <sub>★ 1 · TypeScript · Apache-2.0 · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @podsec/cli`</sub>
- **[alexar76/aimarket-mcp](https://github.com/alexar76/aimarket-mcp)** — SSRF-hardened web gateway MCP — web_fetch, web_search, metis_verify; one audited security core for Metis, ARGUS, and the ecosystem. stdio + optional HTTP · Python · Glama · Registry io.github.alexar76/aimarket-mcp
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install aimarket-mcp`</sub>
- **[alexar76/argus](https://github.com/alexar76/argus)** — ARGUS-3 as a stdio MCP server (argus mcp → argus_ask, argus_status). WARDEN vets third-party MCP servers before any tool runs (LUMEN-scored firewall, tool-def pinning, drift sentinel). Distinct from aimarket-oracle-gateway (oracle tools) and aimarket-plugins (hub packager). npm @alexar76/argus3 · live
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g argus-warden@latest`</sub>
- **[alexfleetcommander/agent-trust-stack-mcp](https://github.com/alexfleetcommander/agent-trust-stack-mcp)** — Cryptographic provenance, bilateral blind reputation scoring, and tamper-evident logging for AI agent interactions. 7 interlocking trust protocols (CoC, ARP, ASA, AJP, ALP, AMP, CWEP) available in Python (pip) and TypeScript (npm). 663 tests. Bitcoin-anchored provenance chains, anti-Goodhart reputation scoring, machine-readable contracts, dispute resolution, lifecycle management, trust-weighted ma
  <sub>★ 1 · Python · Apache-2.0 · pip · pushed 2026-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-trust-stack-mcp`</sub>
- **[123Ergo/unphurl-mcp](https://github.com/123Ergo/unphurl-mcp)** — URL intelligence for AI agents. 13 tools for security signals and data quality: redirect behaviour, brand impersonation detection, domain age, SSL validation, parked detection, URL structural analysis, DNS enrichment
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx unphurl`</sub>
- **[KOVY/agentforge-trust-mcp](https://github.com/KOVY/agentforge-trust-mcp)** — Query the AgentForge Trust Score (0-100 across five dimensions: security, code health, behavioral audit, community trust, EU compliance) for any MCP server before connecting. Exposes check_trust, evaluate_policy, list_trusted, and recommend tools. 3,600+ servers audited, free public API
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-05-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y agentforge-trust-mcp@latest`</sub>
- **[agntor/mcp](https://github.com/agntor/mcp)** — MCP audit server for agent discovery and certification. Provides trust and payment rail for AI agents including identity verification, escrow, settlement, and reputation management
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-02-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @agntor/mcp`</sub>
- **[vinaybhosle/agentstamp](https://github.com/vinaybhosle/agentstamp)** — Trust intelligence for AI agents — identity stamps, reputation scoring (0-100), registry, forensic audit trails, and A2A passports via x402 micropayments
  <sub>★ 1 · JavaScript · Apache-2.0 · clone · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vinaybhosle/agentstamp.git`</sub>
- **[alberthild/shieldapi-mcp](https://github.com/alberthild/shieldapi-mcp)** — Security intelligence for AI agents: password breach checks (900M+ HIBP hashes), email/domain/IP/URL reputation, prompt injection detection (200+ patterns), and skill supply chain scanning. Pay-per-request via x402 USDC micropayments or free demo mode, no API key needed
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-03-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx shieldapi-mcp`</sub>
- **[Perufitlife/web-exposure-mcp](https://github.com/Perufitlife/web-exposure-mcp)** — Points an AI agent at a live URL and confirms publicly-served secret files by fetching the bytes — exposed .git, .env, JS source maps, backup/SQL dumps, directory listing, and dotfiles. Zero dependencies, read-only
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-06-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g web-exposure-mcp`</sub>
- **[Bichev/agentradar-mcp](https://github.com/Bichev/agentradar-mcp)** — On-chain trust oracle for the ERC-8004 + x402 agent economy. 18 tools for verifying AI agents: 6-signal composite trust scoring (0-100), 272-wallet scam database, ERC-8004 identity lookup, EAS attestations on Base mainnet. x402-payable. Free get_score / check_scam. Live at vvpro.ai · npm @agentradar/mcp
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agentradar/mcp`</sub>
- **[chrbailey/promptspeak-mcp-server](https://github.com/chrbailey/promptspeak-mcp-server)** — Pre-execution governance for AI agents. Intercepts and validates every agent tool call through an 8-stage pipeline before execution — risk classification, behavioral drift detection, hold queue for dangerous operations, and complete audit trail. 45 tools, 658 tests
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-07-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chrbailey/promptspeak-mcp-server.git`</sub>
- **[Erodenn/fetch-guard](https://github.com/Erodenn/fetch-guard)** — URL fetcher and HTML-to-markdown converter with three-layer prompt injection defense: pre-extraction sanitization of hidden/off-screen elements and non-printing Unicode, 15-pattern risk scanning (HIGH/MEDIUM/OK), and per-request session-salt content boundary wrapping
  <sub>★ 1 · Python · MIT · pip · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install fetch-guard`</sub>
- **[gridinsoft/mcp-inspector](https://github.com/gridinsoft/mcp-inspector)** — MCP server for domain and URL security analysis powered by GridinSoft Inspector, enabling AI agents to verify website and link safety
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-01-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @gridinsoft/mcp-inspector`</sub>
- **[ARKALDA/hejdar-mcp](https://github.com/ARKALDA/hejdar-mcp)** — Runtime policy enforcement for AI agents. Evaluate actions against organization policies before execution, with observe and enforce modes
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx hejdar-mcp`</sub>
- **[goldmembrane/cleaner-code](https://github.com/goldmembrane/cleaner-code)** — AI code security scanner MCP server. Detects 9 categories of threats in AI-generated code (invisible Unicode, Trojan Source, homoglyphs, Glassworm steganography, rules file backdoors, dependency typosquatting, obfuscation) using static analysis plus CodeBERT deep learning. Runs locally, free tier
  <sub>★ 1 · HTML · MIT · clone · pushed 2026-05-04</sub>
  <sub>`git clone https://github.com/goldmembrane/cleaner-code.git`</sub>
- **[infai-tech/vulnfeed-mcp](https://github.com/novadyne-hq/vulnfeed-mcp)** — Dependency vulnerability scanner with EPSS exploit probability scoring. Scans lockfiles (npm, pip, Go, Cargo, Ruby, Composer, Gradle, NuGet, Mix), prioritizes by real-world exploit likelihood, recommends fix versions. 9 MCP tools for scanning, monitoring, and alerting. Free tier + x402 micropayments. pip install vulnfeed-mcp
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx vulnfeed-mcp`</sub>
- **[itsalissonsilva/ModelSafetyMCP](https://github.com/itsalissonsilva/ModelSafetyMCP)** — MCP server for scanning machine learning model artifacts for unsafe serialization, malicious model patterns, risky packaging, URL-based artifact scanning, and directory-level triage using ModelScan, PickleScan, and heuristic inspection
  <sub>★ 1 · Python · MIT · source · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/itsalissonsilva/ModelSafetyMCP.git`</sub>
- **[joergmichno/clawguard-mcp](https://github.com/joergmichno/clawguard-mcp)** — Security scanner for AI agents that detects prompt injections using 42+ regex patterns
  <sub>★ 1 · Python · MIT · npx · pushed 2026-07-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory . run clawguard-mcp`</sub>
- **[JoeyBrar/agentseal-mcp](https://github.com/JoeyBrar/agentseal-mcp)** — Action logs for AI agents. Records every agent action in a SHA-256 hash chain, making an audit trail. Install via npx agentseal-mcp
  <sub>★ 1 · JavaScript · MIT · pip · pushed 2026-04-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentseal-sdk`</sub>
- **[juanisidoro/securecode-mcp](https://github.com/juanisidoro/securecode-mcp)** — Secrets vault for Claude Code with audit logs, MCP access rules, and AES-256 encryption. Secrets are injected to local files so the AI never sees raw values. Includes session lock, device approval, and per-model access policies
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/juanisidoro/securecode-mcp.git`</sub>
- **[nh4ttruong/secobserve-mcp](https://github.com/nh4ttruong/secobserve-mcp)** — SecObserve vulnerability and license management from an agent: triage observations through the four-eyes approval workflow, manage products, branches and rules, import scan reports and SBOMs, run scans, and generate VEX. 18 tools over ~50 REST resources, with mandatory field projection and filter validation — a wrong filter name errors instead of silently returning the unfiltered list. uvx secobse
  <sub>★ 1 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx secobserve-mcp --help`</sub>
- **[rob925/mcp-shield](https://github.com/rob925/mcp-shield)** — Static security scanner and MCP server for MCP servers and AI agent tools. Detects secrets, shell execution, risky tool descriptions, environment access, and prompt-injection phrases. mcp-shield-server
  <sub>★ 1 · Python · MIT · pipx · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install mcp-shield`</sub>
- **[Pentagonal-ai/pentagonal](https://github.com/Pentagonal-ai/pentagonal)** — AI-powered smart contract security forge with 8-agent adversarial pen test. Generate, audit, fix, and compile contracts across 8 chains (Ethereum, Solana, Polygon, Base, Arbitrum, Optimism, BSC, Avalanche). Token intelligence with honeypot detection. x402 USDC payments for autonomous agents
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx pentagonal-mcp`</sub>
- **[rev2ret/SecureAudit-MCP](https://github.com/rev2ret/SecureAudit-MCP)** — Model Context Protocol (MCP) server for static C/C++ memory-safety scanning and compiled PE/ELF binary protections auditing (ASLR, DEP/NX, SafeSEH, PIE) with secure templates remediation
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rev2ret/SecureAudit-MCP.git`</sub>
- **[samvas-codes/dawshund_mcp](https://github.com/samvas-codes/dawshund_mcp)** — An MCP server based on dAWShund to enumerate AWS IAM data, analyze effective permissions, and visualize access relationships across users, roles, and resources. Built for cloud security engineers who want fast, easy and effective insights into AWS identity risk
  <sub>★ 1 · Python · source · pushed 2025-11-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/samvas-codes/dawshund_mcp.git`</sub>
- **[scamverifyai/scamverify-mcp](https://github.com/scamverifyai/scamverify-mcp)** — AI-powered scam and threat verification MCP server. Check phone numbers, URLs, text messages, emails, documents, and QR codes against 8M+ threat intelligence records (FTC/FCC complaints, carrier analysis, URLhaus, ThreatFox). Returns risk scores, verdicts, and detailed signals. 10 tools, OAuth 2.1 + API key auth, Streamable HTTP transport
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-04-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @scamverifyai/scamverify-mcp`</sub>
- **[Thezenmonster/agentscore-mcp-server](https://github.com/Thezenmonster/agentscore-mcp-server)** — MCP security trust layer. Continuously monitors 800+ MCP packages on npm for install scripts, command injection, hardcoded secrets, capability drift, and publisher posture. Ships a GitHub Action policy gate for PR-level allow/warn/block decisions with OIDC auto-provisioning. 5 MCP tools, no API key required
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-04-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @agentscore-xyz/mcp-server`</sub>
- **[GUCCI-atlasv/skillssafe-mcp](https://github.com/GUCCI-atlasv/skillssafe-mcp)** — Free AI agent skill security scanner. Scan SKILL.md, MCP configs, and system prompts for credential theft, prompt injection, zero-width character attacks, and ClawHavoc indicators. Supports OpenClaw, Claude Code, Cursor, and Codex. No signup required
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/GUCCI-atlasv/skillssafe-mcp.git`</sub>
- **[vikasny30/aletheia-mcp](https://github.com/vikasny30/aletheia-mcp)** — Deterministic (no-LLM) pre-execution filter for agent tool calls. Pattern-matches known scope-creep (out-of-mandate writes, credential-file reads, SSRF, destructive shell/SQL) and prompt-injection vectors and blocks them in ~25 µs. Runs as standalone guard tools or a fail-closed transparent proxy in front of any downstream MCP server. Signatures from the Aletheia research paper; a first-line pre-f
  <sub>★ 1 · TypeScript · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vikasny30/aletheia-mcp.git`</sub>
- **[wei9072/aegis](https://github.com/wei9072/aegis)** — AI-agent admission-control MCP server: validates file edits against Ring 0 syntax + Ring 0.5 structural-cost regression + workspace boundary (path / glob / shell-redirect / symlink). Negative-space framing — emits BLOCK / WARN / PASS verdicts, never coaches the agent
  <sub>★ 1 · Python · MIT · cargo · pushed 2026-05-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --path crates/aegis-mcp`</sub>
- **[zekebuilds-lab/captcha-mcp](https://github.com/zekebuilds-lab/captcha-mcp)** — L402 Lightning paywall + Hashcash proof-of-work gate for MCP tool calls. Free tier solves a PoW challenge; paid tier pays a Lightning invoice via self-hosted LNBits. No accounts, no API keys, no third-party SaaS. Drop-in middleware for any MCP server. npx @powforge/captcha-mcp
  <sub>★ 1 · JavaScript · MIT · npx · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @powforge/captcha-mcp`</sub>
- **[uchit/mcp-regulated-ai-compliance](https://github.com/uchit/mcp-regulated-ai-compliance)** — Regulated-industry AI compliance knowledge as MCP. 6 tools (lookup_control · classify_use_case · crosswalk · walk_playbook · get_anti_pattern · list_regulations), 53 resources, 5 prompts. Covers EU AI Act, APRA CPS 230/234, NIST AI RMF, ISO 42001, AU AI Safety Standard (DISR Aug 2024), OWASP LLM Top 10, SLSA, SSDF, OAIC APPs, GDPR, DORA + 17 more frameworks. 56 controls × 28 regulations × 261 tool
  <sub>★ 1 · TypeScript · Apache-2.0 · npx · pushed 2026-06-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-regulated-ai-compliance-http`</sub>
- **[iamredmh/volta-mcp-server](https://github.com/iamredmh/volta-mcp-server)** — Burn-after-read encrypted notes for AI agents. Create and read self-destructing notes via Volta Notes with AES-256-GCM E2E encryption — the decryption key never leaves the URL fragment. Secure credential handoff between users and agents without secrets appearing in chat history
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-04-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @voltanotes/mcp`</sub>
- **[zkproofport/proofport-ai](https://github.com/zkproofport/proofport-ai)** — Zero-knowledge proof generation MCP server for AI agents. Lets agents prove identity claims (Coinbase KYC, Country, Google OIDC, Google Workspace, Microsoft 365) without revealing personal information. Server-side proving in AWS Nitro Enclave TEE, paid via x402 USDC on Base. Built on Noir circuits (Aztec) and ERC-8004 agent identity. Reference application OpenStoa won 1st place at The Synthesis Ha
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx zkproofport-mcp # Starts stdio MCP server`</sub>
- **[cuttalo/depscope](https://github.com/cuttalo/depscope)** — Package Intelligence for AI agents. 22 tools across 17 ecosystems (npm/pypi/cargo/go/maven/nuget/rubygems/composer/pub/hex/swift/cocoapods/cpan/hackage/cran/conda/homebrew) — check health, vulnerabilities (OSV + CISA KEV + EPSS), typosquats, malicious flags, alternatives, known bugs, breaking changes, stack compatibility and error-to-fix. 31k+ packages, 2.2k+ CVEs enriched. Zero auth, MIT. Remote
  <sub>★ 1 · source · pushed 2026-05-05</sub>
  <sub>`git clone https://github.com/cuttalo/depscope.git`</sub>
- **[vaulted-fyi/vaulted-mcp-server](https://github.com/vaulted-fyi/vaulted-mcp-server)** — Share encrypted, self-destructing secrets from your AI agent. Zero-knowledge E2E encryption. Agent-blind input sources (env:, file:, dotenv:) keep secrets out of LLM context
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @vaulted/mcp-server`</sub>
- **[BeBraveBeKind/mcpskills-server](https://github.com/BeBraveBeKind/mcpskills-server)** — Pre-install trust layer for MCP servers, AI skills, and npm packages. Scores any repo or package across 15 signals (incl. OSV/KEV/EPSS vulnerability intelligence) with safety scanning for prompt injection, credential theft, and supply-chain risk; the auto_gate tool returns a go/no-go install decision. Listed in the official MCP Registry as io.mcpskills/server. npm: @mcpskillsio/server. https://mcp
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BeBraveBeKind/mcpskills-server.git`</sub>
- **[gautam-u/sieve-mcp](https://github.com/gautam-u/sieve-mcp)** — Local AI chat history secret scanner for macOS. Finds API keys and secrets leaked into Claude Code, Cursor, Copilot Chat, Cline, Codex, Gemini CLI, and other AI tool transcripts. 9 MCP tools: findings list with redacted previews, boolean secret detection (sieve_check_text), placeholder-only redaction (sieve_redact_text returns sieve://project/key, never raw values), vault-backed command execution,
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-08-02 · macOS</sub>
  <sub>`git clone https://github.com/gautam-u/sieve-mcp.git`</sub>
- **[aggrete/aggrete](https://github.com/aggrete/aggrete)** — Policy proxy that governs what AI assistants can reach and do: refuses forbidden tool calls before the upstream is contacted, with per-user memory and a tamper-evident audit. Stops prompt-injection exfiltration and forbidden data combinations across Slack, Drive, GitHub and more. pip install aggrete
  <sub>★ 1 · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx aggrete --demo # the walkthrough — no config, auth, or network`</sub>
- **[Jiangw2718i/frisk](https://github.com/Jiangw2718i/frisk)** — Screen the counterparty of an x402 payment before an agent pays it. One tool, screen_payment, runs deterministic checks — address sanity, dynamic-payTo swap detection, transport safety and your own spend policy — and returns allow/review/block with the reasons for the verdict. Advisory: it never holds funds, and your code decides. Runs entirely on your machine by default with no key, no account an
  <sub>★ 1 · Python · MIT · source · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Jiangw2718i/frisk.git`</sub>
- **[AIops-tools/Compliance-AIops](https://github.com/AIops-tools/Compliance-AIops)** — A meta-tool that reads other AIops tools' audit trails and seals framework-mapped (HIPAA/PCI-DSS/SOC 2/GDPR) hash-chained evidence bundles — deterministic, offline, and tamper-evident (19 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards
  <sub>Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install compliance-aiops # or: pipx install compliance-aiops`</sub>
- **[chasdaddy/basescope](https://github.com/chasdaddy/basescope)** — The read-only safety layer for onchain AI agents. 13 read-only tools on Base + EVM: token/contract safety (honeypot &amp; rug-pull checks cross-referenced across GoPlus + honeypot.is), risky-approval detection, verified-source lookup, balances, ENS + Basenames, gas, and prices. No private keys, no required API keys. npx -y basescope
  <sub>TypeScript · MIT · clone · pushed 2026-07-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chasdaddy/basescope.git`</sub>
- **[elang2/mcp-audit-gateway](https://github.com/elang2/mcp-audit-gateway)** — Tamper-proof audit trail for AI agent tool calls. Transparent stdio proxy with cryptographic attestation (Ed25519 signing), hash-chained records, YAML policy enforcement (allow/deny/transform), and OpenTelemetry export. Zero server modification required. npm i @mcp-audit-gateway/core
  <sub>TypeScript · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @mcp-audit-gateway/core`</sub>
- **[sachio222/54ch10-mcp](https://github.com/sachio222/54ch10-mcp)** — Pre-interact JSON risk briefs for wallet/agent builders: address / token / url → score, band, flags, sources (phishing/scam/wallet/URL-reputation heuristics). Live OpenPhish + eth_getCode. x402 $0.01 USDC/brief or free demo 20/day. Analytics-only — not financial advice. Install: npx -y github:sachio222/54ch10-mcp. Site: https://54ch10.uk
  <sub>JavaScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y github:sachio222/54ch10-mcp`</sub>
- **[jamesdfinance-dev/lazaretto-mcp](https://github.com/jamesdfinance-dev/lazaretto-mcp)** — Check whether anything you depend on is known malware, before an agent installs it. check_lockfile takes a package-lock.json, yarn.lock or pnpm-lock.yaml and matches every pinned version against published malicious-package advisories in one call, free and with no API key, catching compromised releases like chalk@5.6.1 while leaving their clean releases alone. scan_artifact adds deterministic behav
  <sub>JavaScript · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jamesdfinance-dev/lazaretto-mcp`</sub>
- **[meloliva14/verity-mcp](https://github.com/meloliva14/verity-mcp)** — Fail-closed "verify before you act" trust gate for AI agents: fact-check (catch hallucinations), prompt-injection detection, content moderation, PII/secret detection, and a pre-action guardrail (allow/review/block). Independent, keyless, pay-per-call via x402. pip install verity-mcp
  <sub>Python · pip · pushed 2026-08-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install verity-mcp`</sub>
- **[hernaninverso/eleion-scanner-mcp](https://github.com/hernaninverso/eleion-scanner-mcp)** — Register/verify your domains, queue security scans (headers, TLS, DNS, ports, CVEs + AI-specific checks) and read findings, for AI agents. Install with npx -y eleion-scanner-mcp
  <sub>JavaScript · source · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hernaninverso/eleion-scanner-mcp.git`</sub>
- **[alexar76/aimarket-oracle-gateway](https://github.com/alexar76/aimarket-oracle-gateway)** — Verifiable oracle MCP server: Platon VRF (get_random), Chronos VDF (compute_vdf / verify_vdf), LUMEN reputation (get_reputation_scores) as agent tools. Pay-per-call over AIMarket Hub; every result independently verifiable. stdio · Python · Glama
  <sub>Python · MIT · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/alexar76/aimarket-oracle-gateway.git`</sub>
- **[equinoxaifinance-rgb/living-stack-mcp](https://github.com/equinoxaifinance-rgb/living-stack-mcp)** — Stops AI agents from claiming done without proof. Fourteen bounded tools add scoped authorization, budget reservations, typed evidence gates, checkpoint recovery, tamper-evident outcomes, and signed metadata-only traces without giving the server shell, browser, or network authority. Apache-2.0; audited MCPB and GitHub installs need no API key
  <sub>unavailable</sub>
- **[maxfain/basedagents](https://github.com/maxfain/basedagents)** — Agent identity, reputation, and key custody. The registry server gives agents an Ed25519 identity with proof-of-work registration, capability search, reputation scores, a task marketplace, and agent-to-agent messaging; the Keyring server holds provider keys in a local encrypted vault and leases them to agents under owner passkey approvals, with env-var injection so values never enter model context
  <sub>TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx basedagents register`</sub>
- **[jagmarques/asqav-mcp](https://github.com/jagmarques/asqav-mcp)** — AI agent governance MCP server with policy enforcement, quantum-safe audit trails (ML-DSA), multi-party authorization, and compliance reporting. Check policies, sign actions, and verify signatures through MCP tools
  <sub>unavailable</sub>
- **[jamjet-labs/jamjet-policy](https://github.com/jamjet-labs/jamjet-policy/tree/main/packages/mcp-shim)** — MCP stdio interceptor (@jamjet/mcp-shim) that applies one YAML policy file (block / require_approval / audit / budget cap) to tools/call requests before they reach the real MCP server. The same policy also runs in Claude Code PreToolUse hooks (@jamjet/claude-code-hook), OpenAI Agents SDK guardrails (@jamjet/openai-guardrail), and JamJet's Python/TS SDKs — jamjet audit show tails every decision acr
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-07-13</sub>
  <sub>`git clone https://github.com/jamjet-labs/jamjet-policy.git && cd jamjet-policy/packages/mcp-shim`</sub>
- **[imran-siddique/agentos-mcp-server](https://github.com/imran-siddique/agent-os/tree/master/extensions/mcp-server)** — Agent OS MCP server for AI agent governance with policy enforcement, code safety verification, multi-model hallucination detection, and immutable audit trails
  <sub>Python · MIT · in-repo · pushed 2026-03-03</sub>
  <sub>`git clone https://github.com/imran-siddique/agent-os.git && cd agent-os/extensions/mcp-server`</sub>
- **[bluetieroperations-create/blackwall-mcp](https://github.com/bluetieroperations-create/blackwall-mcp)** — Pre-action risk gate for AI agents. One forecast tool the agent calls before any irreversible action (send money, run SQL, delete data); returns a risk score (0–100), reversibility class, named red flags from 28 failure modes, and a gate: proceed / confirm / human-required
  <sub>JavaScript · MIT · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bluetieroperations-create/blackwall-mcp.git`</sub>
- **[corewebvitals/state-of-cwv-mcp](https://github.com/corewebvitals/state-of-cwv-mcp)** — Free remote MCP for Core Web Vitals metrics by CMS, CDN, and framework (Chrome field data + multi-site crawl). No auth. Endpoint: https://www.corewebvitals.io/api/state-of-cwv/mcp
  <sub>JavaScript · MIT · docker · pushed 2026-07-16 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i state-of-cwv-mcp`</sub>
- **[CSOAI-ORG/councilof-ai](https://github.com/CSOAI-ORG/councilof-ai)** — Live GSPC measurement board over MCP (https://councilof.ai/mcp, npx -y csoai-gspc-mcp@0.1.1). Seven read-only tools. Measurement, never certification. Verify: https://councilof.ai/gspc-verify
  <sub>unavailable</sub>
- **[Cubiczan/governed-mcp-gateway](https://github.com/Cubiczan/governed-mcp-gateway)** — HTTP MCP gateway: principal on tools/call + SSE, allowlists, vault rotate. npx -y @cubiczan/governed-mcp-gateway
  <sub>TypeScript · MIT · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Cubiczan/governed-mcp-gateway.git`</sub>
- **[Cubiczan/trust-ledger-os](https://github.com/Cubiczan/trust-ledger-os)** — Trust/risk control plane for AI teams: phases, routes, package catalog over MCP. node packages/mcp/dist/server.js after build
  <sub>TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Cubiczan/trust-ledger-os.git`</sub>
- **[dambuchs/redact-pdf-mcp](https://github.com/dambuchs/redact-pdf-mcp)** — Permanently redact PII from PDFs, scans and screenshots: names, emails, phone numbers, addresses, IBANs and card numbers are removed from the file (pages rasterized, text layer dropped), not covered. OCR in 100+ languages, EU/Swiss-hosted, keyless demo on your own file
  <sub>TypeScript · MIT · npx · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx redact-pdf-mcp-http # listens on :8080/mcp`</sub>
- **[dkvdm/onepassword-mcp-server](https://github.com/dkvdm/onepassword-mcp-server)** — An MCP server that enables secure credential retrieval from 1Password to be used by Agentic AI
  <sub>unavailable</sub>
- **[elberacasa/umbra](https://github.com/elberacasa/umbra)** — Trust score and guardrails for AI-generated code: static security rules, Docker-verified build/boot checks, and claim receipts that catch agents lying about tests. Tools: scan_repo, guard_content, get_score. Run with npx --yes -p @elberacasa/umbra umbra-mcp
  <sub>TypeScript · MIT · npx · pushed 2026-08-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx umbra-scan # check — scans the directory you're standing in`</sub>
- **[forgemeshlabs/x402-notary-mcp](https://github.com/forgemeshlabs/x402-notary-mcp)** — Cryptographic receipts for AI outputs: notarize any model inference with a signed Ed25519 attestation, sha256 content hash, and Merkle chain-anchor on Base or Solana. $0.001 per call via x402 USDC micropayments; verification is free and needs no wallet. Notarizes the hash, never your prompts. npx -y @forgemeshlabs/x402-notary-mcp
  <sub>JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/forgemeshlabs/x402-notary-mcp.git`</sub>
- **[Kjopstad-IT/rqwstr](https://github.com/Kjopstad-IT/rqwstr-mcp)** — AI-native HTTP security testing toolkit: 17 tools (send, intruder, race, chain, oob) with low-level control over HTTP/1.1 + HTTP/2 (raw framing, connection pinning)
  <sub>Dockerfile · source · pushed 2026-08-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Kjopstad-IT/rqwstr-mcp.git`</sub>
- **[knowledgepa3/gia-mcp-server](https://github.com/knowledgepa3/gia-mcp-server)** — Enterprise AI governance layer with 29 tools: MAI decision classification (Mandatory/Advisory/Informational), hash-chained forensic audit trails, human-in-the-loop gates, compliance mapping (NIST AI RMF, EU AI Act, ISO 42001), governed memory packs, and site reliability tools
  <sub>unavailable</sub>
- **[haruodev/tamperlens-mcp](https://github.com/haruodev/tamperlens-mcp)** — Document forensics before an agent reads the file: whether a PDF, Office file or image was edited after it was written, whether its redactions actually removed the text, and whether it carries text addressed to a language model rather than to a reader — the recovered injection payload is elided rather than echoed back into the context. Thin client over the Tamperlens REST API; signals with evidenc
  <sub>TypeScript · MIT · source · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/haruodev/tamperlens-mcp.git`</sub>
- **[jaimenbell/rails-mcp](https://github.com/jaimenbell/rails-mcp)** — Self-hosted default-deny action registry, append-only spend-intent ledger and human sign-off audit trail, exposed as MCP tools. Provides the schema and audit trail for gating irreversible agent actions rather than intercepting them: you wire it into your own hook or CI gate, and it ships with no preloaded action data. pip install rails-mcp
  <sub>Python · MIT · pip · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install rails-mcp`</sub>
- **[jaspertvdm/mcp-server-inject-bender](https://github.com/jaspertvdm/mcp-server-inject-bender)** — Security through absurdity: transforms SQL injection and XSS attempts into harmless comedy responses using AI-powered humor defense
  <sub>unavailable</sub>
- **[ndl-systems/kevros-mcp](https://github.com/ndl-systems/kevros-mcp)** — Governance primitives for autonomous agents — verify actions against policy, record signed provenance, and bind intents cryptographically. Free tier: 100 calls/month
  <sub>unavailable</sub>
- **[mobb-dev/mobb-vibe-shield-mcp](https://github.com/mobb-dev/bugsy?tab=readme-ov-file#model-context-protocol-mcp-server)** — Mobb Vibe Shield identifies and remediates vulnerabilities in both human and AI-written code, ensuring your applications remain secure without slowing development
  <sub>TypeScript · MIT · in-repo · pushed 2026-08-31</sub>
  <sub>`git clone https://github.com/mobb-dev/bugsy.git && cd bugsy/?tab=readme-ov-file#model-context-protocol-mcp-server`</sub>
- **[nickgeorgeseo/mcp-gatehouse](https://github.com/nickgeorgeseo/mcp-gatehouse)** — Permission tiers, approval gates, and secret-redacting audit logging enforced inside the server at the tool boundary; includes a demo order-desk server. uvx mcp-gatehouse
  <sub>Python · MIT · pip · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mcp-gatehouse`</sub>
- **[project-feldspar-resources/feldspar-scan](https://github.com/project-feldspar-resources/feldspar-scan)** — Free deterministic security scan of any public git repository, for agents and CI: vulnerable dependencies via OSV.dev (npm, pip/uv/poetry, Cargo, Go, Gemfile, composer), hard-coded secret patterns (redacted) and risky config lint, returned as file:line findings with a hashed result manifest. Hosted remote MCP at https://project-feldspar.com/mcp (no key, 5 scans/hour/IP, registry com.project-feldsp
  <sub>Python · MIT · gh-action · pushed 2026-09-05</sub>
  <sub>`uses: project-feldspar-resources/feldspar-scan@main # in .github/workflows/*.yml`</sub>
- **[rafapra3008/cervellaswarm](https://github.com/rafapra3008/cervellaswarm/tree/main/packages/mcp-server)** — Verify AI agent communication protocols using session types. Formal specification with Lean 4 proofs, linter, formatter, and LSP. Catches deadlocks and role violations before deployment
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-08-18</sub>
  <sub>`git clone https://github.com/rafapra3008/cervellaswarm.git && cd cervellaswarm/packages/mcp-server`</sub>
- **[safedep/vet](https://github.com/safedep/vet/blob/main/docs/mcp.md)** — vet-mcp checks open source packages—like those suggested by AI coding tools—for vulnerabilities and malicious code. It supports npm and PyPI, and runs locally via Docker or as a standalone binary for fast, automated vetting
  <sub>Go · Apache-2.0 · in-repo · pushed 2026-09-16</sub>
  <sub>`git clone https://github.com/safedep/vet.git && cd vet/docs/mcp.md`</sub>
- **[SaravananJaichandar/etch-mcp](https://github.com/SaravananJaichandar/etch-mcp)** — Signed audit chain for AI agent decisions. Every event signed, Merkle-chained per project, anchored to public transparency logs, and offline-verifiable against a pinned public key without dependency on our infrastructure. Post-hoc evidence primitive, complementary to runtime enforcement (not a substitute). Zero-signup try-it-now: curl -X POST https://etch.systems/v1/your-project returns a bearer t
  <sub>Python · MIT · source · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SaravananJaichandar/etch-mcp.git`</sub>
- **[sp3ak/safenode-mcp-gateway](https://github.com/sp3ak/safenode-mcp-gateway)** — Policy proxy for MCP tool calls. Evaluates every call before forwarding; deny means it never reaches the downstream server. Warn forwards with a visible banner, review holds for human approval. Client-side redaction reports what it stripped so server-side rules still fire on data they never receive. Fail-closed by default. npx safenode-mcp-gateway
  <sub>TypeScript · MIT · npx · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx safenode-mcp-gateway`</sub>
- **[swnotmetal/Project-Koma](https://github.com/swnotmetal/Project-Koma/tree/main/packages/koma-gate-mcp)** — MCP server exposing Koma Gate's LLM-based classification of prompt injection and out-of-scope input through the classify_input tool
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-12</sub>
  <sub>`git clone https://github.com/swnotmetal/Project-Koma.git && cd Project-Koma/packages/koma-gate-mcp`</sub>
- **[zboralski/ida-headless-mcp](https://github.com/zboralski/ida-headless-mcp)** — Headless IDA Pro binary analysis via MCP. Multi-session concurrency with Go orchestration and Python workers. Supports Il2CppDumper and Blutter metadata import for Unity and Flutter reverse engineering
  <sub>unavailable</sub>
- **[tponscr-debug/oracle-h-mcp](https://github.com/tponscr-debug/oracle-h-mcp)** — Mandatory human approval gate for autonomous AI agents. Intercepts critical, irreversible, or financially significant actions and routes them to a human via Telegram for real-time approve/reject. Raises workflow success probability from 81.5% to 99.6%
  <sub>unavailable</sub>
- **[shieldly-io/mcp](https://github.com/shieldly-io/mcp)** — Official Shieldly MCP server: analyze_iam_policy and analyze_cloudformation_template tools flag AWS IAM privilege-escalation paths, wildcards, and over-permissive access. Free demo mode, no signup or API key needed. npx -y @shieldly/mcp
  <sub>JavaScript · MIT · source · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shieldly-io/mcp.git`</sub>
- **[OksigeniaSL/checker-mcp](https://github.com/OksigeniaSL/checker-mcp)** — Domain security &amp; privacy checker: 17 live checks (SPF, DMARC, DKIM, DNSSEC, TLS, CAA, security headers) scored 0-100 with remediation. Local-first, zero telemetry. In the official MCP Registry as com.oksigenia/checker-mcp; npm @oksigenia/checker-mcp
  <sub>TypeScript · GPL-3.0 · npx · pushed 2026-07-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @oksigenia/checker-mcp`</sub>
- **[mcpindex-ai/mcp-server-mcpindex](https://github.com/mcpindex-ai/mcp-server-mcpindex)** — Find MCP servers by natural-language task and get advisory trust screens (check_tool_trust, assess_server) before you connect. The directory client for mcpindex.ai; advisory, not a safety verdict
  <sub>JavaScript · MIT · npm · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g mcp-server-mcpindex`</sub>
- **[williamblakecunningham-max/screenverity-mcp](https://github.com/williamblakecunningham-max/screenverity-mcp)** — Free U.S. exclusion, debarment and licence screening for agents (OIG LEIE, SAM.gov, state boards) with an Ed25519-signed receipt of the exact list snapshots checked
  <sub>JavaScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx screenverity-mcp`</sub>
- **[trustscoreagent/trustscoreagent](https://github.com/trustscoreagent/trustscoreagent)** — Check the reputation of an AI microservice or public API *before* calling it, and submit ratings afterward — from a free, open trust registry (no account or API key). Scores combine Bayesian reputation and EigenTrust, strengthened by cryptographically signed service receipts and a Merkle audit trail. Install: npx -y @trustscoreagent/mcp-server
  <sub>C# · Apache-2.0 · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/trustscoreagent/trustscoreagent.git`</sub>
- **[aurumflux20/seal](https://github.com/aurumflux20/seal)** — Exactly-once execution for agents that move money: the same payment can't settle twice across processes or retries. World-confirmation asks the provider ("did this charge actually land?") and returns CONFIRMED_ONE / MULTIPLE / ABSENT / UNKNOWN; out-of-band reconcile catches spend that bypassed the gateway; earned-autonomy licensing (L0–L5) only raises an agent's unattended spend ceiling on proven-
  <sub>Python · pip · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install seal-kernel`</sub>
- **[epistemedeus/skillguard](https://github.com/epistemedeus/skillguard)** — Static security scanner for Claude Code skills, plugins, and MCP servers — vet a dependency for malware (secret/env exfiltration, install-time hooks, prompt injection, committed binaries) before you install it. Static-only: it clones and reads files, never executes the scanned code. npx -y github:epistemedeus/skillguard mcp
  <sub>JavaScript · npx · pushed 2026-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:epistemedeus/skillguard https://github.com/owner/repo`</sub>
- **[Drumworks/ssid-mcp](https://github.com/Drumworks/ssid-mcp)** — MAC-address (OUI) vendor lookup and router default-login directory for AI agents. Identify a device manufacturer from its MAC address, detect randomized/private (locally-administered) addresses instead of reporting "unknown", or fetch a router's default login IP and admin credentials — every router field cited to the manufacturer's own documentation. Free tier, no signup. npx -y ssid-mcp
  <sub>JavaScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Drumworks/ssid-mcp.git`</sub>
- **[gostanos/smallprint-action](https://github.com/gostanos/smallprint-action/tree/main/mcp)** — Read the Small Print record: the tool descriptions, schemas and instructions of MCP servers, agent skills and plugins, hashed every version and diffed between releases, each change graded by a printed rule, with public advisories joined by version. Four read-only tools over the public record, including a yes-or-no check that a server's small print has not moved since the version you approved; npx
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/gostanos/smallprint-action.git && cd smallprint-action/mcp`</sub>

## Cloud Platforms

- **[awslabs/mcp](https://github.com/awslabs/mcp)** — AWS MCP servers for seamless integration with AWS services and resources
  <sub>★ 9.7k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/awslabs/mcp.git`</sub>
- **[cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)** — Integration with Cloudflare services including Workers, KV, R2, and D1
  <sub>★ 4.3k · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cloudflare/mcp-server-cloudflare.git`</sub>
- **[txn2/kubefwd](https://github.com/txn2/kubefwd)** — Kubernetes bulk port forwarding with service discovery, /etc/hosts management, traffic monitoring, and pod log streaming
  <sub>★ 4.2k · Go · Apache-2.0 · winget · pushed 2026-09-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`winget install txn2.kubefwd`</sub>
- **[manusa/Kubernetes MCP Server](https://github.com/containers/kubernetes-mcp-server)** — A - powerful Kubernetes MCP server with additional support for OpenShift. Besides providing CRUD operations for any Kubernetes resource, this server provides specialized tools to interact with your cluster
  <sub>★ 2.1k · Go · Apache-2.0 · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx kubernetes-mcp-server@latest --help`</sub>
- **[flux159/mcp-server-kubernetes](https://github.com/Flux159/mcp-server-kubernetes)** — /🏠 - Typescript implementation of Kubernetes cluster operations for pods, deployments, services
  <sub>★ 1.6k · TypeScript · MIT · npx · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx mcp-chat --server "npx mcp-server-kubernetes"`</sub>
- **[hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server)** — The official Terraform MCP Server seamlessly integrates with the Terraform ecosystem, enabling provider discovery, module analysis, and direct Registry API integration for advanced Infrastructure as Code workflows
  <sub>★ 1.5k · Go · MPL-2.0 · go · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`go install github.com/hashicorp/terraform-mcp-server/cmd/terraform-mcp-server@latest`</sub>
- **[TencentCloudBase/CloudBase-AI-ToolKit](https://github.com/TencentCloudBase/CloudBase-AI-Toolkit)** — One-stop backend services for WeChat Mini-Programs and full-stack apps. Provides specialized MCP tools for serverless cloud functions, databases, and one-click deployment to production with China market access through WeChat ecosystem
  <sub>★ 1.1k · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @cloudbase/cli`</sub>
- **[rohitg00/kubectl-mcp-server](https://github.com/rohitg00/kubectl-mcp-server)** — /🏠 - A Model Context Protocol (MCP) server for Kubernetes that enables AI assistants like Claude, Cursor, and others to interact with Kubernetes clusters through natural language
  <sub>★ 960 · Python · MIT · npm · pushed 2026-04-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g kubectl-mcp-server`</sub>
- **[weibaohui/k8m](https://github.com/weibaohui/k8m)** — /🏠 - Provides MCP multi-cluster Kubernetes management and operations, featuring a management interface, logging, and nearly 50 built-in tools covering common DevOps and development scenarios. Supports both standard and CRD resources
  <sub>★ 887 · Go · MIT · source · pushed 2026-09-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/weibaohui/k8m.git`</sub>
- **[strowk/mcp-k8s-go](https://github.com/strowk/mcp-k8s-go)** — /🏠 - Kubernetes cluster operations through MCP
  <sub>★ 384 · Go · MIT · npm · pushed 2025-12-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @strowk/mcp-k8s`</sub>
- **[nwiizo/tfmcp](https://github.com/nwiizo/tfmcp)** — A Terraform MCP server allowing AI assistants to manage and operate Terraform environments, enabling reading configurations, analyzing plans, applying configurations, and managing Terraform state
  <sub>★ 371 · Rust · MIT · cargo · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install tfmcp --version 0.2.3`</sub>
- **[portainer/portainer-mcp](https://github.com/portainer/portainer-mcp)** — /🏠 - A powerful MCP server that enables AI assistants to seamlessly interact with Portainer instances, providing natural language access to container management, deployment operations, and infrastructure monitoring capabilities
  <sub>★ 233 · Python · MIT · docker · pushed 2026-09-19 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name portainer-mcp -p 17717:17717 \`</sub>
- **[alexei-led/k8s-mcp-server](https://github.com/alexei-led/k8s-mcp-server)** — A lightweight yet robust server that empowers AI assistants to securely execute Kubernetes CLI commands (kubectl, helm, istioctl, and argocd) using Unix pipes in a safe Docker environment with multi-architecture support
  <sub>★ 212 · Python · MIT · source · pushed 2026-02-27 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/alexei-led/k8s-mcp-server.git`</sub>
- **[alexei-led/aws-mcp-server](https://github.com/alexei-led/cloud-mcp-server)** — A lightweight but powerful server that enables AI assistants to execute AWS CLI commands, use Unix pipes, and apply prompt templates for common AWS tasks in a safe Docker environment with multi-architecture support
  <sub>★ 186 · Python · MIT · source · pushed 2026-02-27 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/alexei-led/aws-mcp-server.git`</sub>
- **[reza-gholizade/k8s-mcp-server](https://github.com/reza-gholizade/k8s-mcp-server)** — /🏠 - A Kubernetes Model Context Protocol (MCP) server that provides tools for interacting with Kubernetes clusters through a standardized interface, including API resource discovery, resource management, pod logs, metrics, and events
  <sub>★ 183 · Go · MIT · script · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/reza-gholizade/k8s-mcp-server/main/scripts/install-vscode-config.sh | bash`</sub>
- **[silenceper/mcp-k8s](https://github.com/silenceper/mcp-k8s)** — /🏠 - MCP-K8S is an AI-driven Kubernetes resource management tool that allows users to operate any resources in Kubernetes clusters through natural language interaction, including native resources (like Deployment, Service) and custom resources (CRD). No need to memorize complex commands - just describe your needs, and AI will accurately execute the corresponding cluster operations, greatly enhanci
  <sub>★ 151 · Go · Apache-2.0 · go · pushed 2026-09-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/silenceper/mcp-k8s/cmd/mcp-k8s@latest`</sub>
- **[weibaohui/kom](https://github.com/weibaohui/kom)** — /🏠 - Provides MCP multi-cluster Kubernetes management and operations. It can be integrated as an SDK into your own project and includes nearly 50 built-in tools covering common DevOps and development scenarios. Supports both standard and CRD resources
  <sub>★ 149 · Go · MIT · source · pushed 2026-08-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/weibaohui/kom.git`</sub>
- **[aliyun/alibaba-cloud-ops-mcp-server](https://github.com/aliyun/alibaba-cloud-ops-mcp-server)** — A MCP server that enables AI assistants to operation resources on Alibaba Cloud, supporting ECS, Cloud Monitor, OOS and widely used cloud products
  <sub>★ 130 · Python · Apache-2.0 · source · pushed 2026-03-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aliyun/alibaba-cloud-ops-mcp-server.git`</sub>
- **[zw008/VMware-AIops](https://github.com/vmware-skills/VMware-AIops)** — VMware vSphere/vCenter management — VM lifecycle (create/clone/delete/migrate), deployment, Guest Operations, snapshots, and cluster operations. 41 tools with double-confirmation gates, dry-run mode, and SQLite-WAL audit logging for destructive operations
  <sub>★ 74 · Python · MIT · npx · pushed 2026-09-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add vmware-skills/VMware-AIops`</sub>
- **[AliKarami/MikroMCP](https://github.com/AliKarami/MikroMCP)** — Manage MikroTik RouterOS devices through AI assistants — interfaces, firewall rules, DHCP, DNS, routes, WireGuard, WiFi, BGP/OSPF, VLANs, and more. 77 tools with dry-run previews, idempotency checks, circuit breakers, RBAC, and rollback-aware change workflows
  <sub>★ 67 · TypeScript · MIT · source · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/AliKarami/MikroMCP.git`</sub>
- **[bright8192/esxi-mcp-server](https://github.com/bright8192/esxi-mcp-server)** — A VMware ESXi/vCenter management server based on MCP (Model Control Protocol), providing simple REST API interfaces for virtual machine management
  <sub>★ 64 · Python · MIT · source · pushed 2025-07-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bright8192/esxi-mcp-server.git`</sub>
- **[StacklokLabs/mkp](https://github.com/StacklokLabs/mkp)** — MKP is a Model Context Protocol (MCP) server for Kubernetes that allows LLM-powered applications to interact with Kubernetes clusters. It provides tools for listing and applying Kubernetes resources through the MCP protocol
  <sub>★ 59 · Go · Apache-2.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/StacklokLabs/mkp.git`</sub>
- **[john-broadway/proximo](https://github.com/john-broadway/proximo)** — All four Proxmox surfaces — VE, Backup Server, Mail Gateway, Datacenter Manager — plus in-container exec on one audited control plane. Every mutation dry-runs to a PLAN with its blast radius named, snapshots first where the platform can, and lands in a hash-chained tamper-evident audit ledger. 365 tools, read-only by default. uvx proximo-proxmox
  <sub>★ 49 · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx proximo-proxmox doctor`</sub>
- **[rosenvladimirov/odoo-claude-mcp](https://github.com/rosenvladimirov/odoo-claude-mcp)** — Self-hosted MCP server suite for Odoo ERP (versions 15-19). 197+ tools across 8 federated MCP servers (odoo-rpc, GitHub, Portainer, OCA, Teams, filesystem). Multi-tenant Claude/Claude Code integration, browser-based xterm.js + tmux terminal, Qdrant + Ollama memory layer, Bulgaria localization (НАП, ДДС, ЕИК). Docker Compose + K3s/Kustomize deployment
  <sub>★ 49 · HTML · AGPL-3.0 · script · pushed 2026-09-10 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/rosenvladimirov/odoo-claude-mcp/2.0/install.sh | bash`</sub>
- **[redis/mcp-redis-cloud](https://github.com/redis/mcp-redis-cloud)** — Manage your Redis Cloud resources effortlessly using natural language. Create databases, monitor subscriptions, and configure cloud deployments with simple commands
  <sub>★ 41 · TypeScript · MIT · source · pushed 2025-05-05 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/redis/mcp-redis-cloud.git`</sub>
- **[qiniu/qiniu-mcp-server](https://github.com/qiniu/qiniu-mcp-server)** — A MCP built on Qiniu Cloud products, supporting access to Qiniu Cloud Storage, media processing services, etc
  <sub>★ 39 · Python · MIT · npx · pushed 2025-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory . run qiniu-mcp-server`</sub>
- **[backblaze-labs/b2-mcp](https://github.com/backblaze-labs/b2-mcp)** — Official Backblaze B2 MCP server for buckets, files, keys, Object Lock, and S3-compatible storage. npx -y @backblaze-labs/b2-mcp
  <sub>★ 36 · TypeScript · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @backblaze-labs/b2-mcp`</sub>
- **[xmpuspus/cloudwright](https://github.com/xmpuspus/cloudwright)** — Natural-language cloud architecture intelligence for AWS, GCP, Azure, and Databricks. 19 tools for architecture design, cost estimation, compliance validation (HIPAA, SOC 2, FedRAMP, GDPR, PCI-DSS, Well-Architected), security scanning, Terraform/CloudFormation export, and blast-radius analysis
  <sub>★ 32 · Python · MIT · pip · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install 'cloudwright-ai[cli]'`</sub>
- **[cyclops-ui/mcp-cyclops](https://github.com/cyclops-ui/mcp-cyclops)** — An MCP server that allows AI agents to manage Kubernetes resources through Cyclops abstraction
  <sub>★ 30 · Go · source · pushed 2025-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cyclops-ui/mcp-cyclops.git`</sub>
- **[wenhuwang/mcp-k8s-eye](https://github.com/wenhuwang/mcp-k8s-eye)** — /🏠 - MCP Server for kubernetes management, and analyze your cluster, application health
  <sub>★ 29 · Go · Apache-2.0 · clone · pushed 2025-05-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wenhuwang/mcp-k8s-eye.git`</sub>
- **[localstack/localstack-mcp-server](https://github.com/localstack/localstack-mcp-server)** — A MCP server for LocalStack to manage local AWS environments, including lifecycle operations, infra deployments, log analysis, fault injection, and state management
  <sub>★ 27 · TypeScript · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @localstack/localstack-mcp-server init`</sub>
- **[pibblokto/cert-manager-mcp-server](https://github.com/pibblokto/cert-manager-mcp-server)** — /🐧 ☁️ - mcp server for cert-manager management and troubleshooting
  <sub>★ 24 · Python · Apache-2.0 · source · pushed 2025-08-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/pibblokto/cert-manager-mcp-server.git`</sub>
- **[Sidd27/infrawise](https://github.com/Sidd27/infrawise)** — Cloud infrastructure analysis for AI coding assistants — detects IaC drift, missing indexes, security gaps, and performance anti-patterns across AWS services and databases. 13 tools, works with Claude Code and Cursor
  <sub>★ 22 · TypeScript · MIT · npm · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g infrawise`</sub>
- **[alexbakers/mcp-ipfs](https://github.com/alexbakers/mcp-ipfs)** — upload and manipulation of IPFS storage
  <sub>★ 21 · TypeScript · MIT · clone · pushed 2025-04-10 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/alexbakers/mcp-ipfs.git`</sub>
- **[trilogy-group/aws-pricing-mcp](https://github.com/trilogy-group/aws-pricing-mcp)** — /🏠 - Get up-to-date EC2 pricing information with one call. Fast. Powered by a pre-parsed AWS pricing catalogue
  <sub>★ 21 · Python · MIT · source · pushed 2025-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trilogy-group/aws-pricing-mcp.git`</sub>
- **[liveblocks/liveblocks-mcp-server](https://github.com/liveblocks/liveblocks-mcp-server)** — Create, modify, and delete different aspects of Liveblocks such as rooms, threads, comments, notifications, and more. Additionally, it has read access to Storage and Yjs
  <sub>★ 20 · TypeScript · Apache-2.0 · source · pushed 2026-05-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/liveblocks/liveblocks-mcp-server.git`</sub>
- **[openstack-kr/python-openstackmcp-server](https://github.com/openstack-kr/python-openstackmcp-server)** — OpenStack MCP server for cloud infrastructure management based on openstacksdk
  <sub>★ 20 · Python · Apache-2.0 · source · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/openstack-kr/python-openstackmcp-server.git`</sub>
- **[chaandannn/finopsmcp](https://github.com/getnable/finopsmcp)** — Local-first FinOps copilot. Connect AWS, Azure, GCP, Kubernetes, and 15+ SaaS and AI bills, then ask cost questions in Claude or Cursor, find waste, and get the fix as a pull request you approve. Read-only; your credentials and bill stay on your machine. uvx nable
  <sub>★ 18 · Python · Apache-2.0 · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install finops-mcp`</sub>
- **[espressif/esp-rainmaker-mcp](https://github.com/espressif/esp-rainmaker-mcp)** — Official Espressif MCP Server to manage and control ESP RainMaker Devices
  <sub>★ 18 · Python · Apache-2.0 · clone · pushed 2025-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/espressif/esp-rainmaker-mcp.git`</sub>
- **[hardik-id/azure-resource-graph-mcp-server](https://github.com/hardik-id/azure-resource-graph-mcp-server)** — /🏠 - A Model Context Protocol server for querying and analyzing Azure resources at scale using Azure Resource Graph, enabling AI assistants to explore and monitor Azure infrastructure
  <sub>★ 18 · TypeScript · MIT · source · pushed 2025-05-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hardik-id/azure-resource-graph-mcp-server.git`</sub>
- **[pythonanywhere/pythonanywhere-mcp-server](https://github.com/pythonanywhere/pythonanywhere-mcp-server)** — MCP server implementation for PythonAnywhere cloud platform
  <sub>★ 17 · Python · MIT · source · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pythonanywhere/pythonanywhere-mcp-server.git`</sub>
- **[antonio-mello-ai/mcp-proxmox](https://github.com/antonio-mello-ai/mcp-proxmox)** — Manage Proxmox VE clusters through AI assistants — VMs, containers, snapshots, templates, cloud-init, firewall, and migrations. 29 tools with two-step confirmation for destructive operations
  <sub>★ 16 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-proxmox`</sub>
- **[aashari/mcp-server-aws-sso](https://github.com/aashari/mcp-server-aws-sso)** — AWS Single Sign-On (SSO) integration enabling AI systems to securely interact with AWS resources by initiating SSO login, listing accounts/roles, and executing AWS CLI commands using temporary credentials
  <sub>★ 15 · TypeScript · npm · pushed 2026-03-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @aashari/mcp-server-aws-sso`</sub>
- **[joachimBrindeau/domain-mcp](https://github.com/joachimBrindeau/domain-mcp)** — Manage Dynadot domains, DNS, WHOIS, nameservers, transfers, and aftermarket through 10 AI-friendly composite tools. Install with npx -y domain-mcp
  <sub>★ 13 · TypeScript · MIT · clone · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/joachimBrindeau/domain-mcp.git`</sub>
- **[Spaceship MCP](https://github.com/BartWaardenburg/spaceship-mcp)** — Manage domains, DNS records, contacts, marketplace listings, and more via the Spaceship API
  <sub>★ 13 · TypeScript · MIT · source · pushed 2026-03-06 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/bartwaardenburg/spaceship-mcp.git`</sub>
- **[StacklokLabs/ocireg-mcp](https://github.com/StacklokLabs/ocireg-mcp)** — An SSE-based MCP server that allows LLM-powered applications to interact with OCI registries. It provides tools for retrieving information about container images, listing tags, and more
  <sub>★ 13 · Go · Apache-2.0 · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/StacklokLabs/ocireg-mcp.git`</sub>
- **[thunderboltsid/mcp-nutanix](https://github.com/thunderboltsid/mcp-nutanix)** — /☁️ - Go-based MCP Server for interfacing with Nutanix Prism Central resources
  <sub>★ 13 · Go · MIT · clone · pushed 2026-01-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/thunderboltsid/mcp-nutanix.git`</sub>
- **[mrostamii/rancher-mcp-server](https://github.com/mrostamii/rancher-mcp-server)** — /🏠 - MCP server for the Rancher ecosystem with multi-cluster Kubernetes operations, Harvester HCI management (VMs, storage, networks), and Fleet GitOps tooling
  <sub>★ 12 · Go · Apache-2.0 · npm · pushed 2026-04-27 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g rancher-mcp-server`</sub>
- **[zw008/VMware-Monitor](https://github.com/vmware-skills/VMware-Monitor)** — Read-only VMware vSphere/vCenter monitoring — inventory, alarms, events, host health, VM info, and snapshot listing. 8 strictly read-only tools with code-level zero-destructive guarantee (validated by test fixtures)
  <sub>★ 12 · Python · MIT · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vmware-skills/VMware-Monitor`</sub>
- **[spre-sre/lumino-mcp-server](https://github.com/spre-sre/lumino-mcp-server)** — AI-powered SRE observability for Kubernetes and OpenShift with 40+ tools for Tekton pipeline debugging, log analysis, root cause analysis, and predictive monitoring
  <sub>★ 11 · Python · Apache-2.0 · clone · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/spre-sre/lumino-mcp-server.git`</sub>
- **[johnneerdael/netskope-mcp](https://github.com/johnneerdael/privateaccess-mcp)** — An MCP to give access to all Netskope Private Access components within a Netskope Private Access environments including detailed setup information and LLM examples on usage
  <sub>★ 8 · TypeScript · docker · pushed 2026-05-20 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 3000:3000 netskope-mcp:local`</sub>
- **[L337-org/docker-mcp](https://github.com/L337-org/docker-mcp)** — Manages one or more Docker daemons (local socket or remote over TCP/TLS/SSH) with 156 tools spanning containers, images, Compose, Swarm, Buildx, Scout, and OCI registries. Mark hosts as read-only for safe monitoring; logs and stats exposed as MCP resources
  <sub>★ 8 · Python · MIT · pipx · pushed 2026-09-21 · macOS</sub>
  <sub>`pipx install docker-mcp-server`</sub>
- **[Mogacode-ma/infomaniak-mcp-agent](https://github.com/Mogacode-ma/infomaniak-mcp-agent)** — Unofficial agentic MCP server for Infomaniak (Swiss cloud provider). 54 tools covering web hosting, mail, kDrive, domains, DNS, DNSSEC, FTP/SSH users, AI catalogue and more. Two-phase commit on every destructive operation, history &amp; undo, transparent reverse-engineering of undocumented manager-private endpoints
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g infomaniak-mcp-agent`</sub>
- **[sevalla-hosting/mcp](https://github.com/sevalla-hosting/mcp)** — Manage your entire Sevalla cloud infrastructure from AI agents. Hosted remote server with OAuth — connect in one click, no API keys to configure
  <sub>★ 8 · TypeScript · MIT · docker · pushed 2026-09-09 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 sevalla-mcp`</sub>
- **[ionos-cloud/ionoscloud-mcp](https://github.com/ionos-cloud/ionoscloud-mcp)** — Inspect and manage IONOS CLOUD infrastructure via MCP
  <sub>★ 7 · Go · Apache-2.0 · npx · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx -y @smithery/cli install @ionos-cloud/ionoscloud-mcp --client claude-desktop`</sub>
- **[shipstatic/mcp](https://github.com/shipstatic/mcp)** — Deploy and manage static sites from AI agents. A simpler alternative to Vercel and Netlify for static website hosting — upload files, get a URL, and connect custom domains
  <sub>★ 7 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @shipstatic/mcp`</sub>
- **[anythink-cloud/anythink-cli](https://github.com/anythink-cloud/anythink-cli)** — #️ ☁️ 🍎 🪟 🐧 - Build and run a complete backend from your agent on the Anythink platform: relational data with row-/field-level security, full-text + semantic + geo search, RBAC + BYOK, a workflow/automation engine, a growth &amp; retention engine (email, actionable push, promotions, per-user referral codes + rewards, points/credits), payments + marketplace billing, and a growing catalog of integration
  <sub>★ 6 · C# · MIT · npx · pushed 2026-08-27 · macOS · Linux</sub>
  <sub>`npx -y @anythink-cloud/mcp`</sub>
- **[antonio-mello-ai/mcp-pfsense](https://github.com/antonio-mello-ai/mcp-pfsense)** — Manage pfSense firewalls through AI assistants — firewall rules, DHCP leases/reservations, DNS overrides, gateway monitoring, ARP table, and service management. 17 tools with two-step confirmation for destructive operations
  <sub>★ 6 · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-pfsense`</sub>
- **[erikhoward/adls-mcp-server](https://github.com/erikhoward/adls-mcp-server)** — /🏠 - MCP Server for Azure Data Lake Storage. It can perform manage containers, read/write/upload/download operations on container files and manage file metadata
  <sub>★ 6 · Python · MIT · clone · pushed 2025-05-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/erikhoward/adls2-mcp-server.git`</sub>
- **[CodesWhat/portkey-admin-mcp](https://github.com/CodesWhat/portkey-admin-mcp)** — Portkey Admin API control-plane MCP server with 181 tools across 20 domains, including prompts, configs, keys, analytics, guardrails, integrations, and deployments
  <sub>★ 6 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y portkey-admin-mcp`</sub>
- **[rrmistry/tilt-mcp](https://github.com/rrmistry/tilt-mcp)** — A Model Context Protocol server that integrates with Tilt to provide programmatic access to Tilt resources, logs, and management operations for Kubernetes development environments
  <sub>★ 6 · Python · MIT · pip · pushed 2026-03-08 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install tilt-mcp`</sub>
- **[vishalsg42/munim](https://github.com/vishalsg42/munim)** — One MCP server holding a live session with every client's account at once, so one agent can read across a dozen businesses and write inside only the one you name. Forwards each provider's own MCP tools (Cloudflare, Vercel, Resend, Supabase, Linear, Notion, Sentry, Netlify, Zoho and more) with that client's credentials, plus deterministic DNS and email checks that never call a model. Install: uv to
  <sub>★ 6 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install munim # or: pipx install munim, or: pip install munim`</sub>
- **[VmLia/books-mcp-server](https://github.com/VmLia/books-mcp-server)** — This is an MCP server used for querying books, and it can be applied in common MCP clients, such as Cherry Studio
  <sub>★ 6 · Python · clone · pushed 2025-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/VmLia/books-mcp-server.git`</sub>
- **[friendlygeorge/docker-mcp-server](https://github.com/friendlygeorge/docker-mcp-server)** — Docker container management for AI agents — health checks, auto-restart, Compose lifecycle, and log streaming. 50+ tools for the agent operations loop
  <sub>★ 5 · TypeScript · MIT · source · pushed 2026-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/friendlygeorge/docker-mcp-server.git`</sub>
- **[GeiserX/spinnaker-mcp](https://github.com/GeiserX/spinnaker-mcp)** — A bridge that exposes any Spinnaker instance as an MCP server via the Gate API, enabling management of applications, pipelines, executions, and cloud infrastructure
  <sub>★ 5 · Go · GPL-3.0 · npm · pushed 2026-08-24 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g spinnaker-mcp`</sub>
- **[jasonwilbur/oci-pricing-mcp](https://github.com/jasonwilbur/oci-pricing-mcp)** — Oracle Cloud Infrastructure pricing data with 602 products, cost calculators, and cross-provider comparisons. One-command install for Claude
  <sub>★ 5 · TypeScript · Apache-2.0 · clone · pushed 2026-06-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jasonwilbur/oci-pricing-mcp.git`</sub>
- **[Labs64/NetLicensing-MCP](https://github.com/Labs64/NetLicensing-MCP)** — The official NetLicensing MCP Server is a natural language interface that enables agentic applications to manage the full software licensing lifecycle in Labs64 NetLicensing without writing a single API call
  <sub>★ 5 · HTML · Apache-2.0 · pip · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install netlicensing-mcp`</sub>
- **[zw008/VMware-NSX](https://github.com/vmware-skills/VMware-NSX)** — VMware NSX network management — Segments, Tier-0/Tier-1 Gateways, NAT rules, static/BGP routing, and IPAM pools. 33 tools with dry-run preview, port-count safety checks, and double-confirmation for delete operations
  <sub>★ 5 · Python · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install vmware-nsx-mgmt`</sub>
- **[zw008/VMware-VKS](https://github.com/vmware-skills/VMware-VKS)** — VMware Tanzu / vSphere Kubernetes Service — Supervisor cluster, Namespace, and TKC (Tanzu Kubernetes Cluster) lifecycle management. 20 tools with dry-run mode, kubeconfig export, and double-confirmation for namespace/TKC deletion
  <sub>★ 5 · Python · MIT · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install vmware-vks`</sub>
- **[elevy99927/devops-mcp-webui](https://github.com/elevy99927/devops-mcp-webui)** — /🏠 - MCP Server for Kubernetes integrated with Open-WebUI, bridging the gap between DevOps and non-technical teams. Supports kubectl and helm operations through natural-language commands
  <sub>★ 4 · Python · source · pushed 2025-10-28 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/elevy99927/devops-mcp-webui.git`</sub>
- **[helbertparanhos/easypanel-mcp-server](https://github.com/helbertparanhos/easypanel-mcp-server)** — Full Easypanel control from Claude Code and Cursor — 37 tools for deployments, services, env vars, logs, domains, databases and monitoring. Safety guards require explicit confirmation for all destructive actions
  <sub>★ 4 · TypeScript · MIT · clone · pushed 2026-09-10 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/helbertparanhos/easypanel-mcp-server`</sub>
- **[jasonwilbur/cloud-cost-mcp](https://github.com/jasonwilbur/cloud-cost-mcp)** — Multi-cloud pricing comparison across AWS, Azure, GCP, and OCI with 2,700+ instance types. Real-time pricing from public APIs, workload calculators, and migration savings estimator
  <sub>★ 4 · TypeScript · Apache-2.0 · npm · pushed 2026-06-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cloud-cost-mcp`</sub>
- **[ofershap/mcp-server-cloudflare](https://github.com/ofershap/mcp-server-cloudflare)** — Manage Cloudflare Workers, KV, R2, Pages, DNS, and cache from your IDE
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-08-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y mcp-server-cloudflare-dns`</sub>
- **[ofershap/mcp-server-s3](https://github.com/ofershap/mcp-server-s3)** — AWS S3 operations — list buckets, browse objects, upload/download files, and generate presigned URLs
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx mcp-server-s3`</sub>
- **[zw008/VMware-NSX-Security](https://github.com/vmware-skills/VMware-NSX-Security)** — VMware NSX security — Distributed Firewall policies/rules, Security Groups, Traceflow troubleshooting, and IDS/IPS profiles. 20 tools with active-rule checks before policy deletion and reference-count validation for security groups
  <sub>★ 4 · Python · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install vmware-nsx-security`</sub>
- **[Focus-GTS/eds-mcp-server](https://github.com/Focus-GTS/eds-mcp-server)** — Adobe Edge Delivery Services (AEM EDS) management with 20 tools for preview, publish, bulk operations, content reading, Core Web Vitals, 404 tracking, A/B experiments, site configuration, and redirects. Install: npx @focusgts/eds-mcp-server
  <sub>★ 3 · TypeScript · Apache-2.0 · clone · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Focus-GTS/eds-mcp-server.git`</sub>
- **[aparajithn/agent-deploy-dashboard-mcp](https://github.com/aparajithn/agent-deploy-dashboard-mcp)** — Unified deployment dashboard MCP server across Vercel, Render, Railway, and Fly.io. 9 tools for deploy status, logs, environment variables, rollback, and health checks across all platforms. Free tier with x402 micropayments
  <sub>★ 3 · Python · MIT · clone · pushed 2026-03-07 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/aparajithn/agent-deploy-dashboard-mcp.git`</sub>
- **[davidlandais/ovh-api-mcp](https://github.com/davidlandais/ovh-api-mcp)** — Code Mode MCP server for the entire OVH API. Two tools (search + execute) give LLMs access to all OVH endpoints via sandboxed JavaScript, using ~1,000 tokens instead of thousands of tool definitions
  <sub>★ 3 · Rust · MIT · cargo · pushed 2026-06-15 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`cargo install --git https://github.com/davidlandais/ovh-api-mcp`</sub>
- **[frndchagas/coolify-mcp](https://github.com/frndchagas/coolify-mcp)** — Manage Coolify (self-hosted PaaS): deploy with verified builds, diagnose apps by name or domain, databases with backup schedules (8 engines), offline docs search, and human-confirmed destructive operations. 65 tools generated from the official OpenAPI spec
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @fndchagas/coolify-mcp`</sub>
- **[helbertparanhos/cloudflare-mcp-pro](https://github.com/helbertparanhos/cloudflare-mcp-pro)** — The most complete Cloudflare MCP — 69 tools over the REST API v4 (DNS, Zones, Workers, KV, R2, D1, Pages, WAF, SSL, Email Routing, Logpush, Workers AI) in a single local stdio server, with a server-side human-approval gate on every mutation. npx -y cloudflare-mcp-pro
  <sub>★ 3 · TypeScript · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y cloudflare-mcp-pro`</sub>
- **[lizard-build/lizard-mcp](https://github.com/lizard-build/lizard-mcp)** — Lizard, the AI-native deployment platform for coding agents: ship services, add managed Postgres, Redis and S3, stream logs and metrics, set secrets, scale and attach domains. 33 tools, OAuth 2.1, destructive actions require confirmation
  <sub>★ 3 · TypeScript · MIT · source · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lizard-build/lizard-mcp.git`</sub>
- **[nitin27may/ms-graph-mcp](https://github.com/nitin27may/ms-graph-mcp)** — Microsoft Graph MCP server — 85 tools across Outlook mail &amp; calendar, Teams, OneDrive, SharePoint, OneNote, Planner and Entra ID. Delegated OAuth, stdio or Streamable HTTP
  <sub>★ 3 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from ms-graph-mcp ms-graph-mcp # stdio, for an MCP client`</sub>
- **[x7even/cloudcostsmcp](https://github.com/x7even/cloudcostsmcp)** — Anchor AI FinOps to real, live cloud pricing. 15 tools for AWS, GCP &amp; Azure — public list prices and enterprise negotiated rates (Reserved Instances, Savings Plans, CUDs, EDPs). No credentials needed for AWS and Azure public pricing. pip install opencloudcosts
  <sub>★ 3 · Go · MIT · brew · pushed 2026-07-09 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew tap x7even/opencloudcosts`</sub>
- **[xns-cloud/relayer-mcp](https://github.com/xns-cloud/relayer-mcp)** — Install and manage a self-hosted XNS Relayer — S3-compatible object storage on a decentralized provider network with $0 egress. 15 tools covering prerequisites, account registration, install, claim, health, VPD configuration, S3 verification, CLI credentials, settings, restart, and backups. npx @xns-cloud/relayer-mcp
  <sub>★ 3 · JavaScript · Apache-2.0 · npx · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @xns-cloud/relayer-mcp@latest`</sub>
- **[zw008/VMware-Storage](https://github.com/vmware-skills/VMware-Storage)** — VMware vSphere storage management — datastores (NFS/VMFS), iSCSI software adapter and dynamic targets, and vSAN cluster operations. 11 tools with dry-run preview and double-confirmation for iSCSI configuration changes
  <sub>★ 3 · Python · MIT · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install vmware-storage`</sub>
- **[dockndevai/mcp-kubernetes](https://github.com/dockndevai/mcp-kubernetes)** — Multi-cluster Kubernetes monitoring &amp; operations (pods, logs, deployments, scale/restart, apply, exec) — safe-by-default access modes, namespace/context allowlists, delete/apply/exec gating, dry-run, audit. npx -y @dockndevai/mcp-kubernetes
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-kubernetes.git`</sub>
- **[4everland/4everland-hosting-mcp](https://github.com/4everland/4everland-hosting-mcp)** — An MCP server implementation for 4EVERLAND Hosting enabling instant deployment of AI-generated code to decentralized storage networks like Greenfield, IPFS, and Arweave
  <sub>★ 2 · TypeScript · clone · pushed 2025-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/4everland/4everland-hosting-mcp.git`</sub>
- **[adiosdotdev/mcp](https://github.com/adiosdotdev/mcp)** — Official Adios MCP server for managing workspaces, previews, builds, logs, services, and production deployments
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @adiosdotdev/mcp`</sub>
- **[agentmetal/mcp](https://github.com/agentmetal/mcp)** — Provision, SSH into, run commands on, and manage Linux VPSes from an agent — pay USDC over x402 or by card over HTTP 402, a running box in under 60s. No signup, no API key to buy
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentmetal/mcp.git`</sub>
- **[BlazingCDN/BlazingCDN-MCP](https://github.com/BlazingCDN/BlazingCDN-MCP)** — Official BlazingCDN server: manage CDN zones (TTLs, compression, on-the-fly image resizing, HLS/DASH), purge and warm up cache, traffic metrics, custom domains, cloud storage and Video CDN. 52 tools, read-only by default with opt-in write/delete. Install: npx -y @blazingcdn/mcp
  <sub>★ 2 · TypeScript · MIT · source · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BlazingCDN/BlazingCDN-MCP.git`</sub>
- **[garlicKim21/ratatosk-mcp](https://github.com/garlicKim21/ratatosk-mcp)** — CNCF release intelligence: typed, quoted facts (security fixes, breaking changes, deprecations) from every graduated/incubating project's release notes, updated daily. check_stack compares running versions locally so they never leave your process
  <sub>★ 2 · Go · Apache-2.0 · source · pushed 2026-09-04 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/garlicKim21/ratatosk-mcp.git`</sub>
- **[zw008/VMware-AVI](https://github.com/vmware-skills/VMware-AVI)** — VMware AVI Load Balancer (NSX ALB) management plus AKO Kubernetes integration. 29 tools across virtual services, pools, analytics metrics, and AKO lifecycle (restart/upgrade/force-resync) with double-confirmation for destructive ops
  <sub>★ 2 · Python · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install vmware-avi`</sub>
- **[dockndevai/mcp-oci](https://github.com/dockndevai/mcp-oci)** — Oracle Cloud (OCI) live resource discovery, dependency mapping &amp; reproducible Terraform generation — read-only and secret-redacting. npx -y @dockndevai/mcp-oci
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-oci.git`</sub>
- **[dockndevai/mcp-azure](https://github.com/dockndevai/mcp-azure)** — Azure Resource Manager inventory, tags, VM power &amp; lifecycle — governed with subscription/resource-group allowlists, protected groups, location allowlist, delete gating, and typed confirmation. npx -y @dockndevai/mcp-azure
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dockndevai/mcp-azure.git`</sub>
- **[arnstarn/mcp-server-spotinst](https://github.com/arnstarn/mcp-server-spotinst)** — MCP server for Spot.io (Spotinst) API with 23 tools for managing Ocean clusters, VNGs, Elastigroups, costs, right-sizing, and logs across AWS and Azure with multi-account support
  <sub>★ 1 · Python · MIT · uv · pushed 2026-05-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-server-spotinst`</sub>
- **[alexpota/cloudscope-mcp](https://github.com/alexpota/cloudscope-mcp)** — Azure cloud cost management — spending analysis, forecasts, anomaly detection, budgets, optimization recommendations, idle resource detection, tag-based cost allocation, and cross-subscription queries through natural language
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alexpota/cloudscope-mcp.git`</sub>
- **[Albaker-Group/cloudprice-mcp](https://github.com/Albaker-Group/cloudprice-mcp)** — Compare on-demand compute, block/object storage, managed Postgres, egress &amp; GPU pricing across AWS, Azure, GCP, and OCI, plus FinOps decision tools (RI/Savings Plan break-even, multi-cloud workload TCO, exit-cost migration analysis, and egress arbitrage). 25 tools
  <sub>★ 1 · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install cloudprice-mcp`</sub>
- **[Drop-to-run/drop2run-cli](https://github.com/Drop-to-run/drop2run-cli)** — Publish what an agent just wrote to a live HTTPS URL. Three tools: publish_files for pages written in the chat, publish_dir for a folder on disk, and list_sites. Static hosting on Cloudflare's edge, so no git, no build step and no repository. npx -y @drop2run/mcp
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g drop2run # https://www.npmjs.com/package/drop2run`</sub>
- **[ganakailabs/cloudeval-cli](https://github.com/ganakailabs/cloudeval-cli)** — Access Cloudeval project context and reports for cloud evaluations and reviews. Supports Azure and static AWS CloudFormation evaluation (beta); includes a read-only toolset and requires authentication
  <sub>★ 1 · TypeScript · psh · pushed 2026-09-10 · Win · WSL2 · macOS? · Linux?</sub>
  <sub>`irm https://cli.cloudeval.ai/install.ps1 | iex`</sub>
- **[Infrawise/mcp-server](https://github.com/Infrawise/mcp-server)** — Azure FinOps infrastructure cost optimization: idle resources, rightsizing, and Reserved Instance recommendations for Claude Code
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @infrawise/mcp-server@latest setup`</sub>
- **[kaka-milan-22/kops](https://github.com/kaka-milan-22/kops)** — Read-only kubectl for Claude Code: returns structured JSON, hardcoded safe verbs (no mutation path even with malicious input), Secret/ConfigMap values never returned, plus one-shot cluster triage &amp; inventory
  <sub>★ 1 · Python · MIT · npx · pushed 2026-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector uv --directory /path/to/kops run kops`</sub>
- **[mikusnuz/dynadot-mcp](https://github.com/mikusnuz/dynadot-mcp)** — MCP server for the Dynadot domain registrar API — 60 tools for domain search, registration, DNS, contacts, transfers, and marketplace
  <sub>★ 1 · TypeScript · MIT · npm · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g dynadot-mcp`</sub>
- **[mctlhq/mctl-mcp](https://github.com/mctlhq/mctl-mcp)** — AI-native platform for Kubernetes management and automated GitOps (30+ tools)
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mctlhq/mctl-mcp.git`</sub>
- **[Nebula-Block-Data/nebulablock-mcp-server](https://github.com/Nebula-Block-Data/nebulablock-mcp-server)** — integrates with the fastmcp library to expose the full range of NebulaBlock API functionalities as accessible tools
  <sub>★ 1 · Python · clone · pushed 2025-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Nebula-Block-Data/api-mcp`</sub>
- **[Novence-ai/mcp](https://github.com/Novence-ai/mcp)** — Hosted MCP for creating, checking, deploying, and hosting static sites for AI agents. Streamable HTTP at https://api.novence.ai/mcp
  <sub>★ 1 · JavaScript · MIT · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Novence-ai/mcp.git`</sub>
- **[nikhilnt1234/TokenBurnRate](https://github.com/nikhilnt1234/TokenBurnRate)** — Track LLM token costs across Claude, GPT and Gemini. MCP server + CLI with optimization hints and $ savings estimates. 📇🏠
  <sub>★ 1 · TypeScript · MIT · clone · pushed 2026-06-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nikhilnt1234/TokenBurnRate.git`</sub>
- **[RajeevSirohi/mcp-server-terraform](https://github.com/RajeevSirohi/mcp-server-terraform)** — Safety-first Terraform operations: plan/apply/destroy with two-step confirmation gates, plan risk &amp; cost analysis that flags expensive always-on resources (NAT gateways, EKS, Azure Firewall), drift detection, import/taint/refresh, provider auth pre-flight checks, and audit logging
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @rajsir/mcp-server-terraform`</sub>
- **[shdomi8599/vibie-mcp](https://github.com/shdomi8599/vibie-mcp)** — Deploy static HTML folders to permanent vibie.page URLs in seconds. One-line auto-install (npx vibie-mcp setup) wires up Claude Desktop and Cursor, OAuth device-flow auth, automatic folder marker for repeat deploys without re-typing slugs
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-05-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx vibie-mcp setup`</sub>
- **[trackerfitness729-jpg/sitelauncher-mcp-server](https://github.com/trackerfitness729-jpg/sitelauncher-mcp-server)** — Deploy live HTTPS websites in seconds. Instant subdomains ($1 USDC) or custom .xyz domains ($10 USDC) on Base chain. Templates for crypto tokens and AI agent profiles
  <sub>★ 1 · TypeScript · npx · pushed 2026-03-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx sitelauncher-mcp-server`</sub>
- **[Woobox/hatchable-mcp](https://github.com/Woobox/hatchable-mcp)** — Build and host full-stack web apps and sites on Hatchable from any MCP client. DB, auth, storage, domains, and cron per project. Free tier
  <sub>★ 1 · JavaScript · MIT · docker · pushed 2026-04-23 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i hatchable-mcp # stdio ↔ https://hatchable.com/mcp`</sub>
- **[zyli5313/dochost-mcp](https://github.com/zyli5313/dochost-mcp)** — Publish Markdown or HTML to a public shareable link straight from your assistant. Streamable HTTP with OAuth, no API keys; published pages are served script-free from a separate cookieless origin
  <sub>★ 1 · JavaScript · MIT · docker · pushed 2026-09-07 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i dochost-mcp`</sub>
- **[AIops-tools/K8s-AIops](https://github.com/AIops-tools/K8s-AIops)** — Governed Kubernetes operations (k3s/EKS/GKE/AKS) — workloads, batch jobs, config, storage, networking, and rollout management (55 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, dry-run, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install k8s-aiops`</sub>
- **[dockndevai/mcp-openshift](https://github.com/dockndevai/mcp-openshift)** — OpenShift &amp; Kubernetes operations — projects, pods, logs, deployments/deploymentconfigs, routes, services, builds; scale, rollout-restart, apply and delete — governed with read-only/read-write/admin modes, namespace allowlists, protected namespaces, apply/delete gating, dry-run, Secret redaction, and typed confirmation. Connect with a web-console token or username/password (local IdP). npx -y @doc
  <sub>TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @dockndevai/mcp-openshift`</sub>
- **[AIops-tools/Nutanix-AIops](https://github.com/AIops-tools/Nutanix-AIops)** — Governed Nutanix Prism Central v4 operations — cluster, VM (AHV + ESXi), storage, networking, snapshot/DR, alerts, and LCM (51 tools) with unbypassable audit logging (MCP + CLI), budget/runaway guards, dry-run, and undo/rollback
  <sub>Python · MIT · uv · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install nutanix-aiops # or: pipx install nutanix-aiops`</sub>
- **[AkaciaNL/basicdeploy-mcp](https://github.com/AkaciaNL/basicdeploy-mcp)** — Deploy and manage BasicDeploy containers, each with a PostgreSQL database, S3-compatible object storage, env vars, and a public URL provisioned automatically. Create containers, deploy apps (Node/Python/Go/Docker, auto-detected), run commands, read logs, and toggle always-on. Install: npx -y basicdeploy-mcp
  <sub>JavaScript · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AkaciaNL/basicdeploy-mcp.git`</sub>
- **[elementfm/mcp](https://gitlab.com/elementfm/mcp)** — Open source podcast hosting platform
  <sub>website</sub>
  <sub>`https://gitlab.com/elementfm/mcp`</sub>
- **[hostodo/hostodo-mcp](https://github.com/hostodo/hostodo-mcp)** — Hosted MCP endpoint for Hostodo VPS management: list VM details, power-control, rename, reinstall from OS templates, toggle per-VM exec, run bounded/async guest-agent commands, and upload/install artifacts with scoped tokens and audit logs
  <sub>JavaScript · MIT · docker · pushed 2026-07-02 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -i -e HOSTODO_MCP_TOKEN=<hostodo_agent_token> hostodo-mcp`</sub>
- **[huangdun/tempmd-mcp](https://github.com/tempmd/tempmd-mcp)** — Publish agent-made artifacts (HTML, Markdown, CSV, Mermaid) to temp.md — one stable public link that updates in place. Anonymous publish with no API key, activity-based expiry with restore. Install: npx tempmd-mcp
  <sub>TypeScript · MIT · source · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/huangdun/tempmd-mcp.git`</sub>
- **[Ilmar7786/marzban-sdk](https://github.com/Ilmar7786/marzban-sdk/tree/main/packages/mcp)** — /🏠 - MCP server for the Gozargah/Marzban proxy/VPN panel API, built on the typed marzban-sdk client. 21 tools across users, subscriptions, nodes, hosts, config and system stats, plus 3 investigation prompts. Env-only credentials (never a tool argument), profile-gated tool visibility (readonly/standard/full), and a one-time confirmation token required before any destructive call. npx -y marzban-mcp
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-11</sub>
  <sub>`git clone https://github.com/Ilmar7786/marzban-sdk.git && cd marzban-sdk/packages/mcp`</sub>
- **[jdubois/azure-cli-mcp](https://github.com/jdubois/azure-cli-mcp)** — A wrapper around the Azure CLI command line that allows you to talk directly to Azure
  <sub>unavailable</sub>
- **[krovacloud/krova-node](https://github.com/krovacloud/krova-node)** — Provision and manage Krova Cloud Cubes — Firecracker microVMs with their own kernel, full root access, and no public IP until you open a port — plus custom domains, TCP port mappings, and snapshots. Billed by the minute. Install with npx -y @krovacloud/mcp
  <sub>TypeScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/krovacloud/krova-node.git`</sub>
- **[shiped-app/shiped-mcp](https://github.com/shiped-app/shiped-mcp)** — Deploy AI-generated HTML/CSS/JS to an instant public HTTPS URL from any MCP agent (Claude Code, Codex, Cursor, Kiro, Copilot). Remote HTTP MCP endpoint with OAuth 2.1 device-flow login — no API key to mint or store
  <sub>TypeScript · npx · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @shiped/mcp login`</sub>
- **[liquidmetal-ai/raindrop-mcp](https://docs.liquidmetal.ai/tutorials/claude-code-mcp-setup/)** — The best way to deploy cloud infrastructure using Claude Code and MCP
  <sub>website</sub>
  <sub>`https://docs.liquidmetal.ai/tutorials/claude-code-mcp-setup/`</sub>
- **[luno-cms/mcp](https://github.com/luno-cms/mcp)** — LUNO — AI Backend Platform (luno.rest): hosted SaaS backend (CMS, Forms, Auth, Storage) for Claude Code, Cursor, and Codex. Not the cryptocurrency Luno exchange MCP. Registry: io.github.luno-cms/mcp
  <sub>TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @luno-cms/mcp setup`</sub>
- **[ni-c/hetzner-dns-mcp](https://github.com/ni-c/hetzner-dns-mcp)** — Manage Hetzner DNS zones and records through the current Hetzner Cloud API (the legacy dns.hetzner.com API was shut down in May 2026). 22 tools: zone and RRSet CRUD, zonefile import/export, TTL and protection changes, primary nameservers, and async action tracking. Every destructive tool requires an explicit confirm. npx -y hetzner-dns-mcp
  <sub>TypeScript · MIT · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -i --rm -e HETZNER_API_TOKEN=your-token ghcr.io/ni-c/hetzner-dns-mcp`</sub>
- **[ni-c/wg-easy-mcp](https://github.com/ni-c/wg-easy-mcp)** — Administer a self-hosted wg-easy (WireGuard Easy) v15 instance: list, create, update, enable/disable and delete VPN clients, fetch configuration files and QR codes, generate one-time links, and inspect server status. Deleting a client takes a two-step, server-issued confirmation token; admin secrets are redacted from responses. npx -y wg-easy-mcp
  <sub>TypeScript · MIT · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ni-c/wg-easy-mcp.git`</sub>
- **[newageflyfish-max/volthq](https://github.com/newageflyfish-max/volthq)** — Compute price oracle for AI agents. Compare inference pricing across 8 providers in real time with routing recommendations and spend tracking. One-command install: npx volthq-mcp-server --setup
  <sub>unavailable</sub>
- **[openpouch/openpouch](https://github.com/openpouch/openpouch)** — Agent-native hosting: deploy any app to a live URL in one command — no account, no dashboard, no CAPTCHA. Full deploy lifecycle as tools (deploy, verify, logs, inspect, rollback, list/delete); production approval stays human-only. Apache-2.0
  <sub>TypeScript · Apache-2.0 · npx · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx openpouch deploy`</sub>
- **[plopino/plopino-mcp](https://github.com/plopino/plopino-mcp)** — Publish a page, a file, or a folder to a public URL. Two tools: publish_html for content written in the chat, and publish_path for something already on disk — folder structure preserved, no need to zip first. Publishing is anonymous by default; no account or API key required. npx -y plopino
  <sub>JavaScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/plopino/plopino-mcp.git`</sub>
- **[Poiuyhje/eqvps-mcp](https://github.com/Poiuyhje/eqvps-mcp)** — No-KYC crypto-paid VPS that AI agents rent and fully operate over MCP: discover plans, register programmatically (no human, OTP or KYC), pay with USDC/USDT on Base or Ethereum, then provision and control the VPS — power, hostname, root-password reset, reinstall, metrics, cancellation and operator delegation. Hosted remote server at mcp.eqvps.com (Streamable HTTP)
  <sub>JavaScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Poiuyhje/eqvps-mcp.git`</sub>
- **[publee-dev/mcp](https://github.com/publee-dev/mcp)** — Publish AI-generated HTML or static files to a shareable .publee.site URL in seconds. Works anonymously with zero setup (7-day retention); an API token adds permanent hosting, in-place updates that keep the same URL, and limited-sharing visibility (password, members-only)
  <sub>JavaScript · MIT · source · pushed 2026-08-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/publee-dev/mcp.git`</sub>
- **[pulumi/mcp-server](https://github.com/pulumi/mcp-server)** — MCP server for interacting with Pulumi using the Pulumi Automation API and Pulumi Cloud API. Enables MCP clients to perform Pulumi operations like retrieving package information, previewing changes, deploying updates, and retrieving stack outputs programmatically
  <sub>unavailable</sub>
- **[stevejford/shiply-mcp](https://github.com/stevejford/shiply-mcp)** — Agent-first web host: publish a static site or edge function to the web in one call (no account), then manage updates, custom domains, SSL, env vars, databases, and email. Hosted remote MCP at https://shiply.now/mcp
  <sub>JavaScript · MIT · npx · pushed 2026-07-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx shiply-mcp`</sub>
- **[stevysmith/stacktree-mcp](https://github.com/stevysmith/stacktree-mcp)** — Publish HTML an agent makes to a private, unguessable URL. Every link is private by default; gate one with a passcode or a company-email domain that viewers pass without creating an account, set an expiry or burn-after-read, and replace it in place so the shared URL always shows the current version. Paid plans add read analytics on who opened the page. OAuth with dynamic client registration, or a
  <sub>TypeScript · MIT · source · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stevysmith/stacktree-mcp.git`</sub>
- **[akkireddy-challa/k8s-mcp-server](https://github.com/akkireddy-challa/k8s-mcp-server)** — MCP server for Kubernetes cluster operations — inspect pods, deployments, services, and logs via AI agents
  <sub>Python · MIT · clone · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/akkireddy-challa/k8s-mcp-server.git`</sub>

## Monitoring

<sub>Entries 1–41 of 87. The rest are on this page's other parts, linked above and below.</sub>

- **[grafana/mcp-grafana](https://github.com/grafana/mcp-grafana)** — Search dashboards, investigate incidents and query datasources in your Grafana instance
  <sub>★ 3.5k · Go · Apache-2.0 · uv · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uvx mcp-grafana`</sub>
- **[getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp)** — Sentry.io integration for error tracking and performance monitoring
  <sub>★ 858 · TypeScript · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @sentry/mcp-server@latest --access-token=sentry-user-token`</sub>
- **[Higangssh/homebutler](https://github.com/Higangssh/homebutler)** — All-in-one homelab management MCP server. Monitor system resources, manage Docker containers, Wake-on-LAN, scan networks, check open ports, and run alerts — across multiple servers via SSH. Single 10MB binary, zero dependencies
  <sub>★ 290 · Go · MIT · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g homebutler`</sub>
- **[mpeirone/zabbix-mcp-server](https://github.com/mpeirone/zabbix-mcp-server)** — Zabbix integration for hosts, items, triggers, templates, problems, data and more
  <sub>★ 255 · Python · GPL-3.0 · docker · pushed 2026-05-10 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -e ZABBIX_URL=https://zabbix.example.com -e ZABBIX_TOKEN=your_token zabbix-mcp-server`</sub>
- **[VictoriaMetrics-Community/mcp-victoriametrics](https://github.com/VictoriaMetrics/mcp-victoriametrics)** — Provides comprehensive integration with your VictoriaMetrics instance APIs and documentation for monitoring, observability, and debugging tasks related to your VictoriaMetrics instances
  <sub>★ 234 · Go · Apache-2.0 · docker · pushed 2026-08-23 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -d --name mcp-victoriametrics \`</sub>
- **[pydantic/logfire-mcp](https://github.com/pydantic/logfire-mcp)** — Provides access to OpenTelemetry traces and metrics through Logfire
  <sub>★ 160 · Python · MIT · source · pushed 2026-07-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pydantic/logfire-mcp.git`</sub>
- **[dynatrace-oss/dynatrace-mcp](https://github.com/dynatrace-oss/dynatrace-mcp)** — Leverage AI-driven observability, security, and automation to analyze anomalies, logs, traces, events, metrics
  <sub>★ 138 · TypeScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @dynatrace-oss/dynatrace-mcp-server@latest --help`</sub>
- **[andreisirbu91-lab/MCPSpend](https://github.com/andreisirbu91-lab/MCPSpend)** — Real-time cost observability for MCP tool calls. Transparent proxy auto-detects every MCP client (Claude Desktop, Cursor, Windsurf, VS Code, Claude Code, Zed, Continue.dev, Cline, Goose) and attributes spend per tool, per project, per end-customer. npx @mcpspend/proxy add install. Free tier 25K calls/month, no card. MIT proxy on npm. EU-hosted, GDPR-ready
  <sub>★ 111 · TypeScript · MIT · npx · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes @mcpspend/proxy@latest init --key mcps_live_xxx`</sub>
- **[avivsinai/langfuse-mcp](https://github.com/avivsinai/langfuse-mcp)** — Query Langfuse traces, debug exceptions, analyze sessions, and manage prompts. Full observability toolkit for LLM applications
  <sub>★ 106 · Python · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add avivsinai/langfuse-mcp -g -y`</sub>
- **[seekrays/mcp-monitor](https://github.com/seekrays/mcp-monitor)** — A system monitoring tool that exposes system metrics via the Model Context Protocol (MCP). This tool allows LLMs to retrieve real-time system information through an MCP-compatible interface.（support CPU、Memory、Disk、Network、Host、Process）
  <sub>★ 91 · Go · Apache-2.0 · clone · pushed 2025-08-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/seekrays/mcp-monitor.git`</sub>
- **[hyperb1iss/lucidity-mcp](https://github.com/hyperb1iss/lucidity-mcp)** — Enhance AI-generated code quality through intelligent, prompt-based analysis across 10 critical dimensions from complexity to security vulnerabilities
  <sub>★ 90 · Python · Apache-2.0 · clone · pushed 2025-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hyperbliss/lucidity-mcp.git`</sub>
- **[ruslanlap/pagespeed-insights-mcp](https://github.com/ruslanlap/pagespeed-insights-mcp)** — 19-tool MCP server for Google PageSpeed Insights, Chrome UX Report (CrUX) and Lighthouse: page analysis &amp; comparison, real-user CrUX data (URL + origin), batch analysis, baselines/regression tracking, deep diagnostics (network, JS, images, render-blocking, third-party impact), visual analysis and a prioritized recommendations engine. Published on npm (npx pagespeed-insights-mcp); listed in the Off
  <sub>★ 63 · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g pagespeed-insights-mcp`</sub>
- **[last9/last9-mcp-server](https://github.com/last9/last9-mcp-server)** — Seamlessly bring real-time production context—logs, metrics, and traces—into your local environment to auto-fix code faster
  <sub>★ 62 · Go · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @last9/mcp-server@latest`</sub>
- **[metoro-io/metoro-mcp-server](https://github.com/metoro-io/metoro-mcp-server)** — Query and interact with kubernetes environments monitored by Metoro
  <sub>★ 51 · Go · MIT · clone · pushed 2026-06-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/metoro-io/metoro-mcp-server.git`</sub>
- **[tumf/grafana-loki-mcp](https://github.com/tumf/grafana-loki-mcp)** — An MCP server that allows querying Loki logs through the Grafana API
  <sub>★ 29 · Python · MIT · pip · pushed 2026-01-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install grafana-loki-mcp`</sub>
- **[inspektor-gadget/ig-mcp-server](https://github.com/inspektor-gadget/ig-mcp-server)** — Debug your Container and Kubernetes workloads with an AI interface powered by eBPF
  <sub>★ 27 · Go · Apache-2.0 · source · pushed 2026-08-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/inspektor-gadget/ig-mcp-server.git`</sub>
- **[agentkitai/agentlens](https://github.com/agentkitai/agentlens)** — Tamper-evident observability for AI agents: a SHA-256 hash-chained audit log with chain verification and signed export (EU AI Act Art. 12). Instrument any agent with zero code via npx -y @agentlensai/mcp; also ingests OpenTelemetry GenAI traces
  <sub>★ 23 · TypeScript · MIT · npx · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @agentkitai/agentlens-server`</sub>
- **[MindscapeHQ/server-raygun](https://github.com/MindscapeHQ/mcp-server-raygun)** — Raygun API V3 integration for crash reporting and real user monitoring
  <sub>★ 22 · source · pushed 2026-09-02</sub>
  <sub>`git clone https://github.com/MindscapeHQ/mcp-server-raygun.git`</sub>
- **[GeiserX/genieacs-mcp](https://github.com/GeiserX/genieacs-mcp)** — Go-based MCP server that bridges any GenieACS (TR-069 ACS) instance, exposing device data, firmware management, and CPE actions (reboot, parameter refresh, firmware download) over JSON-RPC. Docker image available
  <sub>★ 17 · Go · GPL-3.0 · npm · pushed 2026-08-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g genieacs-mcp`</sub>
- **[alilxxey/openobserve-community-mcp](https://github.com/alilxxey/openobserve-community-mcp)** — Read-only MCP server for OpenObserve Community Edition via REST API. Search logs, traces, stream schemas, and dashboards without requiring the Enterprise license
  <sub>★ 16 · Python · GPL-3.0 · uv · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from openobserve-community-mcp openobserve-mcp init-config`</sub>
- **[smigolsmigol/llmkit](https://github.com/smigolsmigol/llmkit)** — AI API cost tracking and budget enforcement across 11 LLM providers. 6 tools for spend analytics, budget monitoring, session summaries, and key management
  <sub>★ 16 · TypeScript · MIT · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @f3d1/llmkit-cli -- python my_agent.py`</sub>
- **[inventer-dev/mcp-internet-speed-test](https://github.com/inventer-dev/mcp-internet-speed-test)** — Internet speed testing with network performance metrics including download/upload speed, latency, jitter analysis, and CDN server detection with geographic mapping
  <sub>★ 14 · Python · MIT · uv · pushed 2026-03-09 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx mcp-internet-speed-test`</sub>
- **[spanlens/Spanlens](https://github.com/spanlens/Spanlens)** — Query your Spanlens LLM observability from any MCP client. 7 read tools for request logs, agent traces, cost stats, anomalies, model-savings, and per-user analytics across OpenAI, Anthropic, and Gemini. Open source, self-hostable. npx -y @spanlens/mcp-server
  <sub>★ 13 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @spanlens/cli init`</sub>
- **[enmanuelmag/heimdall-mcp](https://github.com/enmanuelmag/heimdall-mcp)** — Transparent proxy for any MCP server that intercepts all JSON-RPC messages, measures latency, and stores traces in SQLite, PostgreSQL, or MySQL. Exports OpenTelemetry (OTLP) spans to Jaeger, Tempo, or Grafana. Supports stdio, HTTP, and SSE transports. npx @cardor/heimdall-mcp
  <sub>★ 11 · TypeScript · npm · pushed 2026-07-16 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @cardor/heimdall-mcp`</sub>
- **[edgedelta/edgedelta-mcp-server](https://github.com/edgedelta/edgedelta-mcp-server)** — Interact with Edge Delta anomalies, query logs / patterns / events, and pinpoint root causes and optimize your pipelines
  <sub>★ 9 · Go · MIT · docker · pushed 2026-07-08 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run mcp/edgedelta …`</sub>
- **[iris-eval/mcp-server](https://github.com/iris-eval/mcp-server)** — MCP-native agent evaluation and observability server with trace logging, output quality evaluation, cost tracking, 12 built-in eval rules, real-time dashboard, and PII detection
  <sub>★ 9 · TypeScript · MIT · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @iris-eval/mcp-server`</sub>
- **[rbmuller/scherlok](https://github.com/rbmuller/scherlok)** — Zero-config data quality monitoring across Postgres, BigQuery, Snowflake, MySQL, and DuckDB. Profile a warehouse, detect anomalies (volume, schema drift, freshness, NULLs, distribution, cardinality), with optional dbt manifest lineage. Read-only — connection resolved server-side, never passed via the model
  <sub>★ 9 · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from "scherlok[duckdb]" scherlok demo`</sub>
- **[utapyngo/sentry-mcp-rs](https://github.com/utapyngo/sentry-mcp-rs)** — Fast and minimal Sentry MCP server written in Rust
  <sub>★ 9 · Rust · MIT · cargo · pushed 2026-03-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install sentry-mcp`</sub>
- **[imprvhub/mcp-status-observer](https://github.com/imprvhub/mcp-status-observer)** — Model Context Protocol server for monitoring Operational Status of major digital platforms in Claude Desktop
  <sub>★ 8 · TypeScript · MPL-2.0 · clone · pushed 2026-07-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/imprvhub/mcp-status-observer`</sub>
- **[mikusnuz/umami-mcp](https://github.com/mikusnuz/umami-mcp)** — Full-coverage MCP server for Umami Analytics API v2 — 66 tools for websites, stats, sessions, events, reports, users, teams, and realtime monitoring
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @mikusnuz/umami-mcp`</sub>
- **[lodordev/mcp-tautulli](https://github.com/lodordev/mcp-tautulli)** — Tautulli (Plex media server monitoring) with 11 read-only tools for activity, history, library stats, user stats, transcode analysis, and resolution breakdowns
  <sub>★ 7 · Python · MIT · uv · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install mcp-tautulli`</sub>
- **[gjenkins20/webmin-mcp-server](https://github.com/gjenkins20/webmin-mcp-server)** — MCP server for Webmin with 61 tools for Linux system administration: services, users, storage, security, databases, and more
  <sub>★ 6 · Python · MIT · clone · pushed 2026-07-07 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/gjenkins20/webmin-mcp-server.git`</sub>
- **[Jwrede/llmprobe](https://github.com/Jwrede/llmprobe)** — Synthetic monitoring for LLM inference endpoints. Measure TTFT, latency, throughput, and errors across OpenAI, Anthropic, Google, Azure, Bedrock, and local servers (vLLM, SGLang, Ollama). CLI + MCP server with Prometheus and OpenTelemetry export
  <sub>★ 6 · Go · MIT · go · pushed 2026-05-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/Jwrede/llmprobe@latest`</sub>
- **[incu6us/loki-mcp-server](https://github.com/incu6us/loki-mcp-server)** — An MCP server for querying Grafana Loki directly with a discovery-first workflow — labels, values, series, and LogQL queries without requiring Grafana
  <sub>★ 6 · Go · MIT · go · pushed 2026-09-11 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/incu6us/loki-mcp-server/cmd/loki-mcp-server@latest`</sub>
- **[TANTIOPE/datadog-mcp-server](https://github.com/TANTIOPE/datadog-mcp-server)** — MCP server providing comprehensive Datadog observability access for AI assistants. Features grep-like log search, APM trace filtering with duration/status/error queries, smart sampling modes for token efficiency, and cross-correlation between logs, traces, and metrics
  <sub>★ 6 · TypeScript · Apache-2.0 · source · pushed 2026-09-19 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/TANTIOPE/datadog-mcp-server.git`</sub>
- **[kascada/logmcp](https://github.com/kascada/logmcp)** — Read-only log access for AI assistants over HTTPS. Whitelist log files on your Linux server; AI can search and read them without shell access. Token-authenticated, syslog-audited
  <sub>★ 5 · Go · MIT · go · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`go install github.com/kascada/logmcp@latest`</sub>
- **[magna-nz/tallybook](https://github.com/magna-nz/tallybook)** — Prices every Claude Code and Codex session already on disk and lets the agent ask what it's spending mid-session: cost by session, sub-agent and model, week-on-week comparison, and plain-English findings with applyable patches. No proxy, no API key, nothing leaves the machine. Install: brew install --cask magna-nz/tap/tallybook
  <sub>★ 5 · Go · MIT · go · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/magna-nz/tallybook/cmd/tallybook@latest`</sub>
- **[ShekharBhardwaj/AgenticLedger](https://github.com/ShekharBhardwaj/AgenticLedger)** — Agents query their own ledger: sessions, costs, loop runs, and stuck-loop flags captured by the Agentic Ledger transparent-proxy flight recorder (local-first, MIT). Install: pip install agentic-ledger
  <sub>★ 5 · Python · MIT · uv · pushed 2026-09-17 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`uv tool install agentic-ledger # or: pipx install agentic-ledger, or pip install -U agentic-ledger`</sub>
- **[vdalhambra/siteaudit-mcp](https://github.com/vdalhambra/siteaudit-mcp)** — Instant website audits with 11 tools — full SEO audit (20+ checks), security headers and SSL verification, Lighthouse performance metrics, multi-site comparison, broken link checker, WCAG accessibility audit, Schema.org structured data validation, competitor gap analysis, and robots.txt parsing. No API keys required
  <sub>★ 5 · Python · MIT · npx · pushed 2026-04-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @smithery/cli install @vdalhambra/siteaudit --client claude`</sub>
- **[alimuratkuslu/byok-observability-mcp](https://github.com/alimuratkuslu/byok-observability-mcp)** — Comprehensive MCP server for Grafana, Prometheus, Kafka UI, and Datadog with a secure "Bring Your Own Key" or BYOK model
  <sub>★ 4 · TypeScript · MIT · npx · pushed 2026-04-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx byok-observability-mcp --init`</sub>
- **[bmdhodl/agent47](https://github.com/bmdhodl/agent47)** — Runtime guardrails and incident read access for coding agents. Query AgentGuard traces, alerts, usage, costs, and budget health
  <sub>★ 4 · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bmdhodl/agent47.git`</sub>

Page **4** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · **4** · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · [7](mcp-servers-punkpeye-7.md) — [continue on page 5 →](mcp-servers-punkpeye-5.md)

---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
