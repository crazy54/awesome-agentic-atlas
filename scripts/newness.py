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
  * Everything present at the baseline is stamped with the baseline itself, and nothing at or before
    the baseline is ever `New`. Without that, the first run of the ledger would mark every repo in the
    atlas as new on the same day and the filter would mean nothing.

WHAT `New` MEANS: THE MOST RECENT IMPORT, NOT THE LAST FORTNIGHT
---------------------------------------------------------------
`New` is the set of repos the *most recent import that brought any* added to the atlas -- one cohort,
named by its date in `state["cohort"]`. An import that brings repos supersedes the previous cohort, so
the mark is removed from last time's arrivals by the act of finding this time's. Nothing accumulates and
nothing has to be un-marked on a timer.

This replaced a fourteen-day window, and the difference is what the mark is *about*. A window answers
"did this arrive recently", which is a question about the calendar; the cohort answers "is this what the
last import brought", which is a question about the atlas. Only the second one can be true of a repo that
has existed on GitHub for three years and reached this site on Sunday -- which is the overwhelmingly
common case here, because repos arrive when a curator adds them to somebody's list, not when they are
written. The badge now means "new to this site", which is the only newness this pipeline can observe.

An import that adds nothing leaves the cohort alone. That is deliberate: the daily build runs whether or
not a source list moved, and letting a no-op run clear the mark would mean a Sunday's arrivals were
visible until Monday lunchtime and then silently were not. The mark moves when there is something newer
to move it to.

`WINDOW` is no longer that fourteen-day window; it is the stale bound on a cohort. If the pipeline stops
-- and it does; five consecutive builds failed in September 2026 on an unmapped upstream heading -- a
cohort with nothing to supersede it would otherwise go on claiming to be the latest news indefinitely.
Past `WINDOW` days with no newer import, `cohort()` returns "" and nothing is `New`. The page is told the
bound as well as the date, so an open browser expires a cohort without waiting for a build, which is the
one property of the old window worth keeping.

WHAT IS AND IS NOT MARKED
-------------------------
The ledger is keyed by `nwo`, and the site's index is one row per GitHub repo, so every row the homepage
lists is a row this module can mark. Two classes of arrival are outside it, both by construction:

  * `site` entries -- a product with a web page and no repository -- have no `nwo`. They are ~28% of the
    parsed rows and none of them become index rows, so nothing on the homepage goes unmarked because of
    this; but if the index ever grows to carry them, they arrive silently.
  * `subpath` entries -- one skill inside a skills monorepo -- carry their *parent* repo's `nwo`. Forty
    new skills inside a repo the atlas already knows add nothing to this ledger, and a genuinely new
    monorepo marks every subpath it brought at once. Both follow from one row per repo.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "state" / "first-seen.json"
SITE_DATA = ROOT / "docs" / "data.json"

# The stale bound on a cohort, not a recency window -- see the module docstring. A cohort this many days
# old with no later import to supersede it stops being `New`.
WINDOW = 14

# nwo -> ISO date, *every* post-baseline arrival and not only the current cohort. Populated by `resolve`,
# read by 17_markdown and 19_pages the way both already read `taxonomy.STARS`: one module-level map,
# filled once per build.
#
# Deliberately wider than `New`. The page needs a date on every arrival for two things the cohort alone
# cannot answer: printing when a row arrived, and the reader's own "since your last visit" count, which
# spans however many cohorts have landed since they were last here.
SEEN: dict[str, str] = {}

# The date of the cohort that is currently `New`, or "" when there is not one to show -- no import has
# added anything since the baseline, or the last one that did is now stale. Set by `resolve`; read as
# `newness.COHORT` by the stages that render the mark.
COHORT: str = ""


def today() -> str:
    return date.today().isoformat()


def blank(day: str) -> dict:
    # `cohort` starts at the baseline, which is the one value that means "nothing is New yet": `cohort()`
    # rejects any cohort at or before the baseline, so a ledger that has never seen an arrival cannot
    # mark one.
    return {"baseline": day, "cohort": day, "window_days": WINDOW, "sources": {}, "repos": {}}


def load() -> dict:
    """The ledger, or an empty one dated today. Missing keys are filled so old files still load."""
    if not PATH.exists():
        return blank(today())
    state = json.loads(PATH.read_text(encoding="utf-8"))
    state.setdefault("baseline", today())
    # A ledger written before cohorts existed has no `cohort` key. Defaulting it to the baseline is what
    # makes that file load as "nothing is New", rather than as a cohort dated 1970 or as a crash: the old
    # model's answer came from arithmetic on each row's date, so there is no previous cohort to recover
    # and inventing one would mark a set nobody imported.
    state.setdefault("cohort", state["baseline"])
    state.setdefault("window_days", WINDOW)
    state.setdefault("sources", {})
    state.setdefault("repos", {})
    return state


def cohort(state: dict | None = None, day: str | None = None) -> str:
    """The date of the cohort that is currently `New`, or "" if there is not one to show.

    Two ways to have none: no import has added a repo since the baseline, so `cohort` is still sitting on
    the baseline it was initialised to; or the last import that did add something is now older than
    `WINDOW` days with nothing having superseded it, which is the stale case the docstring describes.
    """
    state = state if state is not None else load()
    stamp = state.get("cohort") or ""
    if not stamp or stamp <= state["baseline"]:
        return ""
    return stamp if within(stamp, day, state.get("window_days", WINDOW)) else ""


def save(state: dict) -> None:
    PATH.parent.mkdir(parents=True, exist_ok=True)
    # Sorted and one key per line on purpose: this file is committed on every run that adds a repo, so
    # the diff should be the repos that arrived and nothing else.
    PATH.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def resolve(nwos, day: str | None = None, sources=None) -> dict[str, str]:
    """Stamp unseen repos, persist, and return the post-baseline arrivals as `{nwo: first_seen}`.

    Idempotent, which is what lets both 17_markdown and 19_pages call it in the same build: whichever
    runs first writes the dates and the second finds them already there and agrees with it.

    With no ledger on disk this bootstraps instead of stamping -- baseline is today and every repo is
    dated to it, so a fresh clone reports nothing new rather than everything.

    Stamping is not the same as marking. Every unseen repo gets a date; `New` is only the newest cohort
    of them, which is what `COHORT` names and what `SEEN` deliberately does not narrow to.

    `sources` is the nwo of every source list this build read. It no longer changes what gets stamped --
    it used to, and the note below says why it stopped -- but it still earns its place in the log: a run
    that reads twenty-eight lists for the first time and a run that picks up three repos from lists it
    already knew are the same event to this function and very different events to read about.

    ON NOT BASELINING A NEWLY-READ LIST
    -----------------------------------
    An earlier version stamped the repos of a first-time list at the *baseline* rather than at `day`, on
    the grounds that several thousand repos arriving because the atlas started reading twenty-eight new
    lists had not "arrived" anywhere -- and that marking 85% of the atlas `New` for a fortnight would
    make the badge mean "we ingested a list".

    The premise was right and the remedy is now the wrong one, because the cohort model removed the cost
    it was paying for. The fortnight is what made a large cohort intolerable: under a window, 7,400 marks
    sat there for fourteen days whatever else happened. A cohort is superseded by the next import that
    brings anything, so the same 7,400 are the answer to "what did the last import bring" for exactly as
    long as that is true, and stop being it the moment something newer lands. And the honest answer to
    "is this repo new to this site" is yes -- it is on the site today and it was not yesterday, which is
    the only newness this pipeline can observe at all.

    So the dodge is gone, and with it the case it could not get right: a build that both added a list and
    picked up genuine arrivals from the older ones used to baseline *both*, silently losing the badge on
    real arrivals to protect the badge from the bulk ones.
    """
    day = day or today()
    bootstrap = not PATH.exists()
    state = load()
    if bootstrap:
        # `load()` dates an absent ledger at the real `today()`, because it has no build to ask. Here there
        # is one, and `day` is what every other stage in this build is stamping. Left alone, a caller that
        # passes an explicit `day` earlier than today bootstraps a baseline in its own future, and then
        # `cohort()`'s `stamp <= baseline` test suppresses every cohort that build goes on to create.
        state["baseline"] = state["cohort"] = day
    repos = state["repos"]
    ingested = [] if bootstrap else sorted(set(sources or ()) - set(state["sources"]))
    # The bootstrap case is the one survivor of the paragraph above, and it is not the same case. With no
    # ledger at all there is no "before" to have arrived since, so every repo is founding stock: baseline
    # is today and the whole atlas is stamped to it. A fresh clone reports nothing new rather than
    # everything, which is what makes this safe to run anywhere.
    stamp = state["baseline"] if bootstrap else day
    added = [n for n in dict.fromkeys(nwos) if n and n not in repos]
    for n in added:
        repos[n] = stamp
    # The cohort moves only when something was added, and only outside the bootstrap -- see `cohort()` for
    # why a cohort at the baseline is no cohort at all.
    if added and not bootstrap:
        state["cohort"] = day
        if ingested:
            print(f"{len(ingested)} source list(s) read for the first time. The {len(added):,} repos "
                  f"they bring are the {day} cohort: new to the atlas, not new in the world, and marked "
                  f"until the next import that brings anything supersedes them.", flush=True)
        else:
            print(f"{len(added):,} repo(s) arrived, so {day} is the new cohort and the previous one "
                  f"stops being marked.", flush=True)
    if added or bootstrap:
        save(state)
    SEEN.clear()
    SEEN.update({n: d for n, d in repos.items() if d > state["baseline"]})
    global COHORT
    COHORT = cohort(state, day)
    return SEEN


def within(iso: str, day: str | None = None, window: int = WINDOW) -> bool:
    """Is `iso` inside the window ending today? Tolerates junk dates by calling them old.

    Used on a cohort date now rather than on a row's, which is the stale bound and not a definition of
    `New` -- see `cohort()`. A row is `New` because it belongs to the current cohort, never because its
    own date is recent.
    """
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


def mark(nwo: str) -> str:
    """The Markdown new-mark for a repo, or "". Sparkles because Markdown cannot carry the site's SVG.

    GitHub strips inline `<svg>` out of rendered Markdown, so the drawn two-tone star on the site is
    U+2728 here. Same mark, same words, the format each surface can actually render.

    Membership is `SEEN[nwo] == COHORT`, not `within(SEEN[nwo])`. Those two agreed under the old window
    and do not agree now: a repo that arrived eight days ago is inside the fortnight and is not what the
    last import brought. `COHORT` is "" until `resolve` has run, so a caller that forgot to resolve gets
    no marks rather than the wrong ones.
    """
    iso = SEEN.get(nwo, "")
    return f" ✨ <sub>Added {pretty(iso)}</sub>" if iso and iso == COHORT else ""


def seed_from_site() -> dict:
    """Build the ledger from the committed `docs/data.json`.

    Used once, to start the ledger on an atlas that was already thousands of repos deep with no memory
    of when any of them arrived. The site snapshot date is the honest baseline: it is the day the build
    that produced those rows ran, and it is the last day on which "everything here is founding stock"
    was true.
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
    now = cohort(state)
    live = {n: d for n, d in fresh.items() if d == now} if now else {}
    print(f"baseline {state['baseline']} · {len(state['repos']):,} repos · "
          f"{len(state['sources'])} sources tracked")
    # The two numbers answer different questions and are reported separately on purpose. `fresh` is every
    # arrival the ledger remembers; `live` is the one cohort the surfaces mark. A run where the second is
    # far smaller than the first is the normal steady state, not a fault.
    if now:
        print(f"{len(fresh):,} arrived since the baseline · {len(live):,} in the {now} cohort, "
              f"which is what is marked New")
    else:
        # Say which of the two reasons it is. "Nothing is New" with no cause reads as a bug in every case
        # including the one where it is correct.
        stamp = state.get("cohort") or ""
        why = ("no import has added a repo since the baseline" if not stamp or stamp <= state["baseline"]
               else f"the {stamp} cohort is past the {state['window_days']}-day stale bound with "
                    f"nothing having superseded it")
        print(f"{len(fresh):,} arrived since the baseline · nothing is marked New: {why}")
    for n, d in sorted(live.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        print(f"  {d}  {n}")


if __name__ == "__main__":
    main()
