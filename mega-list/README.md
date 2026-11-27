# Awesome Agentic Atlas

**39 curated awesome-lists merged into one.** 19,626 entries, 12,212 distinct GitHub repos, 34,345,639 stars — each entry resolved to its repo and given a screenshot, an install line, and platform evidence for Windows, WSL2, macOS, Linux and Docker.

Every list below was made by someone else. This is not a new selection: it is their selections in one place, with the facts filled in and the overlap made visible.

Also here as a page you can filter in the browser, no download: **[the Atlas site](https://aaa.jeremyfhall.com/catalog/)**. Spreadsheet edition: retired. The last copy, built 2026-10-22, stays available but is no longer updated. The website is the maintained edition. Its last workbooks: [dark theme](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-DARK.xlsx) · [light theme](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-LIGHT.xlsx).

## Pick your platform

| Platform | Confirmed | Inferred | Total | Page |
|---|--:|--:|--:|---|
| **Windows** | 3,312 | 7,584 | 10,896 | [Windows](platforms/windows.md) · [inferred](platforms/windows-inferred.md) |
| **macOS** | 2,469 | 8,065 | 10,534 | [macOS](platforms/macos.md) · [inferred](platforms/macos-inferred.md) |
| **Linux** | 3,043 | 7,859 | 10,902 | [Linux](platforms/linux.md) · [inferred](platforms/linux-inferred.md) |
| **Docker** | 2,227 | 0 | 2,227 | [Docker](platforms/docker.md) |

**Confirmed** means a release asset for that platform, or the README saying so outright. **Inferred** means the install route or the language runtime implies it and nothing states it — a good bet, not a promise, and each row carries the reasoning that put it there.

Those four are drawn from the 11,984 distinct repos that entries across the 39 lists resolve to. A hosted product with no public repo and a folder inside a larger repo have no platform support of their own to report, so neither appears on a platform page — both are on their list's page instead.

## Pick your topic

39 curators used 619 different section names and agreed on almost none of them — `Frameworks`, `Agent Frameworks` and `Build-your-own` are one shelf under three names. These 14 are one vocabulary over all of it, so that "the best X" becomes a question with an answer.

| Topic | Projects | Ranked | ★ combined | Most-starred |
|---|--:|--:|--:|---|
| [**Orchestrators &amp; Multi-Agent**](topics/orchestrators-multi-agent.md) | 535 | 526 | 2,714,580 | [n8n](https://github.com/n8n-io/n8n) ★ 212.4k |
| [**Coding Agents**](topics/coding-agents.md) | 562 | 557 | 3,043,723 | [OpenCode](https://github.com/anomalyco/opencode) ★ 229.5k |
| [**Agent Skills**](topics/agent-skills.md) | 1,635 | 1,477 | 8,064,230 | [morluto/rea](https://github.com/morluto/rea) ★ 480.5k |
| [**MCP Servers**](topics/mcp-servers.md) | 5,686 | 4,707 | 2,615,343 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ★ 92.3k |
| [**Frameworks &amp; SDKs**](topics/frameworks-sdks.md) | 544 | 512 | 3,377,495 | [openclaw](https://github.com/openclaw/openclaw) ★ 395.3k |
| [**Harnesses &amp; Runtime Infra**](topics/harnesses-runtime-infra.md) | 682 | 621 | 4,797,721 | [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) ★ 287.9k |
| [**Context, Memory &amp; RAG**](topics/context-memory-rag.md) | 179 | 172 | 1,290,803 | [RAGFlow](https://github.com/infiniflow/ragflow) ★ 94.8k |
| [**Sandbox, Security &amp; Governance**](topics/sandbox-security-governance.md) | 218 | 189 | 517,413 | [Strix](https://github.com/usestrix/strix) ★ 77.9k |
| [**Observability &amp; Evals**](topics/observability-evals.md) | 486 | 400 | 888,500 | [FreeLLMAPI](https://github.com/tashfeenahmed/freellmapi) ★ 59k |
| [**Plugins, Themes &amp; Clients**](topics/plugins-themes-clients.md) | 747 | 730 | 2,262,180 | [cc-switch](https://github.com/farion1231/cc-switch) ★ 157.6k |
| [**Research &amp; Data Agents**](topics/research-data-agents.md) | 42 | 41 | 217,244 | [Pathway](https://github.com/pathwaycom/pathway) ★ 62k |
| [**Creative, Voice &amp; Media**](topics/creative-voice-media.md) | 33 | 32 | 506,075 | [whisper](https://github.com/openai/whisper) ★ 113.6k |
| [**Assistants &amp; Domain Agents**](topics/assistants-domain-agents.md) | 716 | 704 | 2,884,667 | [hermes-agent](https://github.com/NousResearch/hermes-agent) ★ 266.5k |
| [**Docs, Learning &amp; Lists**](topics/docs-learning-lists.md) | 147 | 139 | 1,165,665 | [f/awesome-chatgpt-prompts](https://github.com/f/prompts.chat) ★ 178.7k |

[**All topics, with what is on each page →**](topics/README.md)

## Pick your harness

The second axis: what a project plugs into, rather than what it is. Cross the two and you get the question none of the 39 lists could answer on its own — the best Claude Code observability tool, the best opencode plugin, the best local-runtime orchestrator.

| Runs with | Projects | Ranked | ★ combined | Most-starred |
|---|--:|--:|--:|---|
| [**Claude Code**](targets/claude-code.md) | 3,798 | 3,575 | 13,443,874 | [morluto/rea](https://github.com/morluto/rea) ★ 480.5k |
| [**Claude / Anthropic**](targets/claude-anthropic.md) | 5,847 | 5,278 | 16,388,516 | [morluto/rea](https://github.com/morluto/rea) ★ 480.5k |
| [**opencode**](targets/opencode.md) | 550 | 541 | 3,669,108 | [mattpocock/skills](https://github.com/mattpocock/skills) ★ 334k |
| [**MCP**](targets/mcp.md) | 6,691 | 5,623 | 9,351,034 | [morluto/rea](https://github.com/morluto/rea) ★ 480.5k |
| [**Codex / OpenAI**](targets/codex-openai.md) | 2,816 | 2,661 | 11,847,731 | [Superpowers](https://github.com/obra/superpowers) ★ 327.9k |
| [**Gemini / Google**](targets/gemini-google.md) | 1,043 | 980 | 4,606,846 | [Superpowers](https://github.com/obra/superpowers) ★ 327.9k |
| [**GitHub Copilot**](targets/github-copilot.md) | 359 | 340 | 2,110,554 | [Superpowers](https://github.com/obra/superpowers) ★ 327.9k |
| [**Cursor**](targets/cursor.md) | 1,626 | 1,421 | 5,085,538 | [mattpocock/skills](https://github.com/mattpocock/skills) ★ 334k |
| [**Cline / Roo**](targets/cline-roo.md) | 122 | 113 | 301,154 | [OmniRoute: Multi-Provider LLM Gateway](https://github.com/cheaper-inference/OmniRoute) ★ 90.7k |
| [**Aider**](targets/aider.md) | 45 | 43 | 76,232 | [Aider](https://github.com/Aider-AI/aider) ★ 50.3k |
| [**LangChain / LangGraph**](targets/langchain-langgraph.md) | 232 | 217 | 1,387,319 | [Langflow](https://github.com/langflow-ai/langflow) ★ 157k |
| [**Local / Ollama**](targets/local-ollama.md) | 220 | 207 | 1,231,410 | [Ollama](https://github.com/ollama/ollama) ★ 188.3k |

A project can be on several of these pages, because plenty serve Claude Code and opencode and Codex at once. A project on none of them only means no harness is named anywhere in its description.

**Crossing the two** takes a filter, not a page, so those links go to the site: [Claude Code observability](https://aaa.jeremyfhall.com/catalog/#topic=observability-evals&target=claude-code) · [opencode plugins](https://aaa.jeremyfhall.com/catalog/#topic=plugins-themes-clients&target=opencode) · [skills for Claude Code, Windows-native](https://aaa.jeremyfhall.com/catalog/#topic=agent-skills&target=claude-code&os=windows&confirmed=1) · [memory and retrieval over MCP](https://aaa.jeremyfhall.com/catalog/#topic=context-memory-rag&target=mcp).

[**All harnesses →**](targets/README.md)

## Every list, credited

★ is the source list's own star count. A dash means its repo was not among the ones this snapshot fetched, so the number is unknown rather than zero.

| Awesome list | ★ | Entries | Repos | What it covers | Page |
|---|--:|--:|--:|---|---|
| [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) | — | 380 | 380 | The original list this atlas grew from: tools that run several coding agents at once. | [Orchestrators](lists/orchestrators.md) |
| [kyrolabs/awesome-agents](https://github.com/kyrolabs/awesome-agents) | 3,019 | 243 | 242 | Frameworks, dev tools and agent products, as curated by kyrolabs. | [Agents (kyrolabs)](lists/agents-kyrolabs.md) |
| [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | 31,089 | 214 | 104 | e2b's catalogue of AI agents and the frameworks behind them. | [Agents (e2b)](lists/agents-e2b.md) |
| [caramaschiHG/awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026) | 2,095 | 260 | 116 | A 2026 market survey — commercial products alongside open source. | [AI Agents 2026](lists/ai-agents-2026.md) |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 58,903 | 252 | 239 | Commands, hooks, status lines and tooling for Claude Code. | [Claude Code](lists/claude-code.md) |
| [awesome-opencode/awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | 11,124 | 198 | 198 | Plugins, themes, agents and projects for the opencode terminal agent. | [Opencode](lists/opencode.md) |
| [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | 5,251 | 531 | 291 | How agent harnesses are built — primitives, papers and reference implementations. | [Harness Engineering](lists/harness-engineering.md) |
| [nibzard/awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns) | 5,093 | 197 | 1 | Named design patterns for agentic systems. Each row is a write-up, not a tool. | [Agentic Patterns](lists/agentic-patterns.md) |
| [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | 6,438 | 422 | 277 | Skill directories by vendor, plus community-published skills. | [Agent Skills](lists/agent-skills.md) |
| [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | 50,430 | 461 | 457 | The upstream repos the Agentic Awesome Skills library aggregates. | [AAS Skill Sources](lists/aas-skill-sources.md) |
| [shubhamsaboo/awesome-llm-apps](https://github.com/shubhamsaboo/awesome-llm-apps) | 145,897 | 124 | 3 | Runnable example apps. Each row is a folder inside the one repo. | [LLM App Templates](lists/llm-app-templates.md) |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 98,565 | 5,011 | 4,999 | A collection of MCP servers. | [MCP Servers (punkpeye)](lists/mcp-servers-punkpeye.md) |
| [crazy54/awesome-agentic-atlas](https://github.com/crazy54/awesome-agentic-atlas) | 10 | 2,484 | 2,484 | Awesome Agentic Atlas is your guide to all the top Awesome repos for AI. | [Scouted on GitHub](lists/scouted-on-github.md) |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | 41,620 | 1,019 | 1 | Community-contributed instructions, agents, skills, and configurations to help you make the most of GitHub Copilot. | [GitHub Copilot Customizations](lists/github-copilot-customizations.md) |
| [jim-schwoebel/awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) | 2,033 | 953 | 827 | 🤖 A comprehensive list of 1,500+ resources and tools related to AI agents. | [AI Agents (Schwoebel)](lists/ai-agents-schwoebel.md) |
| [jqueryscript/awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code) | 558 | 819 | 793 | A curated list of awesome tools, IDE integrations, frameworks, and other resources for developers working with Anthropic's Claude Code. | [Claude Code (jqueryscript)](lists/claude-code-jqueryscript.md) |
| [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | 2,872 | 673 | 302 | The most comprehensive toolkit for Claude Code -- 135 agents, 35 curated skills, 42 commands, 176+ plugins, 20 hooks, 15 rules, 7 templates, 14 MCP c… | [Claude Code Toolkit](lists/claude-code-toolkit.md) |
| [tensorchord/Awesome-LLMOps](https://github.com/tensorchord/Awesome-LLMOps) | 5,984 | 516 | 451 | An awesome &amp; curated list of best LLMOps tools for developers | [LLMOps (tensorchord)](lists/llmops-tensorchord.md) |
| [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) | 4,422 | 516 | 468 | A curated list of Model Context Protocol (MCP) servers | [MCP Servers (wong2)](lists/mcp-servers-wong2.md) |
| [ai-for-developers/awesome-ai-coding-tools](https://github.com/ai-for-developers/awesome-ai-coding-tools) | 2,309 | 502 | 214 | A curated list of AI-powered coding tools | [AI Coding Tools (a4d)](lists/ai-coding-tools-a4d.md) |
| [Jenqyang/Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents) | 1,278 | 437 | 414 | A collection of autonomous agents 🤖️ powered by LLM. | [AI Agents (Jenqyang)](lists/ai-agents-jenqyang.md) |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 37,583 | 410 | 345 | A curated collection of 1000+ agent skills from official dev teams and the community, compatible with Claude Code, Codex, Gemini CLI, Cursor, and mor… | [Agent Skills (VoltAgent)](lists/agent-skills-voltagent.md) |
| [Piebald-AI/awesome-gemini-cli](https://github.com/Piebald-AI/awesome-gemini-cli) | 676 | 327 | 259 | A curated list of awesome tools, extensions, and resources for Gemini CLI. | [Gemini CLI Ecosystem](lists/gemini-cli-ecosystem.md) |
| [ccplugins/awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) | 1,019 | 290 | 93 | Awesome Claude Code plugins — a curated list of slash commands, subagents, MCP servers, and hooks for Claude Code | [Claude Code Plugins](lists/claude-code-plugins.md) |
| [RoggeOhta/awesome-codex-cli](https://github.com/RoggeOhta/awesome-codex-cli) | 589 | 269 | 211 | Curated list of 150+ tools, skills, subagents &amp; plugins for OpenAI Codex CLI | [Codex CLI Ecosystem](lists/codex-cli-ecosystem.md) |
| [jamesmurdza/awesome-ai-devtools](https://github.com/jamesmurdza/awesome-ai-devtools) | 4,002 | 264 | 73 | Curated list of AI-powered developer tools. | [AI Dev Tools (murdza)](lists/ai-dev-tools-murdza.md) |
| [InftyAI/Awesome-LLMOps](https://github.com/InftyAI/Awesome-LLMOps) | 273 | 262 | 260 | 🎉 An awesome &amp; curated list of best LLMOps tools. | [LLMOps (InftyAI)](lists/llmops-inftyai.md) |
| [promptslab/Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering) | 6,460 | 219 | 178 | This repository contains a hand-curated resources for Prompt Engineering with a focus on Generative Pre-trained Transformer (GPT), ChatGPT, PaLM etc | [Prompt Engineering (promptslab)](lists/prompt-engineering-promptslab.md) |
| [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) | 41,202 | 216 | 1 | 📄 Configuration files that enhance Cursor AI editor experience with custom rules and behaviors | [Cursor Rules](lists/cursor-rules.md) |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 1,031 | 203 | 193 | A curated list of awesome MCP servers focused on DevOps tools and capabilities. | [DevOps MCP Servers](lists/devops-mcp-servers.md) |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 26,801 | 170 | 5 | A collection of 100+ specialized Claude Code subagents covering a wide range of development use cases | [Claude Code Subagents](lists/claude-code-subagents.md) |
| [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills) | 901 | 153 | 21 | A curated list of awesome skills for Cursor | [Cursor Skills](lists/cursor-skills.md) |
| [LLMSecurity/awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) | 296 | 134 | 88 | 🛡️ A curated list of resources on agent skills security: attacks, defenses, frameworks, and benchmarks for securing AI agent tool use and skill ecosy… | [Agent Skill Security](lists/agent-skill-security.md) |
| [Merit-Systems/awesome-agentic-commerce](https://github.com/Merit-Systems/awesome-agentic-commerce) | 155 | 112 | 38 | Curated resources for the agentic commerce ecosystem | [Agentic Commerce (x402)](lists/agentic-commerce-x402.md) |
| [kaushikb11/awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents) | 1,629 | 108 | 108 | A curated list of awesome LLM agents frameworks. | [LLM Agents (kaushikb11)](lists/llm-agents-kaushikb11.md) |
| [filipecalegario/awesome-vibe-coding](https://github.com/filipecalegario/awesome-vibe-coding) | 5,459 | 99 | 47 | A curated list of vibe coding references, collaborating with AI to write code. | [Vibe Coding](lists/vibe-coding.md) |
| [JackyST0/awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills) | 671 | 84 | 55 | 🤖 精选的 AI Agent Skills 列表，适用于 Cursor、Claude Code、GitHub Copilot 等 AI 编程工具 | [Agent Skills (JackyST0)](lists/agent-skills-jackyst0.md) |
| [machinae/awesome-claws](https://github.com/machinae/awesome-claws) | 515 | 35 | 35 | A curated list of awesome AI agents inspired by OpenClaw | [OpenClaw Assistants](lists/openclaw-assistants.md) |
| [libukai/awesome-agent-skills](https://github.com/libukai/awesome-agent-skills) | 5,235 | 35 | 26 | Agent Skills 终极指南：快速入门、资源推荐、精选技能与实用工具 ｜The Ultimate Guide to Agent Skills: QuickStart, Resources, Features&amp;Toolkit | [Agent Skills (libukai)](lists/agent-skills-libukai.md) |
| [ProjectRecon/awesome-ai-agents-security](https://github.com/ProjectRecon/awesome-ai-agents-security) | 81 | 24 | 22 | A living map of the AI agent security ecosystem. | [AI Agent Security Tooling](lists/ai-agent-security-tooling.md) |

Lists overlap heavily — 1398 projects are named by two or more of them. [**Leaderboard**](leaderboard.md) is the deduplicated view, ranked by stars, with the count of how many lists agree.

## Most-starred, across every list

|   |   |   |
|---|---|---|
| <a href="https://github.com/morluto/rea"><img src="https://raw.githubusercontent.com/morluto/rea/main/docs/assets/rea-showcases.png" width="260"></a> | <a href="https://github.com/openclaw/openclaw"><img src="https://opengraph.githubassets.com/1/openclaw/openclaw" width="260"></a> | <a href="https://github.com/mattpocock/skills"><img src="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png" width="260"></a> |
| **[morluto/rea](https://github.com/morluto/rea)**<br>★ 480.5k | **[openclaw](https://github.com/openclaw/openclaw)**<br>★ 395.3k | **[mattpocock/skills](https://github.com/mattpocock/skills)**<br>★ 334k |
| <a href="https://github.com/obra/superpowers"><img src="https://opengraph.githubassets.com/1/obra/superpowers" width="260"></a> | <a href="https://github.com/affaan-m/ECC"><img src="https://raw.githubusercontent.com/affaan-m/ECC/main/assets/hero.png" width="260"></a> | <a href="https://github.com/deepseek-ai/deepseek-harness"><img src="https://opengraph.githubassets.com/1/deepseek-ai/deepseek-harness" width="260"></a> |
| **[Superpowers](https://github.com/obra/superpowers)**<br>★ 327.9k | **[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)**<br>★ 311.5k | **[DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness)**<br>★ 287.9k |

## How to read this

- **Stars, language, licence and last-push** come from the GitHub API at snapshot time. They drift daily; treat them as an order of magnitude, not a live count.
- **Platform columns are derived evidence, not a vendor support matrix.** The strongest signal is a published release asset — a `.msi` or `windows-amd64.zip` proves native Windows, a lone `.dmg` disproves it. Then explicit README prose, then the install route, then the language runtime alone, which only ever earns a `?`.
- **A `?` means inferred.** Every platform page carries the reasoning per row in its `Why` column, so a verdict you doubt can be checked rather than taken.
- **1,688 entries are hosted products with no public repo** and 2,964 are items inside a larger repo (a template folder, a pattern write-up). Neither has stars or platform support of its own, so those show `—` rather than borrowing the parent's.
- **26 listed repos now return an error from GitHub** — deleted, renamed, or made private. They are kept, marked, so nothing silently vanishes from a count.
- **Screenshots are the first usable image in the README**, falling back to the project's own social card and then to GitHub's. A GitHub card means no project image could be found, not that the project has no UI.
- **Sections keep the wording each list published.** Nothing was renamed to make the lists agree, because a section name is part of the curation.

## Contents

- [Leaderboard](leaderboard.md) — top projects across every list, deduplicated
- [Browse by topic](topics/README.md) — 14 topics, one page each
- [Browse by harness](targets/README.md) — 12 harnesses, one page each
- [The Atlas site](https://aaa.jeremyfhall.com/catalog/) — all 12,212 in one page, both axes filterable
- [Windows](platforms/windows.md) — 10,896 repos
- [macOS](platforms/macos.md) — 10,534 repos
- [Linux](platforms/linux.md) — 10,902 repos
- [Docker](platforms/docker.md) — 2,227 repos
- [Orchestrators](lists/orchestrators.md) — 380 entries from `andyrewlee/awesome-agent-orchestrators`
- [Agents (kyrolabs)](lists/agents-kyrolabs.md) — 243 entries from `kyrolabs/awesome-agents`
- [Agents (e2b)](lists/agents-e2b.md) — 214 entries from `e2b-dev/awesome-ai-agents`
- [AI Agents 2026](lists/ai-agents-2026.md) — 260 entries from `caramaschiHG/awesome-ai-agents-2026`
- [Claude Code](lists/claude-code.md) — 252 entries from `hesreallyhim/awesome-claude-code`
- [Opencode](lists/opencode.md) — 198 entries from `awesome-opencode/awesome-opencode`
- [Harness Engineering](lists/harness-engineering.md) — 531 entries from `ai-boost/awesome-harness-engineering`
- [Agentic Patterns](lists/agentic-patterns.md) — 197 entries from `nibzard/awesome-agentic-patterns`
- [Agent Skills](lists/agent-skills.md) — 422 entries from `heilcheng/awesome-agent-skills`
- [AAS Skill Sources](lists/aas-skill-sources.md) — 461 entries from `sickn33/agentic-awesome-skills`
- [LLM App Templates](lists/llm-app-templates.md) — 124 entries from `shubhamsaboo/awesome-llm-apps`
- [MCP Servers (punkpeye)](lists/mcp-servers-punkpeye.md) — 5,011 entries from `punkpeye/awesome-mcp-servers`
- [Scouted on GitHub](lists/scouted-on-github.md) — 2,484 entries from `crazy54/awesome-agentic-atlas`
- [GitHub Copilot Customizations](lists/github-copilot-customizations.md) — 1,019 entries from `github/awesome-copilot`
- [AI Agents (Schwoebel)](lists/ai-agents-schwoebel.md) — 953 entries from `jim-schwoebel/awesome_ai_agents`
- [Claude Code (jqueryscript)](lists/claude-code-jqueryscript.md) — 819 entries from `jqueryscript/awesome-claude-code`
- [Claude Code Toolkit](lists/claude-code-toolkit.md) — 673 entries from `rohitg00/awesome-claude-code-toolkit`
- [LLMOps (tensorchord)](lists/llmops-tensorchord.md) — 516 entries from `tensorchord/Awesome-LLMOps`
- [MCP Servers (wong2)](lists/mcp-servers-wong2.md) — 516 entries from `wong2/awesome-mcp-servers`
- [AI Coding Tools (a4d)](lists/ai-coding-tools-a4d.md) — 502 entries from `ai-for-developers/awesome-ai-coding-tools`
- [AI Agents (Jenqyang)](lists/ai-agents-jenqyang.md) — 437 entries from `Jenqyang/Awesome-AI-Agents`
- [Agent Skills (VoltAgent)](lists/agent-skills-voltagent.md) — 410 entries from `VoltAgent/awesome-agent-skills`
- [Gemini CLI Ecosystem](lists/gemini-cli-ecosystem.md) — 327 entries from `Piebald-AI/awesome-gemini-cli`
- [Claude Code Plugins](lists/claude-code-plugins.md) — 290 entries from `ccplugins/awesome-claude-code-plugins`
- [Codex CLI Ecosystem](lists/codex-cli-ecosystem.md) — 269 entries from `RoggeOhta/awesome-codex-cli`
- [AI Dev Tools (murdza)](lists/ai-dev-tools-murdza.md) — 264 entries from `jamesmurdza/awesome-ai-devtools`
- [LLMOps (InftyAI)](lists/llmops-inftyai.md) — 262 entries from `InftyAI/Awesome-LLMOps`
- [Prompt Engineering (promptslab)](lists/prompt-engineering-promptslab.md) — 219 entries from `promptslab/Awesome-Prompt-Engineering`
- [Cursor Rules](lists/cursor-rules.md) — 216 entries from `PatrickJS/awesome-cursorrules`
- [DevOps MCP Servers](lists/devops-mcp-servers.md) — 203 entries from `rohitg00/awesome-devops-mcp-servers`
- [Claude Code Subagents](lists/claude-code-subagents.md) — 170 entries from `VoltAgent/awesome-claude-code-subagents`
- [Cursor Skills](lists/cursor-skills.md) — 153 entries from `spencerpauly/awesome-cursor-skills`
- [Agent Skill Security](lists/agent-skill-security.md) — 134 entries from `LLMSecurity/awesome-agent-skills-security`
- [Agentic Commerce (x402)](lists/agentic-commerce-x402.md) — 112 entries from `Merit-Systems/awesome-agentic-commerce`
- [LLM Agents (kaushikb11)](lists/llm-agents-kaushikb11.md) — 108 entries from `kaushikb11/awesome-llm-agents`
- [Vibe Coding](lists/vibe-coding.md) — 99 entries from `filipecalegario/awesome-vibe-coding`
- [Agent Skills (JackyST0)](lists/agent-skills-jackyst0.md) — 84 entries from `JackyST0/awesome-agent-skills`
- [OpenClaw Assistants](lists/openclaw-assistants.md) — 35 entries from `machinae/awesome-claws`
- [Agent Skills (libukai)](lists/agent-skills-libukai.md) — 35 entries from `libukai/awesome-agent-skills`
- [AI Agent Security Tooling](lists/ai-agent-security-tooling.md) — 24 entries from `ProjectRecon/awesome-ai-agents-security`

---

Snapshot 2026-11-27. Stars, language, licence and last-push come from the GitHub API and drift daily.

Filter the same data in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/). Spreadsheet edition: retired. The last copy, built 2026-10-22, stays available but is no longer updated. The website is the maintained edition. Its last workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-LIGHT.xlsx).
