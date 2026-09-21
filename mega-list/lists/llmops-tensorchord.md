# LLMOps (tensorchord)

An awesome & curated list of best LLMOps tools for developers

Curated by **[tensorchord/Awesome-LLMOps](https://github.com/tensorchord/Awesome-LLMOps)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

383 entries · 339 distinct repos · 33 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/openai/whisper"><img src="https://raw.githubusercontent.com/openai/whisper/main/approach.png" width="260"></a> | <a href="https://github.com/CompVis/stable-diffusion"><img src="https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/txt2img/merged-0006.png" width="260"></a> | <a href="https://github.com/facebookresearch/segment-anything"><img src="https://raw.githubusercontent.com/facebookresearch/segment-anything-2/main/assets/model_diagram.png?raw=true" width="260"></a> |
| **[whisper](https://github.com/openai/whisper)**<br>★ 109.4k | **[stable-diffusion](https://github.com/CompVis/stable-diffusion)**<br>★ 73.5k | **[segment-anything (SAM)](https://github.com/facebookresearch/segment-anything)**<br>★ 54.9k |
| <a href="https://github.com/zai-org/ChatGLM-6B"><img src="https://raw.githubusercontent.com/THUDM/ChatGLM-6B/main/resources/web-demo.gif" width="260"></a> | <a href="https://github.com/lm-sys/FastChat"><img src="https://raw.githubusercontent.com/lm-sys/FastChat/main/assets/screenshot_cli.png" width="260"></a> | <a href="https://github.com/suno-ai/bark"><img src="https://user-images.githubusercontent.com/5068315/235310676-a4b3b511-90ec-4edf-8153-7ccf14905d73.png" width="260"></a> |
| **[GLM-6B (ChatGLM)](https://github.com/zai-org/ChatGLM-6B)**<br>★ 41k | **[FastChat (Vicuna)](https://github.com/lm-sys/FastChat)**<br>★ 39.5k | **[bark](https://github.com/suno-ai/bark)**<br>★ 39.3k |

## Contents

- [Audio Foundation Model](#audio-foundation-model) (2)
- [CV Foundation Model](#cv-foundation-model) (4)
- [Large Language Model](#large-language-model) (14)
- [Robotics Foundation Model](#robotics-foundation-model) (7)
- [Foundation Model Fine Tuning](#foundation-model-fine-tuning) (9)
- [Model Editing](#model-editing) (1)
- [Large Model Serving](#large-model-serving) (24)
- [Optimizations](#optimizations) (10)
- [Frameworks/Servers for Serving](#frameworksservers-for-serving) (15)
- [ML Compiler](#ml-compiler) (3)
- [Frameworks for Training](#frameworks-for-training) (23)
- [AutoML](#automl) (40)
- [Experiment Tracking](#experiment-tracking) (9)
- [Federated ML](#federated-ml) (6)
- [LLMOps](#llmops) (79)
- [ML Platforms](#ml-platforms) (14)
- [Vector search](#vector-search) (22)
- [Hybrid search](#hybrid-search) (1)
- [Data Management](#data-management) (6)
- [Data Storage](#data-storage) (3)
- [Feature Engineering](#feature-engineering) (2)
- [Data/Feature enrichment](#datafeature-enrichment) (4)
- [Data Tracking](#data-tracking) (2)
- [Visualization](#visualization) (9)
- [Profiling](#profiling) (2)
- [Observability](#observability) (18)
- [Frameworks for LLM security](#frameworks-for-llm-security) (4)
- [IDEs and Workspaces](#ides-and-workspaces) (6)
- [Code AI](#code-ai) (10)
- [Workflow](#workflow) (12)
- [Awesome Lists](#awesome-lists) (15)
- [Scheduling](#scheduling) (4)
- [Model Management](#model-management) (3)

## Audio Foundation Model

- **[whisper](https://github.com/openai/whisper)** — Robust Speech Recognition via Large-Scale Weak Supervision
  <sub>★ 109.4k · Python · MIT · source · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/openai/whisper.git`</sub>
- **[bark](https://github.com/suno-ai/bark)** — Bark is a transformer-based text-to-audio model created by Suno. Bark can generate highly realistic, multilingual speech as well as other audio - including music, background noise and simple sound effects
  <sub>★ 39.3k · Jupyter Notebook · MIT · pip · pushed 2024-08-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/suno-ai/bark.git`</sub>

## CV Foundation Model

- **[stable-diffusion](https://github.com/CompVis/stable-diffusion)** — A latent text-to-image diffusion model
  <sub>★ 73.5k · Jupyter Notebook · source · pushed 2024-06-18</sub>
  <sub>`git clone https://github.com/CompVis/stable-diffusion.git`</sub>
- **[segment-anything (SAM)](https://github.com/facebookresearch/segment-anything)** — produces high quality object masks from input prompts such as points or boxes, and it can be used to generate masks for all objects in an image
  <sub>★ 54.9k · Jupyter Notebook · Apache-2.0 · pip · pushed 2024-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/facebookresearch/segment-anything.git`</sub>
- **[disco-diffusion](https://github.com/alembics/disco-diffusion)** — A frankensteinian amalgamation of notebooks, models and techniques for the generation of AI Art and Animations
  <sub>★ 7.4k · Jupyter Notebook · source · pushed 2023-07-09 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/alembics/disco-diffusion.git`</sub>
- **[midjourney](https://www.midjourney.com/home/)** — Midjourney is an independent research lab exploring new mediums of thought and expanding the imaginative powers of the human species
  <sub>website</sub>
  <sub>`https://www.midjourney.com/home/`</sub>

## Large Language Model

- **[GLM-6B (ChatGLM)](https://github.com/zai-org/ChatGLM-6B)** — An Open Bilingual Pre-Trained Model, quantization of ChatGLM-130B, can run on consumer-level GPUs
  <sub>★ 41k · Python · Apache-2.0 · clone · pushed 2024-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://huggingface.co/THUDM/chatglm-6b`</sub>
- **[FastChat (Vicuna)](https://github.com/lm-sys/FastChat)** — An open platform for training, serving, and evaluating large language models. Release repo for Vicuna and FastChat-T5
  <sub>★ 39.5k · Python · Apache-2.0 · clone · pushed 2026-05-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lm-sys/FastChat.git`</sub>
- **[Alpaca](https://github.com/tatsu-lab/stanford_alpaca)** — Code and documentation to train Stanford's Alpaca models, and generate the data
  <sub>★ 30.2k · Python · Apache-2.0 · source · pushed 2024-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tatsu-lab/stanford_alpaca.git`</sub>
- **[StableLM](https://github.com/Stability-AI/StableLM)** — StableLM: Stability AI Language Models
  <sub>★ 15.7k · Jupyter Notebook · Apache-2.0 · source · pushed 2024-04-08</sub>
  <sub>`git clone https://github.com/Stability-AI/StableLM.git`</sub>
- **[ChatGLM2-6B](https://github.com/zai-org/ChatGLM2-6B)** — ChatGLM2-6B is the second-generation version of the open-source bilingual (Chinese-English) chat model ChatGLM-6B
  <sub>★ 15.5k · Python · clone · pushed 2024-06-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/THUDM/ChatGLM2-6B`</sub>
- **[dolly](https://github.com/databrickslabs/dolly)** — Databricks’ Dolly, a large language model trained on the Databricks Machine Learning Platform
  <sub>★ 10.8k · Python · Apache-2.0 · source · pushed 2023-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/databrickslabs/dolly.git`</sub>
- **[BELLE](https://github.com/LianjiaTech/BELLE)** — A 7B Large Language Model fine-tune by 34B Chinese Character Corpus, based on LLaMA and Alpaca
  <sub>★ 8.3k · HTML · Apache-2.0 · source · pushed 2024-10-16 · Win? · macOS</sub>
  <sub>`git clone https://github.com/LianjiaTech/BELLE.git`</sub>
- **[GLM-130B (ChatGLM)](https://github.com/zai-org/GLM-130B)** — An Open Bilingual Pre-Trained Model (ICLR 2023)
  <sub>★ 7.6k · Python · Apache-2.0 · source · pushed 2023-07-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/THUDM/GLM-130B.git`</sub>
- **[GPT-NeoX](https://github.com/EleutherAI/gpt-neox)** — An implementation of model parallel autoregressive transformers on GPUs, based on the DeepSpeed library
  <sub>★ 7.5k · Python · Apache-2.0 · source · pushed 2026-09-04 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/EleutherAI/gpt-neox.git`</sub>
- **[Luotuo](https://github.com/LC1332/Luotuo-Chinese-LLM)** — A Chinese LLM, Based on LLaMA and fine tune by Stanford Alpaca, Alpaca LoRA, Japanese-Alpaca-LoRA
  <sub>★ 3.6k · Jupyter Notebook · Apache-2.0 · source · pushed 2023-09-03</sub>
  <sub>`git clone https://github.com/LC1332/Luotuo-Chinese-LLM.git`</sub>
- **[Bloom](https://github.com/bigscience-workshop/model_card)** — BigScience Large Open-science Open-access Multilingual Language Model
  <sub>★ 25 · Apache-2.0 · source · pushed 2022-07-11</sub>
  <sub>`git clone https://github.com/bigscience-workshop/model_card.git`</sub>
- **[Falcon 40B](https://huggingface.co/tiiuae/falcon-40b-instruct)** — Falcon-40B-Instruct is a 40B parameters causal decoder-only model built by TII based on Falcon-40B and finetuned on a mixture of Baize. It is made available under the Apache 2.0 license
  <sub>website</sub>
  <sub>`https://huggingface.co/tiiuae/falcon-40b-instruct`</sub>
- **[Gemma](https://www.kaggle.com/models/google/gemma)** — Gemma is a family of lightweight, open models built from the research and technology that Google used to create the Gemini models
  <sub>website</sub>
  <sub>`https://www.kaggle.com/models/google/gemma`</sub>
- **[Mixtral-8x7B-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-v0.1)** — The Mixtral-8x7B Large Language Model (LLM) is a pretrained generative Sparse Mixture of Experts
  <sub>website</sub>
  <sub>`https://huggingface.co/mistralai/Mixtral-8x7B-v0.1`</sub>

## Robotics Foundation Model

- **[LeRobot](https://github.com/huggingface/lerobot)** — A central community library by Hugging Face for AI in robotics — end-to-end learning tools, data pipelines, and support for training/deploying VLA models
  <sub>★ 27.7k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lerobot`</sub>
- **[OpenPI](https://github.com/Physical-Intelligence/openpi)** — Open-source VLA models from Physical Intelligence, including π₀ and π₀.5 — flow-based vision-language-action models pretrained on large-scale robot data with fine-tuning support
  <sub>★ 13.9k · Python · Apache-2.0 · source · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Physical-Intelligence/openpi.git`</sub>
- **[OpenVLA](https://github.com/openvla/openvla)** — A 7B-parameter open-source Vision-Language-Action model trained on 970K+ robot demonstrations from the Open X-Embodiment dataset for generalist robotic manipulation
  <sub>★ 7.1k · Python · MIT · pip · pushed 2025-03-23 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`pip install --no-deps --force-reinstall git+https://github.com/moojink/dlimp_openvla`</sub>
- **[Octo](https://github.com/octo-models/octo)** — A transformer-based generalist robot policy pretrained on 800K+ robot trajectories from the Open X-Embodiment dataset. Supports language instructions, goal images, and fine-tuning to new embodiments
  <sub>★ 1.8k · Python · MIT · source · pushed 2024-07-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/octo-models/octo.git`</sub>
- **[DiVLA](https://github.com/hustvl/DiVLA)** — A continuous diffusion-based Vision-Language-Action model that integrates diffusion policies into autoregressive VLMs for robust and precise continuous robotic control
  <sub>unavailable</sub>
- **[RoboMamba](https://github.com/hustvl/RoboMamba)** — An efficient VLA model leveraging State Space Models (Mamba) instead of standard self-attention, offering linear inference complexity for efficient, recurrent robotic reasoning
  <sub>unavailable</sub>
- **[SmolVLA](https://huggingface.co/blog/smolvla)** — A compact ~450M parameter VLA by Hugging Face, designed to be computationally efficient and accessible, running on consumer GPUs or CPUs. Part of the LeRobot ecosystem
  <sub>website</sub>
  <sub>`https://huggingface.co/blog/smolvla`</sub>

## Foundation Model Fine Tuning

- **[peft](https://github.com/huggingface/peft)** — State-of-the-art Parameter-Efficient Fine-Tuning
  <sub>★ 21.7k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install peft`</sub>
- **[TRL](https://github.com/huggingface/trl)** — Train transformer language models with reinforcement learning
  <sub>★ 19.4k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install trl`</sub>
- **[alpaca-lora](https://github.com/tloen/alpaca-lora)** — Instruct-tune LLaMA on consumer hardware
  <sub>★ 18.9k · Jupyter Notebook · Apache-2.0 · docker · pushed 2024-07-29 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`docker run --gpus=all --shm-size 64g -p 7860:7860 -v ${HOME}/.cache:/root/.cache --rm alpaca-lora generate.py \`</sub>
- **[QLoRA](https://github.com/artidoro/qlora)** — Efficient finetuning approach that reduces memory usage enough to finetune a 65B parameter model on a single 48GB GPU while preserving full 16-bit finetuning task performance
  <sub>★ 11k · Jupyter Notebook · MIT · source · pushed 2024-06-10</sub>
  <sub>`git clone https://github.com/artidoro/qlora.git`</sub>
- **[LMFlow](https://github.com/OptimalScale/LMFlow)** — An Extensible Toolkit for Finetuning and Inference of Large Foundation Models
  <sub>★ 8.5k · Python · Apache-2.0 · pip · pushed 2026-08-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lmflow-finetune`</sub>
- **[Lora](https://github.com/cloneofsimo/lora)** — Using Low-rank adaptation to quickly fine-tune diffusion models
  <sub>★ 7.6k · Jupyter Notebook · Apache-2.0 · pip · pushed 2024-03-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install git+https://github.com/cloneofsimo/lora.git`</sub>
- **[p-tuning-v2](https://github.com/THUDM/P-tuning-v2)** — An optimized prompt tuning strategy achieving comparable performance to fine-tuning on small/medium-sized models and sequence tagging challenges. (ACL 2022)
  <sub>★ 2.1k · Python · Apache-2.0 · source · pushed 2023-11-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/THUDM/P-tuning-v2.git`</sub>
- **[finetuning-scheduler](https://github.com/speediedan/finetuning-scheduler)** — A PyTorch Lightning extension that accelerates and enhances foundation model experimentation with flexible fine-tuning schedules
  <sub>★ 69 · Python · Apache-2.0 · clone · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/speediedan/finetuning-scheduler.git`</sub>
- **[Flyflow](https://github.com/flyflow-devs)** — Open source, high performance fine tuning as a service for GPT4 quality models with 5x lower latency and 3x lower cost
  <sub>website</sub>
  <sub>`https://github.com/flyflow-devs`</sub>

## Model Editing

- **[FastEdit](https://github.com/hiyouga/FastEdit)** — FastEdit aims to assist developers with injecting fresh and customized knowledge into large language models efficiently using one single command
  <sub>★ 1.4k · Python · Apache-2.0 · pip · pushed 2023-08-13 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pyfastedit`</sub>

## Large Model Serving

- **[Ollama](https://github.com/ollama/ollama)** — Serve Llama 2 and other large language models locally from command line or through a browser interface
  <sub>★ 181.4k · Go · MIT · psh · pushed 2026-09-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm https://ollama.com/install.ps1 | iex`</sub>
- **[llama.cpp](https://github.com/ggml-org/llama.cpp)** — Port of Facebook's LLaMA model in C/C++
  <sub>★ 129.1k · C++ · MIT · source · pushed 2026-09-21 · Win · macOS</sub>
  <sub>`git clone https://github.com/ggerganov/llama.cpp.git`</sub>
- **[vllm](https://github.com/vllm-project/vllm)** — A high-throughput and memory-efficient inference and serving engine for LLMs
  <sub>★ 92.3k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/vllm-project/vllm.git`</sub>
- **[Flowise](https://github.com/FlowiseAI/Flowise)** — Drag &amp; drop UI to build your customized LLM flow using LangchainJS
  <sub>★ 55.5k · TypeScript · npm · pushed 2026-08-13 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g flowise`</sub>
- **[whisper.cpp](https://github.com/ggml-org/whisper.cpp)** — Port of OpenAI's Whisper model in C/C++
  <sub>★ 53.8k · C++ · MIT · pip · pushed 2026-09-21 · Win · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install openai-whisper`</sub>
- **[Faster Whisper](https://github.com/SYSTRAN/faster-whisper)** — fast inference engine for whisper in C++ using CTranslate2
  <sub>★ 25.5k · Python · MIT · pip · pushed 2025-11-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install faster-whisper`</sub>
- **[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)** — Inference engine for TensorRT on Nvidia GPUs
  <sub>★ 14.7k · Python · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NVIDIA/TensorRT-LLM.git`</sub>
- **[Clip-as-a-service](https://github.com/jina-ai/clip-as-service)** — serving the OpenAI CLIP model
  <sub>★ 12.8k · Python · source · pushed 2024-01-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/jina-ai/clip-as-service.git`</sub>
- **[tokenizers](https://github.com/huggingface/tokenizers)** — Fast State-of-the-Art Tokenizers optimized for Research and Production
  <sub>★ 11.1k · Rust · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --pre tokenizers`</sub>
- **[text-generation-inference](https://github.com/huggingface/text-generation-inference)** — Large Language Model Text Generation Inference
  <sub>★ 10.9k · Python · Apache-2.0 · clone · pushed 2026-03-21 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/huggingface/text-generation-inference`</sub>
- **[FlexGen](https://github.com/FMInference/FlexLLMGen)** — Running large language models on a single GPU for throughput-oriented scenarios. *(Archived)
  <sub>★ 9.3k · Python · Apache-2.0 · clone · pushed 2024-10-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FMInference/FlexLLMGen.git`</sub>
- **[Shimmy](https://github.com/Michael-A-Kuykendall/shimmy)** — Python-free Rust inference server with OpenAI API compatibility and hot model swapping
  <sub>★ 5.9k · Rust · Apache-2.0 · cargo · pushed 2026-08-30 · Win · WSL2? · macOS · Linux</sub>
  <sub>`cargo install shimmy`</sub>
- **[text-embeddings-inference](https://github.com/huggingface/text-embeddings-inference)** — Inference for text-embedding models
  <sub>★ 5.1k · Rust · Apache-2.0 · brew · pushed 2026-09-17 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install text-embeddings-inference`</sub>
- **[CTranslate2](https://github.com/OpenNMT/CTranslate2)** — fast inference engine for Transformer models in C++
  <sub>★ 4.7k · C++ · MIT · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ctranslate2`</sub>
- **[Rapid-MLX](https://github.com/raullenchai/Rapid-MLX)** — OpenAI-compatible LLM inference server for Apple Silicon using MLX. 2-4x faster than Ollama with tool calling and prompt caching
  <sub>★ 3.8k · Python · uv · pushed 2026-09-21 · macOS</sub>
  <sub>`uv tool install rapid-mlx@latest`</sub>
- **[Alpaca-LoRA-Serve](https://github.com/deep-diver/LLM-As-Chatbot)** — Alpaca-LoRA as Chatbot service
  <sub>★ 3.3k · Python · Apache-2.0 · source · pushed 2023-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/deep-diver/Alpaca-LoRA-Serve.git`</sub>
- **[Off Grid](https://github.com/off-grid-ai/OGAM)** — Open-source iOS/Android app running LLMs on-device via llama.cpp. Voice (Whisper), vision, image gen, tool calling — fully offline
  <sub>★ 3.1k · TypeScript · MIT · clone · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/off-grid-ai/OGAM.git`</sub>
- **[Infinity](https://github.com/michaelfeil/infinity)** — Rest API server for serving text-embeddings
  <sub>★ 2.9k · Python · MIT · pip · pushed 2026-03-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install infinity-emb[all]`</sub>
- **[DeepSpeed-MII](https://github.com/deepspeedai/DeepSpeed-MII)** — MII makes low-latency and high-throughput inference possible, powered by DeepSpeed
  <sub>★ 2.1k · Python · Apache-2.0 · pip · pushed 2025-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install deepspeed-mii`</sub>
- **[whisper-ctranslate2](https://github.com/Softcatala/whisper-ctranslate2)** — is a 4x faster and low-memory usage drop-in cli replacement that supports word-level timestamps and VAD filter
  <sub>★ 1.4k · Python · MIT · source · pushed 2026-02-14 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Softcatala/whisper-ctranslate2.git`</sub>
- **[x-stable-diffusion](https://github.com/stochasticai/x-stable-diffusion)** — Real-time inference for Stable Diffusion - 0.88s latency. Covers AITemplate, nvFuser, TensorRT, FlashAttention. *(Archived)
  <sub>★ 556 · Jupyter Notebook · Apache-2.0 · pip · pushed 2023-12-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install stochasticx`</sub>
- **[OneComp](https://github.com/FujitsuResearch/OneCompression)** — Fujitsu Research's post-training quantization pipeline for LLMs (QEP, AutoBit, JointQ, rotation) with vLLM plugin (arXiv:2603.28845)
  <sub>★ 426 · Python · MIT · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install onecomp`</sub>
- **[Modelz-LLM](https://github.com/tensorchord/modelz-llm)** — OpenAI compatible API for LLMs and embeddings (LLaMA, Vicuna, ChatGLM and many others)
  <sub>★ 274 · Python · Apache-2.0 · pip · pushed 2023-10-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install modelz-llm`</sub>
- **[LLMKube](https://github.com/defilantech/LLMKube)** — Kubernetes operator for LLM inference with pluggable runtimes (llama.cpp, PersonaPlex/Moshi, generic), multi-GPU sharding, NVIDIA CUDA and Apple Silicon Metal support, and GGUF/MLX/SafeTensors model formats
  <sub>★ 210 · Go · Apache-2.0 · brew · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`brew install defilantech/tap/llmkube`</sub>

## Optimizations

- **[NCNN](https://github.com/Tencent/ncnn)** — ncnn is a high-performance neural network inference framework optimized for the mobile platform
  <sub>★ 23.9k · C++ · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Tencent/ncnn.git`</sub>
- **[TNN](https://github.com/Tencent/TNN)** — A uniform deep learning inference framework for mobile, desktop and server
  <sub>★ 4.7k · C++ · source · pushed 2025-05-09 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/Tencent/TNN.git`</sub>
- **[lean-ctx](https://github.com/yvgude/lean-ctx)** — Context runtime and MCP server that reduces AI coding agent token costs via session caching, AST-aware compression, and shell output patterns. Website
  <sub>★ 3.8k · Rust · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`npm install -g lean-ctx-bin # Node.js`</sub>
- **[PocketFlow](https://github.com/Tencent/PocketFlow)** — use AutoML to do model compression
  <sub>★ 2.9k · Python · source · pushed 2023-03-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Tencent/PocketFlow.git`</sub>
- **[TensorFlow Model Optimization](https://github.com/tensorflow/model-optimization)** — A suite of tools that users, both novice and advanced, can use to optimize machine learning models for deployment and execution
  <sub>★ 1.6k · Python · Apache-2.0 · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tensorflow/model-optimization.git`</sub>
- **[FeatherCNN](https://github.com/Tencent/FeatherCNN)** — FeatherCNN is a high performance inference engine for convolutional neural networks
  <sub>★ 1.2k · C++ · source · pushed 2019-09-24 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/Tencent/FeatherCNN.git`</sub>
- **[Forward](https://github.com/Tencent/Forward)** — A library for high performance deep learning inference on NVIDIA GPUs
  <sub>★ 557 · C++ · source · pushed 2022-01-29</sub>
  <sub>`git clone https://github.com/Tencent/Forward.git`</sub>
- **[Entroly](https://github.com/juyterman1000/entroly)** — Information-theoretic context optimization proxy. Cuts LLM token costs by 70–95% with zero accuracy loss using greedy submodular knapsack maximization
  <sub>★ 465 · Python · Apache-2.0 · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g entroly`</sub>
- **[optimum-tpu](https://github.com/huggingface/optimum-tpu)** — Google TPU optimizations for transformers models
  <sub>★ 136 · Python · Apache-2.0 · pip · pushed 2026-01-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install optimum-tpu -f https://storage.googleapis.com/libtpu-releases/index.html`</sub>
- **[agent-opt](https://github.com/future-agi/agent-opt)** — Automated optimization engine for improving agent workflows using feedback-driven iterative refinements
  <sub>★ 73 · Python · Apache-2.0 · pip · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-opt`</sub>

## Frameworks/Servers for Serving

- **[Jina](https://github.com/jina-ai/serve)** — Build multimodal AI services via cloud native technologies · Model Serving · Generative AI · Neural Search · Cloud Native
  <sub>★ 21.9k · Python · Apache-2.0 · pip · pushed 2025-03-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install jina`</sub>
- **[Triton Server (TRTIS)](https://github.com/triton-inference-server/server)** — The Triton Inference Server provides an optimized cloud and edge inferencing solution
  <sub>★ 11k · Python · BSD-3-Clause · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/triton-inference-server/server.git`</sub>
- **[Xinference](https://github.com/xorbitsai/inference)** — Replace OpenAI GPT with another LLM in your app by changing a single line of code. Xinference gives you the freedom to use any LLM you need. With Xinference, you're empowered to run inference with any open-source language models, speech recognition models, and multimodal models, whether in the cloud, on-premises, or even on your laptop
  <sub>★ 9.6k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install "xinference[all]"`</sub>
- **[BentoML](https://github.com/bentoml/BentoML)** — The Unified Model Serving Framework
  <sub>★ 8.9k · Python · Apache-2.0 · pip · pushed 2026-09-07 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -U bentoml`</sub>
- **[TFServing](https://github.com/tensorflow/serving)** — A flexible, high-performance serving system for machine learning models
  <sub>★ 6.4k · C++ · Apache-2.0 · clone · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/tensorflow/serving`</sub>
- **[Torchserve](https://github.com/pytorch/serve)** — Serve, optimize and scale PyTorch models in production *(Archived)
  <sub>★ 4.3k · Java · Apache-2.0 · pip · pushed 2025-08-06 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install torchserve torch-model-archiver torch-workflow-archiver`</sub>
- **[langchain-serve](https://github.com/jina-ai/langchain-serve)** — Serverless LLM apps on Production with Jina AI Cloud *(Archived)
  <sub>★ 1.6k · Python · Apache-2.0 · pip · pushed 2023-09-20 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langchain-serve`</sub>
- **[KubeAI](https://github.com/kubeai-project/kubeai)** — Deploy and scale machine learning models on Kubernetes. Built for LLMs, embeddings, and speech-to-text
  <sub>★ 1.3k · Go · Apache-2.0 · helm · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`helm install kubeai kubeai/kubeai --wait --timeout 10m`</sub>
- **[ray-llm](https://github.com/ray-project/ray-llm)** — LLMs on Ray - RayLLM *(Archived)
  <sub>★ 1.3k · source · pushed 2025-03-13</sub>
  <sub>`git clone https://github.com/ray-project/ray-llm.git`</sub>
- **[Kaito](https://github.com/kaito-project/kaito)** — A Kubernetes operator that simplifies serving and tuning large AI models (e.g. Falcon or phi-3) using container images and GPU auto-provisioning. Includes an OpenAI-compatible server for inference and preset configurations for popular runtimes such as vLLM and transformers
  <sub>★ 1k · Go · source · pushed 2026-09-18 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/kaito-project/kaito.git`</sub>
- **[lanarky](https://github.com/ajndkr/lanarky)** — FastAPI framework to build production-grade LLM applications
  <sub>★ 990 · Python · MIT · pip · pushed 2024-07-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lanarky`</sub>
- **[Mosec](https://github.com/mosecorg/mosec)** — A machine learning model serving framework with dynamic batching and pipelined stages, provides an easy-to-use Python interface
  <sub>★ 902 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U mosec`</sub>
- **[mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go)** — Open-source MCP proxy with BM25 tool filtering, quarantine security, activity logging, and web UI. Routes multiple MCP servers through single endpoint, reducing context bloat by ~97%
  <sub>★ 376 · Go · MIT · go · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/smart-mcp-proxy/mcpproxy-go/cmd/mcpproxy@latest`</sub>
- **[KubeStellar Console](https://github.com/kubestellar/console)** — AI-powered multi-cluster Kubernetes dashboard for hybrid edge and cloud. GPU monitoring, LLM inference cluster management, benchmark streaming, and 20+ CNCF integrations. CNCF Sandbox (Apache 2.0)
  <sub>★ 137 · TypeScript · Apache-2.0 · brew · pushed 2026-09-21 · Win? · WSL2 · macOS · Linux?</sub>
  <sub>`brew tap kubestellar/tap`</sub>
- **[Open Responses](https://docs.julep.ai/open-responses)** — Serverless open-source platform for building long-running LLM agents with tool use
  <sub>website</sub>
  <sub>`https://docs.julep.ai/open-responses`</sub>

## ML Compiler

- **[TVM](https://github.com/apache/tvm)** — Open deep learning compiler stack for cpu, gpu and specialized accelerators
  <sub>★ 13.8k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/apache/tvm.git`</sub>
- **[bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes)** — Accessible large language models via k-bit quantization for PyTorch
  <sub>★ 8.5k · Python · MIT · source · pushed 2026-09-07 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/bitsandbytes-foundation/bitsandbytes.git`</sub>
- **[ONNX-MLIR](https://github.com/onnx/onnx-mlir)** — Compiler technology to transform a valid Open Neural Network Exchange (ONNX) graph into code that implements the graph with minimum runtime support
  <sub>★ 1.1k · C++ · Apache-2.0 · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/onnx/onnx-mlir.git`</sub>

## Frameworks for Training

- **[TensorFlow](https://github.com/tensorflow/tensorflow)** — An Open Source Machine Learning Framework for Everyone
  <sub>★ 200.2k · C++ · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install tensorflow`</sub>
- **[PyTorch](https://github.com/pytorch/pytorch)** — Tensors and Dynamic neural networks in Python with strong GPU acceleration
  <sub>★ 103.2k · Python · docker · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`docker run --gpus all --rm -ti --ipc=host pytorch/pytorch:latest`</sub>
- **[scikit-learn](https://github.com/scikit-learn/scikit-learn)** — Machine Learning in Python
  <sub>★ 67.3k · Python · BSD-3-Clause · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scikit-learn/scikit-learn.git`</sub>
- **[Keras](https://github.com/keras-team/keras)** — Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow
  <sub>★ 64.3k · Python · Apache-2.0 · pip · pushed 2026-09-19 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pip install keras --upgrade`</sub>
- **[DeepSpeed](https://github.com/deepspeedai/DeepSpeed)** — DeepSpeed is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective
  <sub>★ 43.1k · Python · Apache-2.0 · pip · pushed 2026-09-21 · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install deepspeed`</sub>
- **[ColossalAI](https://github.com/hpcaitech/ColossalAI)** — An integrated large-scale model training system with efficient parallelization techniques
  <sub>★ 41.4k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install colossalai`</sub>
- **[Jax](https://github.com/jax-ml/jax)** — Autograd and XLA for high-performance machine learning research
  <sub>★ 36.3k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`pip install -U jax`</sub>
- **[Caffe](https://github.com/BVLC/caffe)** — A fast open framework for deep learning
  <sub>★ 34.6k · C++ · source · pushed 2024-07-31 · Win?</sub>
  <sub>`git clone https://github.com/BVLC/caffe.git`</sub>
- **[PyTorch Lightning](https://github.com/Lightning-AI/pytorch-lightning)** — Deep learning framework to train, deploy, and ship AI products Lightning fast
  <sub>★ 31.4k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lightning`</sub>
- **[XGBoost](https://github.com/dmlc/xgboost)** — Scalable, Portable and Distributed Gradient Boosting (GBDT, GBRT or GBM) Library
  <sub>★ 28.8k · C++ · Apache-2.0 · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/dmlc/xgboost.git`</sub>
- **[PaddlePaddle](https://github.com/PaddlePaddle/Paddle)** — Machine Learning Framework from Industrial Practice
  <sub>★ 24.1k · C++ · Apache-2.0 · source · pushed 2026-09-21 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/PaddlePaddle/Paddle.git`</sub>
- **[Candle](https://github.com/huggingface/candle)** — Minimalist ML framework for Rust
  <sub>★ 21.1k · Rust · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/huggingface/candle.git`</sub>
- **[Apache MXNet](https://github.com/apache/mxnet)** — Lightweight, Portable, Flexible Distributed/Mobile Deep Learning with Dynamic, Mutation-aware Dataflow Dep Scheduler
  <sub>★ 20.8k · C++ · Apache-2.0 · source · pushed 2023-10-25 · Win?</sub>
  <sub>`git clone https://github.com/apache/mxnet.git`</sub>
- **[LightGBM](https://github.com/lightgbm-org/LightGBM)** — A fast, distributed, high performance gradient boosting (GBT, GBDT, GBRT, GBM or MART) framework based on decision tree algorithms, used for ranking, classification and many other machine learning tasks
  <sub>★ 18.8k · C++ · MIT · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/microsoft/LightGBM.git`</sub>
- **[Horovod](https://github.com/horovod/horovod)** — Distributed training framework for TensorFlow, Keras, PyTorch, and Apache MXNet
  <sub>★ 14.7k · Python · source · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/horovod/horovod.git`</sub>
- **[axolotl](https://github.com/axolotl-ai-cloud/axolotl)** — A tool designed to streamline the fine-tuning of various AI models, offering support for multiple configurations and architectures
  <sub>★ 12.5k · Python · Apache-2.0 · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run --gpus '"all"' --ipc=host --rm -it axolotlai/axolotl:main-latest`</sub>
- **[Kedro](https://github.com/kedro-org/kedro)** — Kedro is an open-source Python framework for creating reproducible, maintainable and modular data science code
  <sub>★ 11k · Python · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kedro-org/kedro.git`</sub>
- **[Accelerate](https://github.com/huggingface/accelerate)** — A simple way to train and use PyTorch models with multi-GPU, TPU, mixed-precision
  <sub>★ 9.9k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install accelerate`</sub>
- **[Oneflow](https://github.com/Oneflow-Inc/oneflow)** — OneFlow is a performance-centered and open-source deep learning framework
  <sub>★ 9.4k · C++ · Apache-2.0 · clone · pushed 2025-12-04 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Oneflow-Inc/oneflow.git`</sub>
- **[MegEngine](https://github.com/MegEngine/MegEngine)** — MegEngine is a fast, scalable and easy-to-use deep learning framework, with auto-differentiation
  <sub>★ 4.8k · C++ · Apache-2.0 · source · pushed 2024-10-24 · Win · WSL2 · macOS · Linux</sub>
  <sub>`git clone https://github.com/MegEngine/MegEngine.git`</sub>
- **[MindSpore](https://github.com/mindspore-ai/mindspore)** — MindSpore is a new open source deep learning training/inference framework that could be used for mobile, edge and cloud scenarios
  <sub>★ 4.7k · C++ · Apache-2.0 · pip · pushed 2024-07-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install https://ms-release.obs.cn-north-4.myhuaweicloud.com/1.2.0-rc1/MindSpore/cpu/ubuntu_x86/mindspore-1.2.0rc1-cp37-cp37m-linux_x86_64.whl`</sub>
- **[metric-learn](https://github.com/scikit-learn-contrib/metric-learn)** — Metric Learning Algorithms in Python
  <sub>★ 1.4k · Python · MIT · pip · pushed 2026-03-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install metric-learn`</sub>
- **[VectorFlow](https://github.com/Netflix/vectorflow)** — A minimalist neural network library optimized for sparse data and single machine environments
  <sub>★ 1.3k · D · Apache-2.0 · source · pushed 2024-05-02 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Netflix/vectorflow.git`</sub>

## AutoML

- **[Optuna](https://github.com/optuna/optuna)** — A hyperparameter optimization framework
  <sub>★ 14.8k · Python · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/optuna/optuna.git`</sub>
- **[NNI](https://github.com/microsoft/nni)** — An open source AutoML toolkit for automate machine learning lifecycle, including feature engineering, neural architecture search, model compression and hyper-parameter tuning
  <sub>★ 14.4k · Python · MIT · source · pushed 2024-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Microsoft/nni.git`</sub>
- **[Ludwig](https://github.com/ludwig-ai/ludwig)** — a toolbox built on top of TensorFlow that allows to train and test deep learning models without the need to write code
  <sub>★ 11.8k · Python · Apache-2.0 · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ludwig # core`</sub>
- **[AutoGluon](https://github.com/autogluon/autogluon)** — AutoML for Image, Text, and Tabular Data
  <sub>★ 10.7k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install autogluon`</sub>
- **[Pycaret](https://github.com/pycaret/pycaret)** — An open-source, low-code machine learning library in Python that automates machine learning workflows
  <sub>★ 9.8k · Python · clone · pushed 2026-07-23 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/pycaret/pycaret.git`</sub>
- **[autokeras](https://github.com/keras-team/autokeras)** — AutoML library for deep learning
  <sub>★ 9.3k · Python · Apache-2.0 · pip · pushed 2025-11-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip3 install autokeras`</sub>
- **[auto-sklearn](https://github.com/automl/auto-sklearn)** — an automated machine learning toolkit and a drop-in replacement for a scikit-learn estimator
  <sub>★ 8.1k · Python · BSD-3-Clause · source · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automl/auto-sklearn.git`</sub>
- **[Hyperopt](https://github.com/hyperopt/hyperopt)** — Distributed Asynchronous Hyperparameter Optimization in Python
  <sub>★ 7.6k · Python · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install hyperopt`</sub>
- **[AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG)** — AutoML tool for RAG - Boost your LLM app performance with your own data
  <sub>★ 5.1k · TypeScript · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @autorag/librarian`</sub>
- **[FLAML](https://github.com/microsoft/FLAML)** — Fast and lightweight AutoML (paper)
  <sub>★ 4.4k · Jupyter Notebook · MIT · pip · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install flaml`</sub>
- **[Determined](https://github.com/determined-ai/determined)** — scalable deep learning training platform with integrated hyperparameter tuning support; includes Hyperband, PBT, and other search methods
  <sub>★ 3.2k · Go · Apache-2.0 · pip · pushed 2025-03-20 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`pip install determined`</sub>
- **[Model Search](https://github.com/google/model_search)** — a framework that implements AutoML algorithms for model architecture search at scale
  <sub>★ 3.2k · Python · Apache-2.0 · source · pushed 2024-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/google/model_search.git`</sub>
- **[Keras Tuner](https://github.com/keras-team/keras-tuner)** — Hyperparameter tuning for humans
  <sub>★ 2.9k · Python · Apache-2.0 · pip · pushed 2025-12-01 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install keras-tuner`</sub>
- **[learn2learn](https://github.com/learnables/learn2learn)** — PyTorch Meta-learning Framework for Researchers
  <sub>★ 2.9k · Python · MIT · source · pushed 2025-12-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/learnables/learn2learn.git`</sub>
- **[scikit-optimize(skopt)](https://github.com/scikit-optimize/scikit-optimize)** — Sequential model-based optimization with a scipy.optimize interface
  <sub>★ 2.8k · Python · BSD-3-Clause · source · pushed 2024-02-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/scikit-optimize/scikit-optimize.git`</sub>
- **[Auto-PyTorch](https://github.com/automl/Auto-PyTorch)** — Automatic architecture search and hyperparameter optimization for PyTorch
  <sub>★ 2.5k · Python · Apache-2.0 · pip · pushed 2024-04-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install autoPyTorch`</sub>
- **[Torchmeta](https://github.com/tristandeleu/pytorch-meta)** — A Meta-Learning library for PyTorch
  <sub>★ 2.1k · Python · MIT · pip · pushed 2023-07-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install torchmeta`</sub>
- **[automl-gs](https://github.com/minimaxir/automl-gs)** — Provide an input CSV and a target field to predict, generate a model + code to run it
  <sub>★ 1.9k · Python · MIT · pip · pushed 2019-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip3 install automl_gs`</sub>
- **[Katib](https://github.com/kubeflow/katib)** — Katib is a Kubernetes-native project for automated machine learning (AutoML)
  <sub>★ 1.7k · Python · Apache-2.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`pip install -U kubeflow-katib`</sub>
- **[Spearmint](https://github.com/HIPS/Spearmint)** — a software package to perform Bayesian optimization
  <sub>★ 1.6k · Python · pip · pushed 2019-12-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -e \</path/to/spearmint/root\>`</sub>
- **[MOE](https://github.com/YelpArchive/MOE)** — a global, black box optimization engine for real world metric optimization by Yelp
  <sub>★ 1.3k · C++ · source · pushed 2023-03-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Yelp/MOE.git`</sub>
- **[AutoGL](https://github.com/THUMNLab/AutoGL)** — An autoML framework &amp; toolkit for machine learning on graphs
  <sub>★ 1.1k · Python · Apache-2.0 · pip · pushed 2025-11-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install autogl`</sub>
- **[DEvol (DeepEvolution)](https://github.com/joeddav/devol)** — a basic proof of concept for genetic architecture search in Keras
  <sub>★ 952 · Python · MIT · source · pushed 2023-05-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/joeddav/devol.git`</sub>
- **[Dragonfly](https://github.com/dragonfly/dragonfly)** — An open source python library for scalable Bayesian optimisation
  <sub>★ 894 · Python · MIT · source · pushed 2023-06-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dragonfly/dragonfly.git`</sub>
- **[EvalML](https://github.com/alteryx/evalml)** — An open source python library for AutoML
  <sub>★ 850 · Python · BSD-3-Clause · pip · pushed 2026-01-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evalml`</sub>
- **[Vegas](https://github.com/huawei-noah/vega)** — an AutoML algorithm tool chain by Huawei Noah's Arb Lab
  <sub>★ 848 · Python · pip · pushed 2023-02-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip3 install --user --upgrade noah-vega`</sub>
- **[FEDOT](https://github.com/aimclub/FEDOT)** — AutoML framework for the design of composite pipelines
  <sub>★ 711 · Python · BSD-3-Clause · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/nccr-itmo/FEDOT.git`</sub>
- **[HpBandSter](https://github.com/automl/HpBandSter)** — a framework for distributed hyperparameter optimization
  <sub>★ 633 · Python · BSD-3-Clause · pip · pushed 2022-10-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install hpbandster`</sub>
- **[Hyperband](https://github.com/zygmuntz/hyperband)** — open source code for tuning hyperparams with Hyperband
  <sub>★ 598 · Python · source · pushed 2018-08-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/zygmuntz/hyperband.git`</sub>
- **[RoBO](https://github.com/automl/RoBO)** — a Robust Bayesian Optimization framework
  <sub>★ 496 · Python · BSD-3-Clause · clone · pushed 2019-04-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automl/RoBO`</sub>
- **[Archai](https://github.com/microsoft/archai)** — a platform for Neural Network Search (NAS) that allows you to generate efficient deep networks for your applications
  <sub>★ 486 · Python · MIT · pip · pushed 2026-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install archai`</sub>
- **[Goptuna](https://github.com/c-bata/goptuna)** — A hyperparameter optimization framework, inspired by Optuna
  <sub>★ 280 · Go · MIT · source · pushed 2025-08-12 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/c-bata/goptuna.git`</sub>
- **[Hypernets](https://github.com/DataCanvasIO/Hypernets)** — A General Automated Machine Learning Framework
  <sub>★ 266 · Python · Apache-2.0 · pip · pushed 2026-04-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install hypernets`</sub>
- **[autoai](https://github.com/blobcity/autoai)** — A framework to find the best performing AI/ML model for any AI problem
  <sub>★ 186 · Python · Apache-2.0 · pip · pushed 2025-03-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install blobcity`</sub>
- **[HPOlib2](https://github.com/automl/HPOBench)** — a library for hyperparameter optimization and black box optimization benchmarks
  <sub>★ 172 · Python · Apache-2.0 · clone · pushed 2025-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/automl/HPOBench.git`</sub>
- **[hyperunity](https://github.com/gdikov/hypertunity)** — A toolset for black-box hyperparameter optimisation
  <sub>★ 137 · Python · Apache-2.0 · pip · pushed 2020-01-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install hypertunity`</sub>
- **[REMBO](https://github.com/ziyuw/rembo)** — Bayesian optimization in high-dimensions via random embedding
  <sub>★ 116 · MATLAB · source · pushed 2013-08-04</sub>
  <sub>`git clone https://github.com/ziyuw/rembo.git`</sub>
- **[Intelli](https://github.com/intelligentnode/Intelli)** — A framework to connect a flow of ML models by applying graph theory
  <sub>★ 55 · Python · Apache-2.0 · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install intelli`</sub>
- **[NASGym](https://github.com/gomerudo/nas-env)** — a proof-of-concept OpenAI Gym environment for Neural Architecture Search (NAS)
  <sub>★ 31 · Python · MIT · source · pushed 2020-05-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/gomerudo/nas-env.git`</sub>
- **[TPOT](http://automl.info/tpot/)** — one of the very first AutoML methods and open-source software packages
  <sub>website</sub>
  <sub>`http://automl.info/tpot/`</sub>

## Experiment Tracking

- **[Weights &amp; Biases](https://github.com/wandb/wandb)** — A developer first, lightweight, user-friendly experiment tracking and visualization tool for machine learning projects, streamlining collaboration and simplifying MLOps. W&amp;B excels at tracking LLM-powered applications, featuring W&amp;B Prompts for LLM execution flow visualization, input and output monitoring, and secure management of prompts and LLM chain configurations
  <sub>★ 11.3k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install wandb`</sub>
- **[ClearML](https://github.com/clearml/clearml)** — Auto-Magical CI/CD to streamline your ML workflow. Experiment Manager, MLOps and Data-Management
  <sub>★ 6.9k · Python · Apache-2.0 · pip · pushed 2026-09-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install clearml`</sub>
- **[Aim](https://github.com/aimhubio/aim)** — an easy-to-use and performant open-source experiment tracker
  <sub>★ 6.3k · Python · Apache-2.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip3 install aim`</sub>
- **[Sacred](https://github.com/IDSIA/sacred)** — Sacred is a tool to help you configure, organize, log and reproduce experiments
  <sub>★ 4.4k · Python · MIT · source · pushed 2025-10-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/IDSIA/sacred.git`</sub>
- **[MLRun](https://github.com/mlrun/mlrun)** — Machine Learning automation and tracking
  <sub>★ 1.7k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/mlrun/mlrun.git`</sub>
- **[Guild AI](https://github.com/guildai/guildai)** — Experiment tracking, ML developer tools
  <sub>★ 907 · Python · Apache-2.0 · source · pushed 2025-04-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/guildai/guildai.git`</sub>
- **[Kedro-Viz](https://github.com/kedro-org/kedro-viz)** — Kedro-Viz is an interactive development tool for building data science pipelines with Kedro. Kedro-Viz also allows users to view and compare different runs in the Kedro project
  <sub>★ 762 · JavaScript · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kedro-org/kedro-viz.git`</sub>
- **[LabNotebook](https://github.com/henripal/labnotebook)** — LabNotebook is a tool that allows you to flexibly monitor, record, save, and query all your machine learning experiments
  <sub>★ 528 · Jupyter Notebook · MIT · clone · pushed 2018-03-31 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/henripal/labnotebook.git`</sub>
- **[Comet](https://github.com/comet-ml/comet-examples)** — Comet is an MLOps platform that offers experiment tracking, model production management, a model registry, and full data lineage from training straight through to production. Comet plays nicely with all your favorite tools, so you don't have to change your existing workflow. Comet Opik to confidently evaluate, test, and ship LLM applications with a suite of observability tools to calibrate languag
  <sub>★ 176 · Jupyter Notebook · pip · pushed 2026-08-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install comet_ml`</sub>

## Federated ML

- **[Flower](https://github.com/flwrlabs/flower)** — A Friendly Federated Learning Framework
  <sub>★ 7.1k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/adap/flower.git`</sub>
- **[FATE](https://github.com/FederatedAI/FATE)** — An Industrial Grade Federated Learning Framework
  <sub>★ 6.1k · Python · Apache-2.0 · source · pushed 2024-11-19 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/FederatedAI/FATE.git`</sub>
- **[FedML](https://github.com/FedML-AI/FedML)** — The federated learning and analytics library enabling secure and collaborative machine learning on decentralized data anywhere at any scale. Supporting large-scale cross-silo federated learning, cross-device federated learning on smartphones/IoTs, and research simulation
  <sub>★ 4.1k · Python · Apache-2.0 · source · pushed 2025-10-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/FedML-AI/FedML.git`</sub>
- **[TensorFlow Federated](https://github.com/google-parfait/tensorflow-federated)** — A framework for implementing federated learning
  <sub>★ 2.5k · Python · Apache-2.0 · source · pushed 2026-09-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tensorflow/federated.git`</sub>
- **[EasyFL](https://github.com/EasyFL-AI/EasyFL)** — An Easy-to-use Federated Learning Platform
  <sub>★ 26 · Python · Apache-2.0 · source · pushed 2023-08-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/EasyFL-AI/EasyFL.git`</sub>
- **[Harmonia](https://github.com/ailabstw/harmonia)** — Harmonia is an open-source project aiming at developing systems/infrastructures and libraries to ease the adoption of federated learning (abbreviated to FL) for researches and production usage
  <sub>★ 17 · Go · MPL-2.0 · source · pushed 2020-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ailabstw/harmonia.git`</sub>

## LLMOps

- **[Dify](https://github.com/langgenius/dify)** — Open-source framework aims to enable developers (and even non-developers) to quickly build useful applications based on large language models, ensuring they are visual, operable, and improvable
  <sub>★ 156.7k · TypeScript · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/langgenius/dify.git`</sub>
- **[LangFlow](https://github.com/langflow-ai/langflow)** — An effortless way to experiment and prototype LangChain flows with drag-and-drop components and a chat interface
  <sub>★ 155.1k · Python · MIT · docker · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run -p 7860:7860 langflowai/langflow:latest`</sub>
- **[langchain](https://github.com/langchain-ai/langchain)** — Building applications with LLMs through composability
  <sub>★ 146.8k · Python · MIT · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/hwchase17/langchain.git`</sub>
- **[Embedchain](https://github.com/mem0ai/mem0)** — Framework to create ChatGPT like bots over your dataset
  <sub>★ 65.8k · Python · Apache-2.0 · npm · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`npm install -g @mem0/cli # or: pip install mem0-cli`</sub>
- **[LiteLLM 🚅](https://github.com/BerriAI/litellm/)** — A simple &amp; light 100 line package to standardize LLM API calls across OpenAI, Azure, Cohere, Anthropic, Replicate API Endpoints
  <sub>★ 59.3k · Python · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install 'litellm[proxy]'`</sub>
- **[LLMApp](https://github.com/pathwaycom/llm-app)** — LLM App is a Python library that helps you build real-time LLM-enabled data pipelines with few lines of code
  <sub>★ 58.9k · Jupyter Notebook · MIT · source · pushed 2026-07-05 · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pathwaycom/llm-app.git`</sub>
- **[LlamaIndex](https://github.com/run-llama/llama_index)** — Provides a central interface to connect your LLMs with external data
  <sub>★ 52.3k · Python · MIT · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llama-index-core`</sub>
- **[Langfuse](https://github.com/langfuse/langfuse)** — Open Source LLM Engineering Platform: Traces, evals, prompt management and metrics to debug and improve your LLM application
  <sub>★ 34.9k · TypeScript · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install langfuse openai`</sub>
- **[Haystack](https://github.com/deepset-ai/haystack)** — Quickly compose applications with LLM Agents, semantic search, question-answering and more
  <sub>★ 26.6k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install haystack-ai`</sub>
- **[promptfoo](https://github.com/promptfoo/promptfoo)** — Open-source tool for testing &amp; evaluating prompt quality. Create test cases, automatically check output quality and catch regressions, and reduce evaluation cost
  <sub>★ 25.3k · TypeScript · MIT · npm · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g promptfoo`</sub>
- **[Opik](https://github.com/comet-ml/opik)** — Confidently evaluate, test, and ship LLM applications with a suite of observability tools to calibrate language model outputs across your dev and production lifecycle
  <sub>★ 22.2k · Python · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx add-mcp https://www.comet.com/opik/api/v1/mcp --name opik-mcp`</sub>
- **[Arize-Phoenix](https://github.com/Arize-ai/phoenix)** — ML observability for LLMs, vision, language, and tabular models
  <sub>★ 11.6k · Python · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @arizeai/phoenix-cli setup`</sub>
- **[Hive](https://github.com/aden-hive/hive)** — Open-source AI agent framework for building goal-driven, self-improving autonomous agents with auto-generated graphs, evolution loops, and MCP integration
  <sub>★ 11.1k · Python · Apache-2.0 · clone · pushed 2026-09-14 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aden-hive/hive.git`</sub>
- **[deeplake](https://github.com/activeloopai/deeplake)** — Stream large multimodal datasets to achieve near 100% GPU utilization. Query, visualize, &amp; version control data. Access data w/o the need to recompute the embeddings for the model finetuning
  <sub>★ 9.2k · C++ · Apache-2.0 · pip · pushed 2026-05-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install deeplake`</sub>
- **[PraisonAI](https://github.com/MervinPraison/PraisonAI)** — Production-ready Multi-AI Agents framework with self-reflection. Fastest agent instantiation (3.77μs), 100+ LLM support via LiteLLM, MCP integration, agentic workflows (route/parallel/loop/repeat), built-in memory, Python &amp; JS SDKs
  <sub>★ 9.1k · Python · MIT · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install praisonai`</sub>
- **[GPTCache](https://github.com/zilliztech/GPTCache)** — Creating semantic cache to store responses from LLM queries
  <sub>★ 8.2k · Python · MIT · pip · pushed 2025-07-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install gptcache`</sub>
- **[GPUStack](https://github.com/gpustack/gpustack)** — An open-source GPU cluster manager for running and managing LLMs
  <sub>★ 5.7k · Python · Apache-2.0 · source · pushed 2026-09-21 · Win · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/gpustack/gpustack.git`</sub>
- **[ZenML](https://github.com/zenml-io/zenml)** — Open-source framework for orchestrating, experimenting and deploying production-grade ML solutions, with built-in langchain &amp; llama_index integrations
  <sub>★ 5.6k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "zenml[server]" # pip install zenml will install a slimmer client`</sub>
- **[LangWatch](https://github.com/langwatch/langwatch)** — LLM Ops platform with Analytics, Monitoring, Evaluations and an LLM Optimization Studio powered by DSPy
  <sub>★ 4.8k · TypeScript · Apache-2.0 · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx langwatch claude # or codex, copilot, opencode, ...`</sub>
- **[agenta](https://github.com/Agenta-AI/agenta)** — The LLMOps platform to build robust LLM apps. Easily experiment and evaluate different prompts, models, and workflows to build robust apps
  <sub>★ 4.8k · TypeScript · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Agenta-AI/agenta.git`</sub>
- **[Laminar](https://github.com/lmnr-ai/lmnr)** — Open-source all-in-one platform for engineering AI products. Traces, Evals, Datasets, Labels
  <sub>★ 3.3k · TypeScript · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install --upgrade 'lmnr[all]'`</sub>
- **[Pezzo 🕹️](https://github.com/pezzolabs/pezzo)** — Pezzo is the open-source LLMOps platform built for developers and teams. In just two lines of code, you can seamlessly troubleshoot your AI operations, collaborate and manage your prompts in one place, and instantly deploy changes to any environment
  <sub>★ 3.3k · TypeScript · Apache-2.0 · source · pushed 2026-08-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/pezzolabs/pezzo.git`</sub>
- **[Cheshire Cat AI](https://github.com/cheshire-cat-ai/core)** — Web framework to create vertical AI agents. FastAPI based, plugin system inspired to WordPress, admin panel, vector DB included
  <sub>★ 3.1k · Python · GPL-3.0 · source · pushed 2026-07-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/cheshire-cat-ai/core.git`</sub>
- **[prompttools](https://github.com/hegelai/prompttools)** — Open-source tools for testing and experimenting with prompts. The core idea is to enable developers to evaluate prompts using familiar interfaces like code and notebooks. In just a few lines of codes, you can test your prompts and parameters across different models (whether you are using OpenAI, Anthropic, or LLaMA models). You can even evaluate the retrieval accuracy of vector databases
  <sub>★ 3.1k · Python · Apache-2.0 · pip · pushed 2026-02-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install prompttools`</sub>
- **[OpenLIT](https://github.com/openlit/openlit)** — OpenLIT is an OpenTelemetry-native GenAI and LLM Application Observability tool and provides OpenTelmetry Auto-instrumentation for monitoring LLMs, VectorDBs and Frameworks. It provides valuable insights into token &amp; cost usage, user interaction, and performance related metrics
  <sub>★ 2.8k · TypeScript · Apache-2.0 · pip · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install openlit`</sub>
- **[xTuring](https://github.com/stochasticai/xTuring)** — Build and control your personal LLMs with fast and efficient fine-tuning
  <sub>★ 2.7k · Python · Apache-2.0 · pip · pushed 2026-09-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install xturing`</sub>
- **[AgentField](https://github.com/Agent-Field/agentfield)** — Open-source control plane for building and operating AI agents like APIs at scale, with routing, memory, observability, identity, auth, and policy controls
  <sub>★ 2.6k · Go · Apache-2.0 · script · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentfield.ai/install.sh | bash`</sub>
- **[magentic](https://github.com/jackmpcollins/magentic)** — Seamlessly integrate LLMs as Python functions. Use type annotations to specify structured output. Mix LLM queries and function calling with regular Python code to create complex LLM-powered functionality
  <sub>★ 2.4k · Python · MIT · pip · pushed 2026-03-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install magentic`</sub>
- **[Dstack](https://github.com/dstackai/dstack)** — Cost-effective LLM development in any cloud (AWS, GCP, Azure, Lambda, etc)
  <sub>★ 2.3k · Python · MPL-2.0 · source · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dstackai/dstack.git`</sub>
- **[future-agi](https://github.com/future-agi/future-agi)** — Open-source self-hostable end-to-end agent engineering and optimization platform unifying tracing, evals, simulations, datasets, gateway, and guardrails for LLM and AI agent applications
  <sub>★ 2k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux? · Docker</sub>
  <sub>`pip install futureagi`</sub>
- **[Mirascope](https://github.com/Mirascope/mirascope)** — Intuitive convenience tooling for lightning-fast, efficient development and ensuring quality in LLM-based applications
  <sub>★ 1.5k · Python · MIT · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Mirascope/mirascope.git`</sub>
- **[BudgetML](https://github.com/ebhy/budgetml)** — Deploy a ML inference service on a budget in less than 10 lines of code
  <sub>★ 1.3k · Python · Apache-2.0 · pip · pushed 2024-02-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install budgetml`</sub>
- **[LangKit](https://github.com/whylabs/langkit)** — Out-of-the-box LLM telemetry collection library that extracts features and profiles prompts, responses and metadata about how your LLM is performing over time to find problems at scale
  <sub>★ 997 · Jupyter Notebook · Apache-2.0 · pip · pushed 2024-11-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install langkit[all]`</sub>
- **[LLMFlows](https://github.com/stoyan-stoyanov/llmflows)** — LLMFlows is a framework for building simple, explicit, and transparent LLM applications such as chatbots, question-answering systems, and agents
  <sub>★ 708 · Python · MIT · pip · pushed 2025-02-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llmflows`</sub>
- **[SwarmClaw](https://github.com/swarmclawai/swarmclaw)** — Self-hosted multi-agent AI runtime with 23+ LLM providers, persistent memory, skills, schedules, sub-agent spawning, and MCP client + server support. Ships as desktop app, CLI, or Docker
  <sub>★ 680 · TypeScript · MIT · npm · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm i -g @swarmclawai/swarmclaw`</sub>
- **[Contexto](https://github.com/ekailabs/contexto)** — Self-hosted context engine for AI agents with persistent conversation memory and recall. Works as a drop-in OpenAI-compatible proxy, OpenClaw plugin, or memory SDK — no code changes required
  <sub>★ 621 · TypeScript · Apache-2.0 · pip · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install contexto-hermes`</sub>
- **[Rhesis](https://github.com/rhesis-ai/rhesis)** — Open-source testing infrastructure for LLM and agentic applications. Collaborative platform enabling teams to define quality metrics, run evaluations, and ship confidently with version control and peer review workflows built for AI engineering
  <sub>★ 392 · Python · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add rhesis-ai/rhesis`</sub>
- **[Statewave](https://github.com/smaramwbc/statewave)** — Open-source memory runtime for AI agents. Compiles events into deterministic, provenance-tagged context bundles instead of query-time retrieval. Apache-2.0, self-hostable on Postgres + pgvector
  <sub>★ 347 · Python · Apache-2.0 · psh · pushed 2026-09-19 · Win · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`irm https://www.statewave.ai/install.ps1 | iex`</sub>
- **[Mengram](https://github.com/alibaizhanov/mengram)** — Open-source memory infrastructure for AI agents. Provides semantic (entities/facts), episodic (conversations), and procedural (learned behaviors) memory with auto-reflection. Python SDK, JS SDK, MCP server, and REST API
  <sub>★ 201 · Python · Apache-2.0 · pip · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mengram-ai # or: npm install mengram-ai`</sub>
- **[AI studio](https://github.com/pyadav/gateway)** — A Reliable Open Source AI studio to build core infrastructure stack for your LLM Applications. It allows you to gain visibility, make your application reliable, and prepare it for production with features such as caching, rate limiting, exponential retry, model fallback, and more
  <sub>★ 161 · Go · Apache-2.0 · brew · pushed 2024-04-08 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install missingstudio/tap/gateway`</sub>
- **[Glide](https://github.com/EinStack/glide)** — Cloud-Native LLM Routing Engine. Improve LLM app resilience and speed
  <sub>★ 160 · Go · Apache-2.0 · brew · pushed 2024-08-12 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`brew install einstack/tap/glide`</sub>
- **[Neurolink](https://github.com/juspay/neurolink)** — Multi-provider AI agent framework that unifies 12+ LLM providers (OpenAI, Google, Anthropic, AWS, Azure, Groq, etc.) with workflow orchestration. Production-grade platform for building LLM applications with streaming, tool calling, caching, and enterprise features. Battle-tested at 15M+ requests/month
  <sub>★ 135 · TypeScript · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx @juspay/neurolink --help`</sub>
- **[Roundtable](https://github.com/yylo-dev/roundtable)** — Zero-configuration unified AI assistant management built on the FastMCP framework. Provides seamless integration with Claude, ChatGPT, and other AI assistants through a single MCP interface with session management, logging, and production-ready operations
  <sub>★ 125 · Python · npx · pushed 2025-10-06 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx @roundtable/mcp-server`</sub>
- **[ai-evaluation](https://github.com/future-agi/agent-learning-kit)** — Evaluation framework for automated, reproducible scoring of LLM, agent, and workflow performance
  <sub>★ 120 · Python · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/future-agi/agent-learning-kit`</sub>
- **[PromptMage](https://github.com/tsterbak/promptmage)** — Open-source tool to simplify the process of creating and managing LLM workflows and prompts as a self-hosted solution
  <sub>★ 116 · Python · MIT · pip · pushed 2024-10-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install promptmage`</sub>
- **[LRM](https://github.com/nickprotop/LocalizationManager)** — CLI/TUI tool for managing localization files (.resx, JSON, Android, iOS) with LLM-powered translation via Ollama, validation, and code scanning for unused/missing keys
  <sub>★ 50 · CSS · MIT · script · pushed 2026-07-10 · Win · WSL2? · macOS · Linux</sub>
  <sub>`curl -sSL https://raw.githubusercontent.com/nickprotop/LocalizationManager/main/install-lrm.sh | bash`</sub>
- **[PromptSite](https://github.com/dkuang1980/promptsite)** — A lightweight Python library for prompt lifecycle management that helps you version control, track, experiment and debug with your LLM prompts with ease. Minimal setup, no servers, databases, or API keys required - works directly with your local filesystem, ideal for data scientists and engineers to easily integrate into existing LLM workflows
  <sub>★ 46 · Python · Apache-2.0 · pip · pushed 2025-02-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install promptsite`</sub>
- **[Hypersigil](https://github.com/hypersigilhq/hypersigil)** — Open-source prompt lifecycle management and gateway with a Web UI
  <sub>★ 28 · Vue · docker · pushed 2026-04-17 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -d --name hypersigil -p 8080:80 -v $(pwd)/hypersigil:/app/data --init codefibers/hypersigil:latest`</sub>
- **[Semantic Cache Router](https://github.com/redjackfred/distributed-semantic-cache-and-stateful-routing-system)** — Distributed semantic cache and stateful routing system that cuts LLM API costs by returning cached responses for semantically similar queries. Uses ANN vector search (cosine ≥ 0.8) and consistent hashing to pin requests to the same worker, achieving ~7× latency reduction on cache hits while scaling horizontally without cache thrash
  <sub>★ 1 · Python · clone · pushed 2026-04-05 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/redjackfred/distributed-semantic-cache-and-stateful-routing-system.git`</sub>
- **[AgentMark](https://github.com/puzzlet-ai/agentmark)** — Type-Safe Markdown-based Agents
  <sub>unavailable</sub>
- **[Dataoorts](https://dataoorts.com/ai)** — Enjoy unlimited API calls with Serverless AI Workers/LLMs for just $25 per month. No rate or concurrency limits
  <sub>website</sub>
  <sub>`https://dataoorts.com/ai`</sub>
- **[Epsilla](https://epsilla.com)** — An all-in-one platform to create vertical AI agents powered by your private data and knowledge
  <sub>website</sub>
  <sub>`https://epsilla.com`</sub>
- **[Fiddler AI](https://www.fiddler.ai/llmops)** — Evaluate, monitor, analyze, and improve MLOps and LLMOps from pre-production to production
  <sub>website</sub>
  <sub>`https://www.fiddler.ai/llmops`</sub>
- **[gotoHuman](https://www.gotohuman.com)** — Bring a human into the loop in your LLM-based and agentic workflows. Prompt users to approve actions, select next steps, or review and validate generated results
  <sub>website</sub>
  <sub>`https://www.gotohuman.com`</sub>
- **[Humanloop](https://humanloop.com)** — The LLM evals platform for enterprises, providing tools to develop, evaluate, and observe AI systems
  <sub>website</sub>
  <sub>`https://humanloop.com`</sub>
- **[Izlo](https://getizlo.com/)** — Prompt management tools for teams. Store, improve, test, and deploy your prompts in one unified workspace
  <sub>website</sub>
  <sub>`https://getizlo.com/`</sub>
- **[Keywords AI](https://keywordsai.co/)** — A unified DevOps platform for AI software. Keywords AI makes it easy for developers to build LLM applications
  <sub>website</sub>
  <sub>`https://keywordsai.co/`</sub>
- **[MLflow](https://github.com/mlflow/mlflow/tree/master)** — An open-source framework for the end-to-end machine learning lifecycle, helping developers track experiments, evaluate models/prompts, deploy models, and add observability with tracing
  <sub>Python · Apache-2.0 · in-repo · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/mlflow/mlflow.git && cd mlflow/master`</sub>
- **[Literal AI](https://literalai.com/)** — Multi-modal LLM observability and evaluation platform. Create prompt templates, deploy prompts versions, debug LLM runs, create datasets, run evaluations, monitor LLM metrics and collect human feedback
  <sub>website</sub>
  <sub>`https://literalai.com/`</sub>
- **[Lunary](https://github.com/lunary-ai/lunary)** — Observability and prompt management for LLM chabots and agents. Debug agents with powerful tracing and logging. Usage analytics and dive deep into the history of your requests. Developer friendly modules with plug-and-play integration into LangChain
  <sub>unavailable</sub>
- **[Manag.ai](https://www.manag.ai)** — Your all-in-one prompt management and observability platform. Craft, track, and perfect your LLM prompts with ease
  <sub>website</sub>
  <sub>`https://www.manag.ai`</sub>
- **[Parea AI](https://www.parea.ai/)** — Platform and SDK for AI Engineers providing tools for LLM evaluation, observability, and a version-controlled enhanced prompt playground
  <sub>website</sub>
  <sub>`https://www.parea.ai/`</sub>
- **[PromptDX](https://github.com/puzzlet-ai/promptdx)** — A declarative, extensible, and composable approach for developing LLM prompts using Markdown and JSX
  <sub>unavailable</sub>
- **[PromptHub](https://www.prompthub.us)** — Full stack prompt management tool designed to be usable by technical and non-technical team members. Test, version, collaborate, deploy, and monitor, all from one place
  <sub>website</sub>
  <sub>`https://www.prompthub.us`</sub>
- **[PromptFoundry](https://www.promptfoundry.ai)** — The simple prompt engineering and evaluation tool designed for developers building AI applications
  <sub>website</sub>
  <sub>`https://www.promptfoundry.ai`</sub>
- **[PromptLayer 🍰](https://www.promptlayer.com)** — Prompt Engineering platform. Collaborate, test, evaluate, and monitor your LLM applications
  <sub>website</sub>
  <sub>`https://www.promptlayer.com`</sub>
- **[Prompteams](https://www.prompteams.com)** — Prompt management system. Version, test, collaborate, and retrieve prompts through real-time APIs. Have GitHub style with repos, branches, and commits (and commit history)
  <sub>website</sub>
  <sub>`https://www.prompteams.com`</sub>
- **[Puzzlet AI](https://www.puzzlet.ai)** — The Git-Based LLM Engineering Platform. Achieve more from GenAI: Manage, evaluate, and improve your full-stack LLM application - with version control, type-safety, and local development built-in
  <sub>website</sub>
  <sub>`https://www.puzzlet.ai`</sub>
- **[systemprompt.io](https://systemprompt.io)** — Systemprompt.io is a Rest API with quality tooling to enable the creation, use and observability of prompts in any AI system. Control every detail of your prompt for a SOTA prompt management experience
  <sub>website</sub>
  <sub>`https://systemprompt.io`</sub>
- **[TeamoRouter](https://router.teamolab.com)** — LLM routing gateway for OpenClaw. One API key to access Claude, GPT-4o, Gemini, DeepSeek, Kimi, MiniMax. Smart routing modes (teamo-best, teamo-balanced, teamo-eco) auto-pick the optimal model. Up to 50% off official prices. 2-second install via skill.md
  <sub>website</sub>
  <sub>`https://router.teamolab.com`</sub>
- **[TreeScale](https://treescale.com)** — All In One Dev Platform For LLM Apps. Deploy LLM-enhanced APIs seamlessly using tools for prompt optimization, semantic querying, version management, statistical evaluation, and performance tracking. As a part of the developer friendly API implementation TreeScale offers Elastic LLM product, which makes a unified API Endpoint for all major LLM providers and open source models
  <sub>website</sub>
  <sub>`https://treescale.com`</sub>
- **[TrueFoundry](https://www.truefoundry.com/)** — Deploy LLMOps tools like Vector DBs, Embedding server etc on your own Kubernetes (EKS,AKS,GKE,On-prem) Infra including deploying, Fine-tuning, tracking Prompts and serving Open Source LLM Models with full Data Security and Optimal GPU Management. Train and Launch your LLM Application at Production scale with best Software Engineering practices
  <sub>website</sub>
  <sub>`https://www.truefoundry.com/`</sub>
- **[ReliableGPT 💪](https://github.com/BerriAI/reliableGPT/)** — Handle OpenAI Errors (overloaded OpenAI servers, rotated keys, or context window errors) for your production LLM Applications
  <sub>unavailable</sub>
- **[Registry Broker](https://github.com/hashgraph-online/registry-broker)** — Universal index and routing layer for AI agents. Aggregates agent metadata from multiple registries (NANDA, MCP, Virtuals, OpenRouter, A2A, X402 Bazaar) across web2 and web3, normalizes profiles, and provides protocol translation between agent ecosystems
  <sub>unavailable</sub>
- **[Portkey](https://portkey.ai/)** — Control Panel with an observability suite &amp; an AI gateway — to ship fast, reliable, and cost-efficient apps
  <sub>website</sub>
  <sub>`https://portkey.ai/`</sub>
- **[TensorZero](https://www.tensorzero.com/)** — TensorZero is an open-source framework for building production-grade LLM applications. It unifies an LLM gateway, observability, optimization, evaluations, and experimentation
  <sub>website</sub>
  <sub>`https://www.tensorzero.com/`</sub>
- **[Vellum](https://www.vellum.ai/)** — An AI product development platform to experiment with, evaluate, and deploy advanced LLM apps
  <sub>website</sub>
  <sub>`https://www.vellum.ai/`</sub>
- **[Weights &amp; Biases (Prompts)](https://docs.wandb.ai/guides/prompts)** — A suite of LLMOps tools within the developer-first W&amp;B MLOps platform. Utilize W&amp;B Prompts for visualizing and inspecting LLM execution flow, tracking inputs and outputs, viewing intermediate results, securely managing prompts and LLM chain configurations
  <sub>website</sub>
  <sub>`https://docs.wandb.ai/guides/prompts`</sub>
- **[Wordware](https://www.wordware.ai)** — A web-hosted IDE where non-technical domain experts work with AI Engineers to build task-specific AI agents. It approaches prompting as a new programming language rather than low/no-code blocks
  <sub>website</sub>
  <sub>`https://www.wordware.ai`</sub>

## ML Platforms

- **[MLflow](https://github.com/mlflow/mlflow)** — Open source platform for the machine learning lifecycle
  <sub>★ 28.1k · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`uvx mlflow server`</sub>
- **[Kubeflow](https://github.com/kubeflow/kubeflow)** — Machine Learning Toolkit for Kubernetes
  <sub>★ 15.9k · Apache-2.0 · source · pushed 2026-08-21</sub>
  <sub>`git clone https://github.com/kubeflow/kubeflow.git`</sub>
- **[OpenLLM](https://github.com/bentoml/OpenLLM)** — An open platform for operating large language models (LLMs) in production. Fine-tune, serve, deploy, and monitor any LLMs with ease
  <sub>★ 12.5k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install openllm # or pip3 install openllm`</sub>
- **[Kserve](https://github.com/kserve/kserve)** — Standardized Serverless ML Inference Platform on Kubernetes
  <sub>★ 6k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kserve/kserve.git`</sub>
- **[Seldon-core](https://github.com/SeldonIO/seldon-core)** — An MLOps framework to package, deploy, monitor and manage thousands of production machine learning models
  <sub>★ 4.8k · Go · source · pushed 2026-03-23 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/SeldonIO/seldon-core.git`</sub>
- **[Polyaxon](https://github.com/polyaxon/polyaxon)** — Machine Learning Management &amp; Orchestration Platform
  <sub>★ 3.7k · MDX · Apache-2.0 · source · pushed 2026-09-19</sub>
  <sub>`git clone https://github.com/polyaxon/polyaxon.git`</sub>
- **[PAI](https://github.com/microsoft/pai)** — Resource scheduling and cluster management for AI
  <sub>★ 2.7k · JavaScript · MIT · source · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/microsoft/pai.git`</sub>
- **[ModelFox](https://github.com/modelfoxdotdev/modelfox)** — ModelFox is a platform for managing and deploying machine learning models
  <sub>★ 1.5k · Rust · source · pushed 2024-08-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/modelfoxdotdev/modelfox.git`</sub>
- **[Hopsworks](https://github.com/logicalclocks/hopsworks)** — Hopsworks is a MLOps platform for training and operating large and small ML systems, including fine-tuning and serving LLMs. Hopsworks includes both a feature store and vector database for RAG
  <sub>★ 1.3k · Java · AGPL-3.0 · source · pushed 2025-02-10 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/logicalclocks/hopsworks.git`</sub>
- **[Primehub](https://github.com/myelintek/primehub)** — An effortless infrastructure for machine learning built on the top of Kubernetes
  <sub>★ 409 · Shell · Apache-2.0 · source · pushed 2026-01-13</sub>
  <sub>`git clone https://github.com/InfuseAI/primehub.git`</sub>
- **[OpenModelZ](https://github.com/tensorchord/openmodelz)** — One-click machine learning deployment (LLM, text-to-image and so on) at scale on any cluster (GCP, AWS, Lambda labs, your home lab, or even a single machine)
  <sub>★ 284 · Go · Apache-2.0 · pip · pushed 2023-11-03 · Win? · WSL2? · macOS? · Linux</sub>
  <sub>`pip install openmodelz`</sub>
- **[Starwhale](https://github.com/star-whale/starwhale)** — An MLOps/LLMOps platform for model building, evaluation, and fine-tuning
  <sub>★ 236 · Java · Apache-2.0 · source · pushed 2024-12-20 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/star-whale/starwhale.git`</sub>
- **[KubeStellar Console](https://console.kubestellar.io)** — Open source AI-powered multi-cluster Kubernetes dashboard for managing LLM workloads across hybrid edge and cloud environments. GPU monitoring, benchmark streaming, real-time observability with 20+ CNCF integrations, and AI-guided cluster operations. CNCF Sandbox project
  <sub>website</sub>
  <sub>`https://console.kubestellar.io`</sub>
- **[TrueFoundry](https://truefoundry.com/llmops)** — A PaaS to deploy, Fine-tune and serve LLM Models on a company’s own Infrastructure with Data Security and Optimal GPU and Cost Management. Launch your LLM Application at Production scale with best DevSecOps practices
  <sub>website</sub>
  <sub>`https://truefoundry.com/llmops`</sub>

## Vector search

- **[Milvus](https://github.com/milvus-io/milvus)** — Vector database for scalable similarity search and AI applications
  <sub>★ 46.2k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/milvus-io/milvus.git`</sub>
- **[Qdrant](https://github.com/qdrant/qdrant)** — Vector Search Engine and Database for the next generation of AI applications. Also available in the cloud
  <sub>★ 34.7k · Rust · Apache-2.0 · docker · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 6333:6333 qdrant/qdrant`</sub>
- **[Chroma](https://github.com/chroma-core/chroma)** — the open source embedding database
  <sub>★ 29.4k · Rust · Apache-2.0 · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install chromadb # python client`</sub>
- **[pgvector](https://github.com/pgvector/pgvector)** — Open-source vector similarity search for Postgres
  <sub>★ 23.1k · C · brew · pushed 2026-09-10 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install pgvector`</sub>
- **[Weaviate](https://github.com/weaviate/weaviate)** — Weaviate is an open source vector search engine that stores both objects and vectors, allowing for combining vector search with structured filtering with the fault-tolerance and scalability of a cloud-native database, all accessible through GraphQL, REST, and various language clients
  <sub>★ 16.8k · Go · npx · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npx skills add weaviate/agent-skills`</sub>
- **[txtai](https://github.com/neuml/txtai)** — Build AI-powered semantic search applications
  <sub>★ 13k · Python · Apache-2.0 · pip · pushed 2026-09-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install txtai`</sub>
- **[Lancedb](https://github.com/lancedb/lancedb)** — Developer-friendly, serverless vector database for AI applications. Easily add long-term memory to your LLM apps!
  <sub>★ 11.5k · Rust · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/lancedb/lancedb.git`</sub>
- **[ParadeDB](https://github.com/paradedb/paradedb)** — The transactional alternative to Elasticsearch, built on Postgres
  <sub>★ 9.3k · Rust · AGPL-3.0 · script · pushed 2026-09-21 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://paradedb.com/install.sh | sh`</sub>
- **[Marqo](https://github.com/marqo-ai/marqo)** — Tensor search for humans
  <sub>★ 5k · Python · Apache-2.0 · source · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/marqo-ai/marqo.git`</sub>
- **[Infinity](https://github.com/infiniflow/infinity)** — The AI-native database built for LLM applications, providing incredibly fast vector and full-text search
  <sub>★ 4.7k · C++ · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`pip install infinity-sdk==0.7.3`</sub>
- **[Vearch](https://github.com/vearch/vearch)** — A distributed system for embedding-based vector retrieval
  <sub>★ 2.3k · Python · Apache-2.0 · source · pushed 2026-07-27 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/vearch/vearch.git`</sub>
- **[pgvecto.rs](https://github.com/tensorchord/pgvecto.rs)** — Vector database plugin for Postgres, written in Rust, specifically designed for LLM
  <sub>★ 2.2k · Rust · Apache-2.0 · source · pushed 2025-02-26 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/tensorchord/pgvecto.rs.git`</sub>
- **[VectorChord](https://github.com/supervc-stack/VectorChord)** — Scalable, fast, and disk-friendly vector search in Postgres, the successor of pgvecto.rs
  <sub>★ 1.8k · Rust · source · pushed 2026-08-06 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/tensorchord/VectorChord.git`</sub>
- **[Vald](https://github.com/vdaas/vald)** — A Highly Scalable Distributed Vector Search Engine
  <sub>★ 1.7k · Go · Apache-2.0 · helm · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`helm install vald-cluster vald/vald`</sub>
- **[Omnigraph](https://github.com/ModernRelay/omnigraph)** — Typed graph database where agents branch and merge like Git. S3-native, Rust, traversal + vector + BM25 in one runtime
  <sub>★ 1.2k · Rust · MIT · npx · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add ModernRelay/omnigraph@omnigraph`</sub>
- **[Epsilla](https://github.com/epsilla-cloud/vectordb)** — A 10x faster, cheaper, and better vector database
  <sub>★ 875 · C++ · GPL-3.0 · pip · pushed 2025-11-29 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install pyepsilla`</sub>
- **[VectorDB](https://github.com/jina-ai/vectordb)** — A Python vector database you just need - no more, no less
  <sub>★ 653 · Python · Apache-2.0 · pip · pushed 2024-03-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install vectordb`</sub>
- **[AquilaDB](https://github.com/Aquila-Network/aquila)** — An easy to use Neural Search Engine. Index latent vectors along with JSON metadata and do efficient k-NN search
  <sub>★ 379 · HTML · docker · pushed 2024-05-06 · WSL2 · Linux · Docker</sub>
  <sub>`docker run -p 5001:5001 -d aquiladb:local`</sub>
- **[Awadb](https://github.com/awa-ai/awadb)** — AI Native database for embedding vectors
  <sub>★ 175 · C++ · Apache-2.0 · pip · pushed 2024-11-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip3 install awadb`</sub>
- **[Pinecone](https://www.pinecone.io/)** — The Pinecone vector database makes it easy to build high-performance vector search applications. Developer-friendly, fully managed, and easily scalable without infrastructure hassles
  <sub>website</sub>
  <sub>`https://www.pinecone.io/`</sub>
- **[Rivestack](https://rivestack.io)** — Managed PostgreSQL with pgvector for AI workloads. Built-in SQL editor lets you query your database with natural language (auto-converted to vector embeddings). Free tier includes 2GB storage
  <sub>website</sub>
  <sub>`https://rivestack.io`</sub>
- **[Vellum](https://www.vellum.ai/products/retrieval)** — A managed service for ingesting documents and performing hybrid semantic/keyword search across them. Comes with out-of-box support for OCR, text chunking, embedding model experimentation, metadata filtering, and production-grade APIs
  <sub>website</sub>
  <sub>`https://www.vellum.ai/products/retrieval`</sub>

## Hybrid search

- **[Airweave](https://github.com/airweave-ai/airweave)** — An easy way to turn any app into searchable data for LLMs
  <sub>★ 6.6k · Python · MIT · pip · pushed 2026-06-05 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install airweave-sdk # Python`</sub>

## Data Management

- **[Dolt](https://github.com/dolthub/dolt)** — Git for Data
  <sub>★ 24.5k · Go · Apache-2.0 · choco · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`choco install dolt`</sub>
- **[DVC](https://github.com/treeverse/dvc)** — Data Version Control - Git for Data &amp; Models - ML Experiments Management
  <sub>★ 15.9k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install 'dvc[s3]'`</sub>
- **[Delta-Lake](https://github.com/delta-io/delta)** — Storage layer that brings scalable, ACID transactions to Apache Spark and other engines
  <sub>★ 9k · Scala · Apache-2.0 · source · pushed 2026-09-21</sub>
  <sub>`git clone https://github.com/delta-io/delta.git`</sub>
- **[Pachyderm](https://github.com/pachyderm/pachyderm)** — Pachyderm is a version control system for data
  <sub>★ 6.3k · Go · Apache-2.0 · source · pushed 2025-02-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pachyderm/pachyderm.git`</sub>
- **[Quilt](https://github.com/quiltdata/quilt)** — A self-organizing data hub for S3
  <sub>★ 1.4k · TypeScript · Apache-2.0 · clone · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/quiltdata/quilt`</sub>
- **[ArtiVC](https://github.com/InfuseAI/ArtiVC)** — A version control system to manage large files. Lake is a dataset format with a simple API for creating, storing, and collaborating on AI datasets of any size
  <sub>★ 314 · Go · Apache-2.0 · source · pushed 2026-08-08 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/InfuseAI/ArtiVC.git`</sub>

## Data Storage

- **[JuiceFS](https://github.com/juicedata/juicefs)** — A distributed POSIX file system built on top of Redis and S3
  <sub>★ 14.4k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/juicedata/juicefs.git`</sub>
- **[Lance](https://github.com/lance-format/lance)** — Modern columnar data format for ML implemented in Rust
  <sub>★ 7.1k · Rust · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pylance`</sub>
- **[LakeFS](https://github.com/treeverse/lakeFS)** — Git-like capabilities for your object storage
  <sub>★ 5.5k · Go · Apache-2.0 · pip · pushed 2026-09-17 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`pip install lakefs`</sub>

## Feature Engineering

- **[FeatureTools](https://github.com/alteryx/featuretools)** — An open source python framework for automated feature engineering
  <sub>★ 7.7k · Python · BSD-3-Clause · source · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Featuretools/featuretools.git`</sub>
- **[Featureform](https://github.com/featureform/featureform)** — The Virtual Feature Store. Turn your existing data infrastructure into a feature store
  <sub>★ 2k · Go · MPL-2.0 · source · pushed 2025-07-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/featureform/featureform.git`</sub>

## Data/Feature enrichment

- **[Feast](https://github.com/feast-dev/feast)** — An open source feature store for machine learning
  <sub>★ 7.3k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`pip install feast`</sub>
- **[distilabel](https://github.com/argilla-io/distilabel)** — distilabel is a framework for synthetic data and AI feedback for AI engineers that require high-quality outputs, full data ownership, and overall efficiency
  <sub>★ 3.4k · Python · Apache-2.0 · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install distilabel --upgrade`</sub>
- **[Upgini](https://github.com/upgini/upgini)** — Free automated data &amp; feature enrichment library for machine learning: automatically searches through thousands of ready-to-use features from public and community shared data sources and enriches your training dataset with only the accuracy improving features
  <sub>★ 358 · Python · BSD-3-Clause · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/upgini/upgini.git`</sub>
- **[FastDatasets](https://github.com/ZhuLinsen/FastDatasets)** — A powerful tool for creating high-quality training datasets for Large Language Models
  <sub>★ 224 · Python · Apache-2.0 · pip · pushed 2025-08-31 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install fastdatasets-llm`</sub>

## Data Tracking

- **[LUX](https://github.com/lux-org/lux)** — A Python library that facilitates fast and easy data exploration by automating the visualization and data analysis process
  <sub>★ 5.4k · Python · Apache-2.0 · pip · pushed 2024-03-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install lux-api`</sub>
- **[Piperider](https://github.com/InfuseAI/piperider)** — A CLI tool that allows you to build data profiles and write assertion tests for easily evaluating and tracking your data's reliability over time
  <sub>★ 495 · Python · Apache-2.0 · pip · pushed 2025-01-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install piperider[<connector>]`</sub>

## Visualization

- **[netron](https://github.com/lutzroeder/netron)** — Visualizer for neural network, deep learning, and machine learning models
  <sub>★ 33.5k · JavaScript · MIT · winget · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`winget install -s winget netron`</sub>
- **[TensorBoard](https://github.com/tensorflow/tensorboard)** — TensorFlow's Visualization Toolkit
  <sub>★ 7.2k · TypeScript · Apache-2.0 · source · pushed 2026-08-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tensorflow/tensorboard.git`</sub>
- **[TensorSpace](https://github.com/tensorspace-team/tensorspace)** — Neural network 3D visualization framework, build interactive and intuitive model in browsers, support pre-trained deep learning models from TensorFlow, Keras, TensorFlow.js
  <sub>★ 5.2k · JavaScript · Apache-2.0 · clone · pushed 2022-12-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/tensorspace-team/tensorspace.git`</sub>
- **[dtreeviz](https://github.com/parrt/dtreeviz)** — A python library for decision tree visualization and model interpretation
  <sub>★ 3.2k · Jupyter Notebook · MIT · pip · pushed 2026-01-02 · Win · WSL2? · macOS · Linux</sub>
  <sub>`pip install dtreeviz # install dtreeviz for sklearn`</sub>
- **[Zetane Viewer](https://github.com/zetane/viewer)** — ML models and internal tensors 3D visualizer
  <sub>★ 1.8k · Python · source · pushed 2022-08-08 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/zetane/viewer.git`</sub>
- **[Maniford](https://github.com/uber/manifold)** — A model-agnostic visual debugging tool for machine learning
  <sub>★ 1.7k · JavaScript · Apache-2.0 · source · pushed 2025-02-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/uber/manifold.git`</sub>
- **[Zeno](https://github.com/zeno-ml/zeno)** — AI evaluation platform for interactively exploring data and model outputs
  <sub>★ 214 · Svelte · MIT · pip · pushed 2023-10-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install zenoml`</sub>
- **[Fiddler AI](https://github.com/fiddler-labs)** — Rich dashboards, reports, and UMAP to perform root cause analysis, pinpoint problem areas, like correctness, safety, and privacy issues, and improve LLM outcomes
  <sub>website</sub>
  <sub>`https://github.com/fiddler-labs`</sub>
- **[OpenOps](https://github.com/ThePlugJumbo/openops)** — Bring multiple data streams into one dashboard
  <sub>unavailable</sub>

## Profiling

- **[scalene](https://github.com/plasma-umass/scalene)** — a high-performance, high-precision CPU, GPU, and memory profiler for Python
  <sub>★ 13.5k · Python · Apache-2.0 · source · pushed 2026-08-27 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/plasma-umass/scalene.git`</sub>
- **[octoml-profile](https://github.com/octoml/octoml-profile)** — octoml-profile is a python library and cloud service designed to provide the simplest experience for assessing and optimizing the performance of PyTorch models on cloud hardware with state-of-the-art ML acceleration technology
  <sub>★ 113 · Apache-2.0 · pip · pushed 2023-04-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "octoml-profile>=0.2.0"`</sub>

## Observability

- **[Great Expectations](https://github.com/fivetran/great_expectations)** — Always know what to expect from your data
  <sub>★ 11.8k · Python · Apache-2.0 · pip · pushed 2026-09-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install great_expectations`</sub>
- **[Evidently](https://github.com/evidentlyai/evidently)** — An open-source framework to evaluate, test and monitor ML and LLM-powered systems
  <sub>★ 7.9k · Jupyter Notebook · Apache-2.0 · pip · pushed 2026-09-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evidently`</sub>
- **[Helicone](https://github.com/Helicone/helicone)** — Open source LLM observability platform. One line of code to monitor, evaluate, and experiment with features like prompt management, agent tracing, and evaluations
  <sub>★ 6.2k · TypeScript · Apache-2.0 · clone · pushed 2026-09-16 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Helicone/helicone.git`</sub>
- **[Deepchecks](https://github.com/deepchecks/deepchecks)** — Tests for Continuous Validation of ML Models &amp; Data. Deepchecks is a Python package for comprehensively validating your machine learning models and data with minimal effort
  <sub>★ 4.1k · Python · pip · pushed 2025-12-28 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install deepchecks -U --user`</sub>
- **[whylogs](https://github.com/whylabs/whylogs)** — The open standard for data logging
  <sub>★ 2.8k · Jupyter Notebook · Apache-2.0 · source · pushed 2025-01-10</sub>
  <sub>`git clone https://github.com/whylabs/whylogs.git`</sub>
- **[onWatch](https://github.com/onllm-dev/onWatch)** — Lightweight Go CLI that tracks AI API quota usage across 7 providers (Anthropic, OpenAI, GitHub Copilot, MiniMax, and more). Background daemon, &lt;50MB RAM, zero telemetry, SQLite storage
  <sub>★ 743 · Go · GPL-3.0 · psh · pushed 2026-09-20 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`irm https://raw.githubusercontent.com/onllm-dev/onwatch/main/install.ps1 | iex`</sub>
- **[traceAI](https://github.com/future-agi/traceAI)** — Open-source AI tracing framework built on OpenTelemetry for deep observability across agentic and LLM workflows
  <sub>★ 221 · Python · Apache-2.0 · pip · pushed 2026-08-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install traceai-openai`</sub>
- **[EvalView](https://github.com/hidai25/eval-view)** — Regression testing for AI agents. Snapshot behavior, detect tool-call and output regressions, with golden-baseline diffing and LLM-as-judge scoring. Supports LangGraph, CrewAI, OpenAI, Claude, and any HTTP API
  <sub>★ 135 · Python · Apache-2.0 · pip · pushed 2026-09-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install evalview`</sub>
- **[Azure OpenAI Logger](https://github.com/aavetis/azure-openai-logger)** — "Batteries included" logging solution for your Azure OpenAI instance
  <sub>★ 73 · Bicep · source · pushed 2025-07-06</sub>
  <sub>`git clone https://github.com/aavetis/azure-openai-logger.git`</sub>
- **[QWED](https://github.com/QWED-AI/qwed-verification)** — Deterministic verification protocol for LLM outputs using 8 formal verification engines (SymPy, Z3, AST, SQLGlot). Prevents hallucinations through mathematical proofs rather than statistical methods
  <sub>★ 59 · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install qwed`</sub>
- **[Future AGI](https://github.com/future-agi/futureagi-sdk)** — Production-grade SDK for observability, automated evaluations and prompt management with sub-100ms guardrails for LLM/agent workflows
  <sub>★ 51 · Python · Apache-2.0 · pip · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install futureagi`</sub>
- **[RagTune](https://github.com/metawake/ragtune)** — CLI tool for debugging and benchmarking RAG retrieval. EXPLAIN ANALYZE for your retrieval layer
  <sub>★ 13 · Go · MIT · go · pushed 2026-03-25 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/metawake/ragtune/cmd/ragtune@latest`</sub>
- **[semantic-coverage](https://github.com/aashirpersonal/semantic-coverage)** — Visualizes RAG knowledge gaps and "blind spots" using 2D UMAP clustering and density detection
  <sub>★ 13 · Python · clone · pushed 2025-12-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aashirpersonal/semantic-coverage.git`</sub>
- **[ClevAgent](https://clevagent.io)** — Runtime monitoring for AI agents — heartbeat watchdog, loop detection, cost tracking, auto-restart. Python SDK or HTTP API
  <sub>website</sub>
  <sub>`https://clevagent.io`</sub>
- **[Fiddler AI](https://github.com/fiddler-labs/fiddler-auditor)** — Evaluate, monitor, analyze, and improve machine learning and generative models from pre-production to production. Ship more ML and LLMs into production, and monitor ML and LLM metrics like hallucination, PII, and toxicity
  <sub>unavailable</sub>
- **[Langfuse 🪢](https://langfuse.com)** — Open-source LLM observability platform that helps teams collaboratively debug, analyze, and iterate on their LLM applications
  <sub>website</sub>
  <sub>`https://langfuse.com`</sub>
- **[Maxim AI](https://getmaxim.ai)** — Platform for AI Agent Simulation, Evaluation &amp; Observability
  <sub>website</sub>
  <sub>`https://getmaxim.ai`</sub>
- **[Weco Observe](https://weco.ai)** — Observability and debugging tool for AI research agents. Trace multi-step LLM agent runs, visualize decision trees, and identify failure modes in autonomous research workflows. Cloud hosted with open-source agent integration
  <sub>website</sub>
  <sub>`https://weco.ai`</sub>

## Frameworks for LLM security

- **[dstack](https://github.com/Dstack-TEE/dstack)** — Open-source confidential AI framework for secure LLM deployment with data privacy, providing hardware-enforced isolation using Intel TDX and NVIDIA Confidential Computing
  <sub>★ 549 · Rust · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install dstack-sdk`</sub>
- **[Cordum](https://github.com/cordum-io/cordum)** — Safety-first agent orchestration platform with pre-dispatch policy evaluation, output scanning (PII, secrets, injection), job scheduling, workflow engine, and full audit trail
  <sub>★ 508 · Go · helm · pushed 2026-09-17 · Win? · WSL2 · Linux · Docker</sub>
  <sub>`helm install cordum oci://ghcr.io/cordum-io/cordum/charts/cordum \`</sub>
- **[Plexiglass](https://github.com/w4-advisory/plexiglass)** — A Python Machine Learning Pentesting Toolbox for Adversarial Attacks. Works with LLMs, DNNs, and other machine learning algorithms
  <sub>★ 156 · Python · Apache-2.0 · pip · pushed 2026-02-04 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install --upgrade plexiglass`</sub>
- **[brood-box](https://github.com/stacklok/brood-box)** — CLI tool for running coding agents inside hardware-isolated microVMs with snapshot isolation, egress control, and MCP authorization
  <sub>★ 72 · Go · Apache-2.0 · source · pushed 2026-09-18 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/stacklok/brood-box.git`</sub>

## IDEs and Workspaces

- **[code server](https://github.com/coder/code-server)** — Run VS Code on any machine anywhere and access it in the browser
  <sub>★ 79.4k · TypeScript · MIT · script · pushed 2026-09-20 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://code-server.dev/install.sh | sh -s -- --dry-run`</sub>
- **[Docker](https://github.com/moby/moby)** — Moby is an open-source project created by Docker to enable and accelerate software containerization
  <sub>★ 72.1k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/moby/moby.git`</sub>
- **[Jupyter Notebooks](https://github.com/jupyter/notebook)** — The Jupyter notebook is a web-based notebook environment for interactive computing
  <sub>★ 13.4k · Jupyter Notebook · BSD-3-Clause · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install notebook`</sub>
- **[conda](https://github.com/conda/conda)** — OS-agnostic, system-level binary package manager and ecosystem
  <sub>★ 7.5k · Python · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/conda/conda.git`</sub>
- **[envd](https://github.com/tensorchord/envd)** — Reproducible development environment for AI/ML
  <sub>★ 2.2k · Go · Apache-2.0 · pip · pushed 2026-07-25 · Win? · WSL2? · macOS? · Linux · Docker</sub>
  <sub>`pip install --upgrade envd`</sub>
- **[Kurtosis](https://github.com/kurtosis-tech/kurtosis)** — A build, packaging, and run system for ephemeral multi-container environments
  <sub>★ 553 · Go · Apache-2.0 · clone · pushed 2026-09-09 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/kurtosis-tech/kurtosis.git`</sub>

## Code AI

- **[Continue](https://github.com/continuedev/continue)** — the open-source autopilot for software development—bring the power of ChatGPT to VS Code
  <sub>★ 36k · TypeScript · Apache-2.0 · source · pushed 2026-09-21 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/continuedev/continue.git`</sub>
- **[tabby](https://github.com/TabbyML/tabby)** — Self-hosted AI coding assistant. An opensource / on-prem alternative to GitHub Copilot
  <sub>★ 33.9k · Rust · source · pushed 2026-06-30 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`git clone https://github.com/TabbyML/tabby.git`</sub>
- **[fauxpilot](https://github.com/fauxpilot/fauxpilot)** — An open-source alternative to GitHub Copilot server
  <sub>★ 14.7k · Python · MIT · source · pushed 2024-04-09 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/fauxpilot/fauxpilot.git`</sub>
- **[CodeGeeX](https://github.com/zai-org/CodeGeeX)** — CodeGeeX: An Open Multilingual Code Generation Model (KDD 2023)
  <sub>★ 8.8k · Python · Apache-2.0 · docker · pushed 2024-08-13 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`docker run --gpus '"device=0,1"' -it --ipc=host --name=codegeex codegeex/codegeex`</sub>
- **[CodeGen](https://github.com/salesforce/CodeGen)** — CodeGen is an open-source model for program synthesis. Trained on TPU-v4. Competitive with OpenAI Codex
  <sub>★ 5.2k · Python · Apache-2.0 · source · pushed 2026-06-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/salesforce/CodeGen.git`</sub>
- **[CodeT5](https://github.com/salesforce/CodeT5)** — Open Code LLMs for Code Understanding and Generation
  <sub>★ 3.1k · Python · BSD-3-Clause · source · pushed 2026-06-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/salesforce/CodeT5.git`</sub>
- **[AgentsMesh](https://github.com/AgentsMesh/AgentsMesh)** — Self-hostable AI Agent Workforce Platform. Multi-agent orchestration with remote AI workstations (AgentPods), PTY sandbox + git worktree isolation, built-in Kanban, and per-pod MCP server. Supports Claude Code, Codex CLI, Gemini CLI, Aider, OpenCode
  <sub>★ 2.4k · Go · script · pushed 2026-08-03 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://agentsmesh.ai/install.sh | sh`</sub>
- **[AIDE](https://github.com/WecoAI/aideml)** — Open-source ML engineering agent that uses tree search to explore solution spaces. Automates machine learning experimentation from data analysis to model training. Paper
  <sub>★ 1.5k · Python · MIT · pip · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install -U aideml`</sub>
- **[Bernstein](https://github.com/sipyourdrink-ltd/bernstein)** — Deterministic Python orchestrator for 37 CLI coding agents (Claude Code, Codex CLI, Gemini CLI, GitHub Copilot CLI, Cursor, Aider, OpenHands, OpenCode, Goose, Qwen, Ollama, ...) running in parallel git worktrees. First-class MCP server, quality gates, cost tracking with budgets
  <sub>★ 1.2k · Python · Apache-2.0 · uv · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install bernstein # or: pipx install bernstein`</sub>
- **[promptext](https://github.com/1broseidon/promptext)** — Smart code context extractor for AI assistants with accurate token counting and budget management
  <sub>★ 22 · Go · MIT · psh · pushed 2026-04-12 · Win · WSL2? · macOS · Linux</sub>
  <sub>`irm chain.sh/promptext/scripts/install.ps1 | iex`</sub>

## Workflow

- **[Prefect](https://github.com/PrefectHQ/prefect)** — The easiest way to automate your data
  <sub>★ 23.9k · Python · Apache-2.0 · pip · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install -U prefect`</sub>
- **[Argo Workflows](https://github.com/argoproj/argo-workflows)** — Workflow engine for Kubernetes
  <sub>★ 17k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/argoproj/argo-workflows.git`</sub>
- **[Metaflow](https://github.com/Netflix/metaflow)** — Build and manage real-life data science projects with ease!
  <sub>★ 10.3k · Python · Apache-2.0 · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install metaflow`</sub>
- **[Flyte](https://github.com/flyteorg/flyte)** — Kubernetes-native workflow automation platform for complex, mission-critical data and ML processes at scale
  <sub>★ 7.5k · Go · Apache-2.0 · source · pushed 2026-09-21 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/flyteorg/flyte.git`</sub>
- **[Kubeflow Pipelines](https://github.com/kubeflow/pipelines)** — Machine Learning Pipelines for Kubeflow
  <sub>★ 4.2k · Go · Apache-2.0 · source · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kubeflow/pipelines.git`</sub>
- **[Ploomber](https://github.com/ploomber/ploomber)** — The fastest way to build data pipelines. Develop iteratively, deploy anywhere
  <sub>★ 3.6k · Python · Apache-2.0 · pip · pushed 2025-05-29 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install ploomber`</sub>
- **[Hamilton](https://github.com/apache/hamilton)** — A lightweight framework to represent ML/language model pipelines as a series of python functions
  <sub>★ 2.6k · Jupyter Notebook · Apache-2.0 · pip · pushed 2026-09-20 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install "apache-hamilton[visualization]"`</sub>
- **[VDP](https://github.com/instill-ai/instill-core)** — An open-source unstructured data ETL tool to streamline the end-to-end unstructured data processing pipeline
  <sub>★ 2.3k · Python · source · pushed 2026-06-01 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/instill-ai/vdp.git`</sub>
- **[aqueduct](https://github.com/RunLLM/aqueduct)** — An Open-Source Platform for Production Data Science
  <sub>★ 518 · Go · Apache-2.0 · pip · pushed 2023-06-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip3 install aqueduct-ml`</sub>
- **[Kitaru](https://github.com/zenml-io/kitaru)** — Durable execution layer for AI agents. Checkpoints, replay, resume, and observability primitives that make agent workflows persistent and replayable — no graph DSL required
  <sub>★ 292 · Python · Apache-2.0 · script · pushed 2026-09-21 · WSL2 · macOS · Linux</sub>
  <sub>`curl -fsSL https://kitaru.ai/install | bash`</sub>
- **[simulate-sdk](https://github.com/future-agi/simulate-sdk)** — Enterprise-grade Voice AI simulation SDK for scenario-driven stress testing of multimodal and agentic systems
  <sub>★ 59 · Python · Apache-2.0 · pip · pushed 2026-06-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-simulate`</sub>
- **[Airflow](https://airflow.apache.org/)** — A platform to programmatically author, schedule and monitor workflows
  <sub>website</sub>
  <sub>`https://airflow.apache.org/`</sub>

## Awesome Lists

- **[Awesome Production Machine Learning](https://github.com/EthicalML/awesome-production-machine-learning)** — A curated list of awesome open source libraries to deploy, monitor, version and scale your machine learning
  <sub>★ 20.9k · MIT · source · pushed 2026-09-06 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/EthicalML/awesome-production-machine-learning.git`</sub>
- **[visenger/awesome-mlops](https://github.com/visenger/awesome-mlops)** — Machine Learning Operations - An awesome list of references for MLOps
  <sub>★ 14.2k · source · pushed 2024-11-21 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/visenger/awesome-mlops.git`</sub>
- **[kelvins/awesome-mlops](https://github.com/kelvins/awesome-mlops)** — A curated list of awesome MLOps tools
  <sub>★ 5.3k · Python · source · pushed 2026-08-17 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kelvins/awesome-mlops.git`</sub>
- **[Awesome AutoML Papers](https://github.com/hibayesian/awesome-automl-papers)** — A curated list of automated machine learning papers, articles, tutorials, slides and projects
  <sub>★ 4.2k · Apache-2.0 · source · pushed 2024-06-11</sub>
  <sub>`git clone https://github.com/hibayesian/awesome-automl-papers.git`</sub>
- **[Awesome Tensor Compilers](https://github.com/merrymercy/awesome-tensor-compilers)** — A list of awesome compiler projects and papers for tensor computation and deep learning
  <sub>★ 2.8k · source · pushed 2024-10-19</sub>
  <sub>`git clone https://github.com/merrymercy/awesome-tensor-compilers.git`</sub>
- **[Awesome Argo](https://github.com/akuity/awesome-argo)** — A curated list of awesome projects and resources related to Argo
  <sub>★ 2.5k · Apache-2.0 · source · pushed 2026-09-18</sub>
  <sub>`git clone https://github.com/terrytangyuan/awesome-argo.git`</sub>
- **[Awesome AutoDL](https://github.com/D-X-Y/Awesome-AutoDL)** — Automated Deep Learning: Neural Architecture Search Is Not the End (a curated list of AutoDL resources and an in-depth analysis)
  <sub>★ 2.3k · Python · MIT · source · pushed 2022-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/D-X-Y/Awesome-AutoDL.git`</sub>
- **[Awesome Federated Learning](https://github.com/chaoyanghe/Awesome-Federated-Learning)** — A curated list of federated learning publications, re-organized from Arxiv (mostly)
  <sub>★ 2k · source · pushed 2022-09-03</sub>
  <sub>`git clone https://github.com/chaoyanghe/Awesome-Federated-Learning.git`</sub>
- **[currentslab/awesome-vector-search](https://github.com/currentslab/awesome-vector-search)** — A curated list of awesome vector search framework/engine, library, cloud service and research papers to vector similarity search
  <sub>★ 1.6k · MIT · source · pushed 2026-07-06</sub>
  <sub>`git clone https://github.com/currentslab/awesome-vector-search.git`</sub>
- **[Awesome-Code-LLM](https://github.com/huybery/Awesome-Code-LLM)** — An awesome and curated list of best code-LLM for research
  <sub>★ 1.3k · MIT · source · pushed 2024-12-10</sub>
  <sub>`git clone https://github.com/huybery/Awesome-Code-LLM.git`</sub>
- **[Awesome AutoML](https://github.com/windmaple/awesome-AutoML)** — Curating a list of AutoML-related research, tools, projects and other resources
  <sub>★ 944 · GPL-3.0 · source · pushed 2026-03-24</sub>
  <sub>`git clone https://github.com/windmaple/awesome-AutoML.git`</sub>
- **[awesome-federated-learning](https://github.com/weimingwill/awesome-federated-learning)** — All materials you need for Federated Learning: blogs, videos, papers, and softwares, etc
  <sub>★ 737 · Shell · MIT · source · pushed 2025-11-16</sub>
  <sub>`git clone https://github.com/weimingwill/awesome-federated-learning.git`</sub>
- **[Awesome Open MLOps](https://github.com/fuzzylabs/awesome-open-mlops)** — This is the Fuzzy Labs guide to the universe of free and open source MLOps tools
  <sub>★ 482 · Apache-2.0 · source · pushed 2025-05-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/fuzzylabs/awesome-open-mlops.git`</sub>
- **[pleisto/flappy](https://github.com/pleisto/flappy)** — Production-Ready LLM Agent SDK for Every Developer
  <sub>★ 304 · Rust · Apache-2.0 · source · pushed 2024-04-19 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/pleisto/flappy.git`</sub>
- **[Awesome Federated Learning Systems](https://github.com/AmberLJC/FLsystem-paper/blob/main/README.md)** — A curated list of Federated Learning Systems related academic papers, articles, tutorials, slides and projects
  <sub>in-repo · pushed 2024-02-07</sub>
  <sub>`git clone https://github.com/AmberLJC/FLsystem-paper.git && cd FLsystem-paper/README.md`</sub>

## Scheduling

- **[Volcano](https://github.com/volcano-sh/volcano)** — A Cloud Native Batch System (Project under CNCF)
  <sub>★ 6k · Go · Apache-2.0 · helm · pushed 2026-09-18 · WSL2? · Linux</sub>
  <sub>`helm install volcano volcano-sh/volcano -n volcano-system --create-namespace`</sub>
- **[Slurm](https://github.com/SchedMD/slurm)** — A Highly Scalable Workload Manager
  <sub>★ 4.4k · C · source · pushed 2026-09-21 · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/SchedMD/slurm.git`</sub>
- **[Kueue](https://github.com/kubernetes-sigs/kueue)** — Kubernetes-native Job Queueing
  <sub>★ 3k · Go · Apache-2.0 · source · pushed 2026-09-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/kubernetes-sigs/kueue.git`</sub>
- **[Yunikorn](https://github.com/apache/yunikorn-core)** — Light-weight, universal resource scheduler for container orchestrator systems
  <sub>★ 1k · Go · Apache-2.0 · source · pushed 2026-09-18 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/apache/yunikorn-core.git`</sub>

## Model Management

- **[ModelDB](https://github.com/VertaAI/modeldb)** — Open Source ML Model Versioning, Metadata, and Experiment Management
  <sub>★ 1.8k · Java · Apache-2.0 · source · pushed 2024-07-23 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/VertaAI/modeldb.git`</sub>
- **[MLEM](https://github.com/iterative/mlem)** — A tool to package, serve, and deploy any ML model on any platform
  <sub>★ 718 · Python · Apache-2.0 · source · pushed 2023-09-13 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/iterative/mlem.git`</sub>
- **[ormb](https://github.com/kleveross/ormb)** — Docker for Your ML/DL Models Based on OCI Artifacts
  <sub>★ 474 · Go · Apache-2.0 · source · pushed 2024-01-26 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/kleveross/ormb.git`</sub>


---

Snapshot 2026-09-21. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://crazy54.github.io/awesome-agentic-atlas/).
