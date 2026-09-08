# Find out what the agent actually did

*Traces, tests, scans and the bill*

An agent that fails loudly is a good afternoon. The expensive failures are the quiet ones: the run that looked fine, the change that passed review, the skill that did something you did not read. None of this category is exciting and all of it is what separates a demo from something you would put in front of a customer. Traces first, then tests, then the two things people leave until after the incident.

7 picks · 119,072 combined stars · snapshot 2026-09-03

[Open all 7 in the atlas](https://crazy54.github.io/awesome-agentic-atlas/#list=langfuse/langfuse,Arize-ai/phoenix,promptfoo/promptfoo,confident-ai/deepeval,traceloop/openllmetry,NVIDIA/SkillSpector,mnfst/manifest) — from there you can save them to your own projects or export the set as Markdown, HTML or a PDF.

---

## 1. The trace — [Langfuse](https://github.com/langfuse/langfuse)

`langfuse/langfuse` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/langfuse/langfuse/)

Self-hostable, which matters here more than anywhere: the traces contain your prompts and your customers' data. The most widely adopted of the open options, and two source lists agree.

> The most widely adopted self-hostable LLM observability platform: traces every agent step, manages prompt versions, and runs evals in one tool. Preferred over cloud-only alternatives when data residency or cost control is a constraint

```sh
pip install langfuse openai
```

**34,156** stars · 2 of 11 lists · TypeScript · no licence stated · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals · Targets: Codex / OpenAI, LangChain / LangGraph

---

## 2. The second opinion — [Arize-Phoenix](https://github.com/Arize-ai/phoenix)

`Arize-ai/phoenix` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/arize-ai/phoenix/)

Three source lists carry it -- the strongest agreement in this category -- and it pairs a trace UI with an eval runtime, so you can grade the runs you are looking at.

> Self-hostable trace UI and eval runtime for agent workflows. Lets harness engineers audit and replay every reasoning step and tool call offline, without sending data to a third-party cloud

```sh
npx @arizeai/phoenix-cli setup
```

**11,307** stars · 3 of 11 lists · Python · no licence stated · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals

---

## 3. The test suite — [promptfoo](https://github.com/promptfoo/promptfoo)

`promptfoo/promptfoo` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/promptfoo/promptfoo/)

Tests as YAML, with assertions and LLM-as-judge. It is the lowest-ceremony way to turn "it seemed better" into something a pull request can fail on.

> YAML-driven LLM testing framework with LLM-as-judge, assertion DSL, and native CI integration. The most practical tool for adding agent output regression tests to a PR pipeline without writing a test harness from scratch

```sh
npm install -g promptfoo
```

**24,786** stars · 1 list · TypeScript · MIT · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals · Targets: Claude / Anthropic, Codex / OpenAI, Gemini / Google

---

## 4. The metrics — [DeepEval](https://github.com/confident-ai/deepeval)

`confident-ai/deepeval` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/confident-ai/deepeval/)

Twenty-plus built-in metrics for LLM and agent evaluation. Use it when you have stopped arguing about whether output is good and started arguing about which axis.

> The most complete open-source LLM/agent eval framework: 20+ built-in metrics (hallucination, answer relevancy, RAGAs, tool correctness), pytest integration, and a CI-friendly runner. Removes the need to hand-roll eval infrastructure when you need structured, repeatable agent quality gates

```sh
pip install -U deepeval
```

**18,082** stars · 1 list · Python · Apache-2.0 · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals

---

## 5. The standard — [OpenLLMetry](https://github.com/traceloop/openllmetry)

`traceloop/openllmetry` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/traceloop/openllmetry/)

OpenTelemetry instrumentation for LLM calls and agent steps. The one pick here that does not lock you in: the traces go wherever your existing observability already goes.

> OpenTelemetry-based instrumentation for LLM calls and agent steps: adds trace spans to every inference and tool call without modifying business logic. The cleanest way to bring the existing OTEL ecosystem (Grafana, Datadog, Jaeger) to a harness

```sh
pip install traceloop-sdk
```

**7,414** stars · 1 list · Python · Apache-2.0 · pushed 2026-08-10

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals

---

## 6. The thing you install — [SkillSpector](https://github.com/NVIDIA/SkillSpector)

`NVIDIA/SkillSpector` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/nvidia/skillspector/)

Scans agent skills for vulnerabilities. Every other page on this site encourages you to install other people's instructions; this is the tool that reads them first.

> by NVIDIA - Security scanner for AI agent skills. Detect vulnerabilities, malicious patterns, and security risks

```sh
uv tool install git+https://github.com/NVIDIA/skillspector.git
```

**15,825** stars · 1 list · Python · Apache-2.0 · pushed 2026-09-01

Platforms: Win L WSL L mac L Lin L Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Sandbox, Security & Governance · Targets: Claude Code, Claude / Anthropic, MCP, Codex / OpenAI

---

## 7. The bill — [Manifest](https://github.com/mnfst/manifest)

`mnfst/manifest` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/mnfst/manifest/)

Real-time cost observability per agent. Cost is a correctness signal in disguise -- a run that suddenly costs four times as much has usually started doing something else.

> Open-source, real-time cost observability platform for AI agents. Track tokens, costs, messages, and model usage with a local-first dashboard. Supports 28+ LLM models, OTLP ingestion, self-hosted

```sh
git clone https://github.com/mnfst/manifest.git
```

**7,502** stars · 1 list · TypeScript · MIT · pushed 2026-09-03

Platforms: Win N WSL Y mac N Lin Y Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals

---

These are editorial picks — the only editorial pages on the atlas. Everything else here is what 11 awesome-lists agreed on. The curation is a [reviewable file](https://github.com/crazy54/awesome-agentic-atlas/blob/main/config/collections.json); open an issue if you would pick differently.
