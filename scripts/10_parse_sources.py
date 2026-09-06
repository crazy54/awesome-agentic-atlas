"""Parse every awesome-list source into one entry table.

Eleven lists, eleven shapes: plain bullets, markdown tables, HTML tables under
`<h3>` headings, one-heading-per-tool, and `<details>` accordions. Rather than
eleven bespoke parsers this is one walker with a small per-source strategy:
which heading level names the category, which line shapes hold entries, and
which headings are front matter to ignore.

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


def read_source(src: dict) -> str:
    return source_path(src).read_text(encoding="utf-8")


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
        cells = [c.strip() for c in body.split("|")]
        if len(cells) < 2 or not LINK.search(cells[0]):
            return []
        m = LINK.search(cells[0])
        desc = next((clean(c) for c in cells[1:] if clean(c)), "")
        return [(clean(m.group("txt")), m.group("url"), desc)]

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
                dropped = strip_emoji(clean(m.group("txt"))).lower() in drop
                if not dropped:
                    rows.append({"_name": clean(m.group("txt")), "_url": m.group("url"),
                                 "_desc": "", "_cat": "", "_sub": ""})
                pending_cat = None
                continue

            heads[lvl] = txt
            for deeper in [k for k in heads if k > lvl]:
                heads.pop(deeper)
            if lvl <= cat_at:
                # headings carry emoji prefixes; drop keys are written plain
                dropped = strip_emoji(txt).lower() in drop
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

        cat = strip_emoji(r["_cat"]) or "Uncategorised"
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
            "description": r["_desc"][:400],
        })
    return out


def main() -> None:
    # This stage reads the lists, it does not fetch them. Missing content used to surface as a bare
    # FileNotFoundError on whichever source happened to be first, which says nothing about the cause:
    # cache/ is not committed, so a cold clone or an Actions cache that did not restore has none of it.
    absent = [src for src in SOURCES if src.get("file") and not source_path(src).exists()]
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


if __name__ == "__main__":
    main()
