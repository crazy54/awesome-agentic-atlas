# macOS

Every project across all 39 lists that runs on macOS — Apple silicon or Intel — **8,926** of 10,204 distinct repos, deduplicated to one row per repo.

Confirmed first, then inferred, each block by stars. Confirmation means a .dmg/.pkg asset or explicit README prose; inference from a portable runtime alone only ever earns Likely.

[← back to the mega list](../README.md) · [6,929 inferred →](macos-inferred.md)

Page **4** of 4, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](macos.md) · [2](macos-2.md) · [3](macos-3.md) · **4**.

## Confirmed (1,997)

A release asset for this platform, or the README saying so outright.

<sub>Projects 1,993–1,997 of 1,997. The rest are on this page's other parts, linked above and below.</sub>

| # | Project | ★ | Lists | Support | Language | Install / Run | What it does | Why |
|--:|---|--:|--:|---|---|---|---|---|
| 1993 | **[ValetFS](https://github.com/WinM2M/valet-fs)**<br><sub>WinM2M/valet-fs</sub> | — | 1 | Win? · WSL2 · macOS · Linux | Go | `curl -fsSL https://winm2m.github.io/valet-fs/install.sh \| bash` | Secrets stay on a paired device and are lent to the agent's machine into daemon memory only, served over FUSE or loopback WebDAV; the daemon zero-wipes them when the pairing drops or a grace window expires | <sub>ships Linux build (valetfs-linux-arm64); install via script; README mentions Windows</sub> |
| 1994 | **[veezeehq/veezee-mcp](https://github.com/veezeehq/veezee-mcp)**<br><sub>veezeehq/veezee-mcp</sub> | — | 1 | Win · WSL2? · macOS · Linux · Docker | JavaScript | `npx github:veezeehq/veezee-mcp` | Real-time LinkedIn, X (Twitter) and Reddit data: profiles, companies, posts, search and sentiment | <sub>README states cross-platform; install via npx; portable runtime (node); Docker supported</sub> |
| 1995 | **[witness](https://github.com/halleylabs/witness)**<br><sub>halleylabs/witness</sub> | — | 1 | WSL2 · macOS · Linux · Docker | Rust | `git clone https://github.com/anzal1/witness.git` | A recording cache for model APIs: one Rust binary that proxies any LLM endpoint, dedupes repeat calls, and writes every model call, MCP tool call, and command side effect into a tamper-evident hash-chained journal with… | <sub>ships macOS build (witness-v0.2.0-macos-x86_64.tar.gz); ships Linux build (witness-v0.2.0-linux-arm64.tar.gz); Docker supported</sub> |
| 1996 | **[zarcherlot/code-relay](https://github.com/zarcherlot/code-relay)**<br><sub>zarcherlot/code-relay</sub> | — | 1 | Win · WSL2? · macOS · Linux | Go | `npx -y code-relay-mcp@latest install --client codex` | Branch-scoped runbooks and cross-machine verification with auditable receipts for coding agents | <sub>ships Windows build (code-relay-agent-windows-amd64.exe); ships macOS build (code-relay-agent-darwin-amd64); ships Linux build (code-relay-agent-linux-arm64)…</sub> |
| 1997 | **[Zsadigzade/trainbud](https://github.com/Zsadigzade/trainbud)**<br><sub>Zsadigzade/trainbud</sub> | — | 1 | Win · WSL2? · macOS · Linux · Docker | TypeScript | `npm install -g trainbud` | Local analysis of Garmin Connect activities, sleep, recovery, body composition, stress and VO2 max against 28-day baselines, with memory for goals and races | <sub>README states cross-platform; install via npm; portable runtime (node); Docker supported</sub> |

## Inferred (6,929)

No direct statement, but the install route or the language runtime implies it. On its own page so this one stays scannable: **[all 6,929 inferred macOS projects →](macos-inferred.md)**

Page **4** of 4, because this list is longer than the 512 KB GitHub will render in one file. In order: [1](macos.md) · [2](macos-2.md) · [3](macos-3.md) · **4**.

---

Snapshot 2026-10-15. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
