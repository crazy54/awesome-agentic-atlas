# Prompt Engineering (promptslab)

This repository contains a hand-curated resources for Prompt Engineering with a focus on Generative Pre-trained Transformer (GPT), ChatGPT, PaLM etc

Curated by **[promptslab/Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

221 entries · 180 distinct repos · 14 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/openai/codex"><img src="https://raw.githubusercontent.com/openai/codex/main/.github/codex-cli-splash.png" width="260"></a> | <a href="https://github.com/google-gemini/gemini-cli"><img src="https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/assets/gemini-screenshot.png" width="260"></a> | <a href="https://github.com/zed-industries/zed"><img src="https://opengraph.githubassets.com/1/zed-industries/zed" width="260"></a> |
| **[OpenAI Codex CLI](https://github.com/openai/codex)**<br>★ 125.7k | **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**<br>★ 107.1k | **[Zed](https://github.com/zed-industries/zed)**<br>★ 90.7k |
| <a href="https://github.com/OpenHands/OpenHands"><img src="https://opengraph.githubassets.com/1/OpenHands/OpenHands" width="260"></a> | <a href="https://github.com/cline/cline"><img src="https://opengraph.githubassets.com/1/cline/cline" width="260"></a> | <a href="https://github.com/aaif-goose/goose"><img src="https://opengraph.githubassets.com/1/block/goose" width="260"></a> |
| **[OpenHands](https://github.com/OpenHands/OpenHands)**<br>★ 88.7k | **[Cline](https://github.com/cline/cline)**<br>★ 68.9k | **[Goose](https://github.com/aaif-goose/goose)**<br>★ 54.5k |

## Contents

- [Vibe Coding and AI Coding Assistants](#vibe-coding-and-ai-coding-assistants) (49)
- [Agent Frameworks](#agent-frameworks) (20)
- [Prompt Optimization Tools](#prompt-optimization-tools) (2)
- [MCP (Model Context Protocol)](#mcp-model-context-protocol) (8)
- [Platform Ports &amp; Hardware Forks](#platform-ports--hardware-forks) (9)
- [General-Purpose Descendants](#general-purpose-descendants) (28)
- [Research-Agent Systems](#research-agent-systems) (26)
- [Domain-Specific Adaptations](#domain-specific-adaptations) (9)
- [LLM Evaluation Tools](#llm-evaluation-tools) (10)
- [Prompt Management and Testing](#prompt-management-and-testing) (19)
- [Red Teaming and Prompt Security](#red-teaming-and-prompt-security) (11)
- [Evaluation &amp; Benchmarks](#evaluation--benchmarks) (5)
- [Other Notable Repositories](#other-notable-repositories) (14)
- [Related Resources](#related-resources) (11)

## Vibe Coding and AI Coding Assistants

- **[OpenAI Codex CLI](https://github.com/openai/codex)** — Open-source terminal coding agent from OpenAI; lightweight, local-first, with sandboxed code execution. ~68K+ ⭐
  <sub>★ 125.7k · Rust · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @openai/codex`</sub>
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — Google's open-source terminal AI agent with 1M-token context window and Google Search grounding. ~96K+ ⭐
  <sub>★ 107.1k · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @google/gemini-cli`</sub>
- **[Zed](https://github.com/zed-industries/zed)** — High-performance editor in Rust with native AI features, Zeta edit prediction, and Agent Client Protocol support. ~77K+ ⭐
  <sub>★ 90.7k · Rust · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/zed-industries/zed.git`</sub>
- **[OpenHands](https://github.com/OpenHands/OpenHands)** — Leading open-source platform for cloud coding agents; consistently top on SWE-bench. Formerly OpenDevin. ~69K+ ⭐
  <sub>★ 88.7k · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[Cline](https://github.com/cline/cline)** — Autonomous coding agent in VS Code with human-in-the-loop approvals; file editing, terminal commands, and browser use. ~59K+ ⭐
  <sub>★ 68.9k · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g cline`</sub>
- **[Goose](https://github.com/aaif-goose/goose)** — Extensible open-source AI agent from Block (Square/Cash App); installs, executes, edits, and tests with any LLM. ~29K+ ⭐
  <sub>★ 54.5k · Rust · Apache-2.0 · script · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash`</sub>
- **[Aider](https://github.com/Aider-AI/aider)** — AI pair programming in terminal with deep Git integration; maps entire codebases and auto-commits changes. ~42K+ ⭐
  <sub>★ 49.1k · Python · Apache-2.0 · source · pushed 2026-05-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Aider-AI/aider.git`</sub>
- **[Continue](https://github.com/continuedev/continue)** — Open-source VS Code and JetBrains extension for creating custom, modular AI dev systems; any model. ~32K+ ⭐
  <sub>★ 36k · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/continuedev/continue.git`</sub>
- **[Tabby](https://github.com/TabbyML/tabby)** — Self-hosted open-source AI coding assistant (Copilot alternative); runs entirely on your infrastructure. ~25K+ ⭐
  <sub>★ 33.9k · Rust · source · pushed 2026-06-30 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/TabbyML/tabby.git`</sub>
- **[Void](https://github.com/voideditor/void)** — Open-source Cursor alternative (VS Code fork); any model or local hosting with change visualization. ~28K+ ⭐
  <sub>★ 28.8k · TypeScript · Apache-2.0 · source · pushed 2026-06-02 · Win · macOS</sub>
  <sub>`git clone https://github.com/voideditor/void.git`</sub>
- **[Crush](https://github.com/charmbracelet/crush)** — Glamorous agentic coding agent from Charmbracelet with multi-model support, LSP integration, and beautiful terminal UI. ~9K+ ⭐
  <sub>★ 28.2k · Go · winget · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`winget install charmbracelet.crush`</sub>
- **[Qwen Code](https://github.com/QwenLM/qwen-code)** — Open-source terminal AI agent optimized for Qwen3-Coder; multi-protocol support (OpenAI/Anthropic/Gemini APIs), 1,000 free requests/day. ~21K+ ⭐
  <sub>★ 28k · TypeScript · Apache-2.0 · psh · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.ps1 | iex`</sub>
- **[SWE-agent](https://github.com/SWE-agent/SWE-agent)** — Takes a GitHub issue and automatically fixes it using a custom agent-computer interface. [NeurIPS 2024] ~19K+ ⭐
  <sub>★ 20.4k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SWE-agent/SWE-agent.git`</sub>
- **[bolt.diy](https://github.com/stackblitz-labs/bolt.diy)** — Community fork of bolt.new with extended features and broader LLM flexibility. ~12K+ ⭐
  <sub>★ 19.9k · TypeScript · MIT · source · pushed 2026-02-07 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/stackblitz-labs/bolt.diy.git`</sub>
- **[Devika](https://github.com/stitionai/devika)** — Open-source agentic software engineer; breaks down instructions, researches, and writes code. Devin alternative. ~18K+ ⭐
  <sub>★ 19.6k · Python · MIT · clone · pushed 2025-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stitionai/devika.git`</sub>
- **[bolt.new](https://github.com/stackblitz/bolt.new)** — AI-powered web dev agent; prompt, run, edit, and deploy full-stack apps directly in the browser via WebContainers. ~15K+ ⭐
  <sub>★ 16.6k · TypeScript · MIT · source · pushed 2024-12-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stackblitz/bolt.new.git`</sub>
- **[OpenCode](https://github.com/opencode-ai/opencode)** — Powerful open-source AI coding agent with beautiful TUI; supports nearly all AI model providers. ~120K+ ⭐
  <sub>★ 13.8k · Go · MIT · go · pushed 2025-09-18 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`go install github.com/opencode-ai/opencode@latest`</sub>
- **[Open SWE](https://github.com/langchain-ai/open-swe)** — LangChain's async cloud-hosted coding agent framework built on LangGraph with Slack/Linear integration. ~8K+ ⭐
  <sub>★ 10.7k · Python · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/open-swe.git`</sub>
- **[CodeGeeX](https://github.com/zai-org/CodeGeeX)** — Open-source multilingual code generation model supporting 20+ languages with VS Code and JetBrains extensions. ~11K+ ⭐
  <sub>★ 8.8k · Python · Apache-2.0 · docker · pushed 2024-08-13 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run --gpus '"device=0,1"' -it --ipc=host --name=codegeex codegeex/codegeex`</sub>
- **[Emdash](https://github.com/generalaction/emdash)** — Open-source agentic dev environment (YC W26) for running multiple coding agents in parallel in isolated Git worktrees
  <sub>★ 5.8k · TypeScript · Apache-2.0 · brew · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask emdash`</sub>
- **[Melty](https://github.com/meltylabs/melty)** — Open-source chat-first AI code editor with multi-file editing and deep Git integration. ~7K+ ⭐
  <sub>★ 5.4k · TypeScript · MIT · source · pushed 2024-11-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/meltylabs/melty.git`</sub>
- **[Devon](https://github.com/entropy-research/Devon)** — Open-source pair programmer SWE agent with code writing, planning, and research; supports Claude, GPT-4, Llama, Ollama. ~3.5K+ ⭐
  <sub>★ 3.5k · Python · AGPL-3.0 · npx · pushed 2025-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx devon-ui`</sub>
- **[AutoCodeRover](https://github.com/AutoCodeRoverSG/auto-code-rover)** — Autonomous program improvement combining LLMs with fault localization for GitHub issue resolution. ~2.8K+ ⭐
  <sub>★ 3.1k · Python · gh-action · pushed 2025-04-24</sub>
  <sub>`uses: nus-apr/auto-code-rover@main # in .github/workflows/*.yml`</sub>
- **[Agentless](https://github.com/OpenAutoCoder/Agentless)** — Simple three-phase approach (localize → repair → validate) to solving software development problems. ~2K+ ⭐
  <sub>★ 2.1k · Python · MIT · clone · pushed 2024-12-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenAutoCoder/Agentless.git`</sub>
- **[Amazon Q Developer CLI](https://github.com/aws/amazon-q-developer-cli)** — Agentic chat experience in terminal from AWS; transitioning to Kiro CLI
  <sub>★ 2k · Rust · Apache-2.0 · brew · pushed 2026-08-24 · WSL2? · macOS · Linux?</sub>
  <sub>`brew install --cask amazon-q`</sub>
- **[PearAI](https://github.com/trypear/pearai-app)** — Open-source AI code editor (VS Code fork) with Continue-based chat and completions. ~40K+ ⭐
  <sub>★ 713 · TypeScript · MIT · source · pushed 2025-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trypear/pearai-app.git`</sub>
- **[Autohand Code CLI](https://github.com/autohandai/code-cli)** — Self-evolving autonomous terminal coding agent with multi-provider LLM support, 40+ tools, and modular skills system
  <sub>★ 196 · TypeScript · Apache-2.0 · brew · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install autohandai/code/autohand-code`</sub>
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — Anthropic's agentic coding CLI; understands full codebases and executes complex multi-step tasks via natural language
  <sub>website</sub>
  <sub>`https://docs.anthropic.com/en/docs/claude-code`</sub>
- **[Amp](https://ampcode.com)** — Sourcegraph's agentic coding tool (Cody successor); works across CLI and IDE
  <sub>website</sub>
  <sub>`https://ampcode.com`</sub>
- **[Junie CLI](https://www.jetbrains.com/junie/)** — JetBrains' LLM-agnostic coding agent CLI (beta 2026); supports all major model providers
  <sub>website</sub>
  <sub>`https://www.jetbrains.com/junie/`</sub>
- **[Cursor](https://cursor.com)** — Leading AI-native code editor (VS Code fork); Composer generates entire apps from natural language, agentic multi-file edits
  <sub>website</sub>
  <sub>`https://cursor.com`</sub>
- **[Windsurf](https://windsurf.com)** — AI-powered IDE (VS Code fork) with proprietary Cascade agent and SWE-1.5 model; acquired by Cognition AI
  <sub>website</sub>
  <sub>`https://windsurf.com`</sub>
- **[Trae](https://www.trae.ai)** — Free AI-powered IDE from ByteDance ("The Real AI Engineer") with Builder Mode; provides free access to Claude, GPT-4o, and DeepSeek
  <sub>website</sub>
  <sub>`https://www.trae.ai`</sub>
- **[Google Antigravity](https://antigravity.google)** — Google's agent-first IDE (VS Code fork) with Manager view for orchestrating multiple agents in parallel; powered by Gemini
  <sub>website</sub>
  <sub>`https://antigravity.google`</sub>
- **[Kiro](https://kiro.dev)** — AWS's spec-driven agentic AI IDE (VS Code fork); turns prompts into specs, then working code, docs, and tests
  <sub>website</sub>
  <sub>`https://kiro.dev`</sub>
- **[GitHub Copilot](https://github.com/features/copilot)** — Most widely adopted AI coding assistant; inline completions, chat, and agentic coding agent across VS Code, JetBrains, Neovim
  <sub>website</sub>
  <sub>`https://github.com/features/copilot`</sub>
- **[Cody](https://sourcegraph.com/cody)** — Sourcegraph-powered AI assistant that pulls context from local and remote codebases; VS Code, JetBrains, Visual Studio
  <sub>website</sub>
  <sub>`https://sourcegraph.com/cody`</sub>
- **[Codeium](https://codeium.com)** — Free AI coding extension for 40+ IDEs with completions, chat, and search across 70+ languages
  <sub>website</sub>
  <sub>`https://codeium.com`</sub>
- **[Amazon Q Developer](https://aws.amazon.com/q/developer/)** — AWS's AI coding assistant with completions, inline chat, and agent mode; deep AWS integration
  <sub>website</sub>
  <sub>`https://aws.amazon.com/q/developer/`</sub>
- **[Gemini Code Assist](https://codeassist.google)** — Google's IDE extension powered by Gemini with completions, Next Edit Predictions, and inline diffs; free for individuals
  <sub>website</sub>
  <sub>`https://codeassist.google`</sub>
- **[Tabnine](https://www.tabnine.com)** — Privacy-focused AI assistant trained on permissive-licensed OSS; supports all major IDEs with on-premises deployment
  <sub>website</sub>
  <sub>`https://www.tabnine.com`</sub>
- **[Augment Code](https://www.augmentcode.com)** — Enterprise AI coding assistant with 200K-token Context Engine for deep codebase understanding
  <sub>website</sub>
  <sub>`https://www.augmentcode.com`</sub>
- **[Qodo](https://www.qodo.ai)** — AI code review and quality platform with multi-agent architecture; test generation, code review, CI/CD enforcement
  <sub>website</sub>
  <sub>`https://www.qodo.ai`</sub>
- **[Devin](https://devin.ai)** — First fully autonomous cloud-based AI software engineer; plans, codes, tests, and opens PRs independently
  <sub>website</sub>
  <sub>`https://devin.ai`</sub>
- **[Replit Agent](https://replit.com/products/agent)** — Cloud-native AI agent that autonomously builds, tests, and deploys full-stack apps in-browser; 50+ languages
  <sub>website</sub>
  <sub>`https://replit.com/products/agent`</sub>
- **[Lovable](https://lovable.dev)** — Full-stack apps from natural language with built-in Supabase, auth, and one-click deploy; fastest European startup to $20M ARR
  <sub>website</sub>
  <sub>`https://lovable.dev`</sub>
- **[v0](https://v0.dev)** — Vercel's AI platform for generating high-quality React/Next.js UI components from natural language
  <sub>website</sub>
  <sub>`https://v0.dev`</sub>
- **[GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace)** — Cloud-based coding environment with plan, brainstorm, and repair agents; included with paid Copilot plans
  <sub>website</sub>
  <sub>`https://githubnext.com/projects/copilot-workspace`</sub>
- **[Firebase Studio](https://firebase.google.com/studio)** — Google's agentic cloud-based development environment
  <sub>website</sub>
  <sub>`https://firebase.google.com/studio`</sub>

## Agent Frameworks

- **[n8n](https://github.com/n8n-io/n8n)** — Workflow automation with AI agent capabilities and 400+ integrations. ~60K+ ⭐
  <sub>★ 205.6k · TypeScript · script · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://get.n8n.io | sh`</sub>
- **[Dify](https://github.com/langgenius/dify)** — All-in-one backend for agentic workflows with tool-using agents and RAG
  <sub>★ 156.7k · TypeScript · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/langgenius/dify.git`</sub>
- **[Langflow](https://github.com/langflow-ai/langflow)** — Node-based visual agent builder with drag-and-drop. ~50K+ ⭐
  <sub>★ 155.1k · Python · MIT · docker · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -p 7860:7860 langflowai/langflow:latest`</sub>
- **[LangChain / LangGraph](https://github.com/langchain-ai/langchain)** — Most widely adopted LLM app framework; LangGraph adds graph-based multi-step agent workflows. ~100K+ / ~10K+ ⭐
  <sub>★ 146.8k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/langchain.git`</sub>
- **[AutoGen (AG2)](https://github.com/microsoft/autogen)** — Microsoft's multi-agent conversational framework. ~40K+ ⭐
  <sub>★ 61.1k · Python · CC-BY-4.0 · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "autogen-agentchat" "autogen-ext[openai]"`</sub>
- **[CrewAI](https://github.com/crewAIInc/crewAI)** — Role-playing AI agent orchestration with 700+ integrations. ~44K+ ⭐
  <sub>★ 58.9k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add crewaiinc/skills`</sub>
- **[LlamaIndex](https://github.com/run-llama/llama_index)** — Data framework for RAG and agent capabilities. ~40K+ ⭐
  <sub>★ 52.3k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llama-index-core`</sub>
- **[Agno (formerly Phidata)](https://github.com/agno-agi/agno)** — Python agent framework with microsecond instantiation. ~20K+ ⭐
  <sub>★ 42.3k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agno-agi/agno.git`</sub>
- **[DSPy](https://github.com/stanfordnlp/dspy)** — Stanford's framework for programming LLMs with automatic prompt/weight optimization. ~22K+ ⭐
  <sub>★ 38.2k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install dspy`</sub>
- **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** — Official agent framework with function calling, guardrails, and handoffs. ~10K+ ⭐
  <sub>★ 29.6k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openai-agents`</sub>
- **[Smolagents](https://github.com/huggingface/smolagents)** — Hugging Face's minimalist code-centric agent framework (~1000 LOC). ~15K+ ⭐
  <sub>★ 29.4k · Python · Apache-2.0 · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "smolagents[toolkit]"`</sub>
- **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** — Microsoft's AI framework powering M365 Copilot; C#, Python, Java. ~24K+ ⭐
  <sub>★ 28.6k · C# · MIT · pip · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install semantic-kernel`</sub>
- **[Mastra](https://github.com/mastra-ai/mastra)** — TypeScript AI agent framework with assistants, RAG, and observability. ~20K+ ⭐
  <sub>★ 28.2k · TypeScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git`</sub>
- **[Haystack](https://github.com/deepset-ai/haystack)** — Open-source NLP framework with pipeline architecture for RAG and agents. ~20K+ ⭐
  <sub>★ 26.6k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install haystack-ai`</sub>
- **[Google ADK](https://github.com/google/adk-python)** — Agent Development Kit deeply integrated with Gemini and Google Cloud
  <sub>★ 21.6k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install google-adk`</sub>
- **[Pydantic AI](https://github.com/pydantic/pydantic-ai)** — Type-safe agent framework using Pydantic for structured validation. ~8K+ ⭐
  <sub>★ 20.1k · Python · MIT · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --with pydantic-ai-harness clai -a pydantic_ai_harness.coder:coder_agent -m anthropic:claude-fable-5`</sub>
- **[PraisonAI](https://github.com/MervinPraison/PraisonAI)** — Multi-AI Agents framework with 100+ LLM support, MCP integration, and built-in memory
  <sub>★ 9.1k · Python · MIT · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install praisonai`</sub>
- **[Strands Agents (AWS)](https://github.com/strands-agents/harness-sdk)** — Model-agnostic framework with deep AWS integrations
  <sub>★ 7.4k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install strands-agents strands-agents-tools`</sub>
- **[Neurolink](https://github.com/juspay/neurolink)** — Multi-provider AI agent framework unifying 12+ providers with workflow orchestration
  <sub>★ 135 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @juspay/neurolink --help`</sub>
- **[Composio](https://github.com/ComposioHQ/composio)** — Connect 100+ tools to AI agents with zero setup
  <sub>source</sub>
  <sub>`git clone https://github.com/composiohq/composio.git`</sub>

## Prompt Optimization Tools

- **[TextGrad](https://github.com/zou-group/textgrad)** — Automatic differentiation via text (Stanford). ~2K+ ⭐
  <sub>★ 3.7k · Python · MIT · pip · pushed 2025-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install textgrad`</sub>
- **[OPRO](https://github.com/google-deepmind/opro)** — Google DeepMind's optimization by prompting
  <sub>★ 778 · Python · Apache-2.0 · source · pushed 2024-12-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/google-deepmind/opro.git`</sub>

## MCP (Model Context Protocol)

- **[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)** — Curated list of 10,000+ community MCP servers. ~30K+ ⭐
  <sub>★ 95.4k · MIT · npx · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx awesome-mcp search postgres`</sub>
- **[MCP Reference Servers](https://github.com/modelcontextprotocol/servers)** — Official implementations: fetch, filesystem, GitHub, Slack, Postgres
  <sub>★ 90.5k · TypeScript · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @modelcontextprotocol/server-memory`</sub>
- **[Context7](https://github.com/upstash/context7)** — MCP server providing version-specific documentation to reduce code hallucination
  <sub>★ 62.3k · TypeScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upstash/context7.git`</sub>
- **[GitHub MCP Server](https://github.com/github/github-mcp-server)** — GitHub's official MCP server for repo, issue, PR, and Actions interaction. ~15K+ ⭐
  <sub>★ 33.1k · Go · MIT · source · pushed 2026-09-16 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/github/github-mcp-server.git`</sub>
- **[FastMCP (Python)](https://github.com/PrefectHQ/fastmcp)** — High-level Pythonic framework for building MCP servers. ~5K+ ⭐
  <sub>★ 27.8k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jlowin/fastmcp.git`</sub>
- **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)** — Visual testing tool for MCP server development
  <sub>★ 10.9k · TypeScript · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector # web UI (default)`</sub>
- **[MCP Specification](https://github.com/modelcontextprotocol/modelcontextprotocol)** — The core protocol specification and SDKs. ~15K+ ⭐
  <sub>★ 9.3k · TypeScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/modelcontextprotocol/modelcontextprotocol.git`</sub>
- **[GitMCP](https://gitmcp.io/)** — Creates remote MCP servers for any GitHub repo by changing the domain
  <sub>website</sub>
  <sub>`https://gitmcp.io/`</sub>

## Platform Ports &amp; Hardware Forks

- **[Colab/Kaggle T4 port](https://github.com/karpathy/autoresearch/issues/208)** — Adapts autoresearch for free T4 GPUs (Google Colab / Kaggle) with zero cost and zero local setup. Key changes: Flash Attention 3 → PyTorch SDPA, removes H100-only kernel dependency
  <sub>★ 96.5k · Python · source · pushed 2026-03-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/karpathy/autoresearch/issues/208.git`</sub>
- **[miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos)** — Widely adopted macOS fork that adapts upstream autoresearch for Apple Silicon / MPS while preserving the original loop shape
  <sub>★ 2.4k · Python · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/miolini/autoresearch-macos.git`</sub>
- **[trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)** — MLX-native Apple Silicon port that keeps the upstream fixed-budget val_bpb loop while removing the PyTorch/CUDA dependency entirely
  <sub>★ 1.8k · Python · MIT · source · pushed 2026-07-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trevin-creator/autoresearch-mlx.git`</sub>
- **[jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx)** — Windows-native RTX fork focused on consumer NVIDIA GPUs, with explicit VRAM floors and a practical desktop setup path
  <sub>★ 729 · Python · source · pushed 2026-03-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/jsegov/autoresearch-win-rtx.git`</sub>
- **[gianfrancopiana/openclaw-autoresearch](https://github.com/gianfrancopiana/openclaw-autoresearch)** — OpenClaw port of pi-autoresearch; autonomous experiment loop for any optimization target with statistical confidence scoring
  <sub>★ 176 · TypeScript · MIT · source · pushed 2026-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gianfrancopiana/openclaw-autoresearch.git`</sub>
- **[iii-hq/n-autoresearch](https://github.com/iii-experimental/n-autoresearch)** — Multi-GPU autoresearch infrastructure with structured experiment tracking, adaptive search strategy, crash recovery, and queryable orchestration around the classic train.py loop
  <sub>★ 102 · Python · Apache-2.0 · clone · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/iii-hq/n-autoresearch.git`</sub>
- **[lucasgelfond/autoresearch-webgpu](https://github.com/lucasgelfond/autoresearch-webgpu)** — Browser/WebGPU port that lets agents generate training code, run experiments in-browser, and feed results back into the loop without a Python setup
  <sub>★ 72 · TypeScript · MIT · source · pushed 2026-03-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lucasgelfond/autoresearch-webgpu.git`</sub>
- **[tonitangpotato/autoresearch-engram](https://github.com/tonitangpotato/autoresearch-engram)** — Fork with persistent cognitive memory — frequency-weighted retrieval of cross-session knowledge for improved experiment continuity
  <sub>★ 20 · Python · pip · pushed 2026-03-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install engramai`</sub>
- **[ArmanJR-Lab/autoautoresearch](https://github.com/ArmanJR-Lab/autoautoresearch)** — Jetson AGX Orin port with a director — a Go binary that acts as a "creative director" injecting novelty (arxiv papers + DeepSeek Reasoner) into the loop to escape local minima. Includes multi-experiment comparison (baseline vs director-guided) with detailed stall analysis
  <sub>★ 2 · Python · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ArmanJR-Lab/autoautoresearch.git`</sub>

## General-Purpose Descendants

- **[davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch)** — pi extension plus dashboard for persistent experiment loops, live metrics, confidence tracking, and resumable autoresearch sessions
  <sub>★ 8.1k · TypeScript · MIT · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/davebcn87/pi-autoresearch.git`</sub>
- **[gepa-ai/gepa](https://github.com/gepa-ai/gepa)** — GEPA (Genetic-Pareto) — ICLR 2026 Oral. Reflective prompt evolution that outperforms RL (GRPO) on benchmarks. Optimizes any textual parameters against any metric using natural language reflection
  <sub>★ 6.7k · Jupyter Notebook · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install gepa`</sub>
- **[uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch)** — Claude Code skill that generalizes autoresearch into a reusable loop for software, docs, security, shipping, debugging, and other measurable goals
  <sub>★ 6.3k · Shell · MIT · npx · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add uditgoenka/autoresearch`</sub>
- **[HKUDS/ClawTeam](https://github.com/HKUDS/ClawTeam)** — Agent swarm intelligence for autoresearch — spawns parallel GPU research directions, distributes work across agents, aggregates results
  <sub>★ 5.5k · Python · MIT · pip · pushed 2026-05-09 · WSL2 · macOS? · Linux</sub>
  <sub>`pip install clawteam`</sub>
- **[leo-lilinxiao/codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch)** — Codex-native autoresearch skill with resume support, lessons across runs, optional parallel experiments, and mode-specific workflows
  <sub>★ 2.6k · Python · MIT · source · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leo-lilinxiao/codex-autoresearch.git`</sub>
- **[ShengranHu/ADAS](https://github.com/ShengranHu/ADAS)** — Automated Design of Agentic Systems — ICLR 2025. Meta-agents that invent novel agent architectures by programming them in code
  <sub>★ 1.6k · Python · Apache-2.0 · source · pushed 2025-01-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ShengranHu/ADAS.git`</sub>
- **[WecoAI/aideml](https://github.com/WecoAI/aideml)** — AIDE: Tree-search ML engineering agent that autonomously improves model performance via iterative code generation and evaluation
  <sub>★ 1.5k · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -U aideml`</sub>
- **[greyhaven-ai/autocontext](https://github.com/greyhaven-ai/autocontext)** — Closed-loop control plane for repeated agent improvement, with evaluation, persistent knowledge, staged validation, and optional distillation into cheaper local runtimes
  <sub>★ 1.3k · Python · Apache-2.0 · uv · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install autocontext==0.18.0`</sub>
- **[sentient-agi/EvoSkill](https://github.com/sentient-agi/EvoSkill)** — Automated skill discovery for coding agents: evolves reusable skills and prompts from failed trajectories against benchmarks, with support for Claude Code, Codex CLI, OpenCode, OpenHands, and Goose
  <sub>★ 1.2k · Python · Apache-2.0 · script · pushed 2026-08-24 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/sentient-agi/EvoSkill/main/install.sh | bash`</sub>
- **[peterskoett/self-improving-agent](https://github.com/pskoett/self-improving-agent)** — Alternative self-improving agent architecture with reflection and meta-learning cycles
  <sub>★ 763 · JavaScript · clone · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pskoett/self-improving-agent.git`</sub>
- **[mutable-state-inc/autoresearch-at-home](https://github.com/mutable-state-inc/autoresearch-at-home)** — Collaborative fork of upstream autoresearch that adds experiment claiming, shared best-config syncing, hypothesis exchange, and swarm-style coordination across many single-GPU agents
  <sub>★ 495 · Python · source · pushed 2026-03-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mutable-state-inc/autoresearch-at-home.git`</sub>
- **[metauto-ai/HGM](https://github.com/metauto-ai/HGM)** — Huxley-Gödel Machine for coding agents — applies self-improvement to SWE-bench performance via meta-level optimization
  <sub>★ 432 · Python · Apache-2.0 · source · pushed 2026-02-07 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/metauto-ai/HGM.git`</sub>
- **[MaximeRobeyns/self_improving_coding_agent](https://github.com/MaximeRobeyns/self_improving_coding_agent)** — SICA: Self-Improving Coding Agent that edits its own codebase. ICLR 2025 Workshop paper demonstrating scaffold-level self-improvement on coding benchmarks
  <sub>★ 399 · Python · MIT · clone · pushed 2025-04-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MaximeRobeyns/self_improving_coding_agent`</sub>
- **[drivelineresearch/autoresearch-claude-code](https://github.com/drivelineresearch/autoresearch-claude-code)** — Claude Code plugin/skill port of pi-autoresearch, with a clean experiment-loop workflow and a concrete biomechanics case study
  <sub>★ 344 · Python · MIT · source · pushed 2026-09-07 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/drivelineresearch/autoresearch-claude-code.git`</sub>
- **[kayba-ai/recursive-improve](https://github.com/kayba-ai/recursive-improve)** — Recursive self-improvement framework where agents capture execution traces, analyze failure patterns, and apply targeted fixes with keep-or-revert evaluation
  <sub>★ 267 · Python · Apache-2.0 · uv · pushed 2026-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "recursive-improve[all] @ git+https://github.com/kayba-ai/recursive-improve.git"`</sub>
- **[jmilinovich/goal-md](https://github.com/jmilinovich/goal-md)** — Generalizes autoresearch into a GOAL.md pattern for repos where the agent must first construct a measurable fitness function before it can optimize
  <sub>★ 164 · Shell · source · pushed 2026-05-03</sub>
  <sub>`git clone https://github.com/jmilinovich/goal-md.git`</sub>
- **[zkarimi22/autoresearch-anything](https://github.com/zkarimi22/autoresearch-anything)** — Generalizes autoresearch to any measurable metric — system prompts, API performance, landing pages, test suites, config tuning, SQL queries. "If you can measure it, you can optimize it."
  <sub>★ 129 · JavaScript · MIT · npx · pushed 2026-03-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx autoresearch-anything`</sub>
- **[Necmttn/ax](https://github.com/Necmttn/ax)** — Local retro loop for AI coding agents: captures session traces, turns repeated friction into proposals, and tracks accepted fixes as experiments
  <sub>★ 111 · TypeScript · AGPL-3.0 · npx · pushed 2026-09-14 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add Necmttn/ax # agent skills: setup, retro, extract-workflow, dojo, …`</sub>
- **[SeeleAI/Thoth](https://github.com/SeeleAI/Thoth)** — Dashboard-first Claude Code and Codex runtime for autoresearch, with durable runs, locked work items, visible ledgers, and reviewable verdicts
  <sub>★ 51 · Python · MIT · source · pushed 2026-08-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/SeeleAI/Thoth.git`</sub>
- **[supratikpm/gemini-autoresearch](https://github.com/supratikpm/gemini-autoresearch)** — Gemini CLI skill that generalises autoresearch to any measurable goal. Gemini-native: uses Google Search grounding as a live verification source inside the loop, true headless overnight mode via --yolo --prompt, and 1M token context. Also works in Antigravity IDE via .agents/skills/
  <sub>★ 45 · JavaScript · clone · pushed 2026-03-27 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/supratikpm/gemini-autoresearch.git`</sub>
- **[xieyulai/steer](https://github.com/xieyulai/steer)** — Governed experiment framework where coding agents edit training code and run rounds while the task, scorer, and evidence stay fixed
  <sub>★ 26 · Python · Apache-2.0 · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/xieyulai/steer.git`</sub>
- **[MrTsepa/autoevolve](https://github.com/MrTsepa/autoevolve)** — GEPA-inspired autoresearch for self-play: mutate code strategies, evaluate head-to-head, rate with Elo/Bradley-Terry, branch from the Pareto front. Agent reads match traces to target mutations. Works as a Claude Code skill
  <sub>★ 22 · Python · MIT · npx · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add MrTsepa/autoevolve -y`</sub>
- **[vukrosic/auto-research](https://github.com/vukrosic/auto-research)** — Docs-only control plane for an open autonomous AI research lab — file-based operating model for human direction and agent execution
  <sub>★ 19 · source · pushed 2026-04-04</sub>
  <sub>`git clone https://github.com/vukrosic/auto-research.git`</sub>
- **[Entrpi/autoresearch-everywhere](https://github.com/Entrpi/autoresearch-everywhere)** — Cross-platform expansion that auto-detects hardware config and starts the loop. The "glue and generalization" half of autoresearch
  <sub>★ 18 · Python · source · pushed 2026-03-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Entrpi/autoresearch-everywhere.git`</sub>
- **[james-s-tayler/lazy-developer](https://github.com/james-s-tayler/lazy-developer)** — Claude Code skill that orchestrates autoresearch across a prioritized sequence of optimization goals (coverage, test speed, build speed, complexity, LOC, performance) using GOAL.md as the engine. Supports standalone and Ralph Mode multi-instance execution
  <sub>★ 12 · source · pushed 2026-03-31</sub>
  <sub>`git clone https://github.com/james-s-tayler/lazy-developer.git`</sub>
- **[junjunjunbong/research-loop](https://github.com/junjunjunbong/research-loop)** — Autoresearch-style Agent Skill for Codex and Claude Code with a deterministic runner, plan-hash approval, isolated Git worktrees, authoritative metric evaluation, and an append-only experiment ledger
  <sub>★ 1 · Python · clone · pushed 2026-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/junjunjunbong/research-loop.git`</sub>
- **[Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)** — Comprehensive skill library including autoresearch orchestration with two-loop architecture (inner optimization + outer synthesis)
  <sub>source</sub>
  <sub>`git clone https://github.com/Orchestra-Research/AI-Research-SKILLs.git`</sub>
- **[weco.ai](https://weco.ai)** — Weco: Cloud platform for AIDE with observability, experiment tracking, and managed runs — brings the autoresearch loop into production
  <sub>website</sub>
  <sub>`https://weco.ai`</sub>

## Research-Agent Systems

- **[wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** — Markdown-first research workflows for Claude Code and other agents, centered on autonomous literature review, experiments, paper iteration, and cross-model critique
  <sub>★ 16.5k · Python · MIT · clone · pushed 2026-09-18 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git`</sub>
- **[SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist)** — The AI Scientist: First comprehensive system for fully automatic scientific discovery. From idea generation to paper writing with minimal human supervision
  <sub>★ 14.6k · Jupyter Notebook · docker · pushed 2025-12-19 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -v `pwd`/templates:/app/AI-Scientist/templates <AI_SCIENTIST_IMAGE> \`</sub>
- **[aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)** — End-to-end research pipeline that turns a topic into literature review, experiments, analysis, peer review, and paper drafts; broader than autoresearch, but clearly in the same lineage
  <sub>★ 14.5k · Python · MIT · clone · pushed 2026-08-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/aiming-lab/AutoResearchClaw.git`</sub>
- **[SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)** — Workshop-level automated scientific discovery via agentic tree search. Removes template dependency from v1, generalizes across research domains
  <sub>★ 7.2k · Python · source · pushed 2025-12-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SakanaAI/AI-Scientist-v2.git`</sub>
- **[SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)** — End-to-end autonomous research workflow: idea → literature review → experiments → report. Supports both autonomous and co-pilot modes
  <sub>★ 5.9k · Python · MIT · clone · pushed 2025-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:SamuelSchmidgall/AgentLaboratory.git`</sub>
- **[HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)** — NeurIPS 2025 paper. Full end-to-end research automation: hypothesis → experiments → manuscript → peer review. Production version at novix.science
  <sub>★ 5.8k · Python · clone · pushed 2025-10-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/HKUDS/AI-Researcher.git`</sub>
- **[hyperspaceai/agi](https://github.com/hyperspaceai/agi)** — Distributed, peer-to-peer research network where autonomous agents run experiments, gossip findings, maintain CRDT leaderboards, and archive results to GitHub across multiple research domains
  <sub>★ 2.1k · JavaScript · MIT · script · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agents.hyper.space/api/install | bash`</sub>
- **[skyllwt/AutoSci](https://github.com/skyllwt/AutoSci)** — Wiki-centric full-lifecycle research platform built on Claude Code, realizing Karpathy's LLM-Wiki vision. 20+ skills cover the full loop: ingest → ideate → novelty check → experiment design / run / eval → paper writing. Research state lives in a structured knowledge wiki with an interactive graph
  <sub>★ 1.7k · Python · MIT · source · pushed 2026-09-18 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/skyllwt/AutoSci.git`</sub>
- **[OpenRaiser/NanoResearch](https://github.com/OpenRaiser/NanoResearch)** — End-to-end autonomous research engine that plans experiments, generates code, runs jobs locally or on SLURM, analyzes real results, and writes papers grounded in those outputs
  <sub>★ 1.4k · Python · MIT · clone · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenRaiser/NanoResearch.git`</sub>
- **[OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw)** — Open-source research workspace with sequential idea-to-paper pipelines and integrated autoresearch tool packs
  <sub>★ 1.1k · JavaScript · npm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g dr-claw`</sub>
- **[Human-Agent-Society/CORAL](https://github.com/Human-Agent-Society/CORAL)** — CORAL: Autonomous multi-agent evolution for open-ended discovery (arXiv:2604.01658). Long-running agents with shared persistent memory, asynchronous execution, and heartbeat-based interventions; SOTA on 10 math/algorithmic/systems tasks
  <sub>★ 1k · Python · Apache-2.0 · script · pushed 2026-09-08 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/Human-Agent-Society/CORAL/main/install.sh | sh`</sub>
- **[eimenhmdt/autoresearcher](https://github.com/eimenhmdt/autoresearcher)** — Early open-source package for automating scientific workflows, currently centered on literature-review generation with an ambition toward broader autonomous research
  <sub>★ 443 · Python · MIT · pip · pushed 2024-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install autoresearcher`</sub>
- **[Sibyl-Research-Team/AutoResearch-SibylSystem](https://github.com/Sibyl-Research-Team/AutoResearch-SibylSystem)** — Fully autonomous AI scientist built on Claude Code, with explicit AutoResearch lineage, multi-agent research iteration, GPU experiment execution, and a self-evolving outer loop
  <sub>★ 281 · Python · clone · pushed 2026-03-25 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/Sibyl-Research-Team/sibyl-research-system.git`</sub>
- **[AweAI-Team/AiScientist](https://github.com/AweAI-Team/AiScientist)** — AiScientist: long-horizon ML research lab with hierarchical orchestration and File-as-Bus coordination — workspace files act as the durable system of record. Drives autonomous paper-reproduction (PaperBench) and competition-style MLE-Bench iteration loops under fixed compute/time budgets. (arXiv 2604.13018)
  <sub>★ 146 · Python · MIT · clone · pushed 2026-07-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/AweAI-Team/AiScientist.git`</sub>
- **[PouriaRouzrokh/LatteReview](https://github.com/PouriaRouzrokh/LatteReview)** — Low-code Python package for automated systematic literature reviews via AI-powered agents
  <sub>★ 121 · Jupyter Notebook · pip · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lattereview`</sub>
- **[MASWorks/ML-Agent](https://github.com/MASWorks/ML-Agent)** — Reinforcing LLM agents for autonomous ML engineering. Learns from trial and error to improve model performance
  <sub>★ 74 · Python · source · pushed 2025-06-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MASWorks/ML-Agent.git`</sub>
- **[du-nlp-lab/MLR-Copilot](https://github.com/du-nlp-lab/MLR-Copilot)** — Autonomous ML research framework — generates ideas, implements experiments, analyzes results
  <sub>★ 70 · Python · source · pushed 2025-03-30 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/du-nlp-lab/MLR-Copilot.git`</sub>
- **[JinheonBaek/ResearchAgent](https://github.com/JinheonBaek/ResearchAgent)** — Iterative research idea generation over scientific literature with LLMs. Multi-agent review and feedback loops
  <sub>★ 60 · Python · source · pushed 2025-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/JinheonBaek/ResearchAgent.git`</sub>
- **[LitLLM/LitLLM](https://github.com/LitLLM/LitLLM)** — AI-powered literature review assistant using RAG for accurate, well-structured related-work sections in academic writing
  <sub>★ 52 · Python · Apache-2.0 · script · pushed 2026-05-07 · WSL2 · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/LitLLM/LitLLM/main/skill/install.sh | bash`</sub>
- **[AutoResearch-Factory/Agon](https://github.com/AutoResearch-Factory/Agon)** — End-to-end research orchestrator built on one cornerstone principle, Prompt Economy (reusable loops, not one-off prompts), plus five supporting rules; runs scientist/coder/auditor loops across 10+ disciplines, same reusable-loop lineage as autoresearch but scaled to full research programs
  <sub>★ 49 · Python · MIT · clone · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AutoResearch-Factory/Agon.git`</sub>
- **[kaust-ark/ARK](https://github.com/kaust-ark/ARK)** — ARK (Automatic Research Kit): idea + venue → paper pipeline orchestrating 6 agents — proposal analysis, literature search, Slurm experiments, LaTeX drafting, iterative peer review. Controlled via CLI, web dashboard, or Telegram
  <sub>★ 35 · Python · Apache-2.0 · docker · pushed 2026-09-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -d --name ark-webapp \`</sub>
- **[happyhappy-jun/writing-driven-autoresearch](https://github.com/happyhappy-jun/writing-driven-autoresearch)** — Autoresearch-style harness that keeps a submittable paper from the first minute and drives every experiment from the claims in that draft, looping modify → measure → verify → revise. 1st place at the Ralphthon@ICML 2026 autonomous-research hackathon
  <sub>★ 22 · Python · Apache-2.0 · source · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/happyhappy-jun/writing-driven-autoresearch.git`</sub>
- **[openags/Auto-Research](https://github.com/openags/auto-researcher)** — OpenAGS: Orchestrates a team of AI agents across the full research lifecycle — lit review, hypothesis generation, experiments, manuscript writing, and peer review
  <sub>★ 9 · TypeScript · MIT · clone · pushed 2026-04-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/openags/OpenAGS.git`</sub>
- **[wjc2830/Easy-AutoResearch-for-DeepLearning](https://github.com/wjc2830/Easy-AutoResearch-for-DeepLearning)** — Claude Code skill that runs an autoresearch-style, human-gated deep-learning loop across six roles, versioned experiments, and evidence-checked completion
  <sub>★ 1 · Python · MIT · clone · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wjc2830/Easy-AutoResearch-for-DeepLearning.git`</sub>
- **[AgentRxiv](https://agentrxiv.github.io/)** — Collaborative autonomous research framework where agent laboratories share a preprint server to build on each other's work iteratively
  <sub>website</sub>
  <sub>`https://agentrxiv.github.io/`</sub>
- **[Agent Laboratory](https://agentlaboratory.github.io/)** — Three-phase research pipeline: Literature Review → Experimentation → Report Writing, with specialized agents for each phase
  <sub>website</sub>
  <sub>`https://agentlaboratory.github.io/`</sub>

## Domain-Specific Adaptations

- **[chrisworsey55/atlas-gic](https://github.com/chrisworsey55/atlas-gic)** — Applies the autoresearch keep-or-revert loop to trading agents, optimizing prompts and portfolio orchestration against rolling Sharpe ratio instead of model loss
  <sub>★ 2.2k · Python · source · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chrisworsey55/atlas-gic.git`</sub>
- **[RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel)** — Applies the autoresearch loop to GPU kernel optimization: profile bottlenecks, edit one kernel, benchmark, keep or revert, repeat
  <sub>★ 1.6k · Python · MIT · clone · pushed 2026-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/RightNow-AI/autokernel.git`</sub>
- **[mattprusak/autoresearch-genealogy](https://github.com/mattprusak/autoresearch-genealogy)** — Applies the autoresearch pattern to genealogy, using structured prompts, archive guides, source checks, and vault workflows to iteratively expand and verify family-history research
  <sub>★ 1.2k · Ruby · MIT · source · pushed 2026-06-30</sub>
  <sub>`git clone https://github.com/mattprusak/autoresearch-genealogy.git`</sub>
- **[ArchishmanSengupta/autovoiceevals](https://github.com/ArchishmanSengupta/autovoiceevals)** — Uses adversarial callers plus keep-or-revert prompt edits to harden voice AI agents across Vapi, Smallest AI, and ElevenLabs
  <sub>★ 154 · Python · MIT · clone · pushed 2026-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ArchishmanSengupta/autovoiceevals.git`</sub>
- **[vlasenkoalexey/tpu_performance_autoresearch_wiki](https://github.com/vlasenkoalexey/tpu_performance_autoresearch_wiki)** — Applies the autoresearch keep-or-revert loop to TPU model performance (MFU / tokens-per-sec) on v6e hardware: profiles each run through an XProf MCP server, makes one model-code change per experiment, and keeps or reverts against measured MFU. Pairs the loop with a Karpathy-style LLM wiki for domain knowledge and per-experiment optimization traces; includes Llama3-8B and Qwen3-8B case studies acro
  <sub>★ 56 · HTML · MIT · source · pushed 2026-09-04</sub>
  <sub>`git clone https://github.com/vlasenkoalexey/tpu_performance_autoresearch_wiki.git`</sub>
- **[ElliotXie/autozyme](https://github.com/ElliotXie/autozyme)** — Multi-agent framework that applies the autoresearch keep-or-revert loop to CPU-side scientific software: profile a target function, generate one optimization candidate, benchmark for speed while preserving the original outputs, keep or revert, repeat
  <sub>★ 50 · Python · MIT · pip · pushed 2026-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install autozyme`</sub>
- **[Rkcr7/autoresearch-sudoku](https://github.com/Rkcr7/autoresearch-sudoku)** — Enhanced autoresearch workflow where an AI agent iteratively rewrites and benchmarks a Rust sudoku solver, ultimately beating leading human-built solvers on hard benchmark sets
  <sub>★ 5 · Rust · MIT · clone · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Rkcr7/autoresearch-sudoku`</sub>
- **[Agent-Analytics/autoresearch-growth](https://github.com/Agent-Analytics/autoresearch-growth)** — Applies autoresearch to landing-page positioning and A/B test candidates, using analytics snapshots and measured experiment results to seed subsequent rounds
  <sub>★ 4 · Python · source · pushed 2026-04-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Agent-Analytics/autoresearch-growth.git`</sub>
- **[jeongph/autospec](https://github.com/jeongph/autospec)** — Reads natural-language business rules and autonomously builds a Spring Boot service with tests via the keep-or-revert loop. Evaluates with Gradle build + JUnit XML. 119-line skeleton to 950 lines in 5 cycles
  <sub>★ 2 · Python · MIT · clone · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jeongph/autospec.git`</sub>

## LLM Evaluation Tools

- **[Langfuse](https://github.com/langfuse/langfuse)** — Open-source LLM observability with tracing, prompt management, and human annotation. ~7K+ ⭐
  <sub>★ 34.9k · TypeScript · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langfuse openai`</sub>
- **[Opik](https://github.com/comet-ml/opik)** — Evaluate, test, and ship LLM applications across dev and production lifecycles
  <sub>★ 22.2k · Python · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx add-mcp https://www.comet.com/opik/api/v1/mcp --name opik-mcp`</sub>
- **[DeepEval](https://github.com/confident-ai/deepeval)** — Open-source evaluation framework covering RAG, agents, and conversations with CI/CD integration. ~7K+ ⭐
  <sub>★ 18.4k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U deepeval`</sub>
- **[Ragas](https://github.com/vibrantlabsai/ragas)** — RAG evaluation with knowledge-graph-based test set generation and 30+ metrics. ~8K+ ⭐
  <sub>★ 15.8k · Python · Apache-2.0 · pip · pushed 2026-02-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ragas`</sub>
- **[Arize AI / Phoenix](https://github.com/Arize-ai/phoenix)** — Real-time LLM monitoring with drift detection and tracing
  <sub>★ 11.6k · Python · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @arizeai/phoenix-cli setup`</sub>
- **[TruLens](https://github.com/truera/trulens)** — Evaluating and explaining LLM apps; tracks hallucinations, relevance, groundedness
  <sub>★ 3.6k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install trulens`</sub>
- **[InspectAI](https://github.com/UKGovernmentBEIS/inspect_ai)** — Purpose-built for evaluating agents against benchmarks (UK AISI)
  <sub>★ 2.8k · Python · MIT · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/UKGovernmentBEIS/inspect_ai.git`</sub>
- **[EvalView](https://github.com/hidai25/eval-view)** — CLI tool for testing multi-step AI agents with YAML test cases, regression detection, and production monitoring
  <sub>★ 135 · Python · Apache-2.0 · pip · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evalview`</sub>
- **[LangSmith](https://smith.langchain.com/)** — LangChain's platform for debugging, testing, evaluating, and monitoring LLM applications
  <sub>website</sub>
  <sub>`https://smith.langchain.com/`</sub>
- **[Braintrust](https://www.braintrust.dev/)** — End-to-end AI evaluation platform, SOC2 Type II certified
  <sub>website</sub>
  <sub>`https://www.braintrust.dev/`</sub>

## Prompt Management and Testing

- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — Open-source CLI for testing, evaluating, and red-teaming LLM prompts. YAML configs, CI/CD integration, adversarial testing. ~9K+ ⭐
  <sub>★ 25.3k · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g promptfoo`</sub>
- **[OpenPrompt](https://github.com/thunlp/OpenPrompt)** — Open-source framework for prompt-learning research
  <sub>★ 4.9k · Python · Apache-2.0 · pip · pushed 2024-07-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openprompt`</sub>
- **[Agenta](https://github.com/Agenta-AI/agenta)** — Open-source LLM developer platform for prompt management, evaluation, human feedback, and deployment
  <sub>★ 4.8k · TypeScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Agenta-AI/agenta.git`</sub>
- **[Promptify](https://github.com/promptslab/Promptify)** — Solve NLP Problems with LLM's &amp; Easily generate different NLP Task prompts for popular generative models like GPT, PaLM, and more with Promptify
  <sub>★ 4.6k · Python · Apache-2.0 · pip · pushed 2026-03-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install promptify`</sub>
- **[LMQL](https://github.com/eth-sri/lmql)** — A query language for LLMs making complex prompt logic programmable
  <sub>★ 4.2k · Python · Apache-2.0 · pip · pushed 2025-05-22 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pip install lmql`</sub>
- **[Prompt Source](https://github.com/bigscience-workshop/promptsource)** — Toolkit for creating, sharing, and using natural language prompts
  <sub>★ 3k · Python · Apache-2.0 · pip · pushed 2023-10-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install promptsource`</sub>
- **[ChainForge](https://github.com/ianarawjo/ChainForge)** — Visual toolkit for building, testing, and comparing LLM prompt responses without code
  <sub>★ 3k · TypeScript · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install chainforge`</sub>
- **[Prompt Engine](https://github.com/microsoft/prompt-engine)** — NPM utility library for creating and maintaining prompts for LLMs (Microsoft)
  <sub>★ 2.8k · TypeScript · MIT · source · pushed 2023-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/prompt-engine.git`</sub>
- **[PromptInject](https://github.com/agencyenterprise/PromptInject)** — Framework for quantitative analysis of LLM robustness to adversarial prompt attacks
  <sub>★ 525 · Python · MIT · source · pushed 2026-04-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agencyenterprise/PromptInject.git`</sub>
- **[LynxPrompt](https://github.com/GeiserX/LynxPrompt)** — Self-hostable platform for managing AI IDE config files (.cursorrules, CLAUDE.md, copilot-instructions.md). Web UI, REST API, CLI, and federated blueprint marketplace for 30+ AI coding assistants
  <sub>★ 47 · TypeScript · Apache-2.0 · choco · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`choco install lynxprompt`</sub>
- **[PromptLayer](https://promptlayer.com/)** — Version, test, and monitor every prompt and agent with robust evals, tracing, and regression sets
  <sub>website</sub>
  <sub>`https://promptlayer.com/`</sub>
- **[Helicone](https://helicone.ai/)** — Production prompt monitoring and optimization platform
  <sub>website</sub>
  <sub>`https://helicone.ai/`</sub>
- **[LangGPT](https://github.com/langgpt/LangGPT)** — Framework for structured and meta-prompt design. 10K+ ⭐
  <sub>unavailable</sub>
- **[Promptotype](https://www.promptotype.io)** — Platform for developing, testing, and managing structured LLM prompts
  <sub>website</sub>
  <sub>`https://www.promptotype.io`</sub>
- **[PromptPanda](https://promptpanda.io)** — AI-powered prompt management system for streamlining prompt workflows
  <sub>website</sub>
  <sub>`https://promptpanda.io`</sub>
- **[Promptimize AI](https://promptimize.ai)** — Browser extension to automatically improve user prompts for any AI model
  <sub>website</sub>
  <sub>`https://promptimize.ai`</sub>
- **[PROMPTMETHEUS](https://promptmetheus.com)** — Web-based "Prompt Engineering IDE" for iteratively creating and running prompts
  <sub>website</sub>
  <sub>`https://promptmetheus.com`</sub>
- **[Better Prompt](https://github.com/krrishdholakia/betterprompt)** — Test suite for LLM prompts before pushing to production
  <sub>unavailable</sub>
- **[flompt](https://flompt.dev)** — Visual AI prompt builder that decomposes prompts into 12 semantic blocks (role, context, constraints, examples, etc.) and compiles them into optimized XML. Browser extension for ChatGPT/Claude/Gemini, and MCP server for Claude Code agents. Free, open-source
  <sub>website</sub>
  <sub>`https://flompt.dev`</sub>

## Red Teaming and Prompt Security

- **[Garak (NVIDIA)](https://github.com/NVIDIA/garak)** — LLM vulnerability scanner for hallucination, injection, and jailbreaks — the "nmap for LLMs." ~3K+ ⭐
  <sub>★ 9.3k · Python · Apache-2.0 · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NVIDIA/garak.git`</sub>
- **[NeMo Guardrails (NVIDIA)](https://github.com/NVIDIA-NeMo/Guardrails)** — Programmable guardrails for conversational systems. ~5K+ ⭐
  <sub>★ 7.2k · Python · source · pushed 2026-09-18 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/NVIDIA/NeMo-Guardrails.git`</sub>
- **[Purple Llama (Meta)](https://github.com/meta-llama/PurpleLlama)** — Open-source LLM safety evaluation including CyberSecEval
  <sub>★ 4.4k · Python · source · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/meta-llama/PurpleLlama.git`</sub>
- **[LLM Guard](https://github.com/protectai/llm-guard)** — Security toolkit for LLM I/O validation. ~2K+ ⭐
  <sub>★ 3.2k · Python · MIT · pip · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llm-guard`</sub>
- **[DeepTeam](https://github.com/confident-ai/deepteam)** — 40+ vulnerabilities, 10+ attack methods, OWASP Top 10 support
  <sub>★ 2.9k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U deepteam`</sub>
- **[Rebuff](https://github.com/protectai/rebuff)** — Open-source tool for detection and prevention of prompt injection
  <sub>★ 1.5k · TypeScript · Apache-2.0 · pip · pushed 2024-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install rebuff`</sub>
- **[GPTFuzz](https://github.com/hubertyoo/GPTFuzz)** — Automated jailbreak template generation achieving >90% success rates
  <sub>★ 611 · Python · MIT · source · pushed 2026-02-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sherdencooper/GPTFuzz.git`</sub>
- **[AgentSeal](https://github.com/getagentseal/agentseal)** — "Open-source scanner that runs 150 attack probes to test AI agents for prompt injection and extraction vulnerabilities."
  <sub>★ 374 · Python · pip · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentseal # or: npm install agentseal`</sub>
- **[PyRIT (Microsoft)](https://github.com/Azure/PyRIT)** — Python Risk Identification Tool for automated red-teaming. ~3K+ ⭐
  <sub>★ 116 · MIT · source · pushed 2026-03-25</sub>
  <sub>`git clone https://github.com/Azure/PyRIT.git`</sub>
- **[Guardrails AI](https://www.guardrailsai.com)** — Define strict output formats (JSON schemas) to ensure system reliability
  <sub>website</sub>
  <sub>`https://www.guardrailsai.com`</sub>
- **[Lakera](https://lakera.ai/)** — AI security platform for real-time prompt injection detection
  <sub>website</sub>
  <sub>`https://lakera.ai/`</sub>

## Evaluation &amp; Benchmarks

- **[THUDM/AgentBench](https://github.com/THUDM/AgentBench)** — Comprehensive benchmark for LLM-as-Agent evaluation across 8 distinct environments. ICLR 2024
  <sub>★ 3.7k · Python · Apache-2.0 · source · pushed 2026-02-08 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/THUDM/AgentBench.git`</sub>
- **[OpenAI/mle-bench](https://github.com/openai/mle-bench)** — OpenAI's benchmark for measuring how well AI agents perform at ML engineering
  <sub>★ 1.7k · Python · source · pushed 2026-04-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openai/mle-bench.git`</sub>
- **[snap-stanford/MLAgentBench](https://github.com/snap-stanford/MLAgentBench)** — Benchmark suite for evaluating AI agents on ML experimentation tasks. 13 tasks from CIFAR-10 to BabyLM
  <sub>★ 354 · Python · MIT · docker · pushed 2024-06-19 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it --user root -v ${PWD}:/MLAgentBench -w /MLAgentBench qhwang123/researchassistant:latest`</sub>
- **[gersteinlab/ML-Bench](https://github.com/gersteinlab/ML-Bench)** — Evaluates LLMs and agents for ML tasks on repository-level code
  <sub>★ 316 · Python · MIT · docker · pushed 2025-07-31 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it -v ML_Bench:/deep_data public.ecr.aws/i5g0m1f6/ml-bench /bin/bash`</sub>
- **[chchenhui/mlrbench](https://github.com/chchenhui/mlrbench)** — MLR-Bench: Evaluating AI agents on open-ended ML research. 201 tasks from NeurIPS/ICLR/ICML workshops
  <sub>★ 36 · Python · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/chchenhui/mlrbench.git`</sub>

## Other Notable Repositories

- **[Awesome ChatGPT Prompts / Prompts.chat](https://github.com/f/prompts.chat)** — World's largest open-source prompt library. 1000s of prompts for all major models
  <sub>★ 170.9k · HTML · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx prompts.chat new my-prompt-library`</sub>
- **[Prompt Engineering Guide (DAIR.AI)](https://github.com/dair-ai/Prompt-Engineering-Guide)** — The definitive open-source guide and resource hub. 3M+ learners. ~55K+ ⭐
  <sub>★ 78.5k · MDX · MIT · source · pushed 2026-03-11</sub>
  <sub>`git clone https://github.com/dair-ai/Prompt-Engineering-Guide.git`</sub>
- **[OpenAI Cookbook](https://github.com/openai/openai-cookbook)** — Official recipes for prompts, tools, RAG, and evaluations
  <sub>★ 76.1k · Jupyter Notebook · MIT · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/openai/openai-cookbook.git`</sub>
- **[Embedchain](https://github.com/mem0ai/mem0)** — Framework to create ChatGPT-like bots over your dataset
  <sub>★ 65.8k · Python · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @mem0/cli # or: pip install mem0-cli`</sub>
- **[12-Factor Agents](https://github.com/humanlayer/12-factor-agents)** — Principles for building production-grade LLM-powered software. ~17K+ ⭐
  <sub>★ 26.3k · TypeScript · source · pushed 2025-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/humanlayer/12-factor-agents.git`</sub>
- **[Context Engineering Repository](https://github.com/jasontang-ai/Context-Engineering)** — First-principles handbook for moving beyond prompt engineering to context design
  <sub>★ 9.3k · Python · MIT · source · pushed 2026-02-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/davidkimai/Context-Engineering.git`</sub>
- **[NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)** — 22 hands-on Jupyter Notebook tutorials. ~3K+ ⭐
  <sub>★ 7.9k · Jupyter Notebook · clone · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/NirDiamant/Prompt_Engineering.git`</sub>
- **[ThoughtSource](https://github.com/OpenBioLink/ThoughtSource)** — Framework for the science of machine thinking
  <sub>★ 1k · Jupyter Notebook · MIT · clone · pushed 2024-12-16</sub>
  <sub>`git clone git@github.com:OpenBioLink/ThoughtSource.git`</sub>
- **[AI Agent System Prompts Library](https://github.com/tallesborges/agentic-system-prompts)** — Collection of system prompts from production AI coding agents (Claude Code, Gemini CLI, Cline, Aider, Roo Code)
  <sub>★ 184 · Jinja · source · pushed 2025-08-04</sub>
  <sub>`git clone https://github.com/tallesborges/agentic-system-prompts.git`</sub>
- **[OpenPaw](https://github.com/daxaur/openpaw)** — CLI tool (npx pawmode) that turns Claude Code into a personal assistant by generating system prompts (CLAUDE.md + SOUL.md) with personality, memory, and 38 skill routers
  <sub>★ 167 · TypeScript · MIT · source · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/daxaur/openpaw.git`</sub>
- **[Awesome Vibe Coding](https://github.com/taskade/awesome-vibe-coding)** — Curated list of 245+ tools and resources for building software through natural language prompts
  <sub>★ 134 · CC-BY-4.0 · npx · pushed 2026-09-11 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx -y @taskade/mcp-server`</sub>
- **[Think Better](https://github.com/HoangTheQuyen/think-better)** — Open-source CLI that permanently injects 10 structured decision frameworks (MECE, Issue Trees, Pre-Mortems) and 12 cognitive bias detectors into AI assistant prompts. Go, MIT
  <sub>★ 120 · Python · MIT · psh · pushed 2026-04-05 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/HoangTheQuyen/think-better/main/install.ps1 | iex`</sub>
- **[Promptext](https://github.com/1broseidon/promptext)** — Extracts and formats code context for AI prompts with token counting
  <sub>★ 22 · Go · MIT · psh · pushed 2026-04-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm chain.sh/promptext/scripts/install.ps1 | iex`</sub>
- **[Price Per Token](https://pricepertoken.com/)** — Compare LLM API pricing across 200+ models
  <sub>website</sub>
  <sub>`https://pricepertoken.com/`</sub>

## Related Resources

- **[VoltAgent/awesome-ai-agent-papers](https://github.com/VoltAgent/awesome-ai-agent-papers)** — Curated AI agent papers from 2026 — agent engineering, memory, evaluation, workflows, and autonomous systems
  <sub>★ 1.8k · MIT · source · pushed 2026-09-21 · Win?</sub>
  <sub>`git clone https://github.com/VoltAgent/awesome-ai-agent-papers.git`</sub>
- **[masamasa59/ai-agent-papers](https://github.com/masamasa59/ai-agent-papers)** — AI agent research papers updated biweekly via automated arxiv search with curated selection
  <sub>★ 1.7k · Python · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/masamasa59/ai-agent-papers.git`</sub>
- **[tmgthb/Autonomous-Agents](https://github.com/tmgthb/Autonomous-Agents)** — Autonomous agents research papers, updated daily
  <sub>★ 1.4k · MIT · source · pushed 2026-06-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tmgthb/Autonomous-Agents.git`</sub>
- **[WecoAI/awesome-autoresearch](https://github.com/WecoAI/awesome-autoresearch)** — Curated list of AutoResearch use cases with verifiable traces and progress charts, organized by domain (LLM training, GPU kernels, voice agents, trading, etc.)
  <sub>★ 1.1k · CC0-1.0 · source · pushed 2026-07-30 · Win? · macOS?</sub>
  <sub>`git clone https://github.com/WecoAI/awesome-autoresearch.git`</sub>
- **[ai-agents-2030/awesome-deep-research-agent](https://github.com/WuizaKaseiyo/awesome-deep-research-agent)** — Curated list of deep research agent papers and systems
  <sub>★ 638 · source · pushed 2025-09-18</sub>
  <sub>`git clone https://github.com/ai-agents-2030/awesome-deep-research-agent.git`</sub>
- **[HKUST-KnowComp/Awesome-LLM-Scientific-Discovery](https://github.com/HKUST-KnowComp/Awesome-LLM-Scientific-Discovery)** — EMNLP 2025 survey on LLMs in scientific discovery
  <sub>★ 439 · MIT · source · pushed 2026-07-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/HKUST-KnowComp/Awesome-LLM-Scientific-Discovery.git`</sub>
- **[YoungDubbyDu/LLM-Agent-Optimization](https://github.com/YoungDubbyDu/Awesome-LLM-Agent-Optimization-Papers)** — Papers on LLM agent optimization methods
  <sub>★ 245 · source · pushed 2026-09-12</sub>
  <sub>`git clone https://github.com/YoungDubbyDu/LLM-Agent-Optimization.git`</sub>
- **[openags/Awesome-AI-Scientist-Papers](https://github.com/openags/Awesome-AI-Scientist-Papers)** — Collection of AI Scientist / Robot Scientist papers
  <sub>★ 173 · MIT · source · pushed 2026-09-15</sub>
  <sub>`git clone https://github.com/openags/Awesome-AI-Scientist-Papers.git`</sub>
- **[agenticscience.github.io](https://agenticscience.github.io/)** — Survey: "From AI for Science to Agentic Science: A Survey on Autonomous Scientific Discovery."
  <sub>website</sub>
  <sub>`https://agenticscience.github.io/`</sub>
- **[dspy.ai/GEPA](https://dspy.ai/api/optimizers/GEPA/overview/)** — DSPy integration of GEPA reflective prompt optimizer for compound AI systems
  <sub>website</sub>
  <sub>`https://dspy.ai/api/optimizers/GEPA/overview/`</sub>
- **[OpenAI Cookbook: Self-Evolving Agents](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining)** — Cookbook for autonomous agent retraining using GEPA-style reflective evolution
  <sub>website</sub>
  <sub>`https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining`</sub>


---

Snapshot 2026-09-21. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
