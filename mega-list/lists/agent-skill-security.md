# Agent Skill Security

🛡️ A curated list of resources on agent skills security: attacks, defenses, frameworks, and benchmarks for securing AI agent tool use and skill ecosystems

Curated by **[LLMSecurity/awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security)** — all credit for the selection belongs there. This page adds stars, platform evidence, an install line and a screenshot to each entry.

98 entries · 57 distinct repos · 4 sections

[← back to the mega list](../README.md)

|   |   |   |
|---|---|---|
| <a href="https://github.com/Significant-Gravitas/AutoGPT"><img src="https://raw.githubusercontent.com/Significant-Gravitas/AutoGPT/master/docs/home/.gitbook/assets/Banner_image.png" width="260"></a> | <a href="https://github.com/f/prompts.chat"><img src="https://raw.githubusercontent.com/f/prompts.chat/main/public/sponsors/clemta.webp" width="260"></a> | <a href="https://github.com/punkpeye/awesome-mcp-servers"><img src="https://opengraph.githubassets.com/1/punkpeye/awesome-mcp-servers" width="260"></a> |
| **[AutoGPT Plugins](https://github.com/Significant-Gravitas/AutoGPT)**<br>★ 187.6k | **[awesome-chatgpt-prompts](https://github.com/f/prompts.chat)**<br>★ 171.3k | **[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)**<br>★ 95.5k |
| <a href="https://github.com/e2b-dev/awesome-ai-agents"><img src="https://opengraph.githubassets.com/1/e2b-dev/awesome-ai-agents" width="260"></a> | <a href="https://github.com/promptfoo/promptfoo"><img src="https://raw.githubusercontent.com/promptfoo/promptfoo/main/site/static/img/claude-vs-gpt-example%402x.png" width="260"></a> | <a href="https://github.com/NVIDIA/NemoClaw"><img src="https://opengraph.githubassets.com/1/NVIDIA/NemoClaw" width="260"></a> |
| **[awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)**<br>★ 30.2k | **[Promptfoo](https://github.com/promptfoo/promptfoo)**<br>★ 25.5k | **[NemoClaw](https://github.com/NVIDIA/NemoClaw)**<br>★ 22.5k |

## Contents

- [Agent Skill Specifications](#agent-skill-specifications) (7)
- [Related Awesome Lists](#related-awesome-lists) (6)
- [Tools &amp; Frameworks](#tools--frameworks) (44)
- [Benchmarks &amp; Datasets](#benchmarks--datasets) (41)

## Agent Skill Specifications

- **[AutoGPT Plugins](https://github.com/Significant-Gravitas/AutoGPT)** — Plugin system for autonomous agents
  <sub>★ 187.6k · Python · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Significant-Gravitas/AutoGPT.git`</sub>
- **[AgentSkills.io](https://agentskills.io/specification)** — Agent skill definition and security requirements
  <sub>website</sub>
  <sub>`https://agentskills.io/specification`</sub>
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** — Tool/resource integration protocol for LLMs
  <sub>website</sub>
  <sub>`https://modelcontextprotocol.io/`</sub>
- **[OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)** — Tool use specification for GPT models
  <sub>website</sub>
  <sub>`https://platform.openai.com/docs/guides/function-calling`</sub>
- **[Tool Use (Claude)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)** — Claude's native tool use interface
  <sub>website</sub>
  <sub>`https://docs.anthropic.com/en/docs/build-with-claude/tool-use`</sub>
- **[LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)** — Tool abstraction for agent frameworks
  <sub>website</sub>
  <sub>`https://python.langchain.com/docs/modules/agents/tools/`</sub>
- **[OpenAPI/Swagger](https://swagger.io/specification/)** — API specification commonly used as tool definitions
  <sub>website</sub>
  <sub>`https://swagger.io/specification/`</sub>

## Related Awesome Lists

- **[awesome-chatgpt-prompts](https://github.com/f/prompts.chat)** — Prompt engineering (includes adversarial examples)
  <sub>★ 171.3k · HTML · npx · pushed 2026-09-09 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx prompts.chat new my-prompt-library`</sub>
- **[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** — MCP server ecosystem (attack surface reference)
  <sub>★ 95.5k · MIT · npx · pushed 2026-09-23 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`npx awesome-mcp search postgres`</sub>
- **[awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)** — AI agent frameworks and projects
  <sub>★ 30.2k · source · pushed 2026-08-21 · Win? · WSL2? · Linux?</sub>
  <sub>`git clone https://github.com/e2b-dev/awesome-ai-agents.git`</sub>
- **[awesome-ml-for-cybersecurity](https://github.com/jivoi/awesome-ml-for-cybersecurity)** — ML applied to cybersecurity
  <sub>★ 9.4k · source · pushed 2024-08-19 · Win · WSL2? · macOS · Linux</sub>
  <sub>`git clone https://github.com/jivoi/awesome-ml-for-cybersecurity.git`</sub>
- **[awesome-llm-security](https://github.com/corca-ai/awesome-llm-security)** — General LLM security resources
  <sub>★ 1.7k · source · pushed 2025-08-20</sub>
  <sub>`git clone https://github.com/corca-ai/awesome-llm-security.git`</sub>
- **[awesome-ai-safety](https://github.com/hari-sikchi/awesome-ai-safety)** — AI safety research and resources
  <sub>★ 71 · source · pushed 2020-02-09 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/hari-sikchi/awesome-ai-safety.git`</sub>

## Tools &amp; Frameworks

- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — LLM red teaming and evaluation framework
  <sub>★ 25.5k · TypeScript · MIT · npm · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g promptfoo`</sub>
- **[NemoClaw](https://github.com/NVIDIA/NemoClaw)** — NVIDIA reference stack for running always-on AI agents more safely in sandboxes, with network policy, hardening, routed inference, and lifecycle controls
  <sub>★ 22.5k · TypeScript · Apache-2.0 · source · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/NVIDIA/NemoClaw.git`</sub>
- **[CubeSandbox](https://github.com/TencentCloud/CubeSandbox)** — Hardware-isolated (per-kernel) sub-60ms sandbox for secure AI agent code execution, with an out-of-sandbox credential vault, eBPF network isolation, and domain-allowlisted egress controls with audit logging
  <sub>★ 12.7k · Go · source · pushed 2026-09-24 · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/TencentCloud/CubeSandbox.git`</sub>
- **[Garak](https://github.com/NVIDIA/garak)** — LLM vulnerability scanner
  <sub>★ 9.4k · Python · Apache-2.0 · source · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/leondz/garak.git`</sub>
- **[NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)** — NVIDIA's toolkit for adding guardrails to LLM-based applications
  <sub>★ 7.2k · Python · source · pushed 2026-09-26 · Win? · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/NVIDIA/NeMo-Guardrails.git`</sub>
- **[LLM Guard](https://github.com/protectai/llm-guard)** — Input/output scanning for LLM applications
  <sub>★ 3.2k · Python · MIT · pip · pushed 2026-07-08 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install llm-guard`</sub>
- **[Agent Scan](https://github.com/snyk/agent-scan)** — Snyk's scanner for local agent supply chains, covering MCP servers and skills with checks for prompt injection, tool poisoning, toxic flows, and malware-laced skill files
  <sub>★ 3.1k · Python · Apache-2.0 · uv · pushed 2026-09-26 · Win · WSL2 · macOS · Linux</sub>
  <sub>`uvx snyk-agent-scan@0.5.17`</sub>
- **[Rebuff](https://github.com/protectai/rebuff)** — Self-hardening prompt injection detector
  <sub>★ 1.5k · TypeScript · Apache-2.0 · pip · pushed 2024-08-07 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install rebuff`</sub>
- **[Pipelock](https://github.com/luckyPipewrench/pipelock)** — Open-source AI agent firewall and MCP-aware egress proxy with DLP, prompt injection scanning, process sandboxing, and mediator-signed action receipts
  <sub>★ 906 · Go · Apache-2.0 · brew · pushed 2026-09-26 · Win? · WSL2 · macOS · Linux · Docker</sub>
  <sub>`brew install luckyPipewrench/tap/pipelock`</sub>
- **[Invariant Guardrails](https://github.com/invariantlabs-ai/invariant)** — Policy-based agent security guardrails
  <sub>★ 463 · Python · Apache-2.0 · source · pushed 2026-01-12 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/invariantlabs-ai/invariant.git`</sub>
- **[Clawvisor](https://github.com/clawvisor/clawvisor)** — AI agent gateway for purpose-based authorization, credential vaulting, and audit logging — agents declare task scope, humans approve once, Clawvisor enforces on every request without the agent ever seeing credentials
  <sub>★ 279 · Go · script · pushed 2026-09-17 · WSL2 · macOS · Linux · Docker</sub>
  <sub>`curl -fsSL https://raw.githubusercontent.com/clawvisor/clawvisor/main/scripts/install.sh | sh`</sub>
- **[Agent Memory Guard](https://github.com/OWASP/www-project-agent-memory-guard)** — OWASP reference implementation for ASI06 (Memory Poisoning): runtime defense that screens every agent memory read/write through detectors + a declarative policy, with source-class provenance, forensic SecurityEvents, and snapshot rollback. LangChain/OpenAI-Agents/AutoGen/CrewAI/mem0 integrations
  <sub>★ 183 · Python · Apache-2.0 · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install agent-memory-guard`</sub>
- **[Humanbound](https://github.com/humanbound/humanbound)** — Open-source adversarial testing engine, SDK, and CLI for AI agents: runs live-endpoint, multi-turn, and tool-abuse tests against a deployed agent and converts findings into deployable guardrail rules
  <sub>★ 158 · Python · Apache-2.0 · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install humanbound # CLI + SDK, core deps`</sub>
- **[Armorer Guard](https://github.com/ArmorerLabs/Armorer-Guard)** — Local Rust scanner for AI-agent prompt injection, credential redaction, sensitive-data requests, exfiltration-style text, and dangerous tool-call context
  <sub>★ 43 · Python · MIT · clone · pushed 2026-09-03 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/ArmorerLabs/Armorer-Guard.git`</sub>
- **[Nobulex](https://github.com/arian-gogani/nobulex)** — Trust Capital scoring layer for AI agents: bilateral Ed25519 receipts (pre- and post-execution signatures), content-addressed via action_ref and hash-chained per RFC 8785, that accumulate into a published 300-850 reputation score gating agent autonomy. CTEF v0.3.2 14/14 conformance. Python + TypeScript SDKs. Receipt-signing approach merged into Microsoft AGT
  <sub>★ 40 · TypeScript · MIT · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install nobulex`</sub>
- **[PIC Standard](https://github.com/pic-standard/pic-standard)** — Local-first standard and reference verifier that checks agent intent, provenance, and evidence at the action boundary and fails closed before high-impact tool calls; Python CLI, MCP/LangGraph/OpenClaw integrations, HTTP bridge, and a language-agnostic conformance suite
  <sub>★ 32 · Python · Apache-2.0 · pip · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install pic-standard`</sub>
- **[trentclaw](https://github.com/trnt-ai/trent-openclaw-security-assessment)** — Security assessment skill for OpenClaw environments: scans gateway config, skill permissions, MCP trust boundaries, and plugins, and correlates them into chained attack paths with severity-ranked remediation steps
  <sub>★ 23 · Python · Apache-2.0 · source · pushed 2026-07-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/trnt-ai/trent-openclaw-security-assessment.git`</sub>
- **[AVE (Agentic Vulnerability Enumeration)](https://github.com/aveproject/ave)** — Open standard and behavioral vulnerability taxonomy for agentic AI components (MCP servers, agent skills, LLM plugins), stable IDs scored with OWASP's AIVSS framework
  <sub>★ 20 · Python · Apache-2.0 · source · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/aveproject/ave.git`</sub>
- **[TraceFold](https://github.com/TraceFold/tracefold)** — Rust engine that escrows a verified pre-commit inverse before an agent's tool effect (filesystem mutation or MCP call) lands, or refuses the effect if no inverse can be verified; issues signed, offline-verifiable DSSE receipts and Merkle tile logs. Apache-2.0, alpha (v0.1.1)
  <sub>★ 18 · Rust · Apache-2.0 · source · pushed 2026-09-04 · Win? · WSL2? · Linux</sub>
  <sub>`git clone https://github.com/TraceFold/tracefold.git`</sub>
- **[IPI-Proxy](https://github.com/VulcanLab/IPI-Proxy)** — Intercepting proxy for red-teaming web-browsing agents against indirect prompt injection on live whitelisted domains
  <sub>★ 15 · Python · pip · pushed 2026-05-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install mitmproxy fastapi uvicorn pyyaml requests pytest`</sub>
- **[SkillCI](https://github.com/kabirnarang39/skillci)** — Regression testing + OWASP Agentic Skills Top 10-mapped static security lint for Claude Skills. Adds a self-growing eval loop (an uncovered regression or successful redteam attack writes its own permanent test case) and git-native bisect to find the exact commit that broke a skill
  <sub>★ 8 · Go · Apache-2.0 · scoop · pushed 2026-08-13 · Win · WSL2? · macOS · Linux · Docker</sub>
  <sub>`scoop bucket add skillci https://github.com/kabirnarang39/skillci scoop install skillci/skillci`</sub>
- **[Sunglasses](https://github.com/sunglasses-dev/sunglasses)** — Runtime trust scanner for agent skills and tool use: 1,089 patterns across 65 attack categories (prompt injection, tool poisoning, MCP attacks, skill compromise) plus a mechanism layer, shipped as a pip package, GitHub Action, and free web scanner with a published precision/recall benchmark
  <sub>★ 8 · Python · MIT · pip · pushed 2026-09-26 · Win? · WSL2? · macOS? · Linux? · Docker</sub>
  <sub>`pip install sunglasses # text scanning — zero dependencies`</sub>
- **[SkilLock](https://github.com/skills-lock/skil-lock)** — Behavior-pinning lockfile + capability-delta PR review for Claude Code &amp; Codex skills; SARIF output for Code Scanning
  <sub>★ 7 · Go · Apache-2.0 · go · pushed 2026-09-23 · Win · WSL2? · macOS · Linux</sub>
  <sub>`go install github.com/skills-lock/skil-lock/cmd/skil-lock@v0.2.5`</sub>
- **[Clay Seal](https://github.com/clayseal/clayseal-identity)** — Attested runtime identity and Biscuit capability tokens for agents: real GCP/Kubernetes/AWS node attestation, SPIFFE JWT-SVID and X.509-SVID (mTLS), and per-tool MCP authorization that is sender-constrained, so a token lifted from a log without the workload key authorizes nothing (Python + JS verifier)
  <sub>★ 7 · Python · MIT · pip · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install clayseal-identity`</sub>
- **[Tuning Engines CLI](https://github.com/cerebrixos-org/tuning-engines-cli)** — MCP server and CLI for governed agent/skill/tool access with policy checks, approvals, traces, and role-scoped registries
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-08-18 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g tuningengines-cli`</sub>
- **[whatileaked](https://github.com/selan-ai/whatileaked)** — Local scanner for credentials a coding agent has already written to disk: Claude Code, Codex and Cursor transcripts plus instruction/memory files (CLAUDE.md, AGENTS.md), which are re-read at the start of every session so a credential there keeps leaking until the file is edited. Uses the gitleaks rule set unmodified, reports a rule name and one-way fingerprint rather than the secret, and wipe reda
  <sub>★ 6 · TypeScript · MIT · npm · pushed 2026-08-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g whatileaked # then just: whatileaked scan`</sub>
- **[SkillTotal](https://github.com/pezhik/skilltotal)** — Static, offline scanner for AI components (MCP servers, agent skills, npm/PyPI packages, repos): supply-chain risk, dangerous capabilities, prompt-injection, exfiltration; deterministic, evidence-anchored, SARIF + pre-commit/GitHub Action
  <sub>★ 4 · Python · Apache-2.0 · pipx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pipx install skilltotal`</sub>
- **[DScan](https://github.com/DeepScan-Security/dscan)** — Open-source agent security suite for runtime tool-call tracing, prompt-injection shielding, MCP audits, adversarial testing, and sequence-level attack detection
  <sub>★ 3 · Python · pip · pushed 2026-07-21 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install dscan-security`</sub>
- **[Skill-audit](https://github.com/AgentPostmortem/Skill-audit)** — Static scanner for Claude/agent skills: flags prompt injection, dangerous shell, secret access, and exfiltration before install; 31 rules with SARIF output
  <sub>★ 3 · JavaScript · MIT · npm · pushed 2026-09-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install -g @royalpinto007/skill-audit`</sub>
- **[AgentSkillsScanner](https://github.com/sumleo/AgentSkillsScanner)** — Static analysis scanner for agent skill definitions
  <sub>★ 2 · Python · MIT · source · pushed 2026-02-09 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/sumleo/AgentSkillsScanner.git`</sub>
- **[Assay Harness](https://github.com/Rul1an/Assay-Harness)** — CI gate that checks an agent's claimed tool side-effects (filesystem, network, process) against independently observed runtime evidence, classifying each claim as supported, degraded, blocked, or not-evaluable (observed support is the ceiling)
  <sub>★ 2 · JavaScript · MIT · npx · pushed 2026-09-24 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npx tsx harness/src/cli.ts carrier supply-chain \`</sub>
- **[Sayfos SDK](https://github.com/sayfos-labs/sayfos-sdk)** — Runtime guardrail SDK for AI agents with provenance checks, budget governance, plan preflight, and adjudication tokens before high-risk tool actions
  <sub>★ 1 · Python · Apache-2.0 · pip · pushed 2026-06-15 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install sayfos-sdk`</sub>
- **[agent-sentinel](https://github.com/junlinwk/agent-sentinel)** — eBPF/BPF-LSM prototype that monitors local agent behavior and atomically blocks prompt-injection-driven access to sensitive files at the kernel boundary
  <sub>★ 1 · Python · source · pushed 2026-06-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/junlinwk/agent-sentinel.git`</sub>
- **[mcp-sploit](https://github.com/Prasanna-27eng/mcp-sploit)** — Metasploit-style framework for authorized security testing of MCP servers and MCP security gateways, including enumeration and exploit modules for unsafe tool exposure
  <sub>★ 1 · Python · MIT · source · pushed 2026-06-11 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/Prasanna-27eng/mcp-sploit.git`</sub>
- **[Bounty Sieve](https://github.com/junbuilds96/bounty-sieve)** — Offline-by-default bounty intake guardrail for coding agents: read-only GitHub issue/URL-list import, deterministic triage, local decision briefs, and human approval gates
  <sub>Python · MIT · source · pushed 2026-05-27 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/junbuilds96/bounty-sieve.git`</sub>
- **[Lakera Guard](https://www.lakera.ai/)** — Enterprise prompt injection defense API
  <sub>website</sub>
  <sub>`https://www.lakera.ai/`</sub>
- **[repo-agent-scan](https://github.com/sunxiayi/repo-agent-instruction-security-scan)** — Local deterministic scanner for agent skills and repository instruction files (SKILL.md, AGENTS.md, CLAUDE.md, and IDE rules), with evidence-anchored findings, SARIF, pre-commit, and GitHub Action support
  <sub>JavaScript · MIT · scoop · pushed 2026-09-23 · Win · WSL2? · macOS? · Linux?</sub>
  <sub>`scoop bucket add repoagentkit https://github.com/sunxiayi/scoop-bucket scoop install repoagentkit/repo-agent-scan`</sub>
- **[agent-diff-guard](https://github.com/cubxxw/agent-diff-guard)** — Pre-push guardrail that flags high-risk coding-agent diffs such as CI/CD changes, dependency edits, test deletions, hardcoded secrets, and task-scope drift before merge
  <sub>TypeScript · MIT · clone · pushed 2026-07-25 · WSL2 · Linux · Docker</sub>
  <sub>`git clone https://github.com/cubxxw/agent-diff-guard`</sub>
- **[Skillid](https://github.com/dkoly/skillid)** — Policy-driven Claude Code plugin that combines skill guidance with per-tool hooks to enforce org guardrails, confirmation rules, redaction, and connector-specific access control
  <sub>Python · MIT · source · pushed 2026-06-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/dkoly/skillid.git`</sub>
- **[Agent Audit](https://arxiv.org/abs/2603.22853)** — Security analysis system for LLM agent apps: dataflow analysis, credential detection, MCP config parsing, privilege-risk checks
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.22853`</sub>
- **[mcp-sec-audit](https://arxiv.org/abs/2603.21641)** — MCP server security toolkit: static pattern matching + dynamic sandboxed fuzzing via Docker/eBPF for detecting over-privileged tool capabilities
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2603.21641`</sub>
- **[SkillGate](https://github.com/selfradiance/skillgate)** — Deterministic local CLI that statically inspects an agent Skill package before harness admission — reports instruction surface and execution surface without executing, installing, or trusting the Skill
  <sub>TypeScript · MIT · source · pushed 2026-05-26 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/selfradiance/skillgate.git`</sub>
- **[SkillWatch](https://github.com/kuzivaai/SkillWatch)** — Periodically re-checks the external URL content that AI skills and MCP tools reference and flags suspicious changes (the post-review bait-and-switch); keeps an append-only, hash-chained content ledger with optional external anchoring (RFC 3161 / git). Local CLI, SARIF output, regex-based best-effort triage
  <sub>Python · Apache-2.0 · pip · pushed 2026-08-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`pip install skillwatch`</sub>
- **[AgentWarden](https://github.com/juangh123/AgentWarden)** — Static security gate for MCP configurations and AI agent skills, with SHA-256 integrity locking, Ed25519 publisher verification, SARIF output, and CI exit codes
  <sub>TypeScript · MIT · npm · pushed 2026-09-25 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`npm install --global agentwarden-cli@0.3.3`</sub>

## Benchmarks &amp; Datasets

- **[ASB](https://github.com/agiresearch/ASB)** — Comprehensive agent security
  <sub>★ 305 · Python · MIT · clone · pushed 2026-04-16 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Zhang-Henry/ASB.git`</sub>
- **[InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent)** — Indirect prompt injection
  <sub>★ 171 · Python · MIT · clone · pushed 2024-07-02 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/uiuc-kang-lab/InjecAgent.git`</sub>
- **[R-Judge](https://github.com/Lordog/R-Judge)** — 162 records, 27 scenarios
  <sub>★ 114 · Python · source · pushed 2026-01-11 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Lordog/R-Judge.git`</sub>
- **[ToolSword](https://github.com/Junjie-Ye/ToolSword)** — 6 scenarios, 3 stages
  <sub>★ 15 · Apache-2.0 · source · pushed 2024-09-12</sub>
  <sub>`git clone https://github.com/Junjie-Ye/ToolSword.git`</sub>
- **[SkillGuard Dataset](https://github.com/LLMSecurity/skillguard)** — Malicious skill detection
  <sub>★ 10 · clone · pushed 2026-02-25</sub>
  <sub>`git clone https://github.com/LLMSecurity/skillguard.git`</sub>
- **[MemoryStackBench](https://github.com/aetna000/MemoryStackBench)** — Agent memory safety and auditability
  <sub>★ 6 · HTML · Apache-2.0 · source · pushed 2026-09-11 · WSL2 · macOS? · Linux · Docker</sub>
  <sub>`git clone https://github.com/aetna000/MemoryStackBench.git`</sub>
- **[AudioAgentSecurity](https://github.com/Limax666/AudioAgentSecurity)** — Audio prompt injection vs. multimodal agents
  <sub>★ 5 · Python · source · pushed 2026-07-30 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Limax666/AudioAgentSecurity.git`</sub>
- **[StepJack](https://github.com/BorealisAI/StepJack)** — Multi-step indirect prompt injection vs. computer-use agents
  <sub>★ 5 · Python · GPL-3.0 · source · pushed 2026-05-05 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/BorealisAI/StepJack.git`</sub>
- **[mcp-defense-bench](https://github.com/Gowthaman90/mcp-defense-bench)** — MCP defensive-proxy attack-surface coverage
  <sub>★ 1 · JavaScript · Apache-2.0 · source · pushed 2026-09-10 · Win? · WSL2? · macOS? · Linux?</sub>
  <sub>`git clone https://github.com/Gowthaman90/mcp-defense-bench.git`</sub>
- **[AgentDyn](https://arxiv.org/abs/2602.03117)** — Dynamic prompt injection
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.03117`</sub>
- **[SkillSafetyBench](https://arxiv.org/abs/2605.12015)** — Skill-mediated agent safety
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2605.12015`</sub>
- **[SkillVetBench](https://arxiv.org/abs/2606.15899)** — Security risk eval of open-source agent skills
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.15899`</sub>
- **[SCR-Bench](https://arxiv.org/abs/2606.15242)** — Skill composition risk
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.15242`</sub>
- **[SafeClawBench](https://arxiv.org/abs/2606.18356)** — Staged harm in tool-using agents
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.18356`</sub>
- **[ToolPrivacyBench](https://arxiv.org/abs/2606.28061)** — Purpose-bound privacy in tool-using agents
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2606.28061`</sub>
- **[TAB](https://arxiv.org/abs/2605.12233)** — Selective cue following in terminal agents
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2605.12233`</sub>
- **[Skill-Inject](https://www.skill-inject.com/)** — Skill file attacks
  <sub>website</sub>
  <sub>`https://www.skill-inject.com/`</sub>
- **[NAAMSE](https://arxiv.org/abs/2602.07391)** — Evolutionary agent security eval
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2602.07391`</sub>
- **[AgentHarm](https://arxiv.org/abs/2410.09024)** — 110 behaviors, 440 variants
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2410.09024`</sub>
- **[WIPI](https://arxiv.org/abs/2402.16965)** — Web-based indirect injection
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2402.16965`</sub>
- **[DUMA-Bench](https://arxiv.org/abs/2609.24662)** — Dual-control agent security (8 vuln classes)
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.24662`</sub>
- **[SkillAtlas](https://arxiv.org/abs/2609.13353)** — Attack trace library for agent skills
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.13353`</sub>
- **[IssueTrojanBench](https://arxiv.org/abs/2607.20759)** — Malicious issue requests vs. coding agents
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.20759`</sub>
- **[OpenSkillRisk](https://arxiv.org/abs/2607.20121)** — Agent safety with risky third-party skills
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.20121`</sub>
- **[AIP-Bench](https://arxiv.org/abs/2607.21824)** — Agentic commerce protocol-level security
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.21824`</sub>
- **[ContainmentBench](https://arxiv.org/abs/2607.23999)** — Post-injection containment in tool-using agents
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.23999`</sub>
- **[MemSecBench](https://arxiv.org/abs/2607.27080)** — Lifecycle security of agent memory poisoning
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.27080`</sub>
- **[IH-Benchmark](https://arxiv.org/abs/2607.25987)** — Instruction-hierarchy robustness incl. tool-mediated conflicts
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.25987`</sub>
- **[AgentS4D](https://arxiv.org/abs/2607.27294)** — Lifecycle runtime risks of workspace agents
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2607.27294`</sub>
- **[HarnessSafe](https://arxiv.org/abs/2608.06984)** — Safety across persistent carriers in agent harnesses
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2608.06984`</sub>
- **[ToolHazard](https://arxiv.org/abs/2608.11878)** — Scalable synthesis of adversarial tool environments for indirect prompt injection
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2608.11878`</sub>
- **[ATOBench](https://arxiv.org/abs/2608.12996)** — Pentest-agent vulnerability verification under deceptive target evidence
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2608.12996`</sub>
- **[HarnessRisk](https://arxiv.org/abs/2608.17597)** — Lifecycle safety of agent harnesses across operational phases
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2608.17597`</sub>
- **[ChemMat-AgentSafetyBench](https://arxiv.org/abs/2609.11952)** — Long-horizon attacks/defenses in chemistry &amp; materials agents (tool-mediated hazardous-protocol release)
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.11952`</sub>
- **[PIDS-Bench](https://arxiv.org/abs/2609.15017)** — Prompt-injection detectors under over-defense, obfuscation, and distribution shift
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.15017`</sub>
- **[HTB (Hallucinated-Tools Benchmark)](https://arxiv.org/abs/2609.19425)** — Tool hallucination (fabricated tools/args) incl. cross-server MCP namespace collisions
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.19425`</sub>
- **[ClashBench](https://arxiv.org/abs/2609.19892)** — Destructive resource preemption by privileged agents (terminating/overwriting incumbent tasks to resolve conflicts)
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.19892`</sub>
- **[VLoc Bench](https://arxiv.org/abs/2609.15939)** — Repository-scale vulnerability localization by security agents (incl. refrain-on-patched)
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.15939`</sub>
- **[APort Vault](https://huggingface.co/datasets/aporthq/vault-benchmark-v1)** — Payment authorization in tool-using agents (deterministic pre-action check vs. model-alone)
  <sub>website</sub>
  <sub>`https://huggingface.co/datasets/aporthq/vault-benchmark-v1`</sub>
- **[EvasionBench](https://arxiv.org/abs/2609.30217)** — Instrumental runtime-monitor evasion under ordinary task pressure
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.30217`</sub>
- **[ACE](https://arxiv.org/abs/2609.28915)** — Cross-layer (kernel syscall + application) evidence for agent security
  <sub>website</sub>
  <sub>`https://arxiv.org/abs/2609.28915`</sub>


---

Snapshot 2026-09-26. Stars, language, licence and last-push come from the GitHub API and drift daily.

The same data with screenshots embedded, filterable, is in the workbooks: [dark](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-DARK.xlsx) · [light](https://github.com/crazy54/awesome-agentic-atlas/releases/latest/download/Awesome-Agentic-Atlas-LIGHT.xlsx). Or filter it in the browser on the [Atlas site](https://aaa.jeremyfhall.com/catalog/).
