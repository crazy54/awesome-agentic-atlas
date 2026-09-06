"""Build the combined workbook: every awesome-list in the atlas, one file, two themes.

Sheet plan
  Start Here     cover, totals, how to filter, how the verdicts were reached
  Sources        every list this workbook was built from, credited
  Orchestrators  the original list, with its full OS/install treatment
  <one per list> the ten lists worth reading one at a time (SHEETS), grouped by
                 section, most stars first, screenshot per row. The other
                 twenty-eight reach the reader through the cross-list sheets --
                 every row of every list is on By Category -- and are credited
                 on Sources, List Stats and the cover's directory all the same.
  Leaderboard    the highest-starred projects across every list at once
  Windows / macOS / Linux / Docker
                 one tab per platform, drawn from every list at once and
                 deduplicated to one row per repo, strongest evidence first.
                 These replace 07_build's orchestrators-only "Windows Picks":
                 a platform question is about the tool, not about which list
                 happened to name it, so the answer should not be per-sheet.
  Category Stats charts for the original list
  List Stats     items and stars per source list

Colour rule: each sheet gets at most eight category hues from the validated
palette, in fixed slot order. Lists with more sections than that fold into <= 8
colour groups (see buckets.py) and print their own section name in its own
column, so hue narrows the field and text identifies the row.

The source lists themselves take no palette hue at all. There are several times
more of them than the palette has slots, so a hue per list would have to either
repeat or be invented, and both are forbidden -- so the three sheets that list
them one per row (Sources, List Stats, the cover's directory) name each one in
text and fill its chip from the theme's neutrals. `slot()` raises rather than
cycle, so the next thing that outgrows eight says so instead of quietly reusing
a colour.
"""
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.drawing.image import Image as XLImage
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, TwoCellAnchor
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

# The one Table in the workbook. Named here because `18_slicers.py` has to find it by name to bind to.
CATEGORY_TABLE = "ByCategory"

sys.path.insert(0, str(Path(__file__).parent))
from buckets import BUCKETS, bucket_order  # noqa: E402
# Safe to import at module scope: taxonomy only reaches back into this module inside `load()`, which
# nothing here calls, so there is no cycle.
import taxonomy as tax  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
SHOTS = CACHE / "shots"
OUT = ROOT

spec = importlib.util.spec_from_file_location("b07", Path(__file__).parent / "07_build.py")
b7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b7)

spec = importlib.util.spec_from_file_location("b10", Path(__file__).parent / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b10)

THEMES = b7.THEMES
fill, side, paint, mix, best_ink = b7.fill, b7.side, b7.paint, b7.mix, b7.best_ink
SHOT_W, SHOT_H = b7.SHOT_W, b7.SHOT_H

# palette slot order is the CVD-safety mechanism -- never re-order, never cycle
SLOTS = [
    ("#2a78d6", "#3987e5"), ("#eb6834", "#d95926"), ("#1baf7a", "#199e70"),
    ("#eda100", "#c98500"), ("#e87ba4", "#d55181"), ("#008300", "#008300"),
    ("#4a3aa7", "#9085e9"), ("#e34948", "#e66767"),
]


def slot(i: int, n: int, what: str) -> tuple[str, str]:
    """Palette slot `i` of `n` things that have to be told apart, or a loud failure.

    Deliberately not `SLOTS[i % len(SLOTS)]`, because that is how this fails quietly: at nine
    things the ninth silently takes the first one's hue, two rows of one legend become one colour,
    and nothing raises -- the workbook merely misleads, which is worse than not building. Every
    caller therefore has to say how many things it is colouring, and asking for more than the
    palette holds stops the build. `buckets.check` and `10_parse_sources.unmapped` already refuse
    above eight upstream; this is the same rule at the point where the slot is actually handed out,
    so it also catches the maps that grew a ninth entry after those two last ran.
    """
    if n > len(SLOTS):
        raise SystemExit(
            f"{what}: {n} things want a hue each and the palette has {len(SLOTS)} -- fold them "
            f"into <= {len(SLOTS)} groups (see buckets.py) or let the text carry the identity")
    return SLOTS[i]


# Which lists get a sheet of their own, in tab order. Ten of the thirty-nine, and deliberately so:
# a sheet per list would be thirty-nine tabs and thirty-nine screenshot sets, and the sheets that cut
# across every list -- By Category, Leaderboard, the four platform tabs -- already carry every row
# from every source. So this list answers "which lists are worth reading one at a time", which is a
# curation question, and it is not the same question as "which lists is the atlas built from".
# Anything that means the second one must read SOURCES; see LIST_TITLE.
SHEETS = [
    ("agents", "Agents (kyrolabs)", "kyrolabs/awesome-agents",
     "Frameworks, dev tools and agent products, as curated by kyrolabs."),
    ("e2b", "Agents (e2b)", "e2b-dev/awesome-ai-agents",
     "e2b's catalogue of AI agents and the frameworks behind them."),
    ("agents2026", "AI Agents 2026", "caramaschiHG/awesome-ai-agents-2026",
     "A 2026 market survey — commercial products alongside open source."),
    ("claudecode", "Claude Code", "hesreallyhim/awesome-claude-code",
     "Commands, hooks, status lines and tooling for Claude Code."),
    ("opencode", "Opencode", "awesome-opencode/awesome-opencode",
     "Plugins, themes, agents and projects for the opencode terminal agent."),
    ("harness", "Harness Engineering", "ai-boost/awesome-harness-engineering",
     "How agent harnesses are built — primitives, papers and reference implementations."),
    ("patterns", "Agentic Patterns", "nibzard/awesome-agentic-patterns",
     "Named design patterns for agentic systems. Each row is a write-up, not a tool."),
    ("skills", "Agent Skills", "heilcheng/awesome-agent-skills",
     "Skill directories by vendor, plus community-published skills."),
    ("skills_aas", "AAS Skill Sources", "sickn33/agentic-awesome-skills",
     "The upstream repos the Agentic Awesome Skills library aggregates."),
    ("llmapps", "LLM App Templates", "shubhamsaboo/awesome-llm-apps",
     "Runnable example apps. Each row is a folder inside the one repo."),
]
SHEET_TITLE = {k: t for k, t, *_ in SHEETS}

# Every source's display name, which is not the same set as SHEETS. `listed_by` on the leaderboard,
# the category sheet and the four platform sheets is built from this: those sheets hold rows from every
# list in `SOURCES`, so a map covering only the ten that have a sheet left every other list printing
# a raw internal key -- a reader saw "Listed by: cc_toolkit_rohitg00" where the other rows said
# "Claude Code". SHEETS wins where it has an entry, so the ten already-shipped names do not move, and
# `orchestrators` keeps the short label the workbook has always used for it rather than its SOURCES
# title. Everything else takes the title its SOURCES entry already declares.
LIST_TITLE = {**{s["key"]: s["title"] for s in b10.SOURCES},
              "orchestrators": "Orchestrators", **SHEET_TITLE}

# The project name, in one place because three things have to agree on it: the two filenames, the
# cover's hyperlink to its sibling theme, and 17_markdown's links out to the workbooks. Deliberately
# no longer "Orchestrators" -- that list is now a couple of hundred rows out of more than thirteen
# thousand, and the original orchestrators-only build in 07_build.py keeps that name because there it
# is accurate.
WORKBOOK = "Awesome-Agentic-Atlas"
TITLE = "AWESOME AGENTIC ATLAS"

# One tab per platform, built from every list at once. Order is install-base order,
# which is also the order the counts come out in.
PLATFORMS = [
    ("Windows", "win_native",
     "runs natively on Windows, or is reachable through WSL2",
     "Native first, then WSL2-only, each block by stars. A Homebrew-only project that ships a "
     "Windows build shows its releases page instead of a command that cannot run here."),
    ("macOS", "macos",
     "runs on macOS — Apple silicon or Intel",
     "Confirmed first, then inferred, each block by stars. Confirmation means a .dmg/.pkg asset or "
     "explicit README prose; inference from a portable runtime alone only ever earns Likely."),
    ("Linux", "linux",
     "runs on Linux",
     "Confirmed first, then inferred, each block by stars. Nearly every container and CI path "
     "implies Linux, so this is the widest of the four — filter on Conf. to tighten it."),
    ("Docker", "docker",
     "ships a container image, a Dockerfile or a compose file",
     "For building a container environment. Membership is evidence-based, not aspirational: a row "
     "is here because something in the repo or its README actually names a container."),
]

DASH = "—"


def chip_style(T, hue: str) -> dict:
    hue = hue.lstrip("#")
    if T is THEMES["dark"]:
        bg = mix(T["surface"], hue, T["chip_mix"])
        ink, ratio = best_ink(bg, [hue, T["ink"], T["ink2"]])
    else:
        bg = mix(hue, T["surface"], T["chip_mix"])
        ink, ratio = best_ink(bg, [T["ink"], "FFFFFF"])
    return dict(hue=hue, chip_bg=bg, chip_ink=ink, ratio=ratio)


def list_chip(T) -> dict:
    """Chip colours for a row that stands for one source list: theme neutrals, never a palette hue.

    Three sheets list the sources one per row -- Sources, List Stats and the cover's directory --
    and each of them used to fill that row's chip from `SLOTS[i % 8]`, `i` being the list's place in
    the order. At eight lists that read as a key: one list, one hue, the same hue on all three. Then
    the ninth list silently took the first one's blue on all three at once, and nothing said so --
    and `10_parse_sources.SOURCES` now names several times the eight hues there are to go round.
    Neither way out is open: the palette is validated at eight, so inventing hues to reach the true
    count is exactly what the method forbids, and folding the lists into eight colour groups the way
    buckets.py folds sections would mean inventing a grouping of other people's lists that no sheet
    ever asks the reader to compare on. So hue drops out and the chip keeps only its shape. Every one
    of those rows already prints the sheet name inside the chip itself, with the list's own name, its
    repo and its counts beside it -- the same conclusion the "By Category" rail reached for fourteen
    topics and `plain_bar` reached for the per-list bars.
    """
    bg = T["plane"]
    ink, ratio = best_ink(bg, [T["ink"], T["ink2"]])
    return dict(hue=T["bar"], chip_bg=bg, chip_ink=ink, ratio=ratio)


def group_styles(T, source: str, rows: list) -> dict:
    """bucket name -> chip colours, assigned to palette slots in fixed order.

    The curated order in buckets.py takes the slots first. A section that map has no entry for keeps
    its own name as its bucket, so it is a ninth group on the sheet and has to be counted as one:
    left out, those sections all fell through to a single fallback hue and collided with the first
    bucket, on the one sheet where the chip *is* the key. `14_classify_all` prints exactly which
    sections are in that state, and the two lists that carry no map at all -- Schwoebel's eight
    sections, wong2's five -- are entirely made of them.
    """
    names = list(bucket_order(source))
    for r in rows:
        if r["bucket"] not in names:
            names.append(r["bucket"])
    out = {}
    for i, name in enumerate(names):
        light, dark = slot(i, len(names), f"{source} sheet colour groups")
        out[name] = chip_style(T, dark if T is THEMES["dark"] else light)
    return out


def img_for(rec, shots, theme: str):
    info = shots.get(rec["shot_key"]) or {}
    name = info.get("dark" if theme == "dark" else "light") or info.get("light")
    if not name:
        return None
    p = SHOTS / name
    return p if p.exists() else None


def place_shots(ws, rows, shots, theme: str, T, col: int, first_row: int):
    """twoCell anchoring is what makes a picture hide when its row is filtered."""
    for i, r in enumerate(rows):
        p = img_for(r, shots, theme)
        if not p:
            continue
        img = XLImage(b7.pad_shot(p, T["shot_bg"]))
        row = first_row + i
        img.anchor = TwoCellAnchor(
            editAs="twoCell",
            _from=AnchorMarker(col=col - 1, colOff=0, row=row - 1, rowOff=0),
            to=AnchorMarker(col=col, colOff=0, row=row, rowOff=0),
        )
        ws.add_image(img)


def header_row(ws, row: int, cols, T, accent=None):
    for i, (name, _w, _a) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=name)
        c.fill = fill(T["header"])
        c.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=side(accent or T["bar"], "medium"))
    ws.row_dimensions[row].height = 30


def title_band(ws, row: int, ncols: int, T, title: str, meta: str, size: int = 15):
    split = max(1, ncols // 2)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=split)
    ws.merge_cells(start_row=row, start_column=split + 1, end_row=row, end_column=ncols)
    t = ws.cell(row=row, column=1, value=title)
    t.font = Font(name="Segoe UI", size=size, bold=True, color=T["ink"])
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    m = ws.cell(row=row, column=split + 1, value=meta + "   ")
    m.font = Font(name="Segoe UI", size=9, color=T["muted"])
    m.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    paint(ws, row, row, 1, ncols, fill(T["plane"]))
    ws.row_dimensions[row].height = 30


# ------------------------------------------------------------------ list sheets
def build_list_sheet(wb, key: str, rows: list, T, shots, theme: str):
    title = SHEET_TITLE[key]
    nwo = next(n for k, _t, n, _b in SHEETS if k == key)
    blurb = next(b for k, _t, _n, b in SHEETS if k == key)
    gs = group_styles(T, key, rows)

    has_sections = any(r["bucket"] != r["section"] for r in rows)
    has_stars = any(r["stars"] > 0 for r in rows)
    has_os = any(r["win_native"] in ("Yes", "Likely") for r in rows)

    cols = [("#", 5.0, "center"), ("Group", 24.0, "left")]
    if has_sections:
        cols.append(("Section", 22.0, "left"))
    cols += [("Item", 26.0, "left"), ("Screenshot", 42.14, "center"),
             ("★ Stars", 10.0, "right"), ("What It Does", 62.0, "left")]
    if has_os:
        cols += [("Win\nNative", 9.0, "center"), ("Win\nWSL2", 9.0, "center"),
                 ("macOS", 9.0, "center"), ("Linux", 9.0, "center"),
                 ("Docker", 9.0, "center"), ("OS Support", 24.0, "left"),
                 ("Conf.", 8.0, "center"), ("Why (evidence)", 42.0, "left")]
    cols += [("Install / Run", 52.0, "left"), ("Method", 11.0, "center"),
             ("Language", 12.0, "left"), ("License", 10.0, "center"),
             ("Last Push", 11.0, "center"), ("Link", 34.0, "left")]

    ws = wb.create_sheet(title)
    ws.sheet_properties.tabColor = T["surface"]
    ws.sheet_view.showGridLines = False
    ncols = len(cols)
    last_row = 2 + len(rows)
    paint(ws, 1, last_row + 20, 1, ncols + 4, fill(T["surface"]))
    for i, (_n, w, _a) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    order_note = ("grouped by section, then most→fewest stars" if has_stars
                  else "grouped by section, in the order the list publishes them")
    title_band(ws, 1, ncols, T,
               f"{title.upper()}  ·  {nwo}",
               f"{len(rows)} items  ·  {order_note}  ·  snapshot {date.today().isoformat()}")
    header_row(ws, 2, cols, T)
    ws.freeze_panes = f"{get_column_letter(min(5, ncols))}3"
    ws.auto_filter.ref = f"A2:{get_column_letter(ncols)}{last_row}"

    f_muted = Font(name="Segoe UI", size=9, color=T["muted"])
    f_body = Font(name="Segoe UI", size=10, color=T["ink"])
    f_body2 = Font(name="Segoe UI", size=10, color=T["ink2"])
    f_mono = Font(name="Consolas", size=9, color=T["ink"])
    f_item = Font(name="Segoe UI", size=11, bold=True, color=T["link"], underline="single")
    f_link = Font(name="Segoe UI", size=9, color=T["link"], underline="single")
    f_stars = Font(name="Segoe UI", size=12, bold=True, color=T["ink"])
    status = {
        "Yes": Font(name="Segoe UI", size=10, bold=True, color=T["good"]),
        "Likely": Font(name="Segoe UI", size=10, color=T["warn"]),
        "No": Font(name="Segoe UI", size=10, color=T["off"]),
        "n/a": Font(name="Segoe UI", size=10, color=T["muted"]),
        DASH: Font(name="Segoe UI", size=10, color=T["muted"]),
    }
    hair = side(T["grid"])
    ctr = Alignment(horizontal="center", vertical="center")
    top = Alignment(vertical="top", wrap_text=True)
    mid = Alignment(vertical="center", wrap_text=True, indent=1)

    shot_col = 5 if has_sections else 4
    for i, r in enumerate(rows):
        row = 3 + i
        ws.row_dimensions[row].height = SHOT_H * 0.75
        # Indexed, not `.get`-with-a-fallback: `group_styles` was handed these same rows, so it
        # holds a slot for every bucket in them. The fallback it replaces was slot 0 for anything
        # missing, which handed the first bucket's blue to every unmapped section at once.
        cs = gs[r["bucket"]]
        band = T["band"] if i % 2 else T["surface"]
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = fill(band)
            cell.border = Border(bottom=hair)

        col = 1
        a = ws.cell(row=row, column=col, value=r["group_rank"])
        a.font = f_muted
        a.alignment = ctr
        a.border = Border(bottom=hair, left=side(cs["hue"], "thick"))
        col += 1

        g = ws.cell(row=row, column=col, value=r["bucket"])
        g.fill = fill(cs["chip_bg"])
        g.font = Font(name="Segoe UI", size=9, bold=True, color=cs["chip_ink"])
        g.alignment = mid
        g.border = Border(bottom=hair, left=side(cs["hue"], "thick"))
        col += 1

        if has_sections:
            s = ws.cell(row=row, column=col, value=r["section"])
            s.font = f_muted
            s.alignment = mid
            col += 1

        it = ws.cell(row=row, column=col, value=r["name"])
        it.font = f_item
        it.alignment = mid
        it.hyperlink = r["url"]
        col += 1

        ws.cell(row=row, column=col).alignment = ctr  # screenshot
        col += 1

        if r["stars_kind"] == "own":
            e = ws.cell(row=row, column=col, value=r["stars"])
            e.font = f_stars
            e.number_format = "#,##0"
            e.alignment = Alignment(horizontal="right", vertical="center", indent=1)
        else:
            e = ws.cell(row=row, column=col, value=DASH)
            e.font = f_muted
            e.alignment = Alignment(horizontal="right", vertical="center", indent=1)
        col += 1

        d = ws.cell(row=row, column=col, value=r["blurb"])
        d.font = f_body
        d.alignment = top
        col += 1

        if has_os:
            for kf in ("win_native", "win_wsl2", "macos", "linux", "docker"):
                c2 = ws.cell(row=row, column=col, value=r[kf])
                c2.font = status.get(r[kf], f_body)
                c2.alignment = ctr
                col += 1
            n = ws.cell(row=row, column=col, value=r["os_summary"])
            n.font = f_body2
            n.alignment = mid
            col += 1
            cf = ws.cell(row=row, column=col, value=r["os_confidence"])
            cf.font = status["Yes"] if r["os_confidence"] == "High" else (
                status["Likely"] if r["os_confidence"] == "Medium" else status[DASH])
            cf.alignment = ctr
            col += 1
            wy = ws.cell(row=row, column=col, value=r["os_evidence"])
            wy.font = f_muted
            wy.alignment = top
            col += 1

        q = ws.cell(row=row, column=col, value=r["install_cmd"] or DASH)
        q.font = f_mono if r["install_cmd"] else f_muted
        q.alignment = mid
        col += 1

        for val, fnt in ((r["install_method"] or DASH, f_muted),
                         (r["language"] or DASH, f_body2),
                         (r["license"] or DASH, f_muted),
                         (r["pushed_at"] or DASH, f_muted)):
            c3 = ws.cell(row=row, column=col, value=val)
            c3.font = fnt
            c3.alignment = ctr
            col += 1

        label = r["url"].replace("https://github.com/", "").replace("https://", "")
        lk = ws.cell(row=row, column=col, value=label[:80])
        lk.font = f_link
        lk.alignment = Alignment(vertical="center", indent=1)
        lk.hyperlink = r["url"]

    place_shots(ws, rows, shots, theme, T, shot_col, 3)
    if has_stars:
        letter = get_column_letter(6 if has_sections else 5)
        ws.conditional_formatting.add(
            f"{letter}3:{letter}{last_row}",
            DataBarRule(start_type="num", start_value=0, end_type="percentile",
                        end_value=90, color=T["bar"], showValue=True))
    return ws


# ------------------------------------------------------------------ sources sheet
def build_sources(wb, per_source, meta, T, shots, theme: str):
    ws = wb.create_sheet("Sources")
    ws.sheet_properties.tabColor = T["bar"]
    ws.sheet_view.showGridLines = False
    cols = [("#", 5.0, "center"), ("Awesome List", 30.0, "left"),
            ("Screenshot", 42.14, "center"), ("★ Stars", 11.0, "right"),
            ("Items Used", 11.0, "center"), ("Repos", 9.0, "center"),
            ("Sections", 10.0, "center"), ("What It Covers", 62.0, "left"),
            ("Sheet In This File", 24.0, "left"), ("Owner", 18.0, "left"),
            ("License", 12.0, "center"), ("Last Push", 12.0, "center"),
            ("Repo", 40.0, "left")]
    ncols = len(cols)
    rows = per_source
    last = 3 + len(rows)
    paint(ws, 1, last + 24, 1, ncols + 3, fill(T["surface"]))
    for i, (_n, w, _a) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    title_band(ws, 1, ncols, T, "SOURCES  ·  every list this workbook was built from",
               f"{len(rows)} curated lists  ·  "
               f"{sum(r['items'] for r in rows):,} items  ·  snapshot {date.today().isoformat()}")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    s = ws.cell(row=2, column=1,
                value="All credit for curation belongs to these maintainers. This workbook only "
                      "reads their lists, resolves each entry to a repo, and adds stars, platform "
                      "evidence, install lines and screenshots. Star counts are of the list itself.")
    s.font = Font(name="Segoe UI", size=9, color=T["muted"])
    s.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
    ws.row_dimensions[2].height = 30
    header_row(ws, 3, cols, T)
    ws.freeze_panes = "C4"

    hair = side(T["grid"])
    ctr = Alignment(horizontal="center", vertical="center")
    mid = Alignment(vertical="center", wrap_text=True, indent=1)
    # One chip for every row, because there is no eight-value question here for hue to answer: the
    # list's name is column 2 and the sheet it feeds is written inside the chip in column 9.
    cs = list_chip(T)
    for i, r in enumerate(rows):
        row = 4 + i
        ws.row_dimensions[row].height = SHOT_H * 0.75
        band = T["band"] if i % 2 else T["surface"]
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = fill(band)
            cell.border = Border(bottom=hair)
        a = ws.cell(row=row, column=1, value=i + 1)
        a.font = Font(name="Segoe UI", size=9, color=T["muted"])
        a.alignment = ctr
        a.border = Border(bottom=hair, left=side(cs["hue"], "thick"))

        n = ws.cell(row=row, column=2, value=r["name"])
        n.font = Font(name="Segoe UI", size=11, bold=True, color=T["link"], underline="single")
        n.alignment = mid
        n.hyperlink = r["url"]
        n.border = Border(bottom=hair, left=side(cs["hue"], "thick"))

        ws.cell(row=row, column=3).alignment = ctr
        for col, val, num in ((4, r["stars"], "#,##0"), (5, r["items"], "#,##0"),
                              (6, r["repos"], "#,##0"), (7, r["sections"], "0")):
            known = val is not None
            c2 = ws.cell(row=row, column=col, value=val if known else DASH)
            c2.font = Font(name="Segoe UI", size=11 if col == 4 else 10, bold=col == 4 and known,
                           color=T["ink"] if known else T["muted"])
            c2.number_format = num
            c2.alignment = Alignment(horizontal="right" if col == 4 else "center",
                                     vertical="center", indent=1 if col == 4 else 0)
        d = ws.cell(row=row, column=8, value=r["blurb"])
        d.font = Font(name="Segoe UI", size=10, color=T["ink"])
        d.alignment = Alignment(vertical="top", wrap_text=True)
        sh = ws.cell(row=row, column=9, value=r["tab"])
        sh.font = Font(name="Segoe UI", size=10, bold=True, color=cs["chip_ink"])
        sh.fill = fill(cs["chip_bg"])
        sh.alignment = mid
        for col, val in ((10, r["owner"]), (11, r["license"]), (12, r["pushed"])):
            c3 = ws.cell(row=row, column=col, value=val or DASH)
            c3.font = Font(name="Segoe UI", size=9, color=T["ink2"])
            c3.alignment = ctr
        lk = ws.cell(row=row, column=13, value=r["nwo"])
        lk.font = Font(name="Segoe UI", size=9, color=T["link"], underline="single")
        lk.alignment = Alignment(vertical="center", indent=1)
        lk.hyperlink = r["url"]

    place_shots(ws, rows, shots, theme, T, 3, 4)
    ws.conditional_formatting.add(
        f"D4:D{last}",
        DataBarRule(start_type="num", start_value=0, end_type="percentile", end_value=90,
                    color=T["bar"], showValue=True))
    return ws


# ------------------------------------------------------------------ leaderboard
def build_leaderboard(wb, rows, T, shots, theme: str):
    cols = [("#", 5.0, "center"), ("Project", 28.0, "left"),
            ("Screenshot", 42.14, "center"), ("★ Stars", 12.0, "right"),
            ("Lists", 7.0, "center"), ("Listed By", 40.0, "left"),
            ("What It Does", 62.0, "left"), ("Language", 13.0, "left"),
            ("License", 11.0, "center"), ("Last Push", 12.0, "center"),
            ("Install / Run", 50.0, "left"), ("Repo", 34.0, "left")]
    ws = wb.create_sheet("Leaderboard")
    ws.sheet_properties.tabColor = T["bar"]
    ws.sheet_view.showGridLines = False
    ncols = len(cols)
    last = 3 + len(rows)
    paint(ws, 1, last + 20, 1, ncols + 3, fill(T["surface"]))
    for i, (_n, w, _a) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    title_band(ws, 1, ncols, T, "LEADERBOARD  ·  most-starred projects across every list",
               f"top {len(rows)}  ·  one row per repo, however many lists name it  ·  "
               f"snapshot {date.today().isoformat()}")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    s = ws.cell(row=2, column=1,
                value="A project named by several lists appears once here, with the count. "
                      "Sort or filter on \"Lists\" to see what the curators agree on.")
    s.font = Font(name="Segoe UI", size=9, color=T["muted"])
    s.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[2].height = 18
    header_row(ws, 3, cols, T)
    ws.freeze_panes = "C4"
    ws.auto_filter.ref = f"A3:{get_column_letter(ncols)}{last}"

    hair = side(T["grid"])
    ctr = Alignment(horizontal="center", vertical="center")
    mid = Alignment(vertical="center", wrap_text=True, indent=1)
    for i, r in enumerate(rows):
        row = 4 + i
        ws.row_dimensions[row].height = SHOT_H * 0.75
        # consensus is the story here, so the rail encodes how many lists agree
        rail = T["good"] if r["list_count"] >= 3 else (T["bar"] if r["list_count"] == 2
                                                      else T["grid"])
        band = T["band"] if i % 2 else T["surface"]
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = fill(band)
            cell.border = Border(bottom=hair)
        a = ws.cell(row=row, column=1, value=i + 1)
        a.font = Font(name="Segoe UI", size=9, color=T["muted"])
        a.alignment = ctr
        a.border = Border(bottom=hair, left=side(rail, "thick"))
        n = ws.cell(row=row, column=2, value=r["name"])
        n.font = Font(name="Segoe UI", size=11, bold=True, color=T["link"], underline="single")
        n.alignment = mid
        n.hyperlink = r["url"]
        n.border = Border(bottom=hair, left=side(rail, "thick"))
        ws.cell(row=row, column=3).alignment = ctr
        st = ws.cell(row=row, column=4, value=r["stars"])
        st.font = Font(name="Segoe UI", size=12, bold=True, color=T["ink"])
        st.number_format = "#,##0"
        st.alignment = Alignment(horizontal="right", vertical="center", indent=1)
        lc = ws.cell(row=row, column=5, value=r["list_count"])
        lc.font = Font(name="Segoe UI", size=11, bold=True,
                       color=T["good"] if r["list_count"] >= 3 else T["ink"])
        lc.alignment = ctr
        lb = ws.cell(row=row, column=6, value=r["listed_by"])
        lb.font = Font(name="Segoe UI", size=9, color=T["ink2"])
        lb.alignment = mid
        d = ws.cell(row=row, column=7, value=r["blurb"])
        d.font = Font(name="Segoe UI", size=10, color=T["ink"])
        d.alignment = Alignment(vertical="top", wrap_text=True)
        for col, val in ((8, r["language"] or DASH), (9, r["license"] or DASH),
                         (10, r["pushed_at"] or DASH)):
            c2 = ws.cell(row=row, column=col, value=val)
            c2.font = Font(name="Segoe UI", size=9, color=T["ink2"])
            c2.alignment = ctr
        q = ws.cell(row=row, column=11, value=r["install_cmd"] or DASH)
        q.font = Font(name="Consolas", size=9, color=T["ink"])
        q.alignment = mid
        lk = ws.cell(row=row, column=12, value=r["url"].replace("https://github.com/", ""))
        lk.font = Font(name="Segoe UI", size=9, color=T["link"], underline="single")
        lk.alignment = Alignment(vertical="center", indent=1)
        lk.hyperlink = r["url"]

    place_shots(ws, rows, shots, theme, T, 3, 4)
    ws.conditional_formatting.add(
        f"D4:D{last}",
        DataBarRule(start_type="num", start_value=0, end_type="percentile", end_value=90,
                    color=T["bar"], showValue=True))
    return ws


# ------------------------------------------------------------------ platform sheets
def _thin(rec) -> bool:
    """A listing with nothing of its own to report: a folder in someone else's repo, or a dead link."""
    return rec.get("kind") == "subpath" or bool(rec.get("unavailable"))


def repo_pool(records, orch, label, keep=None):
    """One row per repo across every list, merged: earliest listing wins, longest blurb wins.

    `keep` decides which listings are eligible. Two callers want different answers to that and both
    are right: a platform sheet must drop the listings that have no OS support of their own, while a
    topic page must keep them, because a skill that lives in a folder still belongs on the Agent
    Skills page even though nothing about it can be measured or ranked.
    """
    pool: dict[str, dict] = {}
    for r in [dict(x, source="orchestrators") for x in orch] + records:
        nwo = r.get("nwo")
        if not nwo or (keep is not None and not keep(r)):
            continue
        a = pool.get(nwo)
        if a is None:
            a = pool[nwo] = dict(r, sources=set())
        elif _thin(a) and not _thin(r):
            # Promote: the row this repo was first seen as cannot report its own stars or platforms,
            # and a later listing can. Never fires for `platform_pool`, whose `keep` makes every
            # eligible listing a full one; it exists for the pools that keep the thin listings.
            a = pool[nwo] = dict(r, sources=a["sources"], blurb=a.get("blurb") or "")
        a["sources"].add(r["source"])
        blurb = r.get("blurb") or r.get("description") or ""
        if len(blurb) > len(a.get("blurb") or ""):
            a["blurb"] = blurb
    out = []
    for nwo, a in pool.items():
        a["list_count"] = len(a["sources"])
        a["listed_by"] = ", ".join(sorted(label.get(s, s) for s in a["sources"]))
        a["shot_key"] = a.get("shot_key") or nwo.replace("/", "__")
        a["blurb"] = a["blurb"] or a.get("description") or ""
        for k in ("win_native", "win_wsl2", "macos", "linux", "docker", "cloud"):
            a[k] = a.get(k) or DASH
        out.append(a)
    return out


def platform_pool(records, orch, label):
    """One row per repo across every list — a platform question is about the tool, not the listing.

    Site-only and sub-path entries never reach here: they have no repo of their own, so every OS
    column on them is a dash, and a platform sheet that listed them would be inviting the reader to
    filter on a value that was never measured.
    """
    return repo_pool(records, orch, label,
                     keep=lambda r: r.get("kind") != "subpath" and not r.get("unavailable"))


def merged_shots(shots, orch_shots):
    """`shots_all` keyed by shot_key, plus the original list's own map re-keyed to match.

    Both maps name files in the same `cache/shots` directory, so the basename is enough to join
    them; the original pipeline just stored absolute paths under different field names.
    """
    out = dict(shots)
    for nwo, v in orch_shots.items():
        key = nwo.replace("/", "__")
        if key in out:
            continue
        light, dark = v.get("shot_light") or "", v.get("shot_dark") or ""
        out[key] = dict(key=key, light=Path(light).name, dark=Path(dark).name,
                        tier=v.get("shot_kind") or "", shot_url=v.get("shot_url") or "")
    return out


RANK = {"Yes": 2, "Likely": 1}


def platform_rows(pool, field):
    """Rows that qualify for one platform, strongest evidence first, then by stars.

    Windows is the one platform with two ways in, so WSL2 counts toward the sort but cannot on its
    own outrank a native build: a reader filtering this sheet wants the native ones at the top.
    """
    if field == "win_native":
        def score(r):
            return RANK.get(r["win_native"], 0) * 2 + (1 if r["win_wsl2"] == "Yes" else 0)
    else:
        def score(r):
            return RANK.get(r[field], 0)
    rows = [r for r in pool if score(r) > 0]
    rows.sort(key=lambda r: (-score(r), -r.get("stars", 0), r["name"].lower()))
    return rows


def platform_install(r, platform: str) -> str:
    """A `brew install` line is unusable on Windows. Point at the build the project publishes."""
    cmd = r.get("install_cmd") or ""
    if platform == "Windows" and r.get("install_method") == "brew" and r["win_native"] == "Yes":
        return f"{r['url']}/releases/latest"
    return cmd


def build_platform_sheet(wb, platform: str, field: str, headline: str, note: str,
                         rows, total: int, T, shots, theme: str):
    cols = [("#", 5.0), ("Project", 26.0), ("Screenshot", 42.14), ("★ Stars", 11.0),
            ("Lists", 7.0), ("Listed By", 30.0),
            ("Win\nNative", 9.0), ("Win\nWSL2", 9.0), ("macOS", 9.0), ("Linux", 9.0),
            ("Docker", 9.0), ("Cloud", 9.0), ("Conf.", 8.0),
            ("What It Does", 60.0), ("Install / Run", 50.0), ("Method", 11.0),
            ("Language", 12.0), ("License", 10.0), ("Last Push", 11.0),
            ("Why (evidence)", 42.0), ("Repo", 32.0)]
    ws = wb.create_sheet(platform)
    ws.sheet_properties.tabColor = T["good"] if platform != "Docker" else T["bar"]
    ws.sheet_view.showGridLines = False
    ncols = len(cols)
    last = 3 + len(rows)
    paint(ws, 1, last + 20, 1, ncols + 3, fill(T["surface"]))
    for i, (_n, w) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    title_band(ws, 1, ncols, T, f"{platform.upper()}  ·  {headline}",
               f"{len(rows):,} of {total:,} distinct repos  ·  every list at once, one row per "
               f"repo  ·  snapshot {date.today().isoformat()}")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    s = ws.cell(row=2, column=1, value=note)
    s.font = Font(name="Segoe UI", size=9, color=T["muted"])
    s.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
    ws.row_dimensions[2].height = 22
    header_row(ws, 3, cols_with_align(cols), T)
    ws.freeze_panes = "D4"
    ws.auto_filter.ref = f"A3:{get_column_letter(ncols)}{last}"

    f_muted = Font(name="Segoe UI", size=9, color=T["muted"])
    f_body = Font(name="Segoe UI", size=10, color=T["ink"])
    f_body2 = Font(name="Segoe UI", size=10, color=T["ink2"])
    f_mono = Font(name="Consolas", size=9, color=T["ink"])
    status = {
        "Yes": Font(name="Segoe UI", size=10, bold=True, color=T["good"]),
        "Likely": Font(name="Segoe UI", size=10, color=T["warn"]),
        "No": Font(name="Segoe UI", size=10, color=T["off"]),
        "n/a": Font(name="Segoe UI", size=10, color=T["muted"]),
        DASH: Font(name="Segoe UI", size=10, color=T["muted"]),
    }
    hair = side(T["grid"])
    ctr = Alignment(horizontal="center", vertical="center")
    top = Alignment(vertical="top", wrap_text=True)
    mid = Alignment(vertical="center", wrap_text=True, indent=1)

    for i, r in enumerate(rows):
        row = 4 + i
        ws.row_dimensions[row].height = SHOT_H * 0.75
        # the rail encodes this sheet's own verdict, because that is what the reader filtered on
        verdict = r[field] if field != "win_native" else (
            r["win_native"] if r["win_native"] in ("Yes", "Likely") else "WSL2")
        rail = {"Yes": T["good"], "Likely": T["warn"]}.get(verdict, T["bar"])
        band = T["band"] if i % 2 else T["surface"]
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = fill(band)
            cell.border = Border(bottom=hair)

        a = ws.cell(row=row, column=1, value=i + 1)
        a.font = f_muted
        a.alignment = ctr
        a.border = Border(bottom=hair, left=side(rail, "thick"))

        n = ws.cell(row=row, column=2, value=r["name"])
        n.font = Font(name="Segoe UI", size=11, bold=True, color=T["link"], underline="single")
        n.alignment = mid
        n.hyperlink = r["url"]
        n.border = Border(bottom=hair, left=side(rail, "thick"))

        ws.cell(row=row, column=3).alignment = ctr  # screenshot

        st = ws.cell(row=row, column=4, value=r.get("stars", 0))
        st.font = Font(name="Segoe UI", size=12, bold=True, color=T["ink"])
        st.number_format = "#,##0"
        st.alignment = Alignment(horizontal="right", vertical="center", indent=1)

        lc = ws.cell(row=row, column=5, value=r["list_count"])
        lc.font = Font(name="Segoe UI", size=11, bold=True,
                       color=T["good"] if r["list_count"] >= 3 else T["ink"])
        lc.alignment = ctr
        lb = ws.cell(row=row, column=6, value=r["listed_by"])
        lb.font = Font(name="Segoe UI", size=9, color=T["ink2"])
        lb.alignment = mid

        col = 7
        for kf in ("win_native", "win_wsl2", "macos", "linux", "docker", "cloud"):
            c2 = ws.cell(row=row, column=col, value=r[kf])
            c2.font = status.get(r[kf], f_body)
            c2.alignment = ctr
            col += 1
        cf = ws.cell(row=row, column=col, value=r.get("os_confidence") or DASH)
        cf.font = status["Yes"] if r.get("os_confidence") == "High" else (
            status["Likely"] if r.get("os_confidence") == "Medium" else status[DASH])
        cf.alignment = ctr
        col += 1

        d = ws.cell(row=row, column=col, value=r["blurb"])
        d.font = f_body
        d.alignment = top
        col += 1

        cmd = platform_install(r, platform)
        q = ws.cell(row=row, column=col, value=cmd or DASH)
        q.font = f_mono if cmd else f_muted
        q.alignment = mid
        col += 1

        for val, fnt in ((r.get("install_method") or DASH, f_muted),
                         (r.get("language") or DASH, f_body2),
                         (r.get("license") or DASH, f_muted),
                         (r.get("pushed_at") or DASH, f_muted)):
            c3 = ws.cell(row=row, column=col, value=val)
            c3.font = fnt
            c3.alignment = ctr
            col += 1

        wy = ws.cell(row=row, column=col, value=r.get("os_evidence") or DASH)
        wy.font = f_muted
        wy.alignment = top
        col += 1

        lk = ws.cell(row=row, column=col, value=r["nwo"])
        lk.font = Font(name="Segoe UI", size=9, color=T["link"], underline="single")
        lk.alignment = Alignment(vertical="center", indent=1)
        lk.hyperlink = r["url"]

    place_shots(ws, rows, shots, theme, T, 3, 4)
    ws.conditional_formatting.add(
        f"D4:D{last}",
        DataBarRule(start_type="num", start_value=0, end_type="percentile", end_value=90,
                    color=T["bar"], showValue=True))
    return ws


def cols_with_align(cols):
    """`header_row` reads (name, width, align) triples; the platform sheets centre every header."""
    return [(n, w, "center") for n, w in cols]


# ------------------------------------------------------------------ by category
CATEGORY_NOTE = (
    "One row per repo, every list at once, ordered by topic and then by stars — so filtering Category "
    "to one value gives that topic's leaderboard. Plugs Into is the second axis: cross the two to ask "
    "for the best Claude Code observability tool, or the best opencode plugin. A blank star cell means "
    "the row has no stars of its own to rank by — a folder inside someone else's repo, or a dead link.")


def build_category_sheet(wb, rows, T, shots, theme: str):
    """The cross-list topic sheet, and the one sheet built as a real Excel Table.

    A Table rather than a bare autofilter for two reasons. Structured references make `Category` a
    named thing a reader can filter without selecting a range first, and a slicer can only bind to a
    Table or a PivotCache — so this is what `18_slicers.py` attaches to afterwards. The table style is
    switched off entirely: the banding here is painted by hand to the theme, and a built-in style would
    fight it.
    """
    cols = [("Rank", 6.0), ("Project", 26.0), ("Screenshot", 42.14),
            ("Category", 24.0), ("Plugs Into", 28.0),
            ("Stars", 11.0), ("Lists", 7.0), ("Listed By", 26.0),
            ("Win", 8.0), ("WSL2", 8.0), ("macOS", 8.0), ("Linux", 8.0), ("Docker", 8.0),
            ("What It Does", 58.0), ("Install / Run", 46.0),
            ("Language", 12.0), ("License", 10.0), ("Last Push", 11.0), ("Repo", 30.0)]
    ws = wb.create_sheet("By Category")
    ws.sheet_properties.tabColor = T["bar"]
    ws.sheet_view.showGridLines = False
    ncols = len(cols)
    last = 3 + len(rows)
    paint(ws, 1, last + 20, 1, ncols + 3, fill(T["surface"]))
    for i, (_n, w) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ranked = sum(1 for r in rows if r["stars"])
    title_band(ws, 1, ncols, T, "BY CATEGORY  ·  every repo, one shared vocabulary",
               f"{len(rows):,} repos  ·  {len(tax.CATEGORIES)} topics  ·  {ranked:,} rankable  ·  "
               f"snapshot {date.today().isoformat()}")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    s = ws.cell(row=2, column=1, value=CATEGORY_NOTE)
    s.font = Font(name="Segoe UI", size=9, color=T["muted"])
    s.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
    ws.row_dimensions[2].height = 30
    header_row(ws, 3, cols_with_align(cols), T)
    ws.freeze_panes = "D4"

    f_muted = Font(name="Segoe UI", size=9, color=T["muted"])
    f_body = Font(name="Segoe UI", size=10, color=T["ink"])
    f_body2 = Font(name="Segoe UI", size=10, color=T["ink2"])
    f_mono = Font(name="Consolas", size=9, color=T["ink"])
    status = {
        "Yes": Font(name="Segoe UI", size=10, bold=True, color=T["good"]),
        "Likely": Font(name="Segoe UI", size=10, color=T["warn"]),
        "No": Font(name="Segoe UI", size=10, color=T["off"]),
        "n/a": Font(name="Segoe UI", size=10, color=T["muted"]),
        DASH: Font(name="Segoe UI", size=10, color=T["muted"]),
    }
    hair = side(T["grid"])
    ctr = Alignment(horizontal="center", vertical="center")
    top = Alignment(vertical="top", wrap_text=True)
    mid = Alignment(vertical="center", wrap_text=True, indent=1)

    # The rail alternates between two neutrals as the topic changes, so the fourteen blocks are visible
    # without inventing fourteen hues. The palette holds eight slots and its safety comes from never
    # reusing one, so colouring topics here would mean two topics sharing a colour in a fourteen-row
    # legend -- worse than no colour at all.
    seen: list[str] = []
    for i, r in enumerate(rows):
        row = 4 + i
        if r["category"] not in seen:
            seen.append(r["category"])
        rail = T["bar"] if len(seen) % 2 else T["plane"]
        ws.row_dimensions[row].height = SHOT_H * 0.75
        band = T["band"] if i % 2 else T["surface"]
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = fill(band)
            cell.border = Border(bottom=hair)

        a = ws.cell(row=row, column=1, value=r["cat_rank"])
        a.font = f_muted
        a.alignment = ctr
        a.border = Border(bottom=hair, left=side(rail, "thick"))

        n = ws.cell(row=row, column=2, value=r["name"])
        n.font = Font(name="Segoe UI", size=11, bold=True, color=T["link"], underline="single")
        n.alignment = mid
        n.hyperlink = r["url"]
        n.border = Border(bottom=hair, left=side(rail, "thick"))

        ws.cell(row=row, column=3).alignment = ctr  # screenshot

        cat = ws.cell(row=row, column=4, value=r["category"])
        cat.font = Font(name="Segoe UI", size=10, bold=True, color=T["ink"])
        cat.alignment = mid

        tg = ws.cell(row=row, column=5, value=", ".join(r["targets"]) or DASH)
        tg.font = f_muted if not r["targets"] else Font(name="Segoe UI", size=9, color=T["ink2"])
        tg.alignment = mid

        # Blank, not a dash: this column is numeric, sorted and data-barred, and a dash in it would
        # make Excel treat the whole column as text.
        st = ws.cell(row=row, column=6, value=r["stars"] or None)
        st.font = Font(name="Segoe UI", size=12, bold=True, color=T["ink"])
        st.number_format = "#,##0"
        st.alignment = Alignment(horizontal="right", vertical="center", indent=1)

        lc = ws.cell(row=row, column=7, value=r["list_count"])
        lc.font = Font(name="Segoe UI", size=11, bold=True,
                       color=T["good"] if r["list_count"] >= 3 else T["ink"])
        lc.alignment = ctr
        lb = ws.cell(row=row, column=8, value=r["listed_by"])
        lb.font = Font(name="Segoe UI", size=9, color=T["ink2"])
        lb.alignment = mid

        col = 9
        for kf in ("win_native", "win_wsl2", "macos", "linux", "docker"):
            c2 = ws.cell(row=row, column=col, value=r[kf])
            c2.font = status.get(r[kf], f_body)
            c2.alignment = ctr
            col += 1

        d = ws.cell(row=row, column=col, value=r["blurb"])
        d.font = f_body
        d.alignment = top
        col += 1

        cmd = r.get("install_cmd") or ""
        q = ws.cell(row=row, column=col, value=cmd or DASH)
        q.font = f_mono if cmd else f_muted
        q.alignment = mid
        col += 1

        for val, fnt in ((r.get("language") or DASH, f_body2),
                         (r.get("license") or DASH, f_muted),
                         (r.get("pushed_at") or DASH, f_muted)):
            c3 = ws.cell(row=row, column=col, value=val)
            c3.font = fnt
            c3.alignment = ctr
            col += 1

        lk = ws.cell(row=row, column=col, value=r["nwo"])
        lk.font = Font(name="Segoe UI", size=9, color=T["link"], underline="single")
        lk.alignment = Alignment(vertical="center", indent=1)
        lk.hyperlink = r["url"]

    place_shots(ws, rows, shots, theme, T, 3, 4)
    ws.conditional_formatting.add(
        f"F4:F{last}",
        DataBarRule(start_type="num", start_value=0, end_type="percentile", end_value=90,
                    color=T["bar"], showValue=True))
    table = Table(displayName=CATEGORY_TABLE, ref=f"A3:{get_column_letter(ncols)}{last}")
    table.tableStyleInfo = TableStyleInfo(name=None, showRowStripes=False, showColumnStripes=False,
                                         showFirstColumn=False, showLastColumn=False)
    ws.add_table(table)
    return ws


def category_rows(records, orch, label, meta):
    """Every repo, with a topic, its targets, and its rank inside that topic.

    Ordered by topic and then by stars, which is what makes filtering Category to one value produce
    that topic's leaderboard rather than an arbitrary slice of it.
    """
    tax.STARS.clear()
    tax.STARS.update(star_map(records, orch, meta))
    agg = tax.by_repo(records + [dict(x, source="orchestrators") for x in orch])
    rows = repo_pool(records, orch, label)
    for r in rows:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        r["stars"] = tax.STARS.get(r["nwo"], 0)
    rows.sort(key=lambda r: (tax.RANK[r["category"]], -r["stars"], r["name"].lower()))
    n: dict[str, int] = {}
    for r in rows:
        n[r["category"]] = n.get(r["category"], 0) + 1
        r["cat_rank"] = n[r["category"]]
    return rows


# ------------------------------------------------------------------ list stats
def plain_bar(T, title: str, data: Reference, cats: Reference, vmax: float) -> BarChart:
    """Magnitude, not identity -- so one sequential hue for every bar.

    There are more source lists than the eight categorical slots, and the bars
    are already named on the axis, so hue has no work to do here.
    """
    ch = BarChart()
    ch.type = "bar"
    ch.style = None
    ch.roundedCorners = False
    ch.varyColors = False
    ch.gapWidth = 50
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.legend = None
    ch.graphical_properties = b7.GraphicalProperties(solidFill=T["plane"])
    ch.graphical_properties.ln = b7.LineProperties(noFill=True)
    ch.plot_area.graphicalProperties = b7.GraphicalProperties(noFill=True)
    ch.plot_area.graphicalProperties.ln = b7.LineProperties(noFill=True)
    ch.title = title
    tp = ch.title.tx.rich.p[0]
    cp = b7.CharacterProperties(solidFill=T["ink"].lstrip("#"), sz=1100, b=True,
                                latin=b7.TFont(typeface="Segoe UI"))
    tp.pPr = b7.ParagraphProperties(defRPr=cp)
    for run in tp.r or []:
        run.rPr = cp
    ch.x_axis.delete = False
    ch.x_axis.title = None
    ch.x_axis.majorGridlines = None
    ch.x_axis.majorTickMark = "none"
    ch.x_axis.minorTickMark = "none"
    ch.x_axis.txPr = b7.chart_text(T["ink2"], 900)
    ch.x_axis.spPr = b7.GraphicalProperties(
        ln=b7.LineProperties(solidFill=T["grid"].lstrip("#"), w=9525))
    ch.x_axis.scaling.orientation = "maxMin"
    ch.y_axis.delete = True
    ch.y_axis.title = None
    ch.y_axis.majorGridlines = None
    ch.y_axis.scaling.min = 0
    ch.y_axis.scaling.max = vmax * 1.2
    ch.dLbls = b7.DataLabelList(showVal=True, showSerName=False, showCatName=False,
                                showLegendKey=False, showPercent=False, showBubbleSize=False)
    ch.dLbls.numFmt = "#,##0"
    ch.dLbls.dLblPos = "outEnd"
    ch.dLbls.txPr = b7.chart_text(T["ink"], 900, bold=True)
    ser = ch.series[0]
    ser.graphicalProperties = b7.GraphicalProperties(solidFill=T["bar"].lstrip("#"))
    ser.graphicalProperties.ln = b7.LineProperties(noFill=True)
    ch.width, ch.height = 15.0, 11.0
    return ch


def build_list_stats(wb, per_source, T):
    ws = wb.create_sheet("List Stats")
    ws.sheet_properties.tabColor = T["surface"]
    ws.sheet_view.showGridLines = False
    # Deep enough for the table *and* the two charts anchored two rows under it, which float over
    # cells rather than occupying them -- so the background has to be painted where they will land or
    # the dark theme shows a white slab behind them. A flat 48 covered that at eleven lists and stops
    # covering it around twenty-five.
    paint(ws, 1, max(48, len(per_source) + 24), 1, 15, fill(T["surface"]))
    for i, w in enumerate([3, 30, 11, 11, 11, 13, 13, 13, 11, 11, 11, 11, 11, 11], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.merge_cells("B2:N2")
    t = ws.cell(row=2, column=2, value="LIST STATS  ·  what each source contributed")
    t.font = Font(name="Segoe UI", size=16, bold=True, color=T["ink"])
    t.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[2].height = 30
    paint(ws, 2, 2, 1, 15, fill(T["plane"]))

    hdrs = ["Source List", "Items", "Repos", "Sections", "Total ★", "Median ★", "Top ★",
            "Win", "WSL2", "macOS", "Linux", "Docker", "Shots"]
    for i, h in enumerate(hdrs, start=2):
        c = ws.cell(row=4, column=i, value=h)
        c.fill = fill(T["header"])
        c.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=side(T["bar"], "medium"))
    ws.row_dimensions[4].height = 26

    row = 5
    # Column B is both the chip and the category axis of the two charts below it, so every list is
    # named twice over on this sheet; `plain_bar` already refuses to colour the bars for the same
    # reason, and a per-list hue on the chip would be the only unlabelled colour on the sheet.
    cs = list_chip(T)
    for r in per_source:
        chip = ws.cell(row=row, column=2, value=r["sheet"])
        chip.fill = fill(cs["chip_bg"])
        chip.font = Font(name="Segoe UI", size=9, bold=True, color=cs["chip_ink"])
        chip.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
        chip.border = Border(left=side(cs["hue"], "thick"), bottom=side(T["grid"]))
        for j, v in enumerate([r["items"], r["repos"], r["sections"], r["sum_stars"],
                               r["median_stars"], r["max_stars"], r["win"], r["wsl"],
                               r["mac"], r["lin"], r["doc"], r["shots"]], start=3):
            c = ws.cell(row=row, column=j, value=v)
            c.font = Font(name="Segoe UI", size=10, color=T["ink"])
            c.number_format = "#,##0"
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.border = Border(bottom=side(T["grid"]))
        ws.row_dimensions[row].height = 22
        row += 1

    cats = Reference(ws, min_col=2, min_row=5, max_row=row - 1)
    for col, title, anchor, vmax in (
        (3, "Items contributed per list", f"B{row + 2}",
         max(r["items"] for r in per_source)),
        (6, "Combined GitHub stars per list", f"I{row + 2}",
         max(r["sum_stars"] for r in per_source)),
    ):
        ws.add_chart(plain_bar(T, title, Reference(ws, min_col=col, min_row=4, max_row=row - 1),
                               cats, vmax), anchor)
    return ws


# ------------------------------------------------------------------ cover
def build_cover(wb, T, stats, per_source):
    ws = wb.create_sheet("Start Here", 0)
    ws.sheet_properties.tabColor = T["bar"]
    ws.sheet_view.showGridLines = False
    # Scales with the directory, which is one row per source list. The fixed 110 this replaces was
    # measured against a cover that listed eleven of them.
    paint(ws, 1, 100 + len(per_source), 1, 14, fill(T["surface"]))

    TILE_W = 32
    widths = [3, 22, 10, 17, 15, 17, 15, 16, 16, 16, 16, 16, 16, 6]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    assert all(widths[c] + widths[c + 1] == TILE_W for c in range(1, 13, 2)), widths
    BODY = 12

    def put(row, col, val, size=10, bold=False, color=None, span=1, align="left",
            wrap=False, italic=False):
        if span > 1:
            ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + span - 1)
        c = ws.cell(row=row, column=col, value=val)
        c.font = Font(name="Segoe UI", size=size, bold=bold, italic=italic,
                      color=color or T["ink"])
        c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap,
                                indent=1 if align == "left" else 0)
        return c

    def bullet_height(text: str, size: int) -> float:
        per_line = sum(widths[1:1 + BODY]) * (1.30 if size <= 9 else 1.12)
        lines = max(1, -(-len(text) // int(per_line)))
        return lines * (13 if size <= 9 else 15) + 3

    paint(ws, 1, 4, 1, 14, fill(T["plane"]))
    ws.row_dimensions[2].height = 40
    ws.row_dimensions[3].height = 32
    put(2, 2, f"{TITLE}  ·  {stats['lists']} AWESOME-LISTS IN ONE", size=23, bold=True, span=9)
    put(3, 2, f"{stats['lists']} curated awesome-lists merged into one workbook — "
              f"{stats['items']:,} items, {stats['repos']:,} distinct GitHub repos, "
              f"grouped by section and ranked by stars, each with a screenshot, "
              f"an install line and platform evidence.",
        size=10, color=T["ink2"], span=11, wrap=True)
    put(4, 2, f"Snapshot {date.today().isoformat()}  ·  every source list is credited on the "
              f"Sources sheet", size=9, color=T["muted"], span=9)

    row = 6
    put(row, 2, "AT A GLANCE", size=10, bold=True, color=T["muted"])
    other = "LIGHT" if T is THEMES["dark"] else "DARK"
    sw = put(row, 11, f"◐  Switch to the {other} theme  →", size=10, bold=True,
             color=T["link"], span=3, align="right")
    sw.font = Font(name="Segoe UI", size=10, bold=True, color=T["link"], underline="single")
    sw.hyperlink = f"{WORKBOOK}-{other}.xlsx"
    row += 1
    tiles = [
        (f"{stats['lists']}", "awesome-lists merged"),
        (f"{stats['items']:,}", "items catalogued"),
        (f"{stats['repos']:,}", "distinct GitHub repos"),
        (f"{stats['stars']:,}", "stars, deduplicated"),
        (f"{stats['shots']:,}", "rows with an image"),
        (f"{stats['multi']}", "named by 2+ lists"),
    ]
    for i, (big, label) in enumerate(tiles):
        col = 2 + i * 2
        last_tile = i == len(tiles) - 1
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + 1)
        ws.merge_cells(start_row=row + 1, start_column=col, end_row=row + 1, end_column=col + 1)
        v = ws.cell(row=row, column=col, value=big)
        v.font = Font(name="Segoe UI", size=22, bold=True, color=T["ink"])
        v.alignment = Alignment(horizontal="left", vertical="bottom", indent=1)
        l = ws.cell(row=row + 1, column=col, value=label)
        l.font = Font(name="Segoe UI", size=9, color=T["muted"])
        l.alignment = Alignment(horizontal="left", vertical="top", indent=1)
        for rr in (row, row + 1):
            for cc in (col, col + 1):
                c = ws.cell(row=rr, column=cc)
                c.fill = fill(T["band"])
                c.border = Border(
                    top=side(T["bar"], "medium") if rr == row else None,
                    right=side(T["surface"], "medium") if cc == col + 1 and not last_tile else None)
    ws.row_dimensions[row].height = 34
    ws.row_dimensions[row + 1].height = 18

    # ---- platform reach, on its own line because it is the question most readers arrive with
    row += 3
    put(row, 2, "BY PLATFORM  ·  distinct repos, confirmed or inferred", size=10, bold=True,
        color=T["muted"], span=6)
    row += 1
    pl = list(stats["platforms"].items())
    for i, (name, n) in enumerate(pl):
        col = 2 + i * 3
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + 2)
        c = ws.cell(row=row, column=col,
                    value=f"{name}   {n:,}   ({n / max(1, stats['pool']):.0%} of "
                          f"{stats['pool']:,})")
        c.font = Font(name="Segoe UI", size=11, bold=True, color=T["ink"])
        c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        for cc in range(col, col + 3):
            k = ws.cell(row=row, column=cc)
            k.fill = fill(T["band"])
            k.border = Border(left=side(T["good"] if name != "Docker" else T["bar"], "thick")
                              if cc == col else None)
    ws.row_dimensions[row].height = 26

    # ---- sheet directory
    row += 2
    put(row, 2, "WHAT'S IN THIS WORKBOOK", size=10, bold=True, color=T["muted"])
    row += 1
    for hdr, col, span in (("List", 2, 1), ("Items", 3, 1), ("Stars", 4, 1),
                           ("Source list", 5, 2), ("What's on it", 7, 7)):
        h = put(row, col, hdr, size=9, bold=True, color="FFFFFF", span=span)
        h.fill = fill(T["header"])
        for k in range(col, col + span):
            ws.cell(row=row, column=k).fill = fill(T["header"])
    row += 1
    cs = list_chip(T)
    for r in per_source:
        chip = put(row, 2, r["sheet"], size=9, bold=True, color=cs["chip_ink"])
        chip.fill = fill(cs["chip_bg"])
        chip.border = Border(left=side(cs["hue"], "thick"), bottom=side(T["grid"]))
        put(row, 3, r["items"], size=10, align="center")
        v = put(row, 4, r["sum_stars"], size=10, align="right")
        v.number_format = "#,##0"
        put(row, 5, r["nwo"], size=9, color=T["ink2"], span=2)
        put(row, 7, r["blurb"], size=9, color=T["muted"], span=7, wrap=True)
        for cc in range(3, 14):
            ws.cell(row=row, column=cc).border = Border(bottom=side(T["grid"]))
        ws.row_dimensions[row].height = 22
        row += 1

    # ---- the sheets that cut across every list rather than presenting one
    cross = [
        ("Leaderboard", 250, "every list",
         f"The most-starred projects across all {len(per_source)} lists, deduplicated, with how many "
         f"lists name each one."),
        ("By Category", stats["repos"], "every list",
         f"Every repo filed under one of {len(tax.CATEGORIES)} topics, ranked inside its topic. Filter "
         f"Category for one topic's leaderboard; add Plugs Into to cross the two axes."),
        *[(name, stats["platforms"][name], "every list",
           f"Every distinct repo that {headline}. One row per repo, strongest evidence first.")
          for name, _f, headline, _n in PLATFORMS],
        ("Category Stats", 0, "Orchestrators",
         "Charts for the original list: items, stars and platform reach per category."),
        ("List Stats", 0, "every list",
         "Items and stars contributed by each source list, and its platform totals."),
    ]
    # One fixed slot for the whole block -- a constant, not a counted index, so there is nothing for
    # `slot` to guard -- and now the only hue in this column, because the per-list rows above it went
    # neutral. It reads as the one distinction it actually is: this sheet belongs to no single list.
    # Beside per-list chips drawn from the same eight slots it used to collide with the eighth list,
    # and with every eighth list after it.
    cs = chip_style(T, SLOTS[-1][1 if T is THEMES["dark"] else 0])
    for name, count, scope, what in cross:
        chip = put(row, 2, name, size=9, bold=True, color=cs["chip_ink"])
        chip.fill = fill(cs["chip_bg"])
        chip.border = Border(left=side(cs["hue"], "thick"), bottom=side(T["grid"]))
        put(row, 3, f"{count:,}" if count else DASH, size=10, align="center")
        put(row, 4, DASH, size=10, align="right", color=T["muted"])
        put(row, 5, scope, size=9, color=T["ink2"], span=2)
        put(row, 7, what, size=9, color=T["muted"], span=7, wrap=True)
        for cc in range(3, 14):
            ws.cell(row=row, column=cc).border = Border(bottom=side(T["grid"]))
        ws.row_dimensions[row].height = 22
        row += 1

    row += 1
    put(row, 2, "HOW TO USE IT", size=10, bold=True, color=T["muted"])
    row += 1
    for line in [
        f'{len(SHEETS) + 1} lists have a sheet of their own, where rows are grouped by section, most stars '
        f'first inside each group. The rest reach you through the cross-list sheets below — every row of '
        f'every list is on "By Category", and "Sources" says which lists have their own sheet and which do not.',
        'Click any dropdown arrow in a header row to filter. Screenshots hide and reappear with their rows.',
        'On your own platform, start on the "Windows", "macOS", "Linux" or "Docker" sheet: every list at once, '
        'one row per repo, the ones with hard evidence at the top. Each carries all five platform columns, so '
        'you can check a second machine without leaving the sheet.',
        'Tighten any platform sheet by filtering Conf. → High, or its own column → Yes to drop the inferred rows.',
        'The "Group" column is the colour key; "Section" is the wording the original list used. Filter on either.',
        '"Leaderboard" ranks every project across all lists at once and shows how many lists name it — a rough consensus score.',
        'For "the best X", go to "By Category" and filter Category to one of the fourteen topics: the rows are already ranked '
        'inside each topic, so the filter is the leaderboard. Filter Plugs Into as well to ask both at once — Category = '
        'Observability & Evals plus Plugs Into = Claude Code is the best Claude Code observability tool.',
        '"Sources" credits every list this was built from. Start there if you want to follow the originals.',
        'Header rows and the first columns stay locked while you scroll. Clear filters with Data ▸ Clear.',
    ]:
        text = "•  " + line
        put(row, 2, text, size=10, color=T["ink2"], span=BODY, wrap=True)
        ws.row_dimensions[row].height = bullet_height(text, 10)
        row += 1

    row += 1
    put(row, 2, "HOW TO READ IT  (and where to distrust it)", size=10, bold=True, color=T["muted"])
    row += 1
    for line in [
        'Stars, language, licence and last-push come from the GitHub API at snapshot time and drift daily.',
        'OS columns are derived evidence, not a vendor matrix. "Why (evidence)" shows the reasoning for every row; Conf. rates it.',
        'Strongest signal is published release assets — a .msi or windows-amd64.zip proves native Windows, a lone .dmg disproves it. '
        'Then explicit README prose, then the install route, then the language runtime alone (which only ever earns "Likely").',
        f'{stats["site_rows"]:,} rows are hosted products with no public repo, and {stats["sub_rows"]:,} are items inside a larger '
        'repo (a template folder, a pattern write-up). Neither has stars or platform support of its own, so those cells show a dash '
        'rather than borrowing the parent\'s.',
        'Sections with more than eight groups were folded into eight colour groups, because the palette carries eight '
        'colourblind-safe hues and inventing a ninth would make two groups indistinguishable. The original section name is kept in its own column.',
        'Screenshots are the first usable image in the README; failing that the site\'s own social card, then a live capture of the '
        'site, then a plain name tile. A name tile means no image could be found — not that the project has no UI.',
        f'{stats["unavailable"]} listed repos now return an error from GitHub (deleted, renamed or made private). They are kept '
        'with a dash so nothing silently vanishes from the count.',
        'Lists overlap heavily. The same project can appear on several sheets; "Leaderboard" is the deduplicated view.',
    ]:
        text = "•  " + line
        put(row, 2, text, size=9, color=T["muted"], span=BODY, wrap=True)
        ws.row_dimensions[row].height = bullet_height(text, 9)
        row += 1

    row += 1
    put(row, 2, f"Theme: {'DARK' if T is THEMES['dark'] else 'LIGHT'}. The {other} theme is the "
                f"sibling file in this folder — use the switch at the top right. (Excel cannot "
                f"repaint a sheet without macros, so the two themes are two files with identical content.)",
        size=9, italic=True, color=T["muted"], span=BODY)
    return ws


# ------------------------------------------------------------------ data prep
def prepare(records, shots):
    for r in records:
        if r.get("license") in ("NOASSERTION", "NONE", "", None):
            r["license"] = ""
        r["shot_key"] = shot_key(r)
    return records


def shot_key(rec):
    import hashlib
    if rec["kind"] == "site":
        return "site__" + hashlib.sha1(rec["url"].encode()).hexdigest()[:16]
    base = (rec.get("nwo") or "x").replace("/", "__")
    if rec["kind"] == "subpath":
        return base + "__" + hashlib.sha1(rec["url"].encode()).hexdigest()[:10]
    return base


def canonicalise_nwo(records, orch, meta) -> int:
    """Give every repo the one name GitHub says it has, so a repo named twice is one row and not two.

    Two different ways the same repo arrives under two names, and both have to be folded or the
    leaderboard ranks it twice, the platform pool counts it twice, and the "listed by N lists"
    consensus score undercounts itself:

      Case. GitHub treats owner/repo case-insensitively, and the source tables were typed by hand, so
        three repos arrive as both `e2b-dev/E2B` and `e2b-dev/e2b`.
      Renames. A repo that moved keeps serving its old URL as a redirect, so lists written at
        different times name it differently and every one of them still works. Twenty repos are in here
        under a stale name -- `OpenDevin/OpenDevin`, `All-Hands-AI/OpenHands` and `OpenHands/OpenHands`
        are one project under three -- and `affaan-m/everything-claude-code` was on the leaderboard
        twice at 246,813 stars each, once as itself and once as `affaan-m/ECC`.

    `meta.json`'s `nameWithOwner` is the API's answer to both at once: it is what the repo is called
    now, whatever was asked for. Where a repo was never fetched there is no answer, and the first
    spelling seen wins so that at least the two spellings agree with each other.

    Called *after* `prepare`, deliberately. `shot_key` is derived from the original spelling and the
    files in cache/shots are named to match, so recomputing it here would break every lookup it fixed.
    """
    # Resolve through at most one hop, then trust the case pass. A rename chain long enough to matter
    # would have to have been re-fetched mid-chain, and following it blindly can loop: two repos that
    # swapped names would point at each other for ever.
    canon: dict[str, str] = {}
    for asked, m in meta.items():
        now = (m or {}).get("nameWithOwner") or asked
        canon[asked.lower()] = ((meta.get(now) or {}).get("nameWithOwner") or now)
    for k, v in list(canon.items()):
        canon.setdefault(v.lower(), v)

    everything = orch + records
    for r in everything:
        if r.get("nwo"):
            canon.setdefault(r["nwo"].lower(), r["nwo"])
    fixed = 0
    for r in everything:
        was = r.get("nwo")
        if not was:
            continue
        now = canon[was.lower()]
        if now != was:
            r["nwo"] = now
            r["owner"], _, r["repo"] = now.partition("/")
            # Only the plain repo URL. A link into a subpath or a release keeps its old spelling,
            # which still redirects, because rewriting just the prefix could invent a path.
            if r.get("url") == f"https://github.com/{was}":
                r["url"] = f"https://github.com/{now}"
            fixed += 1
    return fixed


def star_map(records, orch, meta) -> dict[str, int]:
    """One star count per repo — the only place this question gets answered.

    Three surfaces print a combined star figure — the workbook cover, the Markdown hub and the category
    report — and they were printing 12,494,678, 12,494,028 and 12,494,807. Each had summed a different
    set with a differently-sourced number: the rows the Leaderboard admits, the platform pool, and a
    per-repo maximum across listings. All three were defensible, no two agreed, and for the headline
    number on a cover that is simply wrong. So there is one map, built once, and everything reads it.

    `meta.json` wins, because it is what the API said and it does not vary by which listing was read
    first. Where it has no count — 82 repos, fetched before that field was recorded — the largest figure
    any listing carries stands in, since discarding real data in favour of a zero would be worse.

    Excluded, and both deliberately: a listing whose `kind` is `subpath` is a folder inside someone
    else's repo and has no stars of its own, and an `unavailable` repo has nothing to count. A repo that
    is a subpath on one list and a real entry on another still appears, via the real entry.

    Call after `canonicalise_nwo`, or a repo under two names appears twice.
    """
    meta_ci = {k.lower(): v for k, v in meta.items()}
    best: dict[str, int] = {}
    for r in list(records) + list(orch):
        nwo = r.get("nwo")
        if not nwo or r.get("kind") == "subpath" or r.get("unavailable"):
            continue
        api = (meta.get(nwo) or meta_ci.get(nwo.lower()) or {}).get("stargazerCount")
        best[nwo] = api or max(best.get(nwo, 0), r.get("stars") or 0)
    return {n: s for n, s in best.items() if s > 0}


def combined_stars(records, orch, meta) -> tuple[int, int]:
    """The collection's combined star count, and how many repos it is spread across."""
    stars = star_map(records, orch, meta)
    return sum(stars.values()), len(stars)


def order_rows(rows, source):
    idx = {b: i for i, b in enumerate(bucket_order(source))}
    rows.sort(key=lambda r: (idx.get(r["bucket"], 99), -r["stars"], r.get("src_order", 0),
                             r["name"].lower()))
    seen = {}
    for r in rows:
        seen[r["bucket"]] = seen.get(r["bucket"], 0) + 1
        r["group_rank"] = seen[r["bucket"]]
    return rows


def main() -> None:
    records = prepare(json.loads((CACHE / "records_all.json").read_text(encoding="utf-8")), None)
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    shots = json.loads((CACHE / "shots_all.json").read_text(encoding="utf-8"))
    orch = b7.prepare(json.loads((CACHE / "records.json").read_text(encoding="utf-8")))
    orch_shots = json.loads((CACHE / "shots.json").read_text(encoding="utf-8"))
    canonicalise_nwo(records, orch, meta)

    # Keyed on every source, not just the ten with a sheet, because the Sources sheet, List Stats
    # and the cover's directory each have to account for all of them. `build_list_sheet` still only
    # reads the SHEETS keys.
    by_source = {s["key"]: [r for r in records if r["source"] == s["key"]] for s in b10.SOURCES
                 if s["key"] != "orchestrators"}
    for k, rows in by_source.items():
        order_rows(rows, k)

    # --sample N builds a thin workbook for checking layout without the wait
    sample = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--sample=")), 0)
    if sample:
        for k in by_source:
            keep, seen = [], {}
            for r in by_source[k]:
                seen[r["bucket"]] = seen.get(r["bucket"], 0) + 1
                if seen[r["bucket"]] <= sample:
                    keep.append(r)
            by_source[k] = keep
        orch = orch[:sample * 4]
        records = [r for rows in by_source.values() for r in rows]

    # GitHub is case-insensitive about owners but reports one canonical spelling, and the source
    # tables were typed by hand -- so `shubhamsaboo/...` misses a record filed under `Shubhamsaboo`.
    meta_ci = {k.lower(): v for k, v in meta.items()}

    # ---- per-source summary, original list first
    def summarise(nwo, sheet, blurb, rows, sections, tab=None):
        m = meta.get(nwo) or meta_ci.get(nwo.lower()) or {}
        st = sorted((r["stars"] for r in rows if r["stars"] > 0), reverse=True)
        return dict(
            nwo=nwo, url=f"https://github.com/{nwo}", name=nwo.split("/")[-1],
            # `sheet` is the row's name -- it is the chip on three sheets and the category axis of
            # List Stats' two charts, so it has to be unique per list. `tab` is the different and
            # narrower question the Sources sheet's ninth column asks, which most lists answer with
            # a dash. Collapsing the two would have printed the same label on twenty-eight rows and
            # given the charts twenty-eight identical categories.
            owner=nwo.split("/")[0], sheet=sheet, tab=tab or sheet, kind="repo",
            # A hand-written blurb where there is one, else the list's own GitHub description. The
            # maintainer's one-liner is what the column asks for and it beats inventing prose for
            # twenty-eight lists or leaving the cell empty.
            blurb=blurb or (m.get("description") or "").strip(),
            shot_key=nwo.replace("/", "__"),
            # None, not 0: a list whose own repo was never fetched has an unknown star count, and
            # zero is a claim. `build_sources` renders it as a dash.
            stars=m.get("stargazerCount"),
            license=((m.get("licenseInfo") or {}).get("spdxId") or "").replace("NOASSERTION", ""),
            pushed=(m.get("pushedAt") or "")[:10],
            items=len(rows), repos=len({r["nwo"] for r in rows if r.get("nwo")}),
            sections=sections,
            sum_stars=sum(st), median_stars=st[len(st) // 2] if st else 0,
            max_stars=st[0] if st else 0,
            win=sum(1 for r in rows if r.get("win_native") == "Yes"),
            wsl=sum(1 for r in rows if r.get("win_wsl2") == "Yes"),
            mac=sum(1 for r in rows if r.get("macos") == "Yes"),
            lin=sum(1 for r in rows if r.get("linux") == "Yes"),
            doc=sum(1 for r in rows if r.get("docker") == "Yes"),
            shots=sum(1 for r in rows if shots.get(r.get("shot_key", ""), {}).get("light")
                      or orch_shots.get(r.get("nwo") or "", {}).get("shot_light")),
        )

    per_source = [summarise(
        "andyrewlee/awesome-agent-orchestrators", "Orchestrators",
        "The original list: tools that run several coding agents at once, with the "
        "fullest treatment — every OS column, every install route.",
        orch, len(b7.CAT_ORDER))]
    for key, title, nwo, blurb in SHEETS:
        per_source.append(summarise(nwo, title, blurb, by_source[key], len(bucket_order(key))))
    # Then every remaining list, largest contribution first. The sheet's own title bar says "every
    # list this workbook was built from" and `stats["lists"]` is drawn from this, so stopping at the
    # ten with sheets made both of those false the moment the atlas grew past them -- it credited ten
    # maintainers for the work of thirty-nine. These rows have no tab of their own to point at, which
    # the ninth column now says with a dash rather than by omitting the list.
    for s in sorted(b10.SOURCES, key=lambda s: -len(by_source.get(s["key"], ()))):
        if s["key"] == "orchestrators" or s["key"] in SHEET_TITLE:
            continue
        rows = by_source[s["key"]]
        per_source.append(summarise(s["nwo"], s["title"], None, rows,
                                    len(bucket_order(s["key"])) or len({r["bucket"] for r in rows}),
                                    tab=DASH))

    # ---- leaderboard: one row per repo across every list
    agg: dict[str, dict] = {}
    for r in records + [dict(x, source="orchestrators") for x in orch]:
        nwo = r.get("nwo") or ""
        if not nwo or r.get("kind") == "subpath" or r.get("unavailable"):
            continue
        if r.get("stars", 0) <= 0:
            continue
        a = agg.setdefault(nwo, dict(r))
        a.setdefault("sources", set())
        a["sources"].add(r["source"])
        if len(r.get("blurb") or r.get("description") or "") > len(a.get("blurb") or ""):
            a["blurb"] = r.get("blurb") or r.get("description") or ""
    label = LIST_TITLE
    board = []
    for nwo, a in agg.items():
        a["list_count"] = len(a["sources"])
        a["listed_by"] = ", ".join(sorted(label.get(s, s) for s in a["sources"]))
        a["shot_key"] = a.get("shot_key") or nwo.replace("/", "__")
        a["blurb"] = a.get("blurb") or a.get("description") or ""
        board.append(a)
    board.sort(key=lambda r: (-r["stars"], r["name"].lower()))
    board = board[:250]

    # ---- platform sheets: also one row per repo, but every repo, not just the starred ones
    all_shots = merged_shots(shots, orch_shots)
    pool = platform_pool(records, orch, label)
    by_platform = {name: platform_rows(pool, field) for name, field, *_ in PLATFORMS}
    by_cat = category_rows(records, orch, label, meta)

    total_stars, starred_repos = combined_stars(records, orch, meta)
    stats = dict(
        lists=len(per_source),
        items=len(records) + len(orch),
        repos=len({r["nwo"] for r in records if r.get("nwo")} | {r["nwo"] for r in orch}),
        stars=total_stars,
        starred=starred_repos,
        shots=sum(1 for r in records if shots.get(r["shot_key"], {}).get("light")) + len(orch),
        multi=sum(1 for a in agg.values() if len(a["sources"]) >= 2),
        site_rows=sum(1 for r in records if r["kind"] == "site"),
        sub_rows=sum(1 for r in records if r["kind"] == "subpath"),
        unavailable=sum(1 for r in records if r.get("unavailable")) +
                    sum(1 for r in orch if r.get("unavailable")),
        pool=len(pool),
        platforms={name: len(rows) for name, rows in by_platform.items()},
    )

    for theme in ("dark", "light"):
        T = THEMES[theme]
        wb = Workbook()
        wb.remove(wb.active)
        cat_style, _rep = b7.cat_styles(T)
        orch_stats = b7.make_stats(orch, orch_shots)

        build_sources(wb, per_source, meta, T, shots, theme)
        b7.build_main(wb, orch, T, cat_style, orch_shots)
        for key, *_ in SHEETS:
            build_list_sheet(wb, key, by_source[key], T, shots, theme)
        build_leaderboard(wb, board, T, shots, theme)
        # Directly after the leaderboard because it answers the question the leaderboard provokes:
        # the global ranking is one column of Category away from being fourteen rankings.
        build_category_sheet(wb, by_cat, T, all_shots, theme)
        # the cross-list platform sheets replace 07_build's orchestrators-only "Windows Picks":
        # every row that sheet held is in this Windows sheet, alongside the other ten lists.
        for name, field, headline, note in PLATFORMS:
            build_platform_sheet(wb, name, field, headline, note,
                                 by_platform[name], len(pool), T, all_shots, theme)
        b7.build_stats(wb, orch, T, cat_style, orch_stats)
        build_list_stats(wb, per_source, T)
        build_cover(wb, T, stats, per_source)
        wb.active = 0

        path = OUT / f"{WORKBOOK}-{theme.upper()}.xlsx"
        wb.save(path)
        print(f"{theme.upper():5s} -> {path.name}  {path.stat().st_size / 1e6:.1f} MB  "
              f"{len(wb.sheetnames)} sheets", flush=True)

    print(f"\nitems {stats['items']:,} · repos {stats['repos']:,} · "
          f"stars {stats['stars']:,} · multi-listed {stats['multi']}")
    print("platforms  " + "  ".join(f"{k} {v:,}" for k, v in stats["platforms"].items()))


if __name__ == "__main__":
    main()
