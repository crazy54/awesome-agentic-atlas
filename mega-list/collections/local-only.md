# Nothing leaves the laptop

*A local stack, top to bottom*

Sometimes the requirement is not cost or latency but that the code, the documents and the prompts stay on hardware you own. That rules out most of the atlas. What is left is a genuine stack: an engine, a runner in front of it, a chat surface, a serving layer for when one machine is not enough, and retrieval over your own files. Every project below names a local runtime as a target, and the build checks it.

7 picks · 674,104 combined stars · snapshot 2026-09-03

[Open all 7 in the atlas](https://crazy54.github.io/awesome-agentic-atlas/#list=ollama/ollama,ggml-org/llama.cpp,mozilla-ai/llamafile,open-webui/open-webui,nomic-ai/gpt4all,PromtEngineer/localGPT,vllm-project/vllm) — from there you can save them to your own projects or export the set as Markdown, HTML or a PDF.

> Every pick is checked at build time: `target` = `local-ollama`. If the committed snapshot stops supporting that for any one of them, this page fails to build rather than quietly meaning something weaker.

---

## 1. The runner — [Ollama](https://github.com/ollama/ollama)

`ollama/ollama` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/ollama/ollama/)

Pull a model, run it, done. It is the layer that made local models an afternoon rather than a weekend, and it stays out of the way afterwards.

> Run LLMs locally. 162k+ stars. Dead simple CLI

```sh
irm https://ollama.com/install.ps1 | iex
```

**180,046** stars · 1 list · Go · MIT · pushed 2026-09-03

Platforms: Win Y WSL L mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

## 2. The engine — [llama.cpp](https://github.com/ggml-org/llama.cpp)

`ggml-org/llama.cpp` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/ggml-org/llama.cpp/)

CPU, GPU and Apple Silicon inference in C++, and the foundation most of the rest of this page is standing on. Quantisation happens here, which is where the speed comes from.

> C/C++ inference. CPU, GPU, Apple Silicon. Foundation of local AI

```sh
git clone https://github.com/ggml-org/llama.cpp.git
```

**126,906** stars · 1 list · C++ · MIT · pushed 2026-09-03

Platforms: Win Y WSL N mac Y Lin N Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

## 3. The zero-setup option — [Llamafile](https://github.com/mozilla-ai/llamafile)

`mozilla-ai/llamafile` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/mozilla-ai/llamafile/)

A model and its runtime as one executable file. Nothing to install and nothing to uninstall, which makes it the right thing to hand to somebody else.

> LLMs as single files. Zero setup. Mozilla

```sh
git clone https://github.com/Mozilla-Ocho/llamafile.git
```

**25,866** stars · 1 list · C++ · no licence stated · pushed 2026-08-26

Platforms: Win Y WSL L mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

## 4. The chat surface — [Open WebUI](https://github.com/open-webui/open-webui)

`open-webui/open-webui` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/open-webui/open-webui/)

A self-hosted interface with access control and extensions, so the local stack has a front door other people can be given a key to.

> Self-hosted ChatGPT UI. Access control. Extensions

```sh
pip install open-webui
```

**150,810** stars · 1 list · Python · no licence stated · pushed 2026-09-02

Platforms: Win L WSL Y mac L Lin L Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: MCP, Codex / OpenAI, Local / Ollama

---

## 5. The consumer-hardware path — [GPT4All](https://github.com/nomic-ai/gpt4all)

`nomic-ai/gpt4all` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/nomic-ai/gpt4all/)

Built for the machine you already have rather than the one you would need. Worth trying first if the honest answer about your GPU is that there isn't one.

> OSS local chat. Consumer hardware

```sh
pip install gpt4all
```

**77,386** stars · 1 list · C++ · MIT · pushed 2025-05-27

Platforms: Win Y WSL L mac Y Lin Y Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

## 6. Your own documents — [Local GPT](https://github.com/PromtEngineer/localGPT)

`PromtEngineer/localGPT` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/promtengineer/localgpt/)

Retrieval over local files with a local model doing the reading, which is the whole point: the documents never become somebody else's training data. Two source lists carry it.

> Inspired on Private GPT with the GPT4ALL model replaced with the Vicuna-7B model and using the InstructorEmbeddings instead of LlamaEmbeddings

```sh
git clone https://github.com/PromtEngineer/localGPT.git
```

**22,206** stars · 2 of 11 lists · Python · MIT · pushed 2026-08-26

Platforms: Win L WSL Y mac L Lin Y Doc Y  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Context, Memory & RAG · Targets: Local / Ollama

---

## 7. When one machine is not enough — [vLLM](https://github.com/vllm-project/vllm)

`vllm-project/vllm` · [detail page](https://crazy54.github.io/awesome-agentic-atlas/repo/vllm-project/vllm/)

High-throughput serving with paged attention. This is the step after a laptop -- still your hardware, but now several people can use it at once.

> High-throughput serving. PagedAttention. Production-grade

```sh
git clone https://github.com/vllm-project/vllm.git
```

**90,884** stars · 1 list · Python · Apache-2.0 · pushed 2026-09-03

Platforms: Win L WSL L mac L Lin L Doc N  (Y stated · L inferred · N no evidence · a n/a · - unknown)

Topic: Harnesses & Runtime Infra · Targets: Local / Ollama

---

These are editorial picks — the only editorial pages on the atlas. Everything else here is what 11 awesome-lists agreed on. The curation is a [reviewable file](https://github.com/crazy54/awesome-agentic-atlas/blob/main/config/collections.json); open an issue if you would pick differently.
