"""Write the GitHub-ready Markdown edition of the merged list.

Same data as the workbooks, same ordering, same verdicts -- this module imports 16_build_all rather
than re-deriving any of it, because a Markdown page that disagreed with the spreadsheet next to it
would be worse than not having one.

Layout, under mega-list/:
  README.md              the hub: counts, every source list credited, a gallery, how to read it
  platforms/*.md         windows / macos / linux / docker, one row per repo, evidence-ordered
  lists/*.md             one file per source list, grouped by the section wording it publishes
  leaderboard.md         the most-starred projects across every list at once

Two things are deliberately different from the workbook. Images are hotlinked rather than embedded
-- a README banner where the pipeline found one, GitHub's own social card otherwise, which exists
for every repo and costs this directory no bytes. And each page is split so no file approaches the
size at which GitHub stops rendering Markdown: the mega list is one list, not one file.
"""
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
OUT = ROOT / "mega-list"

spec = importlib.util.spec_from_file_location("b16", Path(__file__).parent / "16_build_all.py")
b16 = importlib.util.module_from_spec(spec)
sys.modules["b16"] = b16
spec.loader.exec_module(b16)

# Registered as "b16" above, which is the name `taxonomy.load` looks for, so importing it here cannot
# load a second copy of the pipeline. `load` itself goes unused: it reads the record files raw, and the
# records in this module have been through `prepare`, so only the classifiers are wanted.
sys.path.insert(0, str(Path(__file__).parent))
import taxonomy as tax  # noqa: E402
import newness  # noqa: E402

SHEETS, PLATFORMS, DASH = b16.SHEETS, b16.PLATFORMS, b16.DASH


REPO = "crazy54/awesome-agentic-atlas"
SITE = f"https://{REPO.split('/')[0]}.github.io/{REPO.split('/')[1]}/"


def site(**filters) -> str:
    """A deep link into the Pages site, with filters already applied.

    The site reads every filter out of the URL hash, and the slugs it expects are the slugs that name
    these files — `fileslug`, one function, both places. So `topics/agent-skills.md` and
    `#topic=agent-skills` are the same view of the same data. It is the only one of the three surfaces
    that can hold both axes at once without Excel, which is why every facet page links into it.
    """
    q = "&".join(f"{k}={v}" for k, v in filters.items() if v)
    return SITE + (f"#{q}" if q else "")


def book(depth: int, theme: str) -> str:
    """Where to download a workbook. Absolute, so `depth` no longer matters — kept for the call sites.

    These used to be relative paths, because the workbooks sat one level above mega-list/. They are
    release assets now: a pair is ~81 MB, every rebuild writes a new pair, and git keeps every version
    for ever, so three rebuilds would mean a quarter-gigabyte clone for two files only the newest of
    which anyone wants. `releases/latest/download/` resolves to the current release's asset by name,
    so the link needs no version in it and never needs editing.

    The cost is that these 404 until the first release is cut. That is `gh release create`, not a code
    change, so it is the one link in the collection that publishing has to catch up with.
    """
    return f"https://github.com/{REPO}/releases/latest/download/{b16.WORKBOOK}-{theme}.xlsx"

# tiers whose shot_url is a real image we can hotlink. "capture" holds the page URL, not an image,
# and "card"/"cached" were rendered locally, so both fall through to the GitHub social card.
LINKABLE = {"readme", "readme-loose", "readme-sub", "og", "repo-card"}

ORCH_NWO = "andyrewlee/awesome-agent-orchestrators"
ORCH_BLURB = ("The original list this workbook grew from: tools that run several coding agents at "
              "once.")


# ------------------------------------------------------------------ formatting
def cached(name: str, default=dict):
    """A cache file, or an empty one. Used only for the screenshot maps.

    Every other file this stage reads is a hard dependency -- without records there is nothing to write.
    Screenshots are different: `image()` already falls back to GitHub's Open Graph card for the two
    thirds of rows that have no captured shot, so an absent map degrades to "every row uses its card"
    rather than to a crash. That is what lets the daily job rebuild the site and the Markdown without
    running the four-hour capture stage, and lets a fresh clone render both with nothing fetched.
    """
    path = CACHE / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default()


def slug(text: str) -> str:
    """GitHub's own heading-anchor rule: lowercase, drop punctuation, spaces to hyphens.

    Deliberately not a tidy slugifier. GitHub leaves the gap where it removed a character, so
    "Conversational / General Agents" anchors as `conversational--general-agents` with two hyphens,
    and collapsing them would produce a link that renders fine and goes nowhere. The same rule
    names the files, where it happens to give the tidy answer anyway.
    """
    out = re.sub(r"[^\w\- ]", "", text.strip().lower(), flags=re.UNICODE)
    return out.replace(" ", "-")


def norm(text, limit: int = 0) -> str:
    """One line, optionally shortened. No escaping — that depends on where the text lands."""
    out = re.sub(r"\s+", " ", str(text or "")).strip()
    if limit and len(out) > limit:
        out = out[: limit - 1].rstrip(" ,;:.") + "…"
    return out


def prose(text, limit: int = 0, table: bool = False) -> str:
    """Human text. `<` and `&` become entities so a description cannot open an HTML tag."""
    out = norm(text, limit).replace("&", "&amp;").replace("<", "&lt;")
    return out.replace("|", "\\|") if table else out


def stars(rec) -> str:
    n = rec.get("stars") or 0
    if rec.get("stars_kind", "own") != "own" or n <= 0:
        return DASH
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def code(text, table: bool = False) -> str:
    """A command, verbatim inside a code span.

    No entity escaping in here: a code span shows its bytes, so `&amp;` would render as `&amp;`
    rather than as the `&&` the command actually contains. Pipes are the one exception, and only
    inside a table — GFM resolves `\\|` before it looks for code spans, so the escape is required
    there and would print as a stray backslash anywhere else.
    """
    out = norm(text)
    if not out or out == DASH:
        return DASH
    return f"`{out.replace('|', chr(92) + '|') if table else out}`"


def support(rec) -> str:
    """The five platform verdicts as one compact string, ? marking an inferred one."""
    marks = []
    for label, key in (("Win", "win_native"), ("WSL2", "win_wsl2"), ("macOS", "macos"),
                       ("Linux", "linux"), ("Docker", "docker")):
        v = rec.get(key)
        if v == "Yes":
            marks.append(label)
        elif v == "Likely":
            marks.append(f"{label}?")
    return " · ".join(marks) or DASH


def image(rec, shots) -> str:
    info = shots.get(rec.get("shot_key") or "", {})
    url = (info.get("shot_url") or "").strip()
    if url and (info.get("tier") or "") in LINKABLE:
        if url.startswith("opengraph.githubassets.com"):
            url = "https://" + url
        if url.startswith("http"):
            return url
    if rec.get("nwo"):
        return f"https://opengraph.githubassets.com/1/{rec['nwo']}"
    return ""


def gallery(rows, shots, cols: int = 3) -> list[str]:
    """A picture grid as a headerless table, because that is the only grid Markdown has."""
    picks = [r for r in rows if image(r, shots)][: cols * 2]
    if not picks:
        return []
    out = ["| " + " | ".join([" "] * cols) + " |", "|" + "---|" * cols]
    for i in range(0, len(picks), cols):
        chunk = picks[i : i + cols]
        shot = [f'<a href="{r["url"]}"><img src="{image(r, shots)}" width="260"></a>'
                for r in chunk]
        name = [f'**[{prose(r["name"], table=True)}]({r["url"]})**<br>★ {stars(r)}' for r in chunk]
        pad = [" "] * (cols - len(chunk))
        out.append("| " + " | ".join(shot + pad) + " |")
        out.append("| " + " | ".join(name + pad) + " |")
    return out + [""]


def footer(depth: int = 0) -> list[str]:
    """`depth` is how many directories below mega-list/ the page lives, for the workbook links."""
    return ["", "---", "",
            f"Snapshot {date.today().isoformat()}. Stars, language, licence and last-push come from "
            "the GitHub API and drift daily.",
            "",
            f"The same data with screenshots embedded, filterable, is in the workbooks: "
            f"[dark]({book(depth, 'DARK')}) · [light]({book(depth, 'LIGHT')}). "
            f"Or filter it in the browser on the [Atlas site]({site()}).", ""]


def write(rel: str, lines: list[str]) -> Path:
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


# ------------------------------------------------------------------ per-list pages
def list_page(title: str, nwo: str, blurb: str, rows, shots) -> list[str]:
    """One source list, grouped by the section wording that list publishes.

    Sections keep their original names rather than the workbook's eight colour buckets: on a page
    there is no palette to run out of, so folding them would lose wording for nothing.
    """
    order: dict[str, tuple] = {}
    for i, r in enumerate(rows):
        order.setdefault(r["section"], (i, r["section"]))
    sections = [name for name, _k in sorted(order.items(), key=lambda kv: kv[1])]

    lines = [f"# {title}",
             "",
             f"{blurb}",
             "",
             f"Curated by **[{nwo}](https://github.com/{nwo})** — all credit for the selection "
             f"belongs there. This page adds stars, platform evidence, an install line and a "
             f"screenshot to each entry.",
             "",
             f"{len(rows):,} entries · "
             f"{len({r['nwo'] for r in rows if r.get('nwo')}):,} distinct repos · "
             f"{len(sections)} sections",
             "",
             "[← back to the mega list](../README.md)",
             ""]
    lines += gallery(rows, shots)
    lines += ["## Contents", ""]
    for name in sections:
        n = sum(1 for r in rows if r["section"] == name)
        lines.append(f"- [{prose(name)}](#{slug(name)}) ({n})")
    lines.append("")

    for name in sections:
        lines += [f"## {prose(name)}", ""]
        for r in sorted([x for x in rows if x["section"] == name],
                        key=lambda x: (-(x.get("stars") or 0), x.get("src_order", 0))):
            facts = [f"★ {stars(r)}"] if stars(r) != DASH else []
            for key in ("language", "license", "install_method"):
                if r.get(key):
                    facts.append(prose(r[key]))
            if r.get("pushed_at"):
                facts.append(f"pushed {r['pushed_at']}")
            if support(r) != DASH:
                facts.append(support(r))
            lines.append(f"- **[{prose(r['name'])}]({r['url']})** — {prose(r.get('blurb') or '')}")
            if facts:
                lines.append(f"  <sub>{' · '.join(facts)}</sub>")
            if r.get("install_cmd"):
                lines.append(f"  <sub>{code(r['install_cmd'])}</sub>")
        lines.append("")
    return lines + footer(1)


# ------------------------------------------------------------------ platform pages
LEGEND = ("`Win` `WSL2` `macOS` `Linux` `Docker` mean the project supports that target. A trailing "
          "`?` marks a verdict inferred from the install route or the language runtime rather than "
          "confirmed by a release asset or by the README saying so — `Why` gives the reasoning for "
          "every row.")


def confirmed(rec, field: str) -> bool:
    """Windows has two ways in, and WSL2 support stated outright is confirmation, not inference."""
    if field == "win_native":
        return rec["win_native"] == "Yes" or rec["win_wsl2"] == "Yes"
    return rec[field] == "Yes"


def platform_table(rows, name: str, start: int = 1) -> list[str]:
    out = ["| # | Project | ★ | Lists | Support | Language | Install / Run | What it does | Why |",
           "|--:|---|--:|--:|---|---|---|---|---|"]
    for i, r in enumerate(rows, start=start):
        out.append(
            f"| {i} | **[{prose(r['name'], table=True)}]({r['url']})**"
            f"<br><sub>{prose(r['nwo'], table=True)}</sub> "
            f"| {stars(r)} | {r['list_count']} | {support(r)} "
            f"| {prose(r.get('language') or DASH, table=True)} "
            f"| {code(b16.platform_install(r, name), table=True)} "
            f"| {prose(r.get('blurb') or '', 220, table=True)} "
            f"| <sub>{prose(r.get('os_evidence') or DASH, 160, table=True)}</sub> |")
    return out


def platform_pages(name: str, field: str, headline: str, note: str, rows, total: int,
                   shots) -> list[tuple[str, list[str]]]:
    """The platform's own page holds the confirmed rows; the inferred ones get a sibling.

    Not a taste call. Three of these tables in one file each would land within a few percent of the
    512 KB at which GitHub stops rendering Markdown, and the split that keeps them clear of it is
    the one a reader wants anyway: proof first, inference one click behind it.
    """
    sure = [r for r in rows if confirmed(r, field)]
    maybe = [r for r in rows if not confirmed(r, field)]
    key, extra = slug(name), f"{slug(name)}-inferred.md"

    lines = [f"# {name}",
             "",
             f"Every project across all eleven lists that {headline} — **{len(rows):,}** of "
             f"{total:,} distinct repos, deduplicated to one row per repo.",
             "",
             note,
             "",
             "[← back to the mega list](../README.md)",
             ""]
    lines += gallery(sure or rows, shots)
    lines += ["## Legend", "", LEGEND, ""]
    lines += [f"## Confirmed ({len(sure):,})",
              "",
              "A release asset for this platform, or the README saying so outright.",
              ""]
    lines += platform_table(sure, name)
    if maybe:
        lines += ["",
                  f"## Inferred ({len(maybe):,})",
                  "",
                  f"No direct statement, but the install route or the language runtime implies it. "
                  f"On its own page so this one stays scannable: "
                  f"**[all {len(maybe):,} inferred {name} projects →]({extra})**",
                  ""]
    pages = [(f"platforms/{key}.md", lines + footer(1))]
    if maybe:
        pages.append((f"platforms/{extra}", [
            f"# {name} — inferred",
            "",
            f"The **{len(maybe):,}** projects that probably run on {name} but do not say so. Each "
            f"verdict here comes from the install route or the language runtime, never from a "
            f"release asset or from the README — that is what puts them on this page rather than "
            f"with the [{len(sure):,} confirmed ones]({key}.md).",
            "",
            "Read `Why` before trusting a row. A portable runtime is a good bet and not a promise.",
            "",
            f"[← {name}]({key}.md) · [← back to the mega list](../README.md)",
            "",
            "## Legend", "", LEGEND, "",
            f"## The list ({len(maybe):,})", "",
            *platform_table(maybe, name),
        ] + footer(1)))
    return pages


# ------------------------------------------------------------------ leaderboard
def leaderboard_page(board, shots) -> list[str]:
    lines = ["# Leaderboard",
             "",
             f"The {len(board):,} most-starred projects across all eleven lists, deduplicated. "
             "`Lists` is how many of the eleven name the project — a rough consensus score, and "
             "the column worth sorting on.",
             "",
             "[← back to the mega list](README.md)",
             ""]
    lines += gallery(board, shots)
    lines += ["| # | Project | ★ | Lists | Listed by | Language | Install / Run | What it does |",
              "|--:|---|--:|--:|---|---|---|---|"]
    for i, r in enumerate(board, start=1):
        lines.append(
            f"| {i} | **[{prose(r['name'], table=True)}]({r['url']})**"
            f"<br><sub>{prose(r['nwo'], table=True)}</sub> "
            f"| {stars(r)} | {r['list_count']} | <sub>{prose(r['listed_by'], table=True)}</sub> "
            f"| {prose(r.get('language') or DASH, table=True)} "
            f"| {code(r.get('install_cmd') or '', table=True)} "
            f"| {prose(r.get('blurb') or '', 200, table=True)} |")
    return lines + footer()


# ------------------------------------------------------------------ topic & target pages
def fileslug(text: str) -> str:
    """`slug` for a filename rather than for an anchor, so runs of hyphens collapse.

    `slug` has to leave the gap where it dropped a character, because GitHub's anchors do: "Context,
    Memory & RAG" anchors as `context-memory--rag` and tidying that would produce a dead link. A
    filename carries no such constraint, and these pages are only ever linked by name, so tidying
    here cannot drift out of step with anything.
    """
    return re.sub(r"-{2,}", "-", slug(text)).strip("-")


TOPIC_BLURB = {
    "Orchestrators & Multi-Agent":
        "Running several agents at once, or one agent for a long time: swarms, loop runners, task "
        "queues, planners and the orchestration write-ups.",
    "Coding Agents":
        "The agent you point at a repository. Terminal, desktop and web, plus the parallel-agent "
        "front-ends built on top of them.",
    "Agent Skills":
        "Capability bundles an agent loads on demand — SKILL.md packages, subagents, slash commands, "
        "and the directories that collect them.",
    "MCP Servers":
        "The Model Context Protocol ecosystem: reference and third-party servers, inspectors, "
        "gateways, transports, and the sibling agent-to-agent protocols.",
    "Frameworks & SDKs":
        "Libraries you build an agent out of, and the tool-calling interfaces it reaches the world "
        "through.",
    "Harnesses & Runtime Infra":
        "The scaffolding around the model rather than the model or the agent: runtimes, providers, "
        "gateways, fine-tuning, and what a harness runs on in production.",
    "Context, Memory & RAG":
        "Everything that decides what the model actually sees: retrieval, memory stores, compaction, "
        "and the chat-with-your-data apps built on them.",
    "Sandbox, Security & Governance":
        "Isolation, permissions, approval gates, guardrails, compliance and audit — plus the security "
        "agents that attack and defend.",
    "Observability & Evals":
        "Traces, benchmarks, graders, linting and CI feedback: how you find out whether the agent "
        "actually did the thing.",
    "Plugins, Themes & Clients":
        "Attaches to an agent you already run — plugins, themes, status lines, alternative clients, "
        "notification bridges and generative UIs.",
    "Research & Data Agents":
        "Agents pointed at literature, the web and datasets: deep research, analysis, business "
        "intelligence and science.",
    "Creative, Voice & Media":
        "Image, audio, video, voice and prose agents, and the ones that play games.",
    "Assistants & Domain Agents":
        "One agent doing one job in one domain: support, sales, finance, health, travel, browser and "
        "desktop automation, personal assistants.",
    "Docs, Learning & Lists":
        "Reading rather than running: guides, courses, pattern write-ups, practice postures, and the "
        "other awesome-lists this one was merged from.",
}

TARGET_BLURB = {
    "Claude Code": "Built for Anthropic's terminal coding agent — skills, hooks, commands, status "
                   "lines, MCP servers and the clients that wrap it.",
    "Claude / Anthropic": "Targets Claude or the Anthropic API, whether or not it goes through "
                          "Claude Code.",
    "opencode": "Built for the opencode agent: its plugins, themes, agents and surrounding projects.",
    "MCP": "Speaks the Model Context Protocol — as a server, as a client, or as a gateway between.",
    "Codex / OpenAI": "Targets Codex, the OpenAI API, or the OpenAI Agents SDK.",
    "Gemini / Google": "Targets Gemini, Vertex AI, or Google's agent stack.",
    "GitHub Copilot": "Targets Copilot: its coding agent, its CLI, or its extension surface.",
    "Cursor": "Targets the Cursor editor — rules, agents and composer workflows.",
    "Cline / Roo": "Targets Cline or Roo Code.",
    "Aider": "Targets aider.",
    "LangChain / LangGraph": "Built on LangChain, LangGraph or LangSmith.",
    "Local / Ollama": "Runs against a named local runtime: Ollama, llama.cpp, vLLM, LM Studio, "
                      "llamafile or GPT4All.",
}

UNRANKED_NOTE = ("No stars of their own to rank by — a folder inside someone else's repository, or a "
                 "link GitHub no longer serves. Listed anyway, so nothing quietly disappears from a "
                 "count.")


def facet_page(title, blurb, rows, shots, hub, other, live) -> list[str]:
    """One topic or one target: a ranked board, then the entries that nothing can rank.

    `other` is the cross-axis column — a topic page shows what each project plugs into, a target page
    shows what each project is. That is the whole reason the taxonomy has two axes: "the best Claude
    Code observability tool" is a question about both at once, and either page can answer it.

    `live` is the same page on the site, already filtered. It exists because a Markdown table can
    *show* the second axis but cannot *filter* on it — the reader can see which of these plug into
    Claude Code, and then has to read 208 rows to find them. One click does it there.
    """
    ranked = sorted([r for r in rows if r["rank"]], key=lambda r: (-r["stars"], r["name"].lower()))
    thin = sorted([r for r in rows if not r["rank"]], key=lambda r: r["name"].lower())
    lines = [f"# {prose(title)}", "",
             blurb, "",
             f"**{len(rows):,} projects** · {len(ranked):,} with stars to rank by · "
             f"{sum(r['stars'] for r in ranked):,} combined stars",
             "",
             f"[← every {hub[0]}]({hub[1]}) · [← back to the mega list](../README.md) · "
             f"[**filter this live →**]({live})",
             ""]
    # Named up front as well as marked in the table, because a reader arriving at a 278-row page has no
    # way to know whether it is worth looking for the mark. This page is a snapshot; the site's chip is
    # the version that expires on its own.
    arrived = [r for r in rows if newness.mark(r["nwo"])]
    if arrived:
        lines += [f"✨ **{len(arrived)} new in the last {newness.WINDOW} days** — "
                  f"marked below, and [filterable on the site]({live}{'&' if '#' in live else '#'}new=1).",
                  ""]
    lines += gallery(ranked or thin, shots)
    if ranked:
        lines += [f"## Ranked by stars ({len(ranked):,})", "",
                  f"| # | Project | ★ | Lists | {other[0]} | Runs on | Install / Run "
                  f"| What it does |",
                  "|--:|---|--:|--:|---|---|---|---|"]
        for i, r in enumerate(ranked, start=1):
            lines.append(
                f"| {i} | **[{prose(r['name'], table=True)}]({r['url']})**{newness.mark(r['nwo'])}"
                f"<br><sub>{prose(r['nwo'], table=True)}</sub> "
                f"| {stars(r)} | {r['list_count']} "
                f"| <sub>{prose(other[1](r) or DASH, table=True)}</sub> "
                f"| <sub>{support(r)}</sub> "
                f"| {code(r.get('install_cmd') or '', table=True)} "
                f"| {prose(r.get('blurb') or '', 180, table=True)} |")
        lines.append("")
    if thin:
        lines += [f"## Also here, unranked ({len(thin):,})", "", UNRANKED_NOTE, ""]
        for r in thin:
            lines.append(f"- **[{prose(r['name'])}]({r['url']})**{newness.mark(r['nwo'])} — "
                         f"{prose(r.get('blurb') or '', 200)}")
        lines.append("")
    return lines + footer(1)


def facet_summary(groups: dict, folder: str) -> list[str]:
    """One table row per facet, for the hub page. Relative to mega-list/, not to the facet folder."""
    out = []
    for name, rows in groups.items():
        ranked = [r for r in rows if r["rank"]]
        top = max(ranked, key=lambda r: r["stars"], default=None)
        cell = f"[{prose(top['name'], 40, table=True)}]({top['url']}) ★ {stars(top)}" if top else DASH
        out.append(f"| [**{prose(name, table=True)}**]({folder}/{fileslug(name)}.md) | {len(rows):,} "
                   f"| {len(ranked):,} | {sum(r['stars'] for r in ranked):,} | {cell} |")
    return out


def facet_hub(title, column, intro, groups, page_for, sibling) -> list[str]:
    """The index over one axis: every topic, or every target, with what is on each page."""
    lines = [f"# {title}", "", intro, "",
             f"[← back to the mega list](../README.md) · [{sibling[0]}]({sibling[1]}) · "
             f"[Leaderboard](../leaderboard.md) · [Filter it live]({site()})",
             "",
             f"| {column} | Projects | Ranked | ★ combined | Most-starred |",
             "|---|--:|--:|--:|---|"]
    for name, blurb, rows in groups:
        ranked = [r for r in rows if r["rank"]]
        top = max(ranked, key=lambda r: r["stars"], default=None)
        cell = (f"[{prose(top['name'], 40, table=True)}]({top['url']}) "
                f"<sub>★ {stars(top)}</sub>" if top else DASH)
        lines.append(f"| **[{prose(name, table=True)}]({page_for(name)})**"
                     f"<br><sub>{prose(blurb, table=True)}</sub> "
                     f"| {len(rows):,} | {len(ranked):,} "
                     f"| {sum(r['stars'] for r in ranked):,} | {cell} |")
    return lines + footer(1)


# ------------------------------------------------------------------ hub page
def readme_page(stats, per_source, board, shots, files, by_topic, by_target) -> list[str]:
    lines = [
        "# Awesome Agentic Atlas",
        "",
        f"**{stats['lists']} curated awesome-lists merged into one.** "
        f"{stats['items']:,} entries, {stats['repos']:,} distinct GitHub repos, "
        f"{stats['stars']:,} stars — each entry resolved to its repo and given a screenshot, an "
        f"install line, and platform evidence for Windows, WSL2, macOS, Linux and Docker.",
        "",
        "Every list below was made by someone else. This is not a new selection: it is their "
        "selections in one place, with the facts filled in and the overlap made visible.",
        "",
        f"Also here as spreadsheets, screenshots embedded and every column filterable: "
        f"**[dark theme]({book(0, 'DARK')})** · **[light theme]({book(0, 'LIGHT')})**. "
        f"And as a page you can filter in the browser, no download: **[the Atlas site]({site()})**.",
        "",
        "## Pick your platform",
        "",
        "| Platform | Confirmed | Inferred | Total | Page |",
        "|---|--:|--:|--:|---|",
    ]
    for name, _f, _headline, _n in PLATFORMS:
        n = stats["platforms"][name]
        sure, maybe = stats["splits"][name]
        extra = (f" · [inferred](platforms/{slug(name)}-inferred.md)" if maybe else "")
        lines.append(f"| **{name}** | {sure:,} | {maybe:,} | {n:,} "
                     f"| [{name}](platforms/{slug(name)}.md){extra} |")
    lines += ["",
              "**Confirmed** means a release asset for that platform, or the README saying so "
              "outright. **Inferred** means the install route or the language runtime implies it "
              "and nothing states it — a good bet, not a promise, and each row carries the "
              "reasoning that put it there."]
    lines += ["",
              f"Those four are drawn from the {stats['pool']:,} distinct repos that entries across "
              f"the eleven lists resolve to. A hosted product with no public repo and a folder "
              f"inside a larger repo have no platform support of their own to report, so neither "
              f"appears on a platform page — both are on their list's page instead.",
              "",
              "## Pick your topic",
              "",
              f"Eleven curators used {len(tax.SECTIONS)} different section names and agreed on almost "
              f"none of them — `Frameworks`, `Agent Frameworks` and `Build-your-own` are one shelf "
              f"under three names. These {len(tax.CATEGORIES)} are one vocabulary over all of it, so "
              f"that \"the best X\" becomes a question with an answer.",
              "",
              "| Topic | Projects | Ranked | ★ combined | Most-starred |",
              "|---|--:|--:|--:|---|"]
    lines += facet_summary(by_topic, "topics")
    lines += ["",
              "[**All topics, with what is on each page →**](topics/README.md)",
              "",
              "## Pick your harness",
              "",
              "The second axis: what a project plugs into, rather than what it is. Cross the two and "
              "you get the question none of the eleven lists could answer on its own — the best "
              "Claude Code observability tool, the best opencode plugin, the best local-runtime "
              "orchestrator.",
              "",
              "| Runs with | Projects | Ranked | ★ combined | Most-starred |",
              "|---|--:|--:|--:|---|"]
    lines += facet_summary(by_target, "targets")
    lines += ["",
              "A project can be on several of these pages, because plenty serve Claude Code and "
              "opencode and Codex at once. A project on none of them only means no harness is named "
              "anywhere in its description.",
              "",
              # The crossing is the one thing Markdown genuinely cannot do -- a page is one axis, and
              # the other is a column you have to read. So the examples are links into the site, where
              # both axes are filters, rather than links to a page that does not exist.
              "**Crossing the two** takes a filter, not a page, so those links go to the site: "
              f"[Claude Code observability]({site(topic='observability-evals', target='claude-code')}) · "
              f"[opencode plugins]({site(topic='plugins-themes-clients', target='opencode')}) · "
              f"[skills for Claude Code, Windows-native]"
              f"({site(topic='agent-skills', target='claude-code', os='windows', confirmed='1')}) · "
              f"[memory and retrieval over MCP]({site(topic='context-memory-rag', target='mcp')}).",
              "",
              "[**All harnesses →**](targets/README.md)",
              "",
              "## Every list, credited",
              "",
              "★ is the source list's own star count. A dash means its repo was not among the ones "
              "this snapshot fetched, so the number is unknown rather than zero.",
              "",
              "| Awesome list | ★ | Entries | Repos | What it covers | Page |",
              "|---|--:|--:|--:|---|---|"]
    for r in per_source:
        page = files.get(r["sheet"])
        link = f"[{r['sheet']}]({page})" if page else r["sheet"]
        own = f"{r['stars']:,}" if r["stars"] is not None else DASH
        lines.append(f"| [{prose(r['nwo'], table=True)}](https://github.com/{r['nwo']}) | {own} "
                     f"| {r['items']:,} | {r['repos']:,} "
                     f"| {prose(r['blurb'], 150, table=True)} | {link} |")
    lines += ["",
              f"Lists overlap heavily — {stats['multi']} projects are named by two or more of "
              f"them. [**Leaderboard**](leaderboard.md) is the deduplicated view, ranked by stars, "
              f"with the count of how many lists agree.",
              "",
              "## Most-starred, across every list",
              ""]
    lines += gallery(board[:12], shots)
    lines += [
        "## How to read this",
        "",
        "- **Stars, language, licence and last-push** come from the GitHub API at snapshot time. "
        "They drift daily; treat them as an order of magnitude, not a live count.",
        "- **Platform columns are derived evidence, not a vendor support matrix.** The strongest "
        "signal is a published release asset — a `.msi` or `windows-amd64.zip` proves native "
        "Windows, a lone `.dmg` disproves it. Then explicit README prose, then the install route, "
        "then the language runtime alone, which only ever earns a `?`.",
        "- **A `?` means inferred.** Every platform page carries the reasoning per row in its "
        "`Why` column, so a verdict you doubt can be checked rather than taken.",
        f"- **{stats['site_rows']:,} entries are hosted products with no public repo** and "
        f"{stats['sub_rows']:,} are items inside a larger repo (a template folder, a pattern "
        f"write-up). Neither has stars or platform support of its own, so those show `—` rather "
        f"than borrowing the parent's.",
        f"- **{stats['unavailable']} listed repos now return an error from GitHub** — deleted, "
        f"renamed, or made private. They are kept, marked, so nothing silently vanishes from a "
        f"count.",
        "- **Screenshots are the first usable image in the README**, falling back to the project's "
        "own social card and then to GitHub's. A GitHub card means no project image could be "
        "found, not that the project has no UI.",
        "- **Sections keep the wording each list published.** Nothing was renamed to make the "
        "lists agree, because a section name is part of the curation.",
        "",
        "## Contents",
        "",
        "- [Leaderboard](leaderboard.md) — top projects across every list, deduplicated",
        f"- [Browse by topic](topics/README.md) — {len(by_topic)} topics, one page each",
        f"- [Browse by harness](targets/README.md) — {len(by_target)} harnesses, one page each",
        f"- [The Atlas site]({site()}) — all {stats['repos']:,} in one page, both axes filterable",
    ]
    for name, *_r in PLATFORMS:
        lines.append(f"- [{name}](platforms/{slug(name)}.md) — "
                     f"{stats['platforms'][name]:,} repos")
    for r in per_source:
        page = files.get(r["sheet"])
        if page:
            lines.append(f"- [{r['sheet']}]({page}) — {r['items']:,} entries from "
                         f"`{r['nwo']}`")
    return lines + footer()


# ------------------------------------------------------------------ assembly
def main() -> None:
    records = b16.prepare(
        json.loads((CACHE / "records_all.json").read_text(encoding="utf-8")), None)
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    orch = json.loads((CACHE / "records.json").read_text(encoding="utf-8"))
    shots = b16.merged_shots(cached("shots_all.json"), cached("shots.json"))

    # the original list has no `section`/`bucket`; its category is the same idea under another name
    for r in orch:
        r.setdefault("section", r["category"])
        r.setdefault("bucket", r["category"])
        r.setdefault("blurb", r.get("description") or "")
        r.setdefault("src_order", r.get("order", 0))
        r["shot_key"] = (r.get("nwo") or "").replace("/", "__")
        if r.get("license") in ("NOASSERTION", "NONE", DASH, "", None):
            r["license"] = ""

    # After the shot_key assignments above, which must keep the spelling the files on disk use.
    b16.canonicalise_nwo(records, orch, meta)

    by_source = {k: [r for r in records if r["source"] == k] for k, *_ in SHEETS}
    for k, rows in by_source.items():
        b16.order_rows(rows, k)
    orch.sort(key=lambda r: (r.get("order", 0), -(r.get("stars") or 0)))

    label = {"orchestrators": "Orchestrators", **{k: t for k, t, *_ in SHEETS}}
    pool = b16.platform_pool(records, orch, label)
    by_platform = {name: b16.platform_rows(pool, field) for name, field, *_ in PLATFORMS}

    board = sorted((r for r in pool if (r.get("stars") or 0) > 0),
                   key=lambda r: (-r["stars"], r["name"].lower()))[:250]

    # The two facet axes. `repo_pool` with no filter rather than `pool`, because a topic page wants the
    # 39 repos a platform sheet has to drop -- a skill in a folder belongs under Agent Skills even
    # though it has no OS support and no stars of its own to rank.
    tax.STARS.clear()
    tax.STARS.update(b16.star_map(records, orch, meta))
    agg = tax.by_repo(records + orch)
    facets = b16.repo_pool(records, orch, label)
    for r in facets:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        # One definition of stars, taken from the map the cover and the hub already print, not from
        # whichever listing happened to seed this row.
        r["stars"] = tax.STARS.get(r["nwo"], 0)
        r["stars_kind"] = "own" if r["stars"] else "none"
        r["rank"] = bool(r["stars"])
    by_topic = {c: [r for r in facets if r["category"] == c] for c in tax.CATEGORIES}
    by_target = {t: [r for r in facets if t in r["targets"]] for t, _p in tax.TARGETS}

    # Fills newness.SEEN, which `mark` reads. The same pool 19_pages resolves, so both surfaces mark the
    # same repos on the same dates -- the whole reason the ledger is one file and not one per stage.
    newness.resolve([r["nwo"] for r in facets])

    # GitHub reports one canonical owner spelling; the hand-typed source table does not always
    # match it, and a list whose own repo was never fetched has an unknown count, not zero.
    meta_ci = {k.lower(): v for k, v in meta.items()}

    def summarise(nwo, sheet, blurb, rows):
        m = meta.get(nwo) or meta_ci.get(nwo.lower()) or {}
        return dict(nwo=nwo, sheet=sheet, blurb=blurb, stars=m.get("stargazerCount"),
                    items=len(rows), repos=len({r["nwo"] for r in rows if r.get("nwo")}))

    per_source = [summarise(ORCH_NWO, "Orchestrators", ORCH_BLURB, orch)]
    for key, title, nwo, blurb in SHEETS:
        per_source.append(summarise(nwo, title, blurb, by_source[key]))

    stats = dict(
        lists=len(per_source),
        items=len(records) + len(orch),
        repos=len({r["nwo"] for r in records if r.get("nwo")} | {r["nwo"] for r in orch}),
        # b16's definition, not a second one summed over the platform pool: this page and the
        # workbook cover print the same figure and used to disagree by 650 stars.
        stars=b16.combined_stars(records, orch, meta)[0],
        multi=sum(1 for r in pool if r["list_count"] >= 2),
        site_rows=sum(1 for r in records if r["kind"] == "site"),
        sub_rows=sum(1 for r in records if r["kind"] == "subpath"),
        unavailable=sum(1 for r in records if r.get("unavailable"))
        + sum(1 for r in orch if r.get("unavailable")),
        pool=len(pool),
        platforms={name: len(rows) for name, rows in by_platform.items()},
        splits={name: (sum(1 for r in by_platform[name] if confirmed(r, field)),
                       sum(1 for r in by_platform[name] if not confirmed(r, field)))
                for name, field, *_ in PLATFORMS},
    )

    written = []
    files = {}
    for sheet, nwo, blurb, rows in (
        [("Orchestrators", ORCH_NWO, ORCH_BLURB, orch)]
        + [(t, n, b, by_source[k]) for k, t, n, b in SHEETS]
    ):
        rel = f"lists/{slug(sheet)}.md"
        files[sheet] = rel
        written.append(write(rel, list_page(sheet, nwo, blurb, rows, shots)))

    for name, field, headline, note in PLATFORMS:
        for rel, lines in platform_pages(name, field, headline, note, by_platform[name],
                                         len(pool), shots):
            written.append(write(rel, lines))

    TOPIC_HUB, TARGET_HUB = ("topic", "README.md"), ("target", "README.md")
    for c in tax.CATEGORIES:
        written.append(write(f"topics/{fileslug(c)}.md", facet_page(
            c, TOPIC_BLURB[c], by_topic[c], shots, TOPIC_HUB,
            ("Plugs into", lambda r: ", ".join(r["targets"])),
            site(topic=fileslug(c)))))
    for t, _p in tax.TARGETS:
        written.append(write(f"targets/{fileslug(t)}.md", facet_page(
            t, TARGET_BLURB[t], by_target[t], shots, TARGET_HUB,
            ("Category", lambda r: r["category"]),
            site(target=fileslug(t)))))
    written.append(write("topics/README.md", facet_hub(
        "Browse by topic", "Topic",
        f"Every one of the {stats['repos']:,} projects, filed under exactly one of "
        f"{len(tax.CATEGORIES)} topics. The eleven source lists published "
        f"{len(tax.SECTIONS)} section names between them and agreed on almost none, so these are one "
        "shared vocabulary over all of them rather than any single curator's shelf.",
        [(c, TOPIC_BLURB[c], by_topic[c]) for c in tax.CATEGORIES],
        lambda c: f"{fileslug(c)}.md", ("by target →", "../targets/README.md"))))
    written.append(write("targets/README.md", facet_hub(
        "Browse by what it plugs into", "Runs with",
        "The other axis: not what a project *is* but what it *runs with*. A project can appear on "
        "several of these pages, because plenty of them serve Claude Code and opencode and Codex at "
        "once — and plenty appear on none, which only means no harness is named anywhere in their "
        "description.",
        [(t, TARGET_BLURB[t], by_target[t]) for t, _p in tax.TARGETS],
        lambda t: f"{fileslug(t)}.md", ("by topic →", "../topics/README.md"))))

    written.append(write("leaderboard.md", leaderboard_page(board, shots)))
    written.append(write("README.md", readme_page(stats, per_source, board, shots, files,
                                                  by_topic, by_target)))

    total = sum(p.stat().st_size for p in written)
    for p in sorted(written, key=lambda x: -x.stat().st_size):
        print(f"  {p.stat().st_size / 1024:7.1f} KB  {p.relative_to(OUT).as_posix()}")
    print(f"\n{len(written)} files · {total / 1024:.0f} KB total · "
          f"largest {max(p.stat().st_size for p in written) / 1024:.0f} KB "
          f"(GitHub renders Markdown up to 512 KB)")
    print(f"entries {stats['items']:,} · repos {stats['repos']:,} · "
          f"platform rows " + " ".join(f"{k} {v:,}" for k, v in stats["platforms"].items()))


if __name__ == "__main__":
    main()
