"""Re-render the site from the committed `docs/data.json` instead of the build cache.

`19_pages.py` needs the cache: 4,800 fetched READMEs and screenshots, 64 MB, deliberately not committed.
That is the right trade for a data rebuild and the wrong one for everything else, because two of the
three reasons to touch the site have nothing to do with the data:

  * the page template changed -- colours, a new filter, a fixed selector
  * the first-seen ledger changed and the rows need to say so

Both are pure functions of files that *are* committed, so this stage does them from a clone with nothing
fetched. It rewrites the page shell from `19_pages.PAGE` and re-derives the `first_seen` column from
`state/first-seen.json`; it never touches a star count, a verdict or the snapshot date, because it has
no way to know whether those are still true.

  python scripts/19b_refresh.py

The daily cron does not need this -- the fourteen-day mark expires in the reader's browser, so no build
is required to un-mark anything. It exists for template work and for the case where the ledger was
edited by hand.

WHAT COMES FROM WHERE, because the page this renders is a mixture and nothing at the call site says so.
`substitute()` fills the template from two different eras of the repository at once:

  * from the *committed* `docs/data.json` -- `__COUNT__`, which is `len(rows)`; `__STARS__`, summed over
    those same rows; `__TOPICS__`; `__SNAPSHOT__`; and every row the table draws. This stage rebuilds no
    row and recounts nothing: `refresh_data` below re-derives one column and hands the rest straight
    through, because it has no crawl to check them against.
  * from the *live* checkout -- the template itself, `newness.WINDOW`, `state/first-seen.json`, the site
    URL, the analytics token. `19_pages.PAGE` is where that bites, and it does not bite through a
    placeholder: the sentences *around* `__COUNT__` spell the source count out in words, as literals.
    "eleven awesome-lists" in the meta description and the og:description, "eleven awesome-lists, merged"
    in the `<h1>`, "all eleven source lists are credited" in the footer, and `#the-eleven-lists` in the
    link out of it. Nothing substitutes those. They say whatever the template last said.

So there is a window in which this stage renders a page that contradicts itself: a twelfth list is added
to `10_parse_sources.SOURCES`, the template's prose is updated to match, and `docs/data.json` still holds
rows a crawl of eleven lists produced. Run this then and it publishes "1,294 agentic AI projects from
twelve awesome-lists" with a star total summed over eleven lists' worth of rows -- on the deploy branch,
served byte-for-byte, indexed. Both halves are honestly derived and the page is a lie, and the failure
looks exactly like a successful build. That is why `main()` compares the number of source lists the
committed rows were built from against the number this checkout configures, and exits rather than render
when they differ; see `check_sources` for how the first number is arrived at and why it is not exact.
`--allow-stale` proceeds anyway, for the case where the template fix is what you came for and you know
the count is about to be rebuilt from under it. (JFH-220)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"

sys.path.insert(0, str(HERE))
import newness  # noqa: E402

spec = importlib.util.spec_from_file_location("b19", HERE / "19_pages.py")
b19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b19)

# The render chain does not reach the parse stage -- `19_pages` loads `17_markdown` loads `16_build_all`,
# and none of the three imports `10_parse_sources`, because by the time a record reaches them it carries
# its provenance as a label and the parser has nothing left to say. So it is loaded here directly, for the
# reason `watch_sources.py` gives for doing the same: `SOURCES` is the single definition of which lists
# this project is built from, and a second copy of that number is a second thing to keep in step.
spec = importlib.util.spec_from_file_location("b10", HERE / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b10)


def source_labels(data: dict) -> set[str]:
    """Every distinct source list the committed rows were built from, by the label they carry.

    `data.json` records provenance per row as `listed_by` -- a comma-joined string of display labels,
    "AI Agents 2026, Agents (kyrolabs), Orchestrators" -- beside `lists`, the count of them. The set of
    those labels over every row is the nearest thing the committed file has to "how many lists is this
    dataset made of", which is the number the template's prose claims. `23_og.py` and `22_detail.py`
    both split this column exactly this way; this is its third reader.

    Indexed rather than guarded, deliberately. A `data.json` with no `listed_by` column is not something
    this stage can render anyway, and `ValueError: 'listed_by' is not in list` names that better than a
    count of zero, which would come back out of here looking like a real disagreement.
    """
    ix = data["cols"].index("listed_by")
    return {n.strip() for row in data["rows"] for n in row[ix].split(",") if n.strip()}


def check_sources(data: dict, configured: list[str], allow_stale: bool = False) -> int:
    """Stop, unless the rows on disk and the lists in the checkout agree on how many lists there are.

    The count is *implied*, not stated, and it is worth being precise about what it measures: the number
    of source lists that produced at least one surviving row. That is not the same claim as the number of
    lists configured. A source that parsed to nothing -- every entry a non-GitHub link, a cached README
    that arrived empty -- is configured, contributes no label, and would be reported here as a
    disagreement that is not one. It has not happened: every list configured when a build ran placed rows
    in it, and `10_parse_sources.py` exits rather than parse a source whose cached file is missing, so
    the way to contribute zero rows is to be a list of things this project does not index. If it does
    happen, the message below prints the labels it found, and `--allow-stale` is the way past it.

    The exact version is not available from here. Having the build write its own source count into
    `data.json` would make this an assertion instead of an inference, and writing a new field means
    writing the file, which needs the 64 MB crawl cache that this stage exists to do without.

    `state/first-seen.json` looks like the better authority, because its `sources` map states a number
    outright rather than implying one. It is not, twice over. `newness.load()` fills a missing `sources`
    with `{}`, so on a checkout that has never had the ledger -- the bare clone this stage is for -- it
    would imply zero sources and refuse every render. And it is written by `watch_sources.py --update`,
    keyed on the live `SOURCES` and meaning "this commit has been built", so it tracks the configuration
    on its own schedule. The rows are what `__COUNT__` and `__STARS__` are counted from, so the rows are
    the side of this comparison that has to be measured.
    """
    labels = source_labels(data)
    implied, live = len(labels), len(configured)
    if implied == live:
        return implied
    note = (
        f"{len(data['rows']):,} rows in docs/data.json were built from {implied} source list(s); "
        f"scripts/10_parse_sources.py configures {live}.\n"
        f"  the committed rows name:  {', '.join(sorted(labels))}\n"
        f"  the checkout configures:  {', '.join(sorted(configured))}\n"
        "Rendering now publishes a page that contradicts itself: the prose counts the lists this "
        "checkout has,\nwhile __COUNT__ and __STARS__ count the rows of a dataset built from a "
        "different number of them.\n"
        "  * let the next full rebuild write data.json from a crawl -- that resolves this by itself\n"
        "  * python scripts/19b_refresh.py --allow-stale, if the mixed page is genuinely what you want")
    if not allow_stale:
        sys.exit(note)
    # Loud, on stderr, and unconditional. The whole hazard is that this render looks like a good one, so
    # the one thing this branch may not do is let it look like a good one quietly.
    print("!! --allow-stale: rendering a page whose prose and whose rows disagree.\n" + note,
          file=sys.stderr)
    return implied


def refresh_data(data: dict, ledger: dict) -> tuple[dict, int]:
    """Put `first_seen` in the column list and a date in every row that has one. Returns (data, live)."""
    baseline = ledger["baseline"]
    seen = {n: d for n, d in ledger["repos"].items() if d > baseline}

    cols = list(data["cols"])
    if "first_seen" not in cols:
        cols.append("first_seen")
    nwo_at, seen_at, width = cols.index("nwo"), cols.index("first_seen"), len(cols)

    for row in data["rows"]:
        # Rows written before the column existed are one short; pad rather than assume, so this is safe
        # to run twice and safe to run on either shape.
        while len(row) < width:
            row.append("")
        row[seen_at] = seen.get(row[nwo_at], "")

    data["cols"] = cols
    data["window_days"] = newness.WINDOW
    data["baseline"] = baseline
    # Backfilled rather than left absent. This stage round-trips a `data.json` that may predate the key,
    # and "absent means 1" is only a documented fallback -- a consumer reading the published file should
    # find the number rather than have to know the rule. `setdefault`, so a future version 2 written by
    # `19_pages.py` survives a refresh instead of being reset to 1 by the stage that only re-renders.
    data.setdefault("schema_version", b19.SCHEMA_VERSION)
    # `generated` is deliberately *not* backfilled, unlike the key above. It is the instant these rows were
    # captured, this stage does not capture any, and the only values available here -- now, or the file's own
    # mtime -- would both be later than the truth and would therefore overstate how fresh the data is, which
    # is the failure JFH-207 exists to fix. A file that predates the key keeps none, and `stamp()` in the
    # page falls to `snapshot`, which is the same fact to the day and has always been in this file.
    live = sum(1 for r in data["rows"] if newness.within(r[seen_at]))
    return data, live


def render(data: dict) -> str:
    return b19.substitute(b19.PAGE, data, b19.REPO, b19.b17.SITE)


def reversion() -> None:
    """Re-run `24_pwa.py`, because this stage just rewrote a file the service worker precaches.

    `sw.js` carries `const VERSION`, a hash of the three precached files -- `index.html` among them. The
    browser decides whether to install a new worker by byte-comparing `sw.js` alone. So rewriting the page
    and stopping produces a repository that looks fine and is not: the worker is byte-identical, no update
    is detected, and every reader with the worker already installed keeps being served the *old* shell out
    of the old cache indefinitely, while the network serves the new one to everybody else.

    There is no self-healing path from that state, which is what makes it worth a subprocess here rather
    than a warning. The trigger for self-healing is a change to `sw.js`, and `sw.js` is the file that did
    not change. It took a peer session checking a live installed worker to find it; nothing in the build
    or the test suite noticed.

    Both workflows already run this stage after `19_pages.py`, so neither can make the mistake. This
    script was the only way to reach it.

    Hashing the working tree is correct *here* -- the bytes it hashes are the bytes this function's caller
    just wrote. It is not correct in general: running `24_pwa.py` to re-version for a commit picks up
    whatever else is dirty in the tree, which yields a version describing bytes nobody will ever be
    served. Re-version for a commit from a worktree at that commit.
    """
    r = subprocess.run([sys.executable, str(HERE / "24_pwa.py")],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        sys.exit(f"24_pwa.py failed, so docs/sw.js still describes the previous page:\n"
                 f"{r.stdout}{r.stderr}")
    for line in r.stdout.splitlines():
        if line.startswith("precache "):
            print(line)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--allow-stale", action="store_true",
                    help="render even when the committed rows and 10_parse_sources.SOURCES disagree "
                         "about how many source lists there are -- see check_sources")
    args = ap.parse_args()

    path = OUT / "data.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    # Before the first write, not after: a check that reports on a file it has already overwritten is a
    # description of the damage rather than a guard against it, and this stage rewrites the page that
    # gets served.
    lists = check_sources(data, [s["nwo"] for s in b10.SOURCES], args.allow_stale)
    ledger = newness.load()
    data, live = refresh_data(data, ledger)

    path.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    (OUT / "index.html").write_text(render(data), encoding="utf-8")
    reversion()

    for f in ("index.html", "data.json", "sw.js"):
        print(f"{f:12s} {(OUT / f).stat().st_size / 1024:8.1f} KB")
    fresh = sum(1 for n, d in ledger["repos"].items() if d > ledger["baseline"])
    print(f"{len(data['rows']):,} rows from {lists} source list(s) · "
          f"snapshot {data['snapshot']} (unchanged) · baseline {ledger['baseline']}")
    print(f"{fresh:,} arrived since the baseline · {live:,} inside the {newness.WINDOW}-day window")


if __name__ == "__main__":
    main()
