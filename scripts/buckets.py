"""Fold each source list's sections into at most eight colour buckets.

The validated categorical palette supplies exactly eight hues and the method
forbids inventing a ninth or cycling the eight. Several lists carry far more
sections than that (e2b tags 24, harness 21), so each sheet groups its sections
into <= 8 buckets that take the hues, and every row still prints its own
section name in a column of its own. Colour narrows the field; the label
identifies the row -- identity is never carried by hue alone.

Buckets are listed in the order they take palette slots. A section absent from
a map keeps its own name as its bucket, which is why the <= 8 lists need no
entry here.
"""

# source key -> [(bucket name, [section names folded into it]), ...]
BUCKETS: dict[str, list[tuple[str, list[str]]]] = {
    "agents": [
        ("Frameworks", ["Frameworks"]),
        ("Software Development", ["Software Development"]),
        ("Conversational Agents", ["Conversational / General Agents"]),
        ("Automation", ["Automation"]),
        ("Knowledge Management", ["Memory - Knowledge Management"]),
        ("Research", ["Research"]),
        ("Testing & Evaluation", ["Testing and Evaluation"]),
        ("Game & Simulation", ["Game / Simulation"]),
    ],
    "e2b": [
        ("Coding", ["Coding"]),
        ("General Purpose", ["General purpose", "Open Source"]),
        ("Build-Your-Own & Dev Tools", [
            "Build-your-own", "Build your own", "Developer tools",
            "Tool for agents", "Technical challenges of building AI products"]),
        ("Productivity & Assistants", ["Productivity", "Personal assistant"]),
        ("Data & Business Intelligence", ["Data analysis", "Business intelligence", "Finance"]),
        ("Research & Science", ["Research", "Science"]),
        ("Multi-Agent & Memory", ["Multi-agent", "Memory management"]),
        ("Creative, Sales & Other", [
            "Content creation", "Design", "Web design", "Sales", "HR",
            "Blockchain", "Uncategorised"]),
    ],
    "claudecode": [
        ("Official & Start Here", ["Start Here", "From Anthropic"]),
        ("Observability & Monitoring", ["Observability & Monitoring"]),
        ("Docs, Knowledge & Research", [
            "Documentation, Knowledge & Learning", "Research & Scientific Inquiry"]),
        ("Security", ["Security"]),
        ("Orchestration", ["Agent Orchestration"]),
        ("Memory & Context", ["Memory & Context Persistence"]),
        ("Clients & Infrastructure", [
            "Alternative Clients", "Providers, Runtime & Integration Infrastructure",
            "Infrastructure & DevOps"]),
        ("Workflow, UI & Media", [
            "Remote Control, Notifications & Voice I/O", "Design & UI/UX", "Linting",
            "Status Lines", "Skills", "Creative Media", "Writing & Prose Quality"]),
    ],
    "harness": [
        ("Foundations & Tutorials", ["Foundations", "Tutorials & Educational"]),
        ("Agent Loop & Planning", ["Agent Loop", "Planning & Task Decomposition"]),
        ("Context & Memory", ["Context Delivery & Compaction", "Memory & State"]),
        ("Tools, Skills & MCP", ["Tool Design", "Skills & MCP"]),
        ("Security & Permissions", [
            "Security, Sandbox & Permissions", "Permissions & Authorization"]),
        ("Orchestration & Human-in-the-Loop", [
            "Task Runners & Orchestration", "Human-in-the-Loop"]),
        ("Evals, Tracing & Debugging", [
            "Evals & Verification", "Verification & CI Integration",
            "Observability & Tracing", "Debugging & Developer Experience"]),
        ("Implementations & Infrastructure", [
            "Demo Harnesses", "Generators & Meta-Harnesses",
            "Production Infrastructure & Operations", "Adjacent Collections",
            "Related Awesome Lists"]),
    ],
    "agents2026": [
        ("Coding Agents", ["Coding Agents"]),
        ("Frameworks & Platforms", ["Agent Frameworks", "Multi-Agent Platforms"]),
        ("Browser, Desktop & Workflow", [
            "Browser and Desktop Agents", "Task and Workflow Agents"]),
        ("Creative & Voice", ["Creative AI", "Voice Agents"]),
        ("Data, Research & Ops", [
            "Data and Research Agents", "Observability and Evaluation",
            "Protocols and Standards"]),
        ("Support, CRM & Sales", ["Customer Support and CRM Agents"]),
        ("Local & Open Models", ["Local and Self-Hosted AI", "Open-Source Models for Agents"]),
        ("Safety, Governance & Health", [
            "AI Governance and Compliance", "AI Safety and Guardrails",
            "Cybersecurity Agents", "Healthcare and Therapy Agents"]),
    ],
    "skills": [
        ("AI Platforms & Models", ["AI Platforms & Models", "Claude and Anthropic"]),
        ("Business & Productivity", ["Business, Productivity & Marketing"]),
        ("Cloud & Infrastructure", ["Cloud & Infrastructure"]),
        ("Developer Tools & Frameworks", [
            "Developer Tools & Frameworks", "Model Context Protocol (MCP)",
            "GitHub Copilot"]),
        ("Security & Web Intelligence", ["Security & Web Intelligence"]),
        ("Community Skills", ["Community Skills"]),
        ("Google Ecosystem", ["Google Ecosystem"]),
    ],
    "llmapps": [
        ("Starter Agents", ["Starter AI Agents"]),
        ("Advanced Agents", ["Advanced AI Agents"]),
        ("Multi-Agent & Autonomous", [
            "Multi-agent Teams", "Always-on Agents", "Autonomous Game-Playing Agents"]),
        ("RAG", ["RAG (Retrieval Augmented Generation)"]),
        ("Memory & Chat-with-X", ["LLM Apps with Memory", "Chat with X"]),
        ("MCP & Skills", ["MCP AI Agents", "Agent Skills"]),
        ("Voice & Generative UI", [
            "Voice AI Agents", "Generative UI and Agentic Frontends"]),
        ("Tooling & Courses", [
            "LLM Optimization Tools", "LLM Fine-tuning",
            "AI Agent Framework Crash Courses"]),
    ],
    "opencode": [
        ("Official Repositories", ["Official Repositories"]),
        ("Plugins", ["PLUGINS"]),
        ("Agents", ["AGENTS"]),
        ("Themes", ["THEMES"]),
        ("Projects", ["PROJECTS"]),
        ("Resources", ["RESOURCES"]),
    ],
    "skills_aas": [
        ("Official Sources", ["Official Sources"]),
        ("Community Contributors", ["Community Contributors"]),
        ("Community", ["Community"]),
        ("Inspirations", ["Inspirations"]),
        ("Additional Sources", ["Additional Sources"]),
    ],
    "patterns": [
        ("Orchestration & Control", ["Orchestration & Control"]),
        ("Context & Memory", ["Context & Memory"]),
        ("Tool Use & Environment", ["Tool Use & Environment"]),
        ("Reliability & Eval", ["Reliability & Eval"]),
        ("Security & Safety", ["Security & Safety"]),
        ("Feedback Loops", ["Feedback Loops"]),
        ("UX & Collaboration", ["UX & Collaboration"]),
        ("Learning & Adaptation", ["Learning & Adaptation"]),
    ],
    # The original list already ships eight sections and its own palette order.
    "orchestrators": [
        ("Parallel Coding Agents — Terminal (TUI/CLI)", []),
        ("Parallel Coding Agents — Desktop & Web", []),
        ("Multi-Agent Swarms", []),
        ("Autonomous Loop Runners", []),
        ("Autonomous Task Runners", []),
        ("Agent Infrastructure & Primitives", []),
        ("Personal Assistants", []),
        ("Resting (no recent pushes)", []),
    ],
    "llmops_tensorchord": [
        ("Models & Fine Tuning", [
            "Large Language Model", "CV Foundation Model", "Audio Foundation Model",
            "Robotics Foundation Model", "Foundation Model Fine Tuning", "Model Editing"]),
        ("Serving & Inference", [
            "Large Model Serving", "Frameworks/Servers for Serving", "Optimizations", "ML Compiler"]),
        ("Training & AutoML", [
            "Frameworks for Training", "AutoML", "Federated ML", "Experiment Tracking"]),
        ("LLMOps Platforms", ["LLMOps", "ML Platforms"]),
        ("Search & Vector DBs", ["Vector search", "Hybrid search"]),
        ("Data & Features", [
            "Data Management", "Data Storage", "Data Tracking", "Feature Engineering",
            "Data/Feature enrichment"]),
        ("Observability, Profiling & Security", [
            "Observability", "Visualization", "Profiling", "Frameworks for LLM security"]),
        ("Deployment, Workspaces & Lists", [
            "Workflow", "Scheduling", "Model Management", "IDEs and Workspaces", "Code AI",
            "Awesome Lists"]),
    ],
    "mcp_devops_rohitg00": [
        ("Cloud & Infrastructure", [
            "Infrastructure as Code", "Container Orchestration", "Cloud Providers",
            "Database Management"]),
        ("Command Line & Version Control", ["Command Line", "Version Control"]),
        ("Security", ["Security"]),
        ("CI/CD, Build & Testing", [
            "Continuous Integration", "Mobile CI/CD", "DevOps Visibility", "Dependency Analysis",
            "Testing & Chaos Engineering", "Code Execution"]),
        ("Coding Agents & Browser Automation", ["Coding Agents", "Browser Automation"]),
        ("Aggregators & Frameworks", ["Aggregators", "Frameworks"]),
        ("Monitoring & Observability", [
            "Metrics & Monitoring", "Application Performance Monitoring",
            "Alerting & Notification", "Social Media Monitoring"]),
        ("Project, Memory & Resources", [
            "Ticketing Systems", "Project Management", "CMS & Web Platforms", "Memory & Context",
            "API Cost Management", "Related Resources"]),
    ],
    "mcp_punkpeye": [
        ("Developer Tools & Code", [
            "Developer Tools", "Coding Agents", "Version Control", "Command Line",
            "Code Execution", "Frameworks", "OS Automation"]),
        ("Data, Databases & Search", [
            "Search & Data Extraction", "Databases", "Data Platforms", "Data Science Tools",
            "Data Visualization", "end to end RAG platforms"]),
        ("Knowledge, Files & Research", [
            "Knowledge & Memory", "File Systems", "Research", "Education"]),
        ("Finance & Commerce", [
            "Finance & Fintech", "E-Commerce", "Legal", "Delivery", "Real Estate", "Cryptography"]),
        ("Cloud, Security & Monitoring", [
            "Security", "Aggregators", "Cloud Platforms", "Monitoring", "Embedded System",
            "Home Automation", "Industrial & IoT"]),
        ("Communication & Marketing", [
            "Communication", "Marketing", "Social Media", "Customer Data Platforms",
            "Support & Service Management", "Conversational AI", "Translation Services"]),
        ("Browser, Media & Creative", [
            "Browser Automation", "Art & Culture", "Gaming", "Multimedia Process",
            "Architecture & Design", "Text-to-Speech", "Podcasts", "Speech-to-Text"]),
        ("Workplace & Other Domains", [
            "Other Tools and Integrations", "Workplace & Productivity", "Travel & Transportation",
            "Location Services", "Biology, Medicine and Bioinformatics", "Sports",
            "Product Management", "Spirituality & Esoterica", "Environment & Nature",
            "Aerospace & Astrodynamics", "Agreements & Coordination", "Health & Wellness",
            "Accessibility"]),
    ],
    "aiagents_jenqyang": [
        ("Frameworks", ["Frameworks"]),
        ("Autonomous Task Solvers", ["Autonomous Agent Task Solver Projects"]),
        ("Multi-Agent & Simulation", [
            "Multi-Agent Task Solver Projects", "Agent Society Simulation"]),
        ("Tools & Components", ["Tools", "Advanced Components"]),
        ("Benchmarks & Evaluators", ["Benchmark/Evaluator"]),
        ("Platforms & APIs", ["Platforms/API"]),
        ("Papers & Surveys", ["Survey", "Paper-List Repo"]),
        ("Lists & Blogs", ["Reference Repo", "Blog"]),
    ],
    "cc_plugins": [
        ("Development & Engineering", [
            "Development Engineering", "Git Workflow", "Official Claude Code Plugins"]),
        ("Workflow Orchestration", ["Workflow Orchestration"]),
        ("Quality, Testing & Security", ["Code Quality Testing", "Security, Compliance, & Legal"]),
        ("Automation & DevOps", ["Automation DevOps"]),
        ("Business, Marketing & Product", [
            "Marketing Growth", "Project & Product Management", "Business Sales",
            "Lifestyle & Entertainment"]),
        ("Data, Docs & Knowledge", [
            "Data Analytics", "Documentation", "Knowledge Management",
            "Thinking & Knowledge Management"]),
        ("Design, Media & Integrations", [
            "Design UX", "AI & Speech", "Audio & Media", "Communication & Integrations",
            "Companion Apps & Tools"]),
        ("MCP, Skills & Marketplaces", [
            "MCP Servers", "Skills & Frameworks", "External Marketplaces", "Marketplaces",
            "Resources"]),
    ],
    "cc_subagents_voltagent": [
        ("01. Core Development", ["01. Core Development"]),
        ("02. Language Specialists", ["02. Language Specialists"]),
        ("03. Infrastructure", ["03. Infrastructure"]),
        ("04. Quality & Security", ["04. Quality & Security"]),
        ("05. Data & AI", ["05. Data & AI"]),
        ("06. Developer Experience", ["06. Developer Experience"]),
        ("07. Specialized Domains", ["07. Specialized Domains"]),
        ("Business, Meta & Research", [
            "08. Business & Product", "09. Meta & Orchestration", "10. Research & Analysis"]),
    ],
    "cc_toolkit_rohitg00": [
        ("Plugins", ["All Plugins", "Featured"]),
        ("Agents", [
            "Core Development", "Language Experts", "Infrastructure", "Quality Assurance",
            "Data & AI", "Developer Experience", "Specialized Domains", "Business & Product",
            "Orchestration", "Research & Analysis"]),
        ("Skills", ["Community Skills", "Skills", "SKY-lv Skills"]),
        ("Commands", [
            "Git", "Testing", "Architecture", "Documentation", "Security", "Refactoring",
            "DevOps", "Workflow"]),
        ("Ecosystem & Companion Apps", ["Ecosystem", "Companion Apps & GUIs"]),
        ("Hooks & MCP Configs", ["Hook Scripts", "Related SDKs", "MCP Configs"]),
        ("Rules, Contexts & Templates", ["Rules", "Contexts", "Templates"]),
        ("Docs & Examples", ["Resources", "Related Awesome Lists", "Examples"]),
    ],
    "claudecode_jq": [
        ("Official & Guides", ["Official Resources", "Guides & Learning"]),
        ("Agents & Orchestration", ["Agents & Orchestration"]),
        ("Agent Skills", ["Agent Skills"]),
        ("Plugins & IDE Integrations", ["Claude Plugins", "IDE & Editor Integrations"]),
        ("Tools & Utilities", ["Tools & Utilities"]),
        ("Clients & GUIs", ["Clients & GUIs"]),
        ("Infrastructure & SDKs", ["Infrastructure & Proxies", "SDKs & Development Kits"]),
        ("Usage & Observability", ["Usage & Observability"]),
    ],
    "codexcli": [
        ("Official & Getting Started", ["Official Resources", "Getting Started"]),
        ("Skills, Subagents & Templates", ["Skills", "Subagents", "AGENTS.md Templates"]),
        ("MCP Servers", ["MCP Servers"]),
        ("Clients, IDE & Remote", [
            "GUI & Desktop Apps", "IDE & Editor Integrations", "Remote Access", "Shell & Terminal"]),
        ("Plugins & Hooks", ["Plugins", "Hooks"]),
        ("Sessions, Providers & Automation", [
            "Session & Workflow Management", "Model Providers & Proxies", "Account & Auth",
            "Cross-Agent Tools", "CI/CD & Automation"]),
        ("Monitoring & Sandboxing", ["Monitoring & Analytics", "Docker & Sandboxing"]),
        ("Docs & Community", ["Tutorials & Articles", "Comparisons", "Community"]),
    ],
    "codingtools_a4d": [
        ("Editors & Completion", ["Code Editors and Assistants", "Code Completion"]),
        ("Agents & CLI", ["Coding Agents", "CLI Tools"]),
        ("Builders & UI", ["App Builders", "UI Generators"]),
        ("Review, Testing & QA", ["Code Review and Refactoring", "Testing and QA"]),
        ("Search, Docs & Lists", ["Code Search and Navigation", "Documentation", "Related Lists"]),
        ("Models & Local Runtimes", ["Code Models", "Local LLM Tools"]),
        ("Frameworks, MCP & Data", [
            "AI Frameworks and SDKs", "MCP Servers and Directories", "Database and API Tools"]),
        ("Productivity, DevOps & Security", [
            "Developer Productivity Tools", "DevOps and Infrastructure", "Security"]),
    ],
    "cursorrules": [
        ("Frontend & UI", [
            "Frontend Frameworks and Libraries", "CSS and Styling", "State Management"]),
        ("Backend & Data", ["Backend and Full-Stack", "Database and API"]),
        ("Language-Specific", ["Language-Specific"]),
        ("Build Tools & Development", ["Build Tools and Development"]),
        ("Testing", ["Testing"]),
        ("Mobile Development", ["Mobile Development"]),
        ("Games & Graphics", ["Games and Graphics"]),
        ("Ops, Security & Reference", [
            "Hosting and Deployments", "Security", "Documentation", "Directories"]),
    ],
    "devtools_murdza": [
        ("Development Environments", ["AI-Native IDEs", "IDE Extensions"]),
        ("Terminal", ["Terminal Agents", "CLI Utilities"]),
        ("Web-Based Tools", [
            "App Builders", "UI Generators", "Coding Agents", "Codebase Intelligence",
            "Database & SQL", "Snippet & Utility Tools"]),
        ("Desktop & Mobile", ["Desktop & Mobile Applications"]),
        ("Automated Workflows", ["PR & Code Review Bots", "CI/CD & Testing Automation"]),
        ("Agent Infrastructure", [
            "Multi-Agent Orchestration", "Sandboxing & Isolation",
            "Configuration & Context Management", "Usage Analytics & Cost Tracking"]),
        ("Specialized Tools", ["Git & Commit Helpers", "Documentation Generation"]),
        ("Resources", ["Resources"]),
    ],
    "geminicli": [
        ("Official & Forks", ["Official", "Forks"]),
        ("Commands, Extensions & Prompts", ["Commands & Extensions", "Prompts"]),
        ("MCP Servers", ["MCP Servers"]),
        ("Orchestration & Frameworks", ["Agent Orchestration & CLI Tools", "Frameworks"]),
        ("Dev Tools & Utilities", ["Development Tools & Utilities"]),
        ("Interfaces & Editor Plugins", [
            "Interfaces", "Neovim Plugins", "Browser Extensions", "Fun"]),
        ("Bridges & SDKs", ["API Bridges & Proxies", "SDKs"]),
        ("Docs & Adjacent", [
            "Documentation & Examples", "Non-Gemini CLI", "Education & Study Tools"]),
    ],
    "llmagents_kaushikb11": [
        ("Core Frameworks", ["Core Frameworks"]),
        ("Multi-Agent Orchestration", [
            "Multi-Agent Orchestration", "Autonomous Agents (2023 wave)"]),
        ("CLI Agent Harnesses", ["CLI Agent Harnesses"]),
        ("Builders & Infrastructure", ["Low-Code & Visual Builders", "Agent Infrastructure"]),
        ("Memory, Retrieval & Data", ["Memory & Context", "Retrieval & Data"]),
        ("Safety, Security & Evaluation", ["Safety, Security & Evaluation"]),
        ("Domain-Specific Agents", ["Domain-Specific Agents"]),
        ("Research & Inactive", ["Research & Experimental", "Inactive"]),
    ],
    "llmops_inftyai": [
        ("Inference Engines & Platforms", [
            "Inference Engine", "Inference Platform", "Middleware", "Simulator"]),
        ("Routers & Gateways", ["LLM Router", "AI Gateway"]),
        ("Frameworks, Tools & Output", ["Agent Framework", "Tool", "Output"]),
        ("Agents & Terminals", ["AI Terminal", "AI Agent", "Code Agent"]),
        ("Workflow & Self-Evolving", ["Workflow", "Evolutionary Framework", "Evolve Agent"]),
        ("RAG & Databases", ["RAG", "Database"]),
        ("Training & Fine-Tuning", ["Framework", "FineTune", "RLHF", "Agentic RL"]),
        ("Observability, Benchmarks & Clients", [
            "Application Framework", "Observation", "Benchmark", "Chatbot", "Sandbox"]),
    ],
    "skills_cursor_spencerpauly": [
        ("Cursor-Native", ["Cursor-Native"]),
        ("Plugins", ["Plugins"]),
        ("Code Quality & Testing", ["Code Quality & Security", "Testing"]),
        ("Frontend & Documentation", ["Frontend & UI", "Documentation"]),
        ("Workflow, Planning & Utilities", ["Workflow", "Planning & Architecture", "Utilities"]),
        ("Infrastructure & Dependencies", ["Infrastructure & DevOps", "Dependencies"]),
        ("Analytics, Auth & Monitoring", [
            "Analytics & Tracking", "Authentication & Payments", "Error Tracking & Monitoring"]),
        ("Cursor Resources", ["Cursor Rules", "Learning", "Directories", "Tools"]),
    ],
    "prompteng_promptslab": [
        ("Coding Agents", ["Vibe Coding and AI Coding Assistants"]),
        ("Frameworks & Optimizers", ["Agent Frameworks", "Prompt Optimization Tools"]),
        ("MCP", ["MCP (Model Context Protocol)"]),
        ("Autonomous Loops & Ports", [
            "General-Purpose Descendants", "Platform Ports & Hardware Forks"]),
        ("Research Agents", ["Research-Agent Systems"]),
        ("Domain Adaptations", ["Domain-Specific Adaptations"]),
        ("Prompt Evals & Security", [
            "Prompt Management and Testing", "LLM Evaluation Tools", "Evaluation & Benchmarks",
            "Red Teaming and Prompt Security"]),
        ("Guides & Collections", ["Other Notable Repositories", "Related Resources"]),
    ],
}


def bucket_map(source: str) -> dict[str, str]:
    """section name -> bucket name for one source."""
    out: dict[str, str] = {}
    for bucket, sections in BUCKETS.get(source, []):
        for s in sections:
            out[s] = bucket
    return out


def bucket_order(source: str) -> list[str]:
    return [b for b, _ in BUCKETS.get(source, [])]


def check() -> None:
    bad = [(k, len(v)) for k, v in BUCKETS.items() if len(v) > 8]
    if bad:
        raise SystemExit(f"more than eight palette slots requested: {bad}")
    for k, v in BUCKETS.items():
        names = [b for b, _ in v]
        if len(names) != len(set(names)):
            raise SystemExit(f"duplicate bucket in {k}")
    print(f"{len(BUCKETS)} sources, buckets per sheet: "
          + ", ".join(f"{k}={len(v)}" for k, v in BUCKETS.items()))


if __name__ == "__main__":
    check()
