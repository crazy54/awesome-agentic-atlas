"""What every page family on the site carries, written once: the embedded typefaces, the build tags in the
footer, and the site script that paints them and opens the admin panel.

Five stages write pages and each keeps its own template, so anything all of them need is a constant here that
each one drops in, rather than five copies that drift. The palette used to be the exception -- copied by hand
into three generators and held together by a byte-for-byte comparison in `tests/theme_test.py` -- and it is
not any more: `THEME_CSS` and `HEAD_THEME` below are the only copies, for the reason given beside them.

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


# THE LOCAL-AI PAGE'S NAME. The owner is choosing it from a shortlist, so the title, the slug and the pitch
# live here, once, and every stage that writes the page or a link to it reads them: `32_local.py` for the page
# itself, and the nav of the homepage, the catalogue, the topic pages, Discover and the collections. Renaming
# is this one edit and a rebuild. Changing `slug` moves the URL, and the old one 404s -- so do it before launch.
# Here rather than in `32_local.py` because importing a numbered stage for a nav label would drag the page
# stack in behind it; this module is already imported by every page family.
LOCAL_PAGE = {
    "title": "Run It Local",
    "slug": "local",
    "pitch": "What AI can your computer run? Find out in a minute, then copy two lines to run it.",
}

# LOOKALIKES' NAME, on the same terms and for the same reasons as LOCAL_PAGE above: the title, the slug and the
# pitch, once. Read by `33_alike.py` for the page, by the nav of the homepage, the catalogue, the topic pages,
# Discover and the collections for the link beside the local-AI page's, and by `22_detail.py` for the "Find
# alternatives" button every detail page carries. Changing `slug` moves the URL and the old one 404s.
ALIKE_PAGE = {
    "title": "Lookalikes",
    "slug": "alike",
    "pitch": "Paste a GitHub or GitLab link, or type a project's name, and see the projects that do the same thing.",
}


# THE THEMES. Three, and one choice that is not a theme.
#
# Light, Dark and High contrast, and "System", which stores nothing and lets the operating system pick: high
# contrast if it asks for more contrast (`prefers-contrast: more`), otherwise its light or dark preference. The
# palette is the mascot's. Archie is warm white ceramic, near-black graphite and a bright lime with steel and
# brass details, and he stands on the homepage masthead, so a page in other colours is a page he is visiting
# rather than one he lives on:
#   * Light is the ceramic. Warm glaze for the page and the panels rather than stark white, graphite ink, and
#     the lime deepened to an olive (`--bar`, `--link`) wherever it is text, a ring or a hairline, because the
#     lime itself is 1.7:1 on the glaze and cannot be read.
#   * Dark is the graphite. His lens-black for the page, his graphite for the panels, ceramic ink, steel for
#     the captions, and the lime at full brightness as the accent.
#   * High contrast is for low-vision readers, and it is the one held to a stricter arithmetic: every text pair
#     7:1 (WCAG AAA), every line, ring and icon 3:1, no hairline that is merely a hint. Black, white and his
#     iris lime. It also changes things that are not colours, all of them paint rather than layout: links are
#     underlined so they are not told apart by hue alone, the focus ring is 3px with a black halo, a pressed
#     control carries an outline as well as a fill, and nothing is drawn behind text (no wash, no masthead
#     art, no text halo, no drop shadows).
#
# The lime fill is its own pair of tokens, `--act` and `--onact`, and that is the one new idea in the token set.
# `--bar` is drawn as text in a dozen rules -- eyebrows, counts, the inverted badge -- so in light it has to be
# the deep olive, and an olive button is a drab one. The primary button and a pressed chip are not text, so
# they take `--act`, which is the real lime in every theme, with graphite ink on it at 8.9:1 or better and a
# 1px `--act-edge` drawn as an inset shadow so the lime has an edge on the glaze without the box growing.
# `--act-hi` is its hover.
#
# ONE COPY, and why it is here. There used to be eight themes times two modes in four hand-kept copies --
# `19_pages.py`, `20_landing.py`, `22_detail.py` and a set of literals in every head script -- held to each
# other by a byte comparison. Three themes in one constant need no comparison: the three generators drop
# `THEME_CSS` into their own stylesheets (the catalogue's inline `<style>`, `pages.css`, `detail.css`), every
# page family's `<head>` takes `HEAD_THEME`, and `tests/theme_test.py` measures this file.
#
# What is NOT here: anything that sizes or places a box. The redesign that introduced this block was held to
# "the layout does not move", and that is a property of this constant as much as of the values in it -- every
# rule below changes paint only (colour, background, border colour, outline, shadow, text decoration), and
# `tests/cards-check.mjs` measures the layout in every theme. A border *width*, a padding or a font weight
# added here would be a layout change on every page of the site at once.
THEMES = ("light", "dark", "contrast")

# The colour tokens, per theme. Opaque hex, every one, because WCAG contrast is a ratio between two colours and
# an rgba over an unknown backdrop has no second colour to be a ratio against. `theme_test.py` reads these out
# of `THEME_CSS` and checks every pairing the stylesheets use -- a ratio written in a comment is not a test.
PALETTE = {
    "dark": {
        "surface": "#121314", "plane": "#1A1A1A", "band": "#252423", "ink": "#F3EFE8", "ink2": "#D9D3C8",
        "muted": "#ABA69F", "grid": "#3E3C39", "link": "#CBE46E", "bar": "#A4C812",
        "good": "#6FD3A0", "warn": "#F29484", "off": "#ABA69F", "onbar": "#151614",
        "act": "#A4C812", "act-hi": "#B9DD2E", "act-edge": "#C4E04A", "onact": "#151614",
        "accent-sky": "#8CC6DE", "accent-mint": "#6FD3A0", "accent-gold": "#DDB36A",
        "accent-coral": "#F29484", "accent-violet": "#B9AAF0"},
    "light": {
        "surface": "#F1EDE6", "plane": "#FBFAF7", "band": "#E8E3D9", "ink": "#1C1B1B", "ink2": "#3A3835",
        "muted": "#5E5A54", "grid": "#CBC3B5", "link": "#3B5C00", "bar": "#456A00",
        "good": "#14704A", "warn": "#A23B2A", "off": "#5E5A54", "onbar": "#FFFFFF",
        "act": "#A4C812", "act-hi": "#B6D93A", "act-edge": "#6B8A00", "onact": "#1C1B1B",
        "accent-sky": "#1F5F7A", "accent-mint": "#14704A", "accent-gold": "#80560F",
        "accent-coral": "#A23B2A", "accent-violet": "#5B4A9E"},
    "contrast": {
        "surface": "#000000", "plane": "#000000", "band": "#141414", "ink": "#FFFFFF", "ink2": "#F2F2F2",
        "muted": "#D6D6D6", "grid": "#B5B5B5", "link": "#E1FA64", "bar": "#DCF55E",
        "good": "#7DF0B0", "warn": "#FFB4A8", "off": "#D6D6D6", "onbar": "#000000",
        "act": "#DCF55E", "act-hi": "#FFFFFF", "act-edge": "#FFFFFF", "onact": "#000000",
        "accent-sky": "#A6E1FF", "accent-mint": "#7DF0B0", "accent-gold": "#FFD98A",
        "accent-coral": "#FFB4A8", "accent-violet": "#D9CCFF"},
}

# The background behind the layout, per theme. Two soft pools of light, fixed to the window: the lime one high
# on the right, where the mascot stands, and a ceramic one on the left under the title. Static gradients, so a
# reader who asked for reduced motion has nothing to ask them to stop doing. High contrast has none.
WASH = {
    "dark": "radial-gradient(1100px 560px at 82% -14%,rgba(164,200,18,.09),transparent 68%),"
            "radial-gradient(900px 520px at 0% -10%,rgba(235,229,218,.05),transparent 70%)",
    "light": "radial-gradient(1100px 560px at 82% -14%,rgba(164,200,18,.12),transparent 68%),"
             "radial-gradient(900px 520px at 0% -10%,rgba(255,255,255,.75),transparent 70%)",
    "contrast": "none",
}


def _tokens(theme: str) -> str:
    return "".join(f"--{k}:{v};" for k, v in PALETTE[theme].items()) + f"--wash:{WASH[theme]};"


THEME_CSS = (
    "/* THE THEMES. Written by `THEME_CSS` in scripts/sitewide.py, which explains every value; do not edit the\n"
    "   copy in a generated file. Dark is on `:root`, so it needs no attribute to be true -- it is the floor a\n"
    "   reader with JavaScript off gets. */\n"
    ":root{color-scheme:dark;" + _tokens("dark")
    # The structural half. Not colours, and not per theme: one typeface, an opaque panel, no backdrop filter.
    # `--bdf:none` and not `blur(0px)`: a non-none backdrop-filter makes an element a containing block and a
    # stacking context, which would re-parent the mascot's speech bubble and re-rank the pinned bar.
    + '--ui:"Geist","Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;'
    '--mono:"Geist Mono",ui-monospace,"Cascadia Mono",Consolas,"Liberation Mono",monospace;'
    "--panel:var(--plane);--bdf:none}\n"
    "html[data-theme=light]{color-scheme:light;" + _tokens("light") + "}\n"
    "html[data-theme=contrast]{color-scheme:dark;" + _tokens("contrast") + "--lift:none;--lift-hi:none}\n"
    + r"""/* Paint only, below this line: no rule here may size or place a box (see the note in sitewide.py). */
/* The focus ring, for every page family: the accent, 2px, clear of the control so it never sits on the
   control's own border. `:focus-visible` so a click does not leave a ring on the chip that was pressed. */
:focus-visible{outline:2px solid var(--bar);outline-offset:2px;border-radius:4px}
::selection{background:color-mix(in srgb,var(--act) 42%,transparent);color:var(--ink)}
/* The primary button, on every page family that has one: the lime fill and its edge. An inset shadow is the
   edge rather than a border, so the box is the size it always was; the second inset is the glaze's own
   highlight, and the soft drop under it is the only glow on the page. */
.cta{box-shadow:inset 0 0 0 1px var(--act-edge),inset 0 1px 0 rgba(255,255,255,.28),
  0 10px 24px -14px color-mix(in srgb,var(--act) 80%,transparent)}
.cta:hover{background:var(--act-hi);filter:none}
.cta:active{box-shadow:inset 0 0 0 1px var(--act-edge),inset 0 2px 4px rgba(0,0,0,.18)}
/* HIGH CONTRAST: the things that are not colours. */
/* Links are underlined, so a link is not told from text by its hue alone (WCAG 1.4.1) -- except the ones drawn
   as a pill or a button, whose border already says "press me" in a shape rather than a colour. */
html[data-theme=contrast] a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em}
html[data-theme=contrast] a:hover{text-decoration-thickness:2px}
html[data-theme=contrast] :is(.chip,.cta,.bychip,.btag,.stamp,.ghstar){text-decoration:none}
html[data-theme=contrast] :focus-visible{outline:3px solid var(--bar);outline-offset:2px;box-shadow:0 0 0 7px #000}
html[data-theme=contrast] .cta{box-shadow:inset 0 0 0 2px var(--act-edge)}
html[data-theme=contrast] [aria-pressed=true]{outline:2px solid var(--ink);outline-offset:1px}
html[data-theme=contrast] *{text-shadow:none!important}
html[data-theme=contrast] ::selection{background:var(--bar);color:var(--onbar)}
/* FORCED COLOURS (Windows High Contrast and its kin). The system palette replaces every colour, which is the
   point, and three things would go with it: the state of a pressed control, the edge of a button whose only
   edge was its fill, and the theme swatches, which are previews and mean nothing in system colours. Outlines
   rather than borders, so nothing grows. */
@media (forced-colors:active){
  :focus-visible{outline:3px solid Highlight;outline-offset:2px}
  [aria-pressed=true]{outline:2px solid Highlight;outline-offset:1px}
  .cta{outline:1px solid ButtonText;outline-offset:-1px}
  .thsw{forced-color-adjust:none}
  .mhart{background:none!important}
}
""")

# The pre-paint script, for every page family's `<head>`: it settles the theme before first paint, because a
# reader who chose light, or whose OS asks for light, otherwise gets a frame of near-black first.
#
# One `theme-color` meta, set by script, rather than two `media` variants: the HTML spec picks the *first* such
# element whose media matches, so a pair keyed on `prefers-color-scheme` cannot be overridden by anything
# appended later, and a reader who chose against their OS would see the chrome in the opposite colour to the
# page. Its value is `--plane`, the header's own background, and it is a literal because no stylesheet has
# parsed yet when this runs; with JavaScript off it stays dark's, which agrees with the `data-theme="dark"`
# floor on <html>. After paint the page scripts re-derive it from the computed value (`THEME_JS`).
#
# Precedence is the reader's choice, then the operating system, then dark. A stored value that is not one of
# the three themes is not honoured -- `theme` is reader-writable storage that outlives the release that wrote
# it. THE MIGRATION is the two keys this deletes. The old site had eight colour "skins" on a second axis,
# `atlas-skin`, and every one of them had a light and a dark half; the half a reader was wearing is already in
# `theme`, so the nearest new theme is the one they land on without anything being mapped, and the skin key,
# and `atlas-unlock` (which only ever unlocked the hidden ninth skin), are removed.
_PLANES = ", ".join(f'{t}: "{PALETTE[t]["plane"]}"' for t in THEMES)
HEAD_THEME = f"""<meta name="theme-color" id="tc" content="{PALETTE['dark']['plane']}">
<script>
try {{
  var t = localStorage.getItem("theme");
  if (localStorage.getItem("atlas-skin") !== null || localStorage.getItem("atlas-unlock") !== null) {{
    localStorage.removeItem("atlas-skin"); localStorage.removeItem("atlas-unlock");
  }}
  if (t !== "light" && t !== "dark" && t !== "contrast")
    t = matchMedia("(prefers-contrast: more)").matches ? "contrast"
      : matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  document.documentElement.dataset.theme = t;
  document.getElementById("tc").content = {{{_PLANES}}}[t];
}} catch (e) {{}}
</script>
"""

# The same resolution, for scripts that run after paint: the Settings menu, the light/dark toggle on the facet
# and project pages, and the OS-preference listeners. A string, so each page family inlines it beside its own
# controls without a second request.
#   atlasTheme().choice()  -> "system" | "light" | "dark" | "contrast"   (what the reader picked)
#   atlasTheme().set(c)    -> stores the choice (removing it for "system"), applies it, repaints the chrome
#   atlasTheme().follow(f) -> calls f() after the OS preference changes, for a reader on "system"
#   atlasTheme().refresh() -> re-reads the stored choice and applies it (another tab changed it)
# A function declaration, memoised, rather than a `var` holding an IIFE, and that is load-bearing: the
# catalogue's page script calls `wireSettings()` from `wire()` hundreds of lines *above* where this is
# inlined, and a function declaration is hoisted with its body where a `var` is hoisted as `undefined`. The
# first call also re-applies the stored choice, which is what catches up a page whose head script is a
# release older than this one: the project pages are rewritten by the daily build, and until then theirs
# knows only light and dark.
THEME_JS = r"""function atlasTheme() {
  if (atlasTheme.api) return atlasTheme.api;
  var root = document.documentElement;
  var stored = function () { try { return localStorage.getItem("theme"); } catch (e) { return null; } };
  var valid = function (t) { return t === "light" || t === "dark" || t === "contrast"; };
  var system = function () {
    try {
      return matchMedia("(prefers-contrast: more)").matches ? "contrast"
        : matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
    } catch (e) { return "dark"; }
  };
  var apply = function () {
    var t = stored();
    root.dataset.theme = valid(t) ? t : system();
    delete root.dataset.skin;
    var plane = getComputedStyle(root).getPropertyValue("--plane").trim(), tc = document.getElementById("tc");
    if (plane && tc) tc.content = plane;
  };
  var api = {
    choice: function () { var t = stored(); return valid(t) ? t : "system"; },
    refresh: apply,
    set: function (c) {
      try { if (c === "system") localStorage.removeItem("theme"); else localStorage.setItem("theme", c); } catch (e) {}
      apply();
    },
    follow: function (f) {
      var on = function () { if (api.choice() === "system") { apply(); if (f) f(); } };
      try {
        matchMedia("(prefers-color-scheme: light)").addEventListener("change", on);
        matchMedia("(prefers-contrast: more)").addEventListener("change", on);
      } catch (e) {}
    }
  };
  apply();
  return (atlasTheme.api = api);
}
"""


# THE BUILD TAGS. One pill per workflow plus the Pages deployment, in the footer of every page, painted live
# from the GitHub API by the site script. The markup is deliberately the same bytes on every page and every
# day: `22_detail.py`'s pages are held byte-identical week to week (see `tests/detail-churn.mjs`), so nothing
# volatile -- no date, no status -- may be written into them at build time. Each pill starts as a neutral dot
# with its label, links to its workflow, and says "status unavailable" to a reader whose browser never runs
# the script or cannot reach the API. Shaped after Prism's "Version Pill" (callouts-version-pill): the face is
# the mono, the state is a glowing dot, and the colours are the page's own tokens, so every theme repaints it.
TAGS = (("daily", "daily.yml", "Daily build: the site and Markdown"),
        ("weekly", "weekly.yml", "Weekly build: screenshots and a full refresh"),
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
    """The whole of `docs/404.html`. `head_theme` is `HEAD_THEME` above, the shared pre-paint script."""
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
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
