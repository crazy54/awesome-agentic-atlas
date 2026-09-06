"""Atom and JSON Feed of the repos that have arrived since the baseline.

`state/first-seen.json` already knows the day each repo entered the atlas, and the page already draws a
mark on everything inside the fourteen-day window -- but only for a reader who happens to load the page
during it. A reader who does not visit hears nothing, and there is no way to ask to be told. This stage
is the other half of the ledger: the same arrivals, pushed instead of polled by hand.

  docs/feed.xml    Atom 1.0
  docs/feed.json   JSON Feed 1.1, the same entries in the same order

Atom rather than RSS 2.0. RSS has no required unique id (`<guid>` is optional, and readers that fall
back to the link or the title re-announce an entry whenever either is edited), its dates are RFC 822 so
they carry a day name the writer can get wrong, and `<description>` does not declare whether it holds
text or markup, which is why RSS entities are guessed at differently by every reader. Atom fixes all
three: `<id>` and `<updated>` are mandatory, timestamps are RFC 3339, and `type="html"` says what the
content is. JSON Feed sits next to it because it costs one more `json.dumps` of the entry list that has
already been built, and it is the format anything speaking JSON can read without an XML parser.

Four decisions, all of them consequences of the fact that a feed is read by software with a memory:

  * "New" means arrived after the baseline, not inside the fourteen-day window. The window is a rule for
    a drop-in visitor -- it answers "is this worth a second look right now", and it has to expire on its
    own because nothing rebuilds the page daily. A subscriber has the opposite problem: it polls on its
    own schedule and wants everything since it last looked. Publishing only the last fortnight would
    silently drop every arrival for anyone who reads their feeds monthly, or who was on holiday, and a
    feed that loses items is worse than no feed. So the window is not applied here at all.

  * Fifty entries, newest first. The ledger is an archive and grows forever; a feed is a window onto the
    end of it. Fifty is roughly two GitHub screens of reading, keeps both files inside a few tens of KB
    on every poll, and is well past the reader-side default of "show me what is unread". The cost is
    honest and worth stating: a subscriber that goes quiet for longer than fifty arrivals loses the ones
    that fell off the end, which is what the site itself is for.

  * Ids are `tag:` URIs built from the repo's `owner/name` and nothing else. Not the build date, not the
    row's position, not the arrival date -- an id that moves is a re-announcement, and the whole point of
    an id is that a reader can say "already seen this". `owner/name` is the same key the ledger and the
    dataset are already indexed by, so the id is stable for exactly as long as the repo is the same repo.

  * Neither file carries a build timestamp. Feed-level `<updated>` is the newest arrival's date, not
    `now`, so two runs a week apart over an unchanged ledger write byte-identical files -- nothing to
    commit, nothing for a conditional GET to re-download, and no reader deciding the feed changed when
    the collection did not.

  python scripts/21_feeds.py

Reads the committed `docs/data.json` for the descriptive columns and the ledger for the dates, so it
runs from a clone with nothing fetched, like `19b_refresh`. The ledger is the authority on when a repo
arrived: `data.json` carries a `first_seen` column, but it is a copy, and it is stale for exactly as
long as the ledger has moved and the site has not been refreshed.
"""
from __future__ import annotations

import html
import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"

sys.path.insert(0, str(HERE))
import newness  # noqa: E402

# 17_markdown owns the canonical site URL, and it is the module every other surface asks for it, so the
# feed asks too rather than growing a second copy that can disagree after a rename.
spec = importlib.util.spec_from_file_location("b17", HERE / "17_markdown.py")
b17 = importlib.util.module_from_spec(spec)
sys.modules["b17"] = b17
spec.loader.exec_module(b17)

SITE = b17.SITE
ATOM_URL = SITE + "feed.xml"
JSON_URL = SITE + "feed.json"

TITLE = "Awesome Agentic Atlas — new arrivals"
SUBTITLE = ("Repos added to the atlas since it started keeping a ledger, newest first. "
            "One entry per project, with its topic, the harnesses it targets and its star count.")
AUTHOR = "Awesome Agentic Atlas"

LIMIT = 50

ATOM = "http://www.w3.org/2005/Atom"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
ET.register_namespace("", ATOM)

# The `tag:` authority is the host that serves the feed, because that is the name actually under the
# author's control (RFC 4151 asks for one, and a repo URL on github.com is not ours to mint ids under).
# The date is a literal year and deliberately not derived from anything in the ledger or the dataset: a
# re-seed moves every baseline and every `first_seen`, and if the ids moved with them every subscriber
# would be shown all fifty entries again as if they were new.
TAG_HOST = urlsplit(SITE).netloc
TAG_NAME = urlsplit(SITE).path.strip("/") or "atlas"
TAG_YEAR = "2026"
FEED_ID = f"tag:{TAG_HOST},{TAG_YEAR}:{TAG_NAME}/feeds/arrivals"


def entry_id(nwo: str) -> str:
    return f"tag:{TAG_HOST},{TAG_YEAR}:{TAG_NAME}/repos/{nwo}"


def stamp(iso: str) -> str:
    """An ISO date as the RFC 3339 instant both formats want.

    The ledger records a day, not a moment -- it is written by a build that only knows `date.today()` --
    so the time of day is invented. Midnight UTC is the one invention that never shifts an entry into a
    different day for a reader in a different timezone, which a local-midnight or a build-time stamp
    both would.
    """
    return f"{iso}T00:00:00Z"


def content_html(e: dict) -> str:
    """The entry body, as an escaped HTML fragment.

    One function for both files: Atom takes it as the text of `<content type="html">` and JSON Feed as
    `content_html`, which are the same contract -- a string of HTML the reader may render. Everything
    interpolated goes through `html.escape` here rather than trusting the serialiser, because half of
    these strings never reach an XML writer.
    """
    esc = html.escape
    topic = f'<a href="{esc(b17.site(topic=e["topic_slug"]))}">{esc(e["topic"])}</a>'
    targets = ", ".join(f'<a href="{esc(b17.site(target=s))}">{esc(n)}</a>'
                        for n, s in e["targets"]) or "—"
    rows = [
        f"<strong>Topic:</strong> {topic}",
        f"<strong>Targets:</strong> {targets}",
        f"<strong>Stars:</strong> {e['stars']:,}",
        f"<strong>Added:</strong> {newness.pretty(e['seen'])}",
    ]
    parts = []
    if e["blurb"]:
        parts.append(f"<p>{esc(e['blurb'])}</p>")
    parts.append("<p>" + "<br>\n".join(rows) + "</p>")
    parts.append(f'<p><a href="{esc(e["url"])}">{esc(e["nwo"])} on GitHub</a></p>')
    return "\n".join(parts)


def arrivals(data: dict, ledger: dict, limit: int = LIMIT) -> tuple[list[dict], int, int]:
    """Feed-ready entries, newest first, capped at `limit`. Returns (entries, total, orphans).

    `total` is every post-baseline arrival the ledger knows, not the capped list, so the caller can say
    how much of the archive did not fit; `orphans` is the arrivals the dataset has never heard of.
    """
    baseline = ledger["baseline"]
    seen = {n: d for n, d in ledger["repos"].items() if d > baseline}

    cols = data["cols"]
    ix = {c: cols.index(c) for c in ("name", "nwo", "cat", "targets", "stars", "blurb", "url")}
    cats, targets = data["cats"], data["targets"]
    rows = {r[ix["nwo"]]: r for r in data["rows"]}

    entries, orphans = [], 0
    for nwo, day in seen.items():
        row = rows.get(nwo)
        # In the ledger but not in the dataset means the ledger ran ahead of the site: something stamped
        # a repo and `data.json` has not been rebuilt yet. There is no title or blurb to publish, so the
        # entry waits for the next build rather than going out as a bare URL that would then be an entry
        # a reader has already seen when the real one arrives.
        if row is None:
            orphans += 1
            continue
        entries.append({
            "nwo": nwo,
            "name": row[ix["name"]] or nwo,
            "url": row[ix["url"]] or f"https://github.com/{nwo}",
            "seen": day,
            "stars": row[ix["stars"]] or 0,
            "blurb": row[ix["blurb"]] or "",
            "topic": cats[row[ix["cat"]]]["name"],
            "topic_slug": cats[row[ix["cat"]]]["slug"],
            "targets": [(targets[t]["name"], targets[t]["slug"]) for t in row[ix["targets"]]],
            "id": entry_id(nwo),
            "stamp": stamp(day),
        })

    # Newest first, then most-starred, then the key. A day's arrivals have no order of their own -- they
    # were all found by the same build -- so stars break the tie, and `nwo` breaks that one, because the
    # order has to be a function of the data alone for two runs to agree.
    entries.sort(key=lambda e: (e["seen"], e["stars"], e["nwo"]), reverse=True)
    return entries[:limit], len(seen), orphans


def el(parent, tag: str, text: str | None = None, **attrs) -> ET.Element:
    """One Atom element. Named for how often it is called: the document is 60 of these."""
    node = ET.SubElement(parent, f"{{{ATOM}}}{tag}", attrs)
    if text is not None:
        node.text = text
    return node


def atom(entries: list[dict], updated: str) -> str:
    """The Atom document. Built as a tree rather than a template so escaping is the parser's problem."""
    feed = ET.Element(f"{{{ATOM}}}feed", {XML_LANG: "en"})
    el(feed, "id", FEED_ID)
    el(feed, "title", TITLE)
    el(feed, "subtitle", SUBTITLE)
    el(feed, "updated", updated)
    # rel=self is what lets a reader that was handed the file re-find it, and it is the one link a feed
    # cannot derive from anything else in the document.
    el(feed, "link", rel="self", type="application/atom+xml", href=ATOM_URL)
    el(feed, "link", rel="alternate", type="text/html", href=SITE)
    author = el(feed, "author")
    el(author, "name", AUTHOR)
    el(author, "uri", SITE)
    el(feed, "rights", f"Blurbs and metadata from the source lists; see {SITE}")
    el(feed, "generator", Path(__file__).name, uri=f"https://github.com/{b17.REPO}")

    for e in entries:
        entry = ET.SubElement(feed, f"{{{ATOM}}}entry")
        el(entry, "id", e["id"])
        el(entry, "title", e["name"])
        el(entry, "link", rel="alternate", type="text/html", href=e["url"])
        # Both, and equal: `published` is when the repo arrived and never changes, `updated` is when the
        # entry last changed and there is no second version of an arrival to record. A reader that sorts
        # on either gets the same feed.
        el(entry, "published", e["stamp"])
        el(entry, "updated", e["stamp"])
        el(entry, "category", term=e["topic_slug"], label=e["topic"])
        for name, slug in e["targets"]:
            el(entry, "category", term=slug, label=name)
        el(entry, "content", content_html(e), type="html")

    ET.indent(feed, space=" ")
    # Serialised to bytes and decoded rather than asked for `encoding="unicode"`, because ElementTree
    # fills the declaration's `encoding=` from the platform locale in that mode -- a feed written on this
    # machine would announce itself as cp1252 while holding UTF-8 em dashes.
    return ET.tostring(feed, encoding="utf-8", xml_declaration=True).decode("utf-8") + "\n"


def jsonfeed(entries: list[dict]) -> str:
    """The same entries as JSON Feed 1.1. No feed-level date, because the spec has no field for one."""
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": TITLE,
        "home_page_url": SITE,
        "feed_url": JSON_URL,
        "description": SUBTITLE,
        "language": "en",
        "authors": [{"name": AUTHOR, "url": SITE}],
        "items": [{
            "id": e["id"],
            "url": e["url"],
            "title": e["name"],
            "content_html": content_html(e),
            "date_published": e["stamp"],
            "date_modified": e["stamp"],
            "tags": [e["topic"]] + [n for n, _ in e["targets"]],
        } for e in entries],
    }
    # Indented and one key per line for the same reason the ledger is: this file is committed, and the
    # diff should be the entries that arrived. Keys stay in spec order rather than sorted, so the shape
    # of the document reads the way JSON Feed documents it.
    return json.dumps(feed, indent=1, ensure_ascii=False) + "\n"


def main() -> None:
    data = json.loads((OUT / "data.json").read_text(encoding="utf-8"))
    ledger = newness.load()
    entries, total, orphans = arrivals(data, ledger)

    # With nothing new the feed is empty rather than absent or padded: an empty Atom feed is legal (a
    # `<feed>` needs id, title and updated, not entries) and it is the honest answer. A reader that has
    # already subscribed keeps working and sees the first arrival on its next poll, which would not be
    # true of a 404. Feed-level `updated` then falls back to the baseline -- the last date on which the
    # collection is known to have changed -- so it is still a real date and still not the build's.
    updated = stamp(entries[0]["seen"] if entries else ledger["baseline"])
    # LF regardless of the OS that built it. Both files are committed, and the alternative is bytes that
    # flip between CRLF and LF depending on whether the day's build ran on a laptop or on the runner.
    (OUT / "feed.xml").write_text(atom(entries, updated), encoding="utf-8", newline="\n")
    (OUT / "feed.json").write_text(jsonfeed(entries), encoding="utf-8", newline="\n")

    for f in ("feed.xml", "feed.json"):
        print(f"{f:12s} {(OUT / f).stat().st_size / 1024:8.1f} KB")
    live = sum(1 for e in entries if newness.within(e["seen"]))
    print(f"{total:,} arrived since the baseline {ledger['baseline']} · "
          f"{len(entries):,} in the feed (cap {LIMIT}) · {live:,} inside the {newness.WINDOW}-day window")
    print(f"feed updated {updated} · newest first · ids under tag:{TAG_HOST},{TAG_YEAR}")
    if orphans:
        print(f"{orphans:,} arrival(s) not yet in docs/data.json; run 19b_refresh.py to pick them up")


if __name__ == "__main__":
    main()
