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


# THE THEMES. Two, and one choice that is not a theme.
#
# Light and Dark, and "System", which stores nothing and lets the operating system's light/dark preference
# pick. The palette is the mascot's. Archie is warm white ceramic, near-black graphite and a bright lime with
# steel and brass details, and he stands on the homepage masthead, so a page in other colours is a page he is
# visiting rather than one he lives on. The design language is neumorphic glass: frosted, translucent panels
# that blur a field of his colours behind them, soft surfaces extruded out of that field by a pair of
# shadows (one light, one dark), and controls that are pushed *in* when they are pressed.
#   * Light is glass on the ceramic. The field is his egg-shell with pools of his iris light and his lime;
#     the panels are white glass over it, and the ink is his graphite. The lime is deepened to an olive
#     (`--bar`, `--link`) wherever it is text or a ring, because the lime itself is 1.5:1 on the glaze.
#   * Dark is the graphite. A dark, dark grey for the field with at most a faint lime glow; graphite glass;
#     his egg-shell (`#EBE5DA`, the main colour of his body) for the text; and the lime for everything that
#     is not body text -- titles (`--title`), the important words (`--bar`), and the lines (`--grid` and the
#     glass edge are lime-tinted).
#
# There used to be a third theme, High contrast. It is gone from the menu, and what it was for is not: a
# reader whose system asks for more contrast (`prefers-contrast: more`), or forces its own colours
# (`forced-colors: active`), or asks for less transparency (`prefers-reduced-transparency: reduce`), gets
# the strengthening below automatically, in either theme -- solid panels, no blur, no field, no soft
# shadows, and (for more contrast) stronger text, 3:1 lines, underlined links and a 3px focus ring. A rule
# keyed on what the reader's system says reaches more of the readers who need it than a menu item they have
# to find. A stored "contrast" is migrated silently to "dark" (see HEAD_THEME), which is the half it was:
# high contrast was a black, dark-scheme theme.
#
# The lime fill is its own pair of tokens, `--act` and `--onact`. `--bar` is drawn as text in a dozen rules --
# eyebrows, counts, the inverted badge -- so in light it has to be the deep olive, and an olive button is a
# drab one. The primary button and a pressed chip are not text, so they take `--act`, which is the real lime
# in both themes, with graphite ink on it at 8.9:1 or better and a 1px `--act-edge` drawn as an inset
# shadow so the lime has an edge on the glaze without the box growing. `--act-hi` is its hover.
#
# ONE COPY, and why it is here. There used to be eight themes times two modes in four hand-kept copies --
# `19_pages.py`, `20_landing.py`, `22_detail.py` and a set of literals in every head script -- held to each
# other by a byte comparison. Two themes in one constant need no comparison: the three generators drop
# `THEME_CSS` into their own stylesheets (the catalogue's inline `<style>`, `pages.css`, `detail.css`), every
# page family's `<head>` takes `HEAD_THEME`, and `tests/theme_test.py` measures this file.
#
# What is NOT here: anything that sizes or places a box. Both redesigns were held to "the layout does not
# move", and that is a property of this constant as much as of the values in it -- every rule below changes
# paint only (colour, background, border colour and radius, outline, shadow, backdrop filter, text
# decoration), and `tests/cards-check.mjs` measures the layout in both themes. A border *width*, a padding or
# a font weight added here would be a layout change on every page of the site at once. That is why every
# glass edge and every neumorphic rim is a `box-shadow` or a border *colour*, never a new border.
THEMES = ("light", "dark")

# The colour tokens, per theme. Opaque hex, every one, because WCAG contrast is a ratio between two colours and
# an rgba over an unknown backdrop has no second colour to be a ratio against. The glass is translucent, so
# these are not all the colours a reader sees -- `GLASS` below is the rest -- and `theme_test.py` measures
# text against what the glass actually composites to over its worst backdrop, not just against these.
#   --surface  the field's base colour, and the page's colour wherever there is no glass
#   --plane    an opaque stand-in for a glass panel (the panel over the bare field), and the panel itself
#              wherever the glass is switched off
#   --band     chips, inputs and raised rows: a step off the plane
#   --title    headings: the ink in light, the lime in dark
PALETTE = {
    "dark": {
        "surface": "#1C1C1B", "plane": "#2A2A27", "band": "#2F2E2C", "ink": "#EBE5DA", "ink2": "#D4CEC3",
        "muted": "#AEAAA4", "title": "#A4C812", "grid": "#3F4526", "link": "#DCF55E", "bar": "#A4C812",
        "good": "#6FD3A0", "warn": "#F29484", "off": "#AEAAA4", "onbar": "#151614",
        "act": "#A4C812", "act-hi": "#B9DD2E", "act-edge": "#C4E04A", "onact": "#151614",
        "accent-sky": "#8CC6DE", "accent-mint": "#6FD3A0", "accent-gold": "#DDB36A",
        "accent-coral": "#F29484", "accent-violet": "#B9AAF0"},
    "light": {
        "surface": "#EAE5DA", "plane": "#F5F2EC", "band": "#F1EEE7", "ink": "#1C1B1B", "ink2": "#3A3835",
        "muted": "#56524C", "title": "#1C1B1B", "grid": "#CEC6B7", "link": "#3B5C00", "bar": "#3E6000",
        "good": "#0F6741", "warn": "#A23B2A", "off": "#56524C", "onbar": "#FFFFFF",
        "act": "#A4C812", "act-hi": "#B6D93A", "act-edge": "#5E7A00", "onact": "#1C1B1B",
        "accent-sky": "#1F5F7A", "accent-mint": "#0F6741", "accent-gold": "#7A520E",
        "accent-coral": "#A23B2A", "accent-violet": "#5B4A9E"},
}

# THE GLASS, per theme: everything that is translucent or a shadow, so none of it is a colour a ratio can be
# taken against on its own. `theme_test.py` reads these and does the compositing.
#   panel / panel-hi  the glass fill, as (colour, alpha). `panel` is a STATIC panel -- header, footer, the
#                     spotlight, a card -- which only ever sits on the field, so its worst backdrop is the
#                     field's darkest (light) or lightest (dark) point, every pool at its peak. `panel-hi` is a
#                     FLOATING one -- the pinned search bar, a menu, a dialog -- which anything can scroll
#                     under, a screenshot included, so its worst backdrop is pure black (light) or pure white
#                     (dark). That is why it is denser.
#   pools             the field's pools of colour, as (colour, peak alpha), for the same arithmetic. They must
#                     agree with the gradients in `WASH`; the test parses `WASH` and checks they do.
#   edge              the glass's hairline: a border *colour*, on borders the layout already has
#   ctl-edge          a control's border colour (chips, inputs), a little firmer than the glass's
#   raise / -sm / -hi the neumorphic extrusion: a light shadow up and left, a dark one down and right
#   press             the same pair inset: a well (inputs, code) or a control being pressed
#   press-act         a pressed lime control: the lime pushed in
#   fog               Archie's fog prank (`html[data-fog]`, archie.js): the glass frosted over for 1.6 s, as
#                     (colour, alpha). Denser than the panel, so every text pair still passes while it is up;
#                     it is measured with the static panels, over the field's worst point.
GLASS = {
    "dark": {
        "panel": ("#33322F", .62), "panel-hi": ("#2B2A29", .94),
        "pools": (("#A4C812", .085), ("#EBE5DA", .035)),
        "edge": "rgba(164,200,18,.20)", "ctl-edge": "rgba(164,200,18,.22)",
        "raise": "-6px -6px 18px rgba(255,255,255,.035),10px 12px 28px rgba(0,0,0,.55)",
        "raise-sm": "-2px -2px 6px rgba(255,255,255,.045),3px 4px 10px rgba(0,0,0,.5)",
        "raise-hi": "-3px -3px 8px rgba(255,255,255,.06),5px 7px 16px rgba(0,0,0,.6)",
        "press": "inset 3px 3px 7px rgba(0,0,0,.55),inset -2px -2px 6px rgba(255,255,255,.045)",
        "press-act": "inset 2px 2px 5px rgba(0,0,0,.32),inset -2px -2px 5px rgba(255,255,255,.3)",
        "fog": ("#3C3B38", .9), "bdf": "blur(20px) saturate(1.4)"},
    "light": {
        "panel": ("#FFFFFF", .52), "panel-hi": ("#FCFBF8", .86),
        "pools": (("#DCF55E", .55), ("#A4C812", .34)),
        "edge": "rgba(255,255,255,.9)", "ctl-edge": "rgba(120,108,86,.26)",
        "raise": "-10px -10px 26px rgba(255,255,255,.75),12px 14px 34px rgba(98,88,60,.22),"
                 "inset 0 1px 0 rgba(255,255,255,.95)",
        "raise-sm": "-3px -3px 8px rgba(255,255,255,.9),3px 4px 10px rgba(104,92,66,.20)",
        "raise-hi": "-4px -4px 10px rgba(255,255,255,.95),5px 7px 16px rgba(104,92,66,.26)",
        "press": "inset 3px 3px 7px rgba(104,92,66,.20),inset -3px -3px 7px rgba(255,255,255,.85)",
        "press-act": "inset 2px 2px 5px rgba(60,80,0,.35),inset -2px -2px 5px rgba(255,255,255,.4)",
        "fog": ("#FFFFFF", .84), "bdf": "blur(22px) saturate(1.7)"},
}

# The field behind the glass, per theme: pools of Archie's colours, fixed to the window so the glass always has
# something to frost, static so a reader who asked for reduced motion has nothing to ask them to stop doing.
# Light: iris-light pools on the left and the bottom, lime ones at the top right (where the mascot stands)
# and the right, and a white bloom in the middle so the glass does not read green all over. Dark: a lime glow
# where the mascot stands, a fainter one opposite, and a breath of ceramic under the title -- nothing more.
# Each pool's peak alpha is the one `GLASS[...]["pools"]` names; the white bloom only lightens, so it is not a
# worst case and is not listed there.
WASH = {
    "dark": "radial-gradient(1000px 640px at 86% -12%,rgba(164,200,18,.085),transparent 66%),"
            "radial-gradient(800px 600px at 0% 100%,rgba(164,200,18,.04),transparent 70%),"
            "radial-gradient(900px 560px at 4% -6%,rgba(235,229,218,.035),transparent 70%)",
    "light": "radial-gradient(820px 620px at 88% -6%,rgba(164,200,18,.30),transparent 66%),"
             "radial-gradient(760px 600px at 6% 28%,rgba(220,245,94,.55),transparent 68%),"
             "radial-gradient(900px 700px at 62% 108%,rgba(220,245,94,.42),transparent 70%),"
             "radial-gradient(700px 520px at 100% 62%,rgba(164,200,18,.34),transparent 70%),"
             "radial-gradient(900px 700px at 30% 70%,rgba(255,255,255,.65),transparent 70%)",
}

# What the strengthened modes lift the secondary inks and the lines to, per theme. Text 7:1 and lines 3:1
# on the solid plane, which is what high contrast used to promise; `theme_test.py` measures them.
STRONG = {
    "dark": {"ink": "#FFFFFF", "ink2": "#F2EEE6", "muted": "#E0DBD2", "grid": "#8FA83A", "link": "#E8FA8A",
             "edge": "#8FA83A", "ctl-edge": "#C9C4BB"},
    "light": {"ink": "#000000", "ink2": "#1C1B1B", "muted": "#2E2C29", "grid": "#7E776B", "link": "#2C4500",
              "edge": "#7E776B", "ctl-edge": "#56524C"},
}


def _rgba(colour: str, alpha: float) -> str:
    h = colour.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha:g})"


def _tokens(theme: str) -> str:
    g = GLASS[theme]
    glass = {"panel": _rgba(*g["panel"]), "panel-hi": _rgba(*g["panel-hi"]), "fog": _rgba(*g["fog"]),
             "bdf": g["bdf"]}
    glass |= {k: g[k] for k in ("edge", "ctl-edge", "raise", "raise-sm", "raise-hi", "press", "press-act")}
    return ("".join(f"--{k}:{v};" for k, v in PALETTE[theme].items())
            + "".join(f"--{k}:{v};" for k, v in glass.items()) + f"--wash:{WASH[theme]};")


def _strong(theme: str) -> str:
    return "".join(f"--{k}:{v};" for k, v in STRONG[theme].items())


# The glass switched off: an opaque panel, no blur, no field. Shared by the three modes that ask for it.
_SOLID = "--panel:var(--plane);--panel-hi:var(--plane);--bdf:none;--wash:none;"
_FLAT = "--raise:none;--raise-sm:none;--raise-hi:none;--press:none;--press-act:none;"

THEME_CSS = (
    "/* THE THEMES. Written by `THEME_CSS` in scripts/sitewide.py, which explains every value; do not edit the\n"
    "   copy in a generated file. Dark is on `:root`, so it needs no attribute to be true -- it is the floor a\n"
    "   reader with JavaScript off gets. */\n"
    ":root{color-scheme:dark;" + _tokens("dark")
    # The structural half: one typeface, the same in both themes.
    + '--ui:"Geist","Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;'
    '--mono:"Geist Mono",ui-monospace,"Cascadia Mono",Consolas,"Liberation Mono",monospace}\n'
    "html[data-theme=light]{color-scheme:light;" + _tokens("light") + "}\n"
    # ARCHIE'S FOG PRANK: every pane frosts over. After the themes, so it wins over both at the same weight,
    # and before the strengthened modes below, so a reader who asked for solid panels never sees it.
    "html[data-fog]{--panel:var(--fog);--panel-hi:var(--fog);--bdf:blur(34px) saturate(.6)}\n"
    # THE GLASS SWITCHED OFF, for the readers and browsers that need it. Each block restates both themes'
    # selectors, `:root` and `html[data-theme]`, so it outranks the theme block above by coming after it at
    # the same weight. A browser with no backdrop filter would show the translucent fill over the page with
    # nothing frosting it, so it gets the opaque panel too.
    "@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){"
    ":root,html[data-theme]{--panel:var(--plane);--panel-hi:var(--plane);--bdf:none}}\n"
    "@media (prefers-reduced-transparency:reduce){:root,html[data-theme]{" + _SOLID + "--edge:var(--grid)}}\n"
    "@media (prefers-contrast:more){:root{" + _SOLID + _FLAT + _strong("dark") + "}"
    "html[data-theme=light]{" + _SOLID + _FLAT + _strong("light") + "}}\n"
    "@media (forced-colors:active){:root,html[data-theme]{" + _SOLID + _FLAT + "}}\n"
    + r"""/* Paint only, below this line: no rule here may size or place a box (see the note in sitewide.py). */
/* THE FIELD, on every page family: fixed to the window and behind everything, so the glass always has it
   to frost and it never scrolls out from under a panel. A pseudo-element of <body> at z-index -1 paints
   over the canvas (which wears the body's --surface) and under every box on the page. */
body::before{content:"";position:fixed;inset:0;z-index:-1;background:var(--wash);pointer-events:none}
/* The focus ring, for every page family: the accent, 2px, clear of the control so it never sits on the
   control's own border or its shadows. `:focus-visible` so a click does not leave a ring on the chip that
   was pressed. */
:focus-visible{outline:2px solid var(--bar);outline-offset:2px;border-radius:4px}
::selection{background:color-mix(in srgb,var(--act) 42%,transparent);color:var(--ink)}
/* THE CONTROLS, on every page family: extruded pills, pushed in while pressed. `html` in front so these
   outrank each family's own `.chip{...}`, which sets the fill and border these leave alone. A pressed chip
   is the lime, pushed in: the fill says "on" and the inset says "held down", two cues rather than one. */
html .chip{box-shadow:var(--raise-sm);border-color:var(--ctl-edge)}
html .chip:hover{box-shadow:var(--raise-hi)}
html .chip:active{box-shadow:var(--press)}
html .chip[aria-pressed=true]{box-shadow:var(--press-act)}
/* The primary button, on every page family that has one: the lime fill, its edge, and the extrusion. An
   inset shadow is the edge rather than a border, so the box is the size it always was. */
html .cta{border-radius:999px;box-shadow:inset 0 0 0 1px var(--act-edge),inset 0 1px 0 rgba(255,255,255,.3),
  var(--raise-sm)}
.cta:hover{background:var(--act-hi);filter:none}
html .cta:active{box-shadow:inset 0 0 0 1px var(--act-edge),var(--press-act)}
/* Titles, in the lime in dark. Page headings only: a heading inside a poster's artwork (`.ph`) sits on a
   fixed dark stage of its own and keeps its own ink. Zero weight (`:where`), so any heading a page family
   has already given a colour of its own keeps it; this only dresses the ones that inherit the ink. */
:where(h1,h2):where(:not(.ph *)){color:var(--title)}
/* MORE CONTRAST: the things that are not colours. Links are underlined, so a link is not told from text by
   its hue alone (WCAG 1.4.1) -- except the ones drawn as a pill or a button, whose shape already says "press
   me". A 3px ring with a halo of the page's own colour, a pressed control outlined as well as filled, and
   nothing drawn behind text. */
@media (prefers-contrast:more){
  a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em}
  a:hover{text-decoration-thickness:2px}
  :is(.chip,.cta,.bychip,.btag,.stamp,.ghstar){text-decoration:none}
  :focus-visible{outline:3px solid var(--bar);outline-offset:2px;box-shadow:0 0 0 7px var(--surface)}
  [aria-pressed=true]{outline:2px solid var(--ink);outline-offset:1px}
  *{text-shadow:none!important}
  ::selection{background:var(--bar);color:var(--onbar)}
  .mhart{background:none!important}
}
/* FORCED COLOURS (Windows High Contrast and its kin). The system palette replaces every colour and drops
   every shadow, which is the point, and three things would go with it: the state of a pressed control, the
   edge of a button whose only edge was its fill, and the theme swatches, which are previews and mean nothing
   in system colours. Outlines rather than borders, so nothing grows. */
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
# page. Its value is `--plane`, the header's own opaque stand-in, and it is a literal because no stylesheet has
# parsed yet when this runs; with JavaScript off it stays dark's, which agrees with the `data-theme="dark"`
# floor on <html>. After paint the page scripts re-derive it from the computed value (`THEME_JS`).
#
# Precedence is the reader's choice, then the operating system, then dark. A stored value that is not one of
# the two themes is not honoured -- `theme` is reader-writable storage that outlives the release that wrote
# it. THE MIGRATIONS. The old site had eight colour "skins" on a second axis, `atlas-skin`, and every one of
# them had a light and a dark half; the half a reader was wearing is already in `theme`, so the skin key and
# `atlas-unlock` (which only ever unlocked the hidden ninth skin) are removed and nothing is mapped. And the
# third theme, High contrast, is rewritten to "dark", the half it was -- once, here, so every page family's
# script after this one sees a theme it knows. Its accessibility is not lost with it: the stylesheet's
# `prefers-contrast` rules apply in either theme.
_PLANES = ", ".join(f'{t}: "{PALETTE[t]["plane"]}"' for t in THEMES)
HEAD_THEME = f"""<meta name="theme-color" id="tc" content="{PALETTE['dark']['plane']}">
<script>
try {{
  var t = localStorage.getItem("theme");
  if (localStorage.getItem("atlas-skin") !== null || localStorage.getItem("atlas-unlock") !== null) {{
    localStorage.removeItem("atlas-skin"); localStorage.removeItem("atlas-unlock");
  }}
  if (t === "contrast") localStorage.setItem("theme", t = "dark");
  if (t !== "light" && t !== "dark")
    t = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  document.documentElement.dataset.theme = t;
  document.getElementById("tc").content = {{{_PLANES}}}[t];
}} catch (e) {{}}
</script>
"""

# The same resolution, for scripts that run after paint: the Settings menu, the light/dark toggle on the facet
# and project pages, and the OS-preference listener. A string, so each page family inlines it beside its own
# controls without a second request.
#   atlasTheme().choice()  -> "system" | "light" | "dark"   (what the reader picked)
#   atlasTheme().set(c)    -> stores the choice (removing it for "system"), applies it, repaints the chrome
#   atlasTheme().follow(f) -> calls f() after the OS preference changes, for a reader on "system"
#   atlasTheme().refresh() -> re-reads the stored choice and applies it (another tab changed it)
# A function declaration, memoised, rather than a `var` holding an IIFE, and that is load-bearing: the
# catalogue's page script calls `wireSettings()` from `wire()` hundreds of lines *above* where this is
# inlined, and a function declaration is hoisted with its body where a `var` is hoisted as `undefined`. The
# first call also re-applies the stored choice and repeats the head script's migration, which is what catches
# up a page whose head script is a release older than this one: the project pages are rewritten by the daily
# build, and until then theirs still knows "contrast".
THEME_JS = r"""function atlasTheme() {
  if (atlasTheme.api) return atlasTheme.api;
  var root = document.documentElement;
  var stored = function () { try { return localStorage.getItem("theme"); } catch (e) { return null; } };
  var valid = function (t) { return t === "light" || t === "dark"; };
  var system = function () {
    try { return matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"; } catch (e) { return "dark"; }
  };
  var apply = function () {
    var t = stored();
    if (t === "contrast") { try { localStorage.setItem("theme", t = "dark"); } catch (e) {} }
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
      try { matchMedia("(prefers-color-scheme: light)").addEventListener("change", on); } catch (e) {}
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
