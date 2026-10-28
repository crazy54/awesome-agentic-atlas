"""What every page family on the site carries, written once: the embedded typefaces, the build tags in the
footer, and the site script that paints them and opens the admin panel.

Five stages write pages and each keeps its own template, so anything all of them need is a constant here that
each one drops in, rather than five copies that drift. The palette is the exception and stays copied by hand,
for the reason `tests/theme_test.py` gives beside `palette_text()`: that test compares the copies.

THE TYPEFACES. Geist for text and Geist Mono for code and the build tags, both SIL OFL 1.1, served from
`docs/assets/fonts/` so a reader who has never installed either sees them. The mono face is the Nerd Fonts
patch, which adds the Octicons the tags draw; `scripts/subset_fonts.py` cut all three files down to
Latin plus those icons, about 70 KB together, and every page preloads all three.

`font-display:optional`, not `swap`, and the suite is why: under `swap` the face arrives after first paint,
the text re-wraps in Geist's metrics, and `tests/spotlight-check.mjs` measured the homepage's spotlight
moving 18px on a phone. `optional` gives the face about 100ms to arrive -- which a preloaded 32 KB file
almost always does -- and otherwise keeps the platform face for that one page view rather than moving
anything; the file is cached by then, so the next page has it. Nothing a reader is looking at ever jumps.

The Octicons are the exception and have a family of their own, "Atlas Icons": the same mono file, only its
private-use range, and `swap`. Under `optional` a face that misses its window is given up on for the page,
and an icon drawn in the fallback is an empty box. The site script writes the icons into the build tags only
once `document.fonts` has loaded "Atlas Icons", into spans that were empty, below the fold.

`up` everywhere below is the path from the file the rule lands in back to `docs/`: a stylesheet's URLs
resolve against the stylesheet, a preload's against the document, which is why the two take it separately.
"""
from __future__ import annotations

import hashlib
from html import escape
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
ASSETS = DOCS / "assets"

FONTS = (("Geist", "geist.woff2", "100 900"),
         ("Geist Mono", "geist-mono.woff2", "400"),
         ("Geist Mono", "geist-mono-600.woff2", "500 800"))
# The build tags' Octicons, from the 400 file. See the note on `optional` above for why they are a family.
ICONS = ("Atlas Icons", "geist-mono.woff2", "U+F400-F5FF")

# The two files the site script is. The admin panel is imported by the first, under the first's `?v=`, so
# one hash covers both and an edit to the panel alone still moves the URL a reader's cache is keyed on.
SITE_JS = "atlas-site.js"
ADMIN_JS = "atlas-admin.js"

# THE SITE KIT. Jeremy's banners, scheduled in his blog admin, drawn by one script from his own host
# (https://jeremyfhall.com/kit/). Last in every page family's `<head>`, deferred and with no slot, so a banner
# only ever floats (a toast or a footer bar) and nothing a reader is looking at moves -- the same promise
# `font-display:optional` keeps above. The URL is versioned and never changes; the `integrity` hash pins the
# bytes, so a new kit version is a new URL and a new hash here, and every page moves with it. Absolute, so it
# takes no `up`. Same bytes on every page and every day, so the detail pages stay byte-identical week to week.
SITE_KIT = ('<script src="https://jeremyfhall.com/kit/site-kit.v1.js" integrity="sha384-XSpQk1dubcVV4dWVZL3B8R6EsmEa4vwZ8PlVTkEmE+RY28H8OP2Y36BpTK7vCJI2" crossorigin="anonymous" data-site="atlas" defer></script>')


def font_faces(up: str) -> str:
    """The @font-face rules, for a stylesheet that sits `up` away from `docs/`."""
    faces = "".join(
        f'@font-face{{font-family:"{family}";src:url({up}assets/fonts/{name}) format("woff2");'
        f"font-weight:{weight};font-style:normal;font-display:optional}}\n"
        for family, name, weight in FONTS)
    family, name, ranges = ICONS
    return faces + (f'@font-face{{font-family:"{family}";src:url({up}assets/fonts/{name}) format("woff2");'
                    f"unicode-range:{ranges};font-display:swap}}\n")


def font_preload(up: str) -> str:
    """A preload per file. Every page uses all three -- text, the tags' labels, the tags' icons -- and under
    `optional` a face that is not fetched early enough is a face this page view does not get."""
    return "".join(f'<link rel="preload" href="{up}assets/fonts/{name}" as="font" type="font/woff2" crossorigin>\n'
                   for _, name, _ in FONTS)


def version(files: tuple[str, ...] = (SITE_JS, ADMIN_JS)) -> str:
    """A hash of the site script and the panel, line endings normalised.

    Normalised because the tree is checked out CRLF on Windows and served LF by Pages, and a version that
    moved with the checkout's platform would bust every reader's cache for an edit nobody made.
    """
    h = hashlib.sha256()
    for f in files:
        p = ASSETS / f
        if p.is_file():
            h.update(p.read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:10]


def site_script(up: str) -> str:
    """The module tag. `up` is from the document to `docs/`."""
    return f'<script type="module" src="{up}assets/{SITE_JS}?v={version()}"></script>'


# THE BUILD TAGS. One pill per workflow plus the Pages deployment, in the footer of every page, painted live
# from the GitHub API by the site script. The markup is deliberately the same bytes on every page and every
# day: `22_detail.py`'s pages are held byte-identical week to week (see `tests/detail-churn.mjs`), so nothing
# volatile -- no date, no status -- may be written into them at build time. Each pill starts as a neutral dot
# with its label, links to its workflow, and says "status unavailable" to a reader whose browser never runs
# the script or cannot reach the API. Shaped after Prism's "Version Pill" (callouts-version-pill): the face is
# the mono, the state is a glowing dot, and the colours are the page's own tokens, so every theme repaints it.
TAGS = (("daily", "daily.yml", "Daily build: the site and Markdown"),
        ("weekly", "weekly.yml", "Weekly build: screenshots and workbooks"),
        ("tests", "tests.yml", "The test suite"))


def buildtags(repo: str) -> str:
    """The footer strip. Static bytes; see the note above."""
    r = escape(repo)
    pills = "".join(
        f'<a class="btag" data-wf="{wf}" href="https://github.com/{r}/actions/workflows/{wf}" '
        f'title="{escape(title)}"><span class="bico" aria-hidden="true"></span><i class="bdot" '
        f'aria-hidden="true"></i><b>{name}</b><span class="bv">&middot;</span></a>'
        for name, wf, title in TAGS)
    pills += (f'<a class="btag" data-pages href="https://github.com/{r}/deployments/github-pages" '
              'title="When GitHub Pages last published this site"><span class="bico" aria-hidden="true">'
              '</span><i class="bdot" aria-hidden="true"></i><b>deployed</b><span class="bv">&middot;</span></a>')
    return (f'<div class="btags" id="btags" data-repo="{r}" role="group" aria-label="Build status">'
            f'{pills}<span class="sr" id="btagsr">Build status is fetched from GitHub when the page loads.'
            '</span></div>')


BUILDTAGS_CSS = """/* The build tags in the footer. See `buildtags()` in scripts/sitewide.py. Two classes deep so that
   `footer a`, which every page family has, does not outrank them. */
.btags{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px;font:600 11px/1 var(--mono)}
.btags .btag{display:inline-flex;align-items:center;gap:6px;min-height:24px;padding:4px 9px;border-radius:7px;
  color:var(--ink);background:var(--band);border:1px solid var(--grid);text-decoration:none;
  letter-spacing:.01em}
.btags .btag:hover{border-color:var(--link);text-decoration:none}
.btags .btag b{font-weight:600}
.btags .btag .bv{color:var(--muted);font-weight:500}
.btags .btag .bico{color:var(--muted);font:400 12px/1 "Atlas Icons",var(--mono)}
.btags .btag .bico:empty{display:none}
.bdot{width:7px;height:7px;flex:none;border-radius:50%;background:var(--off)}
.btags .btag[data-state=ok] .bdot{background:var(--good);box-shadow:0 0 8px var(--good)}
.btags .btag[data-state=bad] .bdot{background:var(--warn);box-shadow:0 0 8px var(--warn)}
.btags .btag[data-state=run] .bdot{background:var(--link);box-shadow:0 0 8px var(--link)}
.btags .btag[data-state=ok] .bv{color:var(--good)}
.btags .btag[data-state=bad] .bv{color:var(--warn)}
.btags .btag[data-state=run] .bv{color:var(--link)}
@media (prefers-reduced-motion:no-preference){
  .btags .btag[data-state=run] .bdot{animation:bpulse 1.6s ease-in-out infinite}
  @keyframes bpulse{50%{opacity:.35}}
}
@media print{.btags{display:none}}
"""


# THE 404 PAGE. GitHub Pages serves `docs/404.html` for any path it has no file for, at that path -- so every
# URL in it is root-absolute, where everything else on the site is relative. The custom domain in
# `docs/CNAME` is what makes `/` the site root; the github.io address redirects there.
#
# It also finishes the admin tail. `/catalog/=admin1337?` is a path, not a query -- the trailing `?` opens an
# empty one -- and Pages has no file there, so the reader lands here. The script turns it into
# `/catalog/?=admin1337`, which is a page that exists with the tail where `atlas-site.js` looks for it. A path
# with no tail is a plain 404 and stays one: `noindex`, the site's own theme and type, two ways home.
def not_found(repo: str, head_theme: str) -> str:
    """The whole of `docs/404.html`. `head_theme` is `20_landing.HEAD_THEME`, the shared pre-paint script."""
    return f"""<!doctype html>
<html lang="en" data-theme="dark" data-skin="graphite">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Not here &mdash; Awesome Agentic Atlas</title>
<meta name="robots" content="noindex">
<script>
(function () {{
  var p = location.pathname, m;
  try {{ p = decodeURIComponent(p); }} catch (e) {{}}
  m = /^(.*?)\\/?=admin1337\\??$/.exec(p);
  if (m) location.replace((m[1] || "") + "/?=admin1337" + location.hash);
}})();
</script>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{font_preload("/")}{head_theme}<link rel="stylesheet" href="/pages.css">
<style>.nf{{max-width:640px;margin:12vh auto 8vh;padding:0 20px}}.nf h1{{margin:0 0 .4em;font-size:28px;letter-spacing:-.01em}}
.nf p{{color:var(--ink2)}}.nf code{{font:13px/1.5 var(--mono);color:var(--muted)}}</style>
{SITE_KIT}
</head>
<body>
<main class="nf">
  <h1>Nothing at this address</h1>
  <p>The Atlas has no page at <code id="nfp"></code>. A project&rsquo;s page moves when its repository is renamed,
  and a topic&rsquo;s when the taxonomy changes.</p>
  <p><a href="/">The shelves</a> &middot; <a href="/catalog/">Search every project</a> &middot;
  <a href="/repo/">Every project, one page each</a></p>
</main>
<footer><div class="wrap">
  {buildtags(repo)}
</div></footer>
<script>document.getElementById("nfp").textContent = location.pathname;</script>
{site_script("/")}
</body>
</html>
"""
