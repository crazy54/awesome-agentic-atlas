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
for every repo and costs this directory no bytes. And every long page is packed to a byte budget and
continued onto `-2.md`, `-3.md` as far as it takes, because GitHub stops rendering a Markdown file
past 512 KB: the mega list is one list, not one file. See `paginate` and the check `main` ends with.
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

# Reached through b16 rather than loaded a second time: b16 has already executed 10_parse_sources, and
# a second copy of SOURCES is the exact drift the docstring above promises this module will not create.
# SHEETS is the ten lists the workbook gives a tab of its own; SOURCES is every list the atlas parses,
# and on this surface those are not the same question -- a Markdown file per list costs nothing.
SOURCES, SHEET_TITLE, LIST_TITLE = b16.b10.SOURCES, b16.SHEET_TITLE, b16.LIST_TITLE


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


# ------------------------------------------------------------------ page size
# GitHub renders a Markdown file up to 512 KB and replaces anything larger with a truncation notice:
# no table, no rows, and nothing in the build that produced it says so. The only structural defence
# used to be one split -- confirmed rows here, inferred rows on a sibling page -- sized by hand for
# 1,294 listed repos, and the limit was *printed* at the end of a run and never checked. At 13,323
# listed rows that left eleven pages unrenderable, `platforms/macos-inferred.md` at 1.86 MB, with
# "GitHub renders Markdown up to 512 KB" logged underneath as though it were reassurance. And that
# was a daily job, so it would have republished all eleven every morning. So every long page is now
# packed to a byte budget and continued onto numbered siblings, and the build fails rather than
# publish a page that is anywhere near the cliff.
PAGE_LIMIT = 512 * 1024

# What one part is packed to. Roughly the largest page this collection has ever published (294 KB),
# so a split page reads like the pages readers already know rather than like a new kind of thing, and
# so a part can grow by a quarter between two daily builds without anyone touching this file -- which
# it can, because names, blurbs and install lines come from other people's repositories and change
# when they edit them.
PAGE_BUDGET = 320 * 1024

# What the build refuses to publish. Well below PAGE_LIMIT rather than just under it, because the gap
# is an alarm band and not spare capacity: a part that lands in it still renders, so the reader keeps
# a working page while the build says loudly that the packer's accounting has drifted. The margin
# also settles an ambiguity -- 512 KB is written in decimal in some of GitHub's own docs and in binary
# in others, and a ceiling within a rounding error of either reading would be a coin toss.
PAGE_CEILING = 400 * 1024

# Allowed for before packing, so the two pager strips a part carries can never be the thing that
# pushes it over. Generous on purpose: a strip is one line naming every part, so this covers a
# fifty-part page twice over.
PAGER_COST = 4 * 1024


def block(title: str = "", intro=(), header=(), rows=(), nav: str = "", unit: str = "rows") -> dict:
    """One `## ` section of a page, split into the part that repeats and the part that gets divided.

    `rows` is the only field `paginate` cuts. An entry that renders as three lines -- a bullet, its
    facts, its install command -- is *one* string with newlines in it rather than three list items,
    so that a cut can never land between a project and its own install line.

    `header` is a GFM table header, re-emitted at the top of every part the section spills into,
    because a table whose header row is on the previous file is not a table. `nav` is the section's
    line in its page's Contents list, generated per part so a part never links `#anchor` at a heading
    that is in a different file. `title` may be empty, for the one page whose body has no heading.
    """
    return dict(title=title, intro=list(intro), header=list(header), rows=list(rows),
                nav=nav, unit=unit)


def cost(lines) -> int:
    """Bytes these lines add to a file. `write` joins on newline, so one separator each."""
    return sum(len(x.encode("utf-8")) + 1 for x in lines)


def pager(name: str, i: int, n: int) -> list[str]:
    """The strip that makes every part of a split page reachable from every other part.

    Every part, not only the neighbours. Prev/next alone means a reader on part 1 of six has no way
    to know part 6 exists, and the whole reason for splitting rather than truncating is that no row
    stops being reachable. Part 1 keeps the unsuffixed filename, so every link written before a page
    grew -- the hub's platform table, both facet hubs, the confirmed/inferred cross-links -- still
    lands on the page it always did.

    Linked by bare filename, never by the path `name` carries: every part of a page is a sibling of
    every other, and `platforms/linux-2.md` resolved from inside `platforms/` is a dead link.
    """
    if n < 2:
        return []
    stem = name.rsplit("/", 1)[-1]

    def where(k: int) -> str:
        return f"{stem}.md" if k == 1 else f"{stem}-{k}.md"

    marks = " · ".join(f"**{k}**" if k == i else f"[{k}]({where(k)})" for k in range(1, n + 1))
    more = f" — [continue on page {i + 1} →]({where(i + 1)})" if i < n else "."
    return [f"Page **{i}** of {n}, because this list is longer than the {PAGE_LIMIT // 1024} KB "
            f"GitHub will render in one file. In order: {marks}{more}", ""]


def part_of(b: dict, first: int, last: int) -> list[str]:
    """One block, or the slice of it that fits on this part."""
    out = [f"## {b['title']}", ""] if b["title"] else []
    if b["intro"]:
        out += b["intro"] + [""]
    if first or last < len(b["rows"]):
        out += [f"<sub>{b['unit'].capitalize()} {first + 1:,}–{last:,} of {len(b['rows']):,}. The "
                f"rest are on this page's other parts, linked above and below.</sub>", ""]
    body = b["header"] + b["rows"][first:last]
    # A prose-only block closes itself -- `intro` already ended with a blank. Adding another put a
    # second blank line into pages nowhere near the size limit, so a change that should have been
    # invisible on most of this directory turned up in the diff for all of it.
    return (out + body + [""]) if body else out


def paginate(rel: str, head: list[str], blocks: list[dict], foot: list[str],
             lede=()) -> list[tuple[str, list[str]]]:
    """One page, as however many files it takes for each of them to render on GitHub.

    Packed by measured bytes rather than by a row count, because rows here are not the same size: a
    bullet on a list page is ~130 bytes and a platform table row with an evidence sentence in it is
    ~700, so any fixed `[:N]` either wastes most of a page or overshoots it, and the one thing this
    must never do is silently drop a repo. Greedy first-fit, splitting inside a section only when the
    section on its own does not fit -- so a page with sections that fit lands one section per part,
    which is the split a reader would have chosen anyway.

    `head` repeats on every part and `lede` is part-1-only, which is where the picture gallery goes:
    the same six images at the top of six files would be six times the bytes for none of the point.

    A page that fits gets exactly one file, named `rel`, with no pager strip -- so this is a no-op for
    the majority of these pages, which have never been near the limit and should not start looking
    like they were.
    """
    name = rel[: -len(".md")]
    room = PAGE_BUDGET - cost(head) - cost(foot) - PAGER_COST
    parts: list[list[tuple[dict, int, int]]] = [[]]
    used = cost(lede)
    for b in blocks:
        fixed = cost(part_of(b, 0, 0))
        first = 0
        while True:
            if parts[-1] and used + fixed > room:
                parts.append([])
                used = 0
            used += fixed
            last = first
            while last < len(b["rows"]) and used + cost([b["rows"][last]]) <= room:
                used += cost([b["rows"][last]])
                last += 1
            # One row always goes somewhere, even a row that is on its own larger than a whole
            # budget. Without this a single oversized row would open empty parts for ever, and the
            # assertion at the end of `main` is what catches the page it lands on.
            last = max(last, min(first + 1, len(b["rows"])))
            parts[-1].append((b, first, last))
            if last >= len(b["rows"]):
                break
            first = last
            parts.append([])
            used = 0

    n = len(parts)
    pages = []
    for i, part in enumerate(parts, start=1):
        strip = pager(name, i, n)
        lines = list(head) + (list(lede) if i == 1 else []) + strip
        nav = [b["nav"] for b, _f, _l in part if b["nav"]]
        if nav:
            lines += ["## Contents", ""] + nav + [""]
        for b, first, last in part:
            lines += part_of(b, first, last)
        # The strip repeats at the foot without its trailing blank, because the block above it ended
        # with one and `footer` opens with one. A page that fits gets `strip == []` and so keeps the
        # shape it has always had.
        pages.append((f"{name}.md" if i == 1 else f"{name}-{i}.md",
                      lines + strip[:-1] + list(foot)))
    return pages


# ------------------------------------------------------------------ per-list pages
def list_page(rel: str, title: str, nwo: str, blurb: str, rows, shots):
    """One source list, grouped by the section wording that list publishes.

    Sections keep their original names rather than the workbook's eight colour buckets: on a page
    there is no palette to run out of, so folding them would lose wording for nothing.
    """
    order: dict[str, tuple] = {}
    for i, r in enumerate(rows):
        order.setdefault(r["section"], (i, r["section"]))
    sections = [name for name, _k in sorted(order.items(), key=lambda kv: kv[1])]

    # Conditional, not `f"{blurb}"`: the eleven curated lists have a hand-written blurb, the rest borrow
    # their repo's GitHub description, and a handful of repos publish none. An unguarded line printed
    # "None" on those pages; skipping the paragraph reads as if it was never meant to be there.
    head = [f"# {title}", ""] + ([blurb, ""] if blurb else []) + [
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

    blocks = []
    for name in sections:
        entries = []
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
            entry = [f"- **[{prose(r['name'])}]({r['url']})** — {prose(r.get('blurb') or '')}"]
            if facts:
                entry.append(f"  <sub>{' · '.join(facts)}</sub>")
            if r.get("install_cmd"):
                entry.append(f"  <sub>{code(r['install_cmd'])}</sub>")
            entries.append("\n".join(entry))
        blocks.append(block(title=prose(name), rows=entries, unit="entries",
                            nav=f"- [{prose(name)}](#{slug(name)}) ({len(entries)})"))
    return paginate(rel, head, blocks, footer(1), gallery(rows, shots))


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


PLATFORM_COLS = ["| # | Project | ★ | Lists | Support | Language | Install / Run | What it does "
                 "| Why |",
                 "|--:|---|--:|--:|---|---|---|---|---|"]


def platform_table(rows, name: str, start: int = 1) -> list[str]:
    """The rows only. `PLATFORM_COLS` is separate because a split section re-emits the header."""
    out = []
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


def platform_pages(name: str, field: str, headline: str, note: str, rows, total: int, shots,
                   lists: int) -> list[tuple[str, list[str]]]:
    """The platform's own page holds the confirmed rows; the inferred ones get a sibling.

    Not a taste call, and not a size measure either -- it used to claim to be one. Proof first,
    inference one click behind it, is the order a reader wants; what it is *not* is a guarantee about
    bytes. At 1,294 listed repos one of these tables happened to fit in a file and the docstring here
    read that coincidence back as a design; at 13,323 every one of the seven pages this function
    writes was over the 512 KB cliff, three of them past 1.7 MB. Fitting a file is `paginate`'s job,
    and every block below is handed to it whole.
    """
    sure = [r for r in rows if confirmed(r, field)]
    maybe = [r for r in rows if not confirmed(r, field)]
    key, extra = slug(name), f"{slug(name)}-inferred.md"

    head = [f"# {name}",
            "",
            f"Every project across all {lists} lists that {headline} — **{len(rows):,}** of "
            f"{total:,} distinct repos, deduplicated to one row per repo.",
            "",
            note,
            "",
            "[← back to the mega list](../README.md)"
            # In the head, so it repeats on every part. The `Inferred` block below it is the last
            # thing on the page, which on a split page means the last part, and a reader who never
            # gets there would otherwise never learn the sibling page exists.
            + (f" · [{len(maybe):,} inferred →]({extra})" if maybe else ""),
            ""]
    blocks = [block(title="Legend", intro=[LEGEND]),
              block(title=f"Confirmed ({len(sure):,})",
                    intro=["A release asset for this platform, or the README saying so outright."],
                    header=PLATFORM_COLS, rows=platform_table(sure, name), unit="projects")]
    if maybe:
        blocks.append(block(
            title=f"Inferred ({len(maybe):,})",
            intro=[f"No direct statement, but the install route or the language runtime implies it. "
                   f"On its own page so this one stays scannable: "
                   f"**[all {len(maybe):,} inferred {name} projects →]({extra})**"]))
    pages = paginate(f"platforms/{key}.md", head, blocks, footer(1), gallery(sure or rows, shots))
    if maybe:
        pages += paginate(f"platforms/{extra}", [
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
        ], [block(title="Legend", intro=[LEGEND]),
            block(title=f"The list ({len(maybe):,})", header=PLATFORM_COLS,
                  rows=platform_table(maybe, name), unit="projects")], footer(1))
    return pages


# ------------------------------------------------------------------ leaderboard
def leaderboard_page(board, shots, lists: int) -> list[tuple[str, list[str]]]:
    head = ["# Leaderboard",
            "",
            f"The {len(board):,} most-starred projects across all {lists} lists, deduplicated. "
            f"`Lists` is how many of the {lists} name the project — a rough consensus score, and "
            "the column worth sorting on.",
            "",
            "[← back to the mega list](README.md)",
            ""]
    rows = []
    for i, r in enumerate(board, start=1):
        rows.append(
            f"| {i} | **[{prose(r['name'], table=True)}]({r['url']})**"
            f"<br><sub>{prose(r['nwo'], table=True)}</sub> "
            f"| {stars(r)} | {r['list_count']} | <sub>{prose(r['listed_by'], table=True)}</sub> "
            f"| {prose(r.get('language') or DASH, table=True)} "
            f"| {code(r.get('install_cmd') or '', table=True)} "
            f"| {prose(r.get('blurb') or '', 200, table=True)} |")
    # Through `paginate` like everything else even though `main` caps the board at 250 rows and this
    # page has never come close: the cap lives at the call site, and a page that grows the day someone
    # raises it should split rather than truncate.
    return paginate("leaderboard.md", head, [block(
        header=["| # | Project | ★ | Lists | Listed by | Language | Install / Run | What it does |",
                "|--:|---|--:|--:|---|---|---|---|"],
        rows=rows, unit="projects")], footer(), gallery(board, shots))


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


def facet_page(rel, title, blurb, rows, shots, hub, other, live) -> list[tuple[str, list[str]]]:
    """One topic or one target: a ranked board, then the entries that nothing can rank.

    `other` is the cross-axis column — a topic page shows what each project plugs into, a target page
    shows what each project is. That is the whole reason the taxonomy has two axes: "the best Claude
    Code observability tool" is a question about both at once, and either page can answer it.

    `live` is the same page on the site, already filtered. It exists because a Markdown table can
    *show* the second axis but cannot *filter* on it — the reader can see which of these plug into
    Claude Code, and then has to scan every row on the page to find them. One click does it there.
    """
    ranked = sorted([r for r in rows if r["rank"]], key=lambda r: (-r["stars"], r["name"].lower()))
    thin = sorted([r for r in rows if not r["rank"]], key=lambda r: r["name"].lower())
    head = [f"# {prose(title)}", "",
            blurb, "",
            f"**{len(rows):,} projects** · {len(ranked):,} with stars to rank by · "
            f"{sum(r['stars'] for r in ranked):,} combined stars",
            "",
            f"[← every {hub[0]}]({hub[1]}) · [← back to the mega list](../README.md) · "
            f"[**filter this live →**]({live})",
            ""]
    # Named up front as well as marked in the table, because a reader arriving at a page of hundreds
    # of rows has no way to know whether it is worth looking for the mark. This page is a snapshot;
    # the site's chip is the version that expires on its own.
    arrived = [r for r in rows if newness.mark(r["nwo"])]
    if arrived:
        head += [f"✨ **{len(arrived)} new in the last {newness.WINDOW} days** — "
                 f"marked below, and [filterable on the site]({live}{'&' if '#' in live else '#'}new=1).",
                 ""]
    blocks = []
    if ranked:
        board = []
        for i, r in enumerate(ranked, start=1):
            board.append(
                f"| {i} | **[{prose(r['name'], table=True)}]({r['url']})**{newness.mark(r['nwo'])}"
                f"<br><sub>{prose(r['nwo'], table=True)}</sub> "
                f"| {stars(r)} | {r['list_count']} "
                f"| <sub>{prose(other[1](r) or DASH, table=True)}</sub> "
                f"| <sub>{support(r)}</sub> "
                f"| {code(r.get('install_cmd') or '', table=True)} "
                f"| {prose(r.get('blurb') or '', 180, table=True)} |")
        blocks.append(block(
            title=f"Ranked by stars ({len(ranked):,})",
            header=[f"| # | Project | ★ | Lists | {other[0]} | Runs on | Install / Run "
                    f"| What it does |",
                    "|--:|---|--:|--:|---|---|---|---|"],
            rows=board, unit="projects"))
    if thin:
        blocks.append(block(
            title=f"Also here, unranked ({len(thin):,})", intro=[UNRANKED_NOTE], unit="projects",
            rows=[f"- **[{prose(r['name'])}]({r['url']})**{newness.mark(r['nwo'])} — "
                  f"{prose(r.get('blurb') or '', 200)}" for r in thin]))
    return paginate(rel, head, blocks, footer(1), gallery(ranked or thin, shots))


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
              f"the {stats['lists']} lists resolve to. A hosted product with no public repo and a "
              f"folder inside a larger repo have no platform support of their own to report, so "
              f"neither appears on a platform page — both are on their list's page instead.",
              "",
              "## Pick your topic",
              "",
              f"{stats['lists']} curators used {len(tax.SECTIONS)} different section names and agreed "
              f"on almost none of them — `Frameworks`, `Agent Frameworks` and `Build-your-own` are "
              f"one shelf under three names. These {len(tax.CATEGORIES)} are one vocabulary over all "
              f"of it, so that \"the best X\" becomes a question with an answer.",
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
              f"you get the question none of the {stats['lists']} lists could answer on its own — the "
              "best Claude Code observability tool, the best opencode plugin, the best local-runtime "
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

    by_source = {s["key"]: [r for r in records if r["source"] == s["key"]] for s in SOURCES
                 if s["key"] != "orchestrators"}
    for k, rows in by_source.items():
        b16.order_rows(rows, k)
    orch.sort(key=lambda r: (r.get("order", 0), -(r.get("stars") or 0)))

    # Every source's display name, not just the ten with a workbook tab. `listed_by` on the leaderboard,
    # the platform pages and both facet axes reads this, and those pages hold rows from all thirty-nine
    # lists: a map covering ten of them printed a raw internal key for the rest, so one row said
    # "Listed by: cc_toolkit_rohitg00" where its neighbour said "Claude Code".
    label = LIST_TITLE
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
    # `sources` lets the ledger tell a list being read for the first time from a day's arrivals; 19_pages
    # passes the same set, and this stage runs first in both workflows, so the two cannot disagree.
    newness.resolve([r["nwo"] for r in facets], sources=[s["nwo"] for s in SOURCES])

    # GitHub reports one canonical owner spelling; the hand-typed source table does not always
    # match it, and a list whose own repo was never fetched has an unknown count, not zero.
    meta_ci = {k.lower(): v for k, v in meta.items()}

    def summarise(nwo, sheet, blurb, rows):
        m = meta.get(nwo) or meta_ci.get(nwo.lower()) or {}
        return dict(nwo=nwo, sheet=sheet, blurb=blurb, stars=m.get("stargazerCount"),
                    items=len(rows), repos=len({r["nwo"] for r in rows if r.get("nwo")}))

    def described(nwo: str) -> str:
        m = meta.get(nwo) or meta_ci.get(nwo.lower()) or {}
        return (m.get("description") or "").strip()

    # (title, repo, blurb, rows) for every list, in the order the hub credits them and the order their
    # pages are written -- one list, so those two can never disagree about which lists exist. The eleven
    # with a hand-written blurb keep their curated order; the rest follow, largest contribution first,
    # each described by its own repo's GitHub description. Building this from SHEETS credited eleven
    # maintainers for the work of thirty-nine, and `stats["lists"]` printed 11 on a hub whose
    # leaderboard was already drawn from all of them.
    listing = ([("Orchestrators", ORCH_NWO, ORCH_BLURB, orch)]
               + [(t, n, b, by_source[k]) for k, t, n, b in SHEETS]
               + [(s["title"], s["nwo"], described(s["nwo"]), by_source[s["key"]])
                  for s in sorted((s for s in SOURCES if s["key"] != "orchestrators"
                                   and s["key"] not in SHEET_TITLE),
                                  key=lambda s: -len(by_source[s["key"]]))])

    per_source = [summarise(nwo, title, blurb, rows) for title, nwo, blurb, rows in listing]

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

    written: list[Path] = []
    files: dict[str, str] = {}

    def emit(pages) -> None:
        """Every generator below returns a list of files, because any of them may have split."""
        written.extend(write(rel, lines) for rel, lines in pages)

    for sheet, nwo, blurb, rows in listing:
        rel = f"lists/{slug(sheet)}.md"
        # The unsuffixed name, always: `paginate` gives part 1 that filename, so the hub's link is
        # right whether this list needed one file or nine.
        files[sheet] = rel
        emit(list_page(rel, sheet, nwo, blurb, rows, shots))

    for name, field, headline, note in PLATFORMS:
        emit(platform_pages(name, field, headline, note, by_platform[name], len(pool), shots,
                            stats["lists"]))

    TOPIC_HUB, TARGET_HUB = ("topic", "README.md"), ("target", "README.md")
    for c in tax.CATEGORIES:
        emit(facet_page(f"topics/{fileslug(c)}.md",
                        c, TOPIC_BLURB[c], by_topic[c], shots, TOPIC_HUB,
                        ("Plugs into", lambda r: ", ".join(r["targets"])),
                        site(topic=fileslug(c))))
    for t, _p in tax.TARGETS:
        emit(facet_page(f"targets/{fileslug(t)}.md",
                        t, TARGET_BLURB[t], by_target[t], shots, TARGET_HUB,
                        ("Category", lambda r: r["category"]),
                        site(target=fileslug(t))))
    # The three hub pages are one row per facet, per source list or per platform, so they grow with the
    # *number* of lists rather than with the number of repos and are two orders of magnitude off the
    # limit. They stay single files, and the check at the end of this function is what would notice if
    # that ever stopped being true.
    written.append(write("topics/README.md", facet_hub(
        "Browse by topic", "Topic",
        f"Every one of the {stats['repos']:,} projects, filed under exactly one of "
        f"{len(tax.CATEGORIES)} topics. The {stats['lists']} source lists published "
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

    emit(leaderboard_page(board, shots, stats["lists"]))
    written.append(write("README.md", readme_page(stats, per_source, board, shots, files,
                                                  by_topic, by_target)))

    sizes = sorted(((p.stat().st_size, p) for p in written), reverse=True)
    total = sum(n for n, _p in sizes)
    for n, p in sizes:
        print(f"  {n / 1024:7.1f} KB  {p.relative_to(OUT).as_posix()}")
    print(f"\n{len(written)} files · {total / 1024:.0f} KB total · "
          f"largest {sizes[0][0] / 1024:.0f} KB · budget {PAGE_BUDGET / 1024:.0f} KB per part, "
          f"ceiling {PAGE_CEILING / 1024:.0f} KB, GitHub renders up to {PAGE_LIMIT / 1024:.0f} KB")
    print(f"entries {stats['items']:,} · repos {stats['repos']:,} · "
          f"platform rows " + " ".join(f"{k} {v:,}" for k, v in stats["platforms"].items()))

    # The line above used to be the whole defence: print the limit, publish whatever was written. A
    # page over it renders on GitHub as a truncation notice with no table under it, which looks like
    # a page that exists, so nothing downstream -- not the site build, not the link linter, not a
    # reader glancing at the diff -- can tell it apart from a page that works. The run that motivated
    # this wrote eleven of them and said "48 files, largest 1856 KB" as though that were fine. So it
    # is an error now, raised after the listing above so the log still says which page and how big.
    over = [(n, p) for n, p in sizes if n > PAGE_CEILING]
    if over:
        raise SystemExit(
            f"{len(over)} page(s) over the {PAGE_CEILING / 1024:.0f} KB ceiling "
            f"(GitHub stops rendering Markdown at {PAGE_LIMIT / 1024:.0f} KB):\n"
            + "\n".join(f"  {n:>9,} bytes  {p.relative_to(OUT).as_posix()}" for n, p in over)
            + "\n\nEvery long page is packed to PAGE_BUDGET by `paginate`, so a page here means "
              "either a block whose fixed header alone is enormous or a generator that bypassed it.")


if __name__ == "__main__":
    main()
