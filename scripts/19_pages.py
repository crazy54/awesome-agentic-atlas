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
cached separately from the 1,294 rows that change on every rebuild. And every filter is mirrored into
the URL hash, which is what makes "the best Claude Code observability tool" a link -- the thing the
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
import pagemin  # noqa: E402

newness = b17.newness

b16 = b17.b16
tax = b17.tax
DASH = b16.DASH
REPO = b17.REPO

# Verdicts compress to one character each because they are printed 6,470 times and there are five of
# them. The page expands them back for display; the JSON is what travels over the wire.
VERDICT = {"Yes": "Y", "Likely": "L", "No": "N", "n/a": "a", DASH: "-", "": "-"}
OS_FIELDS = ["win_native", "win_wsl2", "macos", "linux", "docker"]
OS_LABELS = ["Windows", "WSL2", "macOS", "Linux", "Docker"]

# The columns of `data.json`, in order. Column-oriented rather than one object per repo: the keys would
# otherwise be repeated 1,294 times, which is 380 KB of the word "category". The page maps them back
# into objects once, on load.
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
        # The page applies the window, so it has to be told what it is. Here rather than hardcoded in the
        # JavaScript so that changing it is one edit in `newness.py` and not two files that disagree.
        "window_days": newness.WINDOW,
        "baseline": newness.load()["baseline"],
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
    return (pagemin.strip_page(page)
            .replace("__BUILT__", stamp_iso)
            .replace("__BUILT_UTC__", stamp_utc)
            .replace("__TOPICLINKS__", facet_links(data["cats"], "topic"))
            .replace("__TARGETLINKS__", facet_links(data["targets"], "target"))
            .replace("__COUNT__", f"{len(data['rows']):,}")
            .replace("__TOPICS__", str(len(data["cats"])))
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


PAGE = r"""<!doctype html>
<!-- `data-view` here as well as in `state`, because the reader looks at this page for the length of a
     561 KB fetch before any script has an opinion about it. Without it the table's column headings sit
     over an empty body until `data.json` lands and then vanish; with it the default view is the one that
     was there all along. A `#view=table` link still lands on the table -- `readHash` cannot run before
     the data either way, so this attribute governs the wait and nothing more. Keep the two in step. -->
<html lang="en" data-theme="dark" data-view="cards">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome Agentic Atlas — browse every agentic tool</title>
<meta name="description" content="__COUNT__ agentic AI projects from eleven awesome-lists, merged, deduplicated and filterable by topic, harness and operating system.">
<meta property="og:title" content="Awesome Agentic Atlas">
<meta property="og:description" content="__COUNT__ projects from eleven awesome-lists, one filterable index.">
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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='14'>&#127760;</text></svg>">
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
<meta name="theme-color" id="tc" content="#181f21">
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
  document.getElementById("tc").content = t === "light" ? "#eef1f2" : "#181f21";
} catch (e) {}
</script>
<style>
/* Lagoon Gold: cyan primary, gold secondary, cool near-black surfaces. Dark is the designed mode --
   its eight neutrals and two accents are the theme's own values. Light is stepped from the same two
   hues rather than flipped, because the accents at their dark-mode lightness fail on white (the cyan
   measures 2.53:1 there), and its neutrals are cooled to match so toggling does not change brand.
   --onbar exists because a filled cyan or gold accent carries DARK ink, not white: white on #08b0cc
   is 2.3:1, while the theme's own #0c1013 on it is 7.36:1. */
:root{
  --surface:#101416; --plane:#181f21; --band:#232d30; --ink:#d0d7d8; --ink2:#a8b0b2;
  --muted:#8c9496; --grid:#2c383d; --link:#08b0cc; --bar:#08b0cc;
  --good:#2eb82e; --warn:#feb932; --off:#8c9496; --onbar:#0c1013;
}
html[data-theme=light]{
  --surface:#fbfcfc; --plane:#eef1f2; --band:#f4f6f6; --ink:#101416; --ink2:#4a5254;
  --muted:#5f6769; --grid:#dbe0e1; --link:#096373; --bar:#0a6f80;
  --good:#0a7c0a; --warn:#8a5a00; --off:#5f6769; --onbar:#fff;
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
header{background:var(--plane);border-bottom:1px solid var(--grid);padding:22px 20px 16px}
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
/* The "last deployed" badge, drawn to match the shields.io badges in the README rather than fetched from
   shields.io. Fetching one is not an option here: the value is a timestamp, so the URL would have to be
   regenerated on every build, the badge would still be a third-party request on the critical path of every
   page view, and it could never be corrected at load by `deployStamp` -- an <img> cannot be re-rendered
   from a response header.
   Every number below is read off the SVG shields actually serves for `?style=for-the-badge`, not guessed:
   28px tall, 10px Verdana, 12px gutters, square corners, label in normal weight on #555 and value in bold
   on the colour. The tracking is the one thing shields does not express as a property -- it forces each run
   of text to a computed width with `textLength` and lets the renderer distribute the slack -- so it is set
   here directly, at the value that lands both segments on shields' own rect widths for this badge (122.25
   and 176.0, measured, not guessed). That stays true for every date this will ever print: the value is
   always exactly 20 characters and Verdana's digits are tabular, so the string's width never moves. The
   right gutter gives the tracking back, because CSS letter-spacing applies after the final character too
   and would otherwise push the text half a pixel off-centre inside its own box.
   Fixed hexes rather than theme variables, and #1a7f37 is the README's own green: those badges are images
   and look identical in GitHub's light and dark themes, so a stamp that repainted itself with this site's
   theme would be the one thing in the family that did not match. Both fills clear 4.5:1 against white. */
.stamp{display:inline-flex;height:28px;margin:10px 0 0;text-decoration:none;
  font-family:Verdana,Geneva,DejaVu Sans,sans-serif;font-size:10px;line-height:28px;
  letter-spacing:1.28px;text-transform:uppercase;white-space:nowrap}
.stamp>span{padding:0 10.72px 0 12px;color:#fff}
.stamp .k{background:#555}
.stamp .v{background:#1a7f37;font-weight:700}
/* Amber on the same fortnight the snapshot text uses, so the header has one staleness threshold and not
   two. Recoloured rather than relabelled, and the badge's own tooltip says what the colour means. */
.stamp.late .v{background:#9a6700}
/* A ring rather than a lighter fill on hover: every lighter step of these two greens and ambers drops
   the white text below 4.5:1, and a badge that becomes unreadable when pointed at is a poor trade for an
   affordance a ring gives just as clearly. */
.stamp:hover,.stamp:focus-visible{box-shadow:0 0 0 2px var(--bar)}
.stamp:focus-visible{outline:none}
/* At its full width the badge is 298px, which needs 338px of viewport once the header's own gutters are
   paid, so on a 320px phone it was the one element on the page wide enough to give the whole document a
   horizontal scrollbar -- measured: 305px of content became 312px. What gives way is the label, never the
   value: the timestamp is the thing the badge exists to say, and "DEPLOYED 2026-09-06 18:07 UTC" loses no
   meaning at all. 360px rather than 338px so the rule lands on a phone width rather than mid-band. */
@media (max-width:360px){.stamp .lw{display:none}}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.top nav{font-size:13px;color:var(--muted);text-align:right;line-height:1.9}
button{font:inherit;cursor:pointer}
.bar{position:sticky;top:0;z-index:20;background:var(--plane);
  border-bottom:1px solid var(--grid);padding:10px 20px}
.bar .wrap{display:flex;flex-direction:column;gap:8px}
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
/* The new-arrivals chip wears the gold accent rather than the cyan every other chip uses, because it
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
.nm .ni{margin-right:.34em}
.newon{color:var(--warn);font-size:12px;font-weight:600;white-space:nowrap}
/* Rising wears green, where the new-arrivals chip wears gold and every other chip wears cyan. Three
   questions get three colours because a reader asks all three of a row at once -- is it alive, did it just
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
/* Saved wears the cyan every ordinary chip wears, and that is the decision rather than an omission. Gold
   and green above are properties *of a repo* -- it arrived recently, it is gaining stars -- and they are
   held to three colours for three questions. Saved is a fact about the reader, true of nothing on the
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
/* Guarded, because a touch device reports a hover that then latches: tapping a row anywhere -- to
   follow its link, or just while scrolling -- left it tinted until something else was tapped. */
@media(hover:hover){tr:hover td{background:var(--band)}}
.rk{color:var(--muted);font-size:12px;font-variant-numeric:tabular-nums}
.shot{width:200px}
/* `aspect-ratio` is load-bearing and not decoration. These pictures have no `src` until a reader gives an
   input event -- see `cardArt()` -- and this is what makes an unsourced one occupy exactly the space the
   loaded one will, so nothing moves when it arrives. Remove it and every card image becomes a layout shift
   that arrives on someone else's schedule. Verified: with every image blocked, CLS was 0.5140; with them
   all loading, 0.5140 (JFH-216). */
.shot img{width:200px;aspect-ratio:2/1;object-fit:cover;border-radius:6px;
  background:var(--band);border:1px solid var(--grid);display:block}
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
   which is what it was for -- keeping "Win ✓" together, not forcing all five onto one line, which on a
   375px card is 260px of unbreakable text. */
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
   choice and it is wrong in both themes: it is *lighter* than `--plane` in light mode, so the selected row
   came out as a barely-there strip of #f4f6f6 on #eef1f2 -- measured 1.05:1 against its own background.
   The highlight is the one thing the palette cannot afford to be subtle about, since it is the only
   indication of what Enter will do. `--onbar` because a filled accent carries dark ink in dark mode and
   white in light, and the muted greys below would vanish against either. */
#palist li.it[aria-selected=true]{background:var(--bar);color:var(--onbar)}
#palist li.it .t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#palist li.it .k,#palist li.it .s{flex-shrink:0;font-size:12px}
#palist li.it .k{color:var(--muted)}
#palist li.it .s{color:var(--warn)}
/* Inherit, not a fixed colour: on the accent fill the secondary text has to shift with `--onbar`, and
   opacity keeps it secondary without needing a second value that passes contrast on cyan and on teal. */
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
     chips -- and gets bumped onto a line of its own, which is two rows per facet again. */
  #cats,#tgts,#oses{display:flex;flex-wrap:nowrap;gap:6px;overflow-x:auto;
    flex:1 1 0;min-width:0;
    scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
  #cats::-webkit-scrollbar,#tgts::-webkit-scrollbar,#oses::-webkit-scrollbar{display:none}
  .bar .wrap{gap:5px}
  .chip{padding:4px 11px}
  /* And a cap on top of the rails, because rails alone still leave four to six control rows. On a tall
     screen the cap sits above the bar's natural height and nothing happens; on a short one the bar
     scrolls inside itself instead of over the page. A fraction rather than a pixel count so that it
     only ever binds where it is needed. `vh` first: a browser that does not understand `dvh` must
     still get a cap rather than none. */
  .bar{max-height:44vh;max-height:44dvh;overflow-y:auto}

  /* ---- and the sheet, which is what the rails and the cap above are the fallback for -----------------
     The handle, at the 44px WCAG 2.5.5 asks for, sharing the one row the bar is now reduced to with the
     search box. Everything in that row grows to 44 with it: the 30px chips above are what you do when six
     control rows have to fit on a phone, and are not what you do once they no longer have to. */
  html[data-fb] #fbt{display:inline-flex;flex:none;min-height:44px;padding:0 14px}
  html[data-fb] #q{flex:1 1 0;min-width:9em;min-height:44px}
  html[data-fb] .bar .chip,html[data-fb] select{min-height:44px}
  /* No `display` in this rule, deliberately. It outranks `.newchip{display:none}`, so setting one here
     would put the New and Rising chips on screen on every build whose window is empty -- which is the one
     thing those two classes exist to prevent. A <button> centres its own content vertically, so the
     min-height above needs no help. */
  html[data-fb] .bar .chip{padding:0 13px}
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
  /* 20px gutters on all four sections cost 40px, 11% of a 375px screen, and the old query left them. */
  header{padding:16px 14px 12px}
  .bar{padding:8px 14px}
  main{padding:0 14px 48px}
  footer{padding:18px 14px}
  h1{font-size:21px}
  h1 span{display:block;font-size:13px}
  .top{gap:10px}
  .top nav{text-align:left;line-height:2.1}

  #q{flex:1 1 100%;min-width:0}
  .line>label[for=q]{display:none}
  .count{margin-left:0;font-size:12px}
  /* Runs-on is the one facet that also carries Confirmed only and Clear all, and at 390px those two
     left its rail about 110px -- one OS chip at a time. That line alone wraps, so the rail keeps most
     of the row and the two buttons drop underneath it. Narrow-only: in landscape there is width enough
     for all four to share the row, and wrapping there would cost a row the bar cannot spare. */
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
  gap:0 10px;margin:0;padding:0 0 12px;background:var(--surface);
  border:1px solid var(--grid);border-radius:10px;overflow:hidden}
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
/* The table tints the row the pointer is over; a card is a box, so it takes the accent on its edge. The
   cell rule has to be undone explicitly or the tint lands as six full-width strips inside the card with
   the gaps between them showing through. Inside `hover:hover` like the rule it overrides, so a touch
   device -- which latches a hover it can never clear -- is not made to carry either of them. */
@media(hover:hover){
  html[data-view=cards] tr:hover td{background:transparent}
  html[data-view=cards] tr:hover{border-color:var(--bar)}
}

/* Nothing here animates on a timer, but the chip hovers transition and the chip rails scroll smoothly,
   and both are motion a reader can have asked their operating system not to show them. A blanket rule is
   safe because no state on this page is communicated *by* an animation -- removing every one of them
   changes nothing but the easing. */
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;
    transition-duration:.01ms !important;scroll-behavior:auto !important}
}

/* Focus lands on a row after "Show more", so the row needs somewhere to put a ring and needs to clear
   the sticky filter bar if anything ever does scroll it into view. */
#out tr:focus{outline:2px solid var(--bar);outline-offset:-2px}
#out tr{scroll-margin-top:160px}
</style>
</head>
<body>
<a class="skip" href="#out">Skip to results</a>
<!-- One shared region for anything the page needs to say that is not already text on the screen: a copy
     succeeding, a clipboard being refused, how many rows "Show more" just added. The result count has its
     own role=status on #count, because that one *is* visible text and should be announced from where it
     is rather than duplicated here. -->
<span class="sr" id="live" role="status" aria-live="polite"></span>
<!-- Drawn here rather than borrowed so there is no third-party licence attached to a 300-byte glyph: a
     four-point star with concave arms, plus a smaller one trailing it. Two tones, gold and cyan, which
     is the theme's own pair -- the mark for "new" is the mark for this site, not a generic sparkle.

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
    <h1>Awesome Agentic Atlas <span>· eleven awesome-lists, merged</span></h1>
    <p class="sub"><b>__COUNT__</b> projects · <b>__TOPICS__</b> topics · <b>__STARS__</b> combined
      stars · <span id="snap" title="Rebuilt daily from the GitHub API">snapshot
      __SNAPSHOT__</span></p>
    <p class="blurb" id="ctx"></p>
    <!-- The DOM text is sentence case and the uppercase is `text-transform`, so the accessible name reads
         "Last deployed 2026-09-06 18:07 UTC" rather than being spelled out, and no aria-label is needed to
         paper over the styling. `<time>` because this is a timestamp and something will want to read it.
         The href goes to the deployment history, which is where the badge's own claim can be checked.
         The line break between the two spans is load-bearing: without a text node between them the
         accessible name comes out as "Last deployed2026-09-06 18:07 UTC", run together. A flex container
         drops whitespace-only children, so it costs nothing in layout. -->
    <a class="stamp" id="deployed" href="https://github.com/__REPO__/deployments"
       title="When this copy of the site was published."><span class="k"><span class="lw">Last </span>deployed</span>
      <span class="v"><time datetime="__BUILT__">__BUILT_UTC__</time></span></a>
  </div>
  <nav>
    <a href="https://github.com/__REPO__">Repository</a> ·
    <a href="https://github.com/__REPO__/tree/main/mega-list">Markdown edition</a> ·
    <a href="https://github.com/__REPO__/releases/latest">Workbook</a><br>
    <!-- No aria-pressed. The label names the action and changes with the state, and "Dark theme" plus
         pressed=true announces as "dark theme is on" -- which is the opposite of what it means. A toggle
         gets a static label and a pressed state, or a changing label and no pressed state; this is the
         second. It also stops the button rendering as a filled accent pill purely because the reader is
         in light mode, which made it look like an active filter. -->
    <button class="chip" id="theme">Light theme</button>
  </nav>
</div></div></header>

<div class="bar"><div class="wrap">
  <div class="line">
    <label for="q">Search</label>
    <!-- aria-label as well as the <label>, because the narrow-viewport rule sets `display:none` on
         `label[for=q]` and that removes it from the accessibility tree as well as from the screen -- so
         on a phone the search box had no accessible name at all. -->
    <input id="q" type="search" aria-label="Search projects"
           placeholder="name, repo, description, language&hellip;"
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
    <button class="chip newchip" id="new" aria-pressed="false"
            title="Projects the source lists added in the last __WINDOW__ days">
      <svg class="ni"><use class="a" href="#star-a"></use><use class="b" href="#star-b"></use></svg>
      <span id="newlabel">New</span></button>
    <button class="chip risechip" id="rise" aria-pressed="false"
            title="Projects gaining stars fastest for their size">
      <span id="riselabel">Rising</span></button>
    <!-- Both start hidden and both are revealed by `render()`, not by `buildChips`: what they count is the
         reader's own saved set, which changes while the page is open. The New and Rising chips beside them
         count something the build decided, so those are settled once and never move. -->
    <button class="chip savechip" id="saved" aria-pressed="false"
            title="Only the projects you have saved on this device"><span id="savedlabel">Saved</span></button>
    <button class="chip clearsave" id="clearsave">Remove all saved</button>
    <button class="chip" id="palhint"></button>
    <!-- role=status makes this a polite live region, so pressing a chip or typing a search announces the
         new result count instead of silently rewriting a number the reader cannot see. aria-atomic so it
         is read as one sentence rather than as whichever digits changed. -->
    <span class="count" id="count" role="status" aria-atomic="true"></span>
  </div>
  <!-- Inside the bar rather than after it, because on a desktop these three rows are part of the sticky
       bar and have been since the page was written; the sheet is a narrow-viewport reading of the same
       markup, which is the trick the cards view plays on the table and it is here for the same reason.
       `position:fixed` is not clipped by the bar's `overflow-y:auto` -- a fixed box's containing block is
       the viewport, and the bar has no transform or `contain` to make itself one instead -- and the bar's
       own `z-index:20` stacking context is what puts the sheet above the results rather than beneath them.

       The backdrop is a sibling and not a `::before` on the sheet: it has to cover the page the sheet is
       over, and a pseudo-element of the sheet is inside it. -->
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

<main><div class="wrap"><div id="out"></div></div></main>

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

<footer><div class="wrap">
  Every entry came from someone else's curation work; all eleven source lists are credited in the
  <a href="https://github.com/__REPO__#the-eleven-lists">repository</a>. Stars, language, licence and
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
  <nav class="facets" aria-label="Browse by topic or by what a project plugs into">
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
// Cards, not the table, because the screenshot is the reason to open this page rather than read
// `mega-list/`: a card carries the project's own banner and a table row has nowhere to put one. The table
// is still the better view for scanning 120 rows against each other, so it keeps its button and gets a
// shareable `#view=table` -- and `readHash` reads both words explicitly, so every `#view=cards` link
// written while cards were opt-in still means exactly what it said.
//
// Kept in step with `data-view` on the <html> tag, which is what the reader looks at until `data.json`
// lands. The two have to agree: disagreeing would show the table's column headings over an empty body for
// the length of a 561 KB fetch and then replace them with cards.
const state = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false, rising: false,
               saved: false, sort: "relevance", shown: PAGE_SIZE, view: "cards"};
let D = null, ROWS = [], NEW = 0, RISE = null, RISING = 0;

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
const VERDICT = {
  Y: ["✓", "stated support"],
  L: ["?", "inferred from the language"],
  N: ["✗", "no evidence of support"],
  a: ["–", "not applicable"],
  "-": ["–", "not established"],
};

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
function since(iso) {
  if (!iso) return "—";
  const d = daysAgo(iso);
  const t = d <= 0 ? "today" : d === 1 ? "yesterday" : d < 30 ? d + "d ago"
    : d < 365 ? Math.round(d / 30) + "mo ago"
    : d < 730 ? (d / 365).toFixed(1) + "y ago" : Math.floor(d / 365) + "y ago";
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
  // Column-oriented on the wire, objects in here. One pass, 1,294 times, so the rest of the page can
  // read `r.stars` instead of `r[4]`.
  ROWS = d.rows.map(a => Object.fromEntries(d.cols.map((c, i) => [c, a[i]])));
  ROWS.forEach(r => {
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
    const age = r.first_seen ? daysAgo(r.first_seen) : Infinity;
    r.isnew = age >= 0 && age <= (d.window_days || 14);
  });
  NEW = ROWS.filter(r => r.isnew).length;
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
  // Again, now that the rows are here. `wire()` already called it off the document's own constant, which is
  // the best that can be said before this fetch resolves; this is the call that replaces that with the
  // stamp the rows brought with them, and the only one whose answer is about what is on screen.
  stamp();
  buildChips();
  readHash();
  render();
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

function chip(parent, label, pressed, onclick, title) {
  const b = document.createElement("button");
  b.className = "chip";
  b.textContent = label;
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
  D.os.forEach((o, i) => chip(oses, o, false, () => {
    const os = state.os.includes(i) ? state.os.filter(x => x !== i) : state.os.concat(i);
    set({os});
  }));
  // Debounced, because `render()` costs ~58ms at today's 1,294 rows on a throttled mobile CPU and used to
  // run once per keystroke -- so typing "agentic" rebuilt a 120-row table seven times and the input
  // visibly trailed the keyboard. Only ~20ms of that is row-count dependent; the rest is the innerHTML
  // rebuild and layout, so this is a defect at the current size and not only a future one. 150ms is short
  // enough to still read as live and collapses those seven renders into one.
  document.getElementById("q").oninput = e => {
    const v = e.target.value;
    clearTimeout(typing);
    typing = setTimeout(() => set({q: v}, true), 150);
  };
  document.getElementById("sort").onchange = e => set({sort: e.target.value});
  // Unhidden here rather than in the markup -- see the button for why it starts hidden. The announcement is
  // on this path only: `applyView` also runs from `render()`, and the view the page opened in is not news. It is
  // needed at all because nothing in the DOM changes, so a screen reader has no mutation to report and the
  // button's own new label is not read back after a click.
  const vb = document.getElementById("view");
  vb.hidden = false;
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
    nb.onclick = () => set({fresh: !state.fresh});
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
const CLEAR = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false, rising: false, saved: false};

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
  let proj = [];
  if (words.length) {
    proj = ROWS.filter(r => words.every(w => r.hay.includes(w)));
    for (const r of proj) r.rel = relevance(r, words);
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
    const b = ev.target.closest(".copy");
    if (b) copy(b);
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
    t.textContent = shown;
    // The same fortnight `stamp()` uses, deliberately -- one staleness threshold in the header rather than
    // two to learn. It is the right number for this clock too: the daily build is gated on a source list
    // having moved, so a quiet week is healthy and a tighter bound would cry wolf, but the weekly rebuild
    // publishes unconditionally, so past 14 days both crons have stopped and the page is on its own.
    const days = (Date.now() - ms) / 86400000;
    el.classList.toggle("late", days > 14);
    const age = days < 1 ? "Today." : days < 2 ? "Yesterday." : Math.round(days) + " days ago.";
    el.title = (Number.isNaN(live)
      ? "Built " + shown + ". This copy is not served by Pages, so its deployment time is unknown. "
      : "Published to GitHub Pages " + shown + ". ") + age
      + (days > 14 ? " Neither scheduled rebuild has run since, so the data here has drifted." : "");
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
  const btn = document.getElementById("view");
  if (!btn) return;
  const cards = state.view === "cards";
  btn.textContent = cards ? "Table view" : "Card view";
  btn.title = cards
    ? "Back to the table, which fits far more rows on a screen"
    : "Show each project as a card, with its screenshot";
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
  history.replaceState(null, "", s ? "#" + s : location.pathname);
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
  // A `#new=1` link outlives the fortnight it was written in. Honouring it once the window has emptied
  // would greet the reader with "nothing matches"; dropping it shows them the atlas instead.
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
  // First, because it is the most selective clause this function has -- a saved set is single digits
  // against 1,294 rows -- and because a Set lookup is the cheapest test here. `match` runs 1,294 times per
  // keystroke, so the order of these lines is not cosmetic.
  if (state.saved && !SAVED.has(r.nwo)) return false;
  if (state.fresh && !r.isnew) return false;
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
// replace `state.os` wholesale, never mutate it, so restoring the reference restores the value.
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
  if (state.rising) opts.push(["Drop the rising filter", {rising: false}]);
  // Offered like any other filter, and it is the one most likely to be the culprit: a saved set is single
  // digits, so crossing it with a topic or a platform empties the table far more easily than crossing two
  // build-wide filters does. The button drops the filter and never the set -- `countWith` only ever patches
  // `state`, so there is no path from an empty table to losing a collection.
  if (state.saved) opts.push(["Look beyond your " + SAVED.size + " saved", {saved: false}]);
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

// Rows matching every filter *except* the search box, ranked by how close their name is to what was
// typed. Only ever called when the exact pass returned nothing, which is what makes it safe: a query that
// does match is never diluted with approximate results, and the cost is paid on the one render where the
// reader would otherwise be staring at an empty table.
//
// It relaxes the search box and nothing else. A reader who has picked a topic and an OS has told us
// something they meant; the typo is in the word they were still typing, so the other filters stand.
function near(q) {
  const want = grams(q);
  // Under three trigrams is a five-character fragment -- a prefix someone is mid-way through typing
  // rather than a misspelling of anything, and matching it loosely would be noise.
  if (want.size < 3) return [];
  const saved = state.q;
  state.q = "";
  const pool = ROWS.filter(match);
  state.q = saved;
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
function relevance(r, words) {
  let total = 0;
  for (const w of words) total += hitScore(r, w);
  return total + Math.log10((r.stars || 0) + 1);
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

// A card's picture is fetched for the cards a reader is actually browsing, and not before. `loading="lazy"`
// was supposed to be this and demonstrably is not: measured at Lighthouse's 412x823 mobile viewport, the
// first paint still fetched three of them, 921,532 B, because Chrome's lazy threshold is a scroll distance
// and the whole first screen sits inside it. On a GitHub runner, on a slower simulated network with a
// longer network-quiet wait, it reached further down and fetched 1,357,388 B one half-hour and 1,827,508 B
// the next -- against a 307,200 B budget, on a byte-identical tree.
//
// So the `src` is withheld: the tag ships `data-src` and nothing is requested until the reader gives an
// input event that means they are looking at the list. Those four are the human ways of beginning a
// scroll -- a wheel or trackpad gesture, a touch, a key (arrows, space, Page Down, Tab), or a pointer
// going down on the scrollbar or on a card. Plain `scroll` is deliberately not among them, because it also
// fires for programmatic scrolling, including the viewport manipulation Lighthouse performs for its
// full-page screenshot once the trace is over; a budget a measuring tool can trip by looking at the page
// is a budget measuring the tool.
//
// This is only safe because the box is already reserved. `.shot img` carries `aspect-ratio:2/1` and the
// cards view inherits it, so a picture with no `src` occupies exactly the space the loaded one will and
// hydrating it shifts nothing. That is not a hope: blocking every image on the page moved layout shift
// from 0.5140 to 0.5140, in three runs each (JFH-216).
let ART = false, ARTIO = null;

function artLoad(i) { i.src = i.dataset.src; i.removeAttribute("data-src"); }

function cardArt() {
  if (!ART) return;
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
  document.querySelectorAll("#out img[data-src]").forEach(i => ARTIO.observe(i));
}

// `once` on each listener and the flag as well: four of them racing to be first would otherwise each walk
// the DOM. `render()` calls `cardArt()` again on every rebuild, which is what covers a filter, a search or
// a "show more" pressed by a reader who engaged with the page long ago.
//
// `window.addEventListener` and not the bare global, which resolves to the same function in a browser and
// does not exist in `tests/probe.mjs`. That harness executes this script against a stub DOM to assert on
// the HTML it renders, and it stubs `window` rather than the global scope -- so the bare form threw a
// ReferenceError at load and took all 276 of its assertions with it, which is exactly the failure it is
// there to catch. This is the only listener registered at the top level rather than inside init.
["wheel", "touchstart", "keydown", "pointerdown"].forEach(t =>
  window.addEventListener(t, () => { if (!ART) { ART = true; cardArt(); } },
                          {once: true, passive: true}));

function render() {
  // Reflect state onto the chips. Cheaper than rebuilding them and it keeps focus where it was.
  const press = (id, on) => [...document.getElementById(id).children]
    .forEach((b, i) => b.setAttribute("aria-pressed", on(i) ? "true" : "false"));
  press("cats", i => i === 0 ? !state.cat : D.cats[i - 1].slug === state.cat);
  press("tgts", i => i === 0 ? !state.tgt : D.targets[i - 1].slug === state.tgt);
  press("oses", i => state.os.includes(i));
  document.getElementById("strict").setAttribute("aria-pressed", state.strict ? "true" : "false");
  document.getElementById("new").setAttribute("aria-pressed", state.fresh ? "true" : "false");
  document.getElementById("rise").setAttribute("aria-pressed", state.rising ? "true" : "false");
  paintSaved();
  // Here as well as on the toggle, for the same reason the chips above are reflected here rather than only
  // where they are clicked: this is the one function every path that changes state already ends at, so a
  // `#view=cards` link, a hashchange and the browser's back button all arrive at the right layout without
  // each of them remembering to.
  applyView();

  const words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
  let hits = ROWS.filter(match);

  // A single mistyped letter used to produce an empty page even when the answer was one letter away. The
  // fallback runs only after the exact pass has failed, so a search that works is never diluted by it.
  // Near matches keep their similarity order rather than the reader's chosen sort: this is a list of
  // corrections, and "closest first" is the only ordering that makes it one.
  let approx = false;
  if (!hits.length && words.length) {
    const alt = near(state.q);
    if (alt.length) { hits = alt; approx = true; }
  }
  if (!approx) {
    const sort = effSort();
    if (sort === "relevance") for (const r of hits) r.rel = relevance(r, words);
    hits.sort(SORTS[sort]);
  }

  const ranked = hits.filter(r => r.stars).length;
  const countHTML = approx
    ? "<b>" + hits.length.toLocaleString() + "</b> near " +
      (hits.length === 1 ? "match" : "matches") + " · nothing matches “" + esc(state.q) + "” exactly"
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
    // A U+2009 thin space, not a full one, between an OS label and its verdict glyph, so that the label
    // ignore-this-line "Win✓" break across lines
    // and its glyph read as one unit beside its four neighbours rather than as ten separate words. The
    // title carries the sentence, because a glyph narrows "amber" to "uncertain" without saying of what.
    const os = D.os.map((o, k) => {
      const v = VERDICT[r.os[k]] || ["", "not established"];
      return '<span class="v' + r.os[k] + '" title="' + esc(o + ": " + v[1]) + '">' +
        o.slice(0, 3) + " " + v[0] + "</span>";
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
    const on = r.isnew ? ' <span class="newon">- New on ' + mmddyy(r.first_seen) + "</span>" : "";
    // The install line, with a button when the clipboard is reachable. The command is the one thing on a
    // row a reader wants to take away, and taking it meant selecting wrapped monospace text without
    // catching the blurb above it. The name is in the label because a screen-reader user arrives at
    // "Copy" 120 times a page and needs to know which project this one belongs to.
    const cmd = r.install
      ? '<div class="cmdrow"><code class="cmd">' + esc(r.install) + "</code>" +
        (CAN_COPY ? '<button class="copy" data-cmd="' + esc(r.install) +
          '" aria-label="Copy install command for ' + esc(r.name) + '">Copy</button>' : "") + "</div>"
      : "";
    return "<tr>" +
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
      '<td class="shot"><a href="' + page + '" tabindex="-1" aria-hidden="true">' +
        '<img loading="lazy" decoding="async" alt="" data-src="' + img + '"></a></td>' +
      '<td class="pj"><a class="nm" href="' + page + '">' + star + esc(r.name) + "</a>" + on +
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
        "</span></div></td>" +
      "</tr>";
  }).join("");
  // Every th carries the same class as the td beneath it. The Shot heading used not to, and since the
  // narrow-viewport rule hides `.shot` it hid only the body cell -- leaving five headings over four
  // columns, so "Shot" sat above the project names, "Project" above the stars, "Stars" above the
  // blurbs, and auto layout invented a fifth column to hang the surplus heading on.
  // Said above the table as well as in the live region, because a sighted reader who mistyped needs to
  // know *why* they are looking at LangGraph when they asked for "langraph" -- otherwise the correction
  // looks like the search quietly ignoring them.
  const note = approx
    ? '<p class="approx">Nothing matches <b>' + esc(state.q) + "</b> exactly. Closest by name" +
      (state.cat || state.tgt || state.os.length || state.strict || state.fresh
        ? ", within your other filters" : "") + ":</p>"
    : "";
  out.innerHTML = note +
    "<table><thead><tr><th class='n'>#</th><th class='shot'>Shot</th><th class='pj'>Project</th>" +
    "<th class='n st-c'>Stars</th>" +
    "<th class='hide tg'>Topic &amp; targets</th><th class='ds'>What it does</th>" +
    "<th class='c hide lc'>Lang / licence / push</th></tr></thead><tbody>" + rows +
    "</tbody></table>";
  // After the subtree exists and before the "show more" button is appended, because the pictures it has to
  // find are in the subtree. A no-op until the reader has given an input event, which is the whole point.
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

    label = {"orchestrators": "Orchestrators", **{k: t for k, t, *_ in b16.SHEETS}}
    tax.STARS.clear()
    tax.STARS.update(b16.star_map(records, orch, meta))
    agg = tax.by_repo(records + [dict(x, source="orchestrators") for x in orch])
    facets = b16.repo_pool(records, orch, label)
    for r in facets:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        r["stars"] = tax.STARS.get(r["nwo"], 0)

    # Before build_data, which reads the map it fills. Idempotent, so 17_markdown having already run in
    # this pipeline is fine -- it stamped the same repos with the same date and this call agrees.
    fresh = newness.resolve([r["nwo"] for r in facets])

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
    live = sum(1 for d in fresh.values() if newness.within(d))
    print(f"{len(fresh):,} arrived since {data['baseline']} · {live:,} inside the "
          f"{newness.WINDOW}-day window")


if __name__ == "__main__":
    main()
