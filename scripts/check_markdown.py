"""Lint the generated mega-list for the five ways this Markdown can be silently wrong.

Not a style check. Each of these renders without error on GitHub and is wrong anyway, which is why
it needs a machine to find it:

  1. `\\|` outside a table renders as a literal backslash-pipe. GFM only resolves that escape while
     it is splitting table cells.
  2. An unescaped `|` inside a table cell splits the row, so one project's description silently
     becomes three columns and every later cell shifts left.
  3. An in-page `](#anchor)` that does not match a heading is a link that goes nowhere. GitHub's
     slug rule keeps the gap where it removed punctuation, so a tidier slugifier produces dead links.
  4. A relative file link to a file that is not there.
  5. A file over 512 KB. GitHub serves it as a truncation notice with no table under it, which from
     the outside is indistinguishable from a page that renders -- the link works, the heading is
     there, the rows are not.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "mega-list"

# GitHub's own limit, and the backstop rather than the guardrail: `17_markdown.PAGE_CEILING` is well
# below this and is what a build actually trips over. Restated here instead of imported because that
# module pulls in the whole workbook builder and openpyxl with it, and a linter that needs Excel
# installed to check a link is a linter nobody runs. So this catches what the generator cannot -- a
# page committed by an older build, a hand edit, a future generator that never called `paginate`.
RENDER_LIMIT = 512 * 1024

UNESCAPED = re.compile(r"(?<!\\)\|")
PUNCT = re.compile(r"[^\w\- ]", re.UNICODE)


def anchor(text: str) -> str:
    """GitHub's heading-anchor rule, applied to the *rendered* heading text."""
    text = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", text)          # link -> its label
    text = re.sub(r"[*_`]", "", text)                          # emphasis markers
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return PUNCT.sub("", text.strip().lower()).replace(" ", "-")


def main() -> int:
    bad: list[str] = []
    for path in sorted(OUT.rglob("*.md")):
        rel = path.relative_to(OUT).as_posix()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        size = path.stat().st_size
        if size > RENDER_LIMIT:
            bad.append(f"{rel}  {size:,} bytes: over the {RENDER_LIMIT // 1024} KB at which GitHub "
                       f"stops rendering Markdown, so this page shows a truncation notice and none "
                       f"of its rows")

        width = 0
        for n, line in enumerate(lines, 1):
            table = line.startswith("|")

            if not table and "\\|" in line:
                bad.append(f"{rel}:{n}  escaped pipe outside a table: {line[:120]}")

            if table:
                cells = len(UNESCAPED.findall(line)) - 1
                if set(line) <= set("|-: "):                   # the header rule row
                    width = cells
                elif width and cells != width:
                    bad.append(f"{rel}:{n}  {cells} cells, table has {width}: {line[:120]}")
            else:
                width = 0

        heads = {anchor(ln[3:]) for ln in lines if ln.startswith("## ")}
        for a in re.findall(r"\]\(#([^)]+)\)", text):
            if a not in heads:
                bad.append(f"{rel}  dead anchor #{a}")

        for target in re.findall(r"\]\((?!https?:|#|mailto:)([^)#]+)", text):
            if not (path.parent / target).exists():
                bad.append(f"{rel}  dead link {target}")

    files = len(list(OUT.rglob("*.md")))
    if bad:
        print(f"{len(bad)} problems across {files} files\n")
        for b in bad[:60]:
            print("  " + b)
        if len(bad) > 60:
            print(f"  ... and {len(bad) - 60} more")
        return 1
    print(f"clean: {files} files, no stray escapes, no split table rows, no dead links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
