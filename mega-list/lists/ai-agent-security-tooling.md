# AI Agent Security Tooling

A living map of the AI agent security ecosystem.

Curated by **[ProjectRecon/awesome-ai-agents-security](https://github.com/ProjectRecon/awesome-ai-agents-security)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

25 entries · 23 distinct repos · 7 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/OpenHands/OpenHands"><img src="https://assets.openhands.dev/screenshot/automation-preview.png" width="260"></a> | <a href="https://github.com/usestrix/strix"><img src="https://raw.githubusercontent.com/usestrix/.github/main/imgs/cover.png" width="260"></a> | <a href="https://github.com/BerriAI/litellm"><img src="https://github.com/user-attachments/assets/c5ee0412-6fb5-4fb6-ab5b-bafae4209ca6" width="260"></a> |
| **[OpenHands](https://github.com/OpenHands/OpenHands)**<br>★ 89.2k | **[Strix](https://github.com/usestrix/strix)**<br>★ 64.9k | **[LiteLLM Guardrails](https://github.com/BerriAI/litellm)**<br>★ 59.7k |
| <a href="https://github.com/NVIDIA/garak"><img src="https://opengraph.githubassets.com/1/leondz/garak" width="260"></a> | <a href="https://github.com/bridgecrewio/checkov"><img src="https://raw.githubusercontent.com/bridgecrewio/checkov/main/docs/checkov-jenkins.png" width="260"></a> | <a href="https://github.com/guardrails-ai/guardrails"><img src="https://opengraph.githubassets.com/1/guardrails-ai/guardrails" width="260"></a> |
| **[Garak](https://github.com/NVIDIA/garak)**<br>★ 9.4k | **[Checkov](https://github.com/bridgecrewio/checkov)**<br>★ 9k | **[Guardrails](https://github.com/guardrails-ai/guardrails)**<br>★ 7.5k |

## Contents

- [Sandboxing &amp; Isolation Environments](#sandboxing--isolation-environments) (4)
- [Red Teaming &amp; Vulnerability Scanners](#red-teaming--vulnerability-scanners) (6)
- [Guardrails &amp; Compliance](#guardrails--compliance) (4)
- [Static Analysis &amp; Linters](#static-analysis--linters) (5)
- [Agent Firewalls &amp; Gateways (Runtime Protection)](#agent-firewalls--gateways-runtime-protection) (3)
- [Identity &amp; Authentication](#identity--authentication) (2)
- [Benchmarks &amp; Datasets](#benchmarks--datasets) (1)

## Sandboxing &amp; Isolation Environments

- **[OpenHands](https://github.com/OpenHands/OpenHands)** — Formerly OpenDevin, this platform includes a secure runtime environment for autonomous coding agents to operate without accessing the host machine's sensitive files
  <sub>★ 89.2k · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g @openhands/agent-canvas`</sub>
- **[Agent-Infra Sandbox](https://github.com/agent-infra/sandbox)** — An "All-In-One" sandbox combining Browser, Shell, VSCode, and File System access in a single Docker container, optimized for agentic tasks
  <sub>★ 6k · Python · Apache-2.0 · pip · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install agent-sandbox`</sub>
- **[Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox)** — A Kubernetes Native project providing a Sandbox Custom Resource Definition (CRD) to manage isolated, stateful workloads for AI agents
  <sub>★ 4k · Go · Apache-2.0 · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install k8s-agent-sandbox`</sub>
- **[SandboxAI](https://github.com/substratusai/sandboxai)** — An open-source runtime for executing AI-generated code (Python/Shell) in isolated containers with granular permission controls
  <sub>★ 143 · Go · pip · pushed 2025-02-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install sandboxai-client`</sub>

## Red Teaming &amp; Vulnerability Scanners

- **[Strix](https://github.com/usestrix/strix)** — An autonomous AI agent designed for penetration testing. It runs inside a docker sandbox to actively probe applications and generate verified exploit capabilities
  <sub>★ 64.9k · Python · Apache-2.0 · npx · pushed 2026-09-25 · Win · WSL2? · macOS · Linux</sub>
  <sub>`npx skills add usestrix/strix`</sub>
- **[Garak](https://github.com/NVIDIA/garak)** — The "Nmap for LLMs." A vulnerability scanner that probes models for hallucination, data leakage, and prompt injection susceptibilities
  <sub>★ 9.4k · Python · Apache-2.0 · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leondz/garak.git`</sub>
- **[Agentic Security](https://github.com/msoedov/agentic_security)** — A dedicated vulnerability scanner for agent workflows and LLMs capable of running multi-step jailbreaks and fuzzing attacks against agent logic
  <sub>★ 2k · Python · Apache-2.0 · pip · pushed 2026-09-22 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentic_security`</sub>
- **[A2A Scanner](https://github.com/cisco-ai-defense/a2a-scanner)** — A scanner by Cisco designed to inspect "Agent-to-Agent" communication protocols for threats, validating agent identities and ensuring compliance with communication specs
  <sub>★ 165 · Python · Apache-2.0 · uv · pushed 2026-04-16 · Win? · WSL2? · macOS · Linux?</sub>
  <sub>`uv tool install --python 3.13 cisco-ai-a2a-scanner`</sub>
- **[PyRIT](https://github.com/Azure/PyRIT)** — Microsoft's open-source red teaming framework for generative AI. It automates multi-turn adversarial attacks to test if an agent can be coerced into harmful behavior
  <sub>★ 115 · MIT · source · pushed 2026-03-25</sub>
  <sub>`git clone https://github.com/Azure/PyRIT.git`</sub>
- **[Cybersecurity AI (CAI)](https://github.com/aliasrobotics/cai)** — A framework for building specialized security agents for offensive and defensive operations, often used in CTF (Capture The Flag) scenarios
  <sub>source</sub>
  <sub>`git clone https://github.com/aliasrobotics/cai.git`</sub>

## Guardrails &amp; Compliance

- **[LiteLLM Guardrails](https://github.com/BerriAI/litellm)** — While known for model proxying, LiteLLM includes built-in guardrail features to filter requests and responses across multiple LLM providers
  <sub>★ 59.7k · Python · uv · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`uv tool install 'litellm[proxy]'`</sub>
- **[Guardrails](https://github.com/guardrails-ai/guardrails)** — A Python framework for validating LLM outputs against structural and semantic rules (e.g., "must return valid JSON," "must not contain PII")
  <sub>★ 7.5k · Python · Apache-2.0 · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install guardrails-ai`</sub>
- **[NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)** — NVIDIA's toolkit for adding programmable rails to LLM-based apps. It ensures agents stay on topic, avoid jailbreaks, and adhere to defined safety policies
  <sub>★ 7.2k · Python · source · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/NVIDIA/NeMo-Guardrails.git`</sub>
- **[OWASP Agent Memory Guard](https://github.com/OWASP/www-project-agent-memory-guard)** — An official OWASP project that detects and blocks AI agent memory poisoning attacks (OWASP ASI06). Provides a drop-in middleware for LangChain, AutoGen, and CrewAI pipelines with real-time threat detection, sanitization hooks, and audit logging. pip install agent-memory-guard
  <sub>★ 183 · Python · Apache-2.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-memory-guard`</sub>

## Static Analysis &amp; Linters

- **[Checkov](https://github.com/bridgecrewio/checkov)** — While primarily for IaC, Checkov includes policies for scanning AI infrastructure and configurations to prevent misconfigurations in deployment
  <sub>★ 9k · Python · Apache-2.0 · pip · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip3 install checkov`</sub>
- **[Agentic Radar](https://github.com/splx-ai/agentic-radar)** — A static analysis tool that visualizes agent workflows (LangGraph, CrewAI, AutoGen). It detects risky tool usage, permission loops, and maps them to known vulnerabilities
  <sub>★ 1.1k · Python · Apache-2.0 · pip · pushed 2025-11-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agentic-radar`</sub>
- **[ATR (Agent Threat Rules)](https://github.com/Agent-Threat-Rule/agent-threat-rules)** — 108 open-source regex detection rules for AI agent threats (prompt injection, tool poisoning, credential exfiltration, skill compromise). &lt;1ms per scan. Adopted by Cisco AI Defense
  <sub>★ 400 · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`npm install -g agent-threat-rules`</sub>
- **[Aguara](https://github.com/garagon/aguara)** — A static security scanner for AI agent skills and MCP server configurations. Detects prompt injection, credential leaks, data exfiltration, and supply-chain attacks with 173 built-in rules, 4 analysis layers, and remediation guidance
  <sub>★ 93 · Go · Apache-2.0 · go · pushed 2026-09-21 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`go install github.com/garagon/aguara/cmd/aguara@v0.28.0`</sub>
- **[Agent Bound](https://github.com/ElPaisano/agent-bound)** — A design-time analysis tool that calculates "Agentic Entropy"—a metric to quantify the unpredictability and risk of infinite loops or unconstrained actions in agent architectures
  <sub>unavailable</sub>

## Agent Firewalls &amp; Gateways (Runtime Protection)

- **[AgentGateway](https://github.com/agentgateway/agentgateway)** — A Linux Foundation project providing an AI-native proxy for secure connectivity (A2A &amp; MCP protocols). It adds RBAC, observability, and policy enforcement to agent-tool interactions
  <sub>★ 5k · Rust · Apache-2.0 · source · pushed 2026-09-26 · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/agentgateway/agentgateway.git`</sub>
- **[Immunity Agent](https://github.com/PrismorSec/prismor)** — Security-focused AI agent runtime for scanning prompt injection, MCP risks, unsafe package installs, and dangerous agent actions before execution
  <sub>★ 377 · Python · Apache-2.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install prismor`</sub>
- **[Envoy AI Gateway](https://gateway.envoyproxy.io/)** — An Envoy-based gateway that manages request traffic to GenAI services, providing a control point for rate limiting and policy enforcement
  <sub>website</sub>
  <sub>`https://gateway.envoyproxy.io/`</sub>

## Identity &amp; Authentication

- **[OneCLI](https://github.com/onecli/onecli)** — Open-source credential vault for AI agents. A Rust HTTP gateway intercepts agent requests and injects API credentials transparently, so agents never handle raw keys. Supports per-agent scoped tokens and AES-256-GCM encryption at rest
  <sub>★ 3.5k · TypeScript · Apache-2.0 · clone · pushed 2026-09-14 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/onecli/onecli.git`</sub>
- **[WSO2](https://github.com/wso2)** — An identity management solution that treats AI agents as first-class identities, enabling secure authentication and authorization for agent actions
  <sub>website</sub>
  <sub>`https://github.com/wso2`</sub>

## Benchmarks &amp; Datasets

- **[CVE Bench](https://github.com/uiuc-kang-lab/cve-bench)** — A benchmark for evaluating an AI agent's ability to exploit real-world web application vulnerabilities (useful for testing defensive agents)
  <sub>★ 291 · Python · Apache-2.0 · source · pushed 2026-09-24 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/uiuc-kang-lab/cve-bench.git`</sub>


---

Snapshot 2026-09-26. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
