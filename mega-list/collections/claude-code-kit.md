# The Claude Code power kit

*What to install after the agent*

Claude Code is the harness the largest single share of this atlas is built for. Installing it is ten seconds; the next hour is the part nobody writes down. These seven cover the format skills come in, three bundles worth reading before writing your own, the two things that make long sessions cheaper, and where to look when you want more. Every project here targets Claude Code, and the build checks that too.

7 picks · 931,081 combined stars · snapshot 2026-09-03

[Open all 7 in the atlas](https://crazy54.github.io/awesome-agentic-atlas/#list=anthropics/skills,obra/superpowers,multica-ai/andrej-karpathy-skills,addyosmani/agent-skills,JuliusBrussee/caveman,ccusage/ccusage,hesreallyhim/awesome-claude-code) — from there you can save them to your own projects or export the set as Markdown, HTML or a PDF.

> Every pick is checked at build time: `target` = `claude-code`. If the committed snapshot stops supporting that for any one of them, this page fails to build rather than quietly meaning something weaker.

---

## 1. The format — [Agent Skills](https://github.com/anthropics/skills)

`anthropics/skills` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/anthropics/skills/)

Anthropic's own repository for Agent Skills: the SKILL.md format, a template and worked examples. Read this first and every other skills bundle in the atlas becomes legible.

> by Anthropic - Anthropic's official repository for Agent Skills — the SKILL.md format, a skill template, and example skills, the same format Claude Code loads natively

```sh
git clone https://github.com/anthropics/skills.git
```

**173,481** stars · 2 of 11 lists · Python · no licence stated · pushed 2026-09-01

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Agent Skills · Targets: Claude Code, Claude / Anthropic

---

## 2. The bundle — [Superpowers](https://github.com/obra/superpowers)

`obra/superpowers` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/obra/superpowers/)

Core software-engineering competencies covering most of the SDLC, well organised and adaptable. It is the most-starred skills project here and the one most often forked as a starting point.

> by Jesse Vincent - A strong bundle of core competencies for software engineering, with good coverage of a large portion of the SDLC - from planning, reviewing, testing, debugging... Well written, well organized, and adaptable. The author refers to them as "superpowers", but many of them are just consolidating engineering best practices - which sometimes does feel like a superpower when working wit

```sh
git clone https://github.com/obra/superpowers.git
```

**281,176** stars · 3 of 11 lists · Shell · MIT · pushed 2026-08-31

Platforms: Win N WSL N mac N Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Agent Skills · Targets: Claude Code, Claude / Anthropic, MCP, Codex / OpenAI, Gemini / Google, GitHub Copilot, Cursor

---

## 3. The instructions file — [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)

`multica-ai/andrej-karpathy-skills` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/multica-ai/andrej-karpathy-skills/)

A drop-in CLAUDE.md distilling four behavioural guidelines, derived from Andrej Karpathy's public notes on LLM coding pitfalls. One file, and the cheapest improvement on this page.

> by multica-ai - A drop-in CLAUDE.md distilling four behavioral guidelines for LLM-assisted coding into Claude Code — a low-friction quick win. Karpathy-inspired, derived from Andrej Karpathy's public notes on LLM coding pitfalls and authored by multica-ai

```sh
git clone https://github.com/multica-ai/andrej-karpathy-skills.git
```

**209,837** stars · 2 of 11 lists · language not detected · no licence stated · pushed 2026-04-20

Platforms: Win N WSL N mac N Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Agent Skills · Targets: Claude Code, Claude / Anthropic

---

## 4. The engineering set — [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)

`addyosmani/agent-skills` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/addyosmani/agent-skills/)

Production-grade engineering skills, and portable: it also targets MCP, Codex and Cursor, so what you learn here is not stranded if you change harnesses.

> Production-grade engineering skills for AI coding agents, packaged as 24 reusable skills covering the full development lifecycle from /spec to /ship. The slash-command interface and context-aware auto-activation make it a concrete reference for turning senior-engineering judgment into agent-executable harness artifacts

```sh
npx skills add addyosmani/agent-skills # install all 25 skills
```

**91,887** stars · 2 of 11 lists · JavaScript · MIT · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Agent Skills · Targets: Claude Code, Claude / Anthropic, MCP, Codex / OpenAI, Cursor

---

## 5. The token diet — [Caveman](https://github.com/JuliusBrussee/caveman)

`JuliusBrussee/caveman` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/juliusbrussee/caveman/)

Conserves tokens by shortening what the agent says back to you. It reads like a joke and is not one -- long sessions are mostly the model narrating, and Windows support is stated.

> by Julius Brussee - A plugin that conserves message tokens by communicating in fragmented "caveman speak" - sort of a clever form of compression. Now accompanied by a whole caveman ecosystem including a memory system, caveman spec kit, and a caveman agent

```sh
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/v2.5.0/install.ps1 | iex
```

**102,940** stars · 1 list · Go · no licence stated · pushed 2026-09-02

Platforms: Win Y WSL N mac N Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Agent Skills · Targets: Claude Code, Claude / Anthropic

---

## 6. The bill — [ccusage](https://github.com/ccusage/ccusage)

`ccusage/ccusage` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/ccusage/ccusage/)

One npx command reports what your Claude Code sessions have actually cost. Zero install, no account, and the first honest number most people see.

> by ryoppippi - A zero-install CLI (npx ccusage) that analyzes Claude Code token usage and cost from local JSONL logs — daily, monthly, per-session, and 5-hour-block breakdowns, a live monitoring mode, and per-model cost estimates. Runs entirely locally, with JSON output for scripting

```sh
git clone https://github.com/ccusage/ccusage.git
```

**18,314** stars · 1 list · Rust · no licence stated · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Observability & Evals · Targets: Claude Code, Claude / Anthropic

---

## 7. Where to look next — [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

`hesreallyhim/awesome-claude-code` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/hesreallyhim/awesome-claude-code/)

The specialist list for this harness. When the kit above stops being enough, this is the catalogue to read rather than a search box to guess into.

> Curated resources, tools, and workflows specifically for Claude Code users

```sh
git clone https://github.com/hesreallyhim/awesome-claude-code.git
```

**53,446** stars · 1 list · Python · no licence stated · pushed 2026-09-03

Platforms: Win N WSL N mac Y Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Docs, Learning & Lists · Targets: Claude Code, Claude / Anthropic

---

These are editorial picks — the only editorial pages on the atlas. Everything else here is what 11 awesome-lists agreed on. The curation is a [reviewable file](https://github.com/crazy54/awesome-agentic-atlas/blob/main/config/collections.json); open an issue if you would pick differently.
