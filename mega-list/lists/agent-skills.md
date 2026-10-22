# Agent Skills

Skill directories by vendor, plus community-published skills.

Curated by **[heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

320 entries · 184 distinct repos · 11 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/openai/skills"><img src="https://opengraph.githubassets.com/1/openai/skills" width="260"></a> | <a href="https://github.com/huggingface/skills"><img src="https://opengraph.githubassets.com/1/huggingface/skills" width="260"></a> | <a href="https://github.com/google-gemini/gemini-skills"><img src="https://opengraph.githubassets.com/1/google-gemini/gemini-skills" width="260"></a> |
| **[openai/develop-web-game](https://github.com/openai/skills)**<br>★ 28.2k | **[huggingface/hugging-face-model-trainer](https://github.com/huggingface/skills)**<br>★ 11.2k | **[google-gemini/vertex-ai-api-dev](https://github.com/google-gemini/gemini-skills)**<br>★ 4.3k |
| <a href="https://github.com/fal-ai-community/skills"><img src="https://opengraph.githubassets.com/1/fal-ai-community/skills" width="260"></a> | <a href="https://github.com/replicate/skills"><img src="https://opengraph.githubassets.com/1/replicate/skills" width="260"></a> | <a href="https://github.com/anthropics/skills/tree/main/skills/docx"><img src="https://opengraph.githubassets.com/1/anthropics/skills" width="260"></a> |
| **[fal-ai-community/fal-generate](https://github.com/fal-ai-community/skills)**<br>★ 254 | **[replicate/replicate](https://github.com/replicate/skills)**<br>★ 136 | **[anthropics/docx](https://github.com/anthropics/skills/tree/main/skills/docx)**<br>★ — |

## Contents

- [AI Platforms &amp; Models](#ai-platforms--models) (47)
- [Claude and Anthropic](#claude-and-anthropic) (3)
- [Business, Productivity &amp; Marketing](#business-productivity--marketing) (47)
- [Cloud &amp; Infrastructure](#cloud--infrastructure) (29)
- [Model Context Protocol (MCP)](#model-context-protocol-mcp) (3)
- [Agent Skills Specification](#agent-skills-specification) (1)
- [Developer Tools &amp; Frameworks](#developer-tools--frameworks) (25)
- [GitHub Copilot](#github-copilot) (2)
- [Security &amp; Web Intelligence](#security--web-intelligence) (21)
- [Community Skills](#community-skills) (132)
- [Google Ecosystem](#google-ecosystem) (10)

## AI Platforms &amp; Models

- **[openai/develop-web-game](https://github.com/openai/skills)** — Build and test web games iteratively using Playwright
  <sub>★ 28.2k · Python · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/openai/skills.git`</sub>
- **[huggingface/hugging-face-model-trainer](https://github.com/huggingface/skills)** — Train models with TRL: SFT, DPO, GRPO
  <sub>★ 11.2k · Python · Apache-2.0 · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/huggingface/skills.git`</sub>
- **[google-gemini/vertex-ai-api-dev](https://github.com/google-gemini/gemini-skills)** — Developing Gemini apps on Google Cloud Vertex AI
  <sub>★ 4.3k · Python · Apache-2.0 · npx · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add google-gemini/gemini-skills --list`</sub>
- **[fal-ai-community/fal-generate](https://github.com/fal-ai-community/skills)** — Generate images and videos using fal.ai
  <sub>★ 254 · JavaScript · source · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fal-ai-community/skills.git`</sub>
- **[replicate/replicate](https://github.com/replicate/skills)** — Discover and run AI models via API
  <sub>★ 136 · Shell · Apache-2.0 · npx · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add replicate/skills`</sub>
- **[anthropics/docx](https://github.com/anthropics/skills/tree/main/skills/docx)** — Create, edit, and analyze Word documents
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/docx`</sub>
- **[anthropics/doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)** — Collaborative document editing and co-authoring
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/doc-coauthoring`</sub>
- **[anthropics/pptx](https://github.com/anthropics/skills/tree/main/skills/pptx)** — Create, edit, and analyze PowerPoint presentations
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/pptx`</sub>
- **[anthropics/xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx)** — Create, edit, and analyze Excel spreadsheets
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/xlsx`</sub>
- **[anthropics/pdf](https://github.com/anthropics/skills/tree/main/skills/pdf)** — Extract text, create PDFs, and handle forms
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/pdf`</sub>
- **[anthropics/algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art)** — Create generative art using p5.js with seeded randomness
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/algorithmic-art`</sub>
- **[anthropics/canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)** — Design visual art in PNG and PDF formats
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/canvas-design`</sub>
- **[anthropics/frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)** — Frontend design and UI/UX development tools
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/frontend-design`</sub>
- **[anthropics/slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator)** — Create animated GIFs optimized for Slack size constraints
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/slack-gif-creator`</sub>
- **[anthropics/theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory)** — Style artifacts with professional themes or generate custom themes
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/theme-factory`</sub>
- **[anthropics/web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder)** — Build complex claude.ai HTML artifacts with React and Tailwind
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/web-artifacts-builder`</sub>
- **[anthropics/mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder)** — Create MCP servers to integrate external APIs and services
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/mcp-builder`</sub>
- **[anthropics/webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing)** — Test local web applications using Playwright
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/webapp-testing`</sub>
- **[anthropics/brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)** — Apply Anthropic's brand colors and typography to artifacts
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/brand-guidelines`</sub>
- **[anthropics/internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms)** — Write status reports, newsletters, and FAQs
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/internal-comms`</sub>
- **[anthropics/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)** — Guide for creating skills that extend Claude's capabilities
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/skills/skill-creator`</sub>
- **[anthropics/template](https://github.com/anthropics/skills/tree/main/template)** — Basic template for creating new skills
  <sub>Python · in-repo · pushed 2026-10-09</sub>
  <sub>`git clone https://github.com/anthropics/skills.git && cd skills/template`</sub>
- **[openai/cloudflare-deploy](https://github.com/openai/skills/tree/main/skills/.curated/cloudflare-deploy)** — Deploy apps to Cloudflare using Workers and Pages
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/cloudflare-deploy`</sub>
- **[openai/gh-address-comments](https://github.com/openai/skills/tree/main/skills/.curated/gh-address-comments)** — Address review and issue comments on open GitHub PRs via CLI
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/gh-address-comments`</sub>
- **[openai/gh-fix-ci](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci)** — Debug and fix failing GitHub Actions PR checks
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/gh-fix-ci`</sub>
- **[openai/imagegen](https://github.com/openai/skills/tree/main/skills/.system/imagegen)** — Generate and edit images using OpenAI's Image API
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.system/imagegen`</sub>
- **[openai/jupyter-notebook](https://github.com/openai/skills/tree/main/skills/.curated/jupyter-notebook)** — Create clean, reproducible Jupyter notebooks
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/jupyter-notebook`</sub>
- **[openai/linear](https://github.com/openai/skills/tree/main/skills/.curated/linear)** — Manage issues, projects, and team workflows in Linear
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/linear`</sub>
- **[openai/netlify-deploy](https://github.com/openai/skills/tree/main/skills/.curated/netlify-deploy)** — Automate Netlify deployments with CLI support
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/netlify-deploy`</sub>
- **[openai/notion-knowledge-capture](https://github.com/openai/skills/tree/main/skills/.curated/notion-knowledge-capture)** — Convert conversations into structured Notion wiki entries
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/notion-knowledge-capture`</sub>
- **[openai/pdf](https://github.com/openai/skills/tree/main/skills/.curated/pdf)** — Read, create, and review PDFs with layout integrity
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/pdf`</sub>
- **[openai/playwright](https://github.com/openai/skills/tree/main/skills/.curated/playwright)** — Automate real browser interactions for navigation and forms
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/playwright`</sub>
- **[openai/speech](https://github.com/openai/skills/tree/main/skills/.curated/speech)** — Generate spoken audio from text using OpenAI's API
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/speech`</sub>
- **[openai/figma](https://github.com/openai/skills/tree/main/skills/.curated/figma)** — Use the Figma MCP server to fetch design context
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/figma`</sub>
- **[openai/figma-implement-design](https://github.com/openai/skills/tree/main/skills/.curated/figma-implement-design)** — Translate Figma designs into production-ready code
  <sub>Python · in-repo · pushed 2026-09-08</sub>
  <sub>`git clone https://github.com/openai/skills.git && cd skills/skills/.curated/figma-implement-design`</sub>
- **[google-gemini/gemini-api-dev](https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-api-dev)** — Best practices for developing Gemini-powered apps
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-13</sub>
  <sub>`git clone https://github.com/google-gemini/gemini-skills.git && cd gemini-skills/skills/gemini-api-dev`</sub>
- **[google-gemini/gemini-live-api-dev](https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-live-api-dev)** — Building real-time bidirectional streaming apps
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-13</sub>
  <sub>`git clone https://github.com/google-gemini/gemini-skills.git && cd gemini-skills/skills/gemini-live-api-dev`</sub>
- **[huggingface/hf-cli](https://github.com/huggingface/skills/tree/main/skills/hf-cli)** — HF CLI tool for Hub operations
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/huggingface/skills.git && cd skills/skills/hf-cli`</sub>
- **[huggingface/hugging-face-datasets](https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets)** — Create and manage datasets with SQL querying
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/huggingface/skills.git && cd skills/skills/huggingface-datasets`</sub>
- **[huggingface/transformers.js](https://github.com/huggingface/skills/tree/main/skills/transformers-js)** — Run ML models in the browser with Transformers.js
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/huggingface/skills.git && cd skills/skills/transformers-js`</sub>
- **[MiniMax-AI/frontend-dev](https://github.com/MiniMax-AI/skills/tree/main/skills/frontend-dev)** — Frontend with animations and AI media via MiniMax
  <sub>C# · MIT · in-repo · pushed 2026-04-18</sub>
  <sub>`git clone https://github.com/MiniMax-AI/skills.git && cd skills/skills/frontend-dev`</sub>
- **[MiniMax-AI/minimax-pdf](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-pdf)** — Generate, fill, and reformat PDFs
  <sub>C# · MIT · in-repo · pushed 2026-04-18</sub>
  <sub>`git clone https://github.com/MiniMax-AI/skills.git && cd skills/skills/minimax-pdf`</sub>
- **[Bria-AI/bria-ai](https://github.com/Bria-AI/bria-skill/tree/main/skills/bria-ai)** — AI image generation, editing, and background removal API
  <sub>Python · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Bria-AI/bria-skill.git && cd bria-skill/skills/bria-ai`</sub>
- **[Bria-AI/remove-background](https://github.com/Bria-AI/bria-skill/tree/main/skills/remove-background)** — Remove image backgrounds for transparent PNGs and cutouts
  <sub>Python · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Bria-AI/bria-skill.git && cd bria-skill/skills/remove-background`</sub>
- **[Bria-AI/video-remove-background](https://github.com/Bria-AI/bria-skill/tree/main/skills/video-remove-background)** — Remove video backgrounds for transparent, alpha-channel clips
  <sub>Python · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Bria-AI/bria-skill.git && cd bria-skill/skills/video-remove-background`</sub>
- **[Bria-AI/vgl](https://github.com/Bria-AI/bria-skill/tree/main/skills/vgl)** — Structured JSON control over AI image generation (FIBO)
  <sub>Python · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Bria-AI/bria-skill.git && cd bria-skill/skills/vgl`</sub>
- **[Bria-AI/image-utils](https://github.com/Bria-AI/bria-skill/tree/main/skills/image-utils)** — Resize, crop, composite, and convert images with Pillow
  <sub>Python · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Bria-AI/bria-skill.git && cd bria-skill/skills/image-utils`</sub>

## Claude and Anthropic

- **[Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)** — Official quick start guide
  <sub>website</sub>
  <sub>`https://support.claude.com/en/articles/12512180-using-skills-in-claude`</sub>
- **[How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)** — Step-by-step authoring
  <sub>website</sub>
  <sub>`https://support.claude.com/en/articles/12512198-creating-custom-skills`</sub>
- **[Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)** — Official reference
  <sub>website</sub>
  <sub>`https://code.claude.com/docs/en/skills`</sub>

## Business, Productivity &amp; Marketing

- **[garrytan/gstack](https://github.com/garrytan/gstack)** — Full gstack collection: YC founder stack for planning, review, QA, and shipping
  <sub>★ 137.2k · TypeScript · MIT · source · pushed 2026-10-22 · macOS</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git`</sub>
- **[coreyhaines31/email-sequence](https://github.com/coreyhaines31/marketingskills)** — Build email sequences and drip campaigns
  <sub>★ 55.8k · JavaScript · MIT · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add coreyhaines31/marketingskills`</sub>
- **[phuryn/pm-skills](https://github.com/phuryn/pm-skills)** — Full collection: advanced product management frameworks, OKRs, and strategy skills
  <sub>★ 27.3k · MIT · source · pushed 2026-10-16 · Win?</sub>
  <sub>`git clone https://github.com/phuryn/pm-skills.git`</sub>
- **[product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills)** — 68 product management skills covering discovery, definition, delivery, and iteration, with 6 sub-agents and 12 workflows
  <sub>★ 750 · JavaScript · Apache-2.0 · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add product-on-purpose/pm-skills`</sub>
- **[better-auth/explain-error](https://github.com/better-auth/skills)** — Explain Better Auth error messages
  <sub>★ 223 · source · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/better-auth/skills.git`</sub>
- **[ndesv21/socialclaw](https://github.com/ndesv21/socialclaw)** — Schedule and publish social media posts across 13 platforms (X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, Pinterest) via a single workspace API key
  <sub>★ 97 · JavaScript · MIT · npm · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g socialclaw`</sub>
- **[agentrhq/authsome](https://github.com/agentrhq/authsome)** — Local OAuth2 and API-key credential broker for AI agents. Login once via browser PKCE or device code, encrypted vault at ~/.authsome, local proxy injects credentials at request time. 30+ providers preconfigured
  <sub>★ 97 · Python · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add agentrhq/authsome`</sub>
- **[humanpen/humanpen-skill](https://github.com/humanpen/humanpen-skill)** — Rewrites .docx/.pptx documents to read as human-written and lower AI-detection scores
  <sub>★ 93 · Python · Apache-2.0 · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/humanpen/humanpen-skill`</sub>
- **[javimosch/supercli](https://github.com/javimosch/supercli)** — Universal CLI router with 4,795+ agent skills (SKILL.md). Agents discover CLI tools by intent via sc skills search, inspect schemas via sc inspect, and execute with deterministic JSON output. Each plugin ships with its own skills/quickstart/SKILL.md — instant agent onboarding for 7,000+ CLI tools
  <sub>★ 55 · JavaScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npx supercli skills search "deploy"`</sub>
- **[surendranb/writing-skills](https://github.com/surendranb/writing-skills)** — 15 writing-style skills: 8 measurable frameworks (plain language, ASD-STE100, AP journalism, GOV.UK, business BLUF) and 7 character voices, each with a verify checklist
  <sub>★ 49 · Python · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add writing-skills`</sub>
- **[trycourier/courier-skills](https://github.com/trycourier/courier-skills)** — Multi-channel notifications via email, SMS, push, and chat
  <sub>★ 14 · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add trycourier/courier-skills`</sub>
- **[stripe/stripe-best-practices](https://github.com/stripe/ai/tree/main/skills/stripe-best-practices)** — Best practices for building Stripe integrations
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/stripe/ai.git && cd ai/skills/stripe-best-practices`</sub>
- **[stripe/upgrade-stripe](https://github.com/stripe/ai/tree/main/skills/upgrade-stripe)** — Upgrade Stripe SDK and API versions
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/stripe/ai.git && cd ai/skills/upgrade-stripe`</sub>
- **[typefully/typefully](https://github.com/typefully/agent-skills/tree/main/skills/typefully)** — Create, schedule, and publish social media content
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/typefully/agent-skills.git && cd agent-skills/skills/typefully`</sub>
- **[composiohq/composio](https://github.com/composio-community/skills/tree/main/skills/composio)** — Connect AI agents to 1000+ external apps with managed authentication
  <sub>Python · MIT · in-repo · pushed 2026-03-19</sub>
  <sub>`git clone https://github.com/composio-community/skills.git && cd skills/skills/composio`</sub>
- **[makenotion/knowledge-capture](https://github.com/makenotion/cursor-notion-plugin/tree/main/skills/knowledge-capture)** — Transform conversations into structured Notion documentation
  <sub>in-repo · pushed 2026-02-07</sub>
  <sub>`git clone https://github.com/makenotion/cursor-notion-plugin.git && cd cursor-notion-plugin/skills/knowledge-capture`</sub>
- **[makenotion/meeting-intelligence](https://github.com/makenotion/cursor-notion-plugin/tree/main/skills/meeting-intelligence)** — Prepare meeting materials by gathering Notion context
  <sub>in-repo · pushed 2026-02-07</sub>
  <sub>`git clone https://github.com/makenotion/cursor-notion-plugin.git && cd cursor-notion-plugin/skills/meeting-intelligence`</sub>
- **[makenotion/spec-to-implementation](https://github.com/makenotion/cursor-notion-plugin/tree/main/skills/spec-to-implementation)** — Turn tech specs into concrete Notion tasks
  <sub>in-repo · pushed 2026-02-07</sub>
  <sub>`git clone https://github.com/makenotion/cursor-notion-plugin.git && cd cursor-notion-plugin/skills/spec-to-implementation`</sub>
- **[resend/resend](https://github.com/resend/resend-skills/tree/main/skills/resend)** — Send and manage emails via the Resend API
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-17</sub>
  <sub>`git clone https://github.com/resend/resend-skills.git && cd resend-skills/skills/resend`</sub>
- **[resend/react-email](https://github.com/resend/resend-skills/tree/main/skills/react-email)** — Build emails with React Email components
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-17</sub>
  <sub>`git clone https://github.com/resend/resend-skills.git && cd resend-skills/skills/react-email`</sub>
- **[resend/email-best-practices](https://github.com/resend/resend-skills/tree/main/skills/email-best-practices)** — Email deliverability and design best practices
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-17</sub>
  <sub>`git clone https://github.com/resend/resend-skills.git && cd resend-skills/skills/email-best-practices`</sub>
- **[sanity-io/sanity-best-practices](https://github.com/sanity-io/agent-toolkit/tree/main/skills/sanity-best-practices)** — Best practices for Sanity Studio and content workflows
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/sanity-io/agent-toolkit.git && cd agent-toolkit/skills/sanity-best-practices`</sub>
- **[sanity-io/content-modeling-best-practices](https://github.com/sanity-io/agent-toolkit/tree/main/skills/content-modeling-best-practices)** — Guidelines for designing scalable content models in Sanity
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/sanity-io/agent-toolkit.git && cd agent-toolkit/skills/content-modeling-best-practices`</sub>
- **[sanity-io/seo-aeo-best-practices](https://github.com/sanity-io/agent-toolkit/tree/main/skills/seo-aeo-best-practices)** — SEO and answer engine optimization patterns
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/sanity-io/agent-toolkit.git && cd agent-toolkit/skills/seo-aeo-best-practices`</sub>
- **[better-auth/best-practices](https://github.com/better-auth/skills/tree/main/better-auth/best-practices)** — Best practices for Better Auth integration
  <sub>in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/better-auth/skills.git && cd skills/better-auth/best-practices`</sub>
- **[better-auth/create-auth](https://github.com/better-auth/skills/tree/main/better-auth/create-auth)** — Create authentication setup with Better Auth
  <sub>in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/better-auth/skills.git && cd skills/better-auth/create-auth`</sub>
- **[better-auth/twoFactor](https://github.com/better-auth/skills/tree/main/better-auth/twoFactor)** — Two-factor authentication with Better Auth
  <sub>in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/better-auth/skills.git && cd skills/better-auth/twoFactor`</sub>
- **[nowork-studio/seo](https://github.com/nowork-studio/NotFair/tree/main/seo)** — SEO and GEO: site analysis, keyword research, meta tags, schema markup, and content writing
  <sub>Python · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/nowork-studio/NotFair.git && cd NotFair/seo`</sub>
- **[nowork-studio/google-ads](https://github.com/nowork-studio/NotFair/tree/main/google-ads)** — Google Ads audits: wasted-spend detection, search-term cleanup, keyword and bid management
  <sub>Python · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/nowork-studio/NotFair.git && cd NotFair/google-ads`</sub>
- **[nowork-studio/meta-ads](https://github.com/nowork-studio/NotFair/tree/main/meta-ads)** — Meta (Facebook + Instagram) Ads: ROAS analysis, creative-fatigue and audience-overlap diagnosis
  <sub>Python · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/nowork-studio/NotFair.git && cd NotFair/meta-ads`</sub>
- **[coreyhaines31/ai-seo](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ai-seo)** — Optimize content for AI-generated answers
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/coreyhaines31/marketingskills.git && cd marketingskills/skills/ai-seo`</sub>
- **[coreyhaines31/copywriting](https://github.com/coreyhaines31/marketingskills/tree/main/skills/copywriting)** — Write marketing copy for landing pages and ads
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/coreyhaines31/marketingskills.git && cd marketingskills/skills/copywriting`</sub>
- **[coreyhaines31/pricing-strategy](https://github.com/coreyhaines31/marketingskills/tree/main/skills/pricing)** — Define pricing and packaging for SaaS
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/coreyhaines31/marketingskills.git && cd marketingskills/skills/pricing`</sub>
- **[coreyhaines31/social-content](https://github.com/coreyhaines31/marketingskills/tree/main/skills/social)** — Create and schedule social media content
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/coreyhaines31/marketingskills.git && cd marketingskills/skills/social`</sub>
- **[deanpeters/epic-hypothesis](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/epic-hypothesis)** — Turn initiatives into testable hypotheses
  <sub>Shell · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/deanpeters/Product-Manager-Skills.git && cd Product-Manager-Skills/skills/epic-hypothesis`</sub>
- **[deanpeters/opportunity-solution-tree](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/opportunity-solution-tree)** — Generate solution trees based on Teresa Torres' method
  <sub>Shell · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/deanpeters/Product-Manager-Skills.git && cd Product-Manager-Skills/skills/opportunity-solution-tree`</sub>
- **[deanpeters/prd-development](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/prd-development)** — Structured PRD process: problem to metrics
  <sub>Shell · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/deanpeters/Product-Manager-Skills.git && cd Product-Manager-Skills/skills/prd-development`</sub>
- **[deanpeters/roadmap-planning](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/roadmap-planning)** — Strategic roadmap process and communication
  <sub>Shell · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/deanpeters/Product-Manager-Skills.git && cd Product-Manager-Skills/skills/roadmap-planning`</sub>
- **[phuryn/create-prd](https://github.com/phuryn/pm-skills/tree/main/pm-execution/skills/create-prd)** — Create a PRD with 8-section template
  <sub>MIT · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/phuryn/pm-skills.git && cd pm-skills/pm-execution/skills/create-prd`</sub>
- **[phuryn/product-strategy](https://github.com/phuryn/pm-skills/tree/main/pm-product-strategy/skills/product-strategy)** — Create product strategy using the Canvas
  <sub>MIT · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/phuryn/pm-skills.git && cd pm-skills/pm-product-strategy/skills/product-strategy`</sub>
- **[phuryn/user-personas](https://github.com/phuryn/pm-skills/tree/main/pm-market-research/skills/user-personas)** — Create user personas with JTBD, pains, and gains
  <sub>MIT · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/phuryn/pm-skills.git && cd pm-skills/pm-market-research/skills/user-personas`</sub>
- **[phuryn/market-sizing](https://github.com/phuryn/pm-skills/tree/main/pm-market-research/skills/market-sizing)** — Estimate TAM, SAM, SOM with top-down and bottom-up
  <sub>MIT · in-repo · pushed 2026-10-16</sub>
  <sub>`git clone https://github.com/phuryn/pm-skills.git && cd pm-skills/pm-market-research/skills/market-sizing`</sub>
- **[garrytan/office-hours](https://github.com/garrytan/gstack/tree/main/office-hours)** — YC Office Hours: reframing product before code
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git && cd gstack/office-hours`</sub>
- **[garrytan/plan-ceo-review](https://github.com/garrytan/gstack/tree/main/plan-ceo-review)** — CEO/Founder plan review modes
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git && cd gstack/plan-ceo-review`</sub>
- **[garrytan/design-review](https://github.com/garrytan/gstack/tree/main/design-review)** — Visual audit and atomic fixes with screenshots
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git && cd gstack/design-review`</sub>
- **[garrytan/qa](https://github.com/garrytan/gstack/tree/main/qa)** — QA Lead: find bugs and generate regression tests
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git && cd gstack/qa`</sub>
- **[garrytan/ship](https://github.com/garrytan/gstack/tree/main/ship)** — Release Engineer: sync, test, audit, and push
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-22</sub>
  <sub>`git clone https://github.com/garrytan/gstack.git && cd gstack/ship`</sub>

## Cloud &amp; Infrastructure

- **[vercel-labs/next-best-practices](https://github.com/vercel-labs/agent-skills)** — Next.js best practices and recommended patterns
  <sub>★ 32.8k · JavaScript · npx · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vercel-labs/agent-skills`</sub>
- **[cloudflare/building-ai-agent-on-cloudflare](https://github.com/cloudflare/skills)** — Build AI agents with state and WebSockets on Cloudflare
  <sub>★ 3.1k · Shell · Apache-2.0 · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/cloudflare/skills`</sub>
- **[cloudflare/agents-sdk](https://github.com/cloudflare/skills/tree/main/skills/agents-sdk)** — Build stateful AI agents with scheduling, RPC, and MCP servers
  <sub>Shell · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/cloudflare/skills.git && cd skills/skills/agents-sdk`</sub>
- **[cloudflare/durable-objects](https://github.com/cloudflare/skills/tree/main/skills/durable-objects)** — Stateful coordination with RPC, SQLite, and WebSockets
  <sub>Shell · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/cloudflare/skills.git && cd skills/skills/durable-objects`</sub>
- **[cloudflare/web-perf](https://github.com/cloudflare/skills/tree/main/skills/web-perf)** — Audit Core Web Vitals and render-blocking resources
  <sub>Shell · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/cloudflare/skills.git && cd skills/skills/web-perf`</sub>
- **[cloudflare/wrangler](https://github.com/cloudflare/skills/tree/main/skills/wrangler)** — Deploy and manage Workers, KV, R2, D1, Vectorize, Queues, Workflows
  <sub>Shell · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/cloudflare/skills.git && cd skills/skills/wrangler`</sub>
- **[netlify/netlify-functions](https://github.com/netlify/context-and-tools/tree/main/skills/netlify-functions)** — Build serverless API endpoints and background tasks
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/netlify/context-and-tools.git && cd context-and-tools/skills/netlify-functions`</sub>
- **[netlify/netlify-edge-functions](https://github.com/netlify/context-and-tools/tree/main/skills/netlify-edge-functions)** — Low-latency edge middleware and geolocation logic
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/netlify/context-and-tools.git && cd context-and-tools/skills/netlify-edge-functions`</sub>
- **[netlify/netlify-blobs](https://github.com/netlify/context-and-tools/tree/main/skills/netlify-blobs)** — Key-value object storage for files and data
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/netlify/context-and-tools.git && cd context-and-tools/skills/netlify-blobs`</sub>
- **[netlify/netlify-db](https://github.com/netlify/context-and-tools/tree/main/skills/netlify-database)** — Managed Postgres with deploy preview branching
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/netlify/context-and-tools.git && cd context-and-tools/skills/netlify-database`</sub>
- **[netlify/netlify-deploy](https://github.com/netlify/context-and-tools/tree/main/skills/netlify-deploy)** — Automated deployment workflow for Netlify sites
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/netlify/context-and-tools.git && cd context-and-tools/skills/netlify-deploy`</sub>
- **[netlify/netlify-ai-gateway](https://github.com/netlify/context-and-tools/tree/main/skills/netlify-ai-gateway)** — Access AI models via unified gateway endpoint
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/netlify/context-and-tools.git && cd context-and-tools/skills/netlify-ai-gateway`</sub>
- **[vercel-labs/react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)** — React best practices and patterns
  <sub>JavaScript · in-repo · pushed 2026-10-14</sub>
  <sub>`git clone https://github.com/vercel-labs/agent-skills.git && cd agent-skills/skills/react-best-practices`</sub>
- **[vercel-labs/web-design-guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines)** — Web design guidelines and standards
  <sub>JavaScript · in-repo · pushed 2026-10-14</sub>
  <sub>`git clone https://github.com/vercel-labs/agent-skills.git && cd agent-skills/skills/web-design-guidelines`</sub>
- **[vercel-labs/react-native-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-native-skills)** — React Native best practices and performance guidelines
  <sub>JavaScript · in-repo · pushed 2026-10-14</sub>
  <sub>`git clone https://github.com/vercel-labs/agent-skills.git && cd agent-skills/skills/react-native-skills`</sub>
- **[hashicorp/new-terraform-provider](https://github.com/hashicorp/agent-skills/tree/main/plugins/terraform/skills/new-terraform-provider)** — Scaffold a new Terraform provider project using the Plugin Framework
  <sub>HCL · MPL-2.0 · in-repo · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/hashicorp/agent-skills.git && cd agent-skills/plugins/terraform/skills/new-terraform-provider`</sub>
- **[hashicorp/provider-resources](https://github.com/hashicorp/agent-skills/tree/main/plugins/terraform/skills/provider-resources)** — Implement Terraform Provider resources and data sources
  <sub>HCL · MPL-2.0 · in-repo · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/hashicorp/agent-skills.git && cd agent-skills/plugins/terraform/skills/provider-resources`</sub>
- **[hashicorp/provider-test-patterns](https://github.com/hashicorp/agent-skills/tree/main/plugins/terraform/skills/provider-test-patterns)** — Acceptance test patterns for Terraform providers
  <sub>HCL · MPL-2.0 · in-repo · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/hashicorp/agent-skills.git && cd agent-skills/plugins/terraform/skills/provider-test-patterns`</sub>
- **[hashicorp/refactor-module](https://github.com/hashicorp/agent-skills/tree/main/plugins/terraform/skills/refactor-module)** — Transform monolithic Terraform configurations into reusable modules
  <sub>HCL · MPL-2.0 · in-repo · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/hashicorp/agent-skills.git && cd agent-skills/plugins/terraform/skills/refactor-module`</sub>
- **[hashicorp/terraform-style-guide](https://github.com/hashicorp/agent-skills/tree/main/plugins/terraform/skills/terraform-style-guide)** — Generate Terraform HCL code following HashiCorp's official style conventions
  <sub>HCL · MPL-2.0 · in-repo · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/hashicorp/agent-skills.git && cd agent-skills/plugins/terraform/skills/terraform-style-guide`</sub>
- **[hashicorp/terraform-stacks](https://github.com/hashicorp/agent-skills/tree/main/plugins/terraform/skills/terraform-stacks)** — Manage infrastructure across multiple environments, regions, and cloud accounts
  <sub>HCL · MPL-2.0 · in-repo · pushed 2026-10-05</sub>
  <sub>`git clone https://github.com/hashicorp/agent-skills.git && cd agent-skills/plugins/terraform/skills/terraform-stacks`</sub>
- **[neondatabase/neon-postgres](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-postgres)** — Best practices for Neon Serverless Postgres
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/neondatabase/agent-skills.git && cd agent-skills/skills/neon-postgres`</sub>
- **[neondatabase/claimable-postgres](https://github.com/neondatabase/mcp-server-neon/tree/main/.agents/skills/claimable-postgres)** — Claimable Postgres database provisioning with Neon
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/neondatabase/mcp-server-neon.git && cd mcp-server-neon/.agents/skills/claimable-postgres`</sub>
- **[neondatabase/neon-postgres-egress-optimizer](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-postgres-egress-optimizer)** — Optimize Neon Postgres egress and data transfer
  <sub>JavaScript · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/neondatabase/agent-skills.git && cd agent-skills/skills/neon-postgres-egress-optimizer`</sub>
- **[clickhouse/clickhouse-best-practices](https://github.com/ClickHouse/agent-skills/tree/main/skills/clickhouse-best-practices)** — Best practices for working with ClickHouse
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/ClickHouse/agent-skills.git && cd agent-skills/skills/clickhouse-best-practices`</sub>
- **[supabase/postgres-best-practices](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices)** — PostgreSQL best practices for Supabase
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-02</sub>
  <sub>`git clone https://github.com/supabase/agent-skills.git && cd agent-skills/skills/supabase-postgres-best-practices`</sub>
- **[tinybirdco/tinybird-best-practices](https://github.com/tinybirdco/tinybird-agent-skills/tree/main/skills/tinybird-best-practices)** — Tinybird project guidelines for datasources, pipes, endpoints, and SQL
  <sub>in-repo · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/tinybirdco/tinybird-agent-skills.git && cd tinybird-agent-skills/skills/tinybird-best-practices`</sub>
- **[tinybirdco/tinybird-cli-guidelines](https://github.com/tinybirdco/tinybird-agent-skills/tree/main/skills/tinybird-cli-guidelines)** — Tinybird CLI usage guidelines and commands
  <sub>in-repo · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/tinybirdco/tinybird-agent-skills.git && cd tinybird-agent-skills/skills/tinybird-cli-guidelines`</sub>
- **[tinybirdco/tinybird-typescript-sdk-guidelines](https://github.com/tinybirdco/tinybird-agent-skills/tree/main/skills/tinybird-typescript-sdk-guidelines)** — Tinybird TypeScript SDK usage guidelines
  <sub>in-repo · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/tinybirdco/tinybird-agent-skills.git && cd tinybird-agent-skills/skills/tinybird-typescript-sdk-guidelines`</sub>

## Model Context Protocol (MCP)

- **[MCP Server Examples](https://github.com/modelcontextprotocol/servers)** — Official server implementations
  <sub>★ 91.5k · TypeScript · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @modelcontextprotocol/server-memory`</sub>
- **[MCP Official Documentation](https://modelcontextprotocol.io/)** — The open standard
  <sub>website</sub>
  <sub>`https://modelcontextprotocol.io/`</sub>
- **[Build your first MCP Server](https://modelcontextprotocol.io/docs/first-server)** — Python/TypeScript guide
  <sub>website</sub>
  <sub>`https://modelcontextprotocol.io/docs/first-server`</sub>

## Agent Skills Specification

- **[agentskills/agentskills](https://github.com/agentskills/agentskills)** — The open SKILL.md format specification and reference docs
  <sub>★ 26.4k · Python · Apache-2.0 · source · pushed 2026-08-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agentskills/agentskills.git`</sub>

## Developer Tools &amp; Frameworks

- **[remotion-dev/remotion](https://github.com/remotion-dev/skills)** — Programmatic video creation with React
  <sub>★ 5.5k · TypeScript · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add remotion-dev/skills`</sub>
- **[callstackincubator/github](https://github.com/callstackincubator/agent-skills)** — GitHub workflow patterns for PRs, code review, branching
  <sub>★ 1.7k · Shell · MIT · npx · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills@latest add callstackincubator/agent-skills --skill '*'`</sub>
- **[Ivy Tendril](https://github.com/Ivy-Interactive/Ivy-Tendril)** — Open-source agentic software factory with an amazing UI that handles parallel Git worktrees for you, complete with programmatic verifications and fast review loops
  <sub>★ 203 · C# · psh · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://cdn.ivy.app/install-tendril.ps1 | iex`</sub>
- **[voltagent/create-voltagent](https://github.com/VoltAgent/skills/tree/main/skills/create-voltagent)** — Project setup guide with CLI and manual steps
  <sub>MIT · in-repo · pushed 2026-01-27</sub>
  <sub>`git clone https://github.com/VoltAgent/skills.git && cd skills/skills/create-voltagent`</sub>
- **[voltagent/voltagent-best-practices](https://github.com/VoltAgent/skills/tree/main/skills/voltagent-best-practices)** — Architecture and usage patterns for agents, workflows, memory, and servers
  <sub>MIT · in-repo · pushed 2026-01-27</sub>
  <sub>`git clone https://github.com/VoltAgent/skills.git && cd skills/skills/voltagent-best-practices`</sub>
- **[voltagent/voltagent-core-reference](https://github.com/VoltAgent/skills/tree/main/skills/voltagent-core-reference)** — Reference for the VoltAgent class options and lifecycle methods
  <sub>MIT · in-repo · pushed 2026-01-27</sub>
  <sub>`git clone https://github.com/VoltAgent/skills.git && cd skills/skills/voltagent-core-reference`</sub>
- **[voltagent/voltagent-docs-bundle](https://github.com/VoltAgent/skills/tree/main/skills/voltagent-docs-bundle)** — Lookup embedded docs from @voltagent/core for version-matched documentation
  <sub>MIT · in-repo · pushed 2026-01-27</sub>
  <sub>`git clone https://github.com/VoltAgent/skills.git && cd skills/skills/voltagent-docs-bundle`</sub>
- **[callstackincubator/react-native-best-practices](https://github.com/callstackincubator/agent-skills/tree/main/skills/react-native-best-practices)** — Performance optimization for React Native apps
  <sub>Shell · MIT · in-repo · pushed 2026-10-08</sub>
  <sub>`git clone https://github.com/callstackincubator/agent-skills.git && cd agent-skills/skills/react-native-best-practices`</sub>
- **[callstackincubator/upgrading-react-native](https://github.com/callstackincubator/agent-skills/tree/main/skills/upgrading-react-native)** — React Native upgrade workflow: templates, dependencies, and pitfalls
  <sub>Shell · MIT · in-repo · pushed 2026-10-08</sub>
  <sub>`git clone https://github.com/callstackincubator/agent-skills.git && cd agent-skills/skills/upgrading-react-native`</sub>
- **[expo/building-native-ui](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-native-ui)** — Build apps with Expo Router, styling, components, and animations
  <sub>Shell · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/expo/skills.git && cd skills/plugins/expo/skills/expo-native-ui`</sub>
- **[expo/expo-api-routes](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-router)** — Create API routes in Expo Router with EAS Hosting
  <sub>Shell · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/expo/skills.git && cd skills/plugins/expo/skills/expo-router`</sub>
- **[expo/expo-deployment](https://github.com/expo/skills/tree/main/plugins/expo/skills/eas-hosting)** — Deploy Expo apps to production
  <sub>Shell · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/expo/skills.git && cd skills/plugins/expo/skills/eas-hosting`</sub>
- **[expo/upgrading-expo](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-upgrade)** — Upgrade Expo SDK versions
  <sub>Shell · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/expo/skills.git && cd skills/plugins/expo/skills/expo-upgrade`</sub>
- **[expo/use-dom](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-dom)** — Run web code in a webview on native using DOM components
  <sub>Shell · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/expo/skills.git && cd skills/plugins/expo/skills/expo-dom`</sub>
- **[duckdb/attach-db](https://github.com/duckdb/duckdb-skills/tree/main/skills/attach-db)** — Attach a DuckDB database file for interactive querying
  <sub>Shell · MIT · in-repo · pushed 2026-04-23</sub>
  <sub>`git clone https://github.com/duckdb/duckdb-skills.git && cd duckdb-skills/skills/attach-db`</sub>
- **[duckdb/query](https://github.com/duckdb/duckdb-skills/tree/main/skills/query)** — Run SQL queries against attached databases or ad-hoc files
  <sub>Shell · MIT · in-repo · pushed 2026-04-23</sub>
  <sub>`git clone https://github.com/duckdb/duckdb-skills.git && cd duckdb-skills/skills/query`</sub>
- **[duckdb/duckdb-docs](https://github.com/duckdb/duckdb-skills/tree/main/skills/duckdb-docs)** — Search DuckDB and DuckLake documentation
  <sub>Shell · MIT · in-repo · pushed 2026-04-23</sub>
  <sub>`git clone https://github.com/duckdb/duckdb-skills.git && cd duckdb-skills/skills/duckdb-docs`</sub>
- **[greensock/gsap-core](https://github.com/greensock/gsap-skills/tree/main/skills/gsap-core)** — Core API: gsap.to(), from(), fromTo(), easing, duration, stagger
  <sub>MIT · in-repo · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/greensock/gsap-skills.git && cd gsap-skills/skills/gsap-core`</sub>
- **[greensock/gsap-scrolltrigger](https://github.com/greensock/gsap-skills/tree/main/skills/gsap-scrolltrigger)** — ScrollTrigger for scroll-linked animations and pinning
  <sub>MIT · in-repo · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/greensock/gsap-skills.git && cd gsap-skills/skills/gsap-scrolltrigger`</sub>
- **[greensock/gsap-react](https://github.com/greensock/gsap-skills/tree/main/skills/gsap-react)** — React integration with useGSAP hook and SSR patterns
  <sub>MIT · in-repo · pushed 2026-07-29</sub>
  <sub>`git clone https://github.com/greensock/gsap-skills.git && cd gsap-skills/skills/gsap-react`</sub>
- **[WordPress/wp-block-development](https://github.com/WordPress/agent-skills/tree/trunk/skills/wp-block-development)** — Gutenberg blocks: block.json, attributes, rendering
  <sub>JavaScript · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/WordPress/agent-skills.git && cd agent-skills/skills/wp-block-development`</sub>
- **[WordPress/wp-plugin-development](https://github.com/WordPress/agent-skills/tree/trunk/skills/wp-plugin-development)** — Plugin architecture, hooks, settings API, security
  <sub>JavaScript · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/WordPress/agent-skills.git && cd agent-skills/skills/wp-plugin-development`</sub>
- **[WordPress/wp-playground](https://github.com/WordPress/agent-skills/tree/trunk/skills/wp-playground)** — WordPress Playground for instant local environments
  <sub>JavaScript · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/WordPress/agent-skills.git && cd agent-skills/skills/wp-playground`</sub>
- **[figma/figma-generate-library](https://github.com/figma/mcp-server-guide/tree/main/skills/figma-generate-library)** — Build or update a design system library in Figma from a codebase
  <sub>Python · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/figma/mcp-server-guide.git && cd mcp-server-guide/skills/figma-generate-library`</sub>
- **[figma/figma-use](https://github.com/figma/mcp-server-guide/tree/main/skills/figma-use)** — Run Figma Plugin API scripts for canvas writes and inspections
  <sub>Python · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/figma/mcp-server-guide.git && cd mcp-server-guide/skills/figma-use`</sub>

## GitHub Copilot

- **[About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)** — GitHub documentation
  <sub>website</sub>
  <sub>`https://docs.github.com/copilot/concepts/agents/about-agent-skills`</sub>
- **[VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)** — VS Code integration
  <sub>website</sub>
  <sub>`https://code.visualstudio.com/docs/copilot/customization/agent-skills`</sub>

## Security &amp; Web Intelligence

- **[trailofbits/building-secure-contracts](https://github.com/trailofbits/skills)** — Smart contract security toolkit for 6 blockchains
  <sub>★ 7.7k · Python · CC-BY-SA-4.0 · source · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trailofbits/skills.git`</sub>
- **[microsoft/skills](https://github.com/microsoft/skills)** — Full official Microsoft agent skills collection
  <sub>★ 3.1k · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add microsoft/skills`</sub>
- **[getsentry/skills](https://github.com/getsentry/skills)** — Full collection: debug errors, performance issues, and traces with Sentry
  <sub>★ 1.1k · Python · Apache-2.0 · npx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add getsentry/skills`</sub>
- **[firecrawl/firecrawl-browser](https://github.com/firecrawl/cli)** — Browser-based web scraping and interaction
  <sub>★ 660 · TypeScript · npm · pushed 2026-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g firecrawl-cli`</sub>
- **[trailofbits/audit-context-building](https://github.com/trailofbits/skills/tree/main/plugins/audit-context-building/skills/audit-context-building)** — Deep architectural context via granular code analysis
  <sub>Python · CC-BY-SA-4.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/trailofbits/skills.git && cd skills/plugins/audit-context-building/skills/audit-context-building`</sub>
- **[trailofbits/modern-python](https://github.com/trailofbits/skills/tree/main/plugins/modern-python/skills/modern-python)** — Modern Python tooling with uv, ruff, and pytest
  <sub>Python · CC-BY-SA-4.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/trailofbits/skills.git && cd skills/plugins/modern-python/skills/modern-python`</sub>
- **[getsentry/agents-md](https://github.com/getsentry/skills/tree/main/skills/agents-md)** — Generate and manage AGENTS.md files
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/getsentry/skills.git && cd skills/skills/agents-md`</sub>
- **[getsentry/code-review](https://github.com/getsentry/skills/tree/main/skills/code-review)** — Perform structured code reviews
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/getsentry/skills.git && cd skills/skills/code-review`</sub>
- **[getsentry/find-bugs](https://github.com/getsentry/skills/tree/main/skills/find-bugs)** — Find and identify bugs in code
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/getsentry/skills.git && cd skills/skills/find-bugs`</sub>
- **[firecrawl/firecrawl-cli](https://github.com/firecrawl/cli/tree/main/skills/firecrawl)** — Scrape, crawl, search, and map the web via CLI
  <sub>TypeScript · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/firecrawl/cli.git && cd cli/skills/firecrawl`</sub>
- **[firecrawl/firecrawl-agent](https://github.com/firecrawl/cli/tree/main/skills/firecrawl-agent)** — AI agent for autonomous web scraping
  <sub>TypeScript · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/firecrawl/cli.git && cd cli/skills/firecrawl-agent`</sub>
- **[firecrawl/firecrawl-scrape](https://github.com/firecrawl/cli/tree/main/skills/firecrawl-scrape)** — Scrape web pages and extract content
  <sub>TypeScript · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/firecrawl/cli.git && cd cli/skills/firecrawl-scrape`</sub>
- **[firecrawl/firecrawl-search](https://github.com/firecrawl/cli/tree/main/skills/firecrawl-search)** — Search the web and extract results
  <sub>TypeScript · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/firecrawl/cli.git && cd cli/skills/firecrawl-search`</sub>
- **[microsoft/cloud-solution-architect](https://github.com/microsoft/skills/tree/main/.github/skills/cloud-solution-architect)** — Design well-architected Azure cloud systems
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/microsoft/skills.git && cd skills/.github/skills/cloud-solution-architect`</sub>
- **[microsoft/copilot-sdk](https://github.com/microsoft/skills/tree/main/.github/skills/copilot-sdk)** — Build applications powered by GitHub Copilot SDK
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/microsoft/skills.git && cd skills/.github/skills/copilot-sdk`</sub>
- **[microsoft/azure-ai-openai-dotnet](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-ai-openai-dotnet)** — GPT-4, embeddings, and DALL-E client for .NET
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/microsoft/skills.git && cd skills/.github/plugins/azure-sdk-dotnet/skills/azure-ai-openai-dotnet`</sub>
- **[microsoft/azure-ai-projects-python](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-ai-projects-py)** — AI Foundry project client and agents for Python
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/microsoft/skills.git && cd skills/.github/plugins/azure-sdk-python/skills/azure-ai-projects-py`</sub>
- **[microsoft/azure-identity-typescript](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-identity-ts)** — Microsoft Entra ID authentication for TypeScript
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/microsoft/skills.git && cd skills/.github/plugins/azure-sdk-typescript/skills/azure-identity-ts`</sub>
- **[binance/crypto-market-rank](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/crypto-market-rank)** — Query crypto market rankings and leaderboards
  <sub>Python · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/binance/binance-skills-hub.git && cd binance-skills-hub/skills/binance-web3/crypto-market-rank`</sub>
- **[binance/query-token-audit](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/query-token-audit)** — Audit token security to detect scams and honeypots
  <sub>Python · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/binance/binance-skills-hub.git && cd binance-skills-hub/skills/binance-web3/query-token-audit`</sub>
- **[binance/trading-signal](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/trading-signal)** — Monitor on-chain Smart Money buy/sell signals
  <sub>Python · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/binance/binance-skills-hub.git && cd binance-skills-hub/skills/binance-web3/trading-signal`</sub>

## Community Skills

- **[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)** — High-agency frontend skill to eliminate generic UI slop
  <sub>★ 100.6k · JavaScript · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"`</sub>
- **[ComposioHQ/composio](https://github.com/ComposioHQ/composio)** — Connect AI agents to 1000+ external apps with managed authentication
  <sub>★ 30.7k · TypeScript · MIT · pip · pushed 2026-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install composio composio-openai-agents openai-agents`</sub>
- **[AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)** — Universal SEO skill for website analysis
  <sub>★ 19.6k · Python · MIT · script · pushed 2026-10-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/uninstall.sh | bash`</sub>
- **[SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser)** — Web browser capability for agents
  <sub>★ 6.7k · TypeScript · MIT · npm · pushed 2026-10-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g dev-browser`</sub>
- **[browser-act/skills](https://github.com/browser-act/skills)** — 22 browser automation skills for structured data extraction
  <sub>★ 6.2k · Python · MIT · source · pushed 2026-08-24 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/browser-act/skills.git`</sub>
- **[sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills)** — Social media marketing skills for 7 platforms: corpus-validated hooks, humanizer, audience insights
  <sub>★ 5k · Python · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add sergebulaev/linkedin-skills`</sub>
- **[lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill)** — Browser automation for testing web apps
  <sub>★ 3.2k · JavaScript · MIT · npx · pushed 2026-10-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add lackeyjb/playwright-skill --skill playwright-skill --global --yes`</sub>
- **[RoundTable02/tutor-skills](https://github.com/bevibing/tutor-skills)** — Transform docs or codebases into interactive StudyVaults
  <sub>★ 1.4k · Shell · MIT · npx · pushed 2026-02-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add RoundTable02/tutor-skills`</sub>
- **[conorluddy/ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill)** — Interact with iOS Simulator for testing
  <sub>★ 1.3k · Python · MIT · clone · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/conorluddy/ios-simulator-skill.git`</sub>
- **[chubbyguan/chubbyskills](https://github.com/chubbyguan/chubbyskills)** — 14 skills for ingesting Chinese content (Douyin, Bilibili, Xiaohongshu, WeChat, X/Twitter, podcasts) into a personal knowledge base — auto image/video routing, subtitle-first transcription, RSS/YouTube subscription scheduling, and a knowledge-base MCP server
  <sub>★ 1.3k · Python · MIT · pipx · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install git+https://github.com/chubbyguan/chubbyskills.git`</sub>
- **[gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills)** — 125 growth/GTM skills for ads, lead gen, outreach, and SEO
  <sub>★ 1.3k · JavaScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx gooseworks@latest install --claude --mcp # or --cursor --mcp, --codex --mcp`</sub>
- **[MoizIbnYousaf/ai-agent-skills](https://github.com/MoizIbnYousaf/ai-agent-skills)** — SkillCreator.ai collection with CLI installer
  <sub>★ 1.2k · JavaScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx ai-agent-skills install install-from-remote-library`</sub>
- **[ZeroPointRepo/youtube-skills](https://github.com/ZeroPointRepo/youtube-skills)** — YouTube transcripts, search, channel data, and playlists via TranscriptAPI. Works anywhere
  <sub>★ 1.1k · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx clawhub@latest install youtube-full`</sub>
- **[vostride/agent-qa](https://github.com/vostride/agent-qa)** — Three skills for authoring natural-language web and mobile tests, triaging failures, and debugging fixes with MCP evidence
  <sub>★ 914 · TypeScript · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-qa init`</sub>
- **[mhattingpete/claude-skills-marketplace](https://github.com/mhattingpete/claude-skills-marketplace)** — Digital forensics analysis and investigation
  <sub>★ 687 · HTML · Apache-2.0 · source · pushed 2026-07-25</sub>
  <sub>`git clone https://github.com/mhattingpete/claude-skills-marketplace.git`</sub>
- **[Qiuner/birdview](https://github.com/Qiuner/birdview)** — Treat architecture and constraints as the enduring work of programming, with reviewable scope, evidence, and verification in standalone HTML
  <sub>★ 668 · TypeScript · MIT · npx · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Qiuner/birdview --skill birdview`</sub>
- **[karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills)** — 50+ verified skills for Claude Code and Claude.ai
  <sub>★ 555 · MIT · source · pushed 2026-10-02</sub>
  <sub>`git clone https://github.com/karanb192/awesome-claude-skills.git`</sub>
- **[NoizAI/skills](https://github.com/NoizAI/skills)** — Human-like TTS skills with tested speaking styles, emotional tone, and local or cloud voice backends
  <sub>★ 530 · Python · npx · pushed 2026-09-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add`</sub>
- **[coffeefuelbump/csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill)** — Analyze CSV files and generate insights with visualizations
  <sub>★ 475 · Python · clone · pushed 2025-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:coffeefuelbump/csv-data-summarizer-claude-skill.git`</sub>
- **[BrianRWagner/ai-marketing-skills](https://github.com/BrianRWagner/ai-marketing-claude-code-skills)** — 17 marketing frameworks for outreach and audits
  <sub>★ 445 · Shell · clone · pushed 2026-03-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/BrianRWagner/ai-marketing-claude-code-skills.git`</sub>
- **[sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills)** — Google Workspace (Gmail, Chat, Calendar, Docs, Drive, Sheets, Slides), AI delegation (Jules, Manus, Deep Research), and database skills
  <sub>★ 441 · Python · Apache-2.0 · npx · pushed 2026-09-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add sanjay3290/ai-skills --list`</sub>
- **[gotalab/skillport](https://github.com/gotalab/skillport)** — Skills distribution via CLI or MCP
  <sub>★ 415 · Python · MIT · uv · pushed 2026-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install skillport`</sub>
- **[DougTrajano/pydantic-ai-skills](https://github.com/DougTrajano/pydantic-ai-skills)** — Pydantic AI integration
  <sub>★ 380 · Python · MIT · pip · pushed 2026-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pydantic-ai-skills`</sub>
- **[zxkane/aws-skills](https://github.com/zxkane/aws-skills)** — AWS development with CDK best practices
  <sub>★ 370 · Python · MIT · npx · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/zxkane/aws-skills --skill aws-cdk-development`</sub>
- **[danjdewhurst/story-skills](https://github.com/danjdewhurst/story-skills)** — 16 skills for planning, tracking, and drafting fiction in markdown (worldbuilding, characters, plot, scenes, chapters, revision, continuity), plus a CLI that checks continuity
  <sub>★ 338 · JavaScript · MIT · npm · pushed 2026-10-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g story-skills # then: story --help (Windows too)`</sub>
- **[ohad6k/ditto](https://github.com/ohad6k/emulo)** — Mine Claude Code and Codex session logs into local, evidence-backed agent profiles
  <sub>★ 298 · HTML · MIT · npx · pushed 2026-10-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add ohad6k/emulo@emulo`</sub>
- **[talkstream/ru-text](https://github.com/talkstream/ru-text)** — Russian text quality: ~1,040 rules for typography, info-style, editorial, UX writing, business correspondence
  <sub>★ 276 · Shell · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add talkstream/ru-text`</sub>
- **[smixs/creative-director-skill](https://github.com/smixs/creative-director-skill)** — 20+ creative methodologies (SIT, TRIZ, SCAMPER)
  <sub>★ 271 · Python · CC-BY-4.0 · npx · pushed 2026-08-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add smixs/creative-director-skill # asks where to install`</sub>
- **[qdrant/skills](https://github.com/qdrant/skills)** — Agent skills for Qdrant vector search, scaling, and performance
  <sub>★ 260 · Python · Apache-2.0 · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add qdrant/skills/meta/qdrant-advisor`</sub>
- **[qualixar/superlocalmemory](https://github.com/qualixar/superlocalmemory)** — Local-first persistent memory for coding agents via MCP, with governed recall
  <sub>★ 254 · Python · AGPL-3.0 · npm · pushed 2026-10-20 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g superlocalmemory # add --media to also turn on pictures and documents`</sub>
- **[chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill)** — D3 charts and interactive data visualizations
  <sub>★ 246 · JavaScript · source · pushed 2025-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chrisvoncsefalvay/claude-d3js-skill.git`</sub>
- **[Evol-ai/SkillCompass](https://github.com/Evol-ai/SkillCompass)** — Local-first skill quality evaluator scoring 6 dimensions with fix suggestions and version tracking
  <sub>★ 215 · JavaScript · MIT · npx · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Evol-ai/SkillCompass`</sub>
- **[coderabbitai/skills](https://github.com/coderabbitai/skills)** — Code review and PR autofix workflows
  <sub>★ 194 · TypeScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add coderabbitai/skills`</sub>
- **[gapmiss/obsidian-plugin-skill](https://github.com/gapmiss/obsidian-plugin-skill)** — Obsidian.md plugin development
  <sub>★ 193 · JavaScript · MIT · npx · pushed 2026-10-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add https://github.com/gapmiss/obsidian-plugin-skill --skill obsidian`</sub>
- **[Digidai/product-manager-skills](https://github.com/Digidai/product-manager-skills)** — PM operator skill across 12 domains: discovery, PRDs, SaaS metrics, pricing, launch, and stakeholder comms
  <sub>★ 191 · Shell · npx · pushed 2026-04-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Digidai/product-manager-skills`</sub>
- **[makenotion/skills](https://github.com/makenotion/skills)** — Notion API integration, database operations, and content management
  <sub>★ 175 · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add makenotion/skills`</sub>
- **[smerchek/claude-epub-skill](https://github.com/smerchek/claude-epub-skill)** — Converts markdown documents into professional EPUB ebook files
  <sub>★ 168 · Python · MIT · source · pushed 2025-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/smerchek/claude-epub-skill.git`</sub>
- **[vaibhavarora14/job-application-agent](https://github.com/vaibhavarora14/job-application-agent)** — Privacy-first skill to discover, qualify, complete, and track your own job applications
  <sub>★ 161 · JavaScript · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx job-application-agent@latest install`</sub>
- **[MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop)** — MCP server and CLI skill that removes named AI writing patterns: tricolons, em-dash overuse, hedging stacks, sycophancy openers, and overused vocab. Lint-only audit mode, five intensity levels
  <sub>★ 161 · Python · MIT · pipx · pushed 2026-10-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install unslop`</sub>
- **[mblode/agent-skills](https://github.com/mblode/agent-skills)** — 26 skills for UI audits, typography, docs, PR review, and releases
  <sub>★ 151 · Python · MIT · npx · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add mblode/agent-skills -g --agent codex claude-code -y`</sub>
- **[Alisa0808/vibe-creating-skill](https://github.com/Alisa0808/vibe-creating-skill)** — Rewrite rough ideas into model-ready text-to-video prompts (Seedance, Sora, Kling, Veo); bilingual EN/中文
  <sub>★ 150 · JavaScript · npx · pushed 2026-06-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx github:Alisa0808/vibe-creating-skill`</sub>
- **[kubestellar/console](https://github.com/kubestellar/console)** — Multi-cluster Kubernetes dashboard with 10+ built-in agent skills for performance testing, cache compliance, CI debugging, and K8s troubleshooting. MCP server bridges agents to kubeconfig and Kubernetes APIs
  <sub>★ 148 · TypeScript · Apache-2.0 · script · pushed 2026-10-21 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/kubestellar/console/main/start.sh | bash`</sub>
- **[aaddrick/building-with-typesafe-jev](https://github.com/aaddrick/building-with-typesafe-jev)** — Design TypeSafe Jev calls: typed questions, confidence routing, 150+ prior-art projects
  <sub>★ 144 · Python · MIT · script · pushed 2026-10-01 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/aaddrick/building-with-typesafe-jev/main/scripts/install_muse.sh | bash`</sub>
- **[wrsmith108/linear-claude-skill](https://github.com/wrsmith108/linear-claude-skill)** — Manage Linear issues, projects, and teams
  <sub>★ 135 · TypeScript · MIT · clone · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wrsmith108/linear-claude-skill`</sub>
- **[Vladimir-Human/humanizer-ru](https://github.com/Vladimir-Human/humanizer-ru)** — Russian AI-writing cleanup with 38 style patterns and 35 regex markers
  <sub>★ 129 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Vladimir-Human/humanizer-ru`</sub>
- **[aaddrick/attention-control](https://github.com/aaddrick/attention-control)** — Air traffic control discipline for coding-agent output, tuned for ADHD reading
  <sub>★ 126 · Python · MIT · source · pushed 2026-08-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aaddrick/attention-control.git`</sub>
- **[OmidZamani/dspy-skills](https://github.com/OmidZamani/dspy-skills)** — Skills for DSPy framework
  <sub>★ 124 · Python · MIT · source · pushed 2026-06-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OmidZamani/dspy-skills.git`</sub>
- **[ameyalambat128/swiftui-skills](https://github.com/ameyalambat128/swiftui-skills)** — Apple-authored SwiftUI and platform guidance extracted from Xcode
  <sub>★ 123 · TypeScript · MIT · npx · pushed 2026-07-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add ameyalambat128/swiftui-skills`</sub>
- **[glacierphonk/naming](https://github.com/glacierphonk/naming)** — Metaphor-driven naming for products, SaaS, brands, and open source projects
  <sub>★ 119 · Shell · MIT · clone · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/glacierphonk/naming.git`</sub>
- **[cognyai/claude-code-marketing-skills](https://github.com/cognyai/claude-code-marketing-skills)** — AI marketing skills: SEO Audit, Landing Page Review, Competitor Analysis, Ad Copy Writer, Lead Qualification. 5 free skills + premium via Cogny MCP
  <sub>★ 107 · HTML · script · pushed 2026-10-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/cognyai/claude-code-marketing-skills/main/install.sh | bash`</sub>
- **[shepsci/kaggle-skill](https://github.com/shepsci/kaggle-skill)** — Complete Kaggle integration — competition reports, dataset downloads, submissions
  <sub>★ 104 · Python · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add shepsci/kaggle-skill`</sub>
- **[xianyu110/ecommerce-image-skills](https://github.com/xianyu110/ecommerce-image-skills)** — 12 skills for ecommerce product images (Amazon main image, A+, banners)
  <sub>★ 103 · Python · MIT · npx · pushed 2026-10-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add xianyu110/ecommerce-image-skills`</sub>
- **[frmoretto/stream-coding](https://github.com/frmoretto/stream-coding)** — Stream Coding methodology
  <sub>★ 96 · clone · pushed 2026-02-26</sub>
  <sub>`git clone https://github.com/frmoretto/stream-coding`</sub>
- **[sametcelikbicak/rolecraft](https://github.com/rolecraft-sh/rolecraft)** — Zero-dependency CLI to install AI agent skills as roles &amp; behaviors from any source. Works with opencode, claude-code, cursor, and all spec-compliant agents
  <sub>★ 95 · JavaScript · MIT · npm · pushed 2026-10-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g rolecraft`</sub>
- **[xianyu110/ecommerce-video-skills](https://github.com/xianyu110/ecommerce-video-skills)** — 12 skills for ecommerce short videos with local ffmpeg rendering
  <sub>★ 92 · Python · MIT · npx · pushed 2026-10-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add xianyu110/ecommerce-video-skills`</sub>
- **[tubeagentkit/youtube-transcript-skills](https://github.com/tubeagentkit/youtube-transcript-skills)** — Fetch YouTube transcripts, search videos/channels, browse channels, and extract playlists via getyoutubetranscript.com's free-tier API
  <sub>★ 82 · Shell · MIT · npx · pushed 2026-10-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add tubeagentkit/youtube-transcript-skills --skill youtube-transcript`</sub>
- **[chadboyda/agent-gtm-skills](https://github.com/chadboyda/agent-gtm-skills)** — 18 go-to-market skills: pricing, outbound, SEO, ads, retention, and ops
  <sub>★ 81 · HTML · npx · pushed 2026-02-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx add-skill chadboyda/agent-gtm-skills`</sub>
- **[eduardo-sl/go-agent-skills](https://github.com/eduardo-sl/go-agent-skills)** — 28 curated Go skills for code review, concurrency, testing, and architecture
  <sub>★ 80 · Shell · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add eduardo-sl/go-agent-skills`</sub>
- **[muthuishere/hand-drawn-diagrams](https://github.com/muthuishere/hand-drawn-diagrams)** — Generate hand-drawn Excalidraw diagrams from prompt
  <sub>★ 79 · Python · npx · pushed 2026-09-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add muthuishere/hand-drawn-diagrams`</sub>
- **[gmickel/sheets-cli](https://github.com/gmickel/sheets-cli)** — Google Sheets CLI automation
  <sub>★ 70 · Python · clone · pushed 2026-02-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gmickel/sheets-cli.git`</sub>
- **[k-kolomeitsev/data-structure-protocol](https://github.com/k-kolomeitsev/data-structure-protocol)** — Graph-based memory for faster context and safer refactors
  <sub>★ 68 · Python · Apache-2.0 · psh · pushed 2026-08-10 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/k-kolomeitsev/data-structure-protocol/main/install.ps1 | iex`</sub>
- **[LeadMagic/gtm-skills](https://github.com/LeadMagic/gtm-skills)** — 189+ GTM playbooks for AI agents covering marketing, sales, customer success, and revenue operations across 26 categories. Compatible with Claude Code, Codex, Cursor, GitHub Copilot, and 12+ agent platforms. Website
  <sub>★ 66 · Python · MIT · source · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/LeadMagic/gtm-skills.git`</sub>
- **[salespeak-ai/buyer-eval-skill](https://github.com/salespeak-ai/buyer-eval-skill)** — B2B vendor evaluation skill: 7-dimension scoring with evidence-tracked scorecards for procurement and build-vs-buy decisions
  <sub>★ 66 · Python · MIT · clone · pushed 2026-09-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/salespeak-ai/buyer-eval-skill.git`</sub>
- **[yzfly/Mind-Cloning-Engineering](https://github.com/yzfly/Mind-Cloning-Engineering)** — Mind cloning with LLM skills
  <sub>★ 61 · Apache-2.0 · clone · pushed 2025-12-21</sub>
  <sub>`git clone https://github.com/yzfly/Mind-Cloning-Engineering.git`</sub>
- **[SHADOWPR0/beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose)** — Hard-edged writing style contract for forceful English prose
  <sub>★ 58 · source · pushed 2025-12-30</sub>
  <sub>`git clone https://github.com/SHADOWPR0/beautiful_prose.git`</sub>
- **[hanfang/claude-memory-skill](https://github.com/hanfang/claude-memory-skill)** — Hierarchical memory system with filesystem persistence
  <sub>★ 57 · Shell · MIT · script · pushed 2026-02-07 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/hanfang/claude-memory-skill/main/install.sh | bash`</sub>
- **[kylehughes/the-unofficial-swift-concurrency-migration-skill](https://github.com/kylehughes/the-unofficial-swift-concurrency-migration-skill)** — Swift Concurrency Migration guide
  <sub>★ 57 · Python · MIT · source · pushed 2025-12-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kylehughes/the-unofficial-swift-concurrency-migration-skill.git`</sub>
- **[jakedahn/pomodoro](https://github.com/jakedahn/pomodoro)** — System Skill Pattern — skills that remember and improve
  <sub>★ 56 · TypeScript · MIT · source · pushed 2025-10-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jakedahn/pomodoro.git`</sub>
- **[wgwtest/novel-writing](https://github.com/wgwtest/novel-writing)** — Codex skill for fiction planning, drafting, and revision with viewpoint, scene-causality, dialogue, and style-preservation checks
  <sub>★ 52 · Python · MIT · npx · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/wgwtest/novel-writing --skill novel-writing`</sub>
- **[massimodeluisa/recursive-decomposition-skill](https://github.com/massimodeluisa/recursive-decomposition-skill)** — Handle long-context tasks (100+ files) via decomposition
  <sub>★ 52 · HTML · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add massimodeluisa/recursive-decomposition-skill`</sub>
- **[fcavalcantirj/claude-code-eyes](https://github.com/fcavalcantirj/claude-code-eyes)** — Camera vision for Claude Code — see hardware, screens and wiring to verify physical output
  <sub>★ 51 · Shell · MIT · clone · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fcavalcantirj/claude-code-eyes.git`</sub>
- **[smorky850612/AuraKit](https://github.com/smorky850612/Aurakit)** — Full dev lifecycle skill for Claude Code: 46 modes (BUILD/FIX/DEPLOY/REVIEW/TDD/QA/DEBUG), 23 sub-agents, 6-layer OWASP+ security, ~55% token savings via Tiered Model routing
  <sub>★ 43 · JavaScript · MIT · npx · pushed 2026-04-16 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx @smorky85/aurakit # Install once (~30 seconds, auto-installs jq)`</sub>
- **[honeydew-ai/honeydew-ai-coding-agents-plugins](https://github.com/honeydew-ai/honeydew-ai-coding-agents-plugins)** — 11 skills + MCP server for building and querying a governed semantic layer over Snowflake, Databricks, and BigQuery from coding agents (Claude Code, Codex, Cursor, Copilot CLI, Gemini CLI). Same trusted model serves BI tools and AI agents. Plugins are Apache 2.0
  <sub>★ 42 · Shell · Apache-2.0 · source · pushed 2026-08-30</sub>
  <sub>`git clone https://github.com/honeydew-ai/honeydew-ai-coding-agents-plugins.git`</sub>
- **[backblaze-labs/claude-skill-b2-cloud-storage](https://github.com/backblaze-labs/claude-skill-b2-cloud-storage)** — Manage Backblaze B2 storage: list, audit, cleanup, security, lifecycle
  <sub>★ 42 · Python · MIT · npx · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add backblaze-labs/claude-skill-b2-cloud-storage -g # global`</sub>
- **[0xheycat/isometric-game-skills](https://github.com/0xheycat/isometric-game-skills)** — 20 agent-ready skills for isometric game dev: ComfyUI art pipeline, terrain, sprites, renderer, pathfinding, and more
  <sub>★ 38 · Python · MIT · clone · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/0xheycat/isometric-game-skills.git`</sub>
- **[YujxZJCN/teaching-skills](https://github.com/YujxZJCN/teaching-skills)** — University teaching lifecycle for professors: course design, lessons, exams, grading (Codex: YujxZJCN/teaching-skills-codex)
  <sub>★ 38 · Python · MIT · source · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YujxZJCN/teaching-skills.git`</sub>
- **[Shilo/pixellab-pip](https://github.com/Shilo/pixellab-pip)** — Route PixelLab MCP/REST to generate, edit, and animate pixel art
  <sub>★ 37 · Python · MIT · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Shilo/pixellab-pip --skill pixellab-pip`</sub>
- **[kukapay/crypto-skills](https://github.com/kukapay/crypto-skills)** — Cryptocurrency, web3 and blockchain skills
  <sub>★ 37 · Python · MIT · npx · pushed 2026-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add kukapay/crypto-skills`</sub>
- **[lukstei/slop-grader](https://github.com/lukstei/slop-grader)** — Rule-based CLI tool evaluating custom rulesets to guide auto-fixing with an AI agent
  <sub>★ 35 · TypeScript · MIT · npx · pushed 2026-10-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @lukstei/slop-grader@latest -r no-ai-slop examples/slop.md`</sub>
- **[fockus/skill-memory-bank](https://github.com/fockus/skill-memory-bank)** — Cross-agent long-term project memory via .memory-bank/ for Claude Code, Cursor, Windsurf, Cline, Kilo, OpenCode, Pi Code, Codex — bundles TDD / SOLID / Clean Architecture / FSD rules and 18 dev-toolkit commands
  <sub>★ 29 · Shell · MIT · npx · pushed 2026-10-18 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx skills add fockus/skill-memory-bank`</sub>
- **[uxuiprinciples/agent-skills](https://github.com/uxuiprinciples/agent-skills)** — 5 UX/UI skills: evaluate interfaces against 168 research-backed principles
  <sub>★ 26 · source · pushed 2026-08-31</sub>
  <sub>`git clone https://github.com/uxuiprinciples/agent-skills.git`</sub>
- **[ckanner/agent-skills](https://github.com/ckanner/agent-skills)** — Curated Claude Agent Skills collection
  <sub>★ 23 · Shell · Apache-2.0 · clone · pushed 2026-10-03</sub>
  <sub>`git clone https://github.com/hikanner/agent-skills.git`</sub>
- **[knot0-com/vibe-testing](https://github.com/knot0-com/vibe-testing)** — Pressure-test spec documents with LLM reasoning before writing code
  <sub>★ 22 · MIT · clone · pushed 2026-03-22</sub>
  <sub>`git clone https://github.com/knot0-com/vibe-testing.git`</sub>
- **[PSPDFKit-labs/nutrient-agent-skill](https://github.com/PSPDFKit-labs/nutrient-agent-skill)** — Document processing: convert, OCR, and redact PII
  <sub>★ 18 · Python · npx · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add PSPDFKit-labs/nutrient-agent-skill`</sub>
- **[fabioc-aloha/spotify-skill](https://github.com/fabioc-aloha/spotify-skill)** — Spotify API integration
  <sub>★ 18 · Python · Apache-2.0 · clone · pushed 2025-10-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YOUR-USERNAME/spotify-skill.git`</sub>
- **[caopulan/Notification-Skill](https://github.com/caopulan/Notification-Skill)** — Send message notifications for agent workflows
  <sub>★ 16 · Python · source · pushed 2026-01-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/caopulan/Notification-Skill.git`</sub>
- **[yshishenya/stitchflow](https://github.com/yshishenya/stitchflow)** — Stitch UI generation with local HTML and screenshots
  <sub>★ 13 · JavaScript · Apache-2.0 · clone · pushed 2026-05-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/yshishenya/stitchflow.git`</sub>
- **[RioTheGreat-ai/agentfund-skill](https://github.com/RioTheGreat-ai/agentfund-skill)** — Crowdfunding for AI agents on Base chain - milestone escrow
  <sub>★ 13 · Shell · source · pushed 2026-02-03</sub>
  <sub>`git clone https://github.com/RioTheGreat-ai/agentfund-skill.git`</sub>
- **[dadwadw233/claude-code-harness](https://github.com/dadwadw233/claude-code-harness)** — Harness blueprint skill for request assembly, control loops, memory boundaries, permissions, and recovery
  <sub>★ 12 · MIT · clone · pushed 2026-04-05</sub>
  <sub>`git clone git@github.com:dadwadw233/claude-code-harness.git`</sub>
- **[dragon1086/claude-skills](https://github.com/dragon1086/claude-skills)** — Analyzes prompts and recommends optimal tools, skills, agents, and orchestration patterns
  <sub>★ 12 · Shell · MIT · npx · pushed 2026-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add dragon1086/claude-skills -y --agent claude-code`</sub>
- **[rickygao/specrate](https://github.com/rickygao/specrate)** — Manage specs and changes in a structured workflow
  <sub>★ 8 · Apache-2.0 · source · pushed 2026-01-13</sub>
  <sub>`git clone https://github.com/rickygao/specrate.git`</sub>
- **[kybernetwork/kyberswap-skills](https://github.com/KyberNetwork/kyberswap-skills)** — Token swap quotes and transactions across 18 EVM chains
  <sub>★ 8 · Shell · npx · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add KyberNetwork/kyberswap-skills`</sub>
- **[dadwadw233/claude-code-philosophy](https://github.com/dadwadw233/claude-code-philosophy)** — Skill for reviewing and structuring agent products around harnesses, memory, permissions, recovery, and UX
  <sub>★ 6 · MIT · clone · pushed 2026-04-05</sub>
  <sub>`git clone git@github.com:dadwadw233/claude-code-philosophy.git`</sub>
- **[HeyVincent-ai/agent-skills](https://github.com/HeyVincent-ai/agent-skills)** — Polymarket prediction market trading for agents
  <sub>★ 5 · source · pushed 2026-03-09</sub>
  <sub>`git clone https://github.com/HeyVincent-ai/agent-skills.git`</sub>
- **[grittygrease/safe-encryption-skill](https://github.com/grittygrease/safe-encryption-skill)** — Modern encryption alternative to GPG/PGP with post-quantum support
  <sub>★ 4 · Apache-2.0 · npm · pushed 2026-02-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g safe-encryption # Node.js`</sub>
- **[c5huracan/meyhem](https://github.com/c5huracan/meyhem)** — Agent-native web search with feedback-driven ranking via REST API and MCP server
  <sub>★ 4 · Python · source · pushed 2026-03-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/c5huracan/meyhem.git`</sub>
- **[techgangboss/agentstore](https://github.com/techgangboss/agentstore)** — Open-source plugin marketplace with CLI install
  <sub>★ 4 · TypeScript · MIT · npm · pushed 2026-02-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agentstore`</sub>
- **[transloadit/skills](https://github.com/transloadit/skills)** — Media processing: video encoding, image manipulation, OCR
  <sub>★ 4 · TypeScript · npx · pushed 2026-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y skills add https://github.com/transloadit/skills --list`</sub>
- **[sametcelikbicak/coverage-guard](https://github.com/sametcelikbicak/coverage-guard)** — Enforces 100% test coverage for any JavaScript/TypeScript project. Works with Vitest, Jest, react-scripts, and more
  <sub>★ 3 · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rolecraft install sametcelikbicak/coverage-guard`</sub>
- **[sametcelikbicak/flaky-test-detector](https://github.com/sametcelikbicak/flaky-test-detector)** — Detects, analyzes, and eliminates flaky tests across any test runner
  <sub>★ 3 · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rolecraft install sametcelikbicak/flaky-test-detector`</sub>
- **[sametcelikbicak/task-decomposer](https://github.com/sametcelikbicak/task-decomposer)** — Decomposes complex requests into structured, AI-friendly task sequences
  <sub>★ 3 · MIT · npx · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx rolecraft install sametcelikbicak/task-decomposer`</sub>
- **[ChaosRealmsAI/agent-cli-spec](https://github.com/ChaosRealmsAI/agent-cli-spec)** — CLI design spec — 98 rules for building agent-safe CLI tools
  <sub>★ 3 · MIT · npx · pushed 2026-03-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add zhuanz/agent-cli-spec`</sub>
- **[AppDeploy-AI/skills](https://github.com/AppDeploy-AI/skills)** — Deploy apps with full stack and get a live URL back
  <sub>★ 2 · MIT · source · pushed 2026-08-02</sub>
  <sub>`git clone https://github.com/AppDeploy-AI/skills.git`</sub>
- **[commune-dev/commune-skill](https://github.com/commune-dev/commune-skill)** — Agent-native email inbox — permanent @commune.ai address with full send/receive, semantic search, triage, and webhooks
  <sub>★ 1 · Python · source · pushed 2026-06-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/commune-dev/commune-skill.git`</sub>
- **[cuongducle/community-demand-prospecting-skill](https://github.com/cuongducle/community-demand-prospecting-skill)** — Repo audit, market research, positioning, and community outreach planning
  <sub>★ 1 · npx · pushed 2026-03-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx clawhub install cuongducle/community-demand-prospecting`</sub>
- **[socai-io/jev-social](https://github.com/socai-io/jev-social/tree/main/skills/jev-social)** — Research social platforms through typed Jev actions in local Chrome
  <sub>JavaScript · MIT · in-repo · pushed 2026-10-12</sub>
  <sub>`git clone https://github.com/socai-io/jev-social.git && cd jev-social/skills/jev-social`</sub>
- **[Orkas-AI/video-router](https://github.com/Orkas-AI/Orkas-VideoStudio/tree/main/packages/skills/video-router)** — Route video requests through deterministic agent production stages
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-13</sub>
  <sub>`git clone https://github.com/Orkas-AI/Orkas-VideoStudio.git && cd Orkas-VideoStudio/packages/skills/video-router`</sub>
- **[anzy-renlab-ai/pronounce-word](https://github.com/anzy-renlab-ai/pronounce/tree/main/skills/pronounce-word)** — Play sourced developer-jargon pronunciations with local TTS, IPA, and contested alternatives
  <sub>Python · MIT · in-repo · pushed 2026-09-01</sub>
  <sub>`git clone https://github.com/anzy-renlab-ai/pronounce.git && cd pronounce/skills/pronounce-word`</sub>
- **[KKKKhazix/aihot](https://github.com/KKKKhazix/khazix-skills/tree/main/aihot)** — Query Chinese AI news, current topics, and daily briefs from AIHOT through anonymous read-only requests; retain dates and original-source links. Service terms apply separately from the MIT-licensed skill
  <sub>Python · MIT · in-repo · pushed 2026-10-01</sub>
  <sub>`git clone https://github.com/KKKKhazix/khazix-skills.git && cd khazix-skills/aihot`</sub>
- **[kranz-org/kranz-services](https://github.com/kranz-org/kranz/tree/main/skills/kranz-services)** — Inspect and control live development services through Kranz MCP
  <sub>Go · MIT · in-repo · pushed 2026-10-20</sub>
  <sub>`git clone https://github.com/kranz-org/kranz.git && cd kranz/skills/kranz-services`</sub>
- **[lmammino/c4-codebase-architecture](https://github.com/lmammino/c4-codebase-architecture-skill/tree/main/skills/c4-codebase-architecture)** — Generate evidence-based C4 architecture docs from codebases
  <sub>MIT · in-repo · pushed 2026-04-09</sub>
  <sub>`git clone https://github.com/lmammino/c4-codebase-architecture-skill.git && cd c4-codebase-architecture-skill/skills/c4-codebase-architecture`</sub>
- **[luoyuctl/agenttrace](https://github.com/luoyuctl/agenttrace/tree/master/skills/agenttrace-session-audit)** — Audit AI coding-agent session health and cost
  <sub>Rust · MIT · in-repo · pushed 2026-10-19</sub>
  <sub>`git clone https://github.com/luoyuctl/agenttrace.git && cd agenttrace/skills/agenttrace-session-audit`</sub>
- **[mcollina/skills](https://github.com/mcollina/skills/tree/main/skills)** — Node.js core, Fastify, and TypeScript skills by Matteo Collina
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-18</sub>
  <sub>`git clone https://github.com/mcollina/skills.git && cd skills/skills`</sub>
- **[swarmclawai/swarmclaw](https://github.com/swarmclawai/swarmclaw/tree/main/skills/swarmclaw)** — Operate self-hosted multi-agent runtime workflows
  <sub>TypeScript · MIT · in-repo · pushed 2026-06-30</sub>
  <sub>`git clone https://github.com/swarmclawai/swarmclaw.git && cd swarmclaw/skills/swarmclaw`</sub>
- **[swarmclawai/karpathy-guidelines](https://github.com/swarmclawai/andrej-karpathy-skills/tree/main/skills/karpathy-guidelines)** — Coding-agent guardrails for clarity, minimal diffs, and verification
  <sub>JavaScript · MIT · in-repo · pushed 2026-05-11</sub>
  <sub>`git clone https://github.com/swarmclawai/andrej-karpathy-skills.git && cd andrej-karpathy-skills/skills/karpathy-guidelines`</sub>
- **[linhay/harmony-next.skills](https://github.com/linhay/harmony-next.skills/tree/master/harmony-next)** — HarmonyOS NEXT workflows for AI coding agents
  <sub>Python · in-repo · pushed 2026-09-20</sub>
  <sub>`git clone https://github.com/linhay/harmony-next.skills.git && cd harmony-next.skills/harmony-next`</sub>
- **[sarveshsea/audit-frontend-design](https://github.com/sarveshsea/memi/tree/main/skills/audit-frontend-design)** — Audit frontend design debt before editing code
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/sarveshsea/memi.git && cd memi/skills/audit-frontend-design`</sub>
- **[mdrbx/nerv-ui](https://github.com/mdrbx/nerv-ui/tree/master/skills/nerv-ui)** — Typed React command-center components, live examples, and a portable Agent Skills-compatible skill
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-04</sub>
  <sub>`git clone https://github.com/mdrbx/nerv-ui.git && cd nerv-ui/skills/nerv-ui`</sub>
- **[Tencent/aig-agent-redteam](https://github.com/Tencent/AI-Infra-Guard/tree/main/skills/aig-agent-redteam)** — One-command Agent red-team security assessment
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/Tencent/AI-Infra-Guard.git && cd AI-Infra-Guard/skills/aig-agent-redteam`</sub>
- **[Continuum-AI-Corp/OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay/tree/main/skills/orca-replay)** — Read a recorded agent run from its trace, replay it offline, or fork it onto another model
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-10-01</sub>
  <sub>`git clone https://github.com/Continuum-AI-Corp/OrcaReplay.git && cd OrcaReplay/skills/orca-replay`</sub>
- **[unbrowse-ai/unbrowse](https://github.com/unbrowse-ai/unbrowse/tree/main/skill)** — Search, call, and read websites through a hosted API or MCP
  <sub>TypeScript · MIT · in-repo · pushed 2026-10-18</sub>
  <sub>`git clone https://github.com/unbrowse-ai/unbrowse.git && cd unbrowse/skill`</sub>
- **[umutbozdag/manage-skills](https://github.com/umutbozdag/agent-skills-manager/tree/main/skills/manage-skills)** — Discover, create, edit, toggle, copy, and move agent skills across 11 tools from the terminal
  <sub>TypeScript · MIT · in-repo · pushed 2026-04-09</sub>
  <sub>`git clone https://github.com/umutbozdag/agent-skills-manager.git && cd agent-skills-manager/skills/manage-skills`</sub>
- **[DrDroidLab/setup-open-index](https://github.com/DrDroidLab/open-index/blob/main/skills/setup-open-index/SKILL.md)** — Set up structured context graphs with hybrid search and read/write MCP access
  <sub>Python · MIT · in-repo · pushed 2026-08-12</sub>
  <sub>`git clone https://github.com/DrDroidLab/open-index.git && cd open-index/skills/setup-open-index/SKILL.md`</sub>
- **[muratcankoylan/context-compression](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/context-compression)** — Compression strategies for long-running sessions
  <sub>Python · MIT · in-repo · pushed 2026-10-12</sub>
  <sub>`git clone https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering.git && cd Agent-Skills-for-Context-Engineering/skills/context-compression`</sub>
- **[muratcankoylan/memory-systems](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/memory-systems)** — Design short-term and graph-based memory architectures
  <sub>Python · MIT · in-repo · pushed 2026-10-12</sub>
  <sub>`git clone https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering.git && cd Agent-Skills-for-Context-Engineering/skills/memory-systems`</sub>
- **[TerminallyLazy/tree-ring-memory](https://github.com/TerminallyLazy/Tree-Ring-Memory/tree/main/skills/tree-ring-memory)** — Lifecycle-aware local memory with recall, evidence, audit, and forgetting
  <sub>Rust · MIT · in-repo · pushed 2026-09-17</sub>
  <sub>`git clone https://github.com/TerminallyLazy/Tree-Ring-Memory.git && cd Tree-Ring-Memory/skills/tree-ring-memory`</sub>
- **[swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault/tree/main/skills/swarmvault)** — Build local knowledge vaults and context packs
  <sub>TypeScript · MIT · in-repo · pushed 2026-06-30</sub>
  <sub>`git clone https://github.com/swarmclawai/swarmvault.git && cd swarmvault/skills/swarmvault`</sub>
- **[Necmttn/ax-extract-workflow](https://github.com/Necmttn/ax/tree/main/skills/ax-extract-workflow)** — Reconstruct shipped workflows from local ax sessions, commits, skills, and subagent traces
  <sub>TypeScript · AGPL-3.0 · in-repo · pushed 2026-10-07</sub>
  <sub>`git clone https://github.com/Necmttn/ax.git && cd ax/skills/ax-extract-workflow`</sub>
- **[coinpaprika/coinpaprika-api](https://github.com/coinpaprika/skills/tree/main/coinpaprika-api)** — Crypto market data for 12,000+ coins and 350+ exchanges
  <sub>MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/coinpaprika/skills.git && cd skills/coinpaprika-api`</sub>
- **[coinpaprika/dexpaprika-api](https://github.com/coinpaprika/skills/tree/main/dexpaprika-api)** — DEX pools, tokens, and OHLCV across 36 chains
  <sub>MIT · in-repo · pushed 2026-10-21</sub>
  <sub>`git clone https://github.com/coinpaprika/skills.git && cd skills/dexpaprika-api`</sub>
- **[jthack/threat-hunting-with-sigma-rules-skill](https://github.com/jthack/threat-hunting-with-sigma-rules-skill)** — Hunt for threats using Sigma detection rules
  <sub>unavailable</sub>
- **[Ivlad003/plugins](https://github.com/Ivlad003/plugins)** — Query and analyze Datadog logs, metrics, monitors, and traces directly from Claude Code via REST API
  <sub>MIT · source · pushed 2026-03-20</sub>
  <sub>`git clone https://github.com/Ivlad003/plugins.git`</sub>

## Google Ecosystem

- **[google-labs-code/design-md](https://github.com/google-labs-code/stitch-skills/tree/main/plugins/stitch-utilities/skills/design-md)** — Create and manage DESIGN.md files
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-08-17</sub>
  <sub>`git clone https://github.com/google-labs-code/stitch-skills.git && cd stitch-skills/plugins/stitch-utilities/skills/design-md`</sub>
- **[google-labs-code/enhance-prompt](https://github.com/google-labs-code/stitch-skills/tree/main/plugins/stitch-utilities/skills/enhance-prompt)** — Improve prompts with design specs and UI/UX vocabulary
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-08-17</sub>
  <sub>`git clone https://github.com/google-labs-code/stitch-skills.git && cd stitch-skills/plugins/stitch-utilities/skills/enhance-prompt`</sub>
- **[google-labs-code/react-components](https://github.com/google-labs-code/stitch-skills/tree/main/plugins/stitch-build/skills/react-components)** — Stitch to React components conversion
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-08-17</sub>
  <sub>`git clone https://github.com/google-labs-code/stitch-skills.git && cd stitch-skills/plugins/stitch-build/skills/react-components`</sub>
- **[google-labs-code/shadcn-ui](https://github.com/google-labs-code/stitch-skills/tree/main/plugins/stitch-build/skills/shadcn-ui)** — Build UI components with shadcn/ui
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-08-17</sub>
  <sub>`git clone https://github.com/google-labs-code/stitch-skills.git && cd stitch-skills/plugins/stitch-build/skills/shadcn-ui`</sub>
- **[google-labs-code/stitch-loop](https://github.com/google-labs-code/stitch-skills/tree/main/plugins/stitch-utilities/skills/stitch-loop)** — Iterative design-to-code feedback loop
  <sub>TypeScript · Apache-2.0 · in-repo · pushed 2026-08-17</sub>
  <sub>`git clone https://github.com/google-labs-code/stitch-skills.git && cd stitch-skills/plugins/stitch-utilities/skills/stitch-loop`</sub>
- **[googleworkspace/gws-drive](https://github.com/googleworkspace/cli/tree/main/skills/gws-drive)** — Manage Google Drive files, folders, and shared drives
  <sub>Rust · Apache-2.0 · in-repo · pushed 2026-10-06</sub>
  <sub>`git clone https://github.com/googleworkspace/cli.git && cd cli/skills/gws-drive`</sub>
- **[googleworkspace/gws-sheets](https://github.com/googleworkspace/cli/tree/main/skills/gws-sheets)** — Read and write Google Sheets spreadsheets
  <sub>Rust · Apache-2.0 · in-repo · pushed 2026-10-06</sub>
  <sub>`git clone https://github.com/googleworkspace/cli.git && cd cli/skills/gws-sheets`</sub>
- **[googleworkspace/gws-gmail](https://github.com/googleworkspace/cli/tree/main/skills/gws-gmail)** — Send, read, and manage Gmail email
  <sub>Rust · Apache-2.0 · in-repo · pushed 2026-10-06</sub>
  <sub>`git clone https://github.com/googleworkspace/cli.git && cd cli/skills/gws-gmail`</sub>
- **[googleworkspace/gws-calendar](https://github.com/googleworkspace/cli/tree/main/skills/gws-calendar)** — Manage Google Calendar calendars and events
  <sub>Rust · Apache-2.0 · in-repo · pushed 2026-10-06</sub>
  <sub>`git clone https://github.com/googleworkspace/cli.git && cd cli/skills/gws-calendar`</sub>
- **[googleworkspace/gws-workflow](https://github.com/googleworkspace/cli/tree/main/skills/gws-workflow)** — Cross-service Google Workspace productivity workflows
  <sub>Rust · Apache-2.0 · in-repo · pushed 2026-10-06</sub>
  <sub>`git clone https://github.com/googleworkspace/cli.git && cd cli/skills/gws-workflow`</sub>


---

Snapshot 2026-10-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
