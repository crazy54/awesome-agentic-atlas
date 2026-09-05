"""When each repo first appeared in the atlas, and therefore what counts as new.

Nothing else in the pipeline remembers anything. Every stage stamps `date.today()` and rebuilds from
scratch, which is the right design for star counts and platform verdicts -- they are facts about now --
but it means the build cannot tell a repo that arrived this morning from one that has been here since
the first commit. So this module keeps the one piece of state the pipeline needs and does not otherwise
have: a ledger of the date each repo was first seen.

  state/first-seen.json   committed, one line per repo, grows by however many the lists add

Two rules make it safe to run on a clone that has never had it:

  * A repo already in the ledger is never re-stamped. The date is when it *arrived*, not when it was
    last built, so a repo that drops off a list and comes back is not new -- it returned.
  * Everything present at the baseline is stamped with the baseline itself, and "new" means
    `first_seen > baseline`. Without that, the first run of the ledger would mark all 1,294 repos as
    new on the same day and the filter would mean nothing for a fortnight.

The fourteen-day window is *not* applied here. `data.json` carries the raw first-seen date and the page
does the arithmetic, so a tag expires on its own fifteenth day in every open browser without anything
being rebuilt. If expiry needed a build, the cron would have to run daily to un-mark things even on the
days when no source list moved.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "state" / "first-seen.json"
SITE_DATA = ROOT / "docs" / "data.json"

WINDOW = 14

# nwo -> ISO date, post-baseline arrivals only. Populated by `resolve`, read by 17_markdown and
# 19_pages the way both already read `taxonomy.STARS`: one module-level map, filled once per build.
SEEN: dict[str, str] = {}


def today() -> str:
    return date.today().isoformat()


def blank(day: str) -> dict:
    return {"baseline": day, "window_days": WINDOW, "sources": {}, "repos": {}}


def load() -> dict:
    """The ledger, or an empty one dated today. Missing keys are filled so old files still load."""
    if not PATH.exists():
        return blank(today())
    state = json.loads(PATH.read_text(encoding="utf-8"))
    state.setdefault("baseline", today())
    state.setdefault("window_days", WINDOW)
    state.setdefault("sources", {})
    state.setdefault("repos", {})
    return state


def save(state: dict) -> None:
    PATH.parent.mkdir(parents=True, exist_ok=True)
    # Sorted and one key per line on purpose: this file is committed on every run that adds a repo, so
    # the diff should be the repos that arrived and nothing else.
    PATH.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def resolve(nwos, day: str | None = None) -> dict[str, str]:
    """Stamp unseen repos, persist, and return the post-baseline arrivals as `{nwo: first_seen}`.

    Idempotent, which is what lets both 17_markdown and 19_pages call it in the same build: whichever
    runs first writes the dates and the second finds them already there and agrees with it.

    With no ledger on disk this bootstraps instead of stamping -- baseline is today and every repo is
    dated to it, so a fresh clone reports nothing new rather than everything.
    """
    day = day or today()
    bootstrap = not PATH.exists()
    state = load()
    repos = state["repos"]
    stamp = state["baseline"] if bootstrap else day
    added = [n for n in dict.fromkeys(nwos) if n and n not in repos]
    for n in added:
        repos[n] = stamp
    if added or bootstrap:
        save(state)
    SEEN.clear()
    SEEN.update({n: d for n, d in repos.items() if d > state["baseline"]})
    return SEEN


def within(iso: str, day: str | None = None, window: int = WINDOW) -> bool:
    """Is `iso` inside the window ending today? Tolerates junk dates by calling them old."""
    if not iso:
        return False
    try:
        seen = datetime.fromisoformat(iso).date()
    except ValueError:
        return False
    end = datetime.fromisoformat(day).date() if day else date.today()
    return 0 <= (end - seen).days <= window


def pretty(iso: str) -> str:
    """ISO to the mm/dd/yy the three surfaces print. Empty stays empty."""
    if not iso or len(iso) < 10:
        return ""
    y, m, d = iso[:10].split("-")
    return f"{m}/{d}/{y[2:]}"


def mark(nwo: str, day: str | None = None) -> str:
    """The Markdown new-mark for a repo, or "". Sparkles because Markdown cannot carry the site's SVG.

    GitHub strips inline `<svg>` out of rendered Markdown, so the drawn two-tone star on the site is
    U+2728 here. Same mark, same words, the format each surface can actually render.
    """
    iso = SEEN.get(nwo, "")
    return f" ✨ <sub>New on {pretty(iso)}</sub>" if within(iso, day) else ""


def seed_from_site() -> dict:
    """Build the ledger from the committed `docs/data.json`.

    Used once, to start the ledger on a repo that already had 1,294 repos and no memory of when any of
    them arrived. The site snapshot date is the honest baseline: it is the day the build that produced
    those rows ran, and it is the last day on which "everything here is founding stock" was true.
    """
    data = json.loads(SITE_DATA.read_text(encoding="utf-8"))
    ix = data["cols"].index("nwo")
    day = data.get("snapshot") or today()
    state = blank(day)
    state["repos"] = {r[ix]: day for r in data["rows"] if r[ix]}
    return state


def main() -> None:
    if "--seed" in sys.argv:
        if PATH.exists() and "--force" not in sys.argv:
            sys.exit(f"{PATH.relative_to(ROOT).as_posix()} already exists; --force to rewrite")
        state = seed_from_site()
        save(state)
        print(f"seeded {len(state['repos']):,} repos at baseline {state['baseline']}")
        return

    state = load()
    fresh = {n: d for n, d in state["repos"].items() if d > state["baseline"]}
    live = {n: d for n, d in fresh.items() if within(d, window=state["window_days"])}
    print(f"baseline {state['baseline']} · {len(state['repos']):,} repos · "
          f"{len(state['sources'])} sources tracked")
    print(f"{len(fresh):,} arrived since the baseline · {len(live):,} inside the "
          f"{state['window_days']}-day window")
    for n, d in sorted(live.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        print(f"  {d}  {n}")


if __name__ == "__main__":
    main()
