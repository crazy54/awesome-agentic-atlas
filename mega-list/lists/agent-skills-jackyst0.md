# Agent Skills (JackyST0)

🤖 精选的 AI Agent Skills 列表，适用于 Cursor、Claude Code、GitHub Copilot 等 AI 编程工具

Curated by **[JackyST0/awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

84 entries · 55 distinct repos · 8 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/obra/superpowers"><img src="https://opengraph.githubassets.com/1/obra/superpowers" width="260"></a> | <a href="https://github.com/anthropics/skills"><img src="https://opengraph.githubassets.com/1/anthropics/skills" width="260"></a> | <a href="https://github.com/browser-use/browser-use"><img src="https://github.com/user-attachments/assets/135885e8-1141-4e10-b719-bf690ae7d260" width="260"></a> |
| **[obra/superpowers](https://github.com/obra/superpowers)**<br>★ 328.6k | **[anthropics/skills](https://github.com/anthropics/skills)**<br>★ 201.7k | **[browser-use/browser-use](https://github.com/browser-use/browser-use)**<br>★ 122.3k |
| <a href="https://github.com/addyosmani/agent-skills"><img src="https://addyosmani.com/assets/images/addys-agent-skills.jpg" width="260"></a> | <a href="https://github.com/career-ops-hq/career-ops"><img src="https://raw.githubusercontent.com/career-ops-hq/career-ops/main/docs/demo.gif" width="260"></a> | <a href="https://github.com/ComposioHQ/awesome-claude-skills"><img src="https://github.com/user-attachments/assets/e91255af-e4ba-4d71-b1a8-bd081e8a234a" width="260"></a> |
| **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)**<br>★ 120.9k | **[career-ops](https://github.com/career-ops-hq/career-ops)**<br>★ 85.3k | **[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)**<br>★ 80.5k |

## Contents

- [Productivity](#productivity) (11)
- [Official Resources](#official-resources) (19)
- [Development Tools](#development-tools) (21)
- [Skills Collections](#skills-collections) (16)
- [Data Processing](#data-processing) (4)
- [DevOps](#devops) (1)
- [Writing](#writing) (6)
- [Design](#design) (6)

## Productivity

- **[obra/superpowers](https://github.com/obra/superpowers)** — 324.3k ⭐ - Complete dev workflow (Debug/TDD/Code Review/Planning)
  <sub>★ 328.6k · Shell · MIT · clone · pushed 2026-11-28</sub>
  <sub>`git clone https://github.com/obra/superpowers.git`</sub>
- **[career-ops](https://github.com/career-ops-hq/career-ops)** — 84.3k ⭐ - Open-source AI job search agent for Claude Code, Codex and OpenCode: scans company career pages, scores each job posting 1-5 against your CV, tailors an ATS-friendly resume and tracks applications; you submit every application yourself. No telemetry; your CV goes only to the AI provider you choose. Website
  <sub>★ 85.3k · JavaScript · MIT · npm · pushed 2026-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @santifer/career-ops`</sub>
- **[last30days](https://github.com/mvanhorn/last30days-skill)** — 72.7k ⭐ - Researches any topic across Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the web from the last 30 days, ranks results by real engagement (upvotes, likes, prediction-market odds), and writes one cited brief. Reddit, Hacker News, Polymarket and GitHub need no setup
  <sub>★ 76.5k · Python · MIT · npx · pushed 2026-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add mvanhorn/last30days-skill -g`</sub>
- **[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)** — 62.1k ⭐ - Marketing Skills (SEO/Copywriting/CRO/Ads)
  <sub>★ 63.1k · JavaScript · MIT · npx · pushed 2026-11-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add coreyhaines31/marketingskills`</sub>
- **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** — 30.3k ⭐ - 20+ productivity tools with 8 expert Agents
  <sub>★ 30.6k · Python · MIT · npx · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add alirezarezvani/claude-skills`</sub>
- **[planning-with-files](https://github.com/OthmanAdi/planning-with-files)** — 28.2k ⭐ - Persistent file-based planning with task plans, findings, progress tracking, and session recovery for long-running agent work
  <sub>★ 28.3k · Shell · MIT · npx · pushed 2026-11-25 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g`</sub>
- **[answer-me-with-html](https://github.com/QingYunA/answer-me-with-html)** — 6.6k ⭐ - Agent skill that writes the answer as a Markdown draft and renders one offline HTML page, using about 1/8 of the output tokens
  <sub>★ 6.7k · JavaScript · MIT · npx · pushed 2026-11-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add QingYunA/answer-me-with-html`</sub>
- **[new-term-radar](https://github.com/zhuyansen/new-term-radar)** — 2.2k ⭐ - Spots new AI model, product and repo names on X, Hugging Face, GitHub and sitemaps, then ranks the search terms behind them by Google Ads volume and DataForSEO Trends (an estimate of Google search interest). Three skills and an MCP server; needs an AIsa API key, and an optional GoAnyAPI key adds Google Trends related queries and country-level trend series
  <sub>★ 2.2k · Python · MIT · npx · pushed 2026-11-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add zhuyansen/new-term-radar`</sub>
- **[claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)** — 909 ⭐ - Skills factory for batch generation and deployment
  <sub>★ 916 · Python · MIT · source · pushed 2025-11-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/alirezarezvani/claude-code-skill-factory.git`</sub>
- **[claude-code-workflows](https://github.com/shinpr/claude-code-workflows)** — 720 ⭐ - Production-grade dev workflows with quality checks
  <sub>★ 722 · JavaScript · MIT · source · pushed 2026-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shinpr/claude-code-workflows.git`</sub>
- **[changelog-generator](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/changelog-generator)** — 80.1k ⭐ - Generate changelogs from Git commits
  <sub>Python · in-repo · pushed 2026-09-18</sub>
  <sub>`git clone https://github.com/ComposioHQ/awesome-claude-skills.git && cd awesome-claude-skills/changelog-generator`</sub>

## Official Resources

- **[anthropics/skills](https://github.com/anthropics/skills)** — 199.1k ⭐ - Official Anthropic Agent Skills repository
  <sub>★ 201.7k · Python · source · pushed 2026-11-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/anthropics/skills.git`</sub>
- **[GitHub Awesome Copilot](https://github.com/github/awesome-copilot)** — 41.5k ⭐ - Official Copilot resources collection
  <sub>★ 41.6k · JavaScript · MIT · source · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/github/awesome-copilot.git`</sub>
- **[vercel-labs/skills](https://github.com/vercel-labs/skills)** — 40.5k ⭐ - Vercel official Skills CLI tool
  <sub>★ 41.2k · TypeScript · MIT · npx · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vercel-labs/agent-skills`</sub>
- **[agentskills/agentskills](https://github.com/agentskills/agentskills)** — 27.5k ⭐ - Official Agent Skills specification and documentation repository
  <sub>★ 27.7k · Python · Apache-2.0 · source · pushed 2026-11-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentskills/agentskills.git`</sub>
- **[microsoft/skills](https://github.com/microsoft/skills)** — 3.2k ⭐ - Microsoft official 131 Azure SDK Skills
  <sub>★ 3.3k · TypeScript · MIT · npx · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add microsoft/skills`</sub>
- **[microsoft/azure-skills](https://github.com/microsoft/azure-skills)** — 1.7k ⭐ - Official Azure skills plugin with MCP server configurations and 20 curated Azure skills
  <sub>★ 1.7k · JavaScript · MIT · npx · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills -a github-copilot -g -y`</sub>
- **[Agent Skills Open Standard](https://skill.md/)** — Official Agent Skills specification
  <sub>website</sub>
  <sub>`https://skill.md/`</sub>
- **[Agent Skills Specification](https://agentskills.io/specification)** — SKILL.md format specification
  <sub>website</sub>
  <sub>`https://agentskills.io/specification`</sub>
- **[GitHub Docs: About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)** — GitHub official overview of agent skills, supported hosts, and gh skill
  <sub>website</sub>
  <sub>`https://docs.github.com/en/copilot/concepts/agents/about-agent-skills`</sub>
- **[GitHub Docs: Adding agent skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/add-skills)** — GitHub official guide for creating, installing, and publishing agent skills
  <sub>website</sub>
  <sub>`https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/add-skills`</sub>
- **[GitHub CLI: gh skill](https://cli.github.com/manual/gh_skill)** — Official GitHub CLI commands for discovering, installing, updating, and publishing Agent Skills
  <sub>website</sub>
  <sub>`https://cli.github.com/manual/gh_skill`</sub>
- **[VS Code Docs: Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)** — Official VS Code guide for using Agent Skills with GitHub Copilot
  <sub>website</sub>
  <sub>`https://code.visualstudio.com/docs/copilot/customization/agent-skills`</sub>
- **[sendbird/sendbird-client-plugin](https://github.com/sendbird/sendbird-client-plugin)** — 0 ⭐ - Official Sendbird plugin with Agent Skills for adding Sendbird Chat, UIKit and Calls to iOS, Android, React and React Native apps, in Claude Code and Codex
  <sub>Shell · Apache-2.0 · source · pushed 2026-11-24</sub>
  <sub>`git clone https://github.com/sendbird/sendbird-client-plugin.git`</sub>
- **[OpenAI Codex: Agent Skills](https://developers.openai.com/codex/skills/)** — OpenAI official guide for using Agent Skills in Codex CLI, IDE extension, and Codex app
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/skills/`</sub>
- **[Agent Skills Index](https://agent-skills.md/)** — Community Skills search engine
  <sub>website</sub>
  <sub>`https://agent-skills.md/`</sub>
- **[Skills Leaderboard](https://skills.sh)** — Open Agent Skills ecosystem directory
  <sub>website</sub>
  <sub>`https://skills.sh`</sub>
- **[Tencent SkillHub](https://skillhub.tencent.com/)** — Tencent's Skills community with 13k+ skills, optimized for Chinese users
  <sub>website</sub>
  <sub>`https://skillhub.tencent.com/`</sub>
- **[ClawHub](https://docs.openclaw.ai/skills)** — OpenClaw's public skills registry for discovering and sharing skills
  <sub>website</sub>
  <sub>`https://docs.openclaw.ai/skills`</sub>
- **[Kling AI Plugin Skill (Global)](https://www.npmjs.com/package/@klingai/plugin-global)** — Official image and video generation and task-tracking Skill. A China npm package is also available. Use an OAuth account and credits for the corresponding region. Installation runs a postinstall script to register the shared kling-plugin CLI locally
  <sub>website</sub>
  <sub>`https://www.npmjs.com/package/@klingai/plugin-global`</sub>

## Development Tools

- **[browser-use/browser-use](https://github.com/browser-use/browser-use)** — 121.8k ⭐ - Browser automation Skill
  <sub>★ 122.3k · Python · MIT · uv · pushed 2026-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install browser-use==1.0.9`</sub>
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** — 119.8k ⭐ - Production-grade engineering skills and slash-command workflows for AI coding agents
  <sub>★ 120.9k · JavaScript · MIT · npx · pushed 2026-11-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add addyosmani/agent-skills # install all 26 skills`</sub>
- **[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)** — 34.8k ⭐ - Vercel React/Web design best practices Skills
  <sub>★ 35.1k · JavaScript · npx · pushed 2026-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vercel-labs/agent-skills`</sub>
- **[trailofbits/skills](https://github.com/trailofbits/skills)** — 8.4k ⭐ - Trail of Bits security research and audit Skills
  <sub>★ 8.5k · Python · CC-BY-SA-4.0 · source · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trailofbits/skills.git`</sub>
- **[claude-code-security-review](https://github.com/anthropics/claude-code-security-review)** — 7.1k ⭐ - AI security review GitHub Action (Official)
  <sub>★ 7.2k · Python · MIT · gh-action · pushed 2026-02-11</sub>
  <sub>`uses: anthropics/claude-code-security-review@main # in .github/workflows/*.yml`</sub>
- **[antfu/skills](https://github.com/antfu/skills)** — 6.1k ⭐ - Vue/Vite/Vitest development Skills
  <sub>★ 6.1k · TypeScript · MIT · source · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/antfu/skills.git`</sub>
- **[Expo Skills](https://github.com/expo/skills)** — 4.2k ⭐ - Expo/React Native development Skills
  <sub>★ 4.2k · Python · MIT · npx · pushed 2026-11-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills@latest add expo/skills --skill '*'`</sub>
- **[task-observer](https://github.com/rebelytics/one-skill-to-rule-them-all)** — 4.0k ⭐ - Watches work sessions, logs where skills fail, and turns the corrections into proposed skill improvements
  <sub>★ 4.1k · Markdown · CC-BY-4.0 · npx · pushed 2026-11-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills@1.8.1 add rebelytics/one-skill-to-rule-them-all --skill task-observer`</sub>
- **[playwright-skill](https://github.com/lackeyjb/playwright-skill)** — 3.3k ⭐ - Playwright browser automation testing Skill
  <sub>★ 3.3k · JavaScript · MIT · npx · pushed 2026-11-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add lackeyjb/playwright-skill --skill playwright-skill --global --yes`</sub>
- **[Supabase Agent Skills](https://github.com/supabase/agent-skills)** — 3.1k ⭐ - PostgreSQL best practices Skill by Supabase
  <sub>★ 3.1k · TypeScript · MIT · npx · pushed 2026-11-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add supabase/agent-skills`</sub>
- **[claude-code-skills](https://github.com/daymade/claude-code-skills)** — 1.5k ⭐ - Professional Skills marketplace
  <sub>★ 1.6k · Python · MIT · npx · pushed 2026-11-28 · macOS</sub>
  <sub>`npx skills add`</sub>
- **[skill-codex](https://github.com/skills-directory/skill-codex)** — 1.5k ⭐ - Delegate tasks to Codex Skill
  <sub>★ 1.5k · MIT · source · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/skills-directory/skill-codex.git`</sub>
- **[birdview](https://github.com/Qiuner/birdview)** — 704 ⭐ - Generate evidence-linked architecture and constraint maps, review planned change scope before implementation, and record verification results
  <sub>★ 707 · TypeScript · MIT · npx · pushed 2026-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Qiuner/birdview --skill birdview`</sub>
- **[elastic/agent-skills](https://github.com/elastic/agent-skills)** — 613 ⭐ - Official Elastic skills for Elasticsearch, Kibana, Observability, and Security workflows
  <sub>★ 615 · JavaScript · Apache-2.0 · npx · pushed 2026-11-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add elastic/agent-skills`</sub>
- **[markstream-install](https://github.com/Simon-He95/markstream-vue/tree/main/.agents/skills/markstream-install)** — 3.1k ⭐ - Install streaming Markdown renderers across Vue, React, Svelte, Angular, and Vue 2 projects
  <sub>Vue · MIT · in-repo · pushed 2026-11-27</sub>
  <sub>`git clone https://github.com/Simon-He95/markstream-vue.git && cd markstream-vue/.agents/skills/markstream-install`</sub>
- **[code-review](https://github.com/JackyST0/awesome-agent-skills/tree/main/examples/code-review)** — 670 ⭐ - Smart code review example Skill
  <sub>JavaScript · CC0-1.0 · in-repo · pushed 2026-11-26</sub>
  <sub>`git clone https://github.com/JackyST0/awesome-agent-skills.git && cd awesome-agent-skills/examples/code-review`</sub>
- **[git-commit](https://github.com/JackyST0/awesome-agent-skills/tree/main/examples/git-commit)** — 670 ⭐ - Git commit message generator Skill
  <sub>JavaScript · CC0-1.0 · in-repo · pushed 2026-11-26</sub>
  <sub>`git clone https://github.com/JackyST0/awesome-agent-skills.git && cd awesome-agent-skills/examples/git-commit`</sub>
- **[unit-test-generator](https://github.com/JackyST0/awesome-agent-skills/tree/main/examples/unit-test-generator)** — 670 ⭐ - Unit test auto-generator Skill
  <sub>JavaScript · CC0-1.0 · in-repo · pushed 2026-11-26</sub>
  <sub>`git clone https://github.com/JackyST0/awesome-agent-skills.git && cd awesome-agent-skills/examples/unit-test-generator`</sub>
- **[api-doc-generator](https://github.com/JackyST0/awesome-agent-skills/tree/main/examples/api-doc-generator)** — 670 ⭐ - API documentation generator Skill
  <sub>JavaScript · CC0-1.0 · in-repo · pushed 2026-11-26</sub>
  <sub>`git clone https://github.com/JackyST0/awesome-agent-skills.git && cd awesome-agent-skills/examples/api-doc-generator`</sub>
- **[debug-helper](https://github.com/JackyST0/awesome-agent-skills/tree/main/examples/debug-helper)** — 670 ⭐ - Code debugging assistant Skill
  <sub>JavaScript · CC0-1.0 · in-repo · pushed 2026-11-26</sub>
  <sub>`git clone https://github.com/JackyST0/awesome-agent-skills.git && cd awesome-agent-skills/examples/debug-helper`</sub>
- **[reverse-engineer-anything](https://github.com/morluto/rea/tree/main/.agents/skills/reverse-engineer-anything)** — 474.4k ⭐ - Inspect shipped binaries and JavaScript/Electron apps using REA CLI/MCP evidence; deep native analysis needs separately installed Hopper, Ghidra, or IDA
  <sub>TypeScript · MIT · in-repo · pushed 2026-11-28</sub>
  <sub>`git clone https://github.com/morluto/rea.git && cd rea/.agents/skills/reverse-engineer-anything`</sub>

## Skills Collections

- **[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)** — 80.1k ⭐ - Claude Skills collection by Composio
  <sub>★ 80.5k · Python · npx · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add chrome-relay`</sub>
- **[awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** — 58.6k ⭐ - Claude Code skills/hooks/plugins collection
  <sub>★ 59k · Python · source · pushed 2026-11-28 · macOS</sub>
  <sub>`git clone https://github.com/hesreallyhim/awesome-claude-code.git`</sub>
- **[awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)** — 41.2k ⭐ - The most comprehensive Cursor Rules collection
  <sub>★ 41.2k · JavaScript · CC0-1.0 · source · pushed 2026-05-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/PatrickJS/awesome-cursorrules.git`</sub>
- **[openskills](https://github.com/numman-ali/openskills)** — 10.8k ⭐ - Universal Skills loader (npm install)
  <sub>★ 10.8k · TypeScript · npx · pushed 2026-01-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx openskills install anthropics/skills`</sub>
- **[heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)** — 6.4k ⭐ - Community-curated Agent Skills directory focused on real-world skills used by engineering teams
  <sub>★ 6.4k · TypeScript · MIT · npx · pushed 2026-11-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills find [query] # Search for related skills`</sub>
- **[best-skills](https://github.com/xstongxue/best-skills)** — 3.2k ⭐ - High-quality Skills collection for paper writing, dev workflow, and content creation
  <sub>★ 3.2k · Python · Apache-2.0 · source · pushed 2026-11-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/xstongxue/best-skills.git`</sub>
- **[iart-ai/motion-skills](https://github.com/iart-ai/motion-skills)** — 2.1k ⭐ - 19 motion graphics and video skill packs covering kinetic typography, data-viz, explainers, social clips, WebGL and Manim animations
  <sub>★ 2.3k · HTML · MIT · npx · pushed 2026-11-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add iart-ai/tiktok-video-skills`</sub>
- **[skillkit](https://github.com/rohitg00/skillkit)** — 1.6k ⭐ - Cross-platform skills manager that installs, translates, and syncs skills across 40+ agents
  <sub>★ 1.6k · TypeScript · Apache-2.0 · npm · pushed 2026-06-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g skillkit # npm`</sub>
- **[nexscope-ai/eCommerce-Skills](https://github.com/nexscope-ai/eCommerce-Skills)** — 1.5k ⭐ - E-commerce skills for AI agents covering product research, marketing, and operations across Amazon, Shopify, TikTok Shop, and more
  <sub>★ 1.6k · Python · MIT · npx · pushed 2026-11-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add nexscope-ai/eCommerce-Skills -g`</sub>
- **[oh-my-agent](https://github.com/first-fluke/oh-my-agent)** — 1.5k ⭐ - 33 skills and 21 workflows kept in one .agents/skills folder and symlinked per skill into Claude Code, Codex, Cursor and other runtimes; oma link --dry-run previews what it will write
  <sub>★ 1.5k · TypeScript · MIT · psh · pushed 2026-11-28 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/first-fluke/oh-my-agent/main/cli/install.ps1 | iex`</sub>
- **[youtube-skills](https://github.com/ZeroPointRepo/youtube-skills)** — 1.2k ⭐ - YouTube transcript, video search, channel and playlist skills for Claude Code, OpenClaw, Hermes Agent, and other agent runtimes
  <sub>★ 1.2k · MIT · npx · pushed 2026-11-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx clawhub@latest install youtube-full`</sub>
- **[claude-skills-collection](https://github.com/abubakarsiddik31/claude-skills-collection)** — 1.1k ⭐ - Curated official and community Skills
  <sub>★ 1.1k · npx · pushed 2026-11-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add https://github.com/anthropics/skills --list`</sub>
- **[simonw/claude-skills](https://github.com/simonw/claude-skills)** — 932 ⭐ - Claude Skills documentation by Simon Willison
  <sub>★ 931 · source · pushed 2025-12-12</sub>
  <sub>`git clone https://github.com/simonw/claude-skills.git`</sub>
- **[laolaoshiren/claude-code-skills-zh](https://github.com/laolaoshiren/claude-code-skills-zh)** — 927 ⭐ - Curated Claude Code skills collection for Chinese developers, with 438+ curated skills and 20 original skills
  <sub>★ 927 · Python · MIT · npx · pushed 2026-11-27 · WSL2 · macOS? · Linux</sub>
  <sub>`npx skills add laolaoshiren/claude-code-skills-zh --skill skill-translator`</sub>
- **[nexscope-ai/Amazon-Skills](https://github.com/nexscope-ai/Amazon-Skills)** — 886 ⭐ - Free Amazon seller skills for keyword research, competitor analysis, listing audits, and more
  <sub>★ 912 · Python · MIT · npx · pushed 2026-11-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add nexscope-ai/Amazon-Skills -g`</sub>
- **[sno-station-skills](https://github.com/sno-ai/sno-station-skills)** — 871 ⭐ - Skills for Claude Code and Codex: cross-vendor peer review, handoff when one agent hits its usage limit, delegation and reporting
  <sub>★ 874 · Shell · Apache-2.0 · script · pushed 2026-11-27 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://sno.ai/install | sh`</sub>

## Data Processing

- **[context-engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** — 18.4k ⭐ - Context engineering and multi-Agent architecture
  <sub>★ 18.4k · Python · MIT · source · pushed 2026-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering.git`</sub>
- **[kordoc](https://github.com/chrisryugj/kordoc/tree/main/plugins/kordoc/skills/kordoc)** — 3.1k ⭐ - Korean document (HWP/HWPX/PDF) to Markdown conversion, form filling, and HWPX generation Skill
  <sub>TypeScript · MIT · in-repo · pushed 2026-11-28</sub>
  <sub>`git clone https://github.com/chrisryugj/kordoc.git && cd kordoc/plugins/kordoc/skills/kordoc`</sub>
- **[jiangshan-atlas](https://github.com/DeanChensj/jiangshan-map/tree/main/skills/jiangshan-atlas)** — 8.9k ⭐ - Interactive Chinese historical atlas Skill for locating ancient places, classical poems, and figure trajectories
  <sub>JavaScript · GPL-3.0 · in-repo · pushed 2026-11-28</sub>
  <sub>`git clone https://github.com/DeanChensj/jiangshan-map.git && cd jiangshan-map/skills/jiangshan-atlas`</sub>
- **[ava](https://github.com/antvis/AVA/tree/ai/skills/ava)** — 1.7k ⭐ - Analyze files and databases, reuse business definitions, verify calculations, and generate interactive charts
  <sub>TypeScript · MIT · in-repo · pushed 2026-11-26</sub>
  <sub>`git clone https://github.com/antvis/AVA.git && cd AVA/skills/ava`</sub>

## DevOps

- **[claudekit-skills](https://github.com/mrgoonie/claudekit-skills)** — 2.2k ⭐ - Docker/GCP/Cloudflare deployment and management
  <sub>★ 2.2k · Python · clone · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mrgoonie/claudekit-skills`</sub>

## Writing

- **[doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)** — 199.1k ⭐ - Document co-authoring Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/doc-coauthoring`</sub>
- **[internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms)** — 199.1k ⭐ - Internal communications generation Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/internal-comms`</sub>
- **[docx](https://github.com/anthropics/skills/tree/main/skills/docx)** — 199.1k ⭐ - Word document processing Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/docx`</sub>
- **[pdf](https://github.com/anthropics/skills/tree/main/skills/pdf)** — 199.1k ⭐ - Portable document format processing Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/pdf`</sub>
- **[pptx](https://github.com/anthropics/skills/tree/main/skills/pptx)** — 199.1k ⭐ - PowerPoint presentation generator Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/pptx`</sub>
- **[xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx)** — 199.1k ⭐ - Excel spreadsheet processing Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/xlsx`</sub>

## Design

- **[frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)** — 199.1k ⭐ - Frontend UI design Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/frontend-design`</sub>
- **[brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)** — 199.1k ⭐ - Brand design guidelines Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/brand-guidelines`</sub>
- **[canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)** — 199.1k ⭐ - Canvas design Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/canvas-design`</sub>
- **[theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory)** — 199.1k ⭐ - Theme style factory Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/theme-factory`</sub>
- **[algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art)** — 199.1k ⭐ - Algorithmic art generation Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/algorithmic-art`</sub>
- **[slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator)** — 199.1k ⭐ - Slack GIF creator Skill
  <sub>Python · in-repo · pushed 2026-11-16</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/slack-gif-creator`</sub>


---

Snapshot 2026-11-28. Stars, language, licence and last-push come from the GitHub API and drift daily.

Filter the same data in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/). Spreadsheet edition: retired. The last copy, built 2026-10-22, stays available but is no longer updated. The website is the maintained edition. Its last workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/download/v2026.10.22/Awesome-Agentic-Atlas-LIGHT.xlsx).
