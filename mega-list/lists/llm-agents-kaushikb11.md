# LLM Agents (kaushikb11)

A curated list of awesome LLM agents frameworks.

Curated by **[kaushikb11/awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

109 entries · 109 distinct repos · 12 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/openclaw/openclaw"><img src="https://opengraph.githubassets.com/1/openclaw/openclaw" width="260"></a> | <a href="https://github.com/langchain-ai/langchain"><img src="https://opengraph.githubassets.com/1/langchain-ai/langchain" width="260"></a> | <a href="https://github.com/huggingface/smolagents"><img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/smolagents/smolagents.png" width="260"></a> |
| **[OpenClaw](https://github.com/openclaw/openclaw)**<br>★ 392.1k | **[LangChain](https://github.com/langchain-ai/langchain)**<br>★ 147.9k | **[Smolagents](https://github.com/huggingface/smolagents)**<br>★ 29.9k |
| <a href="https://github.com/mastra-ai/mastra"><img src="https://opengraph.githubassets.com/1/mastra-ai/mastra" width="260"></a> | <a href="https://github.com/microsoft/semantic-kernel"><img src="https://opengraph.githubassets.com/1/microsoft/semantic-kernel" width="260"></a> | <a href="https://github.com/google/adk-python"><img src="https://raw.githubusercontent.com/google/adk-python/main/assets/adk-web-dev-ui.png" width="260"></a> |
| **[Mastra](https://github.com/mastra-ai/mastra)**<br>★ 28.8k | **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)**<br>★ 28.7k | **[Google ADK](https://github.com/google/adk-python)**<br>★ 21.9k |

## Contents

- [Core Frameworks](#core-frameworks) (34)
- [Autonomous Agents (2023 wave)](#autonomous-agents-2023-wave) (4)
- [Multi-Agent Orchestration](#multi-agent-orchestration) (14)
- [CLI Agent Harnesses](#cli-agent-harnesses) (14)
- [Low-Code &amp; Visual Builders](#low-code--visual-builders) (3)
- [Agent Infrastructure](#agent-infrastructure) (3)
- [Retrieval &amp; Data](#retrieval--data) (2)
- [Memory &amp; Context](#memory--context) (6)
- [Safety, Security &amp; Evaluation](#safety-security--evaluation) (6)
- [Domain-Specific Agents](#domain-specific-agents) (11)
- [Inactive](#inactive) (5)
- [Research &amp; Experimental](#research--experimental) (7)

## Core Frameworks

- **[OpenClaw](https://github.com/openclaw/openclaw)** — Personal AI assistant that runs on any platform
  <sub>★ 392.1k · TypeScript · MIT · npm · pushed 2026-10-15 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g openclaw@latest --allow-scripts=openclaw`</sub>
- **[LangChain](https://github.com/langchain-ai/langchain)** — Compose LLM apps from modular pieces
  <sub>★ 147.9k · Python · MIT · source · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/langchain.git`</sub>
- **[Smolagents](https://github.com/huggingface/smolagents)** — Minimal agents that write code to act
  <sub>★ 29.9k · Python · Apache-2.0 · pip · pushed 2026-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "smolagents[toolkit]"`</sub>
- **[Mastra](https://github.com/mastra-ai/mastra)** — TypeScript agents with RAG and observability
  <sub>★ 28.8k · TypeScript · source · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git`</sub>
- **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** — Plugin-based AI integration for .NET and Python
  <sub>★ 28.7k · C# · MIT · pip · pushed 2026-10-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install semantic-kernel`</sub>
- **[Google ADK](https://github.com/google/adk-python)** — Code-first agents that deploy to Vertex AI
  <sub>★ 21.9k · Python · Apache-2.0 · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install google-adk`</sub>
- **[Pydantic AI](https://github.com/pydantic/pydantic-ai)** — Type-safe agents on Pydantic with structured output
  <sub>★ 20.6k · Python · MIT · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --with pydantic-ai-harness clai -a pydantic_ai_harness.coder:coder_agent -m anthropic:claude-fable-5-1`</sub>
- **[Tambo](https://github.com/tambo-ai/tambo)** — React components rendered by AI at runtime
  <sub>★ 11.2k · TypeScript · MIT · source · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tambo-ai/tambo.git`</sub>
- **[Hive](https://github.com/aden-hive/hive)** — Multi-agent harness aimed at production
  <sub>★ 11.1k · Python · Apache-2.0 · clone · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aden-hive/hive.git`</sub>
- **[Openwork](https://github.com/accomplish-ai/coworker)** — Open-source AI coworker platform
  <sub>★ 10.8k · source · pushed 2026-08-13</sub>
  <sub>`git clone https://github.com/accomplish-ai/coworker.git`</sub>
- **[Upsonic](https://github.com/Upsonic/Upsonic)** — Agents with MCP and isolated execution
  <sub>★ 8k · Python · MIT · source · pushed 2026-06-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upsonic/upsonic.git`</sub>
- **[Atomic Agents](https://github.com/Eigenwise/atomic-agents)** — Compose agents from small interchangeable parts
  <sub>★ 6.3k · Python · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add eigenwise/atomic-agents`</sub>
- **[OpenAgent](https://github.com/the-open-agent/openagent)** — Personal assistant built on LLM, RAG and agent loops
  <sub>★ 5.7k · Go · Apache-2.0 · psh · pushed 2026-10-15 · Win · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/the-open-agent/openagent/master/scripts/install.ps1 | iex`</sub>
- **[AG2](https://github.com/ag2ai/ag2)** — Community fork of AutoGen, now an AgentOS
  <sub>★ 5k · Python · Apache-2.0 · pip · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ag2-classic`</sub>
- **[Oh My Hermes](https://github.com/rlaope/oh-my-hermes)** — Harness with optimized tools and memory
  <sub>★ 3.4k · Python · MIT · psh · pushed 2026-10-15 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://raw.githubusercontent.com/rlaope/oh-my-hermes/main/install.ps1 | iex`</sub>
- **[AGiXT](https://github.com/Josh-XT/AGiXT)** — Multi-provider agent platform with command chaining
  <sub>★ 3.2k · Python · MIT · pip · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agixt`</sub>
- **[trpc-agent-go](https://github.com/trpc-group/trpc-agent-go)** — Go framework for agents with graph workflows
  <sub>★ 1.9k · Go · Apache-2.0 · clone · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trpc-group/trpc-agent-go.git`</sub>
- **[Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS)** — Specialist agent hub with temporary orchestrators
  <sub>★ 1.6k · Python · Apache-2.0 · psh · pushed 2026-10-14 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://agentlas.cloud/install.ps1 | iex # Windows PowerShell`</sub>
- **[Ouroboros](https://github.com/razzant/ouroboros)** — Agent runtime with reviewed self-modification
  <sub>★ 1.5k · Python · MIT · uv · pushed 2026-10-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install "git+https://github.com/razzant/ouroboros.git@ouroboros"`</sub>
- **[ConnectOnion](https://github.com/openonion/connectonion)** — Python framework focused on agent collaboration
  <sub>★ 1.5k · Python · Apache-2.0 · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade 'connectonion==1.9.2'`</sub>
- **[LightAgent](https://github.com/wanxingai/LightAgent)** — Lightweight Python agents with tools and memory
  <sub>★ 1.2k · Python · Apache-2.0 · pip · pushed 2026-09-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lightagent`</sub>
- **[ix](https://github.com/kreneskyp/ix)** — Autonomous agents with a visual workflow builder
  <sub>★ 1k · Python · MIT · pip · pushed 2026-10-10 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install agent-ix`</sub>
- **[Promptise Foundry](https://github.com/promptise-com/Foundry)** — Agentic framework with controllable reasoning
  <sub>★ 873 · Python · Apache-2.0 · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install promptise`</sub>
- **[Aeon](https://github.com/aeonfun/aeon)** — Runs unattended on GitHub Actions, self-healing
  <sub>★ 774 · JavaScript · MIT · clone · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aeonfun/aeon`</sub>
- **[Octochains](https://github.com/ahmadvh/octochains)** — Parallel isolated reasoning with an aggregator
  <sub>★ 377 · Python · pip · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install octochains`</sub>
- **[Axar](https://github.com/axar-ai/axar)** — Minimal TypeScript agents with Zod validation
  <sub>★ 166 · TypeScript · Apache-2.0 · source · pushed 2026-02-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/axar-ai/axar.git`</sub>
- **[Neurolink](https://github.com/juspay/neurolink)** — One interface across 12+ LLM providers
  <sub>★ 157 · TypeScript · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @juspay/neurolink --help`</sub>
- **[NarraNexus](https://github.com/NetMindAI-Open/NarraNexus)** — Builds nexuses where agent intelligence emerges
  <sub>★ 91 · Python · Apache-2.0 · clone · pushed 2026-10-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/NetMindAI-Open/NarraNexus.git`</sub>
- **[ProtoLink](https://github.com/nMaroulis/protolink)** — Python agents with native A2A communication
  <sub>★ 86 · Python · MIT · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install 'protolink[integrations]'`</sub>
- **[KodeAgent](https://github.com/barun-saha/kodeagent)** — Minimal agent engine, deliberately small
  <sub>★ 43 · Python · Apache-2.0 · pip · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U kodeagent # Upgrade existing installation`</sub>
- **[Octomind](https://github.com/Muvon/octomind)** — Model-agnostic runtime with specialist agents
  <sub>source</sub>
  <sub>`git clone https://github.com/Muvon/octomind.git`</sub>
- **[OpenProgram](https://github.com/Fzkuji/OpenProgram)** — Agents create and refine their own workflows
  <sub>unavailable</sub>
- **[ShaprAI](https://github.com/Scottcjn/shaprai)** — Sharpens raw models into principled agents
  <sub>unavailable</sub>
- **[TrashClaw](https://github.com/Scottcjn/trashclaw)** — Zero-dependency local agent for old hardware
  <sub>unavailable</sub>

## Autonomous Agents (2023 wave)

- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** — The original autonomous GPT-4 agent loop
  <sub>★ 187.6k · Python · source · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Significant-Gravitas/AutoGPT.git`</sub>
- **[OpenManus](https://github.com/FoundationAgents/OpenManus)** — General-purpose agent, no invite code needed
  <sub>★ 58.7k · Python · MIT · clone · pushed 2026-09-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FoundationAgents/OpenManus.git`</sub>
- **[BabyAGI](https://github.com/yoheinakajima/babyagi)** — Minimal task-driven autonomous agent loop
  <sub>★ 22.4k · Python · pip · pushed 2026-01-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install babyagi`</sub>
- **[XAgent](https://github.com/OpenBMB/XAgent)** — Autonomous agent with planning and tool learning
  <sub>★ 8.5k · Python · Apache-2.0 · source · pushed 2026-07-31 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/OpenBMB/XAgent.git`</sub>

## Multi-Agent Orchestration

- **[MetaGPT](https://github.com/FoundationAgents/MetaGPT)** — Agents role-play a software company
  <sub>★ 70.9k · Python · MIT · pip · pushed 2026-01-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade metagpt`</sub>
- **[AutoGen](https://github.com/microsoft/autogen)** — Conversational multi-agent systems
  <sub>★ 61.4k · Python · CC-BY-4.0 · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "autogen-agentchat" "autogen-ext[openai]"`</sub>
- **[CrewAI](https://github.com/crewAIInc/crewAI)** — Orchestrate role-playing agent crews
  <sub>★ 59.7k · Python · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add crewaiinc/skills`</sub>
- **[CAMEL](https://github.com/camel-ai/camel)** — Role-playing agents for studying agent society
  <sub>★ 17.9k · Python · Apache-2.0 · pip · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install camel-ai`</sub>
- **[PraisonAI](https://github.com/MervinPraison/PraisonAI)** — Multi-agent workflows with self-reflection
  <sub>★ 9.2k · Python · MIT · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install praisonai`</sub>
- **[OpenAgents](https://github.com/openagents-org/openagents)** — Agent networks over WebSocket, gRPC, MCP and A2A
  <sub>★ 4.2k · TypeScript · Apache-2.0 · psh · pushed 2026-10-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://openagents.org/install.ps1 | iex`</sub>
- **[hcom](https://github.com/aannoo/hcom)** — Agents message and spawn each other in terminals
  <sub>★ 572 · Rust · MIT · psh · pushed 2026-10-15 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://github.com/aannoo/hcom/releases/latest/download/hcom-installer.ps1 | iex`</sub>
- **[Markus](https://github.com/markus-global/markus)** — Agents coordinate and review each other's work
  <sub>★ 204 · TypeScript · Apache-2.0 · npm · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @markus-global/cli`</sub>
- **[CommonGround Kernel](https://github.com/Intelligent-Internet/CommonGround)** — Postgres-backed shared substrate for agent teams
  <sub>★ 153 · Python · Apache-2.0 · uv · pushed 2026-05-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install commonground-kernel`</sub>
- **[Flock](https://github.com/whiteducksoftware/flock)** — Declarative agents via blackboard architecture
  <sub>★ 121 · Python · MIT · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install flock-core # or: uv add flock-core`</sub>
- **[Quorum](https://github.com/Detrol/quorum-cli)** — Structured multi-agent debate in the terminal
  <sub>★ 121 · Python · uv · pushed 2026-09-27 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`uvx --from quorum-cli quorum-mcp-server`</sub>
- **[OpenAcme](https://github.com/sandydasari/openacme)** — Role-specialized agents that self-organize
  <sub>★ 89 · TypeScript · MIT · npm · pushed 2026-07-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @openacme/cli`</sub>
- **[Hivekeep](https://github.com/MarlBurroW/hivekeep)** — Self-hosted team of persistent personal agents
  <sub>★ 69 · TypeScript · MIT · script · pushed 2026-10-15 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/MarlBurroW/hivekeep/main/install.sh | bash`</sub>
- **[auto-co](https://github.com/NikitaDmitrieff/auto-co-meta)** — 14 agents run a company in a continuous loop
  <sub>★ 51 · TypeScript · MIT · npx · pushed 2026-06-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx create-auto-co my-company`</sub>

## CLI Agent Harnesses

- **[Atomic Agent](https://github.com/AtomicBot-ai/atomic-agent)** — Local-first CLI agent for open-weight models
  <sub>★ 3.3k · TypeScript · MIT · psh · pushed 2026-10-15 · macOS</sub>
  <sub>`irm https://atomicagent.io/install.ps1 | iex`</sub>
- **[Agent Teams](https://github.com/777genius/agent-teams-ai)** — Desktop app running coding-agent teams across CLIs
  <sub>★ 2.3k · TypeScript · AGPL-3.0 · clone · pushed 2026-10-15 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/777genius/agent-teams-ai.git`</sub>
- **[Bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Deterministic orchestrator for 40+ CLI agents
  <sub>★ 1.3k · Python · Apache-2.0 · uv · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[h5i](https://github.com/h5i-dev/h5i)** — Runs agents in sandboxes, merges the verified result
  <sub>★ 779 · Rust · Apache-2.0 · npx · pushed 2026-10-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add h5i-dev/h5i # if you do not have the binary yet`</sub>
- **[SwarmClaw](https://github.com/swarmclawai/swarmclaw)** — Self-hosted runtime for multi-agent CLI work
  <sub>★ 689 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @swarmclawai/swarmclaw`</sub>
- **[Dorothy](https://github.com/Charlie85270/Dorothy)** — Desktop app to run several CLI agents at once
  <sub>★ 351 · TypeScript · MIT · clone · pushed 2026-07-07 · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/Charlie85270/Dorothy.git`</sub>
- **[ClawFleet](https://github.com/clawfleet/ClawFleet)** — Deploys isolated agent instances via Docker
  <sub>★ 175 · Go · MIT · script · pushed 2026-04-27 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://clawfleet.io/install.sh | sh`</sub>
- **[OpenPaw](https://github.com/daxaur/openpaw)** — Turns Claude Code into an assistant with 38 skills
  <sub>★ 173 · TypeScript · MIT · source · pushed 2026-05-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/daxaur/openpaw.git`</sub>
- **[ORCH](https://github.com/oxgeneral/ORCH)** — One CLI to manage a team of agents on tasks
  <sub>★ 173 · TypeScript · MIT · npm · pushed 2026-08-01 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g @oxgeneral/orch # Install`</sub>
- **[OpenHermit](https://github.com/HCF-STUDIOS/openhermit)** — Deploys agent fleets as long-running services
  <sub>★ 88 · TypeScript · MIT · npm · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g openhermit`</sub>
- **[5dive](https://github.com/5dive-ai/5dive)** — Run a company of named agents on your own server
  <sub>★ 71 · Shell · MIT · npx · pushed 2026-10-15 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`npx -y skills add https://github.com/5dive-ai/skills --skill 5dive-cli --agent <runtime> --yes`</sub>
- **[Agon](https://github.com/AutoResearch-Factory/Agon)** — Claude Code plugin for autonomous research loops
  <sub>★ 54 · Python · MIT · clone · pushed 2026-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AutoResearch-Factory/Agon.git`</sub>
- **[TeamHero](https://github.com/sagiyaacoby/TeamHero)** — Manage agents like a team, with structured roles
  <sub>★ 38 · JavaScript · MIT · clone · pushed 2026-04-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sagiyaacoby/TeamHero.git`</sub>
- **[OpenSepia](https://github.com/CelaenoIndustry/OpenSepia)** — Nine Claude agents running as an agile team
  <sub>★ 35 · Python · MIT · clone · pushed 2026-03-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/CelaenoIndustry/OpenSepia.git`</sub>

## Low-Code &amp; Visual Builders

- **[Dify](https://github.com/langgenius/dify)** — Visual orchestration for LLM apps and agents
  <sub>★ 158.6k · TypeScript · source · pushed 2026-10-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/langgenius/dify.git`</sub>
- **[Kiln AI](https://github.com/Kiln-AI/Kiln)** — Desktop app for evals, RAG and fine-tuning
  <sub>★ 5.2k · Python · pip · pushed 2026-10-15 · Win · WSL2? · macOS · Linux?</sub>
  <sub>`pip install kiln-ai`</sub>
- **[Heym](https://github.com/heymrun/heym)** — Visual builder for agentic workflow automation
  <sub>★ 1.2k · Python · clone · pushed 2026-10-14 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/heymrun/heym.git`</sub>

## Agent Infrastructure

- **[Mem0](https://github.com/mem0ai/mem0)** — Memory layer that persists across agent sessions
  <sub>★ 67.2k · Python · Apache-2.0 · npm · pushed 2026-10-14 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @mem0/cli # or: pip install mem0-cli`</sub>
- **[AgentField](https://github.com/Agent-Field/agentfield)** — Agent identity and RPC using W3C DIDs
  <sub>★ 2.6k · Go · Apache-2.0 · script · pushed 2026-10-15 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentfield.ai/install.sh | bash`</sub>
- **[openma](https://github.com/openma-ai/open-managed-agents)** — Self-hosted Managed Agents API implementation
  <sub>★ 323 · TypeScript · Apache-2.0 · clone · pushed 2026-10-15 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openma-ai/open-managed-agents.git`</sub>

## Retrieval &amp; Data

- **[LlamaIndex](https://github.com/run-llama/llama_index)** — Connects LLMs to 160+ data sources
  <sub>★ 52.5k · Python · MIT · pip · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llama-index-core`</sub>
- **[Haystack](https://github.com/deepset-ai/haystack)** — Composable pipelines for search and RAG
  <sub>★ 26.7k · Python · Apache-2.0 · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install haystack-ai`</sub>

## Memory &amp; Context

- **[Hindsight](https://github.com/vectorize-io/hindsight)** — Agent memory with retain, recall and reflect
  <sub>★ 50k · Python · MIT · npx · pushed 2026-10-15 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[Caura](https://github.com/caura-ai/caura)** — Governed shared memory for fleets of agents
  <sub>★ 496 · Python · Apache-2.0 · pip · pushed 2026-10-15 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install caura-client`</sub>
- **[AnimaWorks](https://github.com/xuiltul/animaworks)** — Organization-as-code with brain-inspired memory
  <sub>★ 266 · Python · Apache-2.0 · pip · pushed 2026-10-15 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install animaworks[transcribe]`</sub>
- **[OMEGA](https://github.com/omega-memory/omega-memory)** — Persistent memory for coding agents over MCP
  <sub>★ 224 · Python · Apache-2.0 · uv · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "omega-memory[server]"`</sub>
- **[Inite Brain](https://github.com/inite-ai/inite-brain-service)** — Bitemporal knowledge graph as agent memory
  <sub>★ 41 · TypeScript · AGPL-3.0 · script · pushed 2026-10-14 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://brain.inite.ai/install.sh | sh`</sub>
- **[Perseus](https://github.com/Perseus-Computing-LLC/perseus)** — Resolves verified workspace state before a call
  <sub>unavailable</sub>

## Safety, Security &amp; Evaluation

- **[Agentic Radar](https://github.com/splx-ai/agentic-radar)** — Scans agent workflows for CVE and OWASP issues
  <sub>★ 1.1k · Python · Apache-2.0 · pip · pushed 2025-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentic-radar`</sub>
- **[Cordum](https://github.com/cordum-io/cordum)** — Evaluates policy before an agent action dispatches
  <sub>★ 509 · Go · helm · pushed 2026-10-14 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`helm install cordum oci://ghcr.io/cordum-io/cordum/charts/cordum \`</sub>
- **[Greywall](https://github.com/GreyhavenHQ/greywall)** — Deny-by-default sandbox for coding agents
  <sub>★ 309 · Go · Apache-2.0 · go · pushed 2026-08-13 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/GreyhavenHQ/greywall/cmd/greywall@latest`</sub>
- **[Kitaru](https://github.com/zenml-io/kitaru)** — Record, replay and improve agents in production
  <sub>★ 308 · Python · Apache-2.0 · script · pushed 2026-10-14 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://kitaru.ai/install | bash`</sub>
- **[RapidFire AI](https://github.com/RapidFireAI/rapidfireai)** — Experiment harness for RAG and fine-tuning runs
  <sub>★ 170 · JavaScript · Apache-2.0 · pip · pushed 2026-10-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install rapidfireai`</sub>
- **[APort Guardrails](https://github.com/aporthq/aport-agent-guardrails)** — Pre-action authorization policy for agent calls
  <sub>★ 28 · Shell · npx · pushed 2026-10-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @aporthq/aport-agent-guardrails github`</sub>

## Domain-Specific Agents

- **[DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze)** — Autonomous data science without fixed workflows
  <sub>★ 4.7k · Python · MIT · source · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ruc-datalab/DeepAnalyze.git`</sub>
- **[Darkmoon](https://github.com/ASCIT31/Dark-Moon)** — Autonomous pentesting across web, cloud and AD
  <sub>★ 1k · Python · GPL-3.0 · script · pushed 2026-10-01 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://portal.dark-moon.org/deploy | bash -s -- aws --license <KEY> --api-key <LLM_KEY>`</sub>
- **[RAI](https://github.com/RobotecAI/rai)** — Agent framework for robotics, built on ROS 2
  <sub>★ 602 · Python · Apache-2.0 · source · pushed 2026-10-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/RobotecAI/rai.git`</sub>
- **[CleverBee](https://github.com/SureScaleAI/cleverbee)** — Deep research agent that browses with Playwright
  <sub>★ 301 · Python · AGPL-3.0 · clone · pushed 2026-01-31 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SureScaleAI/cleverbee.git`</sub>
- **[text2sql-framework](https://github.com/Text2SqlAgent/text2sql-framework)** — Text-to-SQL agent that explores schema, not RAG
  <sub>★ 160 · Python · MIT · pip · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "text2sql-framework[anthropic]" # or: "text2sql-framework[openai]"`</sub>
- **[GenoMAS](https://github.com/Liu-Hy/GenoMAS)** — Multi-agent pipeline for genomics data analysis
  <sub>★ 135 · Python · MIT · source · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Liu-Hy/GenoMAS.git`</sub>
- **[wechat-mac-rpa](https://github.com/wq19901103wq/wechat-mac-rpa)** — Visual agent automating WeChat on macOS
  <sub>★ 122 · Python · MIT · source · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wq19901103wq/wechat-mac-rpa.git`</sub>
- **[DNA Claude Analysis](https://github.com/shmlkv/dna-claude-analysis)** — Explore your genome in natural language
  <sub>★ 58 · Python · MIT · source · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/shmlkv/dna-claude-analysis.git`</sub>
- **[everyrow](https://github.com/futuresearch/futuresearch-python)** — Run LLM agents over pandas DataFrames
  <sub>★ 57 · Python · MIT · pip · pushed 2026-10-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install futuresearch`</sub>
- **[Inalpha](https://github.com/mirror29/inalpha)** — Quant agents that pick factors that still work
  <sub>★ 44 · Python · AGPL-3.0 · clone · pushed 2026-10-14 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/mirror29/inalpha.git`</sub>
- **[Omni-Rewriter](https://github.com/WayneJin0918/Omni-Rewriter)** — Prompt expansion for image and video generation
  <sub>unavailable</sub>

## Inactive

- **[Flowise](https://github.com/FlowiseAI/Flowise)** — Drag-and-drop builder for LLM flows
  <sub>★ 55.5k · TypeScript · npm · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g flowise`</sub>
- **[SuperAGI](https://github.com/TransformerOptimus/SuperAGI)** — Autonomous agent platform with a tool framework
  <sub>★ 17.7k · Python · MIT · clone · pushed 2025-01-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/TransformerOptimus/SuperAGI.git`</sub>
- **[OpenAgents (XLang)](https://github.com/xlang-ai/OpenAgents)** — Platform for data, web and coding agents
  <sub>★ 4.9k · Python · Apache-2.0 · source · pushed 2024-11-18 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/xlang-ai/OpenAgents.git`</sub>
- **[Agent Protocol](https://github.com/agi-inc/agent-protocol)** — Standard interface for agent interoperability
  <sub>★ 1.5k · Python · MIT · source · pushed 2025-04-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agi-inc/agent-protocol.git`</sub>
- **[AI Legion](https://github.com/eumemic/ai-legion)** — TypeScript swarm of autonomous agents
  <sub>★ 1.4k · TypeScript · MIT · source · pushed 2025-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/eumemic/ai-legion.git`</sub>

## Research &amp; Experimental

- **[EvoAgentX](https://github.com/ANative-Lab/EvoAgentX)** — Agent workflows that evolve and self-optimize
  <sub>★ 3.4k · Python · pip · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evoagentx`</sub>
- **[AgentFlow](https://github.com/lupantech/AgentFlow)** — Trainable multi-agent system using Flow-GRPO
  <sub>★ 2.1k · Python · MIT · source · pushed 2026-02-08 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/lupantech/AgentFlow.git`</sub>
- **[Cache-to-Cache](https://github.com/thu-nics/C2C)** — Agents exchange meaning directly via KV-cache
  <sub>★ 728 · Python · Apache-2.0 · source · pushed 2026-10-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/thu-nics/C2C.git`</sub>
- **[AgentSquare](https://github.com/tsinghua-fib-lab/AgentSquare)** — Automatic search over modular agent designs
  <sub>★ 233 · HTML · clone · pushed 2025-11-04</sub>
  <sub>`git clone https://github.com/tsinghua-fib-lab/AgentSquare.git`</sub>
- **[GNAP](https://github.com/farol-team/gnap)** — Git-native protocol draft for agent coordination
  <sub>★ 87 · MIT · source · pushed 2026-03-17</sub>
  <sub>`git clone https://github.com/farol-team/gnap.git`</sub>
- **[agent-opt](https://github.com/future-agi/agent-opt)** — Optimizes prompts and agent workflows
  <sub>★ 75 · Python · Apache-2.0 · pip · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-opt`</sub>
- **[AVP](https://github.com/VectorArc/avp-python)** — Transfers KV-cache between agents, not text
  <sub>★ 29 · Python · Apache-2.0 · pip · pushed 2026-04-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install avp[hf]`</sub>


---

Snapshot 2026-10-15. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
