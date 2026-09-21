"""Write the GitHub Pages site: one static page over every repo, filterable in the browser.

The third surface, and the only one where the two axes are actually crossable live. The workbook can
cross them because Excel filters two columns at once; a Markdown page cannot, because Markdown has no
filter -- so `mega-list/topics/` and `mega-list/targets/` each pick one axis and print the other as a
column. This page does what the workbook does, without Excel.

Same data, same ordering, same verdicts as the other two: it imports `17_markdown`, which imports
`16_build_all`, so nothing here re-derives a star count or a platform call.

  docs/index.html   the page. no build step, no framework, no dependency to install.
  docs/data.json    every repo, column-oriented.
  docs/.nojekyll    stops Pages running Jekyll over a directory that has no Jekyll in it.

Two decisions worth stating. The data is a separate file rather than inlined, so the page is 30 KB and
cached separately from the nearly 8,000 rows that change on every rebuild. And every filter is mirrored
into the URL hash, which is what makes "the best Claude Code observability tool" a link -- the thing the
Markdown pages can only approximate by existing in two directories.
"""
import importlib.util
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
OUT = ROOT / "docs"

spec = importlib.util.spec_from_file_location("b17", Path(__file__).parent / "17_markdown.py")
b17 = importlib.util.module_from_spec(spec)
sys.modules["b17"] = b17
spec.loader.exec_module(b17)

# `17_markdown` puts `scripts/` on the path for its own plain-named siblings, but relying on that as a side
# effect of somebody else's import is how this breaks the day the import order changes. Stated here.
sys.path.insert(0, str(Path(__file__).parent))
import app_flags  # noqa: E402
import osicons  # noqa: E402
import pagemin  # noqa: E402

newness = b17.newness

b16 = b17.b16
tax = b17.tax
DASH = b16.DASH
REPO = b17.REPO
APP_FLAGS = app_flags.FLAGS

# How many curated lists the atlas is built from, read off the parser's own table rather than written
# down here. The page states it four times -- the heading, both social descriptions and the footer --
# and all four said "eleven" for a while after the atlas had stopped being eleven lists. `SOURCES` is
# the same authority `16_build_all.LIST_TITLE` and `watch_sources.py` read, so the site cannot
# disagree with the workbook about how many lists were merged.
LISTS = len(b16.b10.SOURCES)

# Verdicts compress to one character each because there are only five of them and every row prints all
# five -- some forty thousand characters across the dataset. The page expands them back for display;
# the JSON is what travels over the wire.
VERDICT = {"Yes": "Y", "Likely": "L", "No": "N", "n/a": "a", DASH: "-", "": "-"}
OS_FIELDS = ["win_native", "win_wsl2", "macos", "linux", "docker"]
OS_LABELS = ["Windows", "WSL2", "macOS", "Linux", "Docker"]
# Checked, not assumed: the marks are paired to these by position, so a reorder would mark the wrong verdict.
osicons.check(OS_LABELS)

# The columns of `data.json`, in order. Column-oriented rather than one object per repo: the keys would
# otherwise be repeated once per row across nearly 8,000 of them, which is megabytes of the word
# "category". The page maps them back into objects once, on load.
COLS = ["name", "nwo", "cat", "targets", "stars", "lists", "listed_by", "os",
        "blurb", "install", "lang", "license", "pushed", "url", "img", "first_seen"]


def og(nwo: str) -> str:
    return f"https://opengraph.githubassets.com/1/{nwo}"


# Where `23_og.py` writes the cards, relative to `docs/`, and the name it gives the one for the root
# view. Spelled here as well as there because no import runs between the two stages that could carry
# it -- the same seam `20_landing.OG` sits on.
OG_DIR = "og"
OG_ROOT = "root.png"


def image_tags(site: str, repo: str) -> str:
    """The root page's Open Graph image block, with the repository card as the fallback.

    `20_landing.image_tags()` does this for the 156 facet pages; this is the same contract for the one
    page that stage does not write. Not imported from it because the import runs the other way -- that
    module loads this one for `SITE` and `beacon()` -- and a cycle to fetch eight lines would cost more
    than the eight lines.

    Absolute, unlike every other URL this page emits. A relative `og:image` is resolved against
    whatever the scraper decides the document's base is, and several of them decide wrong. Built by the
    same concatenation `20_landing.py` uses, so `SITE`'s trailing slash is load-bearing in one place
    rather than in two that could drift.

    The disk check is what makes the fallback mean something, and it is worth being exact about what it
    can and cannot do. It resolves at build time, so the published document carries one `og:image` and
    only one: there is no runtime fallback here, and a scraper handed a URL whose file is missing shows
    a bare link rather than trying the next tag. What the check buys is the state where `23_og.py` has
    never produced `root.png` -- no Chromium on the runner, or a clone where that stage has not run --
    and there, pointing at the generic repository card beats pointing at a 404.
    """
    if not (OUT / OG_DIR / OG_ROOT).exists():
        return "\n".join([
            f'<meta property="og:image" content="{og(repo)}">',
            '<meta property="og:image:alt" content="The Awesome Agentic Atlas repository on GitHub.">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:image" content="{og(repo)}">',
        ])
    # 1200x630 is asserted against the render in `23_og.dimensions()` before the file is written, so
    # these two are a promise the writing stage refuses to break rather than a number typed twice.
    url = f"{site}{OG_DIR}/{OG_ROOT}"
    return "\n".join([
        f'<meta property="og:image" content="{url}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="The Awesome Agentic Atlas: how many projects it '
        'indexes, how many source lists and topics they came from, and its three most starred '
        'projects.">',
        # Not optional and not implied by the rest: without it X renders a small square thumbnail
        # beside the text whatever the image is, which is the one shape a 1.91:1 card cannot survive.
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{url}">',
    ])


def row_for(r, shots, cat_ix, tgt_ix) -> list:
    img = b17.image(r, shots)
    return [
        r["name"],
        r["nwo"],
        cat_ix[r["category"]],
        sorted(tgt_ix[t] for t in r["targets"]),
        r["stars"] or 0,
        r["list_count"],
        r["listed_by"],
        "".join(VERDICT.get(r.get(f) or "", "-") for f in OS_FIELDS),
        b17.norm(r.get("blurb") or "", 400),
        b17.norm(r.get("install_cmd") or ""),
        r.get("language") or "",
        r.get("license") or "",
        r.get("pushed_at") or "",
        r["url"],
        # Empty means "derive it": the social card exists for every repo and is what 608 of these 1,294
        # rows would name anyway, so spelling it out would be 55 bytes x 608 of a string the page can
        # rebuild from `nwo`. ("Two thirds" stood here and was wrong in the wrong direction -- it is 47.0%,
        # and the 686 rows that *do* carry a URL are the majority.)
        #
        # Still written, and deliberately, even though as of JFH-218 neither the index cards nor the facet
        # pages render it: both now show the derived card unconditionally, because nothing bounds what these
        # 686 URLs serve. This column stays because it is the only record of *which* repos published artwork
        # of their own, `22_detail.py` still shows it one page at a time where one image is nobody's budget
        # problem, and that page's caption can only say "the project's own screenshot" while the datum
        # distinguishing them exists. Shedding it was measured and is not worth it: emptying every value
        # saves 14,483 B gzipped and removing the column as well saves 232 B more, so the deletion earns
        # 1.6% of the saving and costs a documented `schema_version` break. If `data.json`'s weight has to
        # come down, JFH-213 owns that trade with these numbers in hand.
        "" if img == og(r["nwo"]) else img,
        # The raw arrival date, not a new/old flag, and for every arrival rather than only the recent
        # ones -- the page needs the date to print it and to expire the mark itself, and once it has to
        # travel anyway there is no reason to throw the older ones away.
        newness.SEEN.get(r["nwo"], ""),
    ]


SCHEMA_VERSION = 1

# The one thing the service worker tells the page in words. It sets this header on the `data.json`
# response it answers out of `atlas-data` when the network did not answer at all, because that is the only
# way the page can know: a body served from the cache the worker filled is byte-for-byte the body that
# filled it. `stamp()` reads it and says "offline, showing data from <date>" instead of "snapshot <date>".
#
# Defined here and asked for by `24_pwa.py`, which writes the worker, rather than spelled out in both --
# the same reason `24_pwa.py` asks `17_markdown` for the site URL instead of keeping a copy. Two files
# agreeing on a string is fine until they stop, and the symptom of stopping is a banner that simply never
# mentions the cache, which nothing would notice.
CACHED_HEADER = "x-atlas-cached"


def build_data(facets, shots) -> dict:
    cats = list(tax.CATEGORIES)
    tgts = [t for t, _p in tax.TARGETS]
    cat_ix = {c: i for i, c in enumerate(cats)}
    tgt_ix = {t: i for i, t in enumerate(tgts)}
    rows = sorted(facets, key=lambda r: (-(r["stars"] or 0), r["name"].lower()))
    return {
        # `data.json` is published at a stable URL with `Access-Control-Allow-Origin: *`, so anyone can
        # fetch it and some people will. This is the number that tells them whether their reader still
        # works. It only moves when the *shape* changes -- the column set or order, the Y/L/N/a/-
        # encoding, the five-OS order, the slug rules, the "no nulls" rule. Adding a top-level key or
        # changing a star count does not move it, because neither breaks a reader.
        # Absent means 1: the snapshot published before this key existed is otherwise identical.
        "schema_version": SCHEMA_VERSION,
        "snapshot": date.today().isoformat(),
        # The same fact as an instant, written here beside the rows it describes rather than only baked
        # into the page as `__SNAPSHOT__`. Offline the two halves of this site arrive from two caches --
        # the shell from `atlas-shell-<version>`, this file from `atlas-data` -- and nothing fills them at
        # the same moment, so a stamp that lives in the document describes the document and not the rows
        # underneath it. This is the copy that travels with the rows and is therefore right however old
        # the body a reader is holding turns out to be. `stamp()` in the page reads it. (JFH-207)
        #
        # Whole minutes, like `built()`, because the banner prints the date and no surface prints the
        # second: a finer figure would claim a precision nothing here gives a reader.
        #
        # UTC, while `snapshot` above is the builder's local date. On the machine that publishes this --
        # Actions, which is UTC -- they are the same day by construction. On a checkout whose local date is
        # not UTC's they can name different days, and the banner prefers this one, as the one that names an
        # instant rather than a day on somebody's clock.
        "generated": (datetime.now(timezone.utc).replace(second=0, microsecond=0)
                      .strftime("%Y-%m-%dT%H:%M:%SZ")),
        "repo": REPO,
        "cols": COLS,
        # The stale bound on a cohort, not a recency window -- see `newness.py`. Here rather than
        # hardcoded in the JavaScript so that changing it is one edit in `newness.py` and not two files
        # that disagree.
        "window_days": newness.WINDOW,
        "baseline": newness.load()["baseline"],
        # WHAT THE PAGE COMPARES A ROW'S `first_seen` AGAINST TO DECIDE `New`.
        #
        # The date of the import that brought the current arrivals, or "" when there is not one to show.
        # A row is New because `first_seen == cohort`, never because `first_seen` is recent: the atlas
        # gains repos when a curator adds one to somebody's list, so every arrival here is years old in
        # the world and the only newness this pipeline can observe is newness to this site.
        #
        # `newness.COHORT` rather than `newness.load()["cohort"]`, and the difference matters on the run
        # that creates a cohort: `resolve()` has already written the ledger by the time this executes, so
        # both would agree today -- but `COHORT` is the value that has been through `cohort()`, which is
        # where the stale bound is applied. Reading the raw key would publish a cohort the rest of the
        # build has already decided is too old to mark.
        "cohort": newness.COHORT,
        # Slugs travel in the URL hash, and they are the same slugs that name the Markdown pages, so a
        # link into this page and a link into `mega-list/topics/` say the same word.
        "cats": [{"name": c, "slug": b17.fileslug(c),
                  "blurb": b17.TOPIC_BLURB.get(c, "")} for c in cats],
        "targets": [{"name": t, "slug": b17.fileslug(t),
                     "blurb": b17.TARGET_BLURB.get(t, "")} for t in tgts],
        "os": OS_LABELS,
        "rows": [row_for(r, shots, cat_ix, tgt_ix) for r in rows],
    }


# Cloudflare Web Analytics: one script, no cookies, no consent banner, nothing to install, and it works
# on Pages without the domain being on Cloudflare -- the beacon reports from the reader's browser, so the
# "JS beacon" mode needs no DNS change.
#
# The token is committed rather than injected from a secret, because it is not one. Pages serves `docs/`
# verbatim and has no build step of its own, so the token has to be *in* the generated page, and that page
# is in the repo; every visitor reads it in view-source anyway. Hardcoding it also means a rebuild by
# anyone cannot quietly ship a page that measures nothing, which is the failure an env-var-only design
# invites. `CF_BEACON_TOKEN` still overrides it, and setting that to "" or "off" drops the script -- which
# is what a fork wants, and what a local `python -m http.server` run wants.
#
# `type=module` is Cloudflare's own current form and is deferred implicitly, so it cannot block the parse.
# The token lands in a JSON attribute inside HTML, so it is validated rather than trusted: one stray quote
# would close the attribute and let the rest be read as markup. Cloudflare issues 32 hex characters, and
# anything else is a typo worth stopping the build for instead of shipping a silent no-op.
CF_TOKEN = "1fe3cbfd55ef4fccab981c064489e656"
TOKEN_RE = re.compile(r"\A[0-9a-f]{32}\Z")


def beacon(token: str | None = None) -> str:
    """The analytics script tag, or "" when the token is disabled."""
    if token is None:
        token = os.environ.get("CF_BEACON_TOKEN", CF_TOKEN)
    token = token.strip()
    if not token or token.lower() in {"off", "none", "0"}:
        return ""
    if not TOKEN_RE.match(token):
        raise SystemExit(
            f"CF_BEACON_TOKEN is not a Cloudflare beacon token (expected 32 hex chars, got {token!r}).")
    return ("<!-- Cloudflare Web Analytics --><script type=\"module\" "
            'src="https://static.cloudflareinsights.com/beacon.min.js" '
            f"data-cf-beacon='{{\"token\": \"{token}\"}}'></script>"
            "<!-- End Cloudflare Web Analytics -->\n")


# Google Search Console's HTML-tag verification, and the IndexNow key. Both live here rather than in the
# stage that emits them, for the reason `CF_TOKEN` does: Pages serves `docs/` verbatim with no build step
# of its own, so a token has to be *in* the generated bytes, and the generated bytes are in the repository.
# Neither is a secret -- one is a public meta tag and the other is a public file at the site root, both
# readable by anyone who fetches the site. What they are is *site identity*, so they belong in one file
# that every surface reads, next to the one token that was already here, and each gets a format assertion
# for the same reason the beacon token got one: a malformed value ships a silent no-op, and a silent no-op
# is exactly the failure this whole ticket exists to undo.
#
# `VERIFY_TOKEN` is empty on purpose and the site is unverified until somebody sets it. It cannot be
# guessed, invented or derived -- Google mints it against an account -- so shipping it wired-and-inert is
# the whole of what a build can do. The moment `GOOGLE_SITE_VERIFICATION` is set (repository variable or
# secret; `daily.yml` and `weekly.yml` forward either), the next rebuild emits the tag with no code change.
VERIFY_TOKEN = ""

# Google's own tag is 43 characters of base64url today. The band is wider than that on purpose: the length
# is a vendor's current choice and not a documented contract, while the *alphabet* is what catches the two
# ways this value actually gets typed wrong. Pasting the whole element -- `<meta name="google-site-
# verification" content="...">` -- brings `<`, `=`, `"` and spaces; pasting `google-site-verification=abc`
# brings `=`. Both are rejected here rather than injected into the head of every page, where a stray quote
# would close the attribute and let the rest of the document be read as markup.
VERIFY_RE = re.compile(r"\A[A-Za-z0-9_-]{32,64}\Z")

# IndexNow. Bing and Yandex accept a POST of changed URLs, and unlike Search Console it needs no account:
# the credential is a key you invent, hosted as `<key>.txt` at the site root containing that key and
# nothing else. `20_landing.py` writes that file -- it is the stage that owns `robots.txt`, and this is the
# same kind of file for the same reason -- and `26_indexnow.py` posts against it.
#
# Committed rather than injected, again, and here the argument is stronger than for the beacon: the key in
# the payload has to match the key in the *published* file, and the published file is a build artefact. A
# key that arrived only from a secret would mean the submitter and the file could disagree, which is a 403
# from the endpoint and no way to tell it from a network problem. `INDEXNOW_KEY` still overrides it, so a
# fork can rotate to its own key with one variable and get a matching file and payload out of one run.
#
# 32 hex characters from `secrets.token_hex(16)`. The spec allows 8-128 of `[A-Za-z0-9-]`; this shape is
# also the beacon token's shape, so one glance says "opaque public identifier" for both.
INDEXNOW_KEY = "995d9cae4a49e575ed9cbbbfe6e46864"
INDEXNOW_RE = re.compile(r"\A[A-Za-z0-9-]{8,128}\Z")


def verification(token: str | None = None) -> str:
    """The Search Console meta tag, or "" while no token is set.

    Returned *with* its newline, and substituted for `__VERIFY__\\n` rather than `__VERIFY__`, so the
    unverified case removes the placeholder's whole line instead of leaving a blank one behind. That is
    what makes wiring this up a zero-byte change to `docs/index.html` until there is a token to print.

    Only the root page carries it. Verification is per *property*, and the property here is the URL prefix
    `https://crazy54.github.io/awesome-agentic-atlas/` -- Google fetches that one URL and looks for the
    tag in it. Emitting it on the other 1,450 pages would verify nothing extra and put an account-linked
    identifier in 1,450 files that have no use for it.
    """
    if token is None:
        token = os.environ.get("GOOGLE_SITE_VERIFICATION", VERIFY_TOKEN)
    token = token.strip()
    if not token or token.lower() in {"off", "none", "0"}:
        return ""
    if not VERIFY_RE.match(token):
        raise SystemExit(
            "GOOGLE_SITE_VERIFICATION is not a Search Console verification token (expected 32-64 "
            f"characters of A-Z a-z 0-9 _ -, which is the `content` value alone, got {token!r}).")
    return f'<meta name="google-site-verification" content="{token}">\n'


def indexnow_key(key: str | None = None) -> str:
    """The IndexNow key, asserted. No "off" spelling: there is no inert form of this one.

    An empty key would mean `20_landing.py` writing `docs/.txt` and `26_indexnow.py` posting a credential
    nothing can validate, which is worse than either failing. So unlike `beacon()` this raises on empty --
    turning IndexNow off is done by not running the submit step, not by blanking the key.
    """
    if key is None:
        key = os.environ.get("INDEXNOW_KEY", INDEXNOW_KEY)
    key = key.strip()
    if not INDEXNOW_RE.match(key):
        raise SystemExit(
            f"INDEXNOW_KEY is not a valid IndexNow key (expected 8-128 of A-Z a-z 0-9 -, got {key!r}).")
    return key


def indexnow_key_file(key: str | None = None) -> str:
    """The key file's name, relative to `docs/`. Spelled once because two stages have to agree on it:
    `20_landing.py` writes the file and `26_indexnow.py` puts its URL in every payload as `keyLocation`.
    A name derived twice is a name that differs once, and the symptom would be a 403 nobody can explain."""
    return f"{indexnow_key(key)}.txt"


def facet_links(items: list[dict], prefix: str) -> str:
    """The footer's crawlable links to the prerendered facet pages `20_landing.py` writes.

    Derived from the same lists the page filters by, rather than written out, so adding a topic adds its
    link. `escape` because these names carry an ampersand -- "Harnesses & Runtime Infra" -- and a raw one
    is a parse error a validator will flag even where a browser recovers from it."""
    return " · ".join(
        f'<a href="{prefix}/{i["slug"]}/">{escape(i["name"])}</a>' for i in items)


def built() -> tuple[str, str]:
    """When this page was rendered, as (machine-readable UTC, the form the badge prints).

    The header carries a "last deployed" badge, and this is the half of its value that can be known here.
    The other half cannot: Pages serves this branch's `docs/` folder, so the commit that carries this very
    file is what triggers its own deployment, and that deployment finishes a minute or two after this
    function runs. A page therefore cannot be told its own publish time at build time -- it can only be
    told when it was built, and then look the real answer up at load. See `deployStamp` in the page, which
    reads it off the `Last-Modified` header of the `data.json` request the page already makes.

    So this value is what the badge shows before that fetch resolves, in the copy committed to the
    repository, and in a local `python -m http.server` where there is no deployment to describe at all.

    Whole minutes because that is what the badge prints, and a `datetime` attribute claiming a precision
    the visible text does not have is a small lie to a machine. It costs nothing in churn either way:
    `__SNAPSHOT__` already puts today's date in this file, so `index.html` differs on every day a build
    runs regardless of what this returns.
    """
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%d %H:%M UTC")


def shield_text(text: str) -> str:
    """Encode free text for shieldcn's static-badge path grammar."""
    return text.replace("_", "__").replace("-", "--").replace(" ", "_")


def substitute(page: str, data: dict, repo: str, site: str) -> str:
    """Fill the template's placeholders. Both this stage and `19b_refresh.py` render the same shell, and
    when the two chains drifted the refreshed page quietly lost whichever one had been added since.

    The comments come out here, which is why the strip is inside this function and not at either call site:
    it is the one place both chains already share, and the docstring above is the record of what happens
    when they stop sharing one. It runs before substitution rather than after, so its input is a constant
    and its output is a pure function of the template -- see `pagemin` for that argument and for why the
    beacon's own marker comments survive it. 36,753 B gzipped becomes 14,448.
    """
    stamp_iso, stamp_utc = built()
    default_view = "cards" if APP_FLAGS["index.card_view"] else "table"
    deployment_badge = DEPLOYMENT_BADGE if APP_FLAGS["index.deployment_badge"] else ""
    return (pagemin.strip_page(page)
            # The four platform-mark placeholders. `osicons` is the only copy of the geometry, the ids, the
            # hover text and the shared rule, so all four arrive here rather than being written into the
            # template -- which is what stops this page and the other three surfaces drawing Docker two ways.
            # The stylesheet fragment goes through `strip_css` on the way in: substitution runs *after*
            # `strip_page`, so a constant injected here would otherwise carry its own comments into the
            # published bytes, which is the one thing this function's comment strip exists to prevent. Its
            # input is still a constant, so the output is still a pure function of the source.
            .replace("__OSSPRITE__", osicons.SPRITE)
            .replace("__OSCSS__", pagemin.strip_css(osicons.CSS))
            .replace("__OSIDS__", osicons.JS_IDS)
            .replace("__OSTITLES__", osicons.JS_TITLES)
            .replace("__DEFAULT_VIEW__", default_view)
            .replace("__INDEX_SCREENSHOTS__", "on" if APP_FLAGS["index.project_screenshots"] else "off")
            .replace("__APP_FLAGS__", app_flags.browser_json(APP_FLAGS))
            .replace("__DEPLOYMENT_BADGE__", deployment_badge)
            .replace("__BUILT__", stamp_iso)
            .replace("__BUILT_UTC__", stamp_utc)
            .replace("__BUILT_BADGE__", shield_text(stamp_utc))
            .replace("__TOPICLINKS__", facet_links(data["cats"], "topic"))
            .replace("__TARGETLINKS__", facet_links(data["targets"], "target"))
            .replace("__COUNT__", f"{len(data['rows']):,}")
            .replace("__TOPICS__", str(len(data["cats"])))
            .replace("__LISTS__", str(LISTS))
            .replace("__STARS__", f"{sum(r[4] for r in data['rows']):,}")
            .replace("__SNAPSHOT__", data["snapshot"])
            .replace("__CACHEHDR__", CACHED_HEADER)
            .replace("__WINDOW__", str(newness.WINDOW))
            .replace("__SITE__", site)
            .replace("__REPO__", repo)
            .replace("__OGIMAGE__", image_tags(site, repo))
            # The placeholder's newline is part of the match -- see `verification()`. With no token set
            # this deletes the line, so the rendered page is byte-identical to one built before the tag
            # was wired up, which is why adding it did not have to re-version the service worker.
            .replace("__VERIFY__\n", verification())
            .replace("__ANALYTICS__", beacon()))


DEPLOYMENT_BADGE = r'''<a class="stamp" id="deployed" href="https://github.com/__REPO__/deployments"
       title="When this copy of the site was published."><img class="deploy-badge" decoding="async"
        src="https://shieldcn.dev/badge/last_deployed-__BUILT_BADGE__-187557.svg?logo=ri%3ALuClock3&amp;size=xs&amp;font=geist&amp;split=true&amp;mode=dark"
        alt="" height="22"><time class="sr" datetime="__BUILT__">Last deployed __BUILT_UTC__</time></a>'''


PAGE = r"""<!doctype html>
<!-- `data-view` here as well as in `state`, because the reader looks at this page for the length of a
     561 KB fetch before any script has an opinion about it. Without it the table's column headings sit
     over an empty body until `data.json` lands and then vanish; with it the default view is the one that
     was there all along. A `#view=table` link still lands on the table -- `readHash` cannot run before
     the data either way, so this attribute governs the wait and nothing more. Keep the two in step. -->
<html lang="en" data-theme="dark" data-view="__DEFAULT_VIEW__" data-index-screenshots="__INDEX_SCREENSHOTS__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome Agentic Atlas — browse every agentic tool</title>
<meta name="description" content="__COUNT__ agentic AI projects from __LISTS__ awesome-lists, merged, deduplicated and filterable by topic, harness and operating system.">
<meta property="og:title" content="Awesome Agentic Atlas">
<meta property="og:description" content="__COUNT__ projects from __LISTS__ awesome-lists, one filterable index.">
__OGIMAGE__
<link rel="canonical" href="__SITE__">
<!-- Google Search Console's HTML-tag verification, and nothing else: this whole line is absent until a
     token exists, because `verification()` matches the placeholder's newline too. It is the discovery
     mechanism `robots.txt` on this deployment cannot be -- a project Pages site's robots.txt is never
     read, so the 1,452 URLs in sitemap.xml have to be *submitted*, and submitting them needs a verified
     property. See `VERIFY_TOKEN` in this file, and JFH-206 for the manual half nobody can automate. -->
__VERIFY__
<!-- Autodiscovery for the arrivals feed. Relative, like the `fetch("data.json")` this page already does,
     so it resolves on Pages and from a local `python -m http.server` alike. GitHub Pages serves .xml as
     text/xml and cannot be told otherwise, so the `type` here is what actually declares the format --
     readers sniff the root element regardless, but the link tag is where a browser looks first. -->
<link rel="alternate" type="application/atom+xml" title="Awesome Agentic Atlas — new arrivals"
      href="feed.xml">
<link rel="alternate" type="application/feed+json" title="Awesome Agentic Atlas — new arrivals"
      href="feed.json">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<!-- Installability, and the offline shell. Every href relative, so the /awesome-agentic-atlas/ path
     prefix Pages adds takes care of itself. Both files are written by `scripts/24_pwa.py`; if that stage
     has not run, the manifest link 404s and the registration at the foot of this page rejects into an
     empty catch, which is the whole failure. -->
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<!-- One `theme-color`, managed by script, rather than the two `media` variants that would be the obvious
     way to write this. The HTML spec picks the *first* such element whose media matches, so a pair keyed
     on `prefers-color-scheme` cannot be overridden by anything appended later -- and this page lets a
     reader choose a theme against their OS preference and remembers it, so the pair would paint the
     browser chrome the opposite colour to the page for exactly those readers. The value here is `--plane`
     in dark, because `--plane` is the header's background and the header is what sits under the chrome;
     it is a literal because the stylesheet below has not parsed yet when the next script runs. With
     JavaScript off it stays this value, which agrees with the `data-theme="dark"` floor on <html>. -->
<meta name="theme-color" id="tc" content="#101217">
<!-- Ahead of the stylesheet deliberately, and inline rather than in a file: this has to settle the theme
     before first paint. A reader who chose light, or whose OS asks for light, otherwise gets a frame of
     near-black before the toggle catches up, and an external script is one more round trip during which
     the wrong theme is on screen.

     Precedence is explicit choice, then the operating system, then dark. Dark stays the fallback because
     it is the designed mode -- the one whose accent contrast ratios were actually measured. The markup's
     data-theme="dark" is the floor if this throws, which localStorage does in some private modes. -->
<script>
try {
  var t = localStorage.getItem("theme");
  if (t !== "light" && t !== "dark")
    t = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  document.documentElement.dataset.theme = t;
  // The two literals track --plane in the two blocks below. After paint `wire()` re-derives this from the
  // computed value so the stylesheet stays the single source of truth; here there is no computed value to
  // read yet, and a chrome one shade out for one frame is the cost of not blocking the paint on a
  // stylesheet.
  document.getElementById("tc").content = t === "light" ? "#FAFBFC" : "#101217";
} catch (e) {}
</script>
<style>
/* A restrained product palette: graphite layers in dark mode and soft cool-grey layers in light. Dark
   uses amber-gold for actions while light keeps the deeper indigo that reads cleanly on pale surfaces.
   Blue is reserved for links, while green and coral/amber carry status.
   The foregrounds are softened off pure white/black so long tables and Markdown remain comfortable.

   --onbar flips between the modes because --bar, --good and --warn are used both as text and as filled
   controls. `tests/theme_test.py` derives those roles from the stylesheet and verifies every text,
   control and focus-ring pairing rather than trusting this description. */
:root{
  --surface:#090A0D; --plane:#101217; --band:#20242D; --ink:#F7F8FA; --ink2:#D0D5DD;
  --muted:#9BA5B3; --grid:#3A414D; --link:#78B7F4; --bar:#D6A034;
  --good:#5BD5AA; --warn:#EF7D86; --off:#9BA5B3; --onbar:#090A0D;
  --accent-sky:#78B7F4; --accent-mint:#5BD5AA; --accent-gold:#E7B64D;
  --accent-coral:#EF7D86; --accent-violet:#A99AF7;
}
html[data-theme=light]{
  --surface:#F2F4F7; --plane:#FAFBFC; --band:#E7EAF0; --ink:#14171C; --ink2:#353C47;
  --muted:#596574; --grid:#CAD1DB; --link:#1D5E9E; --bar:#6557C8;
  --good:#187557; --warn:#875A19; --off:#596574; --onbar:#FFFFFF;
  --accent-sky:#1D5E9E; --accent-mint:#187557; --accent-gold:#9A6718;
  --accent-coral:#B6465E; --accent-violet:#6557C8;
}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);
  font:15px/1.5 "Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
/* Only #q had a focus ring, so every chip, the sort menu and both nav buttons were invisible to anyone
   driving this page from the keyboard. :focus-visible rather than :focus so a mouse click does not leave
   a ring behind on the chip that was pressed. */
:focus-visible{outline:2px solid var(--bar);outline-offset:2px;border-radius:4px}
/* Off screen rather than display:none or visibility:hidden -- both of those take the text out of the
   accessibility tree as well as off the screen, which defeats the point. */
.sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;
  clip-path:inset(50%);white-space:nowrap;border:0}
/* Six control rows sit between the top of the document and the first result, and a screen-reader or
   keyboard reader had to walk all of them on every visit. Hidden until focused, which is the only
   state in which it is useful. */
.skip{position:absolute;left:-999px;top:0;z-index:40;background:var(--bar);color:var(--onbar);
  padding:10px 16px;border-radius:0 0 8px 0;font-weight:600}
.skip:focus{left:0}
/* NOT STICKY, AND THAT IS THE FIX FOR JFH-354. This was pinned to keep Archie and the primary navigation
   in reach, and it did that by covering the search box completely. `header` and `.bar` are siblings both
   at `top:0`, so from the first scroll gesture they occupied the same band and the higher `z-index` won:
   `elementFromPoint` at the centre of `#q` returned this element's `<h1>` at 1440x900, 1024x800, 768x900
   and 390x844, with the field 100% covered on all four. The search box was not obscured, it was
   unreachable, and getting to it meant scrolling back to the top with nothing on screen saying so.

   Offsetting the bar below the header instead -- `.bar{top:var(--head-h)}` -- was measured and rejected:
   it uncovers the field and then pins the sum of both, 51% of the viewport at 1440x900 and 86% at
   1024x800. The masthead cannot be made short enough to fix that, because Archie is 177px of a 216px
   header whose text block is 96px.

   So the masthead scrolls away and the bar keeps the top of the screen: 7% of the viewport at 1440x900,
   11% at 1024x800, 12% at 768x900, 20% at 390x844. Nothing pinned here is needed while reading rows --
   the title, the tagline, the mascot, the nav to the other pages and the theme chip are all things you
   use on arrival -- and the one thing that is needed is in the bar.

   `position:relative` with a `z-index` *under* the bar's 20, not `static`: Archie's speech bubble is
   absolutely positioned inside this element, so the header still needs a stacking context, and while the
   masthead is halfway off the top the bar is pinned across it. Whatever is pinned paints over whatever is
   scrolling, which is why 10 and not 30. The shadow moves to the bar for the same reason: it belongs to
   the element that floats over the results, and that is no longer this one. */
header{position:relative;z-index:10;background:var(--plane);border-bottom:1px solid var(--grid);
  padding:22px 20px 16px}
.wrap{max-width:1500px;margin:0 auto}
h1{margin:0 0 4px;font-size:26px;letter-spacing:-.02em}
h1 span{color:var(--muted);font-weight:400;font-size:15px;letter-spacing:0}
.sub{color:var(--ink2);font-size:14px;margin:0}
.sub b{color:var(--ink)}
/* The snapshot's age, shown only when it is bad news. A green "3 days ago" beside the date was telling
   the reader twice over that the site is current, because the "last deployed" badge below says it in the
   same header -- so the healthy case is now just the date, and this is what is left of the pair: amber,
   once the daily build has stopped keeping up and the star counts on the page are measurably drifting.
   The two dates are not the same fact -- this one is when the data was captured, the badge is when the
   copy was published -- but "is this current" is one question, and it only needs one answer. */
.stale{color:var(--warn);font-weight:600}
/* Shieldcn supplies the badge's SVG, typography and clock. The semantic time remains local so the link
   keeps an accessible name, works with the live Last-Modified correction, and still says something if
   the third-party image is unavailable. */
.stamp{display:inline-block;height:22px;margin:8px 0 0;border-radius:6px;text-decoration:none;
  vertical-align:top;box-shadow:0 0 0 1px color-mix(in srgb,var(--grid) 70%,transparent)}
.deploy-badge{display:block;width:auto;height:22px;border:0;border-radius:6px}
.stamp:hover,.stamp:focus-visible{box-shadow:0 0 0 2px var(--bar)}
.stamp:focus-visible{outline:none}
/* The tighter badge fits a 320px phone with both words intact, so its accessible and visible labels stay
   the same at every width. */
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.headside{display:flex;align-items:flex-start;justify-content:flex-end;gap:18px}
.top nav{font-size:13px;color:var(--muted);text-align:right;line-height:1.9}
.atlas-byte-wrap{position:relative;flex:0 0 auto;width:128px;isolation:isolate;
  transition:transform .18s ease}
.atlas-byte-wrap:before{content:"";position:absolute;inset:14% 2% 10%;z-index:-1;border-radius:50%;
  background:radial-gradient(circle,color-mix(in srgb,var(--bar) 17%,transparent),transparent 68%);
  filter:blur(7px)}
.atlas-byte{display:block;width:128px;height:auto;filter:drop-shadow(0 12px 18px rgba(0,0,0,.3));
  animation:atlas-byte-float 4.2s ease-in-out infinite;transform-origin:50% 72%}
.atlas-byte-wrap:hover{transform:rotate(2deg) scale(1.035)}
#byte-tip{display:block;padding:0;border:0;background:transparent;border-radius:50%;color:inherit}
/* Two lines by design. "Archie 'Atlas' Algorithm" is 24 characters where "Atlas Byte" was 10, and the
   mascot's column is 128px, so a single-line pill would have overflowed the column and run into the nav
   beside it. Wrapping inside the column keeps the name in the mascot's own width; below 641px the column is
   82px and no two-line arrangement of the full name survives a font change, so the pill shows one word there
   instead -- see the narrow-width rule at the bottom of this stylesheet. The radius drops from a 999px
   stadium, which reads as a lozenge once there are two lines, to a rounded rectangle that stays a name tag. */
.atlas-name{display:block;margin:-11px auto 0;position:relative;z-index:2;padding:3px 9px;
  border:1px solid var(--grid);border-radius:12px;background:var(--plane);color:var(--ink);
  font-size:10px;font-weight:700;letter-spacing:.03em;line-height:1.35;text-align:center;
  text-wrap:balance}
/* Full name here, one word at the narrow breakpoint; the swap is at the bottom of this stylesheet. Both are in
   the markup rather than one being written by script, so the pill is right in the first painted frame and
   right with JavaScript off. There is 25% of slack for the two-line arrangement at this width -- 108px of
   content against 81px for the worst face measured -- so this one is not font-dependent. */
.atlas-name-short{display:none}
.atlas-name:hover{border-color:var(--bar);color:var(--ink)}
.byte-quiet{display:block;margin:5px auto 0;padding:0;border:0;background:transparent;color:var(--muted);
  font-size:10px;text-decoration:underline;text-underline-offset:2px}
.byte-quiet:hover{color:var(--ink)}
/* THE MASTHEAD HAS EXACTLY ONE HOLE THIS FITS IN, and both of the obvious anchors miss it. The original
   `right:calc(100% + 12px); top:8px` put the bubble immediately left of the mascot at the nav's own height,
   and the only thing there is `.top nav` -- so it covered the navigation at every text length, not merely
   when the text was long. Hanging it under the mascot instead (`top:calc(100% + 10px)`) clears the nav and
   was measured landing on the filter bar's Ctrl/K hint at 1440 and over the search field itself at 375,
   which is the same defect with a different victim.
   What is actually free is the band left of the mascot and BELOW the nav: the nav is four short lines
   (338x86 at 1440, counted as line boxes rather than by eye) and the mascot column is taller than they are,
   so bottom-aligning to the wrap puts the bubble in that gap. Measured clear of both `.top nav` and `.bar`
   from 1500px down to 641, and the gap is 38px there -- about one and a half nav lines, not a generous margin.
   THAT GAP IS SPENDABLE, AND A READER CAN SPEND IT. Forcing the nav's type up the way Chrome's minimum font
   size setting does: 26px of clearance at 16px, 7px at 20px, and at 24px -- that setting's maximum -- the
   rectangles overlap by 13px. What does NOT happen then is the thing this ticket is about. The header's own
   `z-index:30` beats this bubble's 4, so the nav paints over it: `elementFromPoint` at the centre of all seven
   nav links returns the link, at every size from 16px to 32px. The reader loses the tail of a fact, which is
   an optional flourish, and keeps the navigation, which is not. Asserted in cards-check at 24px.
   `z-index:4` clears `#atlas-orbit` (3) and `.atlas-name` (2) inside the wrap's isolated stacking context;
   the header's own `z-index:30` already carries it over the sticky filter bar.
   The width was `min(270px,calc(100vw - 200px))` and the second arm was inert: the bubble is hidden at 640
   and below, and at 641 that arm is 441px, so 270 always won. A clamp that cannot clamp is worse than no
   clamp, because it reads as protection that is not there.
   220 AND NOT 270, WHICH IS A SEPARATE CUT FROM THE LINE COUNT AND WAS ASKED FOR SEPARATELY. Bottom-aligning
   and capping at two lines already stopped the box covering anything -- what a reader saw before was 270x219
   at its worst, twelve lines of somebody else's GitHub "about" field, and it sat on a nav link, the facet
   line and the filter bar (sampled down its left edge with `elementFromPoint`, against the same points with
   the bubble hidden). Two lines is 53px, and 53px cannot leave the masthead, which is opaque and paints at
   `z-index:30`. So the remaining width was not covering results. It was still a 270px rectangle over the
   navigation, and narrower is better as long as narrower is honest -- see `SAY_MAX` below, which is what
   pays for this. 220x53 is 11,660px2 against the 59,130 a reader gets today: 80% less box. */
/* TWO LINES GEOMETRICALLY, BECAUSE `SAY_MAX` BUYS TWO LINES ONLY IN THE FONT IT WAS MEASURED IN. The cap was
   derived by rendering every string into this box on a Windows stack that resolves to Segoe UI. CI renders it
   on ubuntu-latest, whose Chromium resolves the same stack to a wider face, and there the worst string --
   "OpenCode comes from anomalyco. Tagged for opencode." -- takes three lines and the box grows to 70px. A
   character cap cannot fix that in general: wrapping is set by where the spaces fall, not by how many
   characters there are, so a 50-character string can need three lines where an artificial 53-character one
   needs two. The clamp makes the bound geometric instead of typographic, so it holds in any face: measured
   h=53 with the box two lines tall in Segoe UI, forced monospace and forced Verdana alike, where the
   unclamped rule gives 70 in the latter two. On the shipped stack nothing is clipped, so a reader sees no
   change at all; on a wider face the tail of the longest sentence is cut rather than the masthead growing,
   which is the trade this ticket asked for.
   Rejected: `max-height:calc(2 * 1.38em)`. It bounds the CONTENT box to two lines and the element to one --
   measured h=33, one line -- because the em length knows nothing about the 9px padding and 1px border.
   `#byte-speech[hidden]` IS NOT DECORATION, and leaving it out is how this rule ships a permanently visible
   bubble. `hidden` works through the UA stylesheet's `[hidden]{display:none}`, which any author `display`
   declaration outranks -- and this rule now has one. Measured: with the clamp and without this line, a bubble
   whose `hidden` attribute is set computes `display:flow-root` and takes a 20px box. Every assertion in
   cards-check that checks Archie has stopped speaking reads the ATTRIBUTE, which is still true, so all seven
   of them stay green while the bubble sits on the masthead forever. There is now one that reads the box. */
#byte-speech{position:absolute;right:calc(100% + 12px);bottom:0;width:220px;
  padding:9px 11px;border:1px solid var(--grid);border-left:3px solid var(--bar);border-radius:9px;
  background:var(--band);color:var(--ink2);font-size:12px;line-height:1.38;z-index:4;
  box-shadow:0 12px 28px rgba(0,0,0,.2);
  display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;overflow:hidden}
#byte-speech[hidden]{display:none}
#byte-speech::after{content:"";position:absolute;right:-6px;bottom:12px;width:11px;height:11px;
  background:var(--band);border-top:1px solid var(--grid);border-right:1px solid var(--grid);transform:rotate(45deg)}
#atlas-orbit{position:absolute;inset:-18px -24px;pointer-events:none;z-index:3}
.orbit-star{position:absolute;left:50%;top:50%;width:5px;height:5px;background:var(--bar);box-shadow:0 0 10px var(--bar);
  transform:rotate(var(--orbit-angle)) translateY(-58px) rotate(45deg);animation:atlas-orbit 1.45s ease-out both}
.orbit-star:nth-child(odd){background:var(--accent-sky);box-shadow:0 0 10px var(--accent-sky)}
@keyframes atlas-orbit{0%{opacity:0;transform:rotate(var(--orbit-angle)) translateY(-16px) rotate(45deg) scale(.4)}20%{opacity:1}100%{opacity:0;transform:rotate(var(--orbit-angle)) translateY(-78px) rotate(45deg) scale(1)}}
@keyframes atlas-byte-float{
  0%,100%{transform:translateY(0) rotate(-.6deg)}
  50%{transform:translateY(-5px) rotate(.8deg)}
}
@media(prefers-reduced-motion:reduce){
  .atlas-byte,.atlas-byte-wrap{animation:none;transition:none}
  .orbit-star{animation:none;opacity:1;transform:rotate(var(--orbit-angle)) translateY(-58px) rotate(45deg)}
}
button{font:inherit;cursor:pointer}
/* The only pinned thing on the page, and therefore the only thing that carries the shadow. */
.bar{position:sticky;top:0;z-index:20;background:var(--plane);
  border-bottom:1px solid var(--grid);padding:10px 20px;box-shadow:0 8px 20px rgba(0,0,0,.12)}
.bar .wrap{display:flex;flex-direction:column;gap:8px}
/* THE HALF OF THE BAR THAT DOES NOT STICK (JFH-354). The three facet rails are in `#sheet`, and they used
   to be inside `.bar` -- which meant the pinned band was 240px at 1440x900 and 403px at 768x900, most of
   it rows a reader scrolling results is not reading. They are not hidden and they have not moved: this
   wrapper sits immediately after the bar, so it renders in exactly the place it always did and `#q`'s
   unscrolled position is unchanged at every width. It simply is not part of what survives a scroll.

   No JavaScript, no scroll listener, no stuck-state sentinel and no measured `--head-h`. A sticky element
   that changes height while stuck moves everything below it, which is a jump to compensate for and a
   threshold to add hysteresis to; a sticky element that was never that tall has neither.

   The border and the padding are the bar's old bottom edge, moved down here: the bar keeps its own so the
   pinned line has an edge of its own while scrolled, which is what makes the two read as one block at rest
   and as chrome-over-content in motion. */
.subbar{background:var(--plane);border-bottom:1px solid var(--grid);padding:0 20px 9px}
.subbar .wrap{display:flex;flex-direction:column;gap:8px}
.line{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.line>label{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em;
  min-width:74px}
#q{flex:1;min-width:220px;background:var(--surface);color:var(--ink);
  border:1px solid var(--grid);border-radius:7px;padding:9px 12px;font:inherit}
#q:focus{outline:2px solid var(--bar);outline-offset:-1px}
select{background:var(--surface);color:var(--ink);border:1px solid var(--grid);
  border-radius:7px;padding:8px 10px;font:inherit;max-width:100%}
.chip{background:var(--band);color:var(--ink2);border:1px solid var(--grid);
  border-radius:999px;padding:5px 12px;font-size:13px;white-space:nowrap}
.chip:hover{border-color:var(--bar);color:var(--ink)}
.chip[aria-pressed=true]{background:var(--bar);border-color:var(--bar);color:var(--onbar);
  font-weight:600}
/* The new-arrivals chip wears `--warn` rather than the `--bar` every other chip uses, because it
   is the only filter that answers a question about time rather than about the data. It is also the only
   chip that can be absent: with nothing inside the window there is nothing to filter to, and a control
   that selects zero rows is worse than no control. */
.newchip{display:none;align-items:center;gap:.4em}
.newchip.on{display:inline-flex}
.newchip[aria-pressed=true]{background:var(--warn);border-color:var(--warn);color:var(--onbar)}
.newchip:hover{border-color:var(--warn)}
.ni{width:1em;height:1em;flex:none;vertical-align:-.12em}
.ni>.a{fill:var(--warn)}
.ni>.b{fill:var(--bar)}
.newchip[aria-pressed=true] .ni>.a,.newchip[aria-pressed=true] .ni>.b{fill:var(--onbar)}
/* The since-your-last-visit chip keeps the plain `--bar` every ordinary filter wears, and does not borrow
   `--warn` from the chip beside it even though the two answer the same question. `--warn` here means "the
   atlas says this is the latest news", which is the same for every reader; this one means "your machine has
   not seen this", which is true of nobody else. Two accents for two kinds of claim, and the reader who has
   been away a month gets a number the New chip cannot give them. Hidden until there is a last visit to
   count from, like `.newchip` above. */
.sincechip{display:none}
.sincechip.on{display:inline-block}
.nm .ni{margin-right:.34em}
.newon{color:var(--warn);font-size:12px;font-weight:600;white-space:nowrap}
/* "by meaning", on a row the semantic pass added. Built like a `.tag` rather than like `.newon`, because
   it is a statement about *this search* and not a property of the project -- the pill reads as a badge the
   row is wearing today, where bare coloured text beside the title reads as a fact about the repository.
   `--link` and not `--warn` or `--good`: those two are already spoken for by the new-arrivals mark and by
   the rising/verdict pair, and a fourth question wearing a third question's colour makes the two read as
   one. It borrows the colour the page already uses for "this is a way through", which is what this is. */
.senseon{display:inline-block;border:1px solid var(--link);border-radius:5px;padding:1px 6px;
  font-size:11px;font-weight:600;color:var(--link);white-space:nowrap;vertical-align:1px}
/* Rising wears `--good`, where the new-arrivals chip wears `--warn` and every other chip wears `--bar`.
   Three questions get three colours because a reader asks all three of a row at once -- is it alive, did it just
   arrive, is anyone arriving now -- and two of them sharing an accent would make the pair read as one
   control. `--good` is not overloaded by this: its only other use is a stated platform verdict, which
   lives in its own column and reads as a tick rather than as a number.
   Like the new-arrivals chip this one can be absent, and for a stronger reason: until the ledger
   `25_velocity.py` writes holds a sample a week old there is no such thing as a rising row, so the chip
   would select zero of 1,294 and the sort would rank a column that is empty everywhere. */
.risechip{display:none}
.risechip.on{display:inline-block}
.risechip[aria-pressed=true]{background:var(--good);border-color:var(--good);color:var(--onbar)}
.risechip:hover{border-color:var(--good)}
/* Saved wears the `--bar` every ordinary chip wears, and that is the decision rather than an omission.
   `--warn` and `--good` above are properties *of a repo* -- it arrived recently, it is gaining stars --
   and they are held to three colours for three questions. Saved is a fact about the reader, true of nothing on the
   server, so giving it a fourth accent would say "here is a fourth thing about this project" about a
   thing that is not about the project at all.
   Absent while it would select nothing, like the two above, but revealed from `render()` rather than from
   `buildChips` -- the counts those two show are fixed when the page is built, and this one changes the
   moment a reader presses Save. */
.savechip{display:none}
.savechip.on{display:inline-block}
.savechip[aria-pressed=true]{background:var(--bar);border-color:var(--bar);color:var(--onbar)}
/* Shown only while the saved filter is on, so "remove everything" is reachable exactly where a reader is
   looking at everything they saved, and nowhere near the rest of the time. Wears no accent: it is
   destructive and the accents on this bar all mean "selected". */
.clearsave{display:none}
.clearsave.on{display:inline-block}
/* The way off this page, and the only control on the row that selects nothing: it opens a dialog. So it
   carries `aria-haspopup` rather than `aria-pressed` -- the distinction the Filters handle makes against the
   chips beside it -- and it never takes the filled accent, which everywhere else on this bar means
   "selected". Hidden until `expWire()` has both the flag and a `<dialog>` that opens modally, for the reason
   the palette hint is: a control that opens nothing is worse than no control. */
.takechip{display:none}
.takechip.on{display:inline-flex;align-items:center;gap:.4em}
/* The other control on this row that selects nothing, hidden by the same mechanism and for the same two
   reasons -- see the constellation block further down for what it opens. */
.mapchip{display:none}
.mapchip.on{display:inline-flex;align-items:center;gap:.4em}
/* The collapsed comparison, and the reason there is no strip pinned to the bottom of the viewport. The tray
   this is standing in for wanted to be `position:fixed;bottom:0`, and that has one defect no styling fixes:
   a fixed strip is read last in the DOM and seen first on the screen, or read first and seen last, and either
   way the reader driving the page from the keyboard reaches it in a place that does not match where it is.
   The bar is already sticky. A chip on it is visible at every scroll position for free, in the reading order
   it occupies, next to the other count on the row.

   `aria-expanded` and not `aria-pressed`, which is the same distinction `.takechip` draws: every chip above
   these two selects rows, and neither of these does. This one discloses `#cmp`, which is what `aria-controls`
   names; that one opens a dialog. Absent at zero like the Saved chip, and revealed from `render()` for the
   same reason -- what it counts is something the reader changes while the page is open. */
.cmpchip{display:none}
.cmpchip.on{display:inline-block}
.cmpchip[aria-expanded=true]{background:var(--bar);border-color:var(--bar);color:var(--onbar)}
/* The per-row control. A word rather than a glyph, deliberately: the obvious glyph is a star, and this
   button sits two cells from a column of GitHub star counts -- a filled star beside "4,300" would be
   asking which of the two it meant. It also needs no sprite entry and no accessible name of its own,
   because the word *is* the name. `aria-pressed` carries the state; the label says which project, since a
   screen reader arrives at this button 120 times a page. */
.save{background:var(--band);color:var(--ink2);border:1px solid var(--grid);border-radius:999px;
  padding:1px 9px;font-family:inherit;font-size:11px;font-weight:600;line-height:1.7;
  white-space:nowrap;cursor:pointer;margin-left:8px;vertical-align:1px}
.save:hover{border-color:var(--bar);color:var(--ink)}
.save[aria-pressed=true]{background:var(--bar);border-color:var(--bar);color:var(--onbar)}
/* The comparison pin, beside Save. Same pill and the same pressed pair, which is a decision and not laziness:
   `--bar`/`--onbar` is one of the pairs `theme_test.py` already holds to a contrast ratio in both palettes,
   and inventing a fifth accent for this would mean either a fourth "thing about the project" -- see the
   `.savechip` note above for why that is wrong -- or a colour nothing checks. The two buttons are told apart
   by their words, which is also the only channel that survives the print sheet and a screen reader.

   A word and not a glyph, for the reason `.save` gives: the obvious glyph is a checkbox, this cell already
   holds a pill that toggles, and a second silent square beside it would be asking which of the two selects. */
.pin{background:var(--band);color:var(--ink2);border:1px solid var(--grid);border-radius:999px;
  padding:1px 9px;font-family:inherit;font-size:11px;font-weight:600;line-height:1.7;
  white-space:nowrap;cursor:pointer;margin-left:6px;vertical-align:1px}
.pin:hover:not(:disabled){border-color:var(--bar);color:var(--ink)}
.pin[aria-pressed=true]{background:var(--bar);border-color:var(--bar);color:var(--onbar)}
/* Disabled at the cap rather than hidden, which is the opposite of what the chips on the bar do and is right
   for the opposite reason. A chip that selects nothing is noise on a control strip a reader scans once. This
   is 1,290 buttons in the results, and removing them the instant the fourth pin lands would reflow every card
   under the reader's finger and give no reason for it. Disabled costs one attribute, keeps the layout still,
   and `pinLabel` puts the reason in the accessible name where a reader who cannot see the dimming gets it. */
.pin:disabled{opacity:.45;cursor:not-allowed}
/* Tabular figures because this sits directly under a star count that already has them, and a proportional
   "+1,182" under a tabular "388,645" makes one column look like two. A fall is drawn in the muted grey and
   not in a red: stars do go down, it is far more often a recount or a transfer than an exodus, and this
   project does not have the evidence to call it a verdict. */
.rise{color:var(--good);font-weight:600;font-variant-numeric:tabular-nums}
.rise.down{color:var(--muted);font-weight:400}
.count{color:var(--muted);font-size:13px;margin-left:auto;white-space:nowrap}
.count b{color:var(--ink)}
/* ---- The filter sheet --------------------------------------------------------------------------------
   The bar carries four control rows and 27 chips. That is right on a 1500px desktop and it is the whole of
   the mobile complaint: on a 375px phone the four rows measured 296px, 36% of the screen, and the two long
   facets were horizontal rails scrolled one chip at a time. So below the table breakpoint the three facet
   rows become a sheet the reader opens, and the handle on it carries the number of filters behind it --
   which is the one thing that must stay legible while it is shut, or shutting the sheet hides the state as
   well as the controls.

   Everything below is inert until `buildChips` puts `data-fb` on <html>, and inert on a wide screen either
   way: there the sheet is a plain block in the bar, exactly what the three rows already were, and the
   handle is not rendered at all. That is load-bearing rather than tidy. `buildChips` only runs once
   `data.json` has arrived, and a handle whose click has not been wired must never become the only way to
   reach the filters -- so the failure mode of the fetch never being answered is today's bar and not a
   sheet nothing can open. */
#sheet{display:flex;flex-direction:column;gap:inherit}
/* `inherit` and not `8px`. The bar's own `gap` is 8px, and 5px once the compact query below applies; this
   wrapper has just been inserted between it and the three rows that used to be its direct flex children,
   so restating either number here is exactly how the two would come to disagree. */
#fbt{display:none;align-items:center;gap:.5em}
/* The count as a filled badge rather than "Filters (3)", because a shut sheet is glanced at and not read.
   Hidden when it is empty: `min-width` would otherwise leave a small filled dot meaning zero. */
#fbn{display:inline-flex;align-items:center;justify-content:center;min-width:1.4em;padding:0 .3em;
  border-radius:999px;background:var(--bar);color:var(--onbar);font-size:12px;font-weight:700;
  line-height:1.4;font-variant-numeric:tabular-nums}
#fbt:not(.act) #fbn{display:none}
/* With something selected the handle takes the accent a pressed chip takes, because at that point it is
   one. The badge inverts so it stays readable on the fill -- `--onbar` is dark ink in dark mode and white
   in light, so the pair swaps correctly in both without a second value. */
#fbt.act{background:var(--bar);border-color:var(--bar);color:var(--onbar);font-weight:600}
#fbt.act #fbn{background:var(--onbar);color:var(--bar)}
/* The sheet's own header and the backdrop behind it exist only in the sheet's narrow form. On a desktop
   there is nothing to head and nothing to dim. */
.shead{display:none}
#fbb{display:none}
main{padding:0 20px 64px}
table{width:100%;border-collapse:collapse;margin-top:14px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
  padding:8px 10px;border-bottom:1px solid var(--grid);position:sticky;top:0;background:var(--surface)}
th.n,td.n{text-align:right}
th.c,td.c{text-align:center}
td{padding:12px 10px;border-bottom:1px solid var(--grid);vertical-align:top}
/* Alternating surfaces make long ranked tables trackable without turning every row into a box. Scoped to
   table view so these cell fills cannot stripe the stacked card layout. */
html[data-view=table] tbody tr:nth-child(odd) td{background:var(--plane)}
html[data-view=table] tbody tr:nth-child(even) td{background:var(--band)}
/* Guarded, because a touch device reports a hover that then latches: tapping a row anywhere -- to
   follow its link, or just while scrolling -- left it tinted until something else was tapped. */
@media(hover:hover){
  html[data-view=table] tbody tr:hover td{
    background:color-mix(in srgb,var(--bar) 10%,var(--band));box-shadow:inset 0 -2px 0 var(--bar)}
}
/* NEW ARRIVALS WEAR AN OUTLINE, AND IT IS DRAWN TWICE
   ---------------------------------------------------
   `.nw` is on the row when the row belongs to the current cohort -- what the most recent import brought.
   Two views, two mechanisms, and the split is forced rather than chosen: `table{border-collapse:collapse}`
   above means a `<tr>` has no box of its own to hang a `box-shadow` on, and one set on it does not render
   at all. So table view draws the edge as `inset` shadows on the *cells* -- the same trick as the hover
   rule directly above -- while cards view, where a row is a grid and does have a box, gets a real ring.
   Both are `--warn`, the page's established colour for this-is-new, and deliberately not `--card-accent`:
   the accent means "this project", so a ring in it would be decoration that says nothing.

   Top and bottom insets on every cell run the width of the row because the cells are adjacent; the two end
   caps are `background-image` on the first and last cell rather than more `box-shadow`, which keeps the
   whole shadow track free for `new-edge` to animate. An animated property outranks the cascade, so the
   pulse survives the hover rule above without either needing to know about the other, and the row keeps
   both its zebra fill and the pointer's tint because nothing here writes a background colour at all.

   That last part started as a `--warn` wash behind the whole row and is deliberately gone. `.newon` -- the
   "Added 09/21/26" beside the title -- is `--warn` text at 12px bold, which WCAG scores as body text at
   4.5:1, and it clears that on `--band` by a whisker: 4.97 in the light palette. A 9% wash of its own colour
   behind it took the same pair to 4.42, and the pointer tint on top of that to 3.80. So the edge is the only
   thing drawn, the fill is left alone, and every contrast this page already guaranteed still holds. */
html[data-view=table] tbody tr.nw td{
  box-shadow:inset 0 1px 0 var(--warn),inset 0 -1px 0 var(--warn);
  animation:new-edge 3s ease-in-out 5}
html[data-view=table] tbody tr.nw td:first-child{
  background-image:linear-gradient(to right,var(--warn) 0 3px,transparent 3px)}
html[data-view=table] tbody tr.nw td:last-child{
  background-image:linear-gradient(to left,var(--warn) 0 3px,transparent 3px)}
/* The table pulse is thickness and nothing else -- no inner glow, for the reason the wash is gone. An
   `inset` shadow paints between the cell's background and its text, so a blurred one reaching in from the
   edges of a 44px row lands behind the row's own words, which is the contrast problem above with a timer on
   it. Cards view can have the glow it wants because there the shadow is *outside* the box. */
@keyframes new-edge{
  0%,100%{box-shadow:inset 0 1px 0 var(--warn),inset 0 -1px 0 var(--warn)}
  50%{box-shadow:inset 0 3px 0 var(--warn),inset 0 -3px 0 var(--warn)}}
/* One table, three reading distances. Compact leaves the identifying facts visible for a fast scan;
   Normal keeps the useful preview; Expanded deliberately gives the evidence and install detail more air.
   The choice belongs to this browser, rather than the URL: it is a reading preference, not a claim about
   a shared filtered view. */
html[data-view=table][data-density=compact] td{padding:6px 8px}
html[data-view=table][data-density=compact] .shot,
html[data-view=table][data-density=compact] .tg,
html[data-view=table][data-density=compact] .lc{display:none}
html[data-view=table][data-density=compact] .desc{display:-webkit-box;-webkit-box-orient:vertical;
  -webkit-line-clamp:1;line-clamp:1;overflow:hidden;font-size:12px;max-width:34em}
html[data-view=table][data-density=compact] .cmdrow{display:none}
html[data-view=table][data-density=compact] .nm{font-size:14px}
html[data-view=table][data-density=compact] .meta{margin-top:2px}
html[data-view=table][data-density=expanded] td{padding:16px 12px}
html[data-view=table][data-density=expanded] .shot{width:280px}
html[data-view=table][data-density=expanded] .shot img{width:280px;border-radius:8px}
html[data-view=table][data-density=expanded] .desc,
html[data-view=table][data-density=expanded] .cmdrow{max-width:56em}
.rk{color:var(--muted);font-size:12px;font-variant-numeric:tabular-nums}
.shot{width:200px}
/* `aspect-ratio` is load-bearing and not decoration. These pictures have no `src` until a reader gives an
   input event -- see `cardArt()` -- and this is what makes an unsourced one occupy exactly the space the
   loaded one will, so nothing moves when it arrives. Remove it and every card image becomes a layout shift
   that arrives on someone else's schedule. Verified: with every image blocked, CLS was 0.5140; with them
   all loading, 0.5140 (JFH-216). */
.shot img{width:200px;aspect-ratio:2/1;object-fit:cover;border-radius:6px;
  background:var(--band);border:1px solid var(--grid);display:block}
.shot-fallback{display:grid;place-items:center;min-height:100px;padding:12px;background:var(--band);
  border:1px solid var(--grid);border-radius:6px;color:var(--muted);font-size:12px;text-align:center}
/* These two set the table's width. Auto table layout takes the widest unbreakable run in the column
   across every row on the page, and neither a slash nor a comma is a break opportunity in Chrome or
   Safari -- so `muratcankoylan/Agent-` and a blurb naming
   `.cursorrules/CLAUDE.md/Copilot/Windsurf/Cline/Aider` were between them demanding ~530px of a 335px
   content box, which the document then had to scroll sideways to satisfy. */
.nm{font-weight:600;font-size:15px;overflow-wrap:anywhere}
/* owner/name is now the link out to GitHub, the title having been given to the local detail page. It stays
   muted rather than picking up `--link`, because it is the secondary of the two links in the cell and a
   second accent-coloured line under every title would fight the title for attention. The class selector
   already outranks `a{color:var(--link)}` on specificity, so this needed no !important -- only the hover,
   which is what tells a reader it is clickable at all now that the colour does not. */
.nwo{display:block;color:var(--muted);font-size:12px;margin-top:2px;word-break:break-all}
a.nwo:hover{color:var(--ink)}
.st{font-size:16px;font-weight:700;font-variant-numeric:tabular-nums}
.st.none{font-size:13px;font-weight:400;color:var(--muted)}
.meta{color:var(--muted);font-size:12px;margin-top:5px}
.desc{color:var(--ink2);font-size:13.5px;max-width:44em;overflow-wrap:anywhere}
.cmd{display:block;margin-top:7px;font:12px/1.5 Consolas,ui-monospace,monospace;
  color:var(--ink2);background:var(--band);border:1px solid var(--grid);border-radius:5px;
  padding:5px 8px;max-width:44em;overflow-wrap:anywhere}
/* The install line is the one thing on a row a reader wants to take with them, and taking it meant
   selecting monospace text that wraps mid-flag without catching the surrounding cell. `align-items:
   stretch` so the button matches whatever height the command wrapped to, and `min-width:0` on the code
   so a long one shrinks rather than pushing the button out of the row. */
.cmdrow{display:flex;align-items:stretch;gap:6px;max-width:44em;margin-top:7px}
.cmdrow .cmd{margin-top:0;flex:1 1 auto;min-width:0}
.copy{flex:none;background:var(--band);color:var(--ink2);border:1px solid var(--grid);
  border-radius:5px;padding:0 10px;font-size:11.5px;letter-spacing:.03em;white-space:nowrap}
.copy:hover{border-color:var(--bar);color:var(--ink)}
.copy.ok{border-color:var(--good);color:var(--good)}
.tag{display:inline-block;background:var(--band);border:1px solid var(--grid);border-radius:5px;
  padding:2px 7px;font-size:11.5px;color:var(--ink2);margin:0 4px 4px 0;white-space:nowrap}
.tag.cat{border-color:var(--bar);color:var(--ink)}
/* This rule was dead: the class was defined here but never put on an element, so the verdict row was
   rendering as plain `.meta` the whole time. The nowrap is now on each verdict rather than on the group,
   which is what it was for -- keeping a platform's mark and its ✓ together, not forcing all five onto one
   line, which on a 375px card is 260px of unbreakable text. */
.os{font-size:11.5px;letter-spacing:.02em}
.os>span{white-space:nowrap}
/* Prefixed because the verdict characters are the class names and one of them is "-", which is not a
   valid CSS identifier on its own -- ".-" invalidates the whole selector list it appears in, so the
   unprefixed version silently dropped the colour from every No, n/a and dash on the page. */
.vY{color:var(--good);font-weight:700}
.vL{color:var(--warn)}
.vN,.va,.v-{color:var(--off)}
/* Each verdict also carries a glyph -- see VERDICT in the script. Colour on its own was the only channel
   here, which is WCAG 1.4.1 and fails for a red/green deficiency, a greyscale print-out and a projector
   with the saturation turned down. The glyph is part of the text rather than a pseudo-element so it is
   copied with the row and announced by a screen reader ("check mark", "question mark"). */
.os .v-,.os .va{opacity:.75}
/* The legend for those five marks -- see the `.vkey` comment in the body for why it is a `<details>` above
   the results rather than a strip or a `<thead>` row. Closed it costs one line, which is the concession it
   makes to keeping cards above the fold; `display:inline-block` is what keeps it one line rather than a
   full-width band with a rule across the page.

   `list-style:none` plus the `::marker` reset because Safari draws the disclosure triangle through a
   pseudo-element the other engines do not use, and a legend that shows two triangles on one browser and one
   on the rest reads as a rendering bug. The caret is drawn here instead, so all three agree. */
.vkey{display:inline-block;margin:0 0 10px;font-size:12px;color:var(--dim)}
.vkey>summary{cursor:pointer;list-style:none;padding:3px 0;border-bottom:1px dotted var(--grid)}
.vkey>summary::-webkit-details-marker{display:none}
.vkey>summary::marker{content:""}
/* The disclosure triangle is drawn from borders rather than set as a character. A `content:"..."` glyph is
   read aloud by some screen readers, and `<summary>` already announces its own collapsed/expanded state, so
   the glyph would be pure noise on top of a correct announcement -- and it would depend on a font having it. */
.vkey>summary::after{content:"";display:inline-block;margin-left:7px;border:4px solid transparent;border-top-color:currentColor;transform:translateY(2px);transition:transform .12s}
.vkey[open]>summary::after{transform:translateY(-2px) rotate(180deg)}
.vkey>summary .vY,.vkey>summary .vL,.vkey>summary .vN,.vkey>summary .v-,.vkey>summary .va{font-weight:700}
/* A two-column grid rather than the default `<dl>` indent: the glyph column is sized to the widest mark so
   the five words start at one edge, which is what makes it scannable as a key instead of as prose. */
.vkey>dl{display:grid;grid-template-columns:1.4em 1fr;gap:4px 8px;margin:8px 0 0;max-width:52ch}
.vkey>dl>dt{text-align:center;font-weight:700}
.vkey>dl>dd{margin:0}
/* At phone width the key is the only thing on its line and wants the whole of it. */
@media (max-width:560px){.vkey{display:block}.vkey>dl{max-width:none}}
/* The base rule for the five platform marks comes from `scripts/osicons.py`, which is also where the shapes
   and the ids come from, so the three stylesheets that draw them cannot drift. Sizing is per-surface and
   stays here, because a chip and a verdict want different answers. */
__OSCSS__
/* Inside a filter chip the mark *is* the label -- there is no word beside it to be in proportion to -- so it
   takes about the height a word would have taken. Deliberately over 1em: a chip is 13px, and a mark matched
   to that reads as punctuation on the button rather than as the thing being chosen. */
.chip .oi{width:1.25em;height:1.25em}
/* In the row of five verdicts, a fixed 14px rather than the base `em`. The surrounding text is 11.5px, and
   1.15em of that is 13.2px -- close enough to the ✓ beside it that the pair reads as one smudge instead of
   as a platform and an answer. Two and a half pixels is the whole difference between a mark and a speck. */
.os .oi{width:14px;height:14px}
/* A repo with no push in over a year. Deliberately not a colour: amber already means "inferred" in the
   verdict column two cells away, and reusing it here would make one hue mean two things on one row. The
   dotted underline is the marker and the hint that there is a title worth hovering. */
.old{text-decoration:underline dotted;text-decoration-color:var(--muted);text-underline-offset:2px}
/* The approximate-match banner. Left-aligned and directly above the table it explains, because a centred
   notice reads as page furniture and gets skipped -- and this one has to be read, or the reader concludes
   the search ignored them. Amber like the other "this is not quite what you asked for" signals. */
.approx{margin:0 0 14px;padding:10px 14px;border-left:3px solid var(--warn);background:var(--band);
  border-radius:0 6px 6px 0;color:var(--ink2);font-size:14px}
.approx b{color:var(--ink)}
/* The command palette. Pinned near the top rather than centred, because the list grows downward and a
   centred dialog would slide the input up the screen every time the result count changed -- so the box
   you are typing into would move while you type. */
dialog#pal{border:1px solid var(--grid);background:var(--plane);color:var(--ink);border-radius:12px;
  padding:0;width:min(620px,calc(100vw - 24px));margin:8vh auto auto;overflow:hidden;
  box-shadow:0 18px 50px rgba(0,0,0,.45)}
dialog#pal::backdrop{background:rgba(0,0,0,.55)}
/* 16px is not a taste choice: iOS Safari zooms the whole page when a focused input's text is under 16px,
   and a modal that zooms on open cannot be read. */
#palq{width:100%;background:var(--surface);color:var(--ink);border:0;font-family:inherit;font-size:16px;
  border-bottom:1px solid var(--grid);padding:14px 16px}
#palq:focus{outline:none}
#palist{list-style:none;margin:0;padding:6px;overflow-y:auto;max-height:min(52vh,420px)}
#palist .grp{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.07em;
  padding:10px 10px 4px}
#palist li.it{display:flex;align-items:baseline;gap:9px;padding:8px 10px;border-radius:7px;cursor:pointer}
/* The filled accent, the same treatment a pressed chip gets, rather than `--band`. `--band` is the obvious
   choice and it is wrong in both themes, because it is only ever one step off `--plane` by design: under
   the previous palette the selected row came out as a barely-there strip of #f4f6f6 on #eef1f2, measured
   at 1.05:1 against its own background; the explicit text is what carries the state here as well.
   A row stripe is supposed to be almost invisible; a selection is not. The highlight is the one thing
   here that cannot afford to be subtle, since it is the only indication of what Enter will do. `--onbar`
   rather than a fixed colour because it is defined as the ink a filled accent carries -- white in both
   themes under this palette, but the indirection is the point, and the muted greys below would vanish
   against the fill either way. */
#palist li.it[aria-selected=true]{background:var(--bar);color:var(--onbar)}
#palist li.it .t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#palist li.it .k,#palist li.it .s{flex-shrink:0;font-size:12px}
#palist li.it .k{color:var(--muted)}
#palist li.it .s{color:var(--warn)}
/* Inherit, not a fixed colour: on the accent fill the secondary text has to shift with `--onbar`, and
   opacity keeps it secondary without needing a second value that passes contrast on `--bar` in both themes. */
#palist li.it[aria-selected=true] .k,#palist li.it[aria-selected=true] .s{color:inherit;opacity:.72}
#palist li.it:hover:not([aria-selected=true]){background:var(--band)}
.palnone{padding:26px 12px;color:var(--muted);text-align:center}
.palfoot{display:flex;gap:14px;background:var(--surface);border-top:1px solid var(--grid);
  padding:7px 14px;color:var(--muted);font-size:12px}
kbd{background:var(--band);border:1px solid var(--grid);border-bottom-width:2px;border-radius:4px;
  padding:1px 5px;color:var(--ink2);font:11px/1.6 ui-monospace,Consolas,monospace}
/* A shortcut nobody is told about is a shortcut nobody uses, and this hint is the only affordance for it.
   Hidden until `buildChips` confirms the browser has `showModal`, like the New chip: a control that opens
   nothing is worse than no control. Hidden again on narrow screens, where there is no keyboard to press
   it with and the search row needs every pixel of the width. */
#palhint{display:none;align-items:center;gap:5px}
#palhint.on{display:inline-flex}
@media (max-width:760px){#palhint.on{display:none}}
/* ---- Take it with you --------------------------------------------------------------------------------
   The export dialog. Centred rather than pinned near the top like the palette, because nothing in it grows
   while the reader reads it -- there is no result list to slide the box up the screen. Otherwise the same
   treatment for the same reasons: a real `<dialog>` opened with `showModal()`, so the focus trap, the Esc
   key, the backdrop, the inertness of the page behind it and the return of focus to the chip that opened it
   are all the browser's rather than five things to hand-roll and get wrong. */
dialog#exp{border:1px solid var(--grid);background:var(--plane);color:var(--ink);border-radius:12px;
  padding:0;width:min(560px,calc(100vw - 24px));overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.45)}
dialog#exp::backdrop{background:rgba(0,0,0,.55)}
#exp h2{margin:0;padding:14px 16px 3px;font-size:16px}
.expsub{margin:0;padding:0 16px 12px;color:var(--muted);font-size:13px}
.expsub b{color:var(--ink2)}
/* One full-width row per destination rather than a row of pills. These are four different documents, not
   four states of one control, so each needs a sentence saying where it goes -- and a pill has nowhere to put
   one. Stacked, so the sentences read as a list of choices instead of wrapping into each other. */
.expacts{display:flex;flex-direction:column;gap:8px;padding:0 16px 12px}
.expacts button{display:flex;align-items:baseline;gap:9px;text-align:left;background:var(--band);
  color:var(--ink);border:1px solid var(--grid);border-radius:9px;padding:9px 12px;font:inherit;
  font-size:14px}
.expacts button:hover{border-color:var(--bar)}
/* Nothing to write a file from. Disabled rather than hidden, because the reader pressed Export *expecting*
   these three and a dialog that silently has one row in it reads as a rendering fault. */
.expacts button:disabled{opacity:.45}
.expacts button:disabled:hover{border-color:var(--grid)}
.expacts .t{font-weight:600;white-space:nowrap}
.expacts .k{color:var(--muted);font-size:12px}
.expurl{display:flex;gap:8px;padding:0 16px 12px}
/* The link is on screen and selectable before anything is pressed, rather than living behind a Copy button
   that either works or shrugs. `navigator.clipboard` rejects on an insecure origin, in a document that is
   not focused, and wherever the permission is refused -- and of the four exports this is the one whose whole
   payload a reader may have to lift by hand. Read-only rather than disabled: a disabled input cannot take
   focus, so it cannot be selected either, which is exactly the fallback this is for. */
#expurl{flex:1;min-width:0;background:var(--surface);color:var(--ink2);border:1px solid var(--grid);
  border-radius:7px;padding:8px 10px;font:12px/1.5 ui-monospace,Consolas,monospace}
#expurl:focus{outline:2px solid var(--bar);outline-offset:-1px}
.expnote{margin:0;padding:0 16px 12px;color:var(--muted);font-size:12px;line-height:1.5}
.expfoot{display:flex;justify-content:flex-end;background:var(--surface);
  border-top:1px solid var(--grid);padding:9px 14px}
/* ---- The constellation -------------------------------------------------------------------------------
   Almost nothing, because almost all of this feature is one `<canvas>` and the stylesheet cannot help with
   what is drawn inside it. What is here is the frame: a `<dialog>` like the other two, a stage for the
   canvas to fill, a readout that follows the pointer, a topic key and a foot.

   Bigger than the export sheet and taller than it is wide is not: the layout in `xy.bin` is roughly square
   and quantised against one shared scale for both axes precisely so that its aspect ratio survives, so a
   letterbox would waste the width and a portrait box would waste the height. `min(1180px, 100vw - 20px)`
   against `min(820px, 100vh - 20px)` is as close to that square as a browser window generally allows, and
   the renderer fits the layout inside whatever it actually gets.

   The canvas is sized in CSS and *resized* in JS, which is the one thing about a canvas that is not
   optional: `width`/`height` are the bitmap and the CSS box is the display size, so a canvas left at its
   300x150 default and stretched to 1,100px is a 300px picture scaled up. `mapFit()` sets both, off
   `devicePixelRatio`, on open and on every resize.

   `touch-action:none` so a drag pans the map instead of scrolling the dialog, and `overscroll-behavior`
   on the stage so a wheel that reaches the end of the zoom range does not start scrolling the page
   behind an inert modal. */
dialog#mapdlg{border:1px solid var(--grid);background:var(--plane);color:var(--ink);border-radius:12px;
  padding:0;width:min(1180px,calc(100vw - 20px));height:min(820px,calc(100vh - 20px));overflow:hidden;
  box-shadow:0 18px 50px rgba(0,0,0,.45);display:flex;flex-direction:column}
/* Darker than the other two backdrops. The whole point of what is behind this one is that it is a field of
   faint dots, and a 55% scrim leaves enough of the table showing to compete with them. */
dialog#mapdlg::backdrop{background:rgba(0,0,0,.74)}
.maphead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:11px 14px;
  border-bottom:1px solid var(--grid)}
.maphead h2{margin:0;font-size:16px;white-space:nowrap}
#mapwhat{margin:0;flex:1;min-width:120px;color:var(--muted);font-size:13px}
#mapwhat b{color:var(--ink2)}
.mapstage{position:relative;flex:1;min-height:0;background:var(--surface);overscroll-behavior:contain}
#mapc{display:block;width:100%;height:100%;touch-action:none;cursor:crosshair}
#mapc.drag{cursor:grabbing}
/* Follows the pointer, so it can never be under it: `pointer-events:none` means a dot at the edge of the
   readout is still hoverable, and `mapMove()` flips the box to the other side of the cursor rather than
   letting it run off the stage. */
#maptip{position:absolute;left:0;top:0;pointer-events:none;width:max-content;max-width:300px;
  background:var(--plane);border:1px solid var(--grid);border-radius:9px;padding:7px 10px;
  font-size:12px;line-height:1.5;box-shadow:0 10px 26px rgba(0,0,0,.45);z-index:2}
#maptip .tn{display:block;font-weight:600;font-size:13px;color:var(--ink)}
#maptip .tk{color:var(--muted)}
#maptip .tb{display:block;margin-top:3px;color:var(--ink2)}
/* The one thing the reader is told when the index and the data disagree, and the reason it is a sentence in
   the dialog rather than a hidden chip: the chip is only hidden when the *flag* is off, which is a decision
   somebody made. A guard that fired is a fact about this build, and a reader who pressed Map deserves to be
   told which. */
#mapnope{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;margin:0;
  padding:0 32px;text-align:center;color:var(--muted);font-size:13px;line-height:1.6}
/* `[hidden]` is a user-agent rule and the author `display` above outranks it, which is the trap the
   shared-list strip further down records. Both boxes here declare a display, so both restate the hiding. */
#mapnope[hidden],.mapkey[hidden]{display:none}
.mapkey{display:flex;flex-wrap:wrap;gap:3px 8px;padding:8px 14px;border-top:1px solid var(--grid);
  background:var(--surface);max-height:22vh;overflow-y:auto}
/* Real buttons, and this is the accessibility answer as much as a convenience. The dots cannot be reached
   by keyboard -- there are 1,294 of them and they are pixels -- but every *territory* can, and pressing one
   is the same `state.cat` the topic chips on the bar set. So the map's structure is operable without a
   pointer, and the projects themselves stay where they have always been readable: the table. */
.mapkey button{display:inline-flex;align-items:center;gap:5px;background:none;border:1px solid transparent;
  border-radius:20px;padding:2px 9px 2px 5px;color:var(--ink2);font:inherit;font-size:12px}
.mapkey button:hover{border-color:var(--grid);color:var(--ink)}
.mapkey button[aria-pressed=true]{border-color:var(--bar);background:var(--band);color:var(--ink)}
/* `--sw` is set inline per button from the same hue the canvas draws that topic with, so the key cannot
   disagree with the picture -- there is one source for the colour and it is `mapHue()`. */
.mapkey i{flex:0 0 auto;width:9px;height:9px;border-radius:50%;background:var(--sw);
  box-shadow:0 0 7px var(--sw)}
.mapkey .kn{color:var(--muted);font-variant-numeric:tabular-nums}
.mapfoot{display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--surface);
  border-top:1px solid var(--grid);padding:9px 14px}
#maphint{flex:1;min-width:0;color:var(--muted);font-size:12px}
@media (max-width:640px){
  /* Full-bleed, because at 375px a 10px inset is a border rather than breathing room -- and the key is the
     first thing to go: fourteen pills are four rows of it, which is a third of the height that should be
     showing the map. The territories stay reachable from the topic chips on the bar underneath. */
  dialog#mapdlg{width:100vw;height:100vh;max-width:none;border:0;border-radius:0}
  .mapkey{display:none}
}
/* The strip a shared list arrives under, between the filter bar and the results. That is where it belongs
   because of what it describes: not a filter the reader chose and not a property of any row, but what this
   page is *of* at the moment -- somebody else's collection. Amber like the approximate-match banner and for
   the same reason: both say "this is not the atlas you asked for, and here is why".

   Absent rather than empty until there is a list, like the Saved chip and for the same reason -- and by the
   same mechanism, a class rather than the `hidden` attribute, because `[hidden]` comes from the user-agent
   sheet and the author `display:flex` below would outrank it. */
.shared{display:none}
.shared.on{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:14px 0 0;padding:10px 14px;
  border-left:3px solid var(--warn);background:var(--band);border-radius:0 6px 6px 0;
  color:var(--ink2);font-size:14px}
.shared b{color:var(--ink)}
/* `margin-left:auto` on the pair, so the two buttons sit at the far end on a wide screen and fall under the
   sentence on a phone rather than squeezing it to one word per line. */
.shared .sp{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.empty{padding:64px 0 80px;text-align:center;color:var(--muted)}
/* "Nothing matches. Try clearing a filter." named neither the filter nor what clearing it would return,
   so the reader had to guess which of six controls was the tight one -- and it is usually not the one
   they touched last. Each button here is a filter to drop with the count it would restore. */
.empty .big{color:var(--ink);font-size:17px;font-weight:600;margin:0 0 6px}
.empty p{margin:0 0 12px}
.fixes{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.fix{background:var(--band);color:var(--ink);border:1px solid var(--grid);border-radius:999px;
  padding:7px 15px;font-size:13.5px}
.fix:hover{border-color:var(--bar)}
.fix .n{color:var(--muted);font-variant-numeric:tabular-nums}
.fix:hover .n{color:var(--ink2)}
/* Quieter than the rescue buttons above it, deliberately. Loosening a filter fixes most empty result sets,
   and a link that shouted would be pressed by readers who only mistyped -- who are already served by the
   near-match rows `near()` renders before this branch can be reached. The underline is explicit because
   `a{text-decoration:none}` above strips it from every anchor on the page and only `a:hover` puts it back,
   and a link that looks like body text until you touch it is not an affordance. */
.empty .miss{color:var(--muted);font-size:13px;text-decoration:underline}
.empty .miss:hover{color:var(--ink)}
.more{display:block;margin:26px auto 0;background:var(--band);color:var(--ink);
  border:1px solid var(--grid);border-radius:8px;padding:11px 22px;font-weight:600}
.more:hover{border-color:var(--bar)}
footer{border-top:1px solid var(--grid);background:var(--plane);padding:22px 20px;
  color:var(--muted);font-size:13px}
.blurb{color:var(--muted);font-size:13px;margin:2px 0 0}
/* Screen readers and screens both have the address bar; only paper does not. The `@media print` block at the
   end of this stylesheet is the one place this is ever visible. */
#printurl{display:none}
.facets{margin-top:14px;padding-top:12px;border-top:1px solid var(--grid);font-size:12.5px;
  line-height:1.9}
.facets p{margin:0 0 4px}
.facets b{color:var(--ink2);font-weight:600}
/* One query used to do all the responsive work here and all it did was hide two columns, so a 375px
   phone got the same layout as an 899px tablet. There are three now, because the page fails in three
   different ways: at 900px the screenshot and the detail columns stop paying for their width; below
   640px four columns stop fitting in what is left at all; and the filter bar fails on *height*, which
   is a separate axis and needs its own query -- see below. */
@media(max-width:900px){
  .shot,.hide{display:none}
  td,th{padding:9px 6px}
}

/* The filter bar competes for vertical space, so it is capped on vertical space -- either axis can
   trigger it. Width alone was not enough: a landscape phone is 844x390, wide enough to clear a 640px
   breakpoint entirely and short enough that the wrapped bar measured 360px of a 390px window. That is
   92% of the screen, which is the reported bug with the phone turned on its side.

   The failure being fixed: a `position:sticky` box taller than its scrollport pins its top edge and
   then covers the screen for the whole of the rest of the document, and the part of it that overflows
   the bottom can never be scrolled into view -- which is what put the Runs-on chips, Confirmed only
   and Clear all permanently out of reach. At 390x844 the bar measured 753px, 89% of the screen, and on
   a 375x667 phone it was taller than the viewport. The 27 topic and target chips are what grew it:
   they were wrapping to sixteen lines between them, so each facet becomes one scrollable rail. */
@media(max-width:640px),(max-height:560px){
  /* iOS Safari zooms the viewport whenever a focused control's text is under 16px, and because the
     viewport tag sets initial-scale=1 with no maximum-scale it never zooms back out again on blur. So
     one tap on the search box left the reader at ~350px of effective width, scrolling sideways, for
     the rest of the visit -- a second, self-inflicted cause of the horizontal scrolling. */
  #q,select{font-size:16px}
  .facet{flex-wrap:nowrap;gap:6px}
  .facet>label{flex:none;min-width:0;font-size:10px}
  .facet>.chip{flex:none}
  /* `flex:1 1 0` with `min-width:0` is what lets a rail sit beside its label and take the width that
     is left. Without the zero basis the rail asks for its full max-content width -- 2,400px of topic
     chips -- and gets bumped onto a line of its own, which is two rows per facet again.
     `#oses` is in here for the shape rather than for the scrolling: five marks are ~224px against the
     ~330px the five words needed, so its rail no longer overflows any phone this query catches. It keeps
     the nowrap because a chip that wrapped inside a `overflow-x:auto` box would be a rail with two rows
     in it, which is the layout the whole query exists to undo. */
  #cats,#tgts,#oses{display:flex;flex-wrap:nowrap;gap:6px;overflow-x:auto;
    flex:1 1 0;min-width:0;
    scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
  #cats::-webkit-scrollbar,#tgts::-webkit-scrollbar,#oses::-webkit-scrollbar{display:none}
  .bar .wrap,.subbar .wrap{gap:5px}
  .chip{padding:4px 11px}
  /* And a cap on top of the rails, because rails alone still leave four to six control rows. On a tall
     screen the cap sits above the bar's natural height and nothing happens; on a short one the bar
     scrolls inside itself instead of over the page. A fraction rather than a pixel count so that it
     only ever binds where it is needed. `vh` first: a browser that does not understand `dvh` must
     still get a cap rather than none.

     Since JFH-354 the bar holds the search line alone, so what the cap guards is that one row wrapping on
     a short landscape phone rather than the four-to-six it was written for. It is measured at 165px of an
     844px screen, so it does not bind here and is not meant to: a cap that only ever fires where it is
     needed is exactly a cap you cannot see working. */
  .bar{max-height:44vh;max-height:44dvh;overflow-y:auto}

  /* ---- and the sheet, which is what the rails and the cap above are the fallback for -----------------
     The handle, at the 44px WCAG 2.5.5 asks for, sharing the one row the bar is now reduced to with the
     search box. Everything in that row grows to 44 with it: the 30px chips above are what you do when six
     control rows have to fit on a phone, and are not what you do once they no longer have to. */
  html[data-fb] #fbt{display:inline-flex;flex:none;min-height:44px;padding:0 14px}
  html[data-fb] #q{flex:1 1 0;min-width:9em;min-height:44px}
  /* `.bar .chip` until JFH-354, which was every chip that mattered only because `#sheet` was inside the
     bar -- the sheet's own chips, `#strict`, `#reset` and every facet rail, got their 44px by descent. The
     sheet moved out to stop being pinned, and a descendant selector would have dropped the WCAG 2.5.5
     floor on precisely the controls a phone reader taps most, silently and with every assertion still
     green. Unscoped is also the honest rule: the floor is a property of a touch viewport, not of one
     container in it. */
  html[data-fb] .chip,html[data-fb] select{min-height:44px}
  /* No `display` in this rule, deliberately. It outranks `.newchip{display:none}`, so setting one here
     would put the New and Rising chips on screen on every build whose window is empty -- which is the one
     thing those two classes exist to prevent. A <button> centres its own content vertically, so the
     min-height above needs no help. */
  html[data-fb] .chip{padding:0 13px}
  header button{min-height:44px;padding:0 14px}
  .fix{min-height:44px}

  /* Anchored to the bottom edge, not dropped open under its own handle. The handle is in a bar stuck to
     the top of the screen, and the top third of a 375x812 phone is exactly where a thumb held one-handed
     cannot reach -- so expanding it in place would move all 27 chips *away* from the hand that opened
     them. `translateY` off the bottom rather than `display:none` so it slides, and `visibility:hidden`
     beside it because a transform alone leaves the chips focusable, tabbable and in the accessibility
     tree while they are off screen. */
  html[data-fb] #sheet{position:fixed;left:0;right:0;bottom:0;top:auto;z-index:30;
    background:var(--plane);border-top:1px solid var(--grid);border-radius:14px 14px 0 0;
    box-shadow:0 -14px 44px rgba(0,0,0,.45);padding:0 14px 16px;gap:14px;
    max-height:80vh;max-height:80dvh;overflow-y:auto;overscroll-behavior:contain;
    transform:translateY(101%);visibility:hidden;transition:transform .18s ease,visibility .18s}
  /* `visibility` is transitioned on the way out and not on the way in, which is the whole reason the open
     state restates `transition` at all. CSS interpolates visibility as a step that reads `visible` for the
     whole duration -- except at progress exactly 0, where it is still the old value. So a transitioned
     open leaves the sheet computed as hidden for the instant `show()` runs in, a hidden element cannot take
     focus, and the focus call in that function silently did nothing. Measured: `document.activeElement`
     stayed on the handle. Dropping visibility from the list here makes the change immediate; keeping it in
     the shut state above is what lets the panel stay on screen for the 180ms it takes to slide back out,
     instead of vanishing and leaving an empty animation behind. */
  html[data-fb][data-sheet=open] #sheet{transform:none;visibility:visible;
    transition:transform .18s ease}
  /* Focused on open so a keyboard reader lands inside it, which is a programmatic focus and not a click --
     so it gets no ring. `:focus-visible` would already have withheld one; this also covers the engines
     where that is still `:focus`. */
  html[data-fb] #sheet:focus{outline:none}
  /* Tap off the sheet to shut it, which is the gesture a sheet trains, over a dimmed page so the two read
     as one thing. `touch-action:none` so a drag that lands on the backdrop does not scroll the document
     underneath the panel that is covering it. */
  html[data-fb] #fbb{display:block;position:fixed;inset:0;z-index:29;background:rgba(0,0,0,.5);
    opacity:0;visibility:hidden;touch-action:none;transition:opacity .18s,visibility .18s}
  html[data-fb][data-sheet=open] #fbb{opacity:1;visibility:visible}
  /* Sticky inside the sheet, so the count and the way out stay on screen while the reader scrolls past
     thirteen topics. The result count is repeated here for one reason: the bar's own copy is behind the
     sheet while the sheet is open, and tapping chips with no number moving anywhere is the state in which
     a reader cannot tell whether the tap landed. */
  html[data-fb] .shead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;
    position:sticky;top:0;z-index:1;background:var(--plane);
    padding:14px 0 10px;border-bottom:1px solid var(--grid)}
  html[data-fb] .shead .sh{flex:1 1 auto;font-size:15px;font-weight:600}
  html[data-fb] #scount{flex:1 1 100%;color:var(--muted);font-size:12.5px}
  html[data-fb] #scount b{color:var(--ink)}
  html[data-fb] #fbx{flex:none;min-height:44px;padding:0 16px}
  /* A rail is the wrong shape once there is height to spend. The rails above exist because the bar has one
     row per facet and 27 chips to get into it; the sheet has the height of a phone, so the chips wrap, all
     thirteen topics are in view at once, and the label goes above them instead of taking width from them.
     That horizontal scroll-one-chip-at-a-time is the "hard to work with on a phone" half of the ticket. */
  html[data-fb] #sheet .facet{display:block}
  html[data-fb] #sheet .facet>label{display:block;min-width:0;margin:0 0 7px;font-size:11px}
  html[data-fb] #sheet #cats,html[data-fb] #sheet #tgts,html[data-fb] #sheet #oses{
    display:flex;flex-wrap:wrap;gap:8px;overflow:visible;flex:none;min-width:0}
  /* Confirmed only and Clear all, which ride on the Runs-on row. With that row a block rather than a flex
     line they follow the OS chips as ordinary inline content and need the gap put back by hand. */
  html[data-fb] #sheet .facet>.chip{margin-top:8px}
}

@media(max-width:640px){
  /* The narrow half of --pin (JFH-356). It lives up here rather than beside its own comment and its wide
     twin at `html{--pin:...}` because `theme_test.py` asserts this query is emitted exactly twice -- once
     here and once for the card order -- and a third copy for one declaration is a third breakpoint to keep
     in step. The reasoning, the 18-width sweep it comes from and the reason there are two tiers at all are
     all at the --pin declaration; this is only the other number.

     280px, against a 269px worst case: the bar at 320px wide in table view, measured on CI's Chromium.
     Windows reads 217px at the same point -- the wrap depends on the rendered text and so on the fonts
     installed -- and `cards-check.mjs` is what found the difference, by asserting the relationship instead
     of this number. It prints both maxima on every run for that reason. */
  html{--pin:280px}
  /* 20px gutters on all four sections cost 40px, 11% of a 375px screen, and the old query left them.
     The header's vertical padding comes down with them, and `.top`'s gap by 2px, for the reason set out
     above the mascot below: every pixel here is one the first result does not get. */
  header{padding:12px 14px 10px}
  .bar{padding:8px 14px}
  .subbar{padding:0 14px 7px}
  main{padding:0 14px 48px}
  footer{padding:18px 14px}
  h1{font-size:21px}
  h1 span{display:block;font-size:13px}
  .top{gap:8px}
  .headside{width:100%;align-items:center;justify-content:space-between;gap:12px}
  .top nav{text-align:left;line-height:2.1}
  /* Measured at 375x760: the masthead was 335px and the bar 165, so the first result began at y=514 and
     its *name* -- the one thing a reader is looking for -- sat at 740, a single pixel of it above the fold.
     A guest arriving on a phone saw a picture and a star count and had to scroll to learn what either was
     attached to.

     The masthead's height is set by this mascot column and not by the nav beside it: 86px of art plus the
     two stacked tap targets under it (the 44px floor every header button gets above -- WCAG 2.5.5, and not
     something to give back) comes to 167, where the nav is 126. So trimming the nav saves nothing at all
     until the column is under 126, and the column cannot get there while both its buttons keep a real
     target. Shrinking the art is the only lever on it that costs nothing: 64px takes the column to 149.

     `.atlas-byte-wrap` keeps its 82px rather than shrinking with the art, because the name tag is sized by
     the wrap and at 64 it wrapped to "Atlas / Byte". Holding the wrap also holds the nav's width, so
     nothing in the nav reflows -- it stays the same three lines it was.

     Rejected: laying the two buttons side by side instead of stacked. It takes 38px off the column rather
     than 18, but the wider column squeezes the nav to 185px, which costs the nav a fourth line and splits
     "All projects" across the break. A net 35px for a worse-looking masthead, against 26px for one that
     looks the same. The rest of the 82px comes out of the card, below the cards block. */
  .atlas-byte-wrap{width:82px}
  .atlas-byte{width:64px;margin-left:auto;margin-right:auto}
  /* ONE WORD HERE, BECAUSE TWO DID NOT FIT IN ANY FONT BUT THIS MACHINE'S. The rule above narrows the mascot's
     column from 128px to 82px and said nothing about the name, so the pill kept its 10px text in a column 46px
     narrower and wrapped to three lines at 640, 600, 500, 414, 375, 360, 320 and 280, against two from 641 up.
     The masthead grew for it at exactly the widths with the least room to spare, and it grew silently because
     the harness compared the pill's text and never its line count.
     9px was the first fix and it was not a fix, it was this machine's font passing a test. `header button`
     gives every button in the masthead the 44px WCAG 2.5.5 floor, so the pill's BOX IS 82x44 whatever the text
     does -- two lines of 9px type is 32px inside a 44px box, and one word is also 44. Quoting 82x44 as the
     evidence for two lines was therefore quoting a number that cannot see a line, which is the same mistake as
     comparing the text: CI reports 82x44 and three lines together. What a third line does is overflow the tap
     target rather than grow it -- 3 x 12.15 + 8 = 44.45 against a 42px content box -- so the text crosses its
     own rounded border. The real margin was 2.41px of 62px, 4%, on "Archie 'Atlas'" in Segoe UI; forced
     monospace, Verdana and Tahoma each take three lines here.
     One word cannot wrap to three lines in any face, so the fix is not font-dependent instead of being retuned
     against one runner. Widest measured "Archie" is 54px (Verdana) in a 62px box, against 82px needed for
     "Archie 'Atlas'" in monospace. The full name stays on `aria-label`, and stays visible from 641 up.
     Rejected: 8px type, which costs legibility and still leaves a two-line arrangement one face away from
     breaking; a 112px wrap and a 108px overhanging pill, both of which un-narrow the column this breakpoint
     exists to narrow; raising the 44px floor to fit three lines, which spends masthead height on a phone to
     show a middle name -- JFH-289 fought for 18px of that height.
     A NOTE ON HOW THE FACES ABOVE WERE PICKED, because it is a trap: you cannot probe a font you do not have.
     Forcing "DejaVu Sans", "Liberation Sans" and a deliberately misspelled family name all measured the same
     105.38px here, because all three fell back to the same default, and `document.fonts.check()` returns true
     for the misspelled one too. Identical metrics across unrelated families is the tell. Only monospace,
     Verdana and Tahoma are real instruments on a Windows machine, and monospace is the upper bound of the
     three, so it is the one a fix has to survive.
     JFH-289's art shrink does not interact with this: the pill is sized by the wrap, which that ticket
     held at 82px precisely so nothing around it reflowed, so the column measured here did not move. */
  .atlas-name{font-size:9px}
  .atlas-name-full{display:none}
  .atlas-name-short{display:inline}
  /* No bubble at all at this width or below, because there is nowhere for it to go. `.headside` is full-width
     here and puts the nav immediately left of the mascot column, so the band the bubble uses on a desktop is the
     navigation, and anything hanging underneath is the search field -- both measured. This is also the width
     at which a reader most likely has no pointer to hover with, and the commentary is a hover affordance:
     the fact is already in the card being touched. The name, the tip button and Quiet mode all stay.
     The column is the wrap's 82px and not the art's 64: JFH-289 shrank the art inside a wrap it deliberately
     held, so the width the nav is measured against did not move when the picture did. */
  #byte-speech{display:none}

  #q{flex:1 1 100%;min-width:0}
  .line>label[for=q]{display:none}
  .count{margin-left:0;font-size:12px}
  /* Runs-on is the one facet that also carries Confirmed only and Clear all, and at 390px those two
     left its rail about 110px -- one OS chip at a time. That line alone wraps, so the rail keeps most
     of the row and the two buttons drop underneath it. Narrow-only: in landscape there is width enough
     for all four to share the row, and wrapping there would cost a row the bar cannot spare.
     The wrap is still needed with marks on those chips and the floor is still the right number, though
     both now hold for a different reason. The five marks measure ~224px where the five words measured
     ~330px, so 62% of 390px is no longer "most of one chip" -- it is the whole rail, and nothing scrolls.
     What did not change is the line: label plus rail plus those two buttons is ~470px however narrow the
     chips get, so a single row would still overflow. Not lowered, because there is no width to reclaim
     -- with the line wrapped the rail's own `flex:1 1 auto` already takes what is left of it. */
  .facet:has(>.chip){flex-wrap:wrap}
  .facet:has(>.chip)>#oses{flex:1 1 auto;min-width:62%}

  /* A row stops being a row. Four columns cannot share 335px -- the blurb on its own wants more than
     that -- so each row becomes a card, and the headings, no longer above anything, go away. */
  thead{display:none}
  table,tbody,tr,td{display:block}
  table{margin-top:12px}
  tr{display:grid;grid-template-columns:1fr auto;gap:1px 12px;align-items:start;
    border:1px solid var(--grid);border-radius:10px;padding:11px 13px;margin:0 0 9px}
  td{border-bottom:0;padding:0}
  td.rk{grid-column:1;grid-row:1;text-align:left}
  td.st-c{grid-column:2;grid-row:1}
  td.pj{grid-column:1/-1;grid-row:2}
  td.ds{grid-column:1/-1;grid-row:3;margin-top:6px}
  /* The two `.hide` columns are dropped at 900px and, until now, never came back -- so a phone reader
     silently lost the topic and target tags and the language, licence and push date. That was a width
     decision inherited from the table, and a card is not competing for column width: it has a whole row
     to spend. `td.hide` outranks the `.hide` that hid them, so this wins without touching that rule and
     without affecting the 641-900px range, where the layout really is still a table.
     A higher specificity than `.hide`, not a later position, is what makes that true. */
  td.hide{display:block}
  td.tg{grid-column:1/-1;grid-row:4;margin-top:8px}
  td.lc{grid-column:1/-1;grid-row:5;margin-top:2px;text-align:left}
  /* Three stacked lines is right in a centred 90px column and wrong on a card, where the same three
     facts fit on one line. The <br>s are the table's formatting, so they go away here rather than
     being conditionally emitted -- the markup stays one shape and the layout decides how to read it. */
  td.lc .meta{display:flex;flex-wrap:wrap;gap:4px 12px}
  td.lc .meta br{display:none}
  .st{font-size:15px}
  .desc{font-size:13px}
  .more{width:100%}
  .cmdrow{max-width:none}
}

/* ---- Cards view --------------------------------------------------------------------------------------
   The same table, read as a gallery. `render()` emits one <table> and nothing else; this block decides how
   it is laid out, which is exactly the trick the 640px query above plays and it is here for the same
   reason. Two things fall out of one markup shape. The toggle costs nothing -- no refetch, no re-render,
   not one row rebuilt, so switching is a repaint whether 120 rows are on screen or 1,294. And the two
   views cannot disagree about what a row says, because there is only one row.

   Every selector is prefixed `html[data-view=cards]`, which outranks the two rules it has to beat --
   `.shot,.hide{display:none}` at 900px, and the whole card block directly above -- on specificity rather
   than on source order. So this works at every width without !important and without either of those
   moving, which matters because both of them are load-bearing in the view this one is not.

   What it costs: a <table> whose cells are `display:block` stops being a table to a screen reader, the
   implicit role going with the display type. The 640px block already accepts that, and both get away with
   it for the same reason -- with the headings gone every cell still names itself, the star count carrying
   "N lists" and the topic and targets being pills. It is a real trade, and it is why the table stays the
   default rather than this. */
html[data-view=cards] thead{display:none}
html[data-view=cards] table{display:block;margin-top:14px}
/* `auto-fill` against a floor rather than a column count, so one rule is four cards on a desktop, two on a
   tablet and one on a phone with nothing to switch between and no second breakpoint to keep in step. The
   floor is what the widest thing a card must hold needs before it would scroll sideways: the install line,
   which is monospace, plus the two 13px gutters. */
html[data-view=cards] tbody{display:grid;gap:14px;
  grid-template-columns:repeat(auto-fill,minmax(290px,1fr))}
/* A grid inside the grid, two columns wide, for one reason: the rank and the star count share a line and
   everything else spans both. Placed by an explicit `grid-row` per cell, like the 640px block, because the
   cells arrive in the table's order, a card wants them in another one, and `order` -- which is the cheaper
   tool -- cannot put two of them side by side. `margin:0` is not tidiness: the block above gives every row
   a 9px bottom margin, which this view has a 14px grid gap for, and margins do not collapse in a grid. */
html[data-view=cards] tr{display:grid;grid-template-columns:1fr auto;align-items:start;align-content:start;
  gap:0 10px;margin:0;padding:0 0 12px;background:var(--band);
  border:1px solid color-mix(in srgb,var(--card-accent) 35%,var(--grid));border-radius:12px;overflow:hidden;
  transition:border-color .14s ease,box-shadow .14s ease,transform .14s ease}
html[data-view=cards] td{display:block;border-bottom:0;padding:0 13px;min-width:0}
/* The screenshot is the whole argument for this view, so it comes back at the widths where the table drops
   it as not paying for its column, and it goes edge to edge. That is what the gutters being on the cells
   rather than on the card buys: this one cell opts out of them by zeroing its own padding. `aspect-ratio`
   is inherited from `.shot img` above, so a card reserves the image's height before it loads and a lazy
   one does not shove the rest of the grid down when it arrives. */
html[data-view=cards] td.shot{grid-column:1/-1;grid-row:1;width:auto;padding:0}
html[data-view=cards] td.shot img{width:100%;border:0;border-radius:0;
  border-bottom:1px solid var(--grid)}
html[data-view=cards] td.rk{grid-column:1;grid-row:2;padding-top:10px;text-align:left}
/* The "#" is the stylesheet's business here because in the table it is the column heading's, and this view
   has no headings -- a bare "37" at the top of a card is a number with nothing attached to it. */
html[data-view=cards] td.rk::before{content:"#"}
html[data-view=cards] td.st-c{grid-column:2;grid-row:2;padding-top:10px;text-align:right}
html[data-view=cards] td.pj{grid-column:1/-1;grid-row:3;margin-top:4px}
html[data-view=cards] td.ds{grid-column:1/-1;grid-row:4;margin-top:7px}
/* Both `.hide` columns come back, for the reason the 640px block gives: they were dropped at 900px because
   they stopped paying for their column *width*, and a card is not competing for column width. */
html[data-view=cards] td.hide{display:block}
html[data-view=cards] td.tg{grid-column:1/-1;grid-row:5;margin-top:9px}
html[data-view=cards] td.lc{grid-column:1/-1;grid-row:6;margin-top:3px;text-align:left}
html[data-view=cards] td.lc .meta{display:flex;flex-wrap:wrap;gap:4px 12px}
html[data-view=cards] td.lc .meta br{display:none}
html[data-view=cards] .project-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
html[data-view=cards] .project-actions a{border:1px solid color-mix(in srgb,var(--card-accent) 55%,var(--grid));
  border-radius:999px;padding:4px 9px;color:var(--ink2);font-size:12px;font-weight:600}
html[data-view=cards] .project-actions a:first-child{background:color-mix(in srgb,var(--card-accent) 18%,var(--band));color:var(--ink)}
html[data-view=cards] .project-actions a:hover{border-color:var(--card-accent);text-decoration:none}
/* Close the banner slot when the screenshot kill switch omits the cell. */
html[data-view=cards][data-index-screenshots=off] td.rk{grid-row:1;padding-top:10px}
html[data-view=cards][data-index-screenshots=off] td.st-c{grid-row:1;padding-top:10px}
html[data-view=cards][data-index-screenshots=off] td.pj{grid-row:2}
html[data-view=cards][data-index-screenshots=off] td.ds{grid-row:3}
html[data-view=cards][data-index-screenshots=off] td.tg{grid-row:4}
html[data-view=cards][data-index-screenshots=off] td.lc{grid-row:5}

/* The other half of the above-the-fold budget the mascot rules opened, and the larger half. A card puts
   226px above its own name on a phone: 165 of screenshot, then the rank and star band under it, which
   `td.rk` and `td.st-c` share at 56. With the masthead trimmed the first card starts at 488, so the name
   still landed at 714-802 and was still cut. Moving it up one row lands it at 658-746, and with it the
   repo link, Save, and all five platform verdicts -- 14px of slack, on a card whose `td.pj` measured
   exactly 88px on all 60 rows in the first page, so there is no content variance to eat it.

   The order is a number here rather than a shape in the markup, which is what makes this a three-line
   change: the screenshots-off rules directly above renumber the same grid for the same reason.

   It costs nothing anywhere else. `td.rk` and `td.st-c` hold no focusable content -- checked, they are
   plain text -- so the only cells that can take focus are still in the order the DOM has them, and the
   card now reads name, then credentials, rather than credentials, then name.

   Screenshots-off is deliberately left alone: those selectors carry two attributes and outrank these, so a
   reader who turned the images off keeps the order that was designed for not having them.

   This block has to sit *below* the cards rules and not in the 640px query up beside the masthead ones,
   because it repeats their selectors exactly and would otherwise lose to them on source order. Same
   specificity, later wins.

   What this does not fix: on a viewport 700px or shorter -- 375x667, 360x640 -- the name is still below the
   fold, by 75 and 94px. Masthead 309 plus bar 165 plus 165 of screenshot is already past 640, so nothing
   short of the screenshot itself or the bar's three rows of 44px targets reaches it, and both of those are
   worth more than the pixels. */
@media(max-width:640px){
  html[data-view=cards] td.pj{grid-row:2}
  html[data-view=cards] td.rk{grid-row:3}
  html[data-view=cards] td.st-c{grid-row:3}
}
/* 44em is a measure for a line of prose in a wide table cell. Inside a 290px card it is not a constraint
   at all, and leaving it there only means the three of them disagree about what the card's width is. */
html[data-view=cards] .desc,html[data-view=cards] .cmdrow,html[data-view=cards] .cmd{max-width:none}
/* Four lines, and this is the one place the cards view shows less than the table rather than differently.
   Cards in a row stretch to the tallest of them, and these blurbs are other people's one-line table cells:
   they run from six words to sixty, so one project with a paragraph set the height of the three beside it
   and left them two thirds empty. Unclamped, the grid stopped being scannable, which is the only thing this
   view is for. The full text is one click away on the project's own page, and it is right here in the table
   -- which is the default, and is where a reader who wants to read rather than browse already is.
   `-webkit-line-clamp` is the prefixed property every engine including Firefox implements; unprefixed
   `line-clamp` is newer, so both are set and the browser takes whichever it knows. */
html[data-view=cards] .desc{display:-webkit-box;-webkit-box-orient:vertical;
  -webkit-line-clamp:4;line-clamp:4;overflow:hidden}
/* The cards half of the new-arrivals outline -- see the long note beside the table rules for why the two
   views cannot share one. Here a row *is* a box, so this is the straightforward version: a `--warn` ring
   that breathes. It sits above the hover and focus rules so that those two, which are the same specificity,
   win on source order: the pointer and the keyboard both need to be able to say "this one, now" over the
   top of a standing property of the row. The pulse itself outlives them either way, because an animated
   property beats the cascade. */
html[data-view=cards] tr.nw{border-color:var(--warn);
  box-shadow:0 0 0 2px var(--warn),0 0 12px color-mix(in srgb,var(--warn) 30%,transparent);
  animation:new-breathe 3s ease-in-out 5}
@keyframes new-breathe{
  0%,100%{box-shadow:0 0 0 2px var(--warn),0 0 10px color-mix(in srgb,var(--warn) 24%,transparent)}
  50%{box-shadow:0 0 0 3px var(--warn),0 0 26px color-mix(in srgb,var(--warn) 58%,transparent)}}
/* The table tints the row the pointer is over; a card is a box, so it takes the accent on its edge. The
   cell rule has to be undone explicitly or the tint lands as six full-width strips inside the card with
   the gaps between them showing through. Inside `hover:hover` like the rule it overrides, so a touch
   device -- which latches a hover it can never clear -- is not made to carry either of them. */
@media(hover:hover){
  html[data-view=cards] tr:hover td{background:transparent}
  html[data-view=cards] tr:hover{border-color:var(--card-accent);
    box-shadow:0 0 0 2px var(--card-accent),0 0 20px color-mix(in srgb,var(--card-accent) 44%,transparent),0 14px 32px rgba(0,0,0,.24);
    transform:translateY(-1px);animation:card-glow 1.5s ease-in-out infinite alternate}
}
html[data-view=cards] tr:focus-within{border-color:var(--card-accent);
  box-shadow:0 0 0 2px var(--card-accent),0 0 20px color-mix(in srgb,var(--card-accent) 40%,transparent)}
@keyframes card-glow{from{box-shadow:0 0 0 2px var(--card-accent),0 0 12px color-mix(in srgb,var(--card-accent) 30%,transparent),0 12px 28px rgba(0,0,0,.2)}to{box-shadow:0 0 0 2px var(--card-accent),0 0 28px color-mix(in srgb,var(--card-accent) 58%,transparent),0 16px 36px rgba(0,0,0,.28)}}
/* A pulse is a way of saying "look at this one", and it can only say that about a few. When an import brings
   most of the atlas at once -- which is not hypothetical: the run that first read twenty-eight source lists
   marked roughly 85% of the rows -- every visible row pulsing says nothing except that the page is busy.
   `render()` sets `data-wave` when the cohort is the majority of the filtered set, and the motion stops
   while the outline, the chip and the count stay exactly as they were. The reader loses the nudge, which
   was worthless at that size, and keeps every way of actually finding the new rows.
   Placed after the cards rule it overrides, which is the same specificity; the table rule it overrides is
   lower, so order does not matter there. */
html[data-wave="1"] tbody tr.nw td,html[data-wave="1"] tr.nw{animation:none}

/* The chip hovers transition, the chip rails scroll smoothly, and new arrivals breathe, and all three are
   motion a reader can have asked their operating system not to show them. A blanket rule stays safe because
   no state on this page is communicated *by* an animation: the new-arrivals pulse is a swell on an outline
   that is already there in the base rule, so stopping it leaves the same `--warn` ring, the same chip and
   the same count. That is a constraint on anything added here, not just a description -- an animation that
   is the only way to see something would be invisible to the readers this rule is for. */
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;
    transition-duration:.01ms !important;scroll-behavior:auto !important}
}

/* Focus lands on a row after "Show more", so the row needs somewhere to put a ring and needs to clear
   the sticky filter bar if anything ever does scroll it into view.

   160px was never enough to do that and could not have been: until JFH-354 the pinned band was the masthead
   plus the whole bar, measured at 456px at 1440x900 and 731px at 768x900, so a row scrolled into view landed
   underneath it whatever this number said. With the bar alone pinned the band is 64 / 91 / 106 / 165px at
   1440x900, 1024x800, 768x900 and 390x844 -- which is where 172px came from, and 172px is WRONG. The
   surplus at a wide width costs nothing (`scroll-margin` only decides where a scroll stops); the shortfall
   at a narrow one costs the whole rule.

   THOSE FOUR NUMBERS WERE A SAMPLE OF ONE VIEW AT FOUR ROUND WIDTHS. The bar is a wrapping flex line, so
   its height is a step function of the width AND of the text in it -- and `#view` and `#take` relabel
   between the two views ("Table view" / "Cards view"), which moves the wrap points. Swept 18 widths from
   320 to 1920 in both views, measured while genuinely stuck (scrolled to 3000; unscrolled the bar is in
   flow under the masthead and reads short):

     cards   320:191  360-414:165  480-640:113  641-700:103  768-900:106  1024:91  1200+:64
     table   320:217  360-414:191  480-540:139  600-640:113  641-768:108  820-1024:106  1200:91  1280+:64

   THOSE HEIGHTS ARE THIS MACHINE'S. The wrap point is a function of the rendered text, so it is a function
   of the fonts installed: CI's Chromium wraps one line further at 320px in table view and reads 269px where
   Windows reads 217px. The tiers below clear the taller of the two, and `cards-check.mjs` prints the maximum
   it measured on both sides of the fold on every run, so the next person choosing a number does not have to
   trust this paragraph's machine.

   So the worst case is 269px at 320px wide in table view, and 172px was already short by 19px at 320px in
   the DEFAULT view before this ticket touched anything. Two tiers, split at the 640px breakpoint the layout
   already turns on, each above the worst case on its side with air: 116px against a 108px maximum above the
   break, 280px against 269px below it.

   A TOKEN AND NOT A LITERAL, BECAUSE THE RULE BELOW NEEDS THE SAME NUMBER (JFH-356). A second copy is a
   second thing to remember when the bar's contents change, and the measurements that justify it are here
   and nowhere else. `cards-check.mjs` asserts the relationship rather than the number -- that `--pin` is at
   least the bar's measured height at every width and view it probes -- so adding a control to the search
   line reddens the suite instead of silently re-breaking this.

   BOTH TIERS ARE INSIDE A QUERY, AND THAT IS DELIBERATE. The narrow one has to live in the
   `@media(max-width:640px)` block ~275 lines above, because `theme_test.py` asserts that query is emitted
   exactly twice and a third copy for one declaration is a third breakpoint to keep in step. A bare
   `html{--pin:116px}` down here then beats it on nothing but source order -- same selector, same
   specificity, later wins -- and the phone silently got the desktop number. Measured: `scroll-margin-top`
   read 116px at 390x844 and 320x844 with the narrow rule sitting right there in the stylesheet. Two
   non-overlapping queries cannot do that to each other whichever order they appear in. */
@media(min-width:641px){html{--pin:116px}}
#out tr:focus{outline:2px solid var(--bar);outline-offset:-2px}
/* The fallback is for a UA that supports custom properties but not these queries: an unset `--pin` makes the
   declaration invalid at computed-value time, which is 0, which is the bug. 280px is the safe side. */
#out tr{scroll-margin-top:var(--pin,280px)}

/* THE RULE ABOVE PROTECTS THE ONE ELEMENT A GUEST CANNOT TAB TO (JFH-356).

   A `tr` carries no `tabindex` in the markup, so it is not focusable and cannot be a tab stop. The one
   place anything focuses a row is the "Show more" handler, which does `t.tabIndex = -1` and then
   `t.focus({preventScroll: true})` -- programmatically focusable, still never a tab stop, and `preventScroll`
   means the margin below is not consulted even on that path. The rule binds nothing in either direction.
   (Not "rows carry tabindex=-1", which is what this comment said first and is wrong: the two `tabindex="-1"`
   attributes in the built page are on `#sheet` and the screenshot cell's link.)

   A 60-stop forward tab walk at each of the four widths above hits `.skip`,
   the masthead nav, `#q`, `#sort`, `#view`, `#take`, `#mapbtn`, 33 facet chips, `#strict`, `#reset`, the
   `summary`, and `a.nm` / `a.nwo` / `.save` / `.pin` / `.copy` inside the rows -- and zero `tr`. Every one
   of those reported `scroll-margin-top: 0px`.

   That is only survivable while the page scrolls the way tests scroll it. Moving focus *forward* down a
   document aligns the new element to the BOTTOM edge of the viewport, and nothing is pinned there, so the
   forward walk finds nothing at any width. Shift+Tab scrolls upward and aligns to the TOP edge, which is
   exactly where the bar is. Measured on 645b549 with dispatched Shift+Tab keys: of 30 reverse stops, 20 at
   1024x800, 14 at 768x900 and 4 at 390x844 landed under the bar, 31 of those 38 entirely -- 100% covered,
   with `document.elementFromPoint` at the focused control's own centre returning a child of `.bar`. The
   focus ring was behind opaque chrome and a pointer could not reach the control either. With this rule the
   same walk reports 0 at all four widths.

   `#out` itself is in the list because it is the skip link's target (`<a class="skip" href="#out">`), and a
   fragment jump is a scroll like any other: without a margin it put the table at `top:0` and the bar sat on
   the first 4 / 3 / 2 / 1 data rows. The skip link's *focus* behaviour was already correct -- the next Tab
   lands on the first row's name link -- so this is the landing position only.

   NOT the controls inside `.bar`. The bar is pinned, so its contents are always visible and have nothing to
   clear; giving `#q` a scroll margin would make focusing the search box jump a scrolled page to the top.
   That exclusion is the reason this is a list of two ancestors rather than a bare `a,button,select,summary`,
   and it is what the negative assertion in probe.mjs pins. */
#out,
main a[href],main button,main select,main summary,
.subbar a[href],.subbar button,.subbar select,.subbar summary{scroll-margin-top:var(--pin,280px)}

/* ---- The comparison panel ----------------------------------------------------------------------------
   Above the results, in the slot `.shared` uses, and for the same reason: it is not a filter the reader chose
   and not a fact about any row, it is what they have asked this page to answer. `display:none` until something
   is pinned, by a class and not `[hidden]`, because the author `display:block` here would outrank the
   user-agent sheet's rule -- the note above `.shared` spells that out.

   WHY THIS IS HERE AND NOT UP BESIDE `.shared`, WHICH IS WHERE IT BELONGS, and why every selector below
   is an id rather than the class every other component on this page is styled by.

   This panel holds the page's second <table>. The sentence at the top of the cards block above -- "`render()`
   emits one <table> and nothing else" -- was true when it was written, and the two view blocks were written
   against it: the 640px card query selects bare `thead`, `table`, `tbody`, `tr` and `td`, and the cards block
   selects them under `html[data-view=cards]`, which is the *default* view. Both reach in here. Measured at
   375px with four projects pinned, before this block existed: the thead had zero height, the cells were laid
   out by `grid-template-columns:1fr auto` in alternating 249/71px pairs, `min-width:0` had collapsed every
   column, and the horizontal scroller had nothing left to scroll -- the panel's whole phone story.

   An id, so the fix does not depend on where it sits. The strongest thing either block reaches for is
   `html[data-view=cards] tr:hover td`; one id outranks all of it, so nothing here can be undone by a rule
   added up there later, and the panel does not need re-verifying every time the cards view is touched.

   The fix this really wants is scoping those two blocks to `#out`, since the results table is what they were
   always about -- `#out tr:focus` directly above is that pattern already. Not done here: it is thirty-odd
   selectors on the layout every reader sees, and `tests.yml` serves the *committed* docs/, so
   `cards-check.mjs` would measure the old stylesheet and pass whatever the change did to the new one. JFH-291
   holds it, to land on its own with a build behind it. The narrow fix is the one that can be verified first.

   `overflow-x:auto` on an inner box rather than on the panel, so the header and its buttons stay put while
   the columns are swiped, and so the rounded corners are not cut off by the scroller.

   The row labels are `position:sticky;left:0`, which is the whole of what makes four columns usable on a
   375px phone: the reader swipes the projects past a column of names that stays where it is. A sticky cell
   needs an opaque background or the cells sliding under it show through, and it needs `min-width` or the
   longest label ("Plugs into") decides the width of the column the reader is trying to see. */
#cmp{display:none}
#cmp.on{display:block;margin:14px 0 0;border:1px solid var(--grid);border-radius:8px;background:var(--band)}
#cmp .ch{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:9px 14px;
  border-bottom:1px solid var(--grid);color:var(--ink2);font-size:13px}
#cmp .ch b{color:var(--ink)}
#cmp .ch .sp{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
#cmp .scroll{overflow-x:auto;border-radius:0 0 8px 8px}
/* The display types are restated, not inherited: this is what the two view blocks above took away. Written
   out in full rather than as `display:revert`, which reverts to the *user-agent* sheet and would be correct
   here by luck -- these are the UA values -- but says nothing about why they are being set. */
#cmp table{display:table;border-collapse:collapse;width:100%;margin-top:0;font-size:13px}
#cmp thead{display:table-header-group}
#cmp tbody{display:table-row-group}
/* `border` and `background` because the 640px query gives every row a card's outline and the cards block
   gives it a fill; both paint on a `table-row` and neither belongs on a matrix. */
#cmp tr{display:table-row;border:0;background:transparent}
#cmp th,#cmp td{display:table-cell;padding:7px 12px;text-align:left;vertical-align:top;
  border-top:1px solid var(--grid)}
#cmp thead th{border-top:0;vertical-align:bottom;color:var(--ink)}
#cmp thead th a{font-weight:600}
/* `display:block` because `.meta` carries a `margin-top`, which a span ignores -- the row builder only ever
   uses that class on a <div>, and this is the first place it lands on an inline element. */
#cmp thead th .meta{display:block;margin-top:2px;font-weight:400}
#cmp tbody th{position:sticky;left:0;background:var(--band);color:var(--ink2);font-weight:600;
  white-space:nowrap;min-width:104px}
/* 148px is the floor that makes the scroller a scroller. Four columns of it plus the 104px label rail is
   696px, so on a 375px phone there is real width to swipe through rather than four columns squeezed to fit
   and nothing legible in any of them. The cards block sets `min-width:0` on every cell, which is right for a
   card that must not push its grid track wider and is exactly wrong here. */
#cmp td{color:var(--ink);min-width:148px}
/* Table view stripes alternate rows and tints the row under the pointer; the cards view puts a glow on the
   row that holds focus. All three are about a list of projects being scanned. This is a matrix being read,
   and a comparison whose cells change colour as the mouse crosses them is harder to read, not easier. */
#cmp tbody td{background:transparent}
#cmp tr:hover,#cmp tr:focus-within{box-shadow:none;transform:none;animation:none;border:0}
#cmp .unpin{margin:5px 0 0;display:block}
/* The marked rows are the only reason to build this panel: four projects agree about most things, and the
   handful they disagree about is the decision. Two channels, never one -- a 3px bar on the label cell and a
   `≠` beside the label, because a difference carried by colour alone is invisible to the readers most likely
   to be comparing four things at once rather than remembering them (WCAG 1.4.1). `--warn` is the same
   colour the shared-list strip uses and means the same thing here: look at this before you decide.

   Deliberately *not* a green on the rows that agree. "These four all run on Linux" is not a finding and does
   not want a colour; drawing one would put twelve marks on screen to say nothing. */
#cmp tr.differs th{border-left:3px solid var(--warn);padding-left:9px}
#cmp .dx{color:var(--warn);font-weight:400;margin-left:4px}

/* ---- Paper -------------------------------------------------------------------------------------------
   "Save as PDF" is a print dialog in every browser there is, so the PDF export and the print sheet are one
   feature and this block is both of them. What a sheet of it holds: the masthead, the sentence saying what
   the table is of, the address it came from, and the table. What it does not hold is anything a reader could
   have pressed -- the filter bar, 120 Save buttons, the palette, the theme toggle, the two dialogs -- because
   a control on paper is ink spent on a promise the medium cannot keep.

   The colour half of this is deliberately not here. It is `printOn()`, which puts the document in the light
   theme for the duration of the print, and the reason is that a stylesheet cannot do it without a second copy
   of the thirteen palette tokens -- and `tests/theme_test.py` exists because copies of this palette drift.
   That matters more than it sounds: browsers print backgrounds off by default, so a dark-theme page prints
   near-white text onto white paper and hands the reader a blank sheet.

   `@page` rather than a margin on <body>, so the margin belongs to the sheet and repeats on every one of
   them rather than being applied once to a very long box. */
@page{margin:14mm}
@media print{
  /* `.skip` included: a skip link is a keyboard affordance, and it is the first thing on the page.
     `.subbar` included since JFH-354, and it is the one entry here that is not a new decision: the three
     facet rails were inside `.bar` and went with it, so taking them out of the pinned band would have put
     them on paper without a line of this rule changing. A hide-list scoped by containment stops being a
     hide-list the moment the containment moves. */
  .bar,.subbar,.more,dialog,#fbb,#live,.skip,header nav,.stamp,.atlas-byte-wrap,.facets,.save,.copy,.shot,
  .shared .sp,.pin,#cmp .ch .sp,#cmp .unpin{display:none}
  /* The comparison itself stays, and this is the one thing on the sheet that is more use on paper than on
     screen: four projects in columns is what somebody carries into the meeting where the choice is made.
     Only its controls go -- an Unpin button under a printed column heading is a button nobody can press.

     The rest of this is what makes it fit, and it is all one observation: paper has no horizontal scroll, so
     every affordance built for swiping is not useless here, it is destructive. A sheet of A4 less the 14mm
     margins is 182mm, about 673 CSS px. Measured at that width with four projects pinned and only
     `overflow-x` released: the table asked for 971px and its last column ended 992px from the left -- 319px
     past the edge of the sheet, with nothing to clip it and nothing to say so. `overflow-x:hidden` would not
     have rescued those columns either; it would have cut them at 631px instead.

     Releasing the 148px cell floor is necessary and, measured, not sufficient -- with `min-width:0` the table
     still wanted 971px, because an auto layout sizes columns to their content and a project column holds a
     name, a topic, a licence and possibly an install line. `table-layout:fixed` is what actually bounds it,
     which is the same tool and the same reason as the results table below. Percentages rather than pixels so
     that pinning two projects gives each of them half the sheet instead of a quarter of it and three columns
     of white space, and `overflow-wrap` because a fixed column that a monospace install command does not fit
     spills out of the cell rather than wrapping inside it. The sticky rail is unstuck last, for the first
     reason again: there is nothing left for it to stay in front of. */
  #cmp .scroll{overflow-x:visible}
  #cmp table{table-layout:fixed}
  #cmp thead th:first-child{width:13%}
  #cmp td{min-width:0;overflow-wrap:anywhere}
  #cmp tbody th{position:static}
  /* Where the sheet came from, which the screen keeps in the address bar and paper has nowhere to put.
     Written by `printOn()`; `#printurl{display:none}` above keeps it off the screen. */
  #printurl{display:block;color:var(--muted);font-size:8.5pt;word-break:break-all;margin:6px 0 0}
  /* The stripes are the browser's to drop and it drops them, but a reader who has turned "Background
     graphics" on should still get a table rather than a barcode. Both selectors restated at the specificity
     of the rules they undo, later in the file -- so this wins on source order and there is still no
     `!important` anywhere on this page outside the reduced-motion block. */
  html[data-view=table] tbody tr:nth-child(odd) td,
  html[data-view=table] tbody tr:nth-child(even) td{background:transparent}
  /* Both `.hide` columns come back. They were dropped at 900px because they stopped paying for their width
     and a sheet of A4 measures about 794 CSS pixels -- but paper has no filter bar above the table and no
     second screenful below it, so the width they cost is width there is. The screenshot column stays gone:
     it is the one thing on this page a printer bills for by the millilitre. */
  td.hide,th.hide{display:table-cell}
  td,th{padding:5px 6px;font-size:11px}
  /* The one number on the sheet still set in screen type. `.st` carries its own 16px, so the 11px above
     never reaches it, and at 16px bold a seven-digit count is wider than the 9% column below: 281,176
     printed as "281,17" with the 6 on the next line. Twelve keeps it emphasised against 11px body text
     and fits the column with room left over. */
  .st{font-size:12px}
  .st.none{font-size:11px}
  /* Fixed, with the six columns proportioned for the sheet rather than inherited from the screen. This is
     the difference between a document and a curiosity, and it was measured: the auto layout gave a 794px
     sheet the proportions of a 900px browser window, which put the description into a 130px column and made
     one row 500px tall -- 278 projects over ninety pages, at two and a bit rows a sheet. The description is
     most of what a printed row is *for*, so it gets the widest column and the rest are cut to what their
     content actually needs. */
  #out table{table-layout:fixed}
  th.n:first-child{width:4%}
  th.pj{width:20%}
  th.st-c{width:9%}
  th.tg{width:20%}
  th.ds{width:36%}
  th.lc{width:11%}
  /* Anything that will not wrap is broken rather than allowed to widen its column past the width above --
     a repository slug, a licence, an install line with a URL in it. */
  td{overflow-wrap:break-word}
  /* The chips become the text they always were. Eight pills at 20% of the width stack eight lines deep and
     the borders are the only thing making them pills; as a comma-separated list the same eight fit two. The
     topic keeps its weight, because it is the one classification here that is ours rather than the
     project's, and flattening the pills is what took away the colour that used to say so. */
  td.tg .tag{display:inline;border:0;border-radius:0;background:none;padding:0;
    color:var(--ink2);font-size:10px}
  /* The separator trails the word it follows rather than leading the word it precedes. Same characters
     either way on one line, but the only break opportunity in ", " is the space inside it -- so as a
     `::before` on the next chip the line broke ahead of the comma and every wrapped line in a narrow
     column started with one: "Agent Skills" then ", Claude Code , MCP".
     `white-space:normal` on the pseudo-element only, and it is load-bearing: `.tag` is `nowrap` so a
     pill never splits mid-name, generated content inherits that, and a nowrap space is not a break
     opportunity -- with the comma moved to `::after` and nothing else changed the whole cell became one
     unbreakable line that ran through the description column and gave the table a scrollbar. Normal here
     makes the one space between two names breakable while the names themselves stay whole. */
  td.tg .tag:not(:last-child)::after{content:", ";white-space:normal}
  td.tg .tag.cat{color:var(--ink);font-weight:600}
  /* Kept, unlike the button beside it, which is already hidden with the rest of the controls. A command
     cannot be copied off paper but it can be read off it, and it is four words. */
  .cmdrow{margin:4px 0 0}
  code.cmd{display:block;border:0;background:none;padding:0;color:var(--ink2);font-size:9.5px}
  /* A row broken across a page break is a row you read twice, and a heading that appears once is a heading
     that is on the wrong sheet from page two onward. Both are one line each and both are what makes this a
     document rather than a screenshot of a document. */
  tr,td{break-inside:avoid}
  thead{display:table-header-group}
}
</style>
</head>
<body>
<!-- The five platform marks, defined once for the whole document. The geometry lives in
     `scripts/osicons.py` and nowhere else, so this page, the 156 facet pages, the 1,294 detail pages and the
     collections cannot end up drawing the same platform two ways -- the failure `tests/theme_test.py` exists
     to catch for the palette. First thing in the body because every `<use>` that points at it is written by
     the script at the bottom, and because `display:none` keeps it out of the layout and out of the skip
     link's focus order either way. A `<symbol>` is never painted where it is defined. -->
__OSSPRITE__
<a class="skip" href="#out">Skip to results</a>
<!-- One shared region for anything the page needs to say that is not already text on the screen: a copy
     succeeding, a clipboard being refused, how many rows "Show more" just added. The result count has its
     own role=status on #count, because that one *is* visible text and should be announced from where it
     is rather than duplicated here. -->
<span class="sr" id="live" role="status" aria-live="polite"></span>
<!-- Drawn here rather than borrowed so there is no third-party licence attached to a 300-byte glyph: a
     four-point star with concave arms, plus a smaller one trailing it. Two tones, `--warn` and `--bar`,
     which is the theme's own pair -- the mark for "new" is the mark for this site, not a generic sparkle.

     Two symbols on one shared viewBox rather than one symbol with two classed paths, because a CSS rule
     cannot reach inside the shadow tree a <use> builds: `.ni .a{fill:...}` matches nothing, and the
     paths fall back to black, which on this surface is an invisible icon. `fill` *is* inherited, though,
     so colouring the two <use> elements -- which are in the ordinary document -- reaches the clones.
     Both symbols share `viewBox="0 0 16 16"`, so the two halves land in one 16x16 space and overlap
     exactly as drawn. -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="star-a" viewBox="0 0 16 16">
    <path d="M6.4.8Q7.63 5.17 12 6.4Q7.63 7.63 6.4 12Q5.17 7.63.8 6.4Q5.17 5.17 6.4.8Z"/></symbol>
  <symbol id="star-b" viewBox="0 0 16 16">
    <path d="M12.6 9.6Q13.26 11.94 15.6 12.6Q13.26 13.26 12.6 15.6Q11.94 13.26 9.6 12.6Q11.94 11.94 12.6 9.6Z"/></symbol>
</svg>
<header><div class="wrap"><div class="top">
  <div>
    <h1>Awesome Agentic Atlas <span>· __LISTS__ awesome-lists, merged</span></h1>
    <p class="sub"><b>__COUNT__</b> projects · <b>__TOPICS__</b> topics · <b>__STARS__</b> combined
      stars · <span id="snap" title="Rebuilt daily from the GitHub API">snapshot
      __SNAPSHOT__</span></p>
    <p class="blurb" id="ctx"></p>
    <!-- Empty on screen, always. `printOn()` writes the link to the current view into it so that a printed
         sheet or a saved PDF says where it came from -- the one thing a screen has in its address bar and
         paper has nowhere to put. -->
    <p id="printurl"></p>
    <!-- The DOM text is sentence case and the uppercase is `text-transform`, so the accessible name reads
         "Last deployed 2026-09-06 18:07 UTC" rather than being spelled out. The clock is decorative and
         hidden from that name; `<time>` carries the timestamp for machines. The href goes to deployment
         history, where the badge's claim can be checked. The line break between the two spans is
         load-bearing: without its text node the accessible name runs "deployed2026" together. A flex
         container drops whitespace-only children, so it costs nothing in layout. -->
    __DEPLOYMENT_BADGE__
  </div>
  <div class="headside">
  <nav>
    <!-- First, because it is the only link here that answers "which of these should I install" and the
         four beside it all answer "what is there". A reader who already knows what they want has the
         filter bar; a reader who does not has 1,294 rows and no way in. -->
    <a href="collections/">Collections</a> ·
    <a href="https://github.com/__REPO__/blob/main/mega-list/leaderboard.md">Leaderboard</a> ·
    <a href="repo/">All projects</a> · <a href="#browse">Topics &amp; harnesses</a><br>
    <a href="https://github.com/__REPO__">Repository</a> ·
    <a href="https://github.com/__REPO__/tree/main/mega-list">Markdown</a> ·
    <a href="https://github.com/__REPO__/releases/latest">Workbook</a><br>
    <!-- No aria-pressed. The label names the action and changes with the state, and "Dark theme" plus
         pressed=true announces as "dark theme is on" -- which is the opposite of what it means. A toggle
         gets a static label and a pressed state, or a changing label and no pressed state; this is the
         second. It also stops the button rendering as a filled accent pill purely because the reader is
         in light mode, which made it look like an active filter. -->
    <button class="chip" id="theme">Light theme</button>
  </nav>
  <div class="atlas-byte-wrap">
    <button type="button" id="byte-tip" aria-label="Ask Archie 'Atlas' Algorithm for a browsing tip">
    <img class="atlas-byte" src="assets/atlas-byte.png" width="512" height="532"
         alt="Archie 'Atlas' Algorithm, the Atlas mascot, wearing pixel sunglasses">
    </button>
    <!-- The accessible name is on `aria-label` so it stays the full name at every width, including the ones
         where only "Archie" is painted. WCAG 2.5.3 wants the visible label contained in the accessible name,
         and "Archie" is. -->
    <button type="button" class="atlas-name" id="byte-name" aria-label="Archie 'Atlas' Algorithm"
            ><span class="atlas-name-full">Archie 'Atlas' Algorithm</span><span class="atlas-name-short">Archie</span></button>
    <button type="button" class="byte-quiet" id="byte-quiet" aria-pressed="false">Quiet mode</button>
    <div id="byte-speech" role="status" aria-live="polite" hidden></div>
  </div>
  </div>
</div></div></header>

<div class="bar"><div class="wrap">
  <div class="line">
    <label for="q">Search</label>
    <!-- aria-label as well as the <label>, because the narrow-viewport rule sets `display:none` on
         `label[for=q]` and that removes it from the accessibility tree as well as from the screen -- so
         on a phone the search box had no accessible name at all. -->
    <!-- The placeholder is the only place the semantic pass is advertised, and it is worth the words: a box
         that says "name, repo, description" is a box nobody types a sentence into, so the capability would
         sit there unused. It names both halves in the order they are tried, and it is phrased as an
         instruction rather than as a field list because the sentence half is the part that needs
         permission. -->
    <input id="q" type="search" aria-label="Search projects"
           placeholder="a name, or describe what you need it to do&hellip;"
           autocomplete="off" spellcheck="false">
    <!-- The handle on the filter sheet. Next to the search box because on a phone those two are the whole
         of the bar, and the pair reads as "what to look for, and what to look in".

         `aria-expanded` and `aria-controls` rather than `aria-pressed`: this opens something, it does not
         turn something on, and the two announce quite differently. `hidden` is not used here and would be
         wrong -- the stylesheet already keeps this out of the layout on every viewport that has room for
         the rows themselves, and JavaScript that never runs must leave those rows on screen rather than
         behind a button. `paintSheet` gives it its accessible name, which always begins with the visible
         word so that a voice-control user can say it (WCAG 2.5.3). -->
    <button class="chip" id="fbt" aria-expanded="false" aria-controls="sheet"
            aria-label="Filters">Filters<span id="fbn"></span></button>
    <select id="sort" aria-label="Sort by">
      <!-- Best match is the default, and it is deliberately not a hidden mode. Ranking search results
           without saying so would silently override a sort the reader had chosen; as an option they can
           see selected, and move away from, the behaviour explains itself. With an empty box it has
           nothing to rank and falls through to Most stars, which is what this page has always opened on. -->
      <option value="relevance">Best match</option>
      <option value="stars">Most stars</option>
      <!-- Removed from this menu rather than left in it on any build whose `data.json` carries no
           velocity -- see `buildChips`. The palette reads these options live, so it loses the entry at the
           same moment and cannot offer a sort the data is unable to answer. -->
      <option value="rising">Rising</option>
      <option value="lists">Named by most lists</option>
      <option value="pushed">Pushed most recently</option>
      <option value="name">Name (A&ndash;Z)</option>
    </select>
    <!-- Beside the sort menu because it answers the same kind of question -- how the results are presented,
         not which ones they are -- and away from the four filter rows below, which all carry aria-pressed
         and mean something else.

         No aria-pressed here, for the reason the theme toggle spells out: the label names the action and
         changes with the state, and "Card view" plus pressed=true announces as "card view is on" when it
         means the opposite. Hidden until `buildChips` runs, like the New chip and the palette hint. That
         function only runs once `data.json` has arrived, and until it has -- or if it never does, which is
         what the error path below is for -- there is no table to lay out either way. -->
    <button class="chip" id="view" hidden>Table view</button>
    <label id="density-control" hidden>Row size
      <select id="density" aria-label="Table row size">
        <option value="compact">Compact</option><option value="normal" selected>Normal</option>
        <option value="expanded">Expanded</option>
      </select>
    </label>
    <button class="chip newchip" id="new" aria-pressed="false"
            title="Projects the most recent import added to the atlas">
      <svg class="ni"><use class="a" href="#star-a"></use><use class="b" href="#star-b"></use></svg>
      <span id="newlabel">New</span></button>
    <!-- The reader's own answer to the same question, and the only filter on this bar that is deliberately
         absent from the URL. Every other one names a property of the data, so a link reproduces the view on
         anybody's machine; this one names a property of *this device* -- the day it was last here -- so a
         shared `?since=1` would show the recipient a set neither of them chose. It stays a local control,
         and `CLEAR` drops it like the rest.

         Hidden until `render()` finds something for it, like the Saved chip beside it and for the same
         reason: on a first visit there is no last visit, so there is nothing this could select. -->
    <button class="chip sincechip" id="since" aria-pressed="false"
            title="Projects added since this device last opened the atlas">
      <span id="sincelabel">Since your last visit</span></button>
    <button class="chip risechip" id="rise" aria-pressed="false"
            title="Projects gaining stars fastest for their size">
      <span id="riselabel">Rising</span></button>
    <!-- Both start hidden and both are revealed by `render()`, not by `buildChips`: what they count is the
         reader's own saved set, which changes while the page is open. The New and Rising chips beside them
         count something the build decided, so those are settled once and never move. -->
    <button class="chip savechip" id="saved" aria-pressed="false"
            title="Only the projects you have saved on this device"><span id="savedlabel">Saved</span></button>
    <button class="chip clearsave" id="clearsave">Remove all saved</button>
    <!-- The comparison, collapsed: this chip *is* the tray. It carries the count while the panel is shut, and
         it sits on the bar rather than in a strip fixed to the bottom of the viewport because the bar is
         already sticky, so a chip here is visible at every scroll position without the one defect a fixed
         strip cannot style away -- being seen at the bottom of the screen and read at the top or the bottom
         of the DOM, so that a keyboard reader arrives at it somewhere other than where it is.
         Painted by `paintCompare()`, from `render()`, like the two chips above. -->
    <button class="chip cmpchip" id="cmpchip" aria-expanded="false" aria-controls="cmp"
            title="Put the projects you have pinned side by side"><span id="cmplabel">Compare</span></button>
    <!-- The way off this page. Not a filter, so no `aria-pressed`: it selects nothing and opens a dialog,
         which is what `aria-haspopup` says instead -- the same distinction the Filters handle makes against
         the chips beside it. Hidden until `expWire()` has both the flag and a `<dialog>` it can open
         modally, for the reason the palette hint is hidden until then: a control that opens nothing is
         worse than no control. -->
    <button class="chip takechip" id="take" aria-haspopup="dialog"
            title="Take this view away as a link, a Markdown table, an HTML page or a PDF">Export</button>
    <!-- Beside Export because it is the same kind of control -- neither one selects rows, both open a dialog,
         so `aria-haspopup` rather than `aria-pressed` for both. Hidden until `mapWire()` has the flag and a
         `<dialog>` it can open modally, exactly like Export: this chip's whole content is a canvas, and a
         browser without `showModal` is not one to hand-roll an overlay for.

         Not the sixth filter. What the map draws is whatever the table is already drawing, so it adds no
         state and takes none away -- which is also why it is not `#view=map`: the two views are two layouts
         of the same rows, and this is one picture of all of them at once. -->
    <button class="chip mapchip" id="mapbtn" aria-haspopup="dialog"
            title="See all __COUNT__ projects at once, laid out by what they do">Map</button>
    <button class="chip" id="palhint"></button>
    <!-- role=status makes this a polite live region, so pressing a chip or typing a search announces the
         new result count instead of silently rewriting a number the reader cannot see. aria-atomic so it
         is read as one sentence rather than as whichever digits changed. -->
    <span class="count" id="count" role="status" aria-atomic="true"></span>
  </div>
</div></div>

<!-- AFTER THE BAR RATHER THAN INSIDE IT (JFH-354). These three rows were inside `.bar` from the day the page
     was written, which made them part of the pinned band: 240px of chrome at 1440x900 and 403px at 768x900,
     most of it rails nobody reads while scrolling results. They render in exactly the same place here -- the
     wrapper follows the bar immediately and carries the bar's old bottom padding -- so the page a reader
     opens is unchanged and only what survives a scroll is different.

     Two things this also settles rather than breaks. The sheet's `position:fixed` needed an argument about
     not being clipped by the bar's `overflow-y:auto`; out here there is no ancestor with an overflow to be
     clipped by, so the argument is gone rather than answered. And its `z-index:30` used to be a *local*
     number, resolved inside the bar's `z-index:20` stacking context, so the sheet could not paint over the
     masthead that was pinned at 30 -- the same collision this ticket is about, in its other direction. In
     the root context 30 outranks both the header's 10 and the bar's 20, which is what a modal sheet wants.

     The backdrop is a sibling and not a `::before` on the sheet: it has to cover the page the sheet is
     over, and a pseudo-element of the sheet is inside it. -->
<div class="subbar"><div class="wrap">
  <div id="fbb"></div>
  <div id="sheet" role="group" aria-label="Filters" tabindex="-1">
    <!-- Only ever on screen in the sheet's narrow form; `.shead{display:none}` above is the desktop, where
         the rows are simply part of the bar and there is no panel to title or to dismiss. -->
    <div class="shead"><span class="sh" id="shtitle">Filters</span>
      <button class="chip" id="fbx">Done</button>
      <!-- No `role=status` on this one, though it is a live number: `#count` in the bar already has one and
           carries the same sentence, and two polite regions saying the same thing announce it twice. -->
      <span id="scount"></span>
    </div>
    <div class="line facet"><label>Topic</label><span id="cats"></span></div>
    <div class="line facet"><label>Plugs into</label><span id="tgts"></span></div>
    <div class="line facet"><label>Runs on</label><span id="oses"></span>
      <button class="chip" id="strict" aria-pressed="false"
              title="Drop rows where support is inferred from the language rather than stated">Confirmed
        only</button>
      <button class="chip" id="reset">Clear all</button>
    </div>
  </div>
</div></div>

<main><div class="wrap">
  <!-- Empty and hidden on every ordinary visit; `paintShared()` fills it only when the hash carried a
       `list=`. Static markup rather than something the script creates, for the reason the Saved chip is
       static: what decides whether it belongs on screen is the reader's own URL, and a strip that has to be
       built before it can be shown is a strip that is missing from the first paint of a shared link.

       Above the results and below the bar, which is where it belongs because of what it describes -- not a
       filter the reader chose and not a fact about any row, but what this page is *of* at the moment, which
       is somebody else's collection. -->
  <div class="shared" id="shared">
    <span id="sharedtext"></span>
    <span class="sp"><button class="chip" id="sharedadd"></button>
      <button class="chip" id="sharedall">Show the whole atlas</button></span>
  </div>
  <!-- The comparison, expanded. Empty and hidden until something is pinned, and static markup for the reason
       the strip above it is: what decides whether it belongs on screen is the reader's own URL, and a `#cmp=`
       link has to arrive with somewhere to put its answer rather than waiting for a script to build the box.

       Here rather than beside the results because of what it is: not a filter, and not a row. It is the
       question the eleven source lists cannot answer -- "which of these three" -- so it goes above the answer
       to "what are the options", in the slot the shared-list strip already established for a sentence about
       what this page is currently of.

       `role=region` with a name, so a screen reader can be told a landmark appeared and jump to it; without
       the name it would be an unlabelled region, which is worse than no landmark. -->
  <div id="cmp" role="region" aria-label="Side-by-side comparison">
    <div class="ch"><span id="cmpwhat"></span>
      <span class="sp"><button class="chip" id="cmpclear">Clear the comparison</button></span></div>
    <div class="scroll" id="cmptable"></div>
  </div>
  <!-- The verdict legend, and the only place on screen that says what the five marks mean. It used to be
       said in `listMarkdown()` and `listHTML()` and nowhere else -- that is, in the exports, and not on the
       page the exports are made from. On screen the sole explainer was each cell's `title`, which needs a
       pointer, so on a phone the marks were undecodable: `?` alone is 3,018 of 6,470 cells, 46.6%, the most
       common verdict on the page.

       `<details>` rather than a permanent strip, because this is a question a reader asks once. Closed it is
       one line whose `<summary>` is real text a reader can see and tap, which is the whole difference from a
       `title`; open it is a `<dl>` naming all five. Not in `<thead>`, which was the obvious home and is the
       wrong one: `html[data-view=cards] thead{display:none}` and cards is the default view, so a legend there
       is invisible to most readers. Above `#out` it is in both views and on the printed sheet.

       The `<dt>` glyphs are `aria-hidden` and the word beside them is the accessible text, so a screen reader
       reads five verdicts rather than five symbol names. Same trade the row builder makes, and the reason
       `VERDICT` was free to move `a` off the dash it shared with `-`. -->
  <details class="vkey">
    <summary>What the <span aria-hidden="true" class="vY">✓</span>
      <span aria-hidden="true" class="vL">?</span> <span aria-hidden="true" class="vN">✗</span>
      <span aria-hidden="true" class="v-">–</span> <span aria-hidden="true" class="va">·</span>
      marks mean</summary>
    <dl>
      <dt aria-hidden="true" class="vY">✓</dt><dd><b>Stated support.</b> The project says so itself.</dd>
      <dt aria-hidden="true" class="vL">?</dt><dd><b>Inferred from the language,</b> not stated. Written in
        something that runs here, with no claim made either way. <b>Confirmed only</b> hides these.</dd>
      <dt aria-hidden="true" class="vN">✗</dt><dd><b>No evidence of support.</b></dd>
      <dt aria-hidden="true" class="v-">–</dt><dd><b>Not established.</b> Too little to tell either
        way.</dd>
      <dt aria-hidden="true" class="va">·</dt><dd><b>Not applicable.</b> The platform question does not
        apply to this project.</dd>
    </dl>
  </details>
  <div id="out"></div>
</div></main>

<!-- Outside the filter bar on purpose. A <dialog> nested inside a flex row that the narrow-viewport rules
     hide would be unopenable on a phone, and a modal is not part of the row it is launched from anyway.
     The combobox attributes are on the input rather than on a wrapper because the input is what holds
     focus the whole time -- aria-activedescendant points at the highlighted option, so a screen reader
     announces each row as you arrow through them without focus ever leaving the box you are typing in. -->
<dialog id="pal" aria-label="Jump to a topic, platform, sort or project">
  <input id="palq" type="text" role="combobox" aria-expanded="true" aria-controls="palist"
         aria-autocomplete="list" autocomplete="off" spellcheck="false"
         placeholder="Jump to a topic, a platform, a sort, or a project&hellip;">
  <ul id="palist" role="listbox" aria-label="Matches"></ul>
  <div class="palfoot"><span><kbd>&uarr;</kbd> <kbd>&darr;</kbd> move</span>
    <span><kbd>Enter</kbd> select</span> <span><kbd>Esc</kbd> close</span></div>
</dialog>

<!-- Outside the filter bar for the same reason the palette is: a <dialog> nested in a flex row that the
     narrow-viewport rules hide cannot be opened on a phone.

     `aria-labelledby` rather than `aria-label`, because this one has a real heading on screen -- so the
     accessible name and the visible title are the same string by construction and cannot drift. -->
<dialog id="exp" aria-labelledby="exph">
  <h2 id="exph">Take this view with you</h2>
  <p class="expsub" id="expwhat"></p>
  <div class="expurl">
    <!-- The link is on screen and selectable before anything is pressed. `readonly` and not `disabled`: a
         disabled input cannot take focus, so it cannot be selected either, and selecting it by hand is
         exactly the fallback for a clipboard write that was refused. -->
    <input id="expurl" type="text" readonly aria-label="Link to this view">
    <!-- Removed rather than disabled where the clipboard is unreachable, which is the rule the 120 row-level
         Copy buttons already follow: a button that fails on click is worse than none, and the input beside
         it is the whole fallback. -->
    <button class="chip" id="expcopy">Copy link</button>
  </div>
  <div class="expacts">
    <button id="expmd"><span class="t">Markdown table</span>
      <span class="k">for a GitHub issue, a README or a wiki</span></button>
    <button id="exphtml"><span class="t">HTML page</span>
      <span class="k">one self-contained file, nothing to fetch</span></button>
    <button id="expprint"><span class="t">Print, or save as PDF</span>
      <span class="k">your browser&rsquo;s print dialog, on the table layout</span></button>
  </div>
  <p class="expnote">Built here, in this tab, out of the rows already on the page. Nothing is uploaded and
    no request leaves your browser &mdash; which is also why a link to your own saved projects carries the
    projects themselves rather than pointing at a list on a server.</p>
  <div class="expfoot"><button class="chip" id="expdone">Done</button></div>
</dialog>

<!-- The map. Outside the filter bar for the third time and for the third time for the same reason: a
     `<dialog>` nested in a flex row the narrow-viewport rules hide cannot be opened on a phone.

     `role="img"` with an `aria-label` that `mapPaint()` rewrites, which is an honest description of what a
     canvas is and the only one available. There is no accessible tree inside a bitmap, and the alternative
     -- 1,294 focusable nodes standing in for dots -- would be a worse experience than the sentence, because
     every fact those nodes could carry is already in the table this dialog is drawn over, in a form that has
     been navigable since the page was written. What the sentence says is therefore what a reader who cannot
     see the picture actually needs: how many projects are lit, out of how many, by which view. The
     *structure* stays operable -- the topic key below is fourteen real buttons, and each one is the same
     filter as the topic chip of that name on the bar. -->
<dialog id="mapdlg" aria-labelledby="maph">
  <div class="maphead"><h2 id="maph">The atlas, as a map</h2>
    <p id="mapwhat"></p>
    <button class="chip" id="mapreset">Reset the view</button>
    <button class="chip" id="mapdone">Done</button></div>
  <div class="mapstage" id="mapstage">
    <canvas id="mapc" role="img" aria-label="A map of every project in the atlas"></canvas>
    <!-- Both start hidden and only one of them is ever shown at a time: the readout when a dot is under the
         pointer, the sentence when there is no map to put a pointer on. -->
    <div id="maptip" hidden></div>
    <p id="mapnope" hidden></p>
  </div>
  <div class="mapkey" id="mapkey" role="group" aria-label="Topics"></div>
  <div class="mapfoot"><span id="maphint"></span>
    <!-- Written by `mapPin()` because its label names a project and a number, and hidden the rest of the
         time: a button that says "show these in the table" with nothing pinned has no "these". -->
    <button class="chip" id="mapnear" hidden></button></div>
</dialog>

<footer><div class="wrap">
  Every entry came from someone else's curation work; all __LISTS__ source lists are credited in the
  <a href="https://github.com/__REPO__#the-source-lists">repository</a>. Stars, language, licence and
  last-push come from the GitHub API on __SNAPSHOT__ and drift daily. Platform verdicts are derived
  from each project's own README, install route, CI config and release assets &mdash;
  <span class="vY">green&#8201;&#10003;</span> is stated evidence,
  <span class="vL">amber&#8201;?</span> is inferred from the language, and
  <span class="vN">grey&#8201;&#10007;</span> is neither. The glyph says the same thing the colour does,
  so the column still reads in greyscale, in print, and with a colour-vision deficiency. A push date
  <span class="old">underlined like this</span> means nothing has landed in that repo for over a year.
  A dash in the star column means the row is a folder inside someone else's repo, or a dead
  link, and has no count of its own.
  <!-- Every filtered view of this page lives in the hash, which a crawler will not execute -- so the 156
       prerendered pages under topic/ and target/ were reachable only from sitemap.xml, and a sitemap is a
       hint rather than a path. These 26 links put each one click from the root and each crossing two.
       Built in `substitute()` from the same `cats`/`targets` the page itself uses, so a new topic appears
       here without anyone remembering to add it. -->
  <nav class="facets" id="browse" aria-label="Browse by topic or by what a project plugs into">
    <p><b>Every topic:</b> __TOPICLINKS__</p>
    <p><b>Every integration:</b> __TARGETLINKS__</p>
    <!-- The 1,294 pages under repo/ have the same discovery problem the 26 links above solve, and one
         worse: the rows that link to them are drawn by the script below, so a crawler receives this page
         with an empty table and never sees one of them. This link and the directory it points at put
         every project page two clicks from the root. -->
    <p><b>Every project:</b> <a href="repo/">all __COUNT__ projects, one page each, grouped by topic</a></p>
  </nav>
</div></footer>

<script>
const PAGE_SIZE = 120;
const FLAGS = __APP_FLAGS__;
// Cards, not the table, because the screenshot is the reason to open this page rather than read
// `mega-list/`: a card carries the project's own banner and a table row has nowhere to put one. The table
// is still the better view for scanning 120 rows against each other, so it keeps its button and gets a
// shareable `#view=table` -- and `readHash` reads both words explicitly, so every `#view=cards` link
// written while cards were opt-in still means exactly what it said.
//
// Kept in step with `data-view` on the <html> tag, which is what the reader looks at until `data.json`
// lands. The two have to agree: disagreeing would show the table's column headings over an empty body for
// the length of a 561 KB fetch and then replace them with cards.
//
// `list` is the odd one and it earns its place here: it is a set of `owner/name`, it filters the table, and
// unlike `SAVED` below it *is* a view -- it arrives in the hash, a link reproduces it exactly, and it is
// somebody else's collection rather than the reader's own store. So it goes in `state` and not beside the
// saved set, and `state.saved` is a flag over a store while `state.list` is the rows themselves.
//
// `cmp` is the odder one and it splits the rule this block states. It belongs in `state` on every count that
// matters: it is a set of `owner/name`, it goes in the hash, and a link reproduces it exactly -- a comparison
// of four projects means the same four on anybody's machine, which is the whole reason it is a URL and not a
// second `localStorage` key beside `SAVED`. But it is the one thing in here that `set()` must never be used to
// change, because `set()` resets `shown` to the first page and pinning the fourth project is precisely what a
// reader forty rows into a topic does. `togglePin` therefore writes the set, writes the hash and repaints, and
// the note above it says why in full. Nothing else in `state` may be mutated that way.
//
// It is also not a filter, and three places downstream depend on that: `match` does not read it, so pinning
// never changes which rows are on screen and a pinned project survives every filter the reader then applies;
// `rescue()` does not offer to drop it, because it cannot be the reason a table is empty; and `viewTitle()`
// does not name it, because an export is of a view and this is not one.
const state = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false, since: false, rising: false,
               saved: false, list: new Set(), cmp: new Set(), sort: "relevance", shown: PAGE_SIZE,
               view: "__DEFAULT_VIEW__"};
let D = null, ROWS = [], NEW = 0, RISE = null, RISING = 0;
// The import whose arrivals are New, as this tab understands it. Not simply `D.cohort`: the build applies
// the stale bound at build time, and a tab left open for a fortnight has to apply it again or it goes on
// pulsing an outline around a cohort that stopped being the latest news while nobody was looking. Set by
// `prepare()`, which is the one place that has `D`.
let COHORT = "";

// `owner/name` to the row object, built once when `ROWS` is. The comparison needs it and nothing else does:
// every other consumer on this page walks `ROWS` because it is answering a question about all of them, and
// this one is answering a question about four keys that arrived in a URL. Four linear scans of 1,294 rows on
// a hashchange is not the reason for the map -- it is that the pinned set has to keep resolving to rows after
// the reader has filtered the table down to nine, so the lookup cannot go through `HITS`.
let BY_NWO = new Map();

// How many projects a comparison holds. Four and not five, which the ticket left open: five columns plus the
// row labels is six, and the panel is a scroller whose columns have a 148px floor -- so at five the reader on
// a 375px phone is swiping through more than two screens of table to see one row of it, and on a 1440px
// desktop the fifth column is the one that falls off the end of the box. Four is also the number a person can
// hold a decision between; past that the panel is a way of postponing one.
//
// Enforced in three places on purpose, because the set has three doors: `togglePin` refuses to add past it,
// `readHash` truncates a hand-edited `#cmp=` to it, and `pinBtn` disables the buttons that would exceed it.
// The middle one is the one that matters -- a hash is an untrusted input, and this is the same argument the
// 200-key cap on `#list=` makes one function along.
const CMP_MAX = 4;

// Whether the panel is open. Not in `state`: it is not in the hash, a link does not reproduce it, and it is
// not what the page is *of* -- it is what the reader is currently looking at, which is the same category as
// which `<details>` they have expanded. It starts true so that the panel appears on the first pin rather than
// behind a second press, and so that a `#cmp=` link opens showing the comparison it was sent to show. The
// chip closes it, and closing it keeps the pins: those are two different things and conflating them would
// make "put this away for a moment" destroy the selection.
let CMP_OPEN = true;

// The reader's saved projects, as a Set of `owner/name`. Two things it deliberately is not:
//
// It is not in `state`. Everything in `state` is a *view* -- it goes in the hash, it is what a link
// reproduces, and `set()` resets the page size whenever any of it changes. The saved set is none of those:
// it survives navigation, it is not what the URL describes, and saving a project should not scroll the
// reader back to row 60. `state.saved` is the filter over this set, which *is* a view; the set itself
// lives out here with the other things `render()` reads and does not own.
//
// It is not the nwo strings' only home either -- rows carry their own -- so this holds the key rather than
// the row, and a saved project that leaves the source lists simply stops matching anything. That is the
// right failure: the alternative is caching a copy of a row and showing a reader stale stars forever.
let SAVED = new Set();
const SAVE_KEY = "saved";

// Both halves swallow their exceptions, and neither is being lazy about it. `localStorage` throws on
// access -- not on read, on *access* -- in Safari's private mode and wherever third-party storage is
// blocked, which is the same reason the theme bootstrap at the top of this page is wrapped. A reader in
// that mode gets a page whose Save buttons work for the session and forget afterwards, which is strictly
// better than a page whose script died before it drew a table.
function loadSaved() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    const list = raw ? JSON.parse(raw) : [];
    // Filtered rather than trusted. This value is editable by hand and survives every deploy, so it is the
    // one input to this page that a future build has no control over: a non-array parses fine and would
    // make `new Set` throw, and a nested object would put `[object Object]` in a `data-nwo` attribute.
    SAVED = new Set(Array.isArray(list) ? list.filter(s => typeof s === "string" && s) : []);
  } catch (e) {
    SAVED = new Set();
  }
}

function storeSaved() {
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify([...SAVED]));
  } catch (e) {}
}

// WHEN THIS DEVICE WAS LAST HERE, AND WHY IT IS A SEPARATE ANSWER FROM THE COHORT.
//
// The New chip counts the latest import. That is the right answer for a reader arriving cold and the wrong
// one for a reader who is here every week: they were present for the last import, and what they have not
// seen is everything that landed since their own last visit -- which can span several cohorts, or none.
//
// A date, not a timestamp. The ledger's resolution is a day, so a finer figure here would be compared
// against `first_seen` strings that cannot answer it, and `r.first_seen > SEEN_AT` would start depending on
// which side of midnight the build ran. Same reason `newness.pretty` prints a day.
//
// Read once at load and deliberately *not* refreshed while the tab is open: the count has to stay still
// while it is being read. `markVisit()` writes today's date, so the next visit compares against this one.
const VISIT_KEY = "atlas-last-visit";
let SEEN_AT = "";
let SINCE = 0;

function loadVisit() {
  try {
    const raw = localStorage.getItem(VISIT_KEY) || "";
    // Shape-checked, not trusted, for the reason `loadSaved` filters its array: this value survives every
    // deploy and is editable by hand. A malformed one is treated as a first visit, which is the state that
    // shows the reader the cohort instead -- never an error.
    SEEN_AT = /^\d{4}-\d{2}-\d{2}$/.test(raw) ? raw : "";
  } catch (e) {
    SEEN_AT = "";
  }
}

function markVisit() {
  // THE SNAPSHOT OF THE DATA THIS READER WAS SHOWN -- not `TODAY`, which is their own clock.
  //
  // What gets stored has to be comparable with `first_seen`, and `first_seen` is a build date. Storing the
  // reader's date loses an import whenever they arrive before that day's build: visit at 08:00 on the 21st,
  // store "2026-09-21", the build lands at 12:40 stamping its arrivals "2026-09-21", and on the next visit
  // `first_seen > SEEN_AT` is false for every one of them. An import silently never happened.
  //
  // `D.snapshot` is the date of the rows they actually read, so anything stamped after it is genuinely
  // unseen and anything stamped at or before it is genuinely seen. Two visits to the same snapshot report
  // nothing new, which is correct rather than a bug. `TODAY` is the floor only for a `data.json` written
  // before `snapshot` existed.
  try {
    localStorage.setItem(VISIT_KEY, (D && D.snapshot) || TODAY);
  } catch (e) {}
}
// Whether the rows on screen came out of the browser's cache instead of off the network. Set from the one
// header the service worker adds, read only by `stamp()`, and false on the error path -- where there are no
// rows to describe.
let FROM_CACHE = false;
// The pending debounced search, if any. Declared out here rather than beside the handler because `set()`
// has to cancel it, and `set()` is not inside the fetch callback where the handlers are wired.
let typing = 0;

// The window is applied here, in the browser, against the reader's own clock -- `data.json` carries the
// raw first-seen date and nothing else. That is what makes the mark expire without a rebuild: a repo
// stamped the 14th stops being new on the 29th in every open tab, on a day the cron may not have run.
// Both sides of the subtraction are ISO dates, which Date.parse reads as UTC midnight, so the result is
// a whole number of days and never 13.958 because of a timezone.
const TODAY = new Date().toISOString().slice(0, 10);
const daysAgo = iso => Math.round((Date.parse(TODAY) - Date.parse(iso)) / 86400000);
const mmddyy = iso => iso.slice(5, 7) + "/" + iso.slice(8, 10) + "/" + iso.slice(2, 4);
const SNAPSHOT = "__SNAPSHOT__";
const BUILT = "__BUILT__";

// Colour was the only thing distinguishing a stated Yes from an inferred Maybe from a No, which is a
// WCAG 1.4.1 failure and, more plainly, unreadable for anyone with a red/green deficiency. Each verdict
// now carries a glyph as well, chosen so that its screen-reader pronunciation is also the meaning:
// "check mark", "question mark", "ballot x". A tilde would have read as "tilde".
//
// That pronunciation argument no longer has to hold, and `a` is why. It and `-` both drew `–`, in the same
// `--off` colour at the same opacity, so "the platform question does not apply to this project" and "we
// could not tell either way" were indistinguishable in every channel a reader has -- not colour-only, which
// is 1.4.1, but absent. 220 of 6,470 cells, and never both in one row, so it is a defect a reader meets
// only when comparing two projects. Splitting them needed a second glyph, and every character with a good
// spoken name was taken. So the word moved instead: the row builder now puts "platform: verdict" in the
// `.sr` span and marks the glyph `aria-hidden`, which means a screen reader reads the verdict rather than
// pronouncing a symbol, and the glyph is free to be chosen for the eye alone. Hence `·` -- a dot against a
// dash is a shape difference at 11.5px, where two dashes were nothing.
//
// Keep this map, the `.vkey` legend in the body, and the gloss in `listMarkdown()` and `listHTML()` in step.
// Three sources for one fact, which is the drift `osicons.py` exists to prevent for the platform icons by
// generating every end from one place. There is no generator here, so `theme_test.py` reads all three out
// of this file and asserts they agree -- not `probe.mjs`, which reads the last page that was *built* and so
// cannot be asked about a legend added to the generator today.
const VERDICT = {
  Y: ["✓", "stated support"],
  L: ["?", "inferred from the language"],
  N: ["✗", "no evidence of support"],
  a: ["·", "not applicable"],
  "-": ["–", "not established"],
};

// The other half of a verdict: which platform it is about. The five words became marks, and these two arrays
// are the whole of what the browser needs to draw them -- the `<symbol>` ids in the sprite at the top of the
// body, and the hover text for the five filter chips. Both are written out by `scripts/osicons.py`, in the
// order `OS_LABELS` is checked against, rather than retyped here: index k of either one describes character
// k of a row's `os` string, and a page whose ids drifted from its sprite draws five invisible boxes per row.
// `OST` is longer than `OSI`'s labels on purpose for WSL2, which is the one mark nobody can be expected to
// recognise on sight.
const OSI = __OSIDS__;
const OST = __OSTITLES__;

// `aria-hidden`, always. Every caller puts the platform's word beside this -- in a `title`, in a `.sr` span,
// or both -- because a picture is a shorthand for people who can see it and nothing at all to anyone else.
function osIcon(k) {
  return '<svg class="oi" aria-hidden="true" focusable="false"><use href="#' + OSI[k] + '"></use></svg>';
}

// Feature-detected rather than assumed, and the button is simply not rendered when the answer is no --
// 120 buttons that fail on click are worse than none. `isSecureContext` is part of the test because the
// API exists but always rejects on plain http, which is how a contributor serving docs/ locally sees it.
const CAN_COPY = !!(navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext);

// Where 22_detail.py put this project's own page. The rule has to match `segment()` in that stage exactly
// or every row links to a 404: lowercased, because 442 of the 1,294 nwo values carry capitals and Pages
// resolves paths case-sensitively, and a leading dot rewritten because whether a dot-directory is served
// at all is the one thing about this tree a local server cannot answer.
const detailURL = nwo => "repo/" + nwo.toLowerCase().split("/")
  .map(s => s.startsWith(".") ? "dot-" + s.slice(1) : s).join("/") + "/";

// The rescue buttons drawn on an empty table, in the order render() drew them. Kept out of the markup
// because a filter patch is an object -- serialising it into a data- attribute and parsing it back would
// be two more chances to get the OS index array wrong.
let RESCUE = [];

// A live region only fires on a *change*, so setting the same string twice announces once -- which is
// exactly the case here, since copying two install lines in a row produces the same sentence. The clear
// and the tick force a second announcement.
function say(msg) {
  const el = document.getElementById("live");
  el.textContent = "";
  setTimeout(() => { el.textContent = msg; }, 30);
}

// Relative, because the question a reader is asking of this column is "is this thing alive", and nobody
// does date arithmetic in their head. Rounding is safe: the exact date stays in the title. Past a year
// it gets the dotted marker -- quietly, because a dormant repo is a fact about the repo, not a verdict.
// Split from the markup below it for one caller: the comparison panel marks a row when the projects in it
// disagree, and what it has to compare is the string the reader is looking at rather than the underlying date.
// Two projects pushed nine and eleven days apart both read "1mo ago", and flagging that as a difference would
// put a `≠` beside two cells a reader can see are identical -- which is worse than missing a difference,
// because it teaches them the marks are noise. So the text is a function and the wrapper is a wrapper.
function sinceText(iso) {
  if (!iso) return "—";
  const d = daysAgo(iso);
  return d <= 0 ? "today" : d === 1 ? "yesterday" : d < 30 ? d + "d ago"
    : d < 365 ? Math.round(d / 30) + "mo ago"
    : d < 730 ? (d / 365).toFixed(1) + "y ago" : Math.floor(d / 365) + "y ago";
}

function since(iso) {
  const t = sinceText(iso);
  if (!iso) return t;
  const d = daysAgo(iso);
  return d >= 365
    ? '<span class="old" title="' + iso + ' — no push in over a year">' + t + "</span>"
    : '<span title="' + iso + '">' + t + "</span>";
}

// The gain figure for one row, or "" where the ledger cannot support one. Absent and not "+0": empty means
// "we were not watching this repo that long ago" and zero means "it gained nothing", and 25_velocity.py
// goes to some trouble to keep the two apart -- collapsing them here would put a fabricated number back on
// every row it kept out. The title carries the measured span rather than the nominal window, because a
// missed weekly build makes them differ and a figure labelled with a window it does not cover is worthless.
function gained(r) {
  if (!RISE || r.gain === null) return "";
  // A zero is dressed as a fall, not as a rise. `--good` at weight 600 is the page saying "this is going
  // up", and a project that gained nothing is not going up -- on a seven-day window most of the long tail
  // of small projects genuinely gains nothing, so this is the common case and not a rare one. It still
  // draws a figure rather than nothing, because nothing already means something else here: that the ledger
  // does not reach back far enough to say. A measured zero and an unknown must not look alike. Unsigned,
  // because "+0" asserts a direction that the number itself denies.
  const sign = r.gain < 0 ? "−" : r.gain > 0 ? "+" : "";
  const n = sign + Math.abs(r.gain).toLocaleString();
  return ' <span class="rise' + (r.gain > 0 ? "" : " down") + '" title="' +
    esc(n + " stars in the " + RISE.span + " days from " + RISE.from +
        " to " + D.velocity.to) + '">' + n + "</span>";
}

fetch("data.json").then(r => {
  // The only place the real deployment time is available, and it arrives on a request the page was going
  // to make anyway. See `deployStamp`. Before `r.json()`, because that consumes the body and there is no
  // reason to wait for 561 KB to parse before correcting a badge that is already on screen.
  deployStamp(r.headers.get("Last-Modified"));
  // Set by `data()` in `docs/sw.js` on the one path where the network did not answer and it fell back to
  // `atlas-data`. Absent on every other path, including a response the worker had just put in that cache,
  // so this is "the network is gone" and not "there is a cached copy".
  FROM_CACHE = !!r.headers.get("__CACHEHDR__");
  return r.json();
}).then(d => {
  D = d;
  // The build-time half of the platform marks against the runtime half. `OSI` was written by
  // `scripts/osicons.py` when this page was generated and `d.os` arrives with the data, so a `data.json`
  // from a build that knew about a sixth platform -- or a cached page that predates a fifth -- would draw
  // marks for the columns it had and an empty box for the rest, silently, on every row. There is no honest
  // fallback: a mark beside the wrong verdict is a page stating a falsehood about the one thing a reader came
  // here to check. Thrown rather than reported, because the `catch` below is the page's existing answer to
  // "the data is not what this page can read" and it puts the reason on screen.
  if (d.os.length !== OSI.length)
    throw new Error("data.json names " + d.os.length + " platforms and this page was built with " +
      OSI.length + " marks — see scripts/osicons.py");
  // THE COHORT, RE-BOUNDED IN THE BROWSER.
  //
  // `d.cohort` was already put through the stale bound by the build that wrote it, so this looks redundant
  // and is not: the build applied the bound *on the day it ran*. A tab left open, or a page the service
  // worker serves out of `atlas-data` after the pipeline has stopped, carries a `data.json` that keeps
  // saying the same thing for as long as it is held -- and the pipeline does stop, for five consecutive
  // days in September 2026 on one unmapped upstream heading. Without this, that fortnight-old import goes
  // on being announced as the latest news, with an outline pulsing around every row of it.
  //
  // Same arithmetic as `newness.cohort`, against the reader's clock rather than the builder's, which is the
  // only clock a held page has. `d.cohort` is absent in a `data.json` written before cohorts existed; `""`
  // is the honest reading of that -- such a build never recorded which import brought what.
  COHORT = d.cohort || "";
  if (COHORT && daysAgo(COHORT) > (d.window_days || 14)) COHORT = "";
  // Column-oriented on the wire, objects in here. One pass over every row, so the rest of the page can
  // read `r.stars` instead of `r[4]`.
  ROWS = d.rows.map(a => Object.fromEntries(d.cols.map((c, i) => [c, a[i]])));
  ROWS.forEach((r, i) => {
    // Position in `d.rows`, kept because it is the only thing that addresses the semantic index:
    // `docs.bin` is one 96-byte vector per row in this order and carries no keys. Recorded here rather
    // than read from `ROWS.indexOf` at score time, which would be a 1,294-row scan per row scored, and
    // recorded before anything sorts anything -- every sort in this page reorders copies, but a row that
    // learned its own ordinal after a sort would learn the wrong one.
    r.ord = i;
    r.hay = (r.name + " " + r.nwo + " " + r.blurb + " " + r.lang + " " + r.listed_by).toLowerCase();
    // `hay` answers "does this row match" and cannot answer "where did it match", which is the only
    // question ranking cares about. Lowercasing the three fields separately here rather than inside the
    // scorer keeps 1,294 * 5 `toLowerCase` calls out of every keystroke.
    r.lname = r.name.toLowerCase();
    r.lnwo = r.nwo.toLowerCase();
    r.lblurb = (r.blurb || "").toLowerCase();
    // GitHub's social card for the repository, derived from `nwo`, for every row -- not `r.img || ...`,
    // which is what stood here and which let 686 of the 1,294 rows override it with whatever URL their
    // upstream README used for its own banner.
    //
    // The override is ignored here (JFH-218) because nothing bounds what those URLs serve. Measured across
    // the 686: median 447,380 B, mean 1,425,377 B, largest 10,946,713 B -- one picture 35x this page's
    // entire 307,200 B budget. The cards view lays out 120 at a time, so the page's weight was a function
    // of what 686 strangers committed to their own repositories: a runner measured 1,357,365 B of images one
    // half-hour and 1,827,508 B the next on a byte-identical tree, and a single animated GIF in one README
    // (`ecc-plan-canvas-demo.gif`, 716,235 B) was 53% of the image total on its own. A social card is a
    // fixed ~100 KB at 1200x600, which still oversupplies the ~1,000x500 device pixels the widest card slot
    // asks for on Lighthouse's mobile profile -- so this bounds the worst case and loses no resolution at
    // any viewport.
    //
    // What it does lose, and this is a decision rather than an oversight: 149 of the 686 are animated GIFs
    // -- 21.7% of the pictures, 11.5% of all rows -- and a social card is a static PNG, so those demos no
    // longer move here. At a 447 KB median and a 10.9 MB maximum that is the trade. The artwork is still
    // reachable in the two places where one image is nobody's budget: the repo's own detail page, which
    // still renders `img`, and the outward `nwo` link under every title.
    //
    // `data.json` keeps the column. Only the render path changed -- see the note beside the writer.
    r.img = "https://opengraph.githubassets.com/1/" + r.nwo;
    // NEW IS COHORT MEMBERSHIP, NOT AN AGE.
    //
    // `d.cohort` is the import that brought the current arrivals. A row is new because it came in on that
    // import -- not because its `first_seen` is within some number of days, which is what stood here and
    // which asked a question about the calendar when the interesting one is about the atlas. Repos reach
    // this site when a curator adds them to a list, so they are all years old in the world; "new" here can
    // only ever mean "new to this site", and the import that brought them is exactly that set.
    //
    // The build applies the stale bound and sends "" when a cohort is past it, so an empty `cohort` means
    // nothing is new and the `&&` short-circuits every row to false. `COHORT_STALE` below re-applies the
    // same bound in the browser, for the tab that was left open across the expiry.
    r.isnew = !!r.first_seen && r.first_seen === COHORT;
    // Per row rather than recomputed in the predicate, for the reason `lname` and `lblurb` above are
    // precomputed: `filter()` runs this on every row on every keystroke, and a string compare per row per
    // keystroke is the thing that map exists to avoid.
    r.issince = !!r.first_seen && !!SEEN_AT && r.first_seen > SEEN_AT;
  });
  NEW = ROWS.filter(r => r.isnew).length;
  // SINCE YOUR LAST VISIT -- the other half of the answer, and a different one per reader.
  //
  // The cohort serves a reader who arrives cold: "what did the last import bring". It serves an active
  // reader badly, because they were here for the last import and the one before it, and what they have
  // not seen is everything since *their* last visit, which may span several cohorts. `SEEN_AT` is that
  // date, off this device; `SINCE` is the arrivals after it.
  //
  // Strictly wider than NEW is not guaranteed and must not be assumed: a reader who last visited an hour
  // ago has an empty SINCE and a full NEW. The two chips are painted independently for that reason.
  SINCE = ROWS.filter(r => r.issince).length;
  // Record the visit now that it has been counted. Safe to call on a repaint -- `19c_live.py` can hand this
  // page a fresher `data.json` and `prepare()` runs again -- because this writes storage and deliberately
  // does not touch `SEEN_AT`. The in-memory value stays on whatever the tab loaded with, so the count a
  // reader is looking at does not drop to zero underneath them mid-session.
  markVisit();
  // Velocity. `25_velocity.py` writes the two columns and the `velocity` block; this page only reads them
  // and owns none of the arithmetic. `rise.col` names the window the ledger could actually answer -- `d30`
  // once a month of history exists, `d7` for the three weeks before that, and "" on the day the ledger
  // started -- so this one test is also "is the feature switched on at all", and a `data.json` written
  // before that stage existed lands on the same branch as one whose ledger is still empty.
  RISE = (d.velocity && d.velocity.rise && d.velocity.rise.col)
    ? Object.assign({}, d.velocity.rise, d.velocity[d.velocity.rise.col]) : null;
  ROWS.forEach(r => {
    // `=== ""` and not a falsy test. Empty means "not watching yet" and 0 means "gained nothing"; a falsy
    // test would throw the second away with the first, which is the fabricated zero the whole ledger
    // design exists to avoid.
    const g = RISE ? r[RISE.col] : "";
    r.gain = (g === "" || g === undefined || g === null) ? null : g;
    // A finite sort key always, so the comparator can never be handed NaN. Rows with no history sort below
    // every row that has any, including below a genuine fall -- "unknown" is not "worst".
    r.gkey = r.gain === null ? -1e9 : r.gain;
    // Both floors, not either. The absolute one is what stops a 4-star repo qualifying on +1 and the
    // relative one is what stops a 200,000-star repo qualifying merely for being large. Both arrive in
    // `data.json` already scaled to the window in use, so this page applies them and does not own them --
    // the same arrangement `window_days` has, and for the same reason.
    r.rise = r.gain !== null &&
      r.gain >= Math.max(RISE.min_abs, RISE.min_pct / 100 * (r.stars || 0));
  });
  RISING = ROWS.filter(r => r.rise).length;
  // After the two `forEach` passes above, so the rows in here are the finished ones -- the map holds the same
  // objects, not copies, but building it earlier would be a claim about ordering that the next stage to add a
  // derived column would quietly break.
  BY_NWO = new Map(ROWS.map(r => [r.nwo, r]));
  // Again, now that the rows are here. `wire()` already called it off the document's own constant, which is
  // the best that can be said before this fetch resolves; this is the call that replaces that with the
  // stamp the rows brought with them, and the only one whose answer is about what is on screen.
  stamp();
  buildChips();
  readHash();
  render();
  // A shared link that already carries a query is a reader who has searched without ever touching the box,
  // so neither of the two listeners in `buildChips` will fire. `render()` first and this second: the rows
  // the words match go up immediately and the ones meaning finds are added when the bytes land, which is
  // the same order a reader who types gets them in.
  if (state.q) semanticReady();
}).catch(err => {
  // A browser will not let a file:// page fetch a sibling file, so double-clicking index.html out of a
  // clone loads the chrome and then nothing at all, with the reason only in the console. Anyone doing
  // that is a contributor, so the message is the two commands that fix it rather than an apology.
  document.getElementById("count").innerHTML =
    "Could not load <code>data.json</code> — " + String(err);
  document.getElementById("out").innerHTML =
    '<p style="max-width:62ch;line-height:1.6">If you opened this file straight off disk, that is ' +
    'expected: browsers refuse to let a <code>file://</code> page read a sibling file. Serve the ' +
    'folder instead — <code>python -m http.server</code> from <code>docs/</code>, then open ' +
    '<code>localhost:8000</code>. The published copy is at ' +
    '<a href="__SITE__">__SITE__</a>.</p>';
});

// Before the fetch resolves, deliberately: none of this needs the data, and the theme toggle in
// particular should work on the error page as well as on the atlas.
wire();

// `icon` is the only optional part, and only the five Runs-on chips pass it: a topic and a harness have no
// mark, and both are names a reader has to be able to read anyway. Where it is passed, the mark replaces the
// word on screen and the word goes into a `.sr` span behind it -- because the label is the whole of a
// button's accessible name, and a chip that read "Windows" to a screen reader before it had a picture on it
// has to read "Windows" after. `aria-pressed` is untouched by either branch and still carries the state.
function chip(parent, label, pressed, onclick, title, icon) {
  const b = document.createElement("button");
  b.className = "chip";
  if (icon) b.innerHTML = icon + '<span class="sr">' + esc(label) + "</span>";
  else b.textContent = label;
  b.setAttribute("aria-pressed", pressed ? "true" : "false");
  if (title) b.title = title;
  b.onclick = onclick;
  parent.appendChild(b);
  return b;
}

function buildChips() {
  const cats = document.getElementById("cats"), tgts = document.getElementById("tgts"),
        oses = document.getElementById("oses");
  chip(cats, "All", true, () => set({cat: ""}));
  D.cats.forEach(c => chip(cats, c.name, false, () => set({cat: c.slug}), c.blurb));
  chip(tgts, "All", true, () => set({tgt: ""}));
  D.targets.forEach(t => chip(tgts, t.name, false, () => set({tgt: t.slug}), t.blurb));
  // The one chip group that shows a mark instead of its word. `OST` rather than the label for the hover,
  // because WSL2 is the entry whose mark and whose name are both opaque -- "WSL2" on a tooltip would only
  // repeat the abbreviation, so the module spells it out. The other four titles are just the platform.
  D.os.forEach((o, i) => chip(oses, o, false, () => {
    const os = state.os.includes(i) ? state.os.filter(x => x !== i) : state.os.concat(i);
    set({os});
  }, OST[i], osIcon(i)));
  // Debounced, because `render()` costs ~58ms at today's 1,294 rows on a throttled mobile CPU and used to
  // run once per keystroke -- so typing "agentic" rebuilt a 120-row table seven times and the input
  // visibly trailed the keyboard. Only ~20ms of that is row-count dependent; the rest is the innerHTML
  // rebuild and layout, so this is a defect at the current size and not only a future one. 150ms is short
  // enough to still read as live and collapses those seven renders into one.
  const qbox = document.getElementById("q");
  qbox.oninput = e => {
    const v = e.target.value;
    // Kicked off from here as well as from `focus`, because a reader who pasted a query or arrived on a
    // `#q=` link never focused anything, and one whose first keystroke was into an already-focused box
    // gets it from the other listener. `semanticReady` hands back the same promise after the first call,
    // so both paths firing costs one comparison.
    semanticReady();
    clearTimeout(typing);
    typing = setTimeout(() => set({q: v}, true), 150);
  };
  // The download starts on the intent to search rather than on the search: 758 KB has to race the reader's
  // first few keystrokes, and starting it when the query is complete would mean the first answer is the one
  // without meaning in it. `once` because there is nothing to do on the second focus.
  qbox.addEventListener("focus", semanticReady, {once: true});
  document.getElementById("sort").onchange = e => set({sort: e.target.value});
  // Unhidden here rather than in the markup -- see the button for why it starts hidden. The announcement is
  // on this path only: `applyView` also runs from `render()`, and the view the page opened in is not news. It is
  // needed at all because nothing in the DOM changes, so a screen reader has no mutation to report and the
  // button's own new label is not read back after a click.
  const vb = document.getElementById("view");
  vb.hidden = false;
  initDiscovery();
  vb.onclick = () => {
    state.view = state.view === "cards" ? "table" : "cards";
    writeHash();
    applyView();
    say(state.view === "cards"
      ? "Card view. Each project is a card with its screenshot."
      : "Table view.");
  };
  document.getElementById("strict").onclick = () => set({strict: !state.strict});
  // Shown only when it would select something. The label carries the count because the whole question
  // this chip answers is "is there anything new", and a reader should be able to see the answer without
  // clicking and then having to click back.
  const nb = document.getElementById("new");
  if (NEW) {
    nb.classList.add("on");
    document.getElementById("newlabel").textContent = "New · " + NEW.toLocaleString();
    // The date is on the chip's `title` rather than its label, because the label has to stay short enough to
    // sit on one line of the bar at 360px and the count is the part a reader scans for. Saying *which*
    // import is what stops "New · 7,412" reading as a claim about the last fortnight.
    nb.title = "The " + mmddyy(COHORT) + " import added these " + NEW.toLocaleString() +
      " projects to the atlas. The next import that brings anything replaces them.";
    nb.onclick = () => set({fresh: !state.fresh});
  }
  // Beside it, and painted here rather than in `render()` even though its count is per-reader: `SEEN_AT` is
  // read once at boot and never refreshed, so `SINCE` is settled by the time this runs and cannot change
  // while the page is open. That is what makes it a `buildChips` control and not a `render()` one -- unlike
  // Saved, whose set the reader edits by clicking things.
  const sb = document.getElementById("since");
  if (SINCE) {
    sb.classList.add("on");
    document.getElementById("sincelabel").textContent = "Since your last visit · " + SINCE.toLocaleString();
    sb.title = SINCE.toLocaleString() + " projects have been added since this device last opened the "
      + "atlas on " + mmddyy(SEEN_AT) + ".";
    sb.onclick = () => set({since: !state.since});
  }
  // Same shape as the chip above and the same reason for it: a control that selects zero of 1,294 rows is
  // worse than no control, and on the day the ledger starts that is exactly what this one would be. The
  // sort option leaves with it, because "Rising" ranking a column that is empty on every row is a menu
  // entry that silently does nothing -- and removing it takes it out of the palette too, which reads these
  // options live rather than keeping a second list.
  const rb = document.getElementById("rise"), sel = document.getElementById("sort"),
        ropt = [...sel.options].find(o => o.value === "rising");
  if (RISE && RISING) {
    rb.classList.add("on");
    rb.title = "Gained at least " + RISE.min_abs.toLocaleString() + " stars, and at least " +
      RISE.min_pct + "% of its own count, in the " + RISE.span + " days from " + RISE.from + " to " +
      D.velocity.to;
    document.getElementById("riselabel").textContent = "Rising · " + RISING.toLocaleString();
    rb.onclick = () => set({rising: !state.rising});
  } else if (ropt) {
    ropt.remove();
  }
  // Wired unconditionally, unlike the two chips above, because whether this one is *shown* is not a fact the
  // build knows: `paintSaved()` decides it on every render from the reader's own set. A handler on a hidden
  // button costs nothing; a hidden button that becomes visible with no handler is a dead control.
  document.getElementById("saved").onclick = () => set({saved: !state.saved});
  document.getElementById("clearsave").onclick = () => {
    const n = SAVED.size;
    SAVED.clear();
    storeSaved();
    // No confirm(). The button is only reachable while the saved filter is on, it says what it does, and the
    // announcement says what it did -- and a modal here would be the only one on the page. What makes that
    // defensible is that this is the *only* destructive control: Clear all drops the filter and leaves the
    // set alone, so nothing else a reader might mis-click can lose the collection.
    say(n ? "Removed all " + n + " saved projects." : "Nothing was saved.");
    // Through `set()` rather than `render()`, because `paintSaved()` is about to turn `state.saved` off under
    // an empty set and the hash has to lose `#saved=1` with it. `set()` is the path that writes the hash.
    set({saved: false});
  };
  document.getElementById("reset").onclick = () => set(CLEAR);
  sheetWire();
  window.addEventListener("hashchange", () => { readHash(); render(); });
  palWire();
  // Last, and here rather than in `wire()`, which is the argument `palWire` and `sheetWire` above it both make:
  // `wire()` also runs on the data.json error path, and every document this one offers is built out of rows.
  expWire();
  // After `expWire`, because the map's own neighbourhood button is behind the export flag -- see `mapPin` --
  // and before the first `render()`, so `mapRepaint` has a key to paint the moment anything is filtered.
  mapWire();
}

// The handle, the backdrop and the Done button. Wired from `buildChips` rather than from `wire()`, and this
// is the same argument `palWire` makes one function down, with more riding on it: `wire()` also runs on the
// data.json error page, and there the three facet rows have no chips in them yet. Putting `data-fb` on
// <html> is what switches the stylesheet's sheet form on at all, so doing it here means the sheet can only
// close over the filters once there are filters and a click handler to open it again with. If the fetch
// never resolves, the reader gets the bar the page had before this existed -- four rows, capped, scrollable
// -- instead of a button that does nothing in front of everything.
function sheetWire() {
  const fbt = document.getElementById("fbt"), sheet = document.getElementById("sheet");
  const root = document.documentElement;
  const shut = () => root.dataset.sheet !== "open";
  const show = on => {
    root.dataset.sheet = on ? "open" : "shut";
    fbt.setAttribute("aria-expanded", on ? "true" : "false");
    // Focus follows the sheet both ways. Without this a keyboard reader opens it and is still outside it,
    // then shuts it and lands on <body> -- which is the top of the document, above every control there is.
    //
    // The reflow is not superstition and it is not a `requestAnimationFrame` because it must not be async:
    // the sheet is `visibility:hidden` while shut, a hidden element cannot take focus, and the line above
    // has only changed an attribute -- the computed style behind it is still the old one until something
    // asks for layout. Measured: without this read `document.activeElement` stays on the handle. Reading
    // `offsetHeight` is the cheapest question that forces the recalculation, and it stays inside this one
    // event rather than deferring focus into a later frame the reader may already have typed into.
    if (on) { void sheet.offsetHeight; sheet.focus(); } else fbt.focus();
  };
  root.dataset.fb = "1";
  root.dataset.sheet = "shut";
  fbt.onclick = () => show(shut());
  document.getElementById("fbx").onclick = () => show(false);
  document.getElementById("fbb").onclick = () => show(false);
  // Esc, like everything else dismissible here. Deliberately not a focus trap and deliberately no
  // preventDefault: this is a disclosure rather than a modal, so Tab is allowed to walk out of it, and the
  // palette is a real <dialog> whose own Esc handling is the browser's -- so when that is open this stands
  // aside rather than closing two things on one key.
  document.addEventListener("keydown", ev => {
    const pal = document.getElementById("pal");
    if (ev.key === "Escape" && !shut() && !(pal && pal.open)) show(false);
  });
}

// Which filters live behind the handle, in the order the sheet lists them, as their own labels.
//
// Three of the seven are not here, and the omissions are the point rather than an oversight. `q` is the
// search box, which stays in the bar with the reader's own words still in it. New and Rising also stay in
// the bar, wearing the filled accent every pressed chip wears. All three are therefore already visible
// while the sheet is shut, and counting them would make the badge over-report what opening it would show:
// a reader who sees "1" and finds nothing selected has been told the wrong thing about the only control
// the number is attached to. So the badge answers exactly one question -- how many of the things behind
// this handle are on -- which is the question a shut sheet cannot otherwise answer.
function sheetFilters() {
  const on = [];
  // `find` rather than an index: `readHash` validates both slugs against the data before they reach state,
  // but a label is not worth a throw if that ever stops being true.
  const name = (list, slug) => (list.find(x => x.slug === slug) || {}).name;
  if (state.cat) on.push(name(D.cats, state.cat));
  if (state.tgt) on.push(name(D.targets, state.tgt));
  state.os.forEach(i => on.push(D.os[i]));
  if (state.strict) on.push("Confirmed only");
  return on.filter(Boolean);
}

// Called from `render()` and nowhere else, for the reason the chip reflection there gives: that is the one
// function every path which changes state already ends at, so a chip, a hashchange, the back button and a
// shared link all repaint this without each of them remembering to.
function paintSheet(countHTML) {
  const on = sheetFilters(), n = on.length;
  const fbt = document.getElementById("fbt");
  document.getElementById("fbn").textContent = n ? String(n) : "";
  fbt.classList.toggle("act", n > 0);
  // "Filters" first and always, so the accessible name still contains the visible label -- WCAG 2.5.3, and
  // the word a voice-control user has to be able to say to press it. The names follow the count because
  // "3 selected" is the glanceable part and the list is the confirmation.
  fbt.setAttribute("aria-label", n
    ? "Filters — " + n + " selected: " + on.join(", ")
    : "Filters — none selected");
  document.getElementById("shtitle").textContent = n ? "Filters · " + n : "Filters";
  document.getElementById("scount").innerHTML = countHTML;
}

// Wired from `buildChips` rather than from `wire()`, because `wire()` also runs on the data.json error
// page: there the palette would have no topics or platforms to offer, so the shortcut and its hint stay
// absent instead of opening an empty box.
function palWire() {
  const dlg = document.getElementById("pal"), q = document.getElementById("palq"),
        list = document.getElementById("palist"), hint = document.getElementById("palhint");
  if (!dlg || !dlg.showModal) return;

  hint.classList.add("on");
  hint.innerHTML = "<kbd>" + esc(PALMOD) + "</kbd><kbd>K</kbd><span>Jump to&hellip;</span>";
  hint.title = "Jump to any topic, platform, sort or project (" + PALMOD + " K)";
  hint.onclick = palOpen;

  document.addEventListener("keydown", ev => {
    // Either modifier, so the shortcut works on a Mac keyboard plugged into anything and on a browser
    // whose platform string lies. Not with Alt held, which is a different chord on several layouts.
    if ((ev.ctrlKey || ev.metaKey) && !ev.altKey && (ev.key === "k" || ev.key === "K")) {
      ev.preventDefault();
      if (dlg.open) dlg.close(); else palOpen();
      return;
    }
    // `/` is the other convention for this, but only where it would not otherwise be a literal slash --
    // stealing the key while someone is typing a path into the search box would be a bug, not a shortcut.
    const t = ev.target && ev.target.tagName || "";
    if (ev.key === "/" && !dlg.open && !/^(INPUT|TEXTAREA|SELECT)$/.test(t) &&
        !(ev.target && ev.target.isContentEditable)) {
      ev.preventDefault();
      palOpen();
    }
  });

  q.oninput = () => { PALI = 0; palRender(); };
  q.onkeydown = ev => {
    const jump = {ArrowDown: 1, ArrowUp: -1}[ev.key];
    if (jump) { ev.preventDefault(); palMove(jump); return; }
    if (ev.key === "Enter") { ev.preventDefault(); palPick(); return; }
    if (ev.key === "Home") { ev.preventDefault(); PALI = 0; palRender(); return; }
    if (ev.key === "End") { ev.preventDefault(); PALI = PAL.length - 1; palRender(); }
  };
  // Delegated: `palRender` replaces the whole list on every keystroke, so per-row handlers would be
  // forty attachments discarded on each one.
  list.addEventListener("click", ev => {
    const li = ev.target.closest("li.it");
    if (!li) return;
    PALI = [...list.querySelectorAll("li.it")].indexOf(li);
    palPick();
  });
  // Clicking the backdrop is the other way people dismiss a modal, and <dialog> fires no event for it --
  // the click lands on the dialog element itself, because the padding is zero and every child is inside
  // one of the three panels.
  dlg.addEventListener("click", ev => { if (ev.target === dlg) dlg.close(); });
}

// `saved` is in here, so Clear all drops the saved *filter* along with every other one. It does not empty
// the saved set: Clear all is next to the search box and means "show me everything again", and a control
// that also deleted a reader's collection would be the worst button on the page. Removing the collection is
// `#clearsave`, which only exists while the reader is looking at it.
//
// `list` is in here too, and that one is a real trade rather than an obvious inclusion. A shared list cannot
// be reconstructed by clicking a chip the way every other filter here can, and `replaceState` leaves no
// history entry to go back to -- so Clear all genuinely loses it. It is in anyway, because the alternative is
// worse: a reader on a shared link who presses "Clear all filters" and still sees twelve of 1,294 rows has
// been told something untrue by a button, and that is the failure that makes a page feel broken. What makes
// it survivable is the strip above the results, whose *first* control saves the list to the reader's own
// projects -- the durable copy is one press away, and it is the press the strip leads with.
//
// The two collection values are shared references, like `os` above them, and safe for the same reason: every
// patch on this page replaces them wholesale and nothing mutates one in place.
const CLEAR = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false, since: false, rising: false,
               saved: false, list: new Set()};

// ---- Command palette -------------------------------------------------------------------------------
//
// Every filter on this page is a pill in one of four rows, and the two facet rows are the long ones:
// thirteen topics and twelve integrations. Reaching "Sandbox & security" means reading thirteen pills to
// find it, and the sort menu is a fifth control in a fifth place. The palette collapses all of that into
// one thing to learn -- type three letters, press Enter -- which is the difference between a page you
// operate and a page you skim.
//
// `<dialog>` and `showModal()`, not a hand-rolled overlay: the focus trap, the Esc handler, the backdrop,
// the inertness of the page behind it and the return of focus to whatever opened it are all native, and
// all of them are things a hand-rolled overlay gets wrong. Where `showModal` is missing the shortcut is
// never wired at all and the hint stays hidden -- an accelerator that half-opens is worse than an absent
// one, and nothing on this page is reachable *only* through the palette.
let PAL = [], PALI = 0;

// `navigator.platform` is deprecated and still the only thing that answers this question in every engine.
// Getting it wrong prints the wrong glyph in a hint; it does not break the shortcut, which listens for
// either modifier regardless.
const PALMOD = /mac|iphone|ipad/i.test((navigator.platform || "") + (navigator.userAgent || ""))
  ? "⌘" : "Ctrl";

function palItems(query) {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  const acts = [];
  const add = (group, label, active, run) => acts.push({group, label, active, run});

  D.cats.forEach(c => add("Topic", c.name, state.cat === c.slug, () => set({cat: c.slug})));
  D.targets.forEach(t => add("Plugs into", t.name, state.tgt === t.slug, () => set({tgt: t.slug})));
  D.os.forEach((o, i) => add("Runs on", o, state.os.includes(i), () => set({
    os: state.os.includes(i) ? state.os.filter(x => x !== i) : state.os.concat(i),
  })));
  // Read straight off the <select>, so a sort mode added there shows up here without a second list to
  // remember to update -- and the palette can never offer a sort `SORTS` does not implement.
  for (const o of document.getElementById("sort").options)
    add("Sort", o.text, state.sort === o.value, () => {
      document.getElementById("sort").value = o.value;
      set({sort: o.value});
    });
  // Same condition the chip itself uses: with nothing inside the window this filter selects zero rows.
  if (NEW) add("Filter", "New arrivals", state.fresh, () => set({fresh: !state.fresh}));
  if (SINCE) add("Filter", "Added since your last visit", state.since,
                 () => set({since: !state.since}));
  // Same condition the chip itself uses, for the same reason.
  if (RISE && RISING) add("Filter", "Rising", state.rising, () => set({rising: !state.rising}));
  add("Filter", "Confirmed platform support only", state.strict, () => set({strict: !state.strict}));
  // Guarded on the set being non-empty for the same reason "New arrivals" is guarded on `NEW` -- an entry
  // that selects nothing is an entry that makes the palette look broken. The difference is that this one is
  // decided per keystroke rather than per build, which costs nothing: `palRender` already rebuilds the list
  // on every keystroke, so it reads the current size for free.
  if (SAVED.size) add("Filter", "Saved (" + SAVED.size + ")", state.saved, () => set({saved: !state.saved}));
  add("Filter", "Clear all filters", false, () => set(CLEAR));
  // Delegated to the real button rather than duplicating its body, so the label, the title and the
  // localStorage write stay in exactly one place.
  add("Page", (document.documentElement.dataset.theme === "light" ? "Dark" : "Light") + " theme", false,
    () => document.getElementById("theme").click());
  // Same delegation, same reason: the label, the title, the hash write and the announcement stay in the one
  // place that owns them. The label is the action, matching the button, so the palette never offers "Card
  // view" to someone already in it.
  add("Page", state.view === "cards" ? "Table view" : "Card view", false,
    () => document.getElementById("view").click());
  // Same delegation again, and gated on the chip actually being on the bar rather than on the flag alone: the
  // chip is hidden where `<dialog>` cannot be opened modally, and an entry that opens nothing is the one thing
  // that makes a palette look broken.
  if (FLAGS["index.export"] && document.getElementById("take").classList.contains("on"))
    add("Page", "Export this view", false, () => document.getElementById("take").click());

  // Substring, not the trigram scorer the search box falls back on. These are forty-odd labels the reader
  // can see in full, so "sand" finding "Sandbox & security" is the entire requirement; near-misses here
  // would only push the exact thing they typed further down the list. Earlier match wins, so "new" ranks
  // "New arrivals" above a topic that merely contains the word.
  const score = a => {
    const l = a.label.toLowerCase();
    let s = 0;
    for (const w of words) {
      const i = l.indexOf(w);
      if (i < 0) return -1;
      s += i === 0 ? 2 : 1;
    }
    return s;
  };
  // Grouped, then ordered by each group's best member -- not a flat sort by score. A flat sort interleaves
  // groups, so "a" produced Topic, Plugs into, then Topic again, and a heading printed twice reads as a
  // rendering fault rather than as a ranking. This keeps every heading unique *and* keeps the globally best
  // match first, because the best item's own group necessarily sorts first. Ties fall back to the order the
  // controls appear in the filter bar, which is the order the reader already knows.
  const gorder = [...new Set(acts.map(a => a.group))];
  const ranked = words.length ? (() => {
    const hits = acts.map(a => ({a, s: score(a)})).filter(x => x.s >= 0);
    const best = new Map();
    for (const x of hits) if (!(best.get(x.a.group) >= x.s)) best.set(x.a.group, x.s);
    return hits.sort((p, r) => best.get(r.a.group) - best.get(p.a.group) ||
      gorder.indexOf(p.a.group) - gorder.indexOf(r.a.group) || r.s - p.s).map(x => x.a);
  })() : acts;

  // Projects appear only once there is something to look for. With an empty box the palette is a menu of
  // the page's own controls, which is what it is for; listing 1,294 repositories there would bury them.
  // The same relevance scorer the results table uses, so the palette cannot disagree with the page about
  // what the best match for a word is.
  //
  // With the semantic term explicitly zero, which is the one place the two deliberately differ. The palette
  // is a keyboard shortcut to a project whose name the reader is part-way through typing -- it answers
  // "take me to the thing I mean", and eight rows found by resemblance rather than by the letters on screen
  // would be eight chances to press Enter on the wrong repository. The table, which the reader reads before
  // clicking anything, is where meaning belongs.
  let proj = [];
  if (words.length) {
    proj = ROWS.filter(r => words.every(w => r.hay.includes(w)));
    for (const r of proj) r.rel = relevance(r, words, 0);
    proj = proj.sort(SORTS.relevance).slice(0, 8).map(r => ({
      group: "Projects", label: r.name, hint: r.nwo, stars: r.stars,
      // Same-tab, like the name links in the table. A palette that opened tabs when the table does not
      // would be the one control on the page that behaves differently from its neighbours.
      run: () => { location.href = r.url; },
    }));
  }
  return ranked.slice(0, words.length ? 8 : 40).concat(proj);
}

function palRender() {
  const box = document.getElementById("palist"), q = document.getElementById("palq");
  PAL = palItems(q.value);
  if (PALI >= PAL.length) PALI = Math.max(0, PAL.length - 1);
  if (!PAL.length) {
    box.innerHTML = '<li class="palnone" role="presentation">Nothing here matches that.</li>';
    q.removeAttribute("aria-activedescendant");
    return;
  }
  let html = "", last = "";
  PAL.forEach((a, i) => {
    if (a.group !== last) {
      html += '<li class="grp" role="presentation">' + esc(a.group) + "</li>";
      last = a.group;
    }
    html += '<li class="it" role="option" id="pal-' + i + '" aria-selected="' + (i === PALI) + '">' +
      '<span class="t">' + esc(a.label) + "</span>" +
      (a.stars ? '<span class="s">' + a.stars.toLocaleString() + "★</span>" : "") +
      // "on" rather than a tick, because this is read aloud as part of the option's name: "Windows, on".
      (a.active ? '<span class="k">on</span>' : a.hint ? '<span class="k">' + esc(a.hint) + "</span>" : "") +
      "</li>";
  });
  box.innerHTML = html;
  q.setAttribute("aria-activedescendant", "pal-" + PALI);
  // `nearest`, so arrowing down inside the visible list does not scroll at all and only the row that
  // just left the viewport pulls it.
  const sel = box.querySelector("[aria-selected=true]");
  if (sel && sel.scrollIntoView) sel.scrollIntoView({block: "nearest"});
}

// Wrapping, because a list this long is faster to reach from the bottom for the last few entries and
// there is no submit-on-last-item semantics to protect.
function palMove(d) {
  if (!PAL.length) return;
  PALI = (PALI + d + PAL.length) % PAL.length;
  palRender();
}

function palPick() {
  const a = PAL[PALI];
  if (!a) return;
  // Close before running. `set()` re-renders the table underneath, and a modal still on screen over a
  // table that has already changed reads as if the keystroke did nothing.
  document.getElementById("pal").close();
  a.run();
}

function palOpen() {
  const dlg = document.getElementById("pal");
  // `D` guards the error page: the palette's topic and platform lists come out of the data, so before it
  // lands there is nothing to jump to.
  if (!dlg || !dlg.showModal || dlg.open || !D) return;
  document.getElementById("palq").value = "";
  PALI = 0;
  dlg.showModal();
  palRender();
  document.getElementById("palq").focus();
}

// Theme and clipboard are wired outside buildChips because buildChips only runs once `data.json` has
// arrived. When the fetch fails -- a contributor opening the file off disk, which the catch block above
// exists for -- the toggle used to be dead too, so the error page could not be read in light mode.
function wire() {
  // First thing, and the ordering is load-bearing rather than tidy. `readHash()` decides whether to honour a
  // `#saved=1` link by asking whether the set is empty, and it runs after this -- so reading the set later
  // would make a reader's own bookmark of their saved view open unfiltered on the first visit of every
  // session, and work on the second. This is also the only synchronous storage read on the boot path besides
  // the theme, and it is one small key: the rows are waiting on a 556 KB fetch either way.
  loadSaved();
  // Beside it and for a related reason: this has to be read before `prepare()` computes `r.issince`, and
  // `prepare()` runs off the `data.json` fetch while this runs synchronously at boot. One more small key on
  // a path already waiting on a 556 KB body.
  loadVisit();
  const btn = document.getElementById("theme");
  const label = () => {
    const light = document.documentElement.dataset.theme === "light";
    btn.textContent = light ? "Dark theme" : "Light theme";
    btn.title = "Switch to the " + (light ? "dark" : "light") + " theme";
    // Read off the stylesheet rather than restated here, so --plane and the browser chrome cannot drift.
    // Folded into label() because label() is the one function every path that changes the theme already
    // calls -- the toggle, the OS-preference listener, and the initial agreement with the head script.
    const plane = getComputedStyle(document.documentElement).getPropertyValue("--plane").trim();
    if (plane) document.getElementById("tc").content = plane;
    paintDeployBadge();
  };
  btn.onclick = () => {
    const light = document.documentElement.dataset.theme !== "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    // The choice is the point: it used to last until the next navigation, so a reader who needs light
    // re-picked it on every page load and every shared filter link.
    try { localStorage.setItem("theme", light ? "light" : "dark"); } catch (e) {}
    label();
  };
  // The head script already resolved the theme; this only has to agree with it, since the markup's
  // hardcoded "Light theme" is wrong half the time now that the OS preference is honoured.
  label();
  // Follow the OS live, but only for a reader who has not overridden it -- flipping someone out of a
  // theme they explicitly chose because the sun went down is worse than not following at all.
  try {
    matchMedia("(prefers-color-scheme: light)").addEventListener("change", ev => {
      if (localStorage.getItem("theme")) return;
      document.documentElement.dataset.theme = ev.matches ? "light" : "dark";
      label();
    });
  } catch (e) {}

  // One delegated listener rather than one per button: `render()` replaces the whole subtree on every
  // keystroke, so per-row handlers would be 120 attachments discarded 120 times a second of typing.
  document.getElementById("out").addEventListener("click", ev => {
    const fix = ev.target.closest(".fix");
    if (fix) {
      if (fix.dataset.all) return set(CLEAR);
      const o = RESCUE[+fix.dataset.i];
      if (o) set(o.patch);
      return;
    }
    const sv = ev.target.closest(".save");
    if (sv) return toggleSave(sv);
    const pn = ev.target.closest(".pin");
    if (pn) return togglePin(pn);
    const b = ev.target.closest(".copy");
    if (b) copy(b);
  });
  // The comparison's own two controls, wired here beside the results' delegated listener rather than in
  // `expWire()`, because unlike the export these are not behind a `<dialog>` the browser may not have. Both are
  // static markup, so one listener each and no delegation: the panel's *contents* are rebuilt on every render,
  // but this header is not.
  //
  // The chip only ever toggles the panel. It does not clear the pins and it does not pin anything, which is
  // what `aria-expanded` on it promises -- a disclosure that also destroyed a selection would be a control that
  // lied about itself. `render()` and not `set()`, for the reason `togglePin` gives at length: nothing about the
  // *view* changed, so the hash is still right and the reader should not be sent back to row 1.
  document.getElementById("cmpchip").onclick = () => { CMP_OPEN = !CMP_OPEN; render(); };
  document.getElementById("cmpclear").onclick = () => {
    const n = state.cmp.size;
    state.cmp = new Set();
    writeHash();
    say(n ? "Comparison cleared." : "Nothing was pinned.");
    render();
  };
  // Delegated, because these live in the header row the panel rebuilds on every keystroke -- the same argument
  // the results listener above makes, for the same reason. The listener is on `#cmptable`, which is static.
  document.getElementById("cmptable").addEventListener("click", ev => {
    const u = ev.target.closest(".unpin");
    if (!u) return;
    const r = BY_NWO.get(u.dataset.nwo);
    state.cmp.delete(u.dataset.nwo);
    writeHash();
    say("Took " + (r ? r.name : u.dataset.nwo) + " out of the comparison. " + state.cmp.size + " pinned.");
    render();
  });
  stamp();
  // With no argument, so the badge shows `BUILT` and gets its relative age and tooltip immediately. The
  // fetch calls it again with the header when it lands, which is the only time the value changes. Wired
  // here rather than only there because `wire()` also runs on the error page, where the fetch never
  // resolves and a badge frozen at its rendered-in markup would have no age on it at all.
  deployStamp();
}

// Save or un-save one project.
//
// Deliberately not routed through `set()`, which every other control on this page uses. `set()` resets
// `state.shown` to the first page, and it should: changing a filter changes what the table is *of*, so
// starting again at row 1 is right. Saving a project changes nothing about what the table is of -- a reader
// forty rows into a topic who saves one would be thrown back to row 1 by the very control that was supposed
// to help them keep it. So this writes the set, then does the smallest repaint that is still correct.
//
// Which repaint that is depends on the filter. With `state.saved` on, the row this button lives in has just
// stopped or started matching, so the table genuinely has to be rebuilt and a full `render()` is the honest
// answer -- the reader is looking at a list defined by this button, and it has to change under them. With the
// filter off, nothing about which rows match has changed, so rebuilding 120 rows to repaint one button would
// also discard the button the reader just pressed and drop focus to <body>. Hence the in-place update, which
// is the same reason `copy()` above flashes its own label instead of re-rendering.
function toggleSave(b) {
  const nwo = b.dataset.nwo, name = b.dataset.name;
  const on = !SAVED.has(nwo);
  if (on) SAVED.add(nwo); else SAVED.delete(nwo);
  storeSaved();
  say(on ? "Saved " + name + ". " + SAVED.size + " saved."
         : "Removed " + name + " from saved. " + SAVED.size + " saved.");
  if (state.saved) return render();
  b.setAttribute("aria-pressed", on ? "true" : "false");
  b.setAttribute("aria-label", saveLabel(name, on));
  b.textContent = saveWord(on);
  paintSaved();
}

// Pin or unpin one project for the comparison.
//
// Not routed through `set()`, and the argument is `toggleSave`'s word for word: `set()` resets `state.shown`,
// which is right when a filter changes and wrong here. Pinning the fourth project is exactly what a reader
// forty rows into a topic does, and being thrown back to row 1 by the control meant to help them keep their
// place is the defect. So this writes the set, writes the hash -- which `toggleSave` does not have to do,
// because `SAVED` is not in the URL and this is -- and repaints.
//
// The repaint is a full `render()`, where `toggleSave` goes out of its way to avoid one. The difference is real:
// crossing the cap changes the `disabled` state of the ~1,290 buttons that are *not* pinned, and there is no
// honest way to update one button and leave the others lying about whether they will work. `toggleSave`'s
// in-place path exists because saving row 40 changes nothing about row 41.
//
// Which leaves the cost `toggleSave` was avoiding -- `render()` replaces the subtree, so the button the reader
// just pressed is gone and focus falls to <body>. That is unacceptable for a control whose whole job is to be
// pressed three or four times in a row, so the equivalent button is found in the new subtree and refocused.
// Matched on `dataset.nwo` rather than through a CSS selector, because an `owner/name` is not a valid selector
// fragment and `CSS.escape` is one more thing to be wrong about a string that came out of somebody's README.
function togglePin(b) {
  const nwo = b.dataset.nwo, name = b.dataset.name;
  const on = !state.cmp.has(nwo);
  // Reached only by a hand-driven click on a button this page drew as disabled -- a `disabled` attribute is
  // enforced by the browser -- so this is the guard for the DOM being edited underneath us rather than a path
  // the UI can take. It says the cap out loud anyway: a silent no-op on a press is the worst of the three.
  if (on && state.cmp.size >= CMP_MAX) {
    say("The comparison already holds " + CMP_MAX + " projects. Take one out to add " + name + ".");
    return;
  }
  if (on) state.cmp.add(nwo); else state.cmp.delete(nwo);
  // Re-opened on a pin and never on an unpin. A reader who shut the panel and then pinned a fifth thing has
  // asked to see the comparison; one who is taking projects out of it has not asked for it to reappear.
  if (on) CMP_OPEN = true;
  writeHash();
  say(on ? "Comparing " + name + ". " + state.cmp.size + " of " + CMP_MAX + " pinned."
         : "Took " + name + " out of the comparison. " + state.cmp.size + " pinned.");
  render();
  const again = [...document.querySelectorAll("#out .pin")].find(x => x.dataset.nwo === nwo);
  if (again) again.focus();
}

// writeText rejects rather than throws -- denied permission, a document that is not focused, an
// http origin -- so the failure path has to be real. Selecting the command is the fallback that leaves
// the reader one keystroke from the same result, which is better than a button that shrugs.
function copy(b) {
  const cmd = b.dataset.cmd;
  const flash = (text, ok) => {
    b.textContent = text;
    b.classList.toggle("ok", !!ok);
    setTimeout(() => { b.textContent = "Copy"; b.classList.remove("ok"); }, 1800);
  };
  navigator.clipboard.writeText(cmd).then(() => {
    flash("Copied", true);
    say("Copied " + cmd);
  }, () => {
    const code = b.parentNode.querySelector(".cmd");
    if (code) {
      const r = document.createRange();
      r.selectNodeContents(code);
      const s = getSelection();
      s.removeAllRanges();
      s.addRange(r);
    }
    flash("Ctrl+C");
    say("The clipboard was refused. The command is selected — press Control C to copy it.");
  });
}

// An ISO date answers "when" and not "is this current", which is the question -- but the "last deployed"
// badge in this same header now answers it, so spelling out "3 days ago" here as well was two answers to
// one question and the header's third date in a row. Amber past a fortnight because that is the point at
// which the star counts on the page have measurably drifted from GitHub's, and the only point at which
// the age says something the date and the badge together do not.
//
// The date comes out of the data and not out of this document, which is the whole of JFH-207. Offline the
// two halves of the page arrive from two caches -- the shell from `atlas-shell-<version>`, `data.json` from
// `atlas-data` -- and nothing reconciles them, so a stamp baked into the document describes the document
// and not the rows a reader is looking at. Three rungs, in order of how well each one knows the answer:
//
//   D.generated  the instant the rows were captured, written beside them by `build_data`. Travels with the
//                body, so it is right however old the body in the cache turns out to be.
//   D.snapshot   the same fact to the day, and it is in every `data.json` this site has ever published --
//                which is what makes this correct for the bodies already sitting in readers' caches and
//                not only for ones built after this shipped.
//   SNAPSHOT     the document's own copy: all there is before the fetch resolves, and all there is if it
//                never does. Deliberately not `BUILT`, which the "last deployed" badge owns: that is when
//                this copy was *published*, a different fact and always the later one -- the committed page
//                routinely carries a `BUILT` several days after its own `SNAPSHOT` -- so falling back to it
//                would overstate how fresh the data is by however far the two have drifted, which is the
//                failure this function is being fixed for rather than a fallback from it.
function stamp() {
  const el = document.getElementById("snap");
  if (!el) return;
  // Tested rather than trusted. A missing key would `slice` the string "undefined" and print it under a
  // "NaN days old", so anything that is not an ISO date drops to the next rung instead of being rendered.
  const own = String((D && (D.generated || D.snapshot)) || "").slice(0, 10);
  const day = /^\d{4}-\d{2}-\d{2}$/.test(own) ? own : SNAPSHOT;
  const d = daysAgo(day);
  // Just the date while the build is keeping up. The relative age is appended only past the fortnight,
  // where it stops being a restatement of "current" and becomes the one thing the reader needs to know.
  //
  // "offline, showing data from" rather than a warning, when these rows came from the cache: the reader
  // asked for a page with no network and got the whole atlas, which is the feature working. What they are
  // owed is the date it is true as of, and no alarm.
  el.innerHTML = (FROM_CACHE ? "offline, showing data from " : "snapshot ") + day +
    (d > 14 ? ' · <span class="stale">' + d + " days old</span>" : "");
  el.title = (FROM_CACHE
      ? "The network did not answer, so these rows came from your browser's cache. " : "") +
    (d > 14
      ? "The daily rebuild has not run in " + d + " days, so stars and push dates here have drifted."
      : "Rebuilt daily from the GitHub API.");
}

// The badge under the masthead. Two sources for one value, in order of authority.
//
// `Last-Modified` on the `data.json` response is the real answer. Pages stamps every file it serves with
// the moment the deployment carrying it was published -- `index.html` and `data.json` come back with the
// same second, which is what proves it is the deployment's clock and not any file's own mtime -- so this
// is the publish time of the exact bytes on screen, and it is free, because the page fetches that file
// regardless. It is also the only value that *can* be right: the commit carrying this page is what
// triggers the deployment that publishes it, so nothing known at build time could have said it.
//
// `BUILT` is the fallback, and the reason the badge is never blank or wrong-looking: it is what the copy
// in the repository shows, what a local `python -m http.server` shows, where there is no deployment to
// describe, and what is on screen for the few hundred milliseconds before the fetch resolves. It runs a
// minute or two ahead of the deployment it precedes, which is inside the minute the badge prints.
//
// Nothing in here may throw. The caller is the first link of the `data.json` promise chain, and an
// exception raised here would land in the `.catch` at the end of it and be reported to the reader as
// "could not load data.json" -- a badge failing would blank the atlas and misattribute why.
function deployStamp(lastModified) {
  try {
    const el = document.getElementById("deployed");
    if (!el) return;
    const live = Date.parse(lastModified || "");
    const ms = Number.isNaN(live) ? Date.parse(BUILT) : live;
    if (Number.isNaN(ms)) return;
    const iso = new Date(ms).toISOString();
    const shown = iso.slice(0, 10) + " " + iso.slice(11, 16) + " UTC";
    const t = el.querySelector("time");
    t.dateTime = iso;
    t.textContent = "Last deployed " + shown;
    // The same fortnight `stamp()` uses, deliberately -- one staleness threshold in the header rather than
    // two to learn. It is the right number for this clock too: the daily build is gated on a source list
    // having moved, so a quiet week is healthy and a tighter bound would cry wolf, but the weekly rebuild
    // publishes unconditionally, so past 14 days both crons have stopped and the page is on its own.
    const days = (Date.now() - ms) / 86400000;
    el.classList.toggle("late", days > 14);
    paintDeployBadge();
    const age = days < 1 ? "Today." : days < 2 ? "Yesterday." : Math.round(days) + " days ago.";
    el.title = (Number.isNaN(live)
      ? "Built " + shown + ". This copy is not served by Pages, so its deployment time is unknown. "
      : "Published to GitHub Pages " + shown + ". ") + age
      + (days > 14 ? " Neither scheduled rebuild has run since, so the data here has drifted." : "");
  } catch (e) {}
}

function paintDeployBadge() {
  try {
    const el = document.getElementById("deployed");
    if (!el) return;
    const img = el.querySelector("img");
    const t = el.querySelector("time");
    if (!img || !t) return;
    const shown = t.textContent.replace(/^Last deployed\s+/, "");
    const message = shown.replace(/_/g, "__").replace(/-/g, "--").replace(/ /g, "_");
    const mode = document.documentElement.dataset.theme === "light" ? "light" : "dark";
    const colour = el.classList.contains("late") ? (mode === "light" ? "875A19" : "EF7D86") : "187557";
    img.src = "https://shieldcn.dev/badge/last_deployed-" + message + "-" + colour
      + ".svg?logo=ri%3ALuClock3&size=xs&font=geist&split=true&mode=" + mode;
  } catch (e) {}
}

// The view is the one thing in `state` that no row depends on: both views are the same table, so changing
// it changes no cell, no order, no count and no row's place in it. Two consequences, and they are the
// design.
//
// It deliberately does not go through `set()`. That function resets `shown` to the first page, which is
// right for a filter -- a new result set has no page 5 -- and wrong here, where a reader who asked for 600
// rows and then wants to see their screenshots should not silently lose 480 of them.
//
// And it does not render. The attribute lands on <html>, the stylesheet reads it, and that is the whole
// switch: no fetch, no re-sort, no innerHTML, not one row object touched. What that is worth, measured
// rather than assumed, at 120 cards on a desktop with both layout modes already warm: the switch is 38ms
// against 48ms for the same change made by re-rendering. Both are dominated by one unavoidable relayout --
// a table and a grid of cards are different enough that the browser starts over either way -- so the saving
// is the innerHTML rebuild and the parse of it, and it is 20% rather than an order of magnitude. The reason
// to do it this way is the part that is not a number: the DOM survives, so the reader keeps their scroll
// position and their focus, and `shown` below keeps the rows they asked for.
function applyView() {
  document.documentElement.dataset.view = state.view;
  const dc = document.getElementById("density-control");
  if (dc) dc.hidden = state.view === "cards";
  const btn = document.getElementById("view");
  if (!btn) return;
  const cards = state.view === "cards";
  btn.textContent = cards ? "Table view" : "Card view";
  btn.title = cards
    ? "Back to the table, which fits far more rows on a screen"
    : "Show each project as a card, with its screenshot";
}

// A stable small palette gives each card its own edge without turning the atlas into a lottery on every
// render. The repository name is already the durable identifier used by Save and shared lists, so hashing
// it makes the colour survive a sort, search, reload, and a future data refresh.
function projectAccent(nwo) {
  let h = 2166136261;
  for (let i = 0; i < nwo.length; i++) h = Math.imul(h ^ nwo.charCodeAt(i), 16777619);
  return ["sky", "mint", "gold", "coral", "violet"][(h >>> 0) % 5];
}

// View and row density are intentionally separate preferences. A shared URL says which projects someone
// meant to show; forcing its recipient to inherit the sender's amount of surrounding prose is not useful.
const DENSITY_KEY = "atlas-table-density";
const DENSITIES = new Set(["compact", "normal", "expanded"]);

function applyDensity(value) {
  const density = DENSITIES.has(value) ? value : "normal";
  document.documentElement.dataset.density = density;
  const select = document.getElementById("density");
  if (select) select.value = density;
  return density;
}

function initDiscovery() {
  const density = document.getElementById("density");
  let stored = "normal";
  try { stored = localStorage.getItem(DENSITY_KEY) || "normal"; } catch (e) {}
  applyDensity(stored);
  if (density) density.onchange = () => {
    const next = applyDensity(density.value);
    try { localStorage.setItem(DENSITY_KEY, next); } catch (e) {}
    say(next[0].toUpperCase() + next.slice(1) + " table rows.");
  };

  // Commentary is an optional layer, not a prerequisite for the mascot. With its release flag off, Archie
  // remains a named bit of the masthead and no hover, speech, stored preference, or Easter egg code
  // runs. That keeps a one-key rollback genuinely quiet.
  const enabled = !!FLAGS["index.mascot_commentary"];
  const tip = document.getElementById("byte-tip"), name = document.getElementById("byte-name"),
        quiet = document.getElementById("byte-quiet"), speech = document.getElementById("byte-speech"),
        wrap = document.querySelector(".atlas-byte-wrap"), out = document.getElementById("out");
  if (!enabled) {
    if (quiet) quiet.hidden = true;
    if (speech) speech.hidden = true;
    return;
  }
  let muted = false, timer = 0, last = null, clicks = [];
  try { muted = localStorage.getItem("atlas-byte-quiet") === "1"; } catch (e) {}
  const setQuiet = on => {
    muted = on;
    if (quiet) {
      quiet.setAttribute("aria-pressed", on ? "true" : "false");
      quiet.textContent = on ? "Commentary off" : "Quiet mode";
    }
    if (on && speech) speech.hidden = true;
    try { localStorage.setItem("atlas-byte-quiet", on ? "1" : "0"); } catch (e) {}
  };
  // TWO LINES, MEASURED -- NOT A PARAGRAPH. `r.blurb` used to be appended here, and it is the upstream
  // repository description passed straight through, so the height of the bubble was set by whatever an
  // unrelated project wrote in its GitHub "about" field.
  //
  // A character cap alone does not buy a line count, which is the thing that actually covered the masthead:
  // the box is 220px at 12px/1.38, so it fits about 34 characters a line, but a project name is one
  // unbreakable run of up to 67 characters and a category like "Orchestrators & Multi-Agent" is another 27.
  // Every one of the 3,837 strings these templates can produce for the 1,294 committed rows was rendered
  // into this box and its line count read back; a 140-character cap reached four lines and even 72 reached
  // three.
  //
  // THERE IS ONE CAP AND NOT TWO, AND THE PAIR THIS REPLACES WAS A TRAP RATHER THAN A BELT AND BRACES. It
  // was `TAG_MAX = 62, BUBBLE_MAX = 74`: add the tag only if the sentence plus tag fits 62, then clip the
  // result to 74. Read as written, 74 is the guarantee and 62 is a nicety. It is the other way round. 74 was
  // only reachable *because* 62 suppressed every string between 63 and 74 that had a tag on it, so the
  // longest thing the page could actually say was well under its own stated cap, and the number a reader of
  // this code would check the layout against was not the number holding it up.
  //
  // 74 never bound anything, and it missed by exactly one character rather than by a comfortable margin,
  // which is the part worth writing down: the worst tagged sentence the old pair could construct was a
  // 26-character clipped name, plus the 17 characters of " is listed under ", plus the longest of the 14
  // category names -- "Sandbox, Security & Governance", 30 -- plus a full stop. 26+17+30+1 = 74, equal to the
  // cap and therefore passing it. So the guard was live and merely never fired, and renaming one category to
  // 31 characters would have started it clipping, silently, with no test anywhere measuring the string it
  // clipped. Do not read the old pair as a cap that was redundant by design. Raising TAG_MAX to meet
  // BUBBLE_MAX -- which looks like a pure win, more tags kept, same stated bound -- takes the bubble to
  // three lines immediately. Measured: at 220px, `24,65,65` is three lines where `24,53,65` is two.
  //
  // So `SAY_MAX` is both tests at once: the tag goes on only if the whole sentence still fits it, and the
  // sentence is clipped to it. The longest string this page can produce is then exactly SAY_MAX code points,
  // which is a bound that can be checked by reading one number. At 220px, 53 is the largest SAY_MAX that
  // held two lines for all 3,837, on two independent instruments that agreed on every one of them (one
  // client rect per line box from a Range, and box height over lineHeight).
  //
  // WHAT THE NARROWER BOX COSTS, because it is not free and the cost is in the copy rather than the layout.
  // At 74 the tag survived on 41.2% of the rows that have one; at 53 it survives on 15.7%, and 10% of
  // sentences now end in an ellipsis rather than a full stop where none did before. That is the trade the
  // width buys and it is a real regression in what Archie manages to say -- 240px/57 would keep 27.5%, and
  // 200px/49 would drop to 5.6% and effectively delete the tag. A reader still always gets a complete
  // subject and verb: it is the category or the owner that gets cut, never the project's own name.
  //
  // NAME_MAX IS NO LONGER THE BINDING CONSTRAINT, which is the other thing collapsing the pair changed. It
  // used to be the number doing the work, because with a total cap that could not really bound the string a
  // single long name filled both lines on its own. Now SAY_MAX bounds the sentence whatever the name did, so
  // NAME_MAX only decides *which end* gets sacrificed: 53 was the answer at 220px for NAME_MAX 20, 22, 24,
  // 26 and 28 alike. Lowering it clips more names and saves more sentence tails, and 22 is the knee -- it
  // truncates 18.5% of names (median length is 12) against 10.0% of sentences losing their full stop, where
  // 24 costs 148 more broken sentences to spare 52 names.
  //
  // The cap is enforced here and not with `line-clamp` because clamping would hide the tail of a fact while
  // reporting a bubble that fits, so the text a reader cannot see would still be the text the page chose to
  // say. Clipping keeps what is shown and what is said the same thing.
  //
  // IT CUTS MID-WORD MOST OF THE TIME, and an earlier version of this comment claimed otherwise. The word
  // boundary is a preference, not a guarantee: the strip only fires when the cut lands after some whitespace,
  // and the names long enough to need cutting are overwhelmingly slugs -- 119 of the 140 names over 26
  // characters have no whitespace in their first 25, so 85% of real truncations are mid-word
  // (`modelcontextprotocol/serv…`, `anthropics/claude-cookboo…`). That is the right behaviour, because the
  // alternative for a slug is to drop the whole thing, but it is not a word boundary and should not be sold
  // as one.
  //
  // Two things the naive version got wrong, both about what a name may contain, and the two lines that fix
  // them are independent -- do not read either as backup for the other.
  //
  // It measured and sliced UTF-16 code units. `"Agents" + 12 robot emoji + "End"` is 21 characters and
  // measures 33, so it was clipped when it did not need clipping at all, and the cut landed inside a surrogate
  // pair: `"Agents🤖🤖🤖🤖🤖🤖🤖🤖🤖\ud83e…"`, ending in mojibake rather than a character. Counting and slicing
  // code points fixes both halves of that, and it is the ONLY thing that fixes the split pair.
  //
  // Whitespace saves such a string rather than endangering it, which is the opposite of the intuition: the
  // strip is `/\s+\S*$/`, so with no whitespace in the first 25 characters it cannot fire and the raw cut
  // ships. That is why nothing in today's 1,294 rows reaches the bug -- the single name with an astral
  // character has spaces -- and why a weekly rebuild that returns one space-free emoji name would.
  //
  // Separately, stripping the partial word could strip almost everything: a name beginning with a space and
  // one long token clipped to a bare `"…"`, saying nothing at all. The half-budget fallback keeps the hard cut
  // when the word-boundary version would throw away more than half the budget. That fallback is what fixes the
  // bare ellipsis and it does NOT fix the surrogate; deleting it as redundant would bring the empty bubble
  // back on its own.
  const NAME_MAX = 22, SAY_MAX = 53;
  const clipWords = (text, limit) => {
    const points = Array.from(text);
    if (points.length <= limit) return text;
    const hard = points.slice(0, limit - 1).join("");
    const word = hard.replace(/\s+\S*$/, "");
    return (Array.from(word).length >= limit / 2 ? word : hard) + "…";
  };
  const wordsFor = r => {
    const category = (D.cats[r.cat] || {}).name || "the atlas";
    const targets = r.targets.map(t => D.targets[t] && D.targets[t].name).filter(Boolean);
    const name = clipWords(r.name, NAME_MAX);
    const owner = r.nwo.split("/")[0];
    // `r.name` is the full `owner/name` for 267 of the committed rows, which made the old "comes from"
    // sentence name the same string twice. The owner alone is the fact that sentence was reaching for, and
    // it is dropped rather than repeated when the project is named after whoever publishes it.
    const facts = [
      name + " is listed under " + category + ".",
      name + " is on " + r.lists + (r.lists === 1 ? " source list." : " source lists.")
    ];
    if (owner.toLowerCase() !== r.name.toLowerCase()) facts.push(name + " comes from " + owner + ".");
    // WHICH FACT A PROJECT SAYS USED TO DEPEND ON THE LENGTH OF A COLOUR NAME. It was
    // `projectAccent(r.nwo).length % facts.length` -- the accent palette's names are 3, 4, 4, 5 and 6
    // characters, so renaming a swatch would have silently re-assigned the sentence for every project in that
    // accent class, and nothing anywhere would have noticed. Two unrelated things do not belong on one hook.
    // This hash is only a spreader: it wants to be stable for a given project and unrelated to everything
    // else, which a 31-multiplier over the `nwo` is.
    let spread = 0;
    for (let i = 0; i < r.nwo.length; i++) spread = (spread * 31 + r.nwo.charCodeAt(i)) | 0;
    const fact = facts[Math.abs(spread) % facts.length];
    const tagged = targets.length ? " Tagged for " + targets[0] + "." : "";
    // Code points here for the same reason `clipWords` counts them, and it is a different symptom of the
    // same mistake rather than a second guard on the same one. `clipWords` counting units split a surrogate
    // pair; this test counting units mismeasures a name that contains one, and the failure is silent in the
    // other direction -- the tag is dropped from a sentence that would have fitted. `"Agents"` plus twelve
    // robot emoji plus `"End"` is 21 characters and measures 33, so it loses its tag with 12 characters of
    // room to spare. Nothing in today's rows reaches it; a rebuild that returns one emoji name would, and
    // the narrower the box gets the more rows sit close enough to the cap for the 2x overcount to decide.
    // SAY_MAX twice on purpose -- see the note above on why this used to be two numbers and must not be
    // again. The tag goes on only if the finished sentence still fits the one bound, so nothing below ever
    // clips a tag it has just added, and the longest string is SAY_MAX rather than something under it.
    return clipWords(fact + (Array.from(fact + tagged).length <= SAY_MAX ? tagged : ""), SAY_MAX);
  };
  const speak = r => {
    if (muted || !speech || !r) return;
    last = r;
    speech.textContent = wordsFor(r);
    speech.hidden = false;
  };
  // Leaving takes the bubble with it, and cancels a fact that has not been spoken yet. Both halves matter:
  // without the `clearTimeout` a reader who brushes across a row on the way to the filter bar still gets a
  // bubble 320ms later, about a row they are no longer anywhere near.
  const hide = () => {
    clearTimeout(timer);
    if (speech) speech.hidden = true;
  };
  const schedule = el => {
    const nwo = el && el.dataset.project;
    const row = nwo && ROWS.find(r => r.nwo === nwo);
    if (!row) return;
    clearTimeout(timer);
    timer = setTimeout(() => speak(row), 320);
  };
  if (out) {
    out.addEventListener("mouseover", ev => schedule(ev.target.closest("tr[data-project]")));
    out.addEventListener("focusin", ev => schedule(ev.target.closest("tr[data-project]")));
    // `mouseout` and `focusout` bubble from every cell, so they fire while the pointer is still inside the
    // same row -- moving from the title to the tags is a leave-then-enter of two `td`s. Hiding on those
    // would flicker the bubble across a row the reader never left, so the row the pointer moved *to* is
    // compared against the row it left and only a genuine exit hides. Crossing straight into another row
    // still hides, and the `mouseover` that follows re-arms the timer, so a fact is replaced rather than
    // left standing.
    const leaving = ev => {
      const row = ev.target.closest("tr[data-project]");
      if (!row) return;
      const to = ev.relatedTarget;
      if (to && row.contains(to)) return;
      hide();
    };
    out.addEventListener("mouseout", leaving);
    out.addEventListener("focusout", leaving);
  }
  // A keyboard reader who has tabbed past the row still has the bubble on screen, and reaching for the
  // mouse to dismiss it is the one thing they are not doing.
  document.addEventListener("keydown", ev => { if (ev.key === "Escape") hide(); });
  if (quiet) quiet.onclick = () => setQuiet(!muted);
  setQuiet(muted);
  if (tip) tip.onclick = () => {
    if (muted) { setQuiet(false); }
    if (last) speak(last);
    else if (speech) {
      speech.textContent = "Hover or focus a project and I’ll introduce it using its Atlas record.";
      speech.hidden = false;
    }
  };
  if (name && wrap) name.onclick = () => {
    const now = Date.now();
    clicks = clicks.filter(t => now - t < 1400);
    clicks.push(now);
    if (clicks.length < 5) return;
    clicks = [];
    document.getElementById("atlas-orbit")?.remove();
    const orbit = document.createElement("span");
    orbit.id = "atlas-orbit";
    orbit.setAttribute("aria-hidden", "true");
    for (let i = 0; i < 12; i++) {
      const star = document.createElement("i");
      star.className = "orbit-star";
      star.style.setProperty("--orbit-angle", (i * 30) + "deg");
      orbit.appendChild(star);
    }
    wrap.appendChild(orbit);
    setTimeout(() => orbit.remove(), 1600);
  };
}

function set(patch, keepFocus) {
  // Any other interaction outranks a search the reader has stopped waiting for. Without this, tapping
  // Clear all inside the 150ms window let the queued timer land afterwards and re-apply the term that was
  // just cleared: empty box, filtered table, `#q=` back in the URL. The debounce made every filter control
  // racy against the search box, so the cancel belongs here, on the shared path, not on each handler.
  clearTimeout(typing);
  Object.assign(state, patch, {shown: PAGE_SIZE});
  writeHash();
  render();
  // A rescue button or Clear all can change the search term, and the box has to say so. Skipped while
  // typing, where the box is the source of the change and rewriting its value moves the caret to the end.
  if (!keepFocus) {
    const q = document.getElementById("q");
    if (q.value !== state.q) q.value = state.q;
    q.blur();
  }
}

// Every filter lives in the hash, so any view is a link. This is the whole point of the page: a
// Markdown file can be one topic or one target, never the crossing of the two.
function writeHash() {
  const p = new URLSearchParams();
  if (state.q) p.set("q", state.q);
  if (state.cat) p.set("topic", state.cat);
  if (state.tgt) p.set("target", state.tgt);
  if (state.os.length) p.set("os", state.os.map(i => D.os[i].toLowerCase()).join(","));
  if (state.strict) p.set("confirmed", "1");
  if (state.fresh) p.set("new", "1");
  if (state.rising) p.set("rising", "1");
  // The flag only, never the set. `#saved=1` says "the saved filter is on", and on somebody else's machine
  // that means *their* saved projects -- which is the honest reading of a filter and the reason this is one
  // parameter rather than a list of repositories in the URL.
  if (state.saved) p.set("saved", "1");
  if (state.sort !== "relevance") p.set("sort", state.sort);
  // In the hash and nowhere else. localStorage is the obvious second home for it -- the theme is kept
  // there -- and it would be a bug: a reader who opens a `#view=cards` link they were sent, then a bare
  // link to the same page, has said nothing about which view they prefer in general, and answering that
  // question for them means two stores that can disagree about one value. The hash already survives a
  // reload, because `replaceState` leaves it in the URL, which is the whole of what this has to do.
  if (state.view !== "cards") p.set("view", state.view);
  const s = p.toString();
  // Appended by hand rather than set on the URLSearchParams above, and this is the only parameter on the page
  // that is. `URLSearchParams` percent-encodes both characters an `owner/name` list is made of -- `/` becomes
  // %2F and the separator %2C -- so a twelve-project link that reads
  // `list=openclaw/openclaw,browser-use/browser-use` would go out as sixty characters of escapes instead.
  // Both are legal unescaped in a fragment (RFC 3986: a fragment admits pchar, "/" and "?", and pchar admits
  // the sub-delims, which include ","), so the encoding buys nothing and costs the one property a link
  // somebody is about to paste into a message has to have -- being readable enough to trust before clicking.
  const list = state.list.size ? "list=" + [...state.list].join(",") : "";
  // Appended by hand for exactly the reason `list=` is, and the reason applies harder here: this is the one
  // parameter on the page whose entire purpose is to be pasted into a message. `cmp=langchain-ai/langgraph,
  // openclaw/openclaw` is a comparison somebody can read before they click; the percent-encoded form is
  // forty characters of escapes that could be anything.
  //
  // Written last, after `list=`, so the readable pair sit together at the end of the fragment rather than
  // having the encoded filters between them.
  const cmp = state.cmp.size ? "cmp=" + [...state.cmp].join(",") : "";
  const all = [s, list, cmp].filter(Boolean).join("&");
  history.replaceState(null, "", all ? "#" + all : location.pathname);
}

function readHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  const slugs = l => l.map(x => x.slug);
  state.q = p.get("q") || "";
  state.cat = slugs(D.cats).includes(p.get("topic")) ? p.get("topic") : "";
  state.tgt = slugs(D.targets).includes(p.get("target")) ? p.get("target") : "";
  const names = D.os.map(o => o.toLowerCase());
  state.os = (p.get("os") || "").split(",").map(s => names.indexOf(s.trim())).filter(i => i >= 0);
  state.strict = p.get("confirmed") === "1";
  // A `#new=1` link outlives the import it was written about -- and now outlives it sooner and more often
  // than it used to, because a cohort is superseded by the next import that brings anything rather than
  // lasting a fixed fortnight. Honouring the flag with no cohort to show would greet the reader with
  // "nothing matches"; dropping it shows them the atlas instead. The guard is unchanged: `NEW > 0` is false
  // both when the cohort is empty and when the build sent no cohort at all.
  state.fresh = p.get("new") === "1" && NEW > 0;
  // A `#rising=1` link can outlive its data as easily as `#new=1` outlives its fortnight: a build where
  // the ledger was reset has no rising rows, and honouring the flag would greet the reader with "nothing
  // matches" instead of the atlas. Same guard as the line above, for the same reason.
  state.rising = p.get("rising") === "1" && RISE !== null && RISING > 0;
  // Guarded on the set being non-empty, which is the same guard `#new=1` and `#rising=1` get one line up and
  // the same reason: a link outliving the thing it selected. This one is stronger, though, because the link
  // can also *travel*. A reader who posts their filtered view to a colleague posts `#saved=1` with it, and
  // on that colleague's machine the set is empty -- so honouring the flag would greet them with "nothing
  // matches" as their first impression of the atlas. `loadSaved()` runs in `wire()`, before this, so the
  // size is known by the time it is read.
  state.saved = p.get("saved") === "1" && SAVED.size > 0;
  // Somebody else's collection, and the counterpart to the line above rather than a duplicate of it. `saved=1`
  // is a flag over a store that only exists on one machine; `list=` carries the rows, so it means the same
  // twelve projects everywhere and is what a reader sends when they want a colleague to see what they see.
  // Nothing is written to storage on the way in -- the strip above the results is where the reader decides
  // whether this becomes theirs.
  //
  // Capped, because a hash is an untrusted input that anyone can hand-edit: this is the only place on the page
  // where the length of a string decides how much work `match` does per keystroke, and 200 is far past any
  // list a person assembles by pressing Save.
  state.list = FLAGS["index.export"]
    ? new Set((p.get("list") || "").split(",").map(s => s.trim()).filter(Boolean).slice(0, 200))
    : new Set();
  // The pinned comparison. Three guards, and each one is a different failure:
  //
  // `BY_NWO.has` -- resolved against the rows rather than kept as typed, which `#list=` deliberately does not
  // do. A `list=` key that matches nothing simply filters nothing out and the reader sees a shorter table; an
  // unresolvable `cmp=` key would be a column of dashes with a name at the top and no way to tell whether the
  // project left the atlas or the link was mistyped. Dropping it shows the comparison that can be made. This
  // is the same call `SAVED` makes -- hold the key, not a copy of the row, and let a departed project stop
  // matching -- reached from the opposite direction, because here the row is what the panel is made of.
  //
  // `slice` -- a hash is hand-editable, so the cap is enforced here and not only where the buttons are. `#cmp=`
  // with forty repositories in it would build a forty-column table that no amount of scrolling makes readable.
  // Sliced after the resolve, so four *valid* keys survive a link that also carried two dead ones.
  //
  // The flag -- so turning the feature off makes a `#cmp=` link inert rather than half-working: no buttons to
  // unpin with is a worse state than no comparison at all.
  state.cmp = FLAGS["index.compare"]
    ? new Set((p.get("cmp") || "").split(",").map(s => s.trim())
        .filter(k => k && BY_NWO.has(k)).slice(0, CMP_MAX))
    : new Set();
  // Every `#sort=stars` link written before Best match existed still says exactly what it said then,
  // because the name is unchanged and only the *default* moved.
  // `rising` is the one sort key that can be unavailable, so it is checked against the data and not only
  // against the map. Without that, a `#sort=rising` link into a build with no velocity would select an
  // <option> that `buildChips` has removed, and the menu would render blank.
  const want = p.get("sort");
  state.sort = SORT_KEYS.includes(want) && (want !== "rising" || RISE) ? want : "relevance";
  // Both words are read explicitly rather than one being tested and the rest falling through, so that
  // `#view=cards` still selects cards now that they are the default -- every such link written while they
  // were opt-in keeps working, and so does the `#view=table` this page writes today. Anything else --
  // absent, or a hand-edited `#view=grid` -- is the default rather than a stylesheet branch that does
  // not exist.
  state.view = p.get("view") === "table" ? "table" : "cards";
  document.getElementById("q").value = state.q;
  document.getElementById("sort").value = state.sort;
}

// "Does this run on my Windows machine" has two answers -- a native build, or reachable through WSL2 --
// and the workbook's Windows sheet counts both, which is where the 1,105 in the README comes from. They
// stay two columns, because a reader without WSL2 needs to see which is which, but the chip has to mean
// the same thing the same word means everywhere else in this project. WSL2 only ever counts as Yes:
// "probably works under WSL2" is not a claim anything here makes.
const OS_ANY = {0: [[0, "YL"], [1, "Y"]]};

function match(r) {
  // These two first, because they are the most selective clauses this function has -- a saved set or a shared
  // list is single digits against 1,294 rows -- and because a Set lookup is the cheapest test here. `match`
  // runs 1,294 times per keystroke, so the order of these lines is not cosmetic.
  if (state.list.size && !state.list.has(r.nwo)) return false;
  if (state.saved && !SAVED.has(r.nwo)) return false;
  if (state.fresh && !r.isnew) return false;
  if (state.since && !r.issince) return false;
  if (state.rising && !r.rise) return false;
  if (state.cat && D.cats[r.cat].slug !== state.cat) return false;
  if (state.tgt) {
    const want = D.targets.findIndex(t => t.slug === state.tgt);
    if (!r.targets.includes(want)) return false;
  }
  for (const i of state.os) {
    const ways = OS_ANY[i] || [[i, "YL"]];
    const ok = ways.some(([k, allow]) =>
      (state.strict ? "Y" : allow).includes(r.os[k]));
    if (!ok) return false;
  }
  if (state.q) {
    for (const w of state.q.toLowerCase().split(/\s+/).filter(Boolean))
      if (!r.hay.includes(w)) return false;
  }
  return true;
}

// What the table would hold with one filter relaxed. Mutate-count-restore rather than threading a state
// argument through `match`, because `match` is called 1,294 times per keystroke and an extra parameter on
// the hot path to serve a case that only fires on an empty table is the wrong trade. The patches only ever
// replace `state.os` and `state.list` wholesale, never mutate either, so restoring the reference restores the
// value -- which is what makes a shallow copy sufficient for a state object holding an array and a Set.
function countWith(patch) {
  const saved = Object.assign({}, state);
  Object.assign(state, patch);
  const n = ROWS.filter(match).length;
  Object.assign(state, saved);
  return n;
}

// Ranked by what each one would return, so the first button is the most productive thing to click. A
// filter whose removal still leaves nothing is dropped -- offering it would be a second dead end.
function rescue() {
  const opts = [];
  if (state.q) opts.push(["Drop the search “" + state.q + "”", {q: ""}]);
  if (state.cat) {
    const c = D.cats.find(x => x.slug === state.cat);
    if (c) opts.push(["Drop topic " + c.name, {cat: ""}]);
  }
  if (state.tgt) {
    const t = D.targets.find(x => x.slug === state.tgt);
    if (t) opts.push(["Stop requiring " + t.name, {tgt: ""}]);
  }
  state.os.forEach(i => opts.push(["Drop " + D.os[i], {os: state.os.filter(x => x !== i)}]));
  if (state.strict) opts.push(["Allow inferred support", {strict: false}]);
  if (state.fresh) opts.push(["Drop the new-arrivals filter", {fresh: false}]);
  if (state.since) opts.push(["Drop the since-your-last-visit filter", {since: false}]);
  if (state.rising) opts.push(["Drop the rising filter", {rising: false}]);
  // Offered like any other filter, and it is the one most likely to be the culprit: a saved set is single
  // digits, so crossing it with a topic or a platform empties the table far more easily than crossing two
  // build-wide filters does. The button drops the filter and never the set -- `countWith` only ever patches
  // `state`, so there is no path from an empty table to losing a collection.
  if (state.saved) opts.push(["Look beyond your " + SAVED.size + " saved", {saved: false}]);
  // Offered like any other filter, and with more reason than most: a shared list crossed with a topic empties
  // the table as easily as a saved set does, and the reader who followed the link did not choose the crossing.
  if (state.list.size)
    opts.push(["Look beyond the shared list of " + state.list.size, {list: new Set()}]);
  return opts.map(o => ({label: o[0], patch: o[1], n: countWith(o[1])}))
    .filter(o => o.n > 0)
    .sort((a, b) => b.n - a.n)
    .slice(0, 4);
}

// The repository, in script as well as in markup, for the one href on this page that has to be composed at
// runtime. `substitute()` replaces __REPO__ across the whole page string and does not care that this
// occurrence is inside a <script>, so it is the same placeholder the footer's links already use. Declared
// here beside its only consumer rather than up with SNAPSHOT and BUILT: unlike those two it is not a fact
// about the build that the rest of the page reads, it is a detail of the link below.
const REPO = "__REPO__";

// The one thing about this page that analytics cannot learn, and the one worth learning.
//
// Cloudflare Web Analytics has no custom-event API at any plan level, and its beacon runs every URL it
// reports through a helper that blanks the hash and the query before sending -- read out of
// beacon.min.js 2026.9.1 -- so `#q=kubernetes` never leaves the browser and no dashboard filter, GraphQL
// dimension or plan upgrade can recover it. Which topic and harness a reader crossed *is* already collected,
// but by paths and not by events: `20_landing.py` and `22_detail.py` prerender 1,451 pages besides this one,
// and each is an ordinary page view of an ordinary `Path`. A search that found nothing has no path to be,
// and it is the more useful of the two facts -- it names either a tool this atlas is missing or a word its
// taxonomy does not use.
//
// So the reader is asked instead of measured. A prefilled issue link costs no script, no request and no
// cookie, and collects nothing whatever from anyone who does not press it; what does arrive lands in the
// tracker where taxonomy work already happens, already written up by someone who knows what they wanted.
// The trade is worth stating plainly: this yields a handful of good reports rather than a rate, and a reader
// who sends one identifies themselves through their own GitHub account -- which is their decision to make,
// on a form they can read first, and exactly why this is an anchor and not a fetch().
//
// Only ever reached from the empty branch of render(), which is the gate that makes it worth having twice
// over. `near()` has already offered every trigram-near correction as real, clickable rows before that
// branch can be reached, so a term that gets this far is not a misspelling of anything here. And the
// 1,294-row rendering loop never calls this, so the hot path pays nothing for it.
function missLink() {
  // The reader's own free text, on its way into a URL. Control characters go because a pasted newline would
  // split the issue title, and the length is capped because a pasted paragraph makes an issue nobody
  // triages -- the terms worth acting on are two or three words.
  const typed = state.q.replace(/[\u0000-\u001f]+/g, " ").trim();
  // Cut by code point and not by UTF-16 unit. `.slice(0, 80)` can land in the middle of a surrogate pair,
  // `encodeURIComponent` throws URIError on the lone surrogate that leaves behind, and the throw would come
  // out of the `innerHTML` expression in render() below -- so a reader who pasted an emoji at exactly the
  // wrong offset would get a blank result area instead of "Nothing matches all of that". Spread iteration
  // yields whole code points, so there is no offset for that to happen at.
  const q = [...typed].slice(0, 80).join("").trim();
  if (!q) return "";
  // The filters travel with the term, because "kubernetes, confirmed-only, Windows" and "kubernetes" are
  // different findings and only one of them is a coverage gap. The hash is already the canonical
  // description of the view and `set()` rewrote it immediately before calling render(), so it is what gets
  // quoted -- percent-encoded exactly as the reader would paste it back.
  const body = "Searched for: " + q + "\n\nFilters: " + (location.hash.slice(1) || "none") +
    "\nSnapshot: " + SNAPSHOT + "\n\nWhat were you hoping to find? A repository URL is ideal.\n";
  const href = "https://github.com/" + REPO + "/issues/new?labels=coverage&title=" +
    encodeURIComponent("Nothing found for “" + q + "”") + "&body=" + encodeURIComponent(body);
  // esc() on the href like every other URL this file writes into an attribute. What needs it here is the
  // pair of query separators: a bare ampersand in an attribute value is exactly what `&amp;` is for, and
  // `&body=` sits close enough to a named character reference to be worth not finding out about.
  // target=_blank because the whole point of keeping state in the hash is that the view survives, and a
  // same-tab navigation to GitHub would throw away the filters the reader spent six clicks building.
  return '<p><a class="miss" href="' + esc(href) + '" target="_blank" rel="noopener">' +
    "Searched for something that isn’t here? Tell us what’s missing</a></p>";
}

// ─────────────────────────────────────────────────────────────────────────────────────────────────────
// SEARCH BY MEANING -- JFH-293.
//
// Every filter above this line is a substring test, and a substring test cannot answer the question most
// people actually arrive with. Measured against the 1,294 rows as committed, 8 of 37 plausible queries
// return literally nothing: "something to review PRs", "scrape websites", "chat with my pdfs", "turn
// speech into text". The projects are all here. The words are not, because a maintainer wrote "pull
// request" and the reader typed "PRs", and `hay.includes(w)` has no opinion about that.
//
// So the page also carries 96-dimensional vectors for every row, and encodes the reader's query into the
// same space here, in the browser, with no model download and no WASM. `scripts/27_semantic.py` builds
// `docs/search/` from `minishlab/potion-base-8M` -- a *static* embedding table, not a transformer, so
// there is no attention to run and pooling is the whole of the forward pass. Encoding a query is:
// segment it into WordPiece tokens, look each one up, add the vectors, normalise. That is the entire
// model on this side, it is the four lines of `semVector` below, and it runs in well under a
// millisecond. 758 KB across four files -- 504 KB gzipped -- fetched once, on the first
// interaction with the search box. Not the 784 KB `docs/search/` weighs: the other 25 KB is
// `xy.bin` and `near.bin`, which the map below fetches on its own trigger and this does not
// need.
//
// WHY IT IS FETCHED ON INTERACTION rather than at load or in the precache. A reader who came for the
// table and never types is charged nothing, and the download races the reader's first keystrokes rather
// than the first paint. The trigger is `focus` as well as `input`, which in practice means the bytes are
// usually there before the second character. Until they are, and forever if the fetch fails, the
// substring filter is exactly what it was -- this feature has no state anywhere that can break it, which
// is the reason there is no flag for it.
//
// THE STALENESS GUARD, which is the one failure that must not be quiet. These vectors are addressed by
// row *ordinal*: `docs.bin` is row 0, row 1, row 2 with nothing naming them. An index built against a
// different `data.json` therefore does not error, does not look wrong, and returns each project's
// neighbour with total confidence. `meta.json` carries a SHA-256 of the `nwo` column it was built from
// and this recomputes it from the rows in hand; a mismatch switches the whole feature off rather than
// ranking with it. `crypto.subtle` needs a secure context, so on `file://` the guard falls back to the
// row count alone -- which catches the ordinary case, a rebuilt crawl of a different size.
//
// WHAT IT WILL NOT DO, and this is a decision rather than a limit of the arithmetic. It never dilutes a
// query that already works: see `render()`, where meaning is consulted only when the words themselves
// found fewer than `SEM_THIN` rows. And it declines outright on a query no word of which appears
// anywhere in the corpus. That gate is here because the obvious one does not work: measured over the
// committed index, "qwerty zxcvb" tops out at cosine 0.576 and "xyzzy plugh frotz" at 0.487, while real
// queries like "chat with my pdfs" reach only 0.452 and "keep my agent from deleting files" 0.483. The
// similarity of nonsense is indistinguishable from the similarity of a real question, so any absolute
// threshold either admits the nonsense or rejects the question. What *does* separate them is the corpus:
// every real query above has at least one word that appears somewhere in these 1,294 rows, and every
// nonsense one has none. That test costs an early-exiting scan of `hay` and no new bytes at all.
const SEM_DIMS_MAX = 512;   // sanity bound on meta.dims before it is used as a stride
const SEM_THIN = 12;        // exact matches at or above which meaning is not consulted
const SEM_MAX = 12;         // most rows meaning may add
const SEM_RATIO = 0.6;      // and only those within this fraction of the best cosine
// Blended into `relevance()`, and the number is ordinal like every other weight there. A perfect cosine
// scores 90 -- the same as a query word at the start of the project's name -- so meaning can outrank a
// word found mid-name or in a blurb and can never outrank a row actually *called* what was typed.
const SEM_LIFT = 90;
// Its own regex object, and not the one `27_semantic.py` compiles, because this is a transcription
// rather than a shared implementation and there is no way to share one across the two languages. The
// stage has this pattern, `tests/semantic_test.py` has it a third time, and all three have to agree: a
// query segmented one way against documents segmented another scores noise while looking healthy.
const SEM_WORD = /[a-z0-9]+|[^\sa-z0-9]/g;
let SEM = null, SEM_STATE = "cold";   // cold | loading | live | off

// Greedy longest-match WordPiece, over the pruned vocabulary this page holds and not the model's full
// one. `27_semantic.py` segments the corpus against exactly the tokens shipped in `vocab.json` for the
// same reason: the stage shipped a subset, so it has to *build* against the subset too, or the same word
// is two different token sequences on the two sides. A word no suffix of which is in the vocabulary is
// dropped whole rather than partially, which is why the stage force-keeps every single-character token.
//
// `slot` is a parameter rather than a read of `SEM.slot`, which makes this the one function in the
// semantic module with no dependency on module state -- and therefore the one a test can call. It is
// also the function most worth calling: `meta.json` ships the stage's own segmentation of a handful of
// texts, and `tests/probe.mjs` runs *this* code against those fixtures. Drift between the two
// tokenisers is the failure that has no symptom -- no exception, no empty result, just a query pointing
// somewhere the documents are not -- so it is checked by comparing token ids and nothing else.
function semTokens(text, slot, stop) {
  const out = [];
  for (const word of String(text).toLowerCase().match(SEM_WORD) || []) {
    // Before the lookup, never after, and never by leaving the token out of the vocabulary instead. A
    // stopword whose token is missing does not disappear -- WordPiece re-spells it out of the longest
    // surviving pieces, and those pieces are rare, so it comes back weighted *higher* than the content
    // words. Measured on this corpus: "should" arrived as `sho` + `##uld` at row norms 172 and 152 against
    // 179 for `pdf`. See the note on STOP in 27_semantic.py.
    if (stop && stop.has(word)) continue;
    let start = 0, ok = true;
    const pieces = [];
    while (start < word.length) {
      let end = word.length;
      for (; end > start; end--) {
        const piece = start === 0 ? word.slice(start, end) : "##" + word.slice(start, end);
        const id = slot.get(piece);
        if (id !== undefined) { pieces.push(id); break; }
      }
      if (end === start) { ok = false; break; }
      start = end;
    }
    if (ok) for (const p of pieces) out.push(p);
  }
  return out;
}

// The forward pass. Sum of the token rows, normalised -- the IDF weighting and the projection are already
// baked into the shipped table, so there is nothing to weight here and nothing to project.
function semVector(query) {
  const ids = semTokens(query, SEM.slot, SEM.stop);
  // Also how a topicless question declines. "please help me choose" is every word a stopword, so it
  // produces no tokens at all and never reaches the corpus below -- which is a better answer than the
  // twelve confident, unrelated projects it used to return.
  if (!ids.length) return null;
  const d = SEM.dims, v = new Float32Array(d);
  for (const id of ids) {
    const base = id * d;
    for (let k = 0; k < d; k++) v[k] += SEM.table[base + k] * SEM.vs;
  }
  let n = 0;
  for (let k = 0; k < d; k++) n += v[k] * v[k];
  n = Math.sqrt(n);
  if (!n) return null;
  for (let k = 0; k < d; k++) v[k] /= n;
  return v;
}

// Does this word appear anywhere in the atlas? Disjunction across the corpus, where the search box is a
// conjunction within one row -- which is why this is a different question and not a slower version of
// the same one. Early-exits on the first hit, so a common word costs one `includes` and only a word that
// is nowhere pays for all 1,294. Words under three characters are not tested: they are in every corpus
// and testing them would pass every query.
function corpusKnows(word) {
  for (const r of ROWS) if (r.hay.includes(word)) return true;
  return false;
}

// Rows this corpus could plausibly mean, excluding the ones the words already found. Returns [] -- never
// a weak guess -- when the index is not live, when nothing segments, or when the gate above declines.
//
// Writes `r.sem` on every row it scored, including the exact matches, because `relevance()` blends the
// cosine into the ranking of the whole result set and not only of the rows meaning contributed. That is
// the *only* thing this writes onto a row, and the restraint is the fix for a bug rather than a
// preference: which rows meaning contributed was a `r.semonly` flag here for one draft, and a flag on a
// row outlives the query that set it. Searching "chat with my pdfs" and then "claude" -- 300 substring
// matches, so meaning is never consulted -- left exactly one row wearing a "by meaning" pill it had
// earned under the previous query, on a result set that had nothing to do with meaning at all. `r.sem` is
// safe where a flag was not because `relevance()` is passed the current render's `sense` and reads the
// score only when meaning actually ran; the membership question is answered by a Set in `render()`, which
// cannot outlive the render that built it.
function senseHits(query, already) {
  if (SEM_STATE !== "live") return [];
  const words = query.toLowerCase().split(/\s+/).filter(w => w.length >= 3);
  if (!words.length || !words.some(corpusKnows)) return [];
  const v = semVector(query);
  if (!v) return [];
  const pool = poolWithoutQuery(), d = SEM.dims, scored = [];
  for (const r of pool) {
    const base = r.ord * d;
    let dot = 0;
    for (let k = 0; k < d; k++) dot += SEM.docs[base + k] * SEM.ds * v[k];
    r.sem = dot;
    scored.push(r);
  }
  if (!scored.length) return [];
  scored.sort((a, b) => b.sem - a.sem);
  // Relative to the best score, not to a constant: this corpus is expected to go from 1,294 rows to
  // several thousand, and the top cosine for a given query moves as the corpus fills in around it while
  // the *shape* of the tail does not.
  const floor = scored[0].sem * SEM_RATIO;
  const seen = new Set(already.map(r => r.nwo)), out = [];
  for (const r of scored) {
    if (out.length >= SEM_MAX || r.sem < floor) break;
    if (seen.has(r.nwo)) continue;
    out.push(r);
  }
  return out;
}

// Fetched once, on the reader's first contact with the search box. Everything here fails closed: any
// throw, any 404, any disagreement with `docs/data.json` leaves `SEM_STATE` at "off" and the page behaves
// as it did before this function existed.
async function loadSemantic() {
  if (SEM_STATE !== "cold") return;
  SEM_STATE = "loading";
  try {
    const grab = async (name, how) => {
      const res = await fetch("search/" + name);
      if (!res.ok) throw new Error("search/" + name + " -> " + res.status);
      return how === "json" ? res.json() : res.arrayBuffer();
    };
    const [meta, vocab, table, docs] = await Promise.all([
      grab("meta.json", "json"), grab("vocab.json", "json"),
      grab("vocab.bin", "buf"), grab("docs.bin", "buf"),
    ]);
    const dims = meta.dims | 0;
    if (!(dims > 0 && dims <= SEM_DIMS_MAX)) throw new Error("meta.dims is " + meta.dims);
    // The guard. The row count first because it is free and catches the common case; the fingerprint
    // second because it is the only test that catches a rebuild of the *same* size in a different order,
    // which is the one that silently returns the wrong project for every query.
    if (meta.rows !== ROWS.length)
      throw new Error("index has " + meta.rows + " rows, data.json has " + ROWS.length);
    if (crypto.subtle) {
      const body = new TextEncoder().encode(ROWS.map(r => r.nwo).join("\n"));
      const hash = [...new Uint8Array(await crypto.subtle.digest("SHA-256", body))]
        .map(b => b.toString(16).padStart(2, "0")).join("").slice(0, 16);
      if (hash !== meta.fingerprint)
        throw new Error("data.json is " + hash + ", index was built against " + meta.fingerprint);
    }
    if (docs.byteLength !== meta.rows * dims) throw new Error("docs.bin is " + docs.byteLength + " B");
    if (table.byteLength !== vocab.tokens.length * dims)
      throw new Error("vocab.bin is " + table.byteLength + " B");
    // The two scales, checked because they are the one input that would otherwise reach the arithmetic
    // unvalidated -- and NaN does not fail closed here, it fails *open* and silent. A missing scale makes
    // every `r.sem` NaN; `r.sem < floor` is then false for every row, so the cutoff never fires and a full
    // twelve arbitrary projects are admitted and labelled "by meaning". Worse, `relevance()` returns NaN
    // too, the comparator returns NaN for every pair, and the whole table -- including the rows that did
    // match the reader's words -- comes out in arbitrary order. No exception, no warning, nothing that
    // looks degraded. Unreachable from `27_semantic.py`, which always writes both; reachable from a
    // truncated or hand-edited meta.json, which is exactly what a guard is for.
    for (const [k, v] of [["doc_scale", meta.doc_scale], ["vocab_scale", meta.vocab_scale]])
      if (!(typeof v === "number" && isFinite(v) && v > 0)) throw new Error("meta." + k + " is " + v);
    SEM = {
      dims,
      slot: new Map(vocab.tokens.map((t, i) => [t, i])),
      // Shipped rather than transcribed a fourth time, and applied by `semTokens` before it looks anything
      // up. Absent in a schema 1 index built before this existed, which degrades to the old behaviour
      // rather than throwing -- an empty set simply strips nothing.
      stop: new Set(meta.stop || []),
      table: new Int8Array(table),
      docs: new Int8Array(docs),
      // int8 was quantised against two separate maxima -- one shared scale crushed every unit-length
      // document component to 0 or +/-1 and collapsed 1,294 rows onto a handful of distinct vectors.
      ds: meta.doc_scale / 127,
      vs: meta.vocab_scale / 127,
      // Kept for the map, which is the other reader of this directory and validates nothing of its own.
      // `rows` and `near` are the two lengths `xy.bin` and `near.bin` have to have; `xy_scale` is the one
      // number that turns their int16s back into positions. Stashed here rather than re-fetched there
      // because `meta.json` is where the fingerprint lives, and a second fetch is a second chance for the
      // two readers to be looking at different metadata.
      rows: meta.rows, near: meta.near | 0, xys: meta.xy_scale,
    };
    SEM_STATE = "live";
    // Only if there is something on screen this changes. A reader who focused the box and typed nothing
    // gets no re-render, and one who has already typed gets their answer the moment the bytes land.
    if (state.q) render();
  } catch (err) {
    SEM_STATE = "off";
    // Reported, not thrown. Search by meaning going quietly missing is a degradation; the page around it
    // is unharmed, and a console line is what tells a contributor why their rebuilt index does nothing.
    console.warn("search by meaning is off:", err.message);
  }
}

// The same fetch, awaitable. `loadSemantic` is already idempotent -- `SEM_STATE` sees to that -- but
// idempotent is not the same as *joinable*: a second caller returns instantly from the guard while the
// first is still mid-`Promise.all`, which is fine for a keystroke that only wants the bytes eventually and
// useless for the map, which has to know when they arrived. Holding the promise makes the second caller
// wait for the first fetch instead of starting another or missing it.
let SEM_LOAD = null;
function semanticReady() { return SEM_LOAD || (SEM_LOAD = loadSemantic()); }

// ─────────────────────────────────────────────────────────────────────────────────────────────────────
// THE ATLAS AS A MAP -- JFH-298.
//
// The other half of JFH-293. That ticket was "search the catalog by meaning, *and draw it as a map*"; the
// search shipped and the map did not. The sentence at the top of the section above used to read "near.bin
// and xy.bin sit in that directory and nothing fetches them yet"; this is what replaced it, and the same
// sentence came out of `24_pwa.py` beside its first-visit cache list.
//
// WHAT IS BEING DRAWN, and it is not a chart. `27_semantic.py` runs a force-directed layout over the same
// 96-dimensional vectors `senseHits` scores against and ships the result as one int16 pair per row: 5,176
// bytes that put every project beside the projects that do what it does. Nothing in that layout was told
// what a topic is. It produces territory anyway, and the territory agrees with the fourteen curated topics
// -- security west, plugins and clients east, observability northeast, research north, orchestrators and
// assistants south. That claim is asserted rather than admired: `semantic_test.py` requires that of the
// eight rows nearest a project, the share sharing its curated category beats two rows drawn at random by
// 2.5x, and that the neighbour edges are shorter than random pairs.
//
// WHY A MAP AND NOT A THIRD VIEW. The table answers "which of these", one row at a time, 120 to a page. It
// cannot answer "what *is* this field", "what sits next to the thing I already use", or "is the gap I think
// I see real" -- those are questions about the shape of 1,294 projects rather than about any one of them,
// and a list has no shape. So this is not `#view=map` beside table and cards. Those two are layouts of the
// rows that matched; this is one picture of all of them, with the ones that matched lit up.
//
// WHICH MEANS IT HAS NO FILTERS OF ITS OWN, and that is the design rather than a shortcut. `mapPaint` lights
// `HITS` -- the rows `render()` last put on screen, before paging -- so the search box, every chip on the
// bar, a shared `#list=` link and the reader's saved set all reach the map for free and none of them can
// disagree with it. `render()` calls `mapRepaint()` on its way out; the key in the map calls `set()` when a
// topic is pressed. There is one state and the map is a second drawing of it.
//
// WHAT A LIT SEARCH ACTUALLY SHOWS, measured rather than asserted, because the temptation here is to promise
// that a sentence lights one neighbourhood and it does not always. Twelve rows drawn at random sit a median
// 0.30 of the layout's width from their own centroid, and the tightest 5% of random draws still sit at 0.22.
// Against that null: "run untrusted agent code in a sandbox" lights a set at 0.12 and "turn my design mockup
// into working code" one at 0.19 -- both tighter than 95% of chance, both visibly one region. But "watch what
// my agent did and replay it" comes out at 0.27 and "keep an eye on what my agents are costing me" at 0.33,
// which is chance: those twelve dots are scattered over the whole cloud.
//
// The split is not noise and it is the most useful thing on the map. A query about what a tool *is* names a
// region, because that is what the layout is made of. A query about a concern that cuts across every kind of
// tool -- cost, replay, audit -- has no region to name, and the map says so by scattering. A reader who sees
// their search land in one place has found a field; a reader who sees it spray has learned that they are
// asking for a property rather than a category, which is the point at which the topic chips are the better
// instrument. Neither picture is a failure, so neither is dressed up as the other: `mapFly` frames whatever
// came back, tight or scattered, and `#mapwhat` counts it without adjectives.
//
// THE NEIGHBOUR LINES ARE NOT THE NEAREST DOTS. `near.bin` names each row's eight nearest neighbours in the
// full 96 dimensions, and this layout is a projection of those dimensions into two -- a projection loses
// things. So a hovered project's edges sometimes reach clear across the map, and that is the honest
// drawing: the reader is being *told* who its neighbours are, which is a stronger statement than "these
// pixels are near each other". The list is also directed -- row i naming j does not put i in j's eight -- so
// the out-edges are drawn solid and the in-edges faint, and a hub named by two hundred rows looks like one.
//
// THE GUARD IS THE SEMANTIC ONE AND NOT A SECOND COPY. Both files are addressed by row ordinal exactly as
// `docs.bin` is, so an index built against a different `data.json` draws a map that is confidently and
// entirely wrong -- every dot in the wrong place, every neighbour the wrong project, nothing thrown
// anywhere. So `loadMap` waits on `semanticReady()` and refuses unless it came back "live". The row count
// and the SHA-256 of the `nwo` column have then been checked once, in one place, for all three binaries.
//
// COST. 25,880 bytes on top of a fetch that already moves 758 KB, and only for a reader who opens the map.
const MAP_NEAR_MAX = 32;       // sanity bound on meta.near before it is used as a stride
const MAP_ZOOM_OUT = 0.75;     // multiples of the fit-to-stage scale a reader may reach, either way
const MAP_ZOOM_IN = 26;
const MAP_PICK = 13;           // px within which the pointer is taken to be on a dot
const MAP_LABELS = 12;         // most projects the map will name at once
const MAP_PAD = 40;            // px of stage kept clear of dots, so a label at the edge has somewhere to go
const MAP_FLY = 520;           // ms of the swing onto a search's answer, and the only animation here
// A canvas has two sizes -- the bitmap and the CSS box -- and a device pixel ratio of 3 means nine times the
// fill for dots that are already 3 px across. Capped, which costs nothing visible and is the difference
// between a smooth pan and a slideshow on a phone.
const MAP_DPR_MAX = 2;
let MAP = null, MAP_STATE = "cold";   // cold | loading | live | off
// The camera, as `px = x * k + ox` and `py = oy - y * k`. One object rather than three globals because
// `mapFly` interpolates between two of them and a reset is an assignment. `MAP_FIT` is the scale that frames
// the whole layout in the stage, kept because both zoom limits and the reset are multiples of it.
let MAP_CAM = null, MAP_FIT = 1, MAP_FLIGHT = 0;
// Which dot the pointer is over and which one a click pinned, as row ordinals: two rather than one because
// they answer different questions -- the readout follows the pointer, the neighbourhood button belongs to
// the pin -- and -1 rather than null so either can be compared without a branch.
let MAP_HOT = -1, MAP_PIN = -1;

// Fetched on the reader's first press of the Map chip, never before. Everything fails closed exactly as
// `loadSemantic` does, and for one extra reason: this is the second reader of `docs/search/`, so a mistake
// here must not be able to take the search down with it.
async function loadMap() {
  if (MAP_STATE !== "cold") return MAP_STATE;
  MAP_STATE = "loading";
  try {
    // The whole guard, borrowed rather than repeated. "live" is the only state in which the row count and the
    // fingerprint have both been checked, and it is the only state these two files may be decoded in.
    await semanticReady();
    if (SEM_STATE !== "live") throw new Error("the semantic index is " + SEM_STATE);
    const grab = async name => {
      const res = await fetch("search/" + name);
      if (!res.ok) throw new Error("search/" + name + " -> " + res.status);
      return res.arrayBuffer();
    };
    const [xyb, nearb] = await Promise.all([grab("xy.bin"), grab("near.bin")]);
    const rows = SEM.rows, n = SEM.near;
    if (!(n > 0 && n <= MAP_NEAR_MAX)) throw new Error("meta.near is " + SEM.near);
    if (!(typeof SEM.xys === "number" && isFinite(SEM.xys) && SEM.xys > 0))
      throw new Error("meta.xy_scale is " + SEM.xys);
    if (xyb.byteLength !== rows * 4) throw new Error("xy.bin is " + xyb.byteLength + " B");
    if (nearb.byteLength !== rows * n * 2) throw new Error("near.bin is " + nearb.byteLength + " B");
    // `DataView` with an explicit `true`, not `new Int16Array(buffer)`. A typed-array view over a raw buffer
    // reads it in the *platform's* byte order, and the stage writes little-endian; every machine anyone will
    // read this on agrees with that today, which is exactly the kind of assumption that is invisible until it
    // is wrong. `docs.bin` gets away with a bare `Int8Array` because a single byte has no order. These do not,
    // so the order is stated. 2,588 + 10,352 `get` calls, once, on a fetch that took milliseconds.
    const dv = new DataView(xyb), s = SEM.xys / 32767;
    const x = new Float32Array(rows), y = new Float32Array(rows);
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (let i = 0; i < rows; i++) {
      // One scale for both axes, which is the stage's decision and the reason this does not normalise each
      // axis to the stage separately: a layout squeezed to fit its box is no longer the layout, and the
      // distances a reader is being invited to read off it would be lies in one direction.
      const a = dv.getInt16(i * 4, true) * s, b = dv.getInt16(i * 4 + 2, true) * s;
      x[i] = a; y[i] = b;
      if (a < x0) x0 = a;
      if (a > x1) x1 = a;
      if (b < y0) y0 = b;
      if (b > y1) y1 = b;
    }
    if (!(x1 > x0 && y1 > y0)) throw new Error("xy.bin has no extent");
    const nv = new DataView(nearb), near = new Uint16Array(rows * n);
    // In-degree in the same pass, because it is the number that makes the picture mean something: eight out
    // is every row's number and says nothing, and "named by 214" is what a hub is. Also the bounds check --
    // an ordinal past the end of the corpus would index `x` as undefined and draw a line to NaN, which
    // canvas discards silently, so a corrupt neighbour list would simply lose edges rather than complain.
    const deg = new Uint16Array(rows);
    for (let i = 0; i < near.length; i++) {
      const v = nv.getUint16(i * 2, true);
      if (v >= rows) throw new Error("near.bin names row " + v + " of " + rows);
      near[i] = v;
      deg[v]++;
    }
    MAP = {x, y, near, deg, n, x0, y0, x1, y1};
    MAP_STATE = "live";
  } catch (err) {
    MAP_STATE = "off";
    // Reported, not thrown, for the reason the search says: a missing map is a degradation and the page
    // around it is unharmed. Unlike the search, a reader has *asked* for this one -- so `mapOpen` also puts
    // a sentence in the dialog rather than showing an empty box.
    console.warn("the map is off:", err.message);
  }
  return MAP_STATE;
}

// One hue per topic, off the golden angle rather than out of a table of fourteen colours. `D.cats` comes from
// the data, so a table would either repeat itself or run out the week a fifteenth topic is added, silently
// and in the one place a reader is being asked to tell colours apart. 137.508 degrees is the angle that keeps
// consecutive indices maximally far apart for every count, which is the property a hand-picked list has to be
// re-picked to keep.
function mapHue(cat) { return ((cat | 0) * 137.508) % 360; }

// The canvas cannot read a custom property, so the four the map needs are read out of the document once per
// paint. Which also means the map follows the theme toggle for free: the same rule that repaints it on every
// render repaints it with whatever `--ink` currently is.
function mapPalette() {
  const cs = getComputedStyle(document.documentElement);
  const pick = (name, fallback) => cs.getPropertyValue(name).trim() || fallback;
  const light = document.documentElement.dataset.theme === "light";
  return {
    light,
    back: pick("--surface", light ? "#fff" : "#090A0D"),
    ink: pick("--ink", light ? "#111" : "#EDEFF3"),
    sub: pick("--muted", "#8A8F98"),
    grid: pick("--grid", light ? "#DDE1E6" : "#22262E"),
    plane: pick("--plane", light ? "#F6F7F9" : "#101217"),
    // Lit dots are lighter than the page on a dark theme and darker than it on a light one, which is the
    // only way one hue set can carry both. The dim ones are the same hue at a lightness that reads as
    // "present but not the answer" rather than as a second colour.
    lit: light ? 40 : 63,
    dim: light ? 78 : 26,
  };
}

// Layout units to CSS px. Two functions rather than one because the hit test needs the inverse and doing it
// by hand at each call site is how a pan ends up half a pixel out of step with what is drawn.
function mapX(x) { return x * MAP_CAM.k + MAP_CAM.ox; }
// Subtracted, so the layout's positive y is up. Canvas y grows downward and the layout has no inherent up,
// so this is a free choice -- and the one that makes a screenshot of this agree with a plot of the same
// numbers in anything else.
function mapY(y) { return MAP_CAM.oy - y * MAP_CAM.k; }

// The bitmap, the CSS box and the camera, in that order, because the camera is a function of the box. Called
// on open and on every resize; returns false when there is nothing to draw on, which is what makes every
// caller safe under a stub DOM.
function mapSize() {
  const c = document.getElementById("mapc"), st = document.getElementById("mapstage");
  if (!c || typeof c.getContext !== "function" || !MAP) return false;
  const w = st.clientWidth || 0, h = st.clientHeight || 0;
  if (!(w > 0 && h > 0)) return false;
  const dpr = Math.min(window.devicePixelRatio || 1, MAP_DPR_MAX);
  c.width = Math.round(w * dpr);
  c.height = Math.round(h * dpr);
  c.dataset.w = w;
  c.dataset.h = h;
  MAP_FIT = Math.min((w - MAP_PAD * 2) / (MAP.x1 - MAP.x0), (h - MAP_PAD * 2) / (MAP.y1 - MAP.y0));
  return true;
}

// The camera that frames a box of layout units in the stage, which is one function for two jobs: the reset
// frames the whole layout, and a search frames the rows it found. `zoom` is capped at the fit scale for the
// second job -- twelve projects in one neighbourhood would otherwise fill the stage at 40x and lose every
// piece of context that made the answer legible.
function mapFrameOn(x0, y0, x1, y1, maxScale) {
  const c = document.getElementById("mapc");
  const w = +c.dataset.w, h = +c.dataset.h;
  const k = Math.min(maxScale, (w - MAP_PAD * 2) / Math.max(x1 - x0, 1e-6),
                     (h - MAP_PAD * 2) / Math.max(y1 - y0, 1e-6));
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  return {k, ox: w / 2 - cx * k, oy: h / 2 + cy * k};
}

// The bounding box of a set of rows, padded by a tenth of its own size so the outermost dot is not on the
// frame. Null for an empty set, which is the render where nothing matched: there is no answer to frame, so
// the camera stays where it is and the whole sky stays dim.
function mapBoxOf(rows) {
  if (!rows.length) return null;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const r of rows) {
    const x = MAP.x[r.ord], y = MAP.y[r.ord];
    if (x < x0) x0 = x;
    if (x > x1) x1 = x;
    if (y < y0) y0 = y;
    if (y > y1) y1 = y;
  }
  const m = Math.max((x1 - x0) * 0.1, (y1 - y0) * 0.1, 0.4);
  return [x0 - m, y0 - m, x1 + m, y1 + m];
}

// The swing onto a search's answer, and the only animation in this module. Gated on the reader's own
// preference in JavaScript, because the blanket `prefers-reduced-motion` rule in the stylesheet collapses
// CSS durations and has no reach into a `requestAnimationFrame` loop -- and gated on `requestAnimationFrame`
// existing at all, which under `tests/probe.mjs` it does not.
function mapFly(to) {
  const from = MAP_CAM, id = ++MAP_FLIGHT;
  const still = typeof requestAnimationFrame !== "function" ||
    (typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion:reduce)").matches);
  if (still) { MAP_CAM = to; mapPaint(); return; }
  const t0 = Date.now();
  const step = () => {
    // A second flight started while this one was in the air -- a reader who typed again, or pressed a topic.
    // The newer camera is the right one, so this frame is simply dropped rather than fighting it.
    if (id !== MAP_FLIGHT) return;
    const t = Math.min(1, (Date.now() - t0) / MAP_FLY);
    // Cubic ease-out. The interesting frames of a zoom are the ones at the end.
    const e = 1 - Math.pow(1 - t, 3);
    MAP_CAM = {k: from.k + (to.k - from.k) * e, ox: from.ox + (to.ox - from.ox) * e,
               oy: from.oy + (to.oy - from.oy) * e};
    mapPaint();
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// Everything on screen, in one pass, from `HITS` and the camera. No caching and no dirty rectangles: the
// whole picture is 1,294 dots and about 10,000 hairlines, which is one `beginPath` and two `stroke` calls,
// and the first draft that cached the edge layer to an offscreen canvas was slower than not caching it
// because the invalidation ran on every zoom.
function mapPaint() {
  const c = document.getElementById("mapc");
  if (!MAP || !c || typeof c.getContext !== "function" || !MAP_CAM) return;
  const ctx = c.getContext("2d");
  if (!ctx) return;
  const w = +c.dataset.w, h = +c.dataset.h;
  const dpr = c.width / (w || 1), p = mapPalette();
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = p.back;
  ctx.fillRect(0, 0, w, h);
  // Lit by ordinal rather than by a Set of names: `match` has already run 1,294 times this render and this
  // is 1,294 more array writes against 1,294 hash lookups per dot drawn.
  const lit = new Uint8Array(ROWS.length);
  for (const r of HITS) lit[r.ord] = 1;
  const n = MAP.n, rows = ROWS.length;

  // ── the sky ──
  // Every edge in `near.bin`, at an alpha low enough that no single one is visible and all 10,352 together
  // are. This is the layer that turns a scatter plot into something worth looking at, and it costs one path.
  ctx.lineWidth = 1;
  ctx.strokeStyle = p.grid;
  ctx.globalAlpha = p.light ? 0.5 : 0.34;
  ctx.beginPath();
  for (let i = 0; i < rows; i++) {
    const ax = mapX(MAP.x[i]), ay = mapY(MAP.y[i]);
    for (let k = 0; k < n; k++) {
      const j = MAP.near[i * n + k];
      ctx.moveTo(ax, ay);
      ctx.lineTo(mapX(MAP.x[j]), mapY(MAP.y[j]));
    }
  }
  ctx.stroke();
  ctx.globalAlpha = 1;

  // ── the dots ──
  // Unlit first, so a lit dot is never painted under one that is not part of the answer. Radius grows with
  // the log of the star count, floored at 1.6 px: the atlas spans 8 stars to 388,645, and a linear radius
  // would make one dot the size of the stage and the rest invisible.
  const rad = i => {
    const s = ROWS[i].stars || 0;
    return 1.6 + Math.min(4.4, Math.log10(s + 1) * 0.85);
  };
  for (let pass = 0; pass < 2; pass++) {
    for (let i = 0; i < rows; i++) {
      if (!!lit[i] !== !!pass) continue;
      const px = mapX(MAP.x[i]), py = mapY(MAP.y[i]);
      if (px < -8 || py < -8 || px > w + 8 || py > h + 8) continue;
      ctx.beginPath();
      ctx.arc(px, py, pass ? rad(i) : 1.5, 0, 6.283185307179586);
      ctx.fillStyle = "hsl(" + mapHue(ROWS[i].cat) + "," + (pass ? "72%," : "18%,") +
        (pass ? p.lit : p.dim) + "%)";
      ctx.fill();
    }
  }

  // ── the one project the reader is asking about ──
  const focus = MAP_HOT >= 0 ? MAP_HOT : MAP_PIN;
  if (focus >= 0) {
    const fx = mapX(MAP.x[focus]), fy = mapY(MAP.y[focus]);
    const hue = mapHue(ROWS[focus].cat);
    // In-edges first and faint: every row that named this one. Drawn underneath the eight it names, so a hub
    // reads as a bright star of eight inside a haze of everything pointing at it.
    //
    // Dashed as well as faint, which is the second channel and not decoration. Direction is the whole claim
    // these two passes make -- "names" and "is named by" are different facts -- and encoding it in alpha
    // alone puts it in the one channel a dim screen, a bright room or a colour-vision difference takes away
    // first. The comparison panel's `≠` makes the same argument against colour-only marks and this repository
    // already tests for it. Set once and cleared after the solid pass, because `setLineDash` is context state
    // and a leaked dash would turn every ring below into a dotted circle.
    ctx.strokeStyle = "hsl(" + hue + ",70%," + (p.light ? 46 : 58) + "%)";
    ctx.globalAlpha = 0.22;
    ctx.setLineDash([3, 4]);
    ctx.beginPath();
    for (let i = 0; i < rows; i++)
      for (let k = 0; k < n; k++)
        if (MAP.near[i * n + k] === focus) {
          ctx.moveTo(fx, fy);
          ctx.lineTo(mapX(MAP.x[i]), mapY(MAP.y[i]));
        }
    ctx.stroke();
    // The eight it names, solid, with each one ringed. These are the projects the atlas is claiming are the
    // nearest to this one -- not the nearest dots, which is the whole reason they are drawn rather than left
    // for the eye to guess.
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    for (let k = 0; k < n; k++) {
      const j = MAP.near[focus * n + k];
      ctx.moveTo(fx, fy);
      ctx.lineTo(mapX(MAP.x[j]), mapY(MAP.y[j]));
    }
    ctx.stroke();
    // Each of the eight is then *emptied* -- filled with the stage's own colour and ringed -- rather than
    // merely circled. Taken from the way a graph view draws a local neighbourhood: the hub is solid and its
    // neighbours are hollow, so which node the picture is about is answered by shape before colour. A ring
    // around a dot that still looks like all 1,294 other dots is a mark the eye has to hunt for; a hollow
    // dot in a field of filled ones is the only thing of its kind on screen.
    for (let k = 0; k < n; k++) {
      const j = MAP.near[focus * n + k];
      const jx = mapX(MAP.x[j]), jy = mapY(MAP.y[j]), jr = rad(j) + 2.6;
      ctx.beginPath();
      ctx.arc(jx, jy, jr, 0, 6.283185307179586);
      ctx.fillStyle = p.plane;
      ctx.fill();
      ctx.stroke();
    }
    // And the hub carries a glow, which is the one place on this canvas a shadow is worth its cost: it is
    // drawn once, on a single arc, and it is what makes the focused project findable after the reader's eye
    // has followed an edge to the far side of the map. Reset immediately -- `shadowBlur` is context state and
    // the label plates below would each acquire a halo.
    ctx.beginPath();
    ctx.arc(fx, fy, rad(focus) + 4.5, 0, 6.283185307179586);
    ctx.lineWidth = 2;
    ctx.strokeStyle = p.ink;
    ctx.shadowColor = "hsl(" + hue + ",70%,50%)";
    ctx.shadowBlur = 12;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.lineWidth = 1;
    // What is deliberately *not* borrowed: the twinkle, the bobbing neighbours and the marching-ants edges
    // that make a five-node graph-view illustration feel alive. All three are `requestAnimationFrame` for as
    // long as the map is open, on a canvas holding 1,294 dots and 10,352 edges rather than five and five --
    // and a reader who opened this to find something would be reading a moving target. The camera flight is
    // the only animation here, it is half a second long, it ends, and it asks `prefers-reduced-motion` first.
  }

  // ── the names ──
  // Twelve at most, and the labels are for orientation rather than for reading every row: this is a picture
  // of 1,294 projects and 1,294 names is a grey rectangle. The biggest lit projects, because those are the
  // ones a reader recognises and therefore the ones that tell them where they are. Placed with a rectangle
  // overlap test rather than a layout pass -- a label that would collide is dropped, which is the only
  // behaviour that keeps every label legible at every zoom.
  ctx.font = "600 11px system-ui,-apple-system,Segoe UI,sans-serif";
  ctx.textBaseline = "middle";
  const named = HITS.filter(r => {
    const px = mapX(MAP.x[r.ord]), py = mapY(MAP.y[r.ord]);
    return px > 0 && py > 0 && px < w && py < h;
  }).sort((a, b) => (b.stars || 0) - (a.stars || 0));
  const taken = [];
  if (focus >= 0) named.unshift(ROWS[focus]);
  // Twelve is the cap for a desktop stage and too many for a phone: the same twelve plates over a third of
  // the width cover the dots they are naming, which is the one thing a label must not do. So the cap is per
  // unit of stage rather than per map -- about one name per 40,000 CSS pixels, which is twelve at 1,178x632
  // and six at 375x588 -- with a floor, because a map that names nothing is a map a reader cannot orient on.
  // The collision test alone does not solve this: it keeps labels off each other, not off the picture.
  const cap = Math.max(4, Math.min(MAP_LABELS, Math.round(w * h / 40000))) + (focus >= 0 ? 1 : 0);
  let drawn = 0;
  for (const r of named) {
    if (drawn >= cap) break;
    const px = mapX(MAP.x[r.ord]), py = mapY(MAP.y[r.ord]);
    const tw = ctx.measureText(r.name).width;
    // Right of the dot, unless that would run off the canvas -- then left of it, and if neither side fits the
    // label is dropped like a colliding one. A canvas clips rather than wraps, so the version of this without
    // the flip put "Oh My Open" and "B" against the right edge on a phone: not a truncation a reader can see
    // is a truncation, because there is no ellipsis and no box, just a word that stops.
    let box = [px + rad(r.ord) + 5, py - 8, tw + 6, 16];
    if (box[0] + box[2] > w) box = [px - rad(r.ord) - 5 - (tw + 6), box[1], box[2], box[3]];
    if (box[0] < 0 || box[0] + box[2] > w) continue;
    if (taken.some(t => box[0] < t[0] + t[2] && t[0] < box[0] + box[2] &&
                        box[1] < t[1] + t[3] && t[1] < box[1] + box[3])) continue;
    taken.push(box);
    drawn++;
    // A plate under the text, not a stroke around it. An outlined glyph over ten crossing hairlines is still
    // unreadable, and the plate is the same colour as the dialog's own surfaces so it reads as part of the
    // page rather than as a sticker on the picture.
    ctx.globalAlpha = 0.82;
    ctx.fillStyle = p.plane;
    ctx.fillRect(box[0] - 3, box[1], box[2], box[3]);
    ctx.globalAlpha = 1;
    ctx.fillStyle = r.ord === focus ? p.ink : p.sub;
    ctx.fillText(r.name, box[0], py);
  }

  // The sentence, rewritten with the picture. `role="img"` and this label are the whole accessible reading of
  // a canvas, and what it says is what a reader who cannot see it actually needs: how many of how many, and
  // by which view. Every project behind it is in the table this dialog is drawn over.
  c.setAttribute("aria-label", HITS.length.toLocaleString() + " of " + rows.toLocaleString() +
    " projects lit on a map of the atlas. " + viewTitle() + ".");
}

// The row under the pointer, or -1. A linear scan of 1,294, which is not worth an index: a quadtree would be
// rebuilt on every zoom and this is two multiplies and a compare per row, on an event that fires at most once
// a frame. Nearest wins rather than first, so two overlapping dots resolve to the one being pointed at.
function mapPickAt(px, py) {
  let best = -1, bd = MAP_PICK * MAP_PICK;
  for (let i = 0; i < ROWS.length; i++) {
    const dx = mapX(MAP.x[i]) - px, dy = mapY(MAP.y[i]) - py, d = dx * dx + dy * dy;
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}

// The readout. Positioned rather than styled: it follows the pointer, flips to the other side when it would
// leave the stage, and carries the two facts about a project that only this picture can tell you -- how many
// rows it names and how many name it.
function mapTip(i, px, py) {
  const tip = document.getElementById("maptip");
  if (!tip) return;
  if (i < 0) { tip.hidden = true; return; }
  const r = ROWS[i], cat = D.cats[r.cat];
  tip.innerHTML = '<span class="tn">' + esc(r.name) + "</span>" +
    '<span class="tk">' + esc(cat ? cat.name : "") +
    (r.stars ? " · " + r.stars.toLocaleString() + "★" : "") + "</span>" +
    '<span class="tb">Names ' + MAP.n + " nearest · named by " + MAP.deg[i].toLocaleString() +
    "</span>";
  tip.hidden = false;
  const c = document.getElementById("mapc"), w = +c.dataset.w, h = +c.dataset.h;
  const bw = tip.offsetWidth || 200, bh = tip.offsetHeight || 60;
  // Placed in the quadrant that hides the least of what it is describing. Down-and-right unconditionally is
  // the obvious version and it is self-defeating here: the readout says "names 8 nearest" and the eight are
  // being drawn from this dot at that moment, so a plate 14px down-right of the pointer lands on top of
  // whichever of them go that way -- the reader is told about eight lines and shown five. So each of the four
  // corners is scored by how many of the eight it would cover, and the winner is the emptiest. Ties break
  // toward down-right, which keeps the common case where a dot has no neighbours nearby exactly as it was.
  //
  // Measured over 37 hovers -- every 40th row, at the opening fit and at 4x -- all four corners get used:
  // 18 down-right, 12 down-left, 4 up-right, 3 up-left. 18 of the 37 move off the naive placement and 26
  // neighbour dots that down-right would have hidden stay visible. Worth 32 comparisons on a pointermove.
  const dirs = [[1, 1], [-1, 1], [1, -1], [-1, -1]];
  let bestAt = null, bestHit = Infinity;
  for (const [sx, sy] of dirs) {
    const lx = Math.max(4, Math.min(w - bw - 4, sx > 0 ? px + 14 : px - 14 - bw));
    const ly = Math.max(4, Math.min(h - bh - 4, sy > 0 ? py + 14 : py - 14 - bh));
    let hit = 0;
    for (let k = 0; k < MAP.n; k++) {
      const j = MAP.near[i * MAP.n + k], jx = mapX(MAP.x[j]), jy = mapY(MAP.y[j]);
      if (jx >= lx && jx <= lx + bw && jy >= ly && jy <= ly + bh) hit++;
    }
    if (hit < bestHit) { bestHit = hit; bestAt = [lx, ly]; }
    if (bestHit === 0) break;
  }
  tip.style.left = bestAt[0] + "px";
  tip.style.top = bestAt[1] + "px";
}

// A pinned dot, and the button that hands its neighbourhood back to the table. `state.list` is the mechanism
// a shared `#list=` link already uses, so a neighbourhood found on the map becomes a filtered view of the
// table -- and a filtered view of the table is a link. That is the whole round trip: search by meaning, see
// where the answer lives, take the neighbourhood away as a URL.
function mapPin(i) {
  MAP_PIN = i;
  const b = document.getElementById("mapnear");
  if (!b) return;
  // Behind the export flag, not because the button needs the dialog but because `state.list` is only carried
  // in the hash when that flag is on -- see `readHash`. A filter that vanishes from the URL it put itself in
  // is worse than no button.
  if (i < 0 || !FLAGS["index.export"]) { b.hidden = true; return; }
  b.hidden = false;
  b.textContent = "Show " + ROWS[i].name + " and its " + MAP.n + " nearest in the table";
  b.onclick = () => {
    const keep = new Set([ROWS[i].nwo]);
    for (let k = 0; k < MAP.n; k++) keep.add(ROWS[MAP.near[i * MAP.n + k]].nwo);
    // Every other filter cleared, which is the only honest reading of this button: a neighbourhood crossed
    // with a search the reader typed ten seconds ago is neither of the two things they asked for.
    set({list: keep, q: "", cat: "", tgt: "", os: [], strict: false, fresh: false, since: false,
         rising: false, saved: false});
    document.getElementById("mapdlg").close();
    say(keep.size.toLocaleString() + " projects shown — " + ROWS[i].name + " and its nearest neighbours.");
  };
}

// The key, built once from `D.cats` and repainted by `render()` like everything else. Each pill is the same
// filter as the topic chip of that name on the bar, which is what makes the map's structure reachable without
// a pointer: the dots cannot be tabbed to and the territories can.
function mapKey() {
  const box = document.getElementById("mapkey");
  if (!box || !D) return;
  const count = new Uint16Array(D.cats.length);
  for (const r of HITS) count[r.cat]++;
  if (!box.children.length) {
    box.innerHTML = D.cats.map((c, i) =>
      '<button type="button" data-cat="' + esc(c.slug) + '" aria-pressed="false" style="--sw:hsl(' +
      mapHue(i).toFixed(1) + ',72%,58%)"><i aria-hidden="true"></i><span>' + esc(c.name) +
      '</span> <span class="kn"></span></button>').join("");
    for (const b of box.querySelectorAll("button"))
      b.onclick = () => set({cat: b.dataset.cat === state.cat ? "" : b.dataset.cat});
  }
  const btns = box.querySelectorAll("button");
  for (let i = 0; i < btns.length; i++) {
    btns[i].setAttribute("aria-pressed", D.cats[i].slug === state.cat ? "true" : "false");
    const n = btns[i].querySelector(".kn");
    if (n) n.textContent = count[i] ? count[i].toLocaleString() : "";
  }
}

// Called from `render()` on the way out. Only when the dialog is open: a closed dialog is a canvas nobody is
// looking at, and `mapOpen` paints before it shows.
function mapRepaint() {
  const dlg = document.getElementById("mapdlg");
  if (MAP_STATE !== "live" || !dlg || !dlg.open) return;
  const what = document.getElementById("mapwhat");
  if (what)
    what.innerHTML = "<b>" + HITS.length.toLocaleString() + "</b> of <b>" +
      ROWS.length.toLocaleString() + "</b> lit · " + esc(viewTitle());
  mapKey();
  // The camera follows the answer, which is the point of pressing Map with a search in the box -- and it
  // follows the answer *back*, which is less obvious and was a real bug. Clearing a search after flying into
  // a nine-row neighbourhood used to repaint 1,294 lit dots through a camera still framed on nine of them:
  // the reader had asked to see everything and was shown one dense green corner, which does not read as
  // "zoomed in", it reads as "this is the atlas". So both directions fly, and the whole-layout fit is where
  // "everything is lit" and "nothing is lit" both land. Not called on a pan or a zoom -- only `render()`
  // reaches here, so the reader's own camera is never taken off them mid-gesture.
  const box = HITS.length && HITS.length < ROWS.length ? mapBoxOf(HITS) : null;
  mapFly(box ? mapFrameOn(box[0], box[1], box[2], box[3], MAP_FIT * 7)
             : mapFrameOn(MAP.x0, MAP.y0, MAP.x1, MAP.y1, MAP_FIT));
}

function mapOpen() {
  const dlg = document.getElementById("mapdlg"), nope = document.getElementById("mapnope");
  dlg.showModal();
  document.getElementById("maphint").textContent =
    "Hover a project to see the eight it is nearest. Drag to pan, scroll to zoom, click to pin.";
  loadMap().then(st => {
    if (!dlg.open) return;
    if (st !== "live" || !mapSize()) {
      // The one thing a reader who pressed this deserves: which of the two reasons it is empty. A flag that
      // is off never shows the chip at all, so the only way to be here is a guard that fired.
      nope.hidden = false;
      nope.textContent = "The map is drawn from the same index as search by meaning, and that index does " +
        "not match the projects on this page — so every dot would be in the wrong place. The console says " +
        "which check failed. Everything the map would show is in the table behind this.";
      document.getElementById("mapkey").hidden = true;
      document.getElementById("maphint").textContent = "";
      return;
    }
    nope.hidden = true;
    MAP_HOT = -1;
    mapPin(-1);
    MAP_CAM = mapFrameOn(MAP.x0, MAP.y0, MAP.x1, MAP.y1, MAP_FIT);
    // Straight to the fit before anything else, so the first frame is the whole atlas -- then `mapRepaint`
    // flies from there onto whatever the table is currently showing. Opening on the answer with no
    // establishing shot is a picture a reader cannot place.
    mapPaint();
    mapRepaint();
  });
}

function mapWire() {
  if (!FLAGS["index.constellation"]) return;
  const dlg = document.getElementById("mapdlg"), chip = document.getElementById("mapbtn");
  const c = document.getElementById("mapc");
  // The capability, never the element: `getElementById` returns something for every id under the stub DOM in
  // `tests/probe.mjs`, so a null test proves nothing and `getContext` is the question actually being asked.
  if (!dlg || !dlg.showModal || !c || typeof c.getContext !== "function") return;
  chip.classList.add("on");
  chip.onclick = mapOpen;
  document.getElementById("mapdone").onclick = () => dlg.close();
  document.getElementById("mapreset").onclick = () => {
    if (MAP_STATE !== "live") return;
    MAP_HOT = -1;
    mapPin(-1);
    mapTip(-1);
    mapFly(mapFrameOn(MAP.x0, MAP.y0, MAP.x1, MAP.y1, MAP_FIT));
  };
  // Nothing pinned when the dialog shuts, so reopening it is the atlas rather than the last thing somebody
  // clicked a session ago.
  dlg.addEventListener("close", () => { MAP_HOT = -1; mapPin(-1); mapTip(-1); });

  let drag = null;
  const at = e => {
    const b = c.getBoundingClientRect();
    return [e.clientX - b.left, e.clientY - b.top];
  };
  c.addEventListener("pointerdown", e => {
    if (MAP_STATE !== "live") return;
    const [px, py] = at(e);
    // Where the pointer went down, and whether it has moved since. A click is a pointerup that never became
    // a drag, which is the only way to have both a pin and a pan on the same button.
    drag = {px, py, ox: MAP_CAM.ox, oy: MAP_CAM.oy, moved: false};
    c.setPointerCapture(e.pointerId);
  });
  c.addEventListener("pointermove", e => {
    if (MAP_STATE !== "live" || !MAP_CAM) return;
    const [px, py] = at(e);
    if (drag) {
      if (Math.abs(px - drag.px) + Math.abs(py - drag.py) > 3) {
        drag.moved = true;
        c.classList.add("drag");
      }
      if (drag.moved) {
        MAP_CAM = {k: MAP_CAM.k, ox: drag.ox + (px - drag.px), oy: drag.oy + (py - drag.py)};
        mapTip(-1);
        mapPaint();
        return;
      }
    }
    const i = mapPickAt(px, py);
    // Repainted only when the answer changed. A pointermove that stays on the same dot is the common case and
    // redrawing 10,000 edges for it would make the map feel heavy for no visible difference.
    if (i !== MAP_HOT) { MAP_HOT = i; mapPaint(); }
    mapTip(i, px, py);
  });
  c.addEventListener("pointerup", e => {
    if (!drag) return;
    const moved = drag.moved;
    drag = null;
    c.classList.remove("drag");
    if (moved || MAP_STATE !== "live") return;
    const [px, py] = at(e);
    const i = mapPickAt(px, py);
    // A click on empty sky unpins, which is the gesture a reader tries first and the only one that does not
    // need a button.
    mapPin(i === MAP_PIN ? -1 : i);
    mapPaint();
  });
  c.addEventListener("pointerleave", () => { MAP_HOT = -1; mapTip(-1); mapPaint(); });
  c.addEventListener("wheel", e => {
    if (MAP_STATE !== "live" || !MAP_CAM) return;
    // Not passive, and preventDefault, because a wheel over the map means zoom -- and without this the same
    // gesture scrolls the dialog's own key strip out from under the picture.
    e.preventDefault();
    const [px, py] = at(e);
    // deltaMode 1 is lines rather than pixels, which is Firefox on most configurations: a raw deltaY of 3
    // there and 100 in Chromium is a 30x difference in zoom speed for one turn of the same wheel.
    const step = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY;
    mapZoomBy(Math.exp(-step / 420), px, py);
  }, {passive: false});
  // The keyboard, on the canvas's own container rather than the document, so the arrows still move a caret
  // in anything the dialog might grow later. Everything the pointer can do except pick a dot, which is the
  // one gesture with no keyboard equivalent -- and the reason the key below is buttons and the table is
  // behind it.
  dlg.addEventListener("keydown", e => {
    if (MAP_STATE !== "live" || !MAP_CAM) return;
    const w = +c.dataset.w, h = +c.dataset.h;
    const pan = (dx, dy) => { MAP_CAM = {k: MAP_CAM.k, ox: MAP_CAM.ox + dx, oy: MAP_CAM.oy + dy};
                              mapPaint(); };
    const step = e.shiftKey ? 160 : 60;
    if (e.key === "ArrowLeft") pan(step, 0);
    else if (e.key === "ArrowRight") pan(-step, 0);
    else if (e.key === "ArrowUp") pan(0, step);
    else if (e.key === "ArrowDown") pan(0, -step);
    else if (e.key === "+" || e.key === "=") mapZoomBy(1.35, w / 2, h / 2);
    else if (e.key === "-" || e.key === "_") mapZoomBy(1 / 1.35, w / 2, h / 2);
    else return;
    e.preventDefault();
  });
  // A resize while the map is open, which on a phone is every rotation and on a desktop is a dragged window
  // corner. `ResizeObserver` where there is one because the stage can change size without the window doing
  // so -- the key strip wraps to a second row and takes 22 px off the picture -- and the window event
  // where there is not.
  const refit = () => {
    if (!dlg.open || MAP_STATE !== "live" || !mapSize()) return;
    // The camera is kept, not reset: a reader who has zoomed into observability and then widened the window
    // has not asked to be sent back to the whole atlas.
    mapPaint();
  };
  if ("ResizeObserver" in window) new ResizeObserver(refit).observe(document.getElementById("mapstage"));
  else window.addEventListener("resize", refit);
}

// Zoom about a point, so the thing under the pointer stays under it. Clamped in multiples of the fit scale
// rather than in absolute units, because what "too far out" means is a function of the stage size.
function mapZoomBy(f, px, py) {
  const k = Math.max(MAP_FIT * MAP_ZOOM_OUT, Math.min(MAP_FIT * MAP_ZOOM_IN, MAP_CAM.k * f));
  const r = k / MAP_CAM.k;
  MAP_CAM = {k, ox: px - (px - MAP_CAM.ox) * r, oy: py - (py - MAP_CAM.oy) * r};
  mapPaint();
}

// Trigram overlap, not Levenshtein: "langraph" vs "LangGraph" is one deletion but "claude cdoe" vs
// "Claude Code" is a transposition inside a two-word name, and trigrams handle both without a matrix.
// Padding with spaces makes the first and last characters count, which is where typos cluster.
// Only ever runs on an empty table, so 1,294 set builds is a few milliseconds nobody waits for -- and it
// is memoised on the row anyway, because a reader who mistypes once usually mistypes twice.
function grams(s) {
  const p = " " + s.toLowerCase().replace(/\s+/g, " ").trim() + " ", out = new Set();
  for (let i = 0; i + 3 <= p.length; i++) out.add(p.slice(i, i + 3));
  return out;
}

// Rows matching every filter *except* the search box. Both fallbacks below need exactly this set, and
// they need it for the same reason: a reader who has picked a topic and an OS has told us something they
// meant, so the term that failed is the one to relax and the other filters stand.
//
// Mutate-restore rather than a `match` that takes the query as an argument, which is `countWith`'s
// argument above and the same one -- `match` runs once per row per keystroke and threading a parameter
// through it to serve two paths that only fire on a thin table is the wrong trade.
function poolWithoutQuery() {
  const saved = state.q;
  state.q = "";
  const pool = ROWS.filter(match);
  state.q = saved;
  return pool;
}

// Rows matching every filter *except* the search box, ranked by how close their name is to what was
// typed. Only ever called when the exact pass returned nothing, which is what makes it safe: a query that
// does match is never diluted with approximate results, and the cost is paid on the one render where the
// reader would otherwise be staring at an empty table.
function near(q) {
  const want = grams(q);
  // Under three trigrams is a five-character fragment -- a prefix someone is mid-way through typing
  // rather than a misspelling of anything, and matching it loosely would be noise.
  if (want.size < 3) return [];
  const pool = poolWithoutQuery();
  const out = [];
  for (const r of pool) {
    if (!r.g) r.g = grams(r.name);
    let hit = 0;
    want.forEach(g => { if (r.g.has(g)) hit++; });
    // Divided by the larger of the two so a long name cannot win by containing a short query, which is
    // what an unnormalised count does -- every three-letter search matched the longest title on the page.
    const score = hit / Math.max(want.size, r.g.size);
    if (score >= 0.3) { r.rel = score; out.push(r); }
  }
  // Capped, because past the first handful these stop being plausible corrections and start being a
  // second way to say "nothing matched".
  return out.sort(SORTS.relevance).slice(0, 12);
}

// Where a query word landed, in descending order of what that tells us. A word in the project's own name
// is the strongest signal available; a word in the list of source lists that named it is the weakest,
// because every row from that list shares it. A prefix outranks a mid-word hit because that is how people
// type -- "lang" is someone reaching for LangGraph, not for the word "multi-language" in a blurb.
//
// The numbers are ordinal, not measured. What matters is the gaps: a name hit must be unreachable by any
// number of blurb hits, or a project merely *described* as an orchestrator outranks the one called it.
function hitScore(r, w) {
  if (r.lname === w) return 120;
  if (r.lname.startsWith(w)) return 90;
  const n = r.lname.indexOf(w);
  // A word boundary is anything that is not alphanumeric, so "code" scores as a word in "Claude Code"
  // and "Claude-Code" alike, but not inside "Decoder".
  if (n > 0) return /[a-z0-9]/.test(r.lname[n - 1]) ? 45 : 70;
  if (r.lnwo.includes(w)) return 30;
  if ((r.lang || "").toLowerCase() === w) return 20;
  const b = r.lblurb.indexOf(w);
  if (b === 0) return 12;
  if (b > 0) return /[a-z0-9]/.test(r.lblurb[b - 1]) ? 6 : 12;
  if ((r.listed_by || "").toLowerCase().includes(w)) return 2;
  return 0;
}

// Summed over the query's words, so two name hits beat one. The star bonus is logarithmic and deliberately
// small: it settles ties between rows that matched the same way, and log10 tops out near 5.5 even for a
// 300,000-star project, so it can never lift a blurb hit above a name hit. Linear stars would have made
// this a star sort wearing a relevance label.
//
// `sense` is the cosine from `senseHits`, and it is passed in rather than read off the row so that a
// stale score from the previous query cannot be blended into this one: it is a number only on the renders
// where meaning actually ran, and 0 on every other. Weighted so that a *perfect* match by meaning ties
// with a query word at the start of the name -- see `SEM_LIFT`. Rows meaning contributed score nothing
// lexically at all, so without the blend they would sort below every exact match rather than among them,
// and the whole point of the result set is that the two kinds are comparable.
function relevance(r, words, sense) {
  let total = 0;
  for (const w of words) total += hitScore(r, w);
  return total + (sense ? SEM_LIFT * (r.sem || 0) : 0) + Math.log10((r.stars || 0) + 1);
}

const SORTS = {
  // `rel` is written onto the row once per render rather than computed inside the comparator, which would
  // score each row the O(log n) times the sort happens to compare it.
  relevance: (a, b) => b.rel - a.rel || b.stars - a.stars || a.name.localeCompare(b.name),
  stars: (a, b) => b.stars - a.stars || a.name.localeCompare(b.name),
  // `gkey` is written onto the row once per load rather than computed here, for the reason `rel` is: a
  // comparator runs O(n log n) times. Ties fall through to the star sort and not to the name, so the rows
  // with no history -- which all share the one sentinel -- come out in the order the page opens on instead
  // of alphabetically, which would read as a second and wrong ranking.
  rising: (a, b) => b.gkey - a.gkey || SORTS.stars(a, b),
  lists: (a, b) => b.lists - a.lists || b.stars - a.stars,
  pushed: (a, b) => (b.pushed || "").localeCompare(a.pushed || "") || b.stars - a.stars,
  name: (a, b) => a.name.localeCompare(b.name),
};

const SORT_KEYS = Object.keys(SORTS);

// Best match with an empty search box has nothing to rank, so it means Most stars until there is a query.
// Resolved here rather than by rewriting `state.sort`, so that clearing the box and typing again returns
// the reader to ranking instead of silently stranding them on a star sort they never chose.
function effSort() {
  return state.sort === "relevance" && !state.q ? "stars" : state.sort;
}

// The Saved chip, its count, and the Remove-all button beside it. Called from `render()` and nowhere else,
// which is the same argument the chip reflection above it makes: `render()` is the one function every path
// that changes anything already ends at, so a press, a hashchange and the back button all arrive here
// without each of them remembering to.
//
// The chip is absent at zero rather than disabled. That is the pattern the New and Rising chips set -- a
// control that selects nothing is worse than no control -- but the reason it has to be re-decided on every
// render, instead of once in `buildChips` like those two, is that this count is the only one on the bar the
// reader can change. It goes from absent to present on the first press of a Save button.
//
// The filter is dropped here too, and this is the subtle half. Un-saving the last row while the saved filter
// is on would otherwise leave `state.saved` true over an empty set: the chip vanishes, the table empties, and
// the control that would have turned the filter back off has gone with it. So emptying the set turns the
// filter off in the same pass. `writeHash` is called because `state` changed and the URL still said
// `#saved=1`; `render()` is not, because this runs inside it.
function paintSaved() {
  const n = SAVED.size;
  if (!n && state.saved) { state.saved = false; writeHash(); }
  const chip = document.getElementById("saved");
  chip.classList.toggle("on", n > 0);
  chip.setAttribute("aria-pressed", state.saved ? "true" : "false");
  document.getElementById("savedlabel").textContent = n ? "Saved · " + n.toLocaleString() : "Saved";
  // Only while the reader is looking at the set it would empty. Shown on the strength of the filter being on
  // rather than of the set being non-empty, so "remove everything" is never one stray click away from
  // somebody who is browsing the atlas and has not asked to see their own collection.
  document.getElementById("clearsave").classList.toggle("on", state.saved && n > 0);
}

// ---- The comparison --------------------------------------------------------------------------------------
//
// The question this page could not answer. It is good at "what are the options" -- a crossing of thirteen
// topics, twelve integrations, five platforms and a search term, which is precisely what `mega-list/` cannot
// be -- and it was no use at all for "which of these three should I pick". Answering that meant scrolling
// between rows and holding the differences in your head, and the differences are the whole of the decision.
//
// So: up to four projects in columns, every fact the atlas holds about them in rows, and a mark on every row
// they disagree on. The mark is the feature. Four projects agree about most things -- they are in the same
// topic, that is why they are being compared -- and the panel's job is to put the handful of rows that are
// actually a choice in front of the reader rather than making them find them.
//
// The selection is in the hash and nowhere else, which makes a comparison a link somebody can send. That is
// deliberately unlike `SAVED`, which is a store on one machine: a shortlist is personal, a comparison is an
// argument, and an argument that cannot be sent is half of one.

// The chip's count, the panel's visibility, and the panel. Called from `render()` like `paintSaved()` and
// `paintShared()`, and for the same reason those two are: `render()` is the one function every path that
// changes anything already ends at, so a pin, a hashchange and the back button all arrive here without each
// of them remembering to.
function paintCompare() {
  const chip = document.getElementById("cmpchip"), panel = document.getElementById("cmp");
  // Both absent means the page was built with the flag off, in which case there is nothing to paint and
  // nothing has put anything in `state.cmp` either -- `readHash` reads the same flag.
  if (!chip || !panel) return;
  // `filter(Boolean)` is belt and braces rather than a live case: `readHash` is the only door into this set and
  // it resolves every key against `BY_NWO` on the way in. It stays because the alternative -- a `null` reaching
  // the field accessors below -- is a TypeError in the middle of a paint, which takes the whole table with it.
  const picks = [...state.cmp].map(k => BY_NWO.get(k)).filter(Boolean);
  const n = picks.length;
  chip.classList.toggle("on", n > 0);
  document.getElementById("cmplabel").textContent = n ? "Compare · " + n : "Compare";
  const open = n > 0 && CMP_OPEN;
  chip.setAttribute("aria-expanded", open ? "true" : "false");
  panel.classList.toggle("on", open);
  // Nothing is built for a closed panel. It is up to thirteen rows of markup that no one is looking at, and
  // rebuilt on every keystroke by the `render()` that calls this.
  if (!open) return;
  const built = cmpTable(picks);
  document.getElementById("cmptable").innerHTML = built.html;
  // The count of differing rows, said in words, because it is the one thing about the panel a reader wants
  // before they start reading it -- and because on a phone the marks are down the sticky left column and the
  // reader may be three swipes to the right of them. "Nothing here differs" is a real answer and worth saying
  // plainly: it means the choice is not in this table, which is itself useful.
  document.getElementById("cmpwhat").innerHTML = n === 1
    ? "Pin up to " + (CMP_MAX - 1) + " more to compare <b>" + esc(picks[0].name) + "</b> against them."
    : "<b>" + n + " projects</b> · " + (built.differs
        ? built.differs + " of " + built.total + (built.differs === 1 ? " row differs" : " rows differ")
        : "every row agrees");
}

// One row per fact, as `[label, accessor]`, where the accessor returns the cell's markup *and* the plain string
// the difference test compares. The two are separate on purpose and it is the subtle part of this panel: the
// test has to run on what the reader can see, not on what the data holds underneath it. Two projects pushed
// nine and eleven days apart are both "1mo ago", and a `≠` beside two visibly identical cells does not read as
// a precise mark -- it reads as a mark that means nothing, and then none of the others are believed either.
// So `pushed` compares its rendered text (see `sinceText`), and the verdicts compare their word rather than
// their letter, because `-` and `a` used to draw the same dash and one of them was the more common.
//
// Built per call rather than once, because `D.os` and `D.cats` only exist after `data.json` lands and the list
// depends on both -- and because `hasCmds()` is a fact about the current view.
function cmpFields(picks) {
  const plain = s => ({html: esc(s), key: s});
  const f = [
    ["Stars", r => plain(r.stars ? r.stars.toLocaleString() : "—")],
    ["Named by", r => plain(r.lists + (r.lists === 1 ? " list" : " lists"))],
    ["Topic", r => plain(D.cats[r.cat].name)],
    ["Plugs into", r => plain(r.targets.length ? r.targets.map(t => D.targets[t].name).join(", ") : "—")],
  ];
  // Five rows and not one, because "which platforms does this run on" is five separate questions and the
  // reader comparing four projects is usually only asking one of them. One row of five glyphs per project
  // would put the answer they want inside a string they have to parse, and would mark the row as differing
  // when the difference is on a platform they do not use.
  //
  // The glyph is drawn *and* the word is written out, which the table view does not do -- there the word is in
  // a `title` and in an `.sr` span, because five words per row across 120 rows is a column nobody can scan.
  // Here there are four columns and thirteen rows and the reader is reading rather than scanning, so the word
  // is the cell and the glyph is the mark beside it. `osIcon` is left out for the same reason: the platform is
  // named once in the row label, and repeating its icon in all four cells is four pictures saying what the
  // label already said.
  D.os.forEach((o, k) => f.push([o, r => {
    const v = VERDICT[r.os[k]] || ["–", "not established"];
    return {html: '<span class="v' + esc(r.os[k]) + '" aria-hidden="true">' + v[0] + "</span> " + esc(v[1]),
            key: v[1]};
  }]));
  f.push(["Language", r => plain(r.lang || "—")]);
  f.push(["Licence", r => plain(r.license || "—")]);
  f.push(["Last push", r => ({html: since(r.pushed), key: sinceText(r.pushed)})]);
  // Both halves of the condition matter, which is the same test `hasCmds()` makes for the export: the flag can
  // be off, and on a comparison where no pinned project has a detected command the row would be a label and
  // four dashes. `hasCmds()` itself is not reusable here -- it asks about `HITS`, and a pinned project need not
  // be on screen at all, which is the point of pinning it.
  if (FLAGS["index.install_commands"] && picks.some(r => r.install))
    f.push(["Install", r => r.install
      ? {html: "<code>" + esc(r.install) + "</code>", key: r.install}
      : plain("—")]);
  return f;
}

// The panel's table, and the count of rows that differ.
//
// A one-project comparison has no differences by construction, and the guard is not just an optimisation: with
// `picks.length === 1` every `Set` of one value has size 1, so the arithmetic already gives zero -- but saying
// it out loud is what stops a future edit that compares against a default from marking all thirteen rows on a
// panel holding a single project.
function cmpTable(picks) {
  const head = picks.map(r =>
    '<th scope="col"><a href="' + detailURL(r.nwo) + '">' + esc(r.name) + "</a>" +
    '<span class="meta">' + esc(r.nwo) + "</span>" +
    // In the heading rather than only on the row's own Compare button, because the reader is looking at this
    // panel and the row it came from may be nine screens away or filtered off the page entirely. The name says
    // which project, since "Unpin" four times across a header row is not four different buttons to anyone
    // reading them one at a time.
    '<button class="chip unpin" data-nwo="' + esc(r.nwo) + '" aria-label="Take ' + esc(r.name) +
    ' out of the comparison">Unpin</button></th>').join("");
  let differs = 0;
  const fields = cmpFields(picks);
  const body = fields.map(([label, get]) => {
    const cells = picks.map(get);
    const d = picks.length > 1 && new Set(cells.map(c => c.key)).size > 1;
    if (d) differs++;
    // Two channels for the mark, never one. The 3px bar on the label cell is colour and the `≠` is not, which
    // is WCAG 1.4.1 and is also just true of the readers most likely to be using this panel: somebody
    // comparing four things at once is doing it because holding them in their head is not working, and a cue
    // they cannot perceive is not a cue. The glyph is `aria-hidden` and the words beside it are the accessible
    // text, so a screen reader hears "Stars, these differ" rather than "Stars, not equal to".
    return "<tr" + (d ? ' class="differs"' : "") + '><th scope="row">' + esc(label) +
      (d ? '<span class="dx" aria-hidden="true">≠</span><span class="sr">, these differ</span>' : "") +
      "</th>" + cells.map(c => "<td>" + c.html + "</td>").join("") + "</tr>";
  }).join("");
  // The corner cell is empty on screen and named for a screen reader, which is the standard shape for a matrix
  // like this: leaving it bare makes the first column a set of row headers with no column header at all.
  return {
    html: '<table><thead><tr><th scope="col"><span class="sr">What is being compared</span></th>' + head +
          "</tr></thead><tbody>" + body + "</tbody></table>",
    differs: differs,
    total: fields.length,
  };
}

// One row's Save button. A function declaration so it hoists above `render()`, which is the only caller.
//
// The accessible name says which project, because a screen-reader user reaches this button once per row and
// "Save" 120 times in a column is not a name. The visible word stays short, since it sits inline after an
// `owner/name` that is already long, and the two do not have to match: `aria-label` replaces the text for
// assistive technology rather than adding to it.
//
// `data-nwo` and not a row index. `render()` re-sorts and re-filters on every keystroke, so an index is only
// valid until the next one -- and the click handler is delegated, which means it reads this attribute from a
// DOM node that may have been rewritten between the press and the read.
function saveBtn(r) {
  const on = SAVED.has(r.nwo);
  return '<button class="save" data-nwo="' + esc(r.nwo) + '" data-name="' + esc(r.name) +
    '" aria-pressed="' + (on ? "true" : "false") + '" aria-label="' + esc(saveLabel(r.name, on)) + '">' +
    saveWord(on) + "</button>";
}

// The visible word and the accessible name, from one place, because `toggleSave` rewrites both in the DOM
// while `saveBtn` writes them as markup -- two call sites that would otherwise each carry their own copy of
// the same string and drift the first time one of them was reworded.
//
// The visible word is the first word of the label on purpose. WCAG 2.5.3 asks that a control's accessible
// name contain its visible text, so that someone driving the page by voice can say what they can see; a
// button reading "Saved" whose name was "Save LangGraph" would fail that in exactly one of its two states,
// which is the kind of bug that only shows up in the state nobody screenshots.
// Declarations rather than `const` arrows, so they hoist with `saveBtn` above them. Both are called from
// inside functions that run long after this script has evaluated, so a `const` would work today -- and would
// fail with a temporal-dead-zone error the first time somebody called either of them from a path that runs
// during evaluation, which is a trap worth simply not laying.
function saveWord(on) { return on ? "Saved" : "Save"; }
function saveLabel(name, on) { return saveWord(on) + " " + name; }

// One row's Compare button, beside its Save button, and returning "" when the flag is off -- the caller
// concatenates it either way, which is what keeps the kill switch to one line here instead of a branch in the
// middle of the row builder.
//
// `data-nwo` and `data-name` for the reason `saveBtn` gives: the handler is delegated, `render()` rewrites the
// subtree on every keystroke, and a row index is only valid until it does.
//
// The disabled state is computed per row rather than set once on the container, because "is this button
// unusable" is not a fact about the cap alone -- the four pinned rows keep working buttons at the cap, since
// theirs unpin. `full` is therefore `size >= CMP_MAX && !on`, and getting that wrong would lock the reader out
// of the only control that could unlock the rest.
function pinBtn(r) {
  if (!FLAGS["index.compare"]) return "";
  const on = state.cmp.has(r.nwo);
  const full = !on && state.cmp.size >= CMP_MAX;
  return '<button class="pin" data-nwo="' + esc(r.nwo) + '" data-name="' + esc(r.name) + '"' +
    (full ? " disabled" : "") + ' aria-pressed="' + (on ? "true" : "false") +
    '" aria-label="' + esc(pinLabel(r.name, on, full)) + '">' + pinWord(on) + "</button>";
}

// Both states' words and both states' names, from one place, for the reason `saveWord`/`saveLabel` are: the
// markup builder above and the in-place update in `togglePin` are two call sites that would otherwise each
// hold their own copy of the same string.
//
// Every branch of the name begins with the visible word, which is WCAG 2.5.3 and not a style preference: a
// reader driving this page by voice says what they can see, so a button showing "Compare" whose name was "Add
// LangGraph to the comparison" is a control they cannot address. The cap's explanation is appended to the name
// rather than replacing it, so the disabled button still says which project it is about -- a screen-reader user
// tabbing past 120 of them otherwise hears the same sentence 120 times with no way to tell them apart.
function pinWord(on) { return on ? "Comparing" : "Compare"; }
function pinLabel(name, on, full) {
  if (on) return "Comparing " + name + ", press to take it out of the comparison";
  return full ? "Compare " + name + ", unavailable: the comparison already holds " + CMP_MAX + " projects"
              : "Compare " + name;
}

// ---- Take it with you ------------------------------------------------------------------------------
//
// Everything on this page is a view: a crossing of thirteen topics, twelve integrations, five platforms, a
// search term and a sort, which is precisely the thing `mega-list/` cannot be -- a Markdown file is one topic
// or one target, never the crossing. And until now the only way to keep a view was to keep the URL. That is
// enough to come back to and no use at all for what people actually do with a shortlist: paste it into an
// issue, hand it to a colleague, print it for a meeting. A link cannot be pasted into a document, and the
// atlas behind it is 1,294 rows that move daily.
//
// So: the same view, as four documents. A link, for the reader who wants the live page. A Markdown table, for
// the issue and the README. A standalone HTML file, for the wiki and the email. And print, which is also how
// every browser makes a PDF -- there is no jsPDF here and there will not be, because this page ships zero
// third-party bytes, is cached whole by a service worker, and a 300 KB library to paginate a table the
// browser already paginates is not a trade worth making.
//
// All four are built from `HITS`, which is what `render()` last put on screen -- not from `ROWS.filter(match)`
// recomputed here. The two agree today, and the first time they did not -- a near-match pass, a sort applied
// after filtering, a cap -- the export would quietly disagree with the table the reader was looking at when
// they pressed the button, which is the one failure an export must not have.
let HITS = [];

// The current view as a sentence, and every one of the four documents is titled with it. This is not
// decoration: a file called `atlas.md` on somebody's desktop in a fortnight has to say what it is of, and
// "1,294 projects" does not. Assembled from `state` rather than from the chips' labels so that it cannot
// describe a filter that is no longer on.
function viewTitle() {
  const w = [];
  if (state.q) w.push("matching “" + state.q + "”");
  const c = state.cat && D.cats.find(x => x.slug === state.cat);
  if (c) w.push("in " + c.name);
  const t = state.tgt && D.targets.find(x => x.slug === state.tgt);
  if (t) w.push("that plug into " + t.name);
  if (state.os.length) w.push("running on " + state.os.map(i => D.os[i]).join(" and "));
  if (state.strict) w.push("with confirmed support");
  if (state.fresh) w.push("added by the latest import");
  if (state.since) w.push("added since this device last visited");
  if (state.rising) w.push("gaining stars fastest for their size");
  if (state.saved) w.push("saved on this device");
  if (state.list.size) w.push("from a shared list");
  return w.length ? "Projects " + w.join(", ") : "Every project in the atlas";
}

// The link that reproduces this view somewhere else, which is not always the URL in the address bar. There is
// exactly one case where the two differ and it is the case that matters most: `#saved=1` means "the saved
// filter is on", and on the recipient's machine that selects *their* set, which is almost always empty -- so
// the reader's most personal view is the one whose URL travels worst. A view built on the reader's own
// collection is therefore shared as the collection itself, `#list=owner/name,...`, which is the same rows on
// any machine and is what `readHash` reads back at the other end.
//
// The rows come from `HITS` and not from `SAVED`, so a saved set crossed with a topic shares the crossing --
// twelve saved projects filtered to four shares four. Everything else is already a link that means the same
// thing anywhere, and stays the one the reader can see in their address bar.
function shareURL() {
  if (!state.saved || !HITS.length) return location.href;
  const p = new URLSearchParams(location.hash.slice(1));
  p.delete("saved");
  p.delete("list");
  const rest = p.toString();
  return location.href.split("#")[0] + "#" +
    ["list=" + HITS.map(r => r.nwo).join(","), rest].filter(Boolean).join("&");
}

// A Markdown table cell ends at the next `|` and at the next newline, and both turn up in real descriptions --
// "runs foo | bar" and the occasional wrapped blurb. Escaped and flattened rather than dropped, so the text
// survives whole and the table does not lose a column halfway down.
function mdCell(s) {
  return String(s == null ? "" : s).replace(/\s+/g, " ").replace(/\|/g, "\\|").trim();
}

// The five platform verdicts as text. The glyph and not the colour, which is the same decision the table makes
// and for a reason that applies twice as hard here: an exported document has no stylesheet of ours, so colour
// is the one channel it definitely loses.
function osText(r) {
  return D.os.map((o, k) => o + " " + (VERDICT[r.os[k]] || ["–"])[0]).join(" · ");
}

// Whether the install column is worth having. Both halves matter: the flag can be off, and on a view where no
// row has a detected command the column would be nothing but a header and N dashes.
function hasCmds() {
  return !!FLAGS["index.install_commands"] && HITS.some(r => r.install);
}

// One GitHub-flavoured Markdown table, which is the dialect of every place a reader would paste this -- an
// issue, a PR body, a README, a wiki, Obsidian, a pasted snippet.
//
// The three header lines are provenance, not preamble. A table of star counts with no date on it is a table
// that will be wrong within the week, and the two dates are different facts: the snapshot is when the GitHub
// API was asked, the export date is when this file was made. The link back is what makes the document a view
// *of* something rather than a fork of it.
function listMarkdown() {
  const cmds = hasCmds();
  const row = c => "| " + c.join(" | ") + " |";
  const head = ["#", "Project", "Stars", "Lists", "Topic", "Plugs into", "Runs on"]
    .concat(cmds ? ["Install"] : []).concat(["What it does"]);
  const rule = ["--:", "---", "--:", "--:", "---", "---", "---"]
    .concat(cmds ? ["---"] : []).concat(["---"]);
  const body = HITS.map((r, i) => row([
    i + 1,
    "[" + mdCell(r.name) + "](" + r.url + ")",
    r.stars ? r.stars.toLocaleString() : "—",
    r.lists,
    mdCell(D.cats[r.cat].name),
    r.targets.map(t => mdCell(D.targets[t].name)).join(", ") || "—",
    osText(r),
  ].concat(cmds ? [r.install ? "`" + mdCell(r.install) + "`" : "—"] : [])
   .concat([mdCell(r.blurb) || "—"])));
  return ["# " + viewTitle(), "",
    HITS.length.toLocaleString() + " of " + ROWS.length.toLocaleString() +
      " projects in the [Awesome Agentic Atlas](" + shareURL() + "). Stars, language and licence come from " +
      "the GitHub API on " + SNAPSHOT + " and drift daily. Platform verdicts read ✓ stated, ? inferred from " +
      "the language, ✗ no evidence, – not established, · not applicable. Exported " + TODAY + ".", "",
    row(head), row(rule), body.join("\n"), ""].join("\n");
}

// One standalone HTML document: no stylesheet to fetch, no script, no font, nothing cross-origin, everything
// inline. That is the requirement and not a preference. This file is going to land in a wiki, an email or a
// folder on a laptop, and the failure mode of a "portable" export that pulls its stylesheet off this origin is
// that it looks right on the machine that made it and broken everywhere else -- including offline, which is
// where a saved page most often gets opened. Dark ink on white for the same reason: there is no `data-theme` at
// the other end and no toggle for the reader to reach for.
function listHTML() {
  const cmds = hasCmds();
  const cell = (c, v) => "<td" + (c ? ' class="' + c + '"' : "") + ">" + v + "</td>";
  const rows = HITS.map((r, i) =>
    "<tr>" + cell("n", i + 1) +
    cell("", '<a href="' + esc(r.url) + '">' + esc(r.name) + "</a><br><code>" + esc(r.nwo) + "</code>") +
    cell("n", r.stars ? r.stars.toLocaleString() : "—") +
    cell("n", r.lists) +
    cell("", esc(D.cats[r.cat].name)) +
    cell("", r.targets.map(t => esc(D.targets[t].name)).join(", ") || "—") +
    cell("", esc(osText(r))) +
    (cmds ? cell("", r.install ? "<code>" + esc(r.install) + "</code>" : "—") : "") +
    cell("", esc(r.blurb)) + "</tr>").join("");
  const head = ["#", "Project", "Stars", "Lists", "Topic", "Plugs into", "Runs on"]
    .concat(cmds ? ["Install"] : []).concat(["What it does"])
    .map(h => "<th>" + esc(h) + "</th>").join("");
  return '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1">' +
    "<title>" + esc(viewTitle()) + " — Awesome Agentic Atlas</title><style>" +
    "body{margin:0 auto;padding:28px 20px;max-width:1100px;background:#fff;color:#14171c;" +
    "font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}" +
    "h1{font-size:21px;margin:0 0 6px}p{color:#596574;font-size:13px;margin:0 0 4px}" +
    "a{color:#1d5e9e}code{font:12px/1.5 ui-monospace,Consolas,monospace;color:#353c47}" +
    "table{border-collapse:collapse;width:100%;margin-top:18px;font-size:13px}" +
    "th{text-align:left;border-bottom:2px solid #cad1db;padding:7px 8px;white-space:nowrap}" +
    "td{border-bottom:1px solid #e7eaf0;padding:7px 8px;vertical-align:top}" +
    ".n{text-align:right;white-space:nowrap}tr{break-inside:avoid}" +
    "</style></head><body>\n<h1>" + esc(viewTitle()) + "</h1>\n" +
    "<p>" + HITS.length.toLocaleString() + " of " + ROWS.length.toLocaleString() +
    ' projects in the <a href="' + esc(shareURL()) + '">Awesome Agentic Atlas</a>. Stars, language and ' +
    "licence come from the GitHub API on " + esc(SNAPSHOT) + " and drift daily.</p>\n" +
    "<p>Platform verdicts read ✓ stated, ? inferred from the language, ✗ no evidence, " +
    "– not established, · not applicable. " +
    "Exported " + esc(TODAY) + ".</p>\n<table><thead><tr>" + head + "</tr></thead><tbody>" + rows +
    "</tbody></table>\n</body></html>\n";
}

// The filename is the view, slugified, so a folder holding three of these says which is which. Capped at 60
// characters because a search term goes into it and a filename is not the place to discover what the operating
// system's limit is.
function fileName(ext) {
  const slug = viewTitle().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
  return "atlas-" + (slug || "export") + "-" + TODAY + "." + ext;
}

// A Blob and an object URL rather than a `data:` URI, which is the same three lines and silently fails at the
// size that matters: Chrome caps a navigated data: URL and Safari refuses one from a synthetic click, and a
// 1,294-row export is comfortably past both. Revoked on the next turn of the event loop rather than on the
// line after the click, because the browser has not necessarily finished reading the blob when this returns.
function download(name, mime, text) {
  const url = URL.createObjectURL(new Blob([text], {type: mime + ";charset=utf-8"}));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  // Appended before the click and removed after it. A detached <a> is clickable in every current engine and
  // was not in older ones, and the two lines cost nothing next to finding that out from a bug report.
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}

// The printed sheet is the table, whichever view is on screen, and the light theme whichever one the reader
// chose. Neither is a preference imposed for tidiness. A card is a box with a screenshot in it, so eight fill a
// page where the table fits twenty-five -- and the screenshots are the one thing here a printer bills for by
// the millilitre. The theme is starker still: browsers print background graphics off by default, so a
// dark-theme page prints near-white text onto white paper and hands the reader a blank sheet.
//
// `shown` is the third swap and the only one that costs anything. The page draws 120 rows and a "Show more"
// button; paper has no button, so printing the view as it stands would truncate it at 120 while the dialog that
// offered the print says how many there are. Expanded and re-rendered, then put back -- ~600ms for the full
// 1,294 on a throttled CPU, spent once, inside a gesture the reader has already accepted a print dialog for.
//
// Hung on `beforeprint` rather than done inside the Print button's handler, so that Ctrl+P, File > Print and
// the button all produce the same sheet -- the button does nothing but call `window.print()`. Safari implements
// neither event and gets the page as it stands, which is exactly the behaviour it has today.
let PRINT = null;

function printOn() {
  if (PRINT || !D) return;
  const root = document.documentElement;
  PRINT = {view: state.view, theme: root.dataset.theme, shown: state.shown};
  root.dataset.theme = "light";
  const u = document.getElementById("printurl");
  if (u) u.textContent = shareURL();
  state.view = "table";
  state.shown = Math.max(state.shown, HITS.length);
  render();
}

function printOff() {
  if (!PRINT) return;
  document.documentElement.dataset.theme = PRINT.theme;
  state.view = PRINT.view;
  state.shown = PRINT.shown;
  PRINT = null;
  // `render()` and not `applyView()` alone, because `shown` is being put back too and the rows the print
  // expanded have to come back off the page. It also restores the "Show more" button the expansion removed.
  render();
}

// The strip a shared list arrives under, and the two ways out of it. Called from `render()` like
// `paintSaved()` and for the same reason: `render()` is the one function every path that changes state already
// ends at, so a hashchange, the back button and a rescue button all arrive here without each of them
// remembering to.
//
// The first control is the one that makes the list durable, and it is first deliberately -- see `CLEAR` for why
// that placement is load-bearing rather than aesthetic. It is disabled rather than hidden once there is nothing
// left to add, so the row does not reflow under the reader's cursor between two presses.
function paintShared() {
  const strip = document.getElementById("shared");
  if (!strip) return;
  const n = state.list.size;
  strip.classList.toggle("on", n > 0);
  if (!n) return;
  const have = [...state.list].filter(k => SAVED.has(k)).length;
  document.getElementById("sharedtext").innerHTML =
    "You are looking at a shared list of <b>" + n.toLocaleString() +
    (n === 1 ? " project" : " projects") + "</b> rather than the whole atlas." +
    (have === n ? " Every one of them is already in your saved projects." : "");
  const add = document.getElementById("sharedadd");
  add.disabled = have === n;
  add.textContent = have === n ? "All saved" : "Save " + (n - have).toLocaleString() + " to my projects";
}

// What the dialog says before anything is downloaded. Rebuilt on every open rather than kept in step, because
// every fact in it -- the count, the sentence, the link -- is a function of a view the reader has been changing
// since the last time they opened it.
function expOpen() {
  const n = HITS.length;
  document.getElementById("expwhat").innerHTML =
    "<b>" + n.toLocaleString() + (n === 1 ? " project" : " projects") + "</b> · " + esc(viewTitle());
  document.getElementById("expurl").value = shareURL();
  // Disabled on an empty table, where all three would write a document with a header and no rows. The link
  // stays live: a link to an empty view is still a link to a view, and it is how a reader shows a colleague
  // that a crossing they both expected to be full is not.
  const none = n === 0;
  document.getElementById("expmd").disabled = none;
  document.getElementById("exphtml").disabled = none;
  document.getElementById("expprint").disabled = none;
  document.getElementById("exp").showModal();
}

function expWire() {
  if (!FLAGS["index.export"]) return;
  // Both of these come before the dialog guard below and stay outside it. What makes Ctrl+P produce a legible
  // sheet has nothing to do with whether this browser can open a modal, and neither does the shared-list strip
  // -- a reader who followed a `#list=` link into a browser without `<dialog>` still needs the way out of it.
  window.addEventListener("beforeprint", printOn);
  window.addEventListener("afterprint", printOff);
  document.getElementById("sharedadd").onclick = () => {
    let added = 0;
    for (const k of state.list) if (!SAVED.has(k)) { SAVED.add(k); added++; }
    storeSaved();
    say(added ? "Saved " + added.toLocaleString() + " projects to this device." : "Nothing new to save.");
    // `render()` and not `set()`: nothing about the *view* changed, so the hash is still correct and the page
    // size should not be reset under a reader who has already pressed "Show more".
    render();
  };
  document.getElementById("sharedall").onclick = () => set({list: new Set()});

  const dlg = document.getElementById("exp"), chip = document.getElementById("take");
  if (!dlg || !dlg.showModal) return;
  chip.classList.add("on");
  chip.onclick = expOpen;
  document.getElementById("expmd").onclick = () => {
    download(fileName("md"), "text/markdown", listMarkdown());
    say("Markdown table downloaded — " + HITS.length.toLocaleString() + " projects.");
  };
  document.getElementById("exphtml").onclick = () => {
    download(fileName("html"), "text/html", listHTML());
    say("HTML page downloaded — " + HITS.length.toLocaleString() + " projects.");
  };
  // Closed first. A modal <dialog> makes the page behind it inert, and several engines refuse to open a print
  // preview of an inert document -- so printing from an open dialog prints the dialog or prints nothing.
  document.getElementById("expprint").onclick = () => { dlg.close(); window.print(); };
  const copy = document.getElementById("expcopy");
  if (CAN_COPY) {
    copy.onclick = () => navigator.clipboard.writeText(shareURL())
      .then(() => say("Link copied."))
      .catch(() => {
        // The write can be refused at the moment of the click even where the API exists -- an unfocused
        // document, a denied permission -- so the failure path selects the text and says which two keys
        // finish the job, rather than reporting that something went wrong and leaving the reader there.
        const u = document.getElementById("expurl");
        u.focus();
        u.select();
        say("Could not copy. The link is selected — press " + PALMOD + " C.");
      });
  } else {
    copy.remove();
  }
  document.getElementById("expdone").onclick = () => dlg.close();
  // Clicking the backdrop, which <dialog> fires no event for: the click lands on the dialog element itself,
  // because its padding is zero and every child is inside one of the panels. Same line as the palette's.
  dlg.addEventListener("click", ev => { if (ev.target === dlg) dlg.close(); });
}

// Screenshot URLs remain deferred until a card is close to the viewport, but they begin immediately when
// it is rendered. The old interaction gate made a first-load card grid look broken until a reader happened
// to nudge a wheel. `aspect-ratio:2/1` reserves the slot while the request is in flight, so this does not
// exchange the blank-image defect for layout shift.
let ARTIO = null;

function artLoad(i) {
  i.onerror = () => {
    i.hidden = true;
    const fallback = document.createElement("span");
    fallback.className = "shot-fallback";
    fallback.textContent = "Preview unavailable · Explore project";
    i.parentElement.appendChild(fallback);
    i.onerror = null;
  };
  i.src = i.dataset.src;
  i.removeAttribute("data-src");
}

function cardArt() {
  if (!("IntersectionObserver" in window)) {
    document.querySelectorAll("#out img[data-src]").forEach(artLoad);
    return;
  }
  // 200px of margin, so a picture has usually arrived by the time its card has, without reaching so far
  // down the list that one flick of a thumb pays for screenfuls nobody stopped at.
  if (!ARTIO) {
    ARTIO = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      ARTIO.unobserve(e.target);
      artLoad(e.target);
    }), {rootMargin: "200px 0px"});
  }
  ARTIO.disconnect();
  document.querySelectorAll("#out img[data-src]").forEach(i => ARTIO.observe(i));
}

function render() {
  // Reflect state onto the chips. Cheaper than rebuilding them and it keeps focus where it was.
  const press = (id, on) => [...document.getElementById(id).children]
    .forEach((b, i) => b.setAttribute("aria-pressed", on(i) ? "true" : "false"));
  press("cats", i => i === 0 ? !state.cat : D.cats[i - 1].slug === state.cat);
  press("tgts", i => i === 0 ? !state.tgt : D.targets[i - 1].slug === state.tgt);
  press("oses", i => state.os.includes(i));
  document.getElementById("strict").setAttribute("aria-pressed", state.strict ? "true" : "false");
  document.getElementById("new").setAttribute("aria-pressed", state.fresh ? "true" : "false");
  document.getElementById("since").setAttribute("aria-pressed", state.since ? "true" : "false");
  document.getElementById("rise").setAttribute("aria-pressed", state.rising ? "true" : "false");
  paintSaved();
  paintShared();
  // Third of the three, and the only one that does not depend on the rows below it: the pinned set resolves
  // through `BY_NWO`, not through `HITS`, which is what lets a pinned project stay in the comparison after the
  // reader has filtered it off the page. The pin buttons *in* the rows are drawn further down, out of the same
  // `state.cmp` this reads.
  paintCompare();
  // Here as well as on the toggle, for the same reason the chips above are reflected here rather than only
  // where they are clicked: this is the one function every path that changes state already ends at, so a
  // `#view=cards` link, a hashchange and the browser's back button all arrive at the right layout without
  // each of them remembering to.
  applyView();

  const words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
  let hits = ROWS.filter(match);

  // Two fallbacks, and which one goes first is the whole of the decision. A single mistyped letter used to
  // produce an empty page even when the answer was one letter away; a whole sentence used to produce one
  // even when the project it described was in the table. Those are different failures and they want
  // different instruments -- so the rule is the shape of the query, and it is one line:
  //
  //   nobody misspells a four-word sentence, and nobody writes a sentence as one word.
  //
  // One word that matched nothing is a typo, and `near()` gets first refusal. Several words that matched
  // nothing is a description, and `senseHits()` does. Whichever goes second still runs if the first came
  // back empty, so "kubernets" and "keep my agent from deleting files" both have two chances rather than
  // one, and neither costs anything on the overwhelming majority of renders where the words just worked.
  // `bym` is the membership answer, and it is a local rather than a flag on the rows for the reason
  // `senseHits` explains: a row that wore a "by meaning" pill under one query wore it into the next.
  // Rebuilt from scratch on every render, so there is no state here that can be stale by construction.
  let approx = false, sense = 0, bym = null;
  const senseInto = (base) => {
    const extra = senseHits(state.q, base);
    sense = extra.length;
    if (!extra.length) return base;
    bym = new Set(extra.map(r => r.nwo));
    return base.concat(extra);
  };
  if (words.length) {
    // A thin result set, never a healthy one. Forty exact matches need no help, and adding to them would
    // read as the search quietly ignoring the words that were typed -- which is the failure mode of every
    // search box that "helpfully" broadens. Meaning is a rescue here, not a re-interpretation.
    if (hits.length && hits.length < SEM_THIN) hits = senseInto(hits);
    if (!hits.length) {
      if (words.length > 1) hits = senseInto(hits);
      if (!hits.length) {
        const alt = near(state.q);
        if (alt.length) { hits = alt; approx = true; }
      }
      if (!hits.length) hits = senseInto(hits);
    }
  }
  // Near matches keep their similarity order rather than the reader's chosen sort: that list is a set of
  // corrections, and "closest first" is the only ordering that makes it one. A set that meaning
  // contributed to is *not* in that category -- those rows are answers, so they are sorted like answers,
  // by whatever the reader picked.
  if (!approx) {
    const sort = effSort();
    if (sort === "relevance") for (const r of hits) r.rel = relevance(r, words, sense);
    hits.sort(SORTS[sort]);
  }
  // After the sort and before the paging, which is exactly what the four exports need: the rows that matched, in
  // the order the reader chose, all of them rather than the 120 on screen. Assigned on every path including the
  // empty one, so a reader who presses Export on "Nothing matches all of that" gets a dialog that says zero
  // rather than the contents of the last search that worked.
  HITS = hits;

  // Whether the pulse is worth running -- `html[data-wave]` in the stylesheet is what acts on it. Two
  // conditions, and both are needed. A majority alone would suppress the motion on a three-row result where
  // two arrived yesterday, which is precisely the case a nudge is for; more new rows than fit on a screen
  // alone would suppress it on a legitimately busy week in a big filtered set. Together they describe the
  // only situation where the pulse stops meaning anything: the reader cannot see a row that is *not* new,
  // so "look at this one" is being said about everything in front of them.
  // Measured on `hits` and not on `ROWS`, so filtering down to one category hands the nudge back: the whole
  // atlas being 85% new says nothing about the eleven rows a reader has narrowed to.
  // Written through `dataset` with an explicit "1"/"" rather than `toggleAttribute`, which is the page's
  // idiom for every other root-level switch (`theme`, `view`, `sheet`) and is what the stub DOM in
  // tests/probe.mjs can carry -- its `documentElement` is an object with a `dataset` and no methods.
  const fresh = hits.filter(r => r.isnew).length;
  document.documentElement.dataset.wave = fresh > PAGE_SIZE && fresh > hits.length / 2 ? "1" : "";

  const ranked = hits.filter(r => r.stars).length;
  // The breakdown replaces the star count rather than joining it, on the renders where there is one. How
  // many of these rows the reader's own words found is the more useful of the two facts and it is the only
  // one that explains why a row with none of those words is on screen -- and a reader who cannot see that
  // distinction has been handed a search box that appears to ignore what they type.
  const countHTML = approx
    ? "<b>" + hits.length.toLocaleString() + "</b> near " +
      (hits.length === 1 ? "match" : "matches") + " · nothing matches “" + esc(state.q) + "” exactly"
    : sense
      ? "<b>" + hits.length.toLocaleString() + "</b> of " + ROWS.length.toLocaleString() + " · " +
        (hits.length - sense
          ? (hits.length - sense).toLocaleString() + " match your words, " +
            sense.toLocaleString() + " by meaning"
          : sense.toLocaleString() + " by meaning · nothing matches “" + esc(state.q) +
            "” word for word")
      : "<b>" + hits.length.toLocaleString() + "</b> of " + ROWS.length.toLocaleString() +
        " · " + ranked.toLocaleString() + " with stars";
  document.getElementById("count").innerHTML = countHTML;
  // The same sentence into the sheet's own header, along with the handle's badge. One string, two places:
  // the bar's copy is behind the sheet while the sheet is open, and a reader tapping chips has to see the
  // number move or they cannot tell that the tap landed.
  paintSheet(countHTML);

  const cat = state.cat && D.cats.find(c => c.slug === state.cat);
  const tgt = state.tgt && D.targets.find(t => t.slug === state.tgt);
  document.getElementById("ctx").textContent =
    cat && tgt ? cat.name + ", filtered to what plugs into " + tgt.name
    : cat ? cat.blurb : tgt ? tgt.blurb : "";

  const out = document.getElementById("out");
  if (!hits.length) {
    RESCUE = rescue();
    // No spelling suggestion here any more. `near()` above already offered every plausible correction as
    // real, clickable rows before this branch could be reached, so reaching it means the trigram pass also
    // came up empty -- and a "did you mean" that has nothing to name is worse than none. What is left is
    // genuinely a filter problem, which is what the rescue buttons address.
    out.innerHTML = '<div class="empty">' +
      '<p class="big">Nothing matches all of that.</p>' +
      (RESCUE.length
        ? "<p>" + (RESCUE.length === 1 ? "Loosening this would help:" : "Loosen one of these:") +
          '</p><div class="fixes">' + RESCUE.map((o, i) =>
            '<button class="fix" data-i="' + i + '">' + esc(o.label) +
            ' <span class="n">' + o.n.toLocaleString() + "</span></button>").join("") + "</div>"
        : "") +
      '<p style="margin-top:16px"><button class="fix" data-all="1">Clear all filters</button></p>' +
      // Last, and below Clear all, because loosening a filter is what most empty result sets actually need
      // and reporting a gap is the rarer thing. Returns "" unless there is a search term, so a reader who
      // has only over-filtered is never invited to file an issue about it. No change is needed in `wire()`:
      // the delegated `#out` listener tests `closest(".fix")` and `closest(".copy")`, so a click on this
      // anchor matches neither and falls through to the browser's own handling of the href -- which is the
      // whole reason it is an anchor.
      missLink() +
      "</div>";
    return;
  }
  const page = hits.slice(0, state.shown);
  const rows = page.map((r, i) => {
    // A U+2009 thin space, not a full one, between a platform's mark and its verdict glyph, so that the two
    // read as one unit beside their four neighbours rather than as ten separate things. The mark replaced the
    // truncated word that used to stand here, and two things put the word back rather than one: the `title`,
    // which was already carrying the platform and the whole verdict sentence for a hover, and a `.sr` span.
    //
    // The `.sr` span now carries the verdict as well as the platform, and the glyph is `aria-hidden`. It used
    // to name the platform only, which left the glyph as the sole spoken carrier of the answer. That worked
    // for three of the five -- the comment on `VERDICT` explains why the marks were chosen to be pronounced
    // -- and left the other two announcing a platform and then nothing. `title` held the sentence, and
    // `title` reaches a mouse and nobody else. So a screen reader now hears "Windows: stated support" rather
    // than "Windows check mark", the two silent verdicts stop being silent, and the glyphs are released from
    // having to be pronounceable, which is what made splitting `a` from `-` possible at all.
    const os = D.os.map((o, k) => {
      const v = VERDICT[r.os[k]] || ["", "not established"];
      return '<span class="v' + r.os[k] + '" title="' + esc(o + ": " + v[1]) + '">' +
        '<span class="sr">' + esc(o + ": " + v[1]) + "</span>" + osIcon(k) +
        '<span aria-hidden="true"> ' + v[0] + "</span></span>";
    }).join(" ");
    const tags = '<span class="tag cat">' + esc(D.cats[r.cat].name) + "</span>" +
      r.targets.map(t => '<span class="tag">' + esc(D.targets[t].name) + "</span>").join("");
    // esc on the URLs too: these are other people's hand-typed table cells, and one stray quote in a
    // source list would otherwise close the attribute and let the rest of it be read as markup.
    const url = esc(r.url), img = esc(r.img), page = detailURL(r.nwo);
    // A new row's title is the star, the name, and the day it arrived. The date is outside the anchor so
    // hovering the title does not underline it, and it is the fact that makes the mark self-explaining:
    // "New" alone leaves the reader wondering new to what, and how long ago.
    const star = r.isnew
      ? '<svg class="ni"><use class="a" href="#star-a"></use><use class="b" href="#star-b"></use></svg>'
      : "";
    // "Added", not "New on". The chip already says New; what the row has to say is *when*, because that is
    // the fact that makes the mark self-explaining -- and because these projects are not new, the atlas's
    // knowledge of them is. A three-year-old repo labelled "New on 09/21/26" is a page making a claim about
    // the repo; "Added 09/21/26" is the page making a claim about itself, which is the true one.
    const on = r.isnew ? ' <span class="newon">- Added ' + mmddyy(r.first_seen) + "</span>" : "";
    // Why this row is here when none of the reader's words are in it. Words, not a glyph: this is the one
    // label on the row that answers a question the reader is actively asking, and a mark would make them
    // hover to find out. Membership comes from the render's own Set, so a row that matched the words as
    // well is never labelled as if it had not, and neither is a row that qualified under a *previous*
    // query -- which is the bug this replaced a per-row flag to fix.
    const sensechip = bym && bym.has(r.nwo)
      ? ' <span class="senseon" title="Found by what it does, not by the words you typed">' +
        "by meaning</span>"
      : "";
    // The install line, with a button when the clipboard is reachable. The command is the one thing on a
    // row a reader wants to take away, and taking it meant selecting wrapped monospace text without
    // catching the blurb above it. The name is in the label because a screen-reader user arrives at
    // "Copy" 120 times a page and needs to know which project this one belongs to.
    const cmd = FLAGS["index.install_commands"] && r.install
      ? '<div class="cmdrow"><code class="cmd">' + esc(r.install) + "</code>" +
        (CAN_COPY ? '<button class="copy" data-cmd="' + esc(r.install) +
          '" aria-label="Copy install command for ' + esc(r.name) + '">Copy</button>' : "") + "</div>"
      : "";
    const shot = FLAGS["index.project_screenshots"]
      ? '<td class="shot"><a href="' + page + '" tabindex="-1" aria-hidden="true">' +
        '<img loading="lazy" decoding="async" alt="" data-src="' + img + '"></a></td>'
      : "";
    // `nw` is the pulse hook, and it is a class on the row rather than a `:has()` on the star inside it so
    // that the table view can reach the row's *cells* -- which is the only way to draw an edge around a row
    // under `border-collapse:collapse`. See the `.nw` rules in the stylesheet.
    return '<tr data-project="' + esc(r.nwo) + '"' + (r.isnew ? ' class="nw"' : "") +
      ' style="--card-accent:var(--accent-' + projectAccent(r.nwo) + ')">' +
      '<td class="n rk">' + (i + 1) + "</td>" +
      // The screenshot is a second link to the same URL as the title next to it, so it was a duplicate
      // tab stop with no accessible name at all -- 120 unlabelled links per page, which is both a 2.4.4
      // failure and a keyboard reader pressing Tab twice for every row. aria-hidden plus tabindex="-1"
      // is the pattern for a redundant adjacent link: it stays clickable by mouse and disappears from the
      // accessibility tree, where the title already says everything it could have said.
      // Both of these now point inward, at the page 22_detail.py wrote for this project. The atlas knows
      // the install command, the five platform verdicts *with the evidence sentence behind each one*, and
      // which of the eleven lists named it -- sending the reader straight to github.com was giving all of
      // that away on the one click they were most likely to make. The shot stays the redundant adjacent
      // link to the title, aria-hidden and untabbable, which is only true while it goes where the title
      // goes.
      // `data-src` rather than `src`, and `cardArt()` below decides when it becomes one. `loading="lazy"`
      // stays on the tag: once the src is set it is still the right hint for a picture that has since been
      // scrolled away from, and it costs nothing to leave the browser's own heuristic in play behind ours.
      shot +
      '<td class="pj"><a class="nm" href="' + page + '">' + star + esc(r.name) + "</a>" + on + sensechip +
        // The way out. owner/name was already sitting under every title reading like a GitHub path, so
        // making it the outward link costs no new text and needs no new label -- "openclaw/openclaw" is a
        // better accessible name than "GitHub" repeated 120 times. It does add one tab stop per row,
        // which is the price of the title no longer being the way out.
        '<a class="nwo" href="' + url + '">' + esc(r.nwo) + "</a>" +
        // In the project cell rather than in a cell of its own, which is not a layout preference: the
        // headings and the body cells of this table have to stay the same length, and a mismatch here has
        // already once produced five headings over four columns with an invented fifth column to hang the
        // surplus on. A control that needs no heading has no business creating that risk. The cards view
        // gets it for free too -- `td.pj` is the full-width row 3 there, so the button lands under the
        // title in both layouts without a second rule.
        saveBtn(r) +
        // Beside Save, in the same cell, for the reason the note above gives about Save: the headings and the
        // body cells of this table have to stay the same length, and a control that needs no heading has no
        // business risking a mismatch. It also lands under the title in the cards view for free, `td.pj` being
        // the full-width row there -- and it lands on the same *line* as Save at 375px, which was measured
        // rather than assumed. That matters more than it sounds: `td.pj` is the cell whose height decides
        // whether a phone reader sees a project's name above the fold at all (JFH-289), and it has 14px of
        // slack. A second line here would spend all of it.
        pinBtn(r) +
        '<div class="meta os">' + os + "</div></td>" +
      '<td class="n st-c"><span class="st' + (r.stars ? "" : " none") + '">' +
        (r.stars ? r.stars.toLocaleString() : "—") + "</span>" +
        // The gain sits under the star count because the two are the same quantity measured twice, and a
        // reader comparing two rows compares both at once. `gained` draws nothing where the ledger has no
        // history for the row, which is what "degrade quietly rather than showing zero" means here.
        '<div class="meta">' + r.lists + (r.lists === 1 ? " list" : " lists") + gained(r) +
          "</div></td>" +
      '<td class="hide tg">' + tags + "</td>" +
      '<td class="ds"><div class="desc">' + esc(r.blurb) + "</div>" + cmd + "</td>" +
      // Each fact in its own span, not bare text between <br>s. The card layout lays this out as a flex
      // row, and flex builds an anonymous item per *contiguous run of text* -- so with the <br>s hidden
      // the three text nodes became one item and rendered as "ShellMIT 6d ago". Real elements are real
      // flex items, and they cost nothing in the table view.
      '<td class="c hide lc"><div class="meta"><span>' + esc(r.lang || "—") + "</span><br>" +
        "<span>" + esc(r.license || "—") + "</span><br><span>" + since(r.pushed) +
        '</span></div><div class="project-actions"><a href="' + page + '" aria-label="Explore ' + esc(r.name) + '">Explore project <span aria-hidden="true">↗</span></a>' +
        '<a href="' + url + '" aria-label="' + esc(r.nwo) + ' on GitHub">GitHub</a></div></td>' +
      "</tr>";
  }).join("");
  // Every th carries the same class as the td beneath it. The Shot heading used not to, and since the
  // narrow-viewport rule hides `.shot` it hid only the body cell -- leaving five headings over four
  // columns, so "Shot" sat above the project names, "Project" above the stars, "Stars" above the
  // blurbs, and auto layout invented a fifth column to hang the surplus heading on.
  // Said above the table as well as in the live region, because a sighted reader who mistyped needs to
  // know *why* they are looking at LangGraph when they asked for "langraph" -- otherwise the correction
  // looks like the search quietly ignoring them.
  const within = state.cat || state.tgt || state.os.length || state.strict || state.fresh || state.since
    ? ", within your other filters" : "";
  // Said above the table on the one render that needs saying most: every row on screen was found by what
  // it does rather than by what it is called, so a reader looking for their own words will not find one of
  // them anywhere. Only when *all* of them came that way -- a mixed set explains itself, because the rows
  // the words did find are sitting there with the term highlighted in them.
  const note = approx
    ? '<p class="approx">Nothing matches <b>' + esc(state.q) + "</b> exactly. Closest by name" +
      within + ":</p>"
    : sense && sense === hits.length
      ? '<p class="approx">Nothing here says <b>' + esc(state.q) +
        "</b>. These are the projects that mean it" + within + ":</p>"
      : "";
  out.innerHTML = note +
    "<table><thead><tr><th class='n'>#</th>" +
    (FLAGS["index.project_screenshots"] ? "<th class='shot'>Shot</th>" : "") +
    "<th class='pj'>Project</th>" +
    "<th class='n st-c'>Stars</th>" +
    "<th class='hide tg'>Topic &amp; targets</th><th class='ds'>What it does</th>" +
    "<th class='c hide lc'>Lang / licence / push</th></tr></thead><tbody>" + rows +
    "</tbody></table>";
  // After the subtree exists and before the "show more" button is appended, so visible images begin loading
  // on a cold visit and further images remain viewport-lazy after every filter or page expansion.
  cardArt();
  if (hits.length > page.length) {
    const b = document.createElement("button");
    b.className = "more";
    b.textContent = "Show " + Math.min(PAGE_SIZE * 4, hits.length - page.length).toLocaleString() +
      " more of " + hits.length.toLocaleString();
    b.onclick = () => {
      const first = state.shown;
      state.shown += PAGE_SIZE * 4;
      render();
      // render() replaced the whole subtree, so the button that was just clicked no longer exists and
      // focus fell to <body> -- which returns a keyboard reader to the top of the document, above six
      // rows of filters, every time they ask for more. Put it on the first newly revealed row instead,
      // which is where a mouse reader is already looking. preventScroll so the viewport does not jump
      // for anyone: the new rows appear below the fold, exactly where the button was.
      const rows = document.querySelectorAll("#out tbody tr");
      const t = rows[first] || document.querySelector("#out .more");
      if (t) { t.tabIndex = -1; t.focus({preventScroll: true}); }
      say(Math.min(state.shown, hits.length).toLocaleString() + " of " +
          hits.length.toLocaleString() + " shown.");
    };
    out.appendChild(b);
  }
  // Last, and outside every branch above: the map draws what this function decided, so it is repainted from
  // the one place that always knows. A no-op unless the dialog is open.
  mapRepaint();
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g,
    c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
}
</script>
<!-- The offline shell. Last thing on the page and inside a `load` listener, because a service worker is
     the least urgent thing here: registering it earlier competes with the fetch that puts rows on screen.
     `sw.js` is written by `scripts/24_pwa.py` and caches the shell, this page's navigation and data.json;
     everything cross-origin it leaves alone.

     `updateViaCache: "none"` because Pages serves with `max-age=600`, and the one file that must never be
     read from the HTTP cache is the worker that decides what the HTTP cache is for. The explicit
     `reg.update()` is not belt-and-braces: per spec, `register()` with an unchanged script URL resolves
     against the existing registration without queueing an update job, so without this line a reader who
     keeps the tab open gets a new worker only when the browser's own soft-update timer decides.

     Guarded on the protocol as well as on support: from `file://` the registration throws a
     SecurityError, and a contributor opening the page off disk should not see it. -->
<script>
if ("serviceWorker" in navigator && location.protocol !== "file:") {
  addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js", {updateViaCache: "none"})
      .then(reg => { if (reg.active) reg.update().catch(() => {}); })
      .catch(() => {});
  });
}
</script>
__ANALYTICS__</body>
</html>
"""


def main() -> None:
    records = b16.prepare(
        json.loads((CACHE / "records_all.json").read_text(encoding="utf-8")), None)
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    orch = json.loads((CACHE / "records.json").read_text(encoding="utf-8"))
    # Optional, unlike everything above: no shot map means every row shows its Open Graph card, which is
    # what the daily job relies on to skip the capture stage entirely. See `b17.cached`.
    shots = b16.merged_shots(b17.cached("shots_all.json"), b17.cached("shots.json"))

    for r in orch:
        r.setdefault("section", r["category"])
        r.setdefault("bucket", r["category"])
        r.setdefault("blurb", r.get("description") or "")
        r.setdefault("src_order", r.get("order", 0))
        r["shot_key"] = (r.get("nwo") or "").replace("/", "__")
        if r.get("license") in ("NOASSERTION", "NONE", DASH, "", None):
            r["license"] = ""
    b16.canonicalise_nwo(records, orch, meta)

    # b16.LIST_TITLE, not a second map built from SHEETS: this is the same defect the workbook and the
    # Markdown edition each carried, and the site was the last surface still holding it. SHEETS is the
    # ten lists with a sheet of their own; `listed_by` here describes rows drawn from all thirty-nine,
    # so 27 of them printed their raw internal key -- 8,158 cells across 89% of rows, reading
    # "agentsec_recon, aiagents_jenqyang" where a neighbour read "Claude Code". No visible column shows
    # it, which is why it survived, but `row_for` folds it into the client-side search haystack: a
    # reader searching "Gemini CLI Ecosystem" matched nothing while "mcp_punkpeye" matched 3,457 rows.
    # LIST_TITLE already layers SHEET_TITLE over the SOURCES titles and already carries the
    # orchestrators override, so every name this used to produce is unchanged.
    label = b16.LIST_TITLE
    tax.STARS.clear()
    tax.STARS.update(b16.star_map(records, orch, meta))
    agg = tax.by_repo(records + [dict(x, source="orchestrators") for x in orch])
    facets = b16.repo_pool(records, orch, label)
    for r in facets:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        r["stars"] = tax.STARS.get(r["nwo"], 0)

    # Before build_data, which reads the map it fills. Idempotent, so 17_markdown having already run in
    # this pipeline is fine -- it stamped the same repos with the same date and this call agrees. Passing
    # `sources` is part of agreeing: whichever stage stamps a repo first decides its date, so a call that
    # omitted it would date the same repos differently depending on which stage got there first.
    fresh = newness.resolve([r["nwo"] for r in facets],
                            sources=[s["nwo"] for s in b16.b10.SOURCES])

    data = build_data(facets, shots)
    OUT.mkdir(exist_ok=True)
    (OUT / "data.json").write_text(
        json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    # Pages runs Jekyll by default, which would try to interpret this directory as a site and skip
    # anything it decided looked like a draft. There is no Jekyll here.
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    page = substitute(PAGE, data, REPO, b17.SITE)
    (OUT / "index.html").write_text(page, encoding="utf-8")

    for f in ("index.html", "data.json"):
        print(f"{f:12s} {(OUT / f).stat().st_size / 1024:8.1f} KB")
    print(f"{len(data['rows']):,} repos · {len(data['cats'])} topics · "
          f"{len(data['targets'])} targets · {sum(r[4] for r in data['rows']):,} stars")
    # Two numbers, because they answer different questions and a build that conflates them cannot be read.
    # `fresh` is every arrival the ledger remembers; the cohort is the one set this page marks New.
    live = sum(1 for d in fresh.values() if d == newness.COHORT) if newness.COHORT else 0
    print(f"{len(fresh):,} arrived since {data['baseline']} · "
          + (f"{live:,} in the {newness.COHORT} cohort, marked New"
             if newness.COHORT else "nothing marked New"))


if __name__ == "__main__":
    main()
