# MCP Servers (punkpeye)

A collection of MCP servers.

Curated by **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

5,011 entries · 4,999 distinct repos · 60 sections

[← back to the mega list](../README.md)

Page **7** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · **7**.

## Contents

- [Environment &amp; Nature](#environment--nature) (12)
- [Health &amp; Wellness](#health--wellness) (13)
- [Accessibility](#accessibility) (5)
- [Aerospace &amp; Astrodynamics](#aerospace--astrodynamics) (3)
- [Jobs](#jobs) (3)

## Environment &amp; Nature

<sub>Entries 10–12 of 12. The rest are on this page's other parts, linked above and below.</sub>

- **[stevensu04/eco-router-mcp](https://github.com/stevensu04/eco-router-mcp)** — Picks the lowest-carbon AWS, Google Cloud or Azure region for a workload. Maps all 134 public regions to their electricity grids and ranks them by carbon intensity and estimated latency, with EU/EEA data residency filters. find_clean_window finds the cleanest start time for batch jobs over the next 72 hours. Works without an API key using annual averages (grid-level for the US and Canada); add an
  <sub>★ 1 · TypeScript · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stevensu04/eco-router-mcp.git`</sub>
- **[ambeelabs/ambee-mcp](https://github.com/ambeelabs/ambee-mcp)** — Live air quality, pollen and weather data from Ambee
  <sub>JavaScript · MIT · clone · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/getambee/ambee-mcp-server.git`</sub>
- **[bartosz-kuc/honest-gios-air-mcp](https://github.com/bartosz-kuc/honest-gios-air-mcp)** — Air-quality data from Poland's GIOŚ monitoring network via its keyless public API. Tools: list_stations (by city or voivodeship), get_station_sensors, get_sensor_readings (recent hourly values), get_air_index (index category, critical pollutant). Runs locally, no third-party middleman
  <sub>Python · MIT · clone · pushed 2026-11-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bartosz-kuc/honest-gios-air-mcp.git`</sub>

## Health &amp; Wellness

- **[Mason-Levyy/myfitnesspal-mcp](https://github.com/Mason-Levyy/myfitnesspal-mcp)** — Read and write your MyFitnessPal diary: search foods with macros, log meals, weight, water, and exercise, and chart nutrition trends
  <sub>★ 37 · Python · MIT · clone · pushed 2026-11-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Mason-Levyy/myfitnesspal-mcp`</sub>
- **[Wewoc/Garmin_Local_Archive](https://github.com/Wewoc/Garmin_Local_Archive)** — Archives Garmin Connect health data locally (steps, HR, sleep, body battery) as JSON, no cloud. Also pulls context data (weather, pollen, air quality/particulate matter) alongside health metrics. Built-in MCP server (with SQLite cache) exposes the archive for querying via LLM tool calls
  <sub>★ 28 · Python · GPL-3.0 · source · pushed 2026-11-22 · Win</sub>
  <sub>`git clone https://github.com/Wewoc/Garmin_Local_Archive.git`</sub>
- **[Jezue/fitatu_library](https://github.com/Jezue/fitatu_library)** — Unofficial MCP server for Fitatu, the Polish calorie counter: read and log meals, weight, water, body measurements and workouts, check calories and macros left, set goals and get weekly reports. 47 tools (26 read-only), read-only and demo modes, stdio or HTTP with a token; on PyPI (uvx --from "fitatu-api[mcp]" fitatu-mcp) and as a Claude Desktop .mcpb
  <sub>★ 27 · Python · MIT · uv · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from "fitatu-api[mcp]" fitatu-mcp`</sub>
- **[io.github.PhilipAD/health-export-mcp](https://github.com/PhilipAD/health-export-mcp)** — Read-only, local-first queries of Apple Health metrics
  <sub>★ 12 · JavaScript · MIT · npx · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y health-export-mcp --doctor`</sub>
- **[Thecimal/quantified-self-mcp](https://github.com/Thecimal/quantified-self-mcp)** — Query personal health and finance data stored in local SQLite files, without any cloud service
  <sub>★ 9 · Python · MIT · pip · pushed 2026-11-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install quantified-self-mcp`</sub>
- **[Bartolome69/garmin-mcp](https://github.com/Bartolome69/garmin-mcp)** — Garmin Connect for ChatGPT and Claude: read runs, sleep, HRV and recovery, and write structured workouts and training plans to the Garmin calendar so they sync to the watch. Hosted at daash.run, or run it yourself
  <sub>★ 8 · Python · MIT · script · pushed 2026-11-27 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Bartolome69/garmin-mcp/main/scripts/bootstrap.sh | bash`</sub>
- **[littlenew117/mibly-apple-health-mcp](https://github.com/littlenew117/mibly-apple-health-mcp)** — Apple Health data (sleep, steps, heart rate, HRV, workouts, body measurements) pushed from the Mibly iPhone app, stored encrypted on your own machine. Local-first, no cloud or telemetry
  <sub>★ 6 · TypeScript · MIT · source · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/littlenew117/mibly-apple-health-mcp.git`</sub>
- **[leonhardprinz/healthaccess-mcp](https://github.com/leonhardprinz/healthaccess-mcp)** — Apple Health and Apple Watch data from local files: workouts with every interval and pool length, daily sleep, HRV and vitals, written as JSON by a free iPhone app into a folder you own. Also puts AI-written workout plans back on the Apple Watch
  <sub>★ 2 · Swift · MIT · npx · pushed 2026-11-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y healthaccess-mcp`</sub>
- **[lewo-media/safe-mind-tools](https://github.com/lewo-media/safe-mind-tools)** — Create and run the legally required psychological risk assessment (GBU Psyche) for German companies via Safe Mind: onboard accounts, set up departments, create survey drafts, and read anonymity-protected aggregated results
  <sub>TypeScript · MIT · npm · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g safe-mind`</sub>
- **[findsaunaplunge/mcp](https://github.com/findsaunaplunge/mcp)** — Cold plunge, sauna and contrast-therapy venues across US metros, with dated temperatures and prices from each venue's own pages, plus city stats
  <sub>TypeScript · MIT · source · pushed 2026-09-05 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/findsaunaplunge/mcp.git`</sub>
- **[Philongevity/phi-mcp-server](https://github.com/Philongevity/phi-mcp-server)** — Guideline-cited lab-results analysis for chronic conditions (type 2 diabetes, kidney, lupus, cancer survivorship): flags missing or overdue tests with the guideline cited. Free sample report; synthetic/de-identified values only
  <sub>TypeScript · Apache-2.0 · source · pushed 2026-11-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Philongevity/phi-mcp-server.git`</sub>
- **[proscar87/oura-mcp](https://github.com/proscar87/oura-mcp)** — Raw access to all Oura Ring API v2 collections with full pagination and page counts, without server-side analysis
  <sub>Python · MIT · uv · pushed 2026-11-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uvx --from mcp-oura oura-mcp`</sub>
- **[t4dhg/mcp-eudamed](https://github.com/t4dhg/mcp-eudamed)** — Read-only search of EU medical device and economic operator records, with source links and an evidence checklist. No API key required
  <sub>TypeScript · MIT · source · pushed 2026-11-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/t4dhg/mcp-eudamed.git`</sub>

## Accessibility

- **[kinti/a11y-toolkit](https://github.com/kinti/a11y-toolkit)** — WCAG 2.2 accessibility tools: color contrast checks including text over images, EU accessibility declaration generation and an aria-live announcement monitor
  <sub>★ 18 · Python · MIT · npx · pushed 2026-11-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y -p @kinti/a11y-toolkit a11y-toolkit-mcp`</sub>
- **[mishan/shotbox](https://github.com/mishan/shotbox)** — Runs real GUI programs in a sealed X11 or Wayland session where an agent can read the accessible tree, take screenshots and clips with sound, click, type and drive gamepads, then check what it finds: unnamed controls, contrast, Tab order, screen reader announcements and audio dropouts
  <sub>★ 2 · Python · MIT · pipx · pushed 2026-11-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install --system-site-packages shotbox`</sub>
- **[kim-dongho/krds-a11y-mcp](https://github.com/kim-dongho/krds-a11y-mcp)** — Korea's government design system (KRDS) components with KWCAG 2.2 (Korean web accessibility standard) built in: refuses markup when labels or alt text are missing, checks rendered pages with axe plus real keyboard and contrast measurements, and ships Claude Code/Codex hooks that keep agents from finishing while violations remain
  <sub>★ 1 · TypeScript · MIT · npx · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y krds-a11y-mcp init`</sub>
- **[pourdev/pour-cli](https://github.com/pourdev/pour-cli)** — WCAG 2.2 audits from the pour accessibility engine, written from the W3C specifications: audit a URL or local HTML file for proven failures and items that need a person to review, trace the keyboard focus order, and screenshot a page through vision and motor simulations
  <sub>★ 1 · JavaScript · MIT · npm · pushed 2026-11-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g pour-cli`</sub>
- **[vince-gonzalez/opticquiz-mcp](https://github.com/vince-gonzalez/opticquiz-mcp)** — Color-vision accessibility: check palettes and images for colorblind safety, generate safe palettes, simulate color blindness and create Ishihara-style plates
  <sub>JavaScript · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vince-gonzalez/opticquiz-mcp.git`</sub>

## Aerospace &amp; Astrodynamics

- **[gregario/astronomy-oracle](https://github.com/gregario/astronomy-oracle)** — Astronomical catalog data and observing session planning: OpenNGC deep-sky objects with visibility, rise/transit/set and alt/az calculations
  <sub>★ 3 · TypeScript · MIT · npm · pushed 2026-11-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g astronomy-oracle`</sub>
- **[viventine-space/orbit-sentinel-mcp](https://github.com/Viventine-Space/orbit-sentinel-mcp)** — Search FCC, ITU, UNOOSA and FAA space regulatory filings via Orbit Sentinel: semantic search, entity dossiers, spectrum holdings, launch licenses and alerts
  <sub>★ 1 · Go · MIT · npx · pushed 2026-11-26 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx mcp-remote https://orbit-sentinel.viventine.com/mcp`</sub>
- **[sr-dash/heliofleet-mcp](https://github.com/sr-dash/heliofleet-mcp)** — Heliophysics spacecraft positions and trajectories, alignments (radial, quadrature, conjunction), viewing geometry, solar observation records (IRIS, DKIST, Solar Orbiter) and PFSS solar magnetic connectivity from JPL Horizons ephemerides; every answer links to the same view on HelioFleet. uvx heliofleet-mcp
  <sub>Python · MIT · npx · pushed 2026-11-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sr-dash/heliofleet-mcp`</sub>

## Jobs

- **[GhoshSrinjoy/linkedin-job-mcp](https://github.com/GhoshSrinjoy/linkedin-job-mcp)** — Job search by keyword and location with date, job type, remote, salary and experience filters, full job details, and a local dashboard that grades postings for ghost-job risk. Reads public job pages, so no account or browser is needed
  <sub>★ 1 · Python · npm · pushed 2026-11-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g linkedin-jobs-mcp`</sub>
- **[MIt9/workatastartup-mcp](https://github.com/MIt9/workatastartup-mcp)** — MCP server for WorkAtAStartup — search startup job listings via Claude or Cursor
  <sub>Python · uv · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx workatastartup-mcp`</sub>
- **[VerbatimCV/verbatimcv-mcp](https://github.com/VerbatimCV/verbatimcv-mcp)** — Official VerbatimCV server: parse CVs and resumes (PDF or DOCX, local file or URL) into versioned JSON where every candidate preference carries the verbatim quote it came from, nothing is invented, and hidden prompt injection is removed and reported. Free API key, no card
  <sub>Python · MIT · uv · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx verbatimcv-mcp`</sub>

Page **7** of 7, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](mcp-servers-punkpeye.md) · [2](mcp-servers-punkpeye-2.md) · [3](mcp-servers-punkpeye-3.md) · [4](mcp-servers-punkpeye-4.md) · [5](mcp-servers-punkpeye-5.md) · [6](mcp-servers-punkpeye-6.md) · **7**.

---

Snapshot 2026-11-27. Stars, language, licence and last-push come from the GitHub API and drift daily.

Filter the same data in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/). Spreadsheet edition: retired. The last copy, built 2026-10-22, stays available but is no longer updated. The website is the maintained edition. Its last workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-LIGHT.xlsx).
