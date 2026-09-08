# A first agentic setup

*Seven decisions, one afternoon*

The atlas has 1,294 projects in it, which is the wrong number to start from. This is one working setup instead: an agent, the things it loads, the place it runs, and the two tools that tell you afterwards whether it did what you asked. Every slot is filled once. Swap any of them later -- the point of the set is that you can start today and still know what each piece is for.

7 picks · 821,311 combined stars · snapshot 2026-09-03

[Open all 7 in the atlas](https://crazy54.github.io/awesome-agentic-atlas/#list=anomalyco/opencode,obra/superpowers,mem0ai/mem0,modelcontextprotocol/servers,daytonaio/daytona,langfuse/langfuse,shareAI-lab/learn-claude-code) — from there you can save them to your own projects or export the set as Markdown, HTML or a PDF.

---

## 1. The agent — [OpenCode](https://github.com/anomalyco/opencode)

`anomalyco/opencode` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/anomalyco/opencode/)

Terminal-native, MIT, and the one coding agent here that three separate source lists picked independently. It runs against whichever model you already pay for rather than tying the setup to one vendor.

> Open-source terminal-native AI coding agent with 131K+ stars and 2.5M+ monthly active developers. Provider-agnostic architecture supports 75+ LLM providers plus native LSP auto-configuration, multi-session parallel agents, and MCP extensibility. The build/plan agent split and client/server architecture make it the most complete open-source reference for a terminal-first coding harness

```sh
scoop install opencode # Windows
```

**203,467** stars · 3 of 11 lists · TypeScript · MIT · pushed 2026-09-03

Platforms: Win N WSL N mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Coding Agents · Targets: opencode, MCP

---

## 2. What it knows how to do — [Superpowers](https://github.com/obra/superpowers)

`obra/superpowers` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/obra/superpowers/)

The most-starred skills bundle in the atlas and, unusually, one that spans seven different harnesses -- so the competencies survive changing your mind about the agent above.

> by Jesse Vincent - A strong bundle of core competencies for software engineering, with good coverage of a large portion of the SDLC - from planning, reviewing, testing, debugging... Well written, well organized, and adaptable. The author refers to them as "superpowers", but many of them are just consolidating engineering best practices - which sometimes does feel like a superpower when working wit

```sh
git clone https://github.com/obra/superpowers.git
```

**281,176** stars · 3 of 11 lists · Shell · MIT · pushed 2026-08-31

Platforms: Win N WSL N mac N Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Agent Skills · Targets: Claude Code, Claude / Anthropic, MCP, Codex / OpenAI, Gemini / Google, GitHub Copilot, Cursor

---

## 3. What it remembers — [mem0](https://github.com/mem0ai/mem0)

`mem0ai/mem0` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/mem0ai/mem0/)

A memory layer you drop in rather than a database you design. Apache-2.0, and it states support on Windows and in Docker, which most of this category does not.

> Drop-in universal memory layer (YC-backed, AWS Agent SDK's exclusive memory provider) that handles cross-session retention without custom harness-level state management code. Lowest integration cost for production-grade persistent memory

```sh
npm install -g @mem0/cli # or: pip install mem0-cli
```

**64,649** stars · 2 of 11 lists · Python · Apache-2.0 · pushed 2026-09-03

Platforms: Win Y WSL L mac Y Lin Y Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Context, Memory & RAG · Targets: Codex / OpenAI

---

## 4. How it reaches your tools — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

`modelcontextprotocol/servers` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/modelcontextprotocol/servers/)

The reference MCP servers, from the people who wrote the protocol. Start here and you learn the shape every third-party server in the atlas is copying.

> Anthropic's official reference MCP server implementations (GitHub, Slack, Postgres, Puppeteer, etc.). The authoritative source for understanding correct MCP server structure before building your own

```sh
npx -y @modelcontextprotocol/server-memory
```

**90,050** stars · 2 of 11 lists · TypeScript · no licence stated · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: MCP Servers · Targets: Claude / Anthropic, MCP

---

## 5. Where it runs — [Daytona](https://github.com/daytonaio/daytona)

`daytonaio/daytona` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/daytonaio/daytona/)

Container sandboxes that start in under a tenth of a second, which is the difference between isolating every run and isolating the runs you remember to. An agent with shell access and no sandbox is a decision, not a default.

> OCI-container sandboxes with sub-90ms startup, built-in Git operations, LSP support, and indefinite state persistence. Complements E2B for harnesses that need long-lived working directories across multiple agent sessions rather than ephemeral code execution

```sh
pip install daytona
```

**71,828** stars · 1 list · language not detected · no licence stated · pushed 2026-07-24

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Sandbox, Security & Governance

---

## 6. What it actually did — [Langfuse](https://github.com/langfuse/langfuse)

`langfuse/langfuse` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/langfuse/langfuse/)

Self-hostable tracing, so the record of what the agent sent and got back stays on your own machine. Two source lists agree on it and it is the most widely adopted of the open options.

> The most widely adopted self-hostable LLM observability platform: traces every agent step, manages prompt versions, and runs evals in one tool. Preferred over cloud-only alternatives when data residency or cost control is a constraint

```sh
pip install langfuse openai
```

**34,156** stars · 2 of 11 lists · TypeScript · no licence stated · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals · Targets: Codex / OpenAI, LangChain / LangGraph

---

## 7. What to read while it runs — [Learn Claude Code](https://github.com/shareAI-lab/learn-claude-code)

`shareAI-lab/learn-claude-code` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/shareai-lab/learn-claude-code/)

A read-through of how a real coding agent is built rather than a tutorial for using one. It is the fastest way to stop being surprised by the six choices above.

> by shareAI-lab - A really interesting analysis of how coding agents like Claude Code are designed. It attempts to break an agent down into its fundamental parts and reconstruct it with minimal code. Great learning resource. Final product is a rudimentary agent with skills, sub-agents, and a todo-list in roughly a few hundred lines of Python

```sh
npm i -g @shareai-lab/kode
```

**75,985** stars · 2 of 11 lists · Python · MIT · pushed 2026-08-26

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Docs, Learning & Lists · Targets: Claude Code, Claude / Anthropic

---

These are editorial picks — the only editorial pages on the atlas. Everything else here is what 11 awesome-lists agreed on. The curation is a [reviewable file](https://github.com/crazy54/awesome-agentic-atlas/blob/main/config/collections.json); open an issue if you would pick differently.
