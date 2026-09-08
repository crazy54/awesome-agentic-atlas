# Runs on Windows, and says so

*Stated support, not inferred*

Most agentic tooling is written on a Mac and tested on Linux, and "it's Python, it'll be fine" is how a Windows afternoon disappears. The atlas records a per-platform verdict for every project, and it distinguishes stated support from support merely inferred from the language. Every project below has documented Windows support -- the build refuses to publish this page if one of them stops.

7 picks · 914,087 combined stars · snapshot 2026-09-03

[Open all 7 in the atlas](https://crazy54.github.io/awesome-agentic-atlas/#list=openclaw/openclaw,earendil-works/pi,continuedev/continue,ollama/ollama,ggml-org/llama.cpp,headroomlabs-ai/headroom,nearai/ironclaw) — from there you can save them to your own projects or export the set as Markdown, HTML or a PDF.

> Every pick is checked at build time: `os` = `Windows`. If the committed snapshot stops supporting that for any one of them, this page fails to build rather than quietly meaning something weaker.

---

## 1. The framework — [openclaw](https://github.com/openclaw/openclaw)

`openclaw/openclaw` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/openclaw/openclaw/)

The most-starred project in the atlas, and it puts Windows in the same sentence as macOS and Linux rather than in a footnote. Three source lists carry it.

> Open-source AI agent framework that turns LLMs into persistent, proactive personal AI agents with multi-channel messaging (Signal, Telegram, Discord, WhatsApp), cron scheduling, memory systems, MCP integration, skill plugins, sub-agent spawning, and browser automation

```sh
npm install -g openclaw@latest --allow-scripts=openclaw
```

**388,645** stars · 3 of 11 lists · TypeScript · no licence stated · pushed 2026-09-02

Platforms: Win Y WSL Y mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Frameworks & SDKs · Targets: MCP

---

## 2. The harness — [Pi](https://github.com/earendil-works/pi)

`earendil-works/pi` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/earendil-works/pi/)

A deliberately small terminal harness built around skills loaded on demand. Small is what makes it portable: there is less of it to be Unix-shaped.

> Minimal terminal coding harness built around "lazy skills": each capability keeps only a one-line description in active context, loading full instructions and tool schemas only when invoked. Keeps the system prompt under 1,000 tokens versus 7,000–10,000 for typical agents, making it a concrete reference for context-minimal harness design

```sh
git clone https://github.com/earendil-works/pi.git
```

**101,379** stars · 1 list · TypeScript · MIT · pushed 2026-09-03

Platforms: Win Y WSL L mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra

---

## 3. The coding agent — [Continue](https://github.com/continuedev/continue)

`continuedev/continue` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/continuedev/continue/)

Ships as an editor extension, which is why it works on Windows without a WSL detour -- the editor has already solved that problem.

> open-source coding agent

```sh
git clone https://github.com/continuedev/continue.git
```

**35,740** stars · 1 list · TypeScript · Apache-2.0 · pushed 2026-09-03

Platforms: Win Y WSL L mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Coding Agents

---

## 4. The model runner — [Ollama](https://github.com/ollama/ollama)

`ollama/ollama` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/ollama/ollama/)

A native Windows build, a one-line pull, and no Python environment to get wrong. If you want a local model on Windows this is the shortest path to one.

> Run LLMs locally. 162k+ stars. Dead simple CLI

```sh
irm https://ollama.com/install.ps1 | iex
```

**180,046** stars · 1 list · Go · MIT · pushed 2026-09-03

Platforms: Win Y WSL L mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

## 5. The inference engine — [llama.cpp](https://github.com/ggml-org/llama.cpp)

`ggml-org/llama.cpp` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/ggml-org/llama.cpp/)

The C++ layer under most of local AI, with first-class Windows builds and no runtime to install. Worth knowing directly once the layer above it surprises you.

> C/C++ inference. CPU, GPU, Apple Silicon. Foundation of local AI

```sh
git clone https://github.com/ggml-org/llama.cpp.git
```

**126,906** stars · 1 list · C++ · MIT · pushed 2026-09-03

Platforms: Win Y WSL N mac Y Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

## 6. The context budget — [headroom](https://github.com/headroomlabs-ai/headroom)

`headroomlabs-ai/headroom` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/headroomlabs-ai/headroom/)

Compresses tool output, logs and files before they reach the window. Windows and Docker support are both stated, and it sits in front of whatever agent you chose.

> Compresses tool outputs, logs, files, and RAG chunks before they enter the context window, cutting active tokens by 60–95% without changing answers. Ships as a library, proxy, and MCP server — the right drop-in layer for any harness where bulky tool returns are the primary context pressure source

```sh
uv tool install --python 3.13 "headroom-ai[all]" # CLI in a self-contained env
```

**68,768** stars · 1 list · Python · Apache-2.0 · pushed 2026-09-03

Platforms: Win Y WSL L mac Y Lin Y Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Context, Memory & RAG · Targets: Claude / Anthropic, MCP, LangChain / LangGraph

---

## 7. The sandbox — [ironclaw](https://github.com/nearai/ironclaw)

`nearai/ironclaw` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/nearai/ironclaw/)

Treats agent execution as a privacy and isolation problem rather than a convenience one. Two source lists agree, and Windows support is documented rather than assumed.

> NEAR AI's open-source agent OS that treats agent execution as a privacy-first harness problem: untrusted tools run in WASM sandboxes with capability-based permissions, credentials are injected at the host boundary with leak detection, and prompt-injection filtering plus endpoint allowlisting constrain agent behavior. The combination of local encrypted storage, hybrid-search memory, MCP server supp

```sh
irm "https://github.com/nearai/ironclaw/releases/download/$IronClawReleaseTag/ironclaw-installer.ps1" | iex
```

**12,603** stars · 2 of 11 lists · Rust · Apache-2.0 · pushed 2026-09-02

Platforms: Win Y WSL Y mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Sandbox, Security & Governance · Targets: MCP

---

These are editorial picks — the only editorial pages on the atlas. Everything else here is what 11 awesome-lists agreed on. The curation is a [reviewable file](https://github.com/crazy54/awesome-agentic-atlas/blob/main/config/collections.json); open an issue if you would pick differently.
