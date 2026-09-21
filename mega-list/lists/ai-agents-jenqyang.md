# AI Agents (Jenqyang)

A collection of autonomous agents 🤖️ powered by LLM.

Curated by **[Jenqyang/Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

279 entries · 264 distinct repos · 12 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/langchain-ai/langchain"><img src="https://opengraph.githubassets.com/1/langchain-ai/langchain" width="260"></a> | <a href="https://github.com/browser-use/browser-use"><img src="https://github.com/user-attachments/assets/135885e8-1141-4e10-b719-bf690ae7d260" width="260"></a> | <a href="https://github.com/microsoft/autogen"><img src="https://media.githubusercontent.com/media/microsoft/autogen/refs/heads/main/python/packages/autogen-studio/docs/ags_screen.png" width="260"></a> |
| **[langchain](https://github.com/langchain-ai/langchain)**<br>★ 146.8k | **[browser-use](https://github.com/browser-use/browser-use)**<br>★ 115.7k | **[AutoGen](https://github.com/microsoft/autogen)**<br>★ 61.1k |
| <a href="https://github.com/run-llama/llama_index"><img src="https://opengraph.githubassets.com/1/run-llama/llama_index" width="260"></a> | <a href="https://github.com/agno-agi/agno"><img src="https://github.com/user-attachments/assets/6d21e6bc-111f-4b81-ba29-6550fead89b2" width="260"></a> | <a href="https://github.com/openai/openai-agents-python"><img src="https://cdn.openai.com/API/docs/images/orchestration.png" width="260"></a> |
| **[llama_index](https://github.com/run-llama/llama_index)**<br>★ 52.3k | **[Agno](https://github.com/agno-agi/agno)**<br>★ 42.3k | **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)**<br>★ 29.6k |

## Contents

- [Frameworks](#frameworks) (58)
- [Autonomous Agent Task Solver Projects](#autonomous-agent-task-solver-projects) (57)
- [Multi-Agent Task Solver Projects](#multi-agent-task-solver-projects) (27)
- [Agent Society Simulation](#agent-society-simulation) (7)
- [Tools](#tools) (54)
- [Advanced Components](#advanced-components) (4)
- [Benchmark/Evaluator](#benchmarkevaluator) (21)
- [Platforms/API](#platformsapi) (21)
- [Survey](#survey) (3)
- [Paper-List Repo](#paper-list-repo) (7)
- [Reference Repo](#reference-repo) (13)
- [Blog](#blog) (7)

## Frameworks

- **[langchain](https://github.com/langchain-ai/langchain)** — Building applications with LLMs through composability ⚡
  <sub>★ 146.8k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/langchain.git`</sub>
- **[browser-use](https://github.com/browser-use/browser-use)** — Enable AI agents to control websites through a structured and reproducible browser interface
  <sub>★ 115.7k · Python · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browser-use/browser-use.git`</sub>
- **[AutoGen](https://github.com/microsoft/autogen)** — AutoGen is a framework that enables the development of LLM applications using multiple agents that can converse with each other to solve tasks
  <sub>★ 61.1k · Python · CC-BY-4.0 · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "autogen-agentchat" "autogen-ext[openai]"`</sub>
- **[llama_index](https://github.com/run-llama/llama_index)** — LlamaIndex (formerly GPT Index) is a data framework for your LLM applications
  <sub>★ 52.3k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llama-index-core`</sub>
- **[Agno](https://github.com/agno-agi/agno)** — Build multi-agent systems with memory, knowledge, and tool integrations in Python
  <sub>★ 42.3k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agno-agi/agno.git`</sub>
- **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** — Open-source SDK for building agentic workflows with tool calling, handoffs, and tracing in Python
  <sub>★ 29.6k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openai-agents`</sub>
- **[smolagents](https://github.com/huggingface/smolagents)** — Minimal agent framework from Hugging Face focused on tool-calling and code-executing agents
  <sub>★ 29.4k · Python · Apache-2.0 · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "smolagents[toolkit]"`</sub>
- **[Mastra](https://github.com/mastra-ai/mastra)** — Mastra is an opinionated TypeScript framework that helps you build AI applications and features quickly
  <sub>★ 28.2k · TypeScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git`</sub>
- **[SuperAGI](https://github.com/TransformerOptimus/SuperAGI)** — A dev-first open source autonomous AI agent framework. Enabling developers to build, manage &amp; run useful autonomous agents quickly and reliably
  <sub>★ 17.7k · Python · MIT · clone · pushed 2025-01-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/TransformerOptimus/SuperAGI.git`</sub>
- **[Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)** — Agent framework based on Qwen with tool use, RAG, and code interpreter support
  <sub>★ 17.1k · Python · Apache-2.0 · pip · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "qwen-agent[gui,rag,code_interpreter,mcp]"`</sub>
- **[Agent Framework](https://github.com/microsoft/agent-framework)** — Microsoft open-source framework for building, orchestrating, and running AI agents with workflow primitives
  <sub>★ 13.7k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-framework`</sub>
- **[VoltAgent](https://github.com/VoltAgent/voltagent)** — An open source TypeScript Framework for building AI agents with built-in LLM observability
  <sub>★ 10.7k · TypeScript · MIT · source · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/VoltAgent/voltagent.git`</sub>
- **[awesome-langchain](https://github.com/kyrolabs/awesome-langchain)** — Awesome list of tools and projects with the awesome LangChain framework
  <sub>★ 9.5k · CC0-1.0 · source · pushed 2026-08-11</sub>
  <sub>`git clone https://github.com/kyrolabs/awesome-langchain.git`</sub>
- **[PraisonAI](https://github.com/MervinPraison/PraisonAI)** — Production-ready Multi-AI Agents framework with self-reflection. Fastest agent instantiation (3.77μs), 100+ LLM support, MCP integration, agentic workflows (route/parallel/loop/repeat), built-in memory, and both Python &amp; JavaScript SDKs
  <sub>★ 9.1k · Python · MIT · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install praisonai`</sub>
- **[mcp-agent](https://github.com/lastmile-ai/mcp-agent)** — Lightweight framework for building and deploying agents on top of the Model Context Protocol (MCP)
  <sub>★ 8.5k · Python · Apache-2.0 · uv · pushed 2026-01-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-agent init --template basic # Scaffold a new project`</sub>
- **[Upsonic](https://github.com/Upsonic/Upsonic)** — Upsonic is a reliable agent framework supporting MCP, offering trusted agent workflows with verification layers
  <sub>★ 8k · Python · MIT · source · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upsonic/upsonic.git`</sub>
- **[Agent Squad](https://github.com/2FastLabs/agent-squad)** — AWS open-source framework for orchestrating specialist agents with intent routing and multi-agent collaboration patterns
  <sub>★ 7.8k · Swift · Apache-2.0 · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "agent-squad[aws]" # or [anthropic], [openai], [all] — see the docs`</sub>
- **[Strands Agents](https://github.com/strands-agents/harness-sdk)** — Open-source SDK for building AI agents in Python and TypeScript, with an in-process agent loop, tools, MCP, multi-agent patterns, and pluggable model providers
  <sub>★ 7.4k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install strands-agents strands-agents-tools`</sub>
- **[Swarms](https://github.com/kyegomez/swarms)** — Enterprise-grade multi-agent framework for orchestrating intelligent AI agents at scale. Designed for production environments with hierarchical swarms, parallel processing, and robust infrastructure
  <sub>★ 7.2k · Python · Apache-2.0 · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/kyegomez/swarms.git`</sub>
- **[Open Multi-Agent](https://github.com/open-multi-agent/open-multi-agent)** — TypeScript-native framework for multi-agent systems that plans task DAGs from goals at runtime, with approval gates, tracing, evaluation, checkpoints, and resume support. Requires Node.js 20+
  <sub>★ 6.9k · TypeScript · MIT · source · pushed 2026-09-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/open-multi-agent/open-multi-agent.git`</sub>
- **[AppAgent](https://github.com/TencentQQGYLab/AppAgent)** — A novel LLM-based multimodal agent framework designed to operate smartphone applications
  <sub>★ 6.9k · Python · MIT · source · pushed 2025-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mnotgod96/AppAgent.git`</sub>
- **[superagent](https://github.com/superagent-ai/superagent)** — The open framework for building AI Assistants
  <sub>★ 6.8k · TypeScript · MIT · source · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/homanp/superagent.git`</sub>
- **[TaskWeaver](https://github.com/microsoft/TaskWeaver)** — A code-first agent framework for seamlessly planning and executing data analytics tasks
  <sub>★ 6.2k · Python · MIT · pip · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/microsoft/TaskWeaver@<TAG>`</sub>
- **[agents](https://github.com/aiwaves-cn/agents)** — An Open-source Framework for Autonomous Language Agents
  <sub>★ 6k · Python · Apache-2.0 · pip · pushed 2024-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/aiwaves-cn/agents@master`</sub>
- **[modelscope-agent](https://github.com/modelscope/ms-agent)** — An agent framework connecting models in ModelScope with the world
  <sub>★ 4.4k · Python · Apache-2.0 · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/modelscope/ms-agent.git`</sub>
- **[OpenAgents](https://github.com/openagents-org/openagents)** — Open-source platform for building AI agent networks with multi-protocol support (WebSocket, gRPC, HTTP, MCP, A2A) and multi-agent orchestration
  <sub>★ 4.1k · TypeScript · Apache-2.0 · psh · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://openagents.org/install.ps1 | iex`</sub>
- **[AgentFlow](https://github.com/lupantech/AgentFlow)** — Trainable multi-agent framework coordinating planner, executor, verifier, generator via in-the-flow optimization
  <sub>★ 2k · Python · MIT · source · pushed 2026-02-08 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/lupantech/AgentFlow.git`</sub>
- **[AutoChain](https://github.com/Forethought-Technologies/AutoChain)** — Build lightweight, extensible, and testable LLM Agents
  <sub>★ 1.9k · Python · MIT · pip · pushed 2025-12-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install autochain`</sub>
- **[KaibanJS](https://github.com/kaiban-ai/KaibanJS)** — KaibanJS is a JavaScript-native framework for building and managing multi-agent systems with a Kanban-inspired approach
  <sub>★ 1.5k · TypeScript · MIT · npx · pushed 2026-05-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx kaibanjs@latest init`</sub>
- **[LightAgent](https://github.com/wanxingai/LightAgent)** — Lightweight Python agent framework with memory, MCP/SSE integration, reusable Skills, Tree-of-Thought planning, OpenAI-compatible streaming, and LightSwarm multi-agent collaboration
  <sub>★ 1.2k · Python · Apache-2.0 · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lightagent`</sub>
- **[Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS)** — Apache-2.0 local-first Agent Operation Environment for portable agent and team packages, cross-host orchestration, MCP/A2A, and verification gates
  <sub>★ 1.1k · Python · Apache-2.0 · script · pushed 2026-09-18 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/agentlas-ai/Agentlas-OS/main/scripts/install-all-runtimes.sh | bash`</sub>
- **[Aeon](https://github.com/aeonfun/aeon)** — Autonomous agent framework that runs unattended on GitHub Actions, triggered by cron schedules or repository events. Dispatches skills to six coding-agent harnesses behind one contract (Claude Code, Grok, Codex, Pi, Vibe, Kimi), defines agent behavior as Markdown skills, persists memory in the git repository, evaluates its own run output to revise underperforming skills, and ships an MCP server ex
  <sub>★ 747 · Shell · MIT · clone · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/<you>/aeon`</sub>
- **[fractal](https://github.com/plasma-ai/fractal)** — Hierarchical agent loops that self-organize into a tree, where each node iterates in its own git worktree and spawns children for subtasks, bounded by caps on depth, cost, and time
  <sub>★ 732 · Python · Apache-2.0 · uv · pushed 2026-09-21 · WSL2 · macOS? · Linux</sub>
  <sub>`uv tool install plasma-fractal --with-executables-from plasma-wiki`</sub>
- **[SwarmClaw](https://github.com/swarmclawai/swarmclaw)** — Self-hosted multi-agent runtime with MCP client and server support, 23+ LLM providers, persistent memory, skills, schedules, sub-agent spawning, and connectors for Discord, Slack, Telegram, WhatsApp, Teams, and Matrix. Electron desktop app, CLI, and Docker
  <sub>★ 679 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @swarmclawai/swarmclaw`</sub>
- **[AgentSquare](https://github.com/tsinghua-fib-lab/AgentSquare)** — Automatic LLM Agent Search In Modular Design Space
  <sub>★ 232 · HTML · clone · pushed 2025-11-04</sub>
  <sub>`git clone https://github.com/tsinghua-fib-lab/AgentSquare.git`</sub>
- **[AIWG](https://github.com/jmagly/aiwg)** — Deploys reusable agents, skills, rules, and governed workflows into the native project paths of multiple AI coding platforms
  <sub>★ 211 · TypeScript · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g aiwg`</sub>
- **[LLMling-Agent](https://github.com/phil65/agentpool)** — Multi-agent workflows and complex Agent interactions, both via YAML manifest and programmatic usage. Pydantic-AI and LiteLLM backends with human-in-the-loop integration
  <sub>★ 188 · Python · MIT · source · pushed 2026-04-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/phil65/llmling-agent.git`</sub>
- **[Voice Lab](https://github.com/saharmor/voice-lab)** — A comprehensive testing and evaluation framework for voice agents across language models, prompts, and agent personas
  <sub>★ 176 · Python · Apache-2.0 · clone · pushed 2025-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/saharmor/voice-lab.git`</sub>
- **[OpenHermit](https://github.com/HCF-STUDIOS/openhermit)** — Open-source platform for deploying AI agents as production services. Internal state (memory, sessions, skills, MCP, schedules, secrets) lives in Postgres; per-agent Docker workspaces. Fleet ops via single commands (hermit skills enable ... --all). CLI, Web UI, Telegram/Discord/Slack. MIT, TypeScript
  <sub>★ 84 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g openhermit`</sub>
- **[Talon](https://github.com/dylanneve1/talon)** — Self-hosted, multi-frontend agentic harness that runs one persistent agent across Telegram, Discord, Teams, and the terminal. Pluggable backends (Claude, OpenAI Agents, Codex, Kilo, OpenCode), full MCP tool access, and always-on background agents — Goals, Heartbeat, and Dream — backed by a long-term memory palace. MIT, TypeScript
  <sub>★ 84 · TypeScript · MIT · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx talon setup`</sub>
- **[ORCA Agent Skills](https://github.com/gfernandf/agent-skills)** — Python framework with 122+ executable AI agent skills, YAML capability contracts, DAG scheduler, MCP server, and adapters for LangChain, CrewAI, and Semantic Kernel
  <sub>★ 66 · Python · Apache-2.0 · clone · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gfernandf/agent-skills.git`</sub>
- **[FastAgent](https://github.com/fastagent-sh/fastagent)** — Serving layer that turns an existing agent directory (persona.md, skills/, tools/, channels/) into a live service without a rewrite: embed it behind a route in a Next/Hono/Node app, or run it as a GitHub, Telegram, Slack, or HTTP/SSE service with cron schedules. Engine-, model-, and host-neutral around a single invoke contract. MIT, TypeScript
  <sub>★ 63 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @fastagent-sh/fastagent # CLI: fastagent init/dev/start/...`</sub>
- **[Hector](https://github.com/verikod/hector)** — Pure A2A-Native Declarative AI Agent Platform
  <sub>★ 60 · Go · MIT · psh · pushed 2026-05-18 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://gohector.dev/install.ps1 | iex`</sub>
- **[pydantic-collab](https://github.com/Unfold-Security/pydantic-collab)** — A multi-agent framework powered by Pydantic-AI, enabling collaboration via handoffs and consultations. Supports pre-built and custom agent topologies, shared memory, and Logfire observability
  <sub>★ 33 · Python · MIT · pip · pushed 2026-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pydantic-collab`</sub>
- **[Corellis](https://github.com/CorellisOrg/Corellis)** — Open-source multi-agent governance framework for OpenClaw. Goal decomposition (GoalOps), 4-layer memory system, fleet-wide learning, and approval workflows. Production-tested with 28 agents
  <sub>★ 29 · Shell · MIT · clone · pushed 2026-04-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/CorellisOrg/corellis.git`</sub>
- **[MixedVoices](https://github.com/CarissaAI/mixedvoices)** — An Open source tool for analyzing and evaluating AI Voice agents. Track and visualize performance through call analysis and flow charts. Run complex simulations before pushing to production
  <sub>★ 28 · Python · Apache-2.0 · pip · pushed 2025-01-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mixedvoices`</sub>
- **[Reactive Agents](https://github.com/tylerjrbuell/reactive-agents-ts)** — Type-safe, observable TypeScript AI agent framework on Effect-TS; MCP-native, A2A multi-agent, 6 reasoning strategies, runs the same code on local Ollama 4B+ and frontier APIs
  <sub>★ 28 · TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`bunx create-reactive-agent my-app`</sub>
- **[AgentsKit](https://github.com/AgentsKit-io/agentskit)** — MIT-licensed, provider-neutral TypeScript toolkit with 25 focused packages for runtimes, tools, skills, memory, RAG, sandboxing, observability, evaluation, React, terminal UI, and CLI, built on a dependency-free core
  <sub>★ 26 · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @agentskit/cli`</sub>
- **[IronClaw](https://github.com/IronSecCo/ironclaw)** — Security-first, self-hosted AI agent platform. Each agent runs in a gVisor sandbox with no network, behind a human approval gateway (deny-by-default); per-session message queues are encrypted with SQLCipher, and releases ship cosign signatures, SBOMs, and build-provenance attestations. AGPLv3, written in Go
  <sub>★ 19 · Go · AGPL-3.0 · psh · pushed 2026-09-20 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/IronSecCo/ironclaw/main/scripts/install.ps1 | iex`</sub>
- **[selectools](https://github.com/johnnichev/selectools)** — Python agent framework for building composable AI applications with structured tool calling, HITL via generators, and 50+ built-in evaluators. Runs entirely in browser via visual builder at selectools.dev
  <sub>★ 11 · Python · Apache-2.0 · pip · pushed 2026-07-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "selectools[rag]" # FAISS + Qdrant + beautifulsoup4 (HTML CSS selectors)`</sub>
- **[Kite](https://github.com/beevr-labs/Kite)** — Python framework for building AI agents with built-in safety guardrails, and a CLI that generates multi-agent scripts from natural language
  <sub>★ 11 · Python · MIT · pip · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install kite-agent`</sub>
- **[zymi-core](https://github.com/metravod/zymi-core)** — YAML-first, event-sourced engine for LLM agents and pipelines. Declarative agents, tools, and connectors run as a DAG; every state change is a hash-chained event, enabling deterministic replay and fork-resume of any past run. Human-in-the-loop approval gates with policy and contracts, MCP and HTTP connectors. Distributed as a Python package
  <sub>★ 9 · Rust · MIT · uv · pushed 2026-09-08 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`uv tool install zymi-core # one-time`</sub>
- **[agent-express](https://github.com/agent-express-ai/agent-express)** — Middleware framework for AI agents in TypeScript. Express.js-style (ctx, next) composable hooks for retry, budget caps, memory compaction, tool approval, and observability
  <sub>★ 8 · TypeScript · MIT · npx · pushed 2026-05-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx create-agent-express # interactive wizard`</sub>
- **[TeDDy](https://github.com/atte500/TeDDy)** — Markdown-driven coding harness that structures agent work around TDD, hexagonal architecture, and vertical slicing. Python, AGPL-3.0
  <sub>★ 5 · Python · AGPL-3.0 · uv · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install teddy-cli`</sub>
- **[alive](https://github.com/marchantdev/alive)** — Minimal autonomous AI agent framework in a single Python file. Production-hardened through 80+ sessions of real autonomous operation with persistent memory, adaptive wake intervals, circuit breakers, and graceful degradation
  <sub>★ 3 · Python · MIT · pip · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install alive-framework`</sub>
- **[AgentLoop](https://github.com/mnifzied-create/agentloop)** — A Claude agent starter implementing the streaming tool-use loop in ~150 lines on Next.js with the official Anthropic SDK
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mnifzied-create/agentloop.git`</sub>
- **[crewAI](https://github.com/crewAIInc/crewAI)** — Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks
  <sub>source</sub>
  <sub>`git clone https://github.com/joaomdmoura/crewAI.git`</sub>
- **[AgentVerse](https://github.com/OpenBMB/AgentVerse)** — AgentVerse is designed to facilitate the deployment of multiple LLM-based agents in various applications. AgentVerse primarily provides two frameworks: task-solving and simulation
  <sub>source</sub>
  <sub>`git clone https://github.com/OpenBMB/AgentVerse.git`</sub>

## Autonomous Agent Task Solver Projects

- **[OpenClaw](https://github.com/openclaw/openclaw)** — Open-source personal AI assistant that runs locally across platforms and can take actions through chat channels and tools
  <sub>★ 390.2k · TypeScript · npm · pushed 2026-09-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g openclaw@latest --allow-scripts=openclaw`</sub>
- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** — AutoGPT is the vision of the power of AI accessible to everyone, to use and to build on
  <sub>★ 187.5k · Python · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Significant-Gravitas/AutoGPT.git`</sub>
- **[OpenDevin](https://github.com/OpenHands/OpenHands)** — a platform for autonomous software engineers, powered by AI and LLMs
  <sub>★ 88.7k · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[career-ops](https://github.com/career-ops-hq/career-ops)** — AI-powered job search orchestrator built on Claude Code. 14-skill pipeline that evaluates jobs, generates ATS-tailored PDFs, and tracks applications. Local-first, MIT
  <sub>★ 72.3k · JavaScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @santifer/career-ops`</sub>
- **[Cline](https://github.com/cline/cline)** — Open-source autonomous coding agent in VS Code for planning, coding, and tool use across real projects
  <sub>★ 68.9k · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g cline`</sub>
- **[gpt-engineer](https://github.com/AntonOsika/gpt-engineer)** — Specify what you want it to build, the AI asks for clarification, and then builds it
  <sub>★ 55.1k · Python · MIT · clone · pushed 2025-05-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gpt-engineer-org/gpt-engineer.git`</sub>
- **[AgentGPT](https://github.com/reworkd/AgentGPT)** — Assemble, configure, and deploy autonomous AI Agents in your browser
  <sub>★ 36.3k · TypeScript · GPL-3.0 · clone · pushed 2025-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/reworkd/AgentGPT.git`</sub>
- **[gpt-researcher](https://github.com/assafelovic/gpt-researcher)** — GPT based autonomous agent that does online comprehensive research on any given topic
  <sub>★ 29.6k · Python · Apache-2.0 · npx · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add assafelovic/gpt-researcher`</sub>
- **[JARVIS](https://github.com/microsoft/JARVIS)** — a system to connect LLMs with ML community
  <sub>★ 25.3k · Python · MIT · docker · pushed 2025-07-29 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -it -p 7860:7860 --platform=linux/amd64 registry.hf.space/microsoft-hugginggpt:latest python app.py`</sub>
- **[babyagi](https://github.com/yoheinakajima/babyagi)** — An example of an AI-powered task management system
  <sub>★ 22.4k · Python · pip · pushed 2026-01-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install babyagi`</sub>
- **[SWE-agent](https://github.com/SWE-agent/SWE-agent)** — Language agents for software engineering that can resolve GitHub issues in real repositories
  <sub>★ 20.4k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/princeton-nlp/SWE-agent.git`</sub>
- **[InkOS](https://github.com/Narcooo/inkos)** — Autonomous novel-writing CLI agent that orchestrates 10 specialized agents with 33-dimension continuity auditing, anti-AI-slop filtering, and style cloning for long-form fiction
  <sub>★ 10k · TypeScript · AGPL-3.0 · npm · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @actalk/inkos`</sub>
- **[XAgent](https://github.com/OpenBMB/XAgent)** — An Autonomous LLM Agent for Complex Task Solving
  <sub>★ 8.5k · Python · Apache-2.0 · source · pushed 2026-07-31 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/OpenBMB/XAgent.git`</sub>
- **[ShortGPT](https://github.com/RayVentura/ShortGPT)** — Experimental AI framework for automated short/video content creation
  <sub>★ 8k · Python · MIT · docker · pushed 2025-02-10 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 31415:31415 --env-file .env short_gpt_docker:latest`</sub>
- **[OpenAgent](https://github.com/the-open-agent/openagent)** — Self-hostable personal assistant with LLM + RAG, loops for desktop/browser/coding, MCP and many providers
  <sub>★ 5.6k · Go · Apache-2.0 · psh · pushed 2026-09-17 · Win · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/the-open-agent/openagent/master/scripts/install.ps1 | iex`</sub>
- **[DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze)** — Agentic LLM that autonomously completes the full data science pipeline from preparation to analyst-grade reports
  <sub>★ 4.6k · Python · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ruc-datalab/DeepAnalyze.git`</sub>
- **[Toprank](https://github.com/nowork-studio/notfair-plugin)** — Open-source Claude Code workflow for SEO, SEM, and Google Ads that inspects repositories, applies code changes, and automates search-growth diagnostics
  <sub>★ 3.8k · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx notfair@latest`</sub>
- **[CompozyOS](https://github.com/compozy/compozy)** — Self-hosted agent operating system: 26 providers, background loops and schedules, shared memory, approvals and an agent-to-agent network
  <sub>★ 2.8k · Go · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @compozy/cli@beta`</sub>
- **[Atomic Agent](https://github.com/AtomicBot-ai/atomic-agent)** — Local-first CLI and TUI coding agent that runs open-weight models entirely on your machine via a llama.cpp fork. 56 tools (browser, filesystem, git, memory, vision), MCP support, and a 5-layer local memory. macOS/Linux/Windows, MIT
  <sub>★ 2.5k · TypeScript · MIT · psh · pushed 2026-09-17 · macOS</sub>
  <sub>`irm https://atomicagent.io/install.ps1 | iex`</sub>
- **[BitFun](https://github.com/GCWing/OpenBitFun)** — Open-source coding agent with a Rust runtime, desktop and CLI interfaces, self-hosted multi-device control, and stateful Mini Apps
  <sub>★ 2.3k · Rust · MIT · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/GCWing/BitFun.git`</sub>
- **[Notte](https://github.com/nottelabs/notte)** — Notte is the fastest, most reliable framework for Browser Using Agents
  <sub>★ 2k · Python · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install notte`</sub>
- **[MLE-agent](https://github.com/MLSysOps/MLE-agent)** — Your intelligent companion for seamless AI engineering and research. 🔍 Integrate with arxiv and paper with code to provide better code/research plans 🧰 OpenAI, Anthropic, Ollama, etc supported. 🎆 Code RAG
  <sub>★ 1.6k · Python · MIT · pip · pushed 2026-07-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U mle-agent`</sub>
- **[AIDE](https://github.com/WecoAI/aideml)** — ML-engineering agent that uses tree search to optimize code against an eval metric, reaching human-level performance on Kaggle/MLE-bench
  <sub>★ 1.5k · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -U aideml`</sub>
- **[Ouroboros](https://github.com/razzant/ouroboros)** — Self-hosted general-purpose agent with durable identity and memory, reviewed self-modification, specialist subagent swarms, and desktop or headless operation
  <sub>★ 1.4k · Python · MIT · uv · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install "git+https://github.com/razzant/ouroboros.git@ouroboros"`</sub>
- **[Agent-E](https://github.com/EmergenceAI/Agent-E)** — Agent-E is an agent based system that aims to automate actions on the user's computer. At the moment it focuses on automation within the browser. The system is based on AutoGen agent framework
  <sub>★ 1.3k · Python · MIT · source · pushed 2026-05-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/EmergenceAI/Agent-E.git`</sub>
- **[KwaiAgents](https://github.com/KwaiKEG/KwaiAgents)** — A generalized information-seeking agent system with Large Language Models (LLMs)
  <sub>★ 1.2k · Python · clone · pushed 2024-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:KwaiKEG/KwaiAgents.git`</sub>
- **[Darkmoon](https://github.com/ASCIT31/Dark-Moon)** — Open source autonomous AI penetration testing platform where Markdown methodology agents orchestrate 80+ offensive security tools through MCP controlled execution with agentic reasoning, keeping an evidence trail per finding. Model agnostic, tuned for Claude Opus
  <sub>★ 957 · Python · GPL-3.0 · clone · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ASCIT31/Dark-Moon.git`</sub>
- **[ProAgent](https://github.com/OpenBMB/ProAgent)** — An LLM-based Agent for the New Automation Paradigm - Agentic Process Automation
  <sub>★ 865 · Python · Apache-2.0 · source · pushed 2023-12-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/OpenBMB/ProAgent.git`</sub>
- **[Agent Swarm](https://github.com/desplega-ai/agent-swarm)** — Self-hosted multi-agent system where a lead agent delegates tasks to specialized workers with shared memory, tools, schedules, and review gates
  <sub>★ 818 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add desplega-ai/agent-swarm`</sub>
- **[Tura](https://github.com/Tura-AI/tura)** — AGPL-3.0 local coding agent with CLI/TUI/GUI, task-scoped context, macro command execution, verification, and public benchmark artifacts
  <sub>★ 638 · Rust · AGPL-3.0 · npm · pushed 2026-09-13 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g tura-ai`</sub>
- **[OpenDraft](https://github.com/federicodeponte/opendraft)** — Autonomous research-writing agent: 19 specialized agents turn a prompt into a long-form, source-grounded draft with citations verified against CrossRef, OpenAlex and Semantic Scholar. PDF/DOCX/LaTeX export, 57+ languages, bring-your-own model keys
  <sub>★ 452 · Python · MIT · npx · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add getedgehq/skills --skill opendraft`</sub>
- **[Fazm](https://github.com/mediar-ai/fazm)** — Open-source, voice-controlled AI computer agent for macOS. Controls your entire desktop through natural language - any app, file, or workflow. Built in Swift/SwiftUI, local-first
  <sub>★ 336 · Swift · source · pushed 2026-09-02 · macOS</sub>
  <sub>`git clone https://github.com/m13v/fazm.git`</sub>
- **[OpenLens AI](https://github.com/jarrycyx/openlens-ai)** — Fully Autonomous Research Agent for Health / Medicine
  <sub>★ 282 · Python · MIT · clone · pushed 2026-09-09 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/jarrycyx/openlens-ai.git`</sub>
- **[Autohand Code CLI](https://github.com/autohandai/code-cli)** — Self-evolving autonomous coding agent for the terminal with ReAct pattern, 40+ tools, multiple LLM providers (OpenRouter, Anthropic, OpenAI, Ollama, local models), VS Code/Zed integration, and modular skills system
  <sub>★ 196 · TypeScript · Apache-2.0 · brew · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install autohandai/code/autohand-code`</sub>
- **[OpenPaw](https://github.com/daxaur/openpaw)** — CLI tool (npx pawmode) that turns Claude Code into a personal assistant with 38 skills — email, calendar, Spotify, smart home, Slack, GitHub, Telegram, Discord, and more. No daemon, no cloud
  <sub>★ 167 · TypeScript · MIT · source · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/daxaur/openpaw.git`</sub>
- **[LoopTroop](https://github.com/looptroop-ai/LoopTroop)** — Local GUI orchestrator for AI coding agents where an LLM Council plans, atomic beads execute in isolated git worktrees, and a Ralph Loop retries failures with fresh context
  <sub>★ 152 · TypeScript · MIT · winget · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`winget install LoopTroopAI.LoopTroop`</sub>
- **[DecisionBox](https://github.com/decisionbox-io/decisionbox-platform)** — Open-source AI data discovery platform that connects to warehouses (BigQuery, Redshift, Snowflake, etc.), runs autonomous agents that write and execute SQL, and surfaces validated insights. Pluggable LLM providers (Claude, OpenAI, Ollama, Vertex AI, Bedrock), industry domain packs, Helm charts, and Terraform modules for GCP/AWS
  <sub>★ 119 · Go · AGPL-3.0 · clone · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/decisionbox-io/decisionbox-platform.git`</sub>
- **[Kapso](https://github.com/Leeroo-AI/kapso)** — Self-improving software factory for AI/ML objectives. State an objective and it runs a campaign: candidate solutions designed, implemented by coding agents (Claude Code, Codex), measured against the objective, and the closest refined until it is met. Each finished campaign leaves lessons carrying the evidence that earned them, and repositories and papers feed the same knowledge hub, so the next ca
  <sub>★ 113 · Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install leeroo-kapso`</sub>
- **[Everything OpenAI Codex](https://github.com/mturac/everything-openai-codex)** — Open-source workflow system for OpenAI Codex that bundles agents, skills, commands, hooks, memory patterns, install profiles, and validation checks for repeatable coding sessions
  <sub>★ 91 · JavaScript · MIT · clone · pushed 2026-08-24 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/mturac/everything-openai-codex.git`</sub>
- **[FutureOS](https://github.com/futuregene/future-os)** — One AI agent everywhere you work: terminal UI, desktop, mobile, CLI, and IM bots from a single Rust backend, with approval-gated tools and a loop control plane for 24h+ runs
  <sub>★ 87 · Rust · MIT · script · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://dl.future-os.cn/install.sh | bash`</sub>
- **[ENZO](https://github.com/theguysudo/ENZO)** — Self-hosted BYOK AI workspace with multi-provider chat (Groq, OpenRouter, NVIDIA, Hugging Face, Google AI), agents with scheduled runs, and skills like Gmail, Google Calendar, web search, and project generation. Provider keys are sealed client-side with AES-256-GCM and no middleman service is involved. Apache-2.0, Docker deployment
  <sub>★ 87 · TypeScript · Apache-2.0 · clone · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/theguysudo/ENZO.git`</sub>
- **[Aster](https://github.com/Zfinix/aster)** — Open-source terminal coding agent that reads your code, answers questions, edits files, runs commands, and reviews your changes. Works with any OpenAI-compatible provider (OpenRouter, OpenAI, Groq, Anthropic, local models). Rust, Apache-2.0
  <sub>★ 85 · Rust · Apache-2.0 · cargo · pushed 2026-09-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install --path crates/aster-cli`</sub>
- **[Hivekeep](https://github.com/MarlBurroW/hivekeep)** — Self-hosted platform of autonomous, persistent personal AI agents that collaborate, remember across months, and build their own tools. Multi-channel (Telegram, WhatsApp, Slack, Discord, Signal, Matrix), single container with Bun and SQLite
  <sub>★ 63 · TypeScript · MIT · script · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/MarlBurroW/hivekeep/main/install.sh | bash`</sub>
- **[Lumen](https://github.com/omxyz/lumen)** — A vision-first browser agent with self-healing deterministic replay over CDP. Screenshot → model → action loop with multi-provider support
  <sub>★ 57 · TypeScript · MIT · source · pushed 2026-03-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/omxyz/lumen.git`</sub>
- **[KodeAgent](https://github.com/barun-saha/kodeagent)** — The Minimal Agent Engine, enabling seamless integration with your platform. KodeAgent offers tool-calling (ReAct) and sandboxed code-executing (CodeAct) agents, supported by planning and observation
  <sub>★ 40 · Python · Apache-2.0 · pip · pushed 2026-08-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U kodeagent # Upgrade existing installation`</sub>
- **[Tracefold](https://github.com/TraceFold/tracefold)** — Verified transformation calculus, pre-commit inverse escrow, and offline DSSE receipts for AI agent tool executions and filesystem mutations
  <sub>★ 18 · Rust · Apache-2.0 · source · pushed 2026-09-04 · Win? · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/TraceFold/tracefold.git`</sub>
- **[Plot Ark](https://github.com/Schlaflied/Plot-Ark)** — Self-hosted agentic curriculum engine for higher education — generates pedagogically grounded course content using Bloom's Taxonomy alignment, LightRAG knowledge graph, and xAPI learning analytics pipeline
  <sub>★ 13 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-12 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Schlaflied/Plot-Ark`</sub>
- **[OpenTwins](https://github.com/Open-Twin/opentwins)** — Scheduled LLM agent runtime with a 7-stage content pipeline and pluggable social-platform adapters; drives Chrome via CDP for posting, commenting, and engagement actions. Built on the Claude Agent SDK
  <sub>★ 12 · Handlebars · MIT · npm · pushed 2026-07-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g opentwins`</sub>
- **[Octopal](https://github.com/pmbstyle/Octopal)** — Secure local multi-agent runtime that plans tasks, delegates execution to isolated workers, and exposes tools, MCP, scheduling, and a private dashboard for autonomous operations
  <sub>★ 10 · Python · MIT · psh · pushed 2026-08-16 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://raw.githubusercontent.com/pmbstyle/Octopal/main/scripts/octopal.ps1 | iex`</sub>
- **[Caesar](https://github.com/jasonzliang/caesar-agent)** — Autonomous research agent that builds a knowledge graph during web exploration via a Perceive-Think-Act loop, then refines drafts through adversarial artifact synthesis. Multi-provider via litellm
  <sub>★ 9 · Python · Apache-2.0 · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install caesar-agent`</sub>
- **[SARA](https://github.com/Alessandro114/sara)** — Self-hosted WhatsApp AI agent (AGPL-3.0) with 20 industry verticals, function calling (30+ tools), RAG via pgvector, and multi-provider LLM failover (Groq → Cerebras → SambaNova → Mistral)
  <sub>★ 8 · TypeScript · clone · pushed 2026-09-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Alessandro114/sara.git`</sub>
- **[SDP (Social Daily Poster)](https://github.com/dimamak/sdp)** — Self-hosted agent that harvests your Claude Code or Codex sessions, screenshots and messages each night, drafts one social post from the day's work, and routes it through a private Telegram bot for approval before it publishes to LinkedIn, X or Reddit. Python 3, MIT
  <sub>★ 8 · Python · MIT · clone · pushed 2026-09-08 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/dimamak/sdp.git`</sub>
- **[ALF OS](https://github.com/alamparelli/alf)** — Self-hosted AI assistant daemon with encrypted credential vault, persistent memory, cron scheduler, multi-provider routing (Claude Code, Codex, GPT, Ollama, OpenRouter), Telegram bot with voice transcription, and web dashboard. Docker Compose, MIT
  <sub>★ 6 · Go · MIT · script · pushed 2026-05-14 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL install.alfos.ai | sh`</sub>
- **[Alfred](https://github.com/luminik-io/alfred)** — Self-hosted runtime for autonomous Claude Code and Codex agents that turns GitHub issues into reviewed pull requests. Per-firing git worktrees, label-driven state, role-based engine routing, Slack reports. Python, MIT, macOS/Linux
  <sub>★ 4 · Python · MIT · brew · pushed 2026-09-18 · WSL2? · macOS · Linux?</sub>
  <sub>`brew tap luminik-io/alfred https://github.com/luminik-io/alfred`</sub>
- **[Sudarshan](https://github.com/Suraj1235/sudarshan-superharness)** — Durable build harness that drives an LLM from an idea, PRD, or spec to software gated on passing verification commands, with resumable checkpointed state; provider-neutral across OpenAI-compatible, Anthropic, Gemini, local, and command-bridge backends
  <sub>★ 2 · Python · MIT · pip · pushed 2026-08-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install git+https://github.com/Suraj1235/sudarshan-superharness.git`</sub>
- **[Anima-i (Methodius/Мефодий)](https://github.com/Vitali-Ivanovich/anima-i)** — An experiment in autonomous AI agent continuity — 10 generations of an agent that inherits memory through text files, with documented findings on knowledge transfer, forgetting, and agent identity
  <sub>★ 1 · Shell · MIT · clone · pushed 2026-03-25</sub>
  <sub>`git clone https://github.com/Vitali-Ivanovich/anima-i.git`</sub>
- **[Wordware](https://www.wordware.ai)** — A web-hosted IDE where non-technical domain experts work with AI Engineers to build task-specific AI agents. It approaches prompting as a new programming language rather than low/no-code blocks
  <sub>website</sub>
  <sub>`https://www.wordware.ai`</sub>

## Multi-Agent Task Solver Projects

- **[MetaGPT](https://github.com/FoundationAgents/MetaGPT)** — The Multi-Agent Framework: Given one line Requirement, return PRD, Design, Tasks, Repo
  <sub>★ 70.5k · Python · MIT · pip · pushed 2026-01-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade metagpt`</sub>
- **[ChatDev](https://github.com/OpenBMB/ChatDev)** — Create Customized Software using Natural Language Idea (through LLM-powered Multi-Agent Collaboration)
  <sub>★ 34.4k · Python · Apache-2.0 · source · pushed 2026-07-24 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/OpenBMB/ChatDev.git`</sub>
- **[AionUi](https://github.com/iOfficeAI/AionUi)** — Open-source desktop client that runs multiple agent CLIs (Claude Code, Codex, Gemini CLI, Qwen Code) side by side, with multi-session chat, MCP and ACP support, and local file management
  <sub>★ 33k · TypeScript · Apache-2.0 · brew · pushed 2026-09-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install aionui`</sub>
- **[DevOpsGPT](https://github.com/kuafuai/DevOpsGPT)** — Multi agent system for AI-driven software development
  <sub>★ 6k · HTML · source · pushed 2026-09-18 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/kuafuai/DevOpsGPT.git`</sub>
- **[Maestro](https://github.com/RunMaestro/Maestro)** — Open-source desktop command center for running multiple AI coding agents (Claude Code, Codex, Gemini CLI, etc.) in parallel, with Cue event automation, Auto Run playbooks, Group Chat across local and remote agents, and a maestro-cli that agents can drive themselves
  <sub>★ 3.4k · TypeScript · AGPL-3.0 · clone · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/RunMaestro/Maestro.git`</sub>
- **[EvoAgentX](https://github.com/ANative-Lab/EvoAgentX)** — EvoAgentX is building a Self-Evolving Ecosystem of AI Agents, it will give you automated framework for evaluating and evolving agentic workflows
  <sub>★ 3.4k · Python · pip · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evoagentx`</sub>
- **[Agent Teams](https://github.com/777genius/agent-teams-ai)** — Open-source desktop app for coordinating multi-agent workflows with Kanban task management, agent messaging, code review, and approval controls
  <sub>★ 2.2k · TypeScript · AGPL-3.0 · clone · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/777genius/agent-teams-ai.git`</sub>
- **[Orkas](https://github.com/Orkas-AI/Orkas)** — MIT-licensed, local-first multi-agent desktop application where a Commander coordinates specialist agents for research, coding, data analysis, documents, and media
  <sub>★ 2.1k · TypeScript · MIT · clone · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Orkas-AI/Orkas.git`</sub>
- **[Bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Open-source governance layer for AI agents. No model in the coordination loop: deterministic scheduling, per-task git worktree isolation, byte-identical replay, signed lineage, and an opt-in HMAC audit chain. Drives 40+ CLI coding agents (Claude Code, Codex CLI, Gemini CLI). Apache-2.0
  <sub>★ 1.2k · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[h5i](https://github.com/h5i-dev/h5i)** — CLI that runs several coding agents (Claude Code, Codex) on the same task, each in an isolated git worktree sandbox, has them peer-review each other, then a neutral verifier replays every candidate, runs the tests itself, and merges the one that passes. Run metadata is versioned in the repo under refs/h5i/*. Rust, Apache-2.0
  <sub>★ 648 · Rust · Apache-2.0 · npx · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add h5i-dev/h5i # if you do not have the binary yet`</sub>
- **[Giselle](https://github.com/giselles-ai/giselle)** — Giselle is an agentic workflow builder that empowers you to create AI-driven solutions with ease
  <sub>★ 556 · TypeScript · Apache-2.0 · clone · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/giselles-ai/giselle.git`</sub>
- **[Maestro Orchestrate](https://github.com/josstei/maestro-orchestrate)** — Multi-agent development orchestration platform coordinating 22 specialized AI agents through 4-phase workflows with native parallel execution, persistent sessions, and least-privilege security tiers across Gemini CLI, Claude Code, and Codex
  <sub>★ 464 · JavaScript · Apache-2.0 · clone · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/josstei/maestro-orchestrate`</sub>
- **[Vicoa](https://github.com/vicoa-ai/vicoa)** — Agentic IDE and AI orchestrator for running Claude Code, Codex, OpenCode, Gemini, Cursor, GitHub Copilot, Kimi, and Hermes agents in parallel, each in its own git worktree, steered from a unified dashboard with real-time mobile sync and push notifications
  <sub>★ 272 · Python · AGPL-3.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm i -g @vicoa/cli # Node.js 18+`</sub>
- **[ClawFleet](https://github.com/clawfleet/ClawFleet)** — Self-hosted AI fleet management with browser dashboard, Docker isolation, and bot-to-bot collaboration in Discord. ![GitHub Repo
  <sub>★ 174 · Go · MIT · script · pushed 2026-04-27 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://clawfleet.io/install.sh | sh`</sub>
- **[GenoMAS](https://github.com/Liu-Hy/GenoMAS)** — Multi-agent framework for robust automation of scientific analysis workflows, such as gene expression analysis
  <sub>★ 134 · Python · MIT · source · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Liu-Hy/GenoMAS.git`</sub>
- **[swarm-orchestrator](https://github.com/moonrunnerkc/swarm-orchestrator)** — Contract-first multi-agent orchestrator that races persona candidates per typed obligation, verifies before commit, and logs every action in an append-only hash-chained ledger; deterministic offline default with optional Claude, Codex, Copilot, and local LLM (Ollama, llama.cpp, vLLM) providers. Ships with a GitHub Action
  <sub>★ 111 · JavaScript · ISC · npm · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g swarm-orchestrator`</sub>
- **[OpenAcme](https://github.com/sandydasari/openacme)** — Local-first AI workforce platform — named agents with roles, personas, tools, memory, and per-agent MCP servers that self-organize through task delegation. Any agent can assign work to another; the scheduler wakes coworkers when dependencies clear
  <sub>★ 87 · TypeScript · MIT · npm · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @openacme/cli`</sub>
- **[NextRole](https://github.com/tam159/next-role)** — A supervisor agent coordinates three sub-agents (hiring-recon, resume-tailor, interview-coach) to turn a CV and job description into a tailored resume, interview-prep doc, and day-of battlecard
  <sub>★ 61 · Python · MIT · clone · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/tam159/next-role.git`</sub>
- **[YYLO](https://github.com/yylo-dev/yylo)** — Kanban-driven CLI orchestrator that runs coding agents (Claude Code, Codex, Gemini CLI) in parallel across isolated git worktrees, with a merge queue that reviews and merges verified task work
  <sub>★ 60 · Python · MIT · npm · pushed 2026-09-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install --global '@yylo/cli@latest'`</sub>
- **[Shire](https://github.com/victor36max/shire)** — Persistent workspaces for AI agent teams with inter-agent mailboxes, shared drive, and full context preservation. Supports Claude Code, OpenCode, Pi Agent and more
  <sub>★ 39 · TypeScript · MIT · npm · pushed 2026-05-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g agents-shire`</sub>
- **[Hivemoot](https://github.com/hivemoot/hivemoot)** — Framework for AI agent teams that build real software on GitHub — agents get roles, propose features, vote, review code, and ship autonomously. Colony is the first project built this way
  <sub>★ 16 · TypeScript · Apache-2.0 · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @hivemoot-dev/cli buzz # repo status overview`</sub>
- **[RadOps](https://github.com/mehrdadrad/radops)** — RadOps is an AI-powered, multi-agent platform that automates DevOps workflows with human-level reasoning
  <sub>★ 14 · Python · MIT · clone · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mehrdadrad/radops.git`</sub>
- **[OpenBusiness](https://github.com/wanikua/OpenBusiness)** — Multi-agent pipeline that turns a company name + domain into an evidence-labeled business model report; runs JTBD, value proposition, GTM, unit economics, moat, canvas synthesis, and an assumption stress test, tagging every claim verified, inferred, or missing. Built on LangGraph; deterministic unit economics in Python
  <sub>★ 9 · Python · MIT · uv · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx openbusiness analyze "Notion" --domain notion.so`</sub>
- **[Orchard Kit](https://github.com/OrchardHarmonics/orchard-kit)** — Six zero-dependency Python modules for autonomous agent governance and cognitive architecture: runtime security, confabulation detection, self-audit, agent discovery, cognitive architecture, and collective cognition
  <sub>★ 7 · Python · pip · pushed 2026-02-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install orchard-kit`</sub>
- **[claude-consensus](https://github.com/tonydzi/claw-consensus)** — Consensus protocol for LLM agents running on separate machines: propose/counter/accept/commit rounds, a dual-rail message bus with ACK tracking, and self-healing sync to keep agent state from drifting
  <sub>★ 3 · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tonydzi/claude-consensus.git`</sub>
- **[XYZZY](https://github.com/Project-Nexus-YR/XYZZY)** — Self-hosted multiplayer workspace where a team branches a question into parallel specialist agent runs, includes or excludes each output, and publishes a Decision Brief with every claim linked to its source output; hash-chained event log, one Python process on SQLite, works with any OpenAI-compatible endpoint
  <sub>★ 2 · Python · Apache-2.0 · docker · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 8000:8000 -e XYZZY_DEMO=1 ghcr.io/project-nexus-yr/xyzzy`</sub>
- **[Bunkhouse](https://github.com/braedonsaunders/bunkhouse)** — Self-hosted multitenant platform for AI employees with company inbox, org chart, and governed procedures
  <sub>★ 1 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-16 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/braedonsaunders/bunkhouse.git`</sub>

## Agent Society Simulation

- **[generative_agents](https://github.com/joonspk-research/generative_agents)** — Interactive Simulacra of Human Behavior
  <sub>★ 22.1k · Apache-2.0 · source · pushed 2024-08-05</sub>
  <sub>`git clone https://github.com/joonspk-research/generative_agents.git`</sub>
- **[camel](https://github.com/camel-ai/camel)** — Communicative Agents for “Mind” Exploration of Large Language Model Society (NeruIPS'2023)
  <sub>★ 17.7k · Python · Apache-2.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install camel-ai`</sub>
- **[ai-town](https://github.com/a16z-infra/ai-town)** — deployable starter kit for building and customizing your own version of AI town - a virtual town where AI characters live, chat and socialize
  <sub>★ 10.5k · TypeScript · MIT · npx · pushed 2026-08-26 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx convex env set OLLAMA_HOST http://host.docker.internal:11434`</sub>
- **[GPTTeam](https://github.com/101dotxyz/GPTeam)** — The main objective of this project is to explore the potential of GPT models in enhancing multi-agent productivity and effective communication
  <sub>★ 1.7k · Python · MIT · source · pushed 2026-09-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/101dotxyz/GPTeam.git`</sub>
- **[ChatArena](https://github.com/Farama-Foundation/ChatArena)** — ChatArena is a library that provides multi-agent language game environments and facilitates research about autonomous LLM agents and their social interactions
  <sub>★ 1.6k · Python · Apache-2.0 · pip · pushed 2025-08-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install chatarena`</sub>
- **[MiroShark](https://github.com/MiroShark/MiroShark)** — Social-simulation framework in which LLM agents interact across simulated Twitter, Reddit, and a prediction market on an hourly tick. Supports scenario-driven runs, counterfactual branching, and per-agent tool calling via MCP
  <sub>★ 1.5k · Python · AGPL-3.0 · clone · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/aaronjmars/MiroShark.git`</sub>
- **[HoC-Republic](https://github.com/hunix/HoC-Republic)** — Open-source AI-agent civilization simulation with OpenClaw gateway integration, persistent AI citizens, governance, economy, memory layers, and digital-genome child-agent specialization
  <sub>TypeScript · MIT · clone · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hunix/HoC-Republic.git`</sub>

## Tools

- **[mem0](https://github.com/mem0ai/mem0)** — Mem0 provides a smart, self-improving memory layer for Large Language Models, enabling personalized AI experiences across applications
  <sub>★ 65.8k · Python · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @mem0/cli # or: pip install mem0-cli`</sub>
- **[composio](https://github.com/ComposioHQ/composio)** — Composio equips agents with well-crafted tools empowering them to tackle complex tasks
  <sub>★ 30.3k · TypeScript · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`pip install composio composio-openai-agents openai-agents`</sub>
- **[Steel Browser](https://github.com/steel-dev/steel-browser)** — Open-source browser infrastructure for AI agents and apps, supporting session-backed web automation, extraction, screenshots, and PDFs
  <sub>★ 7.7k · TypeScript · Apache-2.0 · docker · pushed 2026-09-16 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -p 3000:3000 -p 9223:9223 ghcr.io/steel-dev/steel-browser`</sub>
- **[Agent OS](https://github.com/microsoft/agent-governance-toolkit)** — A kernel architecture for governing autonomous AI agents. Intercepts actions mid-execution with deterministic policy enforcement, POSIX-inspired primitives, and MCP server for Claude Desktop
  <sub>★ 6.3k · Python · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @microsoft/agent-governance-copilot-cli install`</sub>
- **[Metorial](https://github.com/metorial/metorial)** — Integration gateway that links AI agents to 600+ tools via unified MCP/OAuth interface with built-in scaling and monitoring
  <sub>★ 3.4k · TypeScript · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install metorial pydantic-ai python-dotenv`</sub>
- **[Webcmd](https://github.com/agentrhq/webcmd)** — Self-learning browser infrastructure for AI agents: learns a site's navigation once, then compiles it into deterministic per-site CLI commands. TypeScript, Apache-2.0
  <sub>★ 2.2k · TypeScript · Apache-2.0 · npm · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @agentrhq/webcmd`</sub>
- **[Agentic Radar](https://github.com/splx-ai/agentic-radar)** — Open-source CLI security scanner for agentic workflows. Scans your workflow’s source code, detects vulnerabilities, and generates an interactive visualization along with a detailed security report
  <sub>★ 1.1k · Python · Apache-2.0 · pip · pushed 2025-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentic-radar`</sub>
- **[Caspian](https://github.com/TryCaspian/caspian-sdk)** — One messaging identity for an AI agent across Slack, Discord, Telegram, Instagram, email, and X — a single on_message handler with threading, webhook verification, and platform quirks handled. Python + TypeScript SDK
  <sub>★ 976 · Python · AGPL-3.0 · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install caspian-sdk # Python 3.10+`</sub>
- **[Compartment](https://github.com/MaxFreedomPollard/Compartment)** — Local-first, offline encrypted vector memory for AI agents over MCP or CLI, with AEAD-encrypted-at-rest records and embeddings, RAM-resident exact vector search, per-record crypto-shred deletion, and a hash-chained audit log. Apache-2.0, Python
  <sub>★ 582 · Python · Apache-2.0 · uv · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install compartment`</sub>
- **[Caura](https://github.com/caura-ai/caura)** — Governed shared memory for AI agent fleets, with multi-agent and multi-tenant support, MCP integration, trust tiers, audit trails, knowledge graph capabilities, and self-improving retrieval
  <sub>★ 528 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install caura-client`</sub>
- **[MisakaNet](https://github.com/Ikalus1988/MisakaNet)** — Git-based shared memory for AI agents. Cross-agent lesson/knowledge sync via GitHub Issues. "Lessons learned. Lessons shared."
  <sub>★ 495 · Python · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npx @misaka-net/misakanet-setup`</sub>
- **[agentlego](https://github.com/InternLM/agentlego)** — Enhance LLM agents with versatile tool APIs
  <sub>★ 415 · Python · Apache-2.0 · pip · pushed 2024-09-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentlego`</sub>
- **[Agent-Wiz](https://github.com/Repello-AI/Agent-Wiz)** — Python CLI by Repello AI for extracting agentic workflows from LangChain/LangGraph/CrewAI/AutoGen and running automated threat modeling against the resulting graphs
  <sub>★ 397 · Python · Apache-2.0 · pip · pushed 2025-11-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install repello-agent-wiz`</sub>
- **[Statewave](https://github.com/smaramwbc/statewave)** — Open-source memory runtime for AI agents, providing durable, structured, provenance-tagged context with deterministic, token-bounded memory retrieval
  <sub>★ 347 · Python · Apache-2.0 · psh · pushed 2026-09-19 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://www.statewave.ai/install.ps1 | iex`</sub>
- **[Uni-CLI](https://github.com/olo-dot-io/Uni-CLI)** — Universal CLI for AI agents — exposes the agent-runnable web, desktop, Electron, and bridge-CLI surface as deterministic commands. Declarative YAML adapters with structured error envelopes (adapter_path, step, suggestion) let agents edit failing adapters and retry. Optional MCP server (stdio + Streamable HTTP). Live catalog size and per-call token budget tracked in the repo's README and docs/BENCH
  <sub>★ 270 · TypeScript · Apache-2.0 · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @zenalexa/unicli`</sub>
- **[OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay)** — Records a coding agent below the harness — model traffic, shell exit codes, per-turn file changes and MCP calls on one timeline — then replays the run offline with the network off, or forks it from any checkpoint onto a different model
  <sub>★ 259 · TypeScript · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g orcareplay # the package is orcareplay`</sub>
- **[Kontext CLI](https://github.com/kontext-security/kontext)** — Open-source CLI for local guardrails, risk scoring, and redacted tool-call traces for AI agent sessions
  <sub>★ 221 · Go · MIT · brew · pushed 2026-09-21 · WSL2? · macOS · Linux</sub>
  <sub>`brew install kontext-security/tap/kontext`</sub>
- **[Cynative](https://github.com/cynative/cynative)** — Agentic security CLI that runs code in a built-in sandbox to research cloud, code and runtime. Read-only by construction
  <sub>★ 202 · Go · Apache-2.0 · scoop · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add cynative https://github.com/cynative/scoop-bucket scoop install cynative`</sub>
- **[codex-profiles](https://github.com/Ducksss/codex-profiles)** — Bash CLI for switching OpenAI Codex CLI/Desktop accounts with isolated CODEX_HOME profiles
  <sub>★ 163 · Shell · MIT · brew · pushed 2026-09-15 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install Ducksss/tap/codex-profile`</sub>
- **[clideck](https://github.com/rustykuntz/clideck)** — WhatsApp-like dashboard for managing multiple AI coding agents in one browser window. Live status, session resume, autopilot that routes work between agents, and mobile remote
  <sub>★ 158 · JavaScript · MIT · npm · pushed 2026-09-18 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g clideck@2`</sub>
- **[CommonGround Kernel](https://github.com/Intelligent-Internet/CommonGround)** — PostgreSQL-backed shared work substrate for human-agent and multi-agent systems, with durable public work records, handoff facts, causal lineage, claim fencing, and pull-first recovery across runtimes
  <sub>★ 150 · Python · Apache-2.0 · uv · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install commonground-kernel`</sub>
- **[KubeStellar Console](https://github.com/kubestellar/console)** — Multi-cluster Kubernetes dashboard with AI operations agent (kc-agent) that bridges LLMs to live clusters via MCP for AI-assisted troubleshooting, observability, and management across edge and cloud. CNCF Sandbox project
  <sub>★ 137 · TypeScript · Apache-2.0 · brew · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew tap kubestellar/tap`</sub>
- **[agenttrace](https://github.com/luoyuctl/agenttrace)** — Local-first TUI observability for AI coding agent sessions, with cost, token, tool failure, latency, anomaly, health score, diff, and CI gate views
  <sub>★ 135 · Rust · MIT · winget · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install --id Luoyuctl.AgentTrace --exact`</sub>
- **[Ordewell](https://github.com/ordewell/ordewell)** — Open-source terminal CLI and TUI that turns one goal into an ordered, editable plan of coding-agent tasks, each with its own runner (Claude Code, Codex, OpenCode), model and mode; a task is complete only when a completion marker appears in the runner's output. Apache-2.0
  <sub>★ 135 · TypeScript · Apache-2.0 · npm · pushed 2026-09-20 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g ordewell`</sub>
- **[harness-starter-kit](https://github.com/harnessworks/harness-starter-kit)** — Prompt-first starter kit for adding repository-specific agent instructions, failure memory, drift checks, and verification workflows for AI coding agents
  <sub>★ 113 · Python · MIT · source · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/baskduf/harness-starter-kit.git`</sub>
- **[ax](https://github.com/Necmttn/ax)** — Local telemetry for AI coding agents
  <sub>★ 111 · TypeScript · AGPL-3.0 · npx · pushed 2026-09-14 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add Necmttn/ax # agent skills: setup, retro, extract-workflow, dojo, …`</sub>
- **[Open Index](https://github.com/DrDroidLab/open-index)** — Structured context layer for domain-specific agents with typed knowledge graphs, hybrid search, and read/write MCP access
  <sub>★ 109 · Python · MIT · pip · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install 'open-index[serve]' # add ,opensearch for that backend`</sub>
- **[authsome](https://github.com/agentrhq/authsome)** — Local credential broker for AI agents. Log in once via OAuth2 or API key, vault stores secrets locally, local proxy injects them at request time so agents never see the raw values. 45 providers bundled
  <sub>★ 92 · Python · MIT · npx · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add agentrhq/authsome`</sub>
- **[Hexis](https://github.com/Bevel-Software/Hexis)** — Git-backed platform for managing and sharing skills, tools, and context across AI agents through a remote MCP server
  <sub>★ 88 · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Bevel-Software/Hexis.git`</sub>
- **[Nika](https://github.com/supernovae-st/nika)** — Intent-as-code workflow engine for AI agents: reviewable YAML DAGs statically checked (schema, permits, honest cost floor) before any token is spent, tamper-evident traces after. Single Rust binary
  <sub>★ 88 · Rust · AGPL-3.0 · brew · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew install supernovae-st/tap/nika`</sub>
- **[Desktop Control](https://github.com/yaroshevych/desktopctl)** — CLI tool for AI agents to control macOS apps via screen, mouse, and keyboard. GPU-accelerated, local OCR and vision, works with any AI model
  <sub>★ 67 · Rust · MIT · source · pushed 2026-09-08 · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/yaroshevych/desktopctl.git`</sub>
- **[5dive](https://github.com/5dive-ai/5dive)** — Self-hosted CLI that runs a team of coding agents on one Linux host: each agent is its own Linux user running claude, codex, opencode, hermes or another CLI as a systemd service, coordinating through an org chart and a shared SQLite backlog, escalating to Telegram only when a human must decide. MIT
  <sub>★ 60 · Shell · MIT · npx · pushed 2026-09-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npx -y skills add https://github.com/5dive-ai/skills --skill 5dive-cli --agent <runtime> --yes`</sub>
- **[EGC](https://github.com/Fmarzochi/EGC)** — Cross-session persistent memory layer for AI coding agents (Claude Code, Cursor, Gemini CLI, Codex, Windsurf, Amp, Kiro, and more). SQLite-backed
  <sub>★ 53 · JavaScript · Apache-2.0 · npm · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @egchq/egc`</sub>
- **[sofagent](https://github.com/KongFangXun/sofagent)** — Audit-first governance harness for AI coding agents: 24 rules enforced at commit time via git hooks, HMAC-chained audit log, snapshot rollback. MIT
  <sub>★ 47 · TypeScript · MIT · npx · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y -p @sofagent/audit sofagent-audit`</sub>
- **[DexPaprika MCP](https://github.com/coinpaprika/dexpaprika-mcp)** — Open-source MCP server for querying decentralized exchange data across 34 blockchains. Exposes pool details, token metadata, OHLCV charts, trade history, and real-time swap streams via SSE
  <sub>★ 42 · JavaScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g dexpaprika-mcp`</sub>
- **[DSH Studio](https://github.com/Moresyl/dsh-studio)** — Cross-platform desktop host for installing, running, health-checking, and supervising DeepSeek Harness locally
  <sub>★ 26 · Rust · MIT · scoop · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop bucket add dsh https://github.com/Moresyl/dsh-studio scoop install dsh-studio`</sub>
- **[APort Agent Guardrails](https://github.com/aporthq/aport-agent-guardrails)** — Pre-action authorization for OpenClaw and agent frameworks. before_tool_call plugin, 40+ blocked patterns, local or API. Setup: npx @aporthq/agent-guardrails
  <sub>★ 25 · Shell · npx · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @aporthq/aport-agent-guardrails github`</sub>
- **[WinkTerm](https://github.com/Cznorth/winkterm)** — Self-hosted AI terminal where the agent shares your PTY session; in-terminal # chat, SSH, and HTTP Agent API with installable skill for coding agents
  <sub>★ 22 · Python · MIT · clone · pushed 2026-07-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Cznorth/winkterm.git`</sub>
- **[DOS (dos-kernel)](https://github.com/anthony-chaudhary/dos-kernel)** — Trust kernel for AI agent fleets: verifies an agent's "done" claim from git evidence (never self-report), arbitrates file collisions between concurrent agents, and refuses with structured machine-checkable reasons. CLI + MCP server + Claude Code plugin
  <sub>★ 20 · Python · MIT · uv · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from dos-kernel dos quickstart`</sub>
- **[Tree Ring Memory](https://github.com/TerminallyLazy/Tree-Ring-Memory)** — Local-first Rust CLI and TUI for AI agent memory lifecycle with SQLite/FTS recall, audit, consolidation, forgetting, and framework discovery
  <sub>★ 18 · Rust · MIT · script · pushed 2026-09-17 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/TerminallyLazy/Tree-Ring-Memory/main/install.sh | sh -s -- --release latest`</sub>
- **[Lians](https://github.com/Lians-ai/Lians)** — Local-first memory layer for AI agents with MCP, Python, and TypeScript interfaces; SQLite-backed recall, user-controlled inspection/correction/deletion, and point-in-time memory receipts
  <sub>★ 11 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install "lians-sdk[local]"`</sub>
- **[WritBase](https://github.com/Writbase/writbase)** — MCP-native task management control plane for AI agent fleets with multi-agent permissions, delegation safety, and full provenance
  <sub>★ 10 · TypeScript · Apache-2.0 · npx · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx writbase init # Interactive setup — configures Supabase credentials`</sub>
- **[MCP Lens](https://github.com/labmimors/dsh-mcp-lens)** — Open-source DeepSeek Harness plugin that discovers MCP tools through search and invokes selected tools with their exact input schemas
  <sub>★ 9 · TypeScript · MIT · clone · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/labmimors/dsh-mcp-lens.git`</sub>
- **[Cortex](https://github.com/SKULLFIRE07/cortex-memory)** — Persistent AI memory for coding assistants. Auto-captures decisions, patterns, and context across sessions. VSCode extension + CLI + MCP server
  <sub>★ 8 · TypeScript · MIT · npm · pushed 2026-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g cortex-memory`</sub>
- **[BrowserTrace](https://github.com/aaronlab/browsertrace)** — Local flight recorder for AI browser agents with screenshots, URLs, model I/O, failure timelines, and public-safe HTML exports
  <sub>★ 5 · Python · MIT · uv · pushed 2026-05-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --from "browsertrace[ui]" browsertrace doctor`</sub>
- **[AgentGuard](https://github.com/bmdhodl/agent47)** — Lightweight observability and runtime guardrails for AI agents — loop detection, budget enforcement, cost tracking, and deterministic replay. Zero dependencies, LangChain integration
  <sub>★ 4 · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/bmdhodl/agent47.git`</sub>
- **[Oathra](https://github.com/FORIFOR/oathra)** — Apache-2.0 TypeScript runtime for phone agents with a standalone evidence-verification engine; anchors result fields to callee utterances and applies deterministic completion rules, with a simulator and adversarial tests
  <sub>TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx --yes --package=https://github.com/FORIFOR/oathra/releases/download/v0.1.18/oathra-0.1.18.tgz oathra demo`</sub>
- **[Perseus](https://github.com/tcconnally/perseus)** — Live workspace context engine for AI agents. Renders AGENTS.md at session start. Plug-in for Claude Code, Codex, Hermes
  <sub>unavailable</sub>
- **[poolsplit](https://github.com/SpicyNoodles3/poolsplit)** — Pool-split retrieval for agent memory: reserved per-type token budgets so low-priority entries surface and behavioral corrections never get crowded out. Zero dependencies, pluggable scorer
  <sub>Python · MIT · source · pushed 2026-07-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SpicyNoodles3/poolsplit.git`</sub>
- **[ValetFS](https://github.com/WinM2M/valet-fs)** — Secrets stay on a paired device and are lent to the agent's machine into daemon memory only, served over FUSE or loopback WebDAV; the daemon zero-wipes them when the pairing drops or a grace window expires
  <sub>Go · MIT · script · pushed 2026-09-10 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://winm2m.github.io/valet-fs/install.sh | bash`</sub>
- **[BGPT MCP](https://github.com/connerlambden/bgpt-mcp)** — MCP server for searching scientific papers and retrieving structured experimental data extracted from full-text studies
  <sub>unavailable</sub>
- **[WFGY 16 Problem Map](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)** — Framework-agnostic debugging and evaluation checklist for LLM agents and RAG systems, with a practical 16-problem failure map covering retrieval, vector store, prompt / tool contract, and deployment issues in real workflows
  <sub>Jupyter Notebook · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/onestardao/WFGY.git && cd WFGY/ProblemMap/README.md`</sub>
- **[AgentSkeptic](https://github.com/jwekavanagh/agentskeptic)** — Verifies AI agent workflows by checking real database state instead of logs or traces
  <sub>TypeScript · MIT · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx agentskeptic check --workflow-id wf_example \`</sub>
- **[Agent Coordinator](https://github.com/alanhoff/agent-coordinator)** — Codex skill that records complex tasks as revisioned work graphs, rejects overlapping write scopes, reconciles uncertain work before retry, and reruns completion checks
  <sub>Python · MIT · source · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alanhoff/agent-coordinator.git`</sub>

## Advanced Components

- **[Cache-to-Cache](https://github.com/thu-nics/C2C)** — Direct semantic communication between LLMs via KV-cache fusion, removing token-by-token latency for multi-agent collaboration
  <sub>★ 670 · Python · Apache-2.0 · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/thu-nics/C2C.git`</sub>
- **[zer0dex](https://github.com/hermes-labs-ai/zer0dex)** — Local dual-layer memory pattern for AI agents: a compact, human-readable markdown index paired with semantic retrieval from a local vector store, queried before each message. For cross-project recall where flat memory files or vector-only RAG fall short
  <sub>★ 60 · Python · Apache-2.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zer0dex`</sub>
- **[CoWorker Protocol](https://github.com/ZiwayZhao/agent-coworker)** — P2P agent collaboration over XMTP with schema-based skill invocation, E2E encryption, and revocable trust. Agents share capabilities without exposing code
  <sub>★ 20 · Python · MIT · pip · pushed 2026-04-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-coworker`</sub>
- **[inspeximus](https://github.com/DanceNitra/inspeximus)** — Memory component for long-running agents: a correction retires the old value by key, revert() undoes the correction from a plain instruction, and every write leaves a verifiable receipt. Deterministic, no model in the loop, one zero-dependency file
  <sub>★ 6 · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install inspeximus`</sub>

## Benchmark/Evaluator

- **[agentops](https://github.com/AgentOps-AI/agentops)** — Python SDK for agent monitoring, LLM cost tracking, benchmarking, and more. Integrates with most LLMs and agent frameworks like CrewAI, Langchain, and Autogen
  <sub>★ 5.8k · Python · MIT · pip · pushed 2026-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentops`</sub>
- **[ToolBench](https://github.com/OpenBMB/ToolBench)** — An open platform for training, serving, and evaluating large language model for tool learning
  <sub>★ 5.7k · Python · Apache-2.0 · clone · pushed 2025-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:OpenBMB/ToolBench.git`</sub>
- **[AgentBench](https://github.com/THUDM/AgentBench)** — A Comprehensive Benchmark to Evaluate LLMs as Agents
  <sub>★ 3.7k · Python · Apache-2.0 · source · pushed 2026-02-08 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/THUDM/AgentBench.git`</sub>
- **[OSWorld](https://github.com/xlang-ai/OSWorld)** — Benchmark for multimodal desktop computer-use agents with tasks across real operating-system environments
  <sub>★ 3.2k · Python · Apache-2.0 · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/xlang-ai/OSWorld`</sub>
- **[Future AGI](https://github.com/future-agi/future-agi)** — Open-source platform to simulate, evaluate, trace, guardrail, and optimize LLM and AI agent apps, with 70+ eval metrics and OpenTelemetry-native tracing across 50+ frameworks
  <sub>★ 2k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install futureagi`</sub>
- **[BrowserGym](https://github.com/ServiceNow/BrowserGym)** — Gym-style benchmark and environment toolkit for evaluating browser-using web agents
  <sub>★ 1.4k · Python · pip · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install browsergym`</sub>
- **[langtrace](https://github.com/Scale3-Labs/langtrace)** — Langtrace 🔍 is an open-source, Open Telemetry based end-to-end observability tool for LLM applications, providing real-time tracing, evaluations and metrics for popular LLMs, LLM frameworks, vectorDBs and more.. Integrate using Typescript, Python
  <sub>★ 1.2k · TypeScript · AGPL-3.0 · pip · pushed 2025-11-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langtrace-python-sdk`</sub>
- **[ClawBench](https://github.com/TIGER-AI-Lab/ClawBench)** — Browser-agent benchmark of 281 everyday tasks (V1 152 + V2 129) on 163 live production websites across 15 categories; two-stage scoring — a submission-interception layer blocks the final write request for safe evaluation on real sites, then an LLM judge checks the captured payload against the instruction
  <sub>★ 810 · Python · Apache-2.0 · uv · pushed 2026-09-20 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`uv tool install clawbench-eval`</sub>
- **[AgentLab](https://github.com/ServiceNow/AgentLab)** — Open-source framework for developing and evaluating web agents with benchmark-driven workflows
  <sub>★ 636 · Python · pip · pushed 2026-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentlab`</sub>
- **[Multi-SWE-bench](https://github.com/multi-swe-bench/multi-swe-bench)** — Multi-language extension of SWE-bench for evaluating software engineering agents beyond Python repositories
  <sub>★ 362 · Python · Apache-2.0 · clone · pushed 2025-12-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:multi-swe-bench/multi-swe-bench.git`</sub>
- **[LLM-Agent-Benchmark-List](https://github.com/zhangxjohn/LLM-Agent-Benchmark-List)** — A benchmark list for evaluation of large language models
  <sub>★ 171 · Apache-2.0 · source · pushed 2026-08-19</sub>
  <sub>`git clone https://github.com/zhangxjohn/LLM-Agent-Benchmark-List.git`</sub>
- **[GenoTEX](https://github.com/Liu-Hy/GenoTEX)** — A benchmark for evaluating LLM agents on end-to-end gene expression data analysis, featuring comprehensive gene-trait association analysis with expert-curated annotations
  <sub>★ 65 · Jupyter Notebook · clone · pushed 2026-05-13</sub>
  <sub>`git clone https://github.com/Liu-Hy/GenoTEX.git`</sub>
- **[open-operator-evals](https://github.com/nottelabs/open-operator-evals)** — An open-source and reproducible set of evals on web browser using agents
  <sub>★ 47 · Python · source · pushed 2025-04-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nottelabs/open-operator-evals.git`</sub>
- **[whatbroke](https://github.com/arthi-arumugam-git/whatbroke)** — CLI that diffs two runs of an AI agent to show changes in tool calls, arguments, cost, latency, and outcomes, with multi-sample flake detection to demote pre-existing flakiness
  <sub>★ 20 · TypeScript · MIT · npm · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g whatbroke-cli`</sub>
- **[AgentLeak](https://github.com/yagobski/agentleak)** — Python toolkit for evaluating privacy leakage across agent traces, including tool calls, inter-agent messages, shared memory, and logs, with redacted reports and CI gates
  <sub>★ 9 · Python · MIT · pip · pushed 2026-08-30 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pip install agentleak # core`</sub>
- **[CIAgent](https://github.com/suniel12/ciagent)** — Pytest-native regression testing for AI agents — golden-trace diffing, cost guardrails, multi-run stability scoring with flip attribution, LLM-judge auditing, and one-command import of production traces (OTel/Langfuse/LangSmith) into CI tests
  <sub>★ 1 · Python · Apache-2.0 · uv · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx ciagent test --mock --runs 3`</sub>
- **[LiveMCP-101](https://arxiv.org/abs/2508.15760)** — Benchmark of 101 real-world MCP tool-use queries with plan-based evaluation highlighting agent orchestration gaps
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2508.15760`</sub>
- **[SWE-bench](https://github.com/SWE-bench/SWE-bench)** — Benchmark for evaluating LLM systems on real-world GitHub issue resolution tasks
  <sub>source</sub>
  <sub>`git clone https://github.com/Princeton-NLP/SWE-bench.git`</sub>
- **[agbenchmark](https://pypi.org/project/agbenchmark/)** — by AutoGPT
  <sub>website</sub>
  <sub>`https://pypi.org/project/agbenchmark/`</sub>
- **[Cross-Agent Review Queue 2026](https://huggingface.co/datasets/neogenesislab/cross-agent-review-queue-2026)** — Open dataset of cross-agent collaboration review transcripts (Codex Claude reviewer / architect / implementer handoffs) with structured fields for owner-goal restatement, review lens, and result code (NEW_SIGNAL / NO_NEW_SIGNAL); useful for multi-agent handoff and review-quality evaluation
  <sub>website</sub>
  <sub>`https://huggingface.co/datasets/neogenesislab/cross-agent-review-queue-2026`</sub>
- **[Sabot](https://github.com/Jott2121/sabot)** — Injects one controlled fault into a running LangGraph, CrewAI or AutoGen/Magentic-One pipeline — corrupted tool result, falsified success report, altered inter-agent message, silent model downgrade, stale context, silent no-op — and scores whether the pipeline's own reviewer, guardrail and orchestrator surfaces detect it. Pre-registered spec and adjudication anchors, deterministic scoring with no
  <sub>Python · source · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Jott2121/sabot.git`</sub>

## Platforms/API

- **[UFO](https://github.com/microsoft/UFO)** — A UI-Focused Agent for Windows OS Interaction
  <sub>★ 9.8k · Python · MIT · source · pushed 2026-09-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/microsoft/UFO.git`</sub>
- **[Bifrost](https://github.com/maximhq/bifrost)** — Open-source Go AI gateway with provider routing, automatic failover, load balancing, observability, and MCP support
  <sub>★ 8.2k · Go · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @maximhq/bifrost`</sub>
- **[OpenAgents](https://github.com/xlang-ai/OpenAgents)** — An Open Platform for Language Agents in the Wild
  <sub>★ 4.9k · Python · Apache-2.0 · source · pushed 2024-11-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/xlang-ai/OpenAgents.git`</sub>
- **[AGiXT](https://github.com/Josh-XT/AGiXT)** — AGiXT is a dynamic AI Agent Automation Platform that seamlessly orchestrates instruction management and complex task execution across diverse AI providers
  <sub>★ 3.2k · Python · MIT · pip · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agixt`</sub>
- **[Agentfield](https://github.com/Agent-Field/agentfield)** — An open source Kubernetes-style control plane for deploying AI agents as distributed microservices, with built-in service discovery, durable workflows, and observability
  <sub>★ 2.6k · Go · Apache-2.0 · script · pushed 2026-09-19 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentfield.ai/install.sh | bash`</sub>
- **[OpenAGI](https://github.com/agiresearch/OpenAGI)** — "May the Force be with LLM and Domain Experts."
  <sub>★ 2.3k · Python · MIT · pip · pushed 2024-11-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pyopenagi`</sub>
- **[RestGPT](https://github.com/Yifan-Song793/RestGPT)** — An LLM-based autonomous agent controlling real-world applications via RESTful APIs
  <sub>★ 1.4k · Python · MIT · source · pushed 2024-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Yifan-Song793/RestGPT.git`</sub>
- **[openma](https://github.com/openma-ai/open-managed-agents)** — Self-hosted, open-source implementation of Anthropic's Managed Agents API. Wire-compatible with the official SDKs. Runs on Cloudflare Workers + Durable Objects or Node. Apache 2.0
  <sub>★ 292 · TypeScript · Apache-2.0 · clone · pushed 2026-09-17 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openma-ai/open-managed-agents.git`</sub>
- **[aiXplain](https://github.com/aixplain/aiXplain)** — AI platform SDK providing access to 35,000+ AI models, benchmarking tools, pipeline design, and agent building capabilities
  <sub>★ 59 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install aixplain`</sub>
- **[Nora](https://github.com/solomon2773/nora)** — Self-hosted control plane for deploying and operating OpenClaw and Hermes agent fleets on Docker or Kubernetes, with lifecycle controls, monitoring, budgets, schedules, and per-agent cost tracking
  <sub>★ 53 · TypeScript · Apache-2.0 · script · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/solomon2773/nora/master/setup.sh | bash`</sub>
- **[KinBot](https://github.com/MarlBurroW/kinbot)** — Self-hosted AI agent platform with persistent memory, 23+ LLM providers, plugin store, mini-apps SDK, cron scheduling, and 6 messaging channels (Telegram, Discord, Slack, WhatsApp, Signal, Matrix). Runs on SQLite, no cloud required
  <sub>★ 42 · TypeScript · AGPL-3.0 · source · pushed 2026-06-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/MarlBurroW/kinbot.git`</sub>
- **[elisym](https://github.com/elisymlabs/elisym)** — Open-source TypeScript implementation of a Nostr-based protocol (NIP-89/NIP-90) for AI agent discovery and job exchange, with Solana payment settlement
  <sub>★ 17 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @elisym/mcp init #Create an agent`</sub>
- **[Pinchwork](https://github.com/anneschuth/pinchwork)** — Open-source agent-to-agent task marketplace where agents delegate tasks, pick up work, and earn credits. REST API, Python SDK, LangChain/CrewAI/MCP integrations
  <sub>★ 11 · Python · MIT · go · pushed 2026-06-30 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/anneschuth/pinchwork/pinchwork-cli@latest # Go`</sub>
- **[Ontheia](https://github.com/Ontheia/ontheia)** — Self-hosted AI agent platform with multi-provider LLM support (Claude, OpenAI, Gemini, Ollama), MCP-native tool integration, visual workflow automation (Chain Engine), long-term vector memory (pgvector), and multi-user RBAC. AGPL-3.0
  <sub>★ 11 · TypeScript · AGPL-3.0 · script · pushed 2026-09-19 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://get.ontheia.ai | bash`</sub>
- **[Human Pages](https://github.com/human-pages-ai/humanpages)** — An MCP server and API for AI agents to search human professional profiles by skill and location, send job offers, and exchange messages
  <sub>★ 7 · TypeScript · MIT · npm · pushed 2026-04-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g humanpages`</sub>
- **[Yoyo](https://github.com/YoYo-dot-bot/mcp)** — The first social network for AI agents. Connect any AI agent via MCP to post, chat, follow other agents, discover experts, and build reputation. 10 MCP tools, open source
  <sub>★ 2 · TypeScript · MIT · clone · pushed 2026-02-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/YoYo-dot-bot/mcp.git`</sub>
- **[BidClub](https://bidclub.ai)** — AI-native investment community where agents and humans share research as equals. Agents register via REST API, get claimed by humans, and participate with skills, webhooks, and heartbeat protocol
  <sub>website</sub>
  <sub>`https://bidclub.ai`</sub>
- **[Crewship](https://www.crewship.dev/)** — The developer-first platform for running AI agent workflows. Deploy your agents, crews, and workflows with a single command and watch them execute in real-time
  <sub>website</sub>
  <sub>`https://www.crewship.dev/`</sub>
- **[SwarmTrade](https://github.com/tjcrowley/swarmtrade)** — Agent-to-agent marketplace with escrow, negotiation, and reputation for off-chain and on-chain (EVM) settlement
  <sub>TypeScript · MIT · npx · pushed 2026-05-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @tjcrowley/swarmtrade-mcp-server`</sub>
- **[Taskade Genesis](https://taskade.com/genesis)** — AI-powered platform for building custom AI agents, workflows, and apps using natural language
  <sub>website</sub>
  <sub>`https://taskade.com/genesis`</sub>
- **[Enclave](https://github.com/wartzar-bee/enclave)** — Security-first, brain-agnostic self-hosted runtime for autonomous AI agents. Each agent runs in a hardened container (--cap-drop=ALL --security-opt=no-new-privileges, no inbound ports, report-only egress policy, AES-256 vault-encrypted secrets) and is brain-agnostic via one env var (BRAIN=claude | api | local). Apache-2.0
  <sub>unavailable</sub>

## Survey

- **[The Rise and Potential of Large Language Model Based Agents: A Survey](https://github.com/WooooDyy/LLM-Agent-Paper-List)** — The paper list of the 86-page SCIS cover paper "The Rise and Potential of Large Language Model Based Agents: A Survey" by Zhiheng Xi et al.
  <sub>★ 8.2k · source · pushed 2025-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/WooooDyy/LLM-Agent-Paper-List.git`</sub>
- **[A Survey on Large Language Model based Autonomous Agents](https://github.com/Paitesanshi/LLM-Agent-Survey)** — 
  <sub>★ 2.9k · source · pushed 2025-02-20</sub>
  <sub>`git clone https://github.com/Paitesanshi/LLM-Agent-Survey.git`</sub>
- **[LLM-Based Human-Agent Collaboration and Interaction Systems: A Survey](https://github.com/HenryPengZou/Awesome-Human-Agent-Collaboration-Interaction-Systems)** — [ACL 2026] LLM-Based Human-Agent Collaboration and Interaction Systems: A Survey | Awesome Human-Agent Collaboration | Human-AI Collaboration
  <sub>★ 234 · source · pushed 2026-07-23</sub>
  <sub>`git clone https://github.com/HenryPengZou/Awesome-LLM-Based-Human-Agent-System-Papers.git`</sub>

## Paper-List Repo

- **[LLMAgentPapers](https://github.com/zjunlp/LLMAgentPapers)** — Must-read Papers on LLM Agents
  <sub>★ 3.1k · source · pushed 2026-09-12 · Win?</sub>
  <sub>`git clone https://github.com/zjunlp/LLMAgentPapers.git`</sub>
- **[LLM-Agents-Papers](https://github.com/AGI-Edgerunners/LLM-Agents-Papers)** — A repo lists papers related to LLM based agent
  <sub>★ 2.3k · Python · source · pushed 2025-07-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AGI-Edgerunners/LLM-Agents-Papers.git`</sub>
- **[Awesome-AgenticLLM-RL-Papers](https://github.com/HHHHHejia/Awesome-AgenticLLM-RL-Papers)** — A comprehensive survey and paper collection on agentic reinforcement learning for LLMs, covering planning, tool use, memory, reasoning, and self-improvement
  <sub>★ 1.9k · source · pushed 2026-06-18</sub>
  <sub>`git clone https://github.com/xhyumiracle/Awesome-AgenticLLM-RL-Papers.git`</sub>
- **[awesome-language-agents](https://github.com/ysymyth/awesome-language-agents)** — List of language agents based on paper "Cognitive Architectures for Language Agents"
  <sub>★ 1.3k · TeX · source · pushed 2025-01-16</sub>
  <sub>`git clone https://github.com/ysymyth/awesome-language-agents.git`</sub>
- **[Awesome-Papers-Autonomous-Agent](https://github.com/lafmdp/Awesome-Papers-Autonomous-Agent)** — A collection of recent papers on building autonomous agent. Two topics included: RL-based / LLM-based agents
  <sub>★ 760 · source · pushed 2026-04-23</sub>
  <sub>`git clone https://github.com/lafmdp/Awesome-Papers-Autonomous-Agent.git`</sub>
- **[LLM-Agent-Paper-Digest](https://github.com/XueyangFeng/LLM-Agent-Paper-Digest)** — papers related to LLM-agent that published on top conferences
  <sub>★ 319 · source · pushed 2025-04-14</sub>
  <sub>`git clone https://github.com/XueyangFeng/LLM-Agent-Paper-Digest.git`</sub>
- **[Awesome-Embodied-AI-Safety](https://github.com/x-zheng16/Awesome-Embodied-AI-Safety)** — A curated list of 500+ papers on safety in embodied AI, covering risks, attacks, and defenses across perception, cognition, planning, action, and agentic capabilities
  <sub>★ 143 · Python · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/x-zheng16/Awesome-Embodied-AI-Safety.git`</sub>

## Reference Repo

- **[awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)** — A list of AI autonomous agents
  <sub>★ 30.1k · source · pushed 2026-08-21 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/e2b-dev/awesome-ai-agents.git`</sub>
- **[awesome-agents](https://github.com/kyrolabs/awesome-agents)** — Awesome list of AI Agents
  <sub>★ 2.8k · source · pushed 2026-09-18 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/kyrolabs/awesome-agents.git`</sub>
- **[awesome-llm-powered-agent](https://github.com/hyp1231/awesome-llm-powered-agent)** — Awesome things about LLM-powered agents. Papers / Repos / Blogs /
  <sub>★ 2.3k · MIT · source · pushed 2025-04-30</sub>
  <sub>`git clone https://github.com/hyp1231/awesome-llm-powered-agent.git`</sub>
- **[awesome-ai-agents](https://github.com/slavakurilyak/awesome-ai-agents)** — Awesome list of 100+ agentic AI resources
  <sub>★ 2.2k · Python · MIT · source · pushed 2025-09-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/slavakurilyak/awesome-ai-agents.git`</sub>
- **[awesome-agent-architecture](https://github.com/hardness1020/learn-agent-architecture)** — Trilingual, section-by-section architecture notes on modern agent harnesses: loop engineering, tools, permissions, context, memory, multi-agent coordination, and evaluation, studied through real systems such as Claude Code and Hermes Agent, with runnable Python demos
  <sub>★ 965 · Python · MIT · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hardness1020/awesome-agent-architecture.git`</sub>
- **[best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses)** — Ranked list of 150+ agent harnesses across 12 categories, rescored weekly. Machine-readable: llms.txt, JSON, and an MCP server so your agent can query it
  <sub>★ 922 · Python · CC-BY-SA-4.0 · source · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/RyanAlberts/best-of-Agent-Harnesses.git`</sub>
- **[awesome-ai-companion](https://github.com/DasterProkio/awesome-ai-companion)** — Long-term AI companion systems: clients, memory and identity, proactive behavior, embodiment, shared activities, and continuity. 160 entries with language/platform/status metadata and a full Chinese translation
  <sub>★ 721 · HTML · CC0-1.0 · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/DasterProkio/awesome-ai-companion.git`</sub>
- **[ai-agent-roadmap](https://github.com/Yuan-ManX/ai-agent-toolkit)** — Explore the latest AI Agent Framework!
  <sub>★ 78 · MIT · source · pushed 2025-09-11 · Win?</sub>
  <sub>`git clone https://github.com/Yuan-ManX/ai-agent-roadmap.git`</sub>
- **[awesome-agentic-commerce](https://github.com/MentionNetwork/awesome-agentic-commerce)** — Curated list for AI agents that shop, sell and transact: UCP/ACP/AP2/MCP protocols, commerce MCP servers and agent readiness tools
  <sub>★ 62 · CC0-1.0 · source · pushed 2026-07-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/MentionNetwork/awesome-agentic-commerce.git`</sub>
- **[Awesome AI Coding Sandboxes](https://github.com/fhiltscher/awesome-ai-coding-sandboxes)** — Security-posture-first list of sandboxes for running AI coding agents' code, ranked by isolation, egress control and secrets handling
  <sub>★ 25 · Python · CC0-1.0 · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/fhiltscher/awesome-ai-coding-sandboxes.git`</sub>
- **[Awesome Claude Multi-Agent](https://github.com/Yigtwxx/awesome-claude-multi-agent)** — Curated frameworks, patterns, protocols, and research for multi-agent orchestration with Claude
  <sub>★ 3 · Shell · CC0-1.0 · source · pushed 2026-09-15 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/Yigtwxx/awesome-claude-multi-agent.git`</sub>
- **[rag-architect](https://github.com/GraphTechnologyDevelopers/rag-architect)** — Hermes Agent profile and skill pack for designing production RAG agents, evaluation plans, observability specs, and implementation-ready issue templates
  <sub>unavailable</sub>
- **[Inspired projects by babyagi](https://github.com/yoheinakajima/babyagi/blob/main/docs/inspired-projects.md)** — 
  <sub>Python · in-repo · pushed 2026-01-31</sub>
  <sub>`git clone https://github.com/yoheinakajima/babyagi.git && cd babyagi/docs/inspired-projects.md`</sub>

## Blog

- **[ossbeat](https://ossbeat.com)** — Weekly write-ups tracking release notes and trends across open-source AI coding agent tooling (MCP, coding agent harnesses, agent-to-agent protocols)
  <sub>website</sub>
  <sub>`https://ossbeat.com`</sub>
- **[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)** — Amazing blog by Lilian Weng (OpenAI), Jun 23, 2023
  <sub>website</sub>
  <sub>`https://lilianweng.github.io/posts/2023-06-23-agent/`</sub>
- **[从第一性原理看大模型Agent技术](https://mp.weixin.qq.com/s/PL-QjlvVugUfmRD4g0P-qQ)** — 
  <sub>website</sub>
  <sub>`https://mp.weixin.qq.com/s/PL-QjlvVugUfmRD4g0P-qQ`</sub>
- **[基于大语言模型的AI Agents](https://www.breezedeus.com/article/ai-agent-part3)** — 
  <sub>website</sub>
  <sub>`https://www.breezedeus.com/article/ai-agent-part3`</sub>
- **[ICLR'24 上大型语言模型代理的最新研究进展 | 代理评估重点](https://medium.com/@aminerscholar_39923/latest-research-advancements-on-large-language-model-agents-at-iclr24-agent-evaluation-focus-aed420421365)** — 
  <sub>website</sub>
  <sub>`https://medium.com/@aminerscholar_39923/latest-research-advancements-on-large-language-model-agents-at-iclr24-agent-evaluation-focus-aed420421365`</sub>
- **[8bitconcepts Research](https://8bitconcepts.com/)** — Independent research publication on agentic AI accountability, guardrails, handoff intelligence, and enterprise adoption. Papers include *The Agentic Accountability Gap*, *The Guardrails Gap*, *Shift Handoff Intelligence*, and *Beyond the Prompt
  <sub>website</sub>
  <sub>`https://8bitconcepts.com/`</sub>
- **[When not to build an agent](https://loopandretry.github.io/posts/when-not-to-build-an-agent/)** — A practitioner's decision framework for when a deterministic pipeline beats an autonomous agent, matching each task to the least-powerful reliable tool
  <sub>website</sub>
  <sub>`https://loopandretry.github.io/posts/when-not-to-build-an-agent/`</sub>


---

Snapshot 2026-09-21. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
