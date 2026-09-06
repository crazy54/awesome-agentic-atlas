"""One shared vocabulary across eleven lists that share none.

The eleven curators wrote 140 distinct section names between them and agreed on almost nothing: 132
`(source, section)` pairs plus the orchestrator list's 8 categories, and 131 distinct section strings.
`Frameworks`, `Agent Frameworks` and `Build-your-own` are the same shelf under three names; `Coding`,
`Software Development`, `Coding Agents` and `Parallel Coding Agents -- Terminal (TUI/CLI)` are the same
shelf under four. Nothing can be ranked "best in category" until the categories are one set, so this
module is that set.

Two axes, because the section names conflate two questions:

  CATEGORY -- what a thing *is*. Exactly one per repo, so it can be a column, a filter and a page.
  TARGETS  -- what it *plugs into*. Zero or more, because a plugin can serve Claude Code and opencode
              both, and "best Claude Code thing" is a question about this axis, not the other one.

Every one of the 140 keys is spelled out below rather than matched by keyword. A regex over section
names would silently re-file a section the day a curator renames it, and re-filing is exactly the thing
this module exists to make deliberate. `check()` fails if a section appears in the data that is not
listed here, which is how a rename gets noticed.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CACHE = Path(__file__).resolve().parent.parent / "cache"

# Order is the display order everywhere -- workbook tab, topic hub, Pages site -- and it is also the
# tie-break when a repo's listings split evenly between two categories: the earlier one wins, so the
# specific shelves are listed before the broad ones.
CATEGORIES = [
    "Orchestrators & Multi-Agent",
    "Coding Agents",
    "Agent Skills",
    "MCP Servers",
    "Frameworks & SDKs",
    "Harnesses & Runtime Infra",
    "Context, Memory & RAG",
    "Sandbox, Security & Governance",
    "Observability & Evals",
    "Plugins, Themes & Clients",
    "Research & Data Agents",
    "Creative, Voice & Media",
    "Assistants & Domain Agents",
    "Docs, Learning & Lists",
]

# Two earlier drafts of this list had `Templates & Starters` and `Patterns & Practices`, and both were
# answers to "what shelf did the curator use", not "what is this thing". Nothing on either page could be
# ranked: the 48 template entries are folders in one monorepo and the 122 pattern entries are write-ups
# in another, so both boards were empty and both pages duplicated a topic page that already existed.
# Their sections are filed topically now -- `Chat with X` is retrieval, `Feedback Loops` is evaluation,
# `Foundations` is reading -- which puts the write-ups on the same page as the tools they describe.

# (source, section) -> category. `orchestrators` keys the original list, whose field is `category`.
SECTIONS: dict[tuple[str, str], str] = {
    # kyrolabs/awesome-agents
    ("agents", "Frameworks"): "Frameworks & SDKs",
    ("agents", "Software Development"): "Coding Agents",
    ("agents", "Conversational / General Agents"): "Assistants & Domain Agents",
    ("agents", "Automation"): "Assistants & Domain Agents",
    # Renamed upstream from "Knowledge Management"; the new name says Memory itself. Only the current
    # spelling is listed, because a map that answers to both names is a map that stops noticing.
    ("agents", "Memory - Knowledge Management"): "Context, Memory & RAG",
    ("agents", "Research"): "Research & Data Agents",
    ("agents", "Testing and Evaluation"): "Observability & Evals",
    ("agents", "Game / Simulation"): "Creative, Voice & Media",

    # awesome-ai-agents-2026
    ("agents2026", "Coding Agents"): "Coding Agents",
    ("agents2026", "Agent Frameworks"): "Frameworks & SDKs",
    ("agents2026", "Creative AI"): "Creative, Voice & Media",
    ("agents2026", "Data and Research Agents"): "Research & Data Agents",
    ("agents2026", "Customer Support and CRM Agents"): "Assistants & Domain Agents",
    ("agents2026", "Local and Self-Hosted AI"): "Harnesses & Runtime Infra",
    ("agents2026", "Browser and Desktop Agents"): "Assistants & Domain Agents",
    ("agents2026", "Voice Agents"): "Creative, Voice & Media",
    ("agents2026", "Task and Workflow Agents"): "Orchestrators & Multi-Agent",
    ("agents2026", "Observability and Evaluation"): "Observability & Evals",
    ("agents2026", "Healthcare and Therapy Agents"): "Assistants & Domain Agents",
    ("agents2026", "Open-Source Models for Agents"): "Harnesses & Runtime Infra",
    ("agents2026", "AI Governance and Compliance"): "Sandbox, Security & Governance",
    ("agents2026", "Protocols and Standards"): "Frameworks & SDKs",
    ("agents2026", "AI Safety and Guardrails"): "Sandbox, Security & Governance",
    ("agents2026", "Cybersecurity Agents"): "Sandbox, Security & Governance",
    ("agents2026", "Multi-Agent Platforms"): "Orchestrators & Multi-Agent",

    # awesome-claude-code
    ("claudecode", "Start Here"): "Docs, Learning & Lists",
    ("claudecode", "From Anthropic"): "Frameworks & SDKs",
    ("claudecode", "Agent Orchestration"): "Orchestrators & Multi-Agent",
    ("claudecode", "Skills"): "Agent Skills",
    ("claudecode", "Memory & Context Persistence"): "Context, Memory & RAG",
    ("claudecode", "Observability & Monitoring"): "Observability & Evals",
    # Hook-driven checks on what the agent just wrote, so they belong with the other verification
    # tooling rather than with the coding agents they wrap.
    ("claudecode", "Linting"): "Observability & Evals",
    ("claudecode", "Security"): "Sandbox, Security & Governance",
    ("claudecode", "Providers, Runtime & Integration Infrastructure"): "Harnesses & Runtime Infra",
    ("claudecode", "Infrastructure & DevOps"): "Harnesses & Runtime Infra",
    ("claudecode", "Alternative Clients"): "Plugins, Themes & Clients",
    ("claudecode", "Remote Control, Notifications & Voice I/O"): "Plugins, Themes & Clients",
    ("claudecode", "Design & UI/UX"): "Plugins, Themes & Clients",
    ("claudecode", "Status Lines"): "Plugins, Themes & Clients",
    ("claudecode", "Creative Media"): "Creative, Voice & Media",
    ("claudecode", "Writing & Prose Quality"): "Creative, Voice & Media",
    ("claudecode", "Research & Scientific Inquiry"): "Research & Data Agents",
    ("claudecode", "Documentation, Knowledge & Learning"): "Docs, Learning & Lists",

    # e2b-dev/awesome-ai-agents -- the long tail is one-entry industry shelves
    ("e2b", "Coding"): "Coding Agents",
    ("e2b", "Developer tools"): "Coding Agents",
    ("e2b", "Multi-agent"): "Orchestrators & Multi-Agent",
    ("e2b", "Build-your-own"): "Frameworks & SDKs",
    ("e2b", "Build your own"): "Frameworks & SDKs",
    ("e2b", "Tool for agents"): "Frameworks & SDKs",
    ("e2b", "Open Source"): "Frameworks & SDKs",
    ("e2b", "Memory management"): "Context, Memory & RAG",
    ("e2b", "Data analysis"): "Research & Data Agents",
    ("e2b", "Research"): "Research & Data Agents",
    ("e2b", "Science"): "Research & Data Agents",
    ("e2b", "Business intelligence"): "Research & Data Agents",
    ("e2b", "Content creation"): "Creative, Voice & Media",
    ("e2b", "Design"): "Creative, Voice & Media",
    ("e2b", "Web design"): "Creative, Voice & Media",
    ("e2b", "General purpose"): "Assistants & Domain Agents",
    ("e2b", "Productivity"): "Assistants & Domain Agents",
    ("e2b", "Personal assistant"): "Assistants & Domain Agents",
    ("e2b", "Sales"): "Assistants & Domain Agents",
    ("e2b", "HR"): "Assistants & Domain Agents",
    ("e2b", "Finance"): "Assistants & Domain Agents",
    ("e2b", "Blockchain"): "Assistants & Domain Agents",
    ("e2b", "Uncategorised"): "Assistants & Domain Agents",
    ("e2b", "Technical challenges of building AI products"): "Docs, Learning & Lists",

    # awesome-harness-engineering
    ("harness", "Agent Loop"): "Orchestrators & Multi-Agent",
    ("harness", "Task Runners & Orchestration"): "Orchestrators & Multi-Agent",
    ("harness", "Planning & Task Decomposition"): "Orchestrators & Multi-Agent",
    ("harness", "Skills & MCP"): "Agent Skills",  # split per listing, see SPLIT_BY_EVIDENCE
    ("harness", "Demo Harnesses"): "Harnesses & Runtime Infra",
    ("harness", "Generators & Meta-Harnesses"): "Harnesses & Runtime Infra",
    ("harness", "Production Infrastructure & Operations"): "Harnesses & Runtime Infra",
    ("harness", "Context Delivery & Compaction"): "Context, Memory & RAG",
    ("harness", "Memory & State"): "Context, Memory & RAG",
    ("harness", "Security, Sandbox & Permissions"): "Sandbox, Security & Governance",
    ("harness", "Permissions & Authorization"): "Sandbox, Security & Governance",
    ("harness", "Observability & Tracing"): "Observability & Evals",
    ("harness", "Evals & Verification"): "Observability & Evals",
    ("harness", "Verification & CI Integration"): "Observability & Evals",
    ("harness", "Debugging & Developer Experience"): "Observability & Evals",
    # All 27 `Foundations` entries are articles -- OpenAI on harness engineering, Anthropic's "Building
    # Effective Agents", Fowler's synthesis, IBM's definitional piece. Reading, so filed as reading.
    ("harness", "Foundations"): "Docs, Learning & Lists",
    # Tool Design is half write-ups and half libraries (`outlines`, `instructor`, `tui-use`), but both
    # halves are about the interface an agent calls through, which is where `e2b / Tool for agents` went.
    ("harness", "Tool Design"): "Frameworks & SDKs",
    # HITL is approval mechanics: interrupt and breakpoint, `canUseTool`, review URLs, autonomy limits.
    # That is the same question as `harness / Permissions & Authorization`, so the same shelf.
    ("harness", "Human-in-the-Loop"): "Sandbox, Security & Governance",
    ("harness", "Tutorials & Educational"): "Docs, Learning & Lists",
    ("harness", "Adjacent Collections"): "Docs, Learning & Lists",
    ("harness", "Related Awesome Lists"): "Docs, Learning & Lists",

    # awesome-llm-apps -- runnable example apps, filed by what each app does rather than by how
    # finished it is. "Starter" and "Advanced" describe the reader's level, not the software: a travel
    # planner, a fitness coach and a fraud investigator are domain agents at either level.
    ("llmapps", "Starter AI Agents"): "Assistants & Domain Agents",
    ("llmapps", "Advanced AI Agents"): "Assistants & Domain Agents",
    # Every "Chat with X" entry is retrieval over one source, and its own description says so -- "any
    # repo, answered in 30 lines of RAG".
    ("llmapps", "Chat with X"): "Context, Memory & RAG",
    ("llmapps", "Generative UI and Agentic Frontends"): "Plugins, Themes & Clients",
    ("llmapps", "Multi-agent Teams"): "Orchestrators & Multi-Agent",
    ("llmapps", "Always-on Agents"): "Orchestrators & Multi-Agent",
    ("llmapps", "Agent Skills"): "Agent Skills",
    ("llmapps", "MCP AI Agents"): "MCP Servers",
    ("llmapps", "RAG (Retrieval Augmented Generation)"): "Context, Memory & RAG",
    ("llmapps", "LLM Apps with Memory"): "Context, Memory & RAG",
    ("llmapps", "LLM Optimization Tools"): "Harnesses & Runtime Infra",
    ("llmapps", "LLM Fine-tuning"): "Harnesses & Runtime Infra",
    ("llmapps", "Voice AI Agents"): "Creative, Voice & Media",
    ("llmapps", "Autonomous Game-Playing Agents"): "Creative, Voice & Media",
    ("llmapps", "AI Agent Framework Crash Courses"): "Docs, Learning & Lists",

    # awesome-opencode -- PROJECTS is tooling built around opencode, not standalone agents
    ("opencode", "PLUGINS"): "Plugins, Themes & Clients",
    ("opencode", "PROJECTS"): "Plugins, Themes & Clients",
    ("opencode", "THEMES"): "Plugins, Themes & Clients",
    ("opencode", "AGENTS"): "Coding Agents",
    ("opencode", "Official Repositories"): "Coding Agents",
    ("opencode", "RESOURCES"): "Docs, Learning & Lists",

    # awesome-agentic-patterns -- filed by the topic each pattern is about, so a topic page carries both
    # the tools and the write-ups about them. Every entry here is a write-up in nibzard's repo with no
    # stars of its own, which is why none of them can have a shelf of their own.
    ("patterns", "Orchestration & Control"): "Orchestrators & Multi-Agent",
    ("patterns", "Context & Memory"): "Context, Memory & RAG",
    ("patterns", "Security & Safety"): "Sandbox, Security & Governance",
    ("patterns", "Reliability & Eval"): "Observability & Evals",
    ("patterns", "Tool Use & Environment"): "Frameworks & SDKs",
    # Graders, self-critique, CI feedback, incident-to-eval: verification loops, so they sit with evals.
    ("patterns", "Feedback Loops"): "Observability & Evals",
    # Postures rather than artefacts -- "humans outside, in, or on the loop", workflow design, tooling
    # assumptions. Guidance for a reader, so it goes where the other guidance is.
    ("patterns", "UX & Collaboration"): "Docs, Learning & Lists",
    ("patterns", "Learning & Adaptation"): "Context, Memory & RAG",

    # Two skill directories. Their sections describe what a skill is *for*, not what it is, so the
    # `Targets` axis and the section column carry that and the category stays one shelf -- except for
    # the one section that names the protocol, which is servers rather than skills.
    ("skills", "AI Platforms & Models"): "Agent Skills",
    ("skills", "Business, Productivity & Marketing"): "Agent Skills",
    ("skills", "Cloud & Infrastructure"): "Agent Skills",
    ("skills", "Developer Tools & Frameworks"): "Agent Skills",
    ("skills", "Security & Web Intelligence"): "Agent Skills",
    ("skills", "Community Skills"): "Agent Skills",
    ("skills", "Google Ecosystem"): "Agent Skills",
    ("skills", "Claude and Anthropic"): "Agent Skills",
    ("skills", "Model Context Protocol (MCP)"): "MCP Servers",
    ("skills", "GitHub Copilot"): "Agent Skills",
    ("skills_aas", "Official Sources"): "Agent Skills",
    ("skills_aas", "Community Contributors"): "Agent Skills",
    ("skills_aas", "Community"): "Agent Skills",
    ("skills_aas", "Additional Sources"): "Agent Skills",
    ("skills_aas", "Inspirations"): "Agent Skills",

    # The original orchestrators list. "Resting" is a liveness bucket, not a topic -- its seventeen
    # entries are orchestration projects that stopped shipping, and the status note says so.
    ("orchestrators", "Parallel Coding Agents — Terminal (TUI/CLI)"): "Coding Agents",
    ("orchestrators", "Parallel Coding Agents — Desktop & Web"): "Coding Agents",
    ("orchestrators", "Multi-Agent Swarms"): "Orchestrators & Multi-Agent",
    ("orchestrators", "Autonomous Loop Runners"): "Orchestrators & Multi-Agent",
    ("orchestrators", "Autonomous Task Runners"): "Orchestrators & Multi-Agent",
    ("orchestrators", "Resting"): "Orchestrators & Multi-Agent",
    ("orchestrators", "Agent Infrastructure & Primitives"): "Frameworks & SDKs",
    ("orchestrators", "Personal Assistants"): "Assistants & Domain Agents",

    # jim-schwoebel/awesome_ai_agents
    # LLM Models is a shelf of open-weight models you actually run, not a reading list, so it lands
    # with the runtime infra on the precedent set by agents2026 / Open-Source Models for Agents.
    ("aiagents_schwoebel", "Frameworks"): "Frameworks & SDKs",
    ("aiagents_schwoebel", "Tools"): "Frameworks & SDKs",
    ("aiagents_schwoebel", "Deployment"): "Harnesses & Runtime Infra",
    ("aiagents_schwoebel", "LLM Models"): "Harnesses & Runtime Infra",
    ("aiagents_schwoebel", "Security"): "Sandbox, Security & Governance",
    ("aiagents_schwoebel", "Benchmarks"): "Observability & Evals",
    ("aiagents_schwoebel", "Testing"): "Observability & Evals",
    ("aiagents_schwoebel", "Repositories"): "Assistants & Domain Agents",

    # tensorchord/Awesome-LLMOps
    ("llmops_tensorchord", "Code AI"): "Coding Agents",
    ("llmops_tensorchord", "AutoML"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Federated ML"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Foundation Model Fine Tuning"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Frameworks for Training"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Frameworks/Servers for Serving"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "IDEs and Workspaces"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Large Language Model"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Large Model Serving"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "ML Compiler"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "ML Platforms"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Model Editing"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Model Management"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Optimizations"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Robotics Foundation Model"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Scheduling"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Workflow"): "Harnesses & Runtime Infra",
    ("llmops_tensorchord", "Data Management"): "Context, Memory & RAG",
    ("llmops_tensorchord", "Data Storage"): "Context, Memory & RAG",
    ("llmops_tensorchord", "Data/Feature enrichment"): "Context, Memory & RAG",
    ("llmops_tensorchord", "Feature Engineering"): "Context, Memory & RAG",
    ("llmops_tensorchord", "Hybrid search"): "Context, Memory & RAG",
    ("llmops_tensorchord", "Vector search"): "Context, Memory & RAG",
    ("llmops_tensorchord", "Frameworks for LLM security"): "Sandbox, Security & Governance",
    ("llmops_tensorchord", "Data Tracking"): "Observability & Evals",
    ("llmops_tensorchord", "Experiment Tracking"): "Observability & Evals",
    ("llmops_tensorchord", "LLMOps"): "Observability & Evals",
    ("llmops_tensorchord", "Observability"): "Observability & Evals",
    ("llmops_tensorchord", "Profiling"): "Observability & Evals",
    ("llmops_tensorchord", "Visualization"): "Observability & Evals",
    ("llmops_tensorchord", "Audio Foundation Model"): "Creative, Voice & Media",
    ("llmops_tensorchord", "CV Foundation Model"): "Creative, Voice & Media",
    ("llmops_tensorchord", "Awesome Lists"): "Docs, Learning & Lists",

    # rohitg00/awesome-devops-mcp-servers
    ("mcp_devops_rohitg00", "API Cost Management"): "MCP Servers",
    ("mcp_devops_rohitg00", "Aggregators"): "MCP Servers",
    ("mcp_devops_rohitg00", "Alerting & Notification"): "MCP Servers",
    ("mcp_devops_rohitg00", "Application Performance Monitoring"): "MCP Servers",
    ("mcp_devops_rohitg00", "Browser Automation"): "MCP Servers",
    ("mcp_devops_rohitg00", "CMS & Web Platforms"): "MCP Servers",
    ("mcp_devops_rohitg00", "Cloud Providers"): "MCP Servers",
    ("mcp_devops_rohitg00", "Code Execution"): "MCP Servers",
    ("mcp_devops_rohitg00", "Coding Agents"): "MCP Servers",
    ("mcp_devops_rohitg00", "Command Line"): "MCP Servers",
    ("mcp_devops_rohitg00", "Container Orchestration"): "MCP Servers",
    ("mcp_devops_rohitg00", "Continuous Integration"): "MCP Servers",
    ("mcp_devops_rohitg00", "Database Management"): "MCP Servers",
    ("mcp_devops_rohitg00", "Dependency Analysis"): "MCP Servers",
    ("mcp_devops_rohitg00", "DevOps Visibility"): "MCP Servers",
    ("mcp_devops_rohitg00", "Infrastructure as Code"): "MCP Servers",
    ("mcp_devops_rohitg00", "Memory & Context"): "MCP Servers",
    ("mcp_devops_rohitg00", "Metrics & Monitoring"): "MCP Servers",
    ("mcp_devops_rohitg00", "Mobile CI/CD"): "MCP Servers",
    ("mcp_devops_rohitg00", "Project Management"): "MCP Servers",
    ("mcp_devops_rohitg00", "Security"): "MCP Servers",
    ("mcp_devops_rohitg00", "Social Media Monitoring"): "MCP Servers",
    ("mcp_devops_rohitg00", "Testing & Chaos Engineering"): "MCP Servers",
    ("mcp_devops_rohitg00", "Ticketing Systems"): "MCP Servers",
    ("mcp_devops_rohitg00", "Version Control"): "MCP Servers",
    ("mcp_devops_rohitg00", "Frameworks"): "Frameworks & SDKs",
    ("mcp_devops_rohitg00", "Related Resources"): "Docs, Learning & Lists",

    # punkpeye/awesome-mcp-servers
    ("mcp_punkpeye", "Accessibility"): "MCP Servers",
    ("mcp_punkpeye", "Aerospace & Astrodynamics"): "MCP Servers",
    ("mcp_punkpeye", "Aggregators"): "MCP Servers",
    ("mcp_punkpeye", "Agreements & Coordination"): "MCP Servers",
    ("mcp_punkpeye", "Architecture & Design"): "MCP Servers",
    ("mcp_punkpeye", "Art & Culture"): "MCP Servers",
    ("mcp_punkpeye", "Biology, Medicine and Bioinformatics"): "MCP Servers",
    ("mcp_punkpeye", "Browser Automation"): "MCP Servers",
    ("mcp_punkpeye", "Cloud Platforms"): "MCP Servers",
    ("mcp_punkpeye", "Code Execution"): "MCP Servers",
    ("mcp_punkpeye", "Coding Agents"): "MCP Servers",
    ("mcp_punkpeye", "Command Line"): "MCP Servers",
    ("mcp_punkpeye", "Communication"): "MCP Servers",
    ("mcp_punkpeye", "Conversational AI"): "MCP Servers",
    ("mcp_punkpeye", "Cryptography"): "MCP Servers",
    ("mcp_punkpeye", "Customer Data Platforms"): "MCP Servers",
    ("mcp_punkpeye", "Data Platforms"): "MCP Servers",
    ("mcp_punkpeye", "Data Science Tools"): "MCP Servers",
    ("mcp_punkpeye", "Data Visualization"): "MCP Servers",
    ("mcp_punkpeye", "Databases"): "MCP Servers",
    ("mcp_punkpeye", "Delivery"): "MCP Servers",
    ("mcp_punkpeye", "Developer Tools"): "MCP Servers",
    ("mcp_punkpeye", "E-Commerce"): "MCP Servers",
    ("mcp_punkpeye", "Education"): "MCP Servers",
    ("mcp_punkpeye", "Embedded System"): "MCP Servers",
    ("mcp_punkpeye", "Environment & Nature"): "MCP Servers",
    ("mcp_punkpeye", "File Systems"): "MCP Servers",
    ("mcp_punkpeye", "Finance & Fintech"): "MCP Servers",
    ("mcp_punkpeye", "Gaming"): "MCP Servers",
    ("mcp_punkpeye", "Health & Wellness"): "MCP Servers",
    ("mcp_punkpeye", "Home Automation"): "MCP Servers",
    ("mcp_punkpeye", "Industrial & IoT"): "MCP Servers",
    ("mcp_punkpeye", "Knowledge & Memory"): "MCP Servers",
    ("mcp_punkpeye", "Legal"): "MCP Servers",
    ("mcp_punkpeye", "Location Services"): "MCP Servers",
    ("mcp_punkpeye", "Marketing"): "MCP Servers",
    ("mcp_punkpeye", "Monitoring"): "MCP Servers",
    ("mcp_punkpeye", "Multimedia Process"): "MCP Servers",
    ("mcp_punkpeye", "OS Automation"): "MCP Servers",
    ("mcp_punkpeye", "Other Tools and Integrations"): "MCP Servers",
    ("mcp_punkpeye", "Podcasts"): "MCP Servers",
    ("mcp_punkpeye", "Product Management"): "MCP Servers",
    ("mcp_punkpeye", "Real Estate"): "MCP Servers",
    ("mcp_punkpeye", "Research"): "MCP Servers",
    ("mcp_punkpeye", "Search & Data Extraction"): "MCP Servers",
    ("mcp_punkpeye", "Security"): "MCP Servers",
    ("mcp_punkpeye", "Social Media"): "MCP Servers",
    ("mcp_punkpeye", "Speech-to-Text"): "MCP Servers",
    ("mcp_punkpeye", "Spirituality & Esoterica"): "MCP Servers",
    ("mcp_punkpeye", "Sports"): "MCP Servers",
    ("mcp_punkpeye", "Support & Service Management"): "MCP Servers",
    ("mcp_punkpeye", "Text-to-Speech"): "MCP Servers",
    ("mcp_punkpeye", "Translation Services"): "MCP Servers",
    ("mcp_punkpeye", "Travel & Transportation"): "MCP Servers",
    ("mcp_punkpeye", "Version Control"): "MCP Servers",
    ("mcp_punkpeye", "Workplace & Productivity"): "MCP Servers",
    ("mcp_punkpeye", "end to end RAG platforms"): "MCP Servers",
    ("mcp_punkpeye", "Frameworks"): "Frameworks & SDKs",

    # wong2/awesome-mcp-servers
    ("mcp_wong2", "Community Servers"): "MCP Servers",
    ("mcp_wong2", "Official Servers"): "MCP Servers",
    ("mcp_wong2", "Reference Servers"): "MCP Servers",
    ("mcp_wong2", "Frameworks"): "Frameworks & SDKs",
    ("mcp_wong2", "Clients"): "Plugins, Themes & Clients",

    # Merit-Systems/awesome-agentic-commerce
    ("agentic_commerce", "Example Apps"): "Frameworks & SDKs",
    ("agentic_commerce", "Open Source & SDKs"): "Frameworks & SDKs",
    ("agentic_commerce", "Standards and EIPs"): "Frameworks & SDKs",
    ("agentic_commerce", "Facilitators & Networks"): "Harnesses & Runtime Infra",
    ("agentic_commerce", "Security & Ops"): "Sandbox, Security & Governance",
    ("agentic_commerce", "Ecosystem"): "Assistants & Domain Agents",
    ("agentic_commerce", "Official Resources"): "Docs, Learning & Lists",
    ("agentic_commerce", "Tutorials & Guides"): "Docs, Learning & Lists",

    # Jenqyang/Awesome-AI-Agents
    ("aiagents_jenqyang", "Autonomous Agent Task Solver Projects"): "Orchestrators & Multi-Agent",
    ("aiagents_jenqyang", "Multi-Agent Task Solver Projects"): "Orchestrators & Multi-Agent",
    ("aiagents_jenqyang", "Frameworks"): "Frameworks & SDKs",
    ("aiagents_jenqyang", "Tools"): "Frameworks & SDKs",
    ("aiagents_jenqyang", "Platforms/API"): "Harnesses & Runtime Infra",
    ("aiagents_jenqyang", "Advanced Components"): "Context, Memory & RAG",
    ("aiagents_jenqyang", "Benchmark/Evaluator"): "Observability & Evals",
    ("aiagents_jenqyang", "Agent Society Simulation"): "Creative, Voice & Media",
    ("aiagents_jenqyang", "Blog"): "Docs, Learning & Lists",
    ("aiagents_jenqyang", "Paper-List Repo"): "Docs, Learning & Lists",
    ("aiagents_jenqyang", "Reference Repo"): "Docs, Learning & Lists",
    ("aiagents_jenqyang", "Survey"): "Docs, Learning & Lists",

    # ccplugins/awesome-claude-code-plugins
    ("cc_plugins", "Workflow Orchestration"): "Orchestrators & Multi-Agent",
    ("cc_plugins", "Skills & Frameworks"): "Agent Skills",
    ("cc_plugins", "MCP Servers"): "MCP Servers",
    ("cc_plugins", "Automation DevOps"): "Harnesses & Runtime Infra",
    ("cc_plugins", "Knowledge Management"): "Context, Memory & RAG",
    ("cc_plugins", "Thinking & Knowledge Management"): "Context, Memory & RAG",
    ("cc_plugins", "Security, Compliance, & Legal"): "Sandbox, Security & Governance",
    ("cc_plugins", "Code Quality Testing"): "Observability & Evals",
    ("cc_plugins", "Communication & Integrations"): "Plugins, Themes & Clients",
    ("cc_plugins", "Companion Apps & Tools"): "Plugins, Themes & Clients",
    ("cc_plugins", "Design UX"): "Plugins, Themes & Clients",
    ("cc_plugins", "Development Engineering"): "Plugins, Themes & Clients",
    ("cc_plugins", "Git Workflow"): "Plugins, Themes & Clients",
    ("cc_plugins", "Official Claude Code Plugins"): "Plugins, Themes & Clients",
    ("cc_plugins", "Data Analytics"): "Research & Data Agents",
    ("cc_plugins", "AI & Speech"): "Creative, Voice & Media",
    ("cc_plugins", "Audio & Media"): "Creative, Voice & Media",
    ("cc_plugins", "Business Sales"): "Assistants & Domain Agents",
    ("cc_plugins", "Lifestyle & Entertainment"): "Assistants & Domain Agents",
    ("cc_plugins", "Marketing Growth"): "Assistants & Domain Agents",
    ("cc_plugins", "Project & Product Management"): "Assistants & Domain Agents",
    ("cc_plugins", "Documentation"): "Docs, Learning & Lists",
    ("cc_plugins", "External Marketplaces"): "Docs, Learning & Lists",
    ("cc_plugins", "Marketplaces"): "Docs, Learning & Lists",
    ("cc_plugins", "Resources"): "Docs, Learning & Lists",

    # VoltAgent/awesome-claude-code-subagents
    ("cc_subagents_voltagent", "01. Core Development"): "Agent Skills",
    ("cc_subagents_voltagent", "02. Language Specialists"): "Agent Skills",
    ("cc_subagents_voltagent", "03. Infrastructure"): "Agent Skills",
    ("cc_subagents_voltagent", "04. Quality & Security"): "Agent Skills",
    ("cc_subagents_voltagent", "05. Data & AI"): "Agent Skills",
    ("cc_subagents_voltagent", "06. Developer Experience"): "Agent Skills",
    ("cc_subagents_voltagent", "07. Specialized Domains"): "Agent Skills",
    ("cc_subagents_voltagent", "08. Business & Product"): "Agent Skills",
    ("cc_subagents_voltagent", "09. Meta & Orchestration"): "Agent Skills",
    ("cc_subagents_voltagent", "10. Research & Analysis"): "Agent Skills",

    # rohitg00/awesome-claude-code-toolkit
    # One repo, itemised: 344 of its 699 rows are markdown/JSON artefacts inside the toolkit itself.
    # Its ten Agents shelves, eight Commands shelves, Rules and Contexts all describe what one
    # uniform artefact is *for*, not what it is, so they take one shelf and the section column
    # carries the domain -- the same reading as ('skills', *) and ('skills_aas', *). Carved out for
    # the same reason ('skills', 'Model Context Protocol (MCP)') is: 'MCP Configs' names the
    # protocol, and 'Research & Analysis (11 agents)' is the one Agents shelf that also holds real
    # third-party research repos. 'Examples' is three walkthroughs, so it reads as reading, like
    # ('harness', 'Tutorials & Educational').
    ("cc_toolkit_rohitg00", "Architecture"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Business & Product"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Community Skills"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Contexts"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Core Development"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Data & AI"): "Agent Skills",
    ("cc_toolkit_rohitg00", "DevOps"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Developer Experience"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Documentation"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Git"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Infrastructure"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Language Experts"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Orchestration"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Quality Assurance"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Refactoring"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Rules"): "Agent Skills",
    ("cc_toolkit_rohitg00", "SKY-lv Skills"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Security"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Skills"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Specialized Domains"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Testing"): "Agent Skills",
    ("cc_toolkit_rohitg00", "Workflow"): "Agent Skills",
    ("cc_toolkit_rohitg00", "MCP Configs"): "MCP Servers",
    ("cc_toolkit_rohitg00", "Related SDKs"): "Frameworks & SDKs",
    ("cc_toolkit_rohitg00", "All Plugins"): "Plugins, Themes & Clients",
    ("cc_toolkit_rohitg00", "Companion Apps & GUIs"): "Plugins, Themes & Clients",
    ("cc_toolkit_rohitg00", "Ecosystem"): "Plugins, Themes & Clients",
    ("cc_toolkit_rohitg00", "Featured"): "Plugins, Themes & Clients",
    ("cc_toolkit_rohitg00", "Hook Scripts"): "Plugins, Themes & Clients",
    ("cc_toolkit_rohitg00", "Templates"): "Plugins, Themes & Clients",
    ("cc_toolkit_rohitg00", "Research & Analysis"): "Research & Data Agents",
    ("cc_toolkit_rohitg00", "Examples"): "Docs, Learning & Lists",
    ("cc_toolkit_rohitg00", "Related Awesome Lists"): "Docs, Learning & Lists",
    ("cc_toolkit_rohitg00", "Resources"): "Docs, Learning & Lists",

    # jqueryscript/awesome-claude-code
    ("claudecode_jq", "Agents & Orchestration"): "Orchestrators & Multi-Agent",
    ("claudecode_jq", "Agent Skills"): "Agent Skills",
    ("claudecode_jq", "Official Resources"): "Frameworks & SDKs",
    ("claudecode_jq", "SDKs & Development Kits"): "Frameworks & SDKs",
    ("claudecode_jq", "Infrastructure & Proxies"): "Harnesses & Runtime Infra",
    ("claudecode_jq", "Usage & Observability"): "Observability & Evals",
    ("claudecode_jq", "Claude Plugins"): "Plugins, Themes & Clients",
    ("claudecode_jq", "Clients & GUIs"): "Plugins, Themes & Clients",
    ("claudecode_jq", "IDE & Editor Integrations"): "Plugins, Themes & Clients",
    ("claudecode_jq", "Tools & Utilities"): "Plugins, Themes & Clients",
    ("claudecode_jq", "Guides & Learning"): "Docs, Learning & Lists",

    # machinae/awesome-claws
    ("claws", "Main Projects"): "Assistants & Domain Agents",

    # RoggeOhta/awesome-codex-cli
    ("codexcli", "CI/CD & Automation"): "Orchestrators & Multi-Agent",
    ("codexcli", "Cross-Agent Tools"): "Orchestrators & Multi-Agent",
    ("codexcli", "Subagents"): "Orchestrators & Multi-Agent",
    ("codexcli", "AGENTS.md Templates"): "Agent Skills",
    ("codexcli", "Skills"): "Agent Skills",
    ("codexcli", "MCP Servers"): "MCP Servers",
    ("codexcli", "Account & Auth"): "Harnesses & Runtime Infra",
    ("codexcli", "Model Providers & Proxies"): "Harnesses & Runtime Infra",
    ("codexcli", "Session & Workflow Management"): "Harnesses & Runtime Infra",
    ("codexcli", "Docker & Sandboxing"): "Sandbox, Security & Governance",
    ("codexcli", "Monitoring & Analytics"): "Observability & Evals",
    ("codexcli", "GUI & Desktop Apps"): "Plugins, Themes & Clients",
    ("codexcli", "Hooks"): "Plugins, Themes & Clients",
    ("codexcli", "IDE & Editor Integrations"): "Plugins, Themes & Clients",
    ("codexcli", "Plugins"): "Plugins, Themes & Clients",
    ("codexcli", "Remote Access"): "Plugins, Themes & Clients",
    ("codexcli", "Shell & Terminal"): "Plugins, Themes & Clients",
    ("codexcli", "Community"): "Docs, Learning & Lists",
    ("codexcli", "Comparisons"): "Docs, Learning & Lists",
    ("codexcli", "Getting Started"): "Docs, Learning & Lists",
    ("codexcli", "Official Resources"): "Docs, Learning & Lists",
    ("codexcli", "Tutorials & Articles"): "Docs, Learning & Lists",

    # ai-for-developers/awesome-ai-coding-tools
    ("codingtools_a4d", "App Builders"): "Coding Agents",
    ("codingtools_a4d", "CLI Tools"): "Coding Agents",
    ("codingtools_a4d", "Code Completion"): "Coding Agents",
    ("codingtools_a4d", "Code Editors and Assistants"): "Coding Agents",
    ("codingtools_a4d", "Coding Agents"): "Coding Agents",
    ("codingtools_a4d", "MCP Servers and Directories"): "MCP Servers",
    ("codingtools_a4d", "AI Frameworks and SDKs"): "Frameworks & SDKs",
    ("codingtools_a4d", "Code Models"): "Harnesses & Runtime Infra",
    ("codingtools_a4d", "DevOps and Infrastructure"): "Harnesses & Runtime Infra",
    ("codingtools_a4d", "Local LLM Tools"): "Harnesses & Runtime Infra",
    ("codingtools_a4d", "Code Search and Navigation"): "Context, Memory & RAG",
    ("codingtools_a4d", "Security"): "Sandbox, Security & Governance",
    ("codingtools_a4d", "Code Review and Refactoring"): "Observability & Evals",
    ("codingtools_a4d", "Testing and QA"): "Observability & Evals",
    ("codingtools_a4d", "Database and API Tools"): "Research & Data Agents",
    ("codingtools_a4d", "UI Generators"): "Creative, Voice & Media",
    ("codingtools_a4d", "Developer Productivity Tools"): "Assistants & Domain Agents",
    ("codingtools_a4d", "Documentation"): "Docs, Learning & Lists",
    ("codingtools_a4d", "Related Lists"): "Docs, Learning & Lists",

    # github/awesome-copilot
    ("copilot_github", "How to Use Agentic Workflows"): "Orchestrators & Multi-Agent",
    ("copilot_github", "How to Use Agent Skills"): "Agent Skills",
    ("copilot_github", "How to Use Custom Agents"): "Agent Skills",
    ("copilot_github", "How to Use Custom Instructions"): "Agent Skills",
    ("copilot_github", "How to Use Hooks"): "Plugins, Themes & Clients",
    ("copilot_github", "How to Use Plugins"): "Plugins, Themes & Clients",
    ("copilot_github", "Additional Resources"): "Docs, Learning & Lists",

    # PatrickJS/awesome-cursorrules
    ("cursorrules", "Backend and Full-Stack"): "Agent Skills",
    ("cursorrules", "Build Tools and Development"): "Agent Skills",
    ("cursorrules", "CSS and Styling"): "Agent Skills",
    ("cursorrules", "Database and API"): "Agent Skills",
    ("cursorrules", "Documentation"): "Agent Skills",
    ("cursorrules", "Frontend Frameworks and Libraries"): "Agent Skills",
    ("cursorrules", "Games and Graphics"): "Agent Skills",
    ("cursorrules", "Hosting and Deployments"): "Agent Skills",
    ("cursorrules", "Language-Specific"): "Agent Skills",
    ("cursorrules", "Mobile Development"): "Agent Skills",
    ("cursorrules", "Security"): "Agent Skills",
    ("cursorrules", "State Management"): "Agent Skills",
    ("cursorrules", "Testing"): "Agent Skills",
    ("cursorrules", "Directories"): "Docs, Learning & Lists",

    # jamesmurdza/awesome-ai-devtools
    ("devtools_murdza", "Multi-Agent Orchestration"): "Orchestrators & Multi-Agent",
    ("devtools_murdza", "AI-Native IDEs"): "Coding Agents",
    ("devtools_murdza", "App Builders"): "Coding Agents",
    ("devtools_murdza", "CLI Utilities"): "Coding Agents",
    ("devtools_murdza", "Coding Agents"): "Coding Agents",
    ("devtools_murdza", "Git & Commit Helpers"): "Coding Agents",
    ("devtools_murdza", "IDE Extensions"): "Coding Agents",
    ("devtools_murdza", "Snippet & Utility Tools"): "Coding Agents",
    ("devtools_murdza", "Terminal Agents"): "Coding Agents",
    ("devtools_murdza", "Codebase Intelligence"): "Context, Memory & RAG",
    ("devtools_murdza", "Configuration & Context Management"): "Context, Memory & RAG",
    ("devtools_murdza", "Sandboxing & Isolation"): "Sandbox, Security & Governance",
    ("devtools_murdza", "CI/CD & Testing Automation"): "Observability & Evals",
    ("devtools_murdza", "PR & Code Review Bots"): "Observability & Evals",
    ("devtools_murdza", "Usage Analytics & Cost Tracking"): "Observability & Evals",
    ("devtools_murdza", "Desktop & Mobile Applications"): "Plugins, Themes & Clients",
    ("devtools_murdza", "Database & SQL"): "Research & Data Agents",
    ("devtools_murdza", "UI Generators"): "Creative, Voice & Media",
    ("devtools_murdza", "Documentation Generation"): "Docs, Learning & Lists",
    ("devtools_murdza", "Resources"): "Docs, Learning & Lists",

    # Piebald-AI/awesome-gemini-cli
    ("geminicli", "Agent Orchestration & CLI Tools"): "Orchestrators & Multi-Agent",
    ("geminicli", "Forks"): "Coding Agents",
    ("geminicli", "Official"): "Coding Agents",
    ("geminicli", "Prompts"): "Agent Skills",
    ("geminicli", "MCP Servers"): "MCP Servers",
    ("geminicli", "Frameworks"): "Frameworks & SDKs",
    ("geminicli", "SDKs"): "Frameworks & SDKs",
    ("geminicli", "API Bridges & Proxies"): "Harnesses & Runtime Infra",
    ("geminicli", "Development Tools & Utilities"): "Harnesses & Runtime Infra",
    ("geminicli", "Browser Extensions"): "Plugins, Themes & Clients",
    ("geminicli", "Commands & Extensions"): "Plugins, Themes & Clients",
    ("geminicli", "Fun"): "Plugins, Themes & Clients",
    ("geminicli", "Interfaces"): "Plugins, Themes & Clients",
    ("geminicli", "Neovim Plugins"): "Plugins, Themes & Clients",
    ("geminicli", "Education & Study Tools"): "Assistants & Domain Agents",
    ("geminicli", "Non-Gemini CLI"): "Assistants & Domain Agents",
    ("geminicli", "Documentation & Examples"): "Docs, Learning & Lists",

    # kaushikb11/awesome-llm-agents
    ("llmagents_kaushikb11", "Autonomous Agents (2023 wave)"): "Orchestrators & Multi-Agent",
    ("llmagents_kaushikb11", "Multi-Agent Orchestration"): "Orchestrators & Multi-Agent",
    ("llmagents_kaushikb11", "CLI Agent Harnesses"): "Coding Agents",
    ("llmagents_kaushikb11", "Agent Infrastructure"): "Frameworks & SDKs",
    ("llmagents_kaushikb11", "Core Frameworks"): "Frameworks & SDKs",
    ("llmagents_kaushikb11", "Inactive"): "Frameworks & SDKs",
    ("llmagents_kaushikb11", "Low-Code & Visual Builders"): "Frameworks & SDKs",
    ("llmagents_kaushikb11", "Research & Experimental"): "Frameworks & SDKs",
    ("llmagents_kaushikb11", "Memory & Context"): "Context, Memory & RAG",
    ("llmagents_kaushikb11", "Retrieval & Data"): "Context, Memory & RAG",
    ("llmagents_kaushikb11", "Safety, Security & Evaluation"): "Sandbox, Security & Governance",
    ("llmagents_kaushikb11", "Domain-Specific Agents"): "Assistants & Domain Agents",

    # InftyAI/Awesome-LLMOps
    ("llmops_inftyai", "AI Terminal"): "Coding Agents",
    ("llmops_inftyai", "Code Agent"): "Coding Agents",
    ("llmops_inftyai", "Agent Framework"): "Frameworks & SDKs",
    ("llmops_inftyai", "Evolve Agent"): "Frameworks & SDKs",
    ("llmops_inftyai", "Output"): "Frameworks & SDKs",
    ("llmops_inftyai", "Tool"): "Frameworks & SDKs",
    ("llmops_inftyai", "AI Gateway"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Agentic RL"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "FineTune"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Framework"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Inference Engine"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Inference Platform"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "LLM Router"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Middleware"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "RLHF"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Simulator"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Workflow"): "Harnesses & Runtime Infra",
    ("llmops_inftyai", "Database"): "Context, Memory & RAG",
    ("llmops_inftyai", "RAG"): "Context, Memory & RAG",
    ("llmops_inftyai", "Sandbox"): "Sandbox, Security & Governance",
    ("llmops_inftyai", "Application Framework"): "Observability & Evals",
    ("llmops_inftyai", "Benchmark"): "Observability & Evals",
    ("llmops_inftyai", "Observation"): "Observability & Evals",
    ("llmops_inftyai", "Chatbot"): "Plugins, Themes & Clients",
    ("llmops_inftyai", "Evolutionary Framework"): "Research & Data Agents",
    ("llmops_inftyai", "AI Agent"): "Assistants & Domain Agents",

    # spencerpauly/awesome-cursor-skills
    ("skills_cursor_spencerpauly", "Analytics & Tracking"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Authentication & Payments"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Code Quality & Security"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Cursor-Native"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Dependencies"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Documentation"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Error Tracking & Monitoring"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Frontend & UI"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Infrastructure & DevOps"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Planning & Architecture"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Testing"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Utilities"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Workflow"): "Agent Skills",
    ("skills_cursor_spencerpauly", "Tools"): "Frameworks & SDKs",
    ("skills_cursor_spencerpauly", "Plugins"): "Plugins, Themes & Clients",
    ("skills_cursor_spencerpauly", "Cursor Rules"): "Docs, Learning & Lists",
    ("skills_cursor_spencerpauly", "Directories"): "Docs, Learning & Lists",
    ("skills_cursor_spencerpauly", "Learning"): "Docs, Learning & Lists",

    # JackyST0/awesome-agent-skills
    ("skills_jackyst0", "Data Processing"): "Agent Skills",
    ("skills_jackyst0", "Design"): "Agent Skills",
    ("skills_jackyst0", "DevOps"): "Agent Skills",
    ("skills_jackyst0", "Development Tools"): "Agent Skills",
    ("skills_jackyst0", "Productivity"): "Agent Skills",
    ("skills_jackyst0", "Skills Collections"): "Agent Skills",
    ("skills_jackyst0", "Writing"): "Agent Skills",
    ("skills_jackyst0", "Official Resources"): "Docs, Learning & Lists",

    # libukai/awesome-agent-skills
    ("skills_libukai", "产品使用"): "Agent Skills",
    ("skills_libukai", "其他类型"): "Agent Skills",
    ("skills_libukai", "内容创作"): "Agent Skills",
    ("skills_libukai", "编程开发"): "Agent Skills",
    ("skills_libukai", "测试与评测"): "Observability & Evals",
    ("skills_libukai", "图文教程"): "Docs, Learning & Lists",
    ("skills_libukai", "官方文档"): "Docs, Learning & Lists",
    ("skills_libukai", "视频教程"): "Docs, Learning & Lists",

    # VoltAgent/awesome-agent-skills
    ("skills_voltagent", "Community Skills"): "Agent Skills",

    # filipecalegario/awesome-vibe-coding
    ("vibecoding", "Task Management for AI Coding"): "Orchestrators & Multi-Agent",
    ("vibecoding", "Browser-based Tools"): "Coding Agents",
    ("vibecoding", "Command Line Tools"): "Coding Agents",
    ("vibecoding", "IDEs and Code Editors"): "Coding Agents",
    ("vibecoding", "Local Apps"): "Coding Agents",
    ("vibecoding", "Mobile Apps"): "Coding Agents",
    ("vibecoding", "Plugins and Extensions"): "Coding Agents",
    ("vibecoding", "Documentation for AI Coding"): "Docs, Learning & Lists",
}

# The second axis: what a thing plugs into. Matched on text because no curator has a column for it --
# `("skills", "GitHub Copilot")` is the only section in 140 that names a harness. Order is display
# order. Each pattern is deliberately narrow: a false positive here puts a repo on a leaderboard it has
# no business being on, which is worse than missing one.
TARGETS: list[tuple[str, str]] = [
    ("Claude Code", r"claude[\s_.-]?code|\bclaude-?code\b|\bcchooks?\b"),
    # "agent skills" and "skills.md" used to belong here: when the only skills lists in the collection
    # were Claude's, the phrase named the vendor as reliably as the vendor's own name did. Ingesting
    # github/awesome-copilot ended that -- 415 of its 951 rows came back badged Anthropic on the word
    # alone, and Cursor, Gemini and Codex lists brought 50 more. Skills are a cross-vendor format now,
    # so the phrase says what a thing is, not whose it is; the Agent Skills category already says that,
    # and the skills lists that really are Claude's keep the tag through SOURCE_TARGETS.
    ("Claude / Anthropic", r"\banthropic\b|\bclaude\b"),
    ("opencode", r"\bopencode\b"),
    ("MCP", r"\bmcps?\b|model[\s-]context[\s-]protocol"),
    ("Codex / OpenAI", r"\bcodex\b|\bopenai\b|\bchatgpt\b|\bgpt-[45]\b|\bo[13]-(mini|pro)\b"),
    ("Gemini / Google", r"\bgemini\b|\bgoogle\b|\bvertex ai\b"),
    ("GitHub Copilot", r"\bcopilot\b"),
    ("Cursor", r"\bcursor(?:\s(?:ide|rules|agent|composer))?\b(?!\s*position)"),
    ("Cline / Roo", r"\bcline\b|roo[\s-]?code"),
    ("Aider", r"\baider\b"),
    ("LangChain / LangGraph", r"\blang(chain|graph|smith)\b"),
    # Named runtimes only. "runs locally" is a deployment fact about nearly everything here and
    # matching it tagged 187 repos, most of which target no local runtime in particular.
    ("Local / Ollama", r"\bollama\b|llama\.cpp|\bvllm\b|lm[\s-]studio|\bllamafile\b|\bgpt4all\b"),
]
_TARGETS = [(name, re.compile(pat, re.IGNORECASE)) for name, pat in TARGETS]

# A whole list devoted to one harness makes every entry in it a hit, which no per-entry text match
# would find: an opencode plugin's README rarely repeats the word.
SOURCE_TARGETS = {
    "claudecode": ("Claude Code", "Claude / Anthropic"),
    "opencode": ("opencode",),
    "skills": ("Claude / Anthropic",),
    "skills_aas": ("Claude / Anthropic",),
    "mcp_devops_rohitg00": ('MCP',),
    "mcp_punkpeye": ('MCP',),
    "mcp_wong2": ('MCP',),
    "cc_plugins": ('Claude Code',),
    "cc_subagents_voltagent": ('Claude Code',),
    "cc_toolkit_rohitg00": ('Claude Code',),
    "claudecode_jq": ('Claude Code',),
    "codexcli": ('Codex / OpenAI',),
    "copilot_github": ('GitHub Copilot',),
    "cursorrules": ('Cursor',),
    "geminicli": ('Gemini / Google',),
    "skills_cursor_spencerpauly": ('Cursor',),
    "skills_jackyst0": ('Claude / Anthropic',),
    "skills_libukai": ('Claude / Anthropic',),
    "skills_voltagent": ('Claude / Anthropic',),
}

RANK = {c: i for i, c in enumerate(CATEGORIES)}

# One key in 140 is both shelves at once and too big to file wholesale on either: `harness / Skills & MCP`
# is 41 entries holding the MCP specification, `modelcontextprotocol/servers`, MCP Inspector and the
# transport write-ups right next to `superpowers`, `addyosmani/agent-skills` and the skill benchmarks.
# Its curator named both shelves in the heading, so this is the one place a listing is read rather than
# looked up. Everywhere else a rename must be noticed, not absorbed -- adding keys here defeats that, so
# there is exactly one.
SPLIT_BY_EVIDENCE = {("harness", "Skills & MCP")}
_MCP = re.compile(r"\bmcps?\b|model[\s_.-]?context[\s_.-]?protocol|\ba2a\b|agent-to-agent|\bjson-?rpc\b",
                  re.IGNORECASE)
_SKILL = re.compile(r"\bskills?\b|SKILL\.md|\bsubagents?\b|\bslash command")


def source_of(rec: dict) -> str:
    """The list a record came from. The orchestrators records predate the `source` field."""
    return rec.get("source") or "orchestrators"


def _is_mcp_server(rec: dict) -> bool:
    """Names a protocol and no skill. Asymmetric on purpose, and the asymmetry is the whole rule.

    A skill is frequently *delivered* over MCP, so naming MCP is not evidence of being a server; naming a
    skill is evidence of being a skill. So the protocol only wins unopposed. Of the 41 listings this
    decides, 19 name a protocol alone and become servers; the other 22 -- 14 that name a skill, 3 that
    name both like "Dataverse Skills", and 5 that name neither -- stay on the section's first shelf.

    Deliberately excludes the section text from what it reads: "Skills & MCP" matches both patterns, so
    including it would veto every listing in the section.
    """
    hay = " ".join(str(rec.get(k) or "") for k in ("name", "nwo", "description", "gh_description"))
    return bool(_MCP.search(hay)) and not _SKILL.search(hay)


def category_of(rec: dict) -> str:
    """The category for one *listing*. A repo listed twice has two of these; see `by_repo`."""
    key = (source_of(rec), rec.get("section") or rec.get("category") or "")
    if key in SPLIT_BY_EVIDENCE and _is_mcp_server(rec):
        return "MCP Servers"
    return SECTIONS[key]


def targets_of(rec: dict) -> list[str]:
    """Every harness this listing names, in display order."""
    hay = " ".join(str(rec.get(k) or "") for k in
                   ("name", "nwo", "description", "gh_description", "section", "category",
                    "sub_category", "install_cmd", "homepage")) + " " + " ".join(rec.get("topics") or [])
    found = set(SOURCE_TARGETS.get(source_of(rec), ()))
    found.update(name for name, pat in _TARGETS if pat.search(hay))
    # "Claude Code" implies its vendor; the reverse is not true, and conflating them would put every
    # Agent Skill in the collection on the Claude Code leaderboard.
    if "Claude Code" in found:
        found.add("Claude / Anthropic")
    return [name for name, _ in TARGETS if name in found]


# `16_build_all.star_map`, filled by `load()`. Not a second opinion about star counts: a category
# leaderboard that ranked by `rec["stars"]` would put totals on these pages that the cover contradicts.
STARS: dict[str, int] = {}


def stars_of(rec: dict) -> int:
    """Stars the repo itself has, or 0 for a listing with none — a folder inside someone else's repo.

    `star_map` has already excluded the subpath and unavailable listings, so a miss here means exactly
    that: nothing to rank. This is what keeps a category leaderboard from claiming that each of the 193
    entries in awesome-agentic-patterns has that repo's whole star count.
    """
    return STARS.get(rec.get("nwo") or "", 0)


def rankable(rec: dict) -> bool:
    """The Leaderboard sheet's admission rule, so the per-category boards agree with the global one."""
    return bool(rec.get("nwo")) and rec.get("kind") != "subpath" \
        and not rec.get("unavailable") and stars_of(rec) > 0


def by_repo(records: list[dict]) -> dict[str, dict]:
    """Collapse listings to one row per repo: one category, the union of the targets.

    A repo on four lists gets four opinions about what it is. The most-listed category wins; an even
    split goes to whichever is earlier in `CATEGORIES`, where the specific shelves are, so a repo that
    is both "Coding" somewhere and "General purpose" elsewhere files under the specific one.

    Every repo gets a row, including the ones that cannot be ranked -- a folder inside a monorepo, an
    archived project, one the API never returned stars for. `rank` says which is which. Dropping them
    instead would quietly shrink the category pages, and a browsable page has every reason to list a
    skill that lives in a folder even though a leaderboard has no way to rank it.
    """
    votes: dict[str, Counter] = defaultdict(Counter)
    agg: dict[str, dict] = {}
    for r in records:
        nwo = r.get("nwo")
        if not nwo:
            continue
        votes[nwo][category_of(r)] += 1
        a = agg.setdefault(nwo, {"targets": set(), "sources": set(), "stars": 0, "rank": False})
        a["targets"].update(targets_of(r))
        a["sources"].add(source_of(r))
        a["stars"] = max(a["stars"], stars_of(r))
        a["rank"] = a["rank"] or rankable(r)
    for nwo, a in agg.items():
        v = votes[nwo]
        a["category"] = min(v, key=lambda c: (-v[c], RANK[c]))
        a["targets"] = [t for t, _ in TARGETS if t in a["targets"]]
        a["sources"] = sorted(a["sources"])
        a["listings"] = sum(v.values())
    return agg


def check(records: list[dict]) -> list[str]:
    """Sections in the data that this module does not name -- i.e. what a curator renamed."""
    seen = {(source_of(r), r.get("section") or r.get("category") or "") for r in records}
    return sorted(f"{s} / {sec}" for s, sec in seen - set(SECTIONS))


def load() -> list[dict]:
    """Both record files, canonicalised, with the orchestrators records given a `source`.

    Imports `16_build_all` for `canonicalise_nwo` rather than repeating it: without that pass three
    repos arrive under two casings each, which here would mean two rows in a category, two entries on
    its leaderboard, and -- because `meta.json` only answers to one spelling -- a star count of zero
    for one of them. Lazily, so that `16_build_all` can import this module without a cycle.
    """
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location("b16", Path(__file__).parent / "16_build_all.py")
    b16 = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("b16", b16)
    spec.loader.exec_module(b16)

    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    records = json.loads((CACHE / "records_all.json").read_text(encoding="utf-8"))
    orch = [dict(r, source="orchestrators")
            for r in json.loads((CACHE / "records.json").read_text(encoding="utf-8"))]
    b16.canonicalise_nwo(records, orch, meta)

    STARS.clear()
    STARS.update(b16.star_map(records, orch, meta))
    return records + orch


def why(records: list[dict], nwo: str) -> None:
    """Every listing of one repo and what each contributes -- for checking a suspicious target tag."""
    for r in records:
        if (r.get("nwo") or "").lower() == nwo.lower():
            print(f"  {source_of(r):12s} {r.get('section') or r.get('category')!r}")
            print(f"    -> {category_of(r)}   targets: {', '.join(targets_of(r)) or '-'}")
            print(f"    stars={stars_of(r):,} kind={r.get('kind', 'repo')} rankable={rankable(r)}")


def main() -> int:
    import sys
    records = load()
    missing = check(records)
    if missing:
        print(f"{len(missing)} unmapped sections:")
        for m in missing:
            print("  " + m)
        return 1

    if "--why" in sys.argv:
        why(records, sys.argv[sys.argv.index("--why") + 1])
        return 0

    repos = by_repo(records)
    ents = Counter(category_of(r) for r in records)
    print(f"{len(records):,} listings  ·  {len(repos):,} repos  ·  "
          f"{sum(1 for v in repos.values() if v['rank']):,} of them rankable  ·  "
          f"{len(CATEGORIES)} categories\n")

    print(f"{'CATEGORY':32s} {'ENTRIES':>7s} {'REPOS':>6s} {'RANK':>5s} {'STARS':>10s}  TOP REPO")
    for c in CATEGORIES:
        mine = {n: v for n, v in repos.items() if v["category"] == c}
        board = {n: v for n, v in mine.items() if v["rank"]}
        top = max(board, key=lambda n: board[n]["stars"], default=None)
        print(f"{c:32s} {ents[c]:7d} {len(mine):6d} {len(board):5d} "
              f"{sum(v['stars'] for v in board.values()):10,d}  "
              f"{f'{top} ({board[top]['stars']:,})' if top else '-- nothing rankable'}")
    print(f"{'TOTAL':32s} {sum(ents.values()):7d} {len(repos):6d} "
          f"{sum(1 for v in repos.values() if v['rank']):5d} "
          f"{sum(v['stars'] for v in repos.values() if v['rank']):10,d}")

    print(f"\n{'TARGET':24s} {'REPOS':>6s} {'RANK':>5s} {'STARS':>10s}  TOP REPO")
    for t, _ in TARGETS:
        board = {n: v for n, v in repos.items() if t in v["targets"] and v["rank"]}
        top = max(board, key=lambda n: board[n]["stars"], default=None)
        print(f"{t:24s} {sum(1 for v in repos.values() if t in v['targets']):6d} "
              f"{len(board):5d} {sum(v['stars'] for v in board.values()):10,d}  "
              f"{f'{top} ({board[top]['stars']:,})' if top else '-'}")
    plain = [v for v in repos.values() if not v["targets"]]
    print(f"{'(none named)':24s} {len(plain):6d} {sum(1 for v in plain if v['rank']):5d} "
          f"{sum(v['stars'] for v in plain if v['rank']):10,d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
