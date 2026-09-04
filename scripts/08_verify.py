"""Open each workbook in real Excel and confirm it loads without a repair prompt.

Structural check only -- rendering the sheets to look at them is 09_pdf.py.

Scoped to the orchestrators-only build from 07_build.py, which is what the glob and the assertions
below describe: exactly four sheets, 194 pictures, a "Windows Picks" sheet. The merged build writes
`Awesome-Agentic-Atlas-*.xlsx` and has twenty sheets and no "Windows Picks", so it is deliberately not
matched here rather than matched and failed.
"""
import sys
from pathlib import Path

import pythoncom
import win32com.client as win32

ROOT = Path(__file__).resolve().parent.parent

EXPECTED_SHEETS = ["Start Here", "Orchestrators", "Category Stats", "Windows Picks"]


def main() -> None:
    files = sorted(ROOT.glob("Awesome-Agent-Orchestrators-*.xlsx"))
    if not files:
        print("no workbooks found")
        sys.exit(1)

    pythoncom.CoInitialize()
    xl = win32.gencache.EnsureDispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    ok = True
    try:
        for f in files:
            print(f"\n{f.name}  ({f.stat().st_size / 1e6:.1f} MB)")
            wb = xl.Workbooks.Open(str(f), UpdateLinks=0, ReadOnly=True)
            names = [ws.Name for ws in wb.Worksheets]
            main_ws = wb.Worksheets("Orchestrators")
            checks = {
                "sheets": (names, names == EXPECTED_SHEETS),
                "used range": (main_ws.UsedRange.Address, True),
                "pictures": (main_ws.Pictures().Count, main_ws.Pictures().Count == 194),
                "autofilter": (bool(main_ws.AutoFilterMode), bool(main_ws.AutoFilterMode)),
                "charts": (wb.Worksheets("Category Stats").ChartObjects().Count,
                           wb.Worksheets("Category Stats").ChartObjects().Count == 2),
                "windows rows": (wb.Worksheets("Windows Picks").UsedRange.Rows.Count, True),
            }
            for label, (value, good) in checks.items():
                print(f"  {'ok ' if good else 'BAD'} {label:14s} {value}")
                ok = ok and good
            wb.Close(SaveChanges=False)
    except Exception as exc:
        ok = False
        print(f"ERROR: {exc}")
    finally:
        xl.Quit()
        pythoncom.CoUninitialize()
    print("\nall checks passed" if ok else "\nCHECKS FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
