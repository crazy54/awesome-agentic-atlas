"""Publish Discover: one dated page of fifty projects a day, seven days at a time.

`scripts/discover.py` decides *which* fifty -- the rule, the rotation ledger and the day boundary all live
there and none of it is repeated here. This stage is the publishing half: it turns a week's plan into two
files, and it is the only thing that writes either of them.

  docs/discover.json           the plan, plus a compact card payload for every row in it
  docs/discover/index.html     the page: the current day's fifty, server-rendered
  state/discover.json          the rotation ledger, written only on a run that picked a new week

  python scripts/19d_discover.py            pick if the published plan does not reach today, else re-render
  python scripts/19d_discover.py --force    pick a fresh week regardless
  python scripts/19d_discover.py --day 2026-09-27 --out build-tmp/d   a dated dry run, off to one side

WHERE IT GOES IN A BUILD, AND WHY IT IS IN BOTH WORKFLOWS
--------------------------------------------------------
After `19_pages.py`, because that stage rewrites `docs/data.json` and this one reads it; before
`20_landing.py`, which puts this page's URL in the sitemap; before `24_pwa.py`, because the worker routes
`discover.json` and is versioned from what it caches.

In `weekly.yml` it picks the week -- the weekly runs on Sundays, which is what "a new seven days every
Sunday" means. In `daily.yml` it re-renders without re-picking: the picks are the week's and a daily run
that re-rolled them would give a reader a different fifty on Tuesday afternoon than Tuesday morning. What
the daily *does* refresh is the card payload, so a star count on a Discover card is Monday's rather than
last Sunday's. Dropping this stage from `daily.yml` would not fail anything loudly -- the page would simply
freeze its numbers for six days at a time -- so `tests/discover_test.py` asserts it is in both, the same
guard `19c_live.py` has for the same reason.

If the weekly fails on a Sunday -- and it has, seven runs in a row in September 2026 -- the first daily
that runs afterwards finds a plan that does not reach today and picks a fresh week starting from that day.
That is the right answer when a build is running at all: the rotation keeps moving and the ledger keeps its
record. `discover.for_day()`'s cycling is for the other failure, where nothing is building and the page has
to make do with the seven cohorts it was given; the two are different outages and each has its own answer.

THE PAGE IS RENDERED TWICE, ON PURPOSE
--------------------------------------
The day's fifty are written into the HTML by this stage *and* rendered in the browser by the page's own
script. That is two implementations of one card, which is a cost, and it buys three things that no single
implementation does:

  * The page works with no JavaScript, and a crawler sees fifty real links to fifty detail pages. A
    carousel built entirely in the browser publishes an empty `<div>` to everything that is not a browser,
    on the one page whose whole purpose is that the tail of this corpus gets seen.
  * It is correct after midnight. A page cached by the service worker, or a tab left open overnight, was
    rendered on a day that has ended; the script re-resolves the date in `TZ` and swaps the cohort. A
    build-time-only page would go on showing Sunday's fifty all week to exactly the readers who come back.
  * The first paint is the content. `discover.json` is ~90 KB and the markup is already there, so nothing
    on this page waits for a fetch -- and the script only touches the DOM when the date has actually moved.

The two are kept honest by a seam rather than by care: the browser half's pure functions are in one
`<script>` block of their own, marked `DISCOVER CORE`, which `tests/probe.mjs` evaluates on its own with no
DOM at all. It asserts the markup this file writes for a row is character-for-character what `cardHTML()`
produces for the same row, that `dayIn()` reproduces every instant in the plan's `probe` map, and that
`forDay()` agrees with `discover.for_day()`. A drift between the two halves is a failed assertion, not a
page that quietly disagrees with itself.

THE CARD PAYLOAD IS EMBEDDED RATHER THAN JOINED AGAINST data.json
-----------------------------------------------------------------
`discover.json` carries `name`, `cat`, `stars`, `lists`, `lang`, `first_seen` and a clipped `blurb` for
every row in the week -- about 350 rows, ~90 KB -- instead of a list of names the page resolves against
`docs/data.json`. `data.json` is 569 KB and rising, this page needs 350 of its 8,856 rows, and the reader
who lands on `/discover` from a search result has no reason to download the other 8,506. The same payload
is what lets the homepage's strip paint before the index's own data has arrived.

The cost of a copy is that it can go stale, and the answer is the daily re-render above: every build
rewrites the payload from the `data.json` in front of it while leaving the picks alone. The other cost is
that a row can leave the atlas mid-week -- dropped from every source list -- and a pick naming it would
link to a detail page this build did not write. Those picks are dropped from the day with a line in the
run's output, so a day is honestly forty-nine rather than a card pointing at a 404.

WHY A CLICK ON THE HOMEPAGE'S STRIP LANDS ON THE CARD IT CAME FROM
------------------------------------------------------------------
The strip on the homepage is a teaser for this page, and a teaser has an obvious cheap version: send every
click to the project's detail page and collect the clickthrough. This does the opposite. Each card there
links to `discover/#repo=<owner/name>`, and this page scrolls that card into the rail and focuses it, so
the click delivers the thing the reader was pointing at *and* the page it lives on. A reader who follows a
stale link -- yesterday's card, shared this morning -- gets told which day it was in and handed the
project, rather than a silent scroll to nothing.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"


# The same dynamic load `25_collections.py` documents: `19_pages` and `20_landing` are not identifiers, and
# both do their work under `if __name__` so importing them runs no build. An already-loaded copy is reused,
# because `20_landing.py` imports this module for its sitemap URLs and would otherwise execute the two big
# stages a second time under new module objects.
def _load(name: str, alias: str):
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, HERE / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


b19 = _load("19_pages.py", "b19")
b20 = _load("20_landing.py", "b20")

# `discover` is an identifier, so it needs none of that. It is the rule; nothing about which fifty get
# picked is decided in this file.
sys.path.insert(0, str(HERE))
import discover  # noqa: E402

SITE = b19.b17.SITE
REPO = b19.REPO
esc, clip, repo_path = b20.esc, b20.clip, b20.repo_path
ICON, HEAD_THEME, THEME_JS = b20.ICON, b20.HEAD_THEME, b20.THEME_JS

# The row fields a card draws, in the order `docs/discover.json` writes them. Column-oriented on the wire
# and objects in the browser, the same shape `data.json` uses and for the same reason: the key names would
# otherwise be repeated 350 times. The page reads them by name off `d.cols`, so appending a field here is
# safe and reordering is invisible.
CARD_COLS = ["name", "cat", "stars", "lists", "lang", "first_seen", "blurb"]

# A blurb on a card, not in a table cell. These are other people's one-line summaries and they run from six
# words to sixty; the rail gives each card a fixed width, so the long ones are clipped here rather than
# clamped in CSS -- the bytes are what this file is trying to keep down, and the full text is one click away
# on the project's own page.
BLURB = 260

# Which accent a card wears, by category. Colour here is a fact about the page rather than decoration: the
# one claim Discover makes is that all fourteen categories are in every day, and a rail that visibly
# alternates between five accents is that claim, visible without reading a single tag. Modulo, so a
# fifteenth category gets a colour instead of a crash.
ACCENTS = ["sky", "mint", "gold", "coral", "violet"]


def urls() -> list[str]:
    """Every URL this stage publishes. Imported by `20_landing.py` for the sitemap."""
    return [SITE + "discover/"]


def rows_of(data: dict) -> list[tuple[str, int]]:
    """`(nwo, cat)` for every row, which is the entire input to the rule."""
    ix = {c: i for i, c in enumerate(data["cols"])}
    return [(r[ix["nwo"]], r[ix["cat"]]) for r in data["rows"]]


def cards(data: dict) -> dict[str, list]:
    """Every row in the corpus as a `CARD_COLS` array, keyed by `nwo`. Narrowed to the week's picks later."""
    ix = {c: i for i, c in enumerate(data["cols"])}
    out = {}
    for r in data["rows"]:
        out[r[ix["nwo"]]] = [
            r[ix["name"]], r[ix["cat"]], r[ix["stars"]], r[ix["lists"]],
            r[ix["lang"]] or "", r[ix["first_seen"]] or "", clip(r[ix["blurb"]] or "", BLURB),
        ]
    return out


def cohort_of(data: dict) -> str:
    """The import that brought the current arrivals, or "" if there is not one worth marking.

    `19_pages.py` applies the stale bound before writing `data.json`, so an empty value here means either
    a build that predates cohorts or a cohort that has aged out -- and both read the same way on a card:
    nothing is new. Not recomputed: a second copy of that bound is a second thing to disagree with the
    index about what is new, on a page sitting next to it.
    """
    return data.get("cohort") or ""


def publish(data: dict, plan: dict, shown: dict | None = None) -> dict:
    """A week's plan plus everything the page needs to draw it, ready to be written as `discover.json`.

    Picks naming a row that is no longer in the corpus are dropped here rather than rendered: a card is a
    link to a detail page, and a build that did not write that page should not publish a link to it. This
    is only reachable on a re-render -- a plan picked from this same `data` cannot name a row it does not
    have -- which is exactly the mid-week case the docstring describes.

    The slot is then refilled by `discover.topup()`, because dropping alone leaves the day one short of the
    count the page prints in its own heading. `shown` is the ledger, read but never written: it decides
    which replacement has waited longest, and the rule for that lives in `discover.py` with every other
    decision about which rows get a turn.

    The refill persists without being stored anywhere new. `discover.json` is this stage's output *and* the
    `published` plan the next run reads, so tomorrow's re-render sees the substitute as an ordinary pick and
    leaves it alone -- it is only reconsidered if it too leaves the corpus.
    """
    known = cards(data)
    days, dropped = [], []
    for c in plan["days"]:
        keep = [n for n in c["picks"] if n in known]
        dropped += [n for n in c["picks"] if n not in known]
        days.append({"date": c["date"], "picks": keep})
    days, added = discover.topup(days, dict(rows_of(data)), shown or {}, plan["week"],
                                 plan.get("per_day", discover.PER_DAY))
    seen = {n for c in days for n in c["picks"]}
    return dict(plan, days=days, dropped=sorted(set(dropped)), added=sorted(set(added)),
                snapshot=data.get("snapshot", ""),
                cohort=cohort_of(data), window_days=data.get("window_days", 14),
                cats=[c["name"] for c in data.get("cats", [])],
                cols=CARD_COLS, rows={n: known[n] for n in sorted(seen)})


def pick(data: dict, day: str, force: bool = False,
         published: dict | None = None, state: dict | None = None) -> tuple[dict, dict | None]:
    """The plan to publish for `day`: the one already out there, or a fresh week.

    Returns `(published, state)`, where `state` is None when nothing was picked -- which is the signal to
    leave `state/discover.json` alone. Re-stamping the ledger on a re-render would move every row in the
    current week to the back of the queue a second time, which changes nothing about this week and quietly
    ages the whole corpus by a week every night.
    """
    rows = rows_of(data)
    if not force and published and discover.covers(published, day):
        # The ledger is passed for ordering a refill and nothing else -- `None` back means don't write it.
        return publish(data, published, (state or {}).get("shown", {})), None
    plan, state = discover.plan(rows, state if state is not None else discover.blank(), day)
    return publish(data, plan, state["shown"]), state


# ------------------------------------------------------------------ the page
def rel(tail: str = "") -> str:
    """A link out of `docs/discover/`. One level down, so everything site-wide is `../`."""
    return "../" + tail


def long_date(day: str) -> str:
    """`2026-09-21` as `Sunday 21 September 2026`, matching the page script's `Intl` call.

    Not `strftime("%A %-d %B %Y")`: `%-d` is a glibc extension and this runs on Windows too. Built from the
    parts instead, which is the same assembly the browser half does with `formatToParts`.
    """
    d = date.fromisoformat(day)
    return f"{d:%A} {d.day} {d:%B} {d.year}"


def card_html(nwo: str, row: list, i: int, cats: list[str], cohort: str) -> str:
    """One card. The canonical version: `cardHTML()` in the page's core block must match it exactly.

    Fields in `CARD_COLS` order, unpacked by name rather than by index so a field added to that list does
    not silently shift what this draws. `ix` is not cached across calls because there are fifty of them.
    """
    ix = {c: k for k, c in enumerate(CARD_COLS)}
    name, cat = row[ix["name"]], row[ix["cat"]]
    stars, lists = row[ix["stars"]], row[ix["lists"]]
    lang, first_seen, blurb = row[ix["lang"]], row[ix["first_seen"]], row[ix["blurb"]]
    isnew = bool(cohort) and first_seen == cohort
    label = cats[cat] if 0 <= cat < len(cats) else "Uncategorised"
    # Stars and language are what a reader uses to decide whether to click, and a project with neither is
    # not a broken row -- 41 of them have no language at all -- so each is omitted rather than dashed.
    meta = [f'<b>{stars:,}</b> stars'] if stars else []
    if lang:
        meta.append(esc(lang))
    meta.append(f"{lists} lists" if lists > 1 else "1 list")
    return (
        f'<article class="dcard{" nw" if isnew else ""}" id="d{i + 1}" data-project="{esc(nwo)}"'
        f' style="--card-accent:var(--accent-{ACCENTS[cat % len(ACCENTS)]})">'
        f'<p class="dtag"><span class="tag cat">{esc(label)}</span>'
        f'{"<span class=\"dnew\">New</span>" if isnew else ""}</p>'
        f'<h2><a href="{esc(rel(repo_path(nwo)))}">{esc(name)}</a></h2>'
        f'<a class="nwo" href="https://github.com/{esc(nwo)}">{esc(nwo)}</a>'
        f'<p class="dmeta">{" · ".join(meta)}</p>'
        f'<p class="desc">{esc(blurb)}</p>'
        f'<p class="dn">{i + 1} of __TOTAL__</p>'
        "</article>"
    )


def rail(published: dict, day: str) -> tuple[str, str, int]:
    """The fifty cards for `day`, the cohort date they came from, and how many there are."""
    shown, picks = discover.for_day(published, day)
    cats, cohort, rows = published["cats"], published["cohort"], published["rows"]
    html = "".join(card_html(n, rows[n], i, cats, cohort) for i, n in enumerate(picks))
    return html.replace("__TOTAL__", str(len(picks))), shown, len(picks)


def head(title: str, desc: str, url: str) -> str:
    """The `<head>`, the same shape `25_collections.py` writes, including the pre-paint theme resolution.

    No `og:image` of its own. `23_og.py` renders cards for the 26 facets and the repository card is the
    fallback every uncarded page here uses; a card for this page would have to name fifty projects that
    change daily, so it would be wrong within a day of being rendered.
    """
    card = f"https://opengraph.githubassets.com/1/{esc(REPO)}"
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{card}">
<meta property="og:image:alt" content="The Awesome Agentic Atlas repository on GitHub.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{card}">
<link rel="icon" href="{esc(rel(ICON))}" type="image/svg+xml">
{HEAD_THEME}<link rel="stylesheet" href="{esc(rel('pages.css'))}">
</head>
"""


# The browser half's pure functions, in a block of their own so `tests/probe.mjs` can evaluate them with no
# DOM. Everything here is a function of its arguments: no fetch, no `document`, no clock except the one
# passed in. `dayIn` is the whole reason this seam exists -- it is the second implementation of
# `discover.today()`, and the plan's `probe` map is what proves the two agree.
CORE_JS = r"""<script>
/* DISCOVER CORE. Pure functions, asserted directly by tests/probe.mjs. See scripts/19d_discover.py. */
const DISCOVER = (() => {
  // The date in a named zone, as ISO. Assembled from `formatToParts` rather than taken from a locale that
  // happens to format this way: `en-CA` does produce `2026-09-21` in every engine tested, and relying on
  // that is relying on a locale database to keep a shape nobody promised. The zone comes from the plan, so
  // this function has no opinion about which zone Discover rolls over in -- `scripts/discover.py` does.
  const dayIn = (tz, at) => {
    const p = {};
    for (const {type, value} of new Intl.DateTimeFormat("en-US", {
      timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(at)) p[type] = value;
    return p.year + "-" + p.month + "-" + p.day;
  };
  // Midnight-to-midnight in whole days, both sides read as UTC. `Date.UTC` on the parts rather than
  // `Date.parse`, which would take the offset of whatever zone the reader is in and land a day out for
  // anyone east of Greenwich.
  const asUTC = (iso) => {
    const [y, m, d] = iso.split("-").map(Number);
    return Date.UTC(y, m - 1, d);
  };
  const daysBetween = (a, b) => Math.round((asUTC(b) - asUTC(a)) / 86400000);
  // The cohort for a date: the one dated that day, or -- if the plan has run out because nothing is
  // building -- the one that day's offset lands on, cycling. `discover.for_day()` is the same arithmetic in
  // Python and tests/probe.mjs asserts the two agree on every date in a fortnight either side of a plan.
  // The `+ n) % n` is not decoration: a plain `%` on a date before the plan begins returns a negative
  // index, and `days[-1]` in JavaScript is `undefined` rather than the last element.
  const forDay = (plan, day) => {
    const days = (plan && plan.days) || [];
    if (!days.length) return null;
    const hit = days.find((c) => c.date === day);
    if (hit) return hit;
    const n = days.length;
    return days[((daysBetween(days[0].date, day) % n) + n) % n];
  };
  // `{name, cat, stars, ...}` from the wire's array, by name off `d.cols`. One pass, so a field appended to
  // CARD_COLS arrives here without this function being touched.
  const hydrate = (d) => {
    const out = {};
    for (const nwo of Object.keys(d.rows || {})) {
      const o = {nwo};
      d.cols.forEach((c, i) => { o[c] = d.rows[nwo][i]; });
      out[nwo] = o;
    }
    return out;
  };
  const ACCENTS = __ACCENTS__;
  const DEVICE_NAMES = __DEVICES__;
  // Verbatim from `19_pages.py`'s copy, which is verbatim from `22_detail.segment()`. Four copies of this
  // rule exist and they must agree exactly or a card links to a 404; `tests/detail-churn.mjs` is what holds
  // all four to the same answer on every row in the atlas.
  const segment = (s) => {
    if (s.startsWith(".")) s = "dot-" + s.slice(1);
    if (s.endsWith(".")) s = s.slice(0, -1) + "-dot";
    if (DEVICE_NAMES.includes(s.split(".")[0])) s = "dev-" + s;
    return s;
  };
  const detailURL = (nwo) => "../repo/" + nwo.toLowerCase().split("/").map(segment).join("/") + "/";
  // `&#x27;` for the apostrophe, not the `&#39;` the index's own esc() writes. The two are the same
  // character and render identically, which is exactly why this had to be pinned: Python's `html.escape`
  // -- which is what `esc()` in 20_landing.py is -- emits the hex form, four of the fifty cards on a
  // typical day have an apostrophe in the blurb, and a card rewritten after midnight with a decimal
  // entity in it is a silent byte-level divergence between two renderers of the same card. Nothing on
  // screen would have shown it; `tests/probe.mjs` compares the markup character for character and did.
  const esc = (s) => String(s === null || s === undefined ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
  const commas = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  // The card, and the contract with `card_html()` in scripts/19d_discover.py: same fields, same order,
  // same markup, character for character. tests/probe.mjs asserts that against the built page rather than
  // trusting this comment -- two renderers for one card is a cost paid for the no-JS page and the
  // after-midnight swap, and an unasserted contract is how that cost turns into a bug.
  const cardHTML = (r, i, total, cats, cohort) => {
    const isnew = !!cohort && r.first_seen === cohort;
    const label = r.cat >= 0 && r.cat < cats.length ? cats[r.cat] : "Uncategorised";
    const meta = [];
    if (r.stars) meta.push("<b>" + commas(r.stars) + "</b> stars");
    if (r.lang) meta.push(esc(r.lang));
    meta.push(r.lists > 1 ? r.lists + " lists" : "1 list");
    return '<article class="dcard' + (isnew ? " nw" : "") + '" id="d' + (i + 1) +
      '" data-project="' + esc(r.nwo) + '" style="--card-accent:var(--accent-' +
      ACCENTS[r.cat % ACCENTS.length] + ')">' +
      '<p class="dtag"><span class="tag cat">' + esc(label) + "</span>" +
      (isnew ? '<span class="dnew">New</span>' : "") + "</p>" +
      '<h2><a href="' + esc(detailURL(r.nwo)) + '">' + esc(r.name) + "</a></h2>" +
      '<a class="nwo" href="https://github.com/' + esc(r.nwo) + '">' + esc(r.nwo) + "</a>" +
      '<p class="dmeta">' + meta.join(" · ") + "</p>" +
      '<p class="desc">' + esc(r.blurb) + "</p>" +
      '<p class="dn">' + (i + 1) + " of " + total + "</p>" +
      "</article>";
  };
  // `Sunday 21 September 2026`, matching `long_date()` in the stage. UTC, because the string is a label for
  // a date that is already decided -- reading it in the reader's zone would print the day before for
  // anyone west of Greenwich.
  const longDate = (day) => {
    const p = {};
    for (const {type, value} of new Intl.DateTimeFormat("en-GB", {
      timeZone: "UTC", weekday: "long", day: "numeric", month: "long", year: "numeric",
    }).formatToParts(new Date(asUTC(day)))) p[type] = value;
    return p.weekday + " " + p.day + " " + p.month + " " + p.year;
  };
  // The instant a cohort runs out: the first quarter-hour mark at which `tz` is no longer on `day`.
  // Stepped rather than computed from an offset, for the reason this whole feature names a zone instead of
  // an offset -- an offset is a second implementation of the DST rule. Fifteen minutes is the granularity
  // every zone in the database uses, and the walk starts a day early and gives up after 75 hours, so it
  // terminates whatever zone it is handed. Used only to tell a reader elsewhere in the world when their
  // own clock reaches Chicago's midnight, so a null is a sentence not printed rather than a failure.
  const endOf = (tz, day) => {
    let t = Date.parse(day + "T00:00:00Z") - 86400000;
    for (let i = 0; i < 300; i++, t += 900000) if (dayIn(tz, new Date(t)) > day) return new Date(t);
    return null;
  };
  return {dayIn, daysBetween, forDay, hydrate, cardHTML, longDate, detailURL, esc, endOf, ACCENTS};
})();
</script>
"""

def core_js() -> str:
    """`CORE_JS` with its two literals filled in from the modules that own them.

    Neither is retyped. `ACCENTS` is this file's, and `DEVICE_NAMES` is `22_detail.py`'s -- the canonical
    copy of the slug rule's reserved list, sorted so the output is stable and the diff of a rebuilt page is
    the page rather than a reordered array. A fifth copy of that list that disagreed with the other four
    would link fifty cards a day at paths no build wrote, which is the one failure on this page a reader
    cannot work around.
    """
    devices = sorted(_load("22_detail.py", "b22").DEVICE_NAMES)
    return (CORE_JS.replace("__ACCENTS__", json.dumps(ACCENTS))
            .replace("__DEVICES__", json.dumps(devices)))


PAGE_JS = r"""<script>
(() => {
  const rail = document.getElementById("drail");
  const note = document.getElementById("dnote");
  const pos = document.getElementById("dpos");
  const line = document.getElementById("dline");
  // The date this page was rendered for, and the plan it was rendered from. Both are written into the
  // markup by the stage, so the script knows whether it has anything to do before it fetches anything.
  const BUILT = rail.dataset.day;
  let PLAN = null;
  let SHOWN = BUILT;

  // Which card the reader was pointed at. `#repo=owner/name` rather than a bare `#owner/name`: the
  // fragment on this site already carries `key=value` state on the index, and an id-shaped fragment would
  // make the browser try to scroll to an element named after a repository before the script ever runs.
  const wanted = () => {
    const m = /(?:^|[#&])repo=([^&]+)/.exec(location.hash || "");
    return m ? decodeURIComponent(m[1]) : "";
  };

  const cards = () => [...rail.querySelectorAll(".dcard")];

  // Which card is under the rail's left edge. Read from geometry rather than counted from a scroll
  // position divided by a card width: the cards are a flex line with a gap and the last one is short, so
  // the arithmetic version is off by one at the end of every rail.
  const current = () => {
    const left = rail.getBoundingClientRect().left;
    let best = 0, gap = Infinity;
    cards().forEach((c, i) => {
      const d = Math.abs(c.getBoundingClientRect().left - left);
      if (d < gap) { gap = d; best = i; }
    });
    return best;
  };

  const setPos = () => {
    const n = cards().length;
    pos.textContent = n ? (current() + 1) + " of " + n : "nothing to show";
  };

  // One rail-width, so a press moves by what the reader can see rather than by a fixed number of cards.
  // `clientWidth` and not a card count: three cards fit at 1440px and one at 390px, and a button that
  // moves three on a phone skips two of them past the reader. The 40px is the gap plus a sliver of the
  // next card, which is what tells a reader there is one there.
  const step = () => Math.max(rail.clientWidth - 40, 120);
  // `behavior` is an argument here rather than the stylesheet's `scroll-behavior`, which a `scrollBy`
  // option overrides -- so the reduced-motion answer has to be given in JavaScript at every call site, and
  // `how()` is that one place. See the note beside the media query in pages.css.
  const how = () => (CALM.matches ? "auto" : "smooth");
  const page = (dir) => rail.scrollBy({left: dir * step(), behavior: how()});

  // THE ROLL. A carousel that advances on its own is the reason "carousel" is a word people say with a
  // sigh, and it is also the whole point of this page: fifty projects nobody asked to see, moving past.
  // So it advances -- and every way of saying "stop" stops it for good. A pointer over the rail, focus
  // inside it, a button, a touch, a wheel, a key, the grid view, a deep link to a particular card: after
  // any of those it never restarts on its own, because a reader who has started reading has already
  // answered the question the motion was asking.
  //
  // Off entirely under `prefers-reduced-motion`, and that is safe rather than merely polite: nothing here
  // is communicated *by* the motion. All fifty cards are in the DOM, the rail scrolls, the buttons work
  // and the count says where you are. Same rule as the blanket one in pages.css, restated in JavaScript
  // because an interval is not an animation a stylesheet can reach.
  const CALM = matchMedia("(prefers-reduced-motion: reduce)");
  let timer = 0;
  const roll = () => {
    // A hidden tab still fires intervals. Skipping rather than clearing means a reader who comes back to
    // the tab finds it where they left it and still moving, which is what they left.
    if (document.hidden) return;
    // Back to the start at the end, which is the one place this is a loop rather than a scroll: a rail that
    // reaches card fifty and sits there has stopped being a carousel with no way of saying so.
    if (current() >= cards().length - 1) rail.scrollTo({left: 0, behavior: how()});
    else page(1);
  };
  const auto = () => {
    if (timer || CALM.matches || cards().length < 2) return;
    timer = setInterval(roll, 6000);
  };
  const quit = () => { clearInterval(timer); timer = 0; };
  // `scroll` is deliberately not in this list. `roll()` scrolls, so quitting on it would stop the carousel
  // one tick after it started; the reader's own scrolling arrives as a wheel, a touch or a key first.
  ["pointerdown", "wheel", "touchstart", "keydown"].forEach((t) =>
    rail.addEventListener(t, quit, {passive: true}));
  rail.addEventListener("mouseenter", quit);
  rail.addEventListener("focusin", quit);
  rail.addEventListener("scroll", setPos, {passive: true});
  CALM.addEventListener("change", () => { if (CALM.matches) quit(); });
  document.getElementById("dprev").onclick = () => { quit(); page(-1); };
  document.getElementById("dnext").onclick = () => { quit(); page(1); };

  // Carousel or all fifty at once. A rail is how you meet something you were not looking for and a grid is
  // how you scan what is on offer, and there is no reason to make a reader pick one of those at the door.
  // The class is on <html> like the index's own view toggle, so the stylesheet does the work and the state
  // survives a re-render of the rail's contents.
  const mode = document.getElementById("dmode");
  const setMode = (grid) => {
    document.documentElement.setAttribute("data-dmode", grid ? "grid" : "rail");
    mode.textContent = grid ? "Carousel view" : "Grid view";
    mode.setAttribute("aria-pressed", grid ? "true" : "false");
    try { localStorage.setItem("aaa-dmode", grid ? "grid" : "rail"); } catch (e) {}
    if (grid) quit();
  };
  mode.onclick = () => setMode(document.documentElement.getAttribute("data-dmode") !== "grid");
  try { if (localStorage.getItem("aaa-dmode") === "grid") setMode(true); } catch (e) {}

  // Arrow keys on the rail itself. The cards are links, so Tab already walks them; this is for the reader
  // who has the rail focused and expects Left and Right to do the obvious thing.
  rail.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") { page(1); e.preventDefault(); }
    if (e.key === "ArrowLeft") { page(-1); e.preventDefault(); }
  });

  // Put the reader on the card they came for, and say something honest when it is not in today's fifty.
  // `scrollIntoView` on the card rather than a hash jump, because the rail scrolls horizontally inside a
  // page that scrolls vertically and a browser asked to reach an id does both at once.
  const goto_ = (nwo) => {
    if (!nwo) return;
    const card = rail.querySelector('[data-project="' + CSS.escape(nwo) + '"]');
    if (card) {
      quit();
      card.scrollIntoView({block: "nearest", inline: "start", behavior: "auto"});
      card.setAttribute("tabindex", "-1");
      card.focus({preventScroll: true});
      card.classList.add("dhit");
      setPos();
      return;
    }
    // Not in today's cohort. Which day it *was* in is a fact the plan still holds, and it is the only
    // thing worth saying here: a link shared yesterday afternoon is not broken, it is dated.
    const was = PLAN && PLAN.days.find((c) => c.picks.includes(nwo));
    const row = PLAN && DISCOVER.hydrate(PLAN)[nwo];
    if (!row) return;
    const when = was ? DISCOVER.longDate(was.date) : "an earlier day";
    note.innerHTML = DISCOVER.esc(row.name) + " was in " + DISCOVER.esc(when) +
      "'s fifty, not today's. " + '<a href="' + DISCOVER.esc(DISCOVER.detailURL(nwo)) + '">' +
      "Open " + DISCOVER.esc(row.name) + "</a>, or browse today's below.";
    note.hidden = false;
  };

  // Draw a cohort that is not the one the stage rendered. The only two ways here: the date has rolled over
  // since this HTML was written, or the page came out of the service worker's cache from an older build.
  const draw = (cohort) => {
    const rows = DISCOVER.hydrate(PLAN);
    const picks = cohort.picks.filter((n) => rows[n]);
    rail.innerHTML = picks
      .map((n, i) => DISCOVER.cardHTML(rows[n], i, picks.length, PLAN.cats, PLAN.cohort)).join("");
    rail.dataset.day = cohort.date;
    SHOWN = cohort.date;
    line.textContent = DISCOVER.longDate(cohort.date) + " · " + picks.length +
      " projects · every category, none of them repeated this week";
    setPos();
  };

  // The rollover, in the browser. The stage rendered one day's fifty; a page held open past midnight, or
  // served out of `atlas-pages` on a morning after the build that wrote it, is showing a day that has
  // ended. Checked once on load and then once a minute, which is a `Date` comparison and a string compare
  // -- and only redraws when the answer has actually changed.
  const check = () => {
    if (!PLAN) return;
    const today = DISCOVER.dayIn(PLAN.tz, new Date());
    if (today === SHOWN) return;
    const cohort = DISCOVER.forDay(PLAN, today);
    if (!cohort || cohort.date === SHOWN) return;
    draw(cohort);
    note.hidden = true;
  };

  fetch("../discover.json").then((r) => r.json()).then((d) => {
    PLAN = d;
    check();
    goto_(wanted());
    setInterval(check, 60000);
    document.addEventListener("visibilitychange", () => { if (!document.hidden) check(); });
    addEventListener("hashchange", () => { note.hidden = true; goto_(wanted()); });
    if (!wanted()) auto();
    // "Tomorrow is fifty different ones" -- but tomorrow starts in Chicago, not where the reader is. For a
    // reader in another zone that is a real difference of up to a day, and the plan carries the zone, so
    // the page can say when the roll happens in their own clock instead of leaving them to work it out.
    // Only for a reader who is somewhere else: telling somebody in Chicago that the day turns at midnight
    // their time is a sentence that has said nothing.
    const own = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const turns = own && own !== d.tz ? DISCOVER.endOf(d.tz, SHOWN) : null;
    if (turns) document.getElementById("dzone").textContent = " Today's " + (PLAN.per_day || 50) +
      " run out at " + new Intl.DateTimeFormat("en-GB", {timeZone: own, weekday: "long",
        hour: "numeric", minute: "2-digit"}).format(turns) + " where you are.";
  }).catch(() => {
    // The page is already showing the day it was built for, with fifty real cards in it. A failed fetch
    // costs the rollover and the deep link and nothing else, so there is nothing to say on screen.
    auto();
  });
})();
</script>
"""


def nav() -> str:
    """The header navigation, matching `20_landing.py`'s so the page families feel like one site."""
    return f"""  <nav>
    <a href="{esc(rel('collections/'))}">Collections</a> &middot;
    <a href="https://github.com/{esc(REPO)}/blob/main/mega-list/leaderboard.md">Leaderboard</a> &middot;
    <a href="{esc(rel('repo/'))}">All projects</a> &middot;
    <a href="{esc(rel())}#browse">Topics &amp; harnesses</a><br>
    <a href="https://github.com/{esc(REPO)}">Repository</a> &middot;
    <a href="https://github.com/{esc(REPO)}/tree/main/mega-list">Markdown</a><br>
    <button class="chip" id="theme" aria-pressed="false">Light theme</button>
  </nav>"""


def render(published: dict, data: dict, day: str) -> str:
    """The page for `day`, with that day's fifty in the markup."""
    html, shown, total = rail(published, day)
    cats = len(published["cats"])
    rows = len(data["rows"])
    title = f"Discover — {total} projects a day from the Awesome Agentic Atlas"
    desc = (f"A different {total} of the {rows:,} projects every day, drawn from all {cats} categories "
            f"so the ones a popularity ranking never reaches get their turn. Rolls over at midnight "
            f"{published['tz'].split('/')[-1].replace('_', ' ')} time.")
    url = SITE + "discover/"
    zone = published["tz"].split("/")[-1].replace("_", " ")
    return f"""{head(title, desc, url)}<body>
<header><div class="wrap">
  <div class="top">
    <div>
      <p class="kick">Discover</p>
      <h1>{total} projects, today only</h1>
      <p class="sub" id="dline">{esc(long_date(shown))} &middot; {total} projects &middot; every category,
        none of them repeated this week</p>
      <p class="blurb">The atlas ranks by stars, and a ranking has a top. This does not: every one of the
        {cats} categories is in every day's {total}, the ones that have waited longest go first, and no
        project appears twice in a week. Tomorrow is {total} different ones.<span id="dzone"></span></p>
    </div>
{nav()}
  </div>
</div></header>
<main><div class="wrap">
  <div class="dctl">
    <button class="chip" id="dprev" aria-label="Previous projects">&larr; Back</button>
    <button class="chip" id="dnext" aria-label="More projects">Next &rarr;</button>
    <button class="chip" id="dmode" aria-pressed="false">Grid view</button>
    <span class="dpos" id="dpos" role="status">1 of {total}</span>
  </div>
  <p class="dnote" id="dnote" hidden></p>
  <div class="drail" id="drail" tabindex="0" role="group" data-day="{esc(shown)}"
       aria-label="{total} projects for {esc(long_date(shown))}">{html}</div>
  <section class="allin">
    <h2>How these {total} were chosen</h2>
    <p>Every category gets slots in every day, weighted by the square root of its size &mdash; so the
      {cats} categories here are all represented, the largest one does not take half the page, and a
      category with a few dozen projects in it is not crowded out by one with thousands. Within a
      category, the projects that have gone longest without appearing go first. Stars are not an input:
      the <a href="{esc(rel())}">front page</a> already ranks by them, and a Discover that consulted them
      would be the front page with a different heading.</p>
    <p>The week's seven days are picked at once, on Sunday, and written to
      <a href="https://github.com/{esc(REPO)}/blob/main/docs/discover.json">discover.json</a> &mdash; so
      today's {total} are the same {total} for everyone, they can be linked to, and they are still here
      when you come back this afternoon. The day turns over at midnight, {esc(zone)} time.</p>
  </section>
</div></main>
<footer><div class="wrap">
  {total} of {rows:,} projects a day, rotated so the whole atlas comes round rather than the popular end of
  it being resampled. Stars, language and last-push come from the GitHub API on
  {esc(published['snapshot'])} and drift daily; the picks are fixed for the week. Everything here is also
  in the <a href="{esc(rel())}">searchable index</a>, on each project's own page, and in the
  <a href="https://github.com/{esc(REPO)}/tree/main/mega-list">Markdown edition</a>.
</div></footer>
{core_js()}{PAGE_JS}{THEME_JS}{b19.follow()}{b19.beacon()}</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--day", help="the date to publish for; defaults to today in the plan's zone")
    ap.add_argument("--force", action="store_true",
                    help="pick a fresh week even if the published plan still reaches --day")
    ap.add_argument("--out", help="write under this directory instead of docs/ (a dry run)")
    args = ap.parse_args()

    data = json.loads((OUT / "data.json").read_text(encoding="utf-8"))
    day = args.day or discover.today()
    out = Path(args.out) if args.out else OUT
    before = out / "discover.json"
    old = json.loads(before.read_text(encoding="utf-8")) if before.exists() else None

    published, state = pick(data, day, args.force, old, discover.load())
    (out / "discover").mkdir(parents=True, exist_ok=True)
    (out / "discover.json").write_text(
        json.dumps(published, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    page = out / "discover" / "index.html"
    page.write_text(render(published, data, day), encoding="utf-8")
    # Only on a run that picked, and only into the real tree: a dry run that stamped the ledger would move
    # every row it dealt to the back of its queue and change what the next real build publishes.
    if state is not None and not args.out:
        discover.save(state)

    shown, picks = discover.for_day(published, day)
    kept = sum(len(c["picks"]) for c in published["days"])
    print(f"{'picked' if state is not None else 'kept'} the week of {published['week']} "
          f"· {kept} picks over {len(published['days'])} days · {len(published['rows']):,} distinct rows")
    print(f"discover.json · {b20.kb((out / 'discover.json').stat().st_size)} · "
          f"discover/index.html · {b20.kb(page.stat().st_size)} · showing {shown} ({len(picks)} cards)")
    if published["dropped"]:
        print(f"{len(published['dropped'])} pick(s) dropped, no longer in the atlas: "
              + ", ".join(published["dropped"][:5]))
    if state is not None:
        print(f"state/discover.json · {len(state['shown']):,} rows stamped"
              + (" (dry run, not written)" if args.out else ""))
    print("sitemap.xml carries this URL via scripts/20_landing.py")


if __name__ == "__main__":
    main()
