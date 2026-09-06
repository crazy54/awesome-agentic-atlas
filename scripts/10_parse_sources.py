"""Parse every awesome-list source into one entry table.

Every list in `SOURCES` has its own shape: plain bullets, markdown tables, HTML
tables under `<h3>` headings, one-heading-per-tool, and `<details>` accordions.
Rather than a bespoke parser per list this is one walker with a small per-source
strategy: which heading level names the category, which line shapes hold
entries, and which headings are front matter to ignore. That is what has let the
list of sources grow without the parser growing with it.

Output is cache/entries_all.json -- one row per listed item per source. A repo
listed by two sources stays two rows (that overlap is itself a finding); the
fetch stage dedupes on nwo so each repo is still only hit once.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
SRC = CACHE / "sources"

# --- source strategies -----------------------------------------------------
# mode:     which line shapes carry entries -- bullet / table / heading
# cat_at:   heading depth that names the category (2 = "## ", 3 = "### ")
# drop:     headings whose whole section is front matter, meta or non-tool
# keep:     the inverse, for a list that is mostly not tools -- name the sections to take and every
#           other heading is dropped. Only one of the two per source; `keep` wins if both are given.
#           A denylist has to be complete to be correct, so it is the wrong shape for a list whose
#           upstream adds sections faster than we notice: a heading nobody has classified yet becomes
#           a live section, and an unmapped section is a taxonomy KeyError, which is a red build for a
#           change made in somebody else's repository. With `keep`, an unrecognised new heading is
#           simply not taken, which is the safe default and needs no maintenance.
# item_rel: relative links are real items (the list indexes folders in its own repo)
SOURCES = [
    dict(key="orchestrators", nwo="andyrewlee/awesome-agent-orchestrators",
         title="Agent Orchestrators", short="Orchestrators", file=None),
    dict(key="agents", nwo="kyrolabs/awesome-agents", title="AI Agents (kyrolabs)",
         short="Agents", file="kyrolabs_awesome-agents.md",
         mode={"bullet"}, cat_at=2, drop={"table of contents", "contents"}),
    dict(key="e2b", nwo="e2b-dev/awesome-ai-agents", title="AI Agents (e2b)",
         short="E2B Agents", file="e2b-dev_awesome-ai-agents.md",
         mode={"heading"}, cat_at=2, heading_cat_from="Category", cat_first_label=True,
         drop={"have anything to add?", "who's behind this?",
               "check out e2b - code interpreting for ai apps"}),
    dict(key="claudecode", nwo="hesreallyhim/awesome-claude-code",
         title="Claude Code Ecosystem", short="Claude Code",
         file="hesreallyhim_awesome-claude-code.md",
         mode={"bullet"}, cat_at=2,
         drop={"contents", "table of contents", "recently added",
               "the claude code ticker - a sample of claude code projects around github",
               "license", "contributing", "acknowledgements", "announcements"}),
    dict(key="harness", nwo="ai-boost/awesome-harness-engineering",
         title="Harness Engineering", short="Harness Eng",
         file="ai-boost_awesome-harness-engineering.md",
         mode={"bullet", "table"}, cat_at=3,
         drop={"contents", "table of contents", "license", "contributing",
               "how to use this list", "star history"}),
    # The AAS README does not inline its 2,109 skills -- it credits the upstream
    # repos they were aggregated from, under Credits & Sources. Those repos are
    # the listable content, so the h3 sources become the categories.
    dict(key="skills_aas", nwo="sickn33/agentic-awesome-skills",
         title="Agentic Skills (AAS)", short="AAS Skills",
         file="sickn33_agentic-awesome-skills.md",
         mode={"bullet", "table"}, cat_at=3,
         drop={"table of contents", "contents", "installation", "quick faq",
               "why this repo", "choose your tool", "license", "contributing",
               "aas core: agent-first preview", "verify the install",
               "repo contributors", "star history", "support the project",
               "browse 2,109+ skills", "troubleshooting", "bundles & workflows",
               "stable skills manifest v1", "recommended specialized plugins",
               "what you get in this repository", "best ways to explore",
               "compare alternatives", "start with bundles",
               "use workflows for outcome-driven execution",
               "need fewer active skills at runtime?"}),
    # Pure HTML: an outer <details><summary><strong>CATEGORY</strong> wraps one
    # inner <details> per entry, with the repo URL on a "View Repository" link.
    dict(key="opencode", nwo="awesome-opencode/awesome-opencode",
         title="Opencode Ecosystem", short="Opencode",
         file="awesome-opencode_awesome-opencode.md",
         mode={"table", "html_details"}, cat_at=3, drop={"contributing", "license"}),
    dict(key="agents2026", nwo="caramaschiHG/awesome-ai-agents-2026",
         title="AI Agents 2026", short="Agents 2026",
         file="caramaschiHG_awesome-ai-agents-2026.md",
         mode={"table"}, cat_at=2,
         drop={"contents", "table of contents", "learning resources",
               "newsletters and communities", "market stats 2026",
               "xvary stock research", "contributing", "license"}),
    dict(key="skills", nwo="heilcheng/awesome-agent-skills",
         title="Agent Skills", short="Agent Skills",
         file="heilcheng_awesome-agent-skills.md",
         mode={"bullet"}, cat_at=3,
         drop={"quick start (30 seconds)", "table of contents",
               "what are agent skills?", "how to find skills (recommended)",
               "compatible agents", "skill quality standards", "using skills",
               "creating skills", "official tutorials and guides",
               "trends & capabilities (2026)", "frequently asked questions",
               "related awesome lists", "contributing", "contact", "citation",
               "license", "when to use this skill", "instructions", "examples"}),
    dict(key="llmapps", nwo="shubhamsaboo/awesome-llm-apps",
         title="LLM App Templates", short="LLM Apps",
         file="shubhamsaboo_awesome-llm-apps.md",
         mode={"bullet"}, cat_at=3, item_rel=True,
         drop={"run one now", "thanks to our sponsors", "browse all templates",
               "contributing", "license", "star history"}),
    dict(key="patterns", nwo="nibzard/awesome-agentic-patterns",
         title="Agentic Patterns", short="Patterns",
         file="nibzard_awesome-agentic-patterns.md",
         mode={"bullet"}, cat_at=3, item_rel=True,
         drop={"what counts as a pattern?", "explore the website",
               "quick tour of categories", "for ai assistants (llms.txt)",
               "contributing in 3 steps", "inspiration", "license"}),
    dict(key="aiagents_schwoebel", nwo="jim-schwoebel/awesome_ai_agents",
         title="AI Agents (Schwoebel)", short="Schwoebel",
         file="jim-schwoebel_awesome_ai_agents.md",
         mode={"bullet"}, cat_at=3,
         drop={"agents connect: the all-demo conference", "applications", "contributing",
               "contributors", "courses", "datasets", "ethics", "license", "linkedin",
               "newsletter", "prompt engineering", "spread the word", "star the repo",
               "table of contents", "twitter", "upcoming event: agents connect conference",
               "workflows"}),
    dict(key="llmops_tensorchord", nwo="tensorchord/Awesome-LLMOps",
         title="LLMOps (tensorchord)", short="LLMOps",
         file="tensorchord_Awesome-LLMOps.md",
         mode={"table"}, cat_at=3,
         drop={"contents", "license", "table of contents"}),
    dict(key="mcp_devops_rohitg00", nwo="rohitg00/awesome-devops-mcp-servers",
         title="DevOps MCP Servers", short="DevOps MCP",
         file="rohitg00_awesome-devops-mcp-servers.md",
         mode={"bullet"}, cat_at=3,
         drop={"contributing", "legend", "license", "what is mcp?"}),
    dict(key="mcp_punkpeye", nwo="punkpeye/awesome-mcp-servers",
         title="MCP Servers (punkpeye)", short="MCP Servers",
         file="punkpeye_awesome-mcp-servers.md",
         mode={"bullet"}, cat_at=3,
         drop={"clients", "community", "legend", "server implementations", "star history",
               "tips and tricks", "tutorials", "what is mcp?"}),
    dict(key="mcp_wong2", nwo="wong2/awesome-mcp-servers",
         title="MCP Servers (wong2)", short="MCP wong2",
         file="wong2_awesome-mcp-servers.md",
         mode={"bullet"}, cat_at=2,
         drop={"sponsors"}),
    dict(key="agentic_commerce", nwo="Merit-Systems/awesome-agentic-commerce",
         title="Agentic Commerce (x402)", short="Agentic Comm",
         file="Merit-Systems_awesome-agentic-commerce.md",
         mode={"bullet"}, cat_at=3,
         drop={"benchmarks & analysis", "community", "contributing", "license",
               "podcasts & media", "quick links", "videos", "what is x402?"}),
    dict(key="aiagents_jenqyang", nwo="Jenqyang/Awesome-AI-Agents",
         title="AI Agents (Jenqyang)", short="Jenqyang",
         file="Jenqyang_Awesome-AI-Agents.md",
         mode={"bullet"}, cat_at=3,
         drop={"contents", "license", "table of contents"}),
    dict(key="cc_plugins", nwo="ccplugins/awesome-claude-code-plugins",
         title="Claude Code Plugins", short="CC Plugins",
         file="ccplugins_awesome-claude-code-plugins.md",
         mode={"bullet", "table"}, cat_at=3, item_rel=True,
         drop={"contributing", "tutorials", "use cases", "what is claude code plugin?"}),
    dict(key="cc_subagents_voltagent", nwo="VoltAgent/awesome-claude-code-subagents",
         title="Claude Code Subagents", short="CC Subagents",
         file="VoltAgent_awesome-claude-code-subagents.md",
         mode={"bullet"}, cat_at=3, item_rel=True,
         drop={"contributing", "contributor thanks", "installation", "license", "sponsors"}),
    dict(key="cc_toolkit_rohitg00", nwo="rohitg00/awesome-claude-code-toolkit",
         title="Claude Code Toolkit", short="CC Toolkit",
         file="rohitg00_awesome-claude-code-toolkit.md",
         mode={"bullet", "table"}, cat_at=3, item_rel=True,
         drop={"contributing", "license", "project structure", "quick install", "setup",
               "table of contents", "xvary stock research"}),
    dict(key="claudecode_jq", nwo="jqueryscript/awesome-claude-code",
         title="Claude Code (jqueryscript)", short="CC (jq)",
         file="jqueryscript_awesome-claude-code.md",
         mode={"bullet"}, cat_at=2,
         drop={"alternatives to claude code", "changelog", "contribution guidelines",
               "table of contents"}),
    dict(key="claws", nwo="machinae/awesome-claws",
         title="OpenClaw Assistants", short="Claws",
         file="machinae_awesome-claws.md",
         mode={"bullet"}, cat_at=2,
         drop={"contributing"}),
    dict(key="codexcli", nwo="RoggeOhta/awesome-codex-cli",
         title="Codex CLI Ecosystem", short="Codex CLI",
         file="RoggeOhta_awesome-codex-cli.md",
         mode={"bullet", "table"}, cat_at=2,
         drop={"contents", "contributing"}),
    dict(key="codingtools_a4d", nwo="ai-for-developers/awesome-ai-coding-tools",
         title="AI Coding Tools (a4d)", short="Coding Tools",
         file="ai-for-developers_awesome-ai-coding-tools.md",
         mode={"bullet"}, cat_at=2,
         drop={"table of contents"}),
    dict(key="copilot_github", nwo="github/awesome-copilot",
         title="GitHub Copilot Customizations", short="Copilot",
         file="github_awesome-copilot.md",
         mode={"bullet", "table"}, cat_at=3, item_rel=True,
         paths=["docs/README.agents.md", "docs/README.instructions.md", "docs/README.skills.md", "docs/README.plugins.md", "docs/README.hooks.md", "docs/README.workflows.md"],
         drop={"contributing", "contributors", "how to contribute", "install a plugin",
               "learning hub", "what's in this repo", "™ trademarks"}),
    dict(key="cursorrules", nwo="PatrickJS/awesome-cursorrules",
         title="Cursor Rules", short="Cursor Rules",
         file="PatrickJS_awesome-cursorrules.md",
         mode={"bullet"}, cat_at=3,
         drop={"coderabbit.ai - cut code review time & bugs in half. instantly", "contents",
               "contributing", "footnotes", "how to use", "project rules", "sponsorships",
               "unblocked mcp- supercharge cursor with your team’s knowledge",
               "warp - built for coding with multiple ai agents", "why cursor rules"}),
    dict(key="devtools_murdza", nwo="jamesmurdza/awesome-ai-devtools",
         title="AI Dev Tools (murdza)", short="AI DevTools",
         file="jamesmurdza_awesome-ai-devtools.md",
         mode={"bullet"}, cat_at=3,
         drop={"categories"}),
    dict(key="geminicli", nwo="Piebald-AI/awesome-gemini-cli",
         title="Gemini CLI Ecosystem", short="Gemini CLI",
         file="Piebald-AI_awesome-gemini-cli.md",
         mode={"bullet", "table"}, cat_at=2,
         drop={"contents", "contributing", "tada: new"}),
    dict(key="llmagents_kaushikb11", nwo="kaushikb11/awesome-llm-agents",
         title="LLM Agents (kaushikb11)", short="LLM Agents",
         file="kaushikb11_awesome-llm-agents.md",
         mode={"table"}, cat_at=2,
         drop={"contents", "license", "table of contents"}),
    dict(key="llmops_inftyai", nwo="InftyAI/Awesome-LLMOps",
         title="LLMOps (InftyAI)", short="LLMOps Infty",
         file="InftyAI_Awesome-LLMOps.md",
         mode={"bullet"}, cat_at=3,
         drop={"contents", "license", "table of contents"}),
    dict(key="skills_cursor_spencerpauly", nwo="spencerpauly/awesome-cursor-skills",
         title="Cursor Skills", short="Cursor Skill",
         file="spencerpauly_awesome-cursor-skills.md",
         mode={"bullet"}, cat_at=3, item_rel=True,
         drop={"contents", "contributing"}),
    dict(key="skills_jackyst0", nwo="JackyST0/awesome-agent-skills",
         title="Agent Skills (JackyST0)", short="JackySkills",
         file="JackyST0_awesome-agent-skills.md",
         mode={"bullet"}, cat_at=2,
         drop={"contents", "contributing", "create your own skill", "footnotes", "manual install",
               "one-click install (recommended)", "quick start", "star history", "support",
               "what are agent skills"}),
    dict(key="skills_libukai", nwo="libukai/awesome-agent-skills",
         title="Agent Skills (libukai)", short="Skills (CN)",
         file="libukai_awesome-agent-skills.md",
         mode={"bullet"}, cat_at=3,
         drop={"优质教程", "创建技能", "在 app 中安装", "在 cli 中安装", "安全审查", "安装技能", "快速入门", "支持状况", "标准结构",
               "特别致谢", "脚本与资源", "设计原则", "通用目录约定", "项目历史"}),
    dict(key="skills_voltagent", nwo="VoltAgent/awesome-agent-skills",
         title="Agent Skills (VoltAgent)", short="VoltSkills",
         file="VoltAgent_awesome-agent-skills.md",
         mode={"bullet"}, cat_at=3,
         drop={"contributing", "contributor thanks", "core skills", "cuda-q", "cuopt", "dali",
               "deepstream", "java skills", "license", "megatron-bridge", "megatron-core",
               "model-optimizer", "nemo-evaluator", "nemo-evaluator-launcher", "nemo-gym",
               "nemo-rl", "nemoclaw", "nemotron-voice-agent", "net skills", "official skills by",
               "python skills", "quality criteria", "rag", "rust skills", "security notice",
               "skill quality standards", "skills paths for other ai coding assistants",
               "sponsors", "table of contents", "tensorrt-llm", "tilegym", "typescript skills",
               "video-search-and-summarization"}),
    dict(key="vibecoding", nwo="filipecalegario/awesome-vibe-coding",
         title="Vibe Coding", short="Vibe Coding",
         file="filipecalegario_awesome-vibe-coding.md",
         mode={"bullet"}, cat_at=2,
         drop={"about the concept", "communities & job boards", "contents", "contribute",
               "news and social media"}),
    dict(key="agentsec_recon", nwo="ProjectRecon/awesome-ai-agents-security",
         title="AI Agent Security Tooling", short="Agent Sec",
         file="ProjectRecon_awesome-ai-agents-security.md",
         mode={"bullet"}, cat_at=2,
         drop={"contributing", "table of contents"}),
    dict(key="prompteng_promptslab", nwo="promptslab/Awesome-Prompt-Engineering",
         title="Prompt Engineering (promptslab)", short="Prompt Eng",
         file="promptslab_Awesome-Prompt-Engineering.md",
         mode={"bullet", "table"}, cat_at=3,
         drop={"agentic prompting and multi-agent systems", "applications of prompt engineering",
               "community and independent guides", "discord servers", "forums and platforms",
               "foundational papers (pre-2024)", "free and research detectors",
               "free platform courses", "free short courses", "github organizations",
               "how to contribute", "in-context learning", "leaderboards and meta-benchmarks",
               "leading commercial detectors", "learn prompting courses",
               "major benchmarks (2024–2026)", "major surveys", "multimodal prompting",
               "official provider guides", "other notable providers",
               "prompt and instruction datasets", "prompt compression",
               "prompt injection and security", "prompt optimization and automatic prompting",
               "reasoning advances", "red teaming and adversarial datasets", "reddit",
               "start here", "structured output and format control", "table of contents",
               "text-to-image generation", "text-to-music/audio generation",
               "university and platform courses", "videos", "watermarking approaches"}),
    # The one source in the atlas taken by allowlist. Four fifths of this list is reading, not tools:
    # 387 of its 535 links are arxiv papers, and the sixteen research sections plus the industry
    # write-ups contribute zero repos between them -- the full 22-section parse and this four-section
    # one both yield 43 distinct repos, so the 180 rows left behind are 180 arxiv pages that would
    # each cost a web screenshot and rank nowhere. What is here is worth having: `Tools & Frameworks`
    # is real installable tooling (llm-guard, NeMo-Guardrails, garak, promptfoo, rebuff) and it is the
    # best single source the atlas has for Sandbox, Security & Governance.
    #
    # `keep` rather than `drop` because of how this list is maintained: its papers carry 2026 arxiv
    # IDs and new h3 subsections appear under Attack Research and Defense Research weekly. Enumerated
    # as a denylist, every one of those would arrive as an unmapped section and break the build until
    # someone added it -- a red daily build caused by somebody else editing their own README. Named
    # the other way round, the four shelves we want are the four we get, for ever.
    dict(key="skills_security", nwo="LLMSecurity/awesome-agent-skills-security",
         title="Agent Skill Security", short="Skill Sec",
         file="LLMSecurity_awesome-agent-skills-security.md",
         mode={"bullet", "table"}, cat_at=3,
         keep={"tools & frameworks", "benchmarks & datasets",
               "agent skill specifications", "related awesome lists"}),
]

MD_H = re.compile(r"^(#{2,4})\s+(?P<txt>.+?)\s*#*$")
HTML_H = re.compile(r"^\s*<h(?P<lvl>[1-6])[^>]*>(?P<txt>.*?)</h\1>", re.I)
SUMMARY = re.compile(r"<summary>(?P<txt>.*?)</summary>", re.I | re.S)
BULLET = re.compile(r"^\s*[-*+]\s+(?P<body>.+)$")
TABLE_ROW = re.compile(r"^\s*\|(?P<body>.+)\|\s*$")
LINK = re.compile(r"\[(?P<txt>(?:[^\[\]]|\[[^\]]*\])*)\]\((?P<url>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
GH = re.compile(r"^https?://(?:www\.)?github\.com/(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)/"
                r"(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?(?P<rest>[/#?].*)?$")
# github.com paths that are not a repository
GH_RESERVED = {"features", "topics", "collections", "sponsors", "orgs", "about",
               "pricing", "marketplace", "apps", "settings", "explore", "trending",
               "readme", "login", "join", "security", "customer-stories", "enterprise"}


def source_path(src: dict) -> Path:
    """Where this source's pulled Markdown lives.

    The orchestrators list is the collection's own origin and is parsed by 01_parse.py, which has
    always read it from cache/README.md; every other list is a file under cache/sources/. Both are
    written by pull_sources.py, so this is the one answer both stages ask rather than two that could
    drift apart.
    """
    return CACHE / "README.md" if not src.get("file") else SRC / src["file"]


def source_paths(src: dict) -> list[Path]:
    """Every file this source's content lives in, primary first.

    Most lists are one README. A few keep their items in sub-documents behind a hub README --
    github/awesome-copilot has 3 rows in its README and 948 across six files under docs/ -- and
    `paths` names those. They land beside the primary file so one source stays one group on
    disk, and pull_sources.py pulls exactly this set: where an extra file goes is decided once,
    here, rather than by two functions free to disagree about it.
    """
    primary = source_path(src)
    out = [primary]
    for p in src.get("paths") or []:
        flat = p.strip("/").replace("/", "__")
        out.append(primary.with_name(f"{primary.stem}__{flat}{primary.suffix}"))
    return out


def read_source(src: dict) -> str:
    """One source is one text, however many files it arrived in.

    Concatenating rather than parsing each file separately is what keeps a hub list's sections in
    one namespace: `paths` files continue the heading structure the README started, and a section
    is `(source key, section name)` no matter which file the heading was written in.
    """
    return "\n\n".join(p.read_text(encoding="utf-8") for p in source_paths(src) if p.exists())


def url_key(url: str) -> str:
    """The identity of a listed entry. Two links to the same target are one entry.

    Used to dedupe within a source here, and by pull_sources.py to decide which entries a source
    added or changed between two commits -- so both must agree on what "the same entry" means.
    """
    return url.strip().lower().rstrip("/")


def clean(s: str) -> str:
    s = IMG.sub("", s or "")
    s = LINK.sub(lambda m: m.group("txt"), s)
    s = HTML_TAG.sub("", s)
    s = s.replace("**", "").replace("`", "")
    # `\|` is a backslash escape, and CommonMark renders it as a bare pipe wherever it appears. It
    # reaches us because `entry_links` splits table rows on unescaped pipes only -- correct, and it
    # deliberately leaves the escape in the cell -- but past that split the cell is no longer a table
    # row and the backslash is not syntax any more, it is a character in a description. Two rows of
    # rohitg00/awesome-claude-code-toolkit carry one: an install line reading
    # `curl ... \| bash`, and a description of shell operators reading `(&&, \|\|, ;, \|, $())`.
    # 17_markdown re-escapes on the way into its own tables, so the round trip is unchanged; what
    # this fixes is those two strings printing a literal backslash on a bullet line and in
    # docs/data.json, and `check_markdown.py`'s "escaped pipe outside a table" failing the build now
    # that both workflows run it.
    s = s.replace("\\|", "|")
    return re.sub(r"\s+", " ", s).strip(" \t*-–—:;.")


def repo_of(url: str) -> tuple[str, str, str] | None:
    """(owner, repo, subpath) for a GitHub URL, or None if it isn't a repo."""
    m = GH.match(url.rstrip("/"))
    if not m:
        return None
    owner, repo = m.group("owner"), m.group("repo")
    if owner.lower() in GH_RESERVED or not repo or repo in (".", ".."):
        return None
    rest = (m.group("rest") or "").lstrip("/")
    return owner, repo, rest


def entry_links(body: str, mode: set[str], kind: str) -> list[tuple[str, str, str]]:
    """(name, url, description) for each entry on one line."""
    if kind == "table":
        # Not a plain split: an escaped `\|` inside a cell is content, and tearing the cell in two
        # there hands the description the tail of a regex. One row in a thousand, but the row reads
        # as gibberish when it happens.
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", body)]
        if len(cells) < 2:
            return []
        # The linked cell is the entry wherever the curator put it. Requiring column 0 silently
        # dropped every row of a `| Human Name | [file.md](path) | Purpose |` table -- six such
        # tables in rohitg00/awesome-claude-code-toolkit, 225 rows -- because the readable name and
        # the link are in different columns. Purely additive for the tables that do lead with a
        # link: the first linked cell of those is still column 0.
        i = next((j for j, c in enumerate(cells) if LINK.search(c)), None)
        if i is None:
            return []
        m = LINK.search(cells[i])
        # When the link sits in a later column, column 0 is the name a person wrote and the link text
        # is the file it points at. Preferring the link text there named 225 rows "commit.md" and
        # "fullstack-engineer.md"; the table already says Commands and Core Development beside them.
        name = clean(cells[0]) if i and clean(cells[0]) else clean(m.group("txt"))
        # Every cell that is neither the name nor the link is a description candidate, on both sides
        # of the link. Reading only the cells after it assumed the link comes before the prose, and
        # `| Name | Description | Link |` puts it last: 133 of promptslab/Awesome-Prompt-Engineering's
        # 218 rows arrived with no description at all, their prose sitting one column to the left of
        # where the rule looked. Longest of the candidates, not the first non-empty one -- a table
        # with a Language or Stars column between the name and the prose used to describe LangChain
        # as "Py/JS" and a 5,300-star plugin as "5,300+"; the description is the cell with the
        # sentence in it, and that argument never depended on which side of the link it sat.
        rest = [clean(c) for j, c in enumerate(cells) if j != i and not (j == 0 and i)]
        return [(name, m.group("url"), max(rest, key=len) if any(rest) else "")]

    # bullet: first link is the entry, the rest of the line is its description
    m = LINK.search(body)
    if not m:
        return []
    desc = clean(body[m.end():])
    return [(clean(m.group("txt")), m.group("url"), desc)]


SUM_ANY = re.compile(r"<summary>(?P<inner>.*?)</summary>", re.I | re.S)
STRONG = re.compile(r"<strong>(?P<txt>.*?)</strong>", re.I | re.S)
BOLD = re.compile(r"<b>(?P<txt>.*?)</b>", re.I | re.S)
ITALIC = re.compile(r"<i>(?P<txt>.*?)</i>", re.I | re.S)
HREF_GH = re.compile(r"href=\"(?P<url>https?://(?:www\.)?github\.com/[^\"]+)\"", re.I)
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF←-⇿⌀-➿⬀-⯿️‍]+")


def strip_emoji(s: str) -> str:
    return re.sub(r"\s+", " ", EMOJI.sub("", s or "")).strip(" -–—:")


# A legend, not prose. Several lists encode facts in emoji immediately after the entry's link --
# punkpeye writes "📇 ☁️ 🏠 🍎 🪟 🐧 - Contract validation..." for language, scope and OS -- and since
# the description is everything after the link, the whole run lands at the front of it. Those glyphs
# only mean anything beside that one list's key, so in a column that shows all the lists together
# they are noise ahead of the sentence the reader wants. Leading only: an emoji mid-sentence is the
# author writing, and `strip_emoji` is not used here for that reason.
DESC_LEAD = re.compile(r"^(?:" + EMOJI.pattern + r"|[\s\-–—:|])+")

# "Language Experts (25 agents)" is the same shelf as "Language Experts (26 agents)", but a section
# name is a taxonomy.SECTIONS key and that lookup is deliberately exact, so the day upstream adds one
# agent the build dies on a heading nobody renamed. rohitg00/awesome-claude-code-toolkit writes the
# count into 18 of its 34 headings and two of them are already wrong -- "(15 agents)" over 16 rows --
# so this is drift in progress, not a hypothetical. Normalising the lookup's input is not the keyword
# matching taxonomy.py refuses: a real rename still raises, only the tally stops counting as one.
# Three digits at most, because four is a year and a year is curation: kaushikb11 separates
# "Autonomous Agents (2023 wave)" from the current crop on purpose, and no shelf holds 2,023 items.
COUNT_IN_HEAD = re.compile(r"\s*\(\d{1,3}\s+\w+\)$")


def parse_html_details(src: dict, text: str | None = None) -> list[dict]:
    """Entries encoded as nested <details> accordions rather than list items.

    <summary><strong>X</strong> marks a category; <summary><b>owner/repo</b>
    marks an entry, whose URL is the github.com href in the block that follows.
    """
    text = read_source(src) if text is None else text
    marks = list(SUM_ANY.finditer(text))
    rows: list[dict] = []
    category = ""
    for i, m in enumerate(marks):
        inner = m.group("inner")
        st = STRONG.search(inner)
        if st and not BOLD.search(inner):
            category = strip_emoji(clean(st.group("txt")))
            continue
        bd = BOLD.search(inner)
        if not bd:
            continue
        name = clean(bd.group("txt"))
        it = ITALIC.search(inner)
        desc = clean(it.group("txt")) if it else ""
        # search only up to the next summary so a link can't be stolen
        stop = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        gh = HREF_GH.search(text, m.end(), stop) or HREF_GH.search(inner)
        if not gh:
            continue
        rows.append({"_name": name.split("/")[-1] if "/" in name else name,
                     "_url": gh.group("url"), "_desc": desc,
                     "_cat": category or "Uncategorised", "_sub": ""})
    return rows


def parse(src: dict, text: str | None = None) -> list[dict]:
    """Entries for one source. `text` overrides the cached file, which is how pull_sources.py
    parses a source's previous *and* current commit through this same parser to diff them."""
    text = read_source(src) if text is None else text
    mode = src.get("mode", {"bullet"})
    cat_at = src.get("cat_at", 2)
    drop = {d.lower() for d in src.get("drop", ())}
    keep = {k.lower() for k in src.get("keep", ())}

    def is_dropped(txt: str) -> bool:
        """Whether this heading's section is skipped. Emoji stripped because headings carry them
        and both key sets are written plain."""
        plain = strip_emoji(txt).lower()
        return plain not in keep if keep else plain in drop

    rows: list[dict] = []
    heads: dict[int, str] = {}
    category = sub = ""
    dropped = False
    pending_cat = None  # e2b: "### Category" then the value on a later line

    lines = text.splitlines()
    for i, raw in enumerate(lines):
        line = raw.rstrip()

        # --- headings, markdown or HTML ---------------------------------
        lvl = txt = None
        mh = MD_H.match(line)
        if mh:
            lvl, txt = len(mh.group(1)), clean(mh.group("txt"))
        else:
            hh = HTML_H.match(line)
            if hh:
                lvl, txt = int(hh.group("lvl")), clean(hh.group("txt"))

        if lvl is not None:
            # entry-per-heading lists (e2b): the heading itself is the item
            if "heading" in mode and lvl == cat_at and LINK.search(mh.group("txt") if mh else line):
                m = LINK.search(mh.group("txt") if mh else line)
                heads[lvl] = clean(m.group("txt"))
                dropped = is_dropped(clean(m.group("txt")))
                if not dropped:
                    rows.append({"_name": clean(m.group("txt")), "_url": m.group("url"),
                                 "_desc": "", "_cat": "", "_sub": ""})
                pending_cat = None
                continue

            heads[lvl] = txt
            for deeper in [k for k in heads if k > lvl]:
                heads.pop(deeper)
            if lvl <= cat_at:
                dropped = is_dropped(txt)
            category = heads.get(cat_at, "") or txt
            sub = heads.get(cat_at + 1, "")
            if "heading" in mode and txt.lower() == src.get("heading_cat_from", "").lower():
                pending_cat = "await"
            else:
                pending_cat = None
            continue

        if dropped:
            continue

        # e2b: the line after "### Category" is the tool's category
        if pending_cat == "await" and line.strip():
            val = clean(line)
            if val and rows:
                rows[-1]["_cat"] = val
            pending_cat = None
            continue

        # --- <summary> inside <details> acts as a sub-heading ------------
        ms = SUMMARY.search(line)
        if ms:
            sub = clean(ms.group("txt"))
            continue

        if "heading" in mode:
            # The heading's own link is often the product site; the GitHub repo
            # lives in the entry's "Links" block. Prefer the repo when both exist.
            if rows and heads.get(cat_at + 1, "").lower() == "links":
                mb = BULLET.match(line)
                if mb:
                    for lm in LINK.finditer(mb.group("body")):
                        cand = lm.group("url")
                        if repo_of(cand) and not repo_of(rows[-1]["_url"]):
                            rows[-1]["_site"] = rows[-1]["_url"]
                            rows[-1]["_url"] = cand
                            break
            continue

        mb = BULLET.match(line)
        mt = TABLE_ROW.match(line)
        if mb and "bullet" in mode:
            found = entry_links(mb.group("body"), mode, "bullet")
        elif mt and "table" in mode:
            found = entry_links(mt.group("body"), mode, "table")
        else:
            continue

        for name, url, desc in found:
            rows.append({"_name": name, "_url": url, "_desc": desc,
                         "_cat": category, "_sub": sub})

    if "html_details" in mode:
        rows += parse_html_details(src, text)
    return finalise(src, rows)


def finalise(src: dict, rows: list[dict]) -> list[dict]:
    """Resolve links to repos/websites, drop anchors and noise, dedupe."""
    out: list[dict] = []
    seen: set[str] = set()
    base = f"https://github.com/{src['nwo']}"
    for r in rows:
        url, name = r["_url"].strip(), r["_name"].strip()
        if not name or not url or url.startswith("#"):
            continue
        if len(name) > 80:
            continue

        rel = not url.startswith("http")
        if rel:
            if not src.get("item_rel"):
                continue
            # a folder inside the list's own repo -- the item *is* that folder
            path = url.lstrip("./").rstrip("/")
            url = f"{base}/tree/HEAD/{path}"

        rp = repo_of(url)
        if rp:
            owner, repo, subpath = rp
            nwo = f"{owner}/{repo}"
            # a link into a repo's tree/blob is an item *within* that repo
            is_sub = bool(subpath) and not subpath.startswith(("releases", "issues", "wiki"))
            kind = "subpath" if is_sub else "repo"
            website = ""
        else:
            owner = repo = nwo = ""
            kind = "site"
            website = url
            subpath = ""

        key = url_key(url)
        if key in seen:
            continue
        seen.add(key)

        cat = COUNT_IN_HEAD.sub("", strip_emoji(r["_cat"])) or "Uncategorised"
        if src.get("cat_first_label"):
            # e2b tags each tool with a free-text comma list ("Coding, GitHub,
            # Multi-agent"). Left-most tag is the primary one; taking it whole
            # would yield 109 one-row "categories".
            cat = re.split(r"\s*[,/]\s*", cat)[0]
            cat = re.sub(r"\s*\(.*", "", cat).strip()
            cat = cat[:1].upper() + cat[1:] if cat else "Uncategorised"

        out.append({
            "source": src["key"],
            "source_nwo": src["nwo"],
            "name": name,
            "url": url,
            "kind": kind,
            "owner": owner,
            "repo": repo,
            "nwo": nwo,
            "subpath": subpath,
            "website": website or r.get("_site", ""),
            "category": cat,
            "sub_category": strip_emoji(r["_sub"]),
            "description": DESC_LEAD.sub("", r["_desc"])[:400],
        })
    return out


def main() -> None:
    # This stage reads the lists, it does not fetch them. Missing content used to surface as a bare
    # FileNotFoundError on whichever source happened to be first, which says nothing about the cause:
    # cache/ is not committed, so a cold clone or an Actions cache that did not restore has none of it.
    # Every file, not just the primary: read_source concatenates whatever is present, so a source
    # whose sub-documents did not restore would otherwise parse quietly as a much shorter list.
    absent = [src for src in SOURCES
              if src.get("file") and not all(p.exists() for p in source_paths(src))]
    if absent:
        names = ", ".join(s["key"] for s in absent)
        sys.exit(f"no cached content for {len(absent)}/{len(SOURCES)} sources ({names}).\n"
                 f"Run `python scripts/pull_sources.py` first -- it pulls each list at its head "
                 f"commit into {SRC.relative_to(ROOT).as_posix()}/.")

    all_rows: list[dict] = []
    print(f"{'source':14s} {'rows':>5s} {'repo':>5s} {'sub':>5s} {'site':>5s}  categories")
    for src in SOURCES:
        if not src["file"]:
            continue
        rows = parse(src)
        for i, r in enumerate(rows, start=1):
            r["src_order"] = i
        all_rows += rows
        cats = {}
        for r in rows:
            cats[r["category"]] = cats.get(r["category"], 0) + 1
        kinds = {k: sum(1 for r in rows if r["kind"] == k) for k in ("repo", "subpath", "site")}
        print(f"{src['key']:14s} {len(rows):5d} {kinds['repo']:5d} {kinds['subpath']:5d} "
              f"{kinds['site']:5d}  {len(cats)} cats")
        for c, n in sorted(cats.items(), key=lambda kv: -kv[1]):
            print(f"                 {n:4d}  {c[:70]}")

    out = CACHE / "entries_all.json"
    out.write_text(json.dumps(all_rows, indent=1, ensure_ascii=False), encoding="utf-8")
    repos = {r["nwo"] for r in all_rows if r["nwo"]}
    print(f"\n{len(all_rows)} rows -> {out}")
    print(f"{len(repos)} distinct GitHub repos to fetch")
    unmapped(all_rows)


def unmapped(rows: list[dict]) -> None:
    """Fail here, on the section names, rather than thousands of repo fetches later.

    Two things every later stage assumes and neither checks while checking is still cheap.
    `taxonomy.category_of` is a hard `SECTIONS[...]` lookup, so one heading a curator renamed
    upstream is a KeyError raised after the fetch stage has spent an hour; `buckets.check` only
    counts the map it was handed, so a source with nine sections and no map at all passes it and
    then asks an eight-hue palette for nine hues. Both are decisions a person has to make by hand,
    so the useful thing to print is exactly which ones are outstanding.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    import buckets as buck  # noqa: E402
    import taxonomy as tax  # noqa: E402

    pairs = {(r["source"], r["category"]) for r in rows}
    missing = sorted(f"({k!r}, {sec!r})" for k, sec in pairs - set(tax.SECTIONS))

    over = []
    for src in SOURCES:
        secs = {sec for k, sec in pairs if k == src["key"]}
        if not secs:
            continue
        fold = buck.bucket_map(src["key"])
        slots = {fold.get(s, s) for s in secs}
        if len(slots) > 8:
            over.append(f"{src['key']}: {len(secs)} sections fold to {len(slots)} buckets")

    if missing:
        print(f"\n{len(missing)} sections no category is named for -- add each to "
              f"taxonomy.SECTIONS:", file=sys.stderr)
        for m in missing:
            print(f"  {m}: ...", file=sys.stderr)
    if over:
        print(f"\n{len(over)} sources want more than the eight palette hues -- give each a "
              f"buckets.BUCKETS map:", file=sys.stderr)
        for o in over:
            print(f"  {o}", file=sys.stderr)
    if missing or over:
        sys.exit(1)
    print("every section is named by taxonomy.SECTIONS and folds into <= 8 buckets")


if __name__ == "__main__":
    main()
