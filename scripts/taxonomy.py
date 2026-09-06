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
this module exists to make deliberate.

A rename therefore has to be noticed. It is `category_of()` that notices -- it raises on a section this
module does not name, and its message says what to do about it. `check()` asks the same question over a
whole record set and reads better, but be clear about its standing: nothing calls it. It runs when
somebody types `python scripts/taxonomy.py`, so it is a thing to reach for while curating, not a guard.
The guard is the raise.
"""
from __future__ import annotations

import difflib
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
    # Renamed upstream to `Memory - Knowledge Management` (2026-09). The old spelling is kept rather than
    # replaced: `check()` below is a one-way set difference, so a key no source produces any more costs
    # nothing and is never reported, while dropping it would break a re-parse of any cache fetched before
    # the rename. Both spellings fold into the same bucket in `buckets.py`.
    ("agents", "Knowledge Management"): "Context, Memory & RAG",
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
}

# The second axis: what a thing plugs into. Matched on text because no curator has a column for it --
# `("skills", "GitHub Copilot")` is the only section in 140 that names a harness. Order is display
# order. Each pattern is deliberately narrow: a false positive here puts a repo on a leaderboard it has
# no business being on, which is worse than missing one.
TARGETS: list[tuple[str, str]] = [
    ("Claude Code", r"claude[\s_.-]?code|\bclaude-?code\b|\bcchooks?\b"),
    ("Claude / Anthropic", r"\banthropic\b|\bclaude\b|agent skills?\b|\bskills?\.md\b"),
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
    """The category for one *listing*. A repo listed twice has two of these; see `by_repo`.

    Unmapped sections raise, deliberately: a section this module does not name must not be guessed at,
    for the reason in the module docstring. The subscript below already did that on its own -- the point
    of the handler is the message. What it used to produce was
    `KeyError ('agents', 'Memory - Knowledge Management')`, which named neither the file to edit nor the
    second file that also has to change and fails quietly. This is the failure a rename actually reaches,
    so this is where the instructions belong.
    """
    key = (source_of(rec), rec.get("section") or rec.get("category") or "")
    if key in SPLIT_BY_EVIDENCE and _is_mcp_server(rec):
        return "MCP Servers"
    try:
        return SECTIONS[key]
    except KeyError:
        near = difflib.get_close_matches(key[1], [s for (m, s) in SECTIONS if m == key[0]], n=3, cutoff=0.4)
        raise KeyError(
            f"{key[0]} / {key[1]!r} is not named in SECTIONS -- a curator renamed or added a section "
            f"upstream. "
            f"Closest already mapped: {near or 'nothing similar'}. Two files need it, and the second one "
            f"fails quietly: add the key to SECTIONS in scripts/taxonomy.py, then fold the new spelling "
            f"into that source's existing bucket in scripts/buckets.py. Skipping the second step leaves "
            f"the section unmapped there, and an unmapped section keeps its own name as its bucket -- "
            f"which asks the eight-hue palette for a ninth colour without buckets.check() objecting."
        ) from None


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
