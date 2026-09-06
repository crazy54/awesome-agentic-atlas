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
"""
from __future__ import annotations

import importlib.util
import json
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
    live = sum(1 for r in data["rows"] if newness.within(r[seen_at]))
    return data, live


def render(data: dict) -> str:
    return b19.substitute(b19.PAGE, data, b19.REPO, b19.b17.SITE)


def main() -> None:
    path = OUT / "data.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    ledger = newness.load()
    data, live = refresh_data(data, ledger)

    path.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    (OUT / "index.html").write_text(render(data), encoding="utf-8")

    for f in ("index.html", "data.json"):
        print(f"{f:12s} {(OUT / f).stat().st_size / 1024:8.1f} KB")
    fresh = sum(1 for n, d in ledger["repos"].items() if d > ledger["baseline"])
    print(f"{len(data['rows']):,} rows · snapshot {data['snapshot']} (unchanged) · "
          f"baseline {ledger['baseline']}")
    print(f"{fresh:,} arrived since the baseline · {live:,} inside the {newness.WINDOW}-day window")


if __name__ == "__main__":
    main()
