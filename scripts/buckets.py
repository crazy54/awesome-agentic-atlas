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
        # Two spellings of one section: renamed upstream to `Memory - Knowledge Management` (2026-09).
        # Both are folded here on purpose. A section absent from this map keeps its own name as its
        # bucket, so listing only the new spelling would give this eight-bucket sheet a ninth that the
        # palette has no hue for -- the docstring's rule breaking quietly rather than loudly.
        ("Knowledge Management", ["Knowledge Management", "Memory - Knowledge Management"]),
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
