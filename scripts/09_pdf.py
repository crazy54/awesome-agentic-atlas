"""Render each sheet to a one-page PDF via Excel's own print engine.

The clipboard route (CopyPicture -> chart -> Export) is timing-flaky and silently
writes empty PNGs. ExportAsFixedFormat is synchronous and always produces the
page, so this is what we look at.
"""
import sys
from pathlib import Path

import pythoncom
import win32com.client as win32

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"

# Both workbook families: the merged Atlas from 16_build_all and the orchestrators-only build from
# 07_build. Unlike 08_verify this script asserts nothing about which sheets it finds, so it renders
# whatever is there and does not need to know which build produced it.
WORKBOOKS = ("Awesome-Agentic-Atlas-*.xlsx", "Awesome-Agent-Orchestrators-*.xlsx")
OUT.mkdir(exist_ok=True)

XL_PDF = 0
LANDSCAPE = 2

# sheet -> (print area, output suffix)
PAGES = [
    ("Start Here", "$A$1:$N$42", "cover"),
    ("Orchestrators", "$A$1:$G$9", "main_left"),
    ("Orchestrators", "$H$1:$W$9", "main_right"),
    ("Category Stats", "$A$1:$M$36", "stats"),
    ("Windows Picks", "$A$1:$I$14", "windows"),
]


def used(ws, max_rows: int = 14) -> str:
    ur = ws.UsedRange
    r0, c0 = ur.Row, ur.Column
    nr = min(ur.Rows.Count, max_rows)
    nc = ur.Columns.Count
    return ws.Range(ws.Cells(r0, c0), ws.Cells(r0 + nr - 1, c0 + nc - 1)).Address


def render(ws, area: str | None, out: Path) -> bool:
    ps = ws.PageSetup
    ps.PrintArea = area or used(ws)
    ps.Orientation = LANDSCAPE
    ps.PrintGridlines = False
    ps.PrintHeadings = False
    ps.CenterHeader = ps.LeftHeader = ps.RightHeader = ""
    ps.CenterFooter = ps.LeftFooter = ps.RightFooter = ""
    for m in ("TopMargin", "BottomMargin", "LeftMargin", "RightMargin"):
        setattr(ps, m, 8)
    ps.Zoom = False
    ps.FitToPagesWide = 1
    ps.FitToPagesTall = 1
    try:
        ws.ExportAsFixedFormat(XL_PDF, str(out))
    except Exception as exc:
        print(f"    ! {out.name}: {exc}")
        return False
    return out.exists() and out.stat().st_size > 4000


def main() -> None:
    files = sorted(p for pat in WORKBOOKS for p in ROOT.glob(pat))
    pythoncom.CoInitialize()
    xl = win32.gencache.EnsureDispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    ok = True
    try:
        for f in files:
            theme = f.stem.rsplit("-", 1)[-1].lower()
            print(f"\n{f.name}")
            wb = xl.Workbooks.Open(str(f), UpdateLinks=0, ReadOnly=False)
            for sheet, area, tag in PAGES:
                out = OUT / f"{theme}_{tag}.pdf"
                good = render(wb.Worksheets(sheet), area, out)
                print(f"  {'ok ' if good else 'FAIL'} {out.name}")
                ok = ok and good
            wb.Close(SaveChanges=False)
    except Exception as exc:
        ok = False
        print(f"ERROR: {exc}")
    finally:
        xl.Quit()
        pythoncom.CoUninitialize()
    print("\npdfs:")
    for p in sorted(OUT.glob("*.pdf")):
        print(f"  {p.name}  {p.stat().st_size/1000:.0f} KB")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
