"""Attach Excel table slicers to the "By Category" sheet, by hand, after openpyxl has saved.

openpyxl cannot write a slicer. There is no slicer module in it at all -- the only trace of the feature
anywhere in the library is two extension URIs sitting in `openpyxl/xml/constants.py`, both labelled
'Slicer List', neither of them used. So a slicer has to be assembled as raw XML and injected into the
saved package, which is what this does.

Seven parts have to agree with each other, and a slicer appears only if all seven do:

  1. two new parts per slicer -- a cache (`xl/slicerCaches/`) and a view (`xl/slicers/`)
  2. `[Content_Types].xml`                 an Override for each new part
  3. `xl/workbook.xml`                     an extLst listing the caches
  4. `xl/_rels/workbook.xml.rels`          workbook -> each cache
  5. `xl/worksheets/sheetN.xml`            an extLst listing the sheet's slicers
  6. `xl/worksheets/_rels/sheetN.xml.rels` sheet -> the slicer part
  7. `xl/drawings/drawingN.xml`            an mc:AlternateContent graphic frame that draws it

The version split matters and is the thing most likely to be got wrong. Slicers arrived in Excel 2010
bound to PivotCaches (namespace x14, `2009/9/main`); binding one to a *table* arrived in Excel 2013 and
lives in x15 (`2010/11/main`) under different extension URIs. This workbook has no pivot tables, so
everything here is the 2013 flavour: `x15:slicerCaches` under `{46BE...}`, `x15:slicerList` under
`{3A4C...}`, `x15:tableSlicerCache`, and the `2012/slicer` drawing namespace. Using the 2010 URIs with a
table binding produces a file Excel offers to repair.

Which is why `--probe` exists. None of this can be validated from here: no schema check proves Excel
will open a file, and the failure mode is a repair prompt that silently drops parts it does not
understand -- on this workbook that would mean every embedded screenshot in it. So the geometry and the
XML are exercised first on a 9-row workbook that takes a second to build and a second to open.

    python scripts/18_slicers.py --probe          # writes slicer-probe.xlsx, open it by hand
    python scripts/18_slicers.py                  # inject into both real workbooks, in place
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKBOOK = "Awesome-Agentic-Atlas"

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
X14 = "http://schemas.microsoft.com/office/spreadsheetml/2009/9/main"
X15 = "http://schemas.microsoft.com/office/spreadsheetml/2010/11/main"
SLE15 = "http://schemas.microsoft.com/office/drawing/2012/slicer"

REL_CACHE = "http://schemas.microsoft.com/office/2007/relationships/slicerCache"
REL_SLICER = "http://schemas.microsoft.com/office/2007/relationships/slicer"
REL_DRAWING = f"{R}/drawing"
REL_TABLE = f"{R}/table"

# The workbook-level and sheet-level extension URIs for *table* slicers. Their x14 siblings
# ({BBE1A952-...} and {A8765BA9-...}) are the PivotTable ones; see the module docstring.
URI_WB_CACHES = "{46BE6895-7355-4a93-B00E-2C351335B9C9}"
URI_WS_LIST = "{3A4CF648-6AED-40f4-86FF-DC5316D8AED3}"
URI_TABLE_CACHE = "{2F2917AC-EB37-4324-AD4E-5DD8C200BD13}"

EMU_PER_PX = 9525
ROW_HEIGHT = 234950  # EMU, one slicer button. Excel's own default; changing it changes nothing else.


# ------------------------------------------------------------------ the XML
def cache_xml(cache_name: str, column: str, table_id: str, col_index: int) -> bytes:
    """One slicer cache: "this slicer reads column N of table T".

    `sourceName` is the column's header text and `column` is its 1-based position in the table. Both
    are required and Excel cross-checks them, so a renamed header with a stale index is a repair.
    """
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<slicerCacheDefinition xmlns="{X14}" xmlns:mc="{MC}" xmlns:x="{MAIN}" '
        f'xmlns:x15="{X15}" mc:Ignorable="x15" '
        f'name="{cache_name}" sourceName="{esc(column)}">'
        '<extLst>'
        f'<ext xmlns:x15="{X15}" uri="{URI_TABLE_CACHE}">'
        # Only the two required attributes and the sort. `customListSort` and `crossFilter` are
        # cosmetic and both default to what is wanted here, and every optional attribute is one more
        # suspect if Excel rejects the file -- which is the one thing that cannot be checked from here.
        f'<x15:tableSlicerCache tableId="{table_id}" column="{col_index}" sortOrder="ascending"/>'
        '</ext></extLst></slicerCacheDefinition>'
    ).encode("utf-8")


def slicers_xml(specs: list[dict], style: str) -> bytes:
    """The view side: caption, how many columns of buttons, which style. One part per sheet."""
    body = "".join(
        f'<slicer name="{esc(s["shape"])}" cache="{s["cache"]}" caption="{esc(s["caption"])}" '
        f'rowHeight="{ROW_HEIGHT}" columnCount="{s["button_cols"]}" style="{style}"/>'
        for s in specs)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<slicers xmlns="{X14}" xmlns:mc="{MC}" xmlns:x="{MAIN}" '
        f'xmlns:x15="{X15}" mc:Ignorable="x15">{body}</slicers>'
    ).encode("utf-8")


def wb_ext(rids: list[str]) -> str:
    caches = "".join(f'<x14:slicerCache xmlns:x14="{X14}" r:id="{rid}"/>' for rid in rids)
    return (f'<extLst><ext xmlns:x15="{X15}" uri="{URI_WB_CACHES}">'
            f'<x15:slicerCaches xmlns:r="{R}">{caches}</x15:slicerCaches></ext></extLst>')


def ws_ext(rid: str) -> str:
    return (f'<extLst><ext xmlns:x15="{X15}" uri="{URI_WS_LIST}">'
            f'<x15:slicerList xmlns:r="{R}">'
            f'<x14:slicer xmlns:x14="{X14}" r:id="{rid}"/>'
            '</x15:slicerList></ext></extLst>')


def anchor_xml(spec: dict, shape_id: int) -> str:
    """The drawing entry: a graphic frame wrapping a `sle15:slicer` reference, plus a fallback shape.

    `editAs="oneCell"` so the slicer moves with its cell but is not resized by it -- a slicer stretched
    to fit a row would be unreadable, and this sheet's rows are 100px tall to hold screenshots.

    The mc:Fallback is not decoration. Anything that reads xlsx and does not know the 2012 slicer
    namespace -- LibreOffice, Google Sheets, openpyxl itself on a later pass -- renders the fallback
    instead of discarding the anchor, which is what keeps this file readable outside Excel.
    """
    c1, r1, c2, r2 = spec["from_col"], spec["from_row"], spec["to_col"], spec["to_row"]
    return (
        '<twoCellAnchor editAs="oneCell">'
        f'<from><col>{c1}</col><colOff>{spec.get("from_off", 0)}</colOff>'
        f'<row>{r1}</row><rowOff>0</rowOff></from>'
        f'<to><col>{c2}</col><colOff>{spec.get("to_off", 0)}</colOff>'
        f'<row>{r2}</row><rowOff>0</rowOff></to>'
        f'<mc:AlternateContent xmlns:mc="{MC}">'
        f'<mc:Choice xmlns:sle15="{SLE15}" Requires="sle15">'
        '<graphicFrame macro="">'
        '<nvGraphicFramePr>'
        f'<cNvPr id="{shape_id}" name="{esc(spec["shape"])}"/>'
        '<cNvGraphicFramePr/>'
        '</nvGraphicFramePr>'
        f'<xfrm><a:off xmlns:a="{A}" x="0" y="0"/><a:ext xmlns:a="{A}" cx="0" cy="0"/></xfrm>'
        f'<a:graphic xmlns:a="{A}">'
        f'<a:graphicData uri="{SLE15}">'
        f'<sle15:slicer name="{esc(spec["shape"])}"/>'
        '</a:graphicData></a:graphic></graphicFrame>'
        '</mc:Choice>'
        '<mc:Fallback>'
        '<sp macro="" textlink="">'
        f'<nvSpPr><cNvPr id="{shape_id}" name="{esc(spec["shape"])}"/>'
        f'<cNvSpPr><a:spLocks xmlns:a="{A}" noTextEdit="1"/></cNvSpPr></nvSpPr>'
        f'<spPr><a:xfrm xmlns:a="{A}"><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm>'
        f'<a:prstGeom xmlns:a="{A}" prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill xmlns:a="{A}"><a:prstClr val="white"/></a:solidFill>'
        f'<a:ln xmlns:a="{A}" w="1"><a:solidFill><a:prstClr val="black"/></a:solidFill></a:ln>'
        '</spPr>'
        f'<txBody><a:bodyPr xmlns:a="{A}" vertOverflow="clip" horzOverflow="clip"/>'
        f'<a:lstStyle xmlns:a="{A}"/><a:p xmlns:a="{A}"><a:r><a:rPr lang="en-US" sz="900"/>'
        f'<a:t>{esc(spec["caption"])} slicer -- needs Excel 2013 or newer. '
        f'Use the filter arrow on the {esc(spec["column"])} header instead.</a:t></a:r></a:p></txBody>'
        '</sp>'
        '</mc:Fallback></mc:AlternateContent><clientData/></twoCellAnchor>'
    )


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ------------------------------------------------------------------ package surgery
def _rid(xml: str) -> str:
    """The next free rId in a rels part. Numbering is per-part, so this has to be read, not guessed."""
    used = [int(m) for m in re.findall(r'Id="rId(\d+)"', xml)]
    return f"rId{max(used, default=0) + 1}"


def _add_rel(xml: str, rid: str, type_: str, target: str) -> str:
    rel = f'<Relationship Type="{type_}" Target="{target}" Id="{rid}"/>'
    return xml.replace("</Relationships>", rel + "</Relationships>")


def _before_close(xml: str, tag: str, insert: str) -> str:
    """Put `insert` immediately before the closing `tag`, which for extLst is where the schema wants it.

    `CT_Worksheet` and `CT_Workbook` both end with extLst, after tableParts and after every other
    child, and Excel enforces child order strictly -- an extLst placed higher is a repair prompt.
    """
    close = f"</{tag}>"
    i = xml.rindex(close)
    return xml[:i] + insert + xml[i:]


def _before_first(xml: str, tags: tuple[str, ...], insert: str, fallback: str) -> str:
    """Put `insert` before whichever of `tags` appears first, or before `</fallback>` if none do.

    `CT_Worksheet` fixes the order of its children and Excel rejects them out of order, so a new
    `<drawing/>` cannot simply be appended -- `tableParts` and `extLst` both follow it.
    """
    at = min((xml.index(f"<{t}") for t in tags if f"<{t}" in xml), default=-1)
    if at < 0:
        return _before_close(xml, fallback, insert)
    return xml[:at] + insert + xml[at:]


def _resolve(target: str, base: str) -> str:
    """A rels Target to a package part name. openpyxl writes some absolute, some relative."""
    if target.startswith("/"):
        return target.lstrip("/")
    parts = (Path(base).parent / target).as_posix()
    while "/../" in parts:
        parts = re.sub(r"[^/]+/\.\./", "", parts, count=1)
    return parts


def inject(src: Path, sheet_name: str, table_name: str, layout: list[dict], style: str,
           dst: Path | None = None) -> Path:
    """Add one slicer per entry in `layout` to `sheet_name`, bound to `table_name`.

    Rewrites the whole package: a zip entry cannot be replaced in place, and every part that is not
    touched is copied across byte-for-byte. On the real workbook that is one entry per distinct
    screenshot -- roughly 2,000, where it was 7,388 before the build began sharing a picture between the
    sheets that show it (`media.py`) -- still the slow part, and the reason this is a separate stage
    rather than something the build does inline.
    """
    zin = zipfile.ZipFile(src)
    part = {n: zin.read(n) for n in zin.namelist() if not n.startswith("xl/media/")}

    wbx = part["xl/workbook.xml"].decode("utf-8")
    wbrels = part["xl/_rels/workbook.xml.rels"].decode("utf-8")

    # sheet name -> r:id -> part name. Never assume "By Category" is sheetN for any particular N;
    # openpyxl numbers parts by creation order and this sheet moved once already.
    m = re.search(rf'<sheet name="{re.escape(sheet_name)}"[^>]*r:id="(rId\d+)"', wbx)
    if not m:
        raise SystemExit(f"{src.name}: no sheet named {sheet_name!r}")
    sheet_rid = m.group(1)
    m = re.search(rf'<Relationship [^>]*Target="([^"]+)" Id="{sheet_rid}"', wbrels) or \
        re.search(rf'<Relationship [^>]*Id="{sheet_rid}"[^>]*Target="([^"]+)"', wbrels)
    ws_part = _resolve(m.group(1), "xl/workbook.xml")
    ws_rels_part = f"{Path(ws_part).parent.as_posix()}/_rels/{Path(ws_part).name}.rels"
    wsx = part[ws_part].decode("utf-8")
    wsrels = part[ws_rels_part].decode("utf-8")

    # the sheet's drawing part, and its table part, both via the sheet's own rels
    def _target(xml: str, type_: str) -> str:
        mm = re.search(rf'<Relationship Type="{re.escape(type_)}" Target="([^"]+)"', xml)
        return _resolve(mm.group(1), ws_part) if mm else ""

    dr_part = _target(wsrels, REL_DRAWING)
    tbl_part = _target(wsrels, REL_TABLE)
    if not tbl_part:
        raise SystemExit(f"{src.name}: sheet {sheet_name!r} has no table to bind a slicer to")
    new_ct = []
    if not dr_part:
        # A sheet with no pictures has no drawing part, and a slicer is drawn from one. True of the
        # probe and of any future sheet built without screenshots, so make one rather than refuse.
        used = [int(m.group(1)) for p in part
                if (m := re.fullmatch(r"xl/drawings/drawing(\d+)\.xml", p))]
        dr_part = f"xl/drawings/drawing{max(used, default=0) + 1}.xml"
        part[dr_part] = (f'<wsDr xmlns="http://schemas.openxmlformats.org/drawingml/2006/'
                         f'spreadsheetDrawing" xmlns:a="{A}" xmlns:r="{R}"></wsDr>').encode("utf-8")
        drid = _rid(wsrels)
        wsrels = _add_rel(wsrels, drid, REL_DRAWING, f"/{dr_part}")
        wsx = _before_first(wsx, ("tableParts", "extLst"),
                            f'<drawing xmlns:r="{R}" r:id="{drid}"/>', "worksheet")
        new_ct.append((dr_part,
                       "application/vnd.openxmlformats-officedocument.drawing+xml"))

    tblx = part[tbl_part].decode("utf-8")
    if f'displayName="{table_name}"' not in tblx:
        raise SystemExit(f"{src.name}: {tbl_part} is not {table_name!r}")
    table_id = re.search(r'<table id="(\d+)"', tblx).group(1)
    headers = re.findall(r'<tableColumn[^>]*name="([^"]*)"', tblx)

    # ---- build the new parts
    specs, cache_rids = [], []
    for i, spec in enumerate(layout, start=1):
        col = spec["column"]
        if col not in headers:
            raise SystemExit(f"{src.name}: table {table_name!r} has no column {col!r}")
        # A slicer's `name` is an identifier, not a label -- it is what the drawing's graphicFrame
        # refers to, and Excel writes underscores for spaces. `caption` is where the human text goes,
        # so "Plugs Into" becomes shape `Plugs_Into` captioned "Plugs into".
        ident = re.sub(r"[^A-Za-z0-9]", "_", col)
        s = dict(spec, cache=f"Slicer_{ident}", shape=spec.get("shape") or ident,
                 index=headers.index(col) + 1)
        cache_part = f"xl/slicerCaches/slicerCache{i}.xml"
        part[cache_part] = cache_xml(s["cache"], col, table_id, s["index"])
        rid = _rid(wbrels)
        wbrels = _add_rel(wbrels, rid, REL_CACHE, f"/{cache_part}")
        cache_rids.append(rid)
        specs.append(s)

    slicer_part = "xl/slicers/slicer1.xml"
    part[slicer_part] = slicers_xml(specs, style)
    srid = _rid(wsrels)
    wsrels = _add_rel(wsrels, srid, REL_SLICER, f"/{slicer_part}")

    # ---- patch the five existing parts
    part["xl/workbook.xml"] = _before_close(wbx, "workbook", wb_ext(cache_rids)).encode("utf-8")
    part["xl/_rels/workbook.xml.rels"] = wbrels.encode("utf-8")
    part[ws_part] = _before_close(wsx, "worksheet", ws_ext(srid)).encode("utf-8")
    part[ws_rels_part] = wsrels.encode("utf-8")

    drx = part[dr_part].decode("utf-8")
    # Shape ids only have to be unique within the drawing. The screenshots number from 1, so start
    # well past them rather than counting: there are thousands today and a different number tomorrow.
    base_id = 900000
    drx = _before_close(drx, "wsDr", "".join(
        anchor_xml(s, base_id + i) for i, s in enumerate(specs)))
    part[dr_part] = drx.encode("utf-8")

    ct = part["[Content_Types].xml"].decode("utf-8")
    overrides = "".join(
        f'<Override PartName="/{p}" ContentType="{c}"/>' for p, c in
        [(f"xl/slicerCaches/slicerCache{i}.xml", "application/vnd.ms-excel.slicerCache+xml")
         for i in range(1, len(specs) + 1)] +
        [(slicer_part, "application/vnd.ms-excel.slicer+xml")] + new_ct
        if f'PartName="/{p}"' not in ct)
    part["[Content_Types].xml"] = ct.replace("</Types>", overrides + "</Types>").encode("utf-8")

    # ---- write it out
    out = dst or src
    tmp = out.with_suffix(".slicers.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.filename in part:
                zout.writestr(info.filename, part.pop(info.filename))
            else:
                zout.writestr(info, zin.read(info.filename))
        for name, data in part.items():  # the parts that did not exist before
            zout.writestr(name, data)
    zin.close()
    shutil.move(str(tmp), str(out))
    return out


# ------------------------------------------------------------------ geometry
def layout_for(strip_rows: tuple[int, int], cols) -> list[dict]:
    """Where each slicer sits. Rows and columns are 1-based here and 0-based in the drawing.

    Kept next to the injector rather than in `16_build_all.py` so the reserved strip and the thing
    placed in it are read from one place; the build imports `SLICER_STRIP` from here.
    """
    top, bottom = strip_rows
    out = []
    for column, caption, c1, c2, button_cols in cols:
        out.append(dict(column=column, caption=caption, button_cols=button_cols,
                        from_col=c1 - 1, to_col=c2, from_row=top - 1, to_row=bottom))
    return out


# The strip of rows `16_build_all.build_category_sheet` leaves empty above its header, and the columns
# each slicer sits over. Both slicers stay inside the frozen top pane, so they remain on screen however
# far down the sheet you are -- a filter control you have to scroll back up to reach is a filter nobody
# uses.
SLICER_STRIP = (2, 6)
SLICER_COLS = [
    #  table column,  caption,      first col, last col, columns of buttons
    ("Category",     "Topic",              1, 3, 2),
    ("Plugs Into",   "Plugs into",         4, 5, 2),
]
STYLES = {"dark": "SlicerStyleDark1", "light": "SlicerStyleLight1"}


# ------------------------------------------------------------------ probe
def probe(path: Path) -> Path:
    """A 9-row workbook with the same slicers, for opening by hand.

    Deliberately tiny. The question it answers -- does Excel accept this XML, or offer to repair it --
    is the same question the 48 MB workbook asks, and it is the only question that cannot be answered
    without Excel. Repairing the real file would drop the screenshots.
    """
    from openpyxl import Workbook
    from openpyxl.worksheet.table import Table, TableStyleInfo

    rows = [
        ("Orchestrators & Multi-Agent", "n8n", 203229, "Claude / Anthropic"),
        ("Orchestrators & Multi-Agent", "Dify", 154335, "Claude / Anthropic"),
        ("Coding Agents", "OpenCode", 203467, "opencode, MCP"),
        ("Coding Agents", "Aider", 38000, "OpenAI / Codex"),
        ("Agent Skills", "Superpowers", 281176, "Claude Code"),
        ("Agent Skills", "andrej-karpathy-skills", 209837, "Claude Code"),
        ("MCP Servers", "modelcontextprotocol/servers", 90050, "MCP"),
        ("Observability & Evals", "Langfuse", 34156, "Claude Code, MCP"),
        ("Observability & Evals", "Braintrust", 1200, "OpenAI / Codex"),
    ]
    wb = Workbook()
    ws = wb.active
    ws.title = "By Category"
    ws["A1"] = "SLICER PROBE  ·  if Excel opens this without offering to repair it, the XML is right"
    for i, (c, n, s, t) in enumerate(rows):
        ws.cell(row=7 + i, column=1, value=c)
        ws.cell(row=7 + i, column=2, value=n)
        ws.cell(row=7 + i, column=3, value=s)
        ws.cell(row=7 + i, column=4, value=t)
    # header row at 6, so the strip is rows 2-5 -- one row shorter than the real sheet's, which only
    # changes how tall the slicers are drawn, not whether they load.
    for j, h in enumerate(("Category", "Project", "Stars", "Plugs Into"), start=1):
        ws.cell(row=6, column=j, value=h)
    for col, w in (("A", 30), ("B", 28), ("C", 12), ("D", 24)):
        ws.column_dimensions[col].width = w
    for r in range(2, 6):
        ws.row_dimensions[r].height = 26
    ws.freeze_panes = "A7"
    t = Table(displayName="ByCategory", ref=f"A6:D{6 + len(rows)}")
    t.tableStyleInfo = TableStyleInfo(name=None, showRowStripes=False, showColumnStripes=False,
                                      showFirstColumn=False, showLastColumn=False)
    ws.add_table(t)
    wb.save(path)
    inject(path, "By Category", "ByCategory",
           layout_for((2, 5), [("Category", "Topic", 1, 2, 1),
                               ("Plugs Into", "Plugs into", 3, 4, 1)]),
           STYLES["light"])
    return path


def main() -> None:
    if "--probe" in sys.argv:
        p = probe(ROOT / "slicer-probe.xlsx")
        print(f"probe -> {p}  {p.stat().st_size:,} bytes\n"
              f"open it. two slicers should appear above the table, and Excel should not "
              f"offer to repair anything.")
        return
    layout = layout_for(SLICER_STRIP, SLICER_COLS)
    for theme in ("dark", "light"):
        p = ROOT / f"{WORKBOOK}-{theme.upper()}.xlsx"
        before = p.stat().st_size
        inject(p, "By Category", CATEGORY_TABLE, layout, STYLES[theme])
        print(f"{theme.upper():5s} -> {p.name}  {before:,} -> {p.stat().st_size:,} bytes  "
              f"{len(layout)} slicers", flush=True)


CATEGORY_TABLE = "ByCategory"

if __name__ == "__main__":
    main()
