# LLMOps (InftyAI)

🎉 An awesome & curated list of best LLMOps tools.

Curated by **[InftyAI/Awesome-LLMOps](https://github.com/InftyAI/Awesome-LLMOps)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

233 entries · 231 distinct repos · 26 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/ollama/ollama"><img src="https://opengraph.githubassets.com/1/ollama/ollama" width="260"></a> | <a href="https://github.com/ggml-org/llama.cpp"><img src="https://github.com/user-attachments/assets/88726b48-1713-48aa-a525-95a02e78afc4" width="260"></a> | <a href="https://github.com/vllm-project/vllm"><img src="https://opengraph.githubassets.com/1/vllm-project/vllm" width="260"></a> |
| **[Ollama](https://github.com/ollama/ollama)**<br>★ 181.5k | **[llama.cpp](https://github.com/ggml-org/llama.cpp)**<br>★ 129.2k | **[vLLM](https://github.com/vllm-project/vllm)**<br>★ 92.4k |
| <a href="https://github.com/sgl-project/sglang"><img src="https://raw.githubusercontent.com/sgl-project/sgl-learning-materials/refs/heads/main/slides/adoption.png" width="260"></a> | <a href="https://github.com/tinygrad/tinygrad"><img src="https://opengraph.githubassets.com/1/tinygrad/tinygrad" width="260"></a> | <a href="https://github.com/modular/modular"><img src="https://opengraph.githubassets.com/1/modular/modular" width="260"></a> |
| **[SGLang](https://github.com/sgl-project/sglang)**<br>★ 36.3k | **[TinyGrad](https://github.com/tinygrad/tinygrad)**<br>★ 33.6k | **[Modular](https://github.com/modular/modular)**<br>★ 29.8k |

## Contents

- [Inference Engine](#inference-engine) (26)
- [Inference Platform](#inference-platform) (12)
- [Middleware](#middleware) (4)
- [Simulator](#simulator) (1)
- [LLM Router](#llm-router) (15)
- [AI Gateway](#ai-gateway) (9)
- [Agent Framework](#agent-framework) (19)
- [Tool](#tool) (12)
- [Output](#output) (4)
- [AI Terminal](#ai-terminal) (7)
- [AI Agent](#ai-agent) (5)
- [Code Agent](#code-agent) (5)
- [Workflow](#workflow) (16)
- [Evolutionary Framework](#evolutionary-framework) (7)
- [Evolve Agent](#evolve-agent) (2)
- [RAG](#rag) (7)
- [Database](#database) (6)
- [FineTune](#finetune) (10)
- [Framework](#framework) (7)
- [Agentic RL](#agentic-rl) (4)
- [RLHF](#rlhf) (2)
- [Chatbot](#chatbot) (14)
- [Sandbox](#sandbox) (2)
- [Application Framework](#application-framework) (14)
- [Benchmark](#benchmark) (13)
- [Observation](#observation) (10)

## Inference Engine

- **[Ollama](https://github.com/ollama/ollama)** — Get up and running with Llama 3.3, DeepSeek-R1, Phi-4, Gemma 3, and other large language models
  <sub>★ 181.5k · Go · MIT · psh · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://ollama.com/install.ps1 | iex`</sub>
- **[llama.cpp](https://github.com/ggml-org/llama.cpp)** — LLM inference in C/C++
  <sub>★ 129.2k · C++ · MIT · source · pushed 2026-09-22 · Win · macOS</sub>
  <sub>`git clone https://github.com/ggerganov/llama.cpp.git`</sub>
- **[vLLM](https://github.com/vllm-project/vllm)** — A high-throughput and memory-efficient inference and serving engine for LLMs
  <sub>★ 92.4k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vllm-project/vllm.git`</sub>
- **[SGLang](https://github.com/sgl-project/sglang)** — SGLang is a fast serving framework for large language models and vision language models
  <sub>★ 36.3k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/sgl-project/sglang.git`</sub>
- **[TinyGrad](https://github.com/tinygrad/tinygrad)** — You like pytorch? You like micrograd? You love tinygrad! ❤️
  <sub>★ 33.6k · Python · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tinygrad/tinygrad.git`</sub>
- **[MLC LLM](https://github.com/mlc-ai/mlc-llm)** — Universal LLM Deployment Engine with ML Compilation
  <sub>★ 23.2k · Python · Apache-2.0 · source · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mlc-ai/mlc-llm.git`</sub>
- **[web-llm](https://github.com/mlc-ai/web-llm)** — High-performance In-browser LLM Inference Engine
  <sub>★ 19.2k · TypeScript · Apache-2.0 · clone · pushed 2026-09-15 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mlc-ai/relax`</sub>
- **[transformers.js](https://github.com/huggingface/transformers.js)** — State-of-the-art Machine Learning for the web. Run 🤗 Transformers directly in your browser, with no need for a server!
  <sub>★ 16.3k · JavaScript · Apache-2.0 · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/huggingface/transformers.js.git`</sub>
- **[OpenLLM](https://github.com/bentoml/OpenLLM)** — Run any open-source LLMs, such as DeepSeek and Llama, as OpenAI compatible API endpoint in the cloud
  <sub>★ 12.5k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openllm # or pip3 install openllm`</sub>
- **[Triton Inference Server](https://github.com/triton-inference-server/server)** — The Triton Inference Server provides an optimized cloud and edge inferencing solution
  <sub>★ 11k · Python · BSD-3-Clause · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/triton-inference-server/server.git`</sub>
- **[OpenVINO](https://github.com/openvinotoolkit/openvino)** — OpenVINO™ is an open source toolkit for optimizing and deploying AI inference
  <sub>★ 10.9k · C++ · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U openvino`</sub>
- **[Text Generation Inference](https://github.com/huggingface/text-generation-inference)** — Large Language Model Text Generation Inference
  <sub>★ 10.9k · Python · Apache-2.0 · clone · pushed 2026-03-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/huggingface/text-generation-inference`</sub>
- **[Petals](https://github.com/bigscience-workshop/petals)** — Run LLMs at home, BitTorrent-style. Fine-tuning and inference up to 10x faster than offloading
  <sub>★ 10.6k · Python · MIT · pip · pushed 2024-09-07 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install git+https://github.com/bigscience-workshop/petals`</sub>
- **[Xinference](https://github.com/xorbitsai/inference)** — Replace OpenAI GPT with another LLM in your app by changing a single line of code. Xinference gives you the freedom to use any LLM you need. With Xinference, you're empowered to run inference with any open-source language models, speech recognition models, and multimodal models, whether in the cloud, on-premises, or even on your laptop
  <sub>★ 9.6k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "xinference[all]"`</sub>
- **[ipex-llm](https://github.com/intel/ipex-llm)** — Accelerate local LLM inference and finetuning (LLaMA, Mistral, ChatGLM, Qwen, DeepSeek, Mixtral, Gemma, Phi, MiniCPM, Qwen-VL, MiniCPM-V, etc.) on Intel XPU (e.g., local PC with iGPU and NPU, discrete GPU such as Arc, Flex and Max); seamlessly integrate with llama.cpp, Ollama, HuggingFace, LangChain, LlamaIndex, vLLM, DeepSpeed, Axolotl, etc
  <sub>★ 8.9k · Python · Apache-2.0 · source · pushed 2026-01-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/intel-analytics/ipex-llm.git`</sub>
- **[Nvidia Dynamo](https://github.com/ai-dynamo/dynamo)** — A Datacenter Scale Distributed Inference Serving Framework
  <sub>★ 8.1k · Rust · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --gpus all --network host --rm -it nvcr.io/nvidia/ai-dynamo/sglang-runtime:1.5.0`</sub>
- **[LMDeploy](https://github.com/InternLM/lmdeploy)** — LMDeploy is a toolkit for compressing, deploying, and serving LLMs
  <sub>★ 8.1k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`pip install lmdeploy`</sub>
- **[zml](https://github.com/zml/zml)** — Any model. Any hardware. Zero compromise. Built with @ziglang / @openxla / MLIR / @bazelbuild
  <sub>★ 4.1k · Zig · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zml/zml.git`</sub>
- **[LoRAX](https://github.com/predibase/lorax)** — Multi-LoRA inference server that scales to 1000s of fine-tuned LLMs
  <sub>★ 3.8k · Python · Apache-2.0 · pip · pushed 2026-05-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install lorax-client`</sub>
- **[Cortex.cpp](https://github.com/janhq/cortex.cpp)** — Local AI API Platform
  <sub>★ 2.8k · C++ · Apache-2.0 · script · pushed 2025-07-04 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -s https://raw.githubusercontent.com/menloresearch/cortex/main/engine/templates/linux/install.sh | sudo bash`</sub>
- **[DeepSpeed-MII](https://github.com/deepspeedai/DeepSpeed-MII)** — MII makes low-latency and high-throughput inference possible, powered by DeepSpeed
  <sub>★ 2.1k · Python · Apache-2.0 · pip · pushed 2025-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install deepspeed-mii`</sub>
- **[MInference](https://github.com/microsoft/MInference)** — [NeurIPS'24 Spotlight, ICLR'25] To speed up Long-context LLMs' inference, approximate and dynamic sparse calculate the attention, which reduces inference latency by up to 10x for pre-filling on an A100 while maintaining accuracy
  <sub>★ 1.2k · Python · MIT · pip · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`pip install minference`</sub>
- **[MLServer](https://github.com/SeldonIO/MLServer)** — An inference server for your machine learning models, including support for multiple frameworks, multi-model serving and more
  <sub>★ 900 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mlserver`</sub>
- **[Ratchet](https://github.com/huggingface/ratchet)** — A cross-platform browser ML framework
  <sub>★ 771 · Rust · MIT · source · pushed 2026-09-17 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/huggingface/ratchet.git`</sub>
- **[Llumnix](https://github.com/llumnix-project/llumnix-ray)** — Efficient and easy multi-instance LLM serving
  <sub>★ 562 · Python · Apache-2.0 · source · pushed 2026-03-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/AlibabaPAI/llumnix.git`</sub>
- **[llama-box](https://github.com/gpustack/llama-box)** — LM inference server implementation based on *.cpp
  <sub>★ 292 · C++ · MIT · source · pushed 2025-11-24 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/gpustack/llama-box.git`</sub>

## Inference Platform

- **[Modular](https://github.com/modular/modular)** — The Modular Platform (includes MAX &amp; Mojo)
  <sub>★ 29.8k · Mojo · source · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/modular/modular.git`</sub>
- **[BentoML](https://github.com/bentoml/BentoML)** — The easiest way to serve AI apps and models - Build Model Inference APIs, Job queues, LLM apps, Multi-model pipelines, and more!
  <sub>★ 8.9k · Python · Apache-2.0 · pip · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -U bentoml`</sub>
- **[Mooncake](https://github.com/kvcache-ai/Mooncake)** — Mooncake is the serving platform for Kimi, a leading LLM service provided by Moonshot AI
  <sub>★ 6.6k · C++ · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`pip install mooncake-transfer-engine`</sub>
- **[Kserve](https://github.com/kserve/kserve)** — Standardized Serverless ML Inference Platform on Kubernetes
  <sub>★ 6k · Go · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kserve/kserve.git`</sub>
- **[AIBrix](https://github.com/vllm-project/aibrix)** — Cost-efficient and pluggable Infrastructure components for GenAI inference
  <sub>★ 5.1k · Go · Apache-2.0 · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vllm-project/aibrix.git`</sub>
- **[llm-d](https://github.com/llm-d/llm-d)** — llm-d is a Kubernetes-native high-performance distributed LLM inference framework
  <sub>★ 4.6k · Shell · Apache-2.0 · source · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/llm-d/llm-d.git`</sub>
- **[beta9](https://github.com/beam-cloud/beta9)** — Ultrafast serverless GPU inference, sandboxes, and background jobs
  <sub>★ 1.8k · Go · AGPL-3.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install beam-client`</sub>
- **[KubeAI](https://github.com/kubeai-project/kubeai)** — AI Inference Operator for Kubernetes. The easiest way to serve ML models in production. Supports VLMs, LLMs, embeddings, and speech-to-text
  <sub>★ 1.3k · Go · Apache-2.0 · helm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`helm install kubeai kubeai/kubeai --wait --timeout 10m`</sub>
- **[OME](https://github.com/ome-projects/ome)** — OME is a Kubernetes operator for enterprise-grade management and serving of Large Language Models (LLMs)
  <sub>★ 511 · Go · Apache-2.0 · helm · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`helm install ome-crd charts/ome-crd --namespace ome --create-namespace`</sub>
- **[llmaz](https://github.com/InftyAI/llmaz)** — Easy, advanced inference platform for large language models on Kubernetes. 🌟 Star to support our work!
  <sub>★ 315 · Go · Apache-2.0 · source · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/InftyAI/llmaz.git`</sub>
- **[Kaito](https://github.com/kaito-project/kaito)** — Kubernetes operator for large-model inference and fine-tuning, with GPU auto-provisioning, container-based hosting, and CRD-based orchestration
  <sub>source</sub>
  <sub>`git clone https://github.com/kaito-project/Kaito.git`</sub>
- **[Paralleliq](https://www.paralleliq.ai)** — Model-aware GPU optimization layer for AI inference clusters. Understands which model runs on which GPU to identify waste and risk — tier misplacement, dark capacity, OOM risk, and CPU:GPU imbalance — with human-in-the-loop approval workflows and a full audit trail
  <sub>website</sub>
  <sub>`https://www.paralleliq.ai`</sub>

## Middleware

- **[LMCache](https://github.com/LMCache/LMCache)** — 10x Faster Long-Context LLM By Smart KV Cache Optimizations
  <sub>★ 11.9k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lmcache`</sub>
- **[kvcached](https://github.com/ovg-project/kvcached)** — Virtualized Elastic KV Cache for Dynamic GPU Sharing and Beyond
  <sub>★ 1.5k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install kvcached --no-build-isolation`</sub>
- **[Checkpoint Engine](https://github.com/MoonshotAI/checkpoint-engine)** — Checkpoint-engine is a simple middleware to update model weights in LLM inference engines
  <sub>★ 1k · Python · MIT · pip · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install checkpoint-engine`</sub>
- **[KV Cache Store](https://kvcachestore.com/)** — Hosted KV-cache artifact registry plus an open-source Rust CLI. Precompute, verify, quantize, and share attention states across RAG and long-context prompts to cut prefill cost and latency. (CLI source)
  <sub>website</sub>
  <sub>`https://kvcachestore.com/`</sub>

## Simulator

- **[Vidur](https://github.com/microsoft/vidur)** — A large-scale simulation framework for LLM inference
  <sub>★ 683 · Python · MIT · source · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/vidur.git`</sub>

## LLM Router

- **[LiteLLM](https://github.com/BerriAI/litellm)** — Python SDK, Proxy Server (LLM Gateway) to call 100+ LLM APIs in OpenAI format - [Bedrock, Azure, OpenAI, VertexAI, Cohere, Anthropic, Sagemaker, HuggingFace, Replicate, Groq]
  <sub>★ 59.4k · Python · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install 'litellm[proxy]'`</sub>
- **[AI Gateway](https://github.com/Portkey-AI/gateway)** — A blazing fast AI Gateway with integrated guardrails. Route to 200+ LLMs, 50+ AI Guardrails with 1 fast &amp; friendly API
  <sub>★ 13.1k · TypeScript · MIT · npx · pushed 2026-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @portkey-ai/gateway`</sub>
- **[bifrost](https://github.com/maximhq/bifrost)** — Fastest LLM gateway (50x faster than LiteLLM) with adaptive load balancer, cluster mode, guardrails, 1000+ models support &amp; &lt;100 µs overhead at 5k RPS
  <sub>★ 8.2k · Go · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @maximhq/bifrost`</sub>
- **[vLLM Semantic Router](https://github.com/vllm-project/semantic-router)** — Intelligent Mixture-of-Models Router for Efficient LLM Inference
  <sub>★ 5.9k · Go · Apache-2.0 · script · pushed 2026-09-22 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://vllm-sr.ai/install.sh | bash -s -- --channel stable`</sub>
- **[RouteLLM](https://github.com/lm-sys/RouteLLM)** — A framework for serving and evaluating LLM routers - save LLM costs without compromising quality
  <sub>★ 5.5k · Python · Apache-2.0 · pip · pushed 2024-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "routellm[serve,eval]"`</sub>
- **[LLMRouter](https://github.com/ulab-uiuc/LLMRouter)** — LLMRouter: An Open-Source Library for LLM Routing
  <sub>★ 3k · Python · MIT · pip · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llmrouter-lib`</sub>
- **[Otari](https://github.com/mozilla-ai/otari)** — Open-source, OpenAI-compatible LLM gateway you run yourself. One endpoint for 40+ providers, with virtual keys, budgets, and usage tracking
  <sub>★ 485 · Python · Apache-2.0 · clone · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/mozilla-ai/otari`</sub>
- **[Ferro Labs AI Gateway](https://github.com/ferro-labs/ai-gateway)** — One API for 25+ LLMs, OpenAI, Anthropic, Bedrock, Azure. Caching, guardrails &amp; cost controls. Go-native LiteLLM &amp; Kong AI Gateway alternative
  <sub>★ 264 · Go · Apache-2.0 · scoop · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop bucket add ferrolabs https://github.com/ferro-labs/homebrew-tap scoop install ferrogw`</sub>
- **[Doubleword Control Layer](https://github.com/doublewordai/control-layer)** — The world’s fastest AI model gateway (450x less overhead than LiteLLM). Unified access to LLMs across endpoints (openAI, self-hosted, etc.) behind a single authentication layer - with API key generation, user management, request logging, and more
  <sub>★ 94 · Rust · Apache-2.0 · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/doublewordai/control-layer.git`</sub>
- **[Hebo AI Gateway](https://github.com/8monkey-ai/hebo-gateway/)** — OpenAI-compatible /chat/completions, /embeddings &amp; /models endpoints
  <sub>★ 26 · TypeScript · source · pushed 2026-09-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/8monkey-ai/hebo-gateway/.git`</sub>
- **[llm-swarm-router](https://github.com/matthewdcage/llm-swarm-router)** — Self-hosted mesh router for local LLM backends — OpenAI /v1 + Anthropic Messages on :11400, mDNS LAN peers. Complements cloud gateways with local LAN mesh for Cursor, Claude Code, Codex, and Honcho
  <sub>★ 25 · Python · MIT · brew · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew tap matthewdcage/netllm https://github.com/matthewdcage/llm-swarm-router`</sub>
- **[Ollama Herd](https://github.com/geeks-accelerator/ollama-herd)** — Routes LLM, image, speech-to-text and embedding requests across a fleet of machines you own. Auto-discovers nodes over mDNS and scores each on memory fit, thermal state, queue depth and already-loaded models. OpenAI-, Ollama- and Anthropic-compatible
  <sub>★ 21 · Python · MIT · pip · pushed 2026-09-08 · macOS</sub>
  <sub>`pip install ollama-herd`</sub>
- **[Swobu](https://github.com/swobuforge/swobu)** — Local AI gateway for routing clients across providers, regions, accounts, and local models
  <sub>★ 18 · Go · AGPL-3.0 · psh · pushed 2026-09-19 · Win · WSL2 · macOS · Linux</sub>
  <sub>`irm https://swobu.com/install.ps1 | iex`</sub>
- **[OpenPaths](https://github.com/lee101/openpaths)** — Open-source, OpenAI-compatible model router/AI gateway routing chat, image, video, music, speech, transcription, embeddings and reasoning models to the lowest-latency provider via a unified API
  <sub>★ 3 · TypeScript · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lee101/openpaths.git`</sub>
- **[llm-cache-router](https://github.com/svalench/llm-cache-router)** — A lightweight, async-first Python library combining semantic caching, multi-provider routing (OpenAI, Anthropic, Gemini, Ollama, MiniMax, Qwen) and cost tracking. Cuts LLM spend 30-70% via vector-similarity cache with in-memory/Redis/Qdrant backends
  <sub>★ 2 · Python · MIT · pip · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install llm-cache-router`</sub>

## AI Gateway

- **[Kong](https://github.com/Kong/kong)** — The Cloud-Native API Gateway and AI Gateway
  <sub>★ 44.2k · Lua · Apache-2.0 · source · pushed 2026-09-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/Kong/kong.git`</sub>
- **[APISIX](https://github.com/apache/apisix)** — The Cloud-Native API Gateway and AI Gateway with extensive plugin system and AI capabilities
  <sub>★ 17.2k · Lua · Apache-2.0 · script · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -sL https://run.api7.ai/apisix/quickstart | sh`</sub>
- **[Higress](https://github.com/higress-group/higress)** — AI Gateway | AI Native API Gateway
  <sub>★ 9.4k · Go · Apache-2.0 · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --rm --name higress-ai -v ${PWD}:/data \`</sub>
- **[kgateway](https://github.com/kgateway-dev/kgateway)** — The Cloud-Native API Gateway and AI Gateway
  <sub>★ 5.7k · Go · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/kgateway-dev/kgateway.git`</sub>
- **[agentgateway](https://github.com/agentgateway/agentgateway)** — Next Generation Agentic Proxy for AI Agents and MCP servers
  <sub>★ 5k · Rust · Apache-2.0 · source · pushed 2026-09-22 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/agentgateway/agentgateway.git`</sub>
- **[Envoy AI Gateway](https://github.com/theagentrouter/agent-router)** — Envoy AI Gateway is an open source project for using Envoy Gateway to handle request traffic from application clients to Generative AI services
  <sub>★ 2.1k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/envoyproxy/ai-gateway.git`</sub>
- **[gateway-api-inference-extension](https://github.com/kubernetes-sigs/gateway-api-inference-extension)** — Gateway API Inference Extension
  <sub>★ 770 · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kubernetes-sigs/gateway-api-inference-extension.git`</sub>
- **[Gram](https://github.com/speakeasy-api/gram)** — Open-source AI control plane for connecting agents to MCPs with role-scoped access, policy enforcement, threat detection, and observability
  <sub>★ 270 · Go · AGPL-3.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/speakeasy-api/gram.git`</sub>
- **[TrustGate](https://github.com/NeuralTrust/TrustGate)** — Self-hosted Go Agent Gateway (Apache-2.0) — OpenAI-compatible LLM proxy + MCP aggregation with per-consumer auth/audit
  <sub>★ 10 · Go · Apache-2.0 · script · pushed 2026-09-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/NeuralTrust/TrustGate/main/scripts/install.sh | bash`</sub>

## Agent Framework

- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** — AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters
  <sub>★ 187.5k · Python · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Significant-Gravitas/AutoGPT.git`</sub>
- **[MetaGPT](https://github.com/FoundationAgents/MetaGPT)** — The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming
  <sub>★ 70.6k · Python · MIT · pip · pushed 2026-01-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade metagpt`</sub>
- **[autogen](https://github.com/microsoft/autogen)** — A programming framework for agentic AI
  <sub>★ 61.1k · Python · CC-BY-4.0 · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "autogen-agentchat" "autogen-ext[openai]"`</sub>
- **[crewAI](https://github.com/crewAIInc/crewAI)** — Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks
  <sub>★ 58.9k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add crewaiinc/skills`</sub>
- **[Flowise](https://github.com/FlowiseAI/Flowise)** — Build AI Agents, Visually
  <sub>★ 55.5k · TypeScript · npm · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g flowise`</sub>
- **[Agno](https://github.com/agno-agi/agno)** — Open-source framework for building multi-agent systems with memory, knowledge and reasoning
  <sub>★ 42.3k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/agno-agi/agno.git`</sub>
- **[LangGraph](https://github.com/langchain-ai/langgraph)** — Build resilient language agents as graphs
  <sub>★ 42.1k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U langgraph`</sub>
- **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** — A lightweight, powerful framework for multi-agent workflows
  <sub>★ 29.6k · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openai-agents`</sub>
- **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** — Integrate cutting-edge LLM technology quickly and easily into your apps
  <sub>★ 28.6k · C# · MIT · pip · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install semantic-kernel`</sub>
- **[Swarm](https://github.com/openai/swarm)** — Educational framework exploring ergonomic, lightweight multi-agent orchestration. Managed by OpenAI Solution team
  <sub>★ 22k · Python · MIT · pip · pushed 2026-04-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+ssh://git@github.com/openai/swarm.git`</sub>
- **[Agent Development Kit (ADK)](https://github.com/google/adk-python)** — An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control
  <sub>★ 21.6k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/google/adk-python.git@main`</sub>
- **[Suna](https://github.com/kortix-ai/suna)** — Suna - Open Source Generalist AI Agent
  <sub>★ 20.2k · TypeScript · script · pushed 2026-09-22 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://kortix.com/install | bash`</sub>
- **[PydanticAI](https://github.com/pydantic/pydantic-ai)** — GenAI Agent Framework, the Pydantic way
  <sub>★ 20.1k · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx --with pydantic-ai-harness clai -a pydantic_ai_harness.coder:coder_agent -m anthropic:claude-fable-5`</sub>
- **[CAMEL](https://github.com/camel-ai/camel)** — CAMEL: The first and the best multi-agent framework. Finding the Scaling Law of Agents
  <sub>★ 17.8k · Python · Apache-2.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install camel-ai`</sub>
- **[Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)** — Agent framework and applications built upon Qwen>=3.0, featuring Function Calling, MCP, Code Interpreter, RAG, Chrome extension, etc
  <sub>★ 17.1k · Python · Apache-2.0 · pip · pushed 2026-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U "qwen-agent[gui,rag,code_interpreter,mcp]"`</sub>
- **[fast-agent](https://github.com/evalstate/fast-agent)** — Define, Prompt and Test MCP enabled Agents and Workflows
  <sub>★ 3.9k · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx fast-agent-mcp@latest -x`</sub>
- **[kagent](https://github.com/kagent-dev/kagent)** — kagent is a kubernetes native framework for building AI agents
  <sub>★ 3.8k · Go · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/kagent-dev/kagent.git`</sub>
- **[AgentField](https://github.com/Agent-Field/agentfield)** — Framework for AI Backend. Build and run AI agents like microservices - scalable, observable, and identity-aware from day one
  <sub>★ 2.6k · Go · Apache-2.0 · script · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentfield.ai/install.sh | bash`</sub>
- **[Agent Shadow Brain](https://github.com/theihtisham/agent-shadow-brain)** — Self-evolving AI coding intelligence with infinite memory (TurboQuant), genetic algorithm evolution, predictive bug detection, PageRank knowledge graphs, and swarm intelligence. The world's first autonomous coding brain
  <sub>unavailable</sub>

## Tool

- **[Browser Use](https://github.com/browser-use/browser-use)** — Make websites accessible for AI agents
  <sub>★ 115.9k · Python · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/browser-use/browser-use.git`</sub>
- **[Mem0](https://github.com/mem0ai/mem0)** — The Memory layer for AI Agents
  <sub>★ 65.8k · Python · Apache-2.0 · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @mem0/cli # or: pip install mem0-cli`</sub>
- **[Graphiti](https://github.com/getzep/graphiti)** — Build Real-Time Knowledge Graphs for AI Agents
  <sub>★ 31.1k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install graphiti-core`</sub>
- **[Beads](https://github.com/gastownhall/beads)** — Beads - A memory upgrade for your coding agent
  <sub>★ 27.4k · Go · MIT · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @beads/bd # Node.js users`</sub>
- **[Webcmd](https://github.com/agentrhq/webcmd)** — Self-learning browser infrastructure for AI agents that compiles a site's navigation into deterministic per-site CLI commands
  <sub>★ 2.3k · TypeScript · Apache-2.0 · npm · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @agentrhq/webcmd`</sub>
- **[OpenAI CUA](https://github.com/openai/openai-cua-sample-app)** — Computer Using Agent Sample App
  <sub>★ 1.9k · TypeScript · MIT · clone · pushed 2026-09-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/openai/openai-cua-sample-app.git`</sub>
- **[deja](https://github.com/vshulcz/deja-vu)** — Shared session memory for coding agents, read from the transcripts 25 agents already write on the machine — no writes to a memory store, no embeddings, one local Go binary
  <sub>★ 921 · Go · MIT · scoop · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`scoop install deja-vu`</sub>
- **[Vestige](https://github.com/samvallad33/vestige)** — Local-first cognitive memory MCP server for AI coding agents. SQLite, FSRS-6 retention with active forgetting and prediction-error gating
  <sub>★ 628 · Rust · AGPL-3.0 · npm · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g vestige-mcp-server@latest`</sub>
- **[SidClaw](https://github.com/sidclawhq/platform)** — The approval and accountability layer for AI agents. Identity → Policy → Approval → Trace. 13 framework integrations. Free during early access
  <sub>★ 14 · TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx sidclaw-demo`</sub>
- **[WritBase](https://github.com/Writbase/writbase)** — MCP-native task management for AI agent fleets
  <sub>★ 10 · TypeScript · Apache-2.0 · npx · pushed 2026-03-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx writbase init # Interactive setup — configures Supabase credentials`</sub>
- **[Model Catalog](https://github.com/openviglet/model-catalog)** — A vendor-neutral, kind-aware catalog of LLM/embedding/rerank/media model ids and their capabilities (context window, modalities), served as a free, unauthenticated, versioned JSON API
  <sub>★ 2 · JavaScript · Apache-2.0 · pip · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openviglet-model-catalog-client`</sub>
- **[Agent-Ready Repository Auditor](https://github.com/wrightops-ai/agent-ready-repo-auditor)** — Free GitHub Action that scores public repositories for Codex, Claude Code, Copilot, and Cursor readiness—without cloning or executing code
  <sub>Python · MIT · gh-action · pushed 2026-07-25</sub>
  <sub>`uses: wrightops-ai/agent-ready-repo-auditor@main # in .github/workflows/*.yml`</sub>

## Output

- **[Outlines](https://github.com/dottxt-ai/outlines)** — Structured Text Generation
  <sub>★ 15.9k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install outlines`</sub>
- **[Instructor](https://github.com/567-labs/instructor)** — structured outputs for llms
  <sub>★ 13.9k · Python · MIT · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install instructor`</sub>
- **[BAML](https://github.com/BoundaryML/baml)** — The AI framework that adds the engineering to prompt engineering (Python/TS/Ruby/Java/C#/Rust/Go compatible)
  <sub>★ 9.3k · Rust · Apache-2.0 · brew · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install baml`</sub>
- **[XGrammar](https://github.com/mlc-ai/xgrammar)** — Fast, Flexible and Portable Structured Generation
  <sub>★ 1.9k · C++ · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install xgrammar`</sub>

## AI Terminal

- **[OpenCode](https://github.com/anomalyco/opencode)** — The AI coding agent built for the terminal
  <sub>★ 209.3k · TypeScript · MIT · scoop · pushed 2026-09-22 · macOS · Linux</sub>
  <sub>`scoop install opencode # Windows`</sub>
- **[Codex](https://github.com/openai/codex)** — Lightweight coding agent that runs in your terminal
  <sub>★ 125.9k · Rust · Apache-2.0 · npm · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npm install -g @openai/codex`</sub>
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — An open-source AI agent that brings the power of Gemini directly into your terminal
  <sub>★ 107.1k · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @google/gemini-cli`</sub>
- **[aider](https://github.com/Aider-AI/aider)** — aider is AI pair programming in your terminal
  <sub>★ 49.1k · Python · Apache-2.0 · source · pushed 2026-05-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Aider-AI/aider.git`</sub>
- **[Crush](https://github.com/charmbracelet/crush)** — The glamourous AI coding agent for your favourite terminal 💘
  <sub>★ 28.2k · Go · winget · pushed 2026-09-22 · Win · WSL2 · macOS · Linux</sub>
  <sub>`winget install charmbracelet.crush`</sub>
- **[Atomic Agent](https://github.com/AtomicBot-ai/atomic-agent)** — Local-first CLI and TUI coding agent that runs open-weight models entirely on your machine through a llama.cpp fork, with no account or API key required. 56 built-in tools, MCP support, and a five-layer local memory system. Currently a developer preview
  <sub>★ 2.5k · TypeScript · MIT · psh · pushed 2026-09-22 · macOS</sub>
  <sub>`irm https://atomicagent.io/install.ps1 | iex`</sub>
- **[Stakpak](https://github.com/stakpak/agent)** — DevOps agent that won't accidentally tweet your AWS credentials 🦀
  <sub>★ 1.8k · Rust · Apache-2.0 · brew · pushed 2026-07-06 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew tap stakpak/stakpak`</sub>

## AI Agent

- **[OpenManus](https://github.com/FoundationAgents/OpenManus)** — No fortress, purely open ground. OpenManus is Coming
  <sub>★ 58.4k · Python · MIT · clone · pushed 2026-08-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FoundationAgents/OpenManus.git`</sub>
- **[goose](https://github.com/aaif-goose/goose)** — an open source, extensible AI agent that goes beyond code suggestions - install, execute, edit, and test with any LLM
  <sub>★ 54.5k · Rust · Apache-2.0 · script · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash`</sub>
- **[Tongyi Deep Research](https://github.com/Alibaba-NLP/DeepResearch)** — Tongyi DeepResearch, the Leading Open-source DeepResearch Agent
  <sub>★ 20k · Python · Apache-2.0 · source · pushed 2026-02-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Alibaba-NLP/DeepResearch.git`</sub>
- **[Magentic-UI](https://github.com/microsoft/magentic-ui)** — A research prototype of a human-centered web agent
  <sub>★ 10.1k · Python · MIT · source · pushed 2026-09-19 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/magentic-ui.git`</sub>
- **[Agent QA](https://github.com/vostride/agent-qa)** — Open-source self-improving QA agent for software teams. A test harness with memory. Write tests in natural language for web and mobile. agent-qa learns from every run, adapts to UI changes, and catches regressions before you ship
  <sub>★ 888 · TypeScript · npx · pushed 2026-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx agent-qa init`</sub>

## Code Agent

- **[Continue](https://github.com/continuedev/continue)** — Create, share, and use custom AI code assistants with our open-source IDE extensions and hub of models, rules, prompts, docs, and other building blocks
  <sub>★ 36k · TypeScript · Apache-2.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/continuedev/continue.git`</sub>
- **[Tabby](https://github.com/TabbyML/tabby)** — Self-hosted AI coding assistant
  <sub>★ 33.9k · Rust · source · pushed 2026-06-30 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/TabbyML/tabby.git`</sub>
- **[SWE-agent](https://github.com/SWE-agent/SWE-agent)** — SWE-agent takes a GitHub issue and tries to automatically fix it, using your LM of choice. It can also be employed for offensive cybersecurity or competitive coding challenges. [NeurIPS 2024]
  <sub>★ 20.4k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SWE-agent/SWE-agent.git`</sub>
- **[Open SWE](https://github.com/langchain-ai/open-swe)** — An Open-Source Asynchronous Coding Agent
  <sub>★ 10.7k · Python · MIT · clone · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/open-swe.git`</sub>
- **[Kolega Code](https://github.com/kolega-ai/kolega-code)** — Terminal coding agent where the model writes its own multi-agent workflows (Gigacode); provider-agnostic with MCP support and journaled resume
  <sub>★ 21 · Python · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install kolega-code`</sub>

## Workflow

- **[Dify](https://github.com/langgenius/dify)** — Production-ready platform for agentic workflow development
  <sub>★ 156.8k · TypeScript · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/langgenius/dify.git`</sub>
- **[LangChain](https://github.com/langchain-ai/langchain)** — Build context-aware reasoning applications
  <sub>★ 146.9k · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/langchain-ai/langchain.git`</sub>
- **[LlamaIndex](https://github.com/run-llama/llama_index)** — LlamaIndex is the leading framework for building LLM-powered agents over your data
  <sub>★ 52.3k · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llama-index-core`</sub>
- **[Ray](https://github.com/ray-project/ray)** — Ray is an AI compute engine. Ray consists of a core distributed runtime and a set of AI Libraries for accelerating ML workloads
  <sub>★ 43.9k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ray`</sub>
- **[FastGPT](https://github.com/labring/FastGPT)** — FastGPT is a knowledge-based platform built on the LLMs, offers a comprehensive suite of out-of-the-box capabilities such as data processing, RAG retrieval, and visual AI workflow orchestration, letting you easily develop and deploy complex question-answering systems without the need for extensive setup or configuration
  <sub>★ 29.7k · TypeScript · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/labring/FastGPT.git`</sub>
- **[MLflow](https://github.com/mlflow/mlflow)** — Open source platform for the machine learning lifecycle
  <sub>★ 28.1k · Python · Apache-2.0 · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mlflow server`</sub>
- **[Haystack](https://github.com/deepset-ai/haystack)** — AI orchestration framework to build customizable, production-ready LLM applications. Connect components (models, vector DBs, file converters) to pipelines or agents that can interact with your data. With advanced retrieval methods, it's best suited for building RAG, question answering, semantic search or conversational agent chatbots
  <sub>★ 26.6k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install haystack-ai`</sub>
- **[Kubeflow](https://github.com/kubeflow/kubeflow)** — Machine Learning Toolkit for Kubernetes
  <sub>★ 15.9k · Apache-2.0 · source · pushed 2026-08-21</sub>
  <sub>`git clone https://github.com/kubeflow/kubeflow.git`</sub>
- **[Metaflow](https://github.com/Netflix/metaflow)** — Build, Deploy and Manage AI/ML Systems
  <sub>★ 10.3k · Python · Apache-2.0 · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install metaflow`</sub>
- **[Flyte](https://github.com/flyteorg/flyte)** — Scalable and flexible workflow orchestration platform that seamlessly unifies data, ML and analytics stacks
  <sub>★ 7.5k · Go · Apache-2.0 · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/flyteorg/flyte.git`</sub>
- **[ZenML](https://github.com/zenml-io/zenml)** — ZenML 🙏: The bridge between ML and Ops. https://zenml.io
  <sub>★ 5.6k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "zenml[server]" # pip install zenml will install a slimmer client`</sub>
- **[Seldon-Core](https://github.com/SeldonIO/seldon-core)** — An MLOps framework to package, deploy, monitor and manage thousands of production machine learning models
  <sub>★ 4.8k · Go · source · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SeldonIO/seldon-core.git`</sub>
- **[Polyaxon](https://github.com/polyaxon/polyaxon)** — MLOps Tools For Managing &amp; Orchestrating The Machine Learning LifeCycle
  <sub>★ 3.7k · MDX · Apache-2.0 · source · pushed 2026-09-19</sub>
  <sub>`git clone https://github.com/polyaxon/polyaxon.git`</sub>
- **[Inference](https://github.com/roboflow/inference)** — Turn any computer or edge device into a command center for your computer vision projects
  <sub>★ 2.5k · Python · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install inference-cli`</sub>
- **[Heym](https://github.com/heymrun/heym)** — Source-available, self-hosted visual platform for building, running, evaluating, and observing AI workflows with agents, RAG, and MCP
  <sub>★ 1.2k · Python · clone · pushed 2026-09-21 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/heymrun/heym.git`</sub>
- **[Nika](https://github.com/supernovae-st/nika)** — Intent-as-code AI workflow engine in a single Rust binary — reviewable YAML DAGs statically checked (schema, permits, honest cost floor) before any token is spent, tamper-evident traces after
  <sub>★ 89 · Rust · AGPL-3.0 · brew · pushed 2026-09-22 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew install supernovae-st/tap/nika`</sub>

## Evolutionary Framework

- **[OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve)** — Open-source implementation of AlphaEvolve
  <sub>★ 7.4k · Python · Apache-2.0 · pip · pushed 2026-07-18 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install openevolve`</sub>
- **[AI-Researcher](https://github.com/HKUDS/AI-Researcher)** — [NeurIPS2025] "AI-Researcher: Autonomous Scientific Innovation" -- A production-ready version: https://novix.science/chat
  <sub>★ 5.8k · Python · clone · pushed 2025-10-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/HKUDS/AI-Researcher.git`</sub>
- **[AIDE ML](https://github.com/WecoAI/aideml)** — AIDE: AI-Driven Exploration in the Space of Code. The machine Learning engineering agent that automates AI R&amp;D
  <sub>★ 1.5k · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -U aideml`</sub>
- **[ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve)** — ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution
  <sub>★ 1.4k · Python · Apache-2.0 · npx · pushed 2026-08-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add SakanaAI/ShinkaEvolve --skill '*' -a claude-code -a codex -y`</sub>
- **[LoongFlow](https://github.com/baidu-baige/LoongFlow)** — LoongFlow: A Thinking &amp; Learning Framework for Expert-Grade AI Agents
  <sub>★ 477 · Python · Apache-2.0 · source · pushed 2026-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/baidu-baige/LoongFlow.git`</sub>
- **[Kapso](https://github.com/Leeroo-AI/kapso)** — A self-improving AI software factory (for measurable objectives). \#1 open-source on MLE-Bench; ALE-Bench; RelBench
  <sub>★ 113 · Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install leeroo-kapso`</sub>
- **[SkyDiscover](https://github.com/skydiscover-ai/skydiscover#-benchmark-performance)** — AI-Driven Scientific and Algorithmic Discovery
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-14</sub>
  <sub>`git clone https://github.com/skydiscover-ai/skydiscover.git && cd skydiscover/#-benchmark-performance`</sub>

## Evolve Agent

- **[EvoAgentX](https://github.com/ANative-Lab/EvoAgentX)** — EvoAgentX: Building a Self-Evolving Ecosystem of AI Agents
  <sub>★ 3.4k · Python · pip · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evoagentx`</sub>
- **[AgentEvolver](https://github.com/modelscope/AgentEvolver)** — AgentEvolver: Towards Efficient Self-Evolving Agent System
  <sub>★ 1.6k · Python · Apache-2.0 · source · pushed 2026-04-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/modelscope/AgentEvolver.git`</sub>

## RAG

- **[RAGFlow](https://github.com/infiniflow/ragflow)** — RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine based on deep document understanding
  <sub>★ 91.2k · Go · Apache-2.0 · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/infiniflow/ragflow.git`</sub>
- **[LightRAG](https://github.com/HKUDS/LightRAG)** — "LightRAG: Simple and Fast Retrieval-Augmented Generation"
  <sub>★ 39.8k · Python · MIT · uv · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install "lightrag-hku[api]"`</sub>
- **[quivr](https://github.com/The-Vibe-Company/quivr)** — Opiniated RAG for integrating GenAI in your apps 🧠 Focus on your product rather than the RAG. Easy integration in existing products with customisation! Any LLM: GPT4, Groq, Llama. Any Vectorstore: PGVector, Faiss. Any Files. Anyway you want
  <sub>★ 39.5k · Python · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install quivr-core # Check that the installation worked`</sub>
- **[GraphRAG](https://github.com/microsoft/graphrag)** — A modular graph-based Retrieval-Augmented Generation (RAG) system
  <sub>★ 36.1k · Python · MIT · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/graphrag.git`</sub>
- **[RAG-Anything](https://github.com/HKUDS/RAG-Anything)** — "RAG-Anything: All-in-One RAG Framework"
  <sub>★ 23.4k · Python · MIT · pip · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install raganything`</sub>
- **[Verbatim Citation Gate](https://github.com/tonydzi/verbatim-citation-gate)** — A zero-token verbatim check plus a burden-of-proof judge that catches fabricated RAG citations before they reach the user; framework-agnostic
  <sub>★ 3 · Python · MIT · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "git+https://github.com/tonydzi/verbatim-citation-gate"`</sub>
- **[EmbedGuard](https://github.com/neerazz/embedguard)** — Cross-layer detection and provenance attestation for adversarial embedding attacks in RAG systems; published in IJCESEN 2026 (DOI 10.22399/ijcesen.4869)
  <sub>Python · MIT · clone · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/neerazz/embedguard`</sub>

## Database

- **[milvus](https://github.com/milvus-io/milvus)** — Milvus is a high-performance, cloud-native vector database built for scalable vector ANN search
  <sub>★ 46.2k · Go · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/milvus-io/milvus.git`</sub>
- **[Faiss](https://github.com/facebookresearch/faiss)** — A library for efficient similarity search and clustering of dense vectors
  <sub>★ 41k · C++ · MIT · source · pushed 2026-09-22</sub>
  <sub>`git clone https://github.com/facebookresearch/faiss.git`</sub>
- **[chroma](https://github.com/chroma-core/chroma)** — the AI-native open-source embedding database
  <sub>★ 29.4k · Rust · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install chromadb # python client`</sub>
- **[Hindsight](https://github.com/vectorize-io/hindsight)** — Hindsight: Agent Memory That Learns
  <sub>★ 25k · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npx @vectorize-io/hindsight-coding-agents install all # every detected agent, wired natively`</sub>
- **[weaviate](https://github.com/weaviate/weaviate)** — Weaviate is an open-source vector database that stores both objects and vectors, allowing for the combination of vector search with structured filtering with the fault tolerance and scalability of a cloud-native database​
  <sub>★ 16.8k · Go · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add weaviate/agent-skills`</sub>
- **[deeplake](https://github.com/activeloopai/deeplake)** — Database for AI. Store Vectors, Images, Texts, Videos, etc. Use with LLMs/LangChain. Store, query, version, &amp; visualize any AI data. Stream data in real-time to PyTorch/TensorFlow
  <sub>★ 9.2k · C++ · Apache-2.0 · pip · pushed 2026-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install deeplake`</sub>

## FineTune

- **[unsloth](https://github.com/unslothai/unsloth)** — Finetune Llama 3.3, DeepSeek-R1 &amp; Reasoning LLMs 2x faster with 70% less memory! 🦥
  <sub>★ 76.6k · Python · Apache-2.0 · psh · pushed 2026-09-22 · Win · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`irm https://unsloth.ai/install.ps1 | iex`</sub>
- **[LLaMa-Factory](https://github.com/hiyouga/LlamaFactory)** — Unified Efficient Fine-Tuning of 100+ LLMs &amp; VLMs (ACL 2024)
  <sub>★ 75k · Python · Apache-2.0 · docker · pushed 2026-09-14 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run -it --rm --gpus=all --ipc=host hiyouga/llamafactory:latest`</sub>
- **[Swift](https://github.com/modelscope/ms-swift)** — Use PEFT or Full-parameter to finetune 450+ LLMs (Qwen2.5, InternLM3, GLM4, Llama3.3, Mistral, Yi1.5, Baichuan2, DeepSeek-R1, ...) and 150+ MLLMs (Qwen2.5-VL, Qwen2-Audio, Llama3.2-Vision, Llava, InternVL2.5, MiniCPM-V-2.6, GLM4v, Xcomposer2.5, Yi-VL, DeepSeek-VL2, Phi3.5-Vision, GOT-OCR2, ...)
  <sub>★ 15.7k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ms-swift -U`</sub>
- **[Axolotl](https://github.com/axolotl-ai-cloud/axolotl)** — Go ahead and axolotl questions
  <sub>★ 12.5k · Python · Apache-2.0 · docker · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --gpus '"all"' --ipc=host --rm -it axolotlai/axolotl:main-latest`</sub>
- **[LMFlow](https://github.com/OptimalScale/LMFlow)** — An Extensible Toolkit for Finetuning and Inference of Large Foundation Models. Large Models for All
  <sub>★ 8.5k · Python · Apache-2.0 · pip · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lmflow-finetune`</sub>
- **[torchtune](https://github.com/meta-pytorch/torchtune)** — PyTorch native post-training library
  <sub>★ 5.8k · Python · BSD-3-Clause · pip · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install torchtune`</sub>
- **[MLX-VLM](https://github.com/Blaizzy/mlx-vlm)** — MLX-VLM is a package for inference and fine-tuning of Vision Language Models (VLMs) on your Mac using MLX
  <sub>★ 5.5k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U mlx-vlm`</sub>
- **[Transformer Lab](https://github.com/transformerlab/transformerlab-app)** — Open Source Application for Advanced LLM Engineering: interact, train, fine-tune, and evaluate large language models on your own computer
  <sub>★ 5.2k · Python · AGPL-3.0 · pip · pushed 2026-09-18 · Win · WSL2 · macOS · Linux</sub>
  <sub>`pip install transformerlab`</sub>
- **[maestro](https://github.com/roboflow/maestro)** — streamline the fine-tuning process for multimodal models: PaliGemma 2, Florence-2, and Qwen2.5-VL
  <sub>★ 2.7k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "maestro[paligemma_2]"`</sub>
- **[EasyLM](https://github.com/young-geng/EasyLM)** — Large language models (LLMs) made easy, EasyLM is a one stop solution for pre-training, finetuning, evaluating and serving LLMs in JAX/Flax
  <sub>★ 2.5k · Python · Apache-2.0 · clone · pushed 2024-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/young-geng/EasyLM.git`</sub>

## Framework

- **[ColossalAI](https://github.com/hpcaitech/ColossalAI)** — Making large AI models cheaper, faster and more accessible
  <sub>★ 41.4k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install colossalai`</sub>
- **[MLX](https://github.com/ml-explore/mlx)** — MLX: An array framework for Apple silicon
  <sub>★ 28.5k · C++ · MIT · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mlx`</sub>
- **[Candle](https://github.com/huggingface/candle)** — Minimalist ML framework for Rust
  <sub>★ 21.1k · Rust · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/huggingface/candle.git`</sub>
- **[Ludwig](https://github.com/ludwig-ai/ludwig)** — Low-code framework for building custom LLMs, neural networks, and other AI models
  <sub>★ 11.8k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ludwig # core`</sub>
- **[MaxText](https://github.com/AI-Hypercomputer/maxtext)** — A simple, performant and scalable Jax LLM!
  <sub>★ 2.4k · Python · Apache-2.0 · source · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/google/maxtext.git`</sub>
- **[AXLearn](https://github.com/apple/axlearn)** — An Extensible Deep Learning Library
  <sub>★ 2.4k · Python · Apache-2.0 · source · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/apple/axlearn.git`</sub>
- **[DLRover](https://github.com/intelligent-machine-learning/dlrover)** — DLRover: An Automatic Distributed Deep Learning System
  <sub>★ 1.7k · Python · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`pip install dlrover[k8s, torch]`</sub>

## Agentic RL

- **[verl](https://github.com/verl-project/verl)** — verl: Volcano Engine Reinforcement Learning for LLMs
  <sub>★ 23.6k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install verl@git+…@<sha>`</sub>
- **[slime](https://github.com/THUDM/slime)** — slime is an LLM post-training framework for RL Scaling
  <sub>★ 8.5k · Python · Apache-2.0 · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/THUDM/slime.git`</sub>
- **[rLLM](https://github.com/rllm-org/rllm)** — Democratizing Reinforcement Learning for LLMs
  <sub>★ 5.8k · Python · Apache-2.0 · source · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/rllm-org/rllm.git`</sub>
- **[AReaL](https://github.com/areal-project/AReaL)** — Lightning-Fast RL for LLM Reasoning and Agents. Made Simple &amp; Flexible
  <sub>★ 5.8k · Python · Apache-2.0 · clone · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/areal-project/AReaL`</sub>

## RLHF

- **[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)** — An Easy-to-use, Scalable and High-performance RLHF Framework (70B+ PPO Full Tuning &amp; Iterative DPO &amp; LoRA &amp; RingAttention &amp; RFT)
  <sub>★ 10k · Python · Apache-2.0 · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install openrlhf # Basic`</sub>
- **[Self-RLHF](https://github.com/PKU-Alignment/safe-rlhf)** — Safe RLHF: Constrained Value Alignment via Safe Reinforcement Learning from Human Feedback
  <sub>★ 1.6k · Python · Apache-2.0 · clone · pushed 2025-11-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/PKU-Alignment/safe-rlhf.git`</sub>

## Chatbot

- **[Open WebUI](https://github.com/open-webui/open-webui)** — User-friendly AI Interface (Supports Ollama, OpenAI API, ...)
  <sub>★ 152.8k · Python · pip · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install open-webui`</sub>
- **[NextChat](https://github.com/ChatGPTNextWeb/NextChat)** — Light and Fast AI Assistant. Support: Web | iOS | MacOS | Android | Linux | Windows
  <sub>★ 88.8k · TypeScript · MIT · source · pushed 2026-08-11 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/ChatGPTNextWeb/NextChat.git`</sub>
- **[Lobe Chat](https://github.com/lobehub/lobehub)** — Lobe Chat - an open-source, modern-design AI chat framework. Supports Multi AI Providers( OpenAI / Claude 3 / Gemini / Ollama / DeepSeek / Qwen), Knowledge Base (file upload / knowledge management / RAG ), Multi-Modals (Plugins/Artifacts) and Thinking. One-click FREE deployment of your private ChatGPT/ Claude / DeepSeek application
  <sub>★ 82.8k · TypeScript · source · pushed 2026-09-22 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/lobehub/lobe-chat.git`</sub>
- **[AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)** — The all-in-one Desktop &amp; Docker AI application with built-in RAG, AI agents, No-code agent builder, MCP compatibility, and more
  <sub>★ 66.3k · JavaScript · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Mintplex-Labs/anything-llm.git`</sub>
- **[PrivateGPT](https://github.com/zylon-ai/private-gpt)** — Interact with your documents using the power of GPT, 100% privately, no data leaks
  <sub>★ 57.5k · Python · Apache-2.0 · brew · pushed 2026-09-22 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`brew install private-gpt`</sub>
- **[Cherry Studio](https://github.com/CherryHQ/cherry-studio)** — Cherry Studio is a desktop client that supports for multiple LLM providers. Support deepseek-r1
  <sub>★ 52.1k · TypeScript · AGPL-3.0 · source · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/CherryHQ/cherry-studio.git`</sub>
- **[Jan](https://github.com/janhq/jan)** — Jan is an open source alternative to ChatGPT that runs 100% offline on your computer
  <sub>★ 44.6k · Rust · clone · pushed 2026-09-22 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/janhq/jan`</sub>
- **[Gradio](https://github.com/gradio-app/gradio)** — Build and share delightful machine learning apps, all in Python. 🌟 Star to support our work!
  <sub>★ 43.6k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade gradio`</sub>
- **[FastChat](https://github.com/lm-sys/FastChat)** — An open platform for training, serving, and evaluating large language models. Release repo for Vicuna and Chatbot Arena
  <sub>★ 39.5k · Python · Apache-2.0 · clone · pushed 2026-05-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lm-sys/FastChat.git`</sub>
- **[Chatbot UI](https://github.com/mckaywrigley/chatbot-ui)** — AI chat for any model
  <sub>★ 33.3k · TypeScript · MIT · clone · pushed 2024-08-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mckaywrigley/chatbot-ui.git`</sub>
- **[opcode](https://github.com/winfunc/opcode)** — A powerful GUI app and Toolkit for Claude Code - Create custom agents, manage interactive Claude Code sessions, run secure background agents, and more
  <sub>★ 22.4k · TypeScript · AGPL-3.0 · clone · pushed 2026-09-18 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/getAsterisk/opcode.git`</sub>
- **[Chat SDK](https://github.com/vercel/chatbot)** — A full-featured, hackable Next.js AI chatbot built by Vercel
  <sub>★ 21k · TypeScript · npm · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g vercel`</sub>
- **[LLM](https://github.com/simonw/llm)** — Access large language models from the command-line
  <sub>★ 12.5k · Python · Apache-2.0 · uv · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install llm`</sub>
- **[5ire](https://github.com/nanbingxyz/5ire)** — 5ire is a cross-platform desktop AI assistant, MCP client. It compatible with major service providers, supports local knowledge base and tools via model context protocol servers
  <sub>★ 5.4k · TypeScript · source · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/nanbingxyz/5ire.git`</sub>

## Sandbox

- **[Daytona](https://github.com/daytonaio/daytona)** — Daytona is a Secure and Elastic Infrastructure for Running AI-Generated Code
  <sub>★ 71.7k · pip · pushed 2026-07-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install daytona`</sub>
- **[E2B](https://github.com/e2b-dev/E2B)** — Secure open source cloud runtime for AI apps &amp; AI agents
  <sub>source</sub>
  <sub>`git clone https://github.com/e2b-dev/E2B.git`</sub>

## Application Framework

- **[PostHog](https://github.com/PostHog/posthog)** — PostHog provides open-source web &amp; product analytics, session recording, feature flagging and A/B testing that you can self-host. Get started - free
  <sub>★ 39.9k · Python · source · pushed 2026-09-22 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/PostHog/posthog.git`</sub>
- **[Langfuse](https://github.com/langfuse/langfuse)** — Open source LLM engineering platform: LLM Observability, metrics, evals, prompt management, playground, datasets. Integrates with OpenTelemetry, Langchain, OpenAI SDK, LiteLLM, and more. 🍊YC W23
  <sub>★ 34.9k · TypeScript · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langfuse openai`</sub>
- **[DeepEval](https://github.com/confident-ai/deepeval)** — The LLM Evaluation Framework
  <sub>★ 18.4k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U deepeval`</sub>
- **[ragas](https://github.com/vibrantlabsai/ragas)** — Supercharge Your LLM Application Evaluations 🚀
  <sub>★ 15.8k · Python · Apache-2.0 · pip · pushed 2026-02-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ragas`</sub>
- **[Evidently](https://github.com/evidentlyai/evidently)** — Evidently is ​​an open-source ML and LLM observability framework. Evaluate, test, and monitor any AI-powered system or data pipeline. From tabular data to Gen AI. 100+ metrics
  <sub>★ 7.9k · Jupyter Notebook · Apache-2.0 · pip · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evidently`</sub>
- **[OpenLIT](https://github.com/openlit/openlit)** — Open source platform for AI Engineering: OpenTelemetry-native LLM Observability, GPU Monitoring, Guardrails, Evaluations, Prompt Management, Vault, Playground. 🚀💻 Integrates with 50+ LLM Providers, VectorDBs, Agent Frameworks and GPUs
  <sub>★ 2.8k · TypeScript · Apache-2.0 · pip · pushed 2026-09-22 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install openlit`</sub>
- **[Future AGI](https://github.com/future-agi/future-agi)** — Open-source, end-to-end platform for evaluating, observing, and improving LLM and AI agent applications. Tracing · Evals · Simulations · Datasets · Gateway · Guardrails. Self-hostable. Apache 2.0
  <sub>★ 2.1k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install futureagi`</sub>
- **[Weave](https://github.com/wandb/weave)** — Weave is a toolkit for developing AI-powered applications, built by Weights &amp; Biases
  <sub>★ 1.1k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install weave`</sub>
- **[Cordum.io](https://github.com/cordum-io/cordum)** — Cordum (cordum.io) is a platform-only control plane for autonomous AI Agents and external workers. It uses NATS for the bus, Redis for state and payload pointers, and CAP v2 wire contracts for jobs, results, and heartbeats. Workers and product packs live outside this repo.Core cordum
  <sub>★ 508 · Go · helm · pushed 2026-09-17 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`helm install cordum oci://ghcr.io/cordum-io/cordum/charts/cordum \`</sub>
- **[Neurolink](https://github.com/juspay/neurolink)** — Universal AI Development Platform with MCP server integration, multi-provider support, and professional CLI. Build, test, and deploy AI applications with multiple ai providers
  <sub>★ 137 · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @juspay/neurolink --help`</sub>
- **[AgentMark](https://github.com/agentmark-ai/agentmark)** — Open-source, Git-native platform for building and observing reliable AI agents. Prompts and datasets in your repo, evals in CI, and OpenTelemetry tracing
  <sub>unavailable</sub>
- **[Helicone](https://github.com/Helicone/helicone)** — Open source LLM observability platform. One line of code to monitor, evaluate, and experiment. YC W23 🍓
  <sub>source</sub>
  <sub>`git clone https://github.com/helicone/helicone.git`</sub>
- **[lunaary](https://github.com/lunary-ai/lunary)** — The production toolkit for LLMs. Observability, prompt management and evaluations
  <sub>unavailable</sub>
- **[phoenix](https://github.com/Arize-ai/phoenix)** — AI Observability &amp; Evaluation
  <sub>source</sub>
  <sub>`git clone https://github.com/arize-ai/phoenix.git`</sub>

## Benchmark

- **[opik](https://github.com/comet-ml/opik)** — Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and production-ready dashboards
  <sub>★ 22.2k · Python · Apache-2.0 · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx add-mcp https://www.comet.com/opik/api/v1/mcp --name opik-mcp`</sub>
- **[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)** — A framework for few-shot evaluation of language models
  <sub>★ 14.1k · Python · MIT · source · pushed 2026-09-14 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/EleutherAI/lm-evaluation-harness.git`</sub>
- **[OpenCompass](https://github.com/open-compass/opencompass)** — OpenCompass is an LLM evaluation platform, supporting a wide range of models (Llama3, Mistral, InternLM2,GPT-4,LLaMa2, Qwen,GLM, Claude, etc) over 100+ datasets
  <sub>★ 7.5k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U opencompass`</sub>
- **[AgentBench](https://github.com/THUDM/AgentBench)** — A Comprehensive Benchmark to Evaluate LLMs as Agents (ICLR'24)
  <sub>★ 3.7k · Python · Apache-2.0 · source · pushed 2026-02-08 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/THUDM/AgentBench.git`</sub>
- **[terminal-bench](https://github.com/harbor-framework/terminal-bench-1)** — A benchmark for LLMs on complicated tasks in the terminal
  <sub>★ 2.6k · Python · Apache-2.0 · uv · pushed 2026-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uv tool install terminal-bench`</sub>
- **[MLE-bench](https://github.com/openai/mle-bench/)** — MLE-bench is a benchmark for measuring how well AI agents perform at machine learning engineering
  <sub>★ 1.8k · Python · source · pushed 2026-04-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/openai/mle-bench/.git`</sub>
- **[LiveBench](https://github.com/LiveBench/LiveBench)** — LiveBench: A Challenging, Contamination-Free LLM Benchmark
  <sub>★ 1.3k · Python · source · pushed 2026-09-21 · WSL2 · Linux</sub>
  <sub>`git clone https://github.com/livebench/livebench.git`</sub>
- **[LongBench](https://github.com/THUDM/LongBench)** — LongBench v2 and LongBench (ACL 2024)
  <sub>★ 1.2k · Python · MIT · source · pushed 2025-01-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/THUDM/LongBench.git`</sub>
- **[genai-bench](https://github.com/sgl-project/genai-bench)** — Genai-bench is a powerful benchmark tool designed for comprehensive token-level performance evaluation of large language model (LLM) serving systems
  <sub>★ 331 · Python · MIT · pip · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install genai-bench`</sub>
- **[Inference Perf](https://github.com/kubernetes-sigs/inference-perf)** — GenAI inference performance benchmarking tool
  <sub>★ 246 · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install inference-perf`</sub>
- **[skill-optimizer](https://github.com/fastxyz/skill-optimizer)** — Benchmark and self-optimize SDK/CLI/MCP guidance so every agent model can use your tool reliably
  <sub>★ 80 · TypeScript · MIT · npx · pushed 2026-05-28 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add fastxyz/skill-optimizer --skill skill-optimizer -a cursor -y`</sub>
- **[ASQI Engineer](https://github.com/asqi-engineer/asqi-engineer)** — ASQI (AI Solutions Quality Index) Engineer - run containerised AI tests and map to score cards!
  <sub>★ 64 · Python · Apache-2.0 · pip · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install asqi-engineer`</sub>
- **[Inference Benchmark](https://github.com/AI-Hypercomputer/inference-benchmark)** — A model server agnostic inference benchmarking tool that can be used to benchmark LLMs running on differet infrastructure like GPU and TPU. It can also be run on a GKE cluster as a container
  <sub>★ 22 · Python · Apache-2.0 · source · pushed 2026-03-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/AI-Hypercomputer/inference-benchmark.git`</sub>

## Observation

- **[wandb](https://github.com/wandb/wandb)** — The AI developer platform. Use Weights &amp; Biases to train and fine-tune models, and manage models from experimentation to production
  <sub>★ 11.3k · Python · MIT · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install wandb`</sub>
- **[OpenLLMetry](https://github.com/traceloop/openllmetry)** — Open-source observability for your LLM application, based on OpenTelemetry
  <sub>★ 7.4k · Python · Apache-2.0 · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install traceloop-sdk`</sub>
- **[Failproof](https://github.com/FailproofAI/failproofai)** — Observability and enforcement for AI agent harnesses. Capture every run and runtime reliability with policy enforcement. 40 built-in policies, a local dashboard, no account required with a generous free cloud plan
  <sub>★ 5.1k · MDX · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g failproofai`</sub>
- **[Latitude](https://github.com/latitude-dev/latitude-llm)** — Latitude is the open-source ai monitoring platform
  <sub>★ 4.7k · TypeScript · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx -y @latitude-data/claude-code-telemetry install`</sub>
- **[ClawMetry](https://github.com/vivekchand/clawmetry)** — Self-hosted observability for coding agents. Reads the session logs runtimes already write on disk, so there is no SDK and nothing in the request path
  <sub>★ 420 · Python · MIT · npx · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx skills add vivekchand/clawmetry --skill agent-kill-switch`</sub>
- **[OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay)** — Record, replay and fork debugger for AI agents. Records a run below the harness, replays it offline with the network off, and forks it from any checkpoint onto another model
  <sub>★ 260 · TypeScript · Apache-2.0 · npm · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm i -g orcareplay # the package is orcareplay`</sub>
- **[Observatory](https://github.com/The-Context-Company/observatory)** — Open-source TypeScript and Python SDKs for instrumenting AI agents and analyzing production runs, traces, sessions, feedback, and recurring patterns
  <sub>★ 123 · TypeScript · MIT · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/The-Context-Company/observatory.git`</sub>
- **[Gait](https://github.com/Clyra-AI/gait)** — OSS Go CLI for signed runpacks (verify, deterministic stub replay, diff), CI regressions, and policy-gated high-risk tool calls for agent workflows
  <sub>★ 12 · Go · Apache-2.0 · go · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/Clyra-AI/gait/cmd/gait@latest`</sub>
- **[LLMeter](https://github.com/amedinat/LLMeter)** — Open-source LLM cost monitoring with per-customer cost attribution. Polls provider billing APIs (OpenAI, Anthropic, DeepSeek, OpenRouter) directly — no proxy or code changes — with budget alerts before surprise bills
  <sub>★ 7 · TypeScript · AGPL-3.0 · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/amedinat/LLMeter.git`</sub>
- **[Vobo](https://github.com/getbeton/vobo)** — Open-source human review for AI output. Anchored comments and a hashed evidence chain
  <sub>★ 5 · TypeScript · Apache-2.0 · clone · pushed 2026-09-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/getbeton/vobo.git`</sub>


---

Snapshot 2026-09-22. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
