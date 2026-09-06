"""The two numbers that move every day, on their own, so a detail page does not download the whole atlas.

  docs/live.json    {"snapshot": "<date>", "repos": {"<owner>/<name>": [stars, "<pushed>"]}}

  python scripts/19c_live.py                  read docs/data.json, write docs/live.json
  python scripts/19c_live.py --out DIR        write into DIR instead of docs/
  python scripts/19c_live.py --data FILE      read this data.json instead of DIR/data.json

  -- what this is for --

`22_detail.py` writes 1,294 per-repository pages and deliberately puts no volatile number in any of them:
`docs/` is committed verbatim on this deployment, so a star count in the markup is 1,294 files rewritten in
git every night. Its pages therefore fetch the star count, the last-push date and the snapshot date after
paint. Until JFH-222 they fetched them out of `docs/data.json` -- 569,096 bytes raw, 162,473 gzipped, all eighteen
columns of all 1,294 rows -- in order to read three values out of one row.

This is that row, for every repository, and nothing else:

  docs/data.json    569,096 raw    162,473 gzipped
  docs/live.json     57,418 raw     21,791 gzipped    7.5x smaller on the wire

Gzipped is the pair to quote. Pages serves both with `Content-Encoding: gzip` and offers no brotli, so the
gzipped figure is what a reader actually pays; the raw ratio is a different and larger number that nobody
is charged. And it is charged 1,294 times over, because these pages are 1,294 of the site's ~1,500 URLs
and the ones a search result lands somebody on cold.

  -- a separate stage, and not part of 22_detail.py --

JFH-222's own acceptance criteria asked for this to be emitted by `22_detail.py`, from the same in-memory
rows as the pages, on the grounds that two derivations of one number can drift. The conclusion is right and
the remedy is backwards here, for a reason that is specific to this pipeline: **`22_detail.py` runs weekly
and `data.json` is rebuilt daily.**

That is not an accident either. `daily.yml` leaves `22_detail.py` out on purpose -- its output is a pure
function of the parts of `data.json` that only move when somebody re-curates, so a daily run of it would
commit 1,294 unchanged files a day for ever. Hanging `live.json` off that stage would peg the star counts
on 1,294 detail pages to the weekly run while the index and the 156 facet pages moved daily, and publish a
page saying 4,010 stars next to a facet page saying 4,193 for the same repository, for up to six days at a
stretch. The drift the criterion was written to prevent is the drift that coupling would create.

So it is a stage of its own, in *both* workflows, after every stage that writes `data.json` -- `19_pages.py`,
which rewrites it, and `25_velocity.py`, which patches two columns and a `velocity` block into it -- so that
this is a projection of the copy that ships and not of an earlier one. There is no drift window in that
ordering: the step runs under `set -euo pipefail`, so either this reads the file those stages just wrote or
the build fails.
The ordering is a property of two files rather than of one function, which is the honest cost of the choice,
so it is commented at both call sites and asserted in `tests/live_test.py`, which fails if this stage stops
appearing in either workflow.

Two more things hold that ordering up without anybody having to remember it. Both workflows assert that
every tracked file under `docs/` was rewritten by the build and fail the job naming any that was not, and
`docs/live.json` is not on either skip list -- so dropping this stage from a workflow is a red build rather
than a file that silently freezes. And `19b_refresh.py`, the cache-free render path, rewrites `data.json`
without running this: that is safe, and it is safe for a checkable reason rather than by luck. It changes
`first_seen`, `window_days`, `baseline` and `schema_version` and hands every other cell through untouched;
it explicitly refuses to touch a star count, a push date or the snapshot, because it has no crawl to check
them against. None of the three values here is among the four it changes.

  -- the shape --

`{nwo: [stars, pushed]}` rather than `{nwo: {"stars": ..., "pushed": ...}}`: the object form is 30 KB of
repeated key names for 1,294 rows, and this file has exactly one reader, seventeen lines of
`docs/repo/detail.js`, which is written by the same repository. `data.json`'s own columnar `cols`/`rows`
shape is the more general answer to the same problem and is the wrong one at this size -- a `cols` array
for two columns costs more than it saves and buys a `indexOf` in the client for a lookup that is now a
single key access. `snapshot` is a sibling of `repos` rather than a member of it because it qualifies all
1,294 pairs at once; without it the page shows two dated figures with nothing saying they are dated.

Keys sorted by `nwo`, not left in `data.json`'s row order. Row order is star-descending, so it permutes
whenever two repositories swap rank -- which is most days -- and this file is rebuilt and committed daily
in a repository that keeps every delta for ever. Sorted, a day of moving stars rewrites values in place
and git stores the difference between the numbers rather than the difference between two orderings.

Measured, because a cost claim here should be a number: 13 generations of the real file with 60% of the
star counts perturbed each time and `git gc --aggressive --prune=now` after every commit, cost taken as
the slope across all 13 rather than any single delta -- 5,221 B per regeneration sorted, 10,499 B in rank
order, so 1.82 MB a year against 3.65 MB. Worth stating that the win is 2.0x and not the 11x the file's
57 KB would suggest: zlib deltas a permuted JSON object of short keys far better than a naive reading of
"the whole file moved" implies. Sorting also makes the file greppable and diffable by a human, which
`data.json` is not, and that is arguably the larger benefit of the two.

Bytes, deliberately: no indentation, no spaces after separators, `ensure_ascii=False`, and no trailing
newline -- the same four choices `19_pages.py` makes for `data.json`, and the reason this file has no line
endings for `core.autocrlf` to rewrite on a Windows checkout.
"""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The published filename, in one place, because `22_detail.py`'s client script fetches it by name and
# `24_pwa.py`'s service worker routes it by name. Three literals, one of them in JavaScript, is not
# something a rename would find.
NAME = "live.json"

# What a detail page reads, and the whole contract of this file. `nwo` is the key; the other two are the
# pair. Named rather than indexed because `25_velocity.py` appends columns to `data.json` after
# `19_pages.py` writes it, so a position is not a stable way to find a column here.
FIELDS = ("nwo", "stars", "pushed")


def rows(data: dict) -> list[tuple[str, int, str]]:
    """`(nwo, stars, pushed)` for every row, in the file's own order.

    Resolved by column name and loudly, because a missing column is the one failure that would otherwise
    produce a perfectly valid sidecar full of nulls: every detail page would then render "No stars
    recorded" and nothing anywhere would say why.
    """
    missing = [c for c in FIELDS if c not in data.get("cols", [])]
    if missing:
        raise SystemExit(f"docs/data.json has no {', '.join(missing)} column(s). Its cols are "
                         f"{', '.join(data.get('cols', [])) or '(none)'}. This stage reads exactly "
                         f"{', '.join(FIELDS)} and cannot invent them.")
    at = [data["cols"].index(c) for c in FIELDS]
    return [(r[at[0]], r[at[1]], r[at[2]]) for r in data["rows"]]


def sidecar(data: dict) -> dict:
    """The published document, ready to serialise.

    The duplicate check is not defensive padding. `22_detail.py` already exits rather than build two pages
    for one repository, because the second would overwrite the first; here a duplicate would be worse than
    that, because a `dict` silently keeps the last one and the file would look complete while carrying one
    repository's numbers under another's name. Same failure, same stage of the pipeline, so it is the same
    hard stop.
    """
    if "snapshot" not in data:
        raise SystemExit("docs/data.json carries no `snapshot`. That date is the qualifier that makes the "
                         "two figures on a detail page honest -- without it the page presents a dated "
                         "star count as a live one -- so this stage will not write a sidecar lacking it.")
    repos: dict[str, list] = {}
    for nwo, stars, pushed in rows(data):
        if nwo in repos:
            raise SystemExit(f"two rows in docs/data.json are both {nwo!r}. One of them would silently "
                             "replace the other in this file, and its numbers would be published under "
                             "the other's name. Resolve the duplicate in the dataset first.")
        repos[nwo] = [stars, pushed]
    # Sorted here rather than by `sort_keys=True` in `dumps`, so the ordering is a property of the document
    # this function returns and is visible to anything that inspects it instead of only to the bytes.
    return {"snapshot": data["snapshot"], "repos": dict(sorted(repos.items()))}


def dumps(doc: dict) -> str:
    """One line, no spaces, no escapes, no trailing newline. See the docstring."""
    return json.dumps(doc, separators=(",", ":"), ensure_ascii=False)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    # The same two flags `22_detail.py` carries, spelled the same way, so the sidecar and the pages it
    # serves can be generated into one scratch tree from one perturbed dataset by a test.
    ap.add_argument("--out", default=str(ROOT / "docs"), metavar="DIR",
                    help=f"write {NAME} into DIR instead of docs/")
    ap.add_argument("--data", default=None, metavar="FILE",
                    help="read this data.json instead of DIR/data.json")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    src = Path(args.data).resolve() if args.data else out / "data.json"
    if not src.exists():
        raise SystemExit(f"{src} is not there. This stage reads the dataset `19_pages.py` writes, so it "
                         "runs after that stage and cannot run before it.")
    data = json.loads(src.read_text(encoding="utf-8"))

    doc = sidecar(data)
    body = dumps(doc)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / NAME
    # newline="" so nothing is translated on a Windows checkout. There is nothing to translate -- the body
    # holds no newline at all -- and saying so is cheaper than the next reader wondering.
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        fh.write(body)

    raw = len(body.encode("utf-8"))
    wire = len(gzip.compress(body.encode("utf-8"), 9))
    src_raw = src.stat().st_size
    src_wire = len(gzip.compress(src.read_bytes().replace(b"\r\n", b"\n"), 9))
    print(f"{NAME:12s} {len(doc['repos']):,} repos · {raw:,} B raw · {wire:,} B gzipped · "
          f"snapshot {doc['snapshot']}")
    print(f"{src.name:12s} {len(data['rows']):,} rows · {src_raw:,} B raw · {src_wire:,} B gzipped · "
          f"{len(data['cols'])} columns")
    # The ratio on the wire, because that is the one a reader is charged. Printed rather than asserted:
    # the win is the reason this stage exists, so a run that stopped delivering it should say so out loud
    # on every build rather than wait for somebody to re-measure it.
    print(f"a detail page now fetches {src_wire / wire:.1f}x fewer bytes than it did before JFH-222 · "
          f"{len(doc['repos']):,} pages x {(src_wire - wire) / 1024:,.0f} KB saved on a cold arrival")
    print(f"not precached by the service worker, cached from the page's own fetch -- see 24_pwa.py")


if __name__ == "__main__":
    main()
