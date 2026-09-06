"""Work out a parse strategy for a list that is not in the atlas yet, without touching the cache.

Adding a source to `10_parse_sources.SOURCES` is four decisions -- which line shapes hold entries,
which heading depth names the category, which headings are front matter, and whether relative links
are real items -- and there is no way to know any of them without looking at the file. Before this
script the loop was: edit SOURCES, run the whole 19-stage pipeline, read 2,000 lines of output,
guess again. For the 45 candidate lists in JFH-202 that loop is the entire cost of the work.

So this does the same parse the build does, against a candidate strategy, on a copy downloaded to
`cache/candidates/`. Nothing here writes `cache/sources/` or `cache/sources/index.json`: a candidate
must not be able to leave a half-tested list looking to `pull_sources.py` like a pulled one.

  try_source.py --nwo owner/repo --headings         the heading tree, with what sits under each
  try_source.py --nwo owner/repo --mode bullet --cat-at 3
  try_source.py cache/candidates/punkpeye.json      a saved candidate, re-run
  try_source.py cache/candidates/punkpeye.json --sections   every section, with sample rows

`--headings` first, always. `cat_at` is whichever depth the shelf names live at, and the answer is
usually visible in one screen of that output; guessing it is what produces a list with one category
called the repo's own title.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
CAND = CACHE / "candidates"

sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("b10", HERE / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b10)

# Every other stage prints category names with `strip_emoji` already applied. This one must print
# headings verbatim -- their emoji are exactly what a `drop` key has to be written against -- and a
# Windows console is cp1252, where one 🔗 in a heading is an unhandled UnicodeEncodeError instead of
# the dump you asked for. Replace the character; the traceback shows nothing worth having.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TIMEOUT = 30
MAX_BYTES = 16_000_000
UA = {"User-Agent": "awesome-agentic-atlas try_source "
                    "(+https://github.com/crazy54/awesome-agentic-atlas)"}


# --- getting the file ------------------------------------------------------------------------
def readme_path(nwo: str) -> str:
    out = subprocess.run(["gh", "api", f"repos/{nwo}/readme", "--jq", ".path"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    path = out.stdout.strip()
    return path if out.returncode == 0 and path and "\n" not in path else "README.md"


def fetch(nwo: str, path: str) -> bytes:
    """Raw at HEAD. Same reasoning as `pull_sources.raw_bytes`: over about a megabyte
    `gh api repos/{nwo}/readme` returns a 200 whose content field is empty, and the biggest
    candidate in JFH-202 is 1.4 MB -- exactly the size that bug hides at."""
    url = f"https://raw.githubusercontent.com/{nwo}/HEAD/{urllib.parse.quote(path)}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        if r.status != 200:
            sys.exit(f"{url} -> HTTP {r.status}")
        data = r.read(MAX_BYTES + 1)
    if not data:
        sys.exit(f"{url} came back empty")
    if len(data) > MAX_BYTES:
        sys.exit(f"{url} is over the {MAX_BYTES:,}B cap")
    return data


def content_of(src: dict, refresh: bool) -> str:
    """The candidate's text, cached under `cache/candidates/` so iterating on a strategy is free.

    Extra `paths` are appended to the primary file, which is what `10_parse_sources.read_source`
    does for a real source: one source is one text however many files it arrived in, so a hub
    README plus four sub-documents parse as one list with one set of sections.
    """
    CAND.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, path in enumerate([None] + list(src.get("paths") or [])):
        flat = "readme" if path is None else path.strip("/").replace("/", "__")
        dest = CAND / f"{src['key']}__{flat}.md"
        if refresh or not dest.exists():
            real = readme_path(src["nwo"]) if path is None else path
            data = fetch(src["nwo"], real)
            dest.write_bytes(data)
            print(f"  fetched {real} -> {dest.relative_to(ROOT).as_posix()} ({len(data):,}B)")
        parts.append(dest.read_text(encoding="utf-8", errors="replace"))
    return "\n\n".join(parts)


# --- the heading tree -----------------------------------------------------------------------
def headings(text: str) -> None:
    """Every heading with the count of bullet and table-row lines beneath it.

    The counts are the point. A `##` with 300 bullets under it and a `###` with 12 answer `cat_at`
    between them, and a heading with none under it is either front matter for `drop` or a section
    whose entries this shape of line does not reach.
    """
    rows: list[tuple[int, str, int, int]] = []
    lvl = txt = None
    for raw in text.splitlines():
        line = raw.rstrip()
        mh = b10.MD_H.match(line)
        hh = None if mh else b10.HTML_H.match(line)
        if mh or hh:
            lvl = len(mh.group(1)) if mh else int(hh.group("lvl"))
            txt = b10.clean(mh.group("txt") if mh else hh.group("txt"))
            rows.append((lvl, txt, 0, 0))
            continue
        if not rows:
            continue
        d, t, b, tb = rows[-1]
        if b10.BULLET.match(line) and b10.LINK.search(line):
            rows[-1] = (d, t, b + 1, tb)
        elif b10.TABLE_ROW.match(line) and b10.LINK.search(line):
            rows[-1] = (d, t, b, tb + 1)

    per_level = Counter(d for d, _, _, _ in rows)
    linked = Counter()
    for d, _, b, tb in rows:
        linked[d] += b + tb
    print(f"{'depth':>5s} {'bullets':>7s} {'tblrows':>7s}  heading")
    for d, t, b, tb in rows:
        print(f"{'#' * d:>5s} {b or '':>7} {tb or '':>7}  {t[:88]}")
    print(f"\n{'depth':>5s} {'count':>5s} {'linked lines below':>18s}")
    for d in sorted(per_level):
        print(f"{'#' * d:>5s} {per_level[d]:5d} {linked[d]:18d}")
    print("\ncat_at is the depth whose headings name shelves -- usually the shallowest depth that has\n"
          "most of the linked lines under it. Headings with 0 of either are `drop` candidates.")


# --- reporting a parse ----------------------------------------------------------------------
def atlas_repos() -> tuple[set[str], str]:
    """Lower-cased nwo of every repo already in the atlas, for the marginal-new count.

    The local parse output first, and `docs/data.json` only when there is none. This used to read the
    committed `data.json` alone, on the reasoning that "new to the *published* atlas" is the honest
    number -- and that is true right up until the moment you start ingesting, at which point the
    published file is the atlas as it was several lists ago and every candidate scores against a
    baseline that no longer exists. That is not a small effect: during JFH-202 `data.json` stood at
    1,294 repos while the branch had already parsed 7,845, so a candidate whose entries were mostly
    repos the atlas had *just* taken on still reported them all as new. Ranking candidates by that
    number is how a set of lists holding 6,532 genuinely new repos got projected at 7,540 -- the
    per-list gains were counted as though they never overlapped each other, because against a stale
    baseline they never appeared to.

    Returns what it used along with the set, because a marginal count is meaningless without knowing
    which atlas it is marginal to.
    """
    live = [p for p in (CACHE / "entries_all.json", CACHE / "entries.json") if p.exists()]
    if live:
        have: set[str] = set()
        for p in live:
            have |= {(e.get("nwo") or "").lower() for e in
                     json.loads(p.read_text(encoding="utf-8")) if e.get("nwo")}
        return have, " + ".join(f"cache/{p.name}" for p in live)
    p = ROOT / "docs" / "data.json"
    if not p.exists():
        return set(), "nothing (no parse output and no published data.json)"
    d = json.loads(p.read_text(encoding="utf-8"))
    i = d["cols"].index("nwo")
    return {(r[i] or "").lower() for r in d["rows"] if r[i]}, "docs/data.json, the published atlas"


def report(src: dict, rows: list[dict], show_sections: bool) -> None:
    kinds = Counter(r["kind"] for r in rows)
    cats = Counter(r["category"] for r in rows)
    have, baseline = atlas_repos()
    mine = {r["nwo"].lower() for r in rows if r["nwo"]}
    new = mine - have

    print(f"\n{len(rows)} rows  ·  {kinds['repo']} repo / {kinds['subpath']} subpath / "
          f"{kinds['site']} site  ·  {len(cats)} sections")
    print(f"{len(mine)} distinct repos, {len(new)} new to the atlas "
          f"({len(mine) - len(new)} already in it)")
    print(f"  measured against {len(have):,} repos from {baseline}")

    blank = sum(1 for r in rows if not r["description"])
    uncat = cats.get("Uncategorised", 0)
    print(f"{blank} rows with no description  ·  {uncat} Uncategorised")
    if rows and uncat / len(rows) > 0.2:
        print("  ! over a fifth Uncategorised -- cat_at is probably wrong for this list")
    if not rows:
        print("  ! nothing parsed -- wrong `mode` for this list's line shapes")

    print(f"\n{'rows':>5s} {'new':>5s}  section")
    for c, n in cats.most_common():
        n_new = len({r["nwo"].lower() for r in rows if r["category"] == c and r["nwo"]} - have)
        print(f"{n:5d} {n_new:5d}  {c[:80]}")

    if show_sections:
        for c, _ in cats.most_common():
            print(f"\n--- {c}")
            for r in [r for r in rows if r["category"] == c][:4]:
                print(f"  {r['kind']:8s} {r['name'][:44]:44s} {r['url'][:66]}")
                if r["description"]:
                    print(f"           {r['description'][:96]}")

    # A name that long is nearly always a whole sentence captured as the link text, which means the
    # line shape matched something that is not an entry.
    longest = sorted(rows, key=lambda r: -len(r["name"]))[:3]
    if longest and len(longest[0]["name"]) > 60:
        print("\nsuspiciously long names (a matched line that is not an entry?):")
        for r in longest:
            if len(r["name"]) > 60:
                print(f"  {len(r['name']):3d}  {r['name'][:96]}")

    print("\nTaxonomy work this source still needs:")
    print(f"  taxonomy.SECTIONS: {len(cats)} keys, one per section above")
    if len(cats) > 8:
        print(f"  buckets.BUCKETS:   {len(cats)} sections must fold into <= 8 palette slots")
    print(f"  every key spelled ('{src['key']}', '<section>') exactly as printed above")


def load_candidate(path: Path) -> dict:
    src = json.loads(path.read_text(encoding="utf-8"))
    src["mode"] = set(src.get("mode") or ["bullet"])
    src["drop"] = set(src.get("drop") or [])
    return src


def save_candidate(src: dict) -> Path:
    CAND.mkdir(parents=True, exist_ok=True)
    out = CAND / f"{src['key']}.json"
    body = dict(src, mode=sorted(src["mode"]), drop=sorted(src["drop"]))
    out.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("candidate", nargs="?", type=Path, help="a saved candidate JSON")
    ap.add_argument("--nwo", help="owner/repo of the list, for a candidate built from flags")
    ap.add_argument("--key", help="source key (defaults to the repo name, lower-cased)")
    ap.add_argument("--mode", default="bullet",
                    help="comma list of bullet,table,heading,html_details")
    ap.add_argument("--cat-at", type=int, default=2, dest="cat_at")
    ap.add_argument("--drop", default="", help="comma list of headings to treat as front matter")
    ap.add_argument("--item-rel", action="store_true", dest="item_rel",
                    help="relative links are real items -- the list indexes its own repo")
    ap.add_argument("--paths", default="",
                    help="comma list of extra in-repo files holding entries, e.g. docs/README.agents.md")
    ap.add_argument("--headings", action="store_true", help="dump the heading tree and stop")
    ap.add_argument("--sections", action="store_true", help="sample rows per section")
    ap.add_argument("--refresh", action="store_true", help="re-download rather than reuse the copy")
    ap.add_argument("--save", action="store_true", help="write the candidate to cache/candidates/")
    args = ap.parse_args()

    if args.candidate:
        src = load_candidate(args.candidate)
    elif args.nwo:
        src = dict(key=args.key or args.nwo.split("/")[-1].lower().replace("awesome-", ""),
                   nwo=args.nwo, title=args.nwo, short=args.nwo.split("/")[-1],
                   file=args.nwo.replace("/", "_") + ".md",
                   mode={m.strip() for m in args.mode.split(",") if m.strip()},
                   cat_at=args.cat_at,
                   drop={d.strip().lower() for d in args.drop.split(",") if d.strip()},
                   item_rel=args.item_rel,
                   paths=[p.strip() for p in args.paths.split(",") if p.strip()])
    else:
        ap.error("give a candidate JSON path or --nwo")

    print(f"{src['key']}  ({src['nwo']})  mode={sorted(src['mode'])} cat_at={src['cat_at']} "
          f"item_rel={bool(src.get('item_rel'))} drop={len(src['drop'])}")
    text = content_of(src, args.refresh)
    print(f"  {len(text):,} characters, {len(text.splitlines()):,} lines")

    if args.headings:
        headings(text)
        return

    report(src, b10.parse(src, text), args.sections)
    if args.save:
        print(f"\nsaved -> {save_candidate(src).relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
