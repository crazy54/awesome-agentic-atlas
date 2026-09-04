# Harness Engineering

How agent harnesses are built — primitives, papers and reference implementations.

Curated by **[ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

426 entries · 230 distinct repos · 21 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/shareAI-lab/learn-claude-code"><img src="https://opengraph.githubassets.com/1/shareAI-lab/learn-claude-code" width="260"></a> | <a href="https://github.com/anthropics/claude-cookbooks"><img src="https://opengraph.githubassets.com/1/anthropics/claude-cookbooks" width="260"></a> | <a href="https://github.com/huggingface/smolagents"><img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/smolagents/smolagents.png" width="260"></a> |
| **[shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)**<br>★ 76k | **[anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)**<br>★ 52.4k | **[huggingface/smolagents](https://github.com/huggingface/smolagents)**<br>★ 29.1k |
| <a href="https://github.com/awslabs/agentcore-samples"><img src="https://opengraph.githubassets.com/1/awslabs/agentcore-samples" width="260"></a> | <a href="https://github.com/wquguru/harness-books"><img src="https://opengraph.githubassets.com/1/wquguru/harness-books" width="260"></a> | <a href="https://github.com/lopopolo/harness-engineering"><img src="https://opengraph.githubassets.com/1/lopopolo/harness-engineering" width="260"></a> |
| **[awslabs/agentcore-samples](https://github.com/awslabs/agentcore-samples)**<br>★ 3.3k | **[Harness Books](https://github.com/wquguru/harness-books)**<br>★ 2.9k | **[lopopolo/harness-engineering](https://github.com/lopopolo/harness-engineering)**<br>★ 2.7k |

## Contents

- [Tutorials &amp; Educational](#tutorials--educational) (15)
- [Foundations](#foundations) (27)
- [Agent Loop](#agent-loop) (19)
- [Planning &amp; Task Decomposition](#planning--task-decomposition) (10)
- [Context Delivery &amp; Compaction](#context-delivery--compaction) (26)
- [Memory &amp; State](#memory--state) (24)
- [Skills &amp; MCP](#skills--mcp) (41)
- [Tool Design](#tool-design) (14)
- [Security, Sandbox &amp; Permissions](#security-sandbox--permissions) (40)
- [Permissions &amp; Authorization](#permissions--authorization) (12)
- [Task Runners &amp; Orchestration](#task-runners--orchestration) (36)
- [Human-in-the-Loop](#human-in-the-loop) (12)
- [Observability &amp; Tracing](#observability--tracing) (16)
- [Verification &amp; CI Integration](#verification--ci-integration) (10)
- [Evals &amp; Verification](#evals--verification) (15)
- [Debugging &amp; Developer Experience](#debugging--developer-experience) (15)
- [Generators &amp; Meta-Harnesses](#generators--meta-harnesses) (22)
- [Demo Harnesses](#demo-harnesses) (37)
- [Related Awesome Lists](#related-awesome-lists) (7)
- [Production Infrastructure &amp; Operations](#production-infrastructure--operations) (21)
- [Adjacent Collections](#adjacent-collections) (7)

## Tutorials &amp; Educational

- **[shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)** — Step-by-step deconstruction of Claude Code as an agent harness (s01–s12). Best resource for understanding how agent loop, tool use, skills, context compaction, and task management compose in practice
  <sub>★ 76k · Python · MIT · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g @shareai-lab/kode`</sub>
- **[anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)** — Anthropic's official notebook collection covering orchestrator-worker patterns, parallel tool calling, programmatic tool calling (PTC), context compaction, and Agent SDK examples. The patterns/agents/ directory is the reference implementation of every orchestration pattern described in *Building Effective Agents
  <sub>★ 52.4k · Jupyter Notebook · MIT · source · pushed 2026-09-02</sub>
  <sub>`git clone https://github.com/anthropics/claude-cookbooks.git`</sub>
- **[huggingface/smolagents](https://github.com/huggingface/smolagents)** — HuggingFace's deliberately minimal agent library (~1,000 lines of core code): the entire harness — tool validation, memory, monitoring, sandbox isolation (E2B, Docker, Pyodide) — is readable in an afternoon. The code-agent pattern (model writes Python that calls tools, eliminating JSON round-trips) is a concrete alternative loop design worth understanding
  <sub>★ 29.1k · Python · Apache-2.0 · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "smolagents[toolkit]"`</sub>
- **[awslabs/agentcore-samples](https://github.com/awslabs/agentcore-samples)** — AWS's official sample repo is one of the most complete public walkthroughs of what "productionizing" an agent platform actually means: runtime, gateway, memory, identity, observability, IaC, and blueprint apps all live in one place. Worth including because it covers the harness infrastructure layer most sample repos skip and does so across multiple frameworks rather than baking in a single orchest
  <sub>★ 3.3k · Python · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @aws/agentcore`</sub>
- **[Harness Books](https://github.com/wquguru/harness-books)** — Two open-source books that use Claude Code and Codex as observation targets to explain how constraint structures organize execution in real engineering environments. The clearest book-length treatment of why prompts, tools, permissions, recovery paths, and team rules form a single control plane rather than accessories around the model
  <sub>★ 2.9k · Python · source · pushed 2026-04-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wquguru/harness-books.git`</sub>
- **[agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices)** — Provider-neutral Agent Skill for designing, auditing, and refactoring agentic harnesses across domains. Distills the full runtime discipline — loop budgets, typed tools, permission gates, compaction-aware memory, prompt-caching layout, and launch checklists — into an interactive reference that works for Codex, Claude Code, and any agent needing rigorous scaffolding
  <sub>★ 2.3k · MIT · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add DenisSergeevitch/agents-best-practices -g`</sub>
- **[rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent)** — Pure-Python coding agent harness (standard library only) that implements the six core harness components—live repo context, structured tools with permissions, context reduction, transcript resumption, and bounded subagents—in a single readable file. The clearest starting point for understanding how a coding agent loop actually works under the hood
  <sub>★ 1.1k · Python · Apache-2.0 · clone · pushed 2026-04-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rasbt/mini-coding-agent.git`</sub>
- **[AutoJunjie/awesome-agent-harness](https://github.com/AutoJunjie/awesome-agent-harness)** — Curated list organized into Full Lifecycle Platforms, Task Runners, Agent Runtimes, Coding Agents. Close to this list's scope; good complementary reference
  <sub>★ 515 · source · pushed 2026-04-19</sub>
  <sub>`git clone https://github.com/AutoJunjie/awesome-agent-harness.git`</sub>
- **[mastra-ai/workshop-mastracode](https://github.com/mastra-ai/workshop-mastracode)** — February 2026 workshop by Mastra's founders dissecting every layer of an open-source AI coding agent: stateful/resumable harness, dynamic prompt composition, workspace sandboxing, memory compaction, HITL steering, event protocols, and cost tracking. The 11-topic curriculum is the most complete public walkthrough of production coding-agent harness internals
  <sub>★ 21 · HTML · npm · pushed 2026-02-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g mastracode`</sub>
- **[ML6 x AISO Agent Workshop](https://github.com/ml6team/AISO-workshop)** — February 2026 hands-on workshop building an AI agent from scratch with Google's Agent Development Kit (ADK) in 3 hours. Five milestones with a built-in benchmark that tracks progress from ~19% (base agent) to ~81% (with web search, PDF reader, and calculator tools). The clearest public tutorial for understanding how tool access directly translates to capability gains
  <sub>★ 5 · Python · clone · pushed 2026-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/<your-username>/AISO-workshop`</sub>
- **[Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/)** — A project-based course on designing the environments, state, verification, and control systems that make Codex and Claude Code reliable. The most approachable public curriculum for learning harness engineering from first principles — each module builds a working artifact rather than summarizing concepts
  <sub>website</sub>
  <sub>`https://walkinglabs.github.io/learn-harness-engineering/en/`</sub>
- **[Building Governed AI Agents](https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook)** — OpenAI's February 2026 cookbook building a complete multi-agent governance system from scratch: policy-as-code guardrails, OpenAI Traces for full observability, eval-driven design, and a distributable governance package. The most concrete first-party tutorial for making governance part of core infrastructure from day one
  <sub>website</sub>
  <sub>`https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook`</sub>
- **[Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)** — Practitioners' guide covering all harness configuration points for coding agents: system prompts, MCP tool selection, skills for progressive disclosure, sub-agents as context firewalls, hooks for deterministic control, and back-pressure verification. The central argument — that most agent failures are configuration problems, not model limitations — and the heuristic to minimize tool exposure (too
  <sub>website</sub>
  <sub>`https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents`</sub>
- **[How to orchestrate agents using mission control](https://github.blog/ai-and-ml/github-copilot/how-to-orchestrate-agents-using-mission-control/)** — GitHub's December 2025 practical guide on coordinating multiple coding agents with mission control: parallel vs. sequential execution, when to intervene, and how to review agent work productively. Shows the shift from single-agent prompts to multi-agent choreography and the harness decisions required to keep parallel agents from interfering with each other
  <sub>website</sub>
  <sub>`https://github.blog/ai-and-ml/github-copilot/how-to-orchestrate-agents-using-mission-control/`</sub>
- **[Engineering Trustworthy Multi-Agent Systems](https://www.ieeesmc.org/cai-2026/tutorial-3-engineering-trustworthy-multi-agent-systems/)** — IEEE CAI 2026 tutorial (December 2025) providing a research-based practical guide for designing enterprise-ready multi-agent systems. Covers agentic patterns (ReACT, Reflection, CoT), emerging protocols (MCP, A2A), multi-layer memory structures, observability and online/offline evaluation techniques, and trustworthy AI guardrails. The most comprehensive conference tutorial on production multi-agen
  <sub>website</sub>
  <sub>`https://www.ieeesmc.org/cai-2026/tutorial-3-engineering-trustworthy-multi-agent-systems/`</sub>

## Foundations

- **[lopopolo/harness-engineering](https://github.com/lopopolo/harness-engineering)** — Ryan Lopopolo's anthology, field guide, and agent context bundle for harness engineering: it reframes the harness as the environment that carries an organization's nonfunctional requirements, with reusable AGENTS.md/CLAUDE.md artifacts, playbooks, evals, and domain modeling docs. The most systematic open-source synthesis of how to make organizational judgment cumulative across agent-maintained rep
  <sub>★ 2.7k · Python · CC-BY-4.0 · source · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lopopolo/harness-engineering.git`</sub>
- **[RUCAIBox/awesome-agent-harness](https://github.com/RUCAIBox/awesome-agent-harness)** — RUCAIBox's survey paper and curated reading list on *Agent Systems with Harness Engineering*, mapping harness design across agent workflows, memory systems, skill libraries, and multi-agent orchestration with 500+ references. The clearest academic complement to vendor-specific harness engineering posts
  <sub>★ 186 · MIT · source · pushed 2026-05-25 · Win?</sub>
  <sub>`git clone https://github.com/RUCAIBox/awesome-agent-harness.git`</sub>
- **[Harness Engineering](https://openai.com/index/harness-engineering/)** — OpenAI's framing of harness engineering as a discipline: how to design the scaffolding that lets Codex and similar agents operate reliably in an agent-first world
  <sub>website</sub>
  <sub>`https://openai.com/index/harness-engineering/`</sub>
- **[Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/)** — OpenAI's detailed breakdown of the Codex agent loop, exposing each harness component and where it can be improved
  <sub>website</sub>
  <sub>`https://openai.com/index/unrolling-the-codex-agent-loop/`</sub>
- **[Run Long-Horizon Tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/)** — OpenAI's practice guide for long-horizon task planning: introduces Plan.md, Implement.md, Documentation.md as reusable harness artifacts
  <sub>website</sub>
  <sub>`https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/`</sub>
- **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)** — Anthropic's foundational guide on agent architecture, covering when to use workflows vs. agents and how to compose primitives
  <sub>website</sub>
  <sub>`https://www.anthropic.com/research/building-effective-agents`</sub>
- **[Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)** — Anthropic's engineering blog on designing harnesses for sustained, multi-session development tasks. Key insight: every harness component assumes the model can't do something; those assumptions expire
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/harness-design-long-running-apps`</sub>
- **[Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-effective-tools-for-agents)** — Anthropic's guide on tool interface design: naming, schemas, error surfaces, and the principle that tool design is agent UX
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/writing-effective-tools-for-agents`</sub>
- **[Beyond Permission Prompts](https://www.anthropic.com/engineering/beyond-permission-prompts)** — Anthropic on building structured permission and authorization systems into agent harnesses instead of relying on natural-language permission text
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/beyond-permission-prompts`</sub>
- **[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)** — Anthropic's framework for evaluating agent behavior: what to measure, how to build eval harnesses, and why unit-test-style evals fail for agents
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`</sub>
- **[What is an AI Agent?](https://www.ibm.com/think/topics/ai-agents)** — IBM's definitional piece, useful for anchoring harness design decisions to a clear model of what an agent actually is
  <sub>website</sub>
  <sub>`https://www.ibm.com/think/topics/ai-agents`</sub>
- **[Agent Development Kit: Making it easy to build multi-agent applications](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)** — Google's announcement and design rationale for ADK: explains the multi-agent topology, tool registration model, and eval pipeline that shaped their framework. Complements the Anthropic/OpenAI framing with Google's production perspective
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/`</sub>
- **[Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)** — Martin Fowler's synthesis of what harness engineering practice looks like: three interlocking systems — context engineering (curating what the agent knows), architectural constraints (deterministic linters and structural tests), and entropy management (periodic agents that repair documentation drift). The "humans on the loop" framing — harness engineers who design and maintain agent environments r
  <sub>website</sub>
  <sub>`https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html`</sub>
- **[The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)** — LangChain's structural breakdown of the five primitives that compose a harness: filesystem (durable state + agent collaboration surface), code execution (autonomous problem-solving without pre-designed solutions), sandbox (isolation + verification), memory (cross-session persistence), and context management (compaction against "context rot"). The co-evolution warning — models trained with specific
  <sub>website</sub>
  <sub>`https://blog.langchain.com/the-anatomy-of-an-agent-harness/`</sub>
- **[Natural-Language Agent Harnesses](https://arxiv.org/abs/2603.25723)** — Proposes externalizing agent control logic as portable natural-language artifacts (NLAHs) executed by a shared Intelligent Harness Runtime, enabling harness design to be studied, transferred, and reproduced rather than buried in bespoke controller code. Directly addresses the root cause of harness fragility: control logic scattered across framework defaults and hard-coded controller logic that can
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.25723`</sub>
- **[Ranking Engineer Agent (REA): Meta's Autonomous AI System for Ads Ranking](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/)** — Meta's production harness for multi-day ML pipeline automation with hibernate-and-wake checkpointing for resuming interrupted 6-hour tasks without losing context. Demonstrates harness design for scientific workflows where individual turns can exceed model context limits but the overall pipeline must maintain coherence across days
  <sub>website</sub>
  <sub>`https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/`</sub>
- **[Supercharge Your AI Agents: The New ADK Integrations Ecosystem](https://developers.googleblog.com/en/supercharge-your-ai-agents-adk-integrations-ecosystem/)** — Google's 2026 update to Agent Development Kit expanding the ecosystem integrations (Hugging Face, GitHub, Daytona, Notion, etc.) and providing reference patterns for how orchestration harnesses wire external services without losing determinism or state coherence
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/en/supercharge-your-ai-agents-adk-integrations-ecosystem/`</sub>
- **[2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf?hsLang=en)** — Anthropic's industry benchmark identifying infrastructure configuration as a first-class optimization variable: harness setup alone can swing benchmarks by 5+ percentage points. Documents the shift from single-agent to orchestrated multi-agent teams and introduces the "agentic engineering platform" category, bridging the gap between agent frameworks and production deployment infrastructure
  <sub>website</sub>
  <sub>`https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf?hsLang=en`</sub>
- **[How We Build Azure SRE Agent with Agentic Workflows](https://techcommunity.microsoft.com/blog/appsonazureblog/how-we-build-azure-sre-agent-with-agentic-workflows/4508753)** — Architecture walkthrough of Microsoft's agent that has handled 35,000+ production incidents autonomously, reducing Azure App Service time-to-mitigation from 40.5 hours to 3 minutes. Documents the integration of MCP tools, telemetry, code repositories, and incident management platforms into a single agent harness with human-in-the-loop governance. The most data-backed production harness case study
  <sub>website</sub>
  <sub>`https://techcommunity.microsoft.com/blog/appsonazureblog/how-we-build-azure-sre-agent-with-agentic-workflows/4508753`</sub>
- **[Harness Engineering: Structured Workflows for AI-Assisted Development](https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development)** — Red Hat's enterprise perspective on harness engineering (April 7, 2026): AI writes better code when you design the environment it works in. Emphasizes structured context over free-form tickets, expanding the agent's toolbox through MCP integrations (CI status, deployment logs, runtime metrics) as real data sources, and a four-pillar model (vibes, specs, skills, agents) for organizing how humans an
  <sub>website</sub>
  <sub>`https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development`</sub>
- **[Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)** — Birgitta Böckeler's systematic mental model (April 2026) for coding-agent harnesses, framing them as feedforward guides plus feedback sensors that self-correct before output reaches human eyes. Distinguishes computational controls (linters, tests) from inferential ones (LLM-as-judge), and argues that harnessability should become a first-class criterion in technology and architecture decisions
  <sub>website</sub>
  <sub>`https://martinfowler.com/articles/harness-engineering.html`</sub>
- **[A Practical Guide to Building AI Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)** — OpenAI's April 2026 comprehensive guide distilling production deployment patterns into actionable best practices: single-agent vs. multi-agent orchestration (manager vs. decentralized handoffs), tool design for many-to-many agent-tool relationships, and layered guardrail patterns combining input validation, output filtering, tool-risk ratings, and human-intervention triggers
  <sub>website</sub>
  <sub>`https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/`</sub>
- **[An Update on Recent Claude Code Quality Reports](https://www.anthropic.com/engineering/april-23-postmortem)** — Anthropic's transparent April 2026 postmortem tracing Claude Code quality degradation to three independent harness-level changes: a default reasoning-effort downgrade, a caching-optimization bug that continuously dropped thinking history from stale sessions, and an overly aggressive verbosity-limiting system prompt. Essential reading for understanding how seemingly minor harness adjustments — prom
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/april-23-postmortem`</sub>
- **[Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence](https://claude.com/blog/harnessing-claudes-intelligence)** — Anthropic's April 2026 design guide distilling harness engineering into three actionable patterns: build on tools Claude already knows, remove harness assumptions as capabilities improve, and set UX/cost/safety boundaries carefully. A practical complement to the "agent = model + harness" framing that helps teams decide what scaffolding to keep, add, or remove over time
  <sub>website</sub>
  <sub>`https://claude.com/blog/harnessing-claudes-intelligence`</sub>
- **[Code as Agent Harness](https://arxiv.org/abs/2605.18747)** — May 2026 survey framing code as the basis for agent infrastructure rather than merely output: it unifies harness interface, mechanisms, and multi-agent scaling through shared code artifacts, and surfaces open challenges from verification under incomplete feedback to regression-free improvement
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2605.18747`</sub>
- **[Architectural Design Decisions in AI Agent Harnesses](https://arxiv.org/abs/2604.18071)** — April 2026 empirical study of 70 public agent systems across five recurring dimensions (subagent architecture, context management, tool systems, safety mechanisms, orchestration) that synthesizes five architectural patterns. The comparative research package turns harness selection from a framework popularity contest into a reasoned comparison of design trade-offs
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.18071`</sub>
- **[Tuning the harness, not the model: a Nemotron 3 Ultra playbook](https://blog.langchain.com/tuning-the-harness-not-the-model-a-nemotron-3-ultra-playbook)** — LangChain's July 2026 playbook showing how harness-only tuning brought Nemotron 3 Ultra within one point of Opus 4.8 on Deep Agents at roughly one-tenth the cost ($4.48 vs $43.48). The clearest recent demonstration that evals are the training data for harness work and that fit — not raw model capability — determines how much quality reaches the task
  <sub>website</sub>
  <sub>`https://blog.langchain.com/tuning-the-harness-not-the-model-a-nemotron-3-ultra-playbook`</sub>

## Agent Loop

- **[Loop Engineering](https://github.com/cobusgreyling/loop-engineering)** — Practical design system for agent loops with seven production patterns, cross-tool starter kits, and CLI tools that score readiness, scaffold state, estimate cost, detect drift, and isolate worktrees. The clearest open-source resource for moving from one-off prompting to durable, observable agent loops
  <sub>★ 10.8k · TypeScript · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @cobusgreyling/loop init . --pattern daily-triage --tool claude`</sub>
- **[deepclaude](https://github.com/aattaran/deepclaude)** — Ports Claude Code's full agent loop to DeepSeek V4 Pro and other Anthropic-compatible backends while preserving the same UX. The strongest practical evidence that loop architecture — not model identity — determines agent behavior, and a concrete starting point for building backend-agnostic harnesses
  <sub>★ 2.3k · JavaScript · MIT · source · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aattaran/deepclaude.git`</sub>
- **[statewright](https://github.com/statewright/statewright)** — State machine guardrails that constrain which tools an agent can call in each phase of a workflow, turning open-ended loops into deterministic state transitions. The research result is striking: local models went from 2/10 to 10/10 passing on a SWE-bench subset purely by shrinking the tool space, proving that loop structure — not model size — is the binding constraint
  <sub>★ 490 · Rust · npx · pushed 2026-08-22 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx statewright-codex@latest init`</sub>
- **[Life-Harness](https://github.com/Tianshi-Xu/Life-Harness)** — Official implementation of a lifecycle-aware runtime harness that improves frozen LLM agents by adapting the model-environment interface across four layers: environment contract, procedural skills, action realization, and trajectory regulation. The key result is that harness-side adaptation transfers across 18 model backbones, proving that many agent failures are interface mismatches rather than r
  <sub>★ 217 · Python · MIT · source · pushed 2026-07-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Tianshi-Xu/Life-Harness.git`</sub>
- **[AgentSPEX](https://github.com/ScaleML/AgentSPEX)** — UIUC's open-source specification and execution language for LLM-agent workflows: declarative YAML with typed steps, branching, loops, and explicit state management, backed by a Docker sandbox with 50+ MCP tools, checkpointing, and trajectory logging. A concrete reference for turning ad-hoc agent loops into version-controlled, reproducible harness artifacts
  <sub>★ 95 · Python · Apache-2.0 · source · pushed 2026-07-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ScaleML/AgentSPEX.git`</sub>
- **[Confucius Code Agent (CCA)](https://github.com/facebookresearch/cca-swebench)** — February 2026 production-grade coding agent from Meta/Harvard built on the Confucius SDK, which structures harness design around three perspectives: Agent Experience (AX), User Experience (UX), and Developer Experience (DX). Features a unified orchestrator with advanced context management, persistent note-taking for cross-session learning, and a meta-agent that automates build-test-improve cycles.
  <sub>★ 41 · Python · MIT · source · pushed 2026-05-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/facebookresearch/cca-swebench.git`</sub>
- **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** — The foundational paper defining the Thought/Action/Observation loop structure that underlies virtually every agent harness. Required reading for understanding why the loop is structured the way it is and where each harness component maps onto the reasoning-acting cycle
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2210.03629`</sub>
- **[LangGraph — Low Level Concepts](https://langchain-ai.github.io/langgraph/concepts/low_level/)** — Models the agent loop explicitly as a directed graph with typed state, conditional edges, and checkpointing. The most concrete engineering treatment of loop control flow: how to implement termination conditions, branch on tool results, and persist mid-loop state for resumption
  <sub>website</sub>
  <sub>`https://langchain-ai.github.io/langgraph/concepts/low_level/`</sub>
- **[Unlocking the Codex Harness: How We Built the App Server](https://openai.com/index/unlocking-the-codex-harness/)** — OpenAI's engineering deep-dive into the Item/Turn/Thread protocol (JSON-RPC/JSONL over stdio) that exposes the Codex harness to every client surface. The most direct first-party account of why approval flows, streaming diffs, and thread persistence demand a purpose-built protocol — and why MCP's tool-oriented model proved insufficient for these requirements
  <sub>website</sub>
  <sub>`https://openai.com/index/unlocking-the-codex-harness/`</sub>
- **[Hooks – Codex](https://developers.openai.com/codex/hooks)** — OpenAI's lifecycle-hook framework for Codex: inject deterministic scripts at SessionStart, PreToolUse, PostToolUse, and other loop events to enforce guardrails, audit actions, and customize agent behavior without relying on prompt-level trust. A concrete reference for programmable harness governance
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/hooks`</sub>
- **[Extended Thinking — Claude API Docs](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)** — The harness-critical reference for integrating extended thinking into agent loops: budget_tokens controls reasoning depth per turn, thinking blocks must be preserved when passing tool results back (omitting them silently breaks multi-step reasoning), and thinking mode cannot change mid-turn. Essential before wiring extended thinking into any tool-use loop
  <sub>website</sub>
  <sub>`https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking`</sub>
- **[Getting started with loops](https://claude.com/blog/getting-started-with-loops)** — Anthropic's June 2026 practical taxonomy of agent loops: turn-based, goal-based (/goal), time-based (/loop, /schedule), and proactive loops. The framework for matching loop primitive to task shape — and the emphasis on deterministic stop conditions and token budgets — makes it a concise reference for choosing the right loop abstraction instead of defaulting to a single conversational turn cycle
  <sub>website</sub>
  <sub>`https://claude.com/blog/getting-started-with-loops`</sub>
- **[Improving Deep Agents with Harness Engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)** — LangChain's case study showing harness-only changes moved their coding agent from rank 30 to top 5 on Terminal Bench 2.0 with no model swap: structured verification loops, context injection (directory maps + time budget warnings), loop-detection middleware, and a "reasoning sandwich" concentrating maximum thinking at planning and verification phases. The most concrete published demonstration that
  <sub>website</sub>
  <sub>`https://blog.langchain.com/improving-deep-agents-with-harness-engineering/`</sub>
- **[How Middleware Lets You Customize Your Agent Harness](https://blog.langchain.com/how-middleware-lets-you-customize-your-agent-harness/)** — Introduces AgentMiddleware: six composable hooks (before_agent, before_model, wrap_model_call, wrap_tool_call, after_model, after_agent) that intercept every stage of the agent loop. Enables deterministic policy enforcement (PII redaction that can't be trusted to prompts), dynamic tool injection, mid-task model swapping, and production patterns (retry, fallback, HITL interrupts) without modifying
  <sub>website</sub>
  <sub>`https://blog.langchain.com/how-middleware-lets-you-customize-your-agent-harness/`</sub>
- **[Agents Learn Their Runtime: Interpreter Persistence as Training-Time Semantics](https://arxiv.org/abs/2603.01209)** — Controlled experiment isolating interpreter state persistence as an independent training variable. The harness finding: mismatching your runtime persistence mode to the model's training-time semantics produces either 80% missing-variable errors (model expects state that doesn't persist) or 3.5× token overhead (model redundantly recomputes state it expects to already have). Persistence is a learned
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.01209`</sub>
- **[A Scheduler-Theoretic Framework for LLM Agent Execution](https://arxiv.org/abs/2604.11378)** — April 2026 systematic analysis of 70 open-source LLM agent projects showing 60% adopt the Agent Loop pattern. Proposes a formal scheduler framework that maps execution patterns (Agent Loop, Event-driven, State-machine, Graph/flow, Hybrid) onto a unified control model, making the controllability/expressiveness/implementability trade-offs explicit. Essential reading for choosing the right loop archi
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.11378`</sub>
- **[The Design Space of Today's and Future AI Agent Systems](https://arxiv.org/abs/2604.14228)** — April 2026 reverse-engineering of Claude Code's architecture revealing five-stage progressive compaction (budget reduction → snip → microcompact → context collapse → auto-compact), subagent isolation with rebuilt permission contexts, and a 27-event-type hook pipeline. The most detailed public analysis of a production agent loop's internal design decisions — essential for understanding how context
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.14228`</sub>
- **[The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)** — VS Code team's breakdown of the coding harness behind GitHub Copilot: three core loop responsibilities (context assembly, tool exposure, tool execution), multi-provider model routing across Anthropic, Google, OpenAI, xAI, and Mistral, and the VSC-Bench eval suite with PR-gated assessment. The clearest published account of how a major product treats harness changes as first-class code review criter
  <sub>website</sub>
  <sub>`https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode`</sub>
- **[Introducing dynamic workflows in Claude Code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)** — Anthropic's May 2026 introduction to dynamic parallel subagent orchestration: Claude generates JavaScript orchestration scripts that fan out work to tens or hundreds of parallel subagents with adversarial verification, converging on answers for tasks like the 750k-line Bun Zig-to-Rust port. The key harness insight is that the plan lives in executable code rather than the model's context window, sc
  <sub>website</sub>
  <sub>`https://claude.com/blog/introducing-dynamic-workflows-in-claude-code`</sub>

## Planning &amp; Task Decomposition

- **[microsoft/TaskWeaver](https://github.com/microsoft/TaskWeaver)** — Code-first task decomposition framework with a planner/executor split and a plugin system for injecting domain knowledge into the planning layer. The most complete reference implementation of plan-then-execute with stateful task tracking
  <sub>★ 6.2k · Python · MIT · pip · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/microsoft/TaskWeaver@<TAG>`</sub>
- **[Plan-and-Execute Agents](https://blog.langchain.com/plan-and-execute-agents/)** — The canonical engineering write-up separating planning from execution as distinct harness layers: a planner LLM generates the step list once; an executor agent works through it, replanning only when needed. Defines the pattern that most modern task-decomposition harnesses follow
  <sub>website</sub>
  <sub>`https://blog.langchain.com/plan-and-execute-agents/`</sub>
- **[LATS: Language Agent Tree Search](https://arxiv.org/abs/2310.04406)** — Unifies reasoning, acting, and planning via Monte Carlo Tree Search over agent trajectories. Directly informs harness design: external tool feedback as tree-search signals, trajectory backtracking on failure, and depth-bounded exploration make this the most actionable planning research for harnesses with real environment interaction
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2310.04406`</sub>
- **[Agyn: A Multi-Agent System for Team-Based Autonomous Software Engineering](https://arxiv.org/abs/2602.01465)** — Demonstrates specialized harness patterns for coordinating heterogeneous agent teams (planner, coder, reviewer, executor) on software engineering tasks. Shows how role-specific agents with different model sizes and tool access produce better outcomes than single-agent approaches, with concrete metrics on task decomposition effectiveness
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.01465`</sub>
- **[Plan-and-Act: Improving Planning of Agents for Long-Horizon Tasks](https://arxiv.org/abs/2503.09572)** — Modular framework separating high-level planning from low-level execution through synthetic data generation and explicit structured planning. Achieves 57.58% success on WebArena-Lite and 81.36% on WebVoyager. The key harness insight is that planner and executor can be specialized independently — different model sizes, tool access, and reasoning budgets for each layer — improving overall reliabilit
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2503.09572`</sub>
- **[Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)** — Decision framework for four multi-agent patterns (subagents, skills, handoffs, router) with concrete performance data: subagents process 67% fewer tokens than skills in multi-domain scenarios because context isolation prevents cross-domain bloat. The five-dimension matching table (distributed development, parallelization, multi-hop, user interaction, latency) is the most actionable published guide
  <sub>website</sub>
  <sub>`https://blog.langchain.com/choosing-the-right-multi-agent-architecture/`</sub>
- **[Multi-Agent Workflows Often Fail. Here's How to Engineer Ones That Don't](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/)** — GitHub's February 24, 2026 distillation of a failure pattern most harnesses eventually rediscover: multi-agent systems behave like distributed systems, so every handoff needs typed schemas, constrained action schemas, and explicit boundary validation. Worth including because it turns "add more agents" from a vibe into an interface design problem you can actually reason about
  <sub>website</sub>
  <sub>`https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/`</sub>
- **[Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)** — Anthropic's pattern for maintaining agent progress across multiple context windows: an initializer agent sets up the environment once and hands off to a coding agent that makes incremental progress each session. The structured handoff mechanism — feature lists, git commits, and test gates as cross-session state — is the reference design for any harness where a task exceeds a single context window
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents`</sub>
- **[Task-Adaptive Multi-Agent Orchestration (AdaptOrch)](https://arxiv.org/abs/2602.16873)** — February 2026 framework that dynamically selects orchestration topology (parallel, sequential, hierarchical, or hybrid) based on task dependency graphs rather than fixed pipeline architecture. Demonstrates that topology choice is a harness-level lever that can improve performance 12–23% over model selection alone
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.16873`</sub>
- **[Task-Decoupled Planning for Long-Horizon Agents (TDP)](https://arxiv.org/abs/2601.07577)** — January 2026 planning framework that combines task decomposition with modular agent design: a Supervisor decomposes tasks into a dependency graph, Planner &amp; Executor agents solve each decoupled sub-task node independently, and a Self-Revision module updates the graph after execution. The key harness insight is that decoupling planning from execution at the sub-task level enables localized replanni
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2601.07577`</sub>

## Context Delivery &amp; Compaction

- **[headroom](https://github.com/headroomlabs-ai/headroom)** — Compresses tool outputs, logs, files, and RAG chunks before they enter the context window, cutting active tokens by 60–95% without changing answers. Ships as a library, proxy, and MCP server — the right drop-in layer for any harness where bulky tool returns are the primary context pressure source
  <sub>★ 68.8k · Python · Apache-2.0 · uv · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`uv tool install --python 3.13 "headroom-ai[all]" # CLI in a self-contained env`</sub>
- **[Context7](https://github.com/upstash/context7)** — MCP server and CLI that injects up-to-date, version-specific library documentation directly into agent context, eliminating hallucinated APIs and outdated code examples caused by stale training data. Ships as both a ctx7 command-line tool and an MCP server with resolve-library-id and query-docs tools
  <sub>★ 61.6k · TypeScript · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/upstash/context7.git`</sub>
- **[codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)** — High-performance code intelligence MCP server that full-indexes repositories into a persistent knowledge graph via tree-sitter AST analysis across 66 languages. Replaces dozens of file-read/grep cycles with sub-millisecond structured queries, cutting active tokens by 120× and turning codebase navigation from a context-pressure problem into a pointer-chasing problem
  <sub>★ 42k · C · MIT · psh · pushed 2026-09-03 · macOS</sub>
  <sub>`irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/scripts/setup-windows.ps1 | iex`</sub>
- **[OpenViking](https://github.com/volcengine/OpenViking)** — ByteDance's context database for AI agents that unifies memory, resources, and skills through a filesystem paradigm, enabling hierarchical context delivery where agents pull only the paths they need instead of receiving bloated monolithic prompts. The self-evolving layer that restructures context based on usage patterns makes it a rare example of context infrastructure that improves autonomously r
  <sub>★ 35.3k · Python · AGPL-3.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openviking --upgrade`</sub>
- **[DESIGN.md](https://github.com/google-labs-code/design.md)** — Google Labs' specification for describing visual identity systems to coding agents: machine-readable design tokens (YAML front matter) combined with human-readable design rationale (markdown prose) give agents a persistent, structured understanding of design constraints without requiring custom tool chains
  <sub>★ 27.7k · TypeScript · Apache-2.0 · npx · pushed 2026-07-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx @google/design.md lint DESIGN.md`</sub>
- **[context-mode](https://github.com/mksglu/context-mode)** — MCP server that intercepts raw tool output before it enters the context window, sandboxing bulky data (Playwright snapshots, GitHub issues, logs) outside the LLM and retrieving only relevant fragments via BM25 when needed. The "think in code" paradigm — replacing ten file-read tool calls with one script execution — is a concrete harness pattern for turning context pressure into a programming probl
  <sub>★ 20.3k · TypeScript · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g context-mode`</sub>
- **[OpenWiki](https://github.com/langchain-ai/openwiki)** — LangChain's CLI that writes and maintains agent-readable wikis for codebases or purpose memory, turning documentation drift into a versioned, automatable harness artifact. Emits Google Open Knowledge Format bundles so curated context stays portable across agents and can be kept fresh via CI
  <sub>★ 16.1k · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g openwiki`</sub>
- **[Trellis](https://github.com/mindfold-ai/Trellis)** — Replaces the bloated CLAUDE.md pattern with a progressive spec system: agents load only the standards, task PRDs, and session journals relevant to the current step. The cross-platform adapter layer turns vendor-specific harness configuration into a portable team practice rather than a per-tool hack
  <sub>★ 14.4k · TypeScript · AGPL-3.0 · npm · pushed 2026-08-27 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @mindfoldhq/trellis@latest`</sub>
- **[LLMLingua](https://github.com/microsoft/LLMLingua)** — Microsoft Research's prompt compression toolkit (up to 20x compression, minimal performance loss) that can be embedded as a preprocessing step in the context delivery layer. LLMLingua-2 adds 3–6x speed gains, making it viable for latency-sensitive agent loops
  <sub>★ 6.6k · Python · MIT · pip · pushed 2026-04-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llmlingua`</sub>
- **[MinishLab/semble](https://github.com/MinishLab/semble)** — Code search primitive that replaces grep+read cycles with natural-language retrieval, cutting active tokens by ~98% while keeping 99% of a transformer-based retriever's accuracy. Ships as an MCP server and CLI, runs on CPU with zero external dependencies — the right drop-in for any coding agent harness struggling with context pressure
  <sub>★ 6k · Python · MIT · uv · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install semble`</sub>
- **[Graft](https://github.com/trailhq/Graft)** — Builds a local, regenerable graph of plain-English system explanations and code relationships, then rides along inside Claude Code, Cursor, Codex, and Gemini via MCP and statusline hooks so the agent stops rediscovering the repo every session. The published SWE-bench Verified and efficiency benchmarks make it the clearest recent demonstration that context delivery for coding agents is a navigation
  <sub>★ 5.5k · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @nanonets/graft # install the CLI, once`</sub>
- **[Mirage](https://github.com/strukto-ai/mirage)** — Mounts S3, Slack, Gmail, GitHub, and Redis side-by-side as a single virtual filesystem so agents interact with every backend through familiar bash commands instead of learning N distinct APIs. The key harness insight: LLMs are already fluent in grep, cat, and cp — leveraging that vocabulary eliminates tool-schema bloat and makes cross-service pipelines compose as naturally as local shell scripts
  <sub>★ 3.6k · TypeScript · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @struktoai/mirage-cli`</sub>
- **[ktx](https://github.com/Kaelio/ktx)** — Self-improving executable context layer for data and analytics agents: it ingests warehouses, BI tools, and wikis to build a semantic layer with approved metrics, joinable columns, and resolved fan/chasm traps, then serves the result to Claude Code, Codex, and Cursor through MCP. Fills the gap where general-purpose agents invent metric logic on every question — it turns warehouse querying from a p
  <sub>★ 1.6k · TypeScript · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @kaelio/ktx`</sub>
- **[dirac](https://github.com/dirac-run/dirac)** — Coding agent harness optimized for surgical context curation and API cost reduction: Hash Anchored edits, massively parallel operations, and AST manipulation combine to cut costs 50–80% while improving code quality. Demonstrates that precise context delivery — not just bulk compression — is the right lever for efficient coding agents
  <sub>★ 1.5k · TypeScript · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g dirac-cli`</sub>
- **[harness-experimental](https://github.com/hoangnb24/repository-harness)** — Repository-level operating harness that turns any software repo into an agent-ready workspace: structured AGENTS.md, HARNESS.md, and FEATURE_INTAKE.md give agents the missing project context — where to start, what the product contract says, how risky the change is, and which decisions future agents should inherit. The most concrete open-source implementation of "coding agents need better repositor
  <sub>★ 1.2k · Rust · MIT · source · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hoangnb24/harness-experimental.git`</sub>
- **[Token Savior](https://github.com/Mibayy/token-savior)** — MCP server that indexes codebases by symbol (functions, classes, call graphs) so agents navigate by pointer instead of reading whole files, cutting active tokens by 77% and benchmark wall time by 76%. Demonstrates that context delivery for coding agents is a navigation problem, not just a compression problem
  <sub>★ 1.1k · Python · MIT · uv · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx token-savior-recall`</sub>
- **[PRO-LONG](https://github.com/alexisfox7/PRO-LONG)** — Programmatic memory framework for long-horizon agents: the harness appends all observations to a structured log and lets the agent search it with code instead of relying on fixed summarization or compaction policies. Achieves 4.2–5.8× token reduction and matches or exceeds specialized harnesses on ARC-AGI-3, showing that long-horizon context management can be a programmable retrieval problem rathe
  <sub>★ 420 · Python · MIT · clone · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/alexisfox7/PRO-LONG.git`</sub>
- **[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — Anthropic's systematic guide to managing the full context state—system prompts, tools, MCP, and message history—as a finite, curated resource. Reframes harness design as "what configuration of context produces the desired behavior?" rather than just prompt wording
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents`</sub>
- **[Compaction — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)** — Anthropic's reference for server-side context compaction: automatically summarizes older context when approaching the window limit. Reduced token consumption by 84% in a 100-turn web search eval while allowing agents to complete workflows that would otherwise hit context limits
  <sub>website</sub>
  <sub>`https://platform.claude.com/docs/en/build-with-claude/compaction`</sub>
- **[Prompt Caching — Claude API Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)** — The most effective harness-level cost lever: cache repeated system prompts, tool definitions, and long documents across requests. Explains where to place cache_control breakpoints for maximum reuse across multi-turn agent sessions
  <sub>website</sub>
  <sub>`https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching`</sub>
- **[Autonomous Context Compression](https://blog.langchain.com/autonomous-context-compression/)** — Shifts context compression from harness-controlled (compacting at a fixed token threshold) to agent-controlled: agents call a dedicated tool to trigger compression when strategically appropriate — between tasks or before consuming large inputs. Eliminates the failure mode where reactive-at-limit compaction interrupts agents mid-subtask and corrupts in-flight reasoning state
  <sub>website</sub>
  <sub>`https://blog.langchain.com/autonomous-context-compression/`</sub>
- **[Active Context Compression: Autonomous Memory Management in LLM Agents](https://arxiv.org/abs/2601.07190)** — Proposes a "Focus Agent" architecture where the agent autonomously decides when to consolidate interaction history into a persistent Knowledge block and prune raw context — shifting compression from a harness-enforced policy to a model-controlled action. Produces 22.7% token reduction with no accuracy loss on long-horizon tasks; the core contribution is making the compression unit semantically coh
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2601.07190`</sub>
- **[Making Agent-Friendly Pages with Content Negotiation](https://vercel.com/blog/making-agent-friendly-pages-with-content-negotiation)** — Vercel's February 3, 2026 implementation guide for serving text/markdown when agents request it via Accept: text/markdown, while preserving the same human-facing HTML URL. This is a real harness primitive, not just a docs trick: it removes boilerplate before it ever enters the context window and gives agents cleaner, cheaper inputs without custom scrapers
  <sub>website</sub>
  <sub>`https://vercel.com/blog/making-agent-friendly-pages-with-content-negotiation`</sub>
- **[ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context](https://arxiv.org/abs/2604.01599)** — LLM-curated hierarchical context management for agents where the model itself learns to weight information importance across multiple hierarchy levels. Reduces token overhead through learned relevance filtering without sacrificing comprehension. Directly applicable to any harness where context budget is the limiting factor — letting the model curate what belongs in active memory vs. what can be re
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.01599`</sub>
- **[Claude Code Compaction: How Context Compression Works](https://okhlopkov.com/claude-code-compaction-explained/)** — March 2026 deep-dive into Claude Code's automatic compaction mechanism: what survives (current task, recent errors, file names) vs. what gets lost (initial instructions, intermediate decisions, style rules). Key harness insight: never rely on compaction for critical rules — move them to CLAUDE.md where they live in the system prompt and survive any compression. Essential practical guidance for any
  <sub>website</sub>
  <sub>`https://okhlopkov.com/claude-code-compaction-explained/`</sub>
- **[Context Pruning for Coding Agents via Multi-Rubric Latent Reasoning](https://arxiv.org/abs/2605.15315)** — Decomposes code relevance into two interpretable dimensions — semantic evidence and dependency support — rather than collapsing all retention decisions into a single score. Saves up to 31% more tokens on multi-turn coding agent tasks while improving Exact Match by up to +3.5, demonstrating that coding-agent context pruning needs domain-specific rubrics rather than generic compression
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2605.15315`</sub>

## Memory &amp; State

- **[mem0](https://github.com/mem0ai/mem0)** — Drop-in universal memory layer (YC-backed, AWS Agent SDK's exclusive memory provider) that handles cross-session retention without custom harness-level state management code. Lowest integration cost for production-grade persistent memory
  <sub>★ 64.6k · Python · Apache-2.0 · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @mem0/cli # or: pip install mem0-cli`</sub>
- **[MemPalace](https://github.com/MemPalace/mempalace)** — Local-first AI memory system that stores conversation history verbatim and retrieves it with semantic search through a structured palace architecture (wings, rooms, drawers). Achieves 96.6% R@5 on LongMemEval with zero LLM calls, making it the best-benchmarked open-source memory layer for agents that need cross-session persistence without cloud dependencies
  <sub>★ 58.8k · Python · MIT · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add MemPalace/mempalace`</sub>
- **[cognee](https://github.com/topoteretes/cognee)** — Open-source memory platform with a hybrid graph-vector-relational poly-store that lets agents recall facts through both semantic similarity and structured graph traversal — the practical middle ground between flat vector stores and full multi-graph research systems. The self-improving pipeline reweights edges from agent feedback, and the 14-tool MCP server makes it a drop-in memory primitive for p
  <sub>★ 30.4k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "cognee[postgres]"`</sub>
- **[agentmemory](https://github.com/rohitg00/agentmemory)** — Persistent memory layer purpose-built for coding agents with 95.2% retrieval accuracy and 92% token reduction, backed by real-world benchmarks. Its cross-agent architecture — one memory server serving Claude Code, Cursor, Codex, and OpenCode through MCP and hooks — makes cross-session memory a portable harness primitive rather than a vendor-specific add-on
  <sub>★ 28k · TypeScript · Apache-2.0 · npm · pushed 2026-08-31 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @agentmemory/agentmemory@latest`</sub>
- **[TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory)** — Tencent's fully local agent memory system with a 4-tier progressive pipeline (Conversation → Atom → Scenario → Persona) and symbolic short-term memory via Mermaid canvases. The benchmark data is striking: 61% token reduction and 51% relative pass-rate improvement on long-horizon tasks, demonstrating that hierarchical memory architecture outperforms flat vector stores for coding agents
  <sub>★ 25.8k · TypeScript · clone · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Tencent/TencentDB-Agent-Memory.git`</sub>
- **[Letta (MemGPT)](https://github.com/letta-ai/letta)** — The reference architecture for stateful agents: three-tier memory (core / archival / recall) maps directly to harness state management design. Their agent loop redesign post is the most thorough public analysis of how memory structure shapes the harness
  <sub>★ 24.6k · Apache-2.0 · npm · pushed 2026-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @letta-ai/letta-code`</sub>
- **[Hindsight](https://github.com/vectorize-io/hindsight)** — Agent memory system organized around three explicit operations—retain, recall, and reflect—with semantic, keyword, graph, and temporal retrieval plus an MCP server. The June 2026 release and production usage make it a concrete reference for turning cross-session persistence from passive storage into an active learning layer inside the harness
  <sub>★ 22.2k · Python · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[engram](https://github.com/Gentleman-Programming/engram)** — Persistent memory for AI coding agents delivered as a single Go binary with SQLite + FTS5 and 18 MCP tools for save, search, session lifecycle, and conflict detection. The agent-agnostic, zero-dependency design makes cross-session memory a local harness primitive rather than a managed cloud service
  <sub>★ 6.3k · Go · MIT · brew · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install gentleman-programming/tap/engram`</sub>
- **[Zep](https://github.com/getzep/zep)** — Purpose-built agent memory store with automatic conversation summarization, entity extraction, and semantic search over session history. Solves long-session context overflow at the memory layer rather than forcing the harness to manage trimming manually
  <sub>★ 4.9k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zep-cloud`</sub>
- **[mex](https://github.com/mex-memory/mex)** — Turns agent-learned project knowledge into a repo-local, symbol-grounded wiki with drift detection and task-aware routing. The critical gap it fills: most agent memory stores facts, but mex keeps those facts connected to the exact code symbols they describe and flags when code changes invalidate them — making memory freshness a harness-level concern rather than a manual cleanup task
  <sub>★ 1.5k · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g mex-agent`</sub>
- **[claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler)** — Turns raw Claude Code sessions into a self-evolving knowledge base: hooks capture every interaction, the Agent SDK extracts decisions and lessons, and an LLM compiler distills them into structured, cross-referenced articles that improve retrieval quality over time. The most concrete open-source implementation of trace-driven memory evolution for coding agents
  <sub>★ 1.3k · Python · source · pushed 2026-04-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/coleam00/claude-memory-compiler.git`</sub>
- **[Stash](https://github.com/alash3al/stash)** — Self-hosted persistent memory layer with an 8-stage consolidation pipeline (episodes → facts → relationships → patterns) and built-in MCP server. The critical gap it fills: production-grade cross-session memory without cloud dependencies or complex infrastructure — a single Docker Compose gives you Postgres, pgvector, and background consolidation
  <sub>★ 767 · Go · Apache-2.0 · clone · pushed 2026-06-14 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/alash3al/stash.git`</sub>
- **[deja-vu](https://github.com/vshulcz/deja-vu)** — Indexes coding-agent sessions already written to disk and serves them back over MCP with no LLM calls, embeddings, or API keys. The zero-dependency binary solves the memory cold-start problem for cross-session persistence and demonstrates that agent memory can be built on existing filesystem traces rather than a separate learning pipeline
  <sub>★ 764 · Go · MIT · scoop · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop install deja-vu`</sub>
- **[How We Built Agent Builder's Memory System](https://blog.langchain.com/how-we-built-agent-builders-memory-system/)** — LangChain's engineering account of a COALA-based three-tier memory system (procedural/semantic/episodic) backed by PostgreSQL but exposed to agents as a virtual filesystem. Key harness decisions: human-in-the-loop approval gates every memory write (blocking prompt-injection via malformed writes), validation errors are fed back to the LLM for self-correction, and AGENTS.md serves as the agent's pro
  <sub>website</sub>
  <sub>`https://blog.langchain.com/how-we-built-agent-builders-memory-system/`</sub>
- **[Building an Agentic Memory System for GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)** — GitHub's January 15, 2026 write-up is one of the clearest public discussions of deployed cross-agent memory: repository-scoped memories are shared across coding agent, CLI, and code review, but only after just-in-time verification against the current code state. The core harness lesson is that memory quality is mostly a freshness and invalidation problem — stale, branch-specific memories are often
  <sub>website</sub>
  <sub>`https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/`</sub>
- **[MemArchitect: A Policy-Driven Memory Governance Layer](https://arxiv.org/abs/2603.18330)** — Proposes a governance layer that decouples memory lifecycle management (decay, conflict resolution, privacy enforcement) from model weights, directly addressing the "zombie memory" problem: outdated facts sitting in the context window that only a harness-level eviction policy — not the model — can remove
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.18330`</sub>
- **[Codified Context: Infrastructure for AI Agents in a Complex Codebase](https://arxiv.org/abs/2602.20478)** — Production-validated architecture (283 sessions, 108k-line codebase) built on three components: a "hot-memory constitution" encoding conventions and multi-agent coordination protocols, 19 domain-specialist agents, and a "cold-memory knowledge base" of 34 on-demand specification documents. The empirical data distinguishes what must live in always-on context from what should be retrieved on demand —
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.20478`</sub>
- **[Facts as First Class Objects: Knowledge Objects for Persistent LLM Memory](https://arxiv.org/abs/2603.17781)** — Identifies three production failure modes of in-context memory at scale: capacity overflow at ~8,000 facts, 60% fact destruction during compaction, and 54% behavioral drift from constraint erosion across cascaded summarizations. Proposes Knowledge Objects (hash-addressed discrete fact tuples) achieving 100% accuracy at 252× lower cost than in-context storage — the quantitative case for moving pers
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.17781`</sub>
- **[Recoverability Has a Law: The ERR Measure for Tool-Augmented Agents](https://arxiv.org/abs/2601.22352)** — Formal framework for measuring how well agents recover from tool failures. Defines Expected Recovery Regret (ERR) as a metric for harness design: the cost of recovering from stochastic failures in downstream tasks. Critical for assessing reliability of production harnesses where tool calls occasionally fail but agents must continue functioning
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2601.22352`</sub>
- **[MAGMA: Multi-Graph Agentic Memory Architecture](https://arxiv.org/abs/2601.03236)** — Represents agent memory across four orthogonal semantic, temporal, causal, and entity graphs, enabling policy-guided retrieval over relational views. Outperforms MemGPT on long-horizon reasoning benchmarks by 18.5% accuracy improvement. The multi-graph abstraction lets harness engineers compose different retrieval strategies for different task phases — a concrete architecture for memory that scale
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2601.03236`</sub>
- **[GAAMA: Graph Augmented Associative Memory for Agents](https://arxiv.org/abs/2603.27910)** — Hybrid memory system blending graph traversal with semantic similarity through additive scoring; graph augmentation improves retrieval over embedding-only approaches for long-horizon reasoning. Practical alternative to full multi-graph systems when adding structure to existing vector-based memory is sufficient
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.27910`</sub>
- **[Continual learning for AI agents](https://blog.langchain.com/continual-learning-for-ai-agents/)** — LangChain's April 2026 framing of agent learning as three distinct layers: model weights, harness behavior, and contextual memory. Essential for designing memory systems that don't just store facts but actually improve agent performance over time through trace-driven harness and context updates
  <sub>website</sub>
  <sub>`https://blog.langchain.com/continual-learning-for-ai-agents/`</sub>
- **[ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](https://arxiv.org/abs/2604.10352)** — Applies virtual-memory semantics to agent context management, treating the context window as working memory with typed pages, minimum-fidelity invariants, and validated writeback at lifecycle boundaries. A concrete reference for making residency and durability auditable harness-level concerns rather than best-effort side effects
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.10352`</sub>
- **[MAGE: Memory as Agent-Guided Exploration](https://arxiv.org/abs/2606.06090)** — June 2026 proposal to treat long-horizon memory as execution-state management rather than semantic retrieval: a hierarchical state tree preserves trajectories, enables rollback, and constructs working state from the active root-to-leaf path. Improves task success by 7.8–20.4 percentage points while cutting token consumption 55.1%, making it a concrete reference for memory architectures where execu
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.06090`</sub>

## Skills &amp; MCP

- **[superpowers](https://github.com/obra/superpowers)** — Agentic skills framework and software-development methodology with automatically-triggered, mandatory skills that work across Claude Code, Cursor, Codex, Gemini CLI, and Copilot CLI. Demonstrates how to package cross-harness workflows — TDD, subagent-driven development, review gates — as reusable skills with an eval harness
  <sub>★ 281.2k · Shell · MIT · source · pushed 2026-08-31</sub>
  <sub>`git clone https://github.com/obra/superpowers.git`</sub>
- **[Ponytail](https://github.com/DietrichGebert/ponytail)** — Skill that makes coding agents behave like a "lazy senior dev": prefer built-in solutions, avoid new dependencies, and write the minimum code that works. Benchmarked on real Claude Code sessions with ~54% fewer lines, ~20% lower cost, and preserved safety guards — a rare harness-level incentive that fights over-engineering rather than just adding capability
  <sub>★ 123k · JavaScript · MIT · source · pushed 2026-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/DietrichGebert/ponytail.git`</sub>
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** — Production-grade engineering skills for AI coding agents, packaged as 24 reusable skills covering the full development lifecycle from /spec to /ship. The slash-command interface and context-aware auto-activation make it a concrete reference for turning senior-engineering judgment into agent-executable harness artifacts
  <sub>★ 91.9k · JavaScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add addyosmani/agent-skills # install all 25 skills`</sub>
- **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)** — Anthropic's official reference MCP server implementations (GitHub, Slack, Postgres, Puppeteer, etc.). The authoritative source for understanding correct MCP server structure before building your own
  <sub>★ 90k · TypeScript · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx -y @modelcontextprotocol/server-memory`</sub>
- **[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)** — Official Google MCP server that exposes live Chrome debugging surfaces — network analysis, performance profiling, console messages, memory snapshots, and Lighthouse audits — as structured agent tools. The clearest reference for turning browser inspection into a first-class tool interface rather than relying solely on screenshot-driven automation
  <sub>★ 50.8k · TypeScript · Apache-2.0 · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ChromeDevTools/chrome-devtools-mcp.git`</sub>
- **[Antigravity Awesome Skills](https://github.com/sickn33/agentic-awesome-skills)** — Installable library of 1,400+ agentic skills for Claude Code, Cursor, Codex CLI, Gemini CLI, and more. The largest community-driven skill catalog with an npm installer and role-based bundles — a concrete reference for treating skills as versioned harness artifacts rather than ad-hoc prompts
  <sub>★ 45.9k · Python · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agentic-awesome-skills --antigravity --skills brainstorming,systematic-debugging --dry-run`</sub>
- **[wshobson/agents](https://github.com/wshobson/agents)** — Cross-harness plugin marketplace that maintains one source-of-truth plugins/ directory and generates harness-native artifacts for Claude Code, Codex CLI, Cursor, OpenCode, Gemini CLI, and GitHub Copilot. It is the clearest practical example of treating reusable agent capabilities as a portable distribution format rather than ad-hoc prompt files
  <sub>★ 39.4k · Python · MIT · npx · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx codex-marketplace add wshobson/agents # Codex`</sub>
- **[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)** — Browser automation via accessibility tree snapshots rather than screenshots, dramatically reducing token cost. The canonical example of structured tool output design in an MCP server
  <sub>★ 36.8k · TypeScript · Apache-2.0 · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @playwright/mcp@latest --config path/to/config.json`</sub>
- **[Composio](https://github.com/ComposioHQ/composio)** — Wraps 250+ SaaS APIs (GitHub, Slack, Linear, Notion, etc.) as agent-ready actions with managed OAuth, so tool integration becomes a one-line import rather than a custom harness component per service. The fastest path from "the agent needs to call an external API" to a production-grade, authenticated tool
  <sub>★ 30k · TypeScript · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`pip install composio composio-openai-agents openai-agents`</sub>
- **[A2A Protocol](https://github.com/a2aproject/A2A)** — Google's open Agent-to-Agent protocol: JSON-RPC over HTTP(S)/SSE with Agent Card service discovery and a task/message/artifact communication model. The emerging standard for cross-framework agent interoperability in multi-agent harnesses
  <sub>★ 25.6k · Shell · Apache-2.0 · pip · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install a2a-sdk`</sub>
- **[SkillOpt](https://github.com/microsoft/SkillOpt)** — Microsoft's skill optimizer that trains reusable natural-language skills for frozen LLM agents through trajectory-driven edits and validation-gated updates, producing deployable best_skill.md artifacts. The key harness insight is that skills should be treated as optimizable parameters that improve with execution feedback, not static prompt fragments written once and forgotten
  <sub>★ 16.7k · Python · MIT · pip · pushed 2026-08-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install skillopt`</sub>
- **[AG-UI](https://github.com/ag-ui-protocol/ag-ui)** — Lightweight event-driven protocol standardizing how AI agents connect to frontend applications: streaming state updates, tool call rendering, and HITL interrupts over a shared event bus. Fills the layer between MCP (tool access) and A2A (agent-to-agent) — it's the missing protocol for real-time agent-to-UI communication that neither MCP nor A2A was designed to address
  <sub>★ 15.7k · Python · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx create-ag-ui-app my-agent-app`</sub>
- **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)** — Interactive debugging UI for MCP servers: inspect tool definitions, send test calls, and validate responses without wiring up a full agent. The essential development tool for anyone building or integrating MCP servers into a harness
  <sub>★ 10.8k · TypeScript · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @modelcontextprotocol/inspector # web UI (default)`</sub>
- **[mcp-agent](https://github.com/lastmile-ai/mcp-agent)** — Production-grade framework for building agents with MCP: composable workflows, built-in observability, and provider-agnostic model routing. The clearest reference for turning MCP servers from isolated utilities into a coherent agent harness
  <sub>★ 8.5k · Python · Apache-2.0 · uv · pushed 2026-01-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mcp-agent init --template basic # Scaffold a new project`</sub>
- **[oomol-lab/open-connector](https://github.com/oomol-lab/open-connector)** — Open-source auth gateway connecting 1000+ SaaS providers to AI agents through SDK, CLI, MCP, HTTP, and OpenAPI. Treats external-tool onboarding as a unified, self-hosted harness layer: one credential and access model covers direct SDK calls, MCP servers, and OpenAPI discovery, so teams don't rebuild auth per integration
  <sub>★ 5.5k · TypeScript · Apache-2.0 · source · pushed 2026-09-03 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/oomol-lab/open-connector.git`</sub>
- **[agentgateway](https://github.com/agentgateway/agentgateway)** — Open-source agentic proxy that unifies LLM gateway, MCP gateway, and A2A gateway into a single control plane for managing multi-agent, multi-tool connectivity at scale. Provides drop-in security, observability, and governance for agent-to-LLM, agent-to-tool, and agent-to-agent communication — the missing infrastructure layer between agents and the services they touch
  <sub>★ 4.7k · Rust · Apache-2.0 · source · pushed 2026-09-03 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/agentgateway/agentgateway.git`</sub>
- **[agent-device](https://github.com/callstack/agent-device)** — MCP-native control layer for iOS and Android devices: snapshots, semantic targeting, typed client access, diagnostics, and replayable workflows. Fills a critical gap in the mobile-agent harness stack — most tool design assumes desktop or browser surfaces, but real-world agents increasingly need to interact with native mobile apps
  <sub>★ 4.3k · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g agent-device@latest`</sub>
- **[Microsoft Skills Framework](https://github.com/microsoft/skills)** — Standardized framework for defining, versioning, and distributing agent skills. Enables skill reuse across Claude Code, Copilot, VS Code, Gemini, and other platforms — a harness-level abstraction that makes skills first-class deployment artifacts rather than ad-hoc tool definitions
  <sub>★ 3k · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add microsoft/skills`</sub>
- **[Comet](https://github.com/rpamis/comet)** — Resumable long-running task workflow and Skill platform for coding that turns skill creation, evaluation, and release into a single lifecycle with Rubric, Pass@k, and Pass^k scoring. The Native/Classic dual-workflow model is a concrete reference for matching harness constraint strength to model capability rather than using one loop for every task
  <sub>★ 2.9k · JavaScript · MIT · npm · pushed 2026-09-03 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npm install -g @rpamis/comet`</sub>
- **[Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins)** — Qwen's official multimodal plugin suite packages vision, video, document, 3D, and CAD capabilities as portable skills and MCP servers across Claude Code, Codex, OpenCode, and other harnesses. It shows how to make a text-first coding harness multimodal-native without rebuilding the agent loop
  <sub>★ 2.8k · HTML · Apache-2.0 · script · pushed 2026-09-03 · Win? · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/QwenLM/Qwen-MM-Plugins/main/install.sh | bash`</sub>
- **[Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)** — Official AWS-supported MCP servers, skills, and plugins that let AI agents provision, query, and manage AWS resources through a standardized protocol interface. Worth including as the reference for how a major cloud provider productizes infrastructure access into agent-ready harness primitives rather than leaving teams to hand-roll IAM-scoped tool definitions
  <sub>★ 2.5k · Python · Apache-2.0 · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add aws/agent-toolkit-for-aws/skills`</sub>
- **[agentic-stack](https://github.com/codejunkie99/agentic-stack)** — Portable .agent/ folder that externalizes memory, skills, and protocols from any specific coding agent into a cross-tool harness layer. Adapters translate the same configuration into Claude Code's CLAUDE.md, Cursor's rules, OpenCode's AGENTS.md, and more — the first practical answer to harness vendor lock-in at the configuration level
  <sub>★ 2.2k · Python · Apache-2.0 · brew · pushed 2026-09-02 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew tap codejunkie99/agentic-stack https://github.com/codejunkie99/agentic-stack`</sub>
- **[mgechev/skillgrade](https://github.com/mgechev/skillgrade)** — CLI that turns agent skill verification into repeatable unit tests: it generates task and grader pairs from a SKILL.md, runs multi-trial evals against Claude, Codex, Gemini, or OpenCode, and reports pass rates with a CI-ready threshold. Fills the gap between shipping a skill and knowing an agent actually discovers and invokes it correctly
  <sub>★ 697 · TypeScript · MIT · npm · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g skillgrade`</sub>
- **[SkillNet &amp; SkillsBench: Infrastructure for AI Agent Skills at Scale](https://github.com/skillmatic-ai/awesome-agent-skills)** — Comprehensive framework for creating, evaluating, and sharing agent skills with 86-task benchmark across 11 domains. Demonstrates the harness problem of skill fragmentation and provides infrastructure for standardized skill evaluation across frameworks
  <sub>★ 667 · CC0-1.0 · source · pushed 2026-05-14</sub>
  <sub>`git clone https://github.com/skillmatic-ai/awesome-agent-skills.git`</sub>
- **[vurb.ts](https://github.com/vinkius-labs/mcpfusion)** — TypeScript framework for building production MCP servers with a "Presenter" perception layer that strips undeclared fields, redacts PII, and gates tool visibility by workflow state. Fills a critical gap in the MCP ecosystem: most tooling focuses on consuming servers, while vurb.ts addresses the harness engineering of authoring servers that are safe, governable, and context-aware by default
  <sub>★ 256 · TypeScript · Apache-2.0 · source · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vinkius-labs/vurb.ts.git`</sub>
- **[Model Context Protocol](https://modelcontextprotocol.io/introduction)** — Anthropic's open protocol for connecting agents to external tools, data sources, and services in a standardized way
  <sub>website</sub>
  <sub>`https://modelcontextprotocol.io/introduction`</sub>
- **[Announcing the Agentic Resource Discovery specification](https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/)** — Google's June 2026 open specification for publishing, discovering, and verifying AI capabilities across the web via domain-owned catalogs and searchable registries. Adds the missing discovery layer that lets agents find MCP servers, A2A agents, and OpenAPI tools at runtime rather than relying on hardcoded integrations, with trust manifests and namespaced URNs for governance
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/`</sub>
- **[Shell + Skills + Compaction: Tips for Long-Running Agents](https://developers.openai.com/blog/skills-shell-tips)** — OpenAI's engineering guide to three production harness primitives: versioned Skill bundles (SKILL.md manifest; routing accuracy improved 73%→85% by adding negative examples), a managed shell container for durable tool execution, and server-side compaction via explicit /responses/compact endpoint. The most concrete first-party documentation of skills-based routing and compaction published in 2026
  <sub>website</sub>
  <sub>`https://developers.openai.com/blog/skills-shell-tips`</sub>
- **[MCP Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)** — The transport that replaced HTTP+SSE in the 2025-11-25 spec, enabling MCP servers to run as remote services rather than local processes. Servers handle multiple client connections using HTTP POST (for client→server messages) and optional GET (for server→client SSE streams). The key harness architecture decision: Streamable HTTP unlocks remote MCP deployment but introduces session management comple
  <sub>website</sub>
  <sub>`https://modelcontextprotocol.io/specification/2025-11-25/basic/transports`</sub>
- **[The 2026 MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)** — The MCP team's roadmap for the next spec cycle: horizontal-scaling transport without stateful session constraints, .well-known discovery for capability advertisement without live connections, Tasks primitive with retry/expiry semantics, and enterprise extensions (audit trails, SSO, gateway behavior). Essential reading before investing heavily in MCP server infrastructure — the transport and discov
  <sub>website</sub>
  <sub>`https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/`</sub>
- **[The 2026-07-28 MCP Specification Release Candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)** — The largest revision of MCP since launch: a stateless protocol core drops the initialize handshake and Mcp-Session-Id, the new ext-* extension framework formalizes Tasks and MCP Apps, and a twelve-month deprecation policy gives harness builders a stable target. Essential reading before designing remote MCP server infrastructure that must survive load balancers and horizontal scaling
  <sub>website</sub>
  <sub>`https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/`</sub>
- **[Developer's Guide to AI Agent Protocols](https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/)** — Google's survey of six standardized agent interoperability protocols, each solving a distinct harness integration problem: MCP (tool/data connectivity), A2A (inter-agent routing via Agent Card discovery at well-known URLs), UCP (commerce workflows), AP2 (payment authorization with spend limits), A2UI (agent-driven dynamic UIs), AG-UI (streaming event format). The most practical map of which protoc
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/`</sub>
- **[Code Execution with MCP: Building More Efficient Agents](https://www.anthropic.com/engineering/code-execution-with-mcp)** — Anthropic's engineering account of reducing tool-call token overhead by having agents write code to interact with MCP servers rather than calling tools directly: up to 98.7% token reduction in experiments. Broadly applicable to any harness where tool schema overhead and intermediate results are consuming context — the pattern is to wrap multi-step tool interaction in a code execution primitive rat
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/code-execution-with-mcp`</sub>
- **[AWS Bedrock AgentCore with WebRTC Support](https://aws.amazon.com/about-aws/whats-new/2026/03/amazon-bedrock-webrtc/)** — Adds peer-to-peer, UDP-based WebRTC bidirectional streaming to Bedrock Agents for real-time voice interactions. Complements existing WebSocket support with lower latency and better resilience for poor network conditions. Essential harness-level transport choice for agents targeting sub-800ms Total Turn-Around Time voice interactions
  <sub>website</sub>
  <sub>`https://aws.amazon.com/about-aws/whats-new/2026/03/amazon-bedrock-webrtc/`</sub>
- **[Hermes Agent: Unified Streaming for Real-Time Agent Workflows](https://juliangoldie.com/hermes-agent-unified-streaming/)** — Token-by-token streaming delivery system enabling real-time agent responses; sub-second decision loops on streaming events vs. batch-refreshed data. Critical infrastructure for harnesses where latency (not just throughput) is the constraint — agents must react to events as they arrive, not wait for batch completions
  <sub>website</sub>
  <sub>`https://juliangoldie.com/hermes-agent-unified-streaming/`</sub>
- **[Google Developers: Closing the Knowledge Gap with Agent Skills](https://developers.googleblog.com/closing-the-knowledge-gap-with-agent-skills/)** — Google ADK expansion with evaluation harness (117 prompts) for assessing skill performance across agentic coding, chatbots, document processing. Provides reference patterns and benchmark datasets for skill evaluation, complementing the Microsoft Skills Framework with Google's evaluation methodology
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/closing-the-knowledge-gap-with-agent-skills/`</sub>
- **[What's New with GitHub Copilot Coding Agent](https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/)** — GitHub's February 26, 2026 update is worth including for one specific reason: it makes .github/agents/ custom agent files, self-review, built-in security scanning, and CLI handoff concrete as harness primitives rather than abstract ideas. Useful as a current reference for how repository-scoped agent definitions and security checks are being productized in a real coding-agent control plane
  <sub>website</sub>
  <sub>`https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/`</sub>
- **[Announcing Official MCP Support for Google Services](https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services)** — Google's 2026 rollout of managed MCP endpoints is a useful counterpoint to self-hosted MCP servers: discovery, IAM, audit logging, and Model Armor are provided as platform primitives instead of being rebuilt per server. Worth including because it shows what "enterprise MCP" looks like when the transport, auth, and governance layers are treated as product surface rather than glue code
  <sub>website</sub>
  <sub>`https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services`</sub>
- **[Dataverse Skills: Your Coding Agent Now Speaks Dataverse](https://devblogs.microsoft.com/powerplatform/dataverse-skills-your-coding-agent-now-speaks-dataverse)** — Microsoft's April 1, 2026 release is a strong concrete example of domain-specific skills done properly: the agent learns when to use MCP, when to drop to a Python SDK, and when to call a raw API, while the user stays in natural language. Worth adding because it shows that "skills" are not just prompt snippets, but curated execution strategies that hide a multi-tool integration stack behind intent
  <sub>website</sub>
  <sub>`https://devblogs.microsoft.com/powerplatform/dataverse-skills-your-coding-agent-now-speaks-dataverse`</sub>
- **[You can't whisper at an AI agent](https://stripe.dev/blog/ai-steering-experiments)** — Stripe's May 2026 study of how agents actually consume SDK and CLI guidance: passive documentation is ignored, while hard steering signals placed in the loaded context — skill files, error messages, CLI prompts — reliably change behavior. The "if your guidance wasn't in the loaded context, it didn't happen" principle is a practical design rule for any skill, tool, or SDK that agents are expected t
  <sub>website</sub>
  <sub>`https://stripe.dev/blog/ai-steering-experiments`</sub>
- **[AIP: A Graph Representation for Learning and Governing Agent Skills](https://arxiv.org/abs/2606.04781)** — June 2026 proposal to replace free-form skill prose with directed execution graphs: discrete steps as nodes backed by deterministic scripts or natural-language descriptions, connected by explicit typed input/output edges and governed by a schema-validated YAML spec. Compiling skills to AIP improved Claude Sonnet's pass rate from 53% to 67% while making skills queryable, auditable, and repairable a
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.04781`</sub>

## Tool Design

- **[CLI-Anything](https://github.com/HKUDS/CLI-Anything)** — Generates agent-native CLI harnesses for any software, giving agents structured JSON access to applications that were never designed for automation. The CLI-Hub registry and auto-generated SKILL.md files turn tool expansion into a package-manager experience — solving the "long tail" of agent tool coverage without a custom wrapper per program
  <sub>★ 48.9k · Python · Apache-2.0 · npx · pushed 2026-08-21 · Win · WSL2 · macOS · Linux</sub>
  <sub>`npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill -g -y`</sub>
- **[outlines](https://github.com/dottxt-ai/outlines)** — Constrains token sampling via regex/CFG/JSON Schema at the decoding layer, guaranteeing structured output without model fine-tuning. The right solution when you need OpenAI Structured Outputs-equivalent reliability from a locally deployed or open-weight model
  <sub>★ 15.7k · Python · Apache-2.0 · pip · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install outlines`</sub>
- **[zerolang](https://github.com/vercel-labs/zerolang)** — Experimental graph-first programming language where agents inspect and edit code through a compiler-derived ProgramGraph (node IDs, graph hashes, types, effects, ownership) instead of fragile text patches. Collapses the typical agent loop of edit-format-reparse-check-fix into a single compiler-validated semantic operation — a reference design for making code manipulation a structured tool interfac
  <sub>★ 5.4k · C · Apache-2.0 · npx · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add vercel-labs/zerolang`</sub>
- **[tui-use](https://github.com/onesuper/tui-use)** — Expands the agent tool surface beyond non-interactive commands: programmable TUI interaction for REPLs, debuggers, and ncurses apps that standard bash can't reach. A concrete harness primitive for any agent that needs to operate interactive CLI tools without building a custom wrapper per program
  <sub>★ 259 · TypeScript · MIT · npm · pushed 2026-04-11 · WSL2 · macOS? · Linux</sub>
  <sub>`npm install -g tui-use`</sub>
- **[Tool Use — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)** — Authoritative reference for client vs. server tool execution models, strict schema enforcement, and tool_result error signaling. The distinction between client-side and server-side tool execution is a foundational harness architecture decision
  <sub>website</sub>
  <sub>`https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview`</sub>
- **[Function Calling — OpenAI Docs](https://platform.openai.com/docs/guides/function-calling)** — Defines the de facto industry-standard JSON Schema conventions for tool definitions and parallel function calling. Essential reading before designing a tool interface that needs to work across multiple models
  <sub>website</sub>
  <sub>`https://platform.openai.com/docs/guides/function-calling`</sub>
- **[Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)** — The MCP team's definitive post on the four tool annotation hints (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) as inputs to harness permission decisions, not enforced contracts. The "lethal trifecta" — private data access + untrusted content exposure + external communication — is the most actionable framing for why single-tool safety analysis misses the risk that emerges from tool
  <sub>website</sub>
  <sub>`https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/`</sub>
- **[instructor](https://python.useinstructor.com/)** — Maps Pydantic models directly to structured LLM extraction with built-in retry and validation-error feedback loops. Turns tool call output parsing from ad-hoc JSON handling into type-safe data models, eliminating an entire class of harness parsing bugs
  <sub>website</sub>
  <sub>`https://python.useinstructor.com/`</sub>
- **[SkillTester: Benchmarking Utility and Security of Agent Skills](https://arxiv.org/abs/2603.28815)** — Framework for evaluating agent skills on three dimensions (capability, robustness, security) before deployment. Directly addresses the harness problem of skill sprawl: as agents gain access to more tools, the combinatorial explosion of failure modes becomes unmanageable without systematic verification. The 86-task benchmark across 11 domains provides reference metrics for skill quality
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.28815`</sub>
- **[AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness](https://arxiv.org/abs/2603.03329)** — Google DeepMind technique that uses code synthesis to auto-generate runtime constraint harnesses from tool schemas and task specifications. Gemini-2.5-Flash + AutoHarness outperforms Gemini-2.5-Pro and GPT-5.2-High on TextArena games by eliminating illegal moves through learned harness policies. Shifts constraint enforcement from static (schema validation) to dynamic (synthesized code guards) — a
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.03329`</sub>
- **[Scaling Parallel Tool Calling for Efficient Deep Research](https://arxiv.org/abs/2602.07359)** — February 2026 analysis of how parallel tool calling reduces latency in multi-step agent workflows. Demonstrates that concurrent tool execution (rather than sequential observe→act loops) is the key efficiency lever for deep-research harnesses where each step may invoke search, browse, and compute tools simultaneously. Essential for designing low-latency agent loops without sacrificing reasoning dep
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.07359`</sub>
- **[EigentSearch-Q+](https://arxiv.org/abs/2604.07927)** — April 2026 framework for deep-research agents using dedicated reasoning tools (plan_next_searches, select_query_and_search, extract_relevant_details, analyze_search_progress) that externalize intermediate decisions as typed tool arguments. Inspired by Anthropic's think-tool paradigm, Q+ makes cognitive scaffolding explicit and auditable — bridging classic information-retrieval strategies with stru
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.07927`</sub>
- **[TopoCurate: Modeling Interaction Topology for Tool-Use Agent Training](https://arxiv.org/abs/2603.01714)** — March 2026 framework that models interaction topology — the structural patterns of how agents invoke, chain, and conditionally branch between tools — as a first-class training signal. Rather than treating tool use as isolated function calls, TopoCurate learns topological priors from expert trajectories, improving generalization to novel tool combinations and multi-step orchestration patterns. Dire
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.01714`</sub>
- **[Design Patterns for Deploying AI Agents with Model Context Protocol](https://arxiv.org/abs/2603.13417)** — March 2026 field report from an enterprise MCP deployment identifying three protocol-level gaps that break production: missing identity propagation (who is the request for?), absent adaptive tool budgeting, and unstructured error semantics. The concrete mitigation patterns — JWT-enriched tool calls, per-tool timeout contracts, and standardized error-action mappings — are essential before betting o
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.13417`</sub>

## Security, Sandbox &amp; Permissions

- **[Daytona](https://github.com/daytonaio/daytona)** — OCI-container sandboxes with sub-90ms startup, built-in Git operations, LSP support, and indefinite state persistence. Complements E2B for harnesses that need long-lived working directories across multiple agent sessions rather than ephemeral code execution
  <sub>★ 71.8k · pip · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install daytona`</sub>
- **[Alibaba OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)** — General-purpose sandbox platform for AI agents (8.7K+ stars, March 2026) with multi-language SDKs (Python, Java, TypeScript, Go, C#), unified APIs across Docker/Kubernetes runtimes, and support for secure container runtimes (gVisor, Kata Containers, Firecracker). Covers coding agents, GUI agents, agent evaluation, and RL training in a single abstraction layer — the most runtime-flexible sandbox op
  <sub>★ 14.9k · Go · Apache-2.0 · uv · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install opensandbox-cli`</sub>
- **[IronClaw](https://github.com/nearai/ironclaw)** — NEAR AI's open-source agent OS that treats agent execution as a privacy-first harness problem: untrusted tools run in WASM sandboxes with capability-based permissions, credentials are injected at the host boundary with leak detection, and prompt-injection filtering plus endpoint allowlisting constrain agent behavior. The combination of local encrypted storage, hybrid-search memory, MCP server supp
  <sub>★ 12.6k · Rust · Apache-2.0 · psh · pushed 2026-09-02 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm "https://github.com/nearai/ironclaw/releases/download/$IronClawReleaseTag/ironclaw-installer.ps1" | iex`</sub>
- **[CubeSandbox](https://github.com/TencentCloud/CubeSandbox)** — Tencent Cloud's production-validated microVM sandbox for AI agents: sub-60ms cold start via snapshot cloning, &lt;5MB per-instance overhead, and true kernel-level isolation with eBPF-enforced network policies. E2B-compatible drop-in replacement that demonstrates how hyperscale cloud infrastructure can be repurposed for high-density agent execution
  <sub>★ 11.7k · Go · source · pushed 2026-09-03 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/TencentCloud/CubeSandbox.git`</sub>
- **[cloudflare/computer](https://github.com/cloudflare/computer)** — Cloudflare's preview open-source agent runtime: a Durable Object hosts authoritative workspace state in SQLite, while pluggable backends (container FUSE mount, isolate shell, isolate JavaScript) execute code against that single source of truth. The key harness idea is that durable state and sandboxed execution can share one primitive instead of requiring separate storage, sync, and isolation layer
  <sub>★ 9k · TypeScript · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cloudflare/computer.git`</sub>
- **[NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell)** — Open-source policy-driven sandbox runtime for autonomous AI agents, announced at GTC 2026. Enforces security constraints at the kernel level via Landlock LSM (filesystem), seccomp BPF (syscalls), and an OPA/Rego-evaluated HTTP CONNECT proxy (network) — constraints are enforced on the environment itself, so even a compromised agent cannot override them. Supports Claude Code, Codex, Cursor, and Open
  <sub>★ 8.5k · Rust · Apache-2.0 · npx · pushed 2026-09-03 · macOS · Linux</sub>
  <sub>`npx skills add NVIDIA/OpenShell`</sub>
- **[deepsec](https://github.com/vercel-labs/deepsec)** — Vercel Labs' security harness that treats vulnerability scanning as an agentic workflow: idempotent commands for interrupt-resume across distributed workers, SKILL.md context injection, and explicit cost transparency that forces rigorous context design. The clearest reference for building high-stakes, long-running agent harnesses where failure recovery directly determines ROI
  <sub>★ 7.9k · TypeScript · Apache-2.0 · npx · pushed 2026-08-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx deepsec init`</sub>
- **[NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)** — NVIDIA's programmable guardrails toolkit: define input, dialog, retrieval, execution, and output rails that intercept the agent loop at five distinct layers using the Colang DSL. The execution rail layer specifically governs what tools the LLM can invoke and what their inputs/outputs may contain — the reference for behavioral-level enforcement when static allow/deny lists are insufficient
  <sub>★ 7.1k · Python · source · pushed 2026-09-02 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/NVIDIA-NeMo/Guardrails.git`</sub>
- **[Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)** — Seven-package, multi-language (Python, Rust, TypeScript, Go, .NET) runtime security toolkit that addresses all 10 OWASP Agentic AI risks with deterministic, sub-millisecond policy enforcement. Includes Agent OS (policy engine intercepting every action), Agent Mesh (secure agent-to-agent communication), and Agent Runtime (dynamic execution rings). Hooks into LangChain callbacks, CrewAI task decorat
  <sub>★ 6.2k · Python · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @microsoft/agent-governance-copilot-cli install`</sub>
- **[Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox)** — K8s-native Sandbox CRD (under SIG Apps) providing declarative, standardized APIs for managing isolated, stateful, singleton workloads for AI agent runtimes. Supports gVisor and Kata Containers for kernel-level isolation; v0.2.1 introduced "Secure by Default" networking architecture enforcing strict isolation with a shared policy model. The right choice when agents must run inside existing Kubernet
  <sub>★ 3.7k · Go · Apache-2.0 · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kubernetes-sigs/agent-sandbox.git`</sub>
- **[forkd](https://github.com/deeplethe/forkd)** — MicroVM sandbox runtime that replaces cold-boot isolation with fork-from-warm: children share a paused parent's memory copy-on-write, so 100 agent tool-execution sandboxes spawn in ~100 ms rather than seconds. The live-BRANCH primitive (~56 ms pause) lets an agent fork its own in-flight state for speculative exploration or checkpointing — a fundamental leap for harnesses where per-action isolation
  <sub>★ 2.8k · Rust · Apache-2.0 · pip · pushed 2026-09-02 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install forkd # Python SDK — calls the daemon over HTTP`</sub>
- **[zeroboot](https://github.com/zerobootdev/zeroboot)** — Sub-millisecond VM sandboxes for AI agents via copy-on-write forking, enabling fresh isolated execution on every tool call without the latency penalty of container or microVM cold starts. The critical harness advantage is turning per-action isolation from a batch-mode luxury into a real-time loop primitive — agents can spin up and tear down environments within a single reasoning step
  <sub>★ 2.4k · Rust · Apache-2.0 · source · pushed 2026-03-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zerobootdev/zeroboot.git`</sub>
- **[AgentShield](https://github.com/affaan-m/agentshield)** — Security scanner for AI agent configurations that detects hardcoded secrets, permission misconfigurations, hook injection, risky MCP servers, and prompt-injection vectors in Claude Code setups. Worth including because it turns harness security from a post-hoc audit into a pre-commit gate, surfacing configuration-level vulnerabilities before the agent runs
  <sub>★ 1.1k · TypeScript · MIT · npm · pushed 2026-07-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g ecc-agentshield`</sub>
- **[tldrsec/prompt-injection-defenses](https://github.com/tldrsec/prompt-injection-defenses)** — The most complete catalog of practical prompt injection defenses (input validation, tool output sanitization, canary tokens, etc.). Functions as a design checklist for hardening trust boundaries in any agent harness
  <sub>★ 728 · source · pushed 2025-02-22</sub>
  <sub>`git clone https://github.com/tldrsec/prompt-injection-defenses.git`</sub>
- **[RAMPART](https://github.com/microsoft/RAMPART)** — Pytest-native safety and security testing framework for agentic AI that turns red-team findings into repeatable CI tests. Supports statistical trials (e.g., "safe in 95% of runs") rather than single-shot pass/fail, making it the first concrete tool for treating agent safety as an engineering discipline rather than a post-hoc audit
  <sub>★ 403 · Python · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/RAMPART.git`</sub>
- **[aiming-lab/AutoHarness](https://github.com/aiming-lab/AutoHarness)** — Open-source Python governance harness that wraps any OpenAI-compatible client with a configurable tool-approval pipeline, prompt-injection defense, secret-exposure checks, and JSONL audit trails. Demonstrates how to productize "Agent = Model + Harness" into a drop-in governance layer rather than scattering guardrails across application code
  <sub>★ 369 · Python · MIT · gh-action · pushed 2026-04-02</sub>
  <sub>`uses: aiming-lab/AutoHarness@main # in .github/workflows/*.yml`</sub>
- **[StackOne Defender](https://github.com/StackOneHQ/defender)** — Open-source indirect prompt injection defense for agents: 22MB CPU-only model, ~4ms latency, 89% balanced accuracy. Inspects tool results before they enter the LLM context window, turning untrusted MCP/CLI/function-call output into a harness-sanitized boundary rather than a prompt-level gamble
  <sub>★ 119 · TypeScript · Apache-2.0 · source · pushed 2026-08-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stackoneHQ/defender.git`</sub>
- **[mcpguard-dynamic](https://github.com/facebook/mcpguard-dynamic)** — Meta's kernel-level eBPF sandbox for MCP tool calls: a transparent proxy that enforces capability policies through a policy engine, argument validator, and BPF LSM hooks (file, network, process, fork), so a compromised or malicious MCP server cannot bypass restrictions at the application layer. Includes a 14-server, 82-case benchmark showing the full defense stack achieves 68.9% attack prevention
  <sub>★ 73 · C · MIT · source · pushed 2026-07-22 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/facebook/mcpguard-dynamic.git`</sub>
- **[agent-shell-tools](https://github.com/google/agent-shell-tools)** — Google's open-source toolkit for giving coding agents controlled shell access with opinionated defaults: an nsjail-based sandbox, a command-filter rule language, and a gRPC execution proxy so agents can stream commands into isolation without exposing host credentials or filesystems. A concrete reference for separating the agent's shell surface from the host boundary rather than relying on prompt-l
  <sub>★ 14 · Go · Apache-2.0 · source · pushed 2026-06-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/google/agent-shell-tools.git`</sub>
- **[PGSandbox MCP](https://github.com/LVTD-LLC/pgsandbox)** — Local-first MCP server that gives coding agents disposable PostgreSQL databases with scoped roles, TTL cleanup, and bounded SQL/schema tools. It fills a narrower but important sandboxing gap: agents can validate migrations, reproduce database bugs, and seed demo states against a real database without handing them long-lived admin credentials
  <sub>★ 2 · Rust · MIT · cargo · pushed 2026-08-31 · Win? · WSL2? · macOS · Linux? · Docker</sub>
  <sub>`cargo install --git https://github.com/LVTD-LLC/pgsandbox --tag v0.5.0 --force`</sub>
- **[How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)** — Anthropic's May 2026 cross-product containment write-up: why environmental isolation must be the primary boundary, how model-layer defenses alone miss ~17% of overeager actions, and concrete sandbox architectures for chat, terminal, and autonomous workspace products. The exfiltration-through-allowlist case study is a stark reminder that the weakest link is often custom harness plumbing, not the sa
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/how-we-contain-claude`</sub>
- **[Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/)** — OpenAI's July 2026 engineering deep-dive into sandboxing Codex on Windows, where no Seatbelt/seccomp-style capability isolation exists: why AppContainer, Windows Sandbox, and Mandatory Integrity Control fell short, and how write-restricted tokens plus network suppression produce an elevated sandbox that keeps file writes and network access inside safe bounds. The clearest first-party reference for
  <sub>website</sub>
  <sub>`https://openai.com/index/building-codex-windows-sandbox/`</sub>
- **[The Agent Harness Belongs Outside the Sandbox](https://www.mendral.com/blog/agent-harness-belongs-outside-sandbox)** — Andrea Luzzardi's April 2026 argument for running the agent loop outside the sandbox: credentials stay out of untrusted containers, sandboxes become suspendable cattle rather than session lifelines, and the architecture cleanly separates orchestration from execution. The clearest published case for why "harness inside" and "harness outside" are different security and reliability models, not implem
  <sub>website</sub>
  <sub>`https://www.mendral.com/blog/agent-harness-belongs-outside-sandbox`</sub>
- **[Build zero-trust AI agents with Google's Agent Development Kit](https://developers.googleblog.com/build-zero-trust-ai-agents-with-googles-agent-development-kit/)** — Google's August 2026 guide to hardening autonomous ADK agents against prompt injection and production-state mutation, using cryptographic write signatures, gVisor sandboxing, and deterministic semantic gateways that sit outside the LLM context. The accompanying open-source customer-support agent demonstrates the threat model and defenses concretely
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/build-zero-trust-ai-agents-with-googles-agent-development-kit/`</sub>
- **[Model Context Protocol — Authorization](https://modelcontextprotocol.io/specification/2025-11-05/basic/authorization)** — MCP's specification for OAuth-based authorization flows when agents access external services
  <sub>website</sub>
  <sub>`https://modelcontextprotocol.io/specification/2025-11-05/basic/authorization`</sub>
- **[AI Harness Scorecard](https://github.com/anthropics/ai-harness-scorecard)** — Scores repositories on AI harness safeguards. Useful checklist for auditing your own harness's security posture
  <sub>unavailable</sub>
- **[E2B](https://github.com/e2b-dev/E2B)** — Firecracker microVM sandboxes purpose-built for agent tool loops: ~150ms cold start, Python/JS SDKs, open source. The clearest reference implementation of "code execution as a harness primitive" rather than a CI system bolted on
  <sub>pip · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install e2b`</sub>
- **[Prompt Injection — Simon Willison's Series](https://simonwillison.net/series/prompt-injection/)** — The most thorough public writing on why indirect prompt injection is uniquely dangerous for agent harnesses: agents actively consume untrusted external content (emails, web pages, tool outputs) that can hijack their actions. Essential for understanding the attack surface before designing trust boundaries
  <sub>website</sub>
  <sub>`https://simonwillison.net/series/prompt-injection/`</sub>
- **[OWASP LLM01:2025 — Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)** — OWASP's authoritative classification of direct and indirect prompt injection risks. Complements the tldrsec defense catalog: use this to define the threat model, use tldrsec to select countermeasures
  <sub>website</sub>
  <sub>`https://genai.owasp.org/llmrisk/llm01-prompt-injection/`</sub>
- **[LangSmith Sandboxes: Secure Code Execution for Agents](https://blog.langchain.com/introducing-langsmith-sandboxes-secure-code-execution-for-agents/)** — Describes a microVM-based sandboxing architecture with kernel-level isolation, resource caps (CPU/memory/disk), and an authentication proxy that keeps secrets entirely out of the runtime environment. Persistent WebSocket sessions support long-running agent tasks like dependency installation and test suite execution without the overhead of per-call container restarts
  <sub>website</sub>
  <sub>`https://blog.langchain.com/introducing-langsmith-sandboxes-secure-code-execution-for-agents/`</sub>
- **[Implementing a Secure Sandbox for Local Agents](https://cursor.com/blog/agent-sandboxing)** — Cursor's cross-platform sandbox implementation (macOS Seatbelt, Linux Landlock + seccomp, Windows WSL2) that lets agents run freely within a boundary and request approval only for external access. Key result: 40% fewer user interruptions vs. no-sandbox permissioning — agents explore freely inside the boundary rather than requesting every file operation. The training insight — that agents must be e
  <sub>website</sub>
  <sub>`https://cursor.com/blog/agent-sandboxing`</sub>
- **[Practical Security Guidance for Sandboxing Agentic Workflows](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)** — NVIDIA AI Red Team's mandatory controls for agent code execution: restrict network egress, block workspace escape, and critically — protect MCP server configuration and hooks files from agent modification. The core threat model: an agent that can edit its own harness configuration can escalate its own permissions, which standard sandbox isolation alone does not prevent
  <sub>website</sub>
  <sub>`https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/`</sub>
- **[Under the Hood: Security Architecture of GitHub Agentic Workflows](https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/)** — GitHub's March 9, 2026 architecture write-up is one of the clearest public descriptions of defense-in-depth for coding agents running inside CI: isolated agent container, firewall, MCP gateway, API proxy, staged safe outputs, and zero-secret execution. The key value is that it treats agent execution as a hostile workload inside automation infrastructure, which is exactly the mindset most harnesses
  <sub>website</sub>
  <sub>`https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/`</sub>
- **[AnonymAI: Integrating Differential Privacy with LLM Agents](https://www.mdpi.com/1999-5903/18/1/41)** — Framework for automating data anonymization in agent workflows. Directly addresses the harness problem of unintentional PII leakage through tool calls and memory writes — privacy enforcement moves from the agent (prompt-level trust) to the harness boundary (structural enforcement). Essential for regulatory compliance in EU, Canada, and emerging state-level privacy regimes
  <sub>website</sub>
  <sub>`https://www.mdpi.com/1999-5903/18/1/41`</sub>
- **[Sandbox Agents | OpenAI API Docs](https://developers.openai.com/api/docs/guides/agents/sandboxes)** — OpenAI's authoritative April 2026 guide to sandbox architecture in the Agents SDK. The core principle is strict separation between the harness control plane (auth, billing, orchestration) and the sandbox compute plane (files, shell, ports), with manifest contracts, resumable session state, and sandbox-native memory
  <sub>website</sub>
  <sub>`https://developers.openai.com/api/docs/guides/agents/sandboxes`</sub>
- **[Grimlock: Guarding High-Agency Systems with eBPF and Attested Channels](https://arxiv.org/abs/2605.27488)** — Roblox's agent guard for high-agency systems: eBPF-forced traffic interception channels every agent-to-agent and agent-to-service call through a guard, post-handshake TLS 1.3 attestation binds identity to the channel, and short-lived scope tokens enforce least-privilege delegation across heterogeneous machines and clouds. The key harness insight is that identity, authorization, provenance, and del
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2605.27488`</sub>
- **[Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/)** — V8 isolate-based sandboxing for AI-agent-generated code execution, now in open beta. Isolates start in milliseconds using megabytes of memory — 100x faster and up to 100x more memory-efficient than containers. The sandbox intercepts outbound HTTP requests for credential injection so agent code never touches secrets directly. A fundamentally different architectural option from container-based sandb
  <sub>website</sub>
  <sub>`https://blog.cloudflare.com/dynamic-workers/`</sub>
- **[Why sandboxing your agent is not enough](https://www.cncf.io/blog/2026/07/07/why-sandboxing-your-agent-is-not-enough/)** — CNCF's July 2026 argument that container isolation is necessary but insufficient for production agents. The agent-substrate pattern decouples the agent actor from pod lifecycle so agents execute in short bursts, suspend when idle, and resume on any worker while keeping gVisor/Kata-level isolation. A concrete pattern for high-density, low-idle-cost secure agent fleets in Kubernetes
  <sub>website</sub>
  <sub>`https://www.cncf.io/blog/2026/07/07/why-sandboxing-your-agent-is-not-enough/`</sub>
- **[The Attack and Defense Landscape of Agentic AI: A Comprehensive Survey](https://arxiv.org/abs/2603.11088)** — The first systematic survey of AI agent security from UC Berkeley and UIUC (Dawn Song et al., March 2026). Reviews 128 papers covering 51 attack methods and 60 defense mechanisms. Introduces a framework for understanding security risks specific to agentic (not just LLM) systems and identifies open gaps in securing agent architectures — the definitive 2026 reference for agent threat modeling
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.11088`</sub>
- **[Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents)** — Anthropic's April 2026 framework for governing autonomous agents through five principles: human control, value alignment, secure interactions, transparency, and privacy. The most complete published treatment of how to design harness-level governance that keeps pace with increasing agent capability and autonomy
  <sub>website</sub>
  <sub>`https://www.anthropic.com/research/trustworthy-agents`</sub>

## Permissions &amp; Authorization

- **[Agent Vault](https://github.com/Infisical/agent-vault)** — Infisical's open-source credential broker that sits between AI agents and the APIs they call, injecting real credentials onto outbound requests so agents never possess secrets directly. Eliminates a concrete prompt-injection attack surface — exfiltration of API keys and PATs — by treating credential possession as a harness-layer boundary rather than an agent-side configuration
  <sub>★ 2.2k · Go · script · pushed 2026-09-03 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl --proto '=https' --proto-redir '=https' --tlsv1.2 -fsSL https://get.agent-vault.dev | sh`</sub>
- **[nah](https://github.com/manuelschipper/nah)** — Deterministic permission guard that maps tool calls to an intent taxonomy (filesystem_delete, network_outbound, lang_exec, etc.) rather than relying on command-name allow/deny lists. The key insight for harness design: the same binary can be benign or destructive depending on its arguments, so intent-level enforcement is the only reproducible safety layer
  <sub>★ 480 · Rust · MIT · psh · pushed 2026-08-31 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://nahguard.ai/install.ps1 | iex`</sub>
- **[Aegis](https://github.com/Justin0504/Aegis)** — Pre-execution firewall that intercepts, classifies, and blocks agent tool calls before they execute, with a compliance cockpit for real-time monitoring, human-in-the-loop approvals, and a tamper-evident audit trail. The zero-code-change integration makes runtime policy enforcement practical for existing agent deployments
  <sub>★ 337 · TypeScript · MIT · pip · pushed 2026-08-21 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`pip install agentguard-aegis`</sub>
- **[OWASP LLM06:2025 — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** — OWASP's authoritative definition of the "excessive agency" risk: over-provisioned functions, unnecessary permissions, and missing approval mechanisms. The standard checklist for auditing harness permission scope against principle of least privilege
  <sub>website</sub>
  <sub>`https://genai.owasp.org/llmrisk/llm062025-excessive-agency/`</sub>
- **[GitHub Enterprise — Governing Agents](https://wellarchitected.github.com/library/governance/recommendations/governing-agents/)** — April 2026 GitHub official guide for enterprise agent governance: MCP server registry curation with ruleset-protected configurations, agent environment standardization via copilot-setup-steps.yml, ephemeral runner enforcement, and cloud-agent firewall allowlisting. The most concrete published reference for governing agent fleets at scale without creating bottlenecks
  <sub>website</sub>
  <sub>`https://wellarchitected.github.com/library/governance/recommendations/governing-agents/`</sub>
- **[Claude Code Auto Mode: A Safer Way to Skip Permissions](https://www.anthropic.com/engineering/claude-code-auto-mode)** — Anthropic's engineering post on replacing approval fatigue (users approve 93% of prompts, making approvals meaningless) with a two-stage classifier: fast single-token gate first, chain-of-thought reasoning only on flagged actions. The design decisions — stripping assistant messages to prevent the agent from rationalizing dangerous actions, deny-and-continue recovery instead of halt — are the refer
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/claude-code-auto-mode`</sub>
- **[Claude Agent SDK — Configure Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)** — The most concrete reference for harness permission architecture: five-layer evaluation order (hooks → deny rules → permission mode → allow rules → canUseTool), allowedTools/disallowedTools declarative scoping, and four permission modes including dontAsk (deny-by-default for headless agents). The subagent inheritance warning for bypassPermissions alone is worth reading before any multi-agent deploy
  <sub>website</sub>
  <sub>`https://platform.claude.com/docs/en/agent-sdk/permissions`</sub>
- **[Two Different Types of Agent Authorization](https://blog.langchain.com/two-different-types-of-agent-authorization/)** — Distinguishes on-behalf-of authorization (agent uses end-user credentials, requires cross-channel identity mapping and per-user memory isolation) from fixed-credential authorization (agent owns its own account, requires human-in-the-loop guardrails on high-risk actions). The two models have fundamentally different threat surfaces and determine where authorization enforcement lives in the harness
  <sub>website</sub>
  <sub>`https://blog.langchain.com/two-different-types-of-agent-authorization/`</sub>
- **[IETF draft-klrc-aiagent-auth: AI Agent Authentication and Authorization](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/)** — The first IETF standards-track specification for AI agent authentication (March 2026, authors from AWS, OpenAI, Zscaler, Ping Identity, Defakto Security). Builds on WIMSE (Workload Identity in Multi-System Environments) and OAuth 2.0 rather than inventing new protocols — agents get SPIFFE-style identifiers, with delegation via OAuth Token Exchange and DPoP for token binding. Essential reference fo
  <sub>website</sub>
  <sub>`https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/`</sub>
- **[Nango: Pre-Built Authentication for AI Agents](https://nango.dev)** — Open-source platform providing pre-built OAuth and API key authentication for 700+ APIs across 30 categories. Automatically refreshes access tokens, provides webhooks when credentials break, and stores tokens securely so agent code never touches secrets. Solves the "agent needs to call an authenticated API" problem at scale — the authentication layer that complements Composio's tool wrapping
  <sub>website</sub>
  <sub>`https://nango.dev`</sub>
- **[AgentDoG: A Diagnostic Guardrail Framework for AI Agent Safety and Security](https://arxiv.org/abs/2601.18491)** — Three-dimensional risk taxonomy (source/failure-mode/consequence) with fine-grained agentic safety benchmark (ATBench) and diagnostic guardrail models (4B–8B parameters) achieving 91.8% accuracy. Shifts safety monitoring from binary safe/unsafe checks to root-cause diagnosis: why did an action violate constraints? Where did the violation originate? What are the downstream consequences? Essential f
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2601.18491`</sub>
- **[When "Do Not" Is Not Deny: Security Rules in CLAUDE.md vs Built-In Controls](https://arxiv.org/abs/2608.23550)** — Analyzes 481 public CLAUDE.md files and finds only ~4% of natural-language security rules are backed by a matching built-in control, exposing the gap between documented intent and enforced permissions. A concrete reminder that harness instructions are not guardrails unless they map to deterministic enforcement
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2608.23550`</sub>

## Task Runners &amp; Orchestration

- **[AutoGen](https://github.com/microsoft/autogen)** — Microsoft's multi-agent conversation framework with a complete AgentChat layer covering agent loop, tool integration, termination conditions, and human-in-the-loop. The most comprehensive open-source reference for large-scale multi-agent harness design
  <sub>★ 60.8k · Python · CC-BY-4.0 · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "autogen-agentchat" "autogen-ext[openai]"`</sub>
- **[OmniRoute: Multi-Provider LLM Gateway](https://github.com/diegosouzapw/OmniRoute)** — Intelligent routing across multiple LLM providers with load balancing, intelligent fallbacks, rate limiting, and response caching. Achieves 40–60% token cost reduction through smart model routing (cheap models for simple tasks, capable models for complex reasoning). Essential infrastructure for harnesses operating under strict cost budgets where model selection is a per-turn decision
  <sub>★ 60.7k · TypeScript · MIT · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g omniroute`</sub>
- **[Orca](https://github.com/stablyai/orca)** — The AI orchestrator for running Codex, Claude Code, OpenCode, and Pi side-by-side in isolated git worktrees. It turns fleet-of-agents execution into a polished desktop IDE with a mobile companion, making parallel agent harness design accessible beyond shell-scripting teams
  <sub>★ 59.9k · TypeScript · MIT · brew · pushed 2026-09-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install --cask stablyai/orca/orca`</sub>
- **[CrewAI](https://github.com/crewAIInc/crewAI)** — Dual-layer harness orchestration: Crew handles autonomous agent delegation, Flow provides event-driven deterministic control (branching + shared Pydantic state). The clearest open-source example of mixing autonomous and scripted execution in the same harness
  <sub>★ 58k · Python · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add crewaiinc/skills`</sub>
- **[LiteLLM](https://github.com/BerriAI/litellm)** — Unified proxy and SDK that routes to 100+ LLM providers behind a single OpenAI-compatible interface, with a Router handling retry/fallback across deployments, per-project cost and rate-limit tracking, and OTEL callback integrations. The right infrastructure layer when your harness needs provider resilience (automatic failover on 429/500 errors), budget guardrails, or the ability to swap models wit
  <sub>★ 57.9k · Python · uv · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install 'litellm[proxy]'`</sub>
- **[LangGraph](https://github.com/langchain-ai/langgraph)** — Graph-based state machine framework for multi-agent harnesses: models supervisor/subagent topologies, error-recovery branches, and checkpoint persistence as first-class primitives. The most widely adopted harness orchestration layer in production
  <sub>★ 41k · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U langgraph`</sub>
- **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** — Lightweight multi-agent framework built around handoffs and guardrails; the production successor to Swarm. Complements LangGraph for harnesses where delegation patterns are simpler than full graph orchestration
  <sub>★ 29.2k · Python · MIT · pip · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openai-agents`</sub>
- **[Mastra](https://github.com/mastra-ai/mastra)** — TypeScript-native agent framework (from the Gatsby team) with 22K+ stars and 300K+ weekly npm downloads. Connects to 40+ providers through one standard interface, with built-in workflows, RAG pipelines, and agent orchestration. The @mastra/deployer handles serverless deployment, and the eval system supports LLM-as-judge out of the box. The strongest alternative to Vercel AI SDK for teams that need
  <sub>★ 27.7k · TypeScript · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mastra-ai/mastra.git`</sub>
- **[Symphony](https://github.com/openai/symphony)** — OpenAI's orchestration layer for moving from supervising coding agents to managing work: it monitors an issue tracker, creates isolated per-issue workspaces, and surfaces proof-of-work artifacts (CI status, review feedback, walkthrough videos) as the handoff signal. The spec deliberately leaves sandbox and approval policies implementation-defined so teams can match trust posture to environment, an
  <sub>★ 27k · Elixir · Apache-2.0 · source · pushed 2026-08-19 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/openai/symphony.git`</sub>
- **[Vercel AI SDK](https://github.com/vercel/ai)** — The leading TypeScript toolkit for building AI agents (20M+ monthly downloads, 25+ provider integrations). AI SDK 6 introduced a first-class Agent abstraction with ToolLoopAgent for production-ready tool execution loops, DevTools for local debugging, full MCP support, and type-safe UI streaming. The unified API across OpenAI, Anthropic, Google, and AWS Bedrock makes it the default choice for TypeS
  <sub>★ 26.6k · TypeScript · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vercel/ai.git`</sub>
- **[Google ADK](https://github.com/google/adk-python)** — Google's code-first agent framework with built-in multi-agent orchestration, tool registration, session state, and eval pipeline. Its Runner and AgentTool patterns are the reference implementation for wrapping sub-agents as tools in a larger harness
  <sub>★ 21.4k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install google-adk`</sub>
- **[Pydantic AI v2](https://github.com/pydantic/pydantic-ai)** — June 2026 harness-first redesign built around the Capability primitive: a single composable unit bundling instructions, tools, lifecycle hooks, and model settings. The split between a small stable core and a fast-moving pydantic-ai-harness lets capabilities graduate as they prove essential, while deferred loading keeps unused tools out of the context window
  <sub>★ 19.7k · Python · MIT · uv · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --with pydantic-ai-harness clai -a pydantic_ai_harness.coder:coder_agent -m anthropic:claude-fable-5`</sub>
- **[Hive](https://github.com/aden-hive/hive)** — YC-backed production harness that compiles multi-agent objectives into deterministic execution DAGs with state persistence, crash recovery, cost enforcement, and human-in-the-loop oversight. The most complete open-source reference for running agent workloads in production rather than demos
  <sub>★ 11k · Python · Apache-2.0 · clone · pushed 2026-08-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aden-hive/hive.git`</sub>
- **[Flue](https://github.com/withastro/flue)** — Astro's TypeScript-native agent harness that treats an agent as a function composed of model, sandbox, skills, tools, and MCP servers. The deploy-anywhere runtime (Node, Cloudflare Workers, GitHub Actions, Daytona) and first-class durability make it a practical reference for building autonomous agents rather than chatbots
  <sub>★ 8.1k · TypeScript · Apache-2.0 · source · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/withastro/flue.git`</sub>
- **[sandcastle](https://github.com/mattpocock/sandcastle)** — TypeScript-native orchestration for sandboxed coding agents that treats provider-agnostic isolation (Docker, Podman, or Vercel Firecracker microVMs) as a primitive, not a framework. The built-in review-pipeline and parallel-AFK-agent patterns demonstrate how lightweight harness layers can enforce safety without the complexity of full graph orchestration
  <sub>★ 7.8k · TypeScript · MIT · npx · pushed 2026-06-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @ai-hero/sandcastle init`</sub>
- **[strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk)** — AWS's open-source, model-driven agent SDK that treats the loop, tool binding, and guardrails as first-class primitives. Supports Bedrock, Anthropic, OpenAI, Gemini, and Ollama with native MCP, built-in observability, and multi-agent patterns — the missing AWS open-source harness framework alongside Bedrock AgentCore
  <sub>★ 7.1k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install strands-agents strands-agents-tools`</sub>
- **[OpenSquilla](https://github.com/opensquilla/opensquilla)** — Token-efficient microkernel agent with an on-device SquillaRouter that dispatches each turn to the cheapest capable model, a unified turn loop across CLI/Web/chat, and persistent memory with on-device embeddings. Demonstrates that harness-level routing and loop optimization — not just model scale — are the binding levers for intelligence density
  <sub>★ 6.9k · Python · Apache-2.0 · clone · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/opensquilla/opensquilla.git`</sub>
- **[open-multi-agent](https://github.com/open-multi-agent/open-multi-agent)** — TypeScript-native multi-agent orchestration that automatically decomposes a natural-language goal into a task DAG, parallelizes independent nodes, and synthesizes results. With only three runtime dependencies, built-in MCP support, token budgets, retries, and context compaction, it is the lightest production-grade harness layer for Node.js backends
  <sub>★ 6.9k · TypeScript · MIT · source · pushed 2026-09-03 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/JackChen-me/open-multi-agent.git`</sub>
- **[LoopX](https://github.com/huangruiteng/loopx)** — Provider-neutral control plane that sits above existing harnesses (Codex, Claude Code, Cursor) and keeps long-horizon objectives, gates, todos, evidence, and quota stable across bounded agent turns. The local-first state kernel makes multi-day work reviewable, restartable, and handoff-safe without replacing the runtime underneath
  <sub>★ 5.5k · Python · Apache-2.0 · clone · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/huangruiteng/loopx`</sub>
- **[AgentScope Java](https://github.com/agentscope-ai/agentscope-java)** — Production-ready Java framework for distributed, enterprise-grade agents with workspace sandboxing, permission-gated tool calls, AOP-style middleware, and cross-replica session recovery. The Java complement to AgentScope Runtime for teams that need a typed, JVM-native harness stack
  <sub>★ 5.4k · Java · source · pushed 2026-09-03</sub>
  <sub>`git clone https://github.com/agentscope-ai/agentscope-java.git`</sub>
- **[eve](https://github.com/vercel/eve)** — Vercel's filesystem-first framework for durable AI agents: instructions, typed tools, on-demand skills, message channels, and cron schedules live in conventional directories, making the harness inspectable and version-controlled by default. A concrete reference for treating the project filesystem as the agent authoring interface rather than burying configuration in framework internals
  <sub>★ 4.9k · TypeScript · Apache-2.0 · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx eve@latest init my-agent`</sub>
- **[Harmonist](https://github.com/GammaLabTechnologies/harmonist)** — Drop-in multi-agent framework where protocol enforcement is a mechanical gate, not a prompt request: IDE-level hooks check every code-changing turn for required reviewers, memory updates, and supply-chain integrity before the turn can complete. Built on stdlib Python with zero dependencies, it demonstrates how to build deterministic harness constraints that even frontier models cannot override
  <sub>★ 2.3k · Python · MIT · clone · pushed 2026-06-09 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/GammaLabTechnologies/harmonist.git`</sub>
- **[thClaws](https://github.com/thClaws/thClaws)** — Native-Rust agent harness platform with four surfaces (GUI, CLI, web, one-shot), multi-provider routing, and sovereign-by-design architecture. The most complete open-source reference for a locally-run, offline-capable harness that unifies MCP, skills, AGENTS.md, hooks, and session resumption in a single binary
  <sub>★ 1.2k · Rust · Apache-2.0 · clone · pushed 2026-08-29 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/thClaws/thClaws.git`</sub>
- **[Shopify Roast](https://github.com/Shopify/roast)** — Shopify's open-source Ruby DSL for structured AI workflows that interleaves deterministic steps (shell commands, Ruby code) with agentic steps via Claude Code or Pi. Its "non-determinism is the enemy of reliability" philosophy makes it a concrete reference for building reproducible, version-controlled harnesses where guardrails are structural rather than prompt-level
  <sub>★ 1.2k · Ruby · MIT · source · pushed 2026-08-10</sub>
  <sub>`git clone https://github.com/Shopify/roast.git`</sub>
- **[bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Deterministic scheduler for 40+ CLI coding agents running in parallel git worktrees with an HMAC-signed audit chain, signed agent cards, and per-artefact lineage. The zero-LLM coordination loop and tamper-evident audit trail make it the only open-source orchestrator designed for compliance-sensitive agent fleets
  <sub>★ 1.1k · Python · Apache-2.0 · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[AgentScope Runtime](https://github.com/agentscope-ai/agentscope-runtime)** — Production-ready open-source runtime focused on two pieces many agent frameworks leave underspecified: secure sandbox execution and durable agent serving. The "Agent as API" model, async sandbox types, and built-in state/sandbox lifecycle management make it one of the few 2026 projects tackling runtime concerns directly instead of stopping at orchestration abstractions
  <sub>★ 862 · Python · Apache-2.0 · pip · pushed 2026-06-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentscope-runtime`</sub>
- **[waggle](https://github.com/modiqo/waggle)** — Attributed, resolvable artifact references for agent handoffs: a ~30-byte token replaces pasted context, letting each consumer resolve only the projection or slice it needs under byte budgets while propagating corrections to every holder. The first concrete primitive that turns multi-agent handoffs from a context-copy problem into a reference-and-projection problem
  <sub>★ 668 · Rust · Apache-2.0 · cargo · pushed 2026-07-20 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install waggle-cli # from crates.io`</sub>
- **[HarnessRouter](https://github.com/HarnessRouter/harnessrouter)** — Self-hosted unified API for running Codex, Claude Code, DeepSeek Harness, Pi, and other terminal agents through the open Unified Harness Protocol (UHP), with sessions, streaming, file access, cancellation, and failure handling. Worth including because harness fragmentation is becoming a real operations problem — this is the clearest open-source attempt to make agent runtimes interchangeable behind
  <sub>★ 656 · Python · Apache-2.0 · docker · pushed 2026-09-03 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --name harnessrouter \`</sub>
- **[Conductor](https://github.com/microsoft/conductor)** — Microsoft’s open-source YAML-first CLI for deterministic multi-agent orchestration: Jinja2 routing, static parallel groups, and per-agent model overrides across Claude and Copilot with zero token overhead on the orchestration layer itself. Treats workflows as version-controlled, diffable infrastructure rather than runtime-discovered topology
  <sub>★ 416 · Python · MIT · psh · pushed 2026-09-02 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`irm https://aka.ms/conductor/install.ps1 | iex`</sub>
- **[Building a C Compiler with a Team of Parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)** — Anthropic's account of coordinating 16 Claude instances in parallel on a shared git repo without a central orchestrator: agents claim tasks via files in current_tasks/, git forces collision resolution naturally, and a continuous restart loop spawns fresh sessions that resume where predecessors left off. Key harness lesson: verbose test output pollutes agent context — the feedback loop must emit on
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/building-c-compiler`</sub>
- **[Codex SDK](https://developers.openai.com/codex/sdk)** — OpenAI's official SDK for programmatically controlling local Codex agents from TypeScript or Python: start threads, run prompts, resume sessions, and choose sandbox presets (read-only, workspace-write, full-access) so Codex can be wired into CI/CD or custom agent surfaces instead of remaining locked inside the CLI
  <sub>website</sub>
  <sub>`https://developers.openai.com/codex/sdk`</sub>
- **[Build Long-running AI agents that pause, resume, and never lose context with ADK](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/)** — Google's May 2026 guide to production agents that survive days-long idle periods: DatabaseSessionService for persistent sessions, webhook-triggered state_delta resumption that lets containers scale to zero, and explicit state machines instead of dumping raw JSON into vector databases. Complements Anthropic's managed-agents architecture with a cloud-native deployment perspective
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/`</sub>
- **[Scaling Managed Agents: Decoupling the Brain from the Hands](https://www.anthropic.com/engineering/managed-agents)** — Anthropic's production architecture for separating three stateless components — the "brain" (Claude + harness), "hands" (sandboxes/tools), and "session" (append-only event log) — enabling independent failure and replacement of each. Crash recovery via session replay (wake(sessionId) + getEvents()) and on-demand container provisioning cut p50 TTFT by ~60% and p95 by over 90%. The reference design f
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/managed-agents`</sub>
- **[Microsoft Agent Framework 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)** — Production-ready 1.0 release (April 2026) unifying Semantic Kernel and AutoGen into a single framework with graph-based orchestration, middleware pipeline for intercepting every execution stage, and declarative YAML agent definitions. DevUI provides a browser-based debugger for visualizing agent execution, message flows, and tool calls in real time. Multi-provider support (Azure OpenAI, Anthropic,
  <sub>website</sub>
  <sub>`https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/`</sub>
- **[Orchestrating Ambient Agents with Temporal](https://temporal.io/blog/orchestrating-ambient-agents-with-temporal)** — Temporal.io's harness infrastructure for persistent agent workflows with native agentic handshake protocol for secure deadline-aware calendar negotiation between autonomous agents. Brings distributed systems best practices (durability, retry semantics, activity monitoring) to agent orchestration, enabling agents to handle long-running tasks that outlast any single HTTP request or session
  <sub>website</sub>
  <sub>`https://temporal.io/blog/orchestrating-ambient-agents-with-temporal`</sub>
- **[The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)** — OpenAI's April 2026 update adding native sandbox execution, configurable memory, and sandbox-aware orchestration to the Agents SDK. The shift toward a "model-native harness" that aligns execution patterns with how frontier models actually perform best is a reference design for SDK-level harness evolution
  <sub>website</sub>
  <sub>`https://openai.com/index/the-next-evolution-of-the-agents-sdk/`</sub>

## Human-in-the-Loop

- **[AutoResearchClaw HITL Co-Pilot](https://github.com/aiming-lab/AutoResearchClaw)** — April 2026 open-source human-in-the-loop system with six intervention modes (full-auto, gate-only, checkpoint, step-by-step, co-pilot, custom), SmartPause confidence-driven dynamic suspension, and Intervention Learning from human corrections. The cost-guardrail system — aborting runs that exceed budget thresholds — makes it a practical reference for production HITL where human time is as constrain
  <sub>★ 14.3k · Python · MIT · clone · pushed 2026-08-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/aiming-lab/AutoResearchClaw.git`</sub>
- **[HITL Protocol](https://github.com/rotorstar/hitl-protocol)** — Open standard (v0.8, February 2026) for human decisions in agent workflows: HTTP 202 + review URL pattern connecting services, agents, and humans across any messaging channel. No SDK required — ~15 lines of code for agents, reference implementations in Express/Hono/Next.js/FastAPI for services, and 13 end-to-end flows including escalation and hybrid approval
  <sub>★ 11 · HTML · Apache-2.0 · source · pushed 2026-07-11 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/rotorstar/hitl-protocol.git`</sub>
- **[aws-samples/sample-human-in-the-loop-patterns](https://github.com/aws-samples/sample-human-in-the-loop-patterns)** — March 2026 AWS reference implementation demonstrating four distinct HITL patterns for sensitive agent tool calls: Hook System (centralized blanket policy), Tool Context (per-tool fine-grained), Step Functions (async third-party approval via SNS), and MCP Elicitation (protocol-native real-time interactive approval). The most concrete production guide for choosing the right HITL architecture based o
  <sub>★ 5 · Python · MIT-0 · source · pushed 2026-03-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aws-samples/sample-human-in-the-loop-patterns.git`</sub>
- **[Dify Human-in-the-Loop Node](https://github.com/langgenius/dify/discussions/32245)** — February 2026 release making human oversight a native workflow primitive: suspend execution at critical decision points, expose review-and-edit UI mid-flow, and route subsequent execution based on human action (approve/reject/escalate). Demonstrates how HITL transitions from bolt-on approval gates to first-class execution-graph nodes with stateful pause/resume backed by Celery workers and Redis Pu
  <sub>TypeScript · in-repo · pushed 2026-09-03</sub>
  <sub>`git clone https://github.com/langgenius/dify.git && cd dify/discussions/32245`</sub>
- **[LangGraph — Human-in-the-Loop Concepts](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)** — Systematic treatment of interrupt, breakpoint, and approve patterns: how to pause an agent mid-loop, persist state, and resume after human review. Directly addresses the harness engineering challenge of inserting human gates into long-running workflows
  <sub>website</sub>
  <sub>`https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/`</sub>
- **[AutoGen — Human-in-the-Loop](https://microsoft.github.io/autogen/0.2/docs/tutorial/human-in-the-loop/)** — Explains human_input_mode (NEVER / TERMINATE / ALWAYS) and the UserProxyAgent as an approval gate. The most concrete implementation reference for adding human review nodes to a multi-agent conversation harness
  <sub>website</sub>
  <sub>`https://microsoft.github.io/autogen/0.2/docs/tutorial/human-in-the-loop/`</sub>
- **[Claude Agent SDK — Handle Approvals and User Input](https://platform.claude.com/docs/en/agent-sdk/user-input)** — The most complete implementation reference for HITL mechanics: canUseTool callback pauses execution at every tool request with allow/deny/approve-with-changes/suggest-alternative response shapes; AskUserQuestion surfaces structured clarifications mid-task; streaming input enables mid-execution redirects. The "approve with changes" pattern — modifying tool input before execution — is the reference
  <sub>website</sub>
  <sub>`https://platform.claude.com/docs/en/agent-sdk/user-input`</sub>
- **[HiL-Bench: Do Agents Know When to Ask for Help?](https://arxiv.org/abs/2604.09408)** — April 2026 benchmark that transforms well-specified tasks into judgment challenges by injecting 3–5 realistic blockers (missing critical information) and giving agents an ask_human() tool. Agents from top models achieve ~90% pass@3 with full information but performance drops significantly when blockers are present — the first systematic measure of when agents should escalate to humans rather than
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2604.09408`</sub>
- **[Human Judgment in the Agent Improvement Loop](https://blog.langchain.com/human-judgment-in-the-agent-improvement-loop/)** — LangChain's April 9, 2026 guide closes an important gap that most HITL write-ups skip: human input is not just an approval gate at execution time, it's also supervision for improving prompts, tools, memory, and evaluators over time. Useful because it treats expert review as a structured data source for harness evolution rather than a one-off manual checkpoint
  <sub>website</sub>
  <sub>`https://blog.langchain.com/human-judgment-in-the-agent-improvement-loop/`</sub>
- **[Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)** — Martin Fowler defines three human-involvement postures — humans outside, in, or on the agent loop — and argues that "humans on the loop" (maintaining the harness rather than reviewing individual outputs) is the only approach that scales with agent throughput. The "agentic flywheel" section — where agents are directed to evaluate results and recommend harness improvements — is the clearest articula
  <sub>website</sub>
  <sub>`https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html`</sub>
- **[Measuring AI Agent Autonomy in Practice](https://www.anthropic.com/news/measuring-agent-autonomy)** — Anthropic's February 2026 empirical study of millions of real-world Claude Code interactions. Key finding: experienced users shift from per-action approval (20% auto-approve when new) to intervention-only oversight (40% auto-approve at 750+ sessions), and agent-initiated clarification stops grow faster than human interruptions as task complexity increases. The most data-grounded reference for desi
  <sub>website</sub>
  <sub>`https://www.anthropic.com/news/measuring-agent-autonomy`</sub>
- **[agent-chief](https://github.com/SmileLikeYe/agent-chief)** — Local-first attention orchestration layer that sits between you and every agent, alert, and feed: a three-stage worthiness engine decides whether to interrupt the human, dispatch work to an agent, or curate to memory. Worth including because it treats human attention as a scarce harness resource and turns the flood of agent-generated notifications into a structured, reviewable HITL decision rather
  <sub>unavailable</sub>

## Observability &amp; Tracing

- **[Langfuse](https://github.com/langfuse/langfuse)** — The most widely adopted self-hostable LLM observability platform: traces every agent step, manages prompt versions, and runs evals in one tool. Preferred over cloud-only alternatives when data residency or cost control is a constraint
  <sub>★ 34.2k · TypeScript · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langfuse openai`</sub>
- **[Opik](https://github.com/comet-ml/opik)** — Comet's open-source AI observability and evaluation platform: deep tracing of LLM calls, conversation logging, and agent activity, plus built-in eval metrics, prompt versioning, guardrails, and the Opik Agent Optimizer. Worth including because it unifies observability, verification, and optimization in one self-hostable stack rather than stitching together separate tools
  <sub>★ 21.8k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install opik`</sub>
- **[Arize Phoenix](https://github.com/Arize-ai/phoenix)** — Self-hostable trace UI and eval runtime for agent workflows. Lets harness engineers audit and replay every reasoning step and tool call offline, without sending data to a third-party cloud
  <sub>★ 11.3k · Python · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @arizeai/phoenix-cli setup`</sub>
- **[OpenLLMetry](https://github.com/traceloop/openllmetry)** — OpenTelemetry-based instrumentation for LLM calls and agent steps: adds trace spans to every inference and tool call without modifying business logic. The cleanest way to bring the existing OTEL ecosystem (Grafana, Datadog, Jaeger) to a harness
  <sub>★ 7.4k · Python · Apache-2.0 · pip · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install traceloop-sdk`</sub>
- **[Helicone](https://github.com/Helicone/helicone)** — Open-source LLM observability proxy (YC W23) with the largest open-source pricing database (300+ models). One-line proxy integration provides cost tracking, token monitoring, session tracing, and prompt versioning across providers. The AI Gateway component handles request routing and caching with zero-code changes. SOC 2 and GDPR compliant, self-hostable via Docker — the natural complement to exec
  <sub>★ 6.1k · TypeScript · Apache-2.0 · clone · pushed 2026-08-31 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Helicone/helicone.git`</sub>
- **[Pydantic Logfire](https://github.com/pydantic/logfire)** — AI observability platform from the Pydantic team with a unique angle: all trace data is SQL-queryable (PostgreSQL-compatible), so coding agents can query production observability data directly via the Logfire MCP server. Full-stack OTEL tracing covers both the AI layer and backend — letting you determine whether a failure is in agent logic or infrastructure. The natural observability choice for Py
  <sub>★ 4.5k · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install logfire`</sub>
- **[Future AGI](https://github.com/future-agi/future-agi)** — Open-source, self-hostable platform unifying tracing, evals, simulations, guardrails, and gateway into a single feedback loop. Worth including because it demonstrates what a unified observability-and-improvement plane looks like rather than stitching together five separate vendor tools
  <sub>★ 1.9k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install futureagi`</sub>
- **[Weights &amp; Biases Weave](https://github.com/wandb/weave)** — W&amp;B's tracing and eval layer purpose-built for agent workflows: automatic call graph capture, dataset versioning, and LLM-as-judge evals that integrate directly with the wandb experiment tracking ecosystem
  <sub>★ 1.1k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install weave`</sub>
- **[agentacct](https://github.com/mikehasa/agentacct)** — Local-first Agent Work Intelligence for coding agents: ingests existing Claude Code, Codex, and OpenCode session logs, attributes tokens and estimated cost to recorded work steps with confidence labels, and surfaces the evidence on a private dashboard with no cloud sync or API keys
  <sub>★ 692 · Python · MIT · uv · pushed 2026-09-03 · macOS</sub>
  <sub>`uv tool install agentacct`</sub>
- **[OTel GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)** — OpenTelemetry's standard attribute names for GenAI spans (gen_ai.system, gen_ai.request.model, etc.). The naming baseline that makes harness traces portable across any OTEL-compatible backend
  <sub>website</sub>
  <sub>`https://opentelemetry.io/docs/specs/semconv/gen-ai/`</sub>
- **[OpenObserve: Unified Observability for LLM Agents](https://openobserve.ai/)** — 2026-standard platform for LLM tracing with infrastructure log/metric unification. Enables harness engineers to correlate agent decisions with system-level events (network delays, GPU memory pressure) that explain agent failures, going beyond isolated LLM call traces
  <sub>website</sub>
  <sub>`https://openobserve.ai/`</sub>
- **[Braintrust](https://www.braintrust.dev)** — Evaluation-first agent observability platform ($80M Series B, Feb 2026) with exhaustive auto-tracing that captures every LLM call, tool invocation, and retrieval step as nested span hierarchies. Brainstore, its purpose-built data store, enables full-trace search without sampling — critical for debugging multi-turn agent failures where the root cause spans multiple steps. Used by Stripe, Notion, Dr
  <sub>website</sub>
  <sub>`https://www.braintrust.dev`</sub>
- **[Building Observable AI Agents: Temporal Now Integrates with Braintrust](https://temporal.io/blog/building-observable-ai-agents-temporal-now-integrates-with-braintrust)** — Combines Temporal's durable execution (automatic retries, state persistence, event history replay) with Braintrust's LLM tracing so every Workflow and Activity becomes a Braintrust span and every LLM call is traced with full context. Demonstrates the pattern with a deep research agent where failed synthesis steps retry without re-executing prior searches, and prompt updates propagate via braintrus
  <sub>website</sub>
  <sub>`https://temporal.io/blog/building-observable-ai-agents-temporal-now-integrates-with-braintrust`</sub>
- **[Introducing BigQuery Agent Analytics](https://cloud.google.com/blog/products/data-analytics/introducing-bigquery-agent-analytics/)** — Google Cloud's 2026 launch treats agent traces, tool calls, sessions, and outcomes as analytical data rather than dashboard exhaust. The important harness idea is that observability becomes queryable infrastructure: once telemetry lands in BigQuery, teams can build evaluators, regressions, and conversational debugging directly on top of production traces instead of maintaining a separate analysis
  <sub>website</sub>
  <sub>`https://cloud.google.com/blog/products/data-analytics/introducing-bigquery-agent-analytics/`</sub>
- **[Distributed Tracing for Agentic Workflows with OpenTelemetry](https://developers.redhat.com/articles/2026/04/06/distributed-tracing-agentic-workflows-opentelemetry)** — Red Hat's April 6, 2026 guide is one of the few concrete references that walks through context propagation across routing agents, specialist agents, MCP servers, and external systems using standard tracing infrastructure. It belongs here because it treats agent observability as a distributed-systems problem, which is exactly how these harnesses fail in production
  <sub>website</sub>
  <sub>`https://developers.redhat.com/articles/2026/04/06/distributed-tracing-agentic-workflows-opentelemetry`</sub>
- **[Red-Teaming Anthropic's Internal Agent Monitoring Systems — METR](https://metr.org/blog/2026-03-25-red-teaming-anthropic-agent-monitoring/)** — METR's three-week adversarial audit of Anthropic's internal agent monitoring and security systems (described in the Opus 4.6 Sabotage Risk Report). Discovered several novel vulnerabilities, some since patched. The most concrete published account of what it takes to stress-test agent monitoring infrastructure — essential reading before trusting any monitoring system as a safety layer
  <sub>website</sub>
  <sub>`https://metr.org/blog/2026-03-25-red-teaming-anthropic-agent-monitoring/`</sub>

## Verification &amp; CI Integration

- **[promptfoo](https://github.com/promptfoo/promptfoo)** — YAML-driven LLM testing framework with LLM-as-judge, assertion DSL, and native CI integration. The most practical tool for adding agent output regression tests to a PR pipeline without writing a test harness from scratch
  <sub>★ 24.8k · TypeScript · MIT · npm · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g promptfoo`</sub>
- **[AgentBench](https://github.com/THUDM/AgentBench)** — Multi-environment agent benchmark (OS, DB, web, code) with a structured eval pipeline. Worth studying for its environment isolation design and task definition format when building custom eval environments for your harness
  <sub>★ 3.7k · Python · Apache-2.0 · source · pushed 2026-02-08 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/THUDM/AgentBench.git`</sub>
- **[sentrux](https://github.com/sentrux/sentrux)** — Real-time architectural sensor that closes the feedback loop for coding agents: scans codebases, scores structural health, and surfaces degradation via MCP so agents can self-correct before entropy compounds. The gate --save / gate pair makes architectural regression detection CI-friendly — filling the verification gap between linters (style) and tests (behavior) for code produced by autonomous ha
  <sub>★ 3.2k · Rust · MIT · brew · pushed 2026-03-19 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install sentrux/tap/sentrux`</sub>
- **[mcp-test-harness](https://github.com/vaquarkhan/mcp-test-harness)** — Pytest-style testing framework for MCP servers with protocol-aware assertions, snapshot tests, and CI-ready reports across stdio/SSE/HTTP transports. Fills the gap between shipping an MCP server and trusting it in production by turning tool/schema regressions into ordinary test failures
  <sub>★ 6 · Python · MIT · pip · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install mcp-test-harness`</sub>
- **[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)** — OpenAI's framework for skill regression testing: four eval dimensions (outcome, process, style, efficiency goals), JSONL trace capture for deterministic checks (command sequences, token budgets, repo cleanliness), then rubric-based grading only where deterministic checks don't suffice. The layering principle — add expensive LLM-as-judge checks only where they reduce meaningful risk — is the most a
  <sub>website</sub>
  <sub>`https://developers.openai.com/blog/eval-skills`</sub>
- **[Agent Evaluation Readiness Checklist](https://blog.langchain.com/agent-evaluation-readiness-checklist/)** — A 33-item checklist covering the full evaluation lifecycle: error taxonomy, three-level granularity (single-step → trace → multi-turn thread), grader specialization, and CI integration. Key insight: capability evals (low pass rate, improvement target) and regression evals (near-100%, protection target) must be separated — mixing them produces wrong prioritization decisions
  <sub>website</sub>
  <sub>`https://blog.langchain.com/agent-evaluation-readiness-checklist/`</sub>
- **[Evaluating Skills](https://blog.langchain.com/evaluating-skills/)** — LangChain's methodology for benchmarking agent skills in Docker-sandboxed environments. Key empirical findings: Claude Code achieved 82% task completion with curated skills vs. 9% without, and consolidating to ≤12 skills improved accuracy over sprawling skill sets. The baseline-vs-skills comparison design with bugfix tasks and clear outcome metrics is the template for systematic skill coverage tes
  <sub>website</sub>
  <sub>`https://blog.langchain.com/evaluating-skills/`</sub>
- **[Eval-Driven Development: Build and Evaluate Reliable AI Agents](https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents)** — Red Hat's eight-stage evaluation maturity progression from manual CLI testing to cost-aware continuous monitoring (March 2026). Uses DeepEval with 15 custom ConversationalGEval metrics and LLM-as-judge; key finding: evaluator model capability matters significantly — llama-3-3-70b caught all known failures while smaller models missed 4–5 cases. The $0.64/run cost estimate and self-hosted evaluator
  <sub>website</sub>
  <sub>`https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents`</sub>
- **[Agent Evaluation Framework 2026: Metrics, Rubrics &amp; Benchmarks](https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks)** — Comprehensive framework combining multi-environment baselines (AgentBench), domain-specific benchmarks (Terminal Bench 2.0, WebArena, SWE-bench Verified), and industry standards (NIST AI Agent Standards Initiative, February 2026). Provides reference metrics and rubrics for evaluating coding agents, chatbots, and specialized agents across dimensions (correctness, efficiency, safety). Essential for
  <sub>website</sub>
  <sub>`https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks`</sub>
- **[Driving the Agent Quality Flywheel from Your Coding Agent](https://developers.googleblog.com/en/driving-the-agent-quality-flywheel-from-your-coding-agent/)** — Google's June 2026 account of automating the eval-optimize loop for coding agents: independent AutoRaters grade agent outputs so the optimizer cannot game its own metrics, and custom rubrics isolate specific behaviors like stale-message echoing that blended scores miss. Shows how to close the verification loop continuously against both synthetic dev scenarios and production traces
  <sub>website</sub>
  <sub>`https://developers.googleblog.com/en/driving-the-agent-quality-flywheel-from-your-coding-agent/`</sub>

## Evals &amp; Verification

- **[DeepEval](https://github.com/confident-ai/deepeval)** — The most complete open-source LLM/agent eval framework: 20+ built-in metrics (hallucination, answer relevancy, RAGAs, tool correctness), pytest integration, and a CI-friendly runner. Removes the need to hand-roll eval infrastructure when you need structured, repeatable agent quality gates
  <sub>★ 18.1k · Python · Apache-2.0 · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U deepeval`</sub>
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — UK AI Security Institute's eval framework with native support for evaluating external agents (Claude Code, Codex CLI) as black-box targets, plus built-in bash/python/web browsing tools. Built for safety-grade rigor; the right foundation for harness-level eval infrastructure
  <sub>★ 2.7k · Python · MIT · clone · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/UKGovernmentBEIS/inspect_ai.git`</sub>
- **[tau-bench](https://github.com/sierra-research/tau-bench)** — Benchmarks agent behavior in three-way user-tool-policy interactions — the failure mode SWE-bench doesn't cover. Useful for validating that a harness correctly enforces business rules across multi-turn, stateful conversations
  <sub>★ 1.4k · Python · MIT · clone · pushed 2026-03-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sierra-research/tau-bench`</sub>
- **[Accio-org/RealReplicaBench](https://github.com/Accio-org/CommerceAgentBench)** — Alibaba International's benchmark for long-horizon agents in high-fidelity, stateful replicas of real online services: 107 tasks spanning CLI, browser, file, and API/MCP workflows, each graded by deterministic or LLM-assisted verifiers in a fresh container. The reproducibility contract — mock services, auditable trajectories, and container metadata — makes it the right eval harness for agents that
  <sub>★ 1.2k · HTML · Apache-2.0 · source · pushed 2026-08-29 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Accio-org/RealReplicaBench.git`</sub>
- **[Claw-Eval](https://github.com/claw-eval/claw-eval)** — 300 human-verified tasks across 9 categories evaluating LLM-as-agent performance on completion, safety, and robustness with a Pass^3 methodology that requires success across three independent trials. Referenced by Meta, Kimi, Qwen, and Tencent as a trustworthy benchmark for general agentic capabilities — the most rigorous community-verified eval harness published in 2026
  <sub>★ 763 · Python · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/claw-eval/claw-eval.git`</sub>
- **[STATE-Bench](https://github.com/microsoft/STATE-Bench)** — Microsoft's open-source benchmark (May 2026) measuring whether agents actually improve with experience on 450 realistic enterprise tasks across customer support, travel, and shopping. The first eval to treat memory as an independent variable with explicit learning tracks, providing a concrete way to compare memory architectures beyond simple recall metrics
  <sub>★ 85 · Python · MIT · source · pushed 2026-08-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/STATE-Bench.git`</sub>
- **[SWE-bench](https://www.swebench.com)** — The canonical benchmark for coding agents. Essential reference for understanding what "verified working" means for harness outputs
  <sub>website</sub>
  <sub>`https://www.swebench.com`</sub>
- **[Quantifying Infrastructure Noise in Agentic Coding Evals](https://www.anthropic.com/engineering/infrastructure-noise)** — Anthropic's empirical study showing container resource configuration alone produces 6+ percentage point benchmark swings — often exceeding model-to-model gaps. The 3x threshold finding is the key practical result: scores are stable up to 3x specified resources, but above that agents shift strategy entirely (lean tools vs. heavy dependencies), meaning tight and generous resource limits measure fund
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/infrastructure-noise`</sub>
- **[AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation](https://arxiv.org/abs/2605.12925)** — Process-level evaluation framework that separates solid solutions from "lucky passes" (regression cycles, blind retries, missing verification) in SWE agent trajectories. Analyzing 2,614 OpenHands trajectories shows up to 23.2% of passes are lucky and model rankings shift by as many as five positions when scored by process quality rather than binary pass/fail — a direct argument for building verifi
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2605.12925`</sub>
- **[StaminaBench: Stress-Testing Coding Agents over 100 Interaction Turns](https://arxiv.org/abs/2606.19613)** — Amazon Science's black-box benchmark for measuring how many consecutive change-request turns a coding agent can sustain before failing. The core finding — test feedback and retry capability improve pass counts by up to 12×, while stronger models show a 6× gap between their best and worst harness — makes long-horizon stamina an explicit eval target rather than an afterthought
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.19613`</sub>
- **[Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666)** — Proposes twelve concrete reliability metrics across four dimensions (consistency, robustness, predictability, safety), evaluated against 14 agentic models. The central finding — that recent capability gains yield only modest reliability improvements — is the empirical case for investing in harness-layer reliability engineering as a discipline distinct from model selection
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.16666`</sub>
- **[VeRO: An Evaluation Harness for Agents to Optimize Agents](https://arxiv.org/abs/2602.22480)** — Framework for evaluating agent-on-agent optimization cycles: a coding agent iteratively modifies a target agent's harness (prompts, tools, configuration) through edit-execute-evaluate loops while VeRO captures versioned agent snapshots, budget-controlled evaluation, and structured execution traces. Addresses the meta-evaluation gap — how to systematically measure whether one agent is improving ano
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.22480`</sub>
- **[Eval Awareness in Claude Opus 4.6's BrowseComp Performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp)** — Anthropic's documented case of Claude Opus 4.6 inferring it was under evaluation, identifying the benchmark by name, and decrypting the answer key — producing 11 non-intended solutions. A direct challenge to eval harness design: any eval that runs in a web-enabled environment is vulnerable to the agent researching the benchmark itself. The practical countermeasure — evaluate in network-isolated en
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/eval-awareness-browsecomp`</sub>
- **[Designing AI-Resistant Technical Evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations)** — Anthropic's January 21, 2026 write-up is the clearest account of a problem eval builders now have to treat as first-class: capable models can invalidate the test itself. The practical value is the redesign methodology — shift toward longer-horizon, tool-building, environment-understanding tasks that remain discriminative even as frontier models get better at short take-homes
  <sub>website</sub>
  <sub>`https://www.anthropic.com/engineering/AI-resistant-technical-evaluations`</sub>
- **[Amazon Bedrock AgentCore Evaluations Is Now Generally Available](https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available/)** — AWS's March 31, 2026 GA launch matters because it operationalizes agent evals as an infrastructure service: trajectory scoring, task completion checks, and model-graded assessments are wired into the same platform that hosts agents. Worth adding because it shows how evaluation stops being an offline benchmark and becomes part of the runtime control plane teams can standardize on
  <sub>website</sub>
  <sub>`https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available/`</sub>

## Debugging &amp; Developer Experience

- **[AgentOps](https://github.com/AgentOps-AI/agentops)** — Open-source agent engineering platform (YC W24) with session replay, cost tracking, and failure detection across 10+ frameworks including CrewAI, LangGraph, and OpenAI Agents SDK. The step-by-step execution graph and cross-session metrics make it the most practical debugging layer for multi-agent systems in production
  <sub>★ 5.8k · Python · MIT · pip · pushed 2026-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentops`</sub>
- **[claude-devtools](https://github.com/matt1398/claude-devtools)** — February 2026 open-source DevTools for Claude Code that reconstructs hidden session internals from local logs: per-turn token attribution across 7 context categories, full subagent execution trees with cost breakdowns, and syntax-highlighted diffs for every tool call. Essential because Claude Code's default UI deliberately collapses tool details and thinking steps — this tool restores the visibili
  <sub>★ 3.9k · TypeScript · MIT · brew · pushed 2026-05-13 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install --cask claude-devtools`</sub>
- **[Better Harness](https://github.com/QoderAI/better-harness)** — Evaluates coding-agent workflows across five dimensions and turns project and session evidence into prioritized, evidence-bounded findings with scoped repair actions. Runs inside Claude Code, Codex, Cursor, GitHub Copilot, and other hosts, making it a practical cross-tool diagnostic layer for improving the harness rather than just reviewing the final diff
  <sub>★ 2.1k · JavaScript · MIT · clone · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/QoderAI/better-harness.git`</sub>
- **[mindwalk](https://github.com/cosmtrek/mindwalk)** — Replays Claude Code and Codex sessions on a 3D map of your codebase, turning raw JSONL logs into a spatial view of where the agent searched, read, and edited. The glow-based visualization makes exploration drift and context pressure immediately visible — a concrete debugging primitive for reviewing whether an agent's footprint matched the intended task scope
  <sub>★ 1.3k · Go · MIT · script · pushed 2026-08-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/cosmtrek/mindwalk/master/scripts/install.sh | sh`</sub>
- **[AgentPrism](https://github.com/evilmartians/agent-prism)** — Open-source React component library (Evil Martians) that transforms OpenTelemetry trace data into interactive visualizations: tree view, timeline/Gantt view, sequence diagrams, and detail panels. Framework-agnostic — works with any OTEL-compatible agent. Fills the gap between raw OTEL spans and human-comprehensible agent debugging UIs
  <sub>★ 387 · TypeScript · MIT · npx · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx degit evilmartians/agent-prism/packages/ui/src/components src/components/agent-prism`</sub>
- **[mcpsnoop](https://github.com/kerlenton/mcpsnoop)** — Wireshark for MCP: a transparent proxy that shows every JSON-RPC frame between your real client and MCP servers, live in your terminal. Worth including because MCP Inspector tests servers from its own client, so it can't see the calls your actual agent makes, misses, or hangs on — mcpsnoop sits in the real data path and makes those failures visible
  <sub>★ 347 · Go · MIT · npm · pushed 2026-08-26 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g mcpsnoop`</sub>
- **[Syncause/debug-skill](https://github.com/Syncause/debug-skill)** — April 2026 agent debugging skill that stops guesswork with runtime evidence. Uses background tracing (Runtime Facts) to capture the exact execution path leading to failures, then constrains the agent to cite specific data points (stack traces, variable snapshots) before proposing fixes. Moves agent debugging from "patch and pray" to evidence-based repair with reviewable results
  <sub>★ 20 · npx · pushed 2026-04-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add Syncause/debug-skill`</sub>
- **[Claude Code /doctor](https://code.claude.com/docs/en/commands)** — Anthropic's July 2026 bundled setup-checkup skill (alias /checkup) that audits harness hygiene: it deduplicates local and checked-in CLAUDE.md files, flags unused skills/MCP servers/plugins, identifies slow hooks, and proposes fixes only after confirmation. The clearest first-party example of treating harness configuration drift — not model output — as the debugging target
  <sub>website</sub>
  <sub>`https://code.claude.com/docs/en/commands`</sub>
- **[AgentTrace: Causal Graph Tracing for Root Cause Analysis in Multi-Agent Systems](https://arxiv.org/abs/2603.14688)** — March 2026 framework that localizes root causes in multi-agent execution traces using causal graph analysis rather than LLM inference. Processes traces in 0.12 seconds (69× faster than LLM-based analysis) with 93.6–95.8% accuracy across 550 synthetic failure scenarios. Distinguishes root causes from downstream symptom propagation — the key capability missing from most trace-inspection debugging wo
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.14688`</sub>
- **[AgentRx: Systematic Debugging for AI Agents](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/)** — Framework for automated root-cause analysis of agent failures: trajectory normalization, constraint synthesis from tool schemas, and constraint-guided evaluation. Achieves 23.6% better failure localization than existing approaches with a 115-trajectory annotated benchmark. Shifts agent debugging from manual log inspection to systematic constraint-based diagnosis — a reference design for harness-le
  <sub>website</sub>
  <sub>`https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/`</sub>
- **[Debugging Deep Agents with LangSmith](https://blog.langchain.com/debugging-deep-agents-with-langsmith/)** — Addresses the core problem of debugging agents that run for minutes, span hundreds of steps, and produce massive traces no human can manually scan. Introduces Polly (an AI assistant that analyzes traces to surface root causes) and langsmith-fetch (CLI for piping trace data to coding agents). Key insight: debugging deep agents requires AI-assisted trace analysis — the volume of data these systems p
  <sub>website</sub>
  <sub>`https://blog.langchain.com/debugging-deep-agents-with-langsmith/`</sub>
- **[Where LLM Agents Fail and How They Can Learn From Failures (AgentDebug)](https://arxiv.org/abs/2509.25370)** — ICLR 2026 paper introducing the Agent Error Taxonomy — a modular classification covering memory, reflection, planning, action, and system-level failures. The AgentDebug framework isolates root-cause failures and provides corrective feedback, achieving +24% higher all-correct accuracy. The Agent Error Benchmark (annotated trajectories from ALFWorld, GAIA, WebShop) is the first systematic failure da
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2509.25370`</sub>
- **[Characterizing Faults in Agentic AI](https://arxiv.org/abs/2603.06847)** — March 2026 empirical study mining 375 GitHub issues across real-world agent systems (AutoGen, CrewAI, OpenAI Agents SDK, LangChain, CAMEL, DB-GPT) to build the first grounded taxonomy of agent-specific faults: initialization failures, role deviation, memory/state deficiencies, orchestration failures, and tool integration errors. Provides architecture-level fault classification that harness enginee
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.06847`</sub>
- **[More Visibility into Copilot Coding Agent Sessions](https://github.blog/changelog/2026-03-19-more-visibility-into-copilot-coding-agent-sessions/)** — GitHub's March 19, 2026 changelog is short but materially useful: setup-step logs, collapsed subagent traces, and clearer session-stage visibility are exactly the kind of DX improvements that make long-running agent failures debuggable in practice. It is a concrete reminder that trace readability is part of the harness, not an afterthought layered on top
  <sub>website</sub>
  <sub>`https://github.blog/changelog/2026-03-19-more-visibility-into-copilot-coding-agent-sessions/`</sub>
- **[AgentStepper: Interactive Debugging of Software Development Agents](https://arxiv.org/abs/2602.06593)** — February 2026 interactive debugger for agent execution trajectories that organizes raw logs into structured, side-by-side conversations (agent↔LLM and agent↔tools). Enables step-through execution, breakpoint manipulation, and mid-trajectory inspection. Developer study shows frustration scores drop from 5.4 to 2.4 (NASA TLX) and comprehension accuracy improves significantly — the first concrete evi
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.06593`</sub>

## Generators &amp; Meta-Harnesses

- **[everything-claude-code](https://github.com/affaan-m/ECC)** — Anthropic Hackathon Winner (140K+ stars). The agent harness performance optimization system: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development. Production-ready agents, skills, hooks, rules, and MCP configurations evolved over 10+ months of intensive daily use building real products. Works across Claude Code, Codex, Cursor, OpenCode, and
  <sub>★ 246.8k · JavaScript · MIT · clone · pushed 2026-09-03 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/affaan-m/ECC.git`</sub>
- **[ECC](https://github.com/affaan-m/ECC)** — Affaan Momin's agent-harness operating system: 68 specialized agents, 286 skills, hooks, memory, continuous learning, and AgentShield security scanning across Claude Code, Codex, Cursor, OpenCode, and other harnesses. The clearest open-source example of packaging an end-to-end engineering workflow — plan, test, implement, review, verify, remember, improve — as installable harness infrastructure
  <sub>★ 246.8k · JavaScript · MIT · npm · pushed 2026-09-03 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npm install -g ecc-universal`</sub>
- **[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)** — Claude Code plugin that externalizes multi-agent orchestration as installable skills and staged team pipelines, with cross-provider advisor routing and built-in requirement-clarification interviews. The most widely adopted example of turning a single-agent CLI into a team-ready meta-harness without rewriting the underlying loop
  <sub>★ 39k · TypeScript · MIT · source · pushed 2026-09-03 · WSL2 · macOS? · Linux</sub>
  <sub>`git clone https://github.com/Yeachan-Heo/oh-my-claudecode.git`</sub>
- **[Omnigent](https://github.com/omnigent-ai/omnigent)** — Databricks' open-source meta-harness (June 2026) that sits above Claude Code, Codex, Pi, and custom agents to compose, govern, and share live agent sessions from one control plane. The key harness insight is that enterprises don't need another agent framework — they need a portability and governance layer above the agents they already run, with policy-driven sandboxing and cost caps enforced outsi
  <sub>★ 9.6k · Python · Apache-2.0 · uv · pushed 2026-09-02 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`uv tool install omnigent # or: pip install "omnigent"`</sub>
- **[revfactory/harness](https://github.com/revfactory/harness)** — A meta-skill that generates domain-specific agent teams and the skills they use. Good example of harness-as-code, where the harness itself is produced by an agent
  <sub>★ 8.9k · HTML · Apache-2.0 · source · pushed 2026-07-24</sub>
  <sub>`git clone https://github.com/revfactory/harness.git`</sub>
- **[Nexent](https://github.com/ModelEngine-Group/nexent)** — Zero-code platform for auto-generating production-grade AI agents using Harness Engineering principles: unified tools, skills, memory, and orchestration with built-in constraints, feedback loops, and control planes. The clearest open-source example of turning harness scaffolding from a hand-rolled craft into a declarative, production-ready system
  <sub>★ 5.8k · Python · MIT · clone · pushed 2026-09-03 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/ModelEngine-Group/nexent.git`</sub>
- **[AutoAgent](https://github.com/thirdlayerinc/autoagent)** — Open-source library (April 2026) that automates the harness engineering loop itself: give it a task and a benchmark, and it iterates overnight on system prompts, tool configurations, agent orchestration, and routing — keeping or discarding each change based on score. In a 24-hour run, hit #1 on SpreadsheetBench (96.5%) and the top GPT-5 score on TerminalBench (55.1%), beating every hand-engineered
  <sub>★ 4.6k · Python · source · pushed 2026-04-03 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/kevinrgu/autoagent.git`</sub>
- **[stanford-iris-lab/meta-harness](https://github.com/stanford-iris-lab/meta-harness)** — April 2026 official implementation of the Meta-Harness paper from Stanford's IRIS Lab. Provides the framework and two reference experiments for end-to-end harness optimization via filesystem-backed search loops where a coding agent proposes, evaluates, and refines harness artifacts. The cleaned-up codebase is the definitive starting point for researchers reproducing or extending meta-harness optim
  <sub>★ 1.5k · Python · MIT · source · pushed 2026-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/stanford-iris-lab/meta-harness.git`</sub>
- **[autocontext](https://github.com/greyhaven-ai/autocontext)** — Recursive self-improving harness that runs multi-generation evaluation loops, distilling successful strategies into persistent playbooks and trace datasets that future agents inherit. The five-role architecture (competitor, analyst, coach, architect, curator) and built-in production trace capture make it the most complete open-source reference for turning meta-harness optimization into a deployabl
  <sub>★ 1.3k · Python · Apache-2.0 · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install autocontext==0.17.0`</sub>
- **[Exo](https://github.com/exoharness/exo)** — A systems approach to recursive self-improvement: a full agent harness that can safely edit its own prompts, memory, tools, and policy because an immutable event log is the one thing it cannot rewrite. The clearest open-source architecture for long-lived agents that evolve their own scaffolding without getting lost in recursive loops
  <sub>★ 1.2k · Rust · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/exoharness/exo.git`</sub>
- **[agentic-harness-engineering](https://github.com/china-qijizhifeng/agentic-harness-engineering)** — Observability-driven automatic evolution of coding-agent harnesses that decomposes the scaffold into seven orthogonal, git-tracked components and iteratively improves them through trace distillation and evidence-backed edits. Ranked #3 on Terminal-Bench 2.0 (84.7%) with demonstrated cross-model transfer, showing that evolved harness components generalize beyond benchmark-specific tuning
  <sub>★ 868 · Python · MIT · clone · pushed 2026-08-03 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/Curry09/agentic-harness-engineering.git`</sub>
- **[ruvnet/metaharness](https://github.com/ruvnet/metaharness)** — Scaffold factory that turns any repo into a branded agent harness with its own npx CLI, MCP server, scoped memory, governance policy, and Darwin Mode self-evolution. The clearest open-source embodiment of "the model is replaceable, the harness is the product" — it generates the owned scaffolding rather than prescribing a fixed framework
  <sub>★ 627 · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx metaharness my-bot --template vertical:coding --host claude-code`</sub>
- **[neosigmaai/auto-harness](https://github.com/neosigmaai/auto-harness)** — April 2026 open-source self-improving agentic system: bring your own coding agent, automatically mine failures from benchmark runs, optimize the harness through iterative edits, and gate changes against regressions. Supports Terminal-Bench 2.0 and tau-bench with Harbor and Docker evaluation backends. The PROGRAM.md pattern — human writes the optimization directive, agent executes the harness engin
  <sub>★ 536 · Python · MIT · clone · pushed 2026-07-08 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/neosigmaai/auto-harness`</sub>
- **[Continual Harness](https://github.com/sethkarten/continual-harness)** — Reset-free framework that lets an LLM Refiner rewrite its own system prompt, sub-agents, skills, and memory mid-episode via an evolve_harness tool. The first open-source implementation of online harness self-improvement with reproducible long-horizon benchmarks (Gemini Plays Pokémon)
  <sub>★ 302 · Python · MIT · clone · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sethkarten/continual-harness`</sub>
- **[metaharness](https://github.com/SuperagenticAI/metaharness)** — Open-source Python library (April 2026) that implements an outer optimization loop around executable harnesses for coding agents. Inspired by the Meta-Harness paper, it treats AGENTS.md, setup scripts, validation logic, and test flows as optimizable artifacts rather than static configs — with filesystem-backed run stores, environment snapshots, and scoped write enforcement. The most practical refe
  <sub>★ 160 · Python · uv · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install superagentic-metaharness`</sub>
- **[meta-agent](https://github.com/canvas-org/meta-agent)** — Lightweight continual harness optimizer (April 2026) built on the Claude Agent SDK. Runs an outer loop that reads task traces, rewrites harness configs, and re-evaluates — achieving 67% → 87% on tau-bench with no labeled training data. Demonstrates that even small, focused meta-harness loops can yield large reliability gains when harness configs are treated as learnable parameters
  <sub>★ 70 · Python · MIT · clone · pushed 2026-08-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/canvas-org/meta-agent.git`</sub>
- **[retro-harness](https://github.com/wbopan/retro-harness)** — Official implementation of RHO (Retrospective Harness Optimization): improves an agent's harness using only its own past trajectories, via self-validation, self-consistency, and pairwise self-preference — no ground-truth labels or external evaluators required. A single round moves SWE-Bench Pro from 59% to 78%, showing that harness evolution can be fully self-supervised rather than dependent on la
  <sub>★ 54 · Python · MIT · clone · pushed 2026-06-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/wbopan/retro-harness.git`</sub>
- **[raphaelchristi/harness-evolver](https://github.com/raphaelchristi/harness-evolver)** — March 2026 Claude Code plugin that autonomously evolves LLM agent harnesses using multi-agent proposers in isolated git worktrees, LangSmith-backed evaluation, and regression guards. Iterates on prompts, routing, retrieval, and orchestration code based on full-trace counterfactual diagnosis. The most practical published implementation of the Meta-Harness outer-loop optimization paradigm
  <sub>★ 49 · Python · MIT · npx · pushed 2026-04-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx harness-evolver@latest`</sub>
- **[Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)** — Anthropic's official SDK that exposes Claude Code's entire harness as a programmable API: built-in tool execution loop, PreToolUse/PostToolUse hooks for interception, subagent definitions, allowedTools permission control, and session resumption. The highest-leverage starting point for building a production harness — you inherit the entire tool execution layer rather than implementing it
  <sub>website</sub>
  <sub>`https://platform.claude.com/docs/en/agent-sdk/overview`</sub>
- **[Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052)** — Treats the entire harness (system prompt, tool definitions, context management, completion logic) as a joint optimization target rather than hand-tuning each piece. The key insight: give the proposer agent filesystem access to all prior harness candidates, scores, and execution traces — 10M-token diagnostic context vs. the 26K in prior work — so it can trace failures back to specific harness decis
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.28052`</sub>
- **[Self-Harness: Harnesses That Improve Themselves](https://arxiv.org/abs/2606.09498)** — June 2026 proposal for a self-improving harness loop: the agent mines its own failure traces, proposes minimal harness edits, and validates them through regression testing. Improves Terminal-Bench-2.0 pass rates by 20+ percentage points across MiniMax, Qwen, and GLM without requiring stronger external agents, showing that model-specific harness tuning can be automated rather than hand-engineered
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.09498`</sub>
- **[HyperAgents: Self-Improving AI Systems](https://pooya.blog/blog/hyperagents-self-improving-ai-meta-research-2026/)** — Meta's framework integrating task-solving and meta-level improvement into a unified, editable program with metacognitive self-modification. Improved paper-review tasks from 0.0 to 0.710, transferred to Olympiad math grading at 0.630 improvement@50 score. Shows how agents can be designed to modify their own harness (prompts, tools, strategy) based on execution history — the ultimate meta-harness wh
  <sub>website</sub>
  <sub>`https://pooya.blog/blog/hyperagents-self-improving-ai-meta-research-2026/`</sub>

## Demo Harnesses

- **[OpenCode](https://github.com/anomalyco/opencode)** — Open-source terminal-native AI coding agent with 131K+ stars and 2.5M+ monthly active developers. Provider-agnostic architecture supports 75+ LLM providers plus native LSP auto-configuration, multi-session parallel agents, and MCP extensibility. The build/plan agent split and client/server architecture make it the most complete open-source reference for a terminal-first coding harness
  <sub>★ 203.5k · TypeScript · MIT · scoop · pushed 2026-09-03 · macOS · Linux</sub>
  <sub>`scoop install opencode # Windows`</sub>
- **[Codex CLI](https://github.com/openai/codex)** — OpenAI's official autonomous coding agent CLI — the open-source reference implementation of the Codex harness with sandboxed tool execution, multi-file editing, and a streaming agent loop. Worth studying because it is the most widely adopted terminal-native coding agent harness and exposes the same loop architecture that OpenAI documents in its harness engineering posts
  <sub>★ 121.2k · Rust · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @openai/codex`</sub>
- **[browser-use](https://github.com/browser-use/browser-use)** — Minimal browser-automation agent harness with clean separation of tool registration, DOM state injection, action loop, and error recovery. Small codebase, clear structure — the best "minimal viable harness" reference for understanding core loop mechanics
  <sub>★ 112.2k · Python · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browser-use/browser-use.git`</sub>
- **[Pi](https://github.com/earendil-works/pi)** — Minimal terminal coding harness built around "lazy skills": each capability keeps only a one-line description in active context, loading full instructions and tool schemas only when invoked. Keeps the system prompt under 1,000 tokens versus 7,000–10,000 for typical agents, making it a concrete reference for context-minimal harness design
  <sub>★ 101.4k · TypeScript · MIT · source · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/earendil-works/pi.git`</sub>
- **[OpenHands](https://github.com/OpenHands/OpenHands)** — The most architecturally complete open-source coding agent: Runtime/Sandbox isolation, EventStream message bus, and Agent Controller are a three-layer harness design worth studying for production deployments
  <sub>★ 86k · TypeScript · MIT · npm · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[DeerFlow](https://github.com/bytedance/deer-flow)** — ByteDance's open-source SuperAgent harness built on LangGraph: orchestrates sub-agents with isolated contexts, persistent multi-tier memory, Docker/K8s sandbox execution, and on-demand skill loading for long-horizon tasks that span minutes to hours. A concrete reference for composing supervisor coordination, scoped delegation, and real execution environments into a single deployable harness
  <sub>★ 81.3k · Python · MIT · npx · pushed 2026-09-03 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add https://github.com/bytedance/deer-flow --skill claude-to-deerflow`</sub>
- **[Goose](https://github.com/aaif-goose/goose)** — Block's open-source, extensible AI agent donated to the Linux Foundation's Agentic AI Foundation in April 2026. Its MCP-native architecture treats every capability as an MCP server, making it a practical reference for building vendor-neutral, extensible harnesses where tool integration is the primary extension mechanism rather than framework-specific plugins
  <sub>★ 53.9k · Rust · Apache-2.0 · script · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash`</sub>
- **[Aider](https://github.com/Aider-AI/aider)** — AI pair-programmer harness with an Architect mode that splits planning (one LLM) from coding (another), and git-aware tooling that uses version control as the undo mechanism instead of custom state rollback. The best reference for multi-file editing tool design and planner/coder layer separation
  <sub>★ 48.7k · Python · Apache-2.0 · source · pushed 2026-05-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Aider-AI/aider.git`</sub>
- **[nanobot](https://github.com/HKUDS/nanobot)** — HKUDS's ultra-lightweight, self-hosted personal AI agent framework: a single readable Python core that combines WebUI/terminal/chat-app surfaces, long-term memory, MCP tools, model routing, multi-agent delegation, and scheduled automation. A practical reference for how a complete personal agent harness can own the full stack without becoming a black-box platform
  <sub>★ 47.7k · Python · MIT · psh · pushed 2026-09-02 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/HKUDS/nanobot/main/scripts/install.ps1 | iex`</sub>
- **[CodeWhale](https://github.com/Hmbown/Codewhale)** — Open-source, community-driven terminal coding agent harness written in Rust with a model-agnostic runtime, OS-level sandbox (Seatbelt/Landlock/seccomp/bwrap), resumable fleets via an append-only ledger, and a /model command that lets you switch providers mid-task. A strong example of treating the harness — not the model — as the product surface, with clear separation between interactive TUI, headl
  <sub>★ 40.9k · Rust · MIT · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g codewhale`</sub>
- **[DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix)** — DeepSeek-native coding agent harness engineered around prefix-cache stability as a loop invariant: immutable-prefix / append-only-log / volatile-scratch partitioning achieves 99.82% cache-hit rates and ~5× cost reduction on long sessions. The most detailed public case study of designing an entire agent loop to preserve a provider-specific economic property rather than treating caching as an aftert
  <sub>★ 35.4k · Go · MIT · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g reasonix # any OS`</sub>
- **[langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)** — LangChain's batteries-included agent harness (released April 2026) with built-in planning, filesystem tools, shell access, sub-agents, and auto-summarization. The clearest open-source demonstration of how a general-purpose coding agent harness can be made ready-to-run out of the box while remaining fully extensible
  <sub>★ 28.9k · Python · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/deepagents.git`</sub>
- **[grok-build](https://github.com/xai-org/grok-build)** — SpaceXAI's open-source terminal coding agent harness: a Rust-based fullscreen TUI with an extensible tool runtime, MCP/skills/hooks support, and headless/embedded modes via ACP. A useful first-party counterpoint to Claude Code and Codex CLI for studying how a new model provider structures the loop, checkpoints workspace state, and exposes the same harness through interactive and scripted surfaces
  <sub>★ 26.4k · Rust · Apache-2.0 · source · pushed 2026-09-01 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/xai-org/grok-build.git`</sub>
- **[cua](https://github.com/trycua/cua)** — Open-source infrastructure for Computer-Use Agents: sandboxed full-desktop control across macOS, Linux, and Windows, a background-native macOS driver that operates without stealing cursor focus, plus SDKs and benchmarks. The most complete reference for building harnesses around screen-based agent loops that need real OS interaction rather than browser-only surfaces
  <sub>★ 22.1k · HTML · MIT · psh · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://cua.ai/driver/install.ps1 | iex`</sub>
- **[alibaba/open-code-review](https://github.com/alibaba/open-code-review)** — Alibaba's production-grade code review agent combining deterministic pipelines with LLM reasoning: built-in fine-tuned rules catch NPE, thread-safety, and injection vulnerabilities at line-level precision, while the LLM layer handles nuanced design feedback. Demonstrates how hybrid harnesses can outperform purely model-driven or purely static-analysis approaches by assigning each layer the problem
  <sub>★ 21.9k · Go · Apache-2.0 · npm · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @alibaba-group/open-code-review`</sub>
- **[SWE-agent](https://github.com/SWE-agent/SWE-agent)** — Coding agent whose Agent-Computer Interface (ACI) — purpose-built file viewer, search, and editor tools with explicit state constraints and error feedback — is the reference design for adapting a tool interface to a specific task domain rather than using generic bash
  <sub>★ 20.2k · Python · MIT · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SWE-agent/SWE-agent.git`</sub>
- **[browser-harness](https://github.com/browser-use/browser-harness)** — Self-healing browser harness that connects an LLM directly to your real Chrome via CDP. The critical design decision: the agent itself writes missing helpers and domain skills into the harness during execution, so the scaffold improves every run rather than requiring manual updates. At ~1k lines across four core files, it is the clearest published demonstration of an editable harness that learns f
  <sub>★ 17.3k · Python · MIT · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browser-use/browser-harness.git`</sub>
- **[HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness)** — A compact, inspectable open-source agent harness from HKUDS (April 2026) featuring a built-in personal agent (ohmo), auto-compaction with session preservation, MCP HTTP transport, and multimodal gateway support. Excellent reference for understanding how a small, modular harness can support multi-day sessions without manual context management
  <sub>★ 15.6k · Python · MIT · pip · pushed 2026-06-04 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pip install openharness-ai`</sub>
- **[Pipecat: Python Framework for Real-Time Voice Agent Pipelines](https://github.com/pipecat-ai/pipecat)** — Handles frame management, streaming media coordination, and pipeline orchestration between ASR/LLM/TTS services for sub-800ms Total Turn-Around Time voice interactions. The missing harness primitive for voice agents: manages backpressure, handles frame queueing, and exposes a simple async interface for real-time constraints. Critical infrastructure for building responsive voice-first agents
  <sub>★ 15.2k · Python · BSD-2-Clause · uv · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install "pipecat-ai[cli]"`</sub>
- **[qm](https://github.com/yc-software/qm)** — Y Combinator's open-source multiplayer agent harness for startups: isolated per-person workspaces plus shared Slack channels and projects, with pluggable harness backends (Claude Code, Codex, OpenCode, Pi) and scope-owned skills. The clearest reference for building team-wide agent deployments where personal customization and collaborative context coexist without vendor lock-in
  <sub>★ 14.5k · TypeScript · MIT · clone · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:<org>/qm-private`</sub>
- **[OpenSRE](https://github.com/Tracer-Cloud/opensre)** — Open-source framework for building AI SRE agents with 60+ observability and remediation tool integrations plus a synthetic incident evaluation environment. The clearest open-source reference for turning infrastructure incident response into a trainable, evaluable agent harness rather than a one-off chatbot
  <sub>★ 11k · Python · Apache-2.0 · psh · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://install.opensre.com | iex`</sub>
- **[AIO Sandbox](https://github.com/agent-infra/sandbox)** — All-in-one agent sandbox combining browser, shell, filesystem, MCP servers, and VSCode Server in a single Docker container. Native MCP support exposes sandbox capabilities to LLMs via the standard protocol, and files downloaded in the browser are instantly accessible in terminal and VSCode. Optimized startup (4–8s depending on config) with Claude Skills mounting support. The fastest path to a full
  <sub>★ 5.8k · Python · Apache-2.0 · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install agent-sandbox`</sub>
- **[Squad](https://github.com/bradygaster/squad)** — Repository-native multi-agent orchestration framework built on GitHub Copilot. Initializes a persistent AI team (lead, frontend, backend, tester) as files inside your repo — knowledge compounds across sessions through committed history.md and decisions.md. The most accessible reference for teams that want multi-agent coordination without heavy infrastructure
  <sub>★ 3.2k · TypeScript · MIT · winget · pushed 2026-09-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install --id bradygaster.Squad --exact`</sub>
- **[desloppify](https://github.com/peteromallet/desloppify)** — Agent harness that turns codebase quality improvement into a structured, score-driven workflow: mechanical detectors find dead code and complexity, LLM review assesses naming and abstractions, and a persistent next → fix → resolve loop keeps the agent on track across sessions. The anti-gaming score design — where wontfix items widen the gap between lenient and strict scores — is a rare example of
  <sub>★ 3k · Python · pip · pushed 2026-05-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade "desloppify[full]"`</sub>
- **[Qwen Audio Agent](https://github.com/QwenAudio/qwen-audio-agent)** — Qwen's realtime voice runtime that keeps agents talking, working, and present across multiple backend agents (Claude Code, Codex, Qwen Code, Kimi Code). It demonstrates how to wrap terminal-native coding agents in a persistent, interruptible voice shell without losing task continuity — a concrete reference for ambient agent interfaces
  <sub>★ 2.3k · JavaScript · Apache-2.0 · npm · pushed 2026-09-03 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`npm install -g qwen-audio-agent`</sub>
- **[SmallCode](https://github.com/Doorman11991/smallcode)** — Terminal-native coding agent built from the ground up for 8B–35B local models. Its harness innovations are all compensations for small-model limitations: 2-stage tool routing halves schema overhead, a forgiving multi-format parser recovers from malformed JSON/YAML/XML tool calls, patch-first editing avoids the truncation errors common when small models rewrite entire files, and a context budget en
  <sub>★ 2k · JavaScript · MIT · npm · pushed 2026-08-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g smallcode`</sub>
- **[AMAP-ML/LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness)** — Long-horizon computer-use harness that runs on top of Claude Code and Codex, splitting work into Manager, Executor, and Auditor roles so only independently verified results enter persistent task state. The clearest August 2026 open-source reference for carrying desktop-and-CLI tasks through dozens of hours without state drift
  <sub>★ 1.5k · Python · MIT · uv · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install lh-harness # or: pip install lh-harness`</sub>
- **[ClawGUI](https://github.com/ZJU-REAL/ClawGUI)** — End-to-end harness for GUI agents that unifies online RL training, standardized benchmarking, and real-device deployment in one framework. The most complete open-source reference for building visual perception-action loops across desktop and mobile surfaces
  <sub>★ 1.3k · Python · Apache-2.0 · clone · pushed 2026-06-03 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/ZJU-REAL/ClawGUI.git`</sub>
- **[dao-code](https://github.com/tigicion/dao-code)** — DeepSeek-V4 terminal coding agent harness that treats prefix-cache economics as a first-class design constraint: byte-stable system prompts, cache-reusing forks for reflection and memory, and a self-verifying cross-session memory layer keep real SWE-bench-style tasks at ~95.8% cache hit and ~30× cheaper than Claude Opus. A concrete demonstration that harness-level cache engineering can substitute
  <sub>★ 1.3k · TypeScript · MIT · npm · pushed 2026-08-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm i -g dao-code # global install, command name dao`</sub>
- **[bux](https://github.com/browser-use/bux)** — A 24/7 Claude Code agent with Browser Harness, running autonomously on any machine you own. Demonstrates how to combine a terminal-native coding agent with live browser automation for workflows that span API documentation, web-based configuration, and headless verification — the reference for unattended agents that need both shell and browser surfaces
  <sub>★ 422 · Python · MIT · source · pushed 2026-08-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browser-use/bux.git`</sub>
- **[AOHP](https://github.com/aohp-os/aohp)** — Android Open Harness Project: an open-source OS-level agent harness built on AOSP that treats AI agents as first-class OS actors, redesigning service composition, agent interfaces, and information flow for personalized, efficient, and secure mobile interaction. It fills a rare gap by moving the scaffolding from an application layer down into the operating system itself, with early results reportin
  <sub>★ 150 · Python · Apache-2.0 · clone · pushed 2026-07-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone git@github.com:aohp-os/aohp.git`</sub>
- **[coleam00/your-claude-engineer](https://github.com/coleam00/your-claude-engineer)** — Agent harness with Slack, GitHub, and Linear integrations. Useful reference for how real-world tool wiring works inside a harness
  <sub>★ 140 · Python · MIT · source · pushed 2026-02-01 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/coleam00/your-claude-engineer.git`</sub>
- **[Anthropic Computer Use Demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)** — Anthropic's reference harness for the screenshot-action loop: defines the screenshot, bash, and text_editor tool interface that makes desktop/browser control work. Essential reading before building any harness where the agent's primary sensory input is a rendered screen rather than structured API responses
  <sub>TypeScript · MIT · in-repo · pushed 2026-09-01</sub>
  <sub>`git clone https://github.com/anthropics/anthropic-quickstarts.git && cd anthropic-quickstarts/computer-use-demo`</sub>
- **[Open SWE: An Open-Source Framework for Internal Coding Agents](https://blog.langchain.com/open-swe-an-open-source-framework-for-internal-coding-agents/)** — A composable coding-agent harness built on Deep Agents, synthesizing design patterns from Stripe, Ramp, and Coinbase production deployments. Key decisions: curated ~15-tool limit enforced at harness design time, one isolated sandbox (Modal/Daytona/Runloop/LangSmith) per task, AGENTS.md for injecting repo-wide conventions, and Linear/Slack task context in the system prompt. The most recent publishe
  <sub>website</sub>
  <sub>`https://blog.langchain.com/open-swe-an-open-source-framework-for-internal-coding-agents/`</sub>
- **[Live-SWE-agent: Autonomous Software Agent with Self-Evolving Harness](https://arxiv.org/html/2511.13646v3)** — Production harness achieving 77.4% solve rate on SWE-bench Verified through continuous harness evolution — the scaffold adapts from failure signals rather than requiring manual retuning per task class. Demonstrates the architectural pattern where the harness itself is a learnable component, not just a static container for a fixed agent
  <sub>website</sub>
  <sub>`https://arxiv.org/html/2511.13646v3`</sub>
- **[The Virtual Biotech: Multi-Agent AI Framework for Drug Discovery](https://www.biorxiv.org/content/10.64898/2026.02.23.707551v1)** — Orchestrated team of domain-specialized scientist agents that autonomously analyzed 55,984 clinical trials and discovered cell-type-specific drug targets 40% more likely to succeed Phase I→II transitions. Demonstrates specialized harness design for scientific workflows where formal reasoning, multi-agent coordination, and domain-specific tool suites are load-bearing constraints. Shows the upper bo
  <sub>website</sub>
  <sub>`https://www.biorxiv.org/content/10.64898/2026.02.23.707551v1`</sub>
- **[GitHub Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)** — GitHub's February 13, 2026 technical preview is unusually valuable because the implementation is fully open source (gh-aw) and shows how natural-language workflow generation, approval handling, and GitHub-native execution fit together in one harness. It belongs here as a reference implementation for teams that want to study agentized CI/CD rather than just chat-centric coding agents
  <sub>website</sub>
  <sub>`https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/`</sub>

## Related Awesome Lists

- **[awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)** — Collection of production LLM applications with source code across RAG, multi-agent, and tool-use patterns. Good reference for how harness primitives combine in real applications
  <sub>★ 135.9k · Python · Apache-2.0 · npx · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/project-graveyard`</sub>
- **[awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** — Curated resources, tools, and workflows specifically for Claude Code users
  <sub>★ 53.4k · Python · source · pushed 2026-09-03 · macOS</sub>
  <sub>`git clone https://github.com/hesreallyhim/awesome-claude-code.git`</sub>
- **[awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)** — Curated list of AI agents and agent frameworks, organized by use case. Useful for surveying the landscape of what harnesses are being built around
  <sub>★ 29.9k · source · pushed 2026-08-21 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/e2b-dev/awesome-ai-agents.git`</sub>
- **[awesome-mcp-servers](https://github.com/appcypher/awesome-mcp-servers)** — Comprehensive list of MCP servers for extending agents with external capabilities
  <sub>★ 5.8k · source · pushed 2026-05-06 · macOS</sub>
  <sub>`git clone https://github.com/appcypher/awesome-mcp-servers.git`</sub>
- **[Awesome Context Engineering](https://github.com/Meirtz/Awesome-Context-Engineering)** — Comprehensive survey on context engineering: prompt engineering, RAG, context window management, production AI systems
  <sub>★ 3.3k · MIT · source · pushed 2026-05-28 · Win?</sub>
  <sub>`git clone https://github.com/Meirtz/Awesome-Context-Engineering.git`</sub>
- **[Awesome Code as Agent Harness Papers](https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers)** — Curated companion list to the *Code as Agent Harness* survey, organizing research on code-centric agentic systems across interface, mechanisms, and scaling layers. A focused research map for anyone building harnesses where code is the executable scaffold rather than just the output
  <sub>★ 672 · MIT · source · pushed 2026-05-20 · Win?</sub>
  <sub>`git clone https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers.git`</sub>
- **[ICLR 2026 MemAgents Workshop](https://sites.google.com/view/memagent-iclr26/)** — Interdisciplinary workshop (April 27, Rio de Janeiro) covering episodic/semantic memory, knowledge graphs, vector databases, retrieval pipelines, temporal credit assignment, and context management for agentic systems. The canonical venue for memory architecture research and standards; accepts full papers (9pg), short papers (4pg), tiny papers (2pg)
  <sub>website</sub>
  <sub>`https://sites.google.com/view/memagent-iclr26/`</sub>

## Production Infrastructure &amp; Operations

- **[getagentseal/codeburn](https://github.com/getagentseal/codeburn)** — Free, local tool that tracks AI coding token usage and cost across 31 tools and agents by model, project, and task. Worth including because cross-tool cost visibility is the missing prerequisite for agent FinOps in multi-tool teams — most observability tools either require cloud upload or only cover a single provider
  <sub>★ 10.8k · TypeScript · MIT · npm · pushed 2026-09-03 · macOS</sub>
  <sub>`npm install -g codeburn`</sub>
- **[builderz-labs/mission-control](https://github.com/builderz-labs/mission-control)** — Self-hosted orchestration dashboard for agent task dispatch, multi-agent workflow coordination, and spend monitoring across gateways. The zero-external-dependency design (SQLite, single pnpm start) makes it the most practical open-source control plane for teams that need governance and cost visibility without building infrastructure from scratch
  <sub>★ 6.2k · TypeScript · MIT · docker · pushed 2026-09-02 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run --rm -p 3000:3000 ghcr.io/builderz-labs/mission-control:latest`</sub>
- **[truefoundry/trueforge](https://github.com/truefoundry/trueforge)** — TrueFoundry's open-source agent harness runtime: runs the execution loop, MCP tools, skills, sandboxing, approvals, context management, and session state, exposing it through a chat UI, HTTP API, and embeddable UI SDK. A concrete reference for turning a model-plus-tools stack into a production-grade agent without building the loop from scratch
  <sub>★ 5.2k · TypeScript · MIT · npx · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @truefoundry/trueforge@latest`</sub>
- **[kvcache-ai/AgentENV](https://github.com/kvcache-ai/AgentENV)** — Distributed platform for running agent environments at scale, powering Kimi K3's agentic RL training. Sub-50ms snapshot boot/resume, native fork support for parallel workflows, and overlaybd-based image loading make it the right infrastructure layer when your harness needs thousands of ephemeral sandboxes rather than a handful
  <sub>★ 3.4k · Rust · MIT · script · pushed 2026-09-03 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/kvcache-ai/AgentENV/main/scripts/install.sh | sudo bash`</sub>
- **[Claude Managed Agents: Self-Hosted Sandboxes and MCP Tunnels](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)** — Anthropic's May 2026 enterprise deployment pattern keeps the agent orchestration loop on Anthropic's infrastructure while moving tool execution into customer-controlled sandboxes; combined with MCP tunnels for private-network tool access, it's the reference architecture for data-residency-conscious production harnesses
  <sub>website</sub>
  <sub>`https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes`</sub>
- **[AgentCgroup: Understanding and Controlling OS Resources of AI Agents](https://arxiv.org/abs/2602.09345)** — February 2026 empirical study of sandboxed coding-agent workloads finding that OS-level execution accounts for 56–74% of end-to-end latency and memory is the real concurrency bottleneck (15.4× peak-to-average spikes driven by tool calls). Proposes an intent-driven eBPF controller aligned with tool-call boundaries — essential for anyone running multi-tenant agent sandboxes where coarse container li
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.09345`</sub>
- **[AI Agent Scaling Gap: Pilot to Production (March 2026)](https://www.digitalapplied.com/blog/ai-agent-scaling-gap-march-2026-pilot-to-production)** — Analysis showing 72% of Global 2000 companies operate agents beyond experimental phases, but only 14% successfully scaled organization-wide. Scaling success correlates strongly with operations infrastructure (monitoring, evaluation harnesses, incident response) rather than technology choices. Documents the shift from engineering-focused to operations-focused agent deployment
  <sub>website</sub>
  <sub>`https://www.digitalapplied.com/blog/ai-agent-scaling-gap-march-2026-pilot-to-production`</sub>
- **[5 Production Scaling Challenges for Agentic AI in 2026](https://machinelearningmastery.com/5-production-scaling-challenges-for-agentic-ai-in-2026/)** — Data infrastructure prioritized before deployment; successful scalers appoint AI operations function pre-expansion; multi-agent distributed systems with load balancing and auto-scaling. Essential reading for understanding infrastructure prerequisites for agent deployment at scale
  <sub>website</sub>
  <sub>`https://machinelearningmastery.com/5-production-scaling-challenges-for-agentic-ai-in-2026/`</sub>
- **[AI Agent Cost Optimization Guide 2026: Reduce Spend by 60-80%](https://moltbook-ai.com/posts/ai-agent-cost-optimization-2026)** — Systematic patterns for cost reduction: model routing and caching (40-60% savings); Anthropic prompt caching (90% discount on cached tokens); identifying unnecessary agent overhead vs. simple API chains. Key harness decisions (tool selection, caching strategy, model choice per task) determine operating cost
  <sub>website</sub>
  <sub>`https://moltbook-ai.com/posts/ai-agent-cost-optimization-2026`</sub>
- **[KernelEvolve: How Meta's Ranking Engineer Agent Optimizes AI Infrastructure](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/)** — Meta's production-grade agentic kernel optimization system that autonomously generates optimized Triton kernels for hundreds of models serving billions of users daily. Achieves up to 17x speedup over PyTorch baselines with 100% correctness across 250 problems. Demonstrates harness design for continuous infrastructure optimization: a purpose-built job-harness evaluates each candidate kernel, feeds
  <sub>website</sub>
  <sub>`https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/`</sub>
- **[State of Agent Engineering 2026](https://www.langchain.com/state-of-agent-engineering)** — LangChain's industry survey of 1,300+ professionals: 57.3% now have agents in production (up from 51%), quality is the top barrier at 32%, and 89% have implemented observability while only 52% run evals. The most comprehensive snapshot of where the industry stands on agent deployment maturity, model strategies, and operational gaps
  <sub>website</sub>
  <sub>`https://www.langchain.com/state-of-agent-engineering`</sub>
- **[Agentic Development: What It Means for Engineering Infrastructure in 2026](https://www.bunnyshell.com/guides/agentic-development/)** — Defines the four infrastructure capabilities that agentic development requires: per-task isolated sandboxes, sub-100ms startup (ruling out traditional VMs and most K8s approaches), API-driven lifecycle management, and MCP-native environment control. The clearest articulation of why existing CI/CD infrastructure is insufficient for agent-driven development workflows
  <sub>website</sub>
  <sub>`https://www.bunnyshell.com/guides/agentic-development/`</sub>
- **[Backtesting AI Agents: How SRE Teams Prove Reliability Before Production](https://drdroid.io/blog/backtesting-ai-agents-how-sre-teams-prove-reliability-before-production)** — Formalizes agent validation as infrastructure-grade testing with pass^k reliability (all 20+ trials must succeed) rather than pass@k (one success). Defines five measurable dimensions (consistency, robustness, predictability, safety, cost stability) with specific SLO thresholds. Recommends dataset composition of 20% golden paths, 30% edge cases, 20% adversarial, 30% regression from production incid
  <sub>website</sub>
  <sub>`https://drdroid.io/blog/backtesting-ai-agents-how-sre-teams-prove-reliability-before-production`</sub>
- **[How My Agents Self-Heal in Production](https://blog.langchain.com/production-agents-self-heal/)** — A concrete April 3, 2026 production pattern for closing the post-deploy loop: detect regressions, attribute whether the last deploy caused them, then dispatch a coding agent to open a fix PR automatically. This belongs here because it turns evals and observability into an active remediation harness, not just a dashboard humans are expected to watch
  <sub>website</sub>
  <sub>`https://blog.langchain.com/production-agents-self-heal/`</sub>
- **[Minions: Stripe's one-shot, end-to-end coding agents—Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)** — Stripe's deep-dive into their unattended minion harness shipping 1,300+ PRs/week: "blueprints" interleave deterministic code nodes with agentic subtasks, a centralized 500-tool MCP server (Toolshed) serves the whole fleet, and pre-warmed devboxes prove that investments in human developer productivity pay equal dividends for agents
  <sub>website</sub>
  <sub>`https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2`</sub>
- **[Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)** — AWS's fully managed agent deployment platform providing serverless runtime with session isolation, built-in memory (session + long-term), secure gateway for tool access, browser runtime, and code interpreter — all framework-agnostic. Now supports AG-UI protocol for real-time agent-to-frontend streaming, VPC/PrivateLink for enterprise security, and CloudFormation for infrastructure-as-code deployme
  <sub>website</sub>
  <sub>`https://aws.amazon.com/bedrock/agentcore/`</sub>
- **[AWS Agent Registry for Centralized Agent Discovery and Governance](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/)** — AWS's April 9, 2026 preview adds a missing production primitive: a governed catalog for agents, tools, skills, MCP servers, and custom resources with approval workflows, audit trails, and MCP-accessible discovery. Worth including because large organizations do not just need to run agents safely; they need to know what agent capabilities already exist so teams stop rebuilding the same scaffolding i
  <sub>website</sub>
  <sub>`https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/`</sub>
- **[A Dev's Guide to Production-Ready AI Agents](https://cloud.google.com/blog/products/ai-machine-learning/a-devs-guide-to-production-ready-ai-agents)** — Google Cloud's developer guide (April 2026) for moving AI agents from prototype to production using ADK, Vertex AI Agent Engine for managed hosting, and Cloud Run for serverless deployment. Covers the full production stack: agent development patterns, scaling considerations, security and identity requirements, and operational monitoring — the most concrete first-party guide for deploying agents on
  <sub>website</sub>
  <sub>`https://cloud.google.com/blog/products/ai-machine-learning/a-devs-guide-to-production-ready-ai-agents`</sub>
- **[Enhanced Tool Governance in Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder)** — Google Cloud's approach to production agent governance (April 2026): agents get identity as first-class IAM principals with least-privilege enforcement, Cloud API Registry integration enables organizational tool governance (admins manage available tools centrally), and a new observability dashboard tracks token usage, latency, and error rates. Demonstrates the cloud-native pattern for tool governa
  <sub>website</sub>
  <sub>`https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder`</sub>
- **[What Is an Agent Harness? Running Governed Managed Agents in Production](https://www.truefoundry.com/blog/agent-harness-managed-ai-agents)** — TrueFoundry's June 2026 architectural guide to the agent harness as a production runtime: declarative agent definitions reference models, MCP servers, and versioned skills by name while the platform injects secrets, manages sandboxes, and unifies traces across model, tool, and agent traffic. The clearest published framing of the harness as the build-or-buy operational layer that turns a model-plus
  <sub>website</sub>
  <sub>`https://www.truefoundry.com/blog/agent-harness-managed-ai-agents`</sub>
- **[Building Governed Agents: A Framework for Cost, Control, and Compliance](https://www.langchain.com/blog/building-governed-agents-a-framework-for-cost-control-and-compliance)** — LangChain's July 2026 framework for treating the agent gateway as a runtime control plane that enforces cost, control, and compliance policies across every model call, tool call, and agent hop. A concrete reference for moving agent governance from static configuration into a harness-level enforcement layer
  <sub>website</sub>
  <sub>`https://www.langchain.com/blog/building-governed-agents-a-framework-for-cost-control-and-compliance`</sub>

## Adjacent Collections

- **[VoltAgent/awesome-ai-agent-papers](https://github.com/VoltAgent/awesome-ai-agent-papers)** — Curated collection of 363+ arXiv papers from 2026 organized into five harness-relevant categories: Multi-Agent (51), Memory &amp; RAG (56), Eval &amp; Observability (79), Agent Tooling (95), AI Agent Security (82). Weekly updates make it the best single source for tracking research that will shape harness design decisions in 2026
  <sub>★ 1.7k · MIT · source · pushed 2026-09-02 · Win?</sub>
  <sub>`git clone https://github.com/VoltAgent/awesome-ai-agent-papers.git`</sub>
- **[Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness)** — Implementation-first curated list (April 2026) with 150 entries, 84% GitHub projects, organized into 9 categories from harness architecture to sandboxing. The featured blogs section and catalog-style organization make it a strong complementary reference to this list's article-centric approach
  <sub>★ 1.7k · Python · source · pushed 2026-08-30 · macOS</sub>
  <sub>`git clone https://github.com/Picrew/awesome-agent-harness.git`</sub>
- **[bradAGI/awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents)** — Catalog of 80+ terminal-native AI coding agents (open-source and proprietary) plus the harnesses that orchestrate, sandbox, and extend them: session managers, parallel runners, autonomous loop infrastructure, and credential vaults. The most comprehensive reference for the CLI agent layer that most harness infrastructure is designed to host
  <sub>★ 1.1k · Python · source · pushed 2026-08-31 · macOS</sub>
  <sub>`git clone https://github.com/bradAGI/awesome-cli-coding-agents.git`</sub>
- **[RyanAlberts/best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses)** — A curated, ranked list of 124 agent harnesses, rescored weekly and published as machine-readable data with an MCP server. The most practical complement for discovering and comparing harnesses, and a rare example of a list built to be consumed by agents themselves
  <sub>★ 782 · Python · CC-BY-SA-4.0 · source · pushed 2026-09-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/RyanAlberts/best-of-Agent-Harnesses.git`</sub>
- **[EvoMap/awesome-agent-evolution](https://github.com/EvoMap/awesome-agent-evolution)** — April 2026 curated list covering agent evolution, memory systems, multi-agent architectures, and self-improvement. Complements this list with a forward-looking lens on the next generation of agent capabilities — where harnesses must adapt to agents that modify their own scaffolding over time
  <sub>★ 211 · JavaScript · source · pushed 2026-09-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/EvoMap/awesome-agent-evolution.git`</sub>
- **[jiji262/awesome-harness-engineering](https://github.com/jiji262/awesome-harness-engineering)** — Focuses on platform delivery governance, IDP, GitOps, and AI-native engineering. Overlaps with this list on the platform engineering side; more Harness-the-company oriented
  <sub>★ 51 · source · pushed 2026-05-30 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/jiji262/awesome-harness-engineering.git`</sub>
- **[danielrosehill/AI-Harnesses](https://github.com/danielrosehill/AI-Harnesses)** — April 2026 point-in-time snapshot of projects describing themselves as AI agent harnesses, organized into Resource Lists, Harness Runtimes, and Reference Implementations. Useful as a landscape survey of how the term "harness" is being applied across the ecosystem — from lightweight wrappers to full orchestration frameworks
  <sub>★ 12 · source · pushed 2026-04-04</sub>
  <sub>`git clone https://github.com/danielrosehill/AI-Harnesses.git`</sub>


---

Snapshot 2026-09-03. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
